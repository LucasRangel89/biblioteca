"""Foco e teclado nas camadas: a gaveta e os diálogos recebem o foco ao abrir, prendem o Tab e devolvem o foco ao fechar."""
from caminhos import PAINEL_URL
from relogio import fixa
from playwright.sync_api import sync_playwright
URL = PAINEL_URL
falhas = []
def ok(nome, cond, extra=''):
    print(('  ok   ' if cond else '  FALHA') + ' ' + nome + (' — ' + str(extra) if extra != '' else ''))
    if not cond: falhas.append(nome)
with sync_playwright() as p:
    b = p.chromium.launch()
    for w, h in [(1440, 900), (390, 844)]:
        print(f'== {w}px')
        ctx = b.new_context(viewport={'width': w, 'height': h}, locale='pt-BR', timezone_id='America/Sao_Paulo')
        pg = ctx.new_page(); fixa(pg); pg.on('pageerror', lambda e: falhas.append('pageerror ' + str(e)))
        pg.goto(URL); pg.wait_for_timeout(1000); pg.click('#aviso .pri'); pg.wait_for_timeout(200)
        foco = lambda: pg.evaluate("() => { const a = document.activeElement; return (a.closest('#dlg') ? 'dlg:' : a.closest('#gaveta') ? 'gaveta:' : 'pagina:') + (a.id || a.dataset.acao || a.dataset.b || a.dataset.f || a.dataset.c || a.className || a.tagName); }")
        nav = '#nav' if w > 820 else '#nav-m'
        pg.click(f'{nav} [data-ir=desejos]'); pg.wait_for_timeout(800)
        pg.click('#p-tab-desejos tbody tr'); pg.wait_for_timeout(500)
        ok('clique na linha: foco entra na gaveta', foco().startswith('gaveta:'), foco())
        seq = []
        for i in range(30): pg.keyboard.press('Tab'); seq.append(foco())
        ok('Tab fica dentro da gaveta e dá a volta', all(x.startswith('gaveta:') for x in seq) and len(set(seq)) < 30, f'{len(set(seq))} paradas')
        seq = []
        for i in range(4): pg.keyboard.press('Shift+Tab'); seq.append(foco())
        ok('Shift+Tab também', all(x.startswith('gaveta:') for x in seq), seq)
        pg.click('#gaveta [data-acao=comprei]'); pg.wait_for_timeout(500)
        ok('diálogo: foco no 1º campo', foco().startswith('dlg:'), foco())
        seq = []
        for i in range(16): pg.keyboard.press('Tab'); seq.append(foco())
        ok('Tab preso no diálogo', all(x.startswith('dlg:') for x in seq) and len(set(seq)) < 16, f'{len(set(seq))} paradas')
        pg.keyboard.press('Shift+Tab'); pg.keyboard.press('Shift+Tab'); ok('Shift+Tab no diálogo', foco().startswith('dlg:'), foco())
        pg.keyboard.press('Escape'); pg.wait_for_timeout(400)
        ok('Esc fecha o diálogo e o foco volta à gaveta', foco().startswith('gaveta:') and pg.evaluate("() => !document.querySelector('#dlg').classList.contains('on') && document.querySelector('#gaveta').classList.contains('on')"), foco())
        pg.keyboard.press('Escape'); pg.wait_for_timeout(500)
        ok('Esc fecha a gaveta e o foco volta à linha', foco().startswith('pagina:') and pg.evaluate("() => !document.querySelector('#gaveta').classList.contains('on') && document.activeElement.tagName === 'TR'"), foco())
        pg.focus('#p-tab-desejos tbody tr >> nth=1'); pg.keyboard.press('Enter'); pg.wait_for_timeout(500)
        ok('Enter na linha: foco entra na gaveta', foco().startswith('gaveta:'), foco())
        pg.keyboard.press('Tab'); ok('1º Tab = botão fechar', pg.evaluate("() => document.activeElement.matches('#gaveta [data-fechar]')"), foco())
        pg.keyboard.press('Enter'); pg.wait_for_timeout(500); ok('Enter no fechar fecha', pg.evaluate("() => !document.querySelector('#gaveta').classList.contains('on')"))
        pg.click('#b-novo'); pg.wait_for_timeout(500); ok('Novo livro: foco no título', foco() == 'dlg:t', foco())
        seq = []
        for i in range(40): pg.keyboard.press('Tab'); seq.append(foco())
        ok('Tab preso em Novo livro', all(x.startswith('dlg:') for x in seq), f'{len(set(seq))} paradas')
        pg.keyboard.press('Escape'); pg.wait_for_timeout(400); ok('Esc: foco volta ao botão Novo', pg.evaluate("() => document.activeElement.id") == 'b-novo', foco())
        pg.click('#b-dados'); pg.wait_for_timeout(500)
        seq = []
        for i in range(14): pg.keyboard.press('Tab'); seq.append(foco())
        ok('Tab preso em Seus dados', all(x.startswith('dlg:') for x in seq), f'{len(set(seq))} paradas')
        pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
        pg.keyboard.press('Tab'); pg.keyboard.press('Tab'); ok('sem camada: Tab anda pela página', foco().startswith('pagina:'), foco())
        if w <= 820:
            # folha de filtros: foco entra, Tab fica preso, Esc devolve o foco ao botão "Filtros"
            pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
            dentro = lambda: pg.evaluate("() => !!document.activeElement.closest('#f-painel')")
            aberta = lambda: pg.evaluate("() => document.querySelector('#filtros').classList.contains('folha')")
            pg.click('#f-abrir'); pg.wait_for_timeout(450)
            ok('folha de filtros: abre e recebe o foco', aberta() and dentro(), pg.evaluate("() => document.activeElement.id || document.activeElement.tagName"))
            ok('folha anunciada como diálogo', pg.evaluate("() => { const p = document.querySelector('#f-painel'); return p.getAttribute('role') === 'dialog' && p.getAttribute('aria-modal') === 'true' && p.getAttribute('aria-label') === 'Filtros'; }"))
            seq = []
            for i in range(70): pg.keyboard.press('Tab'); seq.append((dentro(), pg.evaluate("() => { const a = document.activeElement; return a.id || a.dataset.v || a.getAttribute('aria-label') || a.textContent.trim().slice(0, 14); }")))
            ok('Tab preso na folha e dá a volta', all(d for d, _ in seq) and len(set(n for _, n in seq)) < 70, f'{len(set(n for _, n in seq))} paradas')
            seq = []
            for i in range(5): pg.keyboard.press('Shift+Tab'); seq.append(dentro())
            ok('Shift+Tab preso na folha', all(seq))
            pg.keyboard.press('Escape'); pg.wait_for_timeout(400)
            ok('Esc fecha a folha e o foco volta ao botão Filtros', (not aberta()) and pg.evaluate("() => document.activeElement.id") == 'f-abrir', pg.evaluate("() => document.activeElement.id"))
            ok('atributos de diálogo saem ao fechar', pg.evaluate("() => { const p = document.querySelector('#f-painel'); return !p.hasAttribute('role') && !p.hasAttribute('tabindex'); }"))
            pg.click('#f-abrir'); pg.wait_for_timeout(450); pg.click('#f-ver'); pg.wait_for_timeout(400)
            ok('"Ver resultados" fecha e devolve o foco', (not aberta()) and pg.evaluate("() => document.activeElement.id") == 'f-abrir')
            pg.click('#f-cal'); pg.wait_for_timeout(500)
            ok('calendário abre a folha com foco na data inicial', aberta() and pg.evaluate("() => document.activeElement.id") == 'f-de', pg.evaluate("() => document.activeElement.id"))
            pg.wait_for_timeout(400); ok('…e o foco continua na data', pg.evaluate("() => document.activeElement.id") == 'f-de')
            # alargar a janela com a folha aberta: fecha e destrava a rolagem
            pg.set_viewport_size({'width': 1100, 'height': 800}); pg.wait_for_timeout(500)
            ok('alargar a janela fecha a folha e destrava a página', (not aberta()) and pg.evaluate("() => !document.documentElement.classList.contains('travado')"))
            pg.set_viewport_size({'width': w, 'height': h}); pg.wait_for_timeout(300)
        ctx.close()
    b.close()
print('FALHAS:', falhas); print('ERROS:', len(falhas))
