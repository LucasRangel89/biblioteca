#!/usr/bin/env python3
"""Lê o Catálogo Mestre (.md) e gera a lista compacta de livros usada pelo painel."""
import re, json, sys, collections, pathlib

# o Catálogo Mestre fica dentro do repositório; para ler outro arquivo, passe o caminho na variável de ambiente CATALOGO
import os
SRC = pathlib.Path(os.environ.get('CATALOGO') or pathlib.Path(__file__).resolve().parent.parent / 'catalogo' / 'Biblioteca_Lucas_Catalogo_Mestre.md')

def parse(md: str):
    books, sec = [], None
    for line in md.splitlines():
        m = re.match(r'^##\s+(\d+)\.\s+(.*)$', line)
        if m:
            sec = (int(m.group(1)), m.group(2).strip())
            continue
        if line.startswith('## '):
            sec = None
            continue
        if sec is None or not line.startswith('|'):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) != 3 or cells[0] in ('Título', '---') or set(cells[0]) <= {'-'}:
            continue
        title, author, tags = cells
        tags = [t.lstrip('#') for t in tags.split() if t.startswith('#')]
        books.append({'t': title, 'a': author, 'tags': tags, 'sec': sec[0]})
    return books

if __name__ == '__main__':
    md = SRC.read_text(encoding='utf-8')
    books = parse(md)
    print('total', len(books))
    c = collections.Counter(b['sec'] for b in books)
    for k in sorted(c): print(' sec', k, c[k])
    tg = collections.Counter(t for b in books for t in b['tags'])
    print(len(tg), 'tags distintas')
    print(sorted(tg.items(), key=lambda x: -x[1]))
    # anomalias
    seen = collections.Counter((b['t'].lower()) for b in books)
    print('títulos repetidos:', [k for k, v in seen.items() if v > 1])
    print('sem d:', [b['t'] for b in books if not any(t in ('d1','d2','d3') for t in b['tags'])])
    print('sem e:', [b['t'] for b in books if not any(t in ('e1','e2','e3') for t in b['tags'])])
    print('sem tipo:', [b['t'] for b in books if not any(t in ('F','NF','poesia','HQ','antologia') for t in b['tags'])])
    print('multi tipo:', [(b['t'], [t for t in b['tags'] if t in ('F','NF','poesia','HQ','antologia')]) for b in books if sum(t in ('F','NF','poesia','HQ','antologia') for t in b['tags']) > 1])
    print('ja-tenho fora da seção 0:', [b['t'] for b in books if 'ja-tenho' in b['tags'] and b['sec'] != 0])
    print('seção 0 sem ja-tenho:', [b['t'] for b in books if 'ja-tenho' not in b['tags'] and b['sec'] == 0])
    print('lido:', [b['t'] for b in books if 'lido' in b['tags']])
    print('top:', sum('top' in b['tags'] for b in books), ' top e ja-tenho:', [b['t'] for b in books if 'top' in b['tags'] and 'ja-tenho' in b['tags']])
    print('autores com parênteses:', [(b['t'], b['a']) for b in books if '(' in b['a']])
    print('títulos com parênteses:', [b['t'] for b in books if '(' in b['t']])
