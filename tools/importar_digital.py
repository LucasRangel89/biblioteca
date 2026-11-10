#!/usr/bin/env python3
"""Biblioteca virtual (os livros digitais) → inventário → Catálogo Mestre.

    python tools/importar_digital.py              atualiza inventário, catálogo e resumo
    python tools/importar_digital.py --conferir   só mostra o que mudaria; não grava nada

O que faz (pode rodar quantas vezes quiser: se nada mudou, nenhum arquivo é alterado):

 1. lê as listagens das pastas (biblioteca-virtual/listagens/*.txte — a saída de `dir /b` de cada pasta);
 2. confere com o inventário (biblioteca-virtual/inventario.tsv, uma linha por arquivo):
      · arquivo que ainda não está no inventário entra com título e autor deduzidos do nome e a observação "novo";
      · arquivo que sumiu da listagem recebe a observação "ausente" (a linha fica; some do catálogo);
 3. atualiza o Catálogo Mestre:
      · livro que já estava catalogado (estante ou recomendação) ganha #tenho-digital;
      · os demais livros entram na seção 17, separados por eixo;
      · o antigo #ja-tenho vira #tenho-fisico;
 4. escreve biblioteca-virtual/RESUMO.md (o que entrou, o que falta conferir, o que ficou de fora).

Quadrinhos: nas pastas de HQ, cada subpasta guarda uma série, e também vira uma linha do inventário (formato "pasta").
No catálogo a série é uma linha só, sejam quantas forem as edições: os arquivos soltos e a pasta de uma mesma série têm
o mesmo título e o mesmo autor no inventário. A exceção é a subpasta que não é uma série, e sim outra pasta da
biblioteca, com a sua listagem (SUBPASTAS_LISTADAS): o que há nela entra por essa listagem.

O inventário é a parte feita à mão: título, autor, eixo e gênero de cada arquivo foram revisados ali.
Para corrigir um livro digital, corrija a linha dele no inventário e rode este script de novo.
"""
import collections, csv, io, pathlib, re, sys, unicodedata

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from parse_catalog import SRC as CATALOGO, parse          # noqa: E402

DIGITAL = RAIZ / 'biblioteca-virtual'
LISTAGENS = DIGITAL / 'listagens'
INVENTARIO = DIGITAL / 'inventario.tsv'
RESUMO = DIGITAL / 'RESUMO.md'

COLUNAS = ['pasta', 'arquivo', 'formato', 'tipo', 'titulo', 'autor', 'catalogo', 'eixo', 'genero', 'obs']
TIPOS_CATALOGO = {'livro', 'hq'}                # o que entra no catálogo; apostila, periódico, artigo e outro ficam só no inventário
EXT_ARQUIVO = {'epub', 'pdf', 'mobi', 'azw3', 'azw', 'djvu', 'doc', 'docx', 'rtf', 'txt', 'cbr', 'cbz', 'rar', 'zip', '7z'}
PASTAS_HQ = {'HQs', 'novashqs', 'novasHQSS', 'novas'}   # pastas de quadrinhos ('novas' é a subpasta de novashqs; a listagem dela chama-se novasHQSS)
# Subpasta de uma pasta de quadrinhos que não é uma série: é outra pasta da biblioteca, e a listagem dela tem outro nome.
# {(listagem da pasta, subpasta): listagem da subpasta} — quem sabe disso é o dono da biblioteca (resposta de 10/11/2026).
SUBPASTAS_LISTADAS = {('novashqs', 'novas'): 'novasHQSS'}
FORMATO_PASTA = 'pasta'                         # coluna `formato` de uma subpasta: nas pastas de quadrinhos, cada subpasta é uma série
LISTAGEM_E_BAT = re.compile(r'\.(txte|bat)$', re.I)   # a própria listagem e o programa que a gera aparecem em toda pasta
SEM_AUTOR = '(autor não informado)'
SECAO_DIGITAL = 17

# pasta → (eixo padrão, gênero padrão, marcadores). Vale para arquivos novos; o que já está no inventário foi revisado um a um.
# Pastas mistas não têm eixo padrão: o arquivo novo entra "a classificar".
PASTAS = {
    'pasta livros': (None, '', ''), 'pasta ficcao e literatura': (None, 'F', ''), 'nao ficcao': (None, 'NF', ''),
    'Contos e cronicas': (None, 'F', 'contos'), 'o livro d': (None, 'NF', 'introducao'),
    'ficcao cientifica e fantasia': (2, 'F', ''), 'classicos e epicos': (3, 'F', 'classico'),
    'literatura contemporanea e estrangeira': (5, 'F', 'contemporaneo'), 'ficcao de guerra e historica': (6, 'F', 'romance-historico'),
    'suspense e thriller': (7, 'F', 'thriller'), 'Terror e horror': (7, 'F', 'horror'), 'poesia': (8, 'poesia', ''),
    'Filosofia': (9, 'NF', 'filosofia'), '90min': (9, 'NF', 'introducao'),
    'Neurociencias e psicologia biologica': (10, 'NF', 'neurociencia'), 'Sociedade e politica': (11, 'NF', 'politica'),
    'historia': (12, 'NF', 'historia'), 'sociologia e antropologia': (12, 'NF', ''),
    'ciencias': (13, 'NF', 'ciencia'), 'fisica e astronomia': (13, 'NF', 'ciencia fisica'), 'I.A': (13, 'NF', 'ia'),
    'tecnologia e informacao': (13, 'NF', 'tecnologia'),
    'psicologia': (14, 'NF', 'psicologia'), 'psicanalise': (14, 'NF', 'psicanalise'),
    'avaliacao psicologica e psicometria': (14, 'NF', 'psicologia psicometria'), 'behaviorismo': (14, 'NF', 'psicologia behaviorismo'),
    'historia fundamentos e introducoes psico': (14, 'NF', 'psicologia introducao'), 'psicologia analitica': (14, 'NF', 'psicologia psicologia-analitica'),
    'psicologia clinica e psicopatologia': (14, 'NF', 'psicologia psicopatologia'), 'psico cognitivo comportamental': (14, 'NF', 'psicologia tcc'),
    'psico humanista e fenomenologica': (14, 'NF', 'psicologia psicologia-humanista'), 'psicologia social e cultural': (14, 'NF', 'psicologia psicologia-social'),
    'autoconhecimento e desenvolvimento pessoal': (14, 'NF', 'autoconhecimento'),
    'Religiao espiritualidade e mitologia': (15, 'NF', 'religiao'), 'artes e cultura': (16, 'NF', 'arte'),
}
PALAVRA_TAG = {'sociologia e antropologia': (('antropolog', 'antropologia'), ('sociolog', 'sociologia'))}   # nestas pastas o marcador sai do título
GENEROS = {'F': 'F', 'NF': 'NF', 'poesia': 'poesia', 'HQ': 'HQ'}
# marcadores que este script põe e tira sozinho na seção 17; qualquer outro, acrescentado à mão, é preservado
TAGS_GERADAS = {'tenho-digital', 'verificar', *GENEROS.values(), *(t for p in PASTAS.values() for t in p[2].split()),
                *(t for regras in PALAVRA_TAG.values() for _, t in regras)}


