"""A sinopse na ficha do livro (Etapa 10, Parte 3).

As sinopses moram em catalogo/sinopses.tsv — uma linha por livro pesquisado: título, autor, sinopse, de onde veio e a
data. O arquivo é também o registro das buscas: linha sem sinopse é pendência (não deu para confirmar do que o livro
trata), com o motivo na coluna "fonte". tools/build_catalog.py leva as sinopses para src/sinopses.json, e tools/build.py
as põe dentro do painel.

Confere que:
  · o arquivo está inteiro: cabeçalho, cinco campos por linha, cada linha achada no catálogo, sem repetição;
  · cada sinopse segue o combinado: duas ou três frases, de 140 a 400 caracteres, com a fonte e a data; as duas amostras
    aprovadas pelo dono (A Metamorfose e O Físico) estão como ele aprovou;
  · pendência não tem sinopse, diz o motivo e aparece na lista de pendências do ROTEIRO.md;
  · os lotes 1 e 2 estão completos: estante, prioridades (#top) e recomendações ainda não adquiridas das seções 1 a 5;
  · o leitor do arquivo avisa do que está errado em vez de deixar passar (livro que não existe, linha repetida, sinopse
    longa, de uma frase só, sem fonte), e acha o livro também pelo nome antigo;
  · src/sinopses.json e o painel pronto estão em dia com o arquivo;
  · na ficha, a sinopse aparece no alto — depois do título e antes dos dados —, com o texto idêntico ao do arquivo;
    livro sem sinopse (e pendência) não mostra nada no lugar, nem espaço vazio;
  · a sinopse vem sempre do catálogo: continua na ficha depois de o livro ser mexido e a página recarregada, e não é
    gravada com os dados do usuário;
  · lê-se bem no tema claro e no escuro (contraste AA), e cabe no celular sem estourar a largura.
"""
from caminhos import PAINEL, PAINEL_LIMPO, RAIZ, TMP
from relogio import fixa
import csv, json, re, sys
from playwright.sync_api import sync_playwright

sys.path.insert(0, str(RAIZ / 'tools'))
import build_catalog as bc

CHAVE = 'biblioteca-lucas:v1'
errs = []; falhas = []
CAT = json.loads((RAIZ / 'src' / 'catalog.json').read_text(encoding='utf-8'))            # [título, autor, "marcadores", seção, eixo, obs, …]
ARQ = RAIZ / 'catalogo' / 'sinopses.tsv'
AMOSTRAS = {      # aprovadas pelo dono em 11/11/2026 ("tamanho e tom estão bons"): o modelo de todas as outras
    'A Metamorfose': 'Gregor Samsa, caixeiro-viajante que sustenta a família, acorda certa manhã transformado num inseto monstruoso. Trancado no quarto, acompanha a mudança dos pais e da irmã, que passam do susto ao incômodo. Uma novela curta sobre trabalho, culpa e o lugar de quem deixa de ser útil.',
    'O Físico': 'Na Inglaterra do século XI, o órfão Rob Cole aprende o ofício com um barbeiro-cirurgião ambulante e descobre que pressente a morte dos doentes. Decidido a ser médico de verdade, atravessa a Europa disfarçado de judeu para estudar na Pérsia com Avicena.',
}
# o que se lê da ficha aberta
FICHA = """() => { const g = document.querySelector('#gaveta'), s = g.querySelector('#gv-sin'), topo = g.querySelector('#gv-topo'), est = g.querySelector('#gv-estado'), p = s.querySelector('.gv-sin-tx'), h = s.querySelector('h4');
  const r = e => { const b = e.getBoundingClientRect(); return { cima: Math.round(b.top), baixo: Math.round(b.bottom), alt: Math.round(b.height) }; };
  return { titulo: g.querySelector('#gv-topo h2').textContent, escondida: s.hidden, vazia: s.innerHTML === '', alt: r(s).alt, cab: h ? h.textContent : '', texto: p ? p.textContent : '', html: p ? p.innerHTML : '',
    rotulada: !!h && s.getAttribute('aria-labelledby') === h.id, ordem: [...topo.parentElement.children].map(e => e.id).filter(Boolean), topo: r(topo), sin: r(s), est: r(est),
    letra: p ? parseFloat(getComputedStyle(p).fontSize) : 0, sobra: g.querySelector('.gv-c').scrollWidth - g.querySelector('.gv-c').clientWidth, fora: document.documentElement.scrollWidth - innerWidth }; }"""
