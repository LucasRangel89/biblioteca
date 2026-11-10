#!/usr/bin/env python3
"""Gera o painel em um único arquivo HTML (CSS, dados e scripts embutidos).

A única coisa que o painel busca fora são as imagens das capas, na Open Library (ou no endereço posto à mão em
catalogo/capas.tsv) — e só quando "Mostrar as capas" está ligado. Nenhum dado do usuário sai do navegador."""
import json, pathlib, re, sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SRC = RAIZ / 'src'
SAIDA = RAIZ / 'Biblioteca_Lucas_Dashboard.html'

css = (SRC / 'styles.css').read_text(encoding='utf-8')
catalogo = json.loads((SRC / 'catalog.json').read_text(encoding='utf-8'))
fontes = sorted((SRC / 'js').glob('*.js'))
js = '\n'.join(f.read_text(encoding='utf-8') for f in fontes)
arq_capas = SRC / 'capas.json'
capas = json.loads(arq_capas.read_text(encoding='utf-8')) if arq_capas.exists() else []
assert not capas or len(capas) == len(catalogo), 'src/capas.json não acompanha src/catalog.json: rode tools/build_catalog.py'
assert all(c == 0 or (isinstance(c, int) and c > 0) or (isinstance(c, str) and c.startswith('https://')) for c in capas)
dados = ('const CATALOGO = ' + json.dumps(catalogo, ensure_ascii=False, separators=(',', ':')) + ';\n'
         + 'const CAPAS = ' + json.dumps(capas, ensure_ascii=False, separators=(',', ':')) + ';')
pacote = '(function () {\n"use strict";\n' + dados + '\n' + js + '\n})();'
for proibido in ('</script', '<!--'):
    assert proibido not in pacote.lower(), f'sequência insegura em script embutido: {proibido}'
assert '</style' not in css.lower()

html = (SRC / 'index.html').read_text(encoding='utf-8')
assert '/*__CSS__*/' in html and '/*__JS__*/' in html
html = html.replace('/*__CSS__*/', css.strip()).replace('/*__JS__*/', pacote)

externos = [u for u in re.findall(r'(?:src|href)=["\'](https?://[^"\']+)', html)]
assert not externos, f'recursos externos no HTML estático: {externos}'
with open(SAIDA, 'w', encoding='utf-8', newline='\n') as f: f.write(html)   # sempre com \n: o arquivo sai igual em qualquer sistema
print(f'{SAIDA.name}  {SAIDA.stat().st_size/1024:.0f} KB  ({len(catalogo)} livros, {sum(1 for c in capas if c)} capas, {len(fontes)} módulos JS)')
