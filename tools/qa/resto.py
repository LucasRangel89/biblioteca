"""Fluxos pouco usados: excluir livro, período personalizado invertido / no futuro, importação com registros ilegíveis."""
from caminhos import PAINEL_URL, TMP
from relogio import fixa
import json
from playwright.sync_api import sync_playwright
URL = PAINEL_URL
errs = []; falhas = []
TOAST = "() => { const t = [...document.querySelectorAll('#toasts .toast')].map(t => t.textContent); return (t[t.length - 1] || '').replace(/\\u00a0/g, ' '); }"
K = "() => Object.fromEntries([...document.querySelectorAll('.visao:not([hidden]) .kpi')].map(k => [k.dataset.k, k.querySelector('.kpi-v b').textContent.replace(/\\u00a0/g, ' ')]))"
INFO = "v => (document.querySelector('#p-tab-' + v + ' .tb-info') || {}).textContent || ''"
mil = lambda n: f'{n:,}'.replace(',', '.')   # 2301 → "2.301", como o painel escreve
def confere(nome, ok, extra=''):
    print(('ok   ' if ok else 'FALHA') + ' ' + nome + (' — ' + str(extra) if extra != '' else ''))
    if not ok: falhas.append(nome)
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={'width': 1440, 'height': 900}, locale='pt-BR', timezone_id='America/Sao_Paulo', accept_downloads=True)
    pg = ctx.new_page(); fixa(pg)
    pg.on('console', lambda m: errs.append(f'[{m.type}] {m.text}') if m.type in ('error', 'warning') else None)
    pg.on('pageerror', lambda e: errs.append(f'[pageerror] {e}'))
    pg.goto(URL); pg.wait_for_timeout(1000); pg.click('#aviso .pri'); pg.wait_for_timeout(200)

    print('— excluir livro')
    k0 = pg.evaluate(K)
    pg.click('#b-novo'); pg.wait_for_timeout(400)
    pg.fill('#dlg [data-f=t]', 'Zz Para Excluir'); pg.fill('#dlg [data-f=a]', 'Autora Teste'); pg.select_option('#dlg [data-f=col]', 'desejo'); pg.fill('#dlg [data-f=alvo]', '40')
    pg.click('#dlg footer .pri'); pg.wait_for_timeout(800)
    confere('gaveta do livro novo aberta', pg.evaluate("() => document.querySelector('#gaveta.on h2, #gaveta.on .gv-t').textContent").startswith('Zz Para Excluir'))
    confere('livro do usuário tem botão Excluir', pg.locator('#gv-acoes [data-acao=excluir]').count() == 1)
    pg.click('#gv-acoes [data-acao=excluir]'); pg.wait_for_timeout(400)
    confere('pede confirmação', 'Zz Para Excluir' in pg.inner_text('#dlg.on'), pg.inner_text('#dlg.on h2'))
    pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
    confere('Esc cancela e mantém a gaveta', pg.evaluate("() => !document.querySelector('#dlg').classList.contains('on') && document.querySelector('#gaveta').classList.contains('on')"))
    pg.click('#gv-acoes [data-acao=excluir]'); pg.wait_for_timeout(400); pg.locator('#dlg.on').screenshot(path=f'{TMP}/shots/dlg-excluir.png'); pg.click('#dlg footer .perigo'); pg.wait_for_timeout(800)
    confere('toast "Livro excluído."', 'Livro excluído' in pg.evaluate(TOAST), pg.evaluate(TOAST))
    confere('gaveta fechou', pg.evaluate("() => !document.querySelector('#gaveta').classList.contains('on')"))
    confere('KPIs voltaram ao que eram', pg.evaluate(K) == k0, pg.evaluate(K))
    pg.fill('#p-tab-geral input[type=search]', 'Zz Para Excluir'); pg.wait_for_timeout(500)
    confere('não aparece mais na tabela', pg.locator('#p-tab-geral tbody tr[data-id]').count() == 0, pg.evaluate(INFO, 'geral'))
    pg.reload(); pg.wait_for_timeout(1000)
    pg.fill('#p-tab-geral input[type=search]', 'Zz Para Excluir'); pg.wait_for_timeout(500)
    confere('continua excluído depois de recarregar', pg.locator('#p-tab-geral tbody tr[data-id]').count() == 0)
    pg.fill('#p-tab-geral input[type=search]', ''); pg.wait_for_timeout(400)
    pg.locator('#p-tab-geral tbody tr[data-id]').first.click(); pg.wait_for_timeout(500)
    confere('livro do catálogo não tem botão Excluir', pg.locator('#gv-acoes [data-acao=excluir]').count() == 0, pg.evaluate("() => document.querySelector('#gaveta.on h2, #gaveta.on .gv-t').textContent")[:40])
    pg.keyboard.press('Escape'); pg.wait_for_timeout(300)

    print('— período personalizado (no fim de "Mais filtros")')
    def mais():
        if not pg.is_visible('#pop-mais'): pg.click('#pw-mais .pop-b'); pg.wait_for_timeout(250)
    mais(); pg.click('#f-cal'); pg.wait_for_timeout(400)
    pg.fill('#f-de', '2026-10-01'); pg.dispatch_event('#f-de', 'change'); pg.fill('#f-ate', '2026-08-01'); pg.dispatch_event('#f-ate', 'change'); pg.wait_for_timeout(600)
    v = pg.evaluate("() => [document.querySelector('#f-de').value, document.querySelector('#f-ate').value]")
    confere('datas invertidas são trocadas', v == ['2026-08-01', '2026-10-01'], v)
    k1 = pg.evaluate(K); confere('KPIs calculados no intervalo', k1.get('acervo') not in (None, ''), k1)
    pg.fill('#f-ate', '2027-03-15'); pg.dispatch_event('#f-ate', 'change'); pg.wait_for_timeout(600)
    v = pg.evaluate("() => [document.querySelector('#f-de').value, document.querySelector('#f-ate').value]")
    confere('data futura é limitada a hoje', v == ['2026-08-01', '2026-11-09'], v)
    pg.fill('#f-de', '2026-11-09'); pg.dispatch_event('#f-de', 'change'); pg.wait_for_timeout(600)
    v = pg.evaluate("() => [document.querySelector('#f-de').value, document.querySelector('#f-ate').value]")
    confere('intervalo de um único dia funciona', v == ['2026-11-09', '2026-11-09'] and pg.evaluate(K).get('acervo') is not None, [v, pg.evaluate(K)])
    pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
    for vis in ['biblioteca', 'recs', 'financas', 'desejos', 'precos', 'geral']:
        pg.click(f'#nav [data-ir={vis}]'); pg.wait_for_timeout(500)
    mais(); pg.fill('#f-de', ''); pg.dispatch_event('#f-de', 'change'); pg.wait_for_timeout(300)
    pg.wait_for_timeout(500); confere('data apagada não quebra nada', pg.evaluate(K).get('acervo') is not None)
    mais(); pg.click('#f-periodo button[data-v="tudo"]'); pg.wait_for_timeout(900)   # a contagem dos KPIs dura 550 ms
    pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
    confere('volta para Tudo', pg.evaluate(K) == k0, pg.evaluate(K))

    print('— importação com registros ilegíveis')
    pg.click('#b-dados'); pg.wait_for_timeout(400)
    with pg.expect_download() as d: pg.click('#dlg [data-x=exportar]')
    d.value.save_as(f'{TMP}/bk-bom.json'); pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
    o = json.load(open(f'{TMP}/bk-bom.json', encoding='utf-8')); n = len(o['livros'])
    lixo = [None, 42, 'texto', [], {}, {'t': ''}, {'t': 123, 'a': 'x'}, {'a': 'sem título'}]
    torto = {'t': 'Zz Registro Torto', 'a': 99, 'col': 'inexistente', 'leit': {}, 'px': {'Loja X': [[1, 'caro'], 'x', [20766, 55.5, 1], [None, 3]], '': [[1, 2]], 'Y': 'não é lista'}, 'alvo': 'quarenta', 'capa': -3, 'prio': 77, 'tags': 'solta', 'adq': 'ontem', 'pg': 1e12, 'nota': 'dez', 'id': '<script>'}
    o['livros'] = lixo[:4] + o['livros'][:300] + lixo[4:] + o['livros'][300:] + [torto]
    json.dump(o, open(f'{TMP}/bk-misto.json', 'w', encoding='utf-8'), ensure_ascii=False)
    pg.click('#b-dados'); pg.wait_for_timeout(400); pg.set_input_files('#arq', f'{TMP}/bk-misto.json'); pg.wait_for_timeout(800)
    txt = pg.inner_text('#dlg.on').replace('\u00a0', ' ')
    confere('confirmação informa os ignorados', f'{len(lixo)} registros ilegíveis serão ignorados' in txt and f'{mil(n + 1)} livros' in txt, txt.replace('\n', ' ')[:200])
    pg.click('#dlg footer .pri'); pg.wait_for_timeout(1000)
    confere('toast "Backup importado."', 'Backup importado' in pg.evaluate(TOAST), pg.evaluate(TOAST))
    for _ in range(2): pg.keyboard.press('Escape'); pg.wait_for_timeout(150)
    info = pg.evaluate(INFO, 'geral'); confere('tabela com um livro a mais (o torto, saneado)', f'de {mil(n + 1)} livros' in info, info)
    pg.fill('#p-tab-geral input[type=search]', 'Zz Registro'); pg.wait_for_timeout(500)
    confere('registro torto aparece', pg.locator('#p-tab-geral tbody tr[data-id]').count() == 1)
    pg.locator('#p-tab-geral tbody tr[data-id]').first.click(); pg.wait_for_timeout(600)
    gav = pg.inner_text('#gaveta.on').replace('\u00a0', ' ')
    confere('gaveta do registro torto abre sem erro', 'Zz Registro Torto' in gav, gav.replace('\n', ' ')[:260])
    confere('cotação válida do registro torto foi aproveitada', 'R$ 55,50' in gav)
    pg.keyboard.press('Escape'); pg.wait_for_timeout(300); pg.fill('#p-tab-geral input[type=search]', ''); pg.wait_for_timeout(300)
    for vis in ['biblioteca', 'recs', 'desejos', 'precos', 'geral']:
        pg.click(f'#nav [data-ir={vis}]'); pg.wait_for_timeout(500)
    pg.reload(); pg.wait_for_timeout(1000)
    info = pg.evaluate(INFO, 'geral'); confere('dados importados sobrevivem ao recarregar', f'de {mil(n + 1)} livros' in info, info)
    b.close()
print('FALHAS:', falhas); print('ERROS:', len(errs)); [print('  ', e[:300]) for e in errs[:10]]
