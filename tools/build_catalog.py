#!/usr/bin/env python3
"""Converte o Catálogo Mestre (.md) no JSON compacto embutido no painel.

Saída: lista de [titulo, autor, "tags separadas por espaço", secao, eixo, observacao, digital, nomes antigos]
- secao:   seção original do catálogo (0 = estante física, 17 = biblioteca virtual)
- eixo:    eixo temático 1..16 (na estante, deduzido das tags — ver eixos.py; na seção 17, o número da subseção)
- digital: só nos livros que estão na biblioteca virtual (biblioteca-virtual/inventario.tsv):
           ["formatos", nº de arquivos, [pastas], [títulos das edições, quando diferem do catálogo], "identificadores dos arquivos"]
           e, nos quadrinhos guardados em pasta própria, um sexto item: [nomes das subpastas da série].
           Os identificadores deixam o painel reconhecer o livro mesmo depois de o título ser corrigido no inventário.
- nomes antigos: só nas linhas cujo título ou autor foi corrigido no catálogo (catalogo/renomeados.tsv):
           [[título antigo, autor antigo], …]. Com eles o painel reencontra o que o usuário já tinha anotado naquele livro.

Também gera:
- src/capas.json (catalogo/capas.tsv) e src/capas-fontes.json (uma letra por livro: de onde veio cada capa);
- src/trilhas.json (catalogo/trilhas.md): as trilhas de leitura, cada uma como
  [marcador, nome, descrição, [posições das linhas do catálogo, na ordem da trilha]];
- src/antes.json (catalogo/antes-da-vistoria.tsv): [posição da linha, eixo, "marcadores"] que a linha tinha no painel
  publicado antes da vistoria de 10/11/2026 — só nas linhas em que a vistoria trocou ou tirou alguma coisa;
- src/sinopses.json (catalogo/sinopses.tsv): [posição da linha, "sinopse"] dos livros que já têm sinopse.
- src/digitais.json (biblioteca-virtual/inventario.tsv): {nome do arquivo: posição da linha} de todos os
  EPUBs e CBZs dos livros ainda sem capa — é assim que o painel reconhece um arquivo na varredura de pasta.
"""
import csv, hashlib, json, pathlib, re, sys, unicodedata
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from parse_catalog import parse, SRC
from eixos import eixo_estante
import importar_digital as digital
import capas

RAIZ = pathlib.Path(__file__).resolve().parent.parent
DEST = RAIZ / 'src' / 'catalog.json'
DEST_CAPAS = RAIZ / 'src' / 'capas.json'
DEST_FONTES = RAIZ / 'src' / 'capas-fontes.json'
DEST_TRILHAS = RAIZ / 'src' / 'trilhas.json'
RENOMEADOS = RAIZ / 'catalogo' / 'renomeados.tsv'
TRILHAS = RAIZ / 'catalogo' / 'trilhas.md'
ANTES = RAIZ / 'catalogo' / 'antes-da-vistoria.tsv'
DEST_ANTES = RAIZ / 'src' / 'antes.json'
SINOPSES = RAIZ / 'catalogo' / 'sinopses.tsv'
DEST_SINOPSES = RAIZ / 'src' / 'sinopses.json'
DEST_DIGITAIS = RAIZ / 'src' / 'digitais.json'          # nome do arquivo → linha do catálogo (ver o quadro de capas)
SINOPSE_MIN, SINOPSE_MAX = 140, 400          # caracteres: as duas amostras aprovadas têm 251 e 281
_ABREV = {'dr', 'dra', 'sr', 'sra', 'prof', 'st', 'vol', 'séc', 'cap', 'ed', 'p', 'pe'}
AUTOR_FIX = {
    'Liev Tolstói (na prateleira consta Dostoiévski; autor correto: Tolstói)': ('Liev Tolstói', 'Na prateleira consta Dostoiévski; o autor correto é Tolstói.'),
    'Irvin D. Yalom (conforme a prateleira)': ('Irvin D. Yalom', 'Autoria conforme a prateleira — conferir.'),
    '(autor não informado)': ('', 'Autor não informado no catálogo.'),
    '(tradição hindu)': ('Tradição hindu', ''),
    '(tradição budista)': ('Tradição budista', ''),
    '(tradição tibetana)': ('Tradição tibetana', ''),
}
OBS = {
    'Notas do Subsolo (Memórias do Subsolo)': 'Mesmo livro conhecido como “Memórias do Subsolo”.',
    'O Xamã': '“O Xamã” e “Xamã” são o mesmo livro.',
    'A Ilha': 'Há dois livros diferentes com este título na estante (Huxley e Benchley).',
    'A Ilha (Benchley)': 'Há dois livros diferentes com este título na estante (Huxley e Benchley).',
    # informações do dono da biblioteca (11/11/2026)
    'O Chamado de Cthulhu': 'Na estante, este conto está dentro do seu livro de contos de Lovecraft: não é um volume à parte.',
    'Nas Montanhas da Loucura': 'Na estante, esta novela está dentro do seu livro de contos de Lovecraft: não é um volume à parte.',
    'A Sombra sobre Innsmouth': 'Na estante, esta novela está dentro do seu livro de contos de Lovecraft: não é um volume à parte.',
    'A Metamorfose': 'Você já leu. Tinha o livro em papel, emprestou e ele não voltou.',
}
_B36 = '0123456789abcdefghijklmnopqrstuvwxyz'