# ───────────────────────── texto ─────────────────────────
def chave(s):
    """Chave de comparação: sem acento, minúsculas, só letras e números."""
    s = ''.join(c for c in unicodedata.normalize('NFD', s or '') if unicodedata.category(c) != 'Mn').lower().replace('&', ' e ')
    return ' '.join(re.sub(r'[^a-z0-9]+', ' ', s).split())


def _sobrenomes(a):
    fora = {'jr', 'junior', 'filho', 'neto', 'org', 'orgs', 'outros'}
    out = set()
    for p in re.split(r',|;| e (?=[A-ZÀ-Ý])| / ', a.replace(' & ', ' e ')):
        k = [w for w in chave(p).split() if w not in fora]
        if k:
            out.update((k[-1], k[0]))
    return out


def autores_compativeis(a, b):
    """Mesmo autor escrito de outro jeito ('Carl G. Jung' × 'C. G. Jung')? Autor em branco combina com qualquer um."""
    a, b = ('' if x == SEM_AUTOR else x for x in (a, b))
    if not chave(a) or not chave(b):
        return True
    return bool(_sobrenomes(a) & _sobrenomes(b)) or chave(a) in chave(b) or chave(b) in chave(a)


def ler_texto(caminho):
    b = pathlib.Path(caminho).read_bytes()
    if b[:2] in (b'\xff\xfe', b'\xfe\xff'):
        return b.decode('utf-16')
    for cod in ('utf-8-sig', 'cp850'):
        try:
            return b.decode(cod)
        except UnicodeDecodeError:
            pass
    return b.decode('cp850', errors='replace')


def gravar(caminho, texto, conferir):
    """Grava só se o conteúdo mudou. Devolve True quando houve (ou haveria) alteração."""
    caminho = pathlib.Path(caminho)
    atual = caminho.read_text(encoding='utf-8') if caminho.exists() else None
    if atual == texto:
        return False
    if not conferir:
        with open(caminho, 'w', encoding='utf-8', newline='\n') as f:
            f.write(texto)
    return True


# ───────────────────────── listagens ─────────────────────────
def pasta_de_hq(nome):
    """A pasta é de quadrinhos? As conhecidas e qualquer listagem nova com HQ, mangá, quadrinho ou gibi no nome."""
    k = chave(nome).replace(' ', '')
    return nome in PASTAS_HQ or any(p in k for p in ('hq', 'manga', 'quadrinho', 'gibi'))


def extensao(nome):
    """Extensão de um arquivo de livro ('pdf', 'cbr'…); '' para uma subpasta e para arquivos de outro tipo."""
    m = re.search(r'\.([A-Za-z0-9]{2,5})$', nome)
    return m.group(1).lower() if m and m.group(1).lower() in EXT_ARQUIVO else ''


def _outro_arquivo(nome):
    """Tem cara de arquivo (termina em ponto e extensão com alguma letra), mas não é de livro: .bat, .html, .jpg…"""
    m = re.search(r'\.([A-Za-z0-9]{2,5})$', nome)
    return bool(m and re.search(r'[A-Za-z]', m.group(1)) and m.group(1).lower() not in EXT_ARQUIVO)


def _linhas_da_listagem(arq):
    for linha in ler_texto(arq).replace('\r', '').split('\n'):
        linha = re.sub(r'[\x00-\x1f]', ' ', linha.replace('\x07', '•')).strip()        # o `dir` escreve "•" como o caractere de controle 7
        if linha:
            yield linha


def _arquivos_de_listagem(pasta):
    return sorted(pathlib.Path(pasta).glob('*.txte'), key=lambda p: p.name.lower())


def subpastas_listadas(nomes):
    """Das subpastas de quadrinhos com listagem própria (SUBPASTAS_LISTADAS), as que valem para as listagens de nome
    `nomes`: {(listagem, subpasta): listagem da subpasta}. Se a listagem da subpasta não estiver entre elas, a subpasta
    volta a ser uma linha do inventário — fica à vista, em vez de sumir sem aviso."""
    return {par: alvo for par, alvo in SUBPASTAS_LISTADAS.items() if par[0] in nomes and alvo in nomes}


