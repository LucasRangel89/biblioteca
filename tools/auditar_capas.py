#!/usr/bin/env python3
"""Olha o que já se sabe das capas e monta a fila de revisão: catalogo/capas-revisao.md.

    python tools/auditar_capas.py             # refaz o relatório (não consulta a internet, não mexe no capas.tsv)
    python tools/auditar_capas.py --resumo    # só mostra o resumo na tela; não grava nada
    python tools/auditar_capas.py --conferir  # confere se o relatório guardado está em dia (para os testes e o robô)
    python tools/auditar_capas.py --rede 40   # pede 40 das imagens e diz quais não abrem (não grava nada)
    python tools/capas.py --auditar           # o mesmo caminho, para quem já usa o script das capas

De onde vêm os números: os mesmos do painel. O catálogo é lido por parse_catalog.parse e o cruzamento com
catalogo/capas.tsv é feito por capas.para_o_painel — a função que gera src/capas.json. Assim a auditoria não inventa
uma contagem própria: se o painel mostra 1.564 capas, é isso que aparece aqui.

O relatório tem duas partes:
  · o retrato — quantos livros têm capa, por parte da biblioteca, por eixo, por tipo e por origem;
  · a fila de revisão — os livros que merecem um olhar, com o motivo e o que fazer, um por linha.

O que entra na fila (tudo conferido sem internet):
  capa que o painel não mostra    endereço que não é número da Open Library nem https limpo
  capa repetida                   a mesma imagem em dois ou mais livros (em geral volumes de uma série)
  pode ser outra edição           capa da obra na Open Library: pode ser de uma edição em outra língua
  casamento duvidoso              tem capa, mas hoje a busca nem procuraria este livro (sem autor certo, adaptação…)
  autoria a conferir              autor vazio, "Vários autores" ou com uma anotação entre parênteses
  título a conferir               título cortado, sem título fora dos parênteses, ou marcado #verificar no catálogo
  linha fora do catálogo          linha do capas.tsv cujo livro não existe mais (só as postas à mão ficam no arquivo)

Com --rede, também: imagem que não abre (resposta que não é imagem, ou "não encontrada"). Essa parte depende do dia
e da rede, por isso vai para a tela e nunca para o arquivo — o relatório guardado é sempre o mesmo para o mesmo catálogo.
"""
import collections, pathlib, re, sys, time

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import capas as C                                                  # noqa: E402
from parse_catalog import SRC as CATALOGO, parse                    # noqa: E402
from eixos import eixo_estante                                      # noqa: E402

RELATORIO = C.RAIZ / 'catalogo' / 'capas-revisao.md'
DIGITAL = 17
PARTES = {0: 'Estante física', DIGITAL: 'Biblioteca virtual'}         # as seções 1 a 16 são as recomendações, por eixo
TIPOS = [('HQ', 'Quadrinhos e mangás'), ('poesia', 'Poesia'), ('antologia', 'Antologias e coletâneas'),
         ('F', 'Ficção'), ('NF', 'Não ficção')]
ROTULO = {                                                          # o que cada origem quer dizer, em português
    'edicao': 'Open Library: capa da edição com o nosso título',
    'obra': 'Open Library: capa da obra (pode ser de outra edição)',
    'apple': 'Apple Books: capa do livro digital no Brasil',
    'google': 'Google Books: capa da edição em português',
    'manual': 'Escolhida à mão',
    'nao-achei': 'Procurada só na Open Library, sem resultado',
    'nao-achei-2': 'Procurada na Open Library e na Apple, sem resultado',
    'nao-achei-3': 'Procurada nas três fontes, sem resultado',
    'sem-autor': 'Não procurada: sem autor certo',
    '': 'Ainda não procurada',
}
# a fila, na ordem em que aparece: código, título do grupo, o que fazer
MOTIVOS = [
    ('imagem-nao-abre', 'A imagem não abre', 'Conferir o endereço; se a capa sumiu da fonte, apagar a linha para a busca tentar de novo.'),
    ('capa-invalida', 'Capa que o painel não consegue mostrar', 'Trocar por um número da Open Library ou um endereço https de imagem.'),
    ('capa-repetida', 'A mesma capa em mais de um livro', 'Escolher a capa de cada volume; `python tools/capas.py --arrumar` tira as repetidas dos volumes com subtítulo.'),
    ('outra-edicao', 'Pode ser capa de outra edição', 'Procurar a edição brasileira; se achar, pôr o endereço e escrever `manual` na origem.'),
    ('casamento-duvidoso', 'Tem capa, mas o casamento é duvidoso', 'Conferir título e autor na fonte; sem autor certo, corrigir o catálogo antes de confiar na capa.'),
    ('autor', 'Autoria a conferir', 'Corrigir o autor no Catálogo Mestre; sem autor certo a busca não procura.'),
    ('titulo', 'Título a conferir', 'Conferir o título no Catálogo Mestre (nome cortado, volume sem número ou #verificar).'),
]


