"""Varredura: em cada visão (claro/escuro, com e sem dados de exemplo, com filtros), clica em todo botão, aba, legenda,
barra e linha visíveis e confere que nada lança erro, nada estoura a largura da página e as camadas fecham com Esc."""
from caminhos import PAINEL_URL
from relogio import fixa
from playwright.sync_api import sync_playwright
import sys
URL = PAINEL_URL
errs = []; avisos = []
ALVOS = "() => { const v = document.querySelector('.visao:not([hidden])'); const vis = e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && getComputedStyle(e).visibility !== 'hidden'; }; const els = [...v.querySelectorAll('button, [role=button], [data-id], [data-k], .leg, .hb-l, .db-l, .mz-c, tbody tr, .li, a[href]')].filter(vis).filter(e => !e.matches('[data-csv], a[target=_blank], a[href^=http]') && !e.closest('a[target=_blank]')); els.forEach((e, i) => e.setAttribute('data-vr', i)); return els.length; }"
def varrer(pg, rotulo, limite=400):
    n = pg.evaluate(ALVOS); feitos = 0
    for i in range(min(n, limite)):
        try:
            existe = pg.evaluate(f"() => {{ const e = document.querySelector('.visao:not([hidden]) [data-vr=\"{i}\"]'); if (!e) return false; const r = e.getBoundingClientRect(); if (!r.width) return false; e.scrollIntoView({{ block: 'center' }}); e.click(); return true; }}")
        except Exception as ex:
            errs.append(f'[{rotulo}] clique {i}: {str(ex)[:160]}'); continue
        if not existe: continue
        feitos += 1; pg.wait_for_timeout(25)
        est = pg.evaluate("() => ({ dlg: document.querySelector('#dlg').classList.contains('on'), gav: document.querySelector('#gaveta').classList.contains('on'), pop: !!document.querySelector('.pop-w.aberto'), rola: document.documentElement.scrollWidth - document.documentElement.clientWidth })")
        if est['rola'] > 0: avisos.append(f'[{rotulo}] alvo {i}: página com rolagem horizontal de {est["rola"]}px')
        for _ in range(3):
            if not (est['dlg'] or est['gav'] or est['pop']): break
            pg.keyboard.press('Escape'); pg.wait_for_timeout(40)
            est = pg.evaluate("() => ({ dlg: document.querySelector('#dlg').classList.contains('on'), gav: document.querySelector('#gaveta').classList.contains('on'), pop: !!document.querySelector('.pop-w.aberto') })")
        if est['dlg'] or est['gav'] or est['pop']: errs.append(f'[{rotulo}] alvo {i}: camada não fechou com Esc: {est}')
    return feitos
with sync_playwright() as p:
    b = p.chromium.launch()
    cenarios = [(1440, 900, 'light'), (1440, 900, 'dark'), (390, 844, 'light')] if len(sys.argv) < 2 else [(int(sys.argv[1]), 900, 'light')]
    for w, h, tema in cenarios:
        ctx = b.new_context(viewport={'width': w, 'height': h}, color_scheme=tema, locale='pt-BR', timezone_id='America/Sao_Paulo', accept_downloads=True)
        pg = ctx.new_page(); fixa(pg)
        pg.on('console', lambda m: errs.append(f'[console.{m.type}] {m.text[:300]}') if m.type in ('error', 'warning') else None)
        pg.on('pageerror', lambda e: errs.append(f'[pageerror] {str(e)[:300]}'))
        pg.goto(URL); pg.wait_for_timeout(1000); pg.click('#aviso .pri'); pg.wait_for_timeout(200)
        nav = '#nav' if w > 820 else '#nav-m'; tot = 0
        for etapa in ['demo', 'filtros', 'limpo']:
            if etapa == 'filtros':
                if w > 820: pg.click('#f-periodo button[data-v="90d"]'); pg.wait_for_timeout(300); pg.click('#f-tipo button[data-v="F"]'); pg.wait_for_timeout(300)
                else: continue
            if etapa == 'limpo':
                pg.evaluate("() => document.querySelector('#f-ativos [data-limpar]')?.click()"); pg.wait_for_timeout(300)
                if w > 820: pg.click('#f-periodo button[data-v="tudo"]'); pg.wait_for_timeout(200)
                pg.click('#b-dados'); pg.wait_for_timeout(300); pg.click('#dlg [data-x=limpar]'); pg.wait_for_timeout(300); pg.click('#dlg footer .pri'); pg.wait_for_timeout(700); pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
            for v in ['geral', 'biblioteca', 'recs', 'desejos', 'precos']:
                pg.evaluate(f"() => document.querySelector('{nav} [data-ir={v}]').click()"); pg.wait_for_timeout(600)
                n = varrer(pg, f'{w}/{tema}/{etapa}/{v}'); tot += n
                # o estado pode ter mudado (filtros por clique em gráfico): volta ao recorte da etapa
                pg.evaluate("() => document.querySelector('#f-ativos [data-limpar]')?.click()"); pg.wait_for_timeout(150)
                if etapa == 'filtros': pg.click('#f-periodo button[data-v="90d"]'); pg.wait_for_timeout(150)
        print(f'{w}px {tema}: {tot} cliques')
        ctx.close()
    b.close()
print('AVISOS:', len(avisos)); [print('  ', x) for x in avisos[:12]]
print('ERROS:', len(errs)); [print('  ', x) for x in errs[:25]]
