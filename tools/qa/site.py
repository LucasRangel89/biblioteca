"""O painel como site: servido por HTTP, de dentro de uma pasta, como página inicial — do jeito do GitHub Pages
(.github/workflows/publicar-site.yml copia o painel para `index.html`).

Os outros testes abrem o arquivo por file://. Aqui se confere o que só aparece num site:
  · o painel vem inteiro numa única requisição: nenhum arquivo ao lado dele, nada buscado em outro endereço;
  · é o mesmo painel: os indicadores são iguais aos do arquivo aberto direto;
  · o navegador guarda o que se anota, e isso continua lá depois de recarregar a página;
  · o backup sai como download;
  · quem já usava o arquivo no computador leva os dados para o site por um backup.
"""
from caminhos import PAINEL, PAINEL_URL, TMP
from relogio import fixa
import functools, http.server, json, shutil, threading
from playwright.sync_api import sync_playwright

CHAVE = 'biblioteca-lucas:v1'
errs = []; falhas = []
K = "() => Object.fromEntries([...document.querySelectorAll('.visao:not([hidden]) .kpi')].map(k => [k.dataset.k, k.querySelector('.kpi-v b').textContent + ' ¦ ' + k.querySelector('.kpi-s').textContent]))"
TOASTS = "() => [...document.querySelectorAll('#toasts .toast')].map(t => t.textContent).join(' ¦ ')"
GUARDADOS = "() => JSON.parse(localStorage.getItem('%s') || '{\"livros\":[]}').livros.map(b => b.t)" % CHAVE
ACHADOS = "() => [...document.querySelectorAll('#p-tab-geral tbody tr[data-id] .tt b')].map(x => x.textContent)"


def ok(nome, cond, extra=''):
    print(('  ok   ' if cond else '  FALHA') + ' ' + nome + (' — ' + str(extra) if extra != '' else ''))
    if not cond: falhas.append(nome)


class Silencioso(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass


def pagina(b, pedidos=None):
    """Página num navegador sem nada guardado; `pedidos` recebe o endereço de tudo o que ela buscar."""
    ctx = b.new_context(viewport={'width': 1440, 'height': 900}, locale='pt-BR', timezone_id='America/Sao_Paulo', accept_downloads=True)
    pg = ctx.new_page(); fixa(pg)
    pg.on('console', lambda m: errs.append(f'[{m.type}] {m.text}') if m.type in ('error', 'warning') else None)
    pg.on('pageerror', lambda e: errs.append(f'[pageerror] {e}'))
    if pedidos is not None: pg.on('request', lambda r: pedidos.append(r.url))
    return pg


def novo_livro(pg, titulo):
    pg.click('#b-novo'); pg.wait_for_timeout(400)
    pg.fill('#dlg [data-f=t]', titulo); pg.fill('#dlg [data-f=a]', 'Autora de Teste')
    pg.click('#dlg footer .pri'); pg.wait_for_timeout(900)
    pg.keyboard.press('Escape'); pg.wait_for_timeout(300)


def exportar(pg, destino):
    pg.click('#b-dados'); pg.wait_for_timeout(400)
    with pg.expect_download() as d: pg.click('#dlg [data-x=exportar]')
    d.value.save_as(destino)
    pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
    return d.value.suggested_filename, json.loads(destino.read_text(encoding='utf-8'))


def busca(pg, termo):
    pg.fill('#p-tab-geral input[type=search]', termo); pg.wait_for_timeout(600)
    return pg.evaluate(ACHADOS)


# o site, montado como na publicação: o painel vira o index.html de uma pasta com o nome do repositório
raiz = TMP / 'site'
shutil.rmtree(raiz, ignore_errors=True)
(raiz / 'biblioteca').mkdir(parents=True)
shutil.copyfile(PAINEL, raiz / 'biblioteca' / 'index.html')
servidor = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Silencioso, directory=str(raiz)))
threading.Thread(target=servidor.serve_forever, daemon=True).start()
SITE = f'http://127.0.0.1:{servidor.server_address[1]}/biblioteca/'

