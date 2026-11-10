"""Item sem preço-alvo ("Sem alvo") e o painel sem os dados de exemplo: indicadores, legendas e estados vazios."""
from caminhos import PAINEL_URL
from relogio import fixa
from playwright.sync_api import sync_playwright
URL = PAINEL_URL
errs = []; falhas = []
K = "() => Object.fromEntries([...document.querySelectorAll('.visao:not([hidden]) .kpi')].map(k => [k.dataset.k, { v: k.querySelector('.kpi-v b').textContent.replace(/\\u00a0/g, ' '), t: k.querySelector('.kpi-t').innerText.replace(/\\s+/g, ' ').trim(), s: k.querySelector('.kpi-s').textContent.replace(/\\u00a0/g, ' ') }]))"
def ok(nome, cond, extra=''):
    print(('  ok   ' if cond else '  FALHA') + ' ' + nome + (' — ' + str(extra) if extra != '' else ''))
    if not cond: falhas.append(nome)
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={'width': 1440, 'height': 900}, locale='pt-BR', timezone_id='America/Sao_Paulo')
    pg = ctx.new_page(); fixa(pg)
    pg.on('console', lambda m: errs.append(f'[{m.type}] {m.text}') if m.type in ('error', 'warning') else None)
    pg.on('pageerror', lambda e: errs.append(f'[pageerror] {e}'))
    pg.goto(URL); pg.wait_for_timeout(1000); pg.click('#aviso .pri'); pg.wait_for_timeout(200)
    print('DEMO')
    pg.click('#nav [data-ir=desejos]'); pg.wait_for_timeout(800); k = pg.evaluate(K)
    ok('cesta: 26 itens · 32,1% abaixo da capa', k['cesta']['s'] == '26 itens · 32,1% abaixo da capa', k['cesta'])
    ok('itens: 26 incluídos em 12 meses', k['itens']['t'] == '26 incluídos em 12 meses', k['itens']['t'])
    print('ITEM SEM ALVO')
    pg.click('#b-novo'); pg.wait_for_timeout(400); pg.fill('#dlg [data-f=t]', 'Um Livro Sem Alvo'); pg.fill('#dlg [data-f=a]', 'Autora Teste'); pg.select_option('#dlg [data-f=col]', 'desejo'); pg.click('#dlg footer .pri'); pg.wait_for_timeout(700)
    fatos = lambda: pg.evaluate("() => Object.fromEntries([...document.querySelectorAll('#gaveta .fatos > div')].map(d => [d.querySelector('dt').textContent, d.querySelector('dd').innerText.replace(/\\u00a0/g, ' ').replace(/\\n/g, ' / ')]))")
    f = fatos(); ok('sem cotação e sem alvo', f.get('Melhor preço') == 'sem cotação' and f.get('Preço-alvo') == 'não definido', f)
    pg.click('#gaveta [data-acao=cotar]'); pg.wait_for_timeout(400); pg.fill('#dlg input[data-c=preco]', '48,00'); pg.click('#dlg [data-c=ok]'); pg.wait_for_timeout(700)
    ok('o diálogo de cotação continua aberto para mais registros', pg.evaluate("() => document.querySelector('#dlg').classList.contains('on')"))
    pg.keyboard.press('Escape'); pg.wait_for_timeout(400)
    f = fatos(); ok('situação "Sem alvo" com R$ 48,00 na Amazon', f.get('Situação') == 'Sem alvo' and 'R$ 48,00' in f.get('Melhor preço', '') and 'Amazon' in f.get('Melhor preço', ''), f)
    pg.keyboard.press('Escape'); pg.wait_for_timeout(400)
    ok('Esc fecha a gaveta', pg.evaluate("() => !document.querySelector('#gaveta').classList.contains('on')"))
    k = pg.evaluate(K); ok('item sem capa não distorce o desconto (32,1%)', k['cesta']['s'] == '27 itens · 32,1% abaixo da capa', k['cesta'])
    pg.fill('#p-tab-desejos input[type=search]', 'sem alvo'); pg.wait_for_timeout(600)
    lin = pg.evaluate("() => [...document.querySelectorAll('#p-tab-desejos tbody tr td')].map(t => t.innerText.replace(/\\u00a0/g, ' ').replace(/\\n/g, ' / '))")
    ok('linha da tabela com o selo "Sem alvo"', len(lin) > 3 and lin[-1] == 'Sem alvo' and 'R$ 48,00 / Amazon' in lin, lin)
    pg.fill('#p-tab-desejos input[type=search]', ''); pg.wait_for_timeout(400)
    print('SEM OS DADOS DE EXEMPLO')
    pg.click('#b-dados'); pg.wait_for_timeout(400); pg.click('#dlg [data-x=limpar]'); pg.wait_for_timeout(400); pg.click('#dlg footer .pri'); pg.wait_for_timeout(900); pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
    esperado = {
        'geral': {'acervo': ('97', 'sem datas de aquisição'), 'investido': ('R$ 0', ''), 'leituras': ('2', ''), 'cesta': ('R$ 48', 'histórico começa hoje'), 'oport': ('0', 'histórico começa hoje'), 'recs': ('545', '')},
        'biblioteca': {'acervo': ('97', 'sem datas de aquisição'), 'investido': ('R$ 0', ''), 'leituras': ('2', ''), 'fila': ('97', '')},
        'recs': {'recs': ('545', ''), 'top': ('51', '9,4% da fila'), 'leves': ('67', '12,3% da fila'), 'pend': ('61', '')},
        'desejos': {'itens': ('1', '1 incluído em 12 meses'), 'cesta': ('R$ 48', 'histórico começa hoje'), 'oport': ('0', 'histórico começa hoje'), 'minimo': ('R$ 48', None)},
        'precos': {'monit': ('1', 'em 1 loja'), 'oport': ('0', 'histórico começa hoje'), 'queda': ('—', ''), 'cot': ('1', None)},
    }
    for v, esp in esperado.items():
        pg.click(f'#nav [data-ir={v}]'); pg.wait_for_timeout(800); k = pg.evaluate(K)
        ruins = {a: k.get(a) for a, (val, t) in esp.items() if a not in k or k[a]['v'] != val or (t is not None and k[a]['t'] != t)}
        ok(f'{v}: indicadores sem tendências inventadas', not ruins, ruins or '')
        leg = pg.evaluate("() => [...document.querySelectorAll('.visao:not([hidden]) .card')].filter(c => { const z = c.querySelector('.ch-vazio'); return z && !z.hidden && !c.classList.contains('card-tab') && c.querySelector('.card-f') && c.querySelector('.card-f').textContent.trim(); }).map(c => c.id + ': ' + c.querySelector('.card-f').textContent.trim().slice(0, 50))")
        ok(f'{v}: nenhum painel vazio com legenda sobrando', not leg, leg or '')
        vaz = pg.evaluate("() => [...document.querySelectorAll('.visao:not([hidden]) .ch-vazio')].filter(z => !z.hidden && z.offsetParent && !z.textContent.trim()).length")
        ok(f'{v}: todo estado vazio tem mensagem', vaz == 0, vaz or '')
    b.close()
print('FALHAS:', falhas); print('ERROS:', len(errs) + len(falhas)); [print('  ', x[:300]) for x in errs[:10]]
