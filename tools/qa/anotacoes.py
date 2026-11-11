"""Suas anotações na ficha do livro: comentários, "possui análise", arquivos anexados e capa enviada.

O painel é aberto como o usuário o abre (sem dados de exemplo). Confere que:
  · o comentário é gravado sozinho (ao parar de digitar, ao fechar a ficha e quando a página sai de cena), aparece na
    aba "Com anotações", é achado pela busca e pode ser apagado;
  · "Possui análise" marca o livro, vira filtro, não aparece no campo de marcadores do formulário e não se perde ao editar;
  · um arquivo anexado fica guardado no navegador (IndexedDB), abre na tela se for texto (UTF-8, Windows-1252 ou UTF-16),
    baixa igual ao original, respeita os limites (vazio, 5 MB, 8 por livro) e sai quando removido;
  · a capa enviada é reduzida para o tamanho de uma capa, vale mais que a do catálogo, aparece mesmo com as capas
    desligadas, pode ser trocada e tirada; arquivo que não é imagem é recusado;
  · tudo isso sobrevive a recarregar a página e vai e volta num backup — inclusive para um navegador que nunca viu o painel;
  · um backup adulterado não entra pela metade, e um backup antigo (sem anexos) não apaga os anexos que estão no navegador;
  · na pré-visualização que bloqueia o armazenamento, as anotações funcionam enquanto a página estiver aberta.
"""
from caminhos import PAINEL_LIMPO, TMP
from relogio import fixa, png
import json
from playwright.sync_api import sync_playwright

CHAVE = 'biblioteca-lucas:v1'
errs = []; falhas = []
TOAST = "() => { const t = [...document.querySelectorAll('#toasts .toast')].map(t => t.textContent.replace(/\\u00a0/g, ' ')); return t[t.length - 1] || ''; }"
DLG = "() => document.querySelector('#dlg').classList.contains('on') ? document.querySelector('#dlg h2').textContent : ''"
# o que está guardado no banco do navegador (IndexedDB), sem o conteúdo: [{k, livro, tipo, nome, tam, ini}].
# Só olha: se o banco ainda não existe, não o cria (abrir um banco que não existe o criaria vazio, sem a tabela).
IDB = """async () => { if (!(await indexedDB.databases()).some(d => d.name === 'biblioteca-lucas')) return [];
  return new Promise(res => { const p = indexedDB.open('biblioteca-lucas'); p.onerror = () => res('erro');
    p.onsuccess = () => { const db = p.result; if (!db.objectStoreNames.contains('anexos')) { db.close(); res('sem tabela'); return; }
      const r = db.transaction('anexos').objectStore('anexos').getAll();
      r.onsuccess = () => { db.close(); res(r.result.map(x => ({k: x.k, livro: x.livro, tipo: x.tipo, nome: x.nome, tam: x.tam, ini: x.dados.slice(0, 22)}))); }; }; }); }"""
ARQS = "() => [...document.querySelectorAll('#nt-arqs li')].map(l => ({nome: l.querySelector('b').textContent, info: l.querySelector('small').textContent.replace(/\\u00a0/g, ' '), acoes: [...l.querySelectorAll('[data-nt]')].map(b => b.dataset.nt)}))"
CAPA_GV = "() => { const i = document.querySelector('#gv-topo .capa img'); return i ? {ini: i.src.slice(0, 22), w: i.naturalWidth, h: i.naturalHeight} : null; }"
CAPA_TB = "() => { const i = document.querySelector('#p-tab-geral tbody tr .capa img'); return i ? i.src.slice(0, 22) : null; }"
ABAS = "() => Object.fromEntries([...document.querySelectorAll('#p-tab-geral .abas [data-a]')].map(a => [a.dataset.a, +a.querySelector('.cont').textContent.replace(/\\D/g, '')]))"
LINHAS = "() => [...document.querySelectorAll('#p-tab-geral tbody tr .tt b')].map(b => b.textContent.trim())"
JPEG = 'data:image/jpeg;base64'

# arquivos de teste
RESENHA = 'Resenha de teste.\nSegunda linha, com acentuação: coração, ação, à toa.\n'
(TMP / 'resenha.txt').write_text(RESENHA, encoding='utf-8')
(TMP / 'ficha-antiga.txt').write_bytes('Fichamento em Windows-1252: coração, pé, maçã.'.encode('cp1252'))
(TMP / 'notas-utf16.txt').write_bytes('\ufeffAnotações em UTF-16: ação e reação.'.encode('utf-16-le'))
(TMP / 'relatorio.pdf').write_bytes(b'%PDF-1.4\n' + bytes(range(256)) * 4)
(TMP / 'vazio.txt').write_bytes(b'')
(TMP / 'grande.bin').write_bytes(b'x' * (5 * 1048576 + 1))
(TMP / 'capa.png').write_bytes(png(200, 40, 40, 600, 900))
(TMP / 'capa-larga.png').write_bytes(png(40, 90, 200, 2000, 500))
(TMP / 'capa-pequena.png').write_bytes(png(40, 160, 90, 120, 180))
(TMP / 'nao-e-imagem.png').write_text('isto não é uma imagem', encoding='utf-8')
for i in range(8): (TMP / f'nota-{i}.md').write_text(f'# Nota {i}\n', encoding='utf-8')


def ok(nome, cond, extra=''):
    print(('  ok   ' if cond else '  FALHA') + ' ' + nome + (' — ' + str(extra)[:600] if extra != '' else ''))
    if not cond: falhas.append(nome)


