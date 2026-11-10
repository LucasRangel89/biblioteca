"""Telas largas (1920 e 2560): primeira dobra de cada visão + medidas da área útil."""
from caminhos import PAINEL_URL, TMP
from relogio import fixa
from playwright.sync_api import sync_playwright
URL = PAINEL_URL
errs = []
with sync_playwright() as p:
    b = p.chromium.launch()
    for w, h in [(1920, 1080), (2560, 1440)]:
        ctx = b.new_context(viewport={'width': w, 'height': h}, locale='pt-BR', timezone_id='America/Sao_Paulo')
        pg = ctx.new_page(); fixa(pg)
        pg.on('console', lambda m: errs.append(f'[{m.type}] {m.text}') if m.type in ('error', 'warning') else None)
        pg.on('pageerror', lambda e: errs.append(f'[pageerror] {e}'))
        pg.goto(URL); pg.wait_for_timeout(1000); pg.click('#aviso .pri'); pg.wait_for_timeout(200)
        for v in ['geral', 'biblioteca', 'recs', 'desejos', 'precos']:
            pg.click(f'#nav [data-ir={v}]'); pg.wait_for_timeout(1000)
            m = pg.evaluate("() => { const s = document.querySelector('.visao:not([hidden])'), r = s.getBoundingClientRect(), k = [...s.querySelectorAll('.kpi')].map(x => Math.round(x.getBoundingClientRect().width)); const cs = [...s.querySelectorAll('.card')].map(c => c.getBoundingClientRect()); return { secao: [Math.round(r.left), Math.round(r.width)], kpis: k.slice(0, 6), maiorCard: Math.round(Math.max(...cs.map(c => c.width))), rolagemX: document.documentElement.scrollWidth - document.documentElement.clientWidth, alturaPag: document.documentElement.scrollHeight }; }")
            print(w, v, m)
            pg.screenshot(path=f'{TMP}/shots/l{w}-{v}.png')
        ctx.close()
    b.close()
print('ERROS:', len(errs)); [print('  ', e[:300]) for e in errs[:10]]
