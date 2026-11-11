"""Trilhas de leitura, camadas curatoriais e a ordem de compra das recomendações.

O painel é aberto como o usuário o abre (sem dados de exemplo). Confere que:
  · o quadro "Trilhas de leitura" mostra as 20 trilhas com o que já está no acervo, o que foi lido e o que falta
    (um livro lido emprestado não falta), em ordem ou começando pelas que estão mais perto de fechar;
  · a trilha abre com os livros em ordem; dali se abre a ficha de cada um, se leva o que falta para a lista de compra
    e se filtra a tabela; comprar o que faltava fecha a trilha;
  · a ficha do livro mostra as camadas (pergunta, clima, papel, ponte, cenário) e as trilhas dele; cada uma vira filtro;
  · "O que comprar primeiro" ordena as recomendações que ainda não estão no acervo, diz o motivo, leva para a lista de
    compra com um clique e acompanha o que muda (o livro comprado sai, a trilha quase completa sobe);
  · a tabela das recomendações ordena pela mesma ordem e o CSV leva a posição, os motivos e as camadas;
  · tudo cabe na tela do telefone.

Os números esperados são um retrato do catálogo atual; se o catálogo mudar, confira as linhas FALHA e atualize.
"""
from caminhos import PAINEL_LIMPO, TMP
from relogio import fixa
import csv, io, json
from playwright.sync_api import sync_playwright

CHAVE = 'biblioteca-lucas:v1'
errs = []; falhas = []
TOAST = "() => { const t = [...document.querySelectorAll('#toasts .toast')].map(t => t.textContent.replace(/\\u00a0/g, ' ')); return t[t.length - 1] || ''; }"
DLG = "() => document.querySelector('#dlg').classList.contains('on') ? document.querySelector('#dlg h2').textContent : ''"
GAVETA = "() => document.querySelector('#gaveta').classList.contains('on') ? document.querySelector('#gaveta h2').textContent : ''"
TRILHAS = "() => [...document.querySelectorAll('#p-trilhas .li')].map(l => [l.querySelector('.tr-n').textContent, l.querySelector('.li-m b').textContent, l.querySelector('.li-m > span').textContent])"
NA_TRILHA = "() => [...document.querySelectorAll('#dlg .tr-l li')].map(l => [l.querySelector('.tr-n').textContent, l.querySelector('.li-m b').textContent, l.querySelector('.pill').textContent])"
COMPRA = "id => [...document.querySelectorAll('#' + id + ' .oc-l')].map(l => ({pos: l.querySelector('.tr-n').textContent, t: l.querySelector('.li-m b').textContent, motivos: l.querySelector('.oc-m').textContent, botao: l.querySelector('.oc-b').getAttribute('aria-label')}))"
CAMADAS = "() => Object.fromEntries([...document.querySelectorAll('#gv-camadas .camadas > div')].map(d => [d.querySelector('dt').textContent, [...d.querySelectorAll('dd .tag')].map(t => t.textContent.replace(/\\s+/g, ' ').trim())]))"
ATIVOS = "() => [...document.querySelectorAll('#f-ativos .ativo')].map(a => a.textContent)"
LINHAS = "v => [...document.querySelectorAll('#p-tab-' + v + ' tbody tr .tt b')].map(b => b.textContent.trim())"
K = "() => Object.fromEntries([...document.querySelectorAll('.visao:not([hidden]) .kpi')].map(k => [k.dataset.k, k.querySelector('.kpi-v b').textContent.replace(/\\u00a0/g, ' ')]))"
FORA = "() => { const d = document.documentElement; return d.scrollWidth - d.clientWidth; }"


def ok(nome, cond, extra=''):
    print(('  ok   ' if cond else '  FALHA') + ' ' + nome + (' — ' + str(extra)[:700] if extra != '' else ''))
    if not cond: falhas.append(nome)


