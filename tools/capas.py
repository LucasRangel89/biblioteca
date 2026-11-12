#!/usr/bin/env python3
"""Procura a capa de cada livro do Catálogo Mestre e guarda o resultado em catalogo/capas.tsv.

    python tools/capas.py                 # procura o que falta: livros novos (nas duas fontes) e, dos já procurados
                                          # só na Open Library, os que ainda não passaram pela Apple
    python tools/capas.py --limite 200    # no máximo 200 livros nesta execução
    python tools/capas.py --minutos 50    # para de procurar depois de 50 minutos (o resto fica para a próxima vez)
    python tools/capas.py --refazer       # procura de novo, nas duas fontes, as que não foram achadas
    python tools/capas.py --conferir      # só conta o que falta; não consulta nem grava
    python tools/capas.py --arrumar       # não consulta: põe o arquivo na ordem do catálogo e tira capas repetidas
    python tools/capas.py --testar 40     # pede 40 das capas guardadas de cada fonte e confere se abrem como imagem
    python tools/capas.py --auditar       # o retrato das capas e a fila de revisão (tools/auditar_capas.py; sem internet)

Precisa de internet (menos --conferir, --arrumar e --auditar). No GitHub, quem roda é .github/workflows/buscar-capas.yml.

As fontes, nesta ordem:
  1. Open Library (openlibrary.org), um catálogo aberto de livros. Tem poucas edições brasileiras.
  2. Apple Books (a busca pública do iTunes, itunes.apple.com/search, na loja do Brasil): os livros digitais à venda
     aqui, quase todos com a capa da edição brasileira. Só é consultada para o que a Open Library não achou, e
     devagar — a busca aceita cerca de 20 consultas por minuto.

O arquivo catalogo/capas.tsv tem uma linha por livro: título, autor, capa e origem.
  capa    número da capa na Open Library (a imagem é https://covers.openlibrary.org/b/id/NÚMERO-M.jpg),
          ou o endereço completo de uma imagem (https://…): o da Apple, ou um posto à mão; vazio = sem capa
  origem  edicao       Open Library: capa da edição com o mesmo título do catálogo (em geral a brasileira ou portuguesa)
          obra         Open Library: capa da obra — pode ser a de uma edição em outra língua
          apple        Apple Books: capa do livro digital com o mesmo título e o mesmo autor
          manual       escolhida à mão: nunca é trocada por este script
          nao-achei    procurada só na Open Library, sem resultado: falta a Apple (a próxima execução procura)
          nao-achei-2  procurada nas duas fontes, sem resultado
          sem-autor    não procurada: sem autor certo (ou com "Vários autores") o resultado não seria confiável

Nenhuma imagem é guardada no repositório: o painel mostra a capa direto da fonte.
Para corrigir uma capa errada: troque o número (ou ponha o endereço de uma imagem) e escreva `manual` na origem.
"""
import concurrent.futures, csv, io, json, pathlib, re, sys, threading, time, unicodedata, urllib.error, urllib.parse, urllib.request

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from parse_catalog import SRC as CATALOGO, parse          # noqa: E402

