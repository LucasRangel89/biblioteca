"""A auditoria das capas (tools/auditar_capas.py), sem internet e sem navegador.

O que se confere aqui:
  · os números saem do mesmo cruzamento que gera src/capas.json — a auditoria não inventa uma contagem própria;
  · cada tipo de problema da fila: capa que o painel não mostra, capa repetida, capa da obra (pode ser outra edição),
    capa cujo casamento hoje não se faria, autoria e título a conferir, linha que ainda falta e linha órfã;
  · o que não é problema não entra na fila (capa certa, capa posta à mão, livro só sem capa);
  · a conferência das imagens (--rede): amostra espalhada, só de quem tem capa, e o que não abre vira item da fila;
  · o relatório é sempre o mesmo para o mesmo catálogo (sem data nem hora), não fala da rede e escapa a barra das tabelas;
  · o comando: --resumo não grava, --conferir acusa relatório desatualizado, --auditar do capas.py é o mesmo caminho;
  · no repositório: o relatório guardado está em dia e fala dos mesmos livros que o painel.
"""
import contextlib, io, pathlib, sys, tempfile

QA = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(QA.parent))
import auditar_capas as A
import capas as C
import build_catalog as bc
from parse_catalog import parse

erros = []


def confere(cond, msg, extra=''):
    print(('ok    ' if cond else 'FALHOU'), msg + (f' — {extra}' if extra != '' and not cond else ''))
    if not cond: erros.append(msg)


def roda(*argv):
    """Roda o comando com a tela guardada: (código, o que ele disse)."""
    tela = io.StringIO()
    with contextlib.redirect_stdout(tela), contextlib.redirect_stderr(tela):
        try: codigo = A.main(list(argv))
        except SystemExit as e: codigo = e.code
    return codigo, tela.getvalue()


JPEG = b'\xff\xd8\xff\xe0' + b'\x00' * 3000
EM_BRANCO = b'GIF89a' + b'\x00' * 37

# ───────── 1 ▸ um catálogo de mentira, com um problema de cada tipo ─────────
print('O QUE ENTRA NA FILA')


def livro(t, a='Autor Certo', tags=('F',), sec=2, sub=0):
    return {'t': t, 'a': a, 'tags': list(tags), 'sec': sec, 'sub': sub}


livros = [livro('Livro Certo'), livro('Volume Um'), livro('Volume Dois'), livro('Obra Estrangeira'),
          livro('Capa Torta'), livro('Casamento Duvidoso', 'Vários autores'), livro('Escolhida à Mão', 'Vários autores'),
          livro('Sem Autor', ''), livro('Autor com Nota', 'Fulano (conforme a prateleira)'),
          livro('Nome Cortado...'), livro('A Verificar', tags=('F', 'verificar')), livro('(só entre parênteses)'),
          livro('Coleção vol.'), livro('Sem Capa Ainda'), livro('Livro Novo'), livro('HQ Sem Capa', tags=('HQ',), sec=17, sub=7)]
k = lambda b: (C.chave(b['t']), C.chave(b['a']))
capas = {}


def poe(b, capa, origem):
    capas[k(b)] = {'titulo': b['t'], 'autor': b['a'], 'capa': capa, 'origem': origem}


poe(livros[0], '1001', 'edicao')
poe(livros[1], '2002', 'edicao')
poe(livros[2], '2002', 'edicao')                     # a mesma capa em dois volumes
poe(livros[3], '3003', 'obra')
poe(livros[4], 'http://sem-seguranca.org/c.jpg', 'edicao')
poe(livros[5], '4004', 'edicao')                     # tem capa, mas hoje não se procuraria: "Vários autores"
poe(livros[6], 'https://exemplo.org/capa.jpg', 'manual')
poe(livros[7], '', 'sem-autor')
poe(livros[8], '5005', 'apple')
poe(livros[13], '', 'nao-achei-2')
for b in livros[9:13]: poe(b, '', 'nao-achei-2')      # os de título duvidoso já foram procurados
capas[('saiu do catalogo', 'alguem')] = {'titulo': 'Saiu do Catálogo', 'autor': 'Alguém', 'capa': 'https://exemplo.org/x.jpg', 'origem': 'manual'}
aud = A.auditar(livros, capas, {2: 'Ficção científica', 7: 'Horror'})
por_titulo = {x['t']: x for x in aud['linhas']}
prob = lambda t: {c for c, _ in por_titulo[t]['problemas']}

