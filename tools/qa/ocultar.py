"""Ocultar: tirar de todas as telas os livros de uma categoria — o contrário de um filtro, e fica guardado.

É a parte 1 da etapa 10 do roteiro. Confere que:
  A. de início nada está oculto: não há aviso, e os números são os de sempre;
  B. o quadro "Ocultar" — ao lado de cada opção (3 situações, 4 tipos, 16 eixos) vai quantos livros ela esconde, e o
     número bate com o catálogo (contado aqui, por fora do painel);
  C. "Sem edição em PT" — os livros saem da tabela, das abas, dos números dos filtros, da fila de recomendações, da ordem
     de compra e da trilha de que um deles faz parte; o aviso sob a barra e o rodapé dizem quantos são; a busca rápida
     ainda acha o livro, e a ficha diz por que ele está fora das listas;
  D. a escolha fica guardada: resiste à recarga e vale em todas as telas; e o número de cada botão de filtro continua
     sendo o tamanho da lista;
  E. "Já li" — os lidos saem das listas, mas continuam contando nas leituras concluídas e no andamento da trilha; com os
     dados de exemplo, os indicadores de leitura da Biblioteca não mudam;
  F. tipo, eixo e marcador — cada um esconde o que diz; o marcador é achado pela busca do quadro;
  G. regras juntas escondem a união (um livro que cai em duas conta uma vez);
  H. "mostrar todos" traz tudo de volta e limpa o que estava guardado; "mudar" abre o quadro;
  I. a barra — em 1366 px, com os três números ligados, continua numa linha só, e o quadro não sai da janela (em 1100 px,
     onde a barra já quebra em duas linhas, o quadro também fica dentro);
  J. no celular — o atalho no topo da folha de filtros leva às opções, e o aviso cabe na tela;
  K. o que estava guardado de um jeito que o painel não entende não o impede de abrir, e só valem as regras que existem;
  L. o que é novo tem contraste AA nos dois temas.

O que se espera é contado aqui, direto de src/catalog.json e src/trilhas.json.
"""
import json, random
from caminhos import PAINEL_LIMPO, PAINEL_URL, RAIZ, TMP
from relogio import fixa
from playwright.sync_api import sync_playwright

CHAVE_DADOS = 'biblioteca-lucas:v1'
errs = []; falhas = []

# ── o catálogo, lido por fora do painel: [título, autor, "marcadores", seção, eixo, …] ──
CAT = json.loads((RAIZ / 'src' / 'catalog.json').read_text(encoding='utf-8'))
TRILHAS = json.loads((RAIZ / 'src' / 'trilhas.json').read_text(encoding='utf-8'))      # [marcador, nome, descrição, [posições]]
MARCAS = [set(r[2].split()) for r in CAT]
TENHO = [bool(m & {'tenho-fisico', 'tenho-digital', 'ja-tenho'}) for m in MARCAS]
EIXO = [r[4] for r in CAT]
N = len(CAT)
tipo = lambda m: 'F' if 'F' in m else 'NF' if 'NF' in m else 'O' if 'poesia' in m else 'HQ' if 'HQ' in m else 'O'      # o filtro "Tipo" do painel
TIPO = [tipo(m) for m in MARCAS]
SIT = {'lido': 'lido', 'sem-pt': 'sem-pt', 'verificar': 'verificar'}                  # situação → marcador do catálogo (no painel limpo, "já li" é o #lido)


def fora(sit=(), tipos=(), eixos=(), tags=()):
    """Os livros (posições no catálogo) que um conjunto de regras esconde: basta cair em uma."""
    return {i for i in range(N) if any(SIT[s] in MARCAS[i] for s in sit) or TIPO[i] in tipos or EIXO[i] in eixos or any(t in MARCAS[i] for t in tags)}


