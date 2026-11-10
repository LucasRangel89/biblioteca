from caminhos import PAINEL_URL
from relogio import fixa
from playwright.sync_api import sync_playwright
URL = PAINEL_URL
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={'width': 1920, 'height': 900}, locale='pt-BR', timezone_id='America/Sao_Paulo')
    pg = ctx.new_page(); fixa(pg); pg.goto(URL); pg.wait_for_timeout(900)
    for v in ['geral', 'biblioteca', 'recs', 'desejos', 'precos']:
        pg.click(f'#nav [data-ir={v}]'); pg.wait_for_timeout(700)
        pg.select_option(f'#p-tab-{v} .tam select', '100'); pg.wait_for_timeout(500)
        r = pg.evaluate(f"() => {{ const t = document.querySelector('#p-tab-{v} .tb'); t.style.width = '1px'; const o = [...t.querySelectorAll('th')].map(h => h.dataset.c + ' ' + Math.round(h.getBoundingClientRect().width)); const w = Math.round(t.getBoundingClientRect().width); t.style.width = ''; return [w, o]; }}")
        print(v, r[0], '|', ' · '.join(r[1]))
    b.close()
