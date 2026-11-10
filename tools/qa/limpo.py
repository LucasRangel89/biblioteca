"""Item sem preço-alvo ("Sem alvo") e o painel sem os dados de exemplo: indicadores, legendas e estados vazios —
depois de "Limpar dados de exemplo" e do jeito que o painel abre (só o catálogo; o endereço sem ?exemplo).
No fim, a guia Preços sem nenhum livro para cotar: o quadro "Registrar cotação" explica como começar.

Os números esperados são um retrato do catálogo atual (2.125 livros no acervo: 97 na estante + 2.028 só digitais;
435 recomendações, 2 delas já lidas). Se o catálogo mudar, rode, confira as linhas FALHA e atualize os literais.
"""
from caminhos import PAINEL_LIMPO, PAINEL_URL
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
    ok('cesta: 26 itens · 33% abaixo da capa', k['cesta']['s'] == '26 itens · 33% abaixo da capa', k['cesta'])
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
    k = pg.evaluate(K); ok('item sem capa não distorce o desconto (33%)', k['cesta']['s'] == '27 itens · 33% abaixo da capa', k['cesta'])
    pg.fill('#p-tab-desejos input[type=search]', 'sem alvo'); pg.wait_for_timeout(600)
    lin = pg.evaluate("() => [...document.querySelectorAll('#p-tab-desejos tbody tr td')].map(t => t.innerText.replace(/\\u00a0/g, ' ').replace(/\\n/g, ' / '))")
    ok('linha da tabela com o selo "Sem alvo"', len(lin) > 3 and lin[-1] == 'Sem alvo' and 'R$ 48,00 / Amazon' in lin, lin)
    pg.fill('#p-tab-desejos input[type=search]', ''); pg.wait_for_timeout(400)
    def visoes(esperado, rotulo):
        """Em cada visão: os indicadores esperados (valor e tendência), nenhuma legenda sobrando e nenhum estado vazio sem mensagem."""
        for v, esp in esperado.items():
            pg.click(f'#nav [data-ir={v}]'); pg.wait_for_timeout(800); k = pg.evaluate(K)
            ruins = {a: k.get(a) for a, (val, t) in esp.items() if a not in k or k[a]['v'] != val or (t is not None and k[a]['t'] != t)}
            ok(f'{rotulo}{v}: indicadores sem tendências inventadas', not ruins and sorted(k) == sorted(esp), ruins or (sorted(k) if sorted(k) != sorted(esp) else ''))
            leg = pg.evaluate("() => [...document.querySelectorAll('.visao:not([hidden]) .card')].filter(c => { const z = c.querySelector('.ch-vazio'); return z && !z.hidden && !c.classList.contains('card-tab') && c.querySelector('.card-f') && c.querySelector('.card-f').textContent.trim(); }).map(c => c.id + ': ' + c.querySelector('.card-f').textContent.trim().slice(0, 50))")
            ok(f'{rotulo}{v}: nenhum painel vazio com legenda sobrando', not leg, leg or '')
            vaz = pg.evaluate("() => [...document.querySelectorAll('.visao:not([hidden]) .ch-vazio')].filter(z => !z.hidden && z.offsetParent && !z.textContent.trim()).length")
            ok(f'{rotulo}{v}: todo estado vazio tem mensagem', vaz == 0, vaz or '')
            gigantes = pg.evaluate("() => [...document.querySelectorAll('.visao:not([hidden]) .ch-vazio svg')].filter(x => x.getBoundingClientRect().width > 60).length")
            ok(f'{rotulo}{v}: o desenho dos estados vazios tem tamanho de ícone', gigantes == 0, gigantes or '')
    print('SEM OS DADOS DE EXEMPLO')
    pg.click('#b-dados'); pg.wait_for_timeout(400); pg.click('#dlg [data-x=limpar]'); pg.wait_for_timeout(400); pg.click('#dlg footer .pri'); pg.wait_for_timeout(900); pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
    visoes({
        'geral': {'acervo': ('2.125', 'sem datas de aquisição'), 'leituras': ('2', ''), 'fila': ('2.125', ''), 'recs': ('433', '')},
        'biblioteca': {'acervo': ('2.125', 'sem datas de aquisição'), 'leituras': ('2', ''), 'fila': ('2.125', ''), 'lendo': ('0', '')},
        'recs': {'recs': ('433', ''), 'top': ('32', '7,4% da fila'), 'leves': ('50', '11,5% da fila'), 'pend': ('61', '')},
        'financas': {'investido': ('R$ 0', ''), 'medio': ('—', ''), 'cesta': ('R$ 48', 'histórico começa hoje'), 'oport': ('0', 'histórico começa hoje')},
        'desejos': {'itens': ('1', '1 incluído em 12 meses'), 'cesta': ('R$ 48', 'histórico começa hoje'), 'oport': ('0', 'histórico começa hoje'), 'minimo': ('R$ 48', None)},
        'precos': {'monit': ('1', 'em 1 loja'), 'oport': ('0', 'histórico começa hoje'), 'queda': ('—', ''), 'cot': ('1', None)},
    }, '')
    pg.context.close()

    print('COMO O PAINEL ABRE: SÓ O CATÁLOGO, NADA INVENTADO')
    ctx = b.new_context(viewport={'width': 1440, 'height': 900}, locale='pt-BR', timezone_id='America/Sao_Paulo')
    pg = ctx.new_page(); fixa(pg)
    pg.on('console', lambda m: errs.append(f'[{m.type}] {m.text}') if m.type in ('error', 'warning') else None)
    pg.on('pageerror', lambda e: errs.append(f'[pageerror] {e}'))
    pg.goto(PAINEL_LIMPO); pg.wait_for_timeout(1000); pg.click('#aviso .pri'); pg.wait_for_timeout(200)
    visoes({
        'geral': {'acervo': ('2.125', 'sem datas de aquisição'), 'leituras': ('2', ''), 'fila': ('2.125', ''), 'recs': ('433', '')},
        'biblioteca': {'acervo': ('2.125', 'sem datas de aquisição'), 'leituras': ('2', ''), 'fila': ('2.125', ''), 'lendo': ('0', '')},
        'recs': {'recs': ('433', ''), 'top': ('32', '7,4% da fila'), 'leves': ('50', '11,5% da fila'), 'pend': ('61', '')},
        'financas': {'investido': ('R$ 0', ''), 'medio': ('—', ''), 'cesta': ('—', ''), 'oport': ('0', '')},
        'desejos': {'itens': ('0', ''), 'cesta': ('—', ''), 'oport': ('0', ''), 'minimo': ('—', None)},
        'precos': {'monit': ('0', ''), 'oport': ('0', ''), 'queda': ('—', ''), 'cot': ('0', None)},
    }, 'ao abrir · ')
    for v, trecho in (('financas', 'Nenhuma compra registrada ainda'), ('desejos', 'A lista está vazia'), ('precos', 'Nenhum preço acompanhado ainda')):
        pg.click(f'#nav [data-ir={v}]'); pg.wait_for_timeout(700)
        txt = pg.inner_text(f'#p-tab-{v} .tb-w .ch-vazio').replace('\u00a0', ' ').replace('\n', ' ')
        ok(f'ao abrir · {v}: a tabela vazia diz o que fazer, em vez de culpar os filtros', trecho in txt and 'filtros' not in txt, txt[:140])

    print('PREÇOS, SEM NENHUM LIVRO PARA COTAR')
    COT = """() => { const c = document.querySelector('#p-cotacao'), vis = e => !!e && !e.closest('[hidden]') && e.getBoundingClientRect().height > 0;
        const s = c.querySelector('.cot-sem'), l = c.querySelector('select[data-c=livro]'), g = document.querySelector('#p-px-loja .ch-vazio');
        return { form: vis(c.querySelector('.form.cot')), aviso: vis(s) ? s.innerText.replace(/\\u00a0/g, ' ').replace(/\\s+/g, ' ').trim() : '',
                 parados: [...c.querySelectorAll('button, select, input')].filter(e => vis(e) && e.disabled).length, livro: vis(l) ? l.selectedOptions[0].textContent : '',
                 grafico: g && !g.hidden ? g.innerText.replace(/\\u00a0/g, ' ').replace(/\\s+/g, ' ').trim() : '' }; }"""
    c = pg.evaluate(COT)
    ok('o quadro "Registrar cotação" diz como começar, em vez de mostrar um formulário que não pode ser usado', not c['form'] and c['parados'] == 0
       and 'Nenhum livro para cotar ainda.' in c['aviso'] and '“Quero comprar”' in c['aviso'] and '“Monitorar preço”' in c['aviso'], c)
    ok('e o gráfico "Preço por loja" aponta um botão que existe na ficha de uma recomendação', c['grafico'].startswith('Nenhum item com cotações ainda.') and '“Monitorar preço”' in c['grafico'] and 'Registrar cotação' not in c['grafico'], c['grafico'])
    pg.click('#nav [data-ir=recs]'); pg.wait_for_timeout(700); pg.fill('#p-tab-recs input[type=search]', 'O Nome da Rosa'); pg.wait_for_timeout(600)
    pg.click('#p-tab-recs tbody tr[data-id]'); pg.wait_for_timeout(600)
    rot = [x.strip() for x in pg.locator('#gv-acoes [data-acao=desejar], #gv-acoes [data-acao=cotar]').all_inner_texts()]
    ok('os dois botões citados existem mesmo, com esses nomes', rot == ['Quero comprar', 'Monitorar preço'], rot)
    pg.click('#gv-acoes [data-acao=desejar]'); pg.wait_for_timeout(600); pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
    pg.fill('#p-tab-recs input[type=search]', ''); pg.wait_for_timeout(300); pg.click('#nav [data-ir=precos]'); pg.wait_for_timeout(800); c = pg.evaluate(COT)
    ok('com um livro na lista de compra, o formulário aparece, já com ele escolhido', c['form'] and not c['aviso'] and c['parados'] == 0 and c['livro'] == 'O Nome da Rosa · sem cotação', c)
    ok('e o gráfico passa a indicar o próprio quadro', '“Registrar cotação”, nesta página' in c['grafico'], c['grafico'])
    pg.click('#f-tipo button[data-v=HQ]'); pg.wait_for_timeout(700); c = pg.evaluate(COT)
    ok('com um filtro que esconde o livro, o quadro e o gráfico dizem que são os filtros', not c['form'] and c['aviso'] == 'Nenhum item da lista de compra com os filtros atuais.'
       and c['grafico'] == 'Nenhum item com cotações com os filtros atuais.', c)
    pg.click('#f-tipo button[data-v=""]'); pg.wait_for_timeout(700)
    pg.fill('#p-cotacao input[data-c=preco]', '39,90'); pg.click('#p-cotacao [data-c=ok]'); pg.wait_for_timeout(900); k = pg.evaluate(K); c = pg.evaluate(COT)
    ok('a primeira cotação entra por ali: 1 item acompanhado, e o gráfico deixa de estar vazio', k['monit']['v'] == '1' and k['cot']['v'] == '1' and c['form'] and not c['grafico'] and c['livro'] == 'O Nome da Rosa', (k['monit'], k['cot'], c))
    b.close()
print('FALHAS:', falhas); print('ERROS:', len(errs) + len(falhas)); [print('  ', x[:300]) for x in errs[:10]]