def ler_listagens(pasta=LISTAGENS):
    """{nome da listagem: [linhas]} — os arquivos de livro de cada pasta e, nas pastas de quadrinhos, também as subpastas
    (cada uma guarda uma série). Ficam de fora o .bat, as próprias listagens e os arquivos de outro tipo; nas pastas de
    livros, também as subpastas (são outras pastas da biblioteca, cada uma com a sua listagem); nas de quadrinhos, a
    subpasta que tem listagem própria (ver `subpastas_listadas`)."""
    arquivos = _arquivos_de_listagem(pasta)
    proprias = subpastas_listadas({arq.stem for arq in arquivos})
    out = collections.OrderedDict()
    for arq in arquivos:
        hq = pasta_de_hq(arq.stem)
        out[arq.stem] = [l for l in _linhas_da_listagem(arq)
                         if extensao(l) or (hq and not _outro_arquivo(l) and (arq.stem, l) not in proprias)]
    return out


def outros_arquivos(pasta=LISTAGENS):
    """[(listagem, nome)] dos arquivos que não são de livro nem de quadrinho (um .html, uma imagem…), para o resumo."""
    return [(arq.stem, l) for arq in _arquivos_de_listagem(pasta) for l in _linhas_da_listagem(arq)
            if _outro_arquivo(l) and not LISTAGEM_E_BAT.search(l)]


# ───────────────────────── inventário ─────────────────────────
def ler_inventario(caminho=INVENTARIO):
    if not pathlib.Path(caminho).exists():
        return []
    b = pathlib.Path(caminho).read_bytes()
    texto = b.decode('utf-16') if b[:2] in (b'\xff\xfe', b'\xfe\xff') else b.decode('utf-8-sig')
    linhas = list(csv.reader(io.StringIO(texto, newline=''), delimiter='\t'))
    if not linhas:
        return []
    cab = [c.strip().lower() for c in linhas[0]]
    falta = [c for c in COLUNAS if c not in cab]
    if falta:
        sys.exit(f'{caminho}: faltam as colunas {", ".join(falta)}')
    out = []
    for n, cel in enumerate(linhas[1:], 2):
        if not any(c.strip() for c in cel):
            continue
        r = {c: (cel[i].strip() if i < len(cel) else '') for i, c in enumerate(cab)}
        if not r['arquivo'] or not r['titulo']:
            sys.exit(f'{caminho}, linha {n}: arquivo e título são obrigatórios')
        out.append(r)
    return out


def texto_inventario(linhas):
    s = io.StringIO(newline='')
    w = csv.writer(s, delimiter='\t', lineterminator='\n', quoting=csv.QUOTE_MINIMAL)
    w.writerow(COLUNAS)
    for r in linhas:
        w.writerow([r.get(c, '') for c in COLUNAS])
    return s.getvalue()


def tem_obs(r, palavra):
    return palavra in re.split(r'[\s,;]+', r.get('obs', '').lower())


def _muda_obs(r, palavra, por):
    ps = [p for p in re.split(r'[\s,;]+', r.get('obs', '')) if p and p.lower() != palavra]
    r['obs'] = ' '.join(ps + [palavra] if por else ps)


# título e autor a partir do nome do arquivo (só para arquivos novos; o resultado entra marcado "novo", para revisão)
_MINUSCULAS = set('a o as os e de da do das dos em no na nos nas um uma para por pelo pela com sem que se ao aos à às ou é sobre sob entre até como seu sua '
                  'seus suas contra of the and in to for on y el la del los las en'.split())
_ORIGEM = re.compile(r'\s*\((?:z-library[^)]*|z-lib\.org|PDFDrive|Portuguese Edition|Em Portugues do Brasil)\)\s*$|\s*-\s*libgen\.li\s*$|[-_ ]+Z-Library_?$', re.I)


def caixa_titulo(t):
    out, inicio = [], True
    for w in t.split():
        if inicio or w.lower() not in _MINUSCULAS:
            sigla = (w.isupper() and 1 < len(w) < 6 and not t.isupper()) or re.fullmatch(r'(?:[A-ZÀ-Ý]\.){2,}\W*', w)   # "ONU", "B.P.D.P.:"
            w = w if sigla else w[:1].upper() + (w[1:].lower() if w.isupper() else w[1:])
        else:
            w = w.lower()
        out.append(w)
        inicio = w.endswith((':', '—', '–', '?', '!'))
    return ' '.join(out)


def deduzir(nome):
    base = re.sub(r'\.[A-Za-z0-9]{2,5}$', '', nome)
    libgen = bool(re.search(r'-\s*libgen\.li\s*$', base, re.I))
    veio_de_acervo = bool(_ORIGEM.search(base))
    for _ in range(3):
        base = re.sub(r'\s*\(\d\)\s*$', '', _ORIGEM.sub('', base))
    titulo, autor = base, ''
    m = re.match(r'^(.*\S)\s*\(([^()]{3,80})\)$', base)
    if libgen and ' - ' in base:                               # "Autor - Título (ano, editora)"
        autor, titulo = re.sub(r'\s*\(\d{4}[^()]*\)\s*$', '', base).split(' - ', 1)
    elif veio_de_acervo and m:                                 # "Título (Autor)"
        titulo, autor = m.group(1), m.group(2)
    elif ' - ' in base:                                         # "Título - Autor"
        titulo, autor = base.rsplit(' - ', 1)
    if re.search(r'\d', autor) or len(autor.split()) > 8:
        titulo, autor = base, ''
    titulo = re.sub(r'\s+', ' ', re.sub(r'_\s', ': ', titulo).replace('_', ' ')).strip(' -.,;:')
    autor = re.sub(r'\s+', ' ', autor.replace('_', ' ')).strip(' -,;:')
    autor = re.sub(r'(?<![A-ZÀ-Ý])\.$', '', autor)             # ponto final, mas não o de uma inicial ("J.R.R.")
    m = re.match(r'^([^,]+), ([^,]+)$', autor)                 # "Sobrenome, Nome"
    if m and len(m.group(1).split()) == 1:
        autor = f'{m.group(2)} {m.group(1).capitalize() if m.group(1).isupper() else m.group(1)}'
    return caixa_titulo(titulo), autor


