#!/usr/bin/env python3
"""Procura a capa de cada livro do Catálogo Mestre e guarda o resultado em catalogo/capas.tsv.

    python tools/capas.py                 # procura o que falta: livros novos (nas três fontes) e, dos já procurados,
                                          # os que ainda não passaram pela Apple ou pelo Google
    python tools/capas.py --limite 200    # no máximo 200 livros nesta execução
    python tools/capas.py --minutos 50    # para de procurar depois de 50 minutos (o resto fica para a próxima vez)
    python tools/capas.py --refazer       # procura de novo, nas três fontes, as que não foram achadas
    python tools/capas.py --sem-google    # fica só nas duas primeiras fontes (se o Google Books estiver recusando)
    python tools/capas.py --conferir      # só conta o que falta; não consulta nem grava
    python tools/capas.py --arrumar       # não consulta: põe o arquivo na ordem do catálogo e tira capas repetidas
    python tools/capas.py --testar 40     # pede 40 das capas guardadas de cada fonte e confere se abrem como imagem
    python tools/capas.py --auditar       # o retrato das capas e a fila de revisão (tools/auditar_capas.py; sem internet)
    python tools/capas.py --candidatos "Dom Casmurro" --autor "Machado de Assis"
                                          # o que cada fonte devolve para um livro, para escolher à mão (não grava)
    python tools/capas.py --candidatos "Dom Casmurro" --isbn 9788525406958
                                          # o mesmo, procurando pelo ISBN da edição que está na sua mão
    python tools/capas.py --candidatos "Dom Casmurro" --autor "Machado de Assis" --arquivo
                                          # inclui o piloto gratuito do Internet Archive (só candidatos; não grava)
    python tools/capas.py --piloto 20     # pede até 20 livros sem capa ao Internet Archive; só mostra, não grava

Precisa de internet (menos --conferir, --arrumar e --auditar). No GitHub, quem roda é .github/workflows/buscar-capas.yml.

As fontes, nesta ordem:
  1. Open Library (openlibrary.org), um catálogo aberto de livros. Tem poucas edições brasileiras.
  2. Apple Books (a busca pública do iTunes, itunes.apple.com/search, na loja do Brasil): os livros digitais à venda
     aqui, quase todos com a capa da edição brasileira. Só é consultada para o que a Open Library não achou, e
     devagar — a busca aceita cerca de 20 consultas por minuto.
  3. Google Books (www.googleapis.com/books/v1/volumes), só para o que as duas primeiras não acharam e só entre
     livros em português. Também devagar, e desiste depois de cinco recusas seguidas. A chave de API é opcional:
     se GOOGLE_BOOKS_API_KEY estiver no ambiente, vai no cabeçalho X-Goog-Api-Key, nunca na URL nem no registro.

Quando catalogo/isbns.tsv traz um ISBN conferido para o livro, a Open Library e o Google procuram primeiro esse
número (a edição exata), e só depois tentam título/autor. O arquivo é opcional e começa vazio; nenhum ISBN é inferido
de outra edição. O Internet Archive é um piloto gratuito e só de leitura: --arquivo/--piloto mostram miniaturas de
itens para revisão humana; nunca entram no casamento automático nem no capas.tsv.

O arquivo catalogo/capas.tsv tem uma linha por livro: título, autor, capa e origem.
  capa    número da capa na Open Library (a imagem é https://covers.openlibrary.org/b/id/NÚMERO-M.jpg),
          ou o endereço completo de uma imagem (https://…): o da Apple, o do Google ou um posto à mão; vazio = sem capa
  origem  edicao       Open Library: capa da edição com o mesmo título do catálogo (em geral a brasileira ou portuguesa)
          obra         Open Library: capa da obra — pode ser a de uma edição em outra língua
          apple        Apple Books: capa do livro digital com o mesmo título e o mesmo autor
          google       Google Books: capa do livro em português com o mesmo título e o mesmo autor
          manual       escolhida à mão: nunca é trocada por este script
          nao-achei    procurada só na Open Library, sem resultado: faltam a Apple e o Google
          nao-achei-2  procurada na Open Library e na Apple, sem resultado: falta o Google
          nao-achei-3  procurada nas três fontes, sem resultado
          sem-autor    não procurada: sem autor certo (ou com "Vários autores") o resultado não seria confiável

Nenhuma imagem é guardada no repositório: o painel mostra a capa direto da fonte.
Para corrigir uma capa errada: troque o número (ou ponha o endereço de uma imagem) e escreva `manual` na origem.
Para escolher à mão vendo o que cada fonte tem: --candidatos (abaixo).
"""
import concurrent.futures, csv, io, json, os, pathlib, re, sys, threading, time, unicodedata, urllib.error, urllib.parse, urllib.request

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from parse_catalog import SRC as CATALOGO, parse          # noqa: E402

CAPAS = RAIZ / 'catalogo' / 'capas.tsv'
ISBNS = RAIZ / 'catalogo' / 'isbns.tsv'
COLUNAS = ['titulo', 'autor', 'capa', 'origem']
COLUNAS_ISBN = ['titulo', 'autor', 'isbn', 'fonte']
ORIGENS = {'edicao', 'obra', 'apple', 'google', 'manual', 'nao-achei', 'nao-achei-2', 'nao-achei-3', 'sem-autor'}
SEM_CAPA = {'nao-achei', 'nao-achei-2', 'nao-achei-3', 'sem-autor'}    # origens de quem foi procurado (ou nem isso) e ficou sem capa
NAO_ACHADAS = ('nao-achei', 'nao-achei-2', 'nao-achei-3')
PROXIMA = {'nao-achei': 'nao-achei-2', 'nao-achei-2': 'nao-achei-3', 'apple': 'nao-achei-2', 'google': 'nao-achei-3'}
BUSCA = 'https://openlibrary.org/search.json'
BUSCA_ISBN = 'https://openlibrary.org/api/books'
APPLE = 'https://itunes.apple.com/search'
GOOGLE = 'https://www.googleapis.com/books/v1/volumes'
ARQUIVO = 'https://archive.org/advancedsearch.php'
ARQUIVO_IMAGEM = 'https://archive.org/services/img/'
PAUSA_APPLE = 3.1                                                     # segundos entre consultas: a busca aceita ~20 por minuto
PAUSA_GOOGLE = 1.5                                                    # o Google Books sem chave é de graça, mas recusa quando se insiste
PAUSA_ISBN = 3.1                                                      # consulta por ISBN: devagar, como a Apple
PAUSA_ARQUIVO = 1.0                                                   # piloto do Internet Archive: uma consulta por segundo
TAMANHO_APPLE = '200x300bb.jpg'                                       # a imagem pedida: cabe em 200 × 300 (perto do tamanho M da Open Library)
IMAGEM_APPLE = re.compile(r'^https://is\d+-ssl\.mzstatic\.com/image/thumb/[\w./%+-]+/\d+x\d+bb\.(?:jpg|jpeg|png)$', re.ASCII)
IMAGEM_GOOGLE = re.compile(r'^https://books\.google\.[a-z]{2,3}(?:\.[a-z]{2})?/books/(?:content|pagedimg)\?[\w&=%.;:+-]+$', re.ASCII)
IMAGEM_OL = re.compile(r'^https://covers\.openlibrary\.org/b/id/(\d+)-[SML]\.jpg$')
IDENTIFICADOR_ARQUIVO = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_.-]{0,254}$')
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