CAPAS = RAIZ / 'catalogo' / 'capas.tsv'
COLUNAS = ['titulo', 'autor', 'capa', 'origem']
ORIGENS = {'edicao', 'obra', 'apple', 'manual', 'nao-achei', 'nao-achei-2', 'sem-autor'}
SEM_CAPA = {'nao-achei', 'nao-achei-2', 'sem-autor'}                  # origens de quem foi procurado (ou nem isso) e ficou sem capa
BUSCA = 'https://openlibrary.org/search.json'
APPLE = 'https://itunes.apple.com/search'
PAUSA_APPLE = 3.1                                                     # segundos entre consultas: a busca aceita ~20 por minuto
TAMANHO_APPLE = '200x300bb.jpg'                                       # a imagem pedida: cabe em 200 × 300 (perto do tamanho M da Open Library)
IMAGEM_APPLE = re.compile(r'^https://is\d+-ssl\.mzstatic\.com/image/thumb/[\w./%+-]+/\d+x\d+bb\.(?:jpg|jpeg|png)$', re.ASCII)
OUTRO_PRODUTO = {'box', 'trilogia', 'tetralogia', 'colecao', 'coletanea', 'resumo', 'resumido', 'summary', 'guia', 'workbook', 'audiolivro', 'audiobook'}
CAMPOS = 'key,title,author_name,cover_i,editions,editions.title,editions.cover_i,editions.language'
AGENTE = 'biblioteca-lucas/1.0 (https://github.com/LucasRangel89/biblioteca; catalogo pessoal de livros)'
SEM_AUTOR = {'', 'autor nao informado', 'varios autores', 'varios', 'anonimo', 'tradicao hindu', 'tradicao budista', 'tradicao tibetana'}
ARTIGOS = {'o', 'a', 'os', 'as', 'um', 'uma', 'the', 'el', 'la', 'le', 'les', 'il', 'der', 'die', 'das'}
FORA_DO_NOME = {'jr', 'junior', 'filho', 'neto', 'org', 'orgs', 'outros', 'e'}


def chave(s):
    """Chave de comparação: sem acento, minúsculas, só letras e números (a mesma do importador)."""
    s = ''.join(c for c in unicodedata.normalize('NFD', s or '') if unicodedata.category(c) != 'Mn').lower().replace('&', ' e ')
    return ' '.join(re.sub(r'[^a-z0-9]+', ' ', s).split())


def sem_parenteses(t):
    return re.sub(r'\s*\([^)]*\)', '', t or '').strip()


def principal(t):
    """O título sem o subtítulo: o que vem antes de ":" , " - " ou " – "."""
    return re.split(r':| [-–—] ', sem_parenteses(t), maxsplit=1)[0].strip()


def nt(t):
    """Título para comparar: sem parênteses, sem acento e sem o artigo do começo ("O Nome da Rosa" = "Nome da Rosa")."""
    p = chave(sem_parenteses(t)).split()
    while len(p) > 1 and p[0] in ARTIGOS:
        p = p[1:]
    return ' '.join(p)


def adaptacao(titulo):
    """Livro adaptado para quadrinhos: o primeiro autor é o do livro original, e a capa do livro não serve."""
    return 'em quadrinhos' in chave(titulo)


def autores(autor):
    """Os autores de uma linha do catálogo, um a um: "A e B", "A, B e C", "Nome (org.)", "X e outros"."""
    a = re.sub(r'\([^)]*\)', ' ', autor or '')
    partes = [p.strip() for p in re.split(r',|;| e | & ', a) if p.strip()]
    return [p for p in partes if chave(p) not in ('outros', '')]


def sobrenome(autor, ultimo=False):
    """O sobrenome que vai na consulta: o do primeiro autor com nome completo (numa adaptação, o do último).
    '' quando não há autor que sirva. "Allan e Barbara Pease" → pease; "Ram V e Evan Cagle" → cagle; "Homero" → homero."""
    if chave(re.sub(r'\([^)]*\)', ' ', autor or '')) in SEM_AUTOR or chave(autor) in SEM_AUTOR:
        return ''
    nomes = [[x for x in chave(n).split() if x not in FORA_DO_NOME] for n in autores(autor)]
    if ultimo:
        nomes = nomes[::-1]
    for minimo in (2, 1):                                # primeiro quem tem nome e sobrenome; depois, nome único
        for p in nomes:
            if len(p) >= minimo and len(p[-1]) > 1:
                return p[-1]
    return ''