_GRUPO = re.compile(r'[\[({][^\[\](){}]*[\])}]')            # "(2021)", "[grupo que digitalizou]", "(13 de 15)"
_EDICAO = re.compile(r"#\s*\d"                                                               # "#01"
                     r"|\b(?:v|vol|volume|livro|tomo|parte|n[ºo°])\.?\s*(?:\d+|[IVX]+)\b"       # "v2", "Vol. 3", "Livro II"
                     r"|\b\d+\s*de\s*\d+\b"                                                  # "01 de 03"
                     r"|(?<![\w'’.])0\d+\b", re.I)                                           # "001", "07": número com zero à esquerda
_NUMERO_SOLTO = re.compile(r'(?<=\s)\d+(?=\s|$)')


def deduzir_hq(nome):
    """Título (e autor, se o nome traz) de um arquivo ou de uma subpasta de quadrinhos. O título é o da série: saem a marca
    de quem digitalizou, o ano e o número da edição — "Coda #03 [Grupo].cbr" e "Coda #04 (2019).cbr" dão os dois "Coda"."""
    base, arquivo = nome, bool(extensao(nome))
    while extensao(base):                                       # "… .rar.cbr"
        base = base[:base.rindex('.')]
    if arquivo and _ORIGEM.search(base):                        # baixado de um acervo: "Título (Autor) (Z-Library)"
        return deduzir(nome)
    base = re.sub(r'-\d{8}T\d{6}Z-\d+$', '', base)              # pasta baixada do Google Drive: "…-20241229T204405Z-001"
    for _ in range(4):
        base = _GRUPO.sub(' ', base)
    base = base.strip()
    pontuado = not re.search(r'\s', base) and bool(re.search(r'[^\W\d_]{2,}\.[^\W_]', base))   # "As.Eras.Perdidas.01"
    if pontuado:
        base = base.replace('.', ' ')
    cortes = [m.start() for m in (_EDICAO.search(base, 1), _NUMERO_SOLTO.search(base, 1) if pontuado else None) if m]
    if cortes and base[:min(cortes)].strip(' -–.,;:_'):
        base = base[:min(cortes)]
    base = re.sub(r'[\s\-–]*\bcomplet[oa]\s*$', '', base.replace('_', ' '), flags=re.I)
    base = re.sub(r'\s+', ' ', re.sub(r'\s*[-–]\s+', ': ', base)).strip(' -–,;:')
    return caixa_titulo(base), ''


def series_de_hq(inventario):
    """{chave do nome: linha} das séries de quadrinhos do inventário, para reconhecer mais uma edição de uma série que já
    está lá. Vale o título da série e, depois, o nome que se deduz de cada arquivo ou subpasta dela ("Kingsway West #01"
    leva a "Kingsway Oeste"). Um nome que serve a duas séries diferentes não leva a nenhuma."""
    por_titulo, por_nome = collections.defaultdict(dict), collections.defaultdict(dict)
    for r in inventario:
        if r['tipo'] == 'hq' and not tem_obs(r, 'ausente'):
            obra = (chave(r['catalogo'] or r['titulo']), chave(r['autor']))
            por_titulo[chave(r['titulo'])].setdefault(obra, r)
            por_nome[chave(deduzir_hq(r['arquivo'])[0])].setdefault(obra, r)
    unica = lambda por: {k: next(iter(v.values())) for k, v in por.items() if k and len(v) == 1}
    return {**{k: r for k, r in unica(por_nome).items() if k not in por_titulo}, **unica(por_titulo)}


def _linha_nova(pasta, nome, series):
    """A linha de inventário de um arquivo (ou de uma subpasta de quadrinhos) que apareceu na listagem."""
    if not pasta_de_hq(pasta):
        eixo, genero, _ = PASTAS.get(pasta, (None, '', ''))
        titulo, autor = deduzir(nome)
        return dict(pasta=pasta, arquivo=nome, formato=extensao(nome), tipo='livro', titulo=titulo, autor=autor,
                    catalogo='', eixo=str(eixo or ''), genero=genero, obs='novo')
    titulo, autor = deduzir_hq(nome)
    r = dict(pasta=pasta, arquivo=nome, formato=extensao(nome) or FORMATO_PASTA, tipo='hq', titulo=titulo, autor=autor,
             catalogo='', eixo='', genero='HQ', obs='novo')
    serie = series.get(chave(titulo))
    if serie:                                                   # mais uma edição de uma série conhecida: herda os dados dela
        r.update(titulo=serie['titulo'], autor=serie['autor'], catalogo=serie['catalogo'], eixo=serie['eixo'],
                 obs='novo' if tem_obs(serie, 'novo') else '')
    return r


def sincronizar(inventario, listagens):
    """Compara inventário e listagens. Altera o inventário no lugar e devolve (novos, ausentes, de_volta, pastas_sem_listagem)."""
    conhecidos = {(r['pasta'], r['arquivo']) for r in inventario}
    series = series_de_hq(inventario)
    novos, ausentes, de_volta = [], [], []
    for pasta, nomes in listagens.items():
        for nome in nomes:
            if (pasta, nome) in conhecidos:
                continue
            conhecidos.add((pasta, nome))
            r = _linha_nova(pasta, nome, series)
            inventario.append(r)
            novos.append(r)
    sem_listagem = sorted({r['pasta'] for r in inventario} - set(listagens), key=str.lower)
    for r in inventario:
        if r['pasta'] not in listagens:
            continue
        presente = r['arquivo'] in listagens[r['pasta']]
        if not presente and not tem_obs(r, 'ausente'):
            _muda_obs(r, 'ausente', True)
            ausentes.append(r)
        elif presente and tem_obs(r, 'ausente'):
            _muda_obs(r, 'ausente', False)
            de_volta.append(r)
    return novos, ausentes, de_volta, sem_listagem