VOLUME = re.compile(r'(?:\b(?:vol(?:ume)?|tomo|livro|book|parte|n[ºo°]?)\s*\.?\s*(\d{1,3})\b|#\s*(\d{1,3})\b)', re.I)


def volume_de(t):
    """O número do volume, quando o próprio título diz qual é ("A Saga de Elric, Livro 2", "Vol. 3", "Saga #4").
     None quando não diz. O que está entre parênteses não conta: ali o catálogo anota a série e o lugar do livro
     nela ("O Império Final (Mistborn, vol. 1)"), e o título do livro é único — a edição não precisa repetir o número."""
    m = VOLUME.search(sem_parenteses(t))
    return int(m.group(1) or m.group(2)) if m else None


def sem_volume(t):
    """O título sem a indicação de volume: "A Saga de Elric, Livro 2" → "A Saga de Elric"."""
    return VOLUME.sub(' ', sem_parenteses(t)).strip(' ,-–—:#')


def isbn_limpo(s):
    return re.sub(r'[^0-9Xx]', '', str(s or '')).upper()


def isbn_valido(s):
    """O ISBN fecha na conta de conferência? (13 dígitos: pesos 1 e 3; 10: pesos 10 a 1, com X valendo 10)."""
    c = isbn_limpo(s)
    if len(c) == 13 and c.isdigit():
        return sum((1 if i % 2 == 0 else 3) * int(d) for i, d in enumerate(c)) % 10 == 0
    if len(c) == 10 and re.fullmatch(r'\d{9}[\dX]', c):
        return sum((10 - i) * (10 if d == 'X' else int(d)) for i, d in enumerate(c)) % 11 == 0
    return False


def isbn_de(s):
    """O primeiro ISBN válido que aparecer num texto (uma anotação do catálogo, por exemplo); '' se não houver."""
    for m in re.finditer(r'\d[\d\- ]{8,16}[\dXx]', str(s or '')):
        c = isbn_limpo(m.group(0))
        if isbn_valido(c):
            return c
    return ''


def isbn13(isbn):
    """ISBN-10 → ISBN-13 (prefixo 978); ISBN-13 válido volta limpo. '' se não der para converter."""
    c = isbn_limpo(isbn)
    if len(c) == 13 and isbn_valido(c):
        return c
    if len(c) != 10 or not isbn_valido(c):
        return ''
    base = '978' + c[:9]
    return base + str((-sum((1 if i % 2 == 0 else 3) * int(d) for i, d in enumerate(base))) % 10)


def mesmo_isbn(a, b):
    """Dois ISBNs são da mesma edição? Compara pelo ISBN-13 (o 10 e o 13 do mesmo livro casam)."""
    x, y = isbn13(a), isbn13(b)
    return bool(x and y and x == y)