confere(aud['livros'] == len(livros) and aud['com_capa'] == sum(1 for c in C.para_o_painel(livros, capas) if c),
        'os totais são os do painel: uma posição por livro, com capa quem o painel mostra', (aud['livros'], aud['com_capa']))
confere(not por_titulo['Livro Certo']['problemas'], 'capa certa, título e autor certos: nada a revisar', por_titulo['Livro Certo']['problemas'])
confere(prob('Volume Um') == prob('Volume Dois') == {'capa-repetida'}, 'a mesma capa em dois livros: os dois entram na fila', (prob('Volume Um'), prob('Volume Dois')))
confere('capa-repetida' in prob('Volume Um') and 'Volume Dois' in dict(por_titulo['Volume Um']['problemas'])['capa-repetida'], 'a repetição diz em que outro livro a capa está')
confere(prob('Obra Estrangeira') == {'outra-edicao'}, 'capa da obra: aviso de que pode ser de outra edição', prob('Obra Estrangeira'))
confere(prob('Capa Torta') == {'capa-invalida'} and not por_titulo['Capa Torta']['tem'], 'endereço que o painel não mostra entra na fila e não conta como capa', prob('Capa Torta'))
confere(prob('Casamento Duvidoso') == {'casamento-duvidoso', 'autor'}, 'capa de livro que hoje não seria procurado: casamento duvidoso', prob('Casamento Duvidoso'))
confere(not prob('Escolhida à Mão') - {'autor'}, 'capa posta à mão não é acusada de casamento duvidoso (quem escolheu foi o dono)', prob('Escolhida à Mão'))
confere(prob('Sem Autor') == {'autor'} and prob('Sem Capa Ainda') == set(), 'livro só sem capa é pendência, não erro da fila', (prob('Sem Autor'), prob('Sem Capa Ainda')))
confere(prob('Autor com Nota') == {'autor'}, 'autor com anotação entre parênteses: conferir', prob('Autor com Nota'))
for t, why in [('Nome Cortado...', 'cortado'), ('A Verificar', 'verificar'), ('(só entre parênteses)', 'parênteses'), ('Coleção vol.', 'número')]:
    confere('titulo' in prob(t) and why in dict(por_titulo[t]['problemas'])['titulo'], f'título a conferir: {t}', por_titulo[t]['problemas'])
confere([x['t'] for x in aud['sem_linha']] == ['Livro Novo', 'HQ Sem Capa'], 'livro do catálogo sem linha no capas.tsv: contado à parte', [x['t'] for x in aud['sem_linha']])
confere([r['titulo'] for r in aud['orfas']] == ['Saiu do Catálogo'], 'linha de livro que saiu do catálogo: apontada', aud['orfas'])
confere(por_titulo['HQ Sem Capa']['tipo'] == 'Quadrinhos e mangás' and por_titulo['HQ Sem Capa']['parte'] == 'Biblioteca virtual' and por_titulo['HQ Sem Capa']['eixo'] == 7,
        'o livro entra no relatório com a parte da biblioteca, o eixo e o tipo certos', por_titulo['HQ Sem Capa'])
confere(por_titulo['Livro Certo']['parte'] == 'Recomendações' and A.parte_de(livro('X', sec=0)) == 'Estante física', 'estante, recomendações e biblioteca virtual são partes distintas')

# ───────── 2 ▸ as imagens (--rede) ─────────
print('A CONFERÊNCIA DAS IMAGENS')


class Imagens:
    def __init__(self, ruins=(), em_branco=()): self.pedidos, self.ruins, self.em_branco = [], set(ruins), set(em_branco)

    def __call__(self, url):
        self.pedidos.append(url)
        if url in self.ruins or any(x in url for x in self.ruins): return 404, '', b''
        if any(x in url for x in self.em_branco): return 200, 'image/gif', EM_BRANCO
        return 200, 'image/jpeg', JPEG


