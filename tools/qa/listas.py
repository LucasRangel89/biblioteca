"""Listas para levar: "Imprimir" e "Copiar", nas tabelas e nas trilhas de leitura.

É a parte 2 da etapa 10 do roteiro. Confere que:
  A. os botões — nas seis tabelas há "Imprimir", "Copiar" e "CSV", nessa ordem, cada um com nome para o leitor de tela;
  B. a folha é a lista da tela — com um filtro ligado, a folha traz as mesmas linhas da tabela (todas as páginas dela), na
     mesma ordem; o cabeçalho diz o nome da lista, quantos livros são, a ordem, os filtros e a data; e acompanha a aba, a
     busca e a ordem escolhidas;
  C. no papel — só a folha aparece; é preta no branco mesmo no tema escuro; o cabeçalho da tabela se repete e nenhuma linha
     é cortada entre páginas; com uma caixa aberta (a página travada) a folha não sai cortada; o PDF de verdade tem o
     número de páginas que o painel estimou;
  D. depois de imprimir, a página volta a ser a de sempre — também quando o navegador não avisa que a impressão acabou;
     e, quando o navegador recusa o pedido (ele recusa pedidos muito seguidos, sem avisar a página), o painel avisa;
  E. lista longa — o painel diz quantas páginas são e pergunta; "Cancelar" não imprime; "Imprimir assim mesmo" imprime tudo;
  F. lista vazia — avisa e não imprime nem copia;
  G. as marcas — o livro lido sai com o quadradinho marcado e a prioridade com a estrela, os dois desenhados (não dependem
     da fonte), com a legenda embaixo;
  H. dinheiro — Finanças e Próximas aquisições levam os valores; com o olho fechado, nenhum valor vai para o papel;
  I. ocultos — o que está oculto não entra, e a folha diz quantos ficaram de fora e por quê;
  J. copiar — vai para a área de transferência a lista numerada, igual à da tela; sem área de transferência, o painel usa o
     comando antigo; sem nenhum dos dois, mostra o texto para copiar à mão;
  K. trilhas — a ficha de uma trilha imprime e copia os livros na ordem do roteiro, com a situação de cada um;
  L. no celular — os três botões cabem, com tamanho para o dedo;
  M. na pré-visualização isolada (sem armazenamento, dentro de outra página) — "Imprimir" mostra a lista em texto em vez
     de pedir uma impressão que o navegador ignoraria.

O que se espera é contado aqui, direto de src/catalog.json e src/trilhas.json, ou lido da própria tabela.
"""
import json, re
from caminhos import PAINEL_LIMPO, PAINEL_URL, RAIZ, TMP
from relogio import fixa
from playwright.sync_api import sync_playwright

errs = []; falhas = []
CAT = json.loads((RAIZ / 'src' / 'catalog.json').read_text(encoding='utf-8'))            # [título, autor, "marcadores", seção, eixo, …]
TRILHAS = json.loads((RAIZ / 'src' / 'trilhas.json').read_text(encoding='utf-8'))        # [marcador, nome, descrição, [posições]]
MARCAS = [set(r[2].split()) for r in CAT]
TENHO = [bool(m & {'tenho-fisico', 'tenho-digital', 'ja-tenho'}) for m in MARCAS]
HOJE = '09/11/2026'                                                                      # o relógio dos testes (relogio.py)

# ── o que se lê da tela ──
FOLHA = """() => { const el = document.querySelector('#impressao'), t = s => (el.querySelector(s) || {}).textContent || '';
  return { marca: t('.imp-m'), h1: t('h1'), desc: t('.imp-d'), meta: [...el.querySelectorAll('.imp-i')].map(p => p.textContent), cols: [...el.querySelectorAll('thead th')].map(th => th.textContent),
    linhas: [...el.querySelectorAll('tbody tr')].map(tr => [...tr.cells].slice(1).map(td => td.textContent)), ok: [...el.querySelectorAll('tbody tr')].map((tr, i) => tr.querySelector('.imp-q.ok') ? i : -1).filter(i => i >= 0),
    estrelas: [...el.querySelectorAll('tbody tr')].map((tr, i) => tr.querySelector('.imp-e') ? i : -1).filter(i => i >= 0), notas: [...el.querySelectorAll('.imp-n')].map(p => p.textContent.replace(/\\s+/g, ' ').trim()) }; }"""
# a caixa de impressão não existe no navegador de teste: no lugar dela, guarda-se a folha como estava na hora do pedido
# (como o navegador de verdade, o substituto anuncia que vai imprimir; quem diz que acabou é o teste)
STUB = "() => { window.__imp = []; window.print = () => { window.dispatchEvent(new Event('beforeprint')); window.__imp.push({ classe: document.documentElement.classList.contains('imprimindo'), titulo: document.title, folha: (%s)() }); }; }" % FOLHA
PEDIDOS = "() => window.__imp.length"
ULTIMA = "() => window.__imp[window.__imp.length - 1] || null"
ACABOU = "() => window.dispatchEvent(new Event('afterprint'))"
ESTADO = "() => ({ classe: document.documentElement.classList.contains('imprimindo'), folha: document.querySelector('#impressao').innerHTML.length, titulo: document.title })"
ABA = "v => { const t = document.querySelector(`#p-tab-${v} .abas [aria-selected=true] .cont`); return t ? +t.textContent.replace(/\\./g, '') : null; }"
LINHAS_TABELA = "v => [...document.querySelectorAll(`#p-tab-${v} tbody tr[data-id]`)].map(tr => { const a = tr.querySelector('.tt > span').textContent.trim(); return [tr.querySelector('.tt b').textContent.trim(), a === 'Autor não informado' ? '' : a]; })"
TOASTS = "() => [...document.querySelectorAll('#toasts .toast')].map(t => t.textContent)"
paginas = lambda pdf: len(re.findall(rb'/Type\s*/Page\b', pdf))


