"""Livro lido que não está no acervo: emprestado, de biblioteca, perdido.

O catálogo já sabia dizer isso (marcador `lido` numa recomendação); o painel, não: "Já li" só existia para os livros
do acervo. Confere que:
  · a ficha de uma recomendação oferece "Já li"; o diálogo explica o que acontece e aceita data e nota, ou nada;
  · a leitura conta como "de fora", o livro sai da fila de recomendações e da ordem de compra, e a trilha o dá por feito;
  · "Não li" desfaz — também no livro que o catálogo traz como lido; nada se perde ao recarregar;
  · o livro que o catálogo já traz como lido (A Metamorfose) pode ir para a lista de compra e continua lido;
  · o livro que está na lista de compra também oferece "Já li" — é o caminho para quem pôs lá, no painel anterior, um
    livro que o catálogo depois passou a dar como lido: o que foi mexido no painel não é trocado pelo catálogo;
  · no celular, os botões da ficha não vazam para o lado.

Os números esperados são um retrato do catálogo atual; se o catálogo mudar, confira as linhas FALHA e atualize.
"""
from caminhos import PAINEL_LIMPO
from relogio import fixa
from playwright.sync_api import sync_playwright

CHAVE = 'biblioteca-lucas:v1'
errs = []; falhas = []
K = "() => Object.fromEntries([...document.querySelectorAll('.visao:not([hidden]) .kpi')].map(k => [k.dataset.k, {v: k.querySelector('.kpi-v b').textContent.replace(/\\u00a0/g, ' '), s: k.querySelector('.kpi-s').textContent.replace(/\\u00a0/g, ' ')}]))"
TOAST = "() => { const t = [...document.querySelectorAll('#toasts .toast')].map(t => t.textContent.replace(/\\u00a0/g, ' ')); return t[t.length - 1] || ''; }"
FATOS = "() => Object.fromEntries([...document.querySelectorAll('#gaveta .fatos > div')].map(d => [d.querySelector('dt').textContent, d.querySelector('dd').innerText.replace(/\\u00a0/g, ' ').replace(/\\s+/g, ' ').trim()]))"
ACOES = "() => [...document.querySelectorAll('#gv-acoes [data-acao]')].map(b => b.dataset.acao + ':' + (b.textContent.trim() || b.getAttribute('aria-label')))"
DLG = "() => document.querySelector('#dlg').classList.contains('on') ? document.querySelector('#dlg h2').textContent : ''"
TRILHAS = "() => [...document.querySelectorAll('#p-trilhas .li')].map(l => [l.querySelector('.tr-n').textContent, l.querySelector('.li-m b').textContent, l.querySelector('.li-m > span').textContent])"
# a ordem de compra: na ficha, a posição do livro e os motivos (null se ele não está na ordem); no quadro, quantos estão na fila
OC = "() => { const d = document.querySelector('#gaveta .f-oc'); return d ? d.innerText.replace(/\\s+/g, ' ') : null; }"
POR_COMPRAR = "() => document.querySelector('#p-compra .oc-n').innerText.replace(/\\u00a0/g, ' ')"
NOTA = "() => document.querySelectorAll('#gaveta .fatos .estrelas i.on').length"
REC = ['desejar:Quero comprar', 'tenho:Já tenho', 'lido:Já li', 'cotar:Monitorar preço', 'editar:Editar']


def ok(nome, cond, extra=''):
    print(('  ok   ' if cond else '  FALHA') + ' ' + nome + (' — ' + str(extra) if extra != '' else ''))
    if not cond: falhas.append(nome)