def n(x):
    """Número escrito como se escreve no Brasil: 2614 → 2.614."""
    return f'{int(x):,}'.replace(',', '.')


def pct(parte, todo):
    return f'{round(100 * parte / todo)}%' if todo else '—'


def secoes(md):
    """{número: nome} das seções do Catálogo Mestre (`## 3. Clássicos universais…`)."""
    return {int(m.group(1)): m.group(2).strip() for m in re.finditer(r'^##\s+(\d+)\.\s+(.*)$', md, flags=re.M)}


def parte_de(b):
    """A parte da biblioteca a que o livro pertence: estante, biblioteca virtual ou recomendações (por eixo)."""
    return PARTES.get(b['sec'], 'Recomendações')


def tipo_de(b):
    for tag, nome in TIPOS:
        if tag in b['tags']:
            return nome
    return 'Sem tipo no catálogo'


def eixo_de(b):
    if b['sec'] == DIGITAL:
        return b['sub'] if 1 <= b['sub'] <= 16 else eixo_estante(b)
    return b['sec'] if b['sec'] else eixo_estante(b)


def titulo_duvidoso(b):
    """O título pede conferência? (o que dá para saber sem abrir o livro: nome cortado, nada fora dos parênteses,
    volume sem número, ou a marca #verificar que o próprio catálogo já põe)."""
    t = b['t'].strip()
    if 'verificar' in b['tags']:
        return 'marcado #verificar no catálogo'
    if not C.chave(C.sem_parenteses(t)):
        return 'não sobra título fora dos parênteses'
    if t.endswith(('...', '…')) or '...' in t:
        return 'título parece cortado'
    if re.search(r'\b(?:vol|v|tomo|livro|n)\.?\s*$', t, flags=re.I):
        return 'termina em "volume" sem o número'
    return ''


def autor_duvidoso(autor):
    a = (autor or '').strip()
    if not a or C.chave(a) in C.SEM_AUTOR:
        return 'sem autor certo'
    if '(' in a:
        return 'autor com uma anotação entre parênteses'
    return ''


def auditar(livros, capas, nomes=None, painel=None):
    """O retrato e a fila, sem internet. `livros` é a saída de parse(); `capas`, a de capas.ler_capas().
    Devolve um dict com as contagens, as linhas (uma por livro, com os problemas de cada uma) e as linhas do arquivo
    que não são mais do catálogo. `painel` (lista) só entra para conferir o que o painel mostra: por padrão é calculado
    com capas.para_o_painel, a mesma função que gera src/capas.json."""
    nomes = {} if nomes is None else nomes
    painel = C.para_o_painel(livros, capas) if painel is None else painel
    assert len(painel) == len(livros), 'uma posição por livro: o relatório e o painel têm de falar do mesmo catálogo'
    por_capa = collections.defaultdict(list)
    for i, b in enumerate(livros):
        r = capas.get((C.chave(b['t']), C.chave(b['a']))) or {}
        if r.get('capa'):
            por_capa[r['capa']].append(i)
    linhas = []
    for i, b in enumerate(livros):
        k = (C.chave(b['t']), C.chave(b['a']))
        r = capas.get(k) or {}
        capa, origem = r.get('capa', ''), r.get('origem', '')
        probs = []
        if capa and not painel[i]:
            probs.append(('capa-invalida', f'o endereço guardado não serve para o painel: {capa}'))
        if capa and len(por_capa[capa]) > 1:
            outros = [livros[j]['t'] for j in por_capa[capa] if j != i]
            probs.append(('capa-repetida', 'a mesma capa está em: ' + '; '.join(outros[:3]) + ('…' if len(outros) > 3 else '')))
        if origem == 'obra':
            probs.append(('outra-edicao', 'capa da obra na Open Library: pode ser de uma edição em outra língua'))
        if capa and origem not in C.SEM_CAPA and origem != 'manual' and C.consulta_de(b['t'], b['a']) is None:
            probs.append(('casamento-duvidoso', 'hoje a busca não procuraria este livro (sem autor certo ou adaptação em quadrinhos)'))
        ma = autor_duvidoso(b['a'])
        if ma:
            probs.append(('autor', ma))
        mt = titulo_duvidoso(b)
        if mt:
            probs.append(('titulo', mt))
        linhas.append({'i': i, 't': b['t'], 'a': b['a'], 'sec': b['sec'], 'eixo': eixo_de(b),
                       'parte': parte_de(b), 'tipo': tipo_de(b), 'capa': capa, 'origem': origem,
                       'tem': bool(painel[i]), 'linha': k in capas, 'problemas': probs})
    chaves = {(C.chave(b['t']), C.chave(b['a'])) for b in livros}
    orfas = [r for k, r in capas.items() if k not in chaves]
    return {'livros': len(livros), 'com_capa': sum(1 for x in linhas if x['tem']), 'linhas': linhas, 'orfas': orfas,
            'sem_linha': [x for x in linhas if not x['linha']], 'repetidas': {c: ix for c, ix in por_capa.items() if len(ix) > 1},
            'rede': None}


