#!/usr/bin/env python3
"""Converte o Catálogo Mestre (.md) no JSON compacto embutido no painel.

Saída: lista de [titulo, autor, "tags separadas por espaço", secao, eixo, observacao]
- secao: seção original do catálogo (0 = estante física)
- eixo:  eixo temático 1..16 (para a estante, deduzido das tags; ver eixos.py)
"""
import json, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from parse_catalog import parse, SRC
from eixos import eixo_estante

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

def build():
    books = parse(SRC.read_text(encoding='utf-8'))
    out = []
    for b in books:
        autor, obs = b['a'], ''
        if autor in AUTOR_FIX:
            autor, obs = AUTOR_FIX[autor]
        obs = OBS.get(b['t'], obs)
        eixo = b['sec'] if b['sec'] else eixo_estante(b)
        out.append([b['t'], autor, ' '.join(b['tags']), b['sec'], eixo, obs])
    return out

if __name__ == '__main__':
    data = build()
    dest = pathlib.Path(__file__).parent.parent / 'src' / 'catalog.json'
    dest.write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    print(len(data), 'livros ->', dest, dest.stat().st_size, 'bytes')