# contraste do texto da sinopse com o fundo que está de fato atrás dele (WCAG)
CONTRASTE = """() => { const lum = c => { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }; return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2]); };
  const cor = s => s.match(/[\\d.]+/g).map(Number);
  const razao = e => { const fg = cor(getComputedStyle(e).color); let bg = [255, 255, 255];
    for (let n = e; n && n.nodeType === 1; n = n.parentElement) { const c = cor(getComputedStyle(n).backgroundColor); if (c.length < 4 || c[3] >= 0.999) { bg = c; break; } }
    const a = lum(fg), b = lum(bg); return Math.round((Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05) * 100) / 100; };
  return { texto: razao(document.querySelector('#gv-sin .gv-sin-tx')), cab: razao(document.querySelector('#gv-sin h4')), tema: document.documentElement.dataset.tema }; }"""


def ok(nome, cond, extra=''):
    print(('  ok   ' if cond else '  FALHA') + ' ' + nome + (' — ' + str(extra) if extra != '' else ''))
    if not cond: falhas.append(nome)


def abre(b, largura=1366, altura=768, tema='light'):
    ctx = b.new_context(viewport={'width': largura, 'height': altura}, locale='pt-BR', timezone_id='America/Sao_Paulo', color_scheme=tema)
    pg = ctx.new_page(); fixa(pg)
    pg.on('console', lambda m: errs.append(f'[{m.type}] {m.text}') if m.type in ('error', 'warning') else None)
    pg.on('pageerror', lambda e: errs.append(f'[pageerror] {e}'))
    pg.goto(PAINEL_LIMPO); pg.wait_for_timeout(1300)
    if pg.is_visible('#aviso .pri'): pg.click('#aviso .pri'); pg.wait_for_timeout(200)
    return pg


def ficha(pg, titulo, visao='geral'):
    """Abre a ficha do livro pela tabela da visão (geral = o acervo; recs = as recomendações) e devolve o que há nela."""
    nav = '#nav' if pg.viewport_size['width'] > 820 else '#nav-m'
    pg.keyboard.press('Escape'); pg.wait_for_timeout(250)
    if not pg.is_visible(f'#p-tab-{visao}'): pg.click(f'{nav} [data-ir={visao}]'); pg.wait_for_timeout(800)
    pg.fill(f'#p-tab-{visao} input[type=search]', titulo); pg.wait_for_timeout(600)
    achou = pg.evaluate("([v, t]) => { const tr = [...document.querySelectorAll(`#p-tab-${v} tbody tr[data-id]`)].find(tr => tr.querySelector('.tt b').textContent.trim() === t); if (tr) tr.click(); return !!tr; }", [visao, titulo])
    if not achou: return None
    pg.wait_for_timeout(700)
    return pg.evaluate(FICHA)


# ───────────── o arquivo (sem navegador) ─────────────
print('A. O arquivo catalogo/sinopses.tsv')
bruto = ARQ.read_text(encoding='utf-8').split('\n')
ok('cabeçalho: titulo, autor, sinopse, fonte, data', bruto[0] == 'titulo\tautor\tsinopse\tfonte\tdata', bruto[0][:80])
ok('termina com quebra de linha e não tem linha em branco no meio', bruto[-1] == '' and all(bruto[:-1]))
ok('cinco campos em toda linha', all(l.count('\t') == 4 for l in bruto[:-1]), [n + 1 for n, l in enumerate(bruto[:-1]) if l.count('\t') != 4][:5])
with open(ARQ, encoding='utf-8', newline='') as f:
    LINHAS = list(csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE))
COM = [r for r in LINHAS if r['sinopse']]; PEND = [r for r in LINHAS if not r['sinopse']]
norm = lambda t, a: (bc._norm(t), bc._norm(a))
POS = {norm(r[0], r[1]): i for i, r in enumerate(CAT)}
ok('título e autor de cada linha são os de uma linha do catálogo, como estão hoje', all(norm(r['titulo'], r['autor']) in POS for r in LINHAS), [r['titulo'] for r in LINHAS if norm(r['titulo'], r['autor']) not in POS][:5])
ok('nenhum livro aparece duas vezes', len({norm(r['titulo'], r['autor']) for r in LINHAS}) == len(LINHAS))
ok('as linhas seguem a ordem do catálogo', [POS.get(norm(r['titulo'], r['autor']), -1) for r in LINHAS] == sorted(POS.get(norm(r['titulo'], r['autor']), -1) for r in LINHAS))
ok('toda linha tem a data da pesquisa (AAAA-MM-DD)', all(re.fullmatch(r'\d{4}-\d{2}-\d{2}', r['data']) for r in LINHAS))