def conferir_imagens(aud, quantas=40, abrir=None, pausa=0.3):
    """Pede `quantas` das capas guardadas (espalhadas pelo arquivo, como a amostra do --testar) no mesmo endereço que
    o painel usa e anota na fila as que não abriram. Devolve (quantas abriram, quantas foram pedidas)."""
    abrir = C.abrir_imagem if abrir is None else abrir
    com_capa = [x for x in aud['linhas'] if x['tem']]
    quantas = max(0, min(quantas, len(com_capa)))
    amostra = [com_capa[i * len(com_capa) // quantas] for i in range(quantas)]
    ruins = []
    for x in amostra:
        url = C.endereco(x['capa']) + ('?default=false' if x['capa'].isdigit() else '')
        codigo, tipo, comeco = abrir(url)
        if not (codigo == 200 and comeco.startswith(C.IMAGEM) and len(comeco) >= 1000):
            detalhe = f'resposta {codigo or "nenhuma"} {tipo}'.strip() if codigo != 200 else f'{tipo}, {len(comeco)} bytes: não parece uma imagem'
            x['problemas'].append(('imagem-nao-abre', detalhe))
            ruins.append((x['t'], url, detalhe))
        if pausa:
            time.sleep(pausa)
    aud['rede'] = {'pedidas': len(amostra), 'abriram': len(amostra) - len(ruins), 'ruins': ruins}
    return len(amostra) - len(ruins), len(amostra)


# ───────── o relatório ─────────

def _tabela(cabecalho, linhas):
    return ['| ' + ' | '.join(cabecalho) + ' |', '|' + '|'.join('---' for _ in cabecalho) + '|'] + ['| ' + ' | '.join(str(c) for c in l) + ' |' for l in linhas]


def _celula(s):
    """Texto que vai numa célula da tabela: sem tabulação, sem quebra de linha e sem a barra que separa as colunas."""
    return ' '.join(str(s or '').split()).replace('|', '\\|') or '—'


def _grupo(linhas, chave):
    """{valor: [linhas]} na ordem em que os valores aparecem."""
    out = collections.OrderedDict()
    for x in linhas:
        out.setdefault(chave(x), []).append(x)
    return out


def resumo(aud):
    """As duas ou três linhas que resumem a auditoria (vão para a tela e para o começo do relatório)."""
    todo, com = aud['livros'], aud['com_capa']
    fila = sum(1 for x in aud['linhas'] if x['problemas'])
    sem = [x for x in aud['linhas'] if not x['tem']]
    return [f'{n(todo)} livros no catálogo · {n(com)} com capa ({pct(com, todo)}) · {n(len(sem))} sem capa',
            f'{n(fila)} livros na fila de revisão · {n(len(aud["sem_linha"]))} ainda sem linha no capas.tsv · {n(len(aud["orfas"]))} linhas de livros que saíram do catálogo']


def relatorio(aud, nomes=None):
    """O texto de catalogo/capas-revisao.md. Sempre o mesmo para o mesmo catálogo e o mesmo capas.tsv (sem data nem
    hora): assim dá para conferir se está em dia e ver no diff o que mudou de uma execução para outra."""
    nomes = {} if nomes is None else nomes
    L, todo, com = [], aud['livros'], aud['com_capa']
    L += ['# Capas: auditoria e fila de revisão', '',
          'Gerado por `python tools/auditar_capas.py` (ou `python tools/capas.py --auditar`). Não edite à mão:',
          'depois de mexer em `catalogo/capas.tsv` ou no catálogo, rode o script de novo.', '',
          'Os números são os do painel: o cruzamento do catálogo com o `capas.tsv` é o mesmo que gera `src/capas.json`.',
          'Nada aqui consulta a internet. Para saber se as imagens ainda abrem: `python tools/auditar_capas.py --rede 40`.', '',
          '## Resumo', '']
    L += ['- ' + s for s in resumo(aud)]
    L += ['', '## De onde vêm as capas', '']
    origens = _grupo(aud['linhas'], lambda x: x['origem'])
    L += _tabela(['Origem', 'Livros', 'O que significa'],
                 [[f'`{o}`' if o else '(sem linha)', n(len(xs)), ROTULO.get(o, o)] for o, xs in sorted(origens.items(), key=lambda kv: -len(kv[1]))])
    L += ['', '## Por parte da biblioteca', '']
    linhas = []
    for parte, xs in _grupo(aud['linhas'], lambda x: x['parte']).items():
        c = sum(1 for x in xs if x['tem'])
        linhas.append([parte, n(len(xs)), n(c), n(len(xs) - c), pct(c, len(xs))])
    L += _tabela(['Parte', 'Livros', 'Com capa', 'Sem capa', 'Com capa (%)'], linhas)
    L += ['', '## Por eixo temático', '', 'Da pior para a melhor cobertura: onde vale a pena procurar primeiro.', '']
    por_eixo = [(e, xs) for e, xs in _grupo(aud['linhas'], lambda x: x['eixo']).items()]
    por_eixo.sort(key=lambda kv: (sum(1 for x in kv[1] if x['tem']) / len(kv[1]), -len(kv[1]), kv[0]))
    L += _tabela(['Eixo', 'Livros', 'Com capa', 'Sem capa', 'Com capa (%)'],
                 [[f'{e}. {nomes.get(e, "Sem eixo")}', n(len(xs)), n(sum(1 for x in xs if x['tem'])),
                   n(sum(1 for x in xs if not x['tem'])), pct(sum(1 for x in xs if x['tem']), len(xs))] for e, xs in por_eixo])
    L += ['', '## Por tipo de livro', '']
    L += _tabela(['Tipo', 'Livros', 'Com capa', 'Sem capa', 'Com capa (%)'],
                 [[t, n(len(xs)), n(sum(1 for x in xs if x['tem'])), n(sum(1 for x in xs if not x['tem'])),
                   pct(sum(1 for x in xs if x['tem']), len(xs))] for t, xs in _grupo(aud['linhas'], lambda x: x['tipo']).items()])
    fila = [x for x in aud['linhas'] if x['problemas']]
    L += ['', f'## Fila de revisão ({n(len(fila))} livros)', '',
          'Um livro pode aparecer em mais de um grupo. A ordem dos grupos é a da urgência: primeiro o que está',
          'quebrado, depois o que pode estar errado, por último o que é pendência do catálogo.', '']
    if not fila:
        L += ['Nada a revisar: nenhuma capa repetida, inválida ou duvidosa.', '']
    for codigo, titulo, fazer in MOTIVOS:
        xs = [x for x in fila if any(p[0] == codigo for p in x['problemas'])]
        if not xs:
            continue
        L += [f'### {titulo} ({n(len(xs))})', '', f'**O que fazer:** {fazer}', '']
        L += _tabela(['Livro', 'Autor', 'Onde', 'Capa', 'Por que está aqui'],
                     [[_celula(x['t']), _celula(x['a']), _celula(f'{x["parte"]} · eixo {x["eixo"]}'),
                       _celula(x['capa'] or '(sem capa)'), _celula(next(p[1] for p in x['problemas'] if p[0] == codigo))] for x in xs])
        L += ['']
    sem = [x for x in aud['linhas'] if not x['tem']]
    L += [f'## Sem capa: onde estão ({n(len(sem))} livros)', '',
          'Não é erro: é o que ainda falta. Quem já passou pelas fontes e não foi achado precisa de outra fonte ou de',
          'uma escolha à mão; quem está sem autor certo precisa de correção no Catálogo Mestre antes de qualquer busca.', '']
    L += _tabela(['Situação', 'Livros', 'O que falta'],
                 [[ROTULO.get(o, o or '(sem linha)'), n(len(xs)),
                   'corrigir o autor no catálogo' if o == 'sem-autor' else 'outra fonte, ou escolher à mão' if o.startswith('nao-achei') else 'rodar a busca']
                  for o, xs in sorted(_grupo(sem, lambda x: x['origem']).items(), key=lambda kv: -len(kv[1]))])
    sem_autor = [x for x in sem if x['origem'] == 'sem-autor']
    if sem_autor:
        L += ['', f'### Sem autor certo ({n(len(sem_autor))})', '',
               'Estes dependem do catálogo, não da busca: com o autor certo, a próxima execução já procura a capa.', '']
        L += _tabela(['Livro', 'Autor no catálogo', 'Onde'],
                     [[_celula(x['t']), _celula(x['a']), _celula(f'{x["parte"]} · eixo {x["eixo"]}')] for x in sem_autor])
    if aud['sem_linha']:
        L += ['', f'## Ainda sem linha no capas.tsv ({n(len(aud["sem_linha"]))})', '',
               'Livros novos no catálogo: a próxima busca de capas olha para eles.', '']
        L += _tabela(['Livro', 'Autor', 'Onde'], [[_celula(x['t']), _celula(x['a']), _celula(x['parte'])] for x in aud['sem_linha'][:50]])
        if len(aud['sem_linha']) > 50:
            L += ['', f'… e mais {n(len(aud["sem_linha"]) - 50)}.']
    if aud['orfas']:
        L += ['', f'## Linhas de livros que saíram do catálogo ({n(len(aud["orfas"]))})', '',
               'Só as postas à mão continuam no arquivo (para não perder a escolha). As outras saem na próxima gravação.', '']
        L += _tabela(['Livro', 'Autor', 'Origem'], [[_celula(r['titulo']), _celula(r['autor']), _celula(r['origem'])] for r in aud['orfas']])
    L += ['', '## Como corrigir uma capa', '',
          '1. Abra `catalogo/capas.tsv` e ache a linha do livro (o arquivo está na ordem do catálogo).',
          '2. Ponha o número da capa na Open Library ou o endereço `https://…` da imagem.',
          '3. Escreva `manual` na coluna `origem`: assim a busca nunca troca a sua escolha.',
          '4. Rode `python tools/atualizar.py` para o painel receber a mudança, e `python tools/auditar_capas.py` para refazer este relatório.',
          '', 'Para ver o que cada fonte devolveria antes de escolher:',
          '`python tools/capas.py --candidatos "Título" --autor "Nome"` (ou `--isbn 978…`, com o número da edição na mão).', '']
    return '\n'.join(L)


def main(argv):
    for saida in (sys.stdout, sys.stderr):
        try: saida.reconfigure(encoding='utf-8', errors='replace')
        except Exception: pass
    desconhecidos = [a for a in argv if a not in ('--resumo', '--conferir', '--rede') and not a.isdigit()]
    if desconhecidos:
        sys.exit(__doc__)
    md = pathlib.Path(CATALOGO).read_text(encoding='utf-8')
    nomes, livros = secoes(md), parse(md)
    aud = auditar(livros, C.ler_capas(), nomes)
    for s in resumo(aud):
        print(s)
    codigo = 0
    if '--rede' in argv:
        i = argv.index('--rede')
        quantas = int(argv[i + 1]) if i + 1 < len(argv) and argv[i + 1].isdigit() else 40
        boas, pedidas = conferir_imagens(aud, quantas)
        print(f'Imagens conferidas: {boas} de {pedidas} abriram' + (' (nada a conferir)' if not pedidas else ''))
        for t, url, detalhe in aud['rede']['ruins'][:20]:
            print(f'   não abriu: {t} — {detalhe} · {url}')
        if pedidas and boas < 0.9 * pedidas:
            codigo = 1
    if '--rede' in argv or '--resumo' in argv:
        return codigo
    texto = relatorio(aud, nomes)
    if '--conferir' in argv:
        atual = RELATORIO.read_text(encoding='utf-8') if RELATORIO.exists() else ''
        if atual != texto:
            print(f'{RELATORIO.name} está desatualizado: rode python tools/auditar_capas.py')
            return 1
        print(f'{RELATORIO.name} está em dia.')
        return 0
    with open(RELATORIO, 'w', encoding='utf-8', newline='\n') as f:
        f.write(texto)
    nome = RELATORIO.relative_to(C.RAIZ) if RELATORIO.is_relative_to(C.RAIZ) else RELATORIO
    print(f'Relatório gravado: {nome} ({n(len(texto))} caracteres)')
    return codigo


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
