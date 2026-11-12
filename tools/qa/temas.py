"""Os temas visuais (Etapa 10, Parte 4): o seletor de aparência e os temas além do padrão.

Um tema troca as cores, a letra dos títulos e, no máximo, um ornamento; as telas e os números ficam onde estão. Cada
tema é um bloco de variáveis em src/styles.css, uma linha em TEMAS (src/js/30-state.js) e um id no começo de
src/index.html. As letras são fontes livres, guardadas em src/letras e postas dentro do painel por tools/build.py.

Confere que:
  · os três lugares que listam os temas dizem a mesma coisa, e todo tema define as mesmas variáveis do tema padrão;
  · em todo tema, cada par de cor de texto e fundo que o painel usa tem contraste AA (4,5) — o a11y.py mede as telas
    de verdade; aqui a conta é feita sobre as variáveis, e aponta o par exato quando um tema novo erra;
  · as letras estão no painel, idênticas aos arquivos de src/letras, cada uma com a sua licença, e nada é buscado fora;
  · sem escolha feita, vale o padrão do sistema (claro ou escuro), e o tema padrão continua como era;
  · o botão da paleta abre o quadro com uma opção por tema; cada amostra mostra as cores do seu tema e cada nome vem na
    letra do seu tema, seja qual for o tema em uso;
  · escolher um tema troca as cores, a letra dos títulos (com a fonte de fato carregada) e a cor da barra do navegador;
    a escolha fica guardada, volta ao recarregar e é aplicada antes de a página aparecer;
  · pelo teclado: as setas andam e já escolhem, Esc fecha e devolve o foco, Tab para fora fecha; clicar fora fecha, e
    só um quadro fica aberto por vez (o dos temas e os dos filtros);
  · cada tema tem o seu ornamento, e só ele; o fundo da página continua de uma cor só;
  · em cada tema, no computador e no celular, nenhuma tela estoura a largura, o título não invade os botões e a ficha
    do livro cabe na tela;
  · a folha de impressão não muda com o tema, e imprimir a página num tema escuro usa o padrão claro;
  · um tema guardado que não existe mais não quebra nada; e na pré-visualização isolada, trocar de tema funciona.
"""
from caminhos import PAINEL, PAINEL_LIMPO, PAINEL_URL, RAIZ, TMP
from relogio import fixa
import base64, json, re
from playwright.sync_api import sync_playwright

CHAVE = 'biblioteca-lucas:v1'
errs = []; falhas = []
SERIF_PADRAO = 'Iowan Old Style'
VISOES = ['geral', 'biblioteca', 'recs', 'financas', 'desejos', 'precos']


def ok(nome, cond, extra=''):
    print(('  ok   ' if cond else '  FALHA') + ' ' + nome + (' — ' + str(extra) if extra != '' else ''))
    if not cond: falhas.append(nome)


# ───────────── os arquivos (sem navegador) ─────────────
print('A. Os três lugares que listam os temas')
js = (RAIZ / 'src' / 'js' / '30-state.js').read_text(encoding='utf-8')
TEMAS = [dict(zip(('id', 'n', 'd', 'clima', 'cor'), m)) for m in re.findall(r"\{ id: '(\w+)', n: '([^']+)', d: '([^']+)', clima: '(claro|escuro)', cor: '(#[0-9A-F]{6})' \}", js)]
IDS = [t['id'] for t in TEMAS]; NOVOS = [t for t in TEMAS if t['id'] not in ('claro', 'escuro')]
ok('TEMAS (src/js/30-state.js) começa pelo padrão — claro e escuro — e traz pelo menos três outros', IDS[:2] == ['claro', 'escuro'] and len(NOVOS) >= 3 and len(set(IDS)) == len(IDS), IDS)
CLIMAS = {'lovecraft': 'escuro', 'holmes': 'claro', 'moby': 'claro', 'deserto': 'claro', 'terras': 'claro', 'greco': 'claro'}
ok('cada tema tem o clima combinado — um só, claro ou escuro', {t['id']: t['clima'] for t in TEMAS} == {'claro': 'claro', 'escuro': 'escuro', **CLIMAS}, {t['id']: t['clima'] for t in NOVOS})
casca = (RAIZ / 'src' / 'index.html').read_text(encoding='utf-8')
m = re.search(r"dataset\.tema=\[([^\]]+)\]\.indexOf\(c\.tema\)>=0\?c\.tema:", casca)
ok('o começo de src/index.html aceita exatamente os mesmos temas', m is not None and re.findall(r"'(\w+)'", m.group(1)) == IDS, m and m.group(1))
css = (RAIZ / 'src' / 'styles.css').read_text(encoding='utf-8')
BLOCOS = {}      # id → {variável: valor}, juntando todo bloco cujo seletor cita [data-tema="id"]
for sel, corpo in re.findall(r'(?m)^((?::root|\[data-tema="\w+"\])(?:, (?::root|\[data-tema="\w+"\]))*) \{\n(.*?)\n\}', css, re.S):
    for tid in re.findall(r'\[data-tema="(\w+)"\]', sel):
        BLOCOS.setdefault(tid, {}).update({k: v.strip() for k, v in re.findall(r'(--[\w-]+):\s*([^;]+);', corpo)})