def id_arquivo(pasta, arquivo):
    """Identificador curto e estável de um arquivo da biblioteca virtual (muda só se o arquivo mudar de pasta ou de nome)."""
    n, s = int.from_bytes(hashlib.blake2s(f'{pasta}/{arquivo}'.encode('utf-8'), digest_size=4).digest(), 'big'), ''
    while n:
        n, r = divmod(n, 36)
        s = _B36[r] + s
    return s or '0'


def dados_digitais(books, avisos):
    """{posição da linha do catálogo: dados da biblioteca virtual}, cruzando o catálogo com o inventário."""
    if not digital.INVENTARIO.exists():
        return {}
    obras = digital.obras_do_inventario(digital.ler_inventario(digital.INVENTARIO))
    ligadas, soltas = digital.casar(obras, books)
    if soltas:
        avisos.append(f'{len(soltas)} livro(s) do inventário ainda sem linha no catálogo (rode tools/importar_digital.py): ' + '; '.join(o['t'] for o in soltas[:5]) + ('…' if len(soltas) > 5 else ''))
    dono, out = {}, {}
    for i, lista in ligadas.items():
        linhas = [r for o in lista for r in o['linhas']]
        ids = [id_arquivo(*a) for a in dict.fromkeys((r['pasta'], r['arquivo']) for r in linhas)]      # arquivos e subpastas de séries
        for x in ids:
            dono.setdefault(x, set()).add(i)
        arquivos = [r for r in linhas if r['formato'] != digital.FORMATO_PASTA]
        subpastas = list(dict.fromkeys(r['arquivo'] for r in linhas if r['formato'] == digital.FORMATO_PASTA))
        out[i] = [' '.join(sorted({r['formato'] for r in arquivos})), len({(r['pasta'], r['arquivo']) for r in arquivos}),
                  list(dict.fromkeys(r['pasta'] for r in linhas)), list(dict.fromkeys(t for o in lista for t in o['edicoes'])), ids]
        if subpastas:
            out[i].append(subpastas)
    for i, d in out.items():                                   # um identificador repetido entre dois livros não serve para reconhecer nenhum dos dois
        d[4] = ' '.join(x for x in d[4] if len(dono[x]) == 1)
    sem_arquivo = [b['t'] for i, b in enumerate(books) if 'tenho-digital' in b['tags'] and i not in out]
    if sem_arquivo:
        avisos.append(f'{len(sem_arquivo)} linha(s) com #tenho-digital sem arquivo no inventário: ' + '; '.join(sem_arquivo[:5]) + ('…' if len(sem_arquivo) > 5 else ''))
    sem_marca = [books[i]['t'] for i in out if 'tenho-digital' not in books[i]['tags']]
    if sem_marca:
        avisos.append(f'{len(sem_marca)} livro(s) do inventário cuja linha não tem #tenho-digital (rode tools/importar_digital.py): ' + '; '.join(sem_marca[:5]) + ('…' if len(sem_marca) > 5 else ''))
    return out


def _norm(s):
    """A normalização que o painel usa para comparar nomes (norm, em src/js/00-util.js): sem acentos e em minúsculas."""
    return ''.join(c for c in unicodedata.normalize('NFD', s or '') if not '\u0300' <= c <= '\u036f').lower()


DIGITAL_LIDO = ('.epub', '.cbz')         # os formatos de que o painel sabe tirar a capa (src/js/54-capa-digital.js)