# ───────────────────────── obras ─────────────────────────
def obras_do_inventario(inventario):
    """Agrupa as linhas do inventário em obras (um livro pode estar em vários arquivos, formatos e pastas).
    A obra é identificada pelo título de catálogo (coluna `catalogo`, se houver; senão `titulo`) e pelo autor."""
    obras = collections.OrderedDict()
    for r in inventario:
        if r['tipo'] not in TIPOS_CATALOGO or tem_obs(r, 'ausente'):
            continue
        titulo = r['catalogo'] or r['titulo']
        k = (chave(titulo), chave(r['autor']))
        o = obras.get(k)
        if o is None:
            o = obras[k] = {'t': titulo, 'a': r['autor'], 'linhas': []}
        o['linhas'].append(r)
    for o in obras.values():
        L = o['linhas']
        arquivos = [r for r in L if r['formato'] != FORMATO_PASTA]
        o['formatos'] = sorted({r['formato'] for r in arquivos})
        o['pastas'] = list(dict.fromkeys(r['pasta'] for r in L))
        o['arquivos'] = len({(r['pasta'], r['arquivo']) for r in arquivos})
        o['subpastas'] = list(dict.fromkeys(r['arquivo'] for r in L if r['formato'] == FORMATO_PASTA))     # séries guardadas em pasta própria
        o['edicoes'] = list(dict.fromkeys(r['titulo'] for r in L if r['catalogo'] and chave(r['titulo']) != chave(o['t'])))
        eixos = collections.Counter(int(r['eixo']) for r in L if r['eixo'].isdigit() and 1 <= int(r['eixo']) <= 16)
        o['eixo'] = eixos.most_common(1)[0][0] if eixos else 0
        generos = collections.Counter(r['genero'] for r in L if r['genero'] in GENEROS)
        o['genero'] = 'HQ' if all(r['tipo'] == 'hq' for r in L) else (generos.most_common(1)[0][0] if generos else '')
        o['verificar'] = any(tem_obs(r, 'verificar') or tem_obs(r, 'novo') for r in L)
    return obras


def casar(obras, livros):
    """Liga cada obra do inventário à linha do catálogo que tem o mesmo título e autor compatível.
    `livros`: lista de dicts com 't', 'a' e, se houver, 'tags'. Devolve {posição em `livros`: [obras]} e a lista das obras sem linha.
    Um quadrinho só se liga a uma linha marcada #HQ: a adaptação de um romance não é o romance, mesmo com o título igual."""
    por_titulo = collections.defaultdict(list)
    for i, b in enumerate(livros):
        por_titulo[chave(b['t'])].append(i)
    ligadas, soltas = collections.defaultdict(list), []
    for (kt, ka), o in obras.items():
        cand = [i for i in por_titulo.get(kt, []) if o['genero'] != 'HQ' or 'HQ' in livros[i].get('tags', ('HQ',))]
        iguais = [i for i in cand if chave('' if livros[i]['a'] == SEM_AUTOR else livros[i]['a']) == ka]
        compat = [i for i in cand if autores_compativeis(livros[i]['a'], o['a'])]
        alvo = iguais[0] if iguais else compat[0] if len(compat) == 1 else None
        if alvo is None:
            soltas.append(o)
        else:
            ligadas[alvo].append(o)
    return ligadas, soltas


def tags_da_obra(o, a_mao=()):
    """Marcadores de uma linha da seção 17, na ordem do resto do catálogo: tipo, temas, os postos à mão, pendências, posse."""
    tags = [GENEROS[o['genero']]] if o['genero'] else []
    ficcao = lambda g: g in ('F', 'poesia', 'HQ')
    for pasta in o['pastas']:
        _, genero_pasta, da_pasta = PASTAS.get(pasta, (None, '', ''))
        if genero_pasta and o['genero'] and ficcao(genero_pasta) != ficcao(o['genero']):
            continue                                            # livro guardado na pasta "errada": o marcador da pasta não vale
        achados = [t for trecho, t in PALAVRA_TAG.get(pasta, ()) if trecho in chave(o['t'])]
        tags += [t for t in da_pasta.split() + achados if t not in tags]
    tags += [t for t in a_mao if t not in tags]
    return tags + (['verificar'] if o['verificar'] else []) + ['tenho-digital']


# ───────────────────────── catálogo ─────────────────────────
_LINHA = re.compile(r'^\|(.*)\|\s*$')


def _celulas(linha):
    m = _LINHA.match(linha)
    if not m:
        return None
    c = [x.strip() for x in m.group(1).split('|')]
    if len(c) != 3 or c[0] in ('Título', '') or set(c[0]) <= set('-: '):
        return None
    return c


def _linha(titulo, autor, tags):
    return f'| {titulo} | {autor} | {" ".join("#" + t for t in tags)} |'


def _tags(celula):
    return [t.lstrip('#') for t in celula.split() if t.startswith('#')]