ok('src/styles.css tem um bloco de variáveis para cada tema, e só para eles', sorted(BLOCOS) == sorted(IDS), sorted(BLOCOS))
base = set(BLOCOS.get('claro', {}))
ok('o tema padrão define as cores, a letra dos títulos e a força do mapa de calor', len(base) >= 40 and {'--bg', '--ink', '--accent', '--serif', '--tit-peso', '--tit-esc', '--tit-esp', '--tit-alt', '--mz-k', '--veu', '--sombra'} <= base, len(base))
ok('todo tema define as mesmas variáveis do padrão — nem a mais, nem a menos', all(set(BLOCOS.get(t, {})) == base for t in IDS), {t: sorted(set(BLOCOS.get(t, {})) ^ base) for t in IDS if set(BLOCOS.get(t, {})) != base})
ok('a cor de fundo de cada tema é a que TEMAS manda para a barra do navegador', all(BLOCOS[t['id']]['--bg'].upper() == t['cor'] for t in TEMAS), [(t['id'], BLOCOS[t['id']]['--bg'], t['cor']) for t in TEMAS if BLOCOS[t['id']]['--bg'].upper() != t['cor']])
ok('cada bloco diz se o tema é claro ou escuro (color-scheme), como em TEMAS', all(re.search(r'\[data-tema="%s"\][^{]*\{[^}]*color-scheme: %s;' % (t['id'], 'dark' if t['clima'] == 'escuro' else 'light'), css) or (t['id'] == 'claro' and 'color-scheme: light;' in css) for t in TEMAS))

print('B. Contraste, par a par, nas variáveis de cada tema')
def lum(h):
    h = h.lstrip('#'); r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda v: v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)
def razao(a, b):
    x, y = lum(a), lum(b); return (max(x, y) + 0.05) / (min(x, y) + 0.05)
def mistura(a, b, p):          # color-mix(in srgb, a p, b)
    a, b = a.lstrip('#'), b.lstrip('#')
    return '#' + ''.join('%02X' % round(int(a[i:i + 2], 16) * p + int(b[i:i + 2], 16) * (1 - p)) for i in (0, 2, 4))
# texto sobre fundo, como o painel usa: tinta nos quatro fundos, destaque e avisos sobre cartão e sobre o próprio tom suave
PARES = ([('ink', f) for f in ('bg', 'surface', 'surface-3', 'accent-soft')] + [(t, f) for t in ('ink-2', 'ink-3') for f in ('bg', 'surface', 'surface-2', 'surface-3')]
         + [('accent', 'bg'), ('accent', 'surface'), ('accent', 'surface-2'), ('accent-ink', 'accent'), ('accent-forte', 'accent-soft'), ('accent-forte', 'surface'), ('accent-forte', 'bg')]
         + [(c, f) for c in ('good', 'bad', 'warn') for f in ('surface', 'bg')] + [('good', 'good-soft'), ('bad', 'bad-soft'), ('warn', 'warn-soft')]
         + [(c, f) for c in ('c2-ink', 'c4-ink') for f in ('surface', 'surface-2')] + [('seg-on-ink', 'seg-on')])
for t in TEMAS:
    v = {k[2:]: x for k, x in BLOCOS[t['id']].items() if re.fullmatch(r'#[0-9A-Fa-f]{6}', x)}
    ruins = [f'{a} sobre {b}: {razao(v[a], v[b]):.2f}' for a, b in PARES if razao(v[a], v[b]) < 4.5]
    k = float(BLOCOS[t['id']]['--mz-k'].rstrip('%')) / 100
    forte = razao(v['ink'], mistura(v['accent'], v['surface-2'], k + .07))
    if forte < 4.5: ruins.append(f'tinta sobre a célula mais forte do mapa de calor: {forte:.2f}')
    desenho = [f'{c}: {razao(v[c], v["surface"]):.2f}' for c in ['estrela'] + [f'c{i}' for i in range(1, 9)] if razao(v[c], v['surface']) < 3]
    ok(f'{t["n"]}: os {len(PARES) + 1} pares de texto e fundo passam de 4,5', not ruins, ruins)
    if t in NOVOS: ok(f'{t["n"]}: as cores dos gráficos e a estrela se destacam do cartão (3:1)', not desenho, desenho)
    escuro = lum(v['bg']) < lum(v['ink'])
    ok(f'{t["n"]}: é mesmo um tema {t["clima"]}', escuro == (t['clima'] == 'escuro'))

