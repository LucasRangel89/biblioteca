from caminhos import PAINEL_URL, TMP
from relogio import fixa
from playwright.sync_api import sync_playwright
errs = []
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, locale='pt-BR', timezone_id='America/Sao_Paulo', has_touch=True, is_mobile=True)
    pg = ctx.new_page(); fixa(pg)
    pg.on('console', lambda m: errs.append(f'[{m.type}] {m.text}') if m.type in ('error', 'warning') else None)
    pg.on('pageerror', lambda e: errs.append(f'[pageerror] {e}'))
    pg.goto(PAINEL_URL); pg.wait_for_timeout(1200)
    pg.tap('#aviso .pri'); pg.wait_for_timeout(300)
    pg.tap('#busca'); pg.wait_for_timeout(400)
    print('foco:', pg.evaluate("() => document.activeElement.id"))
    pg.keyboard.type('duna'); pg.wait_for_timeout(500)
    pg.screenshot(path=f'{TMP}/shots/m-busca.png')
    print('resultados:', pg.evaluate("() => [...document.querySelectorAll('#q-r .qr')].map(x => x.innerText.replace(/\\n/g, ' · '))"))
    pg.tap('#q-r .qr >> nth=0'); pg.wait_for_timeout(700)
    print('gaveta:', pg.evaluate("() => document.querySelector('#gaveta').classList.contains('on') ? document.querySelector('#gaveta h2').textContent : 'fechada'"))
    pg.screenshot(path=f'{TMP}/shots/m-busca-2.png')
    # rolagem horizontal indevida?
    pg.tap('#gaveta [data-fechar] >> nth=1'); pg.wait_for_timeout(500)
    for v in ['geral', 'biblioteca', 'recs', 'desejos', 'precos']:
        pg.tap(f'#nav-m [data-ir={v}]'); pg.wait_for_timeout(900)
        print(v, pg.evaluate("() => ({sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth, largos: [...document.querySelectorAll('.visao:not([hidden]) *')].filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.right > document.documentElement.clientWidth + 1 && !e.closest('.abas, .f-per, .rolavel, svg, .tb-rol, .seg-rol'); }).slice(0, 5).map(e => e.tagName + '.' + e.className + ' ' + Math.round(e.getBoundingClientRect().right))})"))
    b.close()
print('ERROS:', len(errs)); [print('  ', x[:300]) for x in errs[:10]]