def atualizar_catalogo(md, obras):
    """Devolve (novo texto do catálogo, relatório)."""
    L = md.split('\n')
    sec, nomes, linhas = None, {}, []                           # linhas: (índice, seção, [título, autor, tags])
    for i, linha in enumerate(L):
        m = re.match(r'^##\s+(\d+)\.\s+(.*)$', linha)
        if m:
            sec = int(m.group(1)); nomes[sec] = m.group(2).strip()
        elif linha.startswith('## '):
            sec = None
        elif sec is not None:
            c = _celulas(linha)
            if c:
                linhas.append((i, sec, c))
    fixas = [(i, s, c) for i, s, c in linhas if s != SECAO_DIGITAL]
    rel = {'renomeadas': 0, 'marcadas': 0, 'ja_marcadas': 0, 'fisico_e_digital': [], 'recomendados': [], 'orfas': [], 'tags_perdidas': []}

    # 1 ▸ #ja-tenho → #tenho-fisico; #tenho-digital nos livros já catalogados
    ligadas, soltas = casar(obras, [{'t': c[0], 'a': c[1], 'tags': _tags(c[2])} for _, _, c in fixas])
    for n, (i, s, c) in enumerate(fixas):
        tags = _tags(c[2])
        novas = ['tenho-fisico' if t == 'ja-tenho' else t for t in tags]
        rel['renomeadas'] += novas != tags
        if n in ligadas:
            if 'tenho-digital' in novas:
                rel['ja_marcadas'] += 1
            else:
                rel['marcadas'] += 1
                p = novas.index('tenho-fisico') + 1 if 'tenho-fisico' in novas else len(novas)
                novas.insert(p, 'tenho-digital')
            (rel['fisico_e_digital'] if 'tenho-fisico' in novas else rel['recomendados']).append((c[0], c[1], s, ligadas[n]))
        elif 'tenho-digital' in novas:
            rel['orfas'].append((c[0], c[1]))
        if novas != tags:
            L[i] = _linha(c[0], c[1], novas)

    # 2 ▸ seção 17, refeita a partir do inventário (marcadores postos à mão nas linhas antigas são mantidos)
    extras = {}
    for i, s, c in linhas:
        if s == SECAO_DIGITAL:
            mais = [t for t in _tags(c[2]) if t not in TAGS_GERADAS]
            if mais:
                extras[(chave(c[0]), chave('' if c[1] == SEM_AUTOR else c[1]))] = (c[0], mais)
    por_eixo = collections.defaultdict(list)
    for o in soltas:
        k = (chave(o['t']), chave(o['a']))
        tags = tags_da_obra(o, extras.pop(k, (None, []))[1])
        por_eixo[o['eixo']].append((chave(o['t']), _linha(o['t'].replace('|', '/'), (o['a'] or SEM_AUTOR).replace('|', '/'), tags)))
    rel['tags_perdidas'] = sorted(extras.values())
    rel['secao17'] = {e: len(v) for e, v in sorted(por_eixo.items())}
    rel['secao17_hq'] = dict(collections.Counter(o['eixo'] for o in soltas if o['genero'] == 'HQ'))
    rel['nomes'] = nomes
    bloco = [f'## {SECAO_DIGITAL}. Biblioteca virtual (tenho: digital)', '',
             'Livros e quadrinhos da biblioteca virtual que não estavam nas seções anteriores, separados pelos mesmos eixos. Os que já '
             'estavam catalogados continuam na seção de origem e ganharam `#tenho-digital`. Os quadrinhos levam `#HQ`; uma série é uma '
             'linha só, sejam quantas forem as edições.', '',
             '> Seção gerada por `tools/importar_digital.py` a partir de `biblioteca-virtual/inventario.tsv`. Para corrigir título, autor ou eixo, '
             'corrija o inventário e rode o script; aqui, só os marcadores acrescentados à mão (`#lido`, `#top`, temas…) são preservados.', '']
    for e in sorted(por_eixo, key=lambda e: (e == 0, e)):
        nome = nomes.get(e, f'Eixo {e}') if e else 'A classificar (sem eixo no inventário)'
        bloco += [f'### {SECAO_DIGITAL}.{e} {nome}', '', '| Título | Autor | Tags |', '|---|---|---|']
        bloco += [linha for _, linha in sorted(por_eixo[e])]
        bloco.append('')
    bloco += ['---', '']

    ini = next((i for i, l in enumerate(L) if re.match(rf'^##\s+{SECAO_DIGITAL}\.\s', l)), None)
    if ini is not None:
        fim = next((i for i in range(ini + 1, len(L)) if L[i].startswith('## ')), len(L))
    else:
        ini = fim = next((i for i, l in enumerate(L) if l.startswith('## Como usar')), len(L))
        if fim == len(L):                                       # catálogo sem a seção final: a 17 vai para o fim
            bloco = ['', '---', ''] + bloco[:-2]
    if not soltas:
        bloco = []
    return '\n'.join(L[:ini] + bloco + L[fim:]), rel


# ───────────────────────── resumo ─────────────────────────
def _subpasta_sem_listagem(r):
    """Subpasta que não é uma série: é outra pasta de quadrinhos, ainda sem listagem (no inventário, tipo `outro`).
    A que tem listagem própria nem chega ao inventário (ver `subpastas_listadas`)."""
    return r['formato'] == FORMATO_PASTA and r['tipo'] not in TIPOS_CATALOGO


def contar(inventario, obras):
    """Os números do inventário: arquivos, subpastas de séries de quadrinhos, pastas e obras (livros e quadrinhos)."""
    ativos = list({(r['pasta'], r['arquivo']): r for r in inventario if not tem_obs(r, 'ausente')}.values())
    hq = sum(o['genero'] == 'HQ' for o in obras.values())
    return {'arquivos': sum(r['formato'] != FORMATO_PASTA for r in ativos),
            'series': sum(r['formato'] == FORMATO_PASTA and r['tipo'] == 'hq' for r in ativos),
            'pastas': len({r['pasta'] for r in ativos}), 'obras': len(obras), 'livros': len(obras) - hq, 'hq': hq}


def _plural(n, um, varios):
    return f'{n} {um if n == 1 else varios}'