with sync_playwright() as p:
    b = p.chromium.launch()

    print('O SITE ABRE')
    pedidos = []
    pg = pagina(b, pedidos); resposta = pg.goto(SITE); pg.wait_for_selector('html.pronto', timeout=15000); pg.wait_for_timeout(1200)
    ok('responde 200 com o painel', resposta.status == 200 and pg.title().endswith('Biblioteca do Lucas'), (resposta.status, pg.title()))
    pg.click('#aviso .pri'); pg.wait_for_timeout(200)
    no_site = pg.evaluate(K)

    arq = pagina(b); arq.goto(PAINEL_URL); arq.wait_for_selector('html.pronto', timeout=15000); arq.wait_for_timeout(1200)
    arq.click('#aviso .pri'); arq.wait_for_timeout(200)
    no_arquivo = arq.evaluate(K)
    ok('mesmos indicadores do arquivo aberto direto', bool(no_site) and no_site == no_arquivo, no_site if no_site != no_arquivo else f'{len(no_site)} indicadores')

    print('O NAVEGADOR GUARDA OS DADOS')
    estado = pg.evaluate("() => document.querySelector('#st-dados').textContent")
    ok('o painel diz que salva neste navegador', 'Salvo neste navegador' in estado, estado)
    novo_livro(pg, 'Livro Anotado no Site')
    ok('o livro novo foi guardado', 'Livro Anotado no Site' in pg.evaluate(GUARDADOS))
    pg.reload(); pg.wait_for_selector('html.pronto', timeout=15000); pg.wait_for_timeout(1200)
    achados = busca(pg, 'Livro Anotado no Site')
    ok('depois de recarregar, o livro continua lá', achados == ['Livro Anotado no Site'], achados)

    print('BACKUP')
    nome, bk = exportar(pg, TMP / 'site-backup.json')
    ok('o backup sai como download (.json)', nome.startswith('biblioteca-lucas-backup-') and nome.endswith('.json'), nome)
    ok('e traz o que foi anotado no site', bk.get('app') == 'biblioteca-lucas' and any(x.get('t') == 'Livro Anotado no Site' for x in bk.get('livros', [])), {k: (len(v) if isinstance(v, (list, dict, str)) else v) for k, v in bk.items()})

    print('DO ARQUIVO PARA O SITE')
    novo_livro(arq, 'Livro Anotado no Arquivo')
    exportar(arq, TMP / 'site-do-arquivo.json')
    pg.click('#b-dados'); pg.wait_for_timeout(400); pg.set_input_files('#arq', str(TMP / 'site-do-arquivo.json')); pg.wait_for_timeout(800)
    pergunta = pg.inner_text('#dlg h2')
    pg.click('#dlg footer .pri'); pg.wait_for_timeout(1200)
    avisos = pg.evaluate(TOASTS)
    ok('o site importa o backup feito no arquivo', pergunta == 'Importar backup' and 'Backup importado' in avisos, (pergunta, avisos))
    pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
    ok('os indicadores continuam os mesmos', pg.evaluate(K) == arq.evaluate(K), pg.evaluate(K))
    pg.reload(); pg.wait_for_selector('html.pronto', timeout=15000); pg.wait_for_timeout(1200)
    achados = busca(pg, 'Livro Anotado no')
    ok('depois de recarregar, o site tem o que estava no arquivo', achados == ['Livro Anotado no Arquivo'], achados)

    print('NADA VEM DE FORA')
    fora = sorted({u for u in pedidos if u != SITE and not u.startswith(('data:', 'blob:'))})
    ok('tudo o que o navegador buscou foi a própria página', pedidos.count(SITE) >= 3 and not fora, fora or f'{pedidos.count(SITE)} cargas da página')
    b.close()
servidor.shutdown()
print('FALHAS:', falhas); print('ERROS:', len(errs) + len(falhas)); [print('  ', x[:300]) for x in errs[:10]]