print('C. As letras')
html = PAINEL.read_text(encoding='utf-8')
estilo = re.search(r'<style>(.*?)</style>', html, re.S).group(1)
faces = re.findall(r'@font-face \{ font-family: "([^"]+)"; font-style: (\w+); font-weight: (\d+); font-display: swap; src: url\(data:font/woff2;base64,([A-Za-z0-9+/=]+)\) format\("woff2"\); unicode-range: ([^;]+); \}', estilo)
arquivos = sorted((RAIZ / 'src' / 'letras').glob('*.woff2'))
ok('o painel traz uma regra @font-face por arquivo de src/letras', len(faces) == len(arquivos) >= 3 and estilo.count('@font-face') == len(faces), (len(faces), len(arquivos)))
ok('…com o arquivo inteiro dentro, idêntico ao da pasta (se falhar: python tools/build.py)', sorted(base64.b64decode(f[3]) for f in faces) == sorted(a.read_bytes() for a in arquivos))
ok('cada arquivo é um WOFF2 com o nome no padrão familia-latin-peso-estilo', all(a.read_bytes()[:4] == b'wOF2' and re.fullmatch(r'[a-z0-9-]+-latin-\d{3}-(normal|italic)\.woff2', a.name) for a in arquivos), [a.name for a in arquivos])
familias = sorted({f[0] for f in faces})
ok('cada família tem a sua licença na pasta, e o LEIAME diz de quem é cada uma', all((RAIZ / 'src' / 'letras' / (re.sub(r'-latin-.*', '', a.name) + '-LICENSE.txt')).exists() for a in arquivos) and all(f in (RAIZ / 'src' / 'letras' / 'LEIAME.md').read_text(encoding='utf-8') for f in familias), familias)
ok('as licenças são a SIL Open Font License 1.1, que permite embutir', all('SIL OPEN FONT LICENSE Version 1.1' in l.read_text(encoding='utf-8') for l in (RAIZ / 'src' / 'letras').glob('*-LICENSE.txt')))
ok('cada tema novo abre a lista de letras dos títulos com uma família embutida — e uma diferente da dos outros', sorted(re.match(r'"([^"]+)"', BLOCOS[t['id']]['--serif']).group(1) for t in NOVOS) == familias, [BLOCOS[t['id']]['--serif'][:30] for t in NOVOS])
ok('…e termina em letras do sistema, para os sinais que a embutida não tem', all(BLOCOS[t['id']]['--serif'].endswith('Georgia, serif') for t in NOVOS))
pesos = {fam: sorted(int(f[2]) for f in faces if f[0] == fam) for fam in familias}
ok('o peso pedido para os títulos existe em cada letra (sem negrito fabricado pelo navegador)', all(int(BLOCOS[t['id']]['--tit-peso']) in pesos[re.match(r'"([^"]+)"', BLOCOS[t['id']]['--serif']).group(1)] for t in NOVOS), pesos)
ok('…e também o peso normal, usado no texto da sinopse', all(400 in p for p in pesos.values()), pesos)
ok('nada é buscado fora: nenhum endereço da internet nas folhas de estilo', not re.findall(r'url\((?!\s*["\']?data:)', estilo) and '@import' not in estilo, re.findall(r'url\((?!\s*["\']?data:).{0,40}', estilo)[:3])

# ───────────── no navegador ─────────────
ESTADO = """() => { const h = document.documentElement, b = document.querySelector('#b-tema'), w = document.querySelector('#pw-tema'), cs = e => getComputedStyle(e);
  const h1 = document.querySelector('.topo h1'), h3 = document.querySelector('.visao:not([hidden]) .card h3');      // o título da página e o de um cartão
  return { tema: h.dataset.tema, aberto: w.classList.contains('aberto'), expandido: b.getAttribute('aria-expanded'), rotulo: b.getAttribute('aria-label'), dica: b.title,
    meta: document.querySelector('meta[name="theme-color"]').content, fundo: cs(document.body).backgroundColor, fundoImg: cs(document.body).backgroundImage, tinta: cs(document.body).color,
    h1: { letra: cs(h1).fontFamily.split(',')[0].trim().replace(/\x22/g, ''), peso: cs(h1).fontWeight, tam: parseFloat(cs(h1).fontSize), esp: cs(h1).letterSpacing }, h3: { letra: cs(h3).fontFamily.split(',')[0].trim().replace(/\x22/g, ''), peso: cs(h3).fontWeight, tam: parseFloat(cs(h3).fontSize) },
    corpo: cs(document.querySelector('.topo-t p, .nav button')).fontFamily.split(',')[0].trim().replace(/\x22/g, ''),
    marcado: [...document.querySelectorAll('#pop-tema [data-tema-id]')].filter(o => o.getAttribute('aria-checked') === 'true').map(o => o.dataset.temaId),
    foco: document.activeElement.dataset.temaId || document.activeElement.id || document.activeElement.tagName,
    guardado: (JSON.parse(localStorage.getItem('%s') || '{}').cfg || {}).tema }; }""" % CHAVE
QUADRO = """() => { const p = document.querySelector('#pop-tema'), r = p.getBoundingClientRect(), cs = e => getComputedStyle(e);
  return { visivel: cs(p).display !== 'none' && r.width > 0, caixa: [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)], janela: [innerWidth, innerHeight], papel: p.getAttribute('role'), nome: p.getAttribute('aria-label'),
    titulo: p.querySelector('.pop-h b').textContent, grupo: p.querySelector('[role=radiogroup]').getAttribute('aria-labelledby') === p.querySelector('.pop-h b').id, nota: p.querySelector('.pop-n').textContent, notaVisivel: p.querySelector('.pop-n').getBoundingClientRect().height > 0,
    marcadaVisivel: [...p.querySelectorAll('[aria-checked="true"]')].every(o => { const ro = o.getBoundingClientRect(); return ro.top >= r.top && ro.bottom <= r.bottom; }),
    opcoes: [...p.querySelectorAll('[data-tema-id]')].map(o => { const am = o.querySelector('.tema-am'), n = o.querySelector('.tema-n'), ro = o.getBoundingClientRect();
      return { id: o.dataset.temaId, papel: o.getAttribute('role'), marcado: o.getAttribute('aria-checked'), tab: o.tabIndex, nome: n.textContent, frase: o.querySelector('em').textContent, alt: Math.round(ro.height),
        amostra: { tema: am.dataset.tema, fundo: cs(am).backgroundColor, cartao: cs(am.children[0]).backgroundColor, tinta: cs(am.children[1]).backgroundColor, destaque: cs(am.children[3]).backgroundColor, oculta: am.getAttribute('aria-hidden') },
        letra: cs(n).fontFamily.split(',')[0].trim().replace(/\x22/g, ''), cor: cs(n).color, corQuadro: cs(p.querySelector('.pop-h b')).color, visto: cs(o.querySelector('svg')).visibility }; }) }; }"""