def ok(nome, cond, extra=''):
    print(('  ok   ' if cond else '  FALHA') + ' ' + nome + (' — ' + str(extra) if extra != '' else ''))
    if not cond: falhas.append(nome)


def abre(b, url, largura=1366, altura=768, tema='light', area=False):
    ctx = b.new_context(viewport={'width': largura, 'height': altura}, locale='pt-BR', timezone_id='America/Sao_Paulo', color_scheme=tema, permissions=['clipboard-read', 'clipboard-write'] if area else [])
    pg = ctx.new_page(); fixa(pg)
    pg.on('console', lambda m: errs.append(f'[{m.type}] {m.text}') if m.type in ('error', 'warning') else None)
    pg.on('pageerror', lambda e: errs.append(f'[pageerror] {e}'))
    pg.goto(url); pg.wait_for_timeout(1300)
    if pg.is_visible('#aviso .pri'): pg.click('#aviso .pri'); pg.wait_for_timeout(200)
    pg.evaluate(STUB)
    return pg


def tabela_inteira(pg, v):
    """As linhas da tabela, de todas as páginas, na ordem em que estão: [título, autor]."""
    pg.select_option(f'#p-tab-{v} .tam select', '100'); pg.wait_for_timeout(300)
    while pg.is_enabled(f'#p-tab-{v} [data-p="-1"]'): pg.click(f'#p-tab-{v} [data-p="-1"]'); pg.wait_for_timeout(120)
    linhas = pg.evaluate(LINHAS_TABELA, v)
    while pg.is_enabled(f'#p-tab-{v} [data-p="1"]'):
        pg.click(f'#p-tab-{v} [data-p="1"]'); pg.wait_for_timeout(150); linhas += pg.evaluate(LINHAS_TABELA, v)
    return linhas


