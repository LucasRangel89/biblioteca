"""A vistoria dos marcadores no painel — e o que acontece com os livros em que o usuário já tinha mexido.

Parte 1 — o catálogo revisto, como o painel o mostra: todo livro com dificuldade e extensão, os marcadores novos
com nome legível e nenhum livro sem eixo.

Parte 2 — quem usava o painel publicado antes da vistoria (tirado do histórico do Git) tem livros guardados no
navegador com a classificação antiga. Ao abrir o painel novo:
  · o que ele não mexeu acompanha a vistoria (tipo, eixo, dificuldade, extensão e temas);
  · o que ele pôs, tirou ou trocou à mão fica como ele deixou;
  · os livros renomeados nesta rodada continuam sendo o mesmo livro, com o que ele tinha anotado.
Sem Git, ou sem aquele commit no histórico, essa parte é pulada (com aviso).

Parte 3 — daqui em diante o painel guarda, em cada livro mexido, a classificação que o catálogo dava a ele. Quando o
catálogo mudar de novo, a mesma regra vale: o que mudou só no catálogo entra; o que o usuário mudou fica.

Os números esperados são um retrato do catálogo atual; se o catálogo mudar, confira as linhas FALHA e atualize.
"""
from caminhos import PAINEL_LIMPO, RAIZ, TMP
from relogio import fixa
import json, subprocess
from playwright.sync_api import sync_playwright

ANTERIOR = '50f5371:Biblioteca_Lucas_Dashboard.html'      # o painel publicado até 10/11/2026, antes da vistoria
CHAVE = 'biblioteca-lucas:v1'
errs = []; falhas = []
K = "() => Object.fromEntries([...document.querySelectorAll('.visao:not([hidden]) .kpi')].map(k => [k.dataset.k, {v: k.querySelector('.kpi-v b').textContent.replace(/\\u00a0/g, ' '), s: k.querySelector('.kpi-s').textContent.replace(/\\u00a0/g, ' ')}]))"
TOASTS = "() => [...document.querySelectorAll('#toasts .toast')].map(t => t.textContent.replace(/\\u00a0/g, ' ')).join(' ¦ ')"
GAVETA = "() => document.querySelector('#gaveta').classList.contains('on') ? document.querySelector('#gaveta h2').textContent : ''"
CHIPS = "() => [...document.querySelectorAll('#gaveta .gv-ch .tag')].map(t => t.textContent.replace(/\\s+/g, ' ').trim())"


def ok(nome, cond, extra=''):
    print(('  ok   ' if cond else '  FALHA') + ' ' + nome + (' — ' + str(extra)[:700] if extra != '' else ''))
    if not cond: falhas.append(nome)


def pagina(b, salvo=None):
    """Página nova; `salvo` é o texto que o navegador já teria guardado (posto uma única vez, antes do painel carregar)."""
    ctx = b.new_context(viewport={'width': 1440, 'height': 900}, locale='pt-BR', timezone_id='America/Sao_Paulo', accept_downloads=True)
    if salvo is not None:
        ctx.add_init_script("(() => { try { if (!sessionStorage.getItem('qa-posto') && window.name !== 'qa-posto') { localStorage.setItem(%s, %s); } sessionStorage.setItem('qa-posto', '1'); window.name = 'qa-posto'; } catch (e) {} })()" % (json.dumps(CHAVE), json.dumps(salvo)))
    pg = ctx.new_page(); fixa(pg)
    pg.on('console', lambda m: errs.append(f'[{m.type}] {m.text}') if m.type in ('error', 'warning') else None)
    pg.on('pageerror', lambda e: errs.append(f'[pageerror] {e}'))
    return pg


def abrir(pg, busca, titulo):
    """Abre a ficha do livro pela tabela da visão geral."""
    for _ in range(2): pg.keyboard.press('Escape'); pg.wait_for_timeout(150)
    pg.fill('#p-tab-geral input[type=search]', busca); pg.wait_for_timeout(600)
    pg.locator('#p-tab-geral tbody tr[data-id]').filter(has=pg.locator('.tt b', has_text=titulo)).first.click(); pg.wait_for_timeout(700)


def lista_de(pg):
    return pg.evaluate("() => JSON.parse(localStorage.getItem('%s')).livros" % CHAVE)


