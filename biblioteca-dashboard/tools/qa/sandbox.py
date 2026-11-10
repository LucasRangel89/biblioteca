"""O painel dentro de um iframe isolado (sandbox="allow-scripts"), como nas pré-visualizações que bloqueiam o
armazenamento local: tem de funcionar em memória, avisar que nada é salvo e oferecer o backup como texto."""
from caminhos import PAINEL_URL, TMP
from relogio import fixa
import json
from playwright.sync_api import sync_playwright
(TMP / 'wrap.html').write_text('<!doctype html><html><body style="margin:0"><iframe id="f" sandbox="allow-scripts" src="' + PAINEL_URL + '" style="width:100vw;height:100vh;border:0;display:block"></iframe></body></html>', encoding='utf-8')
errs = []
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={'width': 1280, 'height': 860}, locale='pt-BR', timezone_id='America/Sao_Paulo')
    pg = ctx.new_page(); fixa(pg)
    pg.on('console', lambda m: errs.append(f'[{m.type}] {m.text}') if m.type in ('error', 'warning') else None)
    pg.on('pageerror', lambda e: errs.append(f'[pageerror] {e}'))
    pg.goto((TMP / 'wrap.html').as_uri()); pg.wait_for_timeout(1500)
    fr = pg.frames[1]
    print('frames:', len(pg.frames), '| título:', fr.evaluate("document.title"))
    print('localStorage acessível?', fr.evaluate("(() => { try { localStorage.getItem('x'); return true; } catch (e) { return 'bloqueado: ' + e.name; } })()"))
    print('status:', fr.evaluate("document.querySelector('#st-dados').title + ' | ' + document.querySelector('#st-dados').className + ' | ' + document.querySelector('#st-dados').textContent"))
    print('KPIs:', fr.evaluate("[...document.querySelectorAll('.visao:not([hidden]) .kpi-v b')].map(x => x.textContent)"))
    # navegar, abrir gaveta, diálogo de dados, exportar (fallback)
    fr.click('#b-dados'); pg.wait_for_timeout(500)
    print('dlg dados:', fr.evaluate("document.querySelector('#dlg .dd-st').innerText.replace(/\\n/g, ' / ')"))
    fr.click('#dlg [data-x=exportar]'); pg.wait_for_timeout(600)
    print('após exportar:', fr.evaluate("(() => { const t = document.querySelector('#dlg textarea'); return { h2: document.querySelector('#dlg h2').textContent, textarea: t ? t.value.length : null, msg: document.querySelector('#dlg .dlg-c').innerText.slice(0, 220) }; })()"))
    pg.screenshot(path=f'{TMP}/shots/sandbox-export.png')
    fr.click('#dlg header [data-fechar]'); pg.wait_for_timeout(300)
    # ação em modo sem armazenamento
    fr.click('#nav [data-ir=desejos]'); pg.wait_for_timeout(900)
    fr.click('#p-tab-desejos tbody tr'); pg.wait_for_timeout(600)
    fr.click('#gaveta [data-acao=comprei]'); pg.wait_for_timeout(400)
    fr.click('#dlg footer .pri'); pg.wait_for_timeout(700)
    print('toast:', fr.evaluate("[...document.querySelectorAll('#toasts .toast')].map(t => t.textContent)"))
    print('KPIs desejos:', fr.evaluate("[...document.querySelectorAll('.visao:not([hidden]) .kpi-v b')].map(x => x.textContent)"))
    print('nota links:', fr.evaluate("(document.querySelector('#gaveta .nota:not(.ex)') || {textContent: '(sem nota)'}).textContent"))
    pg.screenshot(path=f'{TMP}/shots/sandbox.png')
    b.close()
print('ERROS:', len(errs)); [print('  ', x[:300]) for x in errs[:20]]