muitos = [livro(f'Livro {i}') for i in range(20)]
caps = {(C.chave(b['t']), C.chave(b['a'])): {'titulo': b['t'], 'autor': b['a'], 'capa': str(1000 + i), 'origem': 'edicao'} for i, b in enumerate(muitos)}
caps[(C.chave(muitos[5]['t']), 'autor certo')]['capa'] = ''
caps[(C.chave(muitos[5]['t']), 'autor certo')]['origem'] = 'nao-achei-2'
aud2 = A.auditar(muitos, caps)
im = Imagens()
boas, pedidas = A.conferir_imagens(aud2, 5, im, 0)
confere((boas, pedidas) == (5, 5) and len(im.pedidos) == 5, 'pede a amostra e conta as que abriram', (boas, pedidas))
confere(all(u.startswith('https://covers.openlibrary.org/b/id/') and u.endswith('-M.jpg?default=false') for u in im.pedidos),
        'pede no mesmo endereço que o painel usa', im.pedidos[:2])
confere([u.split('/b/id/')[1].split('-')[0] for u in im.pedidos] == ['1000', '1003', '1008', '1012', '1016'],
        'a amostra é espalhada e pula quem não tem capa', im.pedidos)
im = Imagens(ruins={'1003'}, em_branco={'1012'})
boas, pedidas = A.conferir_imagens(aud2, 5, im, 0)
fila_rede = {x['t']: dict(x['problemas']).get('imagem-nao-abre', '') for x in aud2['linhas'] if any(c == 'imagem-nao-abre' for c, _ in x['problemas'])}
confere((boas, pedidas) == (3, 5) and set(fila_rede) == {'Livro 3', 'Livro 12'}, 'imagem que não abre (404 ou quadradinho em branco) vira item da fila, com o nome do livro', (boas, fila_rede))
confere('404' in fila_rede['Livro 3'] and 'bytes' in fila_rede['Livro 12'], 'o motivo diz o que veio no lugar da imagem', fila_rede)
confere(aud2['rede']['pedidas'] == 5 and len(aud2['rede']['ruins']) == 2, 'o resultado da rede fica guardado à parte, para a tela', aud2['rede'])
aud3 = A.auditar(muitos, caps)
confere(A.conferir_imagens(aud3, 99, Imagens(), 0) == (19, 19), 'pedir mais do que existe: confere todas as que têm capa, uma vez cada')
confere(A.conferir_imagens(A.auditar([livro('Sem nada')], {}), 10, Imagens(), 0) == (0, 0), 'sem nenhuma capa: nada a pedir')

# ───────── 3 ▸ o relatório ─────────
print('O RELATÓRIO')
texto = A.relatorio(aud, {2: 'Ficção científica', 7: 'Horror'})
confere(texto == A.relatorio(A.auditar(livros, capas), {2: 'Ficção científica', 7: 'Horror'}), 'o mesmo catálogo e o mesmo capas.tsv dão o mesmo relatório (dá para conferir se está em dia)')
confere('16 livros no catálogo' in texto and '7 com capa' in texto, 'o resumo conta os livros e as capas', texto.splitlines()[9:12])
confere('## Por eixo temático' in texto and '2. Ficção científica' in texto and '## Por tipo de livro' in texto and 'Quadrinhos e mangás' in texto, 'o retrato vem por parte da biblioteca, eixo e tipo')
confere('### A mesma capa em mais de um livro (2)' in texto and '### Pode ser capa de outra edição (1)' in texto and '### Autoria a conferir (4)' in texto,
        'cada grupo da fila aparece com a sua contagem', [l for l in texto.splitlines() if l.startswith('### ')])
confere('### Sem autor certo (1)' in texto and '## Ainda sem linha no capas.tsv (2)' in texto and '## Linhas de livros que saíram do catálogo (1)' in texto,
        'as pendências do catálogo também aparecem')
confere('A imagem não abre' not in texto, 'o que depende da rede não entra no arquivo guardado')
confere('python tools/capas.py --arrumar' in texto and 'manual' in texto, 'cada grupo diz o que fazer')
barrado = A.auditar([livro('Título | com barra')], {})
confere('Título \\| com barra' in A.relatorio(barrado), 'a barra que separa as colunas não quebra a tabela')