def texto_resumo(inventario, obras, rel, listagens, sem_listagem, outros=()):
    ativos = [r for r in inventario if not tem_obs(r, 'ausente')]
    por_tipo = collections.Counter()
    for r in ativos:
        por_tipo[r['tipo']] += 1
    fmt = collections.Counter(r['formato'] for r in {(r['pasta'], r['arquivo']): r for r in ativos}.values() if r['formato'] != FORMATO_PASTA)
    nomes = rel['nomes']
    n17 = sum(rel['secao17'].values())
    N = contar(inventario, obras)
    T = ['# Biblioteca virtual — resumo da importação', '',
         'Gerado por `tools/importar_digital.py`. Não edite: é refeito a cada execução.', '',
         '## Números', '',
         f'- **{N["arquivos"]} arquivos** no inventário ({", ".join(f"{n} {e}" for e, n in fmt.most_common())})'
         + (f' e **{_plural(N["series"], "pasta", "pastas")} de séries** de quadrinhos (cada uma guarda as edições de uma série)' if N['series'] else '')
         + f', em {N["pastas"]} pastas.',
         f'- **{N["obras"]} obras** diferentes: **{_plural(N["livros"], "livro", "livros")}** e **{_plural(N["hq"], "quadrinho", "quadrinhos")}**. O mesmo livro em dois '
         'formatos, ou em duas pastas, conta uma vez; uma série de quadrinhos conta uma vez, sejam quantas forem as edições.',
         f'- **{len(rel["fisico_e_digital"])}** delas também estão na estante física (`#tenho-fisico #tenho-digital`).',
         f'- **{len(rel["recomendados"])}** estavam entre as recomendações do catálogo e agora aparecem como `#tenho-digital`.',
         f'- **{n17}** são novas no catálogo: entraram na seção 17.']
    fora = [(t, n) for t, n in sorted(por_tipo.items()) if t not in TIPOS_CATALOGO]
    if fora:
        T.append(f'- Ficaram só no inventário, fora do catálogo: {", ".join(f"{n} {t}" for t, n in fora)} (linhas do inventário).')
    for (pai, sub), alvo in sorted(subpastas_listadas(set(listagens)).items()):
        T.append(f'- A subpasta `{sub}`, de `{pai}`, tem listagem própria, `{alvo}`: o que há nela está contado nessa pasta.')
    hq17 = rel.get('secao17_hq', {})
    T += ['', '## Seção 17, por eixo', '', '| Eixo | Livros | Quadrinhos |', '|---|---|---|']
    T += [f'| {f"{e}. " + nomes.get(e, "") if e else "A classificar"} | {n - hq17.get(e, 0)} | {hq17.get(e, 0)} |'
          for e, n in sorted(rel['secao17'].items(), key=lambda x: (x[0] == 0, x[0]))]

    def lista(titulo, intro, itens):
        if itens:
            T.extend(['', f'## {titulo}', '', intro, ''] + itens)

    lista('Tenho nos dois formatos', 'Livros da estante física que também estão na biblioteca virtual.',
          [f'- {t} — {a}' for t, a, _, _ in rel['fisico_e_digital']])
    lista('Recomendações que já tenho em digital', 'Estavam no catálogo como recomendação; continuam na seção de origem, agora com `#tenho-digital`.',
          [f'- {t} — {a} (seção {s})' for t, a, s, _ in sorted(rel['recomendados'], key=lambda x: (x[2], chave(x[0])))])
    difer = sorted({(r['titulo'], r['catalogo']) for r in ativos if r['tipo'] in TIPOS_CATALOGO and r['catalogo']}, key=lambda x: (chave(x[1]), chave(x[0])))
    lista('Edições com título diferente do catálogo', 'O arquivo tem um título; a linha do catálogo, outro. Confira se é mesmo o mesmo livro '
          '(se não for, apague a coluna `catalogo` da linha no inventário).', [f'- “{t}” → catálogo: **{c}**' for t, c in difer])
    verif = sorted({(r['titulo'], r['autor'], r['pasta'], r['tipo'] in TIPOS_CATALOGO) for r in ativos if tem_obs(r, 'verificar')}, key=lambda x: chave(x[0]))
    lista('A verificar', 'Título, autor ou identificação incertos (coluna `obs` = `verificar`). Os que estão no catálogo levam `#verificar`.',
          [f'- {t} — {a or "sem autor"} · pasta `{p}`' + ('' if no_catalogo else ' · fora do catálogo') for t, a, p, no_catalogo in verif])
    novos = [r for r in ativos if tem_obs(r, 'novo')]
    lista('Arquivos novos, a revisar', 'Entraram nesta execução ou numa anterior, com título e autor deduzidos do nome do arquivo (nas pastas de '
          'quadrinhos, também do nome da subpasta). Revise a linha no inventário (tipo, título, autor, eixo, gênero) e apague `novo` da coluna `obs`.',
          [f'- `{r["pasta"]}/{r["arquivo"]}` → {r["titulo"]} — {r["autor"] or "sem autor"}' for r in novos])
    aus = [r for r in inventario if tem_obs(r, 'ausente')]
    lista('Arquivos ausentes', 'Estão no inventário, mas não aparecem mais na listagem da pasta. Se o arquivo foi apagado de propósito, apague a linha.',
          [f'- `{r["pasta"]}/{r["arquivo"]}` — {r["titulo"]}' for r in aus])
    naolivro = sorted({(r['tipo'], r['titulo'], r['pasta']) for r in ativos if r['tipo'] not in TIPOS_CATALOGO and not _subpasta_sem_listagem(r)})
    lista('Itens que não são livros', 'Apostilas, revistas, artigos e afins: ficam no inventário e não entram no catálogo.',
          [f'- {tp}: {t} · pasta `{p}`' for tp, t, p in naolivro])
    lista('Marcados `#tenho-digital` sem arquivo no inventário', 'O catálogo diz que há cópia digital, mas o inventário não tem o arquivo. '
          'Nada foi alterado; tire o marcador à mão se for engano.', [f'- {t} — {a}' for t, a in rel['orfas']])
    lista('Marcadores que ficaram sem linha', 'Linhas da seção 17 que tinham marcadores postos à mão e deixaram de existir (título ou autor mudou no inventário).',
          [f'- {t}: {" ".join("#" + x for x in tags)}' for t, tags in rel['tags_perdidas']])
    fora = []
    if N['series']:
        fora.append(f'- Edições dentro das pastas de séries: de cada uma das {N["series"]} pastas de séries de quadrinhos só o nome é conhecido. '
                    'Quantas e quais edições há dentro delas não foi conferido.')
    subpastas = [r for r in ativos if _subpasta_sem_listagem(r)]
    if subpastas:
        nomes_sub = ', '.join('`%s/%s`' % (r['pasta'], r['arquivo']) for r in subpastas)
        if len(subpastas) == 1:
            fora.append(f'- Subpasta sem listagem: {nomes_sub}. Só o nome dela é conhecido; o que há dentro não entrou. Para entrar, gere a '
                        'listagem dela e ponha em `biblioteca-virtual/listagens/`.')
        else:
            fora.append(f'- Subpastas sem listagem: {nomes_sub}. Só o nome delas é conhecido; o que há dentro não entrou. Para entrar, gere a '
                        'listagem de cada uma e ponha em `biblioteca-virtual/listagens/`.')
    if outros:
        fora.append('- Arquivos que não são livro nem quadrinho (ignorados): ' + ', '.join('`%s/%s`' % par for par in outros) + '.')
    if sem_listagem:
        fora.append(f'- Pastas do inventário sem listagem (nada foi conferido nelas): {", ".join(f"`{p}`" for p in sem_listagem)}.')
    lista('Fora desta importação', 'O que existe na biblioteca virtual e não foi conferido arquivo por arquivo.', fora)
    return '\n'.join(T) + '\n'


