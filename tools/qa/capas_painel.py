"""As capas no painel: onde aparecem, o que acontece quando a imagem falta e o que o navegador pede à internet.

Para não depender das capas que estiverem em catalogo/capas.tsv no dia, o teste usa uma cópia do painel com uma
lista de capas conhecida (alguns livros com capa, o resto sem). Nada sai para a internet: os pedidos de imagem são
respondidos aqui (ver relogio.py). Confere que:
  · a capa aparece na tabela, nas listas, na grade e na ficha; livro sem capa mostra o desenho com a inicial do título;
  · imagem que não existe (404) deixa o desenho com a inicial; na ficha, acrescenta o recado e tira o botão de ampliar;
  · os pedidos levam só o número da capa, e só são feitos para o que está na tela;
  · com as capas desligadas em "Seus dados", nenhuma imagem é pedida — nem depois de recarregar;
  · a capa não é guardada: nem no navegador, nem no backup; e um backup não consegue trocar a capa de um livro;
  · endereço de capa que não seja https é ignorado, e aspas no endereço não escapam do atributo;
  · no celular, a capa cabe no cartão do livro;
  · de onde vem a capa (Open Library, Apple, Google, à mão) e o aviso de que pode ser outra edição;
  · a capa maior só é pedida quando o usuário clica, e no tamanho certo de cada fonte;
  · a mesma lista como grade de capas: a escolha fica guardada, o cartão abre o livro e nada é pedido a mais.
"""
from caminhos import PAINEL, TMP
from relogio import fixa, capas_de_mentira, png
import json, re
from playwright.sync_api import sync_playwright

CHAVE = 'biblioteca-lucas:v1'
OL = 'https://covers.openlibrary.org/b/id/'
APPLE = 'https://is1-ssl.mzstatic.com/image/thumb/Publication115/v4/aa/bb/cc/capa-de-teste.jpg/200x300bb.jpg'     # como a busca guarda a capa da Apple Books
APPLE_SUMIU = 'https://is1-ssl.mzstatic.com/image/thumb/Publication9/v4/dd/ee/ff/saiu-da-loja.jpg/200x300bb.jpg'     # uma que a Apple deixou de ter
errs = []; falhas = []
TOAST = "() => { const t = [...document.querySelectorAll('#toasts .toast')].map(t => t.textContent.replace(/\\u00a0/g, ' ')); return t[t.length - 1] || ''; }"


def ok(nome, cond, extra=''):
    print(('  ok   ' if cond else '  FALHA') + ' ' + nome + (' — ' + str(extra) if extra != '' else ''))
    if not cond: falhas.append(nome)


# ───────── a cópia do painel com capas conhecidas ─────────
html = PAINEL.read_text(encoding='utf-8')
m = re.search(r'^const CATALOGO = (\[.*\]);$', html, flags=re.M)
catalogo = json.loads(m.group(1)) if m else []
def linha(titulo): return next(i for i, r in enumerate(catalogo) if r[0] == titulo)
CONHECIDAS = {
    'Fundação': 111,                                                # capa que existe
    'As Cavernas de Aço': 222,                                      # capa que existe
    'A Peste': 404404,                                              # número sem imagem: a Open Library responde 404
    'Guerra e Paz': 'https://exemplo.org/capas/guerra-e-paz.jpg',   # endereço posto à mão no capas.tsv
    'Contos da Taberna': APPLE,                                     # capa achada na Apple Books: o endereço inteiro
    '1984': APPLE_SUMIU,                                            # capa da Apple que não existe mais: responde 404
    'O Vento Solar': 'javascript:alert(1)',                         # não é https: tem de ser ignorado
    'A Ilha': 'https://exemplo.org/x.jpg" onerror="window.__furo=1',  # aspas no endereço: não podem virar atributo
}
FONTES = {'Fundação': 'e', 'As Cavernas de Aço': 'o', 'A Peste': 'e', 'Guerra e Paz': 'm', 'Contos da Taberna': 'a', '1984': 'a'}
lista = [0] * len(catalogo)
for titulo, capa in CONHECIDAS.items(): lista[linha(titulo)] = capa
fontes = ['0'] * len(catalogo)
for titulo, f in FONTES.items(): fontes[linha(titulo)] = f
copia, n = re.subn(r'^const CAPAS = \[.*\];$', lambda _: 'const CAPAS = ' + json.dumps(lista, ensure_ascii=False) + ';', html, count=1, flags=re.M)
copia, nf = re.subn(r'^const CAPAS_FONTES = ".*";$', lambda _: 'const CAPAS_FONTES = ' + json.dumps(''.join(fontes)) + ';', copia, count=1, flags=re.M)
arq = TMP / 'painel-capas.html'; arq.write_text(copia, encoding='utf-8')
URL = arq.as_uri()
print('PREPARO')
ok('o painel traz o catálogo e, logo depois, a lista de capas (uma posição por livro)', bool(m) and n == 1 and len(json.loads(re.search(r'^const CAPAS = (\[.*\]);$', html, flags=re.M).group(1))) == len(catalogo), (bool(m), n))

