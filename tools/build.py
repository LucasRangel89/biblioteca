#!/usr/bin/env python3
"""Gera o painel em um único arquivo HTML (CSS, dados e scripts embutidos).

A única coisa que o painel busca fora são as imagens das capas — na Open Library, na Apple Books ou no endereço posto
à mão em catalogo/capas.tsv — e só quando "Mostrar as capas" está ligado. Nenhum dado do usuário sai do navegador.

As letras dos temas (src/letras/*.woff2) também vão dentro do arquivo: assim o tema fica igual em qualquer aparelho,
sem depender das fontes instaladas e sem buscar nada na internet."""
import base64, json, pathlib, re, sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SRC = RAIZ / 'src'
SAIDA = RAIZ / 'Biblioteca_Lucas_Dashboard.html'

# As letras dos temas: arquivo "familia-latin-peso-estilo.woff2" em src/letras → uma regra @font-face com o arquivo
# dentro. Só o alfabeto latino (cobre o português); o que faltar numa letra o navegador desenha com a letra seguinte da
# lista do tema. As licenças (SIL OFL 1.1) estão na mesma pasta; ver src/letras/LEIAME.md.
FAMILIAS = {'im-fell-english': 'IM Fell English', 'libre-baskerville': 'Libre Baskerville', 'old-standard-tt': 'Old Standard TT',
            'marcellus': 'Marcellus', 'cormorant-garamond': 'Cormorant Garamond', 'cinzel': 'Cinzel'}
LATINO = ('U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,'
          'U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD')
letras = []
for arq in sorted((SRC / 'letras').glob('*.woff2')):
    m = re.fullmatch(r'([a-z0-9-]+)-latin-(\d{3})-(normal|italic)\.woff2', arq.name)
    assert m and m.group(1) in FAMILIAS, f'src/letras/{arq.name}: o nome deve ser familia-latin-peso-estilo.woff2, de uma família de FAMILIAS'
    bruto = arq.read_bytes()
    assert bruto[:4] == b'wOF2', f'src/letras/{arq.name} não é um arquivo WOFF2'
    assert (SRC / 'letras' / f'{m.group(1)}-LICENSE.txt').exists(), f'falta a licença de {m.group(1)} em src/letras'
    letras.append('@font-face { font-family: "%s"; font-style: %s; font-weight: %s; font-display: swap; src: url(data:font/woff2;base64,%s) format("woff2"); unicode-range: %s; }'
                  % (FAMILIAS[m.group(1)], m.group(3), m.group(2), base64.b64encode(bruto).decode('ascii'), LATINO))

css = (SRC / 'styles.css').read_text(encoding='utf-8')
for familia in FAMILIAS.values():
    assert (f'"{familia}"' in css) == any(f'font-family: "{familia}"' in r for r in letras), f'a letra {familia} está em src/styles.css ou em src/letras, mas não nos dois'
css = '/* letras dos temas (src/letras) */\n' + '\n'.join(letras) + '\n' + css.lstrip() if letras else css
catalogo = json.loads((SRC / 'catalog.json').read_text(encoding='utf-8'))
fontes = sorted((SRC / 'js').glob('*.js'))
js = '\n'.join(f.read_text(encoding='utf-8') for f in fontes)
arq_capas = SRC / 'capas.json'
capas = json.loads(arq_capas.read_text(encoding='utf-8')) if arq_capas.exists() else []
assert not capas or len(capas) == len(catalogo), 'src/capas.json não acompanha src/catalog.json: rode tools/build_catalog.py'
assert all(c == 0 or (isinstance(c, int) and c > 0) or (isinstance(c, str) and c.startswith('https://')) for c in capas)
arq_fontes = SRC / 'capas-fontes.json'                  # de onde veio cada capa: uma letra por livro (ver capas.para_as_fontes)
fontes_capas = json.loads(arq_fontes.read_text(encoding='utf-8')) if arq_fontes.exists() else ''
assert isinstance(fontes_capas, str) and (not fontes_capas or len(fontes_capas) == len(catalogo)), 'src/capas-fontes.json não acompanha src/catalog.json: rode tools/build_catalog.py'
assert set(fontes_capas) <= set('eoagm0'), 'src/capas-fontes.json: só as letras e, o, a, g, m e 0'
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
         + 'const CAPAS_FONTES = ' + json.dumps(fontes_capas, ensure_ascii=False) + ';\n'
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
print(f'{SAIDA.name}  {SAIDA.stat().st_size/1024:.0f} KB  ({len(catalogo)} livros, {sum(1 for c in capas if c)} capas, {len(trilhas)} trilhas, {len(sinopses)} sinopses, {len(letras)} letras, {len(fontes)} módulos JS)')
