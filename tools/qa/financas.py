"""A guia Finanças e a navegação de seis itens.

  · dinheiro tem lugar próprio: Visão geral, Biblioteca e Recomendações não mostram nenhum valor em reais — nem nos
    indicadores, nem nos gráficos, nem nas colunas das tabelas; os valores ficam em Finanças, Próximas aquisições e Preços;
  · Finanças: quatro indicadores, cinco cartões e a tabela "Compras registradas";
  · sem nenhuma compra registrada, cada cartão de Finanças diz o que falta, em vez de ficar em branco;
  · o botão de ocultar valores esconde todos os reais das três guias que os mostram;
  · a navegação tem os mesmos seis itens, na mesma ordem, no computador e no celular;
  · no celular os seis cabem numa linha só, de 412 a 320 px, sem cortar os nomes — e nenhuma guia estoura a largura da
    tela, com ou sem dados (um gráfico vazio já estourou, a 320 px).
"""
from caminhos import PAINEL_LIMPO, PAINEL_URL
from relogio import fixa, fonte_usada
from playwright.sync_api import sync_playwright

errs = []; falhas = []
GUIAS = [['geral', 'Visão geral', 'Geral'], ['biblioteca', 'Biblioteca', 'Biblioteca'], ['recs', 'Recomendações', 'Recomend.'],
         ['financas', 'Finanças', 'Finanças'], ['desejos', 'Próximas aquisições', 'Aquisições'], ['precos', 'Preços', 'Preços']]
SEM_REAIS = ('geral', 'biblioteca', 'recs'); COM_REAIS = ('financas', 'desejos', 'precos')
CARTOES = ['p-evo-valor', 'p-gastos', 'p-gasto-loja', 'p-ranking', 'p-cesta', 'p-tab-financas']
K = "() => Object.fromEntries([...document.querySelectorAll('.visao:not([hidden]) .kpi')].map(k => [k.dataset.k, k.querySelector('.kpi-v b').textContent.replace(/\\u00a0/g, ' ')]))"
NAV = "(s) => [...document.querySelectorAll(s + ' button[data-ir]')].map(x => [x.dataset.ir, x.querySelector('.nv-l').textContent, x.querySelector('.nv-c').textContent])"
# o que a guia aberta mostra: quantos "R$", os nomes das colunas da tabela e os cartões (com título e se estão vazios)
GUIA = """(v) => { const el = document.querySelector('#v-' + v), txt = el.innerText.replace(/\\u00a0/g, ' ');
    return { aberta: !el.hidden, reais: (txt.match(/R\\$/g) || []).length, comNumero: (el.textContent.replace(/\\u00a0/g, ' ').match(/R\\$ ?\\d/g) || []).length, ocultos: (txt.match(/R\\$ •••/g) || []).length,
             colunas: [...el.querySelectorAll('thead th')].map(t => t.textContent.trim()),
             cartoes: [...el.querySelectorAll('.card')].map(c => ({ id: c.id, titulo: (c.querySelector('h3') || {}).textContent || '', vazio: [...c.querySelectorAll('.vazio, .tb-vazio')].filter(x => x.getClientRects().length).map(x => x.textContent.replace(/\\s+/g, ' ').trim()).join(' ¦ ') })),
             titulo: document.querySelector('#titulo') ? document.querySelector('#titulo').textContent.trim() : '', estouro: document.documentElement.scrollWidth - document.documentElement.clientWidth }; }"""


def ok(nome, cond, extra=''):
    print(('  ok   ' if cond else '  FALHA') + ' ' + nome + (' — ' + str(extra) if extra != '' else ''))
    if not cond: falhas.append(nome)