with sync_playwright() as p:
    b = p.chromium.launch()

    def pagina(largura=1440, altura=900, celular=False):
        ctx = b.new_context(viewport={'width': largura, 'height': altura}, locale='pt-BR', timezone_id='America/Sao_Paulo', accept_downloads=True, is_mobile=celular, has_touch=celular)
        pg = ctx.new_page(); fixa(pg)
        pedidos = []
        capas_de_mentira(pg, faltam=[404404, APPLE_SUMIU], pedidos=pedidos)   # as da Open Library (a 404404 não existe) e as da Apple (uma saiu da loja)
        def outras(rota):                                                # qualquer outro endereço de fora
            pedidos.append(rota.request.url)
            if rota.request.url.startswith('https://exemplo.org/'): rota.fulfill(status=200, content_type='image/png', body=png(40, 90, 160))
            else: rota.abort()
        pg.route(re.compile(r'^https?://(?!covers\.openlibrary\.org/|is\d+-ssl\.mzstatic\.com/)'), outras)
        # a imagem que falta deixa uma linha no console do navegador ("Failed to load resource … 404"): é esperado
        pg.on('console', lambda m: errs.append(f'[{m.type}] {m.text}') if m.type in ('error', 'warning') and 'Failed to load resource' not in m.text else None)
        pg.on('pageerror', lambda e: errs.append(f'[pageerror] {e}'))
        pg.goto(URL); pg.wait_for_timeout(1200); pg.click('#aviso .pri'); pg.wait_for_timeout(200)
        return pg, pedidos

    def busca(pg, texto, tab='geral'):
        pg.keyboard.press('Escape'); pg.wait_for_timeout(150)
        pg.fill(f'#p-tab-{tab} input[type=search]', texto); pg.wait_for_timeout(700)
    # a capa da primeira linha da tabela: [tem imagem?, endereço, carregou?, inicial desenhada, escondida de leitores de tela?]
    CAPA = """(sel) => { const c = document.querySelector(sel); if (!c) return null; const im = c.querySelector('img');
        return { img: !!im, src: im ? im.getAttribute('src') : '', carregou: !!im && im.complete && im.naturalWidth > 0, alt: im ? im.getAttribute('alt') : null, preguica: im ? im.getAttribute('loading') : null,
                 letra: c.dataset.l, desenho: getComputedStyle(c, '::before').content, oculto: c.getAttribute('aria-hidden'), larg: Math.round(c.getBoundingClientRect().width), alt_px: Math.round(c.getBoundingClientRect().height) }; }"""
    LINHA1 = '#p-tab-geral tbody tr[data-id] .capa'
    def abre(pg): pg.locator('#p-tab-geral tbody tr[data-id]').first.click(); pg.wait_for_timeout(800)

    print('NA TABELA')
    pg, pedidos = pagina()
    busca(pg, 'Fundação Asimov'); pg.wait_for_timeout(300); c = pg.evaluate(CAPA, LINHA1)
    ok('livro com capa: a imagem vem da Open Library pelo número', c and c['img'] and c['src'] == OL + '111-M.jpg?default=false' and c['carregou'], c)
    ok('a imagem é decorativa (alt vazio, fora da leitura de tela) e só é buscada quando chega perto da tela', c and c['alt'] == '' and c['oculto'] == 'true' and c['preguica'] == 'lazy', c)
    ok('tem o formato de um livro em pé (30 × 45)', c and (c['larg'], c['alt_px']) == (30, 45), c and (c['larg'], c['alt_px']))
    busca(pg, 'Duna Herbert'); c = pg.evaluate(CAPA, LINHA1)
    ok('livro sem capa: nenhuma imagem, só o desenho com a inicial do título', c and not c['img'] and c['letra'] == 'D' and c['desenho'] == '"D"', c)
    busca(pg, 'Peste Camus'); pg.wait_for_timeout(500); c = pg.evaluate(CAPA, LINHA1)
    ok('capa que não existe (404): a imagem some e fica o desenho com a inicial', c and not c['img'] and c['letra'] == 'A' and any(u.startswith(OL + '404404-') for u in pedidos), c)
    busca(pg, 'Guerra e Paz Tolstói'); pg.wait_for_timeout(400); c = pg.evaluate(CAPA, LINHA1)
    ok('capa posta à mão: vale o endereço completo', c and c['img'] and c['src'] == 'https://exemplo.org/capas/guerra-e-paz.jpg' and c['carregou'], c)
    busca(pg, 'Contos da Taberna'); pg.wait_for_timeout(400); c = pg.evaluate(CAPA, LINHA1)
    ok('capa da Apple Books: a imagem vem do endereço guardado, sem nada acrescentado', c and c['img'] and c['src'] == APPLE and c['carregou'] and c['preguica'] == 'lazy', c)
    busca(pg, '1984 Orwell'); pg.wait_for_timeout(500); c = pg.evaluate(CAPA, '#p-tab-geral tbody tr[data-id]:first-child .capa')
    ok('capa da Apple que deixou de existir (404): fica o desenho com a inicial, como na Open Library', c and not c['img'] and c['letra'] == '1' and APPLE_SUMIU in pedidos, c)
    busca(pg, 'Vento Solar'); c = pg.evaluate(CAPA, LINHA1)
    ok('endereço que não é https é ignorado', c and not c['img'], c)
    busca(pg, 'A Ilha Huxley'); pg.wait_for_timeout(300); c = pg.evaluate(CAPA, LINHA1)
    atributos = pg.evaluate(f"() => {{ const im = document.querySelector('{LINHA1} img'); return im ? im.getAttributeNames().sort() : []; }}")
    ok('aspas no endereço não escapam: a imagem só tem os atributos de sempre', atributos == ['alt', 'decoding', 'loading', 'src'] and pg.evaluate('() => window.__furo') is None, atributos)

    print('NA FICHA DO LIVRO')
    TOPO = "() => { const t = document.querySelector('#gaveta.on #gv-topo'); if (!t) return null; const c = t.querySelector('.capa'), im = c && c.querySelector('img'), f = t.querySelector('#gv-capa-f'); return { quadro: !!c, grande: !!c && c.classList.contains('g'), src: im ? im.getAttribute('src') : '', carregou: !!im && im.complete && im.naturalWidth > 0, larg: c ? Math.round(c.getBoundingClientRect().width) : 0, titulo: t.querySelector('h2').textContent, letra: c ? c.dataset.l : '', zoom: !!t.querySelector('[data-capa-zoom]'), fonte: f ? f.textContent : '', aviso: !!f && f.classList.contains('av') }; }"
    busca(pg, 'Fundação Asimov'); abre(pg); t = pg.evaluate(TOPO)
    ok('livro com capa: a ficha abre com a capa grande ao lado do título', t and t['grande'] and t['src'] == OL + '111-M.jpg?default=false' and t['carregou'] and t['larg'] == 104 and t['titulo'] == 'Fundação', t)
    busca(pg, 'Duna Herbert'); abre(pg); t = pg.evaluate(TOPO)
    ok('livro sem capa: a ficha não reserva espaço para ela', t and not t['quadro'] and t['titulo'].startswith('Duna'), t)
    busca(pg, 'Peste Camus'); abre(pg); pg.wait_for_timeout(500); t = pg.evaluate(TOPO)
    ok('capa que não existe: fica o desenho com a inicial, o recado e nenhum botão de ampliar', t and t['quadro'] and not t['src'] and t['letra'] == 'A' and not t['zoom'] and 'não carregou' in t['fonte'] and t['aviso'], t)
    pg.keyboard.press('Escape'); pg.wait_for_timeout(300)

    print('DE ONDE VEM A CAPA')
    for termo, titulo, trecho, aviso in [('Fundação Asimov', 'Fundação', 'Capa da Open Library, da edição com este título.', False),
                                         ('Cavernas de Aço', 'As Cavernas de Aço', 'pode ser de outra edição ou língua', True),
                                         ('Contos da Taberna', 'Contos da Taberna', 'Capa da Apple Books', False),
                                         ('Guerra e Paz Tolstói', 'Guerra e Paz', 'escolhida à mão', False)]:
        busca(pg, termo); abre(pg); pg.wait_for_timeout(300); t = pg.evaluate(TOPO)
        ok(f'{titulo}: a ficha diz de onde vem a capa' + (' e avisa que pode ser outra edição' if aviso else ''), t and t['titulo'] == titulo and trecho in t['fonte'] and t['aviso'] == aviso, t and (t['fonte'], t['aviso']))
        pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
    busca(pg, 'Duna Herbert'); abre(pg); t = pg.evaluate(TOPO)
    ok('livro sem capa: nenhuma frase sobre origem', t and not t['fonte'], t and t['fonte'])
    pg.keyboard.press('Escape'); pg.wait_for_timeout(200)

    print('A CAPA MAIOR')
    busca(pg, 'Fundação Asimov'); pg.wait_for_timeout(400)
    ok('antes do clique, nenhuma imagem grande foi pedida', not any('-L.jpg' in u for u in pedidos), [u for u in pedidos if '-L.jpg' in u])
    abre(pg); pg.wait_for_timeout(300); pg.click('#gv-topo [data-capa-zoom]'); pg.wait_for_timeout(600)
    z = pg.evaluate("() => { const d = document.querySelector('#dlg.on'); if (!d) return null; const im = d.querySelector('.capa-grande img'); return { titulo: d.querySelector('#dlg-t').textContent, src: im ? im.getAttribute('src') : '', alt: im ? im.getAttribute('alt') : '', carregou: !!im && im.complete && im.naturalWidth > 0, larg: im ? Math.round(im.getBoundingClientRect().width) : 0, fonte: d.querySelector('.capa-grande-f').textContent }; }")
    ok('clique na capa da ficha: abre a imagem grande da Open Library (tamanho L)', z and z['titulo'] == 'Fundação' and z['src'] == OL + '111-L.jpg?default=false' and z['carregou'] and z['larg'] > 104, z)
    ok('a imagem grande tem descrição para leitor de tela e diz a fonte', z and z['alt'] == 'Capa de Fundação, de Isaac Asimov' and 'Open Library' in z['fonte'], z and (z['alt'], z['fonte']))
    ok('a ficha continua aberta por baixo', pg.evaluate("() => !!document.querySelector('#gaveta.on')"))
    pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
    ok('Esc fecha a capa maior e volta para a ficha', not pg.evaluate("() => !!document.querySelector('#dlg.on')") and pg.evaluate("() => !!document.querySelector('#gaveta.on')"))
    pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
    busca(pg, 'Contos da Taberna'); abre(pg); pg.wait_for_timeout(300); pg.click('#gv-topo [data-capa-zoom]'); pg.wait_for_timeout(600)
    z = pg.evaluate("() => { const im = document.querySelector('#dlg.on .capa-grande img'); return im ? { src: im.getAttribute('src'), carregou: im.complete && im.naturalWidth > 0 } : null; }")
    ok('capa da Apple: a maior é pedida no tamanho 600 × 900, no mesmo endereço', z and z['src'] == APPLE.replace('200x300bb', '600x900bb') and z['carregou'], z)
    for _ in range(2): pg.keyboard.press('Escape'); pg.wait_for_timeout(200)

    print('A LISTA COMO GRADE DE CAPAS')
    busca(pg, 'Asimov'); pg.wait_for_timeout(400)
    ok('a tabela começa como tabela', pg.evaluate("() => { const t = document.querySelector('#p-tab-geral'); return !t.querySelector('.tb-grade').hidden === false && t.querySelector('table').style.display !== 'none' && t.querySelector('[data-modo=tabela]').getAttribute('aria-pressed') === 'true'; }"))
    pg.click('#p-tab-geral [data-modo=grade]'); pg.wait_for_timeout(500)
    g = pg.evaluate("() => { const t = document.querySelector('#p-tab-geral'), cs = [...t.querySelectorAll('.tb-grade .gc')]; return { n: cs.length, tabela: t.querySelector('table').style.display, escondido: t.querySelector('.tb-grade').hidden, comCapa: cs.filter(c => c.querySelector('.capa.m')).length, comImg: cs.filter(c => c.querySelector('.capa img')).length, botao: t.querySelector('[data-modo=grade]').getAttribute('aria-pressed'), primeiro: cs[0] ? cs[0].querySelector('.gc-t b').textContent : '', larg: cs[0] ? Math.round(cs[0].querySelector('.capa').getBoundingClientRect().width) : 0 }; }")
    ok('o botão de grade troca a lista por cartões com capa, título e autor', g['n'] >= 3 and g['tabela'] == 'none' and not g['escondido'] and g['comCapa'] == g['n'] and g['botao'] == 'true' and g['larg'] == 76, g)
    ok('a grade mostra as capas dos livros que estão na tela', g['comImg'] >= 2, g)
    pg.click('#p-tab-geral .tb-grade .gc'); pg.wait_for_timeout(600)
    ok('clique num cartão abre a ficha do livro', pg.evaluate("() => !!document.querySelector('#gaveta.on #gv-topo h2')"))
    pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
    pg.reload(); pg.wait_for_timeout(1400)
    ok('a escolha entre tabela e grade fica guardada', pg.evaluate("() => !document.querySelector('#p-tab-geral .tb-grade').hidden"))
    ok('e o que fica salvo é só a escolha, nunca a capa', '_img' not in (pg.evaluate("() => localStorage.getItem('%s')" % CHAVE) or '') and 'openlibrary' not in (pg.evaluate("() => localStorage.getItem('%s')" % CHAVE) or ''))
    pg.click('#p-tab-geral [data-modo=tabela]'); pg.wait_for_timeout(400)
    ok('dá para voltar à tabela', pg.evaluate("() => { const t = document.querySelector('#p-tab-geral'); return t.querySelector('.tb-grade').hidden && t.querySelector('table').style.display !== 'none' && t.querySelectorAll('tbody tr[data-id]').length > 0; }"))
    ok('as outras listas não ganharam botão de grade', pg.evaluate("() => { document.querySelector('#nav [data-ir=financas]').click(); return true; }") and (pg.wait_for_timeout(600) or pg.evaluate("() => !document.querySelector('#p-tab-financas .tb-modo')")))
    pg.click('#nav [data-ir=geral]'); pg.wait_for_timeout(500)

    print('NAS LISTAS')
    busca(pg, ''); pg.evaluate('() => window.scrollTo(0, 0)'); pg.wait_for_timeout(500)
    listas = pg.evaluate("() => { const ls = [...document.querySelectorAll('.visao:not([hidden]) .li')]; return { n: ls.length, comQuadro: ls.filter(l => l.querySelector('.capa')).length, primeiro: ls.filter(l => l.firstElementChild && l.firstElementChild.classList.contains('capa')).length }; }")
    ok('cada linha das listas da visão geral começa pelo quadro da capa', listas['n'] > 0 and listas['n'] == listas['comQuadro'] == listas['primeiro'], listas)

    print('O QUE O NAVEGADOR PEDIU')
    de_fora = sorted(set(pedidos))
    ruins = [u for u in de_fora if not re.fullmatch(re.escape(OL) + r'\d+-[ML]\.jpg\?default=false', u) and u not in ('https://exemplo.org/capas/guerra-e-paz.jpg', APPLE, APPLE_SUMIU, APPLE.replace('200x300bb', '600x900bb')) and not u.startswith('https://exemplo.org/x.jpg')]
    ok('só imagens de capa: pelo número (Open Library), pelo endereço da Apple ou pelo posto à mão — e as maiores, só onde houve clique', bool(de_fora) and not ruins, ruins[:3] or de_fora)
    numeros = sorted({re.search(r'/(\d+)-[ML]', u).group(1) for u in de_fora if u.startswith(OL)})
    ok('e só das capas que apareceram na tela (111, 404404 e a 222, que foi vista na grade)', numeros == ['111', '222', '404404'], numeros)
    ok('nenhum pedido de capa para "javascript:" nem para livro sem capa', not any('javascript' in u for u in de_fora))

    print('CAPAS DESLIGADAS')
    pg.click('#b-dados'); pg.wait_for_timeout(400)
    texto = pg.inner_text('#dlg').replace('\u00a0', ' ')
    ok('"Seus dados" explica de onde vêm as capas e quantos livros têm', 'Open Library' in texto and 'Apple Books' in texto and 'Google Books' in texto and '7 dos 2.614 livros têm capa encontrada' in texto, re.findall(r'\d+ dos [\d.]+ livros[^.]*', texto))
    ok('a chave "mostrar as capas" começa ligada', pg.is_checked('#dlg input[data-x=capas]'))
    pg.click('#dlg input[data-x=capas]'); pg.wait_for_timeout(500)
    ok('desligar avisa que nada mais será buscado', pg.evaluate(TOAST) == 'Capas desligadas: o painel não busca mais nenhuma imagem.', pg.evaluate(TOAST))
    pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
    del pedidos[:]
    busca(pg, 'Fundação Asimov'); c = pg.evaluate(CAPA, LINHA1); abre(pg); t = pg.evaluate(TOPO)
    ok('a tabela mostra o desenho com a inicial, e a ficha fica sem o quadro', c and not c['img'] and c['letra'] == 'F' and t and not t['quadro'], (c, t))
    pg.keyboard.press('Escape'); pg.wait_for_timeout(200); busca(pg, '')
    for v in ('biblioteca', 'recs', 'financas', 'desejos', 'precos', 'geral'):
        pg.click(f'#nav [data-ir={v}]'); pg.wait_for_timeout(500)
    ok('em nenhuma visão sobra imagem de capa', pg.evaluate("() => document.querySelectorAll('.capa img').length") == 0)
    pg.click('#p-tab-geral [data-modo=grade]'); pg.wait_for_timeout(500)
    ok('na grade, com as capas desligadas, ficam os desenhos com as iniciais', pg.evaluate("() => { const cs = [...document.querySelectorAll('#p-tab-geral .tb-grade .gc')]; return cs.length > 0 && cs.every(c => c.querySelector('.capa') && !c.querySelector('img')); }"))
    pg.click('#p-tab-geral [data-modo=tabela]'); pg.wait_for_timeout(300)
    pg.wait_for_timeout(700); pg.reload(); pg.wait_for_timeout(1300)
    busca(pg, 'Cavernas de Aço'); abre(pg); pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
    ok('nem depois de recarregar: nenhum pedido de imagem foi feito', pedidos == [] and pg.evaluate("() => document.querySelectorAll('.capa img').length") == 0, pedidos[:3])
    ok('a escolha ficou guardada', pg.evaluate("() => JSON.parse(localStorage.getItem('%s')).cfg.capas" % CHAVE) is False)
    pg.click('#b-dados'); pg.wait_for_timeout(400)
    ok('ao reabrir "Seus dados", a chave está desligada', not pg.is_checked('#dlg input[data-x=capas]'))
    pg.click('#dlg input[data-x=capas]'); pg.wait_for_timeout(500)
    ok('ligar de novo', pg.evaluate(TOAST) == 'Capas ligadas.', pg.evaluate(TOAST))
    pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
    busca(pg, 'Cavernas de Aço'); pg.wait_for_timeout(400); c = pg.evaluate(CAPA, LINHA1)
    ok('as capas voltam', c and c['img'] and c['src'] == OL + '222-M.jpg?default=false' and c['carregou'], c)

    print('A CAPA NÃO É GUARDADA')
    abre(pg); pg.click('#gv-acoes [data-acao=editar]'); pg.wait_for_timeout(500); pg.fill('#dlg [data-f=pg]', '250'); pg.click('#dlg footer .pri'); pg.wait_for_timeout(900)
    pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
    guardado = pg.evaluate("() => localStorage.getItem('%s')" % CHAVE)
    ok('no navegador: nem o número nem o endereço de nenhuma capa', '_img' not in guardado and 'openlibrary' not in guardado and 'exemplo.org' not in guardado and '"As Cavernas de Aço"' in guardado, len(guardado))
    pg.click('#b-dados'); pg.wait_for_timeout(400)
    with pg.expect_download() as d: pg.click('#dlg [data-x=exportar]')
    d.value.save_as(f'{TMP}/capas-backup.json'); texto = open(f'{TMP}/capas-backup.json', encoding='utf-8').read()
    ok('no backup: também não', '_img' not in texto and 'openlibrary' not in texto and 'exemplo.org' not in texto, len(texto))
    # um backup adulterado, que tenta dar a um livro uma capa de outro endereço
    bk = json.loads(texto)
    for x in bk['livros']:
        if x.get('t') in ('As Cavernas de Aço', 'Duna'): x['_img'] = 'https://outro-lugar.example/espia.png'; x['img'] = 'https://outro-lugar.example/espia.png'
    open(f'{TMP}/capas-backup-mexido.json', 'w', encoding='utf-8').write(json.dumps(bk, ensure_ascii=False))
    del pedidos[:]
    pg.set_input_files('#arq', f'{TMP}/capas-backup-mexido.json'); pg.wait_for_timeout(800); pg.click('#dlg footer .pri'); pg.wait_for_timeout(1200)
    for _ in range(2): pg.keyboard.press('Escape'); pg.wait_for_timeout(150)
    busca(pg, 'Cavernas de Aço'); pg.wait_for_timeout(400); c1 = pg.evaluate(CAPA, LINHA1); busca(pg, 'Duna Herbert'); pg.wait_for_timeout(300); c2 = pg.evaluate(CAPA, LINHA1)
    ok('um backup não troca a capa de um livro: vale sempre a do catálogo', c1 and c1['src'] == OL + '222-M.jpg?default=false' and c2 and not c2['img'] and not any('outro-lugar' in u for u in pedidos), (c1, c2, pedidos[:3]))
    pg.context.close()

    print('LIVRO CRIADO NO PAINEL')
    pg, pedidos = pagina()
    pg.click('#b-novo'); pg.wait_for_timeout(400); pg.fill('#dlg [data-f=t]', 'Ímpar, o Livro Novo'); pg.click('#dlg footer .pri'); pg.wait_for_timeout(900)
    t = pg.evaluate(TOPO); pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
    busca(pg, 'Ímpar, o Livro Novo'); c = pg.evaluate(CAPA, LINHA1)
    ok('não tem capa: desenho com a inicial (com acento) e ficha sem quadro', c and not c['img'] and c['letra'] == 'Í' and t and not t['quadro'], (c, t))
    pg.context.close()

    print('NO CELULAR')
    for largura in (390, 320):
        pg, pedidos = pagina(largura, 800, celular=True)
        pg.click('#nav-m [data-ir=biblioteca]'); pg.wait_for_timeout(900)
        pg.fill('#p-tab-biblioteca input[type=search]', 'Asimov'); pg.wait_for_timeout(700)
        r = pg.evaluate("""() => { const linhas = [...document.querySelectorAll('#p-tab-biblioteca tbody tr[data-id]')];
            const fora = linhas.filter(l => { const c = l.querySelector('.capa'), q = c.getBoundingClientRect(), d = l.getBoundingClientRect(), t = l.querySelector('.tt').getBoundingClientRect(); return q.width !== 30 || q.left < d.left || q.right > t.left + 1 || t.right > d.right + 1; });
            return { n: linhas.length, comImagem: linhas.filter(l => l.querySelector('.capa img')).length, fora: fora.length, pagina: document.documentElement.scrollWidth - document.documentElement.clientWidth }; }""")
        ok(f'{largura} px: no cartão do livro, a capa fica à esquerda do título, sem apertar nem estourar', r['n'] >= 3 and r['comImagem'] >= 2 and r['fora'] == 0 and r['pagina'] <= 0, r)
        pg.locator('#p-tab-biblioteca tbody tr[data-id]').filter(has=pg.locator('.tt b', has_text='Fundação')).first.click(); pg.wait_for_timeout(800)
        r = pg.evaluate("""() => { const g = document.querySelector('#gaveta.on'), t = g.querySelector('#gv-topo'), c = t.querySelector('.capa.g'), x = t.querySelector('.gv-tx'), h = t.querySelector('h2');
            const q = c.getBoundingClientRect(), tx = x.getBoundingClientRect(), gq = g.getBoundingClientRect();
            return { capa: Math.round(q.width), texto: Math.round(tx.width), dentro: q.left >= gq.left && tx.right <= gq.right + 1, corta: h.scrollWidth > h.clientWidth + 1 }; }""")
        ok(f'{largura} px: na ficha, a capa e o título cabem lado a lado', r['capa'] >= 72 and r['texto'] >= 120 and r['dentro'] and not r['corta'], r)
        pg.click('#gv-topo [data-capa-zoom]'); pg.wait_for_timeout(600)
        r = pg.evaluate("() => { const d = document.querySelector('#dlg.on'), im = d && d.querySelector('.capa-grande img'); if (!im) return null; const q = im.getBoundingClientRect(); return { larg: Math.round(q.width), dentro: q.left >= 0 && q.right <= innerWidth + 1, carregou: im.complete && im.naturalWidth > 0 }; }")
        ok(f'{largura} px: a capa maior cabe na tela do celular', r and r['dentro'] and r['larg'] > 100 and r['carregou'], r)
        pg.keyboard.press('Escape'); pg.wait_for_timeout(200); pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
        pg.click('#p-tab-biblioteca [data-modo=grade]'); pg.wait_for_timeout(500)
        r = pg.evaluate("() => { const cs = [...document.querySelectorAll('#p-tab-biblioteca .tb-grade .gc')]; return { n: cs.length, pagina: document.documentElement.scrollWidth - document.documentElement.clientWidth, fora: cs.filter(c => { const q = c.getBoundingClientRect(); return q.left < 0 || q.right > innerWidth + 1; }).length }; }")
        ok(f'{largura} px: a grade de capas cabe na tela, sem estourar para os lados', r['n'] >= 3 and r['fora'] == 0 and r['pagina'] <= 0, r)
        pg.context.close()
    b.close()
print('FALHAS:', falhas); print('ERROS:', len(errs) + len(falhas)); [print('  ', x[:300]) for x in errs[:10]]