with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={'width': 1440, 'height': 900}, locale='pt-BR', timezone_id='America/Sao_Paulo')
    pg = ctx.new_page(); fixa(pg)
    pg.on('console', lambda m: errs.append(f'[{m.type}] {m.text}') if m.type in ('error', 'warning') else None)
    pg.on('pageerror', lambda e: errs.append(f'[pageerror] {e}'))
    pg.goto(PAINEL_LIMPO); pg.wait_for_timeout(1200); pg.click('#aviso .pri'); pg.wait_for_timeout(200)

    def ir(v): pg.keyboard.press('Escape'); pg.wait_for_timeout(150); pg.click(f'#nav [data-ir={v}]'); pg.wait_for_timeout(900); return pg.evaluate(K)
    def abrir(busca, titulo):
        """Abre a ficha do livro pela tabela da visão geral."""
        for _ in range(2): pg.keyboard.press('Escape'); pg.wait_for_timeout(150)
        if not pg.is_visible('#p-tab-geral'): pg.click('#nav [data-ir=geral]'); pg.wait_for_timeout(800)
        pg.fill('#p-tab-geral input[type=search]', busca); pg.wait_for_timeout(600)
        pg.locator('#p-tab-geral tbody tr[data-id]').filter(has=pg.locator('.tt b', has_text=titulo)).first.click(); pg.wait_for_timeout(700)
    def acao(a): pg.click(f'#gv-acoes [data-acao={a}]'); pg.wait_for_timeout(500)
    def confirma(): pg.click('#dlg footer .pri'); pg.wait_for_timeout(800)
    guardado = lambda titulo: pg.evaluate("t => (JSON.parse(localStorage.getItem('%s')).livros.find(x => x.t === t) || null)" % CHAVE, titulo)
    def trilha(nome): return next((t[2] for t in pg.evaluate(TRILHAS) if t[1] == nome), None)
    def recs():
        """Na guia Recomendações: os indicadores, quantos estão na ordem de compra e a trilha de que "Piranesi" faz parte."""
        k = ir('recs'); return k, pg.evaluate(POR_COMPRAR), trilha('Labirintos de Borges')
    resumo = lambda k: (k['leituras']['v'], k['leituras']['s'], k['recs']['v'])

    k0 = ir('geral'); r0, compra0, tr0 = recs()
    ok('ponto de partida: 3 leituras, todas de fora; 487 recomendações na fila', resumo(k0) == ('3', '0 do acervo + 3 de fora', '487'), resumo(k0))
    abrir('Piranesi', 'Piranesi'); oc0 = pg.evaluate(OC)
    ok('"Piranesi" é o único livro que falta na trilha "Labirintos de Borges", e a ordem de compra diz isso', tr0 == 'tenho 8 de 9 · falta 1' and compra0 == '487 recomendações por comprar · a ordem não olha preços' and bool(oc0) and ' de 487 ' in oc0 and 'é o que falta para fechar a trilha “Labirintos de Borges”' in oc0, (tr0, compra0, oc0))

    print('JÁ LI, E NÃO TENHO')
    a = pg.evaluate(ACOES)
    ok('a ficha de uma recomendação oferece "Já li", ao lado de "Quero comprar" e "Já tenho"', a == REC, a)
    acao('lido'); nota = pg.inner_text('#dlg .form-n.ini')
    ok('o diálogo diz para que serve e o que acontece', pg.evaluate(DLG) == 'Já li este livro' and nota == 'Para o livro que você leu e não tem: emprestado, de biblioteca, perdido. Ele conta nas suas leituras e sai da fila de recomendações.', (pg.evaluate(DLG), nota))
    confirma(); f = pg.evaluate(FATOS); a = pg.evaluate(ACOES); g = guardado('Piranesi'); oc = pg.evaluate(OC)
    ok('sem data e sem nota: a leitura é registrada assim mesmo', pg.evaluate(TOAST) == 'Leitura registrada.' and f.get('Leitura') == 'Lido' and 'Nota' not in f and g['leit'] == 'lido' and g.get('lidoEm') is None and g['col'] == 'rec', (pg.evaluate(TOAST), f, {x: g.get(x) for x in ('leit', 'lidoEm', 'col')}))
    ok('o livro continua fora do acervo, e a ficha passa a oferecer "Não li"', a == ['desejar:Quero comprar', 'tenho:Já tenho', 'naoli:Não li', 'cotar:Monitorar preço', 'editar:Editar'] and 'Formato' not in f, a)
    k = ir('geral'); r, compra, tr = recs()
    ok('conta como leitura de fora e sai da fila de recomendações', resumo(k) == ('4', '0 do acervo + 4 de fora', '486') and r['recs']['v'] == '486', (resumo(k), r['recs']['v']))
    ok('sai da ordem de compra, e a trilha dá o livro por feito', oc is None and compra == '486 recomendações por comprar · a ordem não olha preços' and tr == 'tenho 8 de 9 · li 1 · nenhum por comprar', (oc, compra, tr))
    pg.reload(); pg.wait_for_timeout(1500); k = ir('geral')
    ok('recarregar não desfaz', resumo(k) == ('4', '0 do acervo + 4 de fora', '486'), resumo(k))

    print('COM DATA E NOTA; DESFAZER')
    abrir('Piranesi', 'Piranesi'); acao('naoli'); f = pg.evaluate(FATOS); t = pg.evaluate(TOAST); k = ir('geral'); r, compra, tr = recs()
    ok('"Não li" desfaz: indicadores, ordem de compra e trilha voltam ao que eram', t == 'Leitura desmarcada.' and 'Leitura' not in f and resumo(k) == resumo(k0) and compra == compra0 and tr == tr0, (t, f.get('Leitura'), resumo(k), tr))
    abrir('Piranesi', 'Piranesi'); a = pg.evaluate(ACOES); oc = pg.evaluate(OC); acao('lido'); pg.fill('#dlg [data-f=em]', '2026-10-01'); pg.select_option('#dlg [data-f=nota]', '4'); confirma(); f = pg.evaluate(FATOS)
    ok('a ficha volta a oferecer "Já li" e a mostrar a posição na ordem de compra', a == REC and oc == oc0, (a, oc))
    ok('com data e nota, as duas aparecem na ficha', f.get('Leitura') == 'Lido · 01/10/2026' and 'Nota' in f and pg.evaluate(NOTA) == 4, (f, pg.evaluate(NOTA)))
    pg.click('#gv-acoes [data-acao=naoli]'); pg.wait_for_timeout(500)

    print('O LIVRO QUE O CATÁLOGO JÁ TRAZ COMO LIDO')
    abrir('Metamorfose Kafka', 'A Metamorfose'); f = pg.evaluate(FATOS); a = pg.evaluate(ACOES)
    ok('"A Metamorfose" aparece como lida, fora do acervo', f.get('Leitura') == 'Lido' and a[:3] == ['desejar:Quero comprar', 'tenho:Já tenho', 'naoli:Não li'], (f.get('Leitura'), a))
    acao('desejar'); f = pg.evaluate(FATOS); a = pg.evaluate(ACOES); g = guardado('A Metamorfose'); k = ir('geral')
    ok('posta na lista de compra, continua lida', g['col'] == 'desejo' and g['leit'] == 'lido' and f.get('Leitura') == 'Lido' and 'naoli:Não li' in a and 'comprei:Comprei' in a and resumo(k) == resumo(k0), ({x: g.get(x) for x in ('col', 'leit')}, a, resumo(k)))
    abrir('Metamorfose Kafka', 'A Metamorfose'); acao('comprei'); confirma(); g = guardado('A Metamorfose'); k = ir('geral')
    ok('comprada, entra no acervo já como lida', g['col'] == 'acervo' and g['leit'] == 'lido' and resumo(k)[:2] == ('3', '1 do acervo + 2 de fora'), ({x: g.get(x) for x in ('col', 'leit')}, resumo(k)))

    print('NA LISTA DE COMPRA')
    abrir('Estrada McCarthy', 'A Estrada'); acao('desejar'); a = pg.evaluate(ACOES)
    ok('o livro da lista de compra também oferece "Já li"', a == ['comprei:Comprei', 'cotar:Registrar cotação', 'tirar:Tirar da lista', 'lido:Já li', 'editar:Editar'], a)
    acao('lido'); nota = pg.inner_text('#dlg .form-n.ini'); confirma(); g = guardado('A Estrada'); k = ir('geral')
    ok('lido, continua na lista de compra (o diálogo avisa)', nota == 'Para o livro que você leu e não tem: emprestado, de biblioteca, perdido. Ele conta nas suas leituras e continua na lista de compra.' and g['col'] == 'desejo' and g['leit'] == 'lido' and resumo(k)[:2] == ('4', '1 do acervo + 3 de fora'), (nota, {x: g.get(x) for x in ('col', 'leit')}, resumo(k)))

    print('DESMARCAR O QUE O CATÁLOGO TRAZ COMO LIDO')
    abrir('Arqueiro Cornwell', 'O Arqueiro'); a = pg.evaluate(ACOES); acao('naoli'); pg.reload(); pg.wait_for_timeout(1500); k = ir('geral'); g = guardado('O Arqueiro (Busca do Graal, vol. 1)')
    ok('"Não li" vale também para o livro que o catálogo dá como lido, e continua valendo depois de recarregar', 'naoli:Não li' in a and not g.get('leit') and g.get('u') == 1 and 'lido' not in g['tags'] and resumo(k)[:2] == ('3', '1 do acervo + 2 de fora'), (a, g.get('leit'), g['tags'], resumo(k)))

    print('NO CELULAR')
    pg.set_viewport_size({'width': 390, 'height': 800}); pg.wait_for_timeout(500)
    abrir('Piranesi', 'Piranesi'); m = pg.evaluate("() => { const g = document.querySelector('#gaveta'), a = document.querySelector('#gv-acoes'), r = a.getBoundingClientRect(); return { vaza: g.scrollWidth - g.clientWidth, larg: Math.round(r.width), tela: innerWidth, fora: [...a.querySelectorAll('button')].filter(b => { const q = b.getBoundingClientRect(); return q.left < r.left - 1 || q.right > r.right + 1; }).length, n: a.querySelectorAll('button').length }; }")
    ok('os cinco botões da ficha cabem na largura do celular, em duas linhas se for preciso', m['vaza'] <= 0 and m['fora'] == 0 and m['n'] == 5 and m['larg'] <= m['tela'], m)
    b.close()
print('FALHAS:', falhas); print('ERROS:', len(errs) + len(falhas)); [print('  ', x[:300]) for x in errs[:10]]
