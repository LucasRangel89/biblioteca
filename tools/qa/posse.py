"""Estante física × biblioteca virtual: posse dos livros, gaveta, formulário e a migração do que a versão anterior salvou.

A parte da migração abre o painel antigo (tirado do histórico do Git), usa-o um pouco e entrega ao painel novo o que
ele salvou no navegador. Sem Git, ou sem aquele commit no histórico, essa parte é pulada (com aviso).

Os números esperados são um retrato do catálogo atual; se o catálogo mudar, confira as linhas FALHA e atualize.
"""
from caminhos import PAINEL_URL, RAIZ, TMP
from relogio import fixa
import json, subprocess
from playwright.sync_api import sync_playwright

ANTIGO = 'dd1ed88:biblioteca-dashboard/Biblioteca_Lucas_Dashboard.html'   # último painel antes da biblioteca virtual
CHAVE = 'biblioteca-lucas:v1'
errs = []; falhas = []
K = "() => Object.fromEntries([...document.querySelectorAll('.visao:not([hidden]) .kpi')].map(k => [k.dataset.k, {v: k.querySelector('.kpi-v b').textContent.replace(/\\u00a0/g, ' '), s: k.querySelector('.kpi-s').textContent.replace(/\\u00a0/g, ' ')}]))"
TOASTS = "() => [...document.querySelectorAll('#toasts .toast')].map(t => t.textContent.replace(/\\u00a0/g, ' ')).join(' ¦ ')"
FATOS = "() => Object.fromEntries([...document.querySelectorAll('#gaveta .fatos > div')].map(d => [d.querySelector('dt').textContent, d.querySelector('dd').innerText.replace(/\\u00a0/g, ' ').replace(/\\s+/g, ' ').trim()]))"
VIRTUAL = "() => { const s = document.querySelector('#gaveta.on #gv-virtual'); return s ? s.textContent.replace(/\\s+/g, ' ').trim() : ''; }"
OPCOES = "() => [...document.querySelectorAll('#dlg [data-f=fmt] option')].map(o => o.value + (o.selected ? '*' : ''))"


def ok(nome, cond, extra=''):
    print(('  ok   ' if cond else '  FALHA') + ' ' + nome + (' — ' + str(extra) if extra != '' else ''))
    if not cond: falhas.append(nome)


def pagina(b, salvo=None):
    """Página nova; `salvo` é o texto que o navegador já teria guardado (posto uma única vez, antes do painel carregar)."""
    ctx = b.new_context(viewport={'width': 1440, 'height': 900}, locale='pt-BR', timezone_id='America/Sao_Paulo', accept_downloads=True)
    if salvo is not None:
        ctx.add_init_script("(() => { try { if (!sessionStorage.getItem('qa-posto')) { sessionStorage.setItem('qa-posto', '1'); localStorage.setItem(%s, %s); } } catch (e) {} })()" % (json.dumps(CHAVE), json.dumps(salvo)))
    pg = ctx.new_page(); fixa(pg)
    pg.on('console', lambda m: errs.append(f'[{m.type}] {m.text}') if m.type in ('error', 'warning') else None)
    pg.on('pageerror', lambda e: errs.append(f'[pageerror] {e}'))
    return pg


def abrir(pg, busca, titulo=None):
    """Abre a gaveta do livro pela tabela da visão geral (a busca é por todos os termos)."""
    pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
    pg.fill('#p-tab-geral input[type=search]', busca); pg.wait_for_timeout(600)
    linhas = pg.locator('#p-tab-geral tbody tr[data-id]')
    alvo = linhas.filter(has=pg.locator('.tt b', has_text=titulo)).first if titulo else linhas.first
    alvo.click(); pg.wait_for_timeout(700)