def titulo_confere(nosso, deles, hq=False):
    """O título achado é o do nosso livro? Igual; ou um dos dois tem subtítulo e o outro não. Num quadrinho, o nosso
    subtítulo não pode faltar do outro lado ("Batman: Ano Um" não é qualquer "Batman")."""
    a, b = nt(nosso), nt(deles)
    if not a or not b:
        return False
    if a == b:
        return True
    pa, pb = nt(principal(nosso)), nt(principal(deles))
    if pa == a and pb == a:                              # o nosso não tem subtítulo; o deles tem
        return True
    return not hq and pb == b and pa == b and len(b) >= 4      # o nosso tem subtítulo; o deles não


def consulta_de(titulo, autor):
    """A consulta à Open Library para um livro (título inteiro + sobrenome do autor), ou None quando não dá para
    procurar com segurança: sem autor, "Vários autores", ou adaptação em quadrinhos com um autor só (não se sabe se
    é o do livro original ou o da adaptação)."""
    adapt = adaptacao(titulo)
    if adapt and len(autores(autor)) < 2:
        return None
    nome = sobrenome(autor, ultimo=adapt)
    frase = re.sub(r'["\\]', ' ', sem_parenteses(titulo)).strip()
    if not nome or not frase:
        return None
    return {'q': f'title:"{frase}" author:{nome}', 'lang': 'pt', 'fields': CAMPOS, 'limit': '8'}


def consulta_so_titulo(titulo):
    """Segunda tentativa: só o título principal (sem subtítulo). O autor é conferido depois, nos nomes alternativos —
    lá o autor pode estar escrito de outro jeito (Tolstói · Tolstoy · Толстой) ou o subtítulo pode ser outro."""
    frase = re.sub(r'["\\]', ' ', principal(titulo)).strip()
    return {'q': f'title:"{frase}"', 'lang': 'pt', 'fields': CAMPOS + ',author_alternative_name', 'limit': '10'}


def autor_confere(nome, doc):
    """O sobrenome aparece entre os nomes (ou nomes alternativos) do autor do resultado?"""
    nomes = list(doc.get('author_name') or []) + list(doc.get('author_alternative_name') or [])
    return bool(nome) and nome in set(chave(' '.join(nomes)).split())


def escolher(titulo, docs, hq=False):
    """(número da capa, origem) entre os resultados da busca; (None, 'nao-achei') se nenhum serve.
    Preferência: capa de edição em português com o nosso título; capa de outra edição com o nosso título; capa da obra."""
    melhor = None
    for pos, d in enumerate(docs or []):
        eds = ((d.get('editions') or {}).get('docs') or [])
        ed = eds[0] if eds else None
        capa_obra = d.get('cover_i') if isinstance(d.get('cover_i'), int) and d.get('cover_i') > 0 else None
        cands = []
        if ed and titulo_confere(titulo, ed.get('title', ''), hq):
            capa_ed = ed.get('cover_i') if isinstance(ed.get('cover_i'), int) and ed.get('cover_i') > 0 else None
            if capa_ed:
                cands.append((0 if 'por' in (ed.get('language') or []) else 1, pos, capa_ed, 'edicao'))
            elif capa_obra:
                cands.append((2, pos, capa_obra, 'obra'))
        elif capa_obra and titulo_confere(titulo, d.get('title', ''), hq):
            cands.append((2, pos, capa_obra, 'obra'))
        for c in cands:
            if melhor is None or c[:2] < melhor[:2]:
                melhor = c
    return (melhor[2], melhor[3]) if melhor else (None, 'nao-achei')


class Limite:
    """No máximo uma consulta a cada `pausa` segundos, somando todas as linhas de execução."""
    def __init__(self, pausa):
        self.pausa, self.proxima, self.trava = pausa, 0.0, threading.Lock()

    def espera(self):
        with self.trava:
            agora = time.monotonic()
            quando = max(agora, self.proxima)
            self.proxima = quando + self.pausa
        if quando > agora:
            time.sleep(quando - agora)


