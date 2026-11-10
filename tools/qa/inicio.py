"""Como o painel começa, e os dados de exemplo — que só entram a pedido.

  · primeira abertura: só o catálogo; nenhuma leitura, data ou valor inventado; nada guardado como "exemplo";
  · "Ver com dados de exemplo" (em Seus dados) liga os exemplos, e eles continuam ligados ao recarregar;
  · "Limpar dados de exemplo" tira tudo de novo; o que foi registrado pelo usuário fica;
  · o endereço terminado em ?exemplo=1 abre com exemplos — mas só num navegador sem nada salvo;
  · "Recomeçar do catálogo original" apaga o que foi anotado e volta ao começo;
  · quem usava o painel de antes (que vinha com exemplos de fábrica) abre o painel novo: os exemplos saem sozinhos,
    uma vez, com aviso; os livros que a pessoa criou ou editou ficam como estavam, e o aviso leva até eles.

A última parte é feita duas vezes: com um estado salvo montado aqui mesmo (sempre) e com o painel que estava no ar
antes desta mudança, tirado do histórico do Git (sem Git, ou sem aquele commit, essa segunda vez é pulada, com aviso).

Os números esperados são um retrato do catálogo atual; se o catálogo mudar, confira as linhas FALHA e atualize.
"""
from caminhos import PAINEL_LIMPO, PAINEL_URL, RAIZ, TMP
from relogio import fixa
import json, subprocess
from playwright.sync_api import sync_playwright

PUBLICADO = 'a5ec27b:Biblioteca_Lucas_Dashboard.html'      # o painel que estava no ar: abria com os exemplos ligados
CHAVE = 'biblioteca-lucas:v1'
errs = []; falhas = []
K = "() => Object.fromEntries([...document.querySelectorAll('.visao:not([hidden]) .kpi')].map(k => [k.dataset.k, k.querySelector('.kpi-v b').textContent.replace(/\\u00a0/g, ' ')]))"
TOASTS = "() => [...document.querySelectorAll('#toasts .toast')].map(t => t.textContent.replace(/\\u00a0/g, ' '))"
AVISO = """() => { const a = document.querySelector('#aviso'); if (a.hidden) return null;
    return { inicio: a.classList.contains('inicio'), titulo: a.querySelector('b').textContent, texto: a.innerText.replace(/\\u00a0/g, ' ').replace(/\\s+/g, ' '), botoes: [...a.querySelectorAll('button')].map(b => b.textContent.trim()) }; }"""
SALVO = """() => { const t = localStorage.getItem('%s'); if (!t) return null; const s = JSON.parse(t);
    return { exemplos: s.exemplos, demo: 'demo' in s ? s.demo : null, comDemo: s.livros.filter(x => x.demo).length, meus: s.livros.filter(x => x.u).length, saiu: (s.cfg || {}).saiu ?? null, n: s.livros.length }; }""" % CHAVE
PILULA = "() => !document.querySelector('#b-exemplo').hidden"
LIMPO = {'acervo': '2.125', 'leituras': '2', 'fila': '2.125', 'recs': '433'}                 # só o catálogo
EXEMPLO = {'acervo': '2.125', 'leituras': '60', 'fila': '2.062', 'recs': '407'}              # com os dados simulados
F_LIMPO = {'investido': 'R$ 0', 'medio': '—', 'cesta': '—', 'oport': '0'}
F_EXEMPLO = {'investido': 'R$ 4.469', 'medio': 'R$ 50,22', 'cesta': 'R$ 1.257', 'oport': '7'}
SAIU = 'Os dados de exemplo saíram: agora o painel mostra só o que é seu.'


def ok(nome, cond, extra=''):
    print(('  ok   ' if cond else '  FALHA') + ' ' + nome + (' — ' + str(extra) if extra != '' else ''))
    if not cond: falhas.append(nome)


