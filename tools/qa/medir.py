from caminhos import PAINEL_URL
from relogio import fixa
from playwright.sync_api import sync_playwright
URL = PAINEL_URL
with sync_playwright() as p:
    b = p.chromium.launch()
    for w in [1920, 1440, 1361, 1360, 1280, 1121, 1120, 1100, 1024, 960, 900, 821, 820, 800]:
        ctx = b.new_context(viewport={'width': w, 'height': 900}, locale='pt-BR', timezone_id='America/Sao_Paulo')
        pg = ctx.new_page(); fixa(pg); pg.goto(URL); pg.wait_for_timeout(900)
        linha = []
        for v in ['geral', 'biblioteca', 'recs', 'desejos', 'precos']:
            pg.evaluate(f"() => document.querySelector('#nav [data-ir={v}], #nav-m [data-ir={v}]').click()"); pg.wait_for_timeout(700)
            r = pg.evaluate(f"() => {{ const x = document.querySelector('#p-tab-{v} .tb-w'); const cab = getComputedStyle(document.querySelector('#p-tab-{v} thead')).display; return [x.scrollWidth, x.clientWidth, cab]; }}")
            linha.append(f"{v} {r[0]}/{r[1]}{'' if r[2] != 'none' else ' (cartões)'}{' <<< ROLA ' + str(r[0] - r[1]) if r[0] > r[1] + 1 else ''}")
        print(w, '|', ' | '.join(linha)); ctx.close()
    b.close()