# ───────────────────────── execução ─────────────────────────
def main(argv):
    conferir = '--conferir' in argv
    for saida in (sys.stdout, sys.stderr):
        try: saida.reconfigure(encoding='utf-8', errors='replace')
        except Exception: pass
    listagens = ler_listagens(LISTAGENS)
    inventario = ler_inventario(INVENTARIO)
    if not inventario and not listagens:
        sys.exit(f'Não encontrei nem o inventário ({INVENTARIO}) nem as listagens ({LISTAGENS}).')
    novos, ausentes, de_volta, sem_listagem = sincronizar(inventario, listagens)
    obras = obras_do_inventario(inventario)
    md = CATALOGO.read_text(encoding='utf-8')
    novo_md, rel = atualizar_catalogo(md, obras)
    assert atualizar_catalogo(novo_md, obras)[0] == novo_md, 'a atualização do catálogo deveria ser estável'
    mudou = [nome for nome, alterado in (
        (INVENTARIO.name, gravar(INVENTARIO, texto_inventario(inventario), conferir)),
        (CATALOGO.name, gravar(CATALOGO, novo_md, conferir)),
        (RESUMO.name, gravar(RESUMO, texto_resumo(inventario, obras, rel, listagens, sem_listagem, outros_arquivos(LISTAGENS)), conferir)),
    ) if alterado]

    N = contar(inventario, obras)
    print(f'Inventário: {N["arquivos"]} arquivos' + (f' e {_plural(N["series"], "pasta", "pastas")} de séries de quadrinhos' if N['series'] else '')
          + f', {N["obras"]} obras diferentes ({_plural(N["livros"], "livro", "livros")}' + (f' e {_plural(N["hq"], "quadrinho", "quadrinhos")}' if N['hq'] else '') + ')'
          + (f' · {len(novos)} arquivo(s) novo(s)' if novos else '') + (f' · {len(ausentes)} ausente(s)' if ausentes else '')
          + (f' · {len(de_volta)} de volta' if de_volta else ''))
    for r in novos[:40]:
        print(f'   novo: {r["pasta"]}/{r["arquivo"]}  →  {r["titulo"]} — {r["autor"] or "sem autor"}'
              + ('' if tem_obs(r, 'novo') else '  (mais uma edição de uma série que já estava no inventário)'))
    if len(novos) > 40:
        print(f'   … e mais {len(novos) - 40} (lista completa em {RESUMO.name})')
    for r in ausentes[:40]:
        print(f'   ausente: {r["pasta"]}/{r["arquivo"]}')
    print(f'Catálogo: {len(rel["fisico_e_digital"])} na estante e em digital · {len(rel["recomendados"])} recomendações que já tenho em digital · '
          f'{sum(rel["secao17"].values())} na seção {SECAO_DIGITAL}'
          + (f' · {rel["marcadas"]} linha(s) marcada(s) agora' if rel['marcadas'] else '') + (f' · {rel["renomeadas"]} #ja-tenho → #tenho-fisico' if rel['renomeadas'] else ''))
    if rel['orfas']:
        print(f'Atenção: {len(rel["orfas"])} linha(s) com #tenho-digital sem arquivo no inventário (ver {RESUMO.name}).')
    if sem_listagem:
        print(f'Atenção: sem listagem para {", ".join(sem_listagem)}.')
    if mudou:
        print(('Mudaria: ' if conferir else 'Atualizado: ') + ', '.join(mudou))
        if not conferir and CATALOGO.name in mudou:
            print('Agora refaça o painel: python tools/build_catalog.py && python tools/build.py   (ou: python tools/atualizar.py)')
    else:
        print('Nada mudou.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
