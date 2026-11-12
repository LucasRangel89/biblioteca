from caminhos import PAINEL_URL
from relogio import fixa
import json
from playwright.sync_api import sync_playwright
URL = PAINEL_URL
errs = []
K = "() => Object.fromEntries([...document.querySelectorAll('.visao:not([hidden]) .kpi')].map(k => [k.dataset.k, k.querySelector('.kpi-v b').textContent]))"
TOAST = "() => { const t = [...document.querySelectorAll('#toasts .toast')].map(t => t.textContent); return t[t.length - 1] || ''; }"
GV = "() => document.querySelector('#gaveta').classList.contains('on') ? document.querySelector('#gaveta h2').textContent + ' [' + [...document.querySelectorAll('#gaveta [data-acao]')].map(x => x.dataset.acao).join(',') + ']' : 'fechada'"
DLG = "() => document.querySelector('#dlg').classList.contains('on') ? document.querySelector('#dlg h2').textContent : 'fechado'"
def ir(pg, v): pg.click(f'#nav [data-ir={v}]'); pg.wait_for_timeout(900)
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={'width': 1440, 'height': 900}, locale='pt-BR', timezone_id='America/Sao_Paulo')
    pg = ctx.new_page(); fixa(pg)
    pg.on('console', lambda m: errs.append(f'[{m.type}] {m.text}') if m.type in ('error', 'warning') else None)
    pg.on('pageerror', lambda e: errs.append(f'[pageerror] {e}'))
    pg.goto(URL); pg.wait_for_timeout(1200)
    # J) aviso
    print('aviso visível:', pg.is_visible('#aviso')); pg.click('#aviso .pri, #aviso [data-ok]'); pg.wait_for_timeout(300); print('  após Entendi:', pg.is_visible('#aviso'))
    # A) .li em Melhores oportunidades (guia Finanças)
    ir(pg, 'financas'); print('A) Finanças: KPIs', pg.evaluate(K))
    pg.click('#p-ranking .li >> nth=0'); pg.wait_for_timeout(600); print('A) li ->', pg.evaluate(GV)); pg.keyboard.press('Escape'); pg.wait_for_timeout(400); print('   esc ->', pg.evaluate(GV))
    # B) biblioteca: cabeceira → progresso; editar nota
    ir(pg, 'biblioteca'); k0 = pg.evaluate(K); print('B) KPIs', k0)
    pg.click('#p-lendo .li >> nth=0'); pg.wait_for_timeout(600); print('   cabeceira ->', pg.evaluate(GV))
    pg.click('#gaveta [data-acao=progresso]'); pg.wait_for_timeout(400); print('   dlg:', pg.evaluate(DLG))
    pg.evaluate("() => { const r = document.querySelector('#dlg [data-f=prog]'); r.value = 77; r.dispatchEvent(new Event('input', {bubbles: true})); }")
    print('   rótulo:', pg.inner_text('#pg-v')); pg.click('#dlg footer .pri'); pg.wait_for_timeout(700)
    print('   gaveta mostra:', pg.evaluate("() => (document.querySelector('#gaveta .fatos').innerText.match(/\\d+%/) || ['?'])[0]"))
    pg.click('#gaveta [data-acao=editar]'); pg.wait_for_timeout(400); print('   editar dlg:', pg.evaluate(DLG), '| campos:', pg.evaluate("() => [...document.querySelectorAll('#dlg [data-f]')].filter(x => x.offsetParent).map(x => x.dataset.f).join(',')"))
    pg.fill('#dlg [data-f=pago]', '61,5'); pg.fill('#dlg [data-f=loja]', 'Sebo do Teste'); pg.click('#dlg footer .pri'); pg.wait_for_timeout(700)
    print('   toast:', pg.evaluate(TOAST), '| fatos:', pg.evaluate("() => [...document.querySelectorAll('#gaveta .fatos > div')].map(d => d.innerText.replace(/\\n/g, ': ')).join(' ¦ ')")[:330])
    pg.keyboard.press('Escape'); pg.wait_for_timeout(400)
    # C) recs: desejar / tenho / monitorar
    ir(pg, 'recs'); print('C) KPIs', pg.evaluate(K), '| abas:', pg.evaluate("() => [...document.querySelectorAll('#p-tab-recs .abas [data-a]')].map(a => a.innerText.replace(/\\s+/g, ' '))"))
    pg.click('#p-tab-recs tbody tr >> nth=0'); pg.wait_for_timeout(600); t1 = pg.evaluate(GV); print('   rec 1:', t1)
    pg.click('#gaveta [data-acao=desejar]'); pg.wait_for_timeout(700); print('   desejar ->', pg.evaluate(TOAST), '|', pg.evaluate(GV)); pg.keyboard.press('Escape'); pg.wait_for_timeout(400)
    pg.click('#p-tab-recs tbody tr >> nth=0'); pg.wait_for_timeout(600); print('   rec 2:', pg.evaluate(GV))
    pg.click('#gaveta [data-acao=tenho]'); pg.wait_for_timeout(500); print('   tenho dlg:', pg.evaluate(DLG), '| campos:', pg.evaluate("() => [...document.querySelectorAll('#dlg [data-f]')].filter(x => x.offsetParent).map(x => x.dataset.f + '=' + x.value).join(', ')"))
    pg.click('#dlg footer .pri'); pg.wait_for_timeout(700); print('   ->', pg.evaluate(TOAST), '|', pg.evaluate(GV)); pg.keyboard.press('Escape'); pg.wait_for_timeout(400)
    pg.click('#p-tab-recs tbody tr >> nth=0'); pg.wait_for_timeout(600); print('   rec 3:', pg.evaluate(GV))
    pg.click('#gv-acoes [data-acao=cotar]'); pg.wait_for_timeout(500); print('   cotar dlg:', pg.evaluate(DLG))
    pg.fill('#dlg input[data-c=preco]', '33,30'); pg.click('#dlg [data-c=ok]'); pg.wait_for_timeout(700); print('   ->', pg.evaluate(TOAST))
    pg.click('#dlg footer .pri'); pg.wait_for_timeout(500); print('   após Concluir:', pg.evaluate(DLG), '|', pg.evaluate(GV))
    pg.click('#gaveta [data-acao=parar]'); pg.wait_for_timeout(600); print('   parar ->', pg.evaluate(TOAST), '|', pg.evaluate(GV))
    pg.click('#gaveta [data-acao=monitorar]'); pg.wait_for_timeout(600); print('   monitorar ->', pg.evaluate(TOAST)); pg.keyboard.press('Escape'); pg.wait_for_timeout(400)
    print('   KPIs', pg.evaluate(K))
    # D) desejos: tirar
    ir(pg, 'desejos'); print('D) KPIs', pg.evaluate(K))
    pg.click('#p-tab-desejos tbody tr >> nth=0'); pg.wait_for_timeout(600); print('   item:', pg.evaluate(GV))
    pg.click('#gaveta [data-acao=tirar]'); pg.wait_for_timeout(700); print('   tirar ->', pg.evaluate(TOAST), '|', pg.evaluate(GV)); pg.keyboard.press('Escape'); pg.wait_for_timeout(400)
    print('   KPIs', pg.evaluate(K))
    ir(pg, 'geral'); print('   geral', pg.evaluate(K)); ir(pg, 'biblioteca'); print('   biblioteca', pg.evaluate(K), '(antes', k0, ')')
    # F) período personalizado (o período fica no fim de "Mais filtros")
    ir(pg, 'geral'); pg.click('#pw-mais .pop-b'); pg.wait_for_timeout(300); print('F) período dentro de Mais filtros:', pg.is_visible('#f-periodo'))
    pg.click('#f-periodo button[data-v="90d"]'); pg.wait_for_timeout(700); print('   90 dias -> KPIs', pg.evaluate(K), '| chips:', pg.inner_text('#f-ativos').replace('\n', ' · '), '| contador de Mais filtros:', pg.inner_text('#pw-mais .pop-b .cont'))
    pg.click('#f-cal'); pg.wait_for_timeout(300); print('   custom visível:', pg.is_visible('#f-custom'), '| de/até:', pg.input_value('#f-de'), pg.input_value('#f-ate'))
    pg.fill('#f-de', '2026-01-01'); pg.dispatch_event('#f-de', 'change'); pg.fill('#f-ate', '2026-06-30'); pg.dispatch_event('#f-ate', 'change'); pg.wait_for_timeout(900)
    print('   KPIs', pg.evaluate(K), '| chips:', pg.inner_text('#f-ativos').replace('\n', ' · '), '| sub gráfico:', pg.inner_text('#p-evolucao .card-s'))
    pg.fill('#f-de', '2026-08-01'); pg.dispatch_event('#f-de', 'change'); pg.wait_for_timeout(700); print('   de > até:', pg.input_value('#f-de'), pg.input_value('#f-ate'), '| KPIs', pg.evaluate(K), '| chips:', pg.inner_text('#f-ativos').replace('\n', ' · '))
    pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
    pg.click('#f-ativos [data-rm^=periodo]'); pg.wait_for_timeout(700); print('   chip removido -> período ativo:', pg.evaluate("() => (document.querySelector('#f-periodo button[aria-pressed=true], #f-periodo button.on') || {textContent: '?'}).textContent"), '| custom visível:', pg.is_visible('#f-custom'))
    # G) mais filtros
    pg.click('#pw-mais .pop-b'); pg.wait_for_timeout(300)
    pg.fill('#f-tagq', 'dist'); pg.wait_for_timeout(300); print('G) tags filtradas:', pg.evaluate("() => [...document.querySelectorAll('#f-tags [data-tag], #f-tags button')].filter(x => x.offsetParent).map(x => x.textContent).slice(0, 6)"))
    pg.evaluate("() => [...document.querySelectorAll('#f-tags button')].filter(x => x.offsetParent)[0].click()"); pg.wait_for_timeout(600)
    pg.click('#f-top'); pg.wait_for_timeout(600); pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
    print('   chips:', pg.inner_text('#f-ativos').replace('\n', ' · '), '| KPIs', pg.evaluate(K))
    pg.click('#f-ativos [data-limpar]'); pg.wait_for_timeout(600); print('   limpar -> chips visíveis:', pg.is_visible('#f-ativos'), '| KPIs', pg.evaluate(K))
    # H) busca rápida
    pg.keyboard.press('/'); pg.wait_for_timeout(200); print('H) foco na busca:', pg.evaluate("() => document.activeElement.id"))
    pg.keyboard.type('borges'); pg.wait_for_timeout(400); print('   resultados:', pg.evaluate("() => [...document.querySelectorAll('#q-r .qr')].map(x => x.innerText.replace(/\\n/g, ' · ')).slice(0, 4)"))
    pg.keyboard.press('ArrowDown'); pg.keyboard.press('ArrowDown'); pg.wait_for_timeout(150); print('   ativo:', pg.evaluate("() => { const a = document.querySelector('#q-r .qr.on, #q-r .qr[aria-selected=true]'); return a ? a.innerText.split('\\n')[0] : '?'; }"))
    pg.keyboard.press('Enter'); pg.wait_for_timeout(600); print('   enter ->', pg.evaluate(GV)); pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
    pg.fill('#q', 'xyzxyz'); pg.wait_for_timeout(300); print('   sem resultado:', pg.inner_text('#q-r')[:80]); pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
    # I) tema e olho
    pg.click('#b-tema'); pg.wait_for_timeout(300); pg.click('#pop-tema [data-tema-id=escuro]'); pg.wait_for_timeout(300); pg.keyboard.press('Escape'); pg.wait_for_timeout(200)      # o tema escuro, pelo quadro da paleta
    pg.click('#b-olho'); pg.wait_for_timeout(600)
    print('I) tema:', pg.evaluate("() => document.documentElement.dataset.tema"), '| KPIs com olho:', pg.evaluate(K))
    pg.wait_for_timeout(700); pg.reload(); pg.wait_for_timeout(1200)
    print('   após recarregar: tema', pg.evaluate("() => document.documentElement.dataset.tema"), '| KPIs:', pg.evaluate(K), '| aviso:', pg.is_visible('#aviso'), '| visão:', pg.inner_text('#titulo .t-l'))
    pg.click('#b-olho'); pg.click('#b-tema'); pg.wait_for_timeout(300); pg.click('#pop-tema [data-tema-id=claro]'); pg.wait_for_timeout(300); pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
    # E) recomeçar
    pg.click('#b-dados'); pg.wait_for_timeout(400); print('E) dados:', pg.evaluate("() => [...document.querySelectorAll('#dlg .dd-n > div')].map(d => d.textContent)"))
    pg.click('#dlg [data-x=zerar]'); pg.wait_for_timeout(400); print('   confirmar:', pg.inner_text('#dlg h2'), '|', pg.inner_text('#dlg .dlg-msg')[:200])
    pg.click('#dlg footer .perigo, #dlg footer .pri'); pg.wait_for_timeout(1300)
    print('   toast:', pg.evaluate(TOAST), '| KPIs:', pg.evaluate(K), '| aviso:', pg.is_visible('#aviso'), '| pill:', pg.is_visible('#b-exemplo'))
    b.close()
print('ERROS:', len(errs)); [print('  ', x[:400]) for x in errs[:20]]