def nomes_digitais(books, capas, avisos=None):
    """{nome do arquivo (sem acentos, em minúsculas): posição da linha do catálogo}, dos EPUBs e CBZs conhecidos.

    É a própria lista de arquivos do dono do projeto dizendo "este arquivo é deste livro": o inventário já foi conferido
    à mão, então o painel reconhece o arquivo por ele, em vez de adivinhar pelo título (e as pastas dele são categorias
    de prateleira — "Filosofia", "ficcao cientifica e fantasia" — que não significam nada para um casamento).
    · nomes que pertencem a mais de uma linha ficam de fora: não servem para reconhecer nenhuma delas (mesma regra dos
      identificadores em dados_digitais) — por isso o dono é contado antes de qualquer filtro de capa;
    · só entram os formatos que têm capa dentro (DIGITAL_LIDO) e as linhas ainda sem capa: é o que o lote pode
      aproveitar; um arquivo fora do mapa não é lido, e o resumo diz isso em palavras;
    · o mapa vai embutido no painel (const DIGITAIS_NOMES), por isso é normalizado aqui do mesmo jeito que o norm() do
      navegador. Quem lê é src/js/56-lote-capas.js."""
    avisos = [] if avisos is None else avisos
    if not digital.INVENTARIO.exists():
        return {}
    obras = digital.obras_do_inventario(digital.ler_inventario(digital.INVENTARIO))
    ligadas, _ = digital.casar(obras, books)
    dono = {}
    for i, lista in ligadas.items():
        for o in lista:
            for r in o['linhas']:
                if r['formato'] == digital.FORMATO_PASTA:
                    continue                                       # série: o arquivo mora numa subpasta, não nesta linha
                nome = _norm(r['arquivo']).strip()
                if nome.lower().endswith(DIGITAL_LIDO):
                    dono.setdefault(nome, set()).add(i)
    ambiguo = sorted(n for n, s in dono.items() if len(s) > 1)
    if ambiguo:
        avisos.append(f'{len(ambiguo)} nome(s) de arquivo pertencem a mais de uma linha do catálogo e ficam fora do mapa: '
                      + '; '.join(ambiguo[:3]) + ('…' if len(ambiguo) > 3 else ''))
    return {n: i for n, (i,) in ((n, tuple(s)) for n, s in sorted(dono.items()) if len(s) == 1)
            if i < len(capas) and not capas[i]}


def nomes_antigos(linhas, avisos):
    """{posição da linha: [[título antigo, autor antigo], …]}, lido de catalogo/renomeados.tsv.

    O painel liga o que o usuário anotou a uma linha do catálogo pelo título e pelo autor. Se um dos dois é corrigido no
    catálogo, a ligação se perde (e o livro anotado apareceria duas vezes); o nome antigo, registrado no arquivo, a refaz.
    Os livros da biblioteca virtual não precisam disto: são reconhecidos pelo arquivo."""
    if not RENOMEADOS.exists():
        return {}
    campo = lambda r, k: (r.get(k) or '').strip()
    autor = lambda a: AUTOR_FIX[a][0] if a in AUTOR_FIX else a
    with open(RENOMEADOS, encoding='utf-8-sig', newline='') as f:
        pares = [((campo(r, 'titulo_antigo'), autor(campo(r, 'autor_antigo'))), (campo(r, 'titulo_novo'), autor(campo(r, 'autor_novo'))))
                 for r in csv.DictReader(f, delimiter='\t') if campo(r, 'titulo_antigo')]
    chave = lambda nome: (_norm(nome[0]), _norm(nome[1]))
    nome = lambda n: f'“{n[0]}” ({n[1] or "sem autor"})'
    pos, para, out = {chave(l): i for i, l in enumerate(linhas)}, {chave(a): n for a, n in pares}, {}
    for antigo, novo in pares:
        vistos = {chave(antigo)}
        while chave(novo) not in pos and chave(novo) in para and chave(novo) not in vistos:      # renomeado mais de uma vez: segue até o nome atual
            vistos.add(chave(novo))
            novo = para[chave(novo)]
        if chave(novo) not in pos:
            avisos.append(f'renomeados.tsv: não achei no catálogo a linha {nome(novo)}, para onde iria {nome(antigo)}')
        elif chave(antigo) == chave(novo):
            continue                                                       # só mudou acento ou maiúscula: para o painel é o mesmo nome
        elif chave(antigo) in pos:
            avisos.append(f'renomeados.tsv: {nome(antigo)} ainda é uma linha do catálogo; o nome antigo foi ignorado')
        elif list(antigo) not in out.setdefault(pos[chave(novo)], []):
            out[pos[chave(novo)]].append(list(antigo))
    return {i: v for i, v in out.items() if v}


