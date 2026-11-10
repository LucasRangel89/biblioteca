from caminhos import PAINEL, PAINEL_URL, TMP
from relogio import fixa
import json, datetime
from playwright.sync_api import sync_playwright
def gerar_teste_falha():
    """Cópia do painel com uma falha proposital na abertura, para exercitar a rede de segurança."""
    import pathlib
    s = PAINEL.read_text(encoding='utf-8')
    alvo = "  irPara(S.visao, true);\n  document.documentElement.classList.add('pronto');"
    assert s.count(alvo) == 1
    s = s.replace(alvo, "  if ((localStorage.getItem(CHAVE) || '').includes('marcador-de-erro')) throw new Error('falha simulada');\n" + alvo)
    pathlib.Path(f'{TMP}/teste-falha.html').write_text(s, encoding='utf-8')
gerar_teste_falha()
URL = PAINEL_URL
errs = []
K = "() => Object.fromEntries([...document.querySelectorAll('.visao:not([hidden]) .kpi')].map(k => [k.dataset.k, k.querySelector('.kpi-v b').textContent.replace(/\\u00a0/g, ' ')]))"
TOAST = "() => [...document.querySelectorAll('#toasts .toast')].map(t => t.textContent).join(' || ')"
def exportar(pg, nome):
    pg.click('#b-dados'); pg.wait_for_timeout(400)
    with pg.expect_download() as d: pg.click('#dlg [data-x=exportar]')
    d.value.save_as(nome); pg.click('#dlg header [data-fechar]'); pg.wait_for_timeout(300)
    return json.load(open(nome, encoding='utf-8'))
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={'width': 1440, 'height': 900}, locale='pt-BR', timezone_id='America/Sao_Paulo', accept_downloads=True)
    pg = ctx.new_page(); fixa(pg)
    pg.on('console', lambda m: errs.append(f'[{m.type}] {m.text}') if m.type in ('error', 'warning') else None)
    pg.on('pageerror', lambda e: errs.append(f'[pageerror] {e}'))
    print('a) ida e volta do estado salvo (o saneamento não pode alterar dados válidos)')
    pg.clock.set_fixed_time(datetime.datetime.fromisoformat('2026-11-09T10:00:00-03:00'))
    pg.goto(URL); pg.wait_for_timeout(1200)
    # algumas edições para ter de tudo: compra, leitura, cotação própria com loja nova, livro novo
    pg.click('#nav [data-ir=desejos]'); pg.wait_for_timeout(800); pg.click('#p-tab-desejos tbody tr'); pg.wait_for_timeout(500); pg.click('#gaveta [data-acao=comprei]'); pg.wait_for_timeout(400); pg.click('#dlg footer .pri'); pg.wait_for_timeout(700); pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
    pg.click('#nav [data-ir=precos]'); pg.wait_for_timeout(800); pg.select_option('#p-cotacao select[data-c=loja]', '__outra'); pg.fill('#p-cotacao input[data-c=outra]', 'Sebo & Cia "Teste"'); pg.fill('#p-cotacao input[data-c=preco]', '27,45'); pg.click('#p-cotacao [data-c=ok]'); pg.wait_for_timeout(700)
    pg.click('#b-novo'); pg.wait_for_timeout(400); pg.fill('#dlg [data-f=t]', 'Livro <i>x</i> & "aspas"'); pg.fill('#dlg [data-f=tags]', 'teste-a teste-b'); pg.click('#dlg footer .pri'); pg.wait_for_timeout(700); pg.keyboard.press('Escape'); pg.wait_for_timeout(900)
    a1 = exportar(pg, f'{TMP}/a1.json'); pg.reload(); pg.wait_for_timeout(1300); a2 = exportar(pg, f'{TMP}/a2.json')
    print('   livros iguais após recarregar:', a1['livros'] == a2['livros'], '| n =', len(a1['livros']), '| exemplos/criadoEm:', (a1['exemplos'], a1['criadoEm']) == (a2['exemplos'], a2['criadoEm']), '| cfg:', a1['cfg'] == a2['cfg'])
    if a1['livros'] != a2['livros']:
        for x, y in zip(a1['livros'], a2['livros']):
            if x != y: print('   DIF:', {k: (x.get(k), y.get(k)) for k in set(x) | set(y) if x.get(k) != y.get(k) and k != 'px'}); break
    pg.click('#b-dados'); pg.wait_for_timeout(300); pg.set_input_files('#arq', f'{TMP}/a1.json'); pg.wait_for_timeout(600); print('   importar:', pg.inner_text('#dlg .dlg-msg').replace('\n', ' ')[:160]); pg.click('#dlg footer .pri'); pg.wait_for_timeout(1000)
    a3 = exportar(pg, f'{TMP}/a3.json'); print('   livros iguais após importar:', a1['livros'] == a3['livros'])
    print('b) mesmo navegador, 41 dias depois (há edições: não regenera)')
    k0 = None
    pg.clock.set_fixed_time(datetime.datetime.fromisoformat('2026-12-20T10:00:00-03:00')); pg.reload(); pg.wait_for_timeout(1300)
    for v in ['geral', 'biblioteca', 'recs', 'desejos', 'precos']:
        pg.click(f'#nav [data-ir={v}]'); pg.wait_for_timeout(900); print('  ', v, json.dumps(pg.evaluate(K), ensure_ascii=False))
    print('   Atualizado:', pg.evaluate("() => [...document.querySelectorAll('#p-tab-precos tbody tr')].slice(0, 3).map(r => r.lastElementChild.innerText.replace(/\\n/g, ' · '))"), '| alertas:', pg.inner_text('#p-alertas .card-s'), '| cot:', pg.evaluate("() => document.querySelector('.visao:not([hidden]) .kpi[data-k=cot] .kpi-s').textContent"))
    pg.click('#nav [data-ir=geral]'); pg.wait_for_timeout(800); print('   eixo x termina em:', pg.evaluate("() => { const t = document.querySelectorAll('#p-evolucao .g-x text'); return t[t.length - 1].textContent; }"), '| cesta sub:', pg.evaluate("() => document.querySelector('.kpi[data-k=cesta] .kpi-s').textContent"))
    a4 = exportar(pg, f'{TMP}/a4.json'); print('   dados preservados:', a4['livros'] == a1['livros'], '| criadoEm:', a4['criadoEm'] == a1['criadoEm'])
    print('c) rede de segurança na abertura')
    pg2 = ctx.new_page(); fixa(pg2); pg2.on('pageerror', lambda e: print('   (pageerror esperado?)', str(e)[:80]))
    pg2.goto((TMP / 'teste-falha.html').as_uri()); pg2.wait_for_timeout(1200)
    pg2.evaluate("() => { const o = JSON.parse(localStorage.getItem('biblioteca-lucas:v1')); o.livros[0].obs = 'marcador-de-erro'; localStorage.setItem('biblioteca-lucas:v1', JSON.stringify(o)); }")
    pg2.reload(); pg2.wait_for_timeout(2500)
    y = pg2.evaluate('() => [Math.round(scrollY), history.scrollRestoration]'); print('   rolagem após recomeçar:', y)
    if y != [0, 'auto']: errs.append(f'rede de segurança: página abriu rolada ou sem restaurar a rolagem padrão: {y}')
    print('   título:', pg2.inner_text('#titulo .t-l'), '| toast:', pg2.evaluate(TOAST)[:150], '| KPIs:', pg2.evaluate(K))
    print('   chaves:', pg2.evaluate("() => Object.keys(localStorage).map(k => k + ' (' + localStorage.getItem(k).length + ')')"))
    pg2.click('#b-dados'); pg2.wait_for_timeout(400); print('   seções em Seus dados:', pg2.evaluate("() => [...document.querySelectorAll('#dlg .dados h3')].map(h => h.textContent)"))
    with pg2.expect_download() as d: pg2.click('#dlg [data-x=falha-baixar]')
    d.value.save_as(f'{TMP}/copia.json'); c = json.load(open(f'{TMP}/copia.json', encoding='utf-8')); print('   cópia baixada:', d.value.suggested_filename, len(c['livros']), 'livros; contém as edições:', any(x['t'].startswith('Livro <i>') for x in c['livros']))
    pg2.click('#dlg [data-x=falha-descartar]'); pg2.wait_for_timeout(500); print('   após descartar:', pg2.evaluate("() => Object.keys(localStorage)"), '|', pg2.evaluate(TOAST)[-40:])
    b.close()
print('ERROS:', len(errs)); [print('  ', x[:500]) for x in errs[:20]]
