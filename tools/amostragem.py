#!/usr/bin/env python3
"""Amostragem da biblioteca virtual: 40 livros digitais para o dono bater o olho.

    python tools/amostragem.py                  mostra as 40 do dia e o que mudaria no arquivo
    python tools/amostragem.py --gravar         escreve catalogo/AMOSTRAGEM.md
    python tools/amostragem.py --semente 20261201   sorteia outras 40 (o arquivo é um retrato, não um compromisso)

Por que isto existe: a classificação dos 1.910 digitais (tema, dificuldade, extensão) foi feita a partir do
título e do autor, sem abrir arquivo. A amostra mede o erro. O arquivo gerado é um retrato da data — a tabela
de 17/11/2026 é a semente 20261117, e é ela que o dono respondeu.

Onde mora a classificação: `biblioteca-virtual/inventario.tsv`, coluna `marcadores`. O Catálogo Mestre é
gerado dali pelo `tools/importar_digital.py`, então é no inventário que a correção entra (a ferramenta existe
para o dono nunca abrir esse arquivo: ele responde no chat, quem edita sou eu).
"""
import argparse, collections, pathlib, random, sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / 'tools'))
import parse_catalog                                                    # noqa: E402
import importar_digital
from importar_digital import ler_inventario, obras_do_inventario, casar, INVENTARIO   # noqa: E402

DESTINO = RAIZ / 'catalogo' / 'AMOSTRAGEM.md'
SEMENTE = 20261117
TAMANHO = 40
SECAO_DIGITAL = 17
DIF = {'d1': 'leve', 'd2': 'média', 'd3': 'exigente'}
EXT = {'e1': 'curta (até ~250 p.)', 'e2': 'média (~250–500 p.)', 'e3': 'longa (500+ p. ou série)'}


def nomes_dos_eixos(books):
    """O catálogo mestre só traz o número do eixo; o nome está no cabeçalho `### 17.N Nome`."""
    md = parse_catalog.SRC.read_text(encoding='utf-8')
    import re
    out = {}
    for linha in md.splitlines():
        m = re.match(r'^###\s+17\.(\d+)\s+(.*)$', linha)
        if m:
            out[int(m.group(1))] = m.group(2).strip()
    return out


def obras_por_linha():
    """{posição no catálogo: [obras do inventário]}, com a lista de arquivos de cada obra."""
    inventario = ler_inventario(INVENTARIO)
    por_chave = collections.defaultdict(list)
    for r in inventario:
        if r['formato'] == 'pasta':
            continue
        titulo = r['catalogo'] or r['titulo']
        por_chave[(importar_digital.chave(titulo), importar_digital.chave(r['autor']))].append((r['pasta'], r['arquivo']))
    obras = obras_do_inventario(inventario)
    for o in obras.values():
        o['arquivos_lista'] = por_chave.get((importar_digital.chave(o['t']), importar_digital.chave(o['a'])), [])
    books = parse_catalog.parse(parse_catalog.SRC.read_text(encoding='utf-8'))
    ligadas, _ = casar(obras, books)
    return ligadas, books


def linha_de(n, i, book, nome_eixo, obras):
    tags = book['tags']
    dif = next((DIF[t] for t in tags if t in DIF), '—')
    ext = next((EXT[t] for t in tags if t in EXT), '—')
    tema = nome_eixo.get(book['sub'], 'sem tema') if book['sub'] else 'sem tema'
    autor = book['a'] if book['a'] and book['a'] != '(autor não informado)' else 'sem autor'
    L = obras.get(i) or []
    arquivos = [arq for o in L for arq in o['arquivos_lista']]
    formatos = sorted({f for o in L for f in o['formatos']})
    series = [s for o in L for s in o['subpastas']]
    pastas = list(dict.fromkeys(p for o in L for p in o['pastas']))
    if arquivos:
        onde = f"`{arquivos[0][0]}/{arquivos[0][1]}`"
        extras = len(arquivos) - 1 + len(series)
        if extras:
            onde += f" + {extras} outro(s)"
    elif series:
        onde = f"pasta `{series[0]}/` dentro de `{pastas[0]}`" + (f" (série: {len(series)} arquivo(s))" if len(series) > 1 else '')
    elif pastas:
        onde = f"pasta `{pastas[0]}`"
    else:
        onde = '(nenhum arquivo ligado a esta linha)'
    formato = '/'.join(formatos) or 'pasta'
    if 'verificar' in tags:
        formato += ' · fila “a verificar”'
    return (f'| {n} | “{book["t"]}” ({autor}) — {formato} | {onde} | {tema} | {dif} | {ext} |')


def tabela(semente, tamanho):
    books = parse_catalog.parse(parse_catalog.SRC.read_text(encoding='utf-8'))
    digitais = [i for i, b in enumerate(books) if b['sec'] == SECAO_DIGITAL]
    R = random.Random(semente)
    amostra = sorted(R.sample(digitais, min(tamanho, len(digitais))))
    obras = obras_por_linha()[0]
    nome_eixo = nomes_dos_eixos(books)
    # agrupar por tema e depois por título: quem lê a tabela vê os livros do mesmo assunto juntos
    amostra.sort(key=lambda i: (books[i]['sub'], books[i]['t'].lower()))
    linhas = [linha_de(n, i, books[i], nome_eixo, obras) for n, i in enumerate(amostra, 1)]
    return amostra, linhas