print('B. Cada sinopse, como combinado')
tam = sorted(len(r['sinopse']) for r in COM)
ok(f'de {bc.SINOPSE_MIN} a {bc.SINOPSE_MAX} caracteres', bool(tam) and tam[0] >= bc.SINOPSE_MIN and tam[-1] <= bc.SINOPSE_MAX, f'{len(COM)} sinopses; menor {tam[0]}, mediana {tam[len(tam) // 2]}, maior {tam[-1]}')
ok('duas ou três frases', all(2 <= bc.frases(r['sinopse']) <= 3 for r in COM), [(r['titulo'], bc.frases(r['sinopse'])) for r in COM if not 2 <= bc.frases(r['sinopse']) <= 3][:5])
ok('o contador de frases não se engana com iniciais e abreviaturas', [bc.frases(t) for t in ('Uma. Duas.', 'O robô R. Daneel Olivaw chega. Fim.', 'Rob J. Cole emigra. O Dr. Cole fica. Fim!', '“Uma frase só?” Outra.', 'C.S. Lewis escreve cartas. Fim.', 'Sem ponto final')] == [2, 2, 3, 2, 2, 0])
ok('começa com maiúscula (ou aspas) e termina com ponto', all(re.match(r'[“A-ZÀ-Ý0-9]', r['sinopse']) and re.search(r'[.!?…]”?$', r['sinopse']) for r in COM), [r['titulo'] for r in COM if not (re.match(r'[“A-ZÀ-Ý0-9]', r['sinopse']) and re.search(r'[.!?…]”?$', r['sinopse']))][:5])
ok('sem aspas retas, espaço dobrado nem espaço nas pontas', all('"' not in r['sinopse'] and '  ' not in r['sinopse'] and r['sinopse'] == r['sinopse'].strip() for r in COM))
ok('aspas curvas e parênteses sempre aos pares', all(r['sinopse'].count('“') == r['sinopse'].count('”') and r['sinopse'].count('(') == r['sinopse'].count(')') for r in COM), [r['titulo'] for r in COM if r['sinopse'].count('“') != r['sinopse'].count('”')][:5])
ok('nenhuma sinopse repetida', len({r['sinopse'] for r in COM}) == len(COM))
ok('toda sinopse diz de onde veio: conhecimento geral ou o endereço consultado', all(r['fonte'].startswith('conhecimento geral') or 'https://' in r['fonte'] or 'http://' in r['fonte'] for r in COM), [r['titulo'] for r in COM if not (r['fonte'].startswith('conhecimento geral') or 'http' in r['fonte'])][:5])
ok('os endereços estão inteiros (sem espaço nem reticências)', all(re.fullmatch(r'https?://[^\s…]+', u) for r in LINHAS for u in re.findall(r'https?://\S*', r['fonte'])))
da = {r['titulo']: r['sinopse'] for r in LINHAS}
ok('as duas amostras aprovadas pelo dono estão como ele aprovou', all(da.get(t) == s for t, s in AMOSTRAS.items()), [t for t, s in AMOSTRAS.items() if da.get(t) != s])
roteiro = (RAIZ / 'ROTEIRO.md').read_text(encoding='utf-8')
ok('…e são as mesmas que o ROTEIRO.md mostra', all(' '.join(s.split()) in ' '.join(roteiro.replace('\n> ', ' ').split()) for s in AMOSTRAS.values()))