# ── o que se lê da tela ──
num = "s => +String(s).replace(/\\./g, '')"
ABA = "a => { const t = document.querySelector(`.visao:not([hidden]) .card-tab .abas [data-a=${a || 'todos'}] .cont`); return t ? +t.textContent.replace(/\\./g, '') : null; }"
KPI = "k => { const e = document.querySelector(`.visao:not([hidden]) .kpi[data-k=${k}]`); return { v: e.querySelector('.kpi-v b').textContent, s: e.querySelector('.kpi-s').textContent }; }"
AVISO = "() => { const e = document.querySelector('#f-fora'); return e.hidden ? null : { n: e.querySelector('b').textContent, r: e.querySelector('.ff-r').textContent, bts: [...e.querySelectorAll('button')].map(b => b.textContent) }; }"
OPCOES = "() => [...document.querySelectorAll('#pop-fora input[data-fora]')].map(i => [i.dataset.fora, i.value, +i.parentElement.querySelector('em').textContent.replace(/\\./g, ''), i.checked])"
SELO = "() => { const c = document.querySelector('#pw-fora .cont'); return c.hidden ? 0 : +c.textContent; }"
GUARDADO = "() => ((JSON.parse(localStorage.getItem('%s') || '{}').cfg || {}).ui || {}).fora" % CHAVE_DADOS
RODAPE = "() => document.querySelector('#rodape-n').textContent"
BOTOES_FILTRO = "() => [...document.querySelectorAll('#pop-mais .chip')].map(c => ({ g: c.parentElement.dataset.grupo, v: c.dataset.v, n: +c.dataset.n }))"
OPCAO_EIXO = "v => { const o = document.querySelector(`#pop-eixo input[value=\"${v}\"]`).parentElement; return { n: +o.querySelector('em').textContent.replace(/\\./g, ''), zero: o.classList.contains('zero') }; }"
TRILHA_PAINEL = "t => { const b = document.querySelector(`#p-trilhas [data-trilha=\"${t}\"]`); return b ? b.querySelector('.li-m span').textContent : null; }"
TRILHA_CAIXA = "() => { const d = document.querySelector('#dlg.on'); return d ? { frase: d.querySelector('.tr-res b').textContent, livros: [...d.querySelectorAll('.tr-l li .li-m b')].map(b => b.textContent), nota: (d.querySelector('.tr-fora') || {}).textContent || '' } : null; }"
# contraste (WCAG) do texto de um elemento contra o fundo que de fato fica atrás dele; a cor é lida pintando um ponto
CONTRASTE = """sels => {
  const cv = document.createElement('canvas'); cv.width = cv.height = 1; const cx = cv.getContext('2d', { willReadFrequently: true });
  const rgba = s => { cx.clearRect(0, 0, 1, 1); cx.fillStyle = '#000'; cx.fillStyle = s; cx.fillRect(0, 0, 1, 1); const d = cx.getImageData(0, 0, 1, 1).data; return [d[0], d[1], d[2], d[3] / 255]; };
  const lum = c => { const [r, g, b] = c.map(v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }); return 0.2126 * r + 0.7152 * g + 0.0722 * b; };
  const fundo = e => { const pilha = []; for (let x = e; x; x = x.parentElement) { const c = rgba(getComputedStyle(x).backgroundColor); if (c[3] > 0) { pilha.push(c); if (c[3] >= 1) break; } }
    let base = [255, 255, 255]; for (const c of pilha.reverse()) base = base.map((v, i) => c[i] * c[3] + v * (1 - c[3])); return base; };
  const razao = e => { const f = fundo(e), t = rgba(getComputedStyle(e).color), cor = [0, 1, 2].map(i => t[i] * t[3] + f[i] * (1 - t[3])), a = lum(cor), b = lum(f); return +((Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05)).toFixed(2); };
  return Object.fromEntries(Object.entries(sels).map(([n, s]) => { const e = document.querySelector(s); return [n, e ? razao(e) : null]; })); }"""


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