def buscar_json(params, limite, tentativas=4):
    url = BUSCA + '?' + urllib.parse.urlencode(params)
    for n in range(tentativas):
        limite.espera()
        try:
            req = urllib.request.Request(url, headers={'User-Agent': AGENTE, 'Accept': 'application/json'})
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.loads(r.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            if e.code not in (429, 500, 502, 503, 504) or n == tentativas - 1:
                raise
        except (urllib.error.URLError, TimeoutError, ConnectionError, json.JSONDecodeError):
            if n == tentativas - 1:
                raise
        time.sleep(3 * (n + 1) ** 2)
    raise RuntimeError('sem resposta')


def procurar(titulo, autor, hq, limite, buscar=buscar_json):
    """(capa, origem) de um livro. Levanta exceção se a consulta falhar (o livro fica para a próxima execução)."""
    params = consulta_de(titulo, autor)
    if params is None:
        return '', 'sem-autor'
    capa, origem = escolher(titulo, (buscar(params, limite) or {}).get('docs'), hq)
    if not capa:
        nome = sobrenome(autor, ultimo=adaptacao(titulo))
        docs = (buscar(consulta_so_titulo(titulo), limite) or {}).get('docs') or []
        capa, origem = escolher(titulo, [d for d in docs if autor_confere(nome, d)], hq)
    return (str(capa) if capa else ''), origem


# ───────── a segunda fonte: Apple Books (busca do iTunes) ─────────

def som(s):
    """Nome para comparar entre grafias do mesmo autor: Tolstói · Tolstoy, Dostoiévski · Dostoyevsky."""
    return chave(s).replace('y', 'i')


def consulta_apple(titulo, autor):
    """A consulta à busca do iTunes para um livro: o título principal e o sobrenome do autor, entre os livros digitais
    da loja brasileira. None quando não dá para procurar com segurança — os mesmos casos da Open Library."""
    adapt = adaptacao(titulo)
    if adapt and len(autores(autor)) < 2:
        return None
    nome = sobrenome(autor, ultimo=adapt)
    frase = ' '.join(re.sub(r'["\\]', ' ', principal(titulo)).split())
    if not nome or not frase:
        return None
    return {'term': f'{frase} {nome}', 'country': 'br', 'media': 'ebook', 'limit': '25'}


def imagem_apple(r):
    """O endereço da capa de um resultado, no tamanho que o painel usa; '' se não tiver a forma dos endereços de
    imagem da Apple (nada de outro tipo entra no capas.tsv por este caminho)."""
    u = str(r.get('artworkUrl100') or r.get('artworkUrl60') or '').strip()
    return u.rsplit('/', 1)[0] + '/' + TAMANHO_APPLE if IMAGEM_APPLE.match(u) else ''


def escolher_apple(titulo, nome, resultados, hq=False):
    """O endereço da capa entre os resultados da busca do iTunes, ou ''. Serve o livro digital com o nosso título
    (igual, ou com subtítulo de um lado só) cujo autor tem o nosso sobrenome. Título igual ganha de título com
    subtítulo; no empate, fica o que veio antes. Caixa, trilogia, resumo ou guia do livro não servem."""
    alvo, nosso, melhor = nt(titulo), set(chave(titulo).split()), None
    for pos, r in enumerate(resultados or []):
        if not isinstance(r, dict) or r.get('kind', 'ebook') != 'ebook':
            continue
        deles, capa = str(r.get('trackName') or ''), imagem_apple(r)
        if not capa or not titulo_confere(titulo, deles, hq):
            continue
        if not nome or som(nome) not in set(som(str(r.get('artistName') or '')).split()):
            continue
        if (set(chave(deles).split()) - nosso) & OUTRO_PRODUTO:
            continue
        cand = (0 if nt(deles) == alvo else 1, pos, capa)
        if melhor is None or cand[:2] < melhor[:2]:
            melhor = cand
    return melhor[2] if melhor else ''


def buscar_apple(params, limite, tentativas=3, dormir=time.sleep):
    """A resposta da busca do iTunes. Quando ela recusa por excesso de consultas (403 ou 429), espera um minuto ou
    dois antes de tentar de novo."""
    url = APPLE + '?' + urllib.parse.urlencode(params)
    for n in range(tentativas):
        limite.espera()
        try:
            req = urllib.request.Request(url, headers={'User-Agent': AGENTE, 'Accept': 'application/json'})
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.loads(r.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            if e.code not in (403, 429, 500, 502, 503, 504) or n == tentativas - 1:
                raise
            dormir(60 * (n + 1) if e.code in (403, 429) else 3 * (n + 1) ** 2)
        except (urllib.error.URLError, TimeoutError, ConnectionError, json.JSONDecodeError):
            if n == tentativas - 1:
                raise
            dormir(3 * (n + 1) ** 2)
    raise RuntimeError('sem resposta')


def procurar_apple(titulo, autor, hq, limite, buscar=buscar_apple):
    """(endereço da capa, 'apple') ou ('', 'nao-achei-2'). Levanta exceção se a consulta falhar (o livro continua
    como estava, e a próxima execução tenta de novo)."""
    params = consulta_apple(titulo, autor)
    if params is None:
        return '', 'nao-achei-2'
    nome = sobrenome(autor, ultimo=adaptacao(titulo))
    capa = escolher_apple(titulo, nome, (buscar(params, limite) or {}).get('results'), hq)
    return (capa, 'apple') if capa else ('', 'nao-achei-2')


def ler_capas(caminho=None):
    """{(chave do título, chave do autor): linha} do capas.tsv."""
    caminho = pathlib.Path(caminho or CAPAS)
    if not caminho.exists():
        return {}
    out = {}
    for r in csv.DictReader(io.StringIO(caminho.read_text(encoding='utf-8-sig'), newline=''), delimiter='\t'):
        r = {c: (r.get(c) or '').strip() for c in COLUNAS}
        if r['titulo']:
            out[(chave(r['titulo']), chave(r['autor']))] = r
    return out


def texto_capas(livros, capas):
    """O capas.tsv na ordem do catálogo. Linha cujo livro saiu do catálogo só fica se foi posta à mão."""
    s = io.StringIO(newline='')
    w = csv.writer(s, delimiter='\t', lineterminator='\n', quoting=csv.QUOTE_MINIMAL)
    w.writerow(COLUNAS)
    vistos = set()
    for b in livros:
        k = (chave(b['t']), chave(b['a']))
        if k in capas and k not in vistos:
            vistos.add(k)
            w.writerow([b['t'], b['a'], capas[k]['capa'], capas[k]['origem']])
    for k, r in capas.items():
        if k not in vistos and r['origem'] == 'manual':
            w.writerow([r[c] for c in COLUNAS])
    return s.getvalue()


def sem_repetidas(capas):
    """Uma capa não serve a dois livros. Quando a busca dá a mesma capa a mais de uma linha, é sinal de série: a edição
    achada tem só o título principal ("Transurfing") e casou com cada volume ("Transurfing: Maçãs Caem ao Céu").
    A capa fica nas linhas sem subtítulo e sai das que têm, que voltam a "não achei" — "nao-achei" se a capa era da
    Open Library (a Apple ainda pode ter a certa), "nao-achei-2" se era da Apple. Capas postas à mão não entram na
    conta. Devolve quantas capas saíram."""
    por_capa = {}
    for k, r in capas.items():
        if r['capa'] and r['origem'] != 'manual':
            por_capa.setdefault(r['capa'], []).append(k)
    tiradas = 0
    for ks in por_capa.values():
        if len(ks) < 2:
            continue
        for k in ks:
            r = capas[k]
            if nt(principal(r['titulo'])) != nt(r['titulo']):
                r['capa'], r['origem'] = '', ('nao-achei-2' if r['origem'] == 'apple' else 'nao-achei')
                tiradas += 1
    return tiradas


def para_o_painel(livros, capas=None):
    """Uma posição por livro do catálogo, na mesma ordem: o número da capa na Open Library, o endereço de uma imagem
    posta à mão, ou 0 quando não há capa. É o que vai embutido no painel (src/capas.json)."""
    capas = ler_capas() if capas is None else capas
    out = []
    for b in livros:
        c = (capas.get((chave(b['t']), chave(b['a']))) or {}).get('capa', '').strip()
        out.append(int(c) if c.isdigit() and int(c) > 0 else c if c.lower().startswith('https://') and not re.search(r'[\s"<>\\]', c) else 0)
    return out


def endereco(capa, tamanho='M'):
    """O endereço da imagem: número da Open Library ou, se posto à mão, o endereço completo."""
    capa = (capa or '').strip()
    if capa.isdigit():
        return f'https://covers.openlibrary.org/b/id/{capa}-{tamanho}.jpg'
    return capa if capa.lower().startswith('https://') else ''


IMAGEM = (b'\xff\xd8\xff', b'\x89PNG\r\n\x1a\n', b'GIF8', b'RIFF')      # começo de um arquivo JPEG, PNG, GIF ou WebP
INEXISTENTE = '999999999'                                                  # número que nenhuma capa tem


def abrir_imagem(url):
    """(código da resposta, tipo do conteúdo, primeiros bytes) de um endereço de imagem; código 0 se a rede falhar."""
    req = urllib.request.Request(url, headers={'User-Agent': AGENTE, 'Accept': 'image/*'})
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            return r.status, r.headers.get('Content-Type', ''), r.read(4096)
    except urllib.error.HTTPError as e:
        return e.code, '', b''
    except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
        return 0, type(e).__name__, b''


def testar(capas, quantas=40, abrir=abrir_imagem, pausa=0.3):
    """Confere, por amostragem, se as capas guardadas abrem: pede `quantas` delas (espalhadas pelo arquivo) no mesmo
    endereço que o painel usa e vê se a resposta é mesmo uma imagem — e não o quadradinho em branco que a Open Library
    manda quando não tem a capa. Pede também uma capa que não existe: a resposta tem de ser "não encontrada" (404),
    porque é com isso que o painel conta para desenhar a inicial do título no lugar da imagem.
    Devolve (quantas abriram, quantas foram pedidas, as que não abriram, a inexistente deu 404?)."""
    numeros = [r['capa'] for r in capas.values() if r['capa'].isdigit()]
    quantas = max(0, min(quantas, len(numeros)))
    amostra = [numeros[i * len(numeros) // quantas] for i in range(quantas)]
    ruins = []
    for n in amostra:
        codigo, tipo, comeco = abrir(endereco(n) + '?default=false')
        if not (codigo == 200 and comeco.startswith(IMAGEM) and len(comeco) >= 1000):
            ruins.append((n, codigo, tipo if codigo != 200 else f'{tipo}, {len(comeco)} bytes'))
        if pausa:
            time.sleep(pausa)
    codigo, _, _ = abrir(endereco(INEXISTENTE) + '?default=false')
    return len(amostra) - len(ruins), len(amostra), ruins, codigo == 404


def testar_apple(capas, quantas=40, abrir=abrir_imagem, pausa=0.3):
    """A mesma conferência para as capas que vieram da Apple: pede `quantas` delas (espalhadas pelo arquivo), no
    endereço guardado, que é o que o painel usa. Devolve (quantas abriram, quantas foram pedidas, as que não abriram)."""
    enderecos = [r['capa'] for r in capas.values() if r['origem'] == 'apple' and r['capa']]
    quantas = max(0, min(quantas, len(enderecos)))
    amostra = [enderecos[i * len(enderecos) // quantas] for i in range(quantas)]
    ruins = []
    for u in amostra:
        codigo, tipo, comeco = abrir(u)
        if not (codigo == 200 and comeco.startswith(IMAGEM) and len(comeco) >= 1000):
            ruins.append((u, codigo, tipo if codigo != 200 else f'{tipo}, {len(comeco)} bytes'))
        if pausa:
            time.sleep(pausa)
    return len(amostra) - len(ruins), len(amostra), ruins


def main(argv):
    def valor(nome, padrao, tipo=float):
        return tipo(argv[argv.index(nome) + 1]) if nome in argv else padrao
    limite_n = valor('--limite', None, int)
    pausa, pausa_apple = valor('--pausa', 0.4), valor('--pausa-apple', PAUSA_APPLE)
    prazo = time.time() + 60 * valor('--minutos', 0) if '--minutos' in argv else None
    conferir, refazer, arrumar = '--conferir' in argv, '--refazer' in argv, '--arrumar' in argv
    for saida in (sys.stdout, sys.stderr):
        try: saida.reconfigure(encoding='utf-8', errors='replace')
        except Exception: pass
    if '--auditar' in argv:                                             # o retrato e a fila de revisão: script só de leitura
        import auditar_capas
        return auditar_capas.main([a for a in argv if a != '--auditar'])
    livros = parse(pathlib.Path(CATALOGO).read_text(encoding='utf-8'))
    capas = ler_capas()
    # o que falta, livro a livro: 'tudo' = as duas fontes, em ordem; 'apple' = já passou pela Open Library, falta a Apple
    falta = {}
    for b in livros:
        k = (chave(b['t']), chave(b['a']))
        r = capas.get(k)
        if r is None or (refazer and r['origem'] in ('nao-achei', 'nao-achei-2')):
            falta.setdefault(k, (b, 'tudo'))
        elif r['origem'] == 'nao-achei':
            falta.setdefault(k, (b, 'apple'))
    falta = [(k, b, modo) for k, (b, modo) in falta.items()]
    so_apple = sum(1 for _, _, modo in falta if modo == 'apple')
    print(f'Catálogo: {len(livros)} livros · {sum(1 for r in capas.values() if r["capa"])} com capa · {len(falta)} a procurar'
          + (f' ({so_apple} só na Apple: já passaram pela Open Library)' if so_apple else ''))
    if conferir:
        return 0
    if '--testar' in argv:
        i = argv.index('--testar')
        quantas = int(argv[i + 1]) if i + 1 < len(argv) and argv[i + 1].isdigit() else 40
        espera = pausa if '--pausa' in argv else 0.3
        boas, pedidas, ruins, falta_ok = testar(capas, quantas, abrir_imagem, espera)
        print(f'Amostra das capas: {boas} de {pedidas} abriram como imagem · capa que não existe responde "não encontrada": {"sim" if falta_ok else "NÃO"}')
        for n, codigo, tipo in ruins[:10]:
            print(f'   não abriu: capa {n} — resposta {codigo or "nenhuma"} {tipo}'.rstrip())
        passou = bool(pedidas and boas >= 0.9 * pedidas and falta_ok)
        boas, pedidas, ruins = testar_apple(capas, quantas, abrir_imagem, espera)
        if pedidas:
            print(f'Amostra das capas da Apple: {boas} de {pedidas} abriram como imagem')
            for u, codigo, tipo in ruins[:10]:
                print(f'   não abriu: {u} — resposta {codigo or "nenhuma"} {tipo}'.rstrip())
            passou = passou and boas >= 0.9 * pedidas
        return 0 if passou else 1
    if arrumar:
        tiradas = sem_repetidas(capas)
        with open(CAPAS, 'w', encoding='utf-8', newline='\n') as f:
            f.write(texto_capas(livros, capas))
        print(f'Arquivo arrumado: {tiradas} capa(s) repetida(s) retirada(s).')
        return 0
    if limite_n is not None:
        falta = falta[:limite_n]
    lim, lim_apple, feitos, adiados, falhas, t0 = Limite(pausa), Limite(pausa_apple), 0, 0, [], time.time()

    estado = {'desistiu': False, 'tentados': 0, 'falhos': 0, 'apple_fora': False, 'apple_seguidas': 0}
    trava = threading.Lock()

    def um(item):
        """(chave, livro, resultado a gravar ou None, erro). erro '' = não foi tentado (fica para a próxima execução)."""
        k, b, modo = item
        if estado['desistiu'] or (prazo and time.time() > prazo):
            return k, b, None, ''                                       # acabou o tempo (ou a rede não responde): fica para a próxima execução
        hq, res = 'HQ' in b['tags'], ('', 'nao-achei')
        if modo == 'tudo':
            try:
                res, erro = procurar(b['t'], b['a'], hq, lim), None
            except Exception as e:                                      # rede fora, limite de consultas…
                res, erro = None, f'{type(e).__name__}: {e}'
            with trava:
                estado['tentados'] += 1
                estado['falhos'] += 1 if erro else 0
                if estado['tentados'] >= 30 and estado['falhos'] == estado['tentados'] and not estado['desistiu']:
                    estado['desistiu'] = True                           # nada responde: não adianta insistir
                    print('As 30 primeiras consultas falharam; parei de procurar.', flush=True)
            if erro:
                return k, b, None, erro
        if res[1] != 'nao-achei':
            return k, b, res, None                                      # achou na Open Library (ou não é livro que se procure)
        if estado['apple_fora']:                                        # a Apple parou de responder: o livro fica (ou continua) "nao-achei"
            return (k, b, res, None) if modo == 'tudo' else (k, b, None, '')
        try:
            achado = procurar_apple(b['t'], b['a'], hq, lim_apple)
        except Exception as e:
            with trava:
                estado['apple_seguidas'] += 1
                if estado['apple_seguidas'] >= 5 and not estado['apple_fora']:
                    estado['apple_fora'] = True
                    print('A Apple não respondeu a 5 consultas seguidas; parei de procurar nela.', flush=True)
            return k, b, (res if modo == 'tudo' else None), f'Apple: {type(e).__name__}: {e}'
        with trava:
            estado['apple_seguidas'] = 0
        return k, b, achado, None

    def gravar():
        with open(CAPAS, 'w', encoding='utf-8', newline='\n') as f:
            f.write(texto_capas(livros, capas))

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
        for k, b, res, erro in ex.map(um, falta):
            feitos += 1
            if erro == '':
                adiados += 1
            elif erro:
                falhas.append((b['t'], erro))
            if res is not None:
                capas[k] = {'titulo': b['t'], 'autor': b['a'], 'capa': res[0], 'origem': res[1]}
            if feitos % 100 == 0 and not adiados:
                gravar()
                print(f'  {feitos}/{len(falta)} · {time.time() - t0:.0f}s · {sum(1 for r in capas.values() if r["capa"])} com capa · {len(falhas)} falha(s)', flush=True)
    tiradas = sem_repetidas(capas)
    gravar()
    if tiradas:
        print(f'{tiradas} capa(s) retirada(s): a mesma imagem tinha sido dada a mais de um livro (volumes de uma série).')
    cont = {}
    for r in capas.values():
        cont[r['origem']] = cont.get(r['origem'], 0) + 1
    motivo = 'a Open Library não respondeu' if estado['desistiu'] else 'a Apple não respondeu' if estado['apple_fora'] else 'acabou o tempo'
    print('Resultado: ' + ' · '.join(f'{n} {o}' for o, n in sorted(cont.items())) + f' · {len(falhas)} consulta(s) falharam'
          + (f' · {adiados} ficaram para a próxima execução ({motivo})' if adiados else ''))
    for t, e in falhas[:10]:
        print(f'   falhou: {t} — {e}')
    return 1 if estado['desistiu'] or estado['apple_fora'] else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