print('C. Pendências e os lotes 1 e 2')
ok('pendência não tem sinopse e diz o motivo ("pendente: …")', all(r['fonte'].startswith('pendente: ') and len(r['fonte']) > 40 for r in PEND), [r['titulo'] for r in PEND if not r['fonte'].startswith('pendente: ')])
ok('cada pendência está na lista de pendências do ROTEIRO.md', bool(PEND) and all(f'*{r["titulo"]}*' in roteiro for r in PEND), [r['titulo'] for r in PEND if f'*{r["titulo"]}*' not in roteiro])
pesquisados = {POS[norm(r['titulo'], r['autor'])] for r in LINHAS if norm(r['titulo'], r['autor']) in POS}
estante = [i for i, r in enumerate(CAT) if r[3] == 0]; top = [i for i, r in enumerate(CAT) if r[3] != 0 and 'top' in r[2].split()]
ok('lote 1: os 97 livros da estante foram pesquisados', len(estante) == 97 and set(estante) <= pesquisados, [CAT[i][0] for i in estante if i not in pesquisados][:5])
ok('lote 1: as 53 prioridades (#top) que não estão na estante também', len(top) == 53 and set(top) <= pesquisados, [CAT[i][0] for i in top if i not in pesquisados][:5])
ok('a tabela de lotes do ROTEIRO.md dá o lote 1 como feito, com os números de hoje', re.search(r'\| 1 \|[^\n]*\| 150 \| Feito[^\n]*\b%d sinopses\b[^\n]*\b%d pendências\b' % (len([r for r in COM if POS[norm(r['titulo'], r['autor'])] in set(estante) | set(top)]), len(PEND)), roteiro) is not None)

sem_posse = lambda r: not any(t in r[2].split() for t in ('tenho-fisico', 'tenho-digital'))
recs_1_5 = [i for i, r in enumerate(CAT) if 1 <= r[3] <= 5 and sem_posse(r)]
lote2 = [POS[norm(r['titulo'], r['autor'])] for r in LINHAS if r['data'] == '2026-11-12' and norm(r['titulo'], r['autor']) in POS]
ok('lote 2: todas as recomendações ainda não adquiridas das seções 1 a 5 foram pesquisadas', set(recs_1_5) <= pesquisados, [CAT[i][0] for i in recs_1_5 if i not in pesquisados][:5])
ok('…sem repetir as prioridades e a amostra que já estavam antes', len(lote2) == 143 and set(lote2) <= set(recs_1_5) and not (set(lote2) & set(top)), len(lote2))
ok('a tabela de lotes dá o lote 2 como feito, com o número de livros de hoje', re.search(r'\| 2 \|[^\n]*\| %d \| Feito[^\n]*\b%d sinopses\b' % (len(lote2), len(lote2)), roteiro) is not None)
restantes = [i for i, r in enumerate(CAT) if 1 <= r[3] <= 16 and i not in pesquisados]
ok('…e o que ainda falta nas recomendações continua certo na tabela', re.search(r'\| 3 a 5 \|[^\n]*\| %d \| A fazer' % len(restantes), roteiro) is not None, len(restantes))

print('D. O leitor do arquivo (tools/build_catalog.py)')
av = []; dados = bc.build([]); lidas = bc.ler_sinopses(dados, av)
ok('lê o arquivo de hoje sem nenhum aviso', not av, av[:3])
ok('uma entrada por sinopse: [posição no catálogo, texto], em ordem', len(lidas) == len(COM) and lidas == sorted(lidas) and all(CAT[i][0] == r['titulo'] and s == r['sinopse'] for (i, s), r in zip(lidas, COM)))
ok('pendência não vai para o painel', not ({POS[norm(r['titulo'], r['autor'])] for r in PEND} & {i for i, _ in lidas}))
ok('src/sinopses.json está em dia com o arquivo (se falhar: python tools/atualizar.py)', lidas == json.loads(bc.DEST_SINOPSES.read_text(encoding='utf-8')))
mini = [['Livro Novo', 'Autora', 'F d1', 1, 2, ''], ['Outro', '', 'NF', 17, 9, '', None, [['Outro Velho', 'Fulano']]], ['Terceiro', 'Beltrano', 'F', 2, 3, '']]
boa = 'Uma frase que apresenta o livro com calma e sem contar o final da história. Outra frase, que fecha a apresentação dizendo que livro é este e para quem ele serve.'
def ensaio(*linhas):
    (TMP / 'sinopses-ensaio.tsv').write_text('titulo\tautor\tsinopse\tfonte\tdata\n' + ''.join('\t'.join(l) + '\n' for l in linhas), encoding='utf-8')
    avs = []; return bc.ler_sinopses(mini, avs, TMP / 'sinopses-ensaio.tsv'), avs