with sync_playwright() as p:
    b = p.chromium.launch()

    print('PAINEL NOVO, SEM NADA SALVO')
    pg = pagina(b); pg.goto(PAINEL_URL); pg.wait_for_timeout(1200); pg.click('#aviso .pri'); pg.wait_for_timeout(200)
    k = pg.evaluate(K); ok('acervo: 97 físicos · 1.792 digitais · 24 nos dois', k['acervo']['v'] == '1.865' and k['acervo']['s'] == '97 físicos · 1.792 digitais · 24 nos dois', k['acervo'])

    abrir(pg, 'Torno do Céu'); f = pg.evaluate(FATOS); v = pg.evaluate(VIRTUAL)
    ok('só digital: formato "Digital · Biblioteca virtual", sem data', f.get('Formato') == 'Digital · Biblioteca virtual' and f.get('Adquirido em') == 'sem data' and 'Valor pago' not in f, f)
    ok('só digital: a gaveta mostra o arquivo, a pasta e o título de lá', '1 arquivo' in v and 'Pasta:' in v and 'A Curva do Sonho' in v, v[:200])

    abrir(pg, 'Fundação Asimov', 'Fundação'); f = pg.evaluate(FATOS); v = pg.evaluate(VIRTUAL)
    ok('nas duas: formato "Físico e digital" e a seção da biblioteca virtual', f.get('Formato') == 'Físico e digital' and '1 arquivo' in v, (f.get('Formato'), v[:120]))
    pg.click('#gv-acoes [data-acao=editar]'); pg.wait_for_timeout(500); o = pg.evaluate(OPCOES)
    ok('nas duas: o formulário não oferece "só físico" (o arquivo existe)', o == ['ambos*', 'ebook', 'audio'], o)
    pg.keyboard.press('Escape'); pg.wait_for_timeout(300)

    abrir(pg, 'Peste Camus', 'A Peste'); f = pg.evaluate(FATOS)
    ok('só físico: formato "Físico", sem seção da biblioteca virtual', f.get('Formato') == 'Físico' and pg.evaluate(VIRTUAL) == '', f.get('Formato'))
    pg.click('#gv-acoes [data-acao=editar]'); pg.wait_for_timeout(500); o = pg.evaluate(OPCOES)
    ok('só físico: o formulário oferece os quatro formatos', o == ['fisico*', 'ambos', 'ebook', 'audio'], o)
    pg.select_option('#dlg [data-f=fmt]', 'ambos'); pg.click('#dlg footer .pri'); pg.wait_for_timeout(800)
    f = pg.evaluate(FATOS); ok('marcar "Físico e digital" à mão', f.get('Formato') == 'Físico e digital', f.get('Formato'))
    pg.keyboard.press('Escape'); pg.wait_for_timeout(300); pg.fill('#p-tab-geral input[type=search]', ''); pg.wait_for_timeout(900)
    k = pg.evaluate(K); ok('acervo: 25 nos dois depois da edição', k['acervo']['s'] == '97 físicos · 1.793 digitais · 25 nos dois', k['acervo']['s'])
    pg.reload(); pg.wait_for_timeout(1200)
    k = pg.evaluate(K); ok('a edição sobrevive ao recarregar', k['acervo']['s'] == '97 físicos · 1.793 digitais · 25 nos dois', k['acervo']['s'])
    ok('recarregar não anuncia mudança de catálogo', 'O catálogo mudou' not in pg.evaluate(TOASTS), pg.evaluate(TOASTS))
    pg.click('#f-acervo button[data-v="ambos"]'); pg.wait_for_timeout(900)
    k = pg.evaluate(K); ok('filtro "Nas duas": 25 livros', k['acervo']['v'] == '25', k['acervo'])
    pg.click('#f-acervo button[data-v="virtual"]'); pg.wait_for_timeout(900)
    k = pg.evaluate(K); ok('filtro "Virtual": 1.793 livros, nenhuma compra', k['acervo']['v'] == '1.793' and k['investido']['v'] == 'R$ 0', (k['acervo']['v'], k['investido']['v']))
    pg.context.close()

    print('CELULAR: O FORMATO CABE NO CARTÃO')
    for largura in (390, 360, 320):
        ctx = b.new_context(viewport={'width': largura, 'height': 800}, locale='pt-BR', timezone_id='America/Sao_Paulo', is_mobile=True, has_touch=True)
        pg = ctx.new_page(); fixa(pg); pg.on('pageerror', lambda e: errs.append(f'[pageerror] {e}'))
        pg.goto(PAINEL_URL); pg.wait_for_timeout(1200); pg.click('#aviso .pri'); pg.wait_for_timeout(200)
        pg.click('#nav-m [data-ir=biblioteca]'); pg.wait_for_timeout(1000)
        r = pg.evaluate("""() => { const fs = [...document.querySelectorAll('#p-tab-biblioteca tbody td .fmt')];
            const fora = fs.filter(f => { const c = f.closest('td').getBoundingClientRect(); return [...f.getClientRects()].some(q => q.right > c.right + 1 || q.left < c.left - 1); });
            return { n: fs.length, duplos: fs.filter(f => f.querySelectorAll('.ic').length === 2).length, fora: fora.length, pagina: document.documentElement.scrollWidth - document.documentElement.clientWidth }; }""")
        ok(f'{largura} px: "Físico e digital" não invade a coluna vizinha', r['n'] >= 5 and r['duplos'] >= 1 and r['fora'] == 0 and r['pagina'] <= 0, r)
        ctx.close()

    print('MIGRAÇÃO: O QUE O PAINEL ANTERIOR SALVOU')
    try:
        antigo = subprocess.run(['git', 'show', ANTIGO], cwd=str(RAIZ), capture_output=True, check=True).stdout
    except Exception as e:
        antigo = None; print(f'  (pulado: não consegui tirar o painel antigo do Git — {type(e).__name__})')
    if antigo:
        arq = TMP / 'painel-antigo.html'; arq.write_bytes(antigo)
        pg = pagina(b); pg.goto(arq.as_uri()); pg.wait_for_timeout(1200); pg.click('#aviso .pri'); pg.wait_for_timeout(200)
        k0 = pg.evaluate(K)
        # no painel antigo: um livro meu na lista de compra e uma edição num livro da estante
        pg.click('#b-novo'); pg.wait_for_timeout(400); pg.fill('#dlg [data-f=t]', 'Zz Livro da Versão Antiga'); pg.fill('#dlg [data-f=a]', 'Autora Teste'); pg.select_option('#dlg [data-f=col]', 'desejo'); pg.fill('#dlg [data-f=alvo]', '40')
        pg.click('#dlg footer .pri'); pg.wait_for_timeout(800)
        abrir(pg, 'Fundação Asimov', 'Fundação'); pg.click('#gv-acoes [data-acao=editar]'); pg.wait_for_timeout(500); pg.fill('#dlg [data-f=pg]', '777'); pg.click('#dlg footer .pri'); pg.wait_for_timeout(800)
        salvo = pg.evaluate(f"() => localStorage.getItem('{CHAVE}')"); estado = json.loads(salvo)
        marcas = sorted({t for x in estado['livros'] for t in x.get('tags', []) if t.startswith(('ja-tenho', 'tenho-'))})
        ok('o painel antigo salvou 645 livros, com #ja-tenho e sem assinatura de catálogo', len(estado['livros']) == 645 and marcas == ['ja-tenho'] and 'cat' not in estado, (len(estado['livros']), marcas, k0['acervo']))
        pg.keyboard.press('Escape'); pg.wait_for_timeout(300); pg.click('#b-dados'); pg.wait_for_timeout(400)
        with pg.expect_download() as d: pg.click('#dlg [data-x=exportar]')
        d.value.save_as(f'{TMP}/bk-antigo.json')
        pg.context.close()

        pg = pagina(b, salvo); pg.goto(PAINEL_URL); pg.wait_for_timeout(1500); t = pg.evaluate(TOASTS)
        ok('aviso: 1.656 livros entraram e as edições foram mantidas', 'O catálogo mudou: 1.656 livros entraram.' in t and 'O que você editou no painel foi mantido.' in t, t)
        if pg.locator('#aviso .pri').is_visible(): pg.click('#aviso .pri'); pg.wait_for_timeout(200)
        k = pg.evaluate(K); ok('acervo migrado: 97 físicos · 1.792 digitais · 24 nos dois', k['acervo']['v'] == '1.865' and k['acervo']['s'] == '97 físicos · 1.792 digitais · 24 nos dois', k['acervo'])
        abrir(pg, 'Zz Livro da Versão Antiga'); f = pg.evaluate(FATOS)
        ok('o livro que eu tinha criado continua na lista de compra, com o alvo', pg.locator('#gaveta.on').count() == 1 and 'R$ 40,00' in f.get('Preço-alvo', ''), f)
        abrir(pg, 'Fundação Asimov', 'Fundação'); f = pg.evaluate(FATOS); v = pg.evaluate(VIRTUAL)
        ok('o livro que eu tinha editado mantém a edição e ganha o exemplar digital', f.get('Páginas') == '777' and f.get('Formato') == 'Físico e digital' and '1 arquivo' in v, f)
        pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
        novo = json.loads(pg.evaluate(f"() => localStorage.getItem('{CHAVE}')"))
        marcas = sorted({t for x in novo['livros'] for t in x.get('tags', []) if t.startswith(('ja-tenho', 'tenho-'))})
        ok('o estado regravado tem 2.301 livros, a assinatura do catálogo e nenhum #ja-tenho', len(novo['livros']) == 2301 and marcas == ['tenho-digital', 'tenho-fisico'] and bool(novo.get('cat')), (len(novo['livros']), marcas, novo.get('cat')))
        pg.reload(); pg.wait_for_timeout(1500); t = pg.evaluate(TOASTS)
        ok('ao reabrir, a migração não se repete', 'O catálogo mudou' not in t, t)
        k = pg.evaluate(K); ok('e os números continuam os mesmos', k['acervo']['v'] == '1.865' and k['acervo']['s'] == '97 físicos · 1.792 digitais · 24 nos dois', k['acervo'])
        pg.context.close()

        print('MIGRAÇÃO: BACKUP EXPORTADO PELO PAINEL ANTERIOR')
        pg = pagina(b); pg.goto(PAINEL_URL); pg.wait_for_timeout(1200); pg.click('#aviso .pri'); pg.wait_for_timeout(200)
        pg.click('#b-dados'); pg.wait_for_timeout(400); pg.set_input_files('#arq', f'{TMP}/bk-antigo.json'); pg.wait_for_timeout(800)
        txt = pg.inner_text('#dlg.on').replace('\u00a0', ' ').replace('\n', ' ')
        ok('a confirmação reconhece o backup antigo (645 livros)', '645 livros' in txt, txt[:160])
        pg.click('#dlg footer .pri'); pg.wait_for_timeout(1200); t = pg.evaluate(TOASTS)
        ok('importado, com o aviso dos 1.656 livros que entraram', 'Backup importado. O catálogo mudou: 1.656 livros entraram.' in t, t)
        for _ in range(2): pg.keyboard.press('Escape'); pg.wait_for_timeout(150)
        k = pg.evaluate(K); ok('acervo depois de importar: 97 físicos · 1.792 digitais · 24 nos dois', k['acervo']['v'] == '1.865' and k['acervo']['s'] == '97 físicos · 1.792 digitais · 24 nos dois', k['acervo'])
        abrir(pg, 'Fundação Asimov', 'Fundação'); f = pg.evaluate(FATOS)
        ok('a edição feita no painel antigo veio no backup', f.get('Páginas') == '777' and f.get('Formato') == 'Físico e digital', f)
        abrir(pg, 'Zz Livro da Versão Antiga'); f = pg.evaluate(FATOS)
        ok('o livro criado no painel antigo veio no backup', pg.locator('#gaveta.on').count() == 1 and 'R$ 40,00' in f.get('Preço-alvo', ''), f)
        pg.context.close()
    b.close()
print('FALHAS:', falhas); print('ERROS:', len(errs) + len(falhas)); [print('  ', x[:300]) for x in errs[:10]]
