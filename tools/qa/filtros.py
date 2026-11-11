"""Os filtros por marcador: o número ao lado de cada botão, a soma dentro do grupo e o grupo da psicologia.

São as três primeiras propostas de catalogo/ANALISE-DOS-FILTROS.md. Confere que:
  A. os grupos — treze, cada marcador num grupo só; a psicologia tem o dela, com dez portas (abordagens, depois áreas);
  B. o número — ao lado de cada botão vai quantos livros a lista da tela mostra com ele ligado: bate com o catálogo
     (contado aqui, por fora do painel); o botão que não mostraria nenhum livro fica apagado, e continua clicável;
  C. a combinação — dois marcadores do mesmo grupo somam ("ou"), de grupos diferentes cruzam ("e"); os filtros ativos
     dizem qual das duas; o número de um botão não muda quando o vizinho de grupo é marcado;
  D. a chave — com dois marcadores ligados num grupo aparece "qualquer um / todos"; "todos" cruza, fica guardado e
     resiste à recarga;
  E. o quadro "Temas e camadas" das recomendações segue a mesma regra: as barras não somem quando uma é clicada;
  F. a busca de marcador acha pelo nome completo e pela explicação, não pelo número;
  G. o número do botão é o número da lista: nas seis telas, com os dados de exemplo, clica botão por botão e compara
     com a aba "Todos" da tabela — também com um período escolhido;
  H. preferências guardadas pelo painel anterior (ou estragadas) são entendidas;
  I. no celular, a chave cabe na folha de filtros e nada vaza para o lado;
  J. o que é novo tem contraste AA nos dois temas: o botão apagado, os números, o "ou", a explicação.

O que se espera é contado aqui, direto de src/catalog.json; só os rótulos e a ordem dos grupos são retrato do painel.
"""
import json, random
from caminhos import PAINEL_LIMPO, PAINEL_URL, RAIZ, TMP
from relogio import fixa
from playwright.sync_api import sync_playwright

CHAVE_DADOS = 'biblioteca-lucas:v1'
errs = []; falhas = []

# ── o catálogo, lido por fora do painel: [título, autor, "marcadores", seção, eixo, …] ──
CAT = json.loads((RAIZ / 'src' / 'catalog.json').read_text(encoding='utf-8'))
MARCAS = [set(r[2].split()) for r in CAT]
TENHO = [bool(m & {'tenho-fisico', 'tenho-digital', 'ja-tenho'}) for m in MARCAS]
EIXO = [r[4] for r in CAT]
quantos = lambda f, onde=None: sum(1 for i, m in enumerate(MARCAS) if f(m) and (onde is None or onde(i)))
tem = lambda *ts: (lambda m: all(t in m for t in ts))
algum = lambda *ts: (lambda m: any(t in m for t in ts))
meu = lambda i: TENHO[i]
de_fora = lambda i: not TENHO[i]

GRUPOS_ESPERADOS = [['Gêneros', 31], ['Temas', 52], ['Psicologia: abordagens e áreas', 10], ['Época e origem', 9], ['Afinidades', 6], ['Perguntas centrais', 12], ['Clima da leitura', 10],
                    ['Papel na biblioteca', 6], ['Pontes entre áreas', 8], ['Cenários', 9], ['Trilhas de leitura', 36], ['Pendências', 2], ['Suas marcas', 1]]
PSI = [['psicanalise', 'Psicanálise'], ['tcc', 'TCC'], ['behaviorismo', 'Behaviorismo'], ['psicologia-analitica', 'Analítica (Jung)'], ['psicologia-humanista', 'Humanista'],
       ['psicologia-social', 'Social'], ['psicopatologia', 'Psicopatologia'], ['psicometria', 'Psicometria'], ['neurociencia', 'Neurociência'], ['autoconhecimento', 'Autoconhecimento']]
SLUGS_PSI = [s for s, _ in PSI]