CABECALHO = """# Amostragem da biblioteca virtual — 40 livros para você bater o olho

Gerado em 17/11/2026 (`python tools/amostragem.py`, semente 20261117). Nada aqui foi corrigido ainda: é a
fotografia do que está gravado hoje, com o nome exato do arquivo em que cada dado vive.

## Para que isto serve

Quando os seus 1.910 arquivos digitais entraram no catálogo, cada um ganhou três coisas: um **tema**, uma
**dificuldade** e um **tamanho**. Eu decidi isso lendo só o título e o autor — não abri arquivo nenhum. Em
livro conhecido quase sempre acerto; num PDF de nome embolado, é palpite.

Aqui estão 40 livros sorteados entre os 1.910, com o que está gravado para cada um. Você que conhece a própria
estante diz onde está certo e onde está errado. Se quase tudo estiver certo, o problema é menor do que parece e
eu sigo em frente. Se aparecer um padrão (toda HQ virou "média", todo conto virou "livro longo"), eu corrijo o
padrão inteiro de uma vez — não só as 40 linhas.

## Como responder

Uma linha por número, aqui no chat. Só o desvio: o que você não comentar eu considero certo.

- `7: tudo certo`
- `12: o tema é horror, não ficção científica`
- `31: é média, não longa`
- `5: não sei — o arquivo é uma pasta com 20 quadrinhos`

Pode responder de uma vez ou em pedaços, quando der tempo. Você não precisa abrir nada a não ser que bata
dúvida: aí o nome do arquivo na tabela diz onde olhar, e vale o que estiver escrito na primeira página.
Se você desconfiar do sorteio, é só dizer "sorteia de novo" e eu refaço com outras 40.

## As 40 linhas

| # | Livro | Arquivo (na sua pasta da biblioteca virtual) | Tema gravado | Dificuldade | Tamanho |
| --- | --- | --- | --- | --- | --- |
"""

RODAPE = """
## De quebra: três coisas que dá para responder na mesma hora

Você já vai estar olhando a pasta. Estas três dúvidas estão presas desde 11/11 e somem no mesmo movimento
(são dos itens 1 e 6 do `PENDENCIAS.md`):

1. **Os dois arquivos abaixo são o mesmo livro?** Um deles chegou com o nome mutilado no download. Abra os dois
   e responda **"é o mesmo, fica um"** ou **"são dois livros"**:
   - `autoconhecimento e desenvolvimento pessoal/persuasopnlehipnoseaplicadasseduo.pdf`
   - `autoconhecimento e desenvolvimento pessoal/Rafael B. Correa - Psicologia, PNL e Hipnose Aplicada a Sedução.pdf`
2. **Onde estão os contos do Lovecraft de papel?** *O Chamado de Cthulhu*, *Nas Montanhas da Loucura* e *A
   Sombra sobre Innsmouth* — olhe o sumário de *Contos (H.P. Lovecraft)* e o de *Lovecraft: Medo Clássico* e
   responda, por exemplo, **"os três estão no Contos"**.
3. ***O Horror de Dunwich* e *Um Sussurro nas Trevas*** estão num desses dois também? Se sim, diga **"os dois
   estão no Contos, marque como tenho em papel"** (hoje as duas linhas constam como recomendação sem edição na
   sua estante).

## O que eu faço com as suas respostas

Corrijo as 40 no inventário digital (`biblioteca-virtual/inventario.tsv`, coluna `marcadores`) e no catálogo,
que é gerado dali. Conto quantos acertos e erros apareceram; se um tipo de erro se repetir, estimo quantos dos
outros 1.870 livros têm o mesmo vício e corrijo em bloco. Refaço o painel, registro a data da correção no
`ROTEIRO.md` e só então abro o lote 7 das sinopses, que usa essa régua.

---

*Como a tabela é feita: 40 sorteadas entre os {n_digitais} livros da seção 17, com `random.Random(20261117)`
sobre a ordem do catálogo; exibidas agrupadas por tema e, dentro do tema, por título. Arquivo por linha vem do
`biblioteca-virtual/inventario.tsv`. Rodar o gerador de novo com a mesma semente reproduz esta tabela.*
"""


def texto():
    books = parse_catalog.parse(parse_catalog.SRC.read_text(encoding='utf-8'))
    n_digitais = sum(1 for b in books if b['sec'] == SECAO_DIGITAL)
    _, linhas = tabela(SEMENTE, TAMANHO)
    return CABECALHO + '\n'.join(linhas) + '\n' + RODAPE.format(n_digitais=f'{n_digitais:,}'.replace(',', '.'))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--gravar', action='store_true', help='escreve catalogo/AMOSTRAGEM.md')
    ap.add_argument('--semente', type=int, default=SEMENTE)
    ap.add_argument('--tamanho', type=int, default=TAMANHO)
    a = ap.parse_args(argv)
    novo = texto() if a.semente == SEMENTE and a.tamanho == TAMANHO else '\n'.join(
        t for t in [CABECALHO.rstrip(), *tabela(a.semente, a.tamanho)[1], RODAPE.format(n_digitais='1.910')])
    atual = DESTINO.read_text(encoding='utf-8') if DESTINO.exists() else ''
    if a.gravar:
        if novo == atual:
            print('Nada mudou.')
        else:
            DESTINO.write_text(novo, encoding='utf-8')
            print(f'Gravado: {DESTINO.relative_to(RAIZ)} ({len(novo.splitlines())} linhas).')
    else:
        print('Mudaria:' if novo != atual else 'Igual ao arquivo de hoje.')
        print('\n'.join(novo.splitlines()[:12] + ['…']))
    return 0


if __name__ == '__main__':
    sys.exit(main())