with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={'width': 1440, 'height': 900}, locale='pt-BR', timezone_id='America/Sao_Paulo', accept_downloads=True)
    pg = ctx.new_page(); fixa(pg)
    pg.on('console', lambda m: errs.append(f'[{m.type}] {m.text}') if m.type in ('error', 'warning') else None)
    pg.on('pageerror', lambda e: errs.append(f'[pageerror] {e}'))
    pg.goto(PAINEL_LIMPO); pg.wait_for_timeout(1200); pg.click('#aviso .pri'); pg.wait_for_timeout(200)

    def fechar():
        for _ in range(3): pg.keyboard.press('Escape'); pg.wait_for_timeout(150)
    def ir(v): fechar(); pg.click(f'#nav [data-ir={v}]'); pg.wait_for_timeout(900)
    def abrir(busca, titulo):
        """Abre a ficha do livro pela tabela da visão geral."""
        fechar()
        if not pg.is_visible('#p-tab-geral'): pg.click('#nav [data-ir=geral]'); pg.wait_for_timeout(800)
        pg.fill('#p-tab-geral input[type=search]', busca); pg.wait_for_timeout(600)
        pg.locator('#p-tab-geral tbody tr[data-id]').filter(has=pg.locator('.tt b', has_text=titulo)).first.click(); pg.wait_for_timeout(700)
    guardado = lambda titulo: pg.evaluate("t => (JSON.parse(localStorage.getItem('%s')).livros.find(x => x.t === t) || null)" % CHAVE, titulo)
    trilha = lambda nome: next((t for t in pg.evaluate(TRILHAS) if t[1] == nome), None)
    def abrir_trilha(nome): pg.locator('#p-trilhas .li').filter(has=pg.locator('.li-m b', has_text=nome)).first.click(); pg.wait_for_timeout(500)

    print('O QUADRO DAS TRILHAS')
    ir('recs'); ts = pg.evaluate(TRILHAS)
    paineis = pg.evaluate("() => [...document.querySelectorAll('#v-recs .card')].map(c => c.id)")
    ok('Recomendações ganhou "O que comprar primeiro" e "Trilhas de leitura"', paineis == ['p-eixos-recs', 'p-matriz', 'p-compra', 'p-trilhas', 'p-tipo-recs', 'p-temas', 'p-sugestoes', 'p-tab-recs'], paineis)
    ok('as 20 trilhas, na ordem do catálogo', [t[0] for t in ts] == [str(i) for i in range(1, 21)] and ts[0][1] == 'Antes da Palavra' and ts[19][1] == 'Sexta à Noite', [t[1] for t in ts])
    ok('cada uma diz quanto já está no acervo e quanto falta', trilha('Divã e Martelo')[2] == 'tenho 7 de 8 · falta 1' and trilha('Das Estrelas à Rede')[2] == 'tenho 9 de 10 · falta 1' and trilha('Cidades Estranhas')[2] == 'tenho 3 de 11 · faltam 8', (trilha('Divã e Martelo'), trilha('Cidades Estranhas')))
    ok('livro lido que não está no acervo conta como feito, não como falta', trilha('Aço e Fé')[2] == 'tenho 7 de 8 · li 1 · nenhum por comprar' and trilha('Bisturi e Fé')[2] == 'tenho 3 de 8 · li 1 · faltam 4', (trilha('Aço e Fé'), trilha('Bisturi e Fé')))
    sub = pg.inner_text('#p-trilhas .card-s'); leg = pg.evaluate("() => [...document.querySelectorAll('#p-trilhas .card-f .leg')].map(l => l.textContent)")
    ok('o subtítulo conta as completas e a legenda explica a barra', sub == '20 roteiros com os livros em ordem · 1 já completo · clique para abrir' and leg == ['lidos', 'no acervo, por ler', 'faltam'], (sub, leg))
    seg = pg.evaluate("() => [...document.querySelectorAll('#p-trilhas .seg button')].map(b => [b.textContent, b.getAttribute('aria-pressed')])")
    ok('abre "Na ordem"', seg == [['Na ordem', 'true'], ['Falta pouco', 'false']], seg)
    pg.click('#p-trilhas .seg button[data-v=perto]'); pg.wait_for_timeout(500); ts = pg.evaluate(TRILHAS)
    ok('"Falta pouco": primeiro as que estão mais perto de fechar; a que não pede compra vai para o fim', [t[1] for t in ts[:4]] == ['Das Estrelas à Rede', 'Divã e Martelo', 'Do Aviso ao Espelho', 'Brasil Profundo'] and ts[-1][1] == 'Aço e Fé', [(t[1], t[2]) for t in ts[:4]] + [ts[-1][1]])
    pg.wait_for_timeout(500); pg.reload(); pg.wait_for_timeout(1500)
    ok('a escolha fica guardada', pg.evaluate(TRILHAS)[0][1] == 'Das Estrelas à Rede' and pg.get_attribute('#p-trilhas .seg button[data-v=perto]', 'aria-pressed') == 'true')
    pg.click('#p-trilhas .seg button[data-v=ordem]'); pg.wait_for_timeout(500)

    print('UMA TRILHA ABERTA')
    abrir_trilha('Divã e Martelo'); itens = pg.evaluate(NA_TRILHA)
    ok('abre com o nome inteiro e a descrição', pg.evaluate(DLG) == 'Trilha 6 · Divã e Martelo: Yalom, Nietzsche e os filósofos-pacientes' and 'Os romances de Yalom servem de ponte' in pg.inner_text('#dlg .dlg-sub') and pg.inner_text('#dlg .tr-res b') == 'Tenho 7 de 8 · falta 1', (pg.evaluate(DLG), pg.inner_text('#dlg .tr-res')))
    ok('os oito livros em ordem, cada um com a situação', [i[1] for i in itens] == ['Quando Nietzsche Chorou', 'Nietzsche Hoje', 'Além do Bem e do Mal', 'Assim Falou Zaratustra', 'Genealogia da Moral', 'Ecce Homo', 'O Enigma de Espinosa', 'A Cura de Schopenhauer']
       and [i[0] for i in itens] == [str(n) for n in range(1, 9)] and [i[2] for i in itens] == ['Tenho'] * 7 + ['Falta'], itens)
    bot = pg.evaluate("() => [...document.querySelectorAll('#dlg footer .btn')].map(b => b.textContent)")
    ok('botões: comprar o que falta e fechar; "ver na tabela" fica junto ao resumo', bot == ['Quero comprar o que falta', 'Fechar'] and pg.inner_text('#dlg [data-tr-tabela]') == 'ver na tabela', bot)
    pg.click('#dlg .tr-l li:nth-child(3) .li'); pg.wait_for_timeout(700)
    ok('clicar num livro fecha a trilha e abre a ficha dele', pg.evaluate(DLG) == '' and pg.evaluate(GAVETA) == 'Além do Bem e do Mal', (pg.evaluate(DLG), pg.evaluate(GAVETA)))
    cam = pg.evaluate(CAMADAS)
    ok('a ficha diz em que trilha o livro está e em que posição', cam.get('Trilha de leitura') == ['Divã e Martelo 3º de 8'], cam)
    pg.click('#gv-camadas [data-trilha]'); pg.wait_for_timeout(500)
    ok('e dali se volta à trilha, por cima da ficha', pg.evaluate(DLG).startswith('Trilha 6 · Divã e Martelo') and pg.evaluate(GAVETA) == 'Além do Bem e do Mal')
    pg.click('#dlg footer .btn >> nth=0'); pg.wait_for_timeout(800); g = guardado('A Cura de Schopenhauer')
    ok('"Quero comprar o que falta" leva o livro para as próximas aquisições', pg.evaluate(TOAST) == '1 livro foi para as próximas aquisições.' and g.get('col') == 'desejo' and g.get('prio') == 2 and g.get('u') == 1 and g.get('add') == 20766, (pg.evaluate(TOAST), {k: g.get(k) for k in ('col', 'prio', 'add')}))
    fechar(); ir('recs')
    ok('na lista de compra o livro ainda falta na trilha (só deixa de faltar quando chega ao acervo)', trilha('Divã e Martelo')[2] == 'tenho 7 de 8 · falta 1', trilha('Divã e Martelo'))
    abrir_trilha('Divã e Martelo'); itens = pg.evaluate(NA_TRILHA); bot = pg.evaluate("() => [...document.querySelectorAll('#dlg footer .btn')].map(b => b.textContent)")
    ok('a trilha mostra "Na lista de compra" e não oferece mais o botão', itens[7][2] == 'Na lista de compra' and bot == ['Fechar'], (itens[7], bot))
    pg.click('#dlg .tr-l li:nth-child(8) .li'); pg.wait_for_timeout(700)
    pg.click('#gv-acoes [data-acao=comprei]'); pg.wait_for_timeout(500); pg.click('#dlg footer .pri'); pg.wait_for_timeout(800); fechar()
    ok('comprado o último, a trilha fecha', trilha('Divã e Martelo')[2] == 'tenho todos os 8' and pg.inner_text('#p-trilhas .card-s') == '20 roteiros com os livros em ordem · 2 já completos · clique para abrir', (trilha('Divã e Martelo'), pg.inner_text('#p-trilhas .card-s')))
    abrir_trilha('Divã e Martelo')
    ok('e a trilha aberta diz o mesmo', pg.inner_text('#dlg .tr-res b') == 'Tenho todos os 8' and pg.evaluate(NA_TRILHA)[7][2] == 'Tenho', pg.inner_text('#dlg .tr-res'))
    pg.click('#dlg [data-tr-tabela]'); pg.wait_for_timeout(900)
    ok('"ver na tabela" filtra a visão geral pelos livros da trilha', pg.evaluate(DLG) == '' and pg.is_visible('#p-tab-geral') and pg.evaluate(ATIVOS) == ['Trilha: Divã e Martelo'] and len(pg.evaluate(LINHAS, 'geral')) == 8 and pg.evaluate(TOAST) == 'Filtrando pela trilha “Divã e Martelo”.', (pg.evaluate(ATIVOS), len(pg.evaluate(LINHAS, 'geral'))))
    pg.click('#f-ativos .ativo'); pg.wait_for_timeout(600)
    ir('recs'); abrir_trilha('Aço e Fé'); itens = pg.evaluate(NA_TRILHA)
    ok('trilha com um livro lido emprestado: "Lido · não tenho", e nada a comprar', itens[0] == ['1', 'O Arqueiro (Busca do Graal, vol. 1)', 'Lido · não tenho'] and pg.inner_text('#dlg .tr-res b') == 'Tenho 7 de 8 · li 1 · nenhum por comprar' and len(pg.evaluate("() => [...document.querySelectorAll('#dlg footer .btn')].map(b => b.textContent)")) == 1, itens[0])
    fechar()
    # o marcador da trilha posto à mão em outro livro: ele entra no fim da trilha
    abrir('Crepúsculo dos Ídolos', 'Crepúsculo dos Ídolos'); titulo9 = pg.evaluate(GAVETA)
    pg.click('#gv-acoes [data-acao=editar]'); pg.wait_for_timeout(500)
    pg.fill('#dlg [data-f=tags]', pg.input_value('#dlg [data-f=tags]') + ' trilha-yalom-nietzsche'); pg.click('#dlg footer .pri'); pg.wait_for_timeout(800)
    cam = pg.evaluate(CAMADAS); fechar(); ir('recs')
    ok('o marcador da trilha posto à mão põe o livro no fim dela', cam.get('Trilha de leitura') == ['Divã e Martelo 9º de 9'] and trilha('Divã e Martelo')[2] == 'tenho todos os 9', (titulo9, cam.get('Trilha de leitura'), trilha('Divã e Martelo')))

    print('CAMADAS NA FICHA E NOS FILTROS')
    abrir('O Nome da Rosa', 'O Nome da Rosa'); cam = pg.evaluate(CAMADAS)
    ok('a ficha mostra por que ler: pergunta, clima, papel e ponte', cam == {'Pergunta central': ['fé e dúvida'], 'Clima da leitura': ['cerebral'], 'Papel na biblioteca': ['ponte entre áreas'], 'Ponte entre áreas': ['ciência e fé']}, cam)
    dicas = pg.evaluate("() => [...document.querySelectorAll('#gv-camadas dd .tag')].map(t => t.title)")
    ok('cada camada explica o que reúne ao passar o mouse', dicas == ['Fé, ceticismo, Deus e o sagrado', 'Jogo de ideias, estrutura e quebra-cabeça intelectual', 'Cruza áreas diferentes e abre caminhos para outras leituras', 'Onde a ciência encontra (ou questiona) o sagrado'], dicas)
    soltos = pg.evaluate("() => [...document.querySelectorAll('#gaveta .gv-tags .tag')].map(t => t.dataset.tag)")
    ok('as camadas não se repetem entre os marcadores comuns', soltos == ['romance-historico', 'medieval', 'misterio', 'filosofia'], soltos)
    pg.click('#gv-camadas [data-tag=clima-cerebral]'); pg.wait_for_timeout(900)
    pg.fill('#p-tab-geral input[type=search]', ''); pg.wait_for_timeout(600)
    n = pg.evaluate("() => +document.querySelector('#p-tab-geral .abas [data-a=todos] .cont').textContent")
    ok('clicar numa camada fecha a ficha e filtra por ela', pg.evaluate(GAVETA) == '' and pg.evaluate(ATIVOS) == ['Clima: cerebral'] and pg.evaluate(TOAST) == 'Filtrando por #clima-cerebral.' and 0 < n < 60, (pg.evaluate(ATIVOS), n))
    pg.click('#pw-mais .pop-b'); pg.wait_for_timeout(300)
    grupos = pg.evaluate("() => [...document.querySelectorAll('#f-tags .tg-g')].map(g => [g.querySelector('.pop-r').textContent, g.querySelectorAll('.chip').length])")
    ok('os filtros ganharam as camadas, as trilhas e as marcas do usuário', grupos == [['Gêneros', 31], ['Temas', 62], ['Época e origem', 9], ['Afinidades', 6], ['Perguntas centrais', 12], ['Clima da leitura', 10], ['Papel na biblioteca', 6], ['Pontes entre áreas', 8], ['Cenários', 9], ['Trilhas de leitura', 20], ['Pendências', 2], ['Suas marcas', 1]], grupos)
    clima = pg.evaluate("() => { const g = [...document.querySelectorAll('#f-tags .tg-g')].find(g => g.querySelector('.pop-r').textContent === 'Clima da leitura'); return [...g.querySelectorAll('.chip')].map(c => [c.textContent, c.title, c.getAttribute('aria-pressed')]); }")
    ok('dentro do grupo o rótulo é curto, com a explicação na dica; o filtro ativo aparece marcado', clima[4] == ['Cerebral', 'Jogo de ideias, estrutura e quebra-cabeça intelectual', 'true'] and clima[0] == ['Claustrofóbico', 'Opressivo, fechado, sem saída', 'false'], clima[:5])
    pg.fill('#f-tagq', 'martelo'); pg.wait_for_timeout(300)
    vis = pg.evaluate("() => [...document.querySelectorAll('#f-tags .chip')].filter(c => !c.hidden).map(c => c.textContent)")
    ok('procurar marcador acha a trilha pelo nome', vis == ['Divã e Martelo'], vis)
    pg.fill('#f-tagq', ''); pg.keyboard.press('Escape'); pg.wait_for_timeout(300); pg.click('#f-ativos .ativo'); pg.wait_for_timeout(600)
    ir('recs')
    ops = pg.evaluate("() => [...document.querySelectorAll('#p-temas select option')].map(o => o.textContent)")
    ok('"Temas e camadas": os grupos num seletor', pg.inner_text('#p-temas h3') == 'Temas e camadas' and ops == ['Gêneros', 'Temas', 'Época e origem', 'Afinidades', 'Perguntas centrais', 'Clima da leitura', 'Papel na biblioteca', 'Pontes entre áreas', 'Cenários', 'Trilhas de leitura'] and pg.evaluate("() => document.querySelector('#p-temas select').selectedOptions[0].textContent") == 'Temas', ops)
    pg.select_option('#p-temas select', label='Clima da leitura'); pg.wait_for_timeout(600)
    barras = pg.evaluate("() => [...document.querySelectorAll('#p-temas .hb-n')].map(n => n.textContent)")
    ok('escolhido "Clima da leitura", as barras são os climas, com rótulo curto', len(barras) >= 8 and 'Cerebral' in barras and all(not x.startswith('Clima') for x in barras), barras)
    pg.wait_for_timeout(500); pg.reload(); pg.wait_for_timeout(1500)
    ok('e a escolha fica guardada', pg.evaluate("() => document.querySelector('#p-temas select').selectedOptions[0].textContent") == 'Clima da leitura')
    pg.select_option('#p-temas select', label='Temas'); pg.wait_for_timeout(400)

    print('O QUE COMPRAR PRIMEIRO')
    oc = pg.evaluate(COMPRA, 'p-compra'); pe = pg.inner_text('#p-compra .oc-n')
    ok('oito recomendações, da 1ª à 8ª, começando por "A Estrada"', [o['pos'] for o in oc] == [f'{i}º' for i in range(1, 9)] and [o['t'] for o in oc[:3]] == ['A Estrada', 'Em Busca de Sentido', 'Pedro Páramo'], [(o['pos'], o['t']) for o in oc])
    ok('cada uma com o motivo', oc[0]['motivos'] == 'prioridade sua (#top) · trilha “Sexta à Noite”: faltam 6 de 10 · porta de entrada da área · leitura-relâmpago' and all(o['motivos'] for o in oc), oc[0]['motivos'])
    ok('e um botão com nome próprio para levar à lista de compra', oc[0]['botao'] == 'Quero comprar: A Estrada' and all(o['botao'] == 'Quero comprar: ' + o['t'] for o in oc), oc[0]['botao'])
    ok('o rodapé conta as recomendações por comprar e avisa que a ordem não olha preços', pe == '429 recomendações por comprar · a ordem não olha preços' and pg.is_visible('#p-compra [data-oc-tudo]'), pe)
    pg.click('#p-compra .oc-l:first-child .li'); pg.wait_for_timeout(700)
    f = pg.evaluate("() => { const d = document.querySelector('#gaveta .f-oc'); return d ? d.innerText.replace(/\\s+/g, ' ') : null; }")
    ok('a ficha da recomendação traz a posição e os motivos', pg.evaluate(GAVETA) == 'A Estrada' and f == 'Ordem de compra sugerida 1º de 429 prioridade sua (#top) · trilha “Sexta à Noite”: faltam 6 de 10 · porta de entrada da área · leitura-relâmpago', f)
    fechar()
    pg.click('#p-compra .oc-l:first-child .oc-b'); pg.wait_for_timeout(800); oc = pg.evaluate(COMPRA, 'p-compra'); g = guardado('A Estrada')
    ok('o botão leva o livro para as próximas aquisições (prioridade alta, por ter #top)', pg.evaluate(TOAST) == 'Adicionado. Defina um preço-alvo em “Editar”.' and g.get('col') == 'desejo' and g.get('prio') == 1, (pg.evaluate(TOAST), g.get('col'), g.get('prio')))
    ok('ele sai da ordem e a fila anda', [o['t'] for o in oc[:2]] == ['Em Busca de Sentido', 'Pedro Páramo'] and oc[0]['pos'] == '1º' and pg.inner_text('#p-compra .oc-n').startswith('428 recomendações por comprar'), [(o['pos'], o['t']) for o in oc[:3]])
    ok('a trilha dele também muda os motivos dos vizinhos? não: na lista de compra ele ainda falta', 'trilha “Sexta à Noite”: faltam 6 de 10' in oc[0]['motivos'], oc[0]['motivos'])
    # a recomendação que fecha uma trilha sobe, e o motivo diz isso
    pg.click('#p-compra [data-oc-tudo]'); pg.wait_for_timeout(900)
    ordenada = pg.evaluate("() => { const th = document.querySelector('#p-tab-recs th[data-c=compra]'); return [th.getAttribute('aria-sort'), th.textContent.trim()]; }")
    linhas = pg.evaluate("() => [...document.querySelectorAll('#p-tab-recs tbody tr')].map(r => [r.querySelector('.tt b').textContent.trim(), r.querySelector('td.c-oc b').textContent, r.querySelector('td.c-oc .sub').textContent, r.querySelector('td.c-oc .sub').title])")
    ok('"ver a lista inteira nesta ordem" ordena a tabela pela ordem de compra', ordenada == ['ascending', 'Ordem de compra'] and [l[1] for l in linhas[:5]] == ['1º', '2º', '3º', '4º', '5º'] and linhas[0][0] == 'Em Busca de Sentido', (ordenada, linhas[:3]))
    ok('na tabela o motivo vem resumido, com o texto inteiro na dica', linhas[0][2] == 'prioridade sua · 2 trilhas' and linhas[0][3].startswith('prioridade sua (#top) · trilha “Sexta à Noite”: faltam 6 de 10 (e mais uma trilha)'), linhas[0])
    LINHA_OC = "t => { const r = [...document.querySelectorAll('#p-tab-recs tbody tr')].find(r => r.querySelector('.tt b').textContent.trim() === t); return r ? [t, r.querySelector('td.c-oc b') ? r.querySelector('td.c-oc b').textContent : '—', r.querySelector('td.c-oc .sub') ? r.querySelector('td.c-oc .sub').textContent : '', r.querySelector('td.c-oc .sub') ? r.querySelector('td.c-oc .sub').title : ''] : null; }"
    pg.fill('#p-tab-recs input[type=search]', '2001 Odisseia'); pg.wait_for_timeout(600); dois = pg.evaluate(LINHA_OC, '2001: Uma Odisseia no Espaço')
    ok('quem fecha uma trilha vem bem colocado, e o motivo diz qual', dois is not None and int(dois[1][:-1]) <= 30 and dois[2] == 'fecha uma trilha' and dois[3] == 'é o que falta para fechar a trilha “Das Estrelas à Rede”', dois)
    pg.fill('#p-tab-recs input[type=search]', 'Arqueiro Graal'); pg.wait_for_timeout(600); lido = pg.evaluate(LINHA_OC, 'O Arqueiro (Busca do Graal, vol. 1)')
    ok('recomendação já lida não entra na ordem de compra', lido == ['O Arqueiro (Busca do Graal, vol. 1)', '—', '', ''], lido)
    pg.fill('#p-tab-recs input[type=search]', ''); pg.wait_for_timeout(600)
    with pg.expect_download() as d: pg.click('#p-tab-recs [data-csv]')
    linhas_csv = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read()), delimiter=';'))
    cab = linhas_csv[0]; l1 = dict(zip(cab, linhas_csv[1]))
    ok('o CSV leva a posição, os motivos, as camadas e as anotações', cab == ['Título', 'Autor', 'Ordem de compra', 'Motivos da ordem', 'Eixo', 'Tipo', 'Dificuldade', 'Extensão', 'Temas', 'Pendência', 'Camadas e trilhas', 'Possui análise', 'Comentários', 'Inclusão']
       and l1['Título'] == 'Em Busca de Sentido' and l1['Ordem de compra'] == '1' and l1['Motivos da ordem'].startswith('prioridade sua (#top)') and 'trilha: Sexta à Noite' in l1['Camadas e trilhas'] and 'papel: porta de entrada' in l1['Camadas e trilhas'] and len(linhas_csv) == 431, (len(linhas_csv), cab, l1))
    # com filtro: só o que está no recorte, com a posição geral
    pg.click('#pw-eixo .pop-b'); pg.wait_for_timeout(300); pg.locator('#pop-eixo .opt', has_text='Espiritualidade').click(); pg.wait_for_timeout(700); pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
    oc = pg.evaluate(COMPRA, 'p-compra'); pe = pg.inner_text('#p-compra .oc-n')
    ok('com um eixo filtrado, o quadro mostra só as recomendações dele, com a posição geral', oc[0]['t'] == 'O Livro dos Espíritos' and [int(o['pos'][:-1]) for o in oc] == sorted(int(o['pos'][:-1]) for o in oc) and int(oc[-1]['pos'][:-1]) > 8 and pe.endswith('no recorte · 428 recomendações por comprar · a ordem não olha preços'), ([(o['pos'], o['t']) for o in oc[:3]], pe))
    pg.click('#f-ativos .ativo'); pg.wait_for_timeout(600)

    print('PRÓXIMAS AQUISIÇÕES')
    ir('desejos'); oc = pg.evaluate(COMPRA, 'p-compra-lista'); k = pg.evaluate(K)
    ok('a lista tem o livro que veio do botão (o outro já foi comprado)', k.get('itens') == '1' and pg.evaluate(LINHAS, 'desejos') == ['A Estrada'], (k, pg.evaluate(LINHAS, 'desejos')))
    ok('e o quadro "O que comprar primeiro" também está aqui, com seis sugestões', len(oc) == 6 and oc[0]['t'] == 'Em Busca de Sentido' and pg.inner_text('#p-compra-lista h3') == 'O que comprar primeiro', [(o['pos'], o['t']) for o in oc])
    pg.click('#p-compra-lista .oc-l:first-child .oc-b'); pg.wait_for_timeout(800)
    ok('levar dali para a lista funciona do mesmo jeito', pg.evaluate(K).get('itens') == '2' and sorted(pg.evaluate(LINHAS, 'desejos')) == ['A Estrada', 'Em Busca de Sentido'] and pg.evaluate(COMPRA, 'p-compra-lista')[0]['t'] == 'Pedro Páramo', pg.evaluate(LINHAS, 'desejos'))
    pg.click('#p-tab-desejos tbody tr >> nth=0'); pg.wait_for_timeout(600); pg.click('#gv-acoes [data-acao=tirar]'); pg.wait_for_timeout(700); fechar()
    ok('tirado da lista, o livro volta para a ordem de compra', pg.evaluate(K).get('itens') == '1' and len(pg.evaluate(LINHAS, 'desejos')) == 1)
    pg.screenshot(path=f'{TMP}/shots/trilhas-desejos.png', full_page=True)
    ir('recs'); pg.screenshot(path=f'{TMP}/shots/trilhas-recs.png', full_page=True)
    pg.context.close()

    print('NO TELEFONE')
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, locale='pt-BR', timezone_id='America/Sao_Paulo', is_mobile=True, has_touch=True, device_scale_factor=2)
    pg = ctx.new_page(); fixa(pg)
    pg.on('console', lambda m: errs.append(f'[{m.type}] {m.text}') if m.type in ('error', 'warning') else None)
    pg.on('pageerror', lambda e: errs.append(f'[pageerror] {e}'))
    pg.goto(PAINEL_LIMPO); pg.wait_for_timeout(1200); pg.click('#aviso .pri'); pg.wait_for_timeout(200)
    pg.click('#nav-m [data-ir=recs]'); pg.wait_for_timeout(1000)
    medidas = pg.evaluate("""() => { const dentro = s => [...document.querySelectorAll(s)].every(e => { const r = e.getBoundingClientRect(); return r.left >= -0.5 && r.right <= innerWidth + 0.5; });
      const c = document.querySelector('#p-trilhas .card-b'); return {fora: document.documentElement.scrollWidth - innerWidth, compra: dentro('#p-compra, #p-compra .oc-l, #p-compra .oc-b'), trilhas: dentro('#p-trilhas, #p-trilhas .li, #p-trilhas .tr-b'),
        altura: Math.round(c.getBoundingClientRect().height), rola: c.scrollHeight > c.clientHeight, botao: Math.round(document.querySelector('#p-compra .oc-b').getBoundingClientRect().width)}; }""")
    ok('os dois quadros cabem na tela, sem rolagem lateral', medidas['fora'] <= 0 and medidas['compra'] and medidas['trilhas'], medidas)
    ok('a lista de trilhas tem altura própria e rola por dentro; o botão da sacola dá para tocar', 300 <= medidas['altura'] <= 420 and medidas['rola'] and medidas['botao'] >= 32, medidas)
    pg.locator('#p-trilhas .li').first.scroll_into_view_if_needed(); pg.locator('#p-trilhas .li').first.click(); pg.wait_for_timeout(600)
    dl = pg.evaluate("() => { const c = document.querySelector('#dlg .dlg-cx').getBoundingClientRect(); return {t: document.querySelector('#dlg h2').textContent, dentro: c.left >= 0 && c.right <= innerWidth && c.bottom <= innerHeight + 1, itens: document.querySelectorAll('#dlg .tr-l li').length, pilulas: [...document.querySelectorAll('#dlg .tr-l .pill')].every(p => p.getBoundingClientRect().right <= innerWidth)}; }")
    ok('a trilha aberta cabe na tela', dl['t'].startswith('Trilha 1 · Antes da Palavra') and dl['dentro'] and dl['itens'] == 8 and dl['pilulas'], dl)
    pg.screenshot(path=f'{TMP}/shots/trilhas-tel-dlg.png')
    pg.click('#dlg .tr-l li:nth-child(2) .li'); pg.wait_for_timeout(700)
    gv = pg.evaluate("""() => { const dentro = s => [...document.querySelectorAll(s)].every(e => { const r = e.getBoundingClientRect(); return r.width === 0 || (r.left >= -0.5 && r.right <= innerWidth + 0.5); });
      return {t: document.querySelector('#gaveta h2').textContent, camadas: dentro('#gv-camadas .tag, #gv-camadas dt'), notas: dentro('#gv-notas textarea, #gv-notas .btn, #gv-notas .nt-an'), fora: document.querySelector('#gaveta .gv-c').scrollWidth - document.querySelector('#gaveta .gv-c').clientWidth}; }""")
    ok('e a ficha do livro, com as camadas e as anotações, também', gv['camadas'] and gv['notas'] and gv['fora'] <= 0, gv)
    pg.screenshot(path=f'{TMP}/shots/trilhas-tel-ficha.png')
    b.close()
print('FALHAS:', falhas); print('ERROS:', len(errs) + len(falhas)); [print('  ', x[:300]) for x in errs[:10]]