# A letra embutida está mesmo desenhando? Compara três textos com a reserva monoespaçada: uma coincidência de largura
# numa frase não prova que a fonte falhou. As aspas em nomes de família variam entre versões do Chromium; retirá-las
# mantém a comparação igual, sem mudar o CSS que o painel usa.
DESENHA = """async fam => { await document.fonts.load('400 40px ' + fam); await document.fonts.ready; const m = (f, texto) => { const s = document.createElement('span'); s.textContent = texto; s.style.cssText = 'position:absolute;left:-9999px;white-space:nowrap;font:400 40px ' + f; document.body.appendChild(s); const w = s.getBoundingClientRect().width; s.remove(); return w; };
  const textos = ['Visão geral — Ação, coração', 'Biblioteca: 2614 livros e muitas histórias', 'Ilhas, memória, água e coração'];
  return { carregada: [...document.fonts].some(f => f.family.replace(/\x22/g, '') === fam.replace(/\x22/g, '') && f.status === 'loaded'), dif: textos.reduce((s, t) => s + Math.abs(m(fam + ', monospace', t) - m('monospace', t)), 0) }; }"""
ORNAMENTO = """() => { const p = (e, ps) => { const c = getComputedStyle(e, ps); return { tem: c.content !== 'none' && c.content !== 'normal' && c.display !== 'none', img: c.backgroundImage !== 'none', pos: c.position, z: c.zIndex, toque: c.pointerEvents, alt: parseFloat(c.height) || 0, borda: c.borderTopWidth }; };
  return { ceu: p(document.body, '::before'), fio: p(document.querySelector('.topo'), '::after') }; }"""
LARGURA = """() => { const d = document.documentElement, t = document.querySelector('.topo-t').getBoundingClientRect(), a = document.querySelector('.topo-a').getBoundingClientRect(), h1 = document.querySelector('.topo h1');
  const v = document.querySelector('.visao:not([hidden])');
  return { sobra: d.scrollWidth - d.clientWidth, invade: Math.round(t.right - a.left), h1corta: getComputedStyle(h1).overflowY === 'visible' ? 0 : h1.scrollHeight - h1.clientHeight,      // só conta onde o título corta o que sobra (no celular)
    h3: [...v.querySelectorAll('.card h3')].filter(h => h.getBoundingClientRect().width > 0 && h.scrollWidth > h.clientWidth + 1).map(h => h.textContent).slice(0, 3) }; }"""


def rgb(h):
    h = h.lstrip('#'); return 'rgb(%d, %d, %d)' % tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def abre(b, largura=1366, altura=768, esquema='light', url=PAINEL_LIMPO, espia=False):
    ctx = b.new_context(viewport={'width': largura, 'height': altura}, locale='pt-BR', timezone_id='America/Sao_Paulo', color_scheme=esquema)
    pg = ctx.new_page(); fixa(pg)
    if espia:      # anota cada vez que o tema da página é posto, e em que ponto do carregamento
        pg.add_init_script("window.__temas = []; new MutationObserver(() => window.__temas.push([document.documentElement.dataset.tema, document.readyState])).observe(document, { subtree: true, attributes: true, attributeFilter: ['data-tema'] });")
    pg.on('console', lambda m: errs.append(f'[{m.type}] {m.text}') if m.type in ('error', 'warning') else None)
    pg.on('pageerror', lambda e: errs.append(f'[pageerror] {e}'))
    pg.goto(url); pg.wait_for_timeout(1300)
    if pg.is_visible('#aviso .pri'): pg.click('#aviso .pri'); pg.wait_for_timeout(200)
    return pg


def escolhe(pg, tema):
    if not pg.evaluate("() => document.querySelector('#pw-tema').classList.contains('aberto')"): pg.click('#b-tema'); pg.wait_for_timeout(200)
    pg.click(f'#pop-tema [data-tema-id={tema}]'); pg.wait_for_timeout(500)
    pg.keyboard.press('Escape'); pg.wait_for_timeout(250)