def ler_trilhas(books, avisos, caminho=None):
    """As trilhas de leitura (catalogo/trilhas.md): [[marcador, nome, descrição, [posições das linhas, em ordem]], …].

    Cada item da trilha é `Título | Autor`, como na linha do catálogo; o livro é achado pelo título (e pelo autor, se
    houver dois títulos iguais). O marcador da trilha também vai na linha do livro: as duas listas têm de bater."""
    caminho = caminho or TRILHAS
    if not pathlib.Path(caminho).exists():
        return []
    por_titulo = {}
    for i, b in enumerate(books):
        por_titulo.setdefault(_norm(b['t']), []).append(i)
    trilhas, t = [], None
    for linha in pathlib.Path(caminho).read_text(encoding='utf-8').splitlines():
        m = re.match(r'^##\s+\d+\.\s+(.+)$', linha)
        if m:
            t = {'nome': m.group(1).strip(), 'tag': '', 'desc': [], 'itens': []}
            trilhas.append(t)
            continue
        if t is None or not linha.strip():
            continue
        m = re.match(r'^`#(trilha-[a-z0-9-]+)`\s*$', linha)
        if m:
            t['tag'] = m.group(1)
            continue
        m = re.match(r'^\d+\.\s+(.+?)\s+\|\s+(.+?)\s*$', linha)
        if m:
            cand = por_titulo.get(_norm(m.group(1)), [])
            if len(cand) > 1:
                cand = [i for i in cand if _norm(books[i]['a']) == _norm(m.group(2))] or cand[:1]
            if cand:
                t['itens'].append(cand[0])
            else:
                avisos.append(f'trilhas.md: “{m.group(1)}” ({t["nome"]}) não é uma linha do catálogo')
            continue
        t['desc'].append(linha.strip())
    out, vistos = [], set()
    for t in trilhas:
        if not t['tag'] or t['tag'] in vistos:
            avisos.append(f'trilhas.md: a trilha “{t["nome"]}” está sem marcador (`#trilha-…`) ou repete o de outra')
            continue
        vistos.add(t['tag'])
        marcados = {i for i, b in enumerate(books) if t['tag'] in b['tags']}
        for i in sorted(marcados ^ set(t['itens'])):
            onde = 'está na lista da trilha, mas a linha não tem o marcador' if i in t['itens'] else 'tem o marcador, mas não está na lista da trilha'
            avisos.append(f'trilhas.md: “{books[i]["t"]}” {onde} #{t["tag"]}')
        out.append([t['tag'], t['nome'], ' '.join(t['desc']), list(dict.fromkeys(t['itens']))])
    for tag in sorted({x for b in books for x in b['tags'] if x.startswith('trilha-')} - vistos):
        avisos.append(f'catálogo: o marcador #{tag} não corresponde a nenhuma trilha de catalogo/trilhas.md')
    return out


def classe_anterior(linhas, avisos, caminho=None):
    """[[posição da linha, eixo, "marcadores"], …]: a classificação de antes da vistoria (catalogo/antes-da-vistoria.tsv).

    O painel guarda no navegador os livros em que o usuário mexeu. Quando chega um catálogo novo, ele precisa saber o que
    mudou no catálogo e o que foi mudado à mão — e, para isso, o que o catálogo dizia antes. Os painéis publicados até
    10/11/2026 não guardavam essa base; este arquivo a devolve para as linhas em que a vistoria trocou ou tirou algo
    (eixo, tipo, dificuldade, extensão ou tema). Nas demais a vistoria só acrescentou, e o painel não precisa de base.
    `linhas` é a saída de build(): a linha é achada pelo título e autor de hoje ou por um nome antigo dela."""
    caminho = pathlib.Path(caminho or ANTES)
    if not caminho.exists():
        return []
    autor = lambda a: AUTOR_FIX[a][0] if a in AUTOR_FIX else a
    chave = lambda t, a: (_norm(t), _norm(autor(a)))
    pos = {}
    for i, l in enumerate(linhas):
        for t, a in [(l[0], l[1])] + [tuple(n) for n in (l[7] if len(l) > 7 and l[7] else [])]:
            pos.setdefault(chave(t, a), i)
    out, vistos = [], set()
    with open(caminho, encoding='utf-8-sig', newline='') as f:
        for r in csv.DictReader(f, delimiter='\t'):
            t, a = (r.get('titulo') or '').strip(), (r.get('autor') or '').strip()
            if not t:
                continue
            i = pos.get(chave(t, a))
            eixo = (r.get('eixo') or '').strip()
            if i is None:
                avisos.append(f'antes-da-vistoria.tsv: “{t}” ({a or "sem autor"}) não é mais uma linha do catálogo; a linha foi ignorada')
            elif not eixo.isdigit() or not 1 <= int(eixo) <= 16:
                avisos.append(f'antes-da-vistoria.tsv: “{t}” está com o eixo “{eixo}” (esperado: 1 a 16); a linha foi ignorada')
            elif i not in vistos:
                vistos.add(i)
                out.append([i, int(eixo), ' '.join((r.get('marcadores') or '').replace('#', '').split())])
    return sorted(out)


