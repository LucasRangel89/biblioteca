#!/usr/bin/env python3
"""Lê o Catálogo Mestre (.md). Rodado sozinho, mostra contagens e aponta anomalias do catálogo."""
import re, json, sys, collections, pathlib

# o Catálogo Mestre fica dentro do repositório; para ler outro arquivo, passe o caminho na variável de ambiente CATALOGO
import os
SRC = pathlib.Path(os.environ.get('CATALOGO') or pathlib.Path(__file__).resolve().parent.parent / 'catalogo' / 'Biblioteca_Lucas_Catalogo_Mestre.md')

def parse(md: str):
    """Linhas `| Título | Autor | Tags |` das seções numeradas (`## N. Nome`).
    Devolve dicts com t, a, tags, sec e sub — a subseção (`### N.M Nome`; na seção 17, M é o eixo temático), ou 0."""
    books, sec, sub = [], None, 0
    for line in md.splitlines():
        m = re.match(r'^##\s+(\d+)\.\s+(.*)$', line)
        if m:
            sec, sub = (int(m.group(1)), m.group(2).strip()), 0
            continue
        if line.startswith('## '):
            sec = None
            continue
        if sec is None:
            continue
        m = re.match(r'^###\s+(\d+)\.(\d+)\b', line)
        if m:
            sub = int(m.group(2)) if int(m.group(1)) == sec[0] else 0
            continue
        if not line.startswith('|'):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) != 3 or cells[0] in ('Título', '---') or set(cells[0]) <= {'-'}:
            continue
        title, author, tags = cells
        tags = [t.lstrip('#') for t in tags.split() if t.startswith('#')]
        books.append({'t': title, 'a': author, 'tags': tags, 'sec': sec[0], 'sub': sub})
    return books

if __name__ == '__main__':
    md = SRC.read_text(encoding='utf-8')
    books = parse(md)
    TIPOS, DIGITAL = ('F', 'NF', 'poesia', 'HQ', 'antologia'), 17
    antigos = [b for b in books if b['sec'] != DIGITAL]           # seções 0–16: curadas à mão, com dificuldade e extensão
    print('total', len(books))
    c = collections.Counter(b['sec'] for b in books)
    for k in sorted(c): print(' sec', k, c[k])
    tg = collections.Counter(t for b in books for t in b['tags'])
    print(len(tg), 'tags distintas')
    print(sorted(tg.items(), key=lambda x: -x[1]))
    posse = collections.Counter(('tenho-fisico' in b['tags'], 'tenho-digital' in b['tags']) for b in books)
    print('posse: só físico', posse[(True, False)], '· físico e digital', posse[(True, True)], '· só digital', posse[(False, True)], '· recomendação', posse[(False, False)])
    # anomalias
    seen = collections.Counter((b['t'].lower(), b['a'].lower()) for b in books)
    print('título e autor repetidos:', [k for k, v in seen.items() if v > 1])
    print('sem d (seções 0–16):', [b['t'] for b in antigos if not any(t in ('d1','d2','d3') for t in b['tags'])])
    print('sem e (seções 0–16):', [b['t'] for b in antigos if not any(t in ('e1','e2','e3') for t in b['tags'])])
    print('sem tipo:', [b['t'] for b in books if not any(t in TIPOS for t in b['tags'])])
    print('multi tipo:', [(b['t'], [t for t in b['tags'] if t in TIPOS]) for b in books if sum(t in TIPOS for t in b['tags']) > 1])
    print('ja-tenho (marcador antigo; deveria ser tenho-fisico):', [b['t'] for b in books if 'ja-tenho' in b['tags']])
    print('tenho-fisico fora da seção 0:', [b['t'] for b in books if 'tenho-fisico' in b['tags'] and b['sec'] != 0])
    print('seção 0 sem tenho-fisico:', [b['t'] for b in books if 'tenho-fisico' not in b['tags'] and b['sec'] == 0])
    print(f'seção {DIGITAL} sem tenho-digital ou sem eixo:', [b['t'] for b in books if b['sec'] == DIGITAL and ('tenho-digital' not in b['tags'] or not b['sub'])])
    print('lido:', [b['t'] for b in books if 'lido' in b['tags']])
    print('top:', sum('top' in b['tags'] for b in books), ' top que já tenho:', [b['t'] for b in books if 'top' in b['tags'] and ('tenho-fisico' in b['tags'] or 'tenho-digital' in b['tags'])])
    print('autores com parênteses (seções 0–16):', [(b['t'], b['a']) for b in antigos if '(' in b['a']])
    print('títulos com parênteses (seções 0–16):', [b['t'] for b in antigos if '(' in b['t']])