def livros_de(pg):
    """Os livros guardados, pelo título (há títulos repetidos no catálogo; para contar, use lista_de)."""
    return {x['t']: x for x in lista_de(pg)}


with sync_playwright() as p:
    b = p.chromium.launch()

    print('O CATÁLOGO REVISTO, NO PAINEL')
    pg = pagina(b); pg.goto(PAINEL_LIMPO); pg.wait_for_timeout(1200); pg.click('#aviso .pri'); pg.wait_for_timeout(600)
    k = pg.evaluate(K); todos = lista_de(pg); L = livros_de(pg)
    ok('2.614 livros: 2.124 no acervo, 3 leituras, 487 recomendações na fila', len(todos) == 2614 and (k['acervo']['v'], k['leituras']['v'], k['recs']['v']) == ('2.124', '3', '487') and k['acervo']['s'] == '100 físicos · 2.049 digitais · 25 nos dois', {a: k[a] for a in ('acervo', 'recs')})
    semd = [x['t'] for x in todos if not any(m in x['tags'] for m in ('d1', 'd2', 'd3'))]; seme = [x['t'] for x in todos if not any(m in x['tags'] for m in ('e1', 'e2', 'e3'))]
    ok('todo livro tem dificuldade e extensão (antes, nenhum da biblioteca virtual tinha)', not semd and not seme, (len(semd), len(seme), semd[:3]))
    semtipo = [x['t'] for x in todos if not any(m in x['tags'] for m in ('F', 'NF', 'HQ', 'poesia', 'antologia'))]
    ok('todo livro tem tipo e um eixo de 1 a 16', not semtipo and all(1 <= x.get('eixo', 0) <= 16 for x in todos), semtipo[:5])
    c = L['Contato']; w = L['Walden II: Uma Sociedade do Futuro']; u = L['A Máquina de Uriel']
    ok('exemplos da vistoria: "Contato" e "Walden II" são ficção; "A Máquina de Uriel", não ficção', c['tags'][:5] == ['F', 'ficcao-cientifica', 'classico', 'd2', 'e2'] and c['eixo'] == 2 and 'F' in w['tags'] and w['eixo'] == 2 and 'NF' in u['tags'] and u['eixo'] == 12, (c['tags'], c['eixo'], u['tags'], u['eixo']))
    abrir(pg, 'Contato Sagan', 'Contato'); chips = pg.evaluate(CHIPS)
    ok('a ficha de um livro da biblioteca virtual mostra eixo, tipo, dificuldade e extensão', chips == ['Ficção científica e fantasia', 'Ficção', 'Média', 'Média · ~250–500 p.'], chips)
    pg.keyboard.press('Escape'); pg.wait_for_timeout(300); pg.fill('#p-tab-geral input[type=search]', ''); pg.wait_for_timeout(500)
    pg.click('#pw-mais .pop-b'); pg.wait_for_timeout(300)
    rot = pg.evaluate("() => Object.fromEntries([...document.querySelectorAll('#f-tags .chip')].map(c => [c.dataset.v, c.querySelector('span').textContent]))")
    novos = {'super-herois': 'Super-heróis', 'manga': 'Mangá', 'adaptacao': 'Adaptação em quadrinhos', 'cronicas': 'Crônicas', 'policial': 'Policial', 'aventura': 'Aventura', 'faroeste': 'Faroeste', 'mitologia': 'Mitologia',
             'educacao': 'Educação', 'biologia': 'Biologia', 'matematica': 'Matemática', 'programacao': 'Programação', 'dados': 'Dados e planilhas', 'design': 'Design', 'enigmas': 'Enigmas e mistérios'}
    ok('os 15 marcadores novos da vistoria aparecem nos filtros, com nome legível', all(rot.get(t) == n for t, n in novos.items()), {t: rot.get(t) for t in novos if rot.get(t) != novos[t]})
    usados = {m for x in todos for m in x['tags']} - {'F', 'NF', 'd1', 'd2', 'd3', 'e1', 'e2', 'e3', 'tenho-fisico', 'tenho-digital', 'lido', 'top'}
    ok('nenhum marcador do catálogo fica fora dos filtros', not (usados - set(rot)), sorted(usados - set(rot)))
    pg.click('#pop-mais .chips[data-grupo=dif] .chip[data-v="1"]'); pg.wait_for_timeout(700); pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
    leves = pg.evaluate(K)['acervo']['v']; esperado = sum(1 for x in todos if 'd1' in x['tags'] and x.get('col') == 'acervo')
    ok('filtrar por dificuldade agora alcança a biblioteca virtual', leves == f'{esperado:,}'.replace(',', '.') and esperado > 900, (leves, esperado))
    pg.context.close()

    print('QUEM JÁ USAVA O PAINEL ANTERIOR')
    try: antigo = subprocess.run(['git', 'show', ANTERIOR], cwd=str(RAIZ), capture_output=True, check=True).stdout
    except Exception as e: antigo = None; motivo = type(e).__name__
    if antigo is None:
        print(f'  (pulado: não consegui tirar o painel anterior do histórico do Git — {motivo}. Numa cópia rasa do repositório, rode: git fetch --unshallow)')
    else:
        (TMP / 'painel-antes-da-vistoria.html').write_bytes(antigo)
        pg = pagina(b); pg.goto((TMP / 'painel-antes-da-vistoria.html').as_uri()); pg.wait_for_timeout(1200); pg.click('#aviso .pri'); pg.wait_for_timeout(300)
        k0 = pg.evaluate(K)
        ok('o painel anterior: 2.125 no acervo, 433 recomendações', (k0['acervo']['v'], k0['recs']['v']) == ('2.125', '433'), {a: k0[a]['v'] for a in k0})
        def form(campos):
            pg.click('#gv-acoes [data-acao=editar]'); pg.wait_for_timeout(500)
            for f, v in campos.items():
                if f in ('tipo', 'd', 'e', 'eixo'): pg.select_option(f'#dlg [data-f={f}]', str(v))
                else: pg.fill(f'#dlg [data-f={f}]', v)
            pg.click('#dlg footer .pri'); pg.wait_for_timeout(700)
        # 1 ▸ só marcou como lido: não mexeu na classificação
        abrir(pg, 'Contato Sagan', 'Contato'); pg.click('#gv-acoes [data-acao=lido]'); pg.wait_for_timeout(400); pg.click('#dlg footer .pri'); pg.wait_for_timeout(700)
        # 2 ▸ deu a dificuldade à mão e pôs um marcador seu; não mexeu em tipo nem em eixo
        abrir(pg, 'Walden II', 'Walden II'); marc = pg.evaluate("() => { document.querySelector('#gv-acoes [data-acao=editar]').click(); return new Promise(r => setTimeout(() => { const v = document.querySelector('#dlg [data-f=tags]').value; document.querySelector('#dlg [data-fechar]').click(); r(v); }, 400)); }"); pg.wait_for_timeout(300)
        form({'d': 3, 'tags': marc + ' favorito'})
        # 3 ▸ trocou o tipo e o eixo e tirou um marcador: tudo escolha dele
        abrir(pg, 'Nascente Rand', 'A Nascente'); form({'tipo': 'P', 'eixo': 16, 'tags': ''})
        # 4 ▸ começou a ler um livro da estante cuja dificuldade a vistoria recalibrou
        abrir(pg, 'Fundação Asimov', 'Fundação'); pg.click('#gv-acoes [data-acao=ler]'); pg.wait_for_timeout(600)
        # 5 ▸ ele mesmo já tinha corrigido o tipo, do mesmo jeito que a vistoria corrigiu depois
        abrir(pg, 'Máquina de Uriel', 'A Máquina de Uriel'); form({'tipo': 'NF'})
        # 6 ▸ duas recomendações postas na lista de compra: uma só ganhou camadas; a outra mudou de título e agora está na biblioteca virtual
        abrir(pg, 'Estrada McCarthy', 'A Estrada'); pg.click('#gv-acoes [data-acao=desejar]'); pg.wait_for_timeout(600)
        abrir(pg, 'Olhando para o Sol', 'Olhando para o Sol'); pg.click('#gv-acoes [data-acao=desejar]'); pg.wait_for_timeout(600)
        # 7 ▸ o mesmo livro estava duas vezes no catálogo (duas edições); ele marcou como lida a que a vistoria juntou à outra
        abrir(pg, 'Vidas Seguintes', 'Vidas Seguintes'); pg.click('#gv-acoes [data-acao=lido]'); pg.wait_for_timeout(400); pg.click('#dlg footer .pri'); pg.wait_for_timeout(700)
        pg.keyboard.press('Escape'); pg.wait_for_timeout(700)
        salvo = pg.evaluate("() => localStorage.getItem('%s')" % CHAVE); A = {x['t']: x for x in json.loads(salvo)['livros']}
        ok('no painel anterior ficaram oito livros mexidos, com a classificação antiga', sorted(t for t, x in A.items() if x.get('u')) == ['A Estrada', 'A Máquina de Uriel', 'A Nascente', 'Contato', 'Fundação', 'Olhando para o Sol', 'Vidas Seguintes', 'Walden II: Uma Sociedade do Futuro']
           and A['Contato']['tags'] == ['NF', 'ciencia', 'fisica', 'tenho-digital', 'lido'] and A['Contato']['eixo'] == 13 and 'cl' not in A['Contato'] and A['Walden II: Uma Sociedade do Futuro']['tags'] == ['NF', 'd3', 'psicologia', 'behaviorismo', 'favorito', 'tenho-digital']
           and A['A Nascente']['tags'] == ['poesia', 'tenho-digital'] and A['A Nascente']['eixo'] == 16, {t: (x['tags'], x.get('eixo')) for t, x in A.items() if x.get('u')})
        pg.context.close()

        pg = pagina(b, salvo); pg.goto(PAINEL_LIMPO); pg.wait_for_timeout(1500); t = pg.evaluate(TOASTS); pg.wait_for_timeout(700)
        N = livros_de(pg); k = pg.evaluate(K); total = len(lista_de(pg))
        ok('o painel novo abre com os dados antigos e avisa que o catálogo mudou', t == 'O catálogo mudou: 60 livros entraram e 6 saíram. O que você editou no painel foi mantido.' and total == 2614, (t, total))
        ok('os indicadores: os dois livros lidos contam; os dois postos na lista de compra não estão no acervo nem nas recomendações', (k['acervo']['v'], k['leituras']['v'], k['recs']['v']) == ('2.123', '5', '486'), {a: k[a]['v'] for a in k})
        x = N['Contato']
        ok('1 ▸ só marcado como lido: a classificação acompanha a vistoria (ficção, eixo 2, temas trocados) e a leitura fica', x['tags'] == ['F', 'd2', 'e2', 'ficcao-cientifica', 'classico', 'tenho-digital', 'lido'] and x['eixo'] == 2 and x.get('leit') == 'lido' and x.get('u') == 1, (x['tags'], x['eixo'], x.get('leit')))
        ok('    e o livro passa a guardar a classificação do catálogo de agora, para a próxima mudança', x.get('cl') == '2|F ficcao-cientifica classico d2 e2', x.get('cl'))
        x = N['Walden II: Uma Sociedade do Futuro']
        ok('2 ▸ dificuldade dada à mão e marcador próprio ficam; tipo, eixo, extensão e temas vêm da vistoria', x['tags'] == ['F', 'd3', 'e2', 'behaviorismo', 'utopia', 'classico', 'favorito', 'tenho-digital'] and x['eixo'] == 2, (x['tags'], x['eixo']))
        x = N['A Nascente']
        ok('3 ▸ tipo e eixo trocados à mão ficam; o marcador tirado não volta; o que a vistoria acrescentou entra', x['tags'] == ['poesia', 'd2', 'e3', 'politica', 'tenho-digital'] and x['eixo'] == 16, (x['tags'], x['eixo']))
        x = N['Fundação']
        ok('4 ▸ livro da estante em leitura: dificuldade e extensão recalibradas, camadas novas, leitura mantida', x['tags'][:5] == ['F', 'd1', 'e1', 'ficcao-cientifica', 'classico'] and 'trilha-ficcao-cientifica-classica' in x['tags'] and 'clima-cerebral' in x['tags'] and 'd2' not in x['tags'] and x.get('leit') == 'lendo' and x.get('fmt') == 'fisico', (x['tags'], x.get('leit')))
        x = N['A Máquina de Uriel']
        ok('5 ▸ o tipo que ele já tinha corrigido fica; o eixo, em que não mexeu, acompanha a vistoria', x['tags'] == ['NF', 'd2', 'e2', 'historia', 'mistica', 'enigmas', 'tenho-digital'] and x['eixo'] == 12, (x['tags'], x['eixo']))
        x = N['A Estrada']
        ok('6 ▸ recomendação na lista de compra: continua lá e ganha as camadas', x.get('col') == 'desejo' and x.get('prio') == 1 and 'trilha-relampago' in x['tags'] and 'papel-porta-de-entrada' in x['tags'] and x['tags'][:6] == ['F', 'd1', 'e1', 'distopia', 'contemporaneo', 'top'], (x.get('col'), x['tags']))
        x = N.get('De Frente para o Sol: Como Superar o Terror da Morte') or {}
        ok('    a que mudou de título é o mesmo livro: segue na lista de compra, agora sabendo que há o digital', 'Olhando para o Sol' not in N and x.get('col') == 'desejo' and x.get('u') == 1 and 'tenho-digital' in x.get('tags', []) and 'trilha-finitude' in x.get('tags', []), (x.get('col'), x.get('tags')))
        abrir(pg, 'Olhando para o Sol', 'De Frente para o Sol'); antes_txt = pg.evaluate("() => { const s = document.querySelector('#gv-antes'); return s ? s.textContent.replace(/\\s+/g, ' ') : ''; }")
        ok('    a busca ainda o acha pelo título antigo, e a ficha diz que o título foi corrigido', pg.evaluate(GAVETA) == 'De Frente para o Sol: Como Superar o Terror da Morte' and 'Olhando para o Sol' in antes_txt, antes_txt)
        x = N.get('Sobrevidas') or {}
        ok('7 ▸ duas edições que viraram uma linha só: fica a que ele marcou como lida, com o título da linha e os dois arquivos', 'Vidas Seguintes' not in N and x.get('leit') == 'lido' and x.get('u') == 1 and x.get('arq') == '1r61pzp v1n83x' and x['tags'] == ['F', 'd2', 'e2', 'colonialismo', 'africa', 'tenho-digital', 'lido'], (x.get('leit'), x.get('arq'), x.get('tags')))
        abrir(pg, 'Walden II', 'Walden II'); chips = pg.evaluate(CHIPS)
        ok('na ficha: eixo e tipo novos, a dificuldade dele e a extensão da vistoria', chips == ['Ficção científica e fantasia', 'Ficção', 'Exigente', 'Média · ~250–500 p.'], chips)
        intactos = [t for t, x in N.items() if not x.get('u') and 'cl' in x]
        ok('livro em que ninguém mexeu não guarda classificação à parte (segue o catálogo)', not intactos, intactos[:3])
        pg.keyboard.press('Escape'); pg.wait_for_timeout(300); pg.reload(); pg.wait_for_timeout(1500)
        ok('recarregar não repete o aviso nem muda nada', 'O catálogo mudou' not in pg.evaluate(TOASTS) and livros_de(pg)['A Nascente']['tags'] == ['poesia', 'd2', 'e3', 'politica', 'tenho-digital'], pg.evaluate(TOASTS))
        pg.context.close()

    print('DAQUI EM DIANTE: O CATÁLOGO MUDA DE NOVO')
    # No painel novo, mexe em quatro livros; depois adultera o que ficou salvo para parecer que o catálogo de quando
    # eles foram mexidos era outro (a "base", campo cl) — é como o painel verá a próxima mudança do catálogo.
    pg = pagina(b); pg.goto(PAINEL_LIMPO); pg.wait_for_timeout(1200); pg.click('#aviso .pri'); pg.wait_for_timeout(300)
    for busca, titulo in (('Ecce Homo', 'Ecce Homo'), ('Peste Camus', 'A Peste'), ('Nome da Rosa', 'O Nome da Rosa'), ('Duna Herbert', 'Duna')):
        abrir(pg, busca, titulo); pg.fill('#nt-com', 'Mexido no painel.'); pg.wait_for_timeout(900)
    pg.keyboard.press('Escape'); pg.wait_for_timeout(700)
    est = json.loads(pg.evaluate("() => localStorage.getItem('%s')" % CHAVE)); S = {x['t']: x for x in est['livros']}
    cat = {t: (S[t]['eixo'], [m for m in S[t]['tags'] if m not in ('tenho-fisico', 'tenho-digital', 'lido')]) for t in ('Ecce Homo', 'A Peste', 'O Nome da Rosa', 'Duna')}
    ok('ponto de partida: os quatro livros guardam a classificação do catálogo', all(S[t].get('cl') == f'{cat[t][0]}|{" ".join(cat[t][1])}' for t in cat), {t: S[t].get('cl') for t in cat})
    sit = lambda t: [m for m in S[t]['tags'] if m in ('tenho-fisico', 'tenho-digital', 'lido')]
    def simular(t, base_eixo, base_tags, meu_eixo, minhas):
        S[t]['cl'] = f'{base_eixo}|{" ".join(base_tags)}'; S[t]['eixo'] = meu_eixo; S[t]['tags'] = minhas + sit(t)
    e, T = cat['Ecce Homo']          # o catálogo "antigo" tinha outro eixo, outra dificuldade, um marcador a menos e um a mais; o usuário não mexeu em nada
    outro = lambda n: 5 if n != 5 else 6
    d_cat = next(m for m in T if m in ('d1', 'd2', 'd3')); d_velho = 'd1' if d_cat != 'd1' else 'd2'
    velhas = [d_velho if m == d_cat else m for m in T if m != 'classico'] + ['tagvelha']
    simular('Ecce Homo', outro(e), velhas, outro(e), list(velhas))
    e2, T2 = cat['A Peste']          # o usuário trocou o eixo e a extensão, pôs um marcador e tirou outro; o catálogo não mudou
    e_cat = next(m for m in T2 if m in ('e1', 'e2', 'e3')); e_meu = 'e3' if e_cat != 'e3' else 'e1'; tirado = next(m for m in T2 if m not in ('F', 'NF', 'd1', 'd2', 'd3', 'e1', 'e2', 'e3', 'top'))
    simular('A Peste', e2, list(T2), outro(e2), [e_meu if m == e_cat else m for m in T2 if m != tirado] + ['minha-marca'])
    e3, T3 = cat['O Nome da Rosa']   # os dois mexeram: o catálogo trocou a dificuldade e ganhou um marcador; o usuário trocou o tipo e tirou a prioridade
    d3_cat = next(m for m in T3 if m in ('d1', 'd2', 'd3')); d3_velho = 'd1' if d3_cat != 'd1' else 'd2'
    base3 = [d3_velho if m == d3_cat else m for m in T3 if m != 'medieval']
    simular('O Nome da Rosa', e3, base3, e3, ['NF' if m == 'F' else m for m in base3 if m != 'top'])
    e4, T4 = cat['Duna']             # nada mudou em lugar nenhum
    est['cat'] = 'outro-catalogo'; est['livros'] = list(S.values())
    pg.context.close()
    pg = pagina(b, json.dumps(est, ensure_ascii=False)); pg.goto(PAINEL_LIMPO); pg.wait_for_timeout(1500); pg.wait_for_timeout(700); N = livros_de(pg)
    x = N['Ecce Homo']; limpo = lambda x: [m for m in x['tags'] if m not in ('tenho-fisico', 'tenho-digital', 'lido')]
    ok('mudou só no catálogo (eixo, dificuldade, marcador novo, marcador retirado): o livro acompanha', x['eixo'] == e and sorted(limpo(x)) == sorted(T) and 'tagvelha' not in x['tags'] and x.get('com') == 'Mexido no painel.', (x['eixo'], x['tags'], (e, T)))
    x = N['A Peste']
    ok('mudou só no painel (eixo, extensão, marcador posto, marcador tirado): fica como o usuário deixou', x['eixo'] == outro(e2) and e_meu in x['tags'] and e_cat not in x['tags'] and 'minha-marca' in x['tags'] and tirado not in x['tags'], (x['eixo'], x['tags'], tirado))
    x = N['O Nome da Rosa']
    ok('mudaram os dois, em coisas diferentes: cada mudança vale (tipo e prioridade do usuário; dificuldade e marcador do catálogo)', 'NF' in x['tags'] and 'F' not in x['tags'] and 'top' not in x['tags'] and d3_cat in x['tags'] and d3_velho not in x['tags'] and 'medieval' in x['tags'] and x['eixo'] == e3, (x['tags'], x['eixo']))
    x = N['Duna']
    ok('nada mudou: nada muda', x['eixo'] == e4 and sorted(limpo(x)) == sorted(T4), (x['eixo'], x['tags']))
    ok('e a base de cada livro passa a ser o catálogo de agora', all(N[t].get('cl') == f'{cat[t][0]}|{" ".join(cat[t][1])}' for t in cat), {t: N[t].get('cl') for t in cat})
    b.close()
print('FALHAS:', falhas); print('ERROS:', len(errs) + len(falhas)); [print('  ', x[:300]) for x in errs[:10]]