def frases(texto):
    """Quantas frases o texto tem: conta os pontos finais (e ? ! …) seguidos de maiúscula ou do fim do texto.
    Inicial de nome ("R. Daneel", "Rob J. Cole", "C.S. Lewis") e abreviatura comum ("Dr.") não encerram frase."""
    n = 0
    for m in re.finditer(r'([^\s.!?…]*)[.!?…]+[”’)]*(?=\s+[“‘(]?[A-ZÀ-Ý0-9]|\s*$)', texto):
        w = m.group(1)
        if not ((len(w) == 1 and w.isupper()) or w.lower() in _ABREV or re.fullmatch(r'(?:[A-Z]\.)*[A-Z]', w)):
            n += 1
    return n


def ler_sinopses(linhas, avisos, caminho=None):
    """[[posição da linha, "sinopse"], …]: as sinopses já escritas (catalogo/sinopses.tsv).

    O arquivo é também o registro das buscas — uma linha por livro pesquisado: título, autor, sinopse, fonte (conhecimento
    geral ou o endereço consultado) e data. Linha sem sinopse é pendência: o livro foi pesquisado e não deu para confirmar
    do que trata; o motivo fica na coluna "fonte", começando por "pendente:". Só as linhas com sinopse vão para o painel.
    `linhas` é a saída de build(): o livro é achado pelo título e autor de hoje ou por um nome antigo dele.
    Os campos são lidos ao pé da letra (sem aspas de planilha): a sinopse pode ter aspas à vontade, só não pode ter tabulação."""
    caminho = pathlib.Path(caminho or SINOPSES)
    if not caminho.exists():
        return []
    autor = lambda a: AUTOR_FIX[a][0] if a in AUTOR_FIX else a
    chave = lambda t, a: (_norm(t), _norm(autor(a)))
    pos = {}
    for i, l in enumerate(linhas):
        for t, a in [(l[0], l[1])] + [tuple(n) for n in (l[7] if len(l) > 7 and l[7] else [])]:
            pos.setdefault(chave(t, a), i)
    out, vistos = [], set()
    with open(caminho, encoding='utf-8-sig', newline='') as f:
        for r in csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE):
            t, a = (r.get('titulo') or '').strip(), (r.get('autor') or '').strip()
            if not t:
                continue
            texto, fonte, data = (' '.join((r.get(k) or '').split()) for k in ('sinopse', 'fonte', 'data'))
            i, quem = pos.get(chave(t, a)), f'sinopses.tsv: “{t}” ({a or "sem autor"})'
            if i is None:
                avisos.append(f'{quem} não é uma linha do catálogo; a linha foi ignorada')
                continue
            if i in vistos:
                avisos.append(f'{quem} aparece mais de uma vez; vale a primeira')
                continue
            vistos.add(i)
            if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', data):
                avisos.append(f'{quem} está com a data “{data}” (esperado: AAAA-MM-DD)')
            if not texto:
                if not fonte.lower().startswith('pendente:'):
                    avisos.append(f'{quem} está sem sinopse e sem o motivo (a coluna "fonte" deve começar por "pendente:")')
                continue
            if not fonte or fonte.lower().startswith('pendente'):
                avisos.append(f'{quem} tem sinopse, mas a fonte não diz de onde ela veio')
            if not SINOPSE_MIN <= len(texto) <= SINOPSE_MAX:
                avisos.append(f'{quem} tem sinopse de {len(texto)} caracteres (esperado: de {SINOPSE_MIN} a {SINOPSE_MAX})')
            if not 2 <= frases(texto) <= 3:
                avisos.append(f'{quem} tem sinopse de {frases(texto)} frase(s) (o combinado: duas ou três)')
            if '"' in texto:
                avisos.append(f'{quem} tem aspas retas na sinopse (use “ ”, que não confundem planilhas)')
            out.append([i, texto])
    return sorted(out)