def ler_isbns(caminho=None):
    """{(chave do título, chave do autor): ISBN-13} do catalogo/isbns.tsv, arquivo opcional e conferido à mão.
    Levanta ValueError se o cabeçalho estiver errado, houver livro repetido, ISBN inválido ou fonte vazia.
    Nenhuma linha é inferida de outra edição: o arquivo começa vazio e só ganha o que o dono conferiu no exemplar."""
    caminho = pathlib.Path(caminho or ISBNS)
    if not caminho.exists():
        return {}
    leitor = csv.DictReader(io.StringIO(caminho.read_text(encoding='utf-8-sig'), newline=''), delimiter='\t')
    if leitor.fieldnames != COLUNAS_ISBN:
        raise ValueError(f'{caminho.name}: o cabeçalho deve ser exatamente: ' + '\t'.join(COLUNAS_ISBN))
    out = {}
    for n, r in enumerate(leitor, 2):
        if None in r or any(r.get(c) is None for c in COLUNAS_ISBN):
            raise ValueError(f'{caminho.name}, linha {n}: use exatamente as quatro colunas do cabeçalho, separadas por TAB')
        r = {c: (r.get(c) or '').strip() for c in COLUNAS_ISBN}
        if not any(r.values()):
            continue
        k = (chave(r['titulo']), chave(r['autor']))
        if not r['titulo'] or not r['fonte']:
            raise ValueError(f'{caminho.name}, linha {n}: título e fonte da conferência são obrigatórios')
        if k in out:
            raise ValueError(f'{caminho.name}, linha {n}: livro repetido ({r["titulo"]} — {r["autor"]})')
        if not isbn_valido(r['isbn']):
            raise ValueError(f'{caminho.name}, linha {n}: ISBN {r["isbn"]!r} não fecha na conta de conferência')
        out[k] = isbn13(r['isbn'])
    return out


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
    subtítulo não pode faltar do outro lado ("Batman: Ano Um" não é qualquer "Batman").
    O volume tem de ser o mesmo: "…, Livro 2" não casa com "…" nem com "…, Livro 1" — era assim que os volumes de uma
    série recebiam a capa do primeiro. "Livro 2" e "Vol. 2" são o mesmo volume."""
    if volume_de(nosso) != volume_de(deles):
        return False
    a, b = nt(sem_volume(nosso)), nt(sem_volume(deles))
    if not a or not b:
        return False
    if a == b:
        return True
    pa, pb = nt(principal(sem_volume(nosso))), nt(principal(sem_volume(deles)))
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


# ───────── a terceira fonte: Google Books ─────────

def consulta_google(titulo, autor):
    """A consulta ao Google Books: título principal e sobrenome do autor, só entre livros em português.
    None nos mesmos casos em que as outras fontes não procuram (sem autor certo, adaptação com um autor só)."""
    adapt = adaptacao(titulo)
    if adapt and len(autores(autor)) < 2:
        return None
    nome = sobrenome(autor, ultimo=adapt)
    frase = ' '.join(re.sub(r'["\\]', ' ', principal(titulo)).split())
    if not nome or not frase:
        return None
    return {'q': f'intitle:"{frase}" inauthor:"{nome}"', 'langRestrict': 'pt', 'printType': 'books', 'maxResults': '20', 'orderBy': 'relevance'}


def imagem_google(v):
    """O endereço da capa de um volume do Google Books, sempre em https e sem a ponta enrolada que a miniatura traz.
    '' quando não tem a forma dos endereços de imagem do Google (nada de outro tipo entra no capas.tsv por aqui)."""
    links = v.get('imageLinks') or {}
    u = str(links.get('thumbnail') or links.get('smallThumbnail') or '').strip()
    u = re.sub(r'^http://', 'https://', u).replace('&edge=curl', '').replace('edge=curl&', '')
    return u if IMAGEM_GOOGLE.match(u) else ''


def titulo_google(v):
    """Título e subtítulo de um volume, como o Google os guarda separados."""
    t, s = str(v.get('title') or '').strip(), str(v.get('subtitle') or '').strip()
    return f'{t}: {s}' if s else t


def escolher_google(titulo, nome, itens, hq=False, isbn=''):
    """O endereço da capa entre os volumes do Google Books, ou ''. Servem os livros em português cujo título é o
    nosso (o subtítulo pode vir no campo separado) e cujo autor tem o nosso sobrenome. Caixa, resumo e guia não
    servem, como na Apple. Título igual ganha de título com subtítulo; no empate, o que veio antes.
    Com `isbn`, o volume também tem de declarar aquele ISBN (10 e 13 da mesma edição casam); nesse caso, um ISBN
    conferido à mão permite aceitar mesmo sem autor certo no catálogo, desde que o título confira."""
    alvo, nosso, melhor = nt(titulo), set(chave(titulo).split()), None
    por_isbn = isbn_valido(isbn)
    for pos, item in enumerate(itens or []):
        v = item.get('volumeInfo') if isinstance(item, dict) else None
        if not isinstance(v, dict) or v.get('printType', 'BOOK') != 'BOOK':
            continue
        if por_isbn:
            ids = [x.get('identifier') for x in (v.get('industryIdentifiers') or []) if isinstance(x, dict)]
            if not any(mesmo_isbn(isbn, x) for x in ids):
                continue
        capa, completo = imagem_google(v), titulo_google(v)
        if not capa or not (titulo_confere(titulo, str(v.get('title') or ''), hq) or titulo_confere(titulo, completo, hq)):
            continue
        autores_deles = set(som(' '.join(str(a) for a in (v.get('authors') or []))).split())
        if nome:
            if som(nome) not in autores_deles:
                continue
        elif not por_isbn:
            continue
        lingua = str(v.get('language') or '')
        if lingua and lingua not in ('pt', 'por'):
            continue
        if (set(chave(completo).split()) - nosso) & OUTRO_PRODUTO:
            continue
        cand = (0 if nt(completo) == alvo else 1, 0 if lingua else 1, pos, capa)
        if melhor is None or cand[:3] < melhor[:3]:
            melhor = cand
    return melhor[3] if melhor else ''


def ocultar_chave(texto, segredo=''):
    """Texto de erro sem a chave de API: remove o valor exato, parâmetros key=… e o formato de chave do Google."""
    texto = str(texto or '')
    if segredo:
        texto = texto.replace(segredo, '[chave ocultada]')
    texto = re.sub(r'(?i)([?&]key=)[^&\s"\']+', r'\1[chave ocultada]', texto)
    texto = re.sub(r'(?i)(\bkey\s*[=:]\s*)[^&\s"\',;]+', r'\1[chave ocultada]', texto)
    return re.sub(r'AIza[0-9A-Za-z_-]{20,}', '[chave ocultada]', texto)


def detalhe_http(e, segredo=''):
    """O motivo que o serviço devolveu no corpo do erro, limpo e curto, para o resumo da execução.
    Nunca devolve a chave de API: remove o valor exato e qualquer parecido com chave na URL/texto."""
    try:
        corpo = e.read(4096).decode('utf-8', 'replace')
    except Exception:
        corpo = ''
    detalhe = ''
    try:
        dado = json.loads(corpo)
        erro = dado.get('error') if isinstance(dado, dict) else None
        if isinstance(erro, dict):
            detalhe = str(erro.get('message') or '')
            status = str(erro.get('status') or '')
            if status and status not in detalhe:
                detalhe = f'{detalhe} ({status})'.strip()
        elif isinstance(erro, str):
            detalhe = erro
    except (json.JSONDecodeError, TypeError, ValueError):
        pass
    if not detalhe:
        detalhe = str(getattr(e, 'msg', '') or getattr(e, 'reason', '') or '')
    detalhe = re.sub(r'[\x00-\x1f\x7f]+', ' ', detalhe).strip()
    return ocultar_chave(detalhe, segredo)[:300]


def buscar_google(params, limite, tentativas=3, dormir=time.sleep, chave=None):
    """A resposta do Google Books. Quando ele recusa por excesso de consultas (429) ou fica fora do ar, espera um
    pouco e tenta de novo; se a recusa continua, a consulta falha e o livro fica para a próxima execução.
    A chave opcional vem de GOOGLE_BOOKS_API_KEY (ou do argumento `chave`) e vai no cabeçalho X-Goog-Api-Key,
    nunca na URL. O motivo do erro HTTP vai na mensagem, sem a chave, para aparecer no resumo do GitHub."""
    if chave is None:
        chave = os.environ.get('GOOGLE_BOOKS_API_KEY', '').strip()
    url = GOOGLE + '?' + urllib.parse.urlencode(params)
    cabecalhos = {'User-Agent': AGENTE, 'Accept': 'application/json'}
    if chave:
        cabecalhos['X-Goog-Api-Key'] = chave
    for n in range(tentativas):
        limite.espera()
        try:
            req = urllib.request.Request(url, headers=cabecalhos)
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.loads(r.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            if e.code not in (429, 500, 502, 503, 504) or n == tentativas - 1:
                motivo = detalhe_http(e, chave)
                msg = ocultar_chave(e.msg, chave)
                e.msg = f'{msg} — {motivo}' if motivo and motivo not in msg else msg
                raise
            dormir(30 * (n + 1) if e.code == 429 else 3 * (n + 1) ** 2)
        except (urllib.error.URLError, TimeoutError, ConnectionError, json.JSONDecodeError):
            if n == tentativas - 1:
                raise
            dormir(3 * (n + 1) ** 2)
    raise RuntimeError('sem resposta')


def consulta_google_isbn(isbn):
    """A consulta ao Google Books pelo ISBN exato da edição conferida à mão."""
    c = isbn_limpo(isbn)
    return {'q': f'isbn:{c}', 'maxResults': '10', 'printType': 'books'} if isbn_valido(c) else None


def procurar_google(titulo, autor, hq, limite, buscar=buscar_google, isbn=''):
    """(endereço da capa, 'google') ou ('', 'nao-achei-3'). Levanta exceção se a consulta falhar.
    Com ISBN conferido, procura primeiro o número exato; se a resposta vier sem capa que sirva, tenta título/autor.
    Erro de rede não vira 'não achei' nem dispara a segunda tentativa: o livro fica para a próxima execução."""
    nome = sobrenome(autor, ultimo=adaptacao(titulo))
    if isbn_valido(isbn):
        itens = (buscar(consulta_google_isbn(isbn), limite) or {}).get('items')
        capa = escolher_google(titulo, nome, itens, hq, isbn=isbn)
        if capa:
            return capa, 'google'
    params = consulta_google(titulo, autor)
    if params is None:
        return '', 'nao-achei-3'
    capa = escolher_google(titulo, nome, (buscar(params, limite) or {}).get('items'), hq)
    return (capa, 'google') if capa else ('', 'nao-achei-3')


# ───────── piloto gratuito: Internet Archive (só leitura, nunca entra no casamento automático) ─────────

def consulta_arquivo(titulo, autor, isbn=''):
    """A consulta ao Internet Archive (advancedsearch.php, API pública e gratuita). Com ISBN conferido, procura o
    número; sem ele, título principal + sobrenome do autor, só entre itens de texto. None quando não há como procurar."""
    c = isbn_limpo(isbn)
    if isbn_valido(c):
        q = f'isbn:{c} AND mediatype:texts'
    else:
        nome = sobrenome(autor, ultimo=adaptacao(titulo))
        frase = ' '.join(re.sub(r'["\\]', ' ', principal(titulo)).split())
        if not nome or not frase:
            return None
        q = f'title:"{frase}" AND creator:"{nome}" AND mediatype:texts'
    return {'q': q, 'fl[]': ['identifier', 'title', 'creator', 'isbn', 'language', 'mediatype'], 'rows': '8', 'output': 'json'}


def buscar_arquivo(params, limite, tentativas=3, dormir=time.sleep):
    """A resposta JSON do Internet Archive. Recusa por excesso (429) ou queda espera e tenta de novo, devagar."""
    url = ARQUIVO + '?' + urllib.parse.urlencode(params, doseq=True)
    for n in range(tentativas):
        limite.espera()
        try:
            req = urllib.request.Request(url, headers={'User-Agent': AGENTE, 'Accept': 'application/json'})
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.loads(r.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            if e.code not in (429, 500, 502, 503, 504) or n == tentativas - 1:
                raise
            dormir(30 * (n + 1) if e.code == 429 else 3 * (n + 1) ** 2)
        except (urllib.error.URLError, TimeoutError, ConnectionError, json.JSONDecodeError):
            if n == tentativas - 1:
                raise
            dormir(3 * (n + 1) ** 2)
    raise RuntimeError('sem resposta')


def _lista_texto(valor):
    if isinstance(valor, list):
        return [str(x) for x in valor if str(x).strip()]
    return [str(valor)] if str(valor or '').strip() else []


def documentos_arquivo(resp):
    """Os itens de uma resposta do advancedsearch.php; lista vazia quando a resposta não tem a forma esperada."""
    if not isinstance(resp, dict):
        return []
    resposta = resp.get('response')
    docs = resposta.get('docs') if isinstance(resposta, dict) else None
    return [d for d in docs if isinstance(d, dict)] if isinstance(docs, list) else []


def candidatos_arquivo(titulo, autor, isbn, docs):
    """Candidatos do Internet Archive para revisão humana. `serve` é sempre False: a miniatura é do item digitalizado,
    pode ser de outra edição ou de uma página que não a capa. Nenhum resultado daqui vai para o capas.tsv sozinho."""
    out = []
    for d in docs or []:
        if not isinstance(d, dict):
            continue
        ident = str(d.get('identifier') or '').strip()
        if not IDENTIFICADOR_ARQUIVO.match(ident):
            continue
        if str(d.get('mediatype') or 'texts') != 'texts':
            continue
        deles = ' '.join(_lista_texto(d.get('title')))
        autor_deles = '; '.join(_lista_texto(d.get('creator')))
        isbn_deles = '; '.join(_lista_texto(d.get('isbn')))
        lingua = '; '.join(_lista_texto(d.get('language')))
        motivo = 'piloto gratuito: a miniatura é do item digitalizado; confira edição e capa antes de escolher'
        if not titulo_confere(titulo, deles, adaptacao(titulo)):
            motivo += '; o título não confere'
        if isbn_valido(isbn) and not any(mesmo_isbn(isbn, x) for x in re.split(r'[;,\s]+', isbn_deles) if x):
            motivo += '; o ISBN não confere'
        out.append({'fonte': 'Internet Archive (piloto)', 'titulo': deles, 'autor': autor_deles, 'lingua': lingua,
                    'isbn': isbn_deles, 'capa': ARQUIVO_IMAGEM + urllib.parse.quote(ident, safe=''),
                    'serve': False, 'motivo': motivo})
    return out


def procurar_arquivo(titulo, autor, isbn, limite, buscar=buscar_arquivo):
    """Só leitura: devolve candidatos do Internet Archive. Levanta exceção se a consulta falhar."""
    params = consulta_arquivo(titulo, autor, isbn)
    if params is None:
        return []
    resp = buscar(params, limite)
    return candidatos_arquivo(titulo, autor, isbn, documentos_arquivo(resp))


def piloto_arquivo(livros, capas, isbns=None, quantos=20, pausa=PAUSA_ARQUIVO, buscar=buscar_arquivo):
    """Amostra determinística e pequena de livros sem capa, só para medir o piloto do Internet Archive.
    Mostra candidatos e miniaturas para revisão humana; não escolhe capa, não consulta as outras fontes e não
    grava em arquivo nenhum. Devolve 1 se alguma consulta falhar, 0 quando todas responderam (mesmo sem candidato)."""
    quantos, isbns = max(1, min(int(quantos), 100)), isbns or {}
    sem_capa, consultaveis, vistos = 0, [], set()
    for b in livros:
        k = (chave(b['t']), chave(b['a']))
        if k in vistos or (capas.get(k) or {}).get('capa', ''):
            continue
        vistos.add(k)
        sem_capa += 1
        isbn = isbns.get(k, '')
        if consulta_arquivo(b['t'], b['a'], isbn) is not None:
            consultaveis.append((b, isbn))
    amostra = [consultaveis[i * len(consultaveis) // min(quantos, len(consultaveis))] for i in range(min(quantos, len(consultaveis)))]
    print(f'Piloto gratuito do Internet Archive: {sem_capa} livros sem capa · {len(consultaveis)} com título/autor ou ISBN para consultar · amostra de {len(amostra)}.')
    print('Só leitura: nada é escolhido nem gravado; a miniatura pode ser de outra edição ou nem ser a capa.')
    if not amostra:
        print('Nada a consultar nesta amostra. Nada foi gravado.')
        return 0
    limite, consultados, com_candidatos, total, falhas, seguidas, restantes = Limite(pausa), 0, 0, 0, 0, 0, 0
    for i, (b, isbn) in enumerate(amostra):
        if seguidas >= 5:
            restantes = len(amostra) - i
            print('O Internet Archive não respondeu a 5 consultas seguidas; parei o piloto.')
            break
        print(f'\n── {i + 1}/{len(amostra)} · {b["t"]} — {b["a"] or "sem autor certo"}', flush=True)
        try:
            lista = procurar_arquivo(b['t'], b['a'], isbn, limite, buscar)
        except Exception as e:
            falhas += 1
            seguidas += 1
            print(f'   falhou: {type(e).__name__}: {e}', flush=True)
            continue
        seguidas, consultados = 0, consultados + 1
        com_candidatos += 1 if lista else 0
        total += len(lista)
        print(texto_candidatos(b['t'], b['a'], lista), flush=True)
    print(f'Piloto Internet Archive: {consultados} consultados · {com_candidatos} com candidatos para revisar · {total} candidatos · {falhas} falha(s)'
          + (f' · {restantes} ficaram sem consultar' if restantes else ''))
    print('Nada foi gravado: nenhum candidato entrou no casamento automático nem em catalogo/capas.tsv.')
    return 1 if falhas else 0


# ───────── escolher à mão: o que cada fonte devolve (--candidatos) ─────────

def consulta_isbn(isbn):
    """A consulta à Open Library pelo ISBN de uma edição (o número que está na quarta capa do livro)."""
    c = isbn_limpo(isbn)
    return {'q': f'isbn:{c}', 'fields': CAMPOS, 'limit': '8'} if isbn_valido(c) else None


def consulta_isbn_exata(isbn):
    """A consulta da edição exata na Open Library (Books API, jscmd=data): ficha, autores e capa do ISBN pedido.
    Diferente da busca por palavras, não devolve a obra com outra edição no lugar. None se o ISBN não fecha."""
    c = isbn_limpo(isbn)
    return {'bibkeys': f'ISBN:{c}', 'format': 'json', 'jscmd': 'data'} if isbn_valido(c) else None


def capa_isbn_ol(registro):
    """O número da capa a partir do endereço que a Books API devolve (covers.openlibrary.org/b/id/N-M.jpg).
    '' quando não há capa ou o endereço não é o da Open Library."""
    capa = (registro or {}).get('cover') or {}
    for tamanho in ('medium', 'large', 'small'):
        m = IMAGEM_OL.match(str(capa.get(tamanho) or '').strip())
        if m and int(m.group(1)) > 0:
            return m.group(1)
    return ''


def escolher_isbn(titulo, autor, isbn, registro, hq=False):
    """(capa, motivo) da edição exata devolvida pela Books API. Só aceita quando o ISBN do registro é o pedido
    (10 e 13 da mesma edição casam), o título confere e — se o catálogo tem autor certo — o autor também.
    Sem autor certo, o ISBN conferido à mão é a segurança; ainda assim o título tem de conferir."""
    if not isinstance(registro, dict) or not registro:
        return '', 'a fonte não devolveu a ficha deste ISBN'
    ids = (registro.get('identifiers') or {})
    numeros = list(ids.get('isbn_13') or []) + list(ids.get('isbn_10') or [])
    if not any(mesmo_isbn(isbn, x) for x in numeros):
        return '', 'o ISBN da ficha não é o desta edição'
    deles = str(registro.get('title') or '')
    if not titulo_confere(titulo, deles, hq):
        return '', 'o título não confere'
    nome = sobrenome(autor, ultimo=adaptacao(titulo))
    if nome:
        nomes = ' '.join(str(a.get('name') or '') for a in (registro.get('authors') or []) if isinstance(a, dict))
        if som(nome) not in set(som(nomes).split()):
            return '', 'o autor não confere'
    if (set(chave(deles).split()) - set(chave(titulo).split())) & OUTRO_PRODUTO:
        return '', 'caixa, resumo ou guia'
    capa = capa_isbn_ol(registro)
    return (capa, SERVE) if capa else ('', 'sem imagem')


def buscar_isbn(params, limite, tentativas=3, dormir=time.sleep):
    """A resposta da Books API da Open Library para um ISBN. Recusa por excesso (429) ou queda espera e tenta de novo."""
    url = BUSCA_ISBN + '?' + urllib.parse.urlencode(params)
    for n in range(tentativas):
        limite.espera()
        try:
            req = urllib.request.Request(url, headers={'User-Agent': AGENTE, 'Accept': 'application/json'})
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.loads(r.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            if e.code not in (429, 500, 502, 503, 504) or n == tentativas - 1:
                raise
            dormir(30 * (n + 1) if e.code == 429 else 3 * (n + 1) ** 2)
        except (urllib.error.URLError, TimeoutError, ConnectionError, json.JSONDecodeError):
            if n == tentativas - 1:
                raise
            dormir(3 * (n + 1) ** 2)
    raise RuntimeError('sem resposta')


def procurar_isbn(titulo, autor, isbn, hq, limite, buscar=buscar_isbn):
    """(capa, 'edicao') da edição exata na Open Library, ou ('', motivo). Levanta exceção se a consulta falhar.
    'edicao' é a mesma origem das capas de edição da Open Library: o painel já sabe mostrar e rotular."""
    params = consulta_isbn_exata(isbn)
    if params is None:
        return '', 'ISBN inválido'
    resp = buscar(params, limite) or {}
    registro = resp.get(f'ISBN:{isbn_limpo(isbn)}')
    capa, motivo = escolher_isbn(titulo, autor, isbn, registro, hq)
    return (capa, 'edicao') if capa else ('', motivo)


SERVE = 'a capa que a busca automática escolheria'                      # o motivo que marca o candidato aceito


def candidatos(titulo, autor, hq=False, isbn='', ol=None, apple=None, google=None, limites=None, arquivo=False, ia=None, ol_isbn=None):
    """O que cada fonte devolve para um livro, para escolher à mão. Não grava nada.

    Devolve uma lista de candidatos: fonte, título, autor, língua, ISBN, capa, se a busca automática aceitaria
    ("serve") e por que não aceitaria. As respostas são as mesmas consultas da busca; o julgamento é o das mesmas
    funções que escolhem a capa sozinha — o que aparece como "serve" é o que entraria numa execução automática.
    Uma consulta que falha não derruba as outras: entra na lista como um candidato de fonte com o erro no motivo.
    Com ISBN conferido, a Open Library responde primeiro pela edição exata; a busca por palavras só entra se essa
    ficha não der capa. Com `arquivo=True`, inclui o piloto gratuito do Internet Archive; esses candidatos nunca
    vêm como "serve"."""
    ol, apple, google = (buscar_json if ol is None else ol), (buscar_apple if apple is None else apple), (buscar_google if google is None else google)
    ia, ol_isbn = (buscar_arquivo if ia is None else ia), (buscar_isbn if ol_isbn is None else ol_isbn)
    lim = {'ol': Limite(0.4), 'apple': Limite(PAUSA_APPLE), 'google': Limite(PAUSA_GOOGLE), 'isbn': Limite(PAUSA_ISBN), 'arquivo': Limite(PAUSA_ARQUIVO)}
    lim.update(limites or {})
    nome = sobrenome(autor, ultimo=adaptacao(titulo))
    out = []

    def consulta(fonte, fn, params):
        if params is None:
            return None, 'não se procura este livro (sem autor certo, ou adaptação em quadrinhos com um autor só)'
        try:
            return fn(params, lim[fonte]), ''
        except Exception as e:
            return None, f'{type(e).__name__}: {e}'

    por_isbn = isbn_valido(isbn)
    ol_resolvido = False
    if por_isbn:
        resp, erro = consulta('isbn', ol_isbn, consulta_isbn_exata(isbn))
        registro = (resp or {}).get(f'ISBN:{isbn_limpo(isbn)}') if not erro else None
        capa, motivo = ('', erro) if erro else escolher_isbn(titulo, autor, isbn, registro, hq)
        registro = registro if isinstance(registro, dict) else {}
        out.append({'fonte': 'Open Library (ISBN)', 'titulo': str(registro.get('title') or ''),
                    'autor': ', '.join(str(a.get('name') or '') for a in (registro.get('authors') or []) if isinstance(a, dict)),
                    'lingua': '', 'isbn': isbn_limpo(isbn), 'capa': capa, 'serve': bool(capa), 'motivo': motivo})
        ol_resolvido = bool(capa)
    if not ol_resolvido:
        params_ol = consulta_isbn(isbn) if por_isbn else (consulta_de(titulo, autor) or consulta_so_titulo(titulo))
        if params_ol is not None:
            params_ol['fields'] = CAMPOS + ',editions.isbn'            # o ISBN da edição, para conferir com o livro na mão
        resp, erro = consulta('ol', ol, params_ol)
        if erro:
            out.append({'fonte': 'Open Library', 'titulo': '', 'autor': '', 'lingua': '', 'isbn': '', 'capa': '', 'serve': False, 'motivo': erro})
        else:
            docs = (resp or {}).get('docs') or []
            escolhida = escolher(titulo, docs, hq)[0]
            for d in docs:
                eds = ((d.get('editions') or {}).get('docs') or [])
                ed = eds[0] if eds else {}
                capa = ed.get('cover_i') or d.get('cover_i')
                deles = ed.get('title') or d.get('title') or ''
                lingua = ', '.join(ed.get('language') or [])
                motivo = ('sem imagem' if not capa else 'o título não confere' if not titulo_confere(titulo, deles, hq) else
                          'o autor não confere' if not autor_confere(nome, d) else
                          SERVE if capa == escolhida else 'não é a que a busca escolheria')
                out.append({'fonte': 'Open Library', 'titulo': deles, 'autor': ', '.join(d.get('author_name') or []), 'lingua': lingua,
                            'isbn': ', '.join((ed.get('isbn') or [])[:2]), 'capa': str(capa) if capa else '',
                            'serve': motivo == SERVE, 'motivo': motivo})
            if not docs:
                out.append({'fonte': 'Open Library', 'titulo': '', 'autor': '', 'lingua': '', 'isbn': '', 'capa': '', 'serve': False, 'motivo': 'a fonte não devolveu nenhum resultado'})
    resp, erro = consulta('google', google, consulta_google_isbn(isbn) if por_isbn else consulta_google(titulo, autor))
    if erro:
        out.append({'fonte': 'Google Books', 'titulo': '', 'autor': '', 'lingua': '', 'isbn': '', 'capa': '', 'serve': False, 'motivo': erro})
    else:
        itens = [i for i in ((resp or {}).get('items') or []) if isinstance(i, dict) and isinstance(i.get('volumeInfo'), dict)]
        escolhida = escolher_google(titulo, nome, itens, hq, isbn=isbn if por_isbn else '')
        for i in itens:
            v = i['volumeInfo']
            capa, completo = imagem_google(v), titulo_google(v)
            autor_deles = ', '.join(str(a) for a in (v.get('authors') or []))
            ids = [x.get('identifier') for x in (v.get('industryIdentifiers') or []) if isinstance(x, dict)]
            bate_isbn = not por_isbn or any(mesmo_isbn(isbn, x) for x in ids)
            bate_titulo = titulo_confere(titulo, str(v.get('title') or ''), hq) or titulo_confere(titulo, completo, hq)
            nomes_deles = set(som(' '.join(str(a) for a in (v.get('authors') or []))).split())
            bate_autor = som(nome) in nomes_deles if nome else (por_isbn and bate_isbn)
            motivo = ('sem imagem' if not capa else
                      'o ISBN não é o desta edição' if not bate_isbn else
                      'caixa, resumo ou guia' if (set(chave(completo).split()) - set(chave(titulo).split())) & OUTRO_PRODUTO else
                      'o título não confere' if not bate_titulo else 'o autor não confere' if not bate_autor else
                      'livro em outra língua' if str(v.get('language') or '') not in ('', 'pt', 'por') else
                      'a capa que a busca automática escolheria' if capa == escolhida else 'não é a que a busca escolheria')
            out.append({'fonte': 'Google Books', 'titulo': completo, 'autor': autor_deles, 'lingua': str(v.get('language') or ''),
                        'isbn': ', '.join(str(x.get('identifier', '')) for x in (v.get('industryIdentifiers') or []) if isinstance(x, dict)),
                        'capa': capa, 'serve': motivo == SERVE, 'motivo': motivo})
        if not itens:
            out.append({'fonte': 'Google Books', 'titulo': '', 'autor': '', 'lingua': '', 'isbn': '', 'capa': '', 'serve': False, 'motivo': 'a fonte não devolveu nenhum resultado'})
    if not por_isbn:                                                   # a busca da Apple não procura por ISBN
        resp, erro = consulta('apple', apple, consulta_apple(titulo, autor))
        if erro:
            out.append({'fonte': 'Apple Books', 'titulo': '', 'autor': '', 'lingua': '', 'isbn': '', 'capa': '', 'serve': False, 'motivo': erro})
        else:
            resultados = [r for r in ((resp or {}).get('results') or []) if isinstance(r, dict)]
            escolhida = escolher_apple(titulo, nome, resultados, hq)
            for r in resultados:
                capa, deles = imagem_apple(r), str(r.get('trackName') or '')
                motivo = ('sem imagem' if not capa else 'não é livro digital' if r.get('kind', 'ebook') != 'ebook' else
                          'caixa, resumo ou guia' if (set(chave(deles).split()) - set(chave(titulo).split())) & OUTRO_PRODUTO else
                          'o título não confere' if not titulo_confere(titulo, deles, hq) else
                          'o autor não confere' if not (nome and som(nome) in set(som(str(r.get('artistName') or '')).split())) else
                          'a capa que a busca automática escolheria' if capa == escolhida else 'não é a que a busca escolheria')
                out.append({'fonte': 'Apple Books', 'titulo': deles, 'autor': str(r.get('artistName') or ''), 'lingua': 'pt (loja do Brasil)',
                            'isbn': '', 'capa': capa, 'serve': motivo == SERVE, 'motivo': motivo})
            if not resultados:
                out.append({'fonte': 'Apple Books', 'titulo': '', 'autor': '', 'lingua': '', 'isbn': '', 'capa': '', 'serve': False, 'motivo': 'a fonte não devolveu nenhum resultado'})
    if arquivo:
        params = consulta_arquivo(titulo, autor, isbn)
        resp, erro = consulta('arquivo', ia, params)
        if erro:
            out.append({'fonte': 'Internet Archive (piloto)', 'titulo': '', 'autor': '', 'lingua': '', 'isbn': '', 'capa': '', 'serve': False, 'motivo': erro})
        else:
            achados = candidatos_arquivo(titulo, autor, isbn, documentos_arquivo(resp))
            out += achados
            if not achados:
                out.append({'fonte': 'Internet Archive (piloto)', 'titulo': '', 'autor': '', 'lingua': '', 'isbn': '', 'capa': '', 'serve': False, 'motivo': 'a fonte não devolveu nenhum resultado'})
    return out


def texto_candidatos(titulo, autor, lista):
    """A lista de candidatos como se lê na tela, com a linha pronta para colar no capas.tsv."""
    L = [f'Candidatos para “{titulo}”' + (f', de {autor}' if autor else ''), '']
    if not lista:
        return '\n'.join(L + ['Nenhuma fonte devolveu nada para este livro.', ''])
    servem = sum(1 for c in lista if c['serve'])
    L += [f'{len(lista)} candidatos · {servem} aceitos pela busca automática', '']
    for i, c in enumerate(lista, 1):
        L.append(f'{i:2}. [{c["fonte"]}] {c["titulo"] or "(sem título)"} — {c["autor"] or "sem autor"}'
                 + (f' · {c["lingua"]}' if c['lingua'] else '') + (f' · ISBN {c["isbn"]}' if c['isbn'] else ''))
        L.append(f'    {"SERVE" if c["serve"] else "não serve"}: {c["motivo"]}')
        L.append(f'    capa: {c["capa"] or "(sem imagem)"}')
        if c['capa'] and c['fonte'].startswith('Internet Archive'):
            L.append('    só para conferir: o piloto do Internet Archive não entra no capas.tsv')
        elif c['capa']:
            L.append(f'    para escolher esta, cole no capas.tsv: {titulo}\t{autor}\t{c["capa"]}\tmanual')
        L.append('')
    if lista and all(c['fonte'].startswith('Internet Archive') for c in lista):
        L += ['Nada foi gravado. Este piloto é só de leitura: nenhum candidato do Internet Archive entra no capas.tsv.', '']
    else:
        L += ['Nada foi gravado. Quem escolhe é você: `manual` na coluna origem garante que a busca não troque a capa.'
              + (' Candidatos do Internet Archive são só para conferir; não entram no capas.tsv.' if any(c['fonte'].startswith('Internet Archive') for c in lista) else ''), '']
    return '\n'.join(L)


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
    A capa fica nas linhas sem subtítulo e sai das que têm, que voltam a "não achei" no ponto em que a busca tinha
    parado: "nao-achei" se a capa era da Open Library (a Apple e o Google ainda podem ter a certa), "nao-achei-2" se
    era da Apple (falta o Google) e "nao-achei-3" se era do Google. Capas postas à mão não entram na conta.
    Devolve quantas capas saíram."""
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
                r['capa'], r['origem'] = '', PROXIMA.get(r['origem'], 'nao-achei')
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


