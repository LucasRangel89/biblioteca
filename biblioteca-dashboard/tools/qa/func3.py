from caminhos import PAINEL_URL, TMP
from relogio import fixa
import json
from playwright.sync_api import sync_playwright
URL = PAINEL_URL
errs = []
K = "() => Object.fromEntries([...document.querySelectorAll('.visao:not([hidden]) .kpi')].map(k => [k.dataset.k, k.querySelector('.kpi-v b').textContent + ' ¦ ' + k.querySelector('.kpi-s').textContent]))"
TOAST = "() => [...document.querySelectorAll('#toasts .toast')].map(t => t.textContent).join(' || ')"
VAZIOS = "() => [...document.querySelectorAll('.visao:not([hidden]) .card')].map(c => c.querySelector('h3').textContent + ': ' + ([...c.querySelectorAll('.vazio')].filter(v => v.offsetParent).map(v => v.textContent.trim().slice(0, 70)).join(' / ') || 'com dados'))"
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={'width': 1440, 'height': 900}, locale='pt-BR', timezone_id='America/Sao_Paulo', accept_downloads=True)
    pg = ctx.new_page(); fixa(pg)
    pg.on('console', lambda m: errs.append(f'[{m.type}] {m.text}') if m.type in ('error', 'warning') else None)
    pg.on('pageerror', lambda e: errs.append(f'[pageerror] {e}'))
    pg.goto(URL); pg.wait_for_timeout(1200)
    # 1) registrar uma cotação própria num item da lista e editar outro
    pg.click('#nav [data-ir=precos]'); pg.wait_for_timeout(900)
    print('form cotação:', pg.evaluate("() => [...document.querySelectorAll('#p-cotacao select, #p-cotacao input')].map(x => (x.dataset.f || x.type) + '=' + x.value)"))
    pg.fill('#p-cotacao input[inputmode=decimal]', '19,90'); pg.click('#p-cotacao .cot-a .btn'); pg.wait_for_timeout(900)
    print('  toast:', pg.evaluate(TOAST)); print('  KPIs:', pg.evaluate(K))
    pg.fill('#p-cotacao input[inputmode=decimal]', 'abc'); pg.click('#p-cotacao .cot-a .btn'); pg.wait_for_timeout(500)
    print('  inválido -> toast:', pg.evaluate(TOAST), '| erro no campo:', pg.evaluate("() => !!document.querySelector('#p-cotacao .erro')"))
    # 2) novo livro
    pg.click('#b-novo'); pg.wait_for_timeout(400)
    pg.click('#dlg footer .pri'); pg.wait_for_timeout(300)
    print('novo sem título ->', pg.evaluate(TOAST), '| dlg aberto:', pg.evaluate("() => document.querySelector('#dlg').classList.contains('on')"))
    pg.fill('#dlg [data-f=t]', 'Livro de Teste <b>&'); pg.fill('#dlg [data-f=a]', 'Autora "Teste"')
    pg.select_option('#dlg [data-f=col]', 'desejo'); pg.wait_for_timeout(200)
    print('  campos visíveis:', pg.evaluate("() => [...document.querySelectorAll('#dlg [data-f]')].filter(x => x.offsetParent).map(x => x.dataset.f).join(',')"))
    pg.fill('#dlg [data-f=alvo]', '45'); pg.fill('#dlg [data-f=tags]', 'filosofia #teste-novo')
    pg.click('#dlg footer .pri'); pg.wait_for_timeout(900)
    print('  toast:', pg.evaluate(TOAST), '| gaveta:', pg.evaluate("() => document.querySelector('#gaveta').classList.contains('on') ? document.querySelector('#gaveta h2').innerHTML + ' · ' + [...document.querySelectorAll('#gaveta [data-acao]')].map(x => x.dataset.acao) : 'fechada'"))
    pg.keyboard.press('Escape'); pg.wait_for_timeout(400)
    # 3) limpar dados de exemplo
    pg.click('#b-dados'); pg.wait_for_timeout(400)
    print('dados:', pg.evaluate("() => [...document.querySelectorAll('#dlg .dd-n > div')].map(d => d.textContent)"), pg.evaluate("() => [...document.querySelectorAll('#dlg [data-x]')].map(x => x.dataset.x)"))
    pg.click('#dlg [data-x=limpar]'); pg.wait_for_timeout(400)
    print('  confirmar:', pg.inner_text('#dlg h2'), '|', pg.evaluate("() => [...document.querySelectorAll('#dlg footer button')].map(x => x.textContent)"))
    pg.click('#dlg footer .perigo, #dlg footer .pri'); pg.wait_for_timeout(1200)
    print('  toast:', pg.evaluate(TOAST), '| pill exemplo visível:', pg.is_visible('#b-exemplo'), '| aviso visível:', pg.is_visible('#aviso'))
    for v in ['geral', 'biblioteca', 'recs', 'desejos', 'precos']:
        pg.click(f'#nav [data-ir={v}]'); pg.wait_for_timeout(1000)
        print(' ', v.upper(), json.dumps(pg.evaluate(K), ensure_ascii=False))
        for l in pg.evaluate(VAZIOS): print('      ', l)
        pg.screenshot(path=f'{TMP}/shots/limpo-{v}.png', full_page=True)
    # 4) persistência do estado limpo + backup + restaurar exemplos
    pg.wait_for_timeout(600); pg.reload(); pg.wait_for_timeout(1300)
    print('após recarregar:', pg.inner_text('#titulo'), json.dumps(pg.evaluate(K), ensure_ascii=False))
    pg.click('#b-dados'); pg.wait_for_timeout(400)
    print('  ações:', pg.evaluate("() => [...document.querySelectorAll('#dlg [data-x]')].map(x => x.dataset.x + ':' + x.textContent.trim())"))
    with pg.expect_download() as d: pg.click('#dlg [data-x=exportar]')
    dl = d.value; dl.save_as(f'{TMP}/backup.json'); bk = json.load(open(f'{TMP}/backup.json', encoding='utf-8'))
    print('  backup:', dl.suggested_filename, {k: (len(v) if isinstance(v, (list, dict, str)) else v) for k, v in bk.items()})
    pg.click('#dlg [data-x=restaurar]'); pg.wait_for_timeout(1200)
    print('  restaurar -> toast:', pg.evaluate(TOAST), '| dlg:', pg.evaluate("() => document.querySelector('#dlg').classList.contains('on') ? document.querySelector('#dlg h2').textContent : 'fechado'"))
    if pg.evaluate("() => document.querySelector('#dlg').classList.contains('on') && !!document.querySelector('#dlg footer .pri, #dlg footer .perigo')"):
        pg.click('#dlg footer .perigo, #dlg footer .pri'); pg.wait_for_timeout(1200); print('  confirmado; toast:', pg.evaluate(TOAST))
    pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
    print('  KPIs:', json.dumps(pg.evaluate(K), ensure_ascii=False), '| pill exemplo:', pg.is_visible('#b-exemplo'))
    # 5) importar o backup "limpo" de volta
    pg.click('#b-dados'); pg.wait_for_timeout(400)
    pg.set_input_files('#arq', f'{TMP}/backup.json'); pg.wait_for_timeout(800)
    print('importar -> dlg:', pg.evaluate("() => document.querySelector('#dlg').classList.contains('on') ? document.querySelector('#dlg h2').textContent + ' ¦ ' + document.querySelector('#dlg .dlg-c').innerText.slice(0, 200) : 'fechado'"))
    if pg.evaluate("() => !!document.querySelector('#dlg.on footer .pri, #dlg.on footer .perigo')"):
        pg.click('#dlg footer .perigo, #dlg footer .pri'); pg.wait_for_timeout(1200)
    print('  toast:', pg.evaluate(TOAST), '| KPIs:', json.dumps(pg.evaluate(K), ensure_ascii=False))
    b.close()
print('ERROS:', len(errs)); [print('  ', x[:400]) for x in errs[:20]]