def build(avisos=None):
    avisos = [] if avisos is None else avisos
    books = parse(SRC.read_text(encoding='utf-8'))
    dig = dados_digitais(books, avisos)
    out = []
    for i, b in enumerate(books):
        autor, obs = b['a'], ''
        if autor in AUTOR_FIX:
            autor, obs = AUTOR_FIX[autor]
        obs = OBS.get(b['t'], obs)
        if b['sec'] == digital.SECAO_DIGITAL:
            eixo = b['sub'] if 1 <= b['sub'] <= 16 else eixo_estante(b)
        else:
            eixo = b['sec'] if b['sec'] else eixo_estante(b)
        linha = [b['t'], autor, ' '.join(b['tags']), b['sec'], eixo, obs]
        if i in dig:
            linha.append(dig[i])
        out.append(linha)
    for i, antigos in nomes_antigos(out, avisos).items():
        out[i] += [None] * (7 - len(out[i])) + [antigos]          # a 7ª posição é a dos dados digitais (vazia quando não há)
    return out


if __name__ == '__main__':
    avisos = []
    data = build(avisos)
    with open(DEST, 'w', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps(data, ensure_ascii=False, separators=(',', ':')))
    print(len(data), 'livros ->', DEST, DEST.stat().st_size, 'bytes')
    # capas: uma posição por linha do catálogo, na mesma ordem (catalogo/capas.tsv → src/capas.json)
    lista = capas.para_o_painel(parse(SRC.read_text(encoding='utf-8')))
    assert len(lista) == len(data)
    with open(DEST_CAPAS, 'w', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps(lista, ensure_ascii=False, separators=(',', ':')))
    print(sum(1 for c in lista if c), 'capas ->', DEST_CAPAS, DEST_CAPAS.stat().st_size, 'bytes')
    fontes = capas.para_as_fontes(parse(SRC.read_text(encoding='utf-8')))
    assert len(fontes) == len(lista) and fontes.count('0') == sum(1 for c in lista if not c)
    with open(DEST_FONTES, 'w', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps(fontes, ensure_ascii=False))
    print(len(fontes), 'origens de capa ->', DEST_FONTES, DEST_FONTES.stat().st_size, 'bytes')
    mapa = nomes_digitais(parse(SRC.read_text(encoding='utf-8')), lista, avisos)
    assert all(0 <= v < len(data) for v in mapa.values()) and all(k.endswith(DIGITAL_LIDO) for k in mapa), 'src/digitais.json: nome ou posição fora do catálogo'
    with open(DEST_DIGITAIS, 'w', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps(mapa, ensure_ascii=False, separators=(',', ':')))
    print(len(mapa), 'arquivos digitais sem capa ->', DEST_DIGITAIS, DEST_DIGITAIS.stat().st_size, 'bytes')
    trilhas = ler_trilhas(parse(SRC.read_text(encoding='utf-8')), avisos)
    with open(DEST_TRILHAS, 'w', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps(trilhas, ensure_ascii=False, separators=(',', ':')))
    print(len(trilhas), 'trilhas ->', DEST_TRILHAS, DEST_TRILHAS.stat().st_size, 'bytes')
    antes = classe_anterior(data, avisos)
    with open(DEST_ANTES, 'w', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps(antes, ensure_ascii=False, separators=(',', ':')))
    print(len(antes), 'classificações de antes da vistoria ->', DEST_ANTES, DEST_ANTES.stat().st_size, 'bytes')
    sinopses = ler_sinopses(data, avisos)
    with open(DEST_SINOPSES, 'w', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps(sinopses, ensure_ascii=False, separators=(',', ':')))
    print(len(sinopses), 'sinopses ->', DEST_SINOPSES, DEST_SINOPSES.stat().st_size, 'bytes')
    for a in avisos:
        print('AVISO:', a)
