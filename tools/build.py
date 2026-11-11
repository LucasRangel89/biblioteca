#!/usr/bin/env python3
"""Gera o painel em um único arquivo HTML (CSS, dados e scripts embutidos).

A única coisa que o painel busca fora são as imagens das capas — na Open Library, na Apple Books ou no endereço posto
à mão em catalogo/capas.tsv — e só quando "Mostrar as capas" está ligado. Nenhum dado do usuário sai do navegador."""
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
arq_trilhas = SRC / 'trilhas.json'                      # trilhas de leitura: [marcador, nome, descrição, [posições no catálogo]]
trilhas = json.loads(arq_trilhas.read_text(encoding='utf-8')) if arq_trilhas.exists() else []
assert all(len(t) == 4 and all(isinstance(i, int) and 0 <= i < len(catalogo) for i in t[3]) for t in trilhas), 'src/trilhas.json não acompanha src/catalog.json: rode tools/build_catalog.py'
arq_antes = SRC / 'antes.json'                          # classificação de antes da vistoria: [posição no catálogo, eixo, "marcadores"]
antes = json.loads(arq_antes.read_text(encoding='utf-8')) if arq_antes.exists() else []
assert all(len(x) == 3 and isinstance(x[0], int) and 0 <= x[0] < len(catalogo) and isinstance(x[1], int) and isinstance(x[2], str) for x in antes), 'src/antes.json não acompanha src/catalog.json: rode tools/build_catalog.py'
arq_sinopses = SRC / 'sinopses.json'                    # sinopses: [posição no catálogo, "texto"], só dos livros que já têm
sinopses = json.loads(arq_sinopses.read_text(encoding='utf-8')) if arq_sinopses.exists() else []
assert all(len(x) == 2 and isinstance(x[0], int) and 0 <= x[0] < len(catalogo) and isinstance(x[1], str) and x[1] for x in sinopses), 'src/sinopses.json não acompanha src/catalog.json: rode tools/build_catalog.py'
assert len({x[0] for x in sinopses}) == len(sinopses), 'src/sinopses.json tem duas sinopses para a mesma linha'
dados = ('const CATALOGO = ' + json.dumps(catalogo, ensure_ascii=False, separators=(',', ':')) + ';\n'
         + 'const CAPAS = ' + json.dumps(capas, ensure_ascii=False, separators=(',', ':')) + ';\n'
         + 'const TRILHAS_DADOS = ' + json.dumps(trilhas, ensure_ascii=False, separators=(',', ':')) + ';\n'
         + 'const CLASSE_ANTES = ' + json.dumps(antes, ensure_ascii=False, separators=(',', ':')) + ';\n'
         + 'const SINOPSES = ' + json.dumps(sinopses, ensure_ascii=False, separators=(',', ':')) + ';')
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
print(f'{SAIDA.name}  {SAIDA.stat().st_size/1024:.0f} KB  ({len(catalogo)} livros, {sum(1 for c in capas if c)} capas, {len(trilhas)} trilhas, {len(sinopses)} sinopses, {len(fontes)} módulos JS)')