FONTE_DA_ORIGEM = {'edicao': 'e', 'obra': 'o', 'apple': 'a', 'google': 'g', 'manual': 'm'}


def para_as_fontes(livros, capas=None):
    """Uma letra por livro do catálogo, na mesma ordem de para_o_painel: de onde veio a capa que o painel mostra.
    'e' edição da Open Library · 'o' obra da Open Library (pode ser outra edição) · 'a' Apple · 'g' Google ·
    'm' escolhida à mão · '0' sem capa. É o que permite ao painel dizer a origem e avisar de uma possível outra edição,
    sem guardar mais nada além de uma letra por livro."""
    capas = ler_capas() if capas is None else capas
    painel = para_o_painel(livros, capas)
    out = []
    for b, tem in zip(livros, painel):
        origem = (capas.get((chave(b['t']), chave(b['a']))) or {}).get('origem', '')
        out.append(FONTE_DA_ORIGEM.get(origem, '0') if tem else '0')
    return ''.join(out)


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
    """A mesma conferência para as capas que vieram da Apple (ver testar_enderecos)."""
    return testar_enderecos(capas, quantas, abrir, pausa, 'apple')


def testar_enderecos(capas, quantas=40, abrir=abrir_imagem, pausa=0.3, origem='apple'):
    """A mesma conferência para as capas guardadas como endereço (Apple, Google): pede `quantas` delas (espalhadas
    pelo arquivo), no endereço guardado, que é o que o painel usa. Devolve (quantas abriram, quantas pedidas, as ruins)."""
    enderecos = [r['capa'] for r in capas.values() if r['origem'] == origem and r['capa']]
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
    if '--candidatos' in argv:                                          # o que cada fonte tem para um livro: nada é gravado
        def texto(nome, padrao=''):
            i = argv.index(nome) + 1 if nome in argv else -1
            return argv[i] if 0 < i < len(argv) else padrao
        titulo, autor, isbn = texto('--candidatos'), texto('--autor'), isbn_limpo(texto('--isbn'))
        if not titulo and not isbn:
            print(__doc__)
            return 2
        if isbn and not isbn_valido(isbn):
            print(f'ISBN {isbn} não fecha na conta de conferência; confira o número.')
            return 2
        titulo = titulo or f'ISBN {isbn}'
        lista = candidatos(titulo, autor, '--hq' in argv, isbn, limites={'ol': Limite(pausa), 'apple': Limite(pausa_apple), 'google': Limite(valor('--pausa-google', PAUSA_GOOGLE)), 'arquivo': Limite(valor('--pausa-arquivo', PAUSA_ARQUIVO))}, arquivo='--arquivo' in argv)
        print(texto_candidatos(titulo, autor, lista))
        return 0
    livros = parse(pathlib.Path(CATALOGO).read_text(encoding='utf-8'))
    capas = ler_capas()
    try:
        isbns = ler_isbns()
    except ValueError as e:
        print(f'Arquivo de ISBN não pode ser usado: {e}')
        return 2
    chaves_do_catalogo = {(chave(b['t']), chave(b['a'])) for b in livros}
    fora_do_catalogo = [k for k in isbns if k not in chaves_do_catalogo]
    if fora_do_catalogo:
        t, a = fora_do_catalogo[0]
        print(f'Arquivo de ISBN não pode ser usado: {len(fora_do_catalogo)} linha(s) não casam com o catálogo. '
              f'Copie o título e o autor exatamente como estão nele; a primeira é “{t}” — “{a}”.')
        return 2
    if '--piloto' in argv:
        i = argv.index('--piloto')
        try:
            quantos = int(argv[i + 1]) if i + 1 < len(argv) else 20
        except ValueError:
            quantos = 0
        if not 1 <= quantos <= 100:
            print('Use --piloto N, com N entre 1 e 100 (por exemplo: --piloto 20).')
            return 2
        return piloto_arquivo(livros, capas, isbns, quantos, valor('--pausa-arquivo', PAUSA_ARQUIVO), buscar_arquivo)
    # o que falta, livro a livro: 'tudo' = as três fontes, em ordem; 'apple' = falta a Apple (e o Google);
    # 'google' = já passou pelas duas primeiras, falta só o Google; 'isbn' = sem autor certo, mas com ISBN conferido
    falta = {}
    for b in livros:
        k = (chave(b['t']), chave(b['a']))
        r = capas.get(k)
        tem_isbn = k in isbns
        if r is None or (refazer and (r['origem'] in NAO_ACHADAS or (tem_isbn and r['origem'] == 'sem-autor'))):
            falta.setdefault(k, (b, 'tudo'))
        elif r['origem'] == 'sem-autor' and tem_isbn:
            falta.setdefault(k, (b, 'isbn'))                     # ISBN conferido à mão: edição exata, mesmo sem autor certo
        elif r['origem'] == 'nao-achei':
            falta.setdefault(k, (b, 'apple'))
        elif r['origem'] == 'nao-achei-2' and '--sem-google' not in argv:
            falta.setdefault(k, (b, 'google'))
    falta = [(k, b, modo) for k, (b, modo) in falta.items()]
    so_apple = sum(1 for _, _, modo in falta if modo == 'apple')
    so_google = sum(1 for _, _, modo in falta if modo == 'google')
    so_isbn = sum(1 for _, _, modo in falta if modo == 'isbn')
    detalhes = ([f'{so_apple} só na Apple: já passaram pela Open Library'] if so_apple else [])
    if so_google:
        detalhes.append(f'{so_google} só no Google: já passaram pelas duas')
    if so_isbn:
        detalhes.append(f'{so_isbn} com ISBN conferido: edição exata')
    print(f'Catálogo: {len(livros)} livros · {sum(1 for r in capas.values() if r["capa"])} com capa · {len(falta)} a procurar'
          + (f' ({" · ".join(detalhes)})' if detalhes else ''))
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
        for origem, nome in (('apple', 'da Apple'), ('google', 'do Google Books')):
            boas, pedidas, ruins = testar_enderecos(capas, quantas, abrir_imagem, espera, origem)
            if pedidas:
                print(f'Amostra das capas {nome}: {boas} de {pedidas} abriram como imagem')
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
    lim, lim_apple, lim_google = Limite(pausa), Limite(pausa_apple), Limite(valor('--pausa-google', PAUSA_GOOGLE))
    lim_isbn = Limite(valor('--pausa-isbn', PAUSA_ISBN))
    feitos, adiados, falhas, t0 = 0, 0, [], time.time()

    estado = {'desistiu': False, 'tentados': 0, 'falhos': 0, 'apple_fora': False, 'apple_seguidas': 0,
              'google_fora': False, 'google_seguidas': 0, 'isbn_fora': False, 'isbn_seguidas': 0}
    trava = threading.Lock()

    def fora_do_ar(fonte):
        """Avisa, uma vez só, que uma fonte parou de responder; devolve True quando já se desistiu dela."""
        with trava:
            estado[f'{fonte}_seguidas'] += 1
            if estado[f'{fonte}_seguidas'] >= 5 and not estado[f'{fonte}_fora']:
                estado[f'{fonte}_fora'] = True
                nome = {'apple': 'A Apple', 'google': 'O Google Books', 'isbn': 'A Open Library por ISBN'}.get(fonte, fonte)
                print(f'{nome} não respondeu a 5 consultas seguidas; parei de procurar nele.', flush=True)
        return estado[f'{fonte}_fora']

    def um(item):
        """(chave, livro, resultado a gravar ou None, erro). erro '' = não foi tentado (fica para a próxima execução)."""
        k, b, modo = item
        if estado['desistiu'] or (prazo and time.time() > prazo):
            return k, b, None, ''                                       # acabou o tempo (ou a rede não responde): fica para a próxima execução
        hq, res = 'HQ' in b['tags'], ('', 'nao-achei')
        isbn = isbns.get(k, '')
        if isbn and not estado['isbn_fora']:
            try:
                achado = procurar_isbn(b['t'], b['a'], isbn, hq, lim_isbn)
            except Exception as e:
                fora_do_ar('isbn')
                return k, b, None, f'Open Library por ISBN: {type(e).__name__}: {e}'
            with trava:
                estado['isbn_seguidas'] = 0
            if achado[1] == 'edicao':
                return k, b, achado, None
        if isbn and estado['isbn_fora']:                                # a ficha exata caiu: não troca por busca ampla
            return k, b, None, ''
        if modo == 'isbn':                                              # sem autor certo, mas com ISBN conferido à mão
            if '--sem-google' in argv:
                return k, b, ('', 'sem-autor'), None
            if estado['google_fora']:
                return k, b, None, ''
            try:
                achado = procurar_google(b['t'], b['a'], hq, lim_google, isbn=isbn)
            except Exception as e:
                fora_do_ar('google')
                return k, b, None, f'Google: {type(e).__name__}: {e}'
            with trava:
                estado['google_seguidas'] = 0
            return k, b, (achado if achado[1] == 'google' else ('', 'sem-autor')), None
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
                return k, b, res, None                                  # achou na Open Library (ou não é livro que se procure)
        if modo in ('tudo', 'apple'):
            if estado['apple_fora']:                                    # a Apple parou de responder: o livro fica como estava
                return (k, b, res, None) if modo == 'tudo' else (k, b, None, '')
            try:
                res = procurar_apple(b['t'], b['a'], hq, lim_apple)
            except Exception as e:
                fora_do_ar('apple')
                return k, b, (res if modo == 'tudo' else None), f'Apple: {type(e).__name__}: {e}'
            with trava:
                estado['apple_seguidas'] = 0
            if res[1] == 'apple':
                return k, b, res, None
        if '--sem-google' in argv:                                      # combinado nesta execução: ficar nas duas primeiras
            return k, b, res, None
        if estado['google_fora']:                                       # o Google parou de responder: fica para a próxima execução
            return (k, b, res, None) if modo != 'google' else (k, b, None, '')
        try:
            res = procurar_google(b['t'], b['a'], hq, lim_google, isbn=isbn)
        except Exception as e:
            fora_do_ar('google')
            return k, b, (res if modo != 'google' else None), f'Google: {type(e).__name__}: {e}'
        with trava:
            estado['google_seguidas'] = 0
        return k, b, res, None

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
    motivo = ('a Open Library não respondeu' if estado['desistiu'] else 'a Open Library por ISBN não respondeu' if estado['isbn_fora']
              else 'a Apple não respondeu' if estado['apple_fora'] else 'o Google Books não respondeu' if estado['google_fora'] else 'acabou o tempo')
    print('Resultado: ' + ' · '.join(f'{n} {o}' for o, n in sorted(cont.items())) + f' · {len(falhas)} consulta(s) falharam'
          + (f' · {adiados} ficaram para a próxima execução ({motivo})' if adiados else ''))
    for t, e in falhas[:10]:
        print(f'   falhou: {t} — {e}')
    return 1 if estado['desistiu'] or estado['isbn_fora'] or estado['apple_fora'] or estado['google_fora'] else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