# ── o que se lê da tela ──
GRUPOS = "() => [...document.querySelectorAll('#f-tags .tg-g')].map(g => [g.querySelector('.pop-r').textContent, [...g.querySelectorAll('.chip')].map(c => [c.dataset.v, c.querySelector('span').textContent, +c.dataset.n])])"
BOTAO = "v => { const c = document.querySelector(`#f-tags .chip[data-v=\"${v}\"]`); return { n: +c.dataset.n, txt: c.querySelector('em').textContent, zero: c.classList.contains('zero'), on: c.getAttribute('aria-pressed') === 'true', nome: c.getAttribute('aria-label'), dica: c.title }; }"
TODOS_BOTOES = "() => [...document.querySelectorAll('#pop-mais .chip')].map(c => ({ g: c.parentElement.dataset.grupo, v: c.dataset.v, n: +c.dataset.n, zero: c.classList.contains('zero') }))"
OPCOES_EIXO = "() => [...document.querySelectorAll('#pop-eixo .opt')].map(o => ({ v: +o.querySelector('input').value, n: +o.querySelector('em').textContent.replace(/\\./g, ''), zero: o.classList.contains('zero') }))"
ABA = "() => { const t = document.querySelector('.visao:not([hidden]) .card-tab .abas [data-a=todos] .cont'); return t ? +t.textContent.replace(/\\./g, '') : null; }"
# filtros ativos, como se lê: o que anda junto vai entre parênteses, com a palavra que une ("ou", "e")
ATIVOS = "() => { const el = document.querySelector('#f-ativos'); return el.hidden ? '' : [...el.children].filter(e => !e.matches('.fa-r, .lk')).map(e => e.matches('.fa-g') ? '(' + [...e.children].map(x => x.textContent).join(' ') + ')' : e.textContent).join(' + '); }"
CHAVE = "nome => { const g = [...document.querySelectorAll('#f-tags .tg-g')].find(g => g.querySelector('.pop-r').textContent === nome), m = g.querySelector('.tg-m'); return m.hidden ? null : [...m.querySelectorAll('button')].filter(b => b.getAttribute('aria-pressed') === 'true').map(b => b.textContent).join('+'); }"
CLICA = "([g, v]) => document.querySelector(`#pop-mais .chips[data-grupo=${g}] .chip[data-v=\"${v}\"]`).click()"
CLICA_EIXO = "v => document.querySelector(`#pop-eixo input[value=\"${v}\"]`).click()"
VISIVEIS = "() => [...document.querySelectorAll('#f-tags .chip')].filter(c => !c.hidden).map(c => c.querySelector('span').textContent)"
BARRAS = "() => [...document.querySelectorAll('#p-temas .hb')].map(h => [h.dataset.k, +h.querySelector('.hb-v').textContent, h.classList.contains('sel')])"
GUARDADO = "() => (JSON.parse(localStorage.getItem('%s') || '{}').cfg || {}).ui" % CHAVE_DADOS
QUADRO = "() => document.querySelector('#p-temas select').selectedOptions[0].textContent"
# contraste (WCAG) do texto de um elemento contra o fundo que de fato fica atrás dele
CONTRASTE = """() => {
  // a cor é lida pintando um ponto: vale para qualquer forma que o navegador use ("rgb(…)", "color(srgb … / .86)", como no fundo da barra de filtros)
  const cv = document.createElement('canvas'); cv.width = cv.height = 1; const cx = cv.getContext('2d', { willReadFrequently: true });
  const rgba = s => { cx.clearRect(0, 0, 1, 1); cx.fillStyle = '#000'; cx.fillStyle = s; cx.fillRect(0, 0, 1, 1); const d = cx.getImageData(0, 0, 1, 1).data; return [d[0], d[1], d[2], d[3] / 255]; };
  const lum = c => { const [r, g, b] = c.map(v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }); return 0.2126 * r + 0.7152 * g + 0.0722 * b; };
  const fundo = e => { const pilha = []; for (let x = e; x; x = x.parentElement) { const c = rgba(getComputedStyle(x).backgroundColor); if (c[3] > 0) { pilha.push(c); if (c[3] >= 1) break; } }
    let base = [255, 255, 255]; for (const c of pilha.reverse()) base = base.map((v, i) => c[i] * c[3] + v * (1 - c[3])); return base; };
  const razao = e => { const f = fundo(e), t = rgba(getComputedStyle(e).color), cor = [0, 1, 2].map(i => t[i] * t[3] + f[i] * (1 - t[3])), a = lum(cor), b = lum(f); return +((Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05)).toFixed(2); };
  const um = s => { const e = document.querySelector(s); return e ? razao(e) : null; };
  return { 'botão apagado': um('#f-tags .chip.zero span'), 'número do apagado': um('#f-tags .chip.zero em'), 'número': um('#f-tags .chip:not(.zero):not([aria-pressed=true]) em'), 'número do ligado': um('#f-tags .chip[aria-pressed=true] em'),
           'explicação': um('#f-regra'), 'ou': um('#f-ativos .fa-c'), 'eixo apagado': um('#pop-eixo .opt.zero span'), 'número das prioridades': um('#f-top-n'), 'nome do grupo': um('#f-tags .tg-h .pop-r') }; }"""


def ok(nome, cond, extra=''):
    print(('  ok   ' if cond else '  FALHA') + ' ' + nome + (' — ' + str(extra) if extra != '' else ''))
    if not cond: falhas.append(nome)


