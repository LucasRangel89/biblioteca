from caminhos import PAINEL_URL, TMP
from relogio import fixa
import json
from playwright.sync_api import sync_playwright
URL = PAINEL_URL
errs = []
K = "() => Object.fromEntries([...document.querySelectorAll('.visao:not([hidden]) .kpi')].map(k => [k.dataset.k, k.querySelector('.kpi-v b').textContent + ' ¦ ' + k.querySelector('.kpi-s').textContent]))"
TOAST = "() => { const t = [...document.querySelectorAll('#toasts .toast')].map(t => t.textContent); return t[t.length - 1] || ''; }"
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={'width': 1440, 'height': 900}, locale='pt-BR', timezone_id='America/Sao_Paulo')
    pg = ctx.new_page(); fixa(pg)
    pg.on('console', lambda m: errs.append(f'[{m.type}] {m.text}') if m.type in ('error', 'warning') else None)
    pg.on('pageerror', lambda e: errs.append(f'[pageerror] {e}'))
    pg.goto(URL); pg.wait_for_timeout(1200)
    pg.click('#b-novo'); pg.wait_for_timeout(400)
    pg.fill('#dlg [data-f=t]', 'Zz Livro Novo'); pg.fill('#dlg [data-f=a]', 'Fulana de Tal')
    pg.select_option('#dlg [data-f=col]', 'desejo'); pg.fill('#dlg [data-f=alvo]', '45')
    pg.click('#dlg footer .pri'); pg.wait_for_timeout(800); pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
    pg.click('#nav [data-ir=precos]'); pg.wait_for_timeout(1000)
    sel = '#p-cotacao select[data-c=livro]'
    ops = pg.evaluate(f"() => [...document.querySelector('{sel}').options].map(o => o.textContent)")
    print('opções:', len(ops), '| últimas:', ops[-2:], '| KPIs:', pg.evaluate(K)['monit'])
    novo = pg.evaluate(f"() => [...document.querySelector('{sel}').options].find(o => o.textContent.startsWith('Zz Livro Novo')).value")
    pg.select_option(sel, novo); pg.wait_for_timeout(700)
    print('após escolher: form =', pg.evaluate(f"() => document.querySelector('{sel}').selectedOptions[0].textContent"), '| gráfico =', pg.inner_text('#p-px-loja .card-s')[:60], '| links:', pg.inner_text('#p-cotacao .lb-t'))
    pg.fill('#p-cotacao input[data-c=preco]', '39,90'); pg.click('#p-cotacao [data-c=ok]'); pg.wait_for_timeout(900)
    print('1ª cotação:', pg.evaluate(TOAST), '| form =', pg.evaluate(f"() => document.querySelector('{sel}').selectedOptions[0].textContent"), '| gráfico =', pg.inner_text('#p-px-loja .card-s')[:60])
    print('  KPIs:', json.dumps(pg.evaluate(K), ensure_ascii=False))
    print('  resumo:', pg.evaluate("() => [...document.querySelectorAll('#p-px-loja .pr-i')].map(x => x.innerText.replace(/\\n/g, ' ')).join(' | ')"))
    print('  marcadores:', pg.evaluate("() => document.querySelectorAll('#p-px-loja .g-pts circle').length"))
    pg.locator('#p-px-loja').screenshot(path=f'{TMP}/shots/px-1ponto.png')
    # loja personalizada, 3 dias antes
    pg.select_option('#p-cotacao select[data-c=loja]', '__outra'); pg.wait_for_timeout(200)
    pg.fill('#p-cotacao input[data-c=outra]', 'Livraria da Vila'); pg.fill('#p-cotacao input[data-c=preco]', '52')
    pg.fill('#p-cotacao input[data-c=data]', '2026-11-06'); pg.click('#p-cotacao [data-c=ok]'); pg.wait_for_timeout(900)
    print('2ª cotação:', pg.evaluate(TOAST), '| legenda:', pg.inner_text('#p-px-loja .card-f').replace('\n', ' · '))
    pg.fill('#p-cotacao input[data-c=preco]', '47,50'); pg.fill('#p-cotacao input[data-c=data]', '2026-11-08'); pg.click('#p-cotacao [data-c=ok]'); pg.wait_for_timeout(900)
    print('3ª cotação:', pg.evaluate(TOAST), '| resumo:', pg.evaluate("() => [...document.querySelectorAll('#p-px-loja .pr-i')].map(x => x.innerText.replace(/\\n/g, ' ')).join(' | ')"))
    print('  marcadores:', pg.evaluate("() => document.querySelectorAll('#p-px-loja .g-pts circle').length"))
    pg.locator('#p-px-loja').screenshot(path=f'{TMP}/shots/px-3pontos.png')
    # data futura
    pg.fill('#p-cotacao input[data-c=preco]', '40'); pg.fill('#p-cotacao input[data-c=data]', '2026-12-01'); pg.click('#p-cotacao [data-c=ok]'); pg.wait_for_timeout(500)
    print('data futura ->', pg.evaluate(TOAST))
    # a linha na tabela
    pg.fill('#p-tab-precos input[type=search]', 'Zz Livro'); pg.wait_for_timeout(600)
    print('tabela:', pg.evaluate("() => [...document.querySelectorAll('#p-tab-precos tbody tr')].map(r => r.innerText.replace(/\\s*\\n\\s*/g, ' | '))"))
    # gaveta do item: histórico por loja + excluir cotação?
    pg.click('#p-tab-precos tbody tr'); pg.wait_for_timeout(700)
    print('gaveta:', pg.evaluate("() => [...document.querySelectorAll('#gaveta .gv-c h3, #gaveta .gv-c h4')].map(h => h.textContent)"), '| ações:', pg.evaluate("() => [...document.querySelectorAll('#gaveta [data-acao]')].map(x => x.dataset.acao)"))
    pg.locator('#gaveta .gv').screenshot(path=f'{TMP}/shots/gaveta-novo.png') if pg.locator('#gaveta .gv').count() else pg.screenshot(path=f'{TMP}/shots/gaveta-novo.png')
    # apagar cotação própria
    print('apagar: botões =', pg.evaluate("() => [...document.querySelectorAll('#gaveta [data-apagar]')].map(x => x.dataset.apagar + '@' + x.dataset.dia)"))
    pg.click('#gaveta [data-apagar="Livraria da Vila"]'); pg.wait_for_timeout(400)
    print('  confirmação:', pg.inner_text('#dlg h2'), '|', pg.inner_text('#dlg .dlg-msg'))
    pg.click('#dlg footer .perigo'); pg.wait_for_timeout(800)
    print('  toast:', pg.evaluate(TOAST), '| lojas agora:', pg.evaluate("() => [...document.querySelectorAll('#gaveta .fontes tbody tr')].map(r => r.innerText.replace(/\\s*\\n\\s*/g, ' | ').replace(/\\t/g, ' | '))"))
    pg.click('#gaveta [data-apagar="Livraria da Vila"]'); pg.wait_for_timeout(300); pg.click('#dlg footer .perigo'); pg.wait_for_timeout(700)
    pg.click('#gaveta [data-apagar="Amazon"]'); pg.wait_for_timeout(300); pg.click('#dlg footer .perigo'); pg.wait_for_timeout(700)
    print('  sem nenhuma: seção de preços oculta =', pg.evaluate("() => document.querySelector('#gv-px').hidden"), '| fatos:', pg.evaluate("() => [...document.querySelectorAll('#gaveta .fatos > div')].map(d => d.innerText.replace(/\\n/g, ': ')).join(' ¦ ')"))
    pg.keyboard.press('Escape'); pg.wait_for_timeout(400)
    print('  KPIs:', json.dumps(pg.evaluate(K), ensure_ascii=False))
    b.close()
print('ERROS:', len(errs)); [print('  ', x[:400]) for x in errs[:20]]
