from caminhos import PAINEL_URL
from relogio import fixa
from playwright.sync_api import sync_playwright
URL = PAINEL_URL
VIS = ['geral', 'biblioteca', 'recs', 'desejos', 'precos']
pior = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={'width': 1500, 'height': 900}, locale='pt-BR', timezone_id='America/Sao_Paulo')
    pg = ctx.new_page(); fixa(pg); pg.goto(URL); pg.wait_for_timeout(900)
    for v in VIS:
        pg.click(f'#nav [data-ir={v}]'); pg.wait_for_timeout(600); pg.select_option(f'#p-tab-{v} .tam select', '100'); pg.wait_for_timeout(400)
    for w in list(range(1500, 820, -17)) + [1366, 1361, 1360, 1280, 1121, 1120, 1024, 821]:
        pg.set_viewport_size({'width': w, 'height': 900}); pg.wait_for_timeout(150)
        linha = []
        for v in VIS:
            pg.evaluate(f"() => document.querySelector('#nav [data-ir={v}]').click()"); pg.wait_for_timeout(350)
            r = pg.evaluate(f"""() => {{ const k = document.querySelector('#p-tab-{v}'), x = k.querySelector('.tb-w'), cab = getComputedStyle(k.querySelector('thead')).display !== 'none';
                const ths = [...k.querySelectorAll('th')].filter(h => getComputedStyle(h).display !== 'none');
                return {{ sw: x.scrollWidth, cw: x.clientWidth, cab, n: ths.length, tit: Math.round(k.querySelector('th.c-tit').getBoundingClientRect().width), ord: getComputedStyle(k.querySelector('.ord-m')).display !== 'none', pag: document.documentElement.scrollWidth - document.documentElement.clientWidth }}; }}""")
            sobra = r['sw'] - r['cw']
            linha.append(f"{v[:4]} {'cart' if not r['cab'] else str(r['n']) + 'c tit ' + str(r['tit'])}{' ord' if r['ord'] else ''}{' !!ROLA ' + str(sobra) if sobra > 1 else ''}{' !!PAG ' + str(r['pag']) if r['pag'] > 0 else ''}")
            if sobra > 1: pior[(w, v)] = sobra
            if (not r['cab']) != r['ord']: pior[(w, v, 'ordenar')] = 'cartões sem seletor de ordem' if not r['cab'] else 'seletor sobrando'
        print(w, '|', ' | '.join(linha))
    b.close()
print('PROBLEMAS:', pior)