def abre(b, url, largura=1440, altura=1000, tema='light'):
    ctx = b.new_context(viewport={'width': largura, 'height': altura}, locale='pt-BR', timezone_id='America/Sao_Paulo', color_scheme=tema)
    pg = ctx.new_page(); fixa(pg)
    pg.on('console', lambda m: errs.append(f'[{m.type}] {m.text}') if m.type in ('error', 'warning') else None)
    pg.on('pageerror', lambda e: errs.append(f'[pageerror] {e}'))
    pg.goto(url); pg.wait_for_timeout(1300)
    if pg.is_visible('#aviso .pri'): pg.click('#aviso .pri'); pg.wait_for_timeout(200)
    return pg


with sync_playwright() as p:
    b = p.chromium.launch()
    pg = abre(b, PAINEL_LIMPO)

    def fecha(): pg.keyboard.press('Escape'); pg.wait_for_timeout(200)                       # fecha "Mais filtros", se estiver aberto
    def ir(v): fecha(); pg.click(f'#nav [data-ir={v}]'); pg.wait_for_timeout(800)
    def mais():                                                                              # abre "Mais filtros" (se já estiver aberto, deixa como está)
        if not pg.evaluate("() => document.querySelector('#pw-mais').classList.contains('aberto')"): pg.click('#pw-mais .pop-b'); pg.wait_for_timeout(300)
    def marcador(v): mais(); pg.click(f'#f-tags .chip[data-v="{v}"]'); pg.wait_for_timeout(450)
    def limpar(): pg.evaluate("() => { const l = document.querySelector('#f-ativos [data-limpar]') || document.querySelector('#f-ativos .ativo'); if (l) l.click(); }"); pg.wait_for_timeout(450)
    botao = lambda v: pg.evaluate(BOTAO, v)
    aba = lambda: pg.evaluate(ABA)
    ativos = lambda: pg.evaluate(ATIVOS)
    chave = lambda nome: pg.evaluate(CHAVE, nome)

    print('A. Os grupos')
    mais()
    grupos = pg.evaluate(GRUPOS)
    ok('treze grupos, na ordem; a psicologia vem logo depois de "Temas"', [[n, len(c)] for n, c in grupos] == GRUPOS_ESPERADOS, [[n, len(c)] for n, c in grupos])
    slugs = [c[0] for _, cs in grupos for c in cs]
    ok('cada marcador mora num grupo só', len(slugs) == len(set(slugs)), sorted({s for s in slugs if slugs.count(s) > 1}))
    psi = next(cs for n, cs in grupos if n.startswith('Psicologia'))
    ok('as dez portas da psicologia: abordagens primeiro, depois as áreas', [c[:2] for c in psi] == PSI, [c[:2] for c in psi])
    ok('dentro do grupo o nome é curto e a dica explica', botao('psicologia-analitica')['dica'] == 'Jung e a psicologia analítica' and botao('tcc')['dica'] == 'Terapia cognitivo-comportamental e terapias cognitivas', (botao('psicologia-analitica')['dica'], botao('tcc')['dica']))
    temas = {c[0] for c in next(cs for n, cs in grupos if n == 'Temas')}
    ok('"Temas" ficou sem as dez, e com a psicologia geral e a psiquiatria', not (temas & set(SLUGS_PSI)) and {'psicologia', 'psiquiatria'} <= temas, sorted(temas & set(SLUGS_PSI)))
    usados = {m for ms in MARCAS for m in ms} - {'F', 'NF', 'd1', 'd2', 'd3', 'e1', 'e2', 'e3', 'tenho-fisico', 'tenho-digital', 'ja-tenho', 'lido', 'top'}
    ok('todo marcador do catálogo tem botão', not (usados - set(slugs)), sorted(usados - set(slugs)))

    print('B. O número ao lado de cada botão')
    fora = {c[0]: (c[2], quantos(tem(c[0]))) for _, cs in grupos for c in cs if c[2] != quantos(tem(c[0]))}
    ok(f'visão geral: os {len(slugs)} números batem com o catálogo', not fora and len(slugs) > 190, fora)
    ok('os números da psicologia: 152 de psicanálise, 9 de psicometria, 101 de autoconhecimento', [c[2] for c in psi] == [quantos(tem(s)) for s in SLUGS_PSI] and (psi[0][2], psi[7][2], psi[9][2]) == (152, 9, 101), [c[2] for c in psi])
    r = botao('cenario-russia')
    ok('o número aparece no botão e é dito a quem usa leitor de tela', r['txt'] == str(r['n']) and r['nome'] == f'Rússia: {r["n"]} livros' and not r['zero'], r)
    outros = pg.evaluate(TODOS_BOTOES)
    dif = [x['n'] for x in outros if x['g'] == 'dif']; ext = [x['n'] for x in outros if x['g'] == 'ext']
    ok('dificuldade e extensão também levam número, e cada trio soma o catálogo inteiro', dif == [quantos(tem(f'd{i}')) for i in (1, 2, 3)] and ext == [quantos(tem(f'e{i}')) for i in (1, 2, 3)] and sum(dif) == sum(ext) == len(CAT), (dif, ext))
    ok('"Só prioridades" diz quantas são', pg.inner_text('#f-top-n') == str(quantos(tem('top'))), pg.inner_text('#f-top-n'))
    eixos = pg.evaluate(OPCOES_EIXO)
    ok('os eixos: os números de sempre, e somam o catálogo', [e['n'] for e in eixos] == [EIXO.count(i) for i in range(1, 17)] and sum(e['n'] for e in eixos) == len(CAT), [e['n'] for e in eixos])
    analise = botao('analise')
    ok('botão sem nenhum livro: apagado, com o zero e a explicação', analise['zero'] and analise['txt'] == '0' and analise['nome'] == 'Possui análise: nenhum livro' and 'nenhum livro nesta tela' in analise['dica'], analise)
    cor = pg.evaluate("() => { const z = document.querySelector('#f-tags .chip.zero'), v = document.querySelector('#f-tags .chip:not(.zero)'); return [getComputedStyle(z).color, getComputedStyle(z).borderTopStyle, getComputedStyle(z).opacity, getComputedStyle(v).color, getComputedStyle(v).borderTopStyle]; }")
    ok('apagado pela cor e pelo contorno tracejado, não por transparência', cor[0] != cor[3] and cor[1] == 'dashed' and cor[4] == 'solid' and cor[2] == '1', cor)

    ir('biblioteca'); mais()
    grupos = pg.evaluate(GRUPOS)
    fora = {c[0]: (c[2], quantos(tem(c[0]), meu)) for _, cs in grupos for c in cs if c[2] != quantos(tem(c[0]), meu)}
    ok('na Biblioteca os números contam só o acervo', not fora and aba() == sum(TENHO), fora)
    ok('os eixos também seguem a tela', [e['n'] for e in pg.evaluate(OPCOES_EIXO)] == [sum(1 for i, e in enumerate(EIXO) if e == k and TENHO[i]) for k in range(1, 17)])
    ir('recs'); mais()
    grupos = pg.evaluate(GRUPOS)
    fora = {c[0]: (c[2], quantos(tem(c[0]), de_fora)) for _, cs in grupos for c in cs if c[2] != quantos(tem(c[0]), de_fora)}
    ok('nas Recomendações, só o que não está no acervo', not fora and aba() == len(CAT) - sum(TENHO), fora)
    tcc = botao('tcc')
    ok('TCC não tem nenhuma recomendação: ali o botão fica apagado', tcc['zero'] and tcc['n'] == 0 == quantos(tem('tcc'), de_fora), tcc)
    marcador('tcc'); tcc = botao('tcc')
    ok('apagado não é desligado: clicado, filtra (a lista fica vazia) e fica aceso como os outros', tcc['on'] and not tcc['zero'] and aba() == 0 and ativos() == '#TCC', (tcc, aba(), ativos()))
    marcador('tcc'); ir('financas'); mais()
    vazios = pg.evaluate(TODOS_BOTOES)
    ok('numa tela sem nenhum livro (Finanças, antes de qualquer compra) todos os botões ficam apagados', aba() == 0 and len(vazios) > 190 and all(x['zero'] and x['n'] == 0 for x in vazios), [x['v'] for x in vazios if not x['zero']][:5])

    print('C. Dentro do grupo soma, entre grupos cruza')
    ir('geral')
    R, N = quantos(tem('cenario-russia')), quantos(tem('cenario-nova-inglaterra'))
    marcador('cenario-russia')
    ok('um cenário: a lista tem o número do botão', aba() == R == 12 and ativos() == 'Cenário: Rússia', (aba(), ativos()))
    ok('com um só marcador a chave do grupo não aparece', chave('Cenários') is None)
    marcador('cenario-nova-inglaterra')
    ok('dois cenários: a lista SOMA os dois (antes dava zero)', aba() == quantos(algum('cenario-russia', 'cenario-nova-inglaterra')) == R + N == 25 and quantos(tem('cenario-russia', 'cenario-nova-inglaterra')) == 0, aba())
    ok('os filtros ativos dizem "ou"', ativos() == '(Cenário: Rússia ou Cenário: Nova Inglaterra)', ativos())
    ok('o número de cada um não muda quando o vizinho é marcado', (botao('cenario-russia')['n'], botao('cenario-nova-inglaterra')['n'], botao('cenario-espaco-profundo')['n']) == (R, N, quantos(tem('cenario-espaco-profundo'))))
    ok('aparece a chave do grupo, em "qualquer um"; os outros grupos seguem sem chave', chave('Cenários') == 'qualquer um' and chave('Clima da leitura') is None, chave('Cenários'))
    dois = lambda t: (lambda m: ('cenario-russia' in m or 'cenario-nova-inglaterra' in m) and t in m)
    ok('os outros grupos passam a contar dentro dos dois cenários', botao('clima-claustrofobico')['n'] == quantos(dois('clima-claustrofobico')) == 3 and botao('clima-comico')['zero'] and quantos(dois('clima-comico')) == 0, (botao('clima-claustrofobico'), botao('clima-comico')))
    marcador('clima-claustrofobico')
    ok('marcador de outro grupo CRUZA: (Rússia ou Nova Inglaterra) e claustrofóbico', aba() == 3 and ativos() == '(Cenário: Rússia ou Cenário: Nova Inglaterra) + Clima: claustrofóbico', (aba(), ativos()))
    pg.evaluate(CLICA_EIXO, 7); pg.wait_for_timeout(450)
    ok('o eixo cruza com os dois', aba() == quantos(dois('clima-claustrofobico'), lambda i: EIXO[i] == 7) == 2, aba())
    pg.evaluate(CLICA_EIXO, 3); pg.wait_for_timeout(450)
    ok('dois eixos somam entre si, como sempre — e agora os filtros ativos dizem', aba() == quantos(dois('clima-claustrofobico'), lambda i: EIXO[i] in (3, 7)) == 3
       and ativos() == '(Clássicos universais ou Horror, weird e mistério) + (Cenário: Rússia ou Cenário: Nova Inglaterra) + Clima: claustrofóbico', (aba(), ativos()))
    fecha(); pg.click('#f-ativos .ativo[data-rm="tags:cenario-russia"]'); pg.wait_for_timeout(450)
    ok('tirar um dos dois pelos filtros ativos desfaz só aquele', ativos() == '(Clássicos universais ou Horror, weird e mistério) + Cenário: Nova Inglaterra + Clima: claustrofóbico' and chave('Cenários') is None and aba() == 2, (ativos(), aba()))
    pg.click('#f-ativos [data-limpar=tudo]'); pg.wait_for_timeout(450)
    ok('"limpar tudo" zera os filtros', ativos() == '' and aba() == len(CAT), (ativos(), aba()))
    for v in ('horror', 'gotico', 'cenario-nova-inglaterra'): marcador(v)
    ok('gêneros somam e o cenário cruza: (horror ou gótico) e Nova Inglaterra', aba() == quantos(lambda m: ('horror' in m or 'gotico' in m) and 'cenario-nova-inglaterra' in m) == 12 and ativos() == '(#horror ou #gótico) + Cenário: Nova Inglaterra', (aba(), ativos()))
    limpar()
    pg.evaluate(CLICA_EIXO, 14); pg.wait_for_timeout(450)
    portas = [botao(s)['n'] for s in SLUGS_PSI]
    ok('o eixo da psicologia (440 livros) visto pelas dez portas', aba() == 440 and portas == [quantos(tem(s), lambda i: EIXO[i] == 14) for s in SLUGS_PSI] and portas[0] == 138, portas)
    for s in SLUGS_PSI: pg.evaluate(CLICA, ['tags', s])
    pg.wait_for_timeout(500)
    ok('as dez juntas alcançam 341 dos 440; os outros 99 só têm a psicologia geral', aba() == quantos(algum(*SLUGS_PSI), lambda i: EIXO[i] == 14) == 341, aba())
    limpar()

    print('D. A chave "qualquer um / todos"')
    marcador('filosofia'); marcador('introducao')
    F, I_, FI = quantos(tem('filosofia')), quantos(tem('introducao')), quantos(tem('filosofia', 'introducao'))
    ok('dois temas somam: filosofia ou introdução', aba() == F + I_ - FI == 437 and chave('Temas') == 'qualquer um', (aba(), chave('Temas')))
    pg.click('#f-tags .tg-g[data-g="1"] .tg-m [data-modo=e]'); pg.wait_for_timeout(500)
    ok('em "todos" cruzam: as introduções à filosofia', aba() == FI == 106 and chave('Temas') == 'todos' and ativos() == '(#filosofia e #introdução)', (aba(), ativos()))
    u = botao('umbanda')
    ok('em "todos" o número é o que sobra se o botão entrar', (botao('filosofia')['n'], botao('introducao')['n'], botao('ciencia')['n']) == (FI, FI, quantos(tem('filosofia', 'introducao', 'ciencia')))
       and u['n'] == quantos(tem('filosofia', 'introducao', 'umbanda')) == 0 and u['zero'], (botao('filosofia')['n'], botao('ciencia')['n'], u))
    marcador('cenario-russia'); marcador('cenario-nova-inglaterra')
    ok('a chave é de cada grupo: os cenários continuam somando', chave('Cenários') == 'qualquer um' and ativos() == '(#filosofia e #introdução) + (Cenário: Rússia ou Cenário: Nova Inglaterra)', ativos())
    pg.wait_for_timeout(600)
    ok('a escolha fica guardada com as preferências', pg.evaluate(GUARDADO).get('cruzar') == {'Temas': True}, pg.evaluate(GUARDADO))
    pg.reload(); pg.wait_for_timeout(1300); mais()
    ok('depois de recarregar: os filtros voltam vazios; a chave de "Temas" continua em "todos", e à vista', ativos() == '' and chave('Temas') == 'todos' and chave('Cenários') is None, (ativos(), chave('Temas')))
    marcador('filosofia')
    ok('com um tema ligado, os vizinhos já mostram o cruzamento', (botao('introducao')['n'], botao('ciencia')['n']) == (FI, quantos(tem('filosofia', 'ciencia'))) and botao('ciencia')['n'] == 18, (botao('introducao')['n'], botao('ciencia')['n']))
    pg.click('#f-tags .tg-g[data-g="1"] .tg-m [data-modo=ou]'); pg.wait_for_timeout(1000)
    ok('de volta a "qualquer um": os vizinhos mostram o que têm, e a chave some (só há um ligado)', (botao('introducao')['n'], botao('ciencia')['n']) == (I_, quantos(tem('ciencia'))) and chave('Temas') is None and pg.evaluate(GUARDADO).get('cruzar') == {},
       (botao('introducao')['n'], chave('Temas'), pg.evaluate(GUARDADO)))
    limpar()

    print('E. O quadro "Temas e camadas" das recomendações')
    ir('recs')
    pg.select_option('#p-temas select', label='Cenários'); pg.wait_for_timeout(600)
    fila = lambda t: quantos(tem(t), lambda i: not TENHO[i] and 'lido' not in MARCAS[i])
    antes = pg.evaluate(BARRAS)
    ok('as barras contam as recomendações ainda não lidas de cada cenário', len(antes) == 9 and all(n == fila(k) for k, n, _ in antes) and not any(s for _, _, s in antes), antes)
    pg.click(f'#p-temas .hb[data-k="{antes[0][0]}"]'); pg.wait_for_timeout(600)
    depois = pg.evaluate(BARRAS)
    ok('clicar numa barra filtra — e as outras continuam à vista, com os mesmos números', [x[:2] for x in depois] == [x[:2] for x in antes] and [x[2] for x in depois] == [True] + [False] * 8 and aba() == quantos(tem(antes[0][0]), de_fora), depois)
    pg.click(f'#p-temas .hb[data-k="{antes[1][0]}"]'); pg.wait_for_timeout(600)
    ok('a segunda barra soma', aba() == quantos(algum(antes[0][0], antes[1][0]), de_fora) and ' ou ' in ativos() and [x[2] for x in pg.evaluate(BARRAS)][:3] == [True, True, False], (aba(), ativos()))
    limpar()
    pg.select_option('#p-temas select', label='Psicologia: abordagens e áreas'); pg.wait_for_timeout(600)
    marcador('tcc'); marcador('psicanalise'); fecha()
    barras = {k: (n, s) for k, n, s in pg.evaluate(BARRAS)}
    ok('o grupo da psicologia está no quadro; marcador ligado que não acha nada fica à vista, com zero', barras.get('tcc') == (0, True) and barras.get('psicanalise') == (fila('psicanalise'), True) and barras.get('neurociencia') == (fila('neurociencia'), False), barras)
    pg.wait_for_timeout(500)
    ok('o grupo escolhido é guardado pelo nome', pg.evaluate(GUARDADO).get('temas') == 'Psicologia: abordagens e áreas', pg.evaluate(GUARDADO))
    limpar()

    print('F. Procurar marcador')
    mais()
    def procura(q): pg.fill('#f-tagq', q); pg.wait_for_timeout(300); return pg.evaluate(VISIVEIS)
    ok('"jung" acha a porta da psicologia analítica (está no nome curto e na explicação)', 'Analítica (Jung)' in procura('jung'), procura('jung'))
    ok('o nome completo acha o botão de nome curto: "psicologia social"', procura('psicologia social') == ['Social'], procura('psicologia social'))
    ok('a explicação também vale: "skinner" acha o behaviorismo, "opressivo" acha o clima claustrofóbico', procura('skinner') == ['Behaviorismo'] and procura('opressivo') == ['Claustrofóbico'], (procura('skinner'), procura('opressivo')))
    ok('procurar pelo número não acha nada (o número não é nome)', procura('152') == [], procura('152'))
    pg.fill('#f-tagq', ''); pg.wait_for_timeout(200)
    pg.context.close()

    print('G. O número do botão é o número da lista — seis telas, com os dados de exemplo')
    pg = abre(b, PAINEL_URL)
    sorteio = random.Random(8); erradas = []; conferidos = 0
    for v in ('geral', 'biblioteca', 'recs', 'financas', 'desejos', 'precos'):
        pg.click(f'#nav [data-ir={v}]'); pg.wait_for_timeout(700)
        total = pg.evaluate(ABA); todos = pg.evaluate(TODOS_BOTOES); eixos = pg.evaluate(OPCOES_EIXO)
        vivos = [c for c in todos if c['n']]; zeros = [c for c in todos if not c['n']]
        if not (total and vivos) or any(c['zero'] != (c['n'] == 0) for c in todos) or sum(e['n'] for e in eixos) != total: erradas.append((v, 'a tela', total, len(vivos)))
        for c in sorteio.sample(vivos, min(12, len(vivos))) + sorteio.sample(zeros, min(2, len(zeros))):
            pg.evaluate(CLICA, [c['g'], c['v']]); pg.wait_for_timeout(110)
            if pg.evaluate(ABA) != c['n']: erradas.append((v, c['v'], c['n'], pg.evaluate(ABA)))
            pg.evaluate(CLICA, [c['g'], c['v']]); pg.wait_for_timeout(50); conferidos += 1
        for e in sorteio.sample(eixos, 3):
            pg.evaluate(CLICA_EIXO, e['v']); pg.wait_for_timeout(110)
            if pg.evaluate(ABA) != e['n']: erradas.append((v, 'eixo', e, pg.evaluate(ABA)))
            pg.evaluate(CLICA_EIXO, e['v']); pg.wait_for_timeout(50); conferidos += 1
        # com um período escolhido os números acompanham
        pg.evaluate("() => document.querySelector('#f-periodo button[data-v=\"90d\"]').click()"); pg.wait_for_timeout(300)
        no_periodo = pg.evaluate(ABA); vivos = [c for c in pg.evaluate(TODOS_BOTOES) if c['n']]
        for c in sorteio.sample(vivos, min(3, len(vivos))):
            pg.evaluate(CLICA, [c['g'], c['v']]); pg.wait_for_timeout(110)
            if pg.evaluate(ABA) != c['n'] or c['n'] > no_periodo: erradas.append((v, '90 dias', c['v'], c['n'], pg.evaluate(ABA)))
            pg.evaluate(CLICA, [c['g'], c['v']]); pg.wait_for_timeout(50); conferidos += 1
        pg.evaluate("() => document.querySelector('#f-periodo button[data-v=\"tudo\"]').click()"); pg.wait_for_timeout(200)
    ok(f'{conferidos} botões clicados, um a um: a aba "Todos" mostra o número que o botão prometia', not erradas and conferidos > 90, erradas[:8])
    pg.context.close()

    print('H. Preferências guardadas pelo painel anterior, ou estragadas')
    pg = abre(b, PAINEL_LIMPO); pg.wait_for_timeout(700)
    troca = "ui => { const o = JSON.parse(localStorage.getItem('%s')); o.cfg.ui = ui; localStorage.setItem('%s', JSON.stringify(o)); }" % (CHAVE_DADOS, CHAVE_DADOS)
    def recarrega(ui): pg.wait_for_timeout(600); pg.evaluate(troca, ui); pg.reload(); pg.wait_for_timeout(1300)
    recarrega({'compor': 'fmt', 'temas': 4, 'prio': 'valor', 'sorteio': 0, 'trilhas': 'ordem'})      # como a rodada 7 guardava: a POSIÇÃO do grupo na lista
    pg.click('#nav [data-ir=recs]'); pg.wait_for_timeout(800)
    ok('quem tinha "Perguntas centrais" no quadro continua com ele (a lista ganhou um grupo no meio)', pg.evaluate(QUADRO) == 'Perguntas centrais', pg.evaluate(QUADRO))
    pg.click('#pw-mais .pop-b'); pg.wait_for_timeout(300)
    pg.click('#f-tags .chip[data-v="filosofia"]'); pg.click('#f-tags .chip[data-v="introducao"]'); pg.wait_for_timeout(500)
    ok('sem chave guardada, os grupos somam', pg.evaluate(CHAVE, 'Temas') == 'qualquer um' and ' ou ' in pg.evaluate(ATIVOS), pg.evaluate(ATIVOS))
    recarrega({'temas': 'Grupo que não existe', 'cruzar': {'Temas': 1, 'Cenários': True, 'Outro': True}})
    ok('preferência estragada não derruba o painel: vale só o que faz sentido', pg.evaluate(CHAVE, 'Cenários') == 'todos' and pg.evaluate(CHAVE, 'Temas') is None and pg.evaluate(QUADRO) == 'Temas', (pg.evaluate(CHAVE, 'Cenários'), pg.evaluate(CHAVE, 'Temas'), pg.evaluate(QUADRO)))
    recarrega({'cruzar': 'x', 'temas': None})
    ok('nem com os campos no formato errado', pg.evaluate(ABA) == len(CAT) - sum(TENHO) and pg.evaluate(QUADRO) == 'Temas' and pg.evaluate(CHAVE, 'Cenários') is None, pg.evaluate(ABA))
    pg.context.close()

    print('I. No celular')
    pg = abre(b, PAINEL_LIMPO, 390, 844)
    pg.click('#f-abrir'); pg.wait_for_timeout(500)
    for v in ('psicanalise', 'psicologia-analitica'): pg.click(f'#f-tags .chip[data-v="{v}"]'); pg.wait_for_timeout(350)
    geo = pg.evaluate("""() => { const r = e => e.getBoundingClientRect(), g = [...document.querySelectorAll('#f-tags .tg-g')].find(g => !g.querySelector('.tg-m').hidden), m = g.querySelector('.tg-m'), c = document.querySelector('#f-painel .f-corpo'), ch = g.querySelector('.chips');
        return { nome: g.querySelector('.pop-r').textContent, chave: [Math.round(r(m).left), Math.round(r(m).right)], limite: Math.round(r(ch).right - parseFloat(getComputedStyle(ch).paddingRight)), botoes: [...m.querySelectorAll('button')].map(b => Math.round(r(b).height)),
                 vaza: c.scrollWidth - c.clientWidth, fora: [...document.querySelectorAll('#pop-mais .chip, #f-regra')].filter(x => r(x).right > innerWidth + 0.5).length }; }""")
    ok('a chave fica à direita do nome do grupo, alinhada com os botões, e dá para tocar', geo['nome'].startswith('Psicologia') and geo['chave'][0] > 150 and geo['chave'][1] == geo['limite'] and min(geo['botoes']) >= 28, geo)
    ok('nada vaza para o lado: nem botão, nem a explicação', geo['vaza'] <= 0 and geo['fora'] == 0, geo)
    pg.click('#f-ver'); pg.wait_for_timeout(500)
    at = pg.evaluate("() => { const r = e => e.getBoundingClientRect(), g = document.querySelector('#f-ativos .fa-g'); return { txt: g.innerText.replace(/\\s+/g, ' '), esq: Math.round(r(g).left), dir: Math.round(r(g).right), rola: document.documentElement.scrollWidth - innerWidth }; }")
    ok('fechada a folha, os filtros ativos cabem na tela, com o "ou"', at['txt'] == '#psicanálise ou #psicologia analítica' and at['esq'] >= 0 and at['dir'] <= 390 and at['rola'] <= 0 and pg.evaluate(ABA) == quantos(algum('psicanalise', 'psicologia-analitica')) == 174, (at, pg.evaluate(ABA)))
    pg.screenshot(path=str(TMP / 'shots' / 'filtros-celular.png'))
    pg.context.close()

    print('J. Contraste do que é novo, nos dois temas')
    for tema, nome in (('light', 'claro'), ('dark', 'escuro')):
        pg = abre(b, PAINEL_LIMPO, tema=tema)
        pg.click('#nav [data-ir=recs]'); pg.wait_for_timeout(700); pg.click('#pw-mais .pop-b'); pg.wait_for_timeout(300)
        for v in ('cenario-russia', 'cenario-nova-inglaterra'): pg.click(f'#f-tags .chip[data-v="{v}"]'); pg.wait_for_timeout(350)
        c = pg.evaluate(CONTRASTE)
        ok(f'tema {nome}: botão apagado, números, "ou" e explicação com contraste de pelo menos 4,5', all(v is not None and v >= 4.5 for v in c.values()), c)
        pg.screenshot(path=str(TMP / 'shots' / f'filtros-{nome}.png'))
        pg.context.close()
    b.close()

print('FALHAS:', falhas); print('ERROS:', len(errs) + len(falhas)); [print('  ', x[:300]) for x in errs[:10]]