with sync_playwright() as p:
    b = p.chromium.launch()

    print('D. Sem escolha feita: o padrão do sistema, como sempre foi')
    for esquema, esperado in (('light', 'claro'), ('dark', 'escuro')):
        pg = abre(b, esquema=esquema)
        e = pg.evaluate(ESTADO); t = next(x for x in TEMAS if x['id'] == esperado)
        ok(f'sistema em modo {esperado}: o painel abre no tema {t["n"]}', e['tema'] == esperado and e['meta'] == t['cor'] and e['fundo'] == rgb(t['cor']) and not e['guardado'], (e['tema'], e['meta'], e['fundo'], e['guardado']))
        ok('…com os títulos na letra, no peso e no tamanho de antes', e['h1'] == {'letra': SERIF_PADRAO, 'peso': '600', 'tam': 27, 'esp': '-0.405px'} and e['h3'] == {'letra': SERIF_PADRAO, 'peso': '600', 'tam': 16.5}, (e['h1'], e['h3']))
        o = pg.evaluate(ORNAMENTO)
        ok('…e sem ornamento nenhum', not o['ceu']['tem'] and not o['fio']['tem'] and e['fundoImg'] == 'none', o)
        if esquema == 'light':
            ok('o botão da paleta diz qual é o tema e o que ele faz', e['rotulo'] == 'Aparência: tema Claro. Trocar o tema' and e['dica'] == 'Trocar o tema do painel' and e['expandido'] == 'false' and not e['aberto'] and pg.get_attribute('#b-tema', 'aria-controls') == 'pop-tema' and pg.get_attribute('#b-tema', 'aria-haspopup') is None, (e['rotulo'], e['dica']))
        pg.context.close()

    print('E. O quadro dos temas')
    pg = abre(b)
    ok('fechado, o quadro não aparece', not pg.evaluate(QUADRO)['visivel'])
    pg.click('#b-tema'); pg.wait_for_timeout(300)
    q = pg.evaluate(QUADRO); e = pg.evaluate(ESTADO)
    ok('o botão abre o quadro "Aparência", logo abaixo dele e dentro da janela', q['visivel'] and e['aberto'] and e['expandido'] == 'true' and q['titulo'] == 'Aparência' and q['nome'] == 'Aparência' and q['caixa'][0] >= 12 and q['caixa'][2] <= q['janela'][0] - 12 and q['caixa'][3] <= q['janela'][1] - 12, q['caixa'])
    ok('uma opção por tema, na ordem de TEMAS, com o nome e a frase de cada um', [(o['id'], o['nome'], o['frase']) for o in q['opcoes']] == [(t['id'], t['n'], t['d']) for t in TEMAS], [o['id'] for o in q['opcoes']])
    ok('é um grupo de opções de escolha única, com nome', q['grupo'] and all(o['papel'] == 'radio' for o in q['opcoes']))
    ok('a opção do tema em uso vem marcada — só ela —, com o sinal de visto, e recebe o foco', [o['id'] for o in q['opcoes'] if o['marcado'] == 'true'] == ['claro'] == [o['id'] for o in q['opcoes'] if o['visto'] == 'visible'] == [o['id'] for o in q['opcoes'] if o['tab'] == 0] and e['foco'] == 'claro', e['foco'])
    ok('cada amostra mostra as cores do seu tema: fundo, cartão, tinta e destaque', all(o['amostra'] == {'tema': o['id'], 'fundo': rgb(BLOCOS[o['id']]['--bg']), 'cartao': rgb(BLOCOS[o['id']]['--surface']), 'tinta': rgb(BLOCOS[o['id']]['--ink']), 'destaque': rgb(BLOCOS[o['id']]['--accent']), 'oculta': 'true'} for o in q['opcoes']), [o['amostra'] for o in q['opcoes'] if o['amostra']['fundo'] != rgb(BLOCOS[o['id']]['--bg'])])
    ok('cada nome vem na letra do seu tema, na cor do quadro (não na do tema da amostra)', all(o['letra'] == BLOCOS[o['id']]['--serif'].split(',')[0].strip('"') and o['cor'] == o['corQuadro'] for o in q['opcoes']), [(o['id'], o['letra'], o['cor']) for o in q['opcoes']])
    ok('a nota diz o que o tema troca e onde a escolha fica', q['notaVisivel'] and 'cores' in q['nota'] and 'letra dos títulos' in q['nota'] and 'neste navegador' in q['nota'], q['nota'])
    ok('as opções têm altura boa para o dedo (44 px ou mais)', all(o['alt'] >= 44 for o in q['opcoes']), [o['alt'] for o in q['opcoes']])

    print('F. Escolher um tema')
    for t in NOVOS:
        pg.click(f'#pop-tema [data-tema-id={t["id"]}]'); pg.wait_for_timeout(600)
        e = pg.evaluate(ESTADO); q = pg.evaluate(QUADRO); v = BLOCOS[t['id']]; fam = v['--serif'].split(',')[0].strip('"')
        ok(f'{t["n"]}: a página troca na hora, com o quadro ainda aberto para experimentar outro', e['tema'] == t['id'] and e['aberto'] and e['marcado'] == [t['id']], (e['tema'], e['aberto'], e['marcado']))
        ok(f'{t["n"]}: fundo, tinta e a cor da barra do navegador são as do tema', e['fundo'] == rgb(v['--bg']) and e['tinta'] == rgb(v['--ink']) and e['meta'] == t['cor'], (e['fundo'], e['tinta'], e['meta']))
        ok(f'{t["n"]}: os títulos passam para a letra do tema, no peso e na escala dele', e['h1']['letra'] == fam == e['h3']['letra'] and e['h1']['peso'] == v['--tit-peso'] == e['h3']['peso'] and abs(e['h1']['tam'] - 27 * float(v['--tit-esc'])) < .02 and abs(e['h3']['tam'] - 16.5 * float(v['--tit-esc'])) < .02 and e['h1']['esp'] in ('normal', '0px'), (e['h1'], e['h3']))
        d = pg.evaluate(DESENHA, fam)
        ok(f'{t["n"]}: a letra {fam} está carregada e desenhando', d['carregada'] and d['dif'] > 5, d)
        ok(f'{t["n"]}: o texto corrido, os botões e os números continuam na letra de sempre', e['corpo'] == 'Inter', e['corpo'])
        ok(f'{t["n"]}: o botão passa a dizer o nome do tema', e['rotulo'] == f'Aparência: tema {t["n"]}. Trocar o tema', e['rotulo'])
        ok(f'{t["n"]}: a escolha fica guardada no navegador', e['guardado'] == t['id'], e['guardado'])
        ok(f'{t["n"]}: as amostras não mudam com o tema em uso', all(o['amostra']['fundo'] == rgb(BLOCOS[o['id']]['--bg']) and o['amostra']['destaque'] == rgb(BLOCOS[o['id']]['--accent']) and o['letra'] == BLOCOS[o['id']]['--serif'].split(',')[0].strip('"') for o in q['opcoes']))
    pg.context.close()

    print('G. A escolha volta ao recarregar — antes de a página aparecer')
    pg = abre(b, esquema='dark', espia=True)          # o sistema em modo escuro: a escolha vale mais que ele
    escolhe(pg, 'holmes'); pg.wait_for_timeout(300)
    pg.reload(); pg.wait_for_timeout(1300)
    e = pg.evaluate(ESTADO); visto = pg.evaluate('() => window.__temas')
    ok('depois de recarregar, o tema é o escolhido — um tema claro, com o sistema em modo escuro', e['tema'] == 'holmes' and e['guardado'] == 'holmes' and e['marcado'] == ['holmes'] and e['meta'] == next(t['cor'] for t in TEMAS if t['id'] == 'holmes'), (e['tema'], e['meta']))
    ok('…posto ainda durante o carregamento, sem passar por outro tema', bool(visto) and visto[0] == ['holmes', 'loading'] and all(x[0] == 'holmes' for x in visto), visto)
    escolhe(pg, 'claro'); pg.reload(); pg.wait_for_timeout(1300)
    e = pg.evaluate(ESTADO)
    ok('voltar ao padrão também fica guardado (o claro, com o sistema em modo escuro)', e['tema'] == 'claro' and e['guardado'] == 'claro' and e['h1']['letra'] == SERIF_PADRAO and e['h1']['peso'] == '600', (e['tema'], e['h1']))
    # um tema que deixou de existir (ou um valor estragado): vale o padrão, sem erro
    pg.evaluate("() => { const o = JSON.parse(localStorage.getItem('%s')); o.cfg.tema = 'gotico'; localStorage.setItem('%s', JSON.stringify(o)); }" % (CHAVE, CHAVE))
    pg.reload(); pg.wait_for_timeout(1300)
    e = pg.evaluate(ESTADO)
    ok('tema guardado que não existe: o painel abre no padrão do sistema, sem erro', e['tema'] == 'escuro' and e['marcado'] == ['escuro'], (e['tema'], e['marcado']))
    pg.context.close()

    print('H. Pelo teclado e pelo mouse')
    pg = abre(b)
    pg.focus('#b-tema'); pg.keyboard.press('Enter'); pg.wait_for_timeout(300)
    e = pg.evaluate(ESTADO)
    ok('Enter no botão abre o quadro e leva o foco à opção marcada', e['aberto'] and e['foco'] == 'claro', e['foco'])
    pg.keyboard.press('ArrowDown'); pg.wait_for_timeout(300); e1 = pg.evaluate(ESTADO)
    pg.keyboard.press('ArrowDown'); pg.wait_for_timeout(300); e2 = pg.evaluate(ESTADO)
    ok('seta para baixo anda para a opção seguinte e já a escolhe', (e1['tema'], e1['foco'], e1['marcado']) == ('escuro', 'escuro', ['escuro']) and (e2['tema'], e2['foco']) == ('lovecraft', 'lovecraft'), (e1['tema'], e2['tema']))
    pg.keyboard.press('End'); pg.wait_for_timeout(300); e1 = pg.evaluate(ESTADO)
    pg.keyboard.press('ArrowDown'); pg.wait_for_timeout(300); e2 = pg.evaluate(ESTADO)
    pg.keyboard.press('ArrowUp'); pg.wait_for_timeout(300); e3 = pg.evaluate(ESTADO)
    pg.keyboard.press('Home'); pg.wait_for_timeout(300); e4 = pg.evaluate(ESTADO)
    ok('End vai à última, a seta dá a volta, seta para cima volta e Home vai à primeira', [x['tema'] for x in (e1, e2, e3, e4)] == [IDS[-1], IDS[0], IDS[-1], IDS[0]] and e4['foco'] == IDS[0], [x['tema'] for x in (e1, e2, e3, e4)])
    pg.keyboard.press('ArrowRight'); pg.keyboard.press('ArrowRight'); pg.wait_for_timeout(300)
    pg.keyboard.press('Escape'); pg.wait_for_timeout(300); e = pg.evaluate(ESTADO)
    ok('Esc fecha o quadro, devolve o foco ao botão e mantém o tema escolhido', not e['aberto'] and e['expandido'] == 'false' and e['foco'] == 'b-tema' and e['tema'] == 'lovecraft' and not pg.evaluate(QUADRO)['visivel'], (e['aberto'], e['foco'], e['tema']))
    ok('…e o Esc não fechou mais nada nem deixou a página travada', not pg.evaluate("() => document.documentElement.classList.contains('travado')"))
    pg.keyboard.press('Enter'); pg.wait_for_timeout(300); pg.keyboard.press('Tab'); pg.wait_for_timeout(300); e = pg.evaluate(ESTADO)
    ok('Tab para fora do quadro fecha-o (só a opção marcada entra na ordem do Tab)', not e['aberto'] and e['foco'] == 'b-dados', (e['aberto'], e['foco']))
    pg.click('#b-tema'); pg.wait_for_timeout(300); pg.mouse.click(100, 520); pg.wait_for_timeout(300)      # um ponto vazio da barra lateral
    ok('clicar fora fecha', not pg.evaluate(ESTADO)['aberto'])
    pg.click('#b-tema'); pg.wait_for_timeout(300); pg.click('#b-tema'); pg.wait_for_timeout(300)
    ok('clicar de novo no botão fecha', not pg.evaluate(ESTADO)['aberto'])
    # o quadro dos temas cobre os botões dos filtros: para chegar a eles com o quadro aberto, só pelo código
    pg.click('#b-tema'); pg.wait_for_timeout(300); pg.evaluate("() => document.querySelector('#pw-mais .pop-b').click()"); pg.wait_for_timeout(300)
    um = pg.evaluate("() => [...document.querySelectorAll('.pop-w.aberto')].map(w => w.id)")
    pg.click('#b-tema'); pg.wait_for_timeout(300)
    outro = pg.evaluate("() => [...document.querySelectorAll('.pop-w.aberto')].map(w => w.id)")
    ok('só um quadro aberto por vez: abrir "Mais filtros" fecha o dos temas, e vice-versa', um == ['pw-mais'] and outro == ['pw-tema'], (um, outro))
    pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
    escolhe(pg, 'moby'); pg.click('#b-dados'); pg.wait_for_timeout(400)
    ok('com o tema trocado, as caixas de diálogo abrem normalmente', pg.evaluate("() => document.querySelector('#dlg').classList.contains('on')"))
    pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
    pg.context.close()

    print('I. O ornamento de cada tema')
    pg = abre(b)
    for t in NOVOS:
        escolhe(pg, t['id']); o = pg.evaluate(ORNAMENTO); e = pg.evaluate(ESTADO)
        if t['id'] == 'lovecraft':
            ok('Lovecraft: um céu de estrelas atrás da página, fixo, que não atrapalha o clique', o['ceu']['tem'] and o['ceu']['img'] and o['ceu']['pos'] == 'fixed' and o['ceu']['z'] == '-1' and o['ceu']['toque'] == 'none' and not o['fio']['tem'], o)
        elif t['id'] == 'holmes':
            ok('Sherlock Holmes: o fio duplo sob o título da página', o['fio']['tem'] and o['fio']['borda'] == '2px' and o['fio']['alt'] >= 4 and o['fio']['toque'] == 'none' and not o['ceu']['tem'], o)
        elif t['id'] == 'moby':
            ok('Moby Dick: a linha de ondas sob o título da página', o['fio']['tem'] and o['fio']['img'] and o['fio']['alt'] >= 6 and o['fio']['toque'] == 'none' and not o['ceu']['tem'], o)
        elif t['id'] == 'deserto':
            ok('Deserto: o sulco de duas linhas sob o título da página', o['fio']['tem'] and o['fio']['borda'] == '1px' and o['fio']['alt'] >= 5 and o['fio']['toque'] == 'none' and not o['ceu']['tem'], o)
        elif t['id'] == 'terras':
            ok('Terras antigas: a linha de folhas sob o título da página', o['fio']['tem'] and o['fio']['img'] and o['fio']['alt'] >= 8 and o['fio']['toque'] == 'none' and not o['ceu']['tem'], o)
        elif t['id'] == 'greco':
            ok('Clássico greco-romano: o meandro sob o título da página', o['fio']['tem'] and o['fio']['img'] and o['fio']['alt'] >= 6 and o['fio']['toque'] == 'none' and not o['ceu']['tem'], o)
        else:
            ok(f'{t["n"]}: falta definir neste teste qual é o ornamento combinado', False)
        ok(f'{t["n"]}: no máximo um ornamento, e o fundo da página continua de uma cor só', o['ceu']['tem'] + o['fio']['tem'] <= 1 and e['fundoImg'] == 'none', (o['ceu']['tem'], o['fio']['tem'], e['fundoImg']))
    pg.context.close()

    print('J. Nada sai do lugar')
    com_sinopse = 'Fundação'
    for largura, altura, nome in ((1366, 768, 'computador'), (390, 780, 'celular')):
        pg = abre(b, largura, altura, url=PAINEL_URL if largura > 820 else PAINEL_LIMPO)
        nav = '#nav' if largura > 820 else '#nav-m'
        for t in NOVOS:
            escolhe(pg, t['id']); ruins = {}
            for v in VISOES:
                pg.click(f'{nav} [data-ir={v}]'); pg.wait_for_timeout(700)
                m = pg.evaluate(LARGURA)
                if m['sobra'] > 0 or m['invade'] > 0 or m['h3'] or m['h1corta'] > 0: ruins[v] = m
            ok(f'{t["n"]}, {nome} ({largura} px): nas seis telas nada estoura a largura, o título não invade os botões nem perde um pedaço das letras, e os títulos dos cartões cabem', not ruins, ruins)
            pg.click(f'{nav} [data-ir=geral]'); pg.wait_for_timeout(600)
            pg.fill('#p-tab-geral input[type=search]', com_sinopse); pg.wait_for_timeout(600)
            pg.evaluate("t => [...document.querySelectorAll('#p-tab-geral tbody tr[data-id]')].find(tr => tr.querySelector('.tt b').textContent.trim() === t).click()", com_sinopse); pg.wait_for_timeout(700)
            f = pg.evaluate("""() => { const g = document.querySelector('#gaveta'), c = g.querySelector('.gv-c'), h2 = g.querySelector('#gv-topo h2'), s = g.querySelector('.gv-sin-tx'), cs = e => getComputedStyle(e);
              return { aberta: g.classList.contains('on'), sobra: c.scrollWidth - c.clientWidth, pagina: document.documentElement.scrollWidth - innerWidth, h2: cs(h2).fontFamily.split(',')[0].trim().replace(/\x22/g, ''), sin: cs(s).fontFamily.split(',')[0].trim().replace(/\x22/g, ''), tam: parseFloat(cs(s).fontSize), peso: cs(s).fontWeight }; }""")
            fam = BLOCOS[t['id']]['--serif'].split(',')[0].strip('"')
            ok(f'{t["n"]}, {nome}: a ficha cabe na largura, com o título e a sinopse na letra do tema (sinopse com 15 px ou mais, em peso normal)', f['aberta'] and f['sobra'] <= 0 and f['pagina'] <= 0 and f['h2'] == fam == f['sin'] and f['tam'] >= 15 and f['peso'] == '400', f)
            pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
            pg.fill('#p-tab-geral input[type=search]', ''); pg.wait_for_timeout(300)
        if largura <= 820:
            pg.click('#b-tema'); pg.wait_for_timeout(300); q = pg.evaluate(QUADRO)
            ok('no celular, o quadro dos temas cabe na tela, com 12 px de folga dos lados', q['visivel'] and q['caixa'][0] >= 12 and q['caixa'][2] <= q['janela'][0] - 12 and q['caixa'][3] <= q['janela'][1] and q['notaVisivel'], q['caixa'])
            ok('…e a última escolha aparece inteira, mesmo quando a lista precisa rolar', q['marcadaVisivel'], q['caixa'])
            pg.keyboard.press('Home'); pg.wait_for_timeout(250); primeiro = pg.evaluate(QUADRO)
            pg.keyboard.press('End'); pg.wait_for_timeout(250); ultimo = pg.evaluate(QUADRO)
            ok('…Home e End alcançam as duas pontas da lista sem esconder a opção escolhida', primeiro['marcadaVisivel'] and ultimo['marcadaVisivel'] and primeiro['opcoes'][0]['marcado'] == 'true' and ultimo['opcoes'][-1]['marcado'] == 'true', (primeiro['caixa'], ultimo['caixa']))
            pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
            pg.set_viewport_size({'width': 320, 'height': 568}); pg.wait_for_timeout(400)
            pg.click('#b-tema'); pg.wait_for_timeout(300); q = pg.evaluate(QUADRO); m = pg.evaluate(LARGURA)
            ok('…e também numa tela de 320 px', q['visivel'] and q['caixa'][0] >= 12 and q['caixa'][2] <= 320 - 12 and m['sobra'] <= 0, (q['caixa'], m['sobra']))
            pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
        pg.context.close()

    print('K. No papel')
    pg = abre(b)
    escolhe(pg, 'lovecraft')
    imp = pg.evaluate("() => { const i = document.querySelector('#impressao'), c = getComputedStyle(i); return { tema: i.dataset.tema, serif: c.getPropertyValue('--serif').trim().split(',')[0].replace(/\x22/g, ''), peso: c.getPropertyValue('--tit-peso').trim(), tinta: c.getPropertyValue('--ink').trim() }; }")
    ok('a folha de impressão das listas não muda com o tema: letra e cores do padrão claro', imp == {'tema': 'claro', 'serif': SERIF_PADRAO, 'peso': '600', 'tinta': BLOCOS['claro']['--ink']}, imp)
    pg.evaluate("() => window.dispatchEvent(new Event('beforeprint'))"); durante = pg.evaluate("() => document.documentElement.dataset.tema")
    pg.evaluate("() => window.dispatchEvent(new Event('afterprint'))"); depois = pg.evaluate("() => document.documentElement.dataset.tema")
    ok('imprimir a página num tema escuro usa o padrão claro, e o tema volta depois', (durante, depois) == ('claro', 'lovecraft'), (durante, depois))
    pg.emulate_media(media='print'); ceu = pg.evaluate("() => getComputedStyle(document.body, '::before').display"); pg.emulate_media(media='screen')
    ok('no papel não há céu de estrelas', ceu == 'none', ceu)
    escolhe(pg, 'holmes')
    pg.evaluate("() => window.dispatchEvent(new Event('beforeprint'))"); durante = pg.evaluate("() => document.documentElement.dataset.tema")
    pg.evaluate("() => window.dispatchEvent(new Event('afterprint'))")
    ok('num tema claro, a página é impressa no próprio tema', durante == 'holmes' and pg.evaluate("() => document.documentElement.dataset.tema") == 'holmes', durante)
    pg.context.close()

    print('L. Na pré-visualização isolada (sem armazenamento)')
    (TMP / 'wrap-temas.html').write_text('<!doctype html><html><body style="margin:0"><iframe id="f" sandbox="allow-scripts" src="' + PAINEL_LIMPO + '" style="width:100vw;height:100vh;border:0;display:block"></iframe></body></html>', encoding='utf-8')
    ctx = b.new_context(viewport={'width': 1280, 'height': 860}, locale='pt-BR', timezone_id='America/Sao_Paulo')
    pg = ctx.new_page(); fixa(pg)
    pg.on('console', lambda m: errs.append(f'[isolada {m.type}] {m.text}') if m.type in ('error', 'warning') else None)
    pg.on('pageerror', lambda e: errs.append(f'[isolada pageerror] {e}'))
    pg.goto((TMP / 'wrap-temas.html').as_uri()); pg.wait_for_timeout(1500)
    fr = pg.frames[1]
    fr.click('#aviso .pri'); pg.wait_for_timeout(200)
    fr.click('#b-tema'); pg.wait_for_timeout(300); fr.click('#pop-tema [data-tema-id=moby]'); pg.wait_for_timeout(600)
    r = fr.evaluate("() => ({ tema: document.documentElement.dataset.tema, fundo: getComputedStyle(document.body).backgroundColor, letra: getComputedStyle(document.querySelector('.topo h1')).fontFamily.split(',')[0].trim().replace(/\x22/g, '') })")
    ok('trocar de tema funciona enquanto a página estiver aberta, sem erro', r == {'tema': 'moby', 'fundo': rgb(BLOCOS['moby']['--bg']), 'letra': BLOCOS['moby']['--serif'].split(',')[0].strip('"')}, r)
    ctx.close()
    b.close()

print('FALHAS:', falhas); print('ERROS:', len(errs) + len(falhas)); [print('  ', x[:300]) for x in errs[:10]]