with sync_playwright() as p:
    b = p.chromium.launch()

    def pagina(salvo=None, largura=1440, altura=900):
        """Página nova; `salvo` é o texto que o navegador já teria guardado (posto uma única vez, antes do painel carregar)."""
        cel = largura < 700
        ctx = b.new_context(viewport={'width': largura, 'height': altura}, locale='pt-BR', timezone_id='America/Sao_Paulo', is_mobile=cel, has_touch=cel)
        if salvo is not None:
            ctx.add_init_script("(() => { try { if (!sessionStorage.getItem('qa-posto') && window.name !== 'qa-posto') { localStorage.setItem(%s, %s); } sessionStorage.setItem('qa-posto', '1'); window.name = 'qa-posto'; } catch (e) {} })()" % (json.dumps(CHAVE), json.dumps(salvo)))
        pg = ctx.new_page(); fixa(pg)
        pg.on('console', lambda m: errs.append(f'[{m.type}] {m.text}') if m.type in ('error', 'warning') else None)
        pg.on('pageerror', lambda e: errs.append(f'[pageerror] {e}'))
        return pg

    def abre(pg, url): pg.goto(url); pg.wait_for_timeout(1300)
    def recarrega(pg): pg.wait_for_timeout(700); pg.reload(); pg.wait_for_timeout(1300)
    def ir(pg, v): pg.click(f'#nav [data-ir={v}]'); pg.wait_for_timeout(800); return pg.evaluate(K)
    def numeros(pg): f = ir(pg, 'financas'); g = ir(pg, 'geral'); return g, f
    def dados(pg): pg.click('#b-dados'); pg.wait_for_timeout(400)
    def confirma(pg, perigo=False): pg.click('#dlg footer .perigo' if perigo else '#dlg footer .pri'); pg.wait_for_timeout(1100)
    def livro(pg, busca, titulo):
        pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
        pg.fill('#p-tab-geral input[type=search]', busca); pg.wait_for_timeout(600)
        pg.locator('#p-tab-geral tbody tr[data-id]').filter(has=pg.locator('.tt b', has_text=titulo)).first.click(); pg.wait_for_timeout(700)
    def edita(pg, busca, titulo, paginas='321'):
        livro(pg, busca, titulo); pg.click('#gv-acoes [data-acao=editar]'); pg.wait_for_timeout(500); pg.fill('#dlg [data-f=pg]', paginas); pg.click('#dlg footer .pri'); pg.wait_for_timeout(800)
        pg.keyboard.press('Escape'); pg.wait_for_timeout(200); pg.fill('#p-tab-geral input[type=search]', ''); pg.wait_for_timeout(500)
    def cria(pg, titulo):                                   # um livro novo, direto no acervo (a lista sugerida depende da guia aberta)
        pg.click('#b-novo'); pg.wait_for_timeout(400); pg.fill('#dlg [data-f=t]', titulo); pg.select_option('#dlg [data-f=col]', 'acervo')
        pg.click('#dlg footer .pri'); pg.wait_for_timeout(800); pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
    def guardado(pg): pg.wait_for_timeout(800); return pg.evaluate("() => localStorage.getItem('%s')" % CHAVE)

    # ─────────────────────────────────────────────────────────────────────────────────────────────
    print('PRIMEIRA ABERTURA: SÓ O CATÁLOGO')
    pg = pagina(); abre(pg, PAINEL_LIMPO); a = pg.evaluate(AVISO)
    ok('o recado de abertura diz que só aparece o que é do usuário', a and a['inicio'] and a['titulo'] == 'Aqui só aparece o que é seu.' and a['botoes'] == ['Entendi'], a)
    ok('e explica que nada é obrigatório, nem as datas', a and 'Os 2.560 títulos, a estante física e a biblioteca virtual vieram do seu catálogo.' in a['texto'] and 'Nada disso é obrigatório — nem as datas.' in a['texto'], a and a['texto'][:260])
    ok('nenhum aviso de "dados de exemplo" na barra de cima', not pg.evaluate(PILULA))
    g, f = numeros(pg)
    ok('indicadores: 2.125 no acervo, 2 leituras (as que o catálogo registra), nada por comprar', g == LIMPO and f == F_LIMPO, (g, f))
    pg.click('#aviso .pri'); pg.wait_for_timeout(400); s = pg.evaluate(SALVO)
    ok('o que fica guardado não tem nada marcado como exemplo', s and s['exemplos'] is False and s['demo'] is None and s['comDemo'] == 0 and s['meus'] == 0 and s['n'] == 2560, s)
    recarrega(pg)
    ok('depois do "Entendi", o recado não volta ao recarregar', pg.evaluate(AVISO) is None and ir(pg, 'geral') == LIMPO)
    dados(pg); texto = pg.inner_text('#dlg').replace('\u00a0', ' ')
    ok('"Seus dados" diz que o painel mostra só o que é do usuário e oferece ver os exemplos', 'O painel mostra só o que é seu' in texto and pg.locator('#dlg [data-x=restaurar]').inner_text().strip() == 'Ver com dados de exemplo' and pg.locator('#dlg [data-x=limpar]').count() == 0, texto[texto.find('Dados de exemplo'):][:200])

    print('"VER COM DADOS DE EXEMPLO"')
    pg.click('#dlg [data-x=restaurar]'); pg.wait_for_timeout(400)
    titulo = pg.inner_text('#dlg h2').strip(); msg = pg.inner_text('#dlg .dlg-msg').replace('\u00a0', ' ')
    ok('pede confirmação e diz que os dados são simulados e como tirá-los', titulo == 'Ver com dados de exemplo' and 'simulados' in msg and 'Limpar dados de exemplo' in msg, (titulo, msg))
    confirma(pg); t = pg.evaluate(TOASTS)
    ok('avisa que foram ligados', t[-1:] == ['Dados de exemplo ligados.'], t)
    for _ in range(2): pg.keyboard.press('Escape'); pg.wait_for_timeout(150)
    a = pg.evaluate(AVISO)
    ok('o recado volta, agora dizendo que o movimento é de exemplo', a and not a['inicio'] and a['titulo'] == 'Seu catálogo é real; o movimento é de exemplo.' and a['botoes'] == ['Gerenciar dados', 'Entendi'], a)
    ok('e a barra de cima passa a avisar "Dados de exemplo"', pg.evaluate(PILULA))
    g, f = numeros(pg)
    ok('indicadores: os mesmos de quem abre com ?exemplo=1 (60 leituras, R$ 4.469 investidos)', g == EXEMPLO and f == F_EXEMPLO, (g, f))
    s = pg.evaluate(SALVO)
    ok('guardado como exemplo pedido (não como exemplo de fábrica)', s and s['exemplos'] is True and s['demo'] == 1 and s['comDemo'] > 500 and s['meus'] == 0, s)
    recarrega(pg); t = pg.evaluate(TOASTS)
    ok('ao recarregar, os exemplos continuam (foram pedidos) e nada é retirado', ir(pg, 'geral') == EXEMPLO and SAIU not in t and pg.evaluate(PILULA), (pg.evaluate(K), t))

    print('"LIMPAR DADOS DE EXEMPLO"')
    pg.click('#aviso [data-av=dados]'); pg.wait_for_timeout(400)
    ok('"Gerenciar dados", no recado, abre "Seus dados" com o botão de limpar', pg.inner_text('#dlg h2').strip() == 'Seus dados' and pg.locator('#dlg [data-x=limpar]').count() == 1 and pg.locator('#dlg [data-x=restaurar]').count() == 0)
    pg.click('#dlg [data-x=limpar]'); pg.wait_for_timeout(400); confirma(pg); t = pg.evaluate(TOASTS)
    for _ in range(2): pg.keyboard.press('Escape'); pg.wait_for_timeout(150)
    g, f = numeros(pg); s = pg.evaluate(SALVO)
    ok('tudo volta ao que era: só o catálogo', t[-1:] == ['Dados de exemplo removidos.'] and g == LIMPO and f == F_LIMPO and not pg.evaluate(PILULA), (t, g, f))
    ok('e nada mais fica guardado como exemplo', s and s['exemplos'] is False and s['demo'] is None and s['comDemo'] == 0, s)
    pg.context.close()

    print('O QUE O USUÁRIO REGISTROU NÃO SE MISTURA COM OS EXEMPLOS')
    pg = pagina(); abre(pg, PAINEL_LIMPO); pg.click('#aviso .pri'); pg.wait_for_timeout(200)
    livro(pg, 'Peste Camus', 'A Peste'); pg.click('#gv-acoes [data-acao=lido]'); pg.wait_for_timeout(500); pg.click('#dlg footer .pri'); pg.wait_for_timeout(800)
    pg.keyboard.press('Escape'); pg.wait_for_timeout(200); pg.fill('#p-tab-geral input[type=search]', ''); pg.wait_for_timeout(500)
    ok('uma leitura registrada (sem data): 3 leituras', ir(pg, 'geral')['leituras'] == '3', pg.evaluate(K))
    dados(pg); pg.click('#dlg [data-x=restaurar]'); pg.wait_for_timeout(400); confirma(pg)
    for _ in range(2): pg.keyboard.press('Escape'); pg.wait_for_timeout(150)
    com = ir(pg, 'geral'); s = pg.evaluate(SALVO)
    ok('ligar os exemplos não mexe no livro que o usuário registrou', s['meus'] == 1 and s['demo'] == 1 and int(com['leituras']) >= 55, (com, s))
    edita(pg, 'Guerra e Paz Tolstói', 'Guerra e Paz', '1500')                 # com os exemplos ligados, o usuário edita outro livro
    dados(pg); pg.click('#dlg [data-x=limpar]'); pg.wait_for_timeout(400); confirma(pg)
    for _ in range(2): pg.keyboard.press('Escape'); pg.wait_for_timeout(150)
    g = ir(pg, 'geral'); s = pg.evaluate(SALVO)
    ok('limpar tira os exemplos e deixa os dois livros do usuário', s['meus'] == 2 and s['exemplos'] is False and s['comDemo'] == 0 and g['acervo'] == '2.125' and g['recs'] == '433' and int(g['leituras']) in (3, 4), (g, s))
    livro(pg, 'Peste Camus', 'A Peste')
    fatos = pg.evaluate("() => Object.fromEntries([...document.querySelectorAll('#gaveta .fatos > div')].map(d => [d.querySelector('dt').textContent, d.querySelector('dd').innerText.replace(/\\u00a0/g, ' ').replace(/\\s+/g, ' ').trim()]))")
    ok('a leitura registrada antes continua lá, sem data inventada', fatos.get('Leitura') == 'Lido' and fatos.get('Concluído em') == 'sem data', fatos)
    pg.keyboard.press('Escape'); pg.wait_for_timeout(200); pg.fill('#p-tab-geral input[type=search]', ''); pg.wait_for_timeout(400)

    print('"RECOMEÇAR DO CATÁLOGO ORIGINAL"')
    dados(pg); pg.click('#dlg [data-x=zerar]'); pg.wait_for_timeout(400)
    msg = pg.inner_text('#dlg .dlg-msg').replace('\u00a0', ' ')
    ok('pede confirmação e avisa que não dá para desfazer', pg.inner_text('#dlg h2').strip() == 'Recomeçar do catálogo original' and 'não pode ser desfeita' in msg and pg.inner_text('#dlg footer .perigo').strip() == 'Apagar tudo', msg)
    pg.click('#dlg footer button:not(.perigo)'); pg.wait_for_timeout(500)
    ok('"Cancelar" não apaga nada', pg.evaluate(SALVO)['meus'] == 2, pg.evaluate(SALVO))
    for _ in range(2): pg.keyboard.press('Escape'); pg.wait_for_timeout(150)
    dados(pg); pg.click('#dlg [data-x=zerar]'); pg.wait_for_timeout(400); confirma(pg, perigo=True); t = pg.evaluate(TOASTS)
    for _ in range(2): pg.keyboard.press('Escape'); pg.wait_for_timeout(150)
    g, f = numeros(pg); s = pg.evaluate(SALVO); a = pg.evaluate(AVISO)
    ok('volta ao começo: só o catálogo, nenhuma anotação', t[-1:] == ['Painel reiniciado.'] and g == LIMPO and f == F_LIMPO and s['meus'] == 0 and s['exemplos'] is False and s['demo'] is None, (t, g, f, s))
    ok('e o recado de abertura aparece de novo', a and a['inicio'] and a['titulo'] == 'Aqui só aparece o que é seu.', a)
    recarrega(pg)
    ok('recarregar confirma: nada do que foi anotado ficou', ir(pg, 'geral') == LIMPO and pg.evaluate(SALVO)['meus'] == 0, pg.evaluate(K))
    pg.context.close()

    print('O ENDEREÇO COM ?exemplo=1')
    pg = pagina(); abre(pg, PAINEL_URL); a = pg.evaluate(AVISO); g, f = numeros(pg)
    ok('num navegador sem nada salvo, abre com os exemplos', g == EXEMPLO and f == F_EXEMPLO and a and a['titulo'] == 'Seu catálogo é real; o movimento é de exemplo.' and pg.evaluate(PILULA), (g, f))
    pg.click('#aviso .pri'); pg.wait_for_timeout(400); s = pg.evaluate(SALVO)
    ok('guardado como exemplo pedido', s['exemplos'] is True and s['demo'] == 1, s)
    dados(pg); pg.click('#dlg [data-x=zerar]'); pg.wait_for_timeout(400); confirma(pg, perigo=True)
    for _ in range(2): pg.keyboard.press('Escape'); pg.wait_for_timeout(150)
    ok('"Recomeçar" nesse endereço volta ao começo dele: com exemplos', ir(pg, 'geral') == EXEMPLO and pg.evaluate(SALVO)['demo'] == 1, pg.evaluate(K))
    abre(pg, PAINEL_LIMPO); t = pg.evaluate(TOASTS)
    ok('voltar ao endereço normal não tira os exemplos que foram pedidos', ir(pg, 'geral') == EXEMPLO and SAIU not in t and pg.evaluate(PILULA), (pg.evaluate(K), t))
    pg.context.close()
    # quem já tem coisas salvas e abre o endereço de demonstração: nada inventado entra no meio do que é dele
    pg = pagina(); abre(pg, PAINEL_LIMPO); pg.click('#aviso .pri'); pg.wait_for_timeout(200); cria(pg, 'Zz Meu Livro de Verdade'); pg.wait_for_timeout(800)
    abre(pg, PAINEL_URL); g, f = numeros(pg); s = pg.evaluate(SALVO)
    ok('com dados já salvos, ?exemplo=1 não mistura exemplos ao que é do usuário', g == dict(LIMPO, acervo='2.126', fila='2.126') and f == F_LIMPO and not pg.evaluate(PILULA) and s['exemplos'] is False and s['comDemo'] == 0 and s['meus'] == 1, (g, f, s))
    pg.context.close()

    # ─────────────────────────────────────────────────────────────────────────────────────────────
    def confere_saida(rotulo, salvo, criados, editados, largura=1440):
        """Abre o painel novo com o que um painel antigo salvou (exemplos de fábrica) e confere a saída dos exemplos."""
        n = len(criados) + len(editados)
        pg = pagina(salvo, largura, 900 if largura >= 700 else 800); abre(pg, PAINEL_LIMPO); t = pg.evaluate(TOASTS); a = pg.evaluate(AVISO)
        ok(f'{rotulo}: os exemplos saem sozinhos na primeira abertura, com aviso', SAIU in t and a and a['inicio'] and a['titulo'] == 'Os dados de exemplo saíram.', (t, a and a['titulo']))
        ok(f'{rotulo}: o recado diz o que foi retirado', a and 'As leituras, datas e valores inventados que o painel mostrava foram retirados: agora só aparece o que é seu.' in a['texto'], a and a['texto'][:200])
        if n == 0:
            ok(f'{rotulo}: sem livros editados, o recado não fala deles', a and 'criou ou editou' not in a['texto'] and a['botoes'] == ['Entendi'], a and a['botoes'])
        elif n == 1:
            ok(f'{rotulo}: o recado fala do livro editado, no singular', a and 'O livro que você criou ou editou enquanto os exemplos estavam ligados ficou como estava: pode trazer datas ou valores de exemplo' in a['texto'] and a['botoes'] == ['Ver esse livro', 'Entendi'], a and (a['texto'][260:480], a['botoes']))
        else:
            ok(f'{rotulo}: o recado fala dos {n} livros editados', a and f'Os {n} livros que você criou ou editou enquanto os exemplos estavam ligados ficaram como estavam: podem trazer datas ou valores de exemplo' in a['texto'] and 'Recomeçar do catálogo original' in a['texto'] and a['botoes'] == ['Ver esses livros', 'Entendi'], a and (a['texto'][260:480], a['botoes']))
        s = pg.evaluate(SALVO)
        ok(f'{rotulo}: guardado sem exemplos; só os livros do usuário continuam marcados', s and s['exemplos'] is False and s['demo'] is None and s['comDemo'] == 0 and s['meus'] == n and s['saiu'] == n + 1, s)
        if largura >= 700:
            g, f = numeros(pg)
            ok(f'{rotulo}: acervo {2125 + len(criados):,} e 433 recomendações; nada do que não foi editado tem leitura ou valor'.replace(',', '.'), g['acervo'] == f'{2125 + len(criados):,}'.replace(',', '.') and g['recs'] == '433' and 2 <= int(g['leituras']) <= 2 + len(editados) and (n > 0 or (g == LIMPO and f == F_LIMPO)), (g, f))
        else:
            r = pg.evaluate("""() => { const a = document.querySelector('#aviso').getBoundingClientRect(), bs = [...document.querySelectorAll('#aviso button')].map(x => x.getBoundingClientRect());
                return { pagina: document.documentElement.scrollWidth - document.documentElement.clientWidth, fora: bs.filter(q => q.left < a.left - .5 || q.right > a.right + .5 || q.height < 30).length, n: bs.length }; }""")
            ok(f'{rotulo}: o recado e os botões cabem na tela de {largura} px', r['pagina'] <= 0 and r['fora'] == 0 and r['n'] == (2 if n else 1), r)
        if n:
            pg.click('#aviso [data-av=meus]'); pg.wait_for_timeout(900)
            aba = pg.evaluate("() => { const x = document.querySelector('#p-tab-geral .abas [aria-selected=true]'); return x ? [x.dataset.a, x.textContent.replace(/\\u00a0/g, ' ')] : null; }")
            linhas = pg.evaluate("() => [...document.querySelectorAll('#p-tab-geral tbody tr[data-id] .tt b')].map(x => x.textContent.trim())")
            ok(f'{rotulo}: o botão do recado leva à lista "Editados por você", com esses livros', aba == ['meus', f'Editados por você{n}'] and sorted(linhas) == sorted(criados + editados), (aba, linhas))
            visivel = pg.evaluate("() => { const x = document.querySelector('#p-tab-geral .abas [aria-selected=true]').getBoundingClientRect(), c = document.querySelector('#p-tab-geral .abas').getBoundingClientRect(); return x.left >= c.left - 1 && x.right <= c.right + 1; }")
            ok(f'{rotulo}: a aba escolhida fica à vista', visivel)
        recarrega(pg); t = pg.evaluate(TOASTS); a = pg.evaluate(AVISO)
        ok(f'{rotulo}: ao recarregar, o recado continua (até o "Entendi"), sem repetir o aviso de saída', a and a['titulo'] == 'Os dados de exemplo saíram.' and SAIU not in t and pg.evaluate(SALVO)['saiu'] == n + 1, (t, a and a['titulo']))
        pg.click('#aviso .pri'); pg.wait_for_timeout(400); recarrega(pg); s = pg.evaluate(SALVO)
        ok(f'{rotulo}: depois do "Entendi", o recado não volta mais', pg.evaluate(AVISO) is None and s['saiu'] is None and s['exemplos'] is False and s['demo'] is None and s['meus'] == n, s)
        pg.context.close()

    def usa(pg, criados, editados):
        """No painel com exemplos: cria e edita livros, e devolve o que ficou salvo no navegador."""
        for titulo in criados: cria(pg, titulo)
        for busca, titulo in editados: edita(pg, busca, titulo)
        return guardado(pg)

    EDITAR = [('Fundação Asimov', 'Fundação'), ('Sapiens Harari', 'Sapiens: Uma Breve História da Humanidade')]
    CRIAR = ['Zz Livro Criado com Exemplos']

    print('QUEM USAVA O PAINEL DE ANTES (EXEMPLOS DE FÁBRICA)')
    # o painel de antes gravava `exemplos: true` e nada mais; o de agora grava também `demo` quando os exemplos foram pedidos
    estados = {}
    for chave_, criar, editar in (('nenhum', [], []), ('um', [], EDITAR[:1]), ('tres', CRIAR, EDITAR)):
        pg = pagina(); abre(pg, PAINEL_URL); pg.click('#aviso .pri'); pg.wait_for_timeout(200)
        e = json.loads(usa(pg, criar, editar)); pg.context.close()
        de_fabrica = e.pop('demo', None) == 1 and e['exemplos'] is True
        estados[chave_] = (json.dumps(e, ensure_ascii=False), criar, [t for _, t in editar], de_fabrica)
    ok('o estado de ensaio é o de um painel antigo: exemplos ligados, sem a marca de "pedido"', all(x[3] for x in estados.values()))
    confere_saida('sem edições', *estados['nenhum'][:3])
    confere_saida('um livro editado', *estados['um'][:3])
    confere_saida('três livros', *estados['tres'][:3])
    confere_saida('celular, três livros', *estados['tres'][:3], largura=360)
    confere_saida('celular estreito, um livro', *estados['um'][:3], largura=320)
    # o mesmo estado antigo, aberto pelo endereço de demonstração: os exemplos ficam (foram pedidos pelo endereço)
    pg = pagina(estados['um'][0]); abre(pg, PAINEL_URL); t = pg.evaluate(TOASTS)
    ok('estado antigo aberto com ?exemplo=1: os exemplos ficam', SAIU not in t and pg.evaluate(PILULA) and int(ir(pg, 'geral')['leituras']) >= 55, (t, pg.evaluate(K)))
    pg.context.close()

    print('O MESMO, COM O PAINEL QUE ESTAVA NO AR (TIRADO DO GIT)')
    try:
        publicado = subprocess.run(['git', 'show', PUBLICADO], cwd=str(RAIZ), capture_output=True, check=True).stdout
    except Exception as e:
        publicado = None; print(f'  (pulado: não consegui tirar o painel publicado do Git — {type(e).__name__})')
    if publicado:
        arq = TMP / 'painel-publicado.html'; arq.write_bytes(publicado)
        pg = pagina(); abre(pg, arq.as_uri()); k0 = pg.evaluate(K); pg.click('#aviso .pri'); pg.wait_for_timeout(200)
        ok('o painel publicado abria com os exemplos (60 leituras)', k0.get('leituras') == '60', k0)
        salvo = usa(pg, CRIAR, EDITAR); e = json.loads(salvo); pg.context.close()
        ok('e gravava os exemplos sem dizer que foram pedidos', e.get('exemplos') is True and 'demo' not in e and sum(1 for x in e['livros'] if x.get('u')) == 3, (e.get('exemplos'), 'demo' in e))
        confere_saida('painel publicado', salvo, CRIAR, [t for _, t in EDITAR])
    b.close()
print('FALHAS:', falhas); print('ERROS:', len(errs) + len(falhas)); [print('  ', x[:300]) for x in errs[:10]]
