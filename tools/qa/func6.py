"""Períodos (dentro de "Mais filtros"), filtros do acervo (física / virtual / nas duas), a guia Finanças, tabelas e CSV.

Os números esperados são um retrato do catálogo atual com os dados de exemplo (relógio fixo em 09/11/2026).
Se o catálogo mudar (livros novos na biblioteca virtual, por exemplo), rode este script, confira os valores
impressos nas linhas FALHA e atualize os literais abaixo.
"""
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
    def per(v):
        """Escolhe o período, que fica no fim de "Mais filtros", e devolve os indicadores da visão aberta."""
        if not pg.is_visible('#pop-mais'): pg.click('#pw-mais .pop-b'); pg.wait_for_timeout(250)
        pg.click(f'#f-periodo button[data-v="{v}"]'); pg.wait_for_timeout(800); return pg.evaluate(K)
    def ir(v): pg.keyboard.press('Escape'); pg.wait_for_timeout(150); pg.click(f'#nav [data-ir={v}]'); pg.wait_for_timeout(900); return pg.evaluate(K)
    chips = lambda: pg.inner_text('#f-ativos').replace('\n', ' ').replace('\u00a0', ' ') if pg.is_visible('#f-ativos') else ''
    print('GERAL × período')
    k = pg.evaluate(K); ok('tudo: acervo 2.125', k['acervo']['v'] == '2.125', k['acervo']); ok('tudo: 97 físicos · 2.052 digitais · 24 nos dois', k['acervo']['s'] == '97 físicos · 2.052 digitais · 24 nos dois', k['acervo']['s']); ok('tudo: leituras 60', k['leituras']['v'] == '60', k['leituras']['v']); ok('tudo: por ler 2.062', k['fila']['v'] == '2.062', k['fila']['v']); ok('tudo: recs 407', k['recs']['v'] == '407', k['recs']['v'])
    ok('a visão geral não mostra dinheiro: sem "Investido", "Cesta" nem "Abaixo do preço-alvo"', sorted(k) == ['acervo', 'fila', 'leituras', 'recs'], sorted(k))
    ok('o período não está na barra de filtros: fica dentro de "Mais filtros"', pg.evaluate("() => !!document.querySelector('#pop-mais #f-periodo') && !document.querySelector('#f-periodo').offsetParent"))
    ok('sem filtro, nada de chip nem de contador em "Mais filtros"', chips() == '' and not pg.is_visible('#pw-mais .pop-b .cont'), chips())
    k = per('30d'); ok('30d: +4 livros', '+4 ' in k['acervo']['t'], k['acervo']['t'])
    ok('30d: o chip "Período: 30 dias" aparece e "Mais filtros" conta 1', 'Período: 30 dias' in chips() and pg.inner_text('#pw-mais .pop-b .cont').strip() == '1', (chips(), pg.inner_text('#pw-mais .pop-b .cont')))
    k = per('90d'); ok('90d: +7', '+7 ' in k['acervo']['t'], k['acervo']['t']); ok('90d: o chip acompanha', 'Período: 90 dias' in chips() and '30 dias' not in chips(), chips())
    k = per('12m'); ok('12m: +17', '+17 ' in k['acervo']['t'], k['acervo']['t']); ok('12m: 13 leituras', k['leituras']['v'] == '13', k['leituras']['v'])
    k = per('ano'); ok('ano: +14', '+14 ' in k['acervo']['t'], k['acervo']['t']); ok('ano: 12 leituras', k['leituras']['v'] == '12', k['leituras']['v'])
    pg.keyboard.press('Escape'); pg.wait_for_timeout(200); pg.click('#f-ativos [data-rm^=periodo]'); pg.wait_for_timeout(800); k = pg.evaluate(K)
    ok('tirar o chip do período volta a "Tudo"', k['leituras']['v'] == '60' and chips() == '' and pg.evaluate("() => document.querySelector('#f-periodo button[aria-pressed=true]').dataset.v") == 'tudo', (k['leituras']['v'], chips()))
    per('90d'); pg.click('#pop-mais [data-limpar=mais]'); pg.wait_for_timeout(800); k = pg.evaluate(K)
    ok('"limpar" de Mais filtros também desfaz o período', k['leituras']['v'] == '60' and chips() == '', (k['leituras']['v'], chips()))
    per('12m'); pg.keyboard.press('Escape'); pg.wait_for_timeout(200); pg.reload(); pg.wait_for_timeout(1200); k = pg.evaluate(K)
    ok('o período não é lembrado ao recarregar: volta a "Tudo"', k['leituras']['v'] == '60' and chips() == '', (k['leituras']['v'], chips()))
    print('FINANÇAS × período')
    k = ir('financas'); ok('tudo: investido 4.469', k['investido']['v'] == 'R$ 4.469', k['investido']['v']); ok('tudo: preço médio 50,22', k['medio']['v'] == 'R$ 50,22', k['medio']['v']); ok('tudo: cesta 1.257', k['cesta']['v'] == 'R$ 1.257', k['cesta']['v']); ok('tudo: oport 7', k['oport']['v'] == '7', k['oport']['v'])
    ok('Finanças tem os quatro indicadores de dinheiro', sorted(k) == ['cesta', 'investido', 'medio', 'oport'], sorted(k))
    k = per('30d'); ok('30d: R$ 208', k['investido']['v'] == 'R$ 208', k['investido']['v'])
    k = per('90d'); ok('90d: R$ 341', k['investido']['v'] == 'R$ 341', k['investido']['v'])
    k = per('12m'); ok('12m: R$ 870', k['investido']['v'] == 'R$ 870', k['investido']['v'])
    k = per('ano'); ok('ano: R$ 688', k['investido']['v'] == 'R$ 688', k['investido']['v'])
    k = per('tudo'); pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
    print('ACERVO: física / virtual / nas duas')
    def acervo(v):
        """Escolhe o filtro do acervo; devolve os indicadores da visão geral e os de Finanças."""
        pg.click(f'#f-acervo button[data-v="{v}"]'); pg.wait_for_timeout(500)
        return ir('geral'), ir('financas')
    g, f = acervo('fisico'); ok('física: 97 / R$ 4.469', g['acervo']['v'] == '97' and f['investido']['v'] == 'R$ 4.469', (g['acervo']['v'], f['investido']['v'])); ok('física: recs "—"', g['recs']['v'] == '—', g['recs'])
    g, f = acervo('virtual'); ok('virtual: 2.052 / R$ 0 (a compra do exemplar físico não conta na biblioteca virtual)', g['acervo']['v'] == '2.052' and f['investido']['v'] == 'R$ 0' and g['acervo']['t'] == 'sem datas de aquisição', (g['acervo']['v'], f['investido']['v'], g['acervo']['t']))
    g, f = acervo('ambos'); ok('nas duas: 24 / R$ 1.280', g['acervo']['v'] == '24' and f['investido']['v'] == 'R$ 1.280' and g['acervo']['s'] == '24 físicos · 24 digitais · 24 nos dois', (g['acervo']['v'], f['investido']['v'], g['acervo']['s'])); ok('nas duas: chip do filtro', 'Nas duas' in pg.inner_text('#f-ativos'), pg.inner_text('#f-ativos'))
    pg.click('#f-acervo button[data-v="tudo"]'); pg.wait_for_timeout(500); ir('geral')
    pg.click('#f-tipo button[data-v="F"]'); pg.wait_for_timeout(800); k = pg.evaluate(K); print('   ficção:', {a: k[a]['v'] for a in k})
    pg.click('#pw-eixo .pop-b'); pg.wait_for_timeout(300); pg.click('#pop-eixo .opt >> nth=1'); pg.wait_for_timeout(800); pg.keyboard.press('Escape')
    k = pg.evaluate(K); print('   ficção + eixo 2:', {a: k[a]['v'] for a in k}, '| chips:', pg.inner_text('#f-ativos').replace('\n', ' · '))
    pg.click('#f-ativos [data-limpar]'); pg.wait_for_timeout(700); k = pg.evaluate(K); ok('limpar filtros volta a 2.125', k['acervo']['v'] == '2.125', k['acervo']['v'])
    print('TABELA biblioteca')
    pg.click('#nav [data-ir=biblioteca]'); pg.wait_for_timeout(1000); T = '#p-tab-biblioteca'
    lin = lambda: pg.evaluate(f"() => [...document.querySelectorAll('{T} tbody tr')].map(r => r.querySelector('.tt b').textContent.trim())")
    info = lambda: pg.inner_text(f'{T} .tb-info')
    ok('25 linhas por página', len(lin()) == 25, info())
    cabs = pg.evaluate(f"() => [...document.querySelectorAll('{T} thead th')].map(x => x.dataset.c)")
    ok('a tabela da biblioteca não tem coluna de valor pago', 'pago' not in cabs and 'valor' not in cabs and 'pg' in cabs, cabs)
    pg.click(f'{T} th[data-c=pg] button'); pg.wait_for_timeout(500); v1 = pg.evaluate(f"() => [...document.querySelectorAll('{T} tbody tr')].slice(0, 3).map(r => r.querySelector('.tt b').textContent.trim())")
    cab = pg.evaluate(f"() => document.querySelector('{T} th[data-c=pg]').getAttribute('aria-sort')"); ok('ordenar por páginas (desc na 1ª vez)', cab == 'descending', (cab, v1))
    pg.click(f'{T} th[data-c=pg] button'); pg.wait_for_timeout(500); ok('2º clique inverte', pg.evaluate(f"() => document.querySelector('{T} th[data-c=pg]').getAttribute('aria-sort')") == 'ascending')
    pg.click(f'{T} .abas [data-a=lendo]'); pg.wait_for_timeout(500); ok('aba Lendo = 3', len(lin()) == 3, info())
    pg.click(f'{T} .abas [data-a=todos]'); pg.wait_for_timeout(400)
    pg.fill(f'{T} input[type=search]', 'borges'); pg.wait_for_timeout(600); ok('busca "borges"', 0 < len(lin()) < 25 and 'de 2.125 no recorte' in info(), (len(lin()), info()))
    pg.fill(f'{T} input[type=search]', 'zzzz'); pg.wait_for_timeout(600); ok('estado vazio', pg.is_visible(f'{T} .ch-vazio, {T} .vazio'), info())
    pg.fill(f'{T} input[type=search]', ''); pg.wait_for_timeout(600)
    pg.click(f'{T} [data-p="1"]'); pg.wait_for_timeout(500); ok('paginação', '26' in info(), info())
    pg.select_option(f'{T} .tam select', '50'); pg.wait_for_timeout(500); ok('50 por página', len(lin()) == 50, info())
    with pg.expect_download() as d: pg.click(f'{T} [data-csv]')
    f = d.value; f.save_as(f'{TMP}/x.csv'); raw = open(f'{TMP}/x.csv', 'rb').read(); txt = raw.decode('utf-8-sig').splitlines()
    ok('CSV: BOM + 2.126 linhas + ;', raw[:3] == b'\xef\xbb\xbf' and len(txt) == 2126 and ';' in txt[0], (f.suggested_filename, len(txt), txt[0][:90]))
    ok('CSV da biblioteca: sem coluna de valor', 'Pago' not in txt[0].split(';') and 'Valor' not in txt[0], txt[0][:160])
    print('TABELA de Finanças: as compras registradas')
    pg.click('#nav [data-ir=financas]'); pg.wait_for_timeout(1000); T = '#p-tab-financas'
    abas = pg.evaluate(f"() => Object.fromEntries([...document.querySelectorAll('{T} .abas [data-a]')].map(a => [a.dataset.a, a.querySelector('.n, .cont, span') ? a.querySelector('.n, .cont, span').textContent.trim() : a.textContent.trim()]))")
    ok('97 compras: 89 com valor e 8 presentes ou gratuitos', abas.get('todos') == '97' and abas.get('pagas') == '89' and abas.get('gratis') == '8' and abas.get('semvalor') == '0', abas)
    topo = pg.inner_text(f'{T} tbody tr >> nth=0').replace('\u00a0', ' ').replace('\n', ' ').replace('\t', ' ')
    ok('vem ordenada pelo valor pago, do maior para o menor', pg.evaluate(f"() => document.querySelector('{T} th[data-c=pago]').getAttribute('aria-sort')") == 'descending' and topo.endswith('R$ 205,90'), topo[-70:])
    with pg.expect_download() as d: pg.click(f'{T} [data-csv]')
    f = d.value; f.save_as(f'{TMP}/x.csv'); txt = open(f'{TMP}/x.csv', 'rb').read().decode('utf-8-sig').splitlines()
    ok('CSV de Finanças: 98 linhas, com as colunas Pago, Origem e Condição', len(txt) == 98 and all(c in txt[0].split(';') for c in ('Pago', 'Origem', 'Condição')), (len(txt), txt[0][:160]))
    print('TABELAS das outras visões (CSV)')
    for v, n in [('geral', 2561), ('recs', 410), ('desejos', 27), ('precos', 39)]:
        pg.click(f'#nav [data-ir={v}]'); pg.wait_for_timeout(1000)
        with pg.expect_download() as d: pg.click(f'#p-tab-{v} [data-csv]')
        f = d.value; f.save_as(f'{TMP}/x.csv'); txt = open(f'{TMP}/x.csv', 'rb').read().decode('utf-8-sig').splitlines()
        ok(f'CSV {v}: {n} linhas', len(txt) == n, (len(txt), txt[0][:110]))
        if v == 'precos': print('     ', txt[1][:200])
    b.close()
print('FALHAS:', falhas); print('ERROS:', len(errs)); [print('  ', x[:400]) for x in errs[:20]]
