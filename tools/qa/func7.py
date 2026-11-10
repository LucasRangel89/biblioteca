from caminhos import PAINEL_URL, TMP
from relogio import fixa
import json, datetime
from playwright.sync_api import sync_playwright
import pathlib
pathlib.Path(f'{TMP}/ruim.txt').write_text('isto não é um backup', encoding='utf-8')
pathlib.Path(f'{TMP}/ruim.json').write_text('{"app":"outro","livros":[]}', encoding='utf-8')
URL = PAINEL_URL
errs = []
K = "() => Object.fromEntries([...document.querySelectorAll('.visao:not([hidden]) .kpi')].map(k => [k.dataset.k, k.querySelector('.kpi-v b').textContent.replace(/\\u00a0/g, ' ') + ' ¦ ' + k.querySelector('.kpi-s').textContent]))"
TOAST = "() => { const t = [...document.querySelectorAll('#toasts .toast')].map(t => t.textContent); return t[t.length - 1] || ''; }"
def novo(p, quando=None, estado=None):
    b = p.chromium.launch()
    ctx = b.new_context(viewport={'width': 1440, 'height': 900}, locale='pt-BR', timezone_id='America/Sao_Paulo', storage_state=estado)
    pg = ctx.new_page(); fixa(pg)
    pg.on('console', lambda m: errs.append(f'[{m.type}] {m.text}') if m.type in ('error', 'warning') else None)
    pg.on('pageerror', lambda e: errs.append(f'[pageerror] {e}'))
    if quando: pg.clock.set_fixed_time(quando)
    return b, ctx, pg
def passeio(pg, rot):
    for v in ['geral', 'biblioteca', 'recs', 'desejos', 'precos']:
        pg.click(f'#nav [data-ir={v}]'); pg.wait_for_timeout(900)
        k = pg.evaluate(K); print(f'   {rot} {v}:', json.dumps({a: k[a].split(' ¦ ')[0] for a in k}, ensure_ascii=False))
    return k
with sync_playwright() as p:
    print('1) demo intocado aberto em outro dia (regenera para a data)')
    for quando in ['2026-12-15T10:00:00-03:00', '2027-06-01T23:30:00-03:00', '2028-02-29T08:00:00-03:00']:
        b, ctx, pg = novo(p, datetime.datetime.fromisoformat(quando)); pg.goto(URL); pg.wait_for_timeout(1300)
        print('  ', quando, '| eixo x do gráfico termina em:', pg.evaluate("() => { const t = document.querySelectorAll('#p-evolucao .g-x text'); return t[t.length - 1].textContent; }"), '| status:', pg.inner_text('#st-dados').replace('\n', ' / '))
        k = passeio(pg, '  '); print('     cot:', k['cot']); b.close()
    print('2) usuário mexeu em 09/11 e volta em 20/12 (não regenera: os dados dele ficam como estavam)')
    # mesmo contexto do navegador (o armazenamento de páginas file:// não viaja por storage_state): muda só o relógio e recarrega
    b, ctx, pg = novo(p, datetime.datetime.fromisoformat('2026-11-09T10:00:00-03:00')); pg.goto(URL); pg.wait_for_timeout(1200)
    pg.click('#nav [data-ir=desejos]'); pg.wait_for_timeout(800); pg.click('#p-tab-desejos tbody tr'); pg.wait_for_timeout(500); pg.click('#gaveta [data-acao=comprei]'); pg.wait_for_timeout(400); pg.click('#dlg footer .pri'); pg.wait_for_timeout(1200)
    pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
    antes = pg.evaluate(K)
    pg.clock.set_fixed_time(datetime.datetime.fromisoformat('2026-12-20T10:00:00-03:00')); pg.reload(); pg.wait_for_timeout(1300)
    k = passeio(pg, '  '); print('     precos:', json.dumps(k, ensure_ascii=False))
    atual = pg.evaluate("() => [...document.querySelectorAll('#p-tab-precos tbody tr')].slice(0, 2).map(r => r.lastElementChild.innerText.replace(/\\n/g, ' · '))")
    print('     coluna Atualizado:', atual, '| alertas:', pg.inner_text('#p-alertas .card-s'))
    pg.click('#nav [data-ir=desejos]'); pg.wait_for_timeout(800); depois = pg.evaluate(K)
    if antes['itens'] != depois['itens'] or not all('há 41 dias' in x for x in atual): errs.append(f'[teste] dados do usuário não foram preservados: {antes["itens"]} -> {depois["itens"]} | {atual}')
    else: print('     preservado: lista com', depois['itens'].split(' ¦ ')[0], 'itens (um a menos que os 26 do exemplo) e cotações paradas em 09/11')
    b.close()
    print('3) armazenamento corrompido / mínimo')
    for rot, val in [('JSON quebrado', '{ruim'), ('registro mínimo', json.dumps({'app': 'biblioteca-lucas', 'v': 1, 'livros': [{'id': 'u1', 't': 'Só um livro'}], 'exemplos': False})), ('outro app', json.dumps({'app': 'x', 'livros': [1, 2]})), ('livros com lixo', json.dumps({'app': 'biblioteca-lucas', 'livros': [None, 5, 'a', {'t': 'Sem id', 'px': {'Amazon': 'xx'}, 'tags': 'F NF'}], 'cfg': {'tema': 7, 'ui': 'x', 'tam': {'geral': 'a'}, 'visao': 'nada'}}))]:
        b, ctx, pg = novo(p); pg.goto(URL); pg.wait_for_timeout(600)
        pg.evaluate("v => localStorage.setItem('biblioteca-lucas:v1', v)", val); pg.reload(); pg.wait_for_timeout(1300)
        n0 = len(errs)
        try:
            k = pg.evaluate(K); print(f'   {rot}: título={pg.inner_text("#titulo .t-l")!r} KPIs={json.dumps({a: k[a].split(" ¦ ")[0] for a in k}, ensure_ascii=False)}')
            for v in ['biblioteca', 'recs', 'desejos', 'precos']: pg.click(f'#nav [data-ir={v}]'); pg.wait_for_timeout(700)
        except Exception as e: print(f'   {rot}: EXCEÇÃO {str(e)[:200]}')
        b.close()
    print('4) importar arquivos inválidos')
    b, ctx, pg = novo(p); pg.goto(URL); pg.wait_for_timeout(1000); pg.click('#b-dados'); pg.wait_for_timeout(400)
    for arq in [f'{TMP}/ruim.txt', f'{TMP}/ruim.json']:
        pg.set_input_files('#arq', arq); pg.wait_for_timeout(700); print('  ', arq, '->', pg.evaluate(TOAST), '| dlg:', pg.inner_text('#dlg h2'))
    b.close()
print('ERROS:', len(errs)); [print('  ', x[:500]) for x in errs[:20]]
