from caminhos import PAINEL_URL, TMP
from relogio import fixa
import json, re
from playwright.sync_api import sync_playwright
URL = PAINEL_URL
errs = []; falhas = []
K = "() => Object.fromEntries([...document.querySelectorAll('.visao:not([hidden]) .kpi')].map(k => [k.dataset.k, {v: k.querySelector('.kpi-v b').textContent.replace(/\\u00a0/g, ' '), t: k.querySelector('.kpi-t').innerText.replace(/\\s+/g, ' ').trim(), s: k.querySelector('.kpi-s').textContent}]))"
def ok(nome, cond, extra=''):
    print(('  ok   ' if cond else '  FALHA') + ' ' + nome + (' — ' + str(extra) if extra != '' else ''))
    if not cond: falhas.append(nome)
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={'width': 1440, 'height': 900}, locale='pt-BR', timezone_id='America/Sao_Paulo', accept_downloads=True)
    pg = ctx.new_page(); fixa(pg)
    pg.on('console', lambda m: errs.append(f'[{m.type}] {m.text}') if m.type in ('error', 'warning') else None)
    pg.on('pageerror', lambda e: errs.append(f'[pageerror] {e}'))
    pg.goto(URL); pg.wait_for_timeout(1200)
    def per(v): pg.click(f'#f-periodo button[data-v="{v}"]'); pg.wait_for_timeout(800); return pg.evaluate(K)
    print('GERAL × período')
    k = pg.evaluate(K); ok('tudo: acervo 143', k['acervo']['v'] == '143', k['acervo']); ok('tudo: investido 5.790', k['investido']['v'] == 'R$ 5.790'); ok('tudo: leituras 97', k['leituras']['v'] == '97'); ok('tudo: cesta 1.258', k['cesta']['v'] == 'R$ 1.258'); ok('tudo: oport 7', k['oport']['v'] == '7'); ok('tudo: recs 473', k['recs']['v'] == '473')
    k = per('30d'); ok('30d: +5 livros', '+5 ' in k['acervo']['t'], k['acervo']['t']); ok('30d: R$ 248', k['investido']['v'] == 'R$ 248', k['investido']['v'])
    k = per('90d'); ok('90d: +14', '+14 ' in k['acervo']['t'], k['acervo']['t']); ok('90d: R$ 611', k['investido']['v'] == 'R$ 611', k['investido']['v'])
    k = per('12m'); ok('12m: +39', '+39 ' in k['acervo']['t'], k['acervo']['t']); ok('12m: R$ 1.633', k['investido']['v'] == 'R$ 1.633', k['investido']['v']); ok('12m: 25 leituras', k['leituras']['v'] == '25', k['leituras']['v'])
    k = per('ano'); ok('ano: +33', '+33 ' in k['acervo']['t'], k['acervo']['t']); ok('ano: R$ 1.337', k['investido']['v'] == 'R$ 1.337', k['investido']['v']); ok('ano: 21 leituras', k['leituras']['v'] == '21', k['leituras']['v'])
    k = per('tudo')
    pg.click('#f-acervo button[data-v="fisico"]'); pg.wait_for_timeout(800); k = pg.evaluate(K); ok('física: 97 / R$ 4.407', k['acervo']['v'] == '97' and k['investido']['v'] == 'R$ 4.407', (k['acervo']['v'], k['investido']['v'])); ok('física: recs "—"', k['recs']['v'] == '—', k['recs'])
    pg.click('#f-acervo button[data-v="virtual"]'); pg.wait_for_timeout(800); k = pg.evaluate(K); ok('virtual: 46 / R$ 1.383', k['acervo']['v'] == '46' and k['investido']['v'] == 'R$ 1.383', (k['acervo']['v'], k['investido']['v']))
    pg.click('#f-acervo button[data-v="tudo"]'); pg.wait_for_timeout(500)
    pg.click('#f-tipo button[data-v="F"]'); pg.wait_for_timeout(800); k = pg.evaluate(K); print('   ficção:', {a: k[a]['v'] for a in k})
    pg.click('#pw-eixo .pop-b'); pg.wait_for_timeout(300); pg.click('#pop-eixo .opt >> nth=1'); pg.wait_for_timeout(800); pg.keyboard.press('Escape')
    k = pg.evaluate(K); print('   ficção + eixo 2:', {a: k[a]['v'] for a in k}, '| chips:', pg.inner_text('#f-ativos').replace('\n', ' · '))
    pg.click('#f-ativos [data-limpar]'); pg.wait_for_timeout(700); k = pg.evaluate(K); ok('limpar filtros volta a 143', k['acervo']['v'] == '143')
    print('TABELA biblioteca')
    pg.click('#nav [data-ir=biblioteca]'); pg.wait_for_timeout(1000); T = '#p-tab-biblioteca'
    lin = lambda: pg.evaluate(f"() => [...document.querySelectorAll('{T} tbody tr')].map(r => r.querySelector('.tt b').textContent.trim())")
    info = lambda: pg.inner_text(f'{T} .tb-info')
    ok('25 linhas por página', len(lin()) == 25, info())
    pg.click(f'{T} th[data-c=pago] button'); pg.wait_for_timeout(500); v1 = pg.evaluate(f"() => [...document.querySelectorAll('{T} tbody tr td[data-c=pago], {T} tbody tr td.c-pago')].slice(0, 3).map(x => x.textContent)")
    cab = pg.evaluate(f"() => document.querySelector('{T} th[data-c=pago]').getAttribute('aria-sort')"); ok('ordenar por pago (desc na 1ª vez)', cab == 'descending', (cab, v1))
    pg.click(f'{T} th[data-c=pago] button'); pg.wait_for_timeout(500); ok('2º clique inverte', pg.evaluate(f"() => document.querySelector('{T} th[data-c=pago]').getAttribute('aria-sort')") == 'ascending')
    pg.click(f'{T} .abas [data-a=lendo]'); pg.wait_for_timeout(500); ok('aba Lendo = 3', len(lin()) == 3, info())
    pg.click(f'{T} .abas [data-a=todos]'); pg.wait_for_timeout(400)
    pg.fill(f'{T} input[type=search]', 'borges'); pg.wait_for_timeout(600); ok('busca "borges"', 0 < len(lin()) < 10, lin())
    pg.fill(f'{T} input[type=search]', 'zzzz'); pg.wait_for_timeout(600); ok('estado vazio', pg.is_visible(f'{T} .ch-vazio, {T} .vazio'), info())
    pg.fill(f'{T} input[type=search]', ''); pg.wait_for_timeout(600)
    pg.click(f'{T} [data-p="1"]'); pg.wait_for_timeout(500); ok('paginação', '26' in info(), info())
    pg.select_option(f'{T} .tam select', '50'); pg.wait_for_timeout(500); ok('50 por página', len(lin()) == 50, info())
    with pg.expect_download() as d: pg.click(f'{T} [data-csv]')
    f = d.value; f.save_as(f'{TMP}/x.csv'); raw = open(f'{TMP}/x.csv', 'rb').read(); txt = raw.decode('utf-8-sig').splitlines()
    ok('CSV: BOM + 144 linhas + ;', raw[:3] == b'\xef\xbb\xbf' and len(txt) == 144 and ';' in txt[0], (f.suggested_filename, len(txt), txt[0][:90]))
    print('TABELAS das outras visões (CSV)')
    for v, n in [('geral', 645), ('recs', 476), ('desejos', 27), ('precos', 39)]:
        pg.click(f'#nav [data-ir={v}]'); pg.wait_for_timeout(1000)
        with pg.expect_download() as d: pg.click(f'#p-tab-{v} [data-csv]')
        f = d.value; f.save_as(f'{TMP}/x.csv'); txt = open(f'{TMP}/x.csv', 'rb').read().decode('utf-8-sig').splitlines()
        ok(f'CSV {v}: {n} linhas', len(txt) == n, (len(txt), txt[0][:110]))
        if v == 'precos': print('     ', txt[1][:200])
    b.close()
print('FALHAS:', falhas); print('ERROS:', len(errs)); [print('  ', x[:400]) for x in errs[:20]]