# ───────── 4 ▸ o comando ─────────
print('O COMANDO')
tmp = pathlib.Path(tempfile.mkdtemp(prefix='biblioteca-auditoria-'))
guardado = A.RELATORIO
A.RELATORIO = tmp / 'capas-revisao.md'
codigo, saida = roda('--resumo')
confere(codigo == 0 and 'livros no catálogo' in saida and not A.RELATORIO.exists(), '--resumo: mostra o retrato e não grava nada', saida)
codigo, saida = roda('--conferir')
confere(codigo == 1 and 'desatualizado' in saida, '--conferir: acusa quando não há relatório em dia', saida)
codigo, saida = roda()
confere(codigo == 0 and A.RELATORIO.exists() and 'Relatório gravado' in saida, 'sem opção: grava o relatório', saida)
antes = A.RELATORIO.read_text(encoding='utf-8')
codigo, saida = roda('--conferir')
confere(codigo == 0 and 'em dia' in saida, '--conferir: passa quando o relatório é o que o script geraria', saida)
A.RELATORIO.write_text(antes + '\nlinha postiça\n', encoding='utf-8')
codigo, _ = roda('--conferir')
confere(codigo == 1, '--conferir: acusa relatório mexido à mão')
A.RELATORIO.write_text(antes, encoding='utf-8')
abrir_real = C.abrir_imagem
C.abrir_imagem = Imagens(ruins={'/b/id/', 'mzstatic'})
codigo, saida = roda('--rede', '4')
confere(codigo == 1 and 'Imagens conferidas: 0 de 4 abriram' in saida and 'não abriu:' in saida, '--rede: diz quantas abriram e termina com erro quando quase nenhuma abre', saida.strip().splitlines()[-5:])
confere(A.RELATORIO.read_text(encoding='utf-8') == antes, '--rede não grava nada: o arquivo guardado não depende do dia')
C.abrir_imagem = Imagens()
codigo, saida = roda('--rede', '4')
confere(codigo == 0 and 'Imagens conferidas: 4 de 4 abriram' in saida, '--rede: passa quando as imagens abrem', saida.strip().splitlines()[-1:])
C.abrir_imagem = abrir_real
codigo, saida = roda('--opcao-que-nao-existe')
confere('--resumo' in str(codigo) and not saida, 'opção desconhecida: mostra a ajuda em vez de fazer alguma coisa', str(codigo)[:60])
tela = io.StringIO()
with contextlib.redirect_stdout(tela):
    codigo = C.main(['--auditar', '--conferir'])
confere(codigo == 0 and 'em dia' in tela.getvalue(), 'python tools/capas.py --auditar é o mesmo caminho', tela.getvalue())
A.RELATORIO = guardado

# ───────── 5 ▸ o que está no repositório ─────────
print('O REPOSITÓRIO')
import json
do_catalogo = parse(bc.SRC.read_text(encoding='utf-8'))
no_painel = json.loads(bc.DEST_CAPAS.read_text(encoding='utf-8'))
real = A.auditar(do_catalogo, C.ler_capas(), A.secoes(bc.SRC.read_text(encoding='utf-8')), no_painel)
confere(real['livros'] == len(no_painel) == len(json.loads(bc.DEST.read_text(encoding='utf-8'))), 'uma linha de auditoria por livro do painel', real['livros'])
confere(real['com_capa'] == sum(1 for c in no_painel if c), 'as capas contadas são as que o painel mostra', (real['com_capa'], sum(1 for c in no_painel if c)))
confere(all(x['tem'] == bool(no_painel[x['i']]) for x in real['linhas']), 'livro a livro, a auditoria e o painel concordam sobre quem tem capa')
codigo, saida = roda('--conferir')
confere(codigo == 0, 'catalogo/capas-revisao.md está em dia (se falhar: python tools/auditar_capas.py)', saida)
confere(A.RELATORIO.read_text(encoding='utf-8').count('| ') > 100 and '## Fila de revisão' in A.RELATORIO.read_text(encoding='utf-8'), 'o relatório guardado tem o retrato e a fila')
print(f'   ({A.n(real["livros"])} livros · {A.n(real["com_capa"])} com capa · {sum(1 for x in real["linhas"] if x["problemas"])} na fila de revisão)')

import shutil
shutil.rmtree(tmp, ignore_errors=True)
print('ERROS:', len(erros))
for e in erros: print('  ', e)
sys.exit(1 if erros else 0)