with sync_playwright() as p:
    b = p.chromium.launch()
    pg = abre(b, PAINEL_LIMPO)
    def ir(v): pg.keyboard.press('Escape'); pg.click(f'#nav [data-ir={v}]'); pg.wait_for_timeout(800)
    def eixo(n): pg.evaluate(f"() => document.querySelector('#pop-eixo input[value=\"{n}\"]').click()"); pg.wait_for_timeout(450)
    def imprime(sel, espera=350):
        """Clica em "Imprimir" e devolve o que foi mandado para o papel (ou None, se nada foi)."""
        antes = pg.evaluate(PEDIDOS); pg.click(sel); pg.wait_for_timeout(espera)
        return pg.evaluate(ULTIMA) if pg.evaluate(PEDIDOS) > antes else None
    def acabou(): pg.evaluate(ACABOU); pg.wait_for_timeout(150)

    print('A. Os botões')
    NOMES = {'geral': 'Todos os livros', 'biblioteca': 'Livros do acervo', 'recs': 'Lista de recomendações', 'financas': 'Compras registradas', 'desejos': 'Lista de próximas aquisições', 'precos': 'Itens acompanhados'}
    bts = {}
    for v in NOMES:
        ir(v)
        bts[v] = pg.evaluate("v => [...document.querySelectorAll(`#p-tab-${v} .tb-levar button`)].map(b => [Object.keys(b.dataset)[0], b.textContent.trim(), b.getAttribute('aria-label') || b.textContent.trim(), !!b.title, Math.round(b.getBoundingClientRect().height)])", v)
    certo = [['imprimir', 'Imprimir', 'Imprimir a lista', True, 30], ['copiar', 'Copiar', 'Copiar a lista como texto', True, 30], ['csv', 'CSV', 'CSV', True, 30]]
    ok('nas seis tabelas: "Imprimir", "Copiar" e "CSV", nessa ordem, com nome e dica', all(x == certo for x in bts.values()), {k: x for k, x in bts.items() if x != certo})

    print('B. A folha é a lista da tela')
    ir('recs'); eixo(7)
    espera_n = sum(1 for i, r in enumerate(CAT) if not TENHO[i] and r[4] == 7)
    tab = tabela_inteira(pg, 'recs')
    f = imprime('#p-tab-recs [data-imprimir]')
    ok(f'recomendações do eixo "Horror, weird e mistério": {espera_n} livros na tabela e na folha', f is not None and len(tab) == espera_n == pg.evaluate(ABA, 'recs') == len(f['folha']['linhas']), (len(tab), espera_n, f and len(f['folha']['linhas'])))
    ok('as mesmas linhas, na mesma ordem: título e autor', [l[:2] for l in f['folha']['linhas']] == tab, [(a, z) for a, z in zip([l[:2] for l in f['folha']['linhas']], tab) if a != z][:3])
    ok('colunas: quadradinho, título, autor e as duas da lista de recomendações', f['folha']['cols'] == ['', 'Título', 'Autor', 'Eixo', 'Extensão'] and {l[2] for l in f['folha']['linhas']} == {'Horror, weird e mistério'} and {l[3] for l in f['folha']['linhas']} <= {'Curta', 'Média', 'Longa', ''}, f['folha']['cols'])
    ok('cabeçalho: o painel e a data, o nome da lista, quantos livros e em que ordem, os filtros', f['folha']['marca'] == f'Biblioteca do Lucas · {HOJE}' and f['folha']['h1'] == 'Lista de recomendações'
       and f['folha']['meta'] == [f'{espera_n} livros, em ordem de eixo', 'Filtros: Horror, weird e mistério'], (f['folha']['marca'], f['folha']['h1'], f['folha']['meta']))
    ok('enquanto imprime, a página leva o nome da lista (é o nome que o navegador sugere para o PDF)', f['classe'] and f['titulo'] == 'Lista de recomendações — Biblioteca do Lucas', (f['classe'], f['titulo']))
    acabou()
    # a aba, a busca e a ordem
    pg.click('#p-tab-recs thead th[data-c=titulo] button'); pg.wait_for_timeout(250); pg.click('#p-tab-recs thead th[data-c=titulo] button'); pg.wait_for_timeout(250)
    pg.fill('#p-tab-recs input[type=search]', 'king'); pg.wait_for_timeout(450)
    tab = tabela_inteira(pg, 'recs')
    f = imprime('#p-tab-recs [data-imprimir]'); acabou()
    ok('com busca e ordem invertida: a folha acompanha, e diz as duas coisas', 1 < len(tab) < espera_n and [l[:2] for l in f['folha']['linhas']] == tab and tab == sorted(tab, key=lambda x: x[0], reverse=True)
       and f['folha']['meta'] == [f'{len(tab)} livros, em ordem de título (decrescente)', 'Filtros: Horror, weird e mistério · busca “king”'], (len(tab), f['folha']['meta']))
    pg.fill('#p-tab-recs input[type=search]', ''); pg.wait_for_timeout(400)
    eixo(7); eixo(3)                                                        # Clássicos universais: aqui há prioridades entre as recomendações
    pg.click('#p-tab-recs .abas [data-a=top]'); pg.wait_for_timeout(350)
    tab = tabela_inteira(pg, 'recs'); n_top = sum(1 for i, r in enumerate(CAT) if not TENHO[i] and r[4] == 3 and 'top' in MARCAS[i] and 'lido' not in MARCAS[i])
    f = imprime('#p-tab-recs [data-imprimir]'); acabou()
    ok('na aba "Prioridades": a folha traz só as prioridades, e o nome da aba vai no título', f is not None and len(tab) == n_top > 0 and [l[:2] for l in f['folha']['linhas']] == tab and f['folha']['h1'] == 'Lista de recomendações — Prioridades', (len(tab), n_top, f and f['folha']['h1']))
    ok('…todas com a estrela, e a legenda embaixo', f is not None and f['folha']['estrelas'] == list(range(n_top)) and f['folha']['notas'] == ['prioridade'], f and (f['folha']['estrelas'], f['folha']['notas']))
    pg.click('#p-tab-recs .abas [data-a=todos]'); pg.wait_for_timeout(300); eixo(3); eixo(7)

    print('C. No papel')
    for tema, nome in (('light', 'claro'), ('dark', 'escuro')):
        pg2 = abre(b, PAINEL_LIMPO, tema=tema)
        pg2.click('#nav [data-ir=biblioteca]'); pg2.wait_for_timeout(700)
        pg2.evaluate("() => document.querySelector('#pop-eixo input[value=\"9\"]').click()"); pg2.wait_for_timeout(450)      # Filosofia e ética: uns 200 livros
        n = pg2.evaluate(ABA, 'biblioteca')
        pg2.click('#p-tab-biblioteca [data-imprimir]'); pg2.wait_for_timeout(350)
        pg2.emulate_media(media='print'); pg2.wait_for_timeout(200)
        papel = pg2.evaluate("""() => { const cs = e => getComputedStyle(e), el = document.querySelector('#impressao');
          return { visiveis: [...document.body.children].filter(e => cs(e).display !== 'none').map(e => e.id || e.tagName), fundo: [cs(document.documentElement).backgroundColor, cs(document.body).backgroundColor], texto: [...new Set([...el.querySelectorAll('h1, td, th, p')].map(e => cs(e).color))],
            cab: cs(el.querySelector('thead')).display, linha: cs(el.querySelector('tbody tr')).breakInside, linhas: el.querySelectorAll('tbody tr').length, largura: el.scrollWidth - el.clientWidth }; }""")
        escuro_demais = lambda c: max(int(x) for x in re.findall(r'\d+', c)[:3]) <= 80
        ok(f'tema {nome}: no papel só a folha aparece, com as {n} linhas', papel['visiveis'] == ['impressao'] and papel['linhas'] == n > 150, (papel['visiveis'], papel['linhas'], n))
        ok(f'tema {nome}: fundo branco e letra escura', set(papel['fundo']) == {'rgb(255, 255, 255)'} and all(escuro_demais(c) for c in papel['texto']), (papel['fundo'], papel['texto']))
        if tema == 'light':
            ok('o cabeçalho da tabela se repete a cada página, e nenhuma linha é cortada entre duas', papel['cab'] == 'table-header-group' and papel['linha'] == 'avoid' and papel['largura'] <= 0, papel)
            pg2.set_viewport_size({'width': 794, 'height': 1123}); pg2.wait_for_timeout(200); pg2.screenshot(path=str(TMP / 'shots' / 'listas-folha.png')); pg2.set_viewport_size({'width': 1366, 'height': 768})
            livre = paginas(pg2.pdf(format='A4', prefer_css_page_size=True))                                      # gerar o PDF avisa a página de que a impressão acabou
            ok(f'o PDF de verdade: as {n} linhas ocupam mais de uma página e menos de uma por dúzia de linhas', 1 < livre <= n / 12, livre)
            est = pg2.evaluate(ESTADO)
            ok('…e, quando o navegador avisa que acabou, a folha some e o nome da página volta', est == {'classe': False, 'folha': 0, 'titulo': 'Biblioteca · Biblioteca do Lucas'}, est)
            # com uma caixa aberta, a página fica travada (não rola): a folha não pode sair cortada na primeira página
            pg2.emulate_media(media='screen'); pg2.evaluate(STUB); pg2.click('#p-tab-biblioteca [data-imprimir]'); pg2.wait_for_timeout(350)
            pg2.evaluate("() => document.documentElement.classList.add('travado')"); pg2.emulate_media(media='print')
            travada = paginas(pg2.pdf(format='A4', prefer_css_page_size=True)); pg2.evaluate("() => document.documentElement.classList.remove('travado')")
            ok('com a página travada por uma caixa aberta, o PDF tem as mesmas páginas', travada == livre, (travada, livre))
        pg2.context.close()

    print('D. Depois de imprimir')
    f = imprime('#p-tab-recs [data-imprimir]')
    antes = pg.evaluate(ESTADO); acabou(); depois = pg.evaluate(ESTADO)
    ok('a folha fica montada até a impressão acabar; depois some, e o nome da página volta', antes['classe'] and antes['folha'] > 1000 and antes['titulo'].startswith('Lista de recomendações') and depois == {'classe': False, 'folha': 0, 'titulo': 'Recomendações · Biblioteca do Lucas'}, (antes, depois))
    imprime('#p-tab-recs [data-imprimir]'); pg.wait_for_timeout(900)                          # o navegador não avisa (acontece em celular)…
    antes = pg.evaluate(ESTADO); pg.mouse.click(700, 20); pg.wait_for_timeout(150); depois = pg.evaluate(ESTADO)
    ok('se o navegador não avisar que acabou, o primeiro clique na página desfaz a folha', antes['classe'] and depois == {'classe': False, 'folha': 0, 'titulo': 'Recomendações · Biblioteca do Lucas'}, (antes, depois))
    imprime('#p-tab-recs [data-imprimir]'); f2 = imprime('#p-tab-recs [data-imprimir]'); acabou()
    ok('dois pedidos seguidos não se atrapalham: vale a folha do último, e a página volta ao normal', f2 is not None and len(f2['folha']['linhas']) == espera_n and pg.evaluate(ESTADO) == {'classe': False, 'folha': 0, 'titulo': 'Recomendações · Biblioteca do Lucas'}, pg.evaluate(ESTADO))
    # o navegador recusa o pedido sem dizer nada (acontece logo depois de uma impressão cancelada): nem anuncia que vai imprimir
    pg.evaluate("() => { window.__mudo = 0; window.__de_verdade = window.print; window.print = () => { window.__mudo++; }; }")
    pg.click('#p-tab-recs [data-imprimir]'); pg.wait_for_timeout(1100)
    recado = pg.evaluate(TOASTS)[-1:]; est = pg.evaluate(ESTADO)
    ok('se o navegador recusar o pedido, o painel avisa e a página volta ao normal', pg.evaluate('() => window.__mudo') == 1 and recado and recado[0].startswith('O navegador não abriu a caixa de impressão') and est == {'classe': False, 'folha': 0, 'titulo': 'Recomendações · Biblioteca do Lucas'}, (recado, est))
    pg.evaluate("() => { window.print = window.__de_verdade; }")
    eixo(7)

    print('E. Lista longa')
    ir('biblioteca'); eixo(14)                                              # Psicologia e psicanálise: o maior eixo
    n = pg.evaluate(ABA, 'biblioteca')
    f = imprime('#p-tab-biblioteca [data-imprimir]', 500)
    msg = pg.inner_text('#dlg.on .dlg-msg') if pg.locator('#dlg.on').count() else ''
    m = re.search(r'Esta lista tem ([\d.]+) livros: no papel, umas ([\d.]+) páginas\.', msg)
    ok(f'{n} livros: em vez de imprimir, o painel diz quantas páginas são e pergunta', f is None and m is not None and int(m.group(1).replace('.', '')) == n > 300, msg)
    estimadas = int(m.group(2)) if m else 0
    pg.click('#dlg.on footer button:has-text("Cancelar")'); pg.wait_for_timeout(300)
    ok('"Cancelar" não imprime nada', pg.evaluate(ULTIMA)['folha']['h1'] != 'Livros do acervo' and pg.evaluate(ESTADO)['folha'] == 0, pg.evaluate(ESTADO))
    antes = pg.evaluate(PEDIDOS); pg.click('#p-tab-biblioteca [data-imprimir]'); pg.wait_for_timeout(400); pg.click('#dlg.on footer button:has-text("Imprimir assim mesmo")'); pg.wait_for_timeout(500)
    f = pg.evaluate(ULTIMA)
    ok('"Imprimir assim mesmo" manda a lista inteira, com a caixa já fechada', pg.evaluate(PEDIDOS) == antes + 1 and len(f['folha']['linhas']) == n and pg.locator('#dlg.on').count() == 0, (pg.evaluate(PEDIDOS) - antes, len(f['folha']['linhas'])))
    pg.emulate_media(media='print'); reais = paginas(pg.pdf(format='A4', prefer_css_page_size=True)); pg.emulate_media(media='screen')
    ok(f'a conta das páginas confere com o PDF de verdade ({reais})', abs(estimadas - reais) <= max(1, round(reais * 0.06)), (estimadas, reais))
    eixo(14); eixo(9)
    n9 = pg.evaluate(ABA, 'biblioteca'); f = imprime('#p-tab-biblioteca [data-imprimir]', 500); acabou()
    ok(f'uma lista de {n9} livros (umas sete páginas) imprime sem perguntar', f is not None and len(f['folha']['linhas']) == n9 and pg.locator('#dlg.on').count() == 0, f and len(f['folha']['linhas']))
    eixo(9)

    print('F. Lista vazia')
    ir('desejos')                                                           # painel sem exemplos: nada na lista de compra
    antes = pg.evaluate(PEDIDOS); pg.click('#p-tab-desejos [data-imprimir]'); pg.wait_for_timeout(300); t1 = pg.evaluate(TOASTS)
    pg.click('#p-tab-desejos [data-copiar]'); pg.wait_for_timeout(300); t2 = pg.evaluate(TOASTS)
    ok('sem linhas, "Imprimir" e "Copiar" só avisam', pg.evaluate(PEDIDOS) == antes and t1[-1:] == ['Não há linhas para imprimir.'] and t2[-1:] == ['Não há linhas para copiar.'] and pg.locator('#dlg.on').count() == 0, (t1, t2))

    print('I. Ocultos')
    ir('recs'); eixo(7)
    pg.click('#pw-fora .pop-b'); pg.wait_for_timeout(300); pg.check('#pop-fora input[data-fora=sit][value="sem-pt"]'); pg.wait_for_timeout(500); pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
    fora = sum(1 for i, r in enumerate(CAT) if not TENHO[i] and r[4] == 7 and 'sem-pt' in MARCAS[i])
    f = imprime('#p-tab-recs [data-imprimir]'); acabou()
    ok(f'com "sem edição em PT" oculto: {fora} livros a menos na folha, e ela diz quantos ficaram de fora e por quê', fora > 1 and len(f['folha']['linhas']) == espera_n - fora
       and f['folha']['notas'][-1] == f'Não entram {fora} livros que estão ocultos (sem edição em PT).', (fora, len(f['folha']['linhas']), f['folha']['notas']))
    pg.click('#f-fora [data-fora-limpar]'); pg.wait_for_timeout(500)
    f = imprime('#p-tab-recs [data-imprimir]'); acabou()
    ok('sem nada oculto, a folha não fala em ocultos', len(f['folha']['linhas']) == espera_n and not any('ocult' in x for x in f['folha']['notas']), f['folha']['notas'])
    pg.context.close()

    print('G. As marcas e H. o dinheiro (com os dados de exemplo)')
    pg = abre(b, PAINEL_URL)
    ir('biblioteca'); eixo(9)
    pg.click('#p-tab-biblioteca .abas [data-a=lido]'); pg.wait_for_timeout(300); lidos = pg.evaluate(ABA, 'biblioteca'); pg.click('#p-tab-biblioteca .abas [data-a=todos]'); pg.wait_for_timeout(300)
    f = imprime('#p-tab-biblioteca [data-imprimir]', 500)
    leg = f['folha']['notas'][0] if f['folha']['notas'] else ''
    ok(f'os {lidos} livros lidos da lista saem com o quadradinho marcado; os outros, vazio', lidos > 0 and len(f['folha']['ok']) == lidos < len(f['folha']['linhas']), (lidos, len(f['folha']['ok'])))
    ok('a legenda, embaixo, explica as marcas que a folha tem — e só elas', leg.endswith('já li') and ('prioridade' in leg) == bool(f['folha']['estrelas']) and len(f['folha']['notas']) == 1, (f['folha']['notas'], len(f['folha']['estrelas'])))
    pg.emulate_media(media='print')
    desenho = pg.evaluate("() => { const q = document.querySelector('#impressao tbody .imp-q.ok'), e = getComputedStyle(q, '::after'), v = document.querySelector('#impressao tbody .imp-q:not(.ok)'); return { visto: e.content, borda: e.borderRightWidth, gira: e.transform !== 'none', texto: q.textContent, caixa: [q.offsetWidth, q.offsetHeight], vazio: getComputedStyle(v, '::after').content }; }")
    pg.emulate_media(media='screen')
    ok('o visto é desenhado, não é uma letra', desenho['texto'] == '' and desenho['gira'] and desenho['borda'] != '0px' and desenho['vazio'] == 'none' and min(desenho['caixa']) >= 11, desenho); acabou()
    eixo(9); ir('recs')
    pg.click('#p-tab-recs .abas [data-a=top]'); pg.wait_for_timeout(300)
    f = imprime('#p-tab-recs [data-imprimir]'); n_estrela = len(f['folha']['estrelas'])
    estrela = pg.evaluate("() => { const e = document.querySelector('#impressao tbody .imp-e'); return e ? { tag: e.tagName.toLowerCase(), dentro: e.closest('td').className, texto: e.closest('td').textContent } : null; }")
    ok('a estrela de prioridade também é desenho, ao lado do título', n_estrela == len(f['folha']['linhas']) > 0 and estrela and estrela['tag'] == 'svg' and estrela['dentro'] == 't' and '★' not in estrela['texto'], (n_estrela, estrela)); acabou()
    pg.click('#p-tab-recs .abas [data-a=todos]'); pg.wait_for_timeout(300)
    ir('financas')
    f = imprime('#p-tab-financas [data-imprimir]', 500); acabou()
    pagos = [l[3] for l in f['folha']['linhas']]
    ok('Finanças: a folha leva a data da compra e o valor pago', f['folha']['cols'] == ['', 'Título', 'Autor', 'Aquisição', 'Pago'] and sum(1 for x in pagos if re.fullmatch(r'R\$\s[\d.]+,\d\d', x)) > 20 and f['folha']['meta'][0].endswith('em ordem de valor pago (decrescente)'), (f['folha']['cols'], pagos[:4], f['folha']['meta']))
    ir('desejos')
    f = imprime('#p-tab-desejos [data-imprimir]'); acabou()
    ok('Próximas aquisições: o melhor preço, com a loja, e o preço-alvo', f['folha']['cols'] == ['', 'Título', 'Autor', 'Melhor preço', 'Alvo'] and all(re.fullmatch(r'R\$\s[\d.]+,\d\d · .+', l[2]) for l in f['folha']['linhas']) and f['folha']['meta'][0].endswith('em ordem de distância até o preço-alvo'), (f['folha']['linhas'][:2], f['folha']['meta']))
    pg.click('#b-olho'); pg.wait_for_timeout(400)
    f = imprime('#p-tab-desejos [data-imprimir]'); acabou()
    ok('com o olho fechado, nenhum valor vai para o papel: as colunas de dinheiro saem', f['folha']['cols'] == ['', 'Título', 'Autor'] and 'R$' not in json.dumps(f['folha'], ensure_ascii=False), f['folha']['cols'])
    ir('financas')
    f = imprime('#p-tab-financas [data-imprimir]', 500); acabou()
    ok('…em Finanças fica a data, sem o valor', f['folha']['cols'] == ['', 'Título', 'Autor', 'Aquisição'] and 'R$' not in json.dumps(f['folha'], ensure_ascii=False), f['folha']['cols'])
    pg.click('#b-olho'); pg.wait_for_timeout(300)
    pg.context.close()

    print('J. Copiar')
    pg = abre(b, PAINEL_LIMPO, area=True)
    ir('recs'); eixo(7)
    tab = tabela_inteira(pg, 'recs')
    pg.click('#p-tab-recs [data-copiar]'); pg.wait_for_timeout(500)
    try: colado = pg.evaluate("() => navigator.clipboard.readText()")
    except Exception as e: colado = None; print('      (pulado: este navegador de teste não deixa ler a área de transferência —', str(e).splitlines()[0][:90] + ')')
    certo = '\n'.join(['Lista de recomendações', f'Biblioteca do Lucas · {HOJE}', f'{len(tab)} livros, em ordem de eixo', 'Filtros: Horror, weird e mistério', ''] + [f'{i + 1}. {t}{" — " + a if a else ""}' for i, (t, a) in enumerate(tab)]) + '\n'
    if colado is not None:
        ok('a área de transferência recebe a lista da tela: cabeçalho e uma linha numerada por livro', colado == certo, [x for x in zip(colado.split('\n'), certo.split('\n')) if x[0] != x[1]][:3] or (len(colado), len(certo)))
    ok('o painel confirma quantos livros copiou', pg.evaluate(TOASTS)[-1:] == [f'Lista copiada: {len(tab)} livros. Agora é só colar onde quiser.'], pg.evaluate(TOASTS))
    # sem a área de transferência moderna: o comando antigo, por um campo de texto escondido
    pg.evaluate("() => { Object.defineProperty(navigator, 'clipboard', { value: undefined, configurable: true }); window.__cmd = []; document.execCommand = c => { const a = document.activeElement; window.__cmd.push([c, a && a.tagName, a && a.value]); return true; }; }")
    pg.focus('#p-tab-recs [data-copiar]'); pg.click('#p-tab-recs [data-copiar]'); pg.wait_for_timeout(400)
    cmd = pg.evaluate("() => window.__cmd")
    ok('sem ela, o painel copia pelo comando antigo, com o mesmo texto', len(cmd) == 1 and cmd[0][:2] == ['copy', 'TEXTAREA'] and cmd[0][2] == certo and pg.evaluate(TOASTS)[-1].startswith('Lista copiada'), (cmd and cmd[0][:2], pg.evaluate(TOASTS)[-1:]))
    sobra = pg.evaluate("() => ({ campos: document.querySelectorAll('body > textarea').length, foco: document.activeElement && Object.keys(document.activeElement.dataset)[0] })")
    ok('o campo escondido some, e o foco volta para o botão', sobra == {'campos': 0, 'foco': 'copiar'}, sobra)
    # nem um nem outro: o texto aparece para copiar à mão
    pg.evaluate("() => { document.execCommand = () => false; }")
    pg.click('#p-tab-recs [data-copiar]'); pg.wait_for_timeout(500)
    cx = pg.evaluate("() => { const d = document.querySelector('#dlg.on'); return d ? { titulo: d.querySelector('h2').textContent, nota: d.querySelector('.nota').textContent, texto: d.querySelector('textarea').value, botoes: [...d.querySelectorAll('footer button')].map(b => b.textContent) } : null; }")
    ok('se o navegador não deixar copiar de jeito nenhum, a lista aparece num campo para copiar à mão', cx and cx['titulo'] == 'Copiar a lista' and cx['texto'] == certo and cx['botoes'] == ['Fechar', 'Selecionar tudo'] and 'Selecionar tudo' in cx['nota'], cx and (cx['titulo'], cx['botoes'], cx['nota']))
    pg.click('#dlg.on footer button:has-text("Selecionar tudo")'); pg.wait_for_timeout(200)
    sel = pg.evaluate("() => { const t = document.querySelector('#dlg.on textarea'); return t ? [t.selectionStart, t.selectionEnd, t.value.length] : null; }")
    ok('"Selecionar tudo" seleciona o texto inteiro e deixa a caixa aberta', sel and sel[0] == 0 and sel[1] == sel[2] > 100, sel)
    pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
    pg.context.close()

    print('K. Trilhas')
    pg = abre(b, PAINEL_LIMPO, area=True)
    ir('recs')
    tr = next(t for t in TRILHAS if t[0] == 'trilha-lovecraft-widows-bay'); livros = [[CAT[i][0], CAT[i][1]] for i in tr[3]]
    pg.click(f'#p-trilhas [data-trilha="{tr[0]}"]'); pg.wait_for_timeout(500)
    links = pg.evaluate("() => [...document.querySelectorAll('#dlg.on .tr-a button')].map(b => [b.textContent, !!b.title, Math.round(b.getBoundingClientRect().height)])")
    ok('na ficha da trilha: "ver na tabela", "imprimir" e "copiar"', [l[0] for l in links] == ['ver na tabela', 'imprimir', 'copiar'] and all(l[1] for l in links[1:]) and min(l[2] for l in links) >= 24, links)
    na_caixa = pg.evaluate("() => [...document.querySelectorAll('#dlg.on .tr-l li')].map(li => [li.querySelector('.li-m b').textContent, li.querySelector('.li-m span').textContent, li.querySelector('.pill').textContent])")
    frase = pg.inner_text('#dlg.on .tr-res b'); titulo = pg.inner_text('#dlg.on h2')
    f = imprime('#dlg.on [data-tr-imprimir]')
    ok('a folha da trilha: o nome, a descrição e o andamento, como na ficha', f is not None and f['folha']['h1'] == titulo and f['folha']['h1'].endswith(tr[1]) and f['folha']['desc'] == tr[2] and f['folha']['meta'] == [frase], f and (f['folha']['h1'], f['folha']['meta']))
    ok(f'os {len(livros)} livros, numerados na ordem do roteiro, com a situação de cada um', f['folha']['cols'] == ['', 'Nº', 'Título', 'Autor', 'Situação'] and [l[1:3] for l in f['folha']['linhas']] == livros
       and [[l[1], l[2], l[3]] for l in f['folha']['linhas']] == na_caixa and [l[0] for l in f['folha']['linhas']] == [str(i + 1) for i in range(len(livros))], f['folha']['linhas'][:3])
    ok('a ficha continua aberta, e a folha diz de onde vem a ordem', pg.locator('#dlg.on .tr-l').count() == 1 and f['folha']['notas'] == ['A ordem é a sugerida no catálogo da biblioteca.'], f['folha']['notas'])
    pg.emulate_media(media='print'); so_folha = pg.evaluate("() => [...document.body.children].filter(e => getComputedStyle(e).display !== 'none').map(e => e.id || e.tagName)")
    pg.set_viewport_size({'width': 794, 'height': 1123}); pg.wait_for_timeout(200); pg.screenshot(path=str(TMP / 'shots' / 'listas-trilha.png')); pg.set_viewport_size({'width': 1366, 'height': 768}); pg.emulate_media(media='screen')
    ok('no papel, a ficha aberta não aparece: só a folha', so_folha == ['impressao'], so_folha); acabou()
    pg.click('#dlg.on [data-tr-copiar]'); pg.wait_for_timeout(500)
    certo = '\n'.join([titulo, f'Biblioteca do Lucas · {HOJE}', tr[2], frase, ''] + [f'{i + 1}. {t} — {a} ({s.lower()})' for i, (t, a, s) in enumerate(na_caixa)] + ['', 'A ordem é a sugerida no catálogo da biblioteca.']) + '\n'
    try: colado = pg.evaluate("() => navigator.clipboard.readText()")
    except Exception: colado = None; print('      (pulado: este navegador de teste não deixa ler a área de transferência)')
    if colado is not None: ok('"copiar" leva a trilha em texto: a situação vai entre parênteses', colado == certo, [x for x in zip(colado.split('\n'), certo.split('\n')) if x[0] != x[1]][:3] or (len(colado), len(certo)))
    ok('…e o painel confirma, com a ficha ainda aberta', pg.evaluate(TOASTS)[-1:] == [f'Lista copiada: {len(livros)} livros. Agora é só colar onde quiser.'] and pg.locator('#dlg.on .tr-l').count() == 1, pg.evaluate(TOASTS))
    pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
    # um livro da trilha oculto
    pg.click('#pw-fora .pop-b'); pg.wait_for_timeout(300); pg.check('#pop-fora input[data-fora=sit][value="sem-pt"]'); pg.wait_for_timeout(500); pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
    some = [CAT[i][0] for i in tr[3] if 'sem-pt' in MARCAS[i]]
    pg.click(f'#p-trilhas [data-trilha="{tr[0]}"]'); pg.wait_for_timeout(500)
    f = imprime('#dlg.on [data-tr-imprimir]'); acabou()
    ok(f'com um livro da trilha oculto ({some[0]}): ele não entra, a numeração segue, e a folha avisa', len(some) == 1 and [l[1] for l in f['folha']['linhas']] == [t for t, _ in livros if t not in some]
       and [l[0] for l in f['folha']['linhas']] == [str(i + 1) for i in range(len(livros) - 1)] and f['folha']['notas'][-1] == 'Não entra 1 livro desta trilha, que está oculto (sem edição em PT).', f['folha']['notas'])
    pg.context.close()

    print('L. No celular')
    pg = abre(b, PAINEL_LIMPO, largura=390, altura=800)
    pg.locator('#p-tab-geral').scroll_into_view_if_needed(); pg.wait_for_timeout(400)
    cel = pg.evaluate("""() => { const r = e => e.getBoundingClientRect(), c = r(document.querySelector('#p-tab-geral')), bs = [...document.querySelectorAll('#p-tab-geral .tb-levar button')];
      return { bts: bs.map(b => [Object.keys(b.dataset)[0], Math.round(r(b).width), Math.round(r(b).height), b.getAttribute('aria-label') || b.textContent.trim(), [...b.querySelectorAll('span')].filter(s => s.offsetWidth).map(s => s.textContent).join('')]),
        dentro: bs.every(b => r(b).left >= c.left && r(b).right <= c.right), linha: new Set(bs.map(b => Math.round(r(b).top))).size, rola: document.documentElement.scrollWidth - innerWidth }; }""")
    ok('os três botões cabem numa linha, dentro do cartão, sem rolagem para o lado', cel['dentro'] and cel['linha'] == 1 and cel['rola'] <= 0, cel)
    ok('"Imprimir" e "Copiar" ficam só com o desenho (o nome vai para o leitor de tela), com tamanho para o dedo', [x[:1] + x[3:] for x in cel['bts']] == [['imprimir', 'Imprimir a lista', ''], ['copiar', 'Copiar a lista como texto', ''], ['csv', 'CSV', 'CSV']] and all(x[1] >= 36 and x[2] >= 32 for x in cel['bts']), cel['bts'])
    pg.screenshot(path=str(TMP / 'shots' / 'listas-celular.png'))
    pg.click('#nav-m [data-ir=recs]'); pg.wait_for_timeout(800)
    pg.evaluate(f"() => document.querySelector('#p-trilhas [data-trilha=\"{tr[0]}\"]').click()"); pg.wait_for_timeout(500)
    tl = pg.evaluate("() => { const r = e => e.getBoundingClientRect(), c = r(document.querySelector('#dlg.on .dlg-c')); return { bts: [...document.querySelectorAll('#dlg.on .tr-a button')].map(b => [b.textContent, Math.round(r(b).height), r(b).left >= c.left && r(b).right <= c.right]), rola: document.querySelector('#dlg.on .dlg-c').scrollWidth - document.querySelector('#dlg.on .dlg-c').clientWidth }; }")
    ok('na ficha da trilha, os três atalhos cabem na largura da caixa', [x[0] for x in tl['bts']] == ['ver na tabela', 'imprimir', 'copiar'] and all(x[2] and x[1] >= 24 for x in tl['bts']) and tl['rola'] <= 0, tl)
    f = imprime('#dlg.on [data-tr-imprimir]'); acabou()
    ok('…e "imprimir" monta a folha da trilha', f is not None and len(f['folha']['linhas']) == len(livros), f and len(f['folha']['linhas']))
    pg.context.close()

    print('M. Na pré-visualização isolada')
    (TMP / 'wrap-listas.html').write_text('<!doctype html><html><body style="margin:0"><iframe id="f" sandbox="allow-scripts" src="' + PAINEL_URL + '" style="width:100vw;height:100vh;border:0;display:block"></iframe></body></html>', encoding='utf-8')
    ctx = b.new_context(viewport={'width': 1280, 'height': 860}, locale='pt-BR', timezone_id='America/Sao_Paulo')
    pg = ctx.new_page(); fixa(pg)
    pg.on('console', lambda m: errs.append(f'[isolada {m.type}] {m.text}') if m.type in ('error', 'warning') else None)
    pg.on('pageerror', lambda e: errs.append(f'[isolada pageerror] {e}'))
    pg.goto((TMP / 'wrap-listas.html').as_uri()); pg.wait_for_timeout(1500)
    fr = pg.frames[1]
    fr.click('#aviso .pri'); pg.wait_for_timeout(200); fr.click('#nav [data-ir=desejos]'); pg.wait_for_timeout(800)
    fr.evaluate("() => { window.__imp = 0; const p = window.print; window.print = () => { window.__imp++; }; }")
    fr.click('#p-tab-desejos [data-imprimir]'); pg.wait_for_timeout(500)
    cx = fr.evaluate("() => { const d = document.querySelector('#dlg.on'); return d ? { titulo: d.querySelector('h2').textContent, nota: d.querySelector('.nota').textContent, linhas: d.querySelector('textarea').value.split('\\n').filter(l => /^\\d+\\. /.test(l)).length, pedidos: window.__imp } : { pedidos: window.__imp }; }")
    n = fr.evaluate(ABA, 'desejos')
    ok('"Imprimir" não pede uma impressão que o navegador ignoraria: explica e mostra a lista em texto', cx.get('titulo') == 'Imprimir a lista' and cx['pedidos'] == 0 and cx['linhas'] == n > 5 and 'não deixa imprimir' in cx['nota'], cx)
    fr.click('#dlg.on header [data-fechar]'); pg.wait_for_timeout(300)
    fr.click('#p-tab-desejos [data-copiar]'); pg.wait_for_timeout(600)
    fim = fr.evaluate("() => ({ caixa: (document.querySelector('#dlg.on h2') || {}).textContent || '', aviso: [...document.querySelectorAll('#toasts .toast')].map(t => t.textContent).pop() || '' })")
    ok('"Copiar" copia ou, se o navegador não deixar, mostra o texto — sem erro', fim['aviso'].startswith('Lista copiada') or fim['caixa'] == 'Copiar a lista', fim)
    ctx.close()
    b.close()

print('FALHAS:', falhas); print('ERROS:', len(errs) + len(falhas)); [print('  ', x[:300]) for x in errs[:10]]
