"""As caixas de diálogo em janela baixa — a de qualquer notebook — e no celular.

O defeito que este teste guarda: com a janela do navegador abaixo de uns 800 px de altura, as caixas "Novo livro",
"Editar livro" e "Seus dados" ficavam mais altas que a janela, e o rodapé — onde estão "Adicionar livro" e "Salvar
alterações" — caía abaixo da borda da tela, sem jeito de alcançar. Os outros testes abrem o painel com 900 px ou mais
de altura, onde tudo cabia; por isso nenhum deles viu.

Confere, em oito tamanhos de janela (da de 1536 × 745 em que o defeito apareceu ao celular deitado), que toda caixa:
  · fica inteira dentro da janela;
  · tem cada botão do rodapé e o X de fechar à vista e recebendo o clique (nada por cima);
  · quando o conteúdo não cabe, rola pelo miolo — o cabeçalho e o rodapé ficam parados — e a rolagem chega ao fim.
O mesmo vale para os botões da ficha do livro, os quadros "Eixo", "Mais filtros" e "Ocultar" e, no celular, a folha de
filtros.
Por fim, numa janela de notebook comum (1366 × 650, onde o botão ficava inteiro fora da tela), usa de verdade: adiciona
um livro e o edita, clicando com o mouse.
"""
from caminhos import PAINEL_LIMPO, PAINEL_URL, TMP
from relogio import fixa
from playwright.sync_api import sync_playwright

CHAVE = 'biblioteca-lucas:v1'
errs = []; falhas = []
JANELAS = [(1536, 745), (1366, 650), (1280, 600), (1024, 560), (900, 480), (390, 600), (320, 480), (740, 360)]

# Uma caixa aberta: o que está fora da janela, o que não recebe o clique, e se o miolo rola até o fim.
CAIXA = """() => { const d = document.querySelector('#dlg.on .dlg-cx'); if (!d) return null;
  const r = e => e.getBoundingClientRect(), H = innerHeight, W = innerWidth, c = d.querySelector('.dlg-c'), f = d.querySelector('footer');
  const dentro = e => { const x = r(e); return x.top >= -0.5 && x.left >= -0.5 && x.bottom <= H + 0.5 && x.right <= W + 0.5; };
  const recebe = e => { const x = r(e), a = document.elementFromPoint(x.left + x.width / 2, x.top + x.height / 2); return !!a && e.contains(a); };
  const bs = [...d.querySelectorAll('footer button'), d.querySelector('header [data-fechar]')], nome = b => b.textContent.trim() || b.getAttribute('aria-label');
  const cabia = c.scrollHeight <= c.clientHeight + 1; c.scrollTop = c.scrollHeight;
  return { t: d.querySelector('h2').textContent, caixa: [Math.round(r(d).top), Math.round(r(d).bottom)], dentro: dentro(d),
           fora: bs.filter(b => !dentro(b)).map(nome), tapados: bs.filter(b => !recebe(b)).map(nome), botoes: bs.length,
           rola: cabia || (['auto', 'scroll'].includes(getComputedStyle(c).overflowY) && c.scrollTop + c.clientHeight >= c.scrollHeight - 1 && c.scrollTop > 0),
           miolo: !f || r(c).bottom <= r(f).top + 1, cabia }; }"""
# Um conjunto de botões que precisa estar à vista (os da ficha do livro, os do pé da folha de filtros).
BOTOES = """s => { const r = e => e.getBoundingClientRect(), bs = [...document.querySelectorAll(s)].filter(b => b.offsetWidth || b.offsetHeight);
  const recebe = e => { const x = r(e), a = document.elementFromPoint(x.left + x.width / 2, x.top + x.height / 2); return !!a && e.contains(a); };
  return { n: bs.length, ruins: bs.filter(b => r(b).bottom > innerHeight + 0.5 || r(b).top < -0.5 || r(b).right > innerWidth + 0.5 || !recebe(b)).map(b => b.textContent.trim() || b.getAttribute('aria-label')) }; }"""
QUADRO = "s => { const x = document.querySelector(s).getBoundingClientRect(); return x.height > 40 && x.top >= -0.5 && x.bottom <= innerHeight + 0.5 && x.left >= -0.5 && x.right <= innerWidth + 0.5; }"


def ok(nome, cond, extra=''):
    print(('  ok   ' if cond else '  FALHA') + ' ' + nome + (' — ' + str(extra) if extra != '' else ''))
    if not cond: falhas.append(nome)


def abre(b, url, w, h):
    ctx = b.new_context(viewport={'width': w, 'height': h}, locale='pt-BR', timezone_id='America/Sao_Paulo')
    pg = ctx.new_page(); fixa(pg)
    pg.on('console', lambda m: errs.append(f'[{m.type}] {m.text}') if m.type in ('error', 'warning') else None)
    pg.on('pageerror', lambda e: errs.append(f'[pageerror] {e}'))
    pg.goto(url); pg.wait_for_timeout(1200)
    pg.evaluate("() => { const a = document.querySelector('#aviso .pri'); if (a) a.click(); }"); pg.wait_for_timeout(200)
    return pg


