"""Capturas que faltavam: "Cópia recuperada" em Seus dados, painel sem dados de exemplo (1440) e cartões de tabela no tema escuro (390)."""
from caminhos import PAINEL, PAINEL_URL, TMP
from relogio import fixa
import pathlib
from playwright.sync_api import sync_playwright
URL = PAINEL_URL
errs = []
def gerar_teste_falha():
    s = PAINEL.read_text(encoding='utf-8')
    alvo = "  irPara(S.visao, true);\n  document.documentElement.classList.add('pronto');"
    assert s.count(alvo) == 1
    s = s.replace(alvo, "  if ((localStorage.getItem(CHAVE) || '').includes('marcador-de-erro')) throw new Error('falha simulada');\n" + alvo)
    pathlib.Path(f'{TMP}/teste-falha.html').write_text(s, encoding='utf-8')
gerar_teste_falha()
def pagina(b, w, h, tema='light'):
    ctx = b.new_context(viewport={'width': w, 'height': h}, color_scheme=tema, locale='pt-BR', timezone_id='America/Sao_Paulo')
    pg = ctx.new_page(); fixa(pg)
    pg.on('console', lambda m: errs.append(f'[{m.type}] {m.text}') if m.type in ('error', 'warning') else None)
    return pg
with sync_playwright() as p:
    b = p.chromium.launch()
    # a) cópia recuperada
    for w, h, tema, nome in [(1440, 900, 'light', 'falha-1440'), (390, 844, 'dark', 'falha-390e')]:
        pg = pagina(b, w, h, tema)
        pg.goto((TMP / 'teste-falha.html').as_uri()); pg.wait_for_timeout(1000); pg.click('#aviso .pri'); pg.wait_for_timeout(200)
        pg.click('#b-novo'); pg.wait_for_timeout(400); pg.fill('#dlg [data-f=t]', 'Zz Meu Livro'); pg.click('#dlg footer .pri'); pg.wait_for_timeout(700); pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
        pg.evaluate("() => { const o = JSON.parse(localStorage.getItem('biblioteca-lucas:v1')); o.livros[0].obs = 'marcador-de-erro'; localStorage.setItem('biblioteca-lucas:v1', JSON.stringify(o)); }")
        pg.reload(); pg.wait_for_timeout(1800); pg.screenshot(path=f'{TMP}/shots/{nome}-a.png')
        pg.wait_for_timeout(7000)   # espera o toast sair
        pg.click('#b-dados'); pg.wait_for_timeout(600); pg.screenshot(path=f'{TMP}/shots/{nome}-b.png')
        print(nome, '| seções:', pg.evaluate("() => [...document.querySelectorAll('#dlg .dados h3')].map(h => h.textContent)"), '| rolagem do diálogo:', pg.evaluate("() => { const c = document.querySelector('#dlg .dlg-c, #dlg .dlg-cx'); return [c.scrollHeight, c.clientHeight]; }"))
        pg.context.close()
    # b) sem dados de exemplo, 1440
    pg = pagina(b, 1440, 900)
    pg.goto(URL); pg.wait_for_timeout(1000); pg.click('#aviso .pri'); pg.wait_for_timeout(200)
    pg.click('#b-dados'); pg.wait_for_timeout(300); pg.click('#dlg [data-x=limpar]'); pg.wait_for_timeout(300); pg.click('#dlg footer .pri'); pg.wait_for_timeout(700); pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
    for v in ['geral', 'biblioteca', 'recs', 'desejos', 'precos']:
        pg.click(f'#nav [data-ir={v}]'); pg.wait_for_timeout(1100); pg.screenshot(path=f'{TMP}/shots/limpo-{v}.png', full_page=True)
    pg.context.close()
    # c) cartões de tabela no escuro, 390
    pg = pagina(b, 390, 844, 'dark')
    pg.goto(URL); pg.wait_for_timeout(1000); pg.click('#aviso .pri'); pg.wait_for_timeout(200)
    for v in ['geral', 'biblioteca', 'recs', 'desejos', 'precos']:
        pg.evaluate(f"() => document.querySelector('#nav-m [data-ir={v}]').click()"); pg.wait_for_timeout(900)
        pg.evaluate(f"() => document.querySelector('#p-tab-{v}').scrollIntoView({{ block: 'start' }})"); pg.wait_for_timeout(300)
        pg.evaluate("() => window.scrollBy(0, -70)"); pg.wait_for_timeout(200)
        pg.screenshot(path=f'{TMP}/shots/esc-tab-{v}.png')
    pg.context.close()
    b.close()
print('ERROS:', len(errs)); [print('  ', x[:300]) for x in errs[:10]]