plural = lambda n: f'{n:,}'.replace(',', '.') + (' livro oculto' if n == 1 else ' livros ocultos')

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = abre(b, PAINEL_LIMPO)

    def fecha(): pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
    def ir(v): fecha(); pg.click(f'#nav [data-ir={v}]'); pg.wait_for_timeout(900)
    def quadro():                                                                              # abre "Ocultar" (se já estiver aberto, deixa)
        if not pg.evaluate("() => document.querySelector('#pw-fora').classList.contains('aberto')"): pg.click('#pw-fora .pop-b'); pg.wait_for_timeout(300)
    def marca(g, v, liga=True): quadro(); pg.set_checked(f'#pop-fora input[data-fora={g}][value="{v}"]', liga); pg.wait_for_timeout(500)
    aba = lambda a='todos': pg.evaluate(ABA, a)
    aviso = lambda: pg.evaluate(AVISO)
    guardado = lambda: (pg.wait_for_timeout(500), pg.evaluate(GUARDADO))[1]

    print('A. De início, nada oculto')
    ok('não há aviso nem número no botão, e a tabela mostra o catálogo inteiro', aviso() is None and pg.evaluate(SELO) == 0 and aba() == N, (aviso(), aba()))
    ok('o rodapé não fala em ocultos', 'oculto' not in pg.evaluate(RODAPE), pg.evaluate(RODAPE))

    print('B. O quadro: cada opção com o número de livros que esconde')
    quadro()
    ops = pg.evaluate(OPCOES)
    espera = [['sit', s, len(fora(sit=[s])), False] for s in ('lido', 'sem-pt', 'verificar')] + [['tipo', t, len(fora(tipos=[t])), False] for t in ('F', 'NF', 'HQ', 'O')] + [['eixo', str(e), len(fora(eixos=[e])), False] for e in range(1, 17)]
    ok('3 situações, 4 tipos e 16 eixos, nada marcado, e os números batem com o catálogo', ops == espera, [x for x in ops if x not in espera][:4] or len(ops))
    ok('os quatro tipos somam o catálogo inteiro', sum(x[2] for x in ops if x[0] == 'tipo') == N, [x[2] for x in ops if x[0] == 'tipo'])
    pg.screenshot(path=str(TMP / 'shots' / 'ocultar-quadro.png'))

    print('C. "Sem edição em PT"')
    sp = fora(sit=['sem-pt']); n_sp = len(sp)
    marca('sit', 'sem-pt'); fecha()
    a = aviso()
    ok(f'o aviso diz quantos são ({n_sp}) e por quê, com "mudar" e "mostrar todos"', a == {'n': plural(n_sp), 'r': 'sem edição em PT', 'bts': ['mudar', 'mostrar todos']}, a)
    ok('o botão "Ocultar" ganha o número de regras ligadas, e o rodapé repete a conta', pg.evaluate(SELO) == 1 and f'· {n_sp} ocultos ·' in pg.evaluate(RODAPE), (pg.evaluate(SELO), pg.evaluate(RODAPE)))
    ok('saem da tabela da visão geral', aba() == N - n_sp, aba())
    pg.fill('#p-tab-geral input[type=search]', CAT[min(sp)][0]); pg.wait_for_timeout(500)
    ok('procurado pelo título na tabela, o livro não aparece', aba() == 0, (CAT[min(sp)][0], aba()))
    pg.fill('#p-tab-geral input[type=search]', ''); pg.wait_for_timeout(400)
    ir('recs')
    fila = sum(1 for i in range(N) if not TENHO[i] and 'lido' not in MARCAS[i] and i not in sp)
    ok('nas recomendações: fora da tabela, a aba "Sem edição em PT" zera', aba() == sum(1 for i in range(N) if not TENHO[i] and i not in sp) and aba('sempt') == 0, (aba(), aba('sempt')))
    k = pg.evaluate(KPI, 'recs'); oc = pg.inner_text('#p-compra .oc-n')
    ok('a fila de recomendações e a ordem de compra deixam de contá-los', pg.evaluate(num, k['v']) == fila and oc.startswith(f'{fila} recomendações por comprar'), (k['v'], oc, fila))
    pg.click('#pw-mais .pop-b'); pg.wait_for_timeout(300)
    bt = next(x for x in pg.evaluate(BOTOES_FILTRO) if x['v'] == 'sem-pt')
    ok('o botão de filtro "Sem edição em PT" passa a mostrar zero', bt['n'] == 0, bt); fecha()
    tr = next(t for t in TRILHAS if any(i in sp for i in t[3])); some = [CAT[i][0] for i in tr[3] if i in sp]; ficam = len(tr[3]) - len(some)
    frase = pg.evaluate(TRILHA_PAINEL, tr[0])
    ok(f'a trilha "{tr[1].split(":")[0]}" passa a ter {ficam} livros e avisa: {len(some)} oculto', frase is not None and f' de {ficam}' in frase and frase.endswith(f'{len(some)} oculto' + ('s' if len(some) > 1 else '')), frase)
    pg.click(f'#p-trilhas [data-trilha="{tr[0]}"]'); pg.wait_for_timeout(500)
    cx = pg.evaluate(TRILHA_CAIXA)
    ok('aberta, a trilha não lista o livro oculto e diz que há um fora', cx and len(cx['livros']) == ficam and not set(some) & set(cx['livros']) and 'você pediu para ocultar' in cx['nota'], cx and (len(cx['livros']), cx['nota'][:70]))
    pg.click('#dlg header [data-fechar]'); pg.wait_for_timeout(300)
    pg.fill('#q', some[0][:22]); pg.wait_for_timeout(500)
    achado = pg.inner_text('#q-r .qr >> nth=0')
    ok('a busca rápida ainda acha o livro, e avisa que ele está fora das listas', some[0][:22] in achado and 'fora das listas (oculto)' in achado, achado.replace('\n', ' | '))
    pg.click('#q-r .qr >> nth=0'); pg.wait_for_timeout(600)
    ficha = pg.inner_text('#gaveta.on .gv-fora') if pg.is_visible('#gaveta.on .gv-fora') else ''
    ok('a ficha abre e diz por que ele não aparece nas listas', ficha == 'Fora das listas: você pediu para ocultar sem edição em PT.', ficha)
    pg.screenshot(path=str(TMP / 'shots' / 'ocultar-ficha.png'))
    pg.click('#gaveta .gv-h [data-fechar]'); pg.wait_for_timeout(300)

    print('D. Fica guardado, vale em todas as telas, e os números dos filtros seguem a lista')
    g = guardado()
    ok('a escolha está guardada no navegador', g == {'sit': ['sem-pt'], 'tipo': [], 'eixo': [], 'tag': []}, g)
    pg.reload(); pg.wait_for_timeout(1300)
    ok('depois de recarregar, continua oculto (a tela das recomendações, a mesma conta)', aviso() and aviso()['n'] == plural(n_sp) and aba() == sum(1 for i in range(N) if not TENHO[i] and i not in sp), (aviso(), aba()))
    vistas = {}
    for v in ('geral', 'biblioteca', 'recs', 'financas', 'desejos', 'precos'):
        ir(v); vistas[v] = bool(aviso())
    ok('o aviso aparece nas seis telas', all(vistas.values()), vistas)
    sorte = random.Random(10)
    for v in ('geral', 'recs'):
        ir(v); pg.click('#pw-mais .pop-b'); pg.wait_for_timeout(300)
        bts = [x for x in pg.evaluate(BOTOES_FILTRO) if x['g'] == 'tags']; erro = []
        for x in sorte.sample(bts, 14):
            pg.evaluate("v => document.querySelector(`#f-tags .chip[data-v=\"${v}\"]`).click()", x['v']); pg.wait_for_timeout(260)
            if aba() != x['n']: erro.append((x['v'], x['n'], aba()))
            pg.evaluate("v => document.querySelector(`#f-tags .chip[data-v=\"${v}\"]`).click()", x['v']); pg.wait_for_timeout(160)
        ok(f'{v}: com livros ocultos, o número de 14 botões de filtro sorteados é o tamanho da lista depois do clique', not erro, erro[:4])
        fecha()

    print('E. "Já li": some das listas, continua contando nas leituras')
    ir('geral'); marca('sit', 'sem-pt', False); marca('sit', 'lido'); fecha()
    li = fora(sit=['lido']); n_li = len(li)
    pg.wait_for_timeout(700)
    k = pg.evaluate(KPI, 'leituras')
    ok(f'os {n_li} lidos saem da tabela, e o aviso diz "já li"', aba() == N - n_li and aviso() == {'n': plural(n_li), 'r': 'já li', 'bts': ['mudar', 'mostrar todos']}, (aba(), aviso()))
    ok('"Leituras concluídas" continua contando os que estão ocultos', pg.evaluate(num, k['v']) == n_li and k['s'].endswith(f'{sum(1 for i in li if not TENHO[i])} de fora'), k)
    nota = pg.inner_text('#p-lendo-geral .li-fora') if pg.is_visible('#p-lendo-geral .li-fora') else ''
    ok('"Na cabeceira" não lista as leituras ocultas e diz quantas são', nota.startswith(f'{n_li} leituras concluídas estão ocultas') and pg.locator('#p-lendo-geral .li[data-id]').count() == 0, nota)
    ir('recs')
    ok('nas recomendações, a aba "Já lidas" zera', aba('lidos') == 0, aba('lidos'))
    tr = next(t for t in TRILHAS if any(i in li for i in t[3])); lidos = [CAT[i][0] for i in tr[3] if i in li]
    frase = pg.evaluate(TRILHA_PAINEL, tr[0])
    ok(f'a trilha "{tr[1].split(":")[0]}" continua com {len(tr[3])} livros e o lido contado; só avisa que há um oculto', frase and f' de {len(tr[3])}' in frase and f'li {len(lidos)}' in frase and frase.endswith(f'{len(lidos)} oculto'), frase)
    pg.click(f'#p-trilhas [data-trilha="{tr[0]}"]'); pg.wait_for_timeout(500)
    cx = pg.evaluate(TRILHA_CAIXA)
    ok('aberta, ela não lista o livro lido, mas a frase do andamento o conta', cx and len(cx['livros']) == len(tr[3]) - len(lidos) and not set(lidos) & set(cx['livros']) and f'li {len(lidos)}' in cx['frase'], cx and (len(cx['livros']), cx['frase']))
    pg.click('#dlg header [data-fechar]'); pg.wait_for_timeout(300)
    pg.context.close()

    pg = abre(b, PAINEL_URL)                                             # com os dados de exemplo: dezenas de leituras, no acervo e de fora
    ir('biblioteca')
    antes = {x: pg.evaluate(KPI, x) for x in ('leituras', 'fila', 'lendo')}; lidos0, todos0 = aba('lido'), aba()
    marca('sit', 'lido'); fecha(); pg.wait_for_timeout(900)
    depois = {x: pg.evaluate(KPI, x) for x in ('leituras', 'fila', 'lendo')}
    ok('dados de exemplo: os lidos do acervo saem da tabela da Biblioteca', lidos0 > 20 and aba('lido') == 0 and aba() == todos0 - lidos0, (lidos0, todos0, aba('lido'), aba()))
    ok('…e os indicadores de leitura ("Leituras concluídas", "Por ler", "Lendo agora") não mudam', antes == depois, (antes, depois))
    acervo = pg.evaluate(KPI, 'acervo')
    ok('…enquanto "Livros no acervo" passa a contar só o que está à vista', pg.evaluate(num, acervo['v']) == todos0 - lidos0, acervo)
    pg.context.close()

    print('F. Tipo, eixo e marcador')
    pg = abre(b, PAINEL_LIMPO)
    hq = fora(tipos=['HQ'])
    marca('tipo', 'HQ'); fecha()
    ok(f'tipo HQ: {len(hq)} livros saem, e o aviso diz "HQ"', aba() == N - len(hq) and aviso() == {'n': plural(len(hq)), 'r': 'HQ', 'bts': ['mudar', 'mostrar todos']}, (aba(), aviso()))
    pg.click('#f-tipo button[data-v=HQ]'); pg.wait_for_timeout(500)
    ok('filtrando por HQ, não sobra nada', aba() == 0, aba())
    pg.click('#f-tipo button[data-v=""]'); pg.wait_for_timeout(400)
    marca('tipo', 'HQ', False)
    e14 = fora(eixos=[14]); marca('eixo', '14'); fecha()
    ok(f'eixo "Psicologia e psicanálise": {len(e14)} livros saem, e o aviso traz o nome do eixo', aba() == N - len(e14) and aviso()['r'] == 'Psicologia e psicanálise', (aba(), aviso()))
    pg.click('#pw-eixo .pop-b'); pg.wait_for_timeout(300); oe = pg.evaluate(OPCAO_EIXO, 14); fecha()
    ok('no filtro "Eixo", a opção desse eixo fica com zero e apagada', oe == {'n': 0, 'zero': True}, oe)
    marca('eixo', '14', False)
    pg.fill('#fo-tagq', 'lovecraft'); pg.wait_for_timeout(350)
    achados = pg.evaluate("() => [...document.querySelectorAll('#fo-tags .chip')].map(c => [c.dataset.v, c.querySelector('span').textContent, +c.querySelector('em').textContent, c.getAttribute('aria-pressed')])")
    alvo = next((x for x in achados if x[1] == 'Lovecraftiano'), None)
    ok('a busca do quadro acha o marcador pelo nome, com o número de livros', alvo is not None and alvo[2] == len(fora(tags=[alvo[0]])) and alvo[3] == 'false' and len(achados) >= 2, achados)
    dentro = pg.evaluate("() => { const c = document.querySelector('#fo-tags .chip').getBoundingClientRect(), q = document.querySelector('#pop-fora').getBoundingClientRect(); return c.top >= q.top && c.bottom <= q.bottom; }")
    ok('o que a busca achou fica à vista dentro do quadro', dentro)
    lv = fora(tags=[alvo[0]])
    pg.click(f'#fo-tags .chip[data-v="{alvo[0]}"]'); pg.wait_for_timeout(500)
    pg.fill('#fo-tagq', ''); pg.wait_for_timeout(300)
    ch = pg.evaluate("() => [...document.querySelectorAll('#fo-tags .chip')].map(c => [c.dataset.v, c.getAttribute('aria-pressed')])")
    ok('o marcador oculto continua à vista no quadro depois de apagar a busca', ch == [[alvo[0], 'true']], ch)
    fecha()
    ok(f'marcador: {len(lv)} livros saem, e o aviso traz o marcador', aba() == N - len(lv) and aviso() == {'n': plural(len(lv)), 'r': '#lovecraftiano', 'bts': ['mudar', 'mostrar todos']}, (aba(), aviso()))

    print('G. Regras juntas escondem a união')
    marca('sit', 'sem-pt'); marca('tipo', 'HQ'); marca('eixo', '14'); fecha()
    uniao = fora(sit=['sem-pt'], tipos=['HQ'], eixos=[14], tags=[alvo[0]]); soma = n_sp + len(hq) + len(e14) + len(lv)
    a = aviso()
    ok(f'quatro regras: {len(uniao)} livros (a soma simples daria {soma})', len(uniao) < soma and aba() == N - len(uniao) and a['n'] == plural(len(uniao)) and pg.evaluate(SELO) == 4, (aba(), a, pg.evaluate(SELO)))
    ok('o aviso lista as quatro, na ordem do quadro', a['r'] == 'sem edição em PT · HQ · Psicologia e psicanálise · #lovecraftiano', a['r'])
    pg.screenshot(path=str(TMP / 'shots' / 'ocultar-aviso.png'))

    print('H. "mostrar todos" e "mudar"')
    pg.click('#f-fora [data-fora-abrir]'); pg.wait_for_timeout(350)
    ok('"mudar" abre o quadro "Ocultar"', pg.evaluate("() => document.querySelector('#pw-fora').classList.contains('aberto')") and pg.is_visible('#pop-fora'))
    fecha()
    pg.click('#f-fora [data-fora-limpar]'); pg.wait_for_timeout(600)
    recado = pg.inner_text('#toasts') if pg.locator('#toasts .toast').count() else ''
    ok('"mostrar todos": o aviso some, a tabela volta ao catálogo inteiro e o painel confirma', aviso() is None and aba() == N and pg.evaluate(SELO) == 0 and 'Nada mais está oculto.' in recado, (aviso(), aba(), recado))
    g = guardado()
    ok('e o que estava guardado é limpo', g == {'sit': [], 'tipo': [], 'eixo': [], 'tag': []}, g)
    quadro()
    ok('no quadro, nada fica marcado', not [x for x in pg.evaluate(OPCOES) if x[3]] and pg.locator('#fo-tags .chip').count() == 0)
    pg.context.close()

    print('I. A barra de filtros')
    LINHA = "() => { const r = e => e.getBoundingClientRect(), gs = [...document.querySelectorAll('.f-corpo > .f-g')].filter(e => e.offsetWidth), q = r(document.querySelector('#pop-fora')); return { topos: [...new Set(gs.map(e => Math.round(r(e).top)))], selos: [...document.querySelectorAll('.f-corpo .pop-b .cont')].filter(c => !c.hidden).length, quadro: [Math.round(q.left), Math.round(q.top), Math.round(q.right), Math.round(q.bottom)], jan: [innerWidth, innerHeight], esq: Math.round(r(document.querySelector('.f-corpo > .f-g')).left), rot: getComputedStyle(document.querySelector('.fo-rot')).display }; }"
    for larg, alt in ((1366, 700), (1536, 745), (1100, 700)):
        pg = abre(b, PAINEL_LIMPO, largura=larg, altura=alt)
        pg.click('#pw-eixo .pop-b'); pg.wait_for_timeout(250); pg.click('#pop-eixo input[value="7"]'); pg.wait_for_timeout(300); fecha()
        pg.click('#pw-mais .pop-b'); pg.wait_for_timeout(250); pg.click('#f-tags .chip[data-v="horror"]'); pg.wait_for_timeout(300); fecha()
        quadro(); pg.check('#pop-fora input[data-fora=sit][value="sem-pt"]'); pg.wait_for_timeout(400)
        m = pg.evaluate(LINHA)
        cabe = m['quadro'][0] >= m['esq'] - 1 and m['quadro'][2] <= m['jan'][0] and m['quadro'][1] >= 0 and m['quadro'][3] <= m['jan'][1]
        if larg >= 1366: ok(f'{larg} px: com os três números ligados, os cinco controles ficam numa linha, e o quadro dentro da janela', len(m['topos']) == 1 and m['selos'] == 3 and cabe, m)
        else: ok(f'{larg} px: a barra já quebra em duas linhas, e o quadro continua dentro da janela', m['selos'] == 3 and cabe, m)
        ok(f'{larg} px: o botão {"mostra o nome" if larg >= 1440 else "fica só com o ícone"}, e o nome vai sempre para o leitor de tela', (m['rot'] != 'none') == (larg >= 1440) and pg.get_attribute('#pw-fora .pop-b', 'aria-label') == 'Ocultar livros', m['rot'])
        try: pg.check('#pop-fora input[data-fora=sit][value=lido]', timeout=3000); clicou = True
        except Exception as e: clicou = False; print('     ', str(e).splitlines()[0][:160])
        ok(f'{larg} px: com o quadro aberto e uma regra já ligada, a opção seguinte aceita o clique', clicou)
        pg.context.close()

    print('J. No celular')
    pg = abre(b, PAINEL_LIMPO, largura=390, altura=800)
    pg.click('#f-abrir'); pg.wait_for_timeout(500)
    pg.click('.f-ph [data-fora-abrir]'); pg.wait_for_timeout(500)
    geo = pg.evaluate("() => { const r = e => e.getBoundingClientRect(), c = r(document.querySelector('.f-corpo')), w = r(document.querySelector('#pw-fora')); return { topo: Math.round(w.top - c.top), vaza: Math.max(...[...document.querySelectorAll('#pw-fora *')].filter(e => e.offsetWidth).map(e => Math.round(r(e).right))) - innerWidth, opcoes: [...document.querySelectorAll('#pop-fora .opt')].filter(o => r(o).height >= 30).length }; }")
    ok('o atalho "ocultar categorias", no topo da folha, leva às opções', 0 <= geo['topo'] <= 40, geo)
    ok('na folha, nada vaza para o lado, e cada opção tem altura para o dedo', geo['vaza'] <= 0 and geo['opcoes'] == 23, geo)
    pg.check('#pop-fora input[data-fora=sit][value="sem-pt"]'); pg.wait_for_timeout(400)
    pg.screenshot(path=str(TMP / 'shots' / 'ocultar-celular-folha.png'))
    pg.click('#f-ver'); pg.wait_for_timeout(500)
    at = pg.evaluate("() => { const r = document.querySelector('#f-fora').getBoundingClientRect(); return { esq: Math.round(r.left), dir: Math.round(r.right), rola: document.documentElement.scrollWidth - innerWidth, bts: [...document.querySelectorAll('#f-fora button')].map(b => Math.round(b.getBoundingClientRect().height)) }; }")
    ok('fechada a folha, o aviso cabe na tela', aviso() and aviso()['n'] == plural(n_sp) and at['esq'] >= 0 and at['dir'] <= 390 and at['rola'] <= 0, (aviso(), at))
    pg.screenshot(path=str(TMP / 'shots' / 'ocultar-celular.png'))
    pg.click('#f-fora [data-fora-abrir]'); pg.wait_for_timeout(600)
    volta = pg.evaluate("() => { const c = document.querySelector('.f-corpo').getBoundingClientRect(), w = document.querySelector('#pw-fora').getBoundingClientRect(); return { folha: document.querySelector('#filtros').classList.contains('folha'), topo: Math.round(w.top - c.top) }; }")
    ok('"mudar", no aviso, abre a folha de filtros já nas opções de ocultar', volta['folha'] and 0 <= volta['topo'] <= 40, volta)
    pg.click('#pop-fora [data-fora-limpar]'); pg.wait_for_timeout(500); pg.click('#f-ver'); pg.wait_for_timeout(400)
    ok('"mostrar tudo", na folha, desfaz', aviso() is None and aba() == N, (aviso(), aba()))
    pg.context.close()

    print('K. O que veio guardado de um jeito estranho')
    pg = abre(b, PAINEL_LIMPO)
    marca('sit', 'verificar'); fecha(); pg.wait_for_timeout(600)                              # só para haver dados guardados
    POE = "v => { const o = JSON.parse(localStorage.getItem('%s')); o.cfg.ui.fora = v; localStorage.setItem('%s', JSON.stringify(o)); }" % (CHAVE_DADOS, CHAVE_DADOS)
    for nome, v in (('um texto', 'tudo'), ('um número', 7), ('uma lista', ['lido']), ('nada', None), ('listas que não são listas', {'sit': 'lido', 'tipo': 3, 'eixo': {'a': 1}, 'tag': None})):
        n0 = len(errs); pg.evaluate(POE, v); pg.reload(); pg.wait_for_timeout(1200)
        ok(f'guardado como {nome}: o painel abre, sem erro e sem nada oculto', len(errs) == n0 and aviso() is None and aba() == N, (errs[n0:][:2], aviso(), aba()))
    n0 = len(errs)
    pg.evaluate(POE, {'sit': ['lido', 'não-existe', 'lido'], 'tipo': ['HQ', 'ZZ', 3], 'eixo': [14, 99, '3', 2.5, 0], 'tag': ['x' * 100, alvo[0], '', 7], 'outra': [1]}); pg.reload(); pg.wait_for_timeout(1200)
    valem = fora(sit=['lido'], tipos=['HQ'], eixos=[14], tags=[alvo[0]])
    quadro(); marcadas = [x[:2] for x in pg.evaluate(OPCOES) if x[3]]
    ok('regras de verdade misturadas com lixo: só as de verdade valem', len(errs) == n0 and aviso() and aviso()['n'] == plural(len(valem)) and marcadas == [['sit', 'lido'], ['tipo', 'HQ'], ['eixo', '14']] and pg.evaluate(SELO) == 4, (errs[n0:][:2], aviso(), marcadas))
    pg.context.close()

    print('L. Contraste do que é novo, nos dois temas')
    ALVOS = {'aviso: quantos': '#f-fora b', 'aviso: por quê': '#f-fora .ff-r', 'aviso: mudar': '#f-fora .lk', 'quadro: explicação': '#pop-fora .fo-n', 'quadro: opção': '#pop-fora .opt span', 'quadro: número': '#pop-fora .opt em',
             'quadro: "mostrar tudo"': '#pop-fora .pop-h .lk', 'quadro: marcador oculto': '#fo-tags .chip[aria-pressed=true] span', 'quadro: marcador achado': '#fo-tags .chip[aria-pressed=false] span', 'quadro: número do achado': '#fo-tags .chip[aria-pressed=false] em',
             'quadro: recado da busca': '#fo-tags-n', 'cabeceira: leituras ocultas': '#p-lendo-geral .li-fora span', 'ficha: fora das listas': '#gaveta .gv-fora span'}
    for tema, nome in (('light', 'claro'), ('dark', 'escuro')):
        pg = abre(b, PAINEL_LIMPO, tema=tema)
        marca('sit', 'lido'); marca('sit', 'sem-pt')
        pg.fill('#fo-tagq', 'lovecraft'); pg.wait_for_timeout(300); pg.click(f'#fo-tags .chip[data-v="{alvo[0]}"]'); pg.wait_for_timeout(400)
        pg.fill('#fo-tagq', 'qqq'); pg.wait_for_timeout(300); c1 = pg.evaluate(CONTRASTE, {'quadro: recado da busca': ALVOS['quadro: recado da busca']})
        pg.fill('#fo-tagq', 'lovecraft'); pg.wait_for_timeout(300)
        c = pg.evaluate(CONTRASTE, {k: v for k, v in ALVOS.items() if not k.startswith(('ficha', 'quadro: recado'))}); c.update(c1)
        pg.screenshot(path=str(TMP / 'shots' / f'ocultar-{nome}.png'))
        fecha(); pg.fill('#q', CAT[min(sp)][0][:22]); pg.wait_for_timeout(500); pg.click('#q-r .qr >> nth=0'); pg.wait_for_timeout(600)
        c.update(pg.evaluate(CONTRASTE, {'ficha: fora das listas': ALVOS['ficha: fora das listas']}))
        ok(f'tema {nome}: o aviso, o quadro e os recados com contraste de pelo menos 4,5', all(v is not None and v >= 4.5 for v in c.values()), c)
        pg.context.close()
    b.close()

print('FALHAS:', falhas); print('ERROS:', len(errs) + len(falhas)); [print('  ', x[:300]) for x in errs[:10]]