def nova_pagina(b, **extra):
    ctx = b.new_context(viewport={'width': 1440, 'height': 900}, locale='pt-BR', timezone_id='America/Sao_Paulo', accept_downloads=True, **extra)
    pg = ctx.new_page(); fixa(pg)
    pg.on('console', lambda m: errs.append(f'[{m.type}] {m.text}') if m.type in ('error', 'warning') else None)
    pg.on('pageerror', lambda e: errs.append(f'[pageerror] {e}'))
    return pg


with sync_playwright() as p:
    b = p.chromium.launch()
    pg = nova_pagina(b)
    pg.goto(PAINEL_LIMPO); pg.wait_for_timeout(1200); pg.click('#aviso .pri'); pg.wait_for_timeout(200)

    def fechar():
        for _ in range(3): pg.keyboard.press('Escape'); pg.wait_for_timeout(150)
    def abrir(busca, titulo):
        """Abre a ficha do livro pela tabela da visão geral."""
        fechar()
        if not pg.is_visible('#p-tab-geral'): pg.click('#nav [data-ir=geral]'); pg.wait_for_timeout(800)
        pg.fill('#p-tab-geral input[type=search]', busca); pg.wait_for_timeout(600)
        pg.locator('#p-tab-geral tbody tr[data-id]').filter(has=pg.locator('.tt b', has_text=titulo)).first.click(); pg.wait_for_timeout(700)
    guardado = lambda titulo: pg.evaluate("t => (JSON.parse(localStorage.getItem('%s')).livros.find(x => x.t === t) || null)" % CHAVE, titulo)
    def anexar(nome, espera=900): pg.set_input_files('#nt-f-arq', str(TMP / nome)); pg.wait_for_timeout(espera); return pg.evaluate(TOAST)
    def capa(nome, espera=1100): pg.set_input_files('#nt-f-capa', str(TMP / nome)); pg.wait_for_timeout(espera); return pg.evaluate(TOAST)

    print('A FICHA')
    abrir('Quando Nietzsche Chorou', 'Quando Nietzsche Chorou')
    sec = pg.evaluate("""() => { const s = document.querySelector('#gv-notas'), ta = s.querySelector('#nt-com');
      return {tit: s.querySelector('h4').textContent, rotulo: ta.getAttribute('aria-label'), max: ta.maxLength, valor: ta.value, marcado: s.querySelector('#nt-an').checked,
        arquivos: s.querySelectorAll('#nt-arqs li').length, botoes: [...s.querySelectorAll('.nt-b .btn')].filter(b => !b.hidden).map(b => b.textContent), nota: s.querySelector('#nt-n').textContent,
        rotulada: s.getAttribute('aria-labelledby') === 'nt-t', escondidos: [...s.querySelectorAll('input[type=file]')].every(i => i.hidden && i.tabIndex === -1)}; }""")
    ok('a ficha tem a seção "Suas anotações", vazia', sec['tit'] == 'Suas anotações' and sec['valor'] == '' and not sec['marcado'] and sec['arquivos'] == 0 and sec['max'] == 5000 and sec['rotulo'] == 'Comentários sobre este livro' and sec['rotulada'] and sec['escondidos'], sec)
    ok('com os botões de anexar e de enviar a capa (o livro já tem capa do catálogo)', sec['botoes'] == ['Anexar arquivo…', 'Enviar outra capa…'] and 'só neste navegador' in sec['nota'] and 'backup' in sec['nota'], sec['botoes'])
    ok('antes de qualquer anotação o banco de anexos está vazio', pg.evaluate(IDB) == [], pg.evaluate(IDB))

    print('COMENTÁRIOS')
    C1 = 'Li em 2019. A conversa entre Breuer e Nietzsche vale o livro.'
    pg.fill('#nt-com', C1); pg.wait_for_timeout(1300)
    g = guardado('Quando Nietzsche Chorou'); st = pg.inner_text('#nt-st')
    ok('o comentário é gravado sozinho, pouco depois de parar de digitar', g.get('com') == C1 and g.get('u') == 1 and st == 'Comentário salvo', (st, g.get('com')))
    ok('o livro guarda a classificação que o catálogo dava a ele (base para futuras atualizações do catálogo)', (g.get('cl') or '').startswith('14|F psicologia filosofia d1 e2') and 'tenho-fisico' not in g.get('cl', ''), g.get('cl'))
    ok('o campo continua com o foco e o texto (a ficha não é redesenhada por cima)', pg.evaluate("() => document.activeElement.id === 'nt-com' && document.activeElement.value.length") == len(C1))
    abas = pg.evaluate(ABAS)
    ok('aba "Com anotações" e "Editados por você" passam a contar o livro', abas.get('notas') == 1 and abas.get('meus') == 1, abas)
    ok('na tabela, o livro ganha a marca de anotação', pg.evaluate("() => { const i = document.querySelector('#p-tab-geral tbody tr .tem-nota'); return i ? i.title : null; }") == 'Tem anotações suas')
    C2 = C1 + ' Reler antes de A Cura de Schopenhauer.'
    pg.fill('#nt-com', C2); pg.keyboard.press('Escape'); pg.wait_for_timeout(600)
    ok('fechar a ficha logo depois de digitar grava o que estava no campo', guardado('Quando Nietzsche Chorou').get('com') == C2, guardado('Quando Nietzsche Chorou').get('com'))
    pg.fill('#q', 'Schopenhauer reler'); pg.wait_for_timeout(500)
    achados = pg.evaluate("() => [...document.querySelectorAll('#q-r .qr b')].map(b => b.textContent)")
    ok('a busca acha o livro por palavras do comentário', achados == ['Quando Nietzsche Chorou'], achados)
    pg.fill('#q', ''); fechar()
    abrir('Ecce Homo', 'Ecce Homo')
    pg.fill('#nt-com', 'Digitado e a página saiu de cena.'); pg.evaluate("() => window.dispatchEvent(new Event('pagehide'))")
    ok('se a página sai de cena (aba fechada, outro aplicativo), o comentário em edição é gravado na hora', guardado('Ecce Homo').get('com') == 'Digitado e a página saiu de cena.', guardado('Ecce Homo').get('com'))
    pg.fill('#nt-com', 'x' * 4600); pg.wait_for_timeout(300)
    ok('perto do limite, a ficha mostra a contagem e sugere anexar um arquivo', pg.is_visible('#nt-cont') and '4.600 de 5.000' in pg.inner_text('#nt-cont') and 'anexe um arquivo' in pg.inner_text('#nt-cont'), pg.inner_text('#nt-cont'))
    pg.fill('#nt-com', ''); pg.wait_for_timeout(1300)
    g = guardado('Ecce Homo')
    ok('apagar o texto apaga o comentário', 'com' not in g and pg.inner_text('#nt-st') == 'Comentário apagado' and not pg.is_visible('#nt-cont'), g.get('com'))
    ok('e o livro sai da aba "Com anotações" (continua em "Editados por você")', pg.evaluate(ABAS).get('notas') == 0 and pg.evaluate(ABAS).get('meus') == 1, pg.evaluate(ABAS))
    abrir('Quando Nietzsche Chorou', 'Quando Nietzsche Chorou')
    ok('ao abrir outro livro e voltar, cada ficha mostra o seu comentário', pg.input_value('#nt-com') == C2, pg.input_value('#nt-com'))

    print('POSSUI ANÁLISE')
    abrir('O Nome da Rosa', 'O Nome da Rosa')
    pg.check('#nt-an'); pg.wait_for_timeout(600)
    g = guardado('O Nome da Rosa')
    ok('marcar "Possui análise" põe a marca no livro', 'analise' in g.get('tags', []) and g.get('u') == 1 and pg.inner_text('#nt-st') == 'Marcado: possui análise', g.get('tags'))
    ok('a marca não vira um marcador solto na ficha', pg.evaluate("() => [...document.querySelectorAll('#gaveta .gv-tags .tag')].map(t => t.dataset.tag)").count('analise') == 0)
    pg.click('#gv-acoes [data-acao=editar]'); pg.wait_for_timeout(500)
    campo = pg.input_value('#dlg [data-f=tags]'); dica = pg.evaluate("() => [...document.querySelectorAll('#dlg .form-n')].map(n => n.textContent).join(' | ')")
    ok('o formulário não mostra a marca no campo de marcadores e diz onde ficam as anotações', 'analise' not in campo.split() and 'Suas anotações' in dica, (campo, dica[-140:]))
    pg.fill('#dlg [data-f=obs]', 'Edição de bolso.'); pg.click('#dlg footer .pri'); pg.wait_for_timeout(700)
    g = guardado('O Nome da Rosa')
    ok('salvar o formulário não tira a marca', 'analise' in g.get('tags', []) and g.get('obs') == 'Edição de bolso.' and pg.is_checked('#nt-an'), g.get('tags'))
    fechar(); pg.fill('#p-tab-geral input[type=search]', ''); pg.wait_for_timeout(400)
    pg.click('#pw-mais .pop-b'); pg.wait_for_timeout(300)
    grupo = pg.evaluate("() => { const g = [...document.querySelectorAll('#f-tags .tg-g')].find(g => g.querySelector('.pop-r').textContent === 'Suas marcas'); return g ? [...g.querySelectorAll('.chip')].map(c => [c.dataset.v, c.textContent]) : null; }")
    ok('"Possui análise" é um filtro, no grupo "Suas marcas"', grupo == [['analise', 'Possui análise']], grupo)
    pg.click('#f-tags .chip[data-v=analise]'); pg.wait_for_timeout(700); pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
    ativos = pg.evaluate("() => [...document.querySelectorAll('#f-ativos .ativo')].map(a => a.textContent)")
    ok('filtrando por ele, sobra só o livro marcado', pg.evaluate(LINHAS) == ['O Nome da Rosa'] and ativos == ['Possui análise'], (pg.evaluate(LINHAS), ativos))
    ok('a marca da tabela diz "Possui análise"', pg.evaluate("() => { const i = document.querySelector('#p-tab-geral tbody tr .tem-nota'); return i ? i.title : null; }") == 'Possui análise')
    pg.click('#f-ativos .ativo'); pg.wait_for_timeout(600)
    abrir('O Nome da Rosa', 'O Nome da Rosa'); pg.uncheck('#nt-an'); pg.wait_for_timeout(600)
    ok('desmarcar tira a marca', 'analise' not in guardado('O Nome da Rosa').get('tags', []) and pg.inner_text('#nt-st') == 'Marca retirada', guardado('O Nome da Rosa').get('tags'))

    print('ARQUIVOS ANEXADOS')
    abrir('Quando Nietzsche Chorou', 'Quando Nietzsche Chorou'); idlivro = pg.evaluate("() => document.querySelector('#p-tab-geral tbody tr[data-id]').dataset.id")
    t = anexar('resenha.txt'); arqs = pg.evaluate(ARQS); banco = pg.evaluate(IDB); g = guardado('Quando Nietzsche Chorou')
    ok('um arquivo de texto anexado aparece na ficha, com tamanho e data', arqs == [{'nome': 'resenha.txt', 'info': '78 B · 09/11/2026', 'acoes': ['abrir', 'baixar', 'tirar']}], arqs)
    ok('o livro é marcado com "possui análise" e o aviso diz isso', pg.is_checked('#nt-an') and 'analise' in g['tags'] and t == 'Arquivo anexado. O livro foi marcado com “possui análise”.', t)
    ok('o conteúdo vai para o banco do navegador; no livro fica só a referência', len(banco) == 1 and banco[0]['tipo'] == 'arquivo' and banco[0]['livro'] == idlivro and banco[0]['nome'] == 'resenha.txt' and banco[0]['tam'] == 78
       and g.get('anx') == [[banco[0]['k'], 'resenha.txt', 78, 20766, 'text/plain']] and RESENHA[:12] not in json.dumps(g), (banco, g.get('anx')))
    ok('o comentário digitado antes continua lá', pg.input_value('#nt-com') == C2 and g.get('com') == C2)
    pg.click('#nt-arqs [data-nt=abrir]'); pg.wait_for_timeout(500)
    ok('"abrir" mostra o texto na tela', pg.evaluate(DLG) == 'resenha.txt' and pg.inner_text('#dlg .anexo-txt') == RESENHA and 'Quando Nietzsche Chorou' in pg.inner_text('#dlg .dlg-sub'), (pg.evaluate(DLG), pg.inner_text('#dlg .anexo-txt')[:60]))
    with pg.expect_download() as d: pg.click('#dlg footer .btn >> nth=0')
    ok('e "Baixar" devolve o arquivo igual ao original', d.value.suggested_filename == 'resenha.txt' and open(d.value.path(), 'rb').read() == RESENHA.encode('utf-8'), d.value.suggested_filename)
    pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
    ok('fechar o texto volta para a ficha, que continua aberta', pg.evaluate(DLG) == '' and pg.evaluate("() => document.querySelector('#gaveta').classList.contains('on')"))
    t2 = anexar('ficha-antiga.txt'); pg.click('#nt-arqs li:nth-child(2) [data-nt=abrir]'); pg.wait_for_timeout(500); txt = pg.inner_text('#dlg .anexo-txt'); pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
    ok('texto antigo do Windows (Windows-1252) abre com os acentos certos', txt == 'Fichamento em Windows-1252: coração, pé, maçã.' and t2 == 'Arquivo anexado.', (t2, txt))
    anexar('notas-utf16.txt'); pg.click('#nt-arqs li:nth-child(3) [data-nt=abrir]'); pg.wait_for_timeout(500); txt = pg.inner_text('#dlg .anexo-txt'); pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
    ok('texto em UTF-16 também', txt == 'Anotações em UTF-16: ação e reação.', txt)
    anexar('relatorio.pdf'); arqs = pg.evaluate(ARQS)
    ok('um PDF é guardado, mas não tem "abrir": só baixar e remover', arqs[3] == {'nome': 'relatorio.pdf', 'info': '1 KB · 09/11/2026', 'acoes': ['baixar', 'tirar']}, arqs[3])
    with pg.expect_download() as d: pg.click('#nt-arqs li:nth-child(4) [data-nt=baixar]')
    ok('e baixa byte a byte igual', open(d.value.path(), 'rb').read() == (TMP / 'relatorio.pdf').read_bytes(), d.value.suggested_filename)
    t = anexar('vazio.txt'); ok('arquivo vazio é recusado', t == 'Este arquivo está vazio.' and len(pg.evaluate(ARQS)) == 4, t)
    t = anexar('grande.bin', 1500); ok('arquivo acima de 5 MB é recusado, dizendo o limite', t == 'O arquivo tem 5,0 MB; o limite é de 5,0 MB por arquivo.' and len(pg.evaluate(ARQS)) == 4 and len(pg.evaluate(IDB)) == 4, t)
    for i in range(4): anexar(f'nota-{i}.md', 500)
    ok('cabem oito arquivos por livro', len(pg.evaluate(ARQS)) == 8 and len(pg.evaluate(IDB)) == 8, len(pg.evaluate(ARQS)))
    t = anexar('nota-4.md'); ok('o nono é recusado', t == 'Cada livro guarda até 8 arquivos. Remova um para anexar outro.' and len(pg.evaluate(ARQS)) == 8 and len(pg.evaluate(IDB)) == 8, t)
    pg.click('#nt-arqs li:nth-child(8) [data-nt=tirar]'); pg.wait_for_timeout(400); pergunta = pg.inner_text('#dlg .dlg-msg')
    pg.click('#dlg footer .btn >> nth=0'); pg.wait_for_timeout(400)
    ok('remover pede confirmação; cancelando, nada muda', 'nota-3.md' in pergunta and len(pg.evaluate(ARQS)) == 8, pergunta)
    for _ in range(5):
        pg.click('#nt-arqs li:last-child [data-nt=tirar]'); pg.wait_for_timeout(350); pg.click('#dlg footer .perigo'); pg.wait_for_timeout(500)
    arqs = pg.evaluate(ARQS); banco = pg.evaluate(IDB)
    ok('removidos, saem da ficha e do banco', [a['nome'] for a in arqs] == ['resenha.txt', 'ficha-antiga.txt', 'notas-utf16.txt'] and sorted(x['nome'] for x in banco) == ['ficha-antiga.txt', 'notas-utf16.txt', 'resenha.txt'], [a['nome'] for a in arqs])
    ok('a busca acha o livro pelo nome do arquivo anexado', pg.evaluate("() => { const q = document.querySelector('#p-tab-geral input[type=search]'); q.value = 'ficha-antiga'; q.dispatchEvent(new Event('input')); return new Promise(r => setTimeout(() => r([...document.querySelectorAll('#p-tab-geral tbody tr .tt b')].map(b => b.textContent.trim())), 500)); }") == ['Quando Nietzsche Chorou'])

    print('CAPA ENVIADA')
    antes = pg.evaluate(CAPA_GV)
    t = capa('capa.png'); gv = pg.evaluate(CAPA_GV); g = guardado('Quando Nietzsche Chorou'); banco = pg.evaluate(IDB); capas = [x for x in banco if x['tipo'] == 'capa']
    ok('a imagem enviada vira a capa do livro, reduzida para o tamanho de uma capa', t == 'Capa enviada.' and (antes or {}).get('ini', '').startswith('https://covers.openlib') and gv == {'ini': JPEG, 'w': 360, 'h': 540}, (antes, gv))
    ok('ela aparece também nas listas', pg.evaluate(CAPA_TB) == JPEG, pg.evaluate(CAPA_TB))
    ok('a imagem vai para o banco; no livro fica a referência', len(capas) == 1 and g.get('cp') == capas[0]['k'] and capas[0]['livro'] == idlivro and capas[0]['ini'] == JPEG and JPEG not in json.dumps(g), (capas, g.get('cp')))
    ok('os botões passam a oferecer trocar e tirar', pg.evaluate("() => [...document.querySelectorAll('#gv-notas .nt-b .btn')].filter(b => !b.hidden).map(b => b.textContent)") == ['Anexar arquivo…', 'Trocar a capa…', 'Tirar a capa enviada'])
    t = capa('nao-e-imagem.png'); ok('um arquivo que não é imagem é recusado e a capa fica como estava', t.startswith('Não consegui abrir este arquivo como imagem') and pg.evaluate(CAPA_GV) == gv and guardado('Quando Nietzsche Chorou').get('cp') == g['cp'], t)
    t = capa('capa-larga.png'); gv2 = pg.evaluate(CAPA_GV); banco = pg.evaluate(IDB); capas2 = [x for x in banco if x['tipo'] == 'capa']
    ok('trocar a capa: a nova cabe em 360 × 540 sem deformar e a antiga sai do banco', t == 'Capa trocada.' and gv2 == {'ini': JPEG, 'w': 360, 'h': 90} and len(capas2) == 1 and capas2[0]['k'] != capas[0]['k'], (gv2, len(capas2)))
    capa('capa-pequena.png'); gv3 = pg.evaluate(CAPA_GV)
    ok('imagem pequena não é ampliada', gv3 == {'ini': JPEG, 'w': 120, 'h': 180}, gv3)
    fechar(); pg.click('#b-dados'); pg.wait_for_timeout(400)
    dados = pg.evaluate("() => ({n: Object.fromEntries([...document.querySelectorAll('#dlg .dd-n > div')].map(d => [d.querySelector('dt').textContent, d.querySelector('dd').textContent])), txt: document.querySelector('#dlg .dados').innerText.replace(/\\s+/g, ' ')})")
    ok('"Seus dados" conta os livros com anotações e fala das capas enviadas e do backup', dados['n'].get('Com anotações') == '1' and dados['n'].get('Editados por você') == '3' and '(1 enviada até agora)' in dados['txt'] and 'comentários, as capas que você enviou e os arquivos anexados' in dados['txt'], dados['n'])
    pg.uncheck('#dlg [data-x=capas]'); pg.wait_for_timeout(600); fechar()
    pg.fill('#p-tab-geral input[type=search]', 'Nietzsche'); pg.wait_for_timeout(600)
    caps = pg.evaluate("() => [...document.querySelectorAll('#p-tab-geral tbody tr')].map(r => [r.querySelector('.tt b').textContent.trim(), (r.querySelector('.capa img') || {src: ''}).src.slice(0, 22)])")
    ok('com "Mostrar as capas" desligado, a capa enviada continua aparecendo (as do catálogo, não)', len(caps) > 2 and all((c == JPEG) == (t == 'Quando Nietzsche Chorou') for t, c in caps) and all(c in ('', JPEG) for _, c in caps), caps[:6])
    pg.click('#b-dados'); pg.wait_for_timeout(400); pg.check('#dlg [data-x=capas]'); pg.wait_for_timeout(600); fechar()

    print('RECARREGAR')
    pg.wait_for_timeout(500); pg.reload(); pg.wait_for_timeout(1800)
    pg.fill('#p-tab-geral input[type=search]', 'Quando Nietzsche Chorou'); pg.wait_for_timeout(600)
    ok('depois de recarregar, a capa enviada volta (vem do banco do navegador)', pg.evaluate(CAPA_TB) == JPEG, pg.evaluate(CAPA_TB))
    pg.click('#p-tab-geral tbody tr[data-id]'); pg.wait_for_timeout(700)
    ok('e a ficha traz o comentário, a marca, os três arquivos e a capa', pg.input_value('#nt-com') == C2 and pg.is_checked('#nt-an') and [a['nome'] for a in pg.evaluate(ARQS)] == ['resenha.txt', 'ficha-antiga.txt', 'notas-utf16.txt'] and pg.evaluate(CAPA_GV) == gv3,
       (pg.input_value('#nt-com')[:30], pg.evaluate(ARQS), pg.evaluate(CAPA_GV)))
    pg.click('#nt-arqs [data-nt=abrir]'); pg.wait_for_timeout(500)
    ok('o arquivo ainda abre', pg.inner_text('#dlg .anexo-txt') == RESENHA); pg.keyboard.press('Escape'); pg.wait_for_timeout(300)

    print('LIVRO CRIADO NO PAINEL')
    fechar(); pg.click('#b-novo'); pg.wait_for_timeout(500); pg.fill('#dlg [data-f=t]', 'Zz Livro com Anexos'); pg.click('#dlg footer .pri'); pg.wait_for_timeout(900)
    ok('livro novo: a ficha abre com o botão "Enviar capa…"', pg.inner_text('#gaveta h2') == 'Zz Livro com Anexos' and pg.evaluate(CAPA_GV) is None and pg.inner_text('#nt-capa-r') == 'Enviar capa…', pg.inner_text('#nt-capa-r'))
    capa('capa.png'); anexar('nota-5.md'); pg.fill('#nt-com', 'Comentário do livro novo.'); pg.wait_for_timeout(1200)
    n1 = len(pg.evaluate(IDB)); g = guardado('Zz Livro com Anexos')
    ok('capa, arquivo e comentário valem para um livro que não veio do catálogo', pg.evaluate(CAPA_GV) == {'ini': JPEG, 'w': 360, 'h': 540} and n1 == 6 and g.get('cp') and len(g.get('anx', [])) == 1 and g.get('com') == 'Comentário do livro novo.' and 'cl' not in g, (n1, g.get('anx')))
    pg.click('#nt-b [data-nt=sem-capa], [data-nt=sem-capa]'); pg.wait_for_timeout(600)
    ok('"Tirar a capa enviada": sem capa do catálogo, volta o desenho com a inicial', pg.evaluate(TOAST) == 'Capa enviada removida.' and pg.evaluate(CAPA_GV) is None and 'cp' not in guardado('Zz Livro com Anexos') and len(pg.evaluate(IDB)) == 5, pg.evaluate(TOAST))
    capa('capa.png')
    pg.click('#gv-acoes [data-acao=excluir]'); pg.wait_for_timeout(400); pg.click('#dlg footer .perigo'); pg.wait_for_timeout(700)
    banco = pg.evaluate(IDB)
    ok('excluir o livro leva junto a capa e os arquivos dele', guardado('Zz Livro com Anexos') is None and len(banco) == 4 and all(x['livro'] == idlivro for x in banco), [(x['tipo'], x['nome']) for x in banco])

    print('TIRAR A CAPA ENVIADA (livro do catálogo)')
    abrir('Quando Nietzsche Chorou', 'Quando Nietzsche Chorou')
    pg.click('[data-nt=sem-capa]'); pg.wait_for_timeout(700); gv = pg.evaluate(CAPA_GV)
    ok('volta a capa do catálogo e a imagem sai do banco', pg.evaluate(TOAST) == 'Capa enviada removida: voltou a do catálogo.' and gv and gv['ini'].startswith('https://covers.openlib') and 'cp' not in guardado('Quando Nietzsche Chorou') and [x['tipo'] for x in pg.evaluate(IDB)] == ['arquivo'] * 3, (pg.evaluate(TOAST), gv))
    capa('capa.png')

    print('BACKUP')
    fechar(); pg.wait_for_timeout(500); pg.click('#b-dados'); pg.wait_for_timeout(400)
    with pg.expect_download() as d: pg.click('#dlg [data-x=exportar]')
    d.value.save_as(f'{TMP}/anotacoes-backup.json'); bk = json.load(open(f'{TMP}/anotacoes-backup.json', encoding='utf-8'))
    liv = next(x for x in bk['livros'] if x['t'] == 'Quando Nietzsche Chorou'); anexos = bk.get('anexos') or []
    ok('o backup leva o comentário, a marca e as referências no livro', liv.get('com') == C2 and 'analise' in liv['tags'] and len(liv.get('anx', [])) == 3 and liv.get('cp'), {k: liv.get(k) for k in ('com', 'cp', 'anx')})
    ok('e os anexos por inteiro: os três arquivos e a capa', sorted((a['tipo'], a['nome']) for a in anexos) == [('arquivo', 'ficha-antiga.txt'), ('arquivo', 'notas-utf16.txt'), ('arquivo', 'resenha.txt'), ('capa', 'capa.png')]
       and {a['k'] for a in anexos} == {liv['cp']} | {x[0] for x in liv['anx']} and all(a['dados'].startswith('data:') for a in anexos), [(a['tipo'], a['nome'], len(a['dados'])) for a in anexos])
    txt_zerar = pg.evaluate("() => [...document.querySelectorAll('#dlg .dados section')].map(s => s.innerText).find(t => t.startsWith('Recomeçar'))")
    pg.click('#dlg [data-x=zerar]'); pg.wait_for_timeout(400); pergunta = pg.inner_text('#dlg .dlg-msg'); pg.click('#dlg footer .perigo'); pg.wait_for_timeout(1200)
    ok('"Recomeçar do catálogo original" avisa que comentários, capas e arquivos também saem', 'comentários, capas enviadas e arquivos anexados' in txt_zerar and 'comentários, capas enviadas, arquivos anexados' in pergunta, pergunta)
    pg.click('#aviso .pri'); pg.wait_for_timeout(300)
    ok('e apaga tudo: banco vazio, nenhum livro anotado', pg.evaluate(IDB) == [] and pg.evaluate(ABAS).get('notas') == 0 and pg.evaluate(ABAS).get('meus') == 0, (pg.evaluate(IDB), pg.evaluate(ABAS)))
    pg.click('#b-dados'); pg.wait_for_timeout(400); pg.set_input_files('#arq', f'{TMP}/anotacoes-backup.json'); pg.wait_for_timeout(800); pergunta = pg.inner_text('#dlg .dlg-msg')
    pg.click('#dlg footer .pri'); pg.wait_for_timeout(1500); fechar()
    ok('ao importar, a confirmação conta os anexos', '4 anexos (capas e arquivos)' in pergunta, pergunta)
    abrir('Quando Nietzsche Chorou', 'Quando Nietzsche Chorou')
    ok('importado, volta tudo: comentário, marca, arquivos e capa', pg.input_value('#nt-com') == C2 and pg.is_checked('#nt-an') and [a['nome'] for a in pg.evaluate(ARQS)] == ['resenha.txt', 'ficha-antiga.txt', 'notas-utf16.txt'] and pg.evaluate(CAPA_GV) == {'ini': JPEG, 'w': 360, 'h': 540} and len(pg.evaluate(IDB)) == 4,
       (pg.input_value('#nt-com')[:30], pg.evaluate(ARQS), pg.evaluate(CAPA_GV)))
    pg.click('#nt-arqs li:nth-child(2) [data-nt=abrir]'); pg.wait_for_timeout(500)
    ok('e o arquivo importado abre com o mesmo conteúdo', pg.inner_text('#dlg .anexo-txt') == 'Fichamento em Windows-1252: coração, pé, maçã.'); pg.keyboard.press('Escape'); pg.wait_for_timeout(300)

    print('BACKUP ANTIGO OU ADULTERADO')
    # um backup feito por um painel antigo não tem o campo "anexos": importá-lo não apaga o que está no navegador
    velho = dict(bk); velho.pop('anexos'); json.dump(velho, open(f'{TMP}/anotacoes-sem-anexos.json', 'w', encoding='utf-8'), ensure_ascii=False)
    fechar(); pg.click('#b-dados'); pg.wait_for_timeout(400); pg.set_input_files('#arq', f'{TMP}/anotacoes-sem-anexos.json'); pg.wait_for_timeout(800); pergunta = pg.inner_text('#dlg .dlg-msg')
    pg.click('#dlg footer .pri'); pg.wait_for_timeout(1500); fechar()
    abrir('Quando Nietzsche Chorou', 'Quando Nietzsche Chorou')
    ok('backup sem anexos: os anexos que já estavam no navegador ficam e continuam ligados ao livro', 'anexos (' not in pergunta and 'anexo (' not in pergunta and len(pg.evaluate(IDB)) == 4 and len(pg.evaluate(ARQS)) == 3 and pg.evaluate(CAPA_GV) == {'ini': JPEG, 'w': 360, 'h': 540}, (pergunta[-90:], len(pg.evaluate(IDB))))
    # adulterado: anexos ilegíveis, capa que não é imagem, e um livro apontando para um anexo que não veio
    ruim = json.loads(json.dumps(bk)); cp = liv['cp']; a_ok = liv['anx'][0][0]
    ruim['anexos'] = [a for a in ruim['anexos'] if a['k'] == a_ok] + [
        {'k': cp, 'tipo': 'capa', 'nome': 'x.html', 'dados': 'data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg=='},
        {'k': '../../etc', 'tipo': 'arquivo', 'nome': 'x', 'dados': 'data:text/plain;base64,eA=='}, {'k': 'abcdef123456', 'tipo': 'arquivo', 'nome': 'sem dados'}, 'lixo', None,
        {'k': 'zzzzzz999999', 'tipo': 'arquivo', 'nome': 'solto.txt', 'tam': 1, 'dados': 'data:text/plain;base64,eA=='}]
    rl = next(x for x in ruim['livros'] if x['t'] == 'Quando Nietzsche Chorou'); rl['anx'] = rl['anx'] + [['inexistente1', 'fantasma.txt', 10, 20766, 'text/plain'], 'lixo', ['!!', 'x', 1, 1, '']]; rl['com'] = 'y' * 9000
    json.dump(ruim, open(f'{TMP}/anotacoes-ruim.json', 'w', encoding='utf-8'), ensure_ascii=False)
    fechar(); pg.click('#b-dados'); pg.wait_for_timeout(400); pg.set_input_files('#arq', f'{TMP}/anotacoes-ruim.json'); pg.wait_for_timeout(800); pergunta = pg.inner_text('#dlg .dlg-msg')
    pg.click('#dlg footer .pri'); pg.wait_for_timeout(1500); fechar()
    abrir('Quando Nietzsche Chorou', 'Quando Nietzsche Chorou'); banco = pg.evaluate(IDB); g = guardado('Quando Nietzsche Chorou'); gv = pg.evaluate(CAPA_GV)
    ok('backup adulterado: só entra o anexo íntegro e usado (o solto é descartado)', '2 anexos' in pergunta and [(x['k'], x['nome']) for x in banco] == [(a_ok, 'resenha.txt')], (pergunta[-110:], banco))
    ok('o livro fica só com o que existe: um arquivo, sem a capa falsa, comentário cortado no limite', [a['nome'] for a in pg.evaluate(ARQS)] == ['resenha.txt'] and len(g.get('anx', [])) == 1 and 'cp' not in g and len(g.get('com', '')) == 5000 and gv and gv['ini'].startswith('https://covers.openlib'), (g.get('anx'), g.get('cp'), len(g.get('com', '')), gv))
    pg.context.close()

    print('EM OUTRO NAVEGADOR')
    pg = nova_pagina(b)
    pg.goto(PAINEL_LIMPO); pg.wait_for_timeout(1200); pg.click('#aviso .pri'); pg.wait_for_timeout(200)
    # antes de o painel usar o banco, outra página do mesmo endereço criou um banco com o mesmo nome, sem a tabela dos anexos
    sem = pg.evaluate("() => new Promise(res => { const p = indexedDB.open('biblioteca-lucas'); p.onsuccess = () => { const v = [p.result.version, [...p.result.objectStoreNames]]; p.result.close(); res(v); }; })")
    pg.click('#b-dados'); pg.wait_for_timeout(400); pg.set_input_files('#arq', f'{TMP}/anotacoes-backup.json'); pg.wait_for_timeout(800)
    pg.click('#dlg footer .pri'); pg.wait_for_timeout(1500); fechar()
    abrir('Quando Nietzsche Chorou', 'Quando Nietzsche Chorou')
    ok('um banco com o mesmo nome e sem a tabela (criado por outra página) não atrapalha: o painel cria a tabela', sem == [1, []] and isinstance(pg.evaluate(IDB), list), (sem, pg.evaluate(IDB)))
    ok('o backup importado num navegador que nunca viu o painel traz as anotações', pg.input_value('#nt-com') == C2 and pg.is_checked('#nt-an') and len(pg.evaluate(ARQS)) == 3 and pg.evaluate(CAPA_GV) == {'ini': JPEG, 'w': 360, 'h': 540} and len(pg.evaluate(IDB)) == 4, (pg.evaluate(ARQS), pg.evaluate(CAPA_GV)))
    pg.wait_for_timeout(500); pg.reload(); pg.wait_for_timeout(1800); pg.fill('#p-tab-geral input[type=search]', 'Quando Nietzsche Chorou'); pg.wait_for_timeout(600)
    ok('e elas ficam gravadas nele', pg.evaluate(CAPA_TB) == JPEG and pg.evaluate(ABAS).get('notas') == 1, (pg.evaluate(CAPA_TB), pg.evaluate(ABAS)))
    pg.screenshot(path=f'{TMP}/shots/anotacoes.png')
    pg.context.close()

    print('PRÉ-VISUALIZAÇÃO (armazenamento bloqueado)')
    (TMP / 'wrap-notas.html').write_text('<!doctype html><html><body style="margin:0"><iframe id="f" sandbox="allow-scripts" src="' + PAINEL_LIMPO + '" style="width:100vw;height:100vh;border:0;display:block"></iframe></body></html>', encoding='utf-8')
    pg = nova_pagina(b)
    pg.goto((TMP / 'wrap-notas.html').as_uri()); pg.wait_for_timeout(1500); fr = pg.frames[1]
    fr.click('#aviso .pri'); pg.wait_for_timeout(200)
    fr.fill('#p-tab-geral input[type=search]', 'Quando Nietzsche Chorou'); pg.wait_for_timeout(600); fr.click('#p-tab-geral tbody tr[data-id]'); pg.wait_for_timeout(700)
    ok('a ficha avisa que as anotações valem só até fechar a página', fr.inner_text('#nt-n') == 'Pré-visualização: o que você anotar aqui vale só até fechar a página.', fr.inner_text('#nt-n'))
    fr.fill('#nt-com', 'Comentário na pré-visualização.'); pg.wait_for_timeout(1200)
    fr.set_input_files('#nt-f-arq', str(TMP / 'resenha.txt')); pg.wait_for_timeout(900); fr.set_input_files('#nt-f-capa', str(TMP / 'capa.png')); pg.wait_for_timeout(1200)
    ok('comentário, arquivo e capa funcionam em memória', fr.inner_text('#nt-st') in ('Comentário salvo', '') and [a['nome'] for a in fr.evaluate(ARQS)] == ['resenha.txt'] and fr.evaluate(CAPA_GV) == {'ini': JPEG, 'w': 360, 'h': 540} and fr.evaluate(ABAS).get('notas') == 1, (fr.evaluate(ARQS), fr.evaluate(CAPA_GV)))
    fr.click('#nt-arqs [data-nt=abrir]'); pg.wait_for_timeout(500)
    ok('o arquivo abre na tela', fr.inner_text('#dlg .anexo-txt') == RESENHA)
    fr.click('#dlg footer .btn >> nth=0'); pg.wait_for_timeout(400)
    ok('baixar avisa que a pré-visualização bloqueia downloads (em vez de falhar calado)', fr.evaluate(TOAST).startswith('Esta pré-visualização bloqueia downloads.'), fr.evaluate(TOAST))
    b.close()
print('FALHAS:', falhas); print('ERROS:', len(errs) + len(falhas)); [print('  ', x[:300]) for x in errs[:10]]