with sync_playwright() as p:
    b = p.chromium.launch()

    print('AS CAIXAS, JANELA POR JANELA (com os dados de exemplo)')
    for w, h in JANELAS:
        pg = abre(b, PAINEL_URL, w, h)
        nav = '#nav' if w > 820 else '#nav-m'
        def js(seletor): pg.evaluate("s => document.querySelector(s).click()", seletor); pg.wait_for_timeout(380)
        def ir(v): js(f'{nav} [data-ir={v}]'); pg.wait_for_timeout(350)
        def fecha():
            for _ in range(3): pg.keyboard.press('Escape'); pg.wait_for_timeout(120)
        caixas = [('Novo livro', lambda: js('#b-novo')),
                  ('Editar livro', lambda: (ir('biblioteca'), js('#p-tab-biblioteca tbody tr[data-id]'), js('#gv-acoes [data-acao=editar]'))),
                  ('Seus dados', lambda: js('#b-dados')),
                  ('Trilha 1', lambda: (ir('recs'), js('#p-trilhas .li'))),
                  ('Registrar cotação', lambda: (ir('desejos'), js('#p-tab-desejos tbody tr[data-id]'), js('#gaveta [data-acao=cotar]'))),
                  ('Registrar compra', lambda: (ir('desejos'), js('#p-tab-desejos tbody tr[data-id]'), js('#gaveta [data-acao=comprei]')))]
        ruins = {}; altas = 0
        for titulo, abrir in caixas:
            abrir(); m = pg.evaluate(CAIXA)
            if not m or not m['t'].startswith(titulo): ruins[titulo] = f'não abriu ({m and m["t"]})'
            elif not (m['dentro'] and not m['fora'] and not m['tapados'] and m['rola'] and m['miolo'] and m['botoes'] >= 1): ruins[titulo] = m
            altas += bool(m and not m['cabia'])
            fecha()
        ok(f'{w} × {h}: as {len(caixas)} caixas cabem na janela, com os botões à mão ({altas} delas rolando por dentro)', not ruins, ruins)
        # a ficha do livro: os botões do pé
        ir('biblioteca'); js('#p-tab-biblioteca tbody tr[data-id]'); pg.wait_for_timeout(250)
        ficha = pg.evaluate(BOTOES, '#gaveta.on #gv-acoes button, #gaveta.on .gv-h [data-fechar]')
        fecha()
        if w > 820:
            js('#pw-eixo .pop-b'); eixo = pg.evaluate(QUADRO, '#pop-eixo'); fecha()
            js('#pw-mais .pop-b'); mais = pg.evaluate(QUADRO, '#pop-mais'); fecha()
            js('#pw-fora .pop-b'); fora = pg.evaluate(QUADRO, '#pop-fora'); fecha()
            ok(f'{w} × {h}: os botões da ficha e os quadros "Eixo", "Mais filtros" e "Ocultar" também', ficha['n'] >= 3 and not ficha['ruins'] and eixo and mais and fora, (ficha, eixo, mais, fora))
        else:
            js('#f-abrir'); pg.wait_for_timeout(250)
            folha = pg.evaluate(BOTOES, '#f-painel .f-pf button, #f-painel .f-ph button'); fecha()
            # na folha: "ocultar categorias" e o X, no topo; "Limpar tudo" e "Ver resultados", no pé
            ok(f'{w} × {h}: os botões da ficha e os da folha de filtros também', ficha['n'] >= 3 and not ficha['ruins'] and folha['n'] == 4 and not folha['ruins'], (ficha, folha))
        pg.context.close()

    print('DE VERDADE, NUMA JANELA DE NOTEBOOK (1366 × 650, painel sem exemplos)')
    pg = abre(b, PAINEL_LIMPO, 1366, 650)
    guardado = lambda t: pg.evaluate("t => (JSON.parse(localStorage.getItem('%s')).livros.find(x => x.t === t) || null)" % CHAVE, t)
    pg.click('#b-novo'); pg.wait_for_timeout(400)
    pg.fill('#dlg [data-f=t]', 'Livro da Janela Baixa'); pg.screenshot(path=str(TMP / 'shots' / 'janela-baixa-novo.png'))
    try: pg.click('#dlg footer .pri', timeout=4000); clicou = True
    except Exception as e: clicou = False; print('     ', str(e).splitlines()[0][:160])
    pg.wait_for_timeout(900)
    ok('"Adicionar livro" está na tela e aceita o clique do mouse', clicou and pg.evaluate("() => !document.querySelector('#dlg').classList.contains('on')"))
    g = guardado('Livro da Janela Baixa')
    ok('o livro foi adicionado, e a ficha dele abriu', bool(g) and pg.evaluate("() => document.querySelector('#gaveta').classList.contains('on')"), g)
    pg.click('#gv-acoes [data-acao=editar]'); pg.wait_for_timeout(400)
    pg.select_option('#dlg [data-f=col]', 'acervo'); pg.wait_for_timeout(300)       # no acervo o formulário tem dez campos a mais: é a caixa mais alta do painel
    pg.fill('#dlg [data-f=a]', 'Autora de Teste'); pg.fill('#dlg [data-f=obs]', 'Edição de bolso.')
    m = pg.evaluate(CAIXA); pg.screenshot(path=str(TMP / 'shots' / 'janela-baixa-editar.png'))
    ok('"Editar livro" com a lista "Acervo": o formulário não cabe, rola por dentro e o rodapé fica à vista', m and not m['cabia'] and m['dentro'] and not m['fora'] and not m['tapados'] and m['rola'] and m['miolo'], m)
    try: pg.click('#dlg footer .pri', timeout=4000); clicou = True
    except Exception as e: clicou = False; print('     ', str(e).splitlines()[0][:160])
    pg.wait_for_timeout(900)
    g = guardado('Livro da Janela Baixa') or {}
    ok('"Salvar alterações" aceita o clique, e o que foi editado fica guardado', clicou and g.get('a') == 'Autora de Teste' and g.get('col') == 'acervo' and g.get('obs') == 'Edição de bolso.', {k: g.get(k) for k in ('a', 'col', 'obs')})
    pg.context.close()
    b.close()

print('FALHAS:', falhas); print('ERROS:', len(errs) + len(falhas)); [print('  ', x[:300]) for x in errs[:10]]
