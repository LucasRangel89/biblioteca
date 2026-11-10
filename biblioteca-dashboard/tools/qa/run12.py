from caminhos import PAINEL_URL, TMP
from relogio import fixa
from playwright.sync_api import sync_playwright
URL = PAINEL_URL
errs = []
with sync_playwright() as p:
    b = p.chromium.launch()
    for tema in ['light', 'dark']:
        ctx = b.new_context(viewport={'width': 1440, 'height': 900}, color_scheme=tema, locale='pt-BR', timezone_id='America/Sao_Paulo')
        pg = ctx.new_page(); fixa(pg)
        pg.on('console', lambda m: errs.append(f'[{m.type}] {m.text}') if m.type in ('error', 'warning') else None)
        pg.on('pageerror', lambda e: errs.append(f'[pageerror] {e}'))
        pg.goto(URL); pg.wait_for_timeout(1100)
        pg.click('#nav [data-ir=precos]'); pg.wait_for_timeout(900)
        tit = pg.evaluate("() => { const s = document.querySelector('#p-cotacao select[data-c=livro]'); return s.selectedOptions[0].textContent; }")
        pg.fill('#p-cotacao input[data-c=preco]', '31,90'); pg.click('#p-cotacao [data-c=ok]'); pg.wait_for_timeout(900)
        print(tema, '| livro do formulário:', tit, '| toast:', pg.evaluate("() => [...document.querySelectorAll('#toasts .toast')].map(t => t.textContent).join(' || ')"))
        pg.fill('#q', tit.split(' — ')[0].split(' · ')[0][:30]); pg.wait_for_timeout(500); pg.click('#q-r .qr >> nth=0'); pg.wait_for_timeout(800)
        pg.evaluate("() => { const a = document.querySelector('#gaveta [data-apagar]'); if (a) a.scrollIntoView({block: 'center'}); }"); pg.wait_for_timeout(400)
        print('   apagar:', pg.evaluate("() => [...document.querySelectorAll('#gaveta [data-apagar]')].map(a => a.dataset.apagar + ' | ' + a.textContent + ' | ' + getComputedStyle(a).color)"))
        pg.screenshot(path=f'{TMP}/shots/apagar-{tema}.png')
        ctx.close()
    b.close()
print('ERROS:', len(errs)); [print('  ', x[:300]) for x in errs[:10]]