r, a = ensaio(['Livro Novo', 'Autora', boa, 'conhecimento geral', '2026-11-11'], ['Outro Velho', 'Fulano', boa + ' Mais uma.', 'https://exemplo.org/livro', '2026-11-11'], ['Terceiro', 'Beltrano', '', 'pendente: não achei o livro em lugar nenhum', '2026-11-11'])
ok('acha o livro pelo nome de hoje e pelo nome antigo; a pendência fica de fora, sem aviso', r == [[0, boa], [1, boa + ' Mais uma.']] and not a, (r, a))
r, a = ensaio(['Não Existe', 'Ninguém', boa, 'conhecimento geral', '2026-11-11'], ['Livro Novo', 'Autora', boa, 'conhecimento geral', '2026-11-11'], ['Livro Novo', 'Autora', boa, 'conhecimento geral', '2026-11-11'])
ok('livro que não é do catálogo e linha repetida: avisa de cada um e ignora', r == [[0, boa]] and len(a) == 2 and 'não é uma linha do catálogo' in a[0] and 'mais de uma vez' in a[1], a)
r, a = ensaio(['Livro Novo', 'Autora', 'Curta demais.', 'conhecimento geral', '2026-11-11'], ['Outro', '', boa + ' ' + boa + ' ' + boa, 'conhecimento geral', '2026-11-11'], ['Terceiro', 'Beltrano', boa.replace('. Outra', ', outra'), 'conhecimento geral', '11/11/2026'])
ok('sinopse curta, longa ou de uma frase só, e data fora do padrão: avisa', len(r) == 3 and sum('caracteres' in x for x in a) == 2 and sum('frase(s)' in x for x in a) == 3 and sum('data' in x for x in a) == 1, a)
r, a = ensaio(['Livro Novo', 'Autora', boa, '', '2026-11-11'], ['Outro', '', '', '', '2026-11-11'], ['Terceiro', 'Beltrano', boa.replace('calma', '"calma"'), 'conhecimento geral', '2026-11-11'])
ok('sinopse sem fonte, linha vazia sem o motivo e aspas retas: avisa', len(a) == 3 and 'não diz de onde' in a[0] and 'sem o motivo' in a[1] and 'aspas retas' in a[2], a)
ok('sem o arquivo, nenhuma sinopse (e sem erro)', bc.ler_sinopses(mini, [], TMP / 'nao-existe.tsv') == [])

print('E. O painel pronto')
html = PAINEL.read_text(encoding='utf-8')
m = re.search(r'^const SINOPSES = (\[.*\]);$', html, re.M)
ok('as sinopses estão dentro do painel, iguais às de src/sinopses.json (se falhar: python tools/build.py)', m is not None and json.loads(m.group(1)) == lidas)