with sync_playwright() as p:
    b = p.chromium.launch()

    def pagina(url, largura=1440, altura=900):
        cel = largura < 700
        ctx = b.new_context(viewport={'width': largura, 'height': altura}, locale='pt-BR', timezone_id='America/Sao_Paulo', is_mobile=cel, has_touch=cel)
        pg = ctx.new_page(); fixa(pg)
        pg.on('console', lambda m: errs.append(f'[{m.type}] {m.text}') if m.type in ('error', 'warning') else None)
        pg.on('pageerror', lambda e: errs.append(f'[pageerror] {e}'))
        pg.goto(url); pg.wait_for_timeout(1300); pg.click('#aviso .pri'); pg.wait_for_timeout(200)
        return pg

    def ir(pg, v, nav='#nav'): pg.click(f'{nav} [data-ir={v}]'); pg.wait_for_timeout(900); return pg.evaluate(GUIA, v)

    print('SEIS GUIAS, NA MESMA ORDEM')
    pg = pagina(PAINEL_URL)
    ok('no computador: Visão geral, Biblioteca, Recomendações, Finanças, Próximas aquisições, Preços', pg.evaluate(NAV, '#nav') == GUIAS, pg.evaluate(NAV, '#nav'))
    ok('a barra do celular tem os mesmos seis', pg.evaluate(NAV, '#nav-m') == GUIAS)

    print('DINHEIRO SÓ ONDE É O ASSUNTO (com os dados de exemplo, para haver valores a mostrar)')
    vistas = {v: ir(pg, v) for v, _, _ in GUIAS}
    for v in SEM_REAIS:
        g = vistas[v]; nome = next(n for i, n, _ in GUIAS if i == v)
        ok(f'{nome}: nenhum valor em reais', g['aberta'] and g['reais'] == 0 and g['comNumero'] == 0, (g['reais'], g['comNumero']))
        ok(f'{nome}: a tabela não tem coluna de valor', g['colunas'] and not [c for c in g['colunas'] if c.lower() in ('pago', 'valor', 'valor pago', 'preço', 'melhor preço', 'alvo')], g['colunas'])
    for v in COM_REAIS:
        g = vistas[v]; nome = next(n for i, n, _ in GUIAS if i == v)
        ok(f'{nome}: mostra valores em reais', g['aberta'] and g['reais'] >= 20, g['reais'])
    k = {v: (pg.click(f'#nav [data-ir={v}]'), pg.wait_for_timeout(700), pg.evaluate(K))[2] for v in ('geral', 'biblioteca')}
    ok('indicadores da Visão geral e da Biblioteca: livros e leituras, nada de dinheiro', list(k['geral']) == ['acervo', 'leituras', 'fila', 'recs'] and list(k['biblioteca']) == ['acervo', 'leituras', 'fila', 'lendo'] and not [x for x in list(k['geral'].values()) + list(k['biblioteca'].values()) if 'R$' in x], k)

    print('A GUIA FINANÇAS')
    g = ir(pg, 'financas'); kf = pg.evaluate(K)
    ok('quatro indicadores: investido, preço médio pago, cesta e itens abaixo do alvo', kf == {'investido': 'R$ 4.428', 'medio': 'R$ 48,66', 'cesta': 'R$ 1.296', 'oport': '6'}, kf)
    ok('cinco cartões e a tabela "Compras registradas"', [c['id'] for c in g['cartoes']] == CARTOES and [c['titulo'] for c in g['cartoes']] == ['Evolução do investimento', 'Gastos por período', 'Gasto por loja ou origem', 'Melhores oportunidades', 'Custo da cesta de aquisições', 'Compras registradas'], [(c['id'], c['titulo']) for c in g['cartoes']])
    ok('com dados, nenhum cartão fica vazio', not [c['id'] for c in g['cartoes'] if c['vazio']], [(c['id'], c['vazio'][:60]) for c in g['cartoes'] if c['vazio']])
    ok('a tabela traz aquisição, origem, condição e o valor pago', g['colunas'] == ['Título', 'Formato', 'Aquisição', 'Origem', 'Condição', 'Pago'], g['colunas'])
    ok('o item da navegação fica marcado como a página atual', pg.evaluate("() => [...document.querySelectorAll('#nav [aria-current=page]')].map(x => x.dataset.ir)") == ['financas'])

    print('OCULTAR VALORES')
    pg.click('#b-olho'); pg.wait_for_timeout(700)
    for v in COM_REAIS:
        g = ir(pg, v); nome = next(n for i, n, _ in GUIAS if i == v)
        ok(f'{nome}: com o olho fechado, nenhum valor em reais à vista (só "R$ •••")', g['comNumero'] == 0 and g['ocultos'] >= 5, (g['comNumero'], g['ocultos']))
    pg.click('#b-olho'); pg.wait_for_timeout(700); g = ir(pg, 'financas')
    ok('abrir o olho traz os valores de volta', g['comNumero'] >= 20 and g['ocultos'] == 0 and pg.evaluate(K)['investido'] == 'R$ 4.428', (g['comNumero'], g['ocultos']))
    pg.context.close()

    print('FINANÇAS SEM NENHUMA COMPRA REGISTRADA')
    pg = pagina(PAINEL_LIMPO); g = ir(pg, 'financas'); kf = pg.evaluate(K)
    ok('indicadores zerados, sem número inventado', kf == {'investido': 'R$ 0', 'medio': '—', 'cesta': '—', 'oport': '0'}, kf)
    vazios = {c['id']: c['vazio'] for c in g['cartoes']}
    ok('cada cartão diz o que falta, em vez de ficar em branco', [c['id'] for c in g['cartoes']] == CARTOES and all(len(t) >= 20 for t in vazios.values()), {i: t[:70] for i, t in vazios.items()})
    ok('a tabela explica como uma compra passa a aparecer', vazios.get('p-tab-financas', '').startswith('Nenhuma compra registrada ainda'), vazios.get('p-tab-financas'))
    ok('nenhum "R$" além do indicador zerado', g['reais'] == 1, g['reais'])
    pg.context.close()

    print('NO CELULAR')
    MEDE = """() => { const n = document.querySelector('#nav-m'), W = document.documentElement.clientWidth;
        const it = [...n.querySelectorAll('button[data-ir]')].map(x => { const r = x.getBoundingClientRect(), s = x.querySelector('.nv-c'), l = x.querySelector('.nv-l');
            return { nome: s.textContent, topo: Math.round(r.top), larg: Math.round(r.width), alt: Math.round(r.height), dentro: r.left >= -0.5 && r.right <= W + 0.5, cortado: s.scrollWidth > s.clientWidth + 1, curto: s.getClientRects().length > 0, longo: l.getClientRects().length > 0 }; });
        return { n: it.length, linhas: new Set(it.map(i => i.topo)).size, fora: it.filter(i => !i.dentro).map(i => i.nome), cortados: it.filter(i => i.cortado).map(i => i.nome), semNome: it.filter(i => !i.curto || i.longo).map(i => i.nome),
                 menor: Math.min(...it.map(i => i.larg)), alt: Math.min(...it.map(i => i.alt)), fixa: getComputedStyle(n).position, baixo: Math.round(n.getBoundingClientRect().bottom) - window.innerHeight }; }"""
    for largura in (412, 390, 360, 320):
        pg = pagina(PAINEL_LIMPO, largura, 800); r = pg.evaluate(MEDE)
        ok(f'{largura} px: os seis itens numa linha só, presos ao pé da tela', r['n'] == 6 and r['linhas'] == 1 and r['fixa'] == 'fixed' and abs(r['baixo']) <= 1, r)
        ok(f'{largura} px: nenhum nome cortado nem para fora da tela; cada item com espaço para o dedo', r['fora'] == [] and r['cortados'] == [] and r['semNome'] == [] and r['menor'] >= 48 and r['alt'] >= 44,
           dict(r, fonte=fonte_usada(pg, '#nav-m .nv-c')) if r['cortados'] else r)     # nome cortado: antes de mexer no painel, veja com que fonte o teste rodou (relogio.py)
        estouros = {}
        for v, nome, _ in GUIAS:
            g = ir(pg, v, '#nav-m')
            if g['estouro'] > 0 or not g['aberta']: estouros[v] = g['estouro']
        ok(f'{largura} px: nenhuma guia estoura a largura da tela (painel sem dados: gráficos vazios)', estouros == {}, estouros)
        atual = pg.evaluate("() => [...document.querySelectorAll('#nav-m [aria-current=page]')].map(x => x.dataset.ir)")
        ok(f'{largura} px: o item tocado fica marcado', atual == ['precos'], atual)
        pg.context.close()
    for largura in (360, 320):
        pg = pagina(PAINEL_URL, largura, 800); estouros = {}
        for v, nome, _ in GUIAS:
            g = ir(pg, v, '#nav-m')
            if g['estouro'] > 0: estouros[v] = g['estouro']
        ok(f'{largura} px: o mesmo com os dados de exemplo (gráficos cheios)', estouros == {}, estouros)
        g = ir(pg, 'financas', '#nav-m'); kf = pg.evaluate(K)
        cab = pg.evaluate("() => { const k = [...document.querySelectorAll('#v-financas .kpi')].map(x => { const v = x.querySelector('.kpi-v b'); return v.scrollWidth > v.clientWidth + 1; }); return k.filter(Boolean).length; }")
        ok(f'{largura} px: os indicadores de Finanças cabem sem cortar o valor', kf.get('investido') == 'R$ 4.428' and cab == 0, (kf, cab))
        pg.context.close()
    b.close()
print('FALHAS:', falhas); print('ERROS:', len(errs) + len(falhas)); [print('  ', x[:300]) for x in errs[:10]]
