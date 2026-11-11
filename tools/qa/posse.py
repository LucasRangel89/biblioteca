"""Estante física × biblioteca virtual: posse dos livros, gaveta, formulário e a migração do que a versão anterior salvou.

A parte da migração abre o painel antigo (tirado do histórico do Git), usa-o um pouco e entrega ao painel novo o que
ele salvou no navegador. Sem Git, ou sem aquele commit no histórico, essa parte é pulada (com aviso).

Os números esperados são um retrato do catálogo atual; se o catálogo mudar, confira as linhas FALHA e atualize.
"""
from caminhos import PAINEL_URL, RAIZ, TMP
from relogio import fixa, fonte_usada
import json, subprocess
from playwright.sync_api import sync_playwright

ANTIGO = 'dd1ed88:biblioteca-dashboard/Biblioteca_Lucas_Dashboard.html'   # último painel antes da biblioteca virtual
ANTERIOR = 'a69fa00:Biblioteca_Lucas_Dashboard.html'                      # painel de antes das correções de título e autor na estante
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
        # a marca de "já posto" fica em dois lugares (sessionStorage e window.name): se uma se perder numa recarga, a outra segura
        ctx.add_init_script("(() => { try { if (!sessionStorage.getItem('qa-posto') && window.name !== 'qa-posto') { localStorage.setItem(%s, %s); } sessionStorage.setItem('qa-posto', '1'); window.name = 'qa-posto'; } catch (e) {} })()" % (json.dumps(CHAVE), json.dumps(salvo)))
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
    k = pg.evaluate(K); ok('acervo: 100 físicos · 2.049 digitais · 25 nos dois', k['acervo']['v'] == '2.124' and k['acervo']['s'] == '100 físicos · 2.049 digitais · 25 nos dois', k['acervo'])

    abrir(pg, 'Mal-Estar Civilização Freud'); f = pg.evaluate(FATOS); v = pg.evaluate(VIRTUAL)      # o arquivo é de outra tradução: "O Mal-Estar na Cultura"
    ok('só digital: formato "Digital · Biblioteca virtual", sem data', f.get('Formato') == 'Digital · Biblioteca virtual' and f.get('Adquirido em') == 'sem data' and 'Valor pago' not in f, f)
    ok('só digital: a gaveta mostra o arquivo, a pasta e o título de lá', '1 arquivo' in v and 'Pasta:' in v and 'O Mal-Estar na Cultura' in v, v[:200])

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
    k = pg.evaluate(K); ok('acervo: 26 nos dois depois da edição', k['acervo']['s'] == '100 físicos · 2.050 digitais · 26 nos dois', k['acervo']['s'])
    pg.reload(); pg.wait_for_timeout(1200)
    k = pg.evaluate(K); ok('a edição sobrevive ao recarregar', k['acervo']['s'] == '100 físicos · 2.050 digitais · 26 nos dois', k['acervo']['s'])
    ok('recarregar não anuncia mudança de catálogo', 'O catálogo mudou' not in pg.evaluate(TOASTS), pg.evaluate(TOASTS))
    pg.click('#f-acervo button[data-v="ambos"]'); pg.wait_for_timeout(900)
    k = pg.evaluate(K); ok('filtro "Nas duas": 26 livros', k['acervo']['v'] == '26', k['acervo'])
    pg.click('#f-acervo button[data-v="virtual"]'); pg.wait_for_timeout(900)
    k = pg.evaluate(K); pg.click('#nav [data-ir=financas]'); pg.wait_for_timeout(900); f = pg.evaluate(K)
    ok('filtro "Virtual": 2.050 livros, nenhuma compra', k['acervo']['v'] == '2.050' and f['investido']['v'] == 'R$ 0', (k['acervo']['v'], f['investido']['v']))
    pg.context.close()

    print('QUADRINHOS: O FILTRO "HQ" E A SUBPASTA DA SÉRIE')
    pg = pagina(b); pg.goto(PAINEL_URL); pg.wait_for_timeout(1200); pg.click('#aviso .pri'); pg.wait_for_timeout(200)
    botoes = pg.evaluate("() => [...document.querySelectorAll('#f-tipo button')].map(x => x.textContent.trim())")
    ok('filtro Tipo: Todos, Ficção, Não ficção, HQ, Outros', botoes == ['Todos', 'Ficção', 'Não ficção', 'HQ', 'Outros'], botoes)
    por_tipo = {}; chips = {}
    for t in ('F', 'NF', 'HQ', 'O'):
        pg.click(f'#f-tipo button[data-v="{t}"]'); pg.wait_for_timeout(900); por_tipo[t] = pg.evaluate(K); chips[t] = pg.inner_text('#f-ativos').replace('\n', ' ').replace('\u00a0', ' ')
    hq = por_tipo['HQ']; n = {t: int(por_tipo[t]['acervo']['v'].replace('.', '')) for t in por_tipo}
    ok('filtro "HQ": 244 quadrinhos no acervo (um deles também na estante) e 1 nas recomendações', hq['acervo']['v'] == '244' and hq['acervo']['s'] == '1 físico · 244 digitais · 1 nos dois' and hq['recs']['v'] == '1', (hq['acervo'], hq['recs']['v']))
    ok('os quatro tipos somam o acervo inteiro: nenhum quadrinho ficou também em "Outros"', sum(n.values()) == 2124 and all(n.values()), n)
    ok('o filtro ativo se chama "HQ"; o de "Outros", "Poesia e outros"', 'HQ' in chips['HQ'] and 'Poesia e outros' in chips['O'] and 'HQ' not in chips['O'], (chips['HQ'], chips['O']))
    tipos = pg.evaluate("""() => { const cab = [...document.querySelectorAll('#p-tab-geral thead th')].map(x => x.textContent.trim().toLowerCase()), i = cab.indexOf('tipo');
        return i < 0 ? ['sem coluna Tipo'] : [...new Set([...document.querySelectorAll('#p-tab-geral tbody tr[data-id]')].map(r => r.children[i].textContent.trim()))]; }""")
    ok('em "Outros", a tabela não mostra nenhuma linha de tipo HQ', bool(tipos) and 'HQ' not in tipos and 'sem coluna Tipo' not in tipos, tipos)
    pg.click('#f-tipo button[data-v=""]'); pg.wait_for_timeout(700)
    abrir(pg, 'Akira Otomo', 'Akira'); f = pg.evaluate(FATOS); v = pg.evaluate(VIRTUAL)
    ok('série que só tem a pasta: a gaveta diz a subpasta e não fala em arquivos', f.get('Formato') == 'Digital · Biblioteca virtual' and '1 pasta de edições' in v and 'As edições estão na subpasta: Akira' in v and 'arquivo' not in v, v[:200])
    abrir(pg, 'Hellboy Mignola', 'Hellboy'); v = pg.evaluate(VIRTUAL)
    ok('série com arquivos soltos e pasta: a gaveta mostra as duas coisas', '2 arquivos · RAR + 1 pasta de edições' in v and 'As edições estão na subpasta: Hellboy' in v, v[:200])
    abrir(pg, 'Coraline Gaiman', 'Coraline'); f = pg.evaluate(FATOS); v = pg.evaluate(VIRTUAL)
    ok('quadrinho que é um arquivo só: sem falar em pasta de edições', f.get('Formato') == 'Físico e digital' and '1 arquivo · RAR' in v and 'pasta de edições' not in v and 'subpasta' not in v, (f.get('Formato'), v[:200]))
    pg.keyboard.press('Escape'); pg.wait_for_timeout(200); pg.fill('#p-tab-geral input[type=search]', 'Faltam 20 a 22'); pg.wait_for_timeout(600)
    tits = pg.evaluate("() => [...document.querySelectorAll('#p-tab-geral tbody tr[data-id] .tt b')].map(x => x.textContent.trim())")
    ok('a busca acha a série pelo nome da subpasta', tits == ['Fábulas'], tits)
    pg.context.close()

    print('CELULAR: O FORMATO CABE NO CARTÃO E O FILTRO TIPO, NA FOLHA DE FILTROS')
    for largura in (390, 360, 320):
        ctx = b.new_context(viewport={'width': largura, 'height': 800}, locale='pt-BR', timezone_id='America/Sao_Paulo', is_mobile=True, has_touch=True)
        pg = ctx.new_page(); fixa(pg); pg.on('pageerror', lambda e: errs.append(f'[pageerror] {e}'))
        pg.goto(PAINEL_URL); pg.wait_for_timeout(1200); pg.click('#aviso .pri'); pg.wait_for_timeout(200)
        pg.click('#nav-m [data-ir=biblioteca]'); pg.wait_for_timeout(1000)
        r = pg.evaluate("""() => { const fs = [...document.querySelectorAll('#p-tab-biblioteca tbody td .fmt')];
            const fora = fs.filter(f => { const c = f.closest('td').getBoundingClientRect(); return [...f.getClientRects()].some(q => q.right > c.right + 1 || q.left < c.left - 1); });
            return { n: fs.length, duplos: fs.filter(f => f.querySelectorAll('.ic').length === 2).length, fora: fora.length, pagina: document.documentElement.scrollWidth - document.documentElement.clientWidth }; }""")
        ok(f'{largura} px: "Físico e digital" não invade a coluna vizinha', r['n'] >= 5 and r['duplos'] >= 1 and r['fora'] == 0 and r['pagina'] <= 0, r)
        pg.click('#f-abrir'); pg.wait_for_timeout(600)
        r = pg.evaluate("""() => { const g = document.querySelector('#f-tipo'), c = g.getBoundingClientRect(), bs = [...g.querySelectorAll('button')];
            const fora = bs.filter(x => { const q = x.getBoundingClientRect(); return q.width < 1 || q.right > c.right + .5 || q.left < c.left - .5 || x.scrollWidth > x.clientWidth + 1; });
            return { n: bs.length, fora: fora.map(x => x.textContent.trim()), rola: g.scrollWidth - g.clientWidth }; }""")
        ok(f'{largura} px: os cinco botões do filtro Tipo cabem na folha de filtros', r['n'] == 5 and r['fora'] == [] and r['rola'] <= 0,
           dict(r, fonte=fonte_usada(pg, '#f-tipo button')) if r['fora'] or r['rola'] > 0 else r)   # não coube: veja com que fonte o teste rodou (relogio.py)
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
        ok('aviso: 1.970 livros entraram e as edições foram mantidas', 'O catálogo mudou: 1.970 livros entraram.' in t and 'O que você editou no painel foi mantido.' in t, t)
        if pg.locator('#aviso .pri').is_visible(): pg.click('#aviso .pri'); pg.wait_for_timeout(200)
        k = pg.evaluate(K); ok('acervo migrado: 100 físicos · 2.049 digitais · 25 nos dois', k['acervo']['v'] == '2.124' and k['acervo']['s'] == '100 físicos · 2.049 digitais · 25 nos dois', k['acervo'])
        abrir(pg, 'Zz Livro da Versão Antiga'); f = pg.evaluate(FATOS)
        ok('o livro que eu tinha criado continua na lista de compra, com o alvo', pg.locator('#gaveta.on').count() == 1 and 'R$ 40,00' in f.get('Preço-alvo', ''), f)
        abrir(pg, 'Fundação Asimov', 'Fundação'); f = pg.evaluate(FATOS); v = pg.evaluate(VIRTUAL)
        ok('o livro que eu tinha editado mantém a edição e ganha o exemplar digital', f.get('Páginas') == '777' and f.get('Formato') == 'Físico e digital' and '1 arquivo' in v, f)
        pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
        novo = json.loads(pg.evaluate(f"() => localStorage.getItem('{CHAVE}')"))
        marcas = sorted({t for x in novo['livros'] for t in x.get('tags', []) if t.startswith(('ja-tenho', 'tenho-'))})
        ok('o estado regravado tem 2.615 livros, a assinatura do catálogo e nenhum #ja-tenho', len(novo['livros']) == 2615 and marcas == ['tenho-digital', 'tenho-fisico'] and bool(novo.get('cat')), (len(novo['livros']), marcas, novo.get('cat')))
        pg.reload(); pg.wait_for_timeout(1500); t = pg.evaluate(TOASTS)
        # se falhar, isto ajuda a ver de onde veio: [livros guardados, assinatura do catálogo, as duas marcas de "já posto"]
        guardado = pg.evaluate("() => { const s = JSON.parse(localStorage.getItem('%s') || 'null'); return [s && s.livros.length, s && (s.cat || ''), sessionStorage.getItem('qa-posto'), window.name]; }" % CHAVE)
        ok('ao reabrir, a migração não se repete', 'O catálogo mudou' not in t, t and (t, guardado))
        k = pg.evaluate(K); ok('e os números continuam os mesmos', k['acervo']['v'] == '2.124' and k['acervo']['s'] == '100 físicos · 2.049 digitais · 25 nos dois', k['acervo'])
        pg.context.close()

        print('MIGRAÇÃO: BACKUP EXPORTADO PELO PAINEL ANTERIOR')
        pg = pagina(b); pg.goto(PAINEL_URL); pg.wait_for_timeout(1200); pg.click('#aviso .pri'); pg.wait_for_timeout(200)
        pg.click('#b-dados'); pg.wait_for_timeout(400); pg.set_input_files('#arq', f'{TMP}/bk-antigo.json'); pg.wait_for_timeout(800)
        txt = pg.inner_text('#dlg.on').replace('\u00a0', ' ').replace('\n', ' ')
        ok('a confirmação reconhece o backup antigo (645 livros)', '645 livros' in txt, txt[:160])
        pg.click('#dlg footer .pri'); pg.wait_for_timeout(1200); t = pg.evaluate(TOASTS)
        ok('importado, com o aviso dos 1.970 livros que entraram', 'Backup importado. O catálogo mudou: 1.970 livros entraram.' in t, t)
        for _ in range(2): pg.keyboard.press('Escape'); pg.wait_for_timeout(150)
        k = pg.evaluate(K); ok('acervo depois de importar: 100 físicos · 2.049 digitais · 25 nos dois', k['acervo']['v'] == '2.124' and k['acervo']['s'] == '100 físicos · 2.049 digitais · 25 nos dois', k['acervo'])
        abrir(pg, 'Fundação Asimov', 'Fundação'); f = pg.evaluate(FATOS)
        ok('a edição feita no painel antigo veio no backup', f.get('Páginas') == '777' and f.get('Formato') == 'Físico e digital', f)
        abrir(pg, 'Zz Livro da Versão Antiga'); f = pg.evaluate(FATOS)
        ok('o livro criado no painel antigo veio no backup', pg.locator('#gaveta.on').count() == 1 and 'R$ 40,00' in f.get('Preço-alvo', ''), f)
        pg.context.close()

    print('TÍTULO OU AUTOR CORRIGIDO DEPOIS DE O LIVRO TER SIDO ANOTADO NO PAINEL')
    try:
        anterior = subprocess.run(['git', 'show', ANTERIOR], cwd=str(RAIZ), capture_output=True, check=True).stdout
    except Exception as e:
        anterior = None; print(f'  (pulado: não consegui tirar o painel anterior do Git — {type(e).__name__})')
    if anterior:
        # dois livros só da estante, sem arquivo que os identifique, corrigidos no catálogo (reencontrados por catalogo/renomeados.tsv)
        # e um livro só digital, corrigido no inventário (reencontrado pelo arquivo)
        # e uma recomendação que tenho em digital, com o título trocado pelo da edição brasileira (as duas coisas)
        # cada caso: o que buscar · título de antes · título de agora · autor de agora · páginas anotadas · o painel conhece o título antigo?
        casos = [('Investigações Cognitivas', 'Investigações Cognitivas', 'Investigações Cognitivas', 'Marcos Barbosa de Oliveira e Marta Kohl de Oliveira (orgs.)', '555', False),
                 ('148 Tecnologias e Ferramentas', '148 Tecnologias e Ferramentas de Gestão', 'Tecnologias e Ferramentas de Gestão (PLT 148)', 'Décio Henrique Franco e outros (orgs.)', '333', True),
                 ('Criação Destruidora', 'Marx: A Criação Destruidora', 'Curso Livre Marx-Engels: A Criação Destruidora', 'José Paulo Netto (org.)', '444', False),
                 ('Torno do Céu', 'O Torno do Céu', 'A Curva do Sonho', 'Ursula K. Le Guin', '222', True)]
        arq = TMP / 'painel-anterior.html'; arq.write_bytes(anterior)
        pg = pagina(b); pg.goto(arq.as_uri()); pg.wait_for_timeout(1200); pg.click('#aviso .pri'); pg.wait_for_timeout(200)
        for busca, antes, _, _, pags, _ in casos:   # no painel anterior: uma anotação em cada um
            abrir(pg, busca, antes); pg.click('#gv-acoes [data-acao=editar]'); pg.wait_for_timeout(500); pg.fill('#dlg [data-f=pg]', pags); pg.click('#dlg footer .pri'); pg.wait_for_timeout(800)
        salvo = pg.evaluate(f"() => localStorage.getItem('{CHAVE}')"); estado = json.loads(salvo)
        ok('o painel anterior salvou 2.300 livros, quatro deles anotados', len(estado['livros']) == 2300 and sum(1 for x in estado['livros'] if x.get('u')) == 4, len(estado['livros']))
        pg.context.close()

        pg = pagina(b, salvo); pg.goto(PAINEL_URL); pg.wait_for_timeout(1500); t = pg.evaluate(TOASTS)
        # as 6 que saíram são linhas que a vistoria juntou a outra (duas edições da mesma obra; a recomendação que já estava num arquivo)
        ok('entraram os 320 livros e quadrinhos que vieram depois e saíram as 6 linhas repetidas; nenhum corrigido "saiu" nem "entrou"', 'O catálogo mudou: 320 livros entraram e 6 saíram. O que você editou no painel foi mantido.' in t, t)
        if pg.locator('#aviso .pri').is_visible(): pg.click('#aviso .pri'); pg.wait_for_timeout(200)
        for busca, antes, depois, autor, pags, conhece in casos:      # a busca é a mesma de antes: nos casos com título novo, é pelo nome antigo
            pg.keyboard.press('Escape'); pg.wait_for_timeout(200); pg.fill('#p-tab-geral input[type=search]', busca); pg.wait_for_timeout(600)
            tits = pg.evaluate("() => [...document.querySelectorAll('#p-tab-geral tbody tr[data-id] .tt b')].map(x => x.textContent.trim())")
            abrir(pg, busca, depois); f = pg.evaluate(FATOS); gav = pg.inner_text('#gaveta.on').replace('\u00a0', ' ')
            anterior_na_gaveta = pg.evaluate("() => { const s = document.querySelector('#gaveta.on #gv-antes'); return s ? s.textContent : ''; }")
            ok(f'{depois}: uma linha só, com o nome corrigido e a anotação de antes', tits == [depois] and autor in gav and f.get('Páginas') == pags, (tits, f.get('Páginas')))
            if conhece: ok(f'{depois}: achado pelo nome antigo, que a gaveta mostra', antes in anterior_na_gaveta, anterior_na_gaveta[:120])
            else: ok(f'{depois}: a gaveta não fala em título anterior', anterior_na_gaveta == '', anterior_na_gaveta[:120])
        pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
        novo = json.loads(pg.evaluate(f"() => localStorage.getItem('{CHAVE}')"))
        ok('o estado regravado tem os 2.614 livros do catálogo de agora, sem nenhum repetido', len(novo['livros']) == 2614, len(novo['livros']))
        pg.context.close()
    b.close()
print('FALHAS:', falhas); print('ERROS:', len(errs) + len(falhas)); [print('  ', x[:300]) for x in errs[:10]]