# ───────────── a ficha ─────────────
SEM = next(r[0] for i, r in enumerate(CAT) if 1 <= r[3] <= 16 and i not in pesquisados and 'tenho-digital' not in r[2].split() and 'tenho-fisico' not in r[2].split())      # recomendação que ainda não foi pesquisada
SEM_DIG = next(r[0] for i, r in enumerate(CAT) if r[3] == 17 and i not in pesquisados)                                                                                       # livro digital, idem
with sync_playwright() as p:
    b = p.chromium.launch()

    print('F. Na ficha')
    pg = abre(b)
    f = ficha(pg, 'Fundação')
    ok('livro da estante: a ficha traz a seção "Sinopse"', f and not f['escondida'] and f['cab'] == 'Sinopse' and f['rotulada'], f and (f['escondida'], f['cab']))
    ok('…com o texto idêntico ao do arquivo', f and f['texto'] == da['Fundação'], f and f['texto'][:80])
    ok('…no alto: depois do título e dos selos, antes dos dados do livro', f and f['ordem'][:3] == ['gv-topo', 'gv-sin', 'gv-estado'] and f['topo']['baixo'] <= f['sin']['cima'] and f['sin']['baixo'] <= f['est']['cima'], f and (f['ordem'][:4], f['topo'], f['sin'], f['est']))
    ok('…e visível sem rolar a ficha', f and f['sin']['baixo'] < 768, f and f['sin'])
    com_sinopse = f
    f = ficha(pg, 'Ismael', 'recs')
    ok('recomendação que não está na estante: também', f and not f['escondida'] and f['texto'] == da['Ismael'], f and f['texto'][:80])
    ok('aspas, travessões e apóstrofos chegam inteiros, como texto', f and '“Professor procura aluno.' in f['texto'] and '—' in f['texto'] and '<' not in f['html'], f and f['html'][:120])
    for titulo in ('Piranesi', 'Vidas Secas'):
        f = ficha(pg, titulo, 'recs')
        ok(f'lote 2: a recomendação “{titulo}” abre com a sinopse nova', f and not f['escondida'] and f['texto'] == da[titulo], f and f['texto'][:80])
    f = ficha(pg, SEM, 'recs')
    ok(f'livro ainda sem sinopse ("{SEM}"): nada no lugar — nem título, nem espaço', f and f['titulo'] == SEM and f['escondida'] and f['vazia'] and f['alt'] == 0, f and (f['titulo'], f['escondida'], f['alt']))
    ok('…e os dados do livro sobem para junto do título', f and com_sinopse and f['est']['cima'] - f['topo']['baixo'] < com_sinopse['est']['cima'] - com_sinopse['topo']['baixo'] - 60, f and (f['topo'], f['est']))
    f = ficha(pg, SEM_DIG)
    ok(f'livro digital sem sinopse ("{SEM_DIG[:40]}"): idem', f and f['escondida'] and f['vazia'], f and (f['titulo'], f['escondida']))
    f = ficha(pg, PEND[0]['titulo'])
    ok(f'pendência ("{PEND[0]["titulo"]}"): sem sinopse na ficha', f and f['titulo'] == PEND[0]['titulo'] and f['escondida'] and f['vazia'], f and (f['titulo'], f['escondida']))
    f = ficha(pg, '1984')
    ok('abrir outro livro troca a sinopse (não sobra a anterior)', f and f['texto'] == da['1984'], f and f['texto'][:60])

    print('G. A sinopse vem do catálogo, não dos dados guardados')
    pg.fill('#nt-com', 'Reler antes da série.'); pg.wait_for_timeout(1200)
    guardado = pg.evaluate("() => localStorage.getItem('%s') || ''" % CHAVE)
    livro = next((x for x in json.loads(guardado or '{"livros": []}')['livros'] if x.get('t') == '1984'), None)
    ok('ao mexer no livro, ele é gravado no navegador — sem a sinopse', livro is not None and livro.get('com') == 'Reler antes da série.' and not any(k.startswith('_') for k in livro) and da['1984'][:40] not in guardado, livro and sorted(livro)[:12])
    pg.reload(); pg.wait_for_timeout(1300)
    if pg.is_visible('#aviso .pri'): pg.click('#aviso .pri'); pg.wait_for_timeout(200)
    f = ficha(pg, '1984')
    ok('depois de recarregar, o livro mexido continua com a sinopse (e com o comentário)', f and f['texto'] == da['1984'] and pg.input_value('#nt-com') == 'Reler antes da série.', f and f['texto'][:60])
    f = ficha(pg, 'Fundação')
    ok('…e os outros também', f and f['texto'] == da['Fundação'])
    pg.context.close()

    print('H. Leitura: contraste e largura')
    maior = max(COM, key=lambda r: len(r['sinopse']))
    onde = 'geral' if 'tenho-' in CAT[POS[norm(maior['titulo'], maior['autor'])]][2] else 'recs'
    for tema, nome in (('light', 'claro'), ('dark', 'escuro')):
        pg = abre(b, tema=tema)
        f = ficha(pg, 'Fundação'); c = pg.evaluate(CONTRASTE)
        ok(f'tema {nome}: contraste do texto e do título da seção (AA: 4,5)', f and c['tema'] == nome and c['texto'] >= 4.5 and c['cab'] >= 4.5, c)
        pg.context.close()
    pg = abre(b, 390, 780)
    f = ficha(pg, maior['titulo'], onde)
    ok(f'no celular (390 px), a sinopse mais longa ({len(maior["sinopse"])} caracteres) cabe na largura', f and f['texto'] == maior['sinopse'] and f['sobra'] <= 0 and f['fora'] <= 0, f and (f['sobra'], f['fora']))
    ok('…com letra de leitura (15 px ou mais)', f and f['letra'] >= 15, f and f['letra'])
    pg.context.close()
    b.close()

print('FALHAS:', falhas); print('ERROS:', len(errs) + len(falhas)); [print('  ', x[:300]) for x in errs[:10]]
