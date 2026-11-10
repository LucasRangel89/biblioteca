#!/usr/bin/env python3
"""Converte o Catálogo Mestre (.md) no JSON compacto embutido no painel.

Saída: lista de [titulo, autor, "tags separadas por espaço", secao, eixo, observacao, digital]
- secao:   seção original do catálogo (0 = estante física, 17 = biblioteca virtual)
- eixo:    eixo temático 1..16 (na estante, deduzido das tags — ver eixos.py; na seção 17, o número da subseção)
- digital: só nos livros que estão na biblioteca virtual (biblioteca-virtual/inventario.tsv):
           ["formatos", nº de arquivos, [pastas], [títulos das edições, quando diferem do catálogo], "identificadores dos arquivos"]
           Os identificadores deixam o painel reconhecer o livro mesmo depois de o título ser corrigido no inventário.
"""
import hashlib, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from parse_catalog import parse, SRC
from eixos import eixo_estante
import importar_digital as digital

DEST = pathlib.Path(__file__).resolve().parent.parent / 'src' / 'catalog.json'
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
        arquivos = list(dict.fromkeys((r['pasta'], r['arquivo']) for r in linhas))
        ids = [id_arquivo(*a) for a in arquivos]
        for x in ids:
            dono.setdefault(x, set()).add(i)
        out[i] = [' '.join(sorted({r['formato'] for r in linhas})), len(arquivos), list(dict.fromkeys(r['pasta'] for r in linhas)),
                  list(dict.fromkeys(t for o in lista for t in o['edicoes'])), ids]
    for i, d in out.items():                                   # um identificador repetido entre dois livros não serve para reconhecer nenhum dos dois
        d[4] = ' '.join(x for x in d[4] if len(dono[x]) == 1)
    sem_arquivo = [b['t'] for i, b in enumerate(books) if 'tenho-digital' in b['tags'] and i not in out]
    if sem_arquivo:
        avisos.append(f'{len(sem_arquivo)} linha(s) com #tenho-digital sem arquivo no inventário: ' + '; '.join(sem_arquivo[:5]) + ('…' if len(sem_arquivo) > 5 else ''))
    sem_marca = [books[i]['t'] for i in out if 'tenho-digital' not in books[i]['tags']]
    if sem_marca:
        avisos.append(f'{len(sem_marca)} livro(s) do inventário cuja linha não tem #tenho-digital (rode tools/importar_digital.py): ' + '; '.join(sem_marca[:5]) + ('…' if len(sem_marca) > 5 else ''))
    return out


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
    return out


if __name__ == '__main__':
    avisos = []
    data = build(avisos)
    with open(DEST, 'w', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps(data, ensure_ascii=False, separators=(',', ':')))
    print(len(data), 'livros ->', DEST, DEST.stat().st_size, 'bytes')
    for a in avisos:
        print('AVISO:', a)
