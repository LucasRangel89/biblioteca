"""A busca de capas (tools/capas.py), sem internet: as respostas da Open Library e da busca do iTunes (Apple Books)
usadas aqui foram montadas no formato das respostas reais (consultadas em 10 e 11/11/2026), só com os campos que o
script lê.

  · que consulta é feita para cada livro, e para quais não se procura;
  · que capa é escolhida entre os resultados (a da edição em português antes da capa da obra);
  · a segunda tentativa, só pelo título, quando o autor está escrito de outro jeito (Tolstói · Толстой);
  · a segunda fonte, a Apple Books: a consulta, o resultado que serve (título e autor conferem; caixa, trilogia e
    resumo não), o endereço da imagem, a espera quando a busca recusa por excesso de consultas;
  · catalogo/capas.tsv: gravar, ler de novo, retomar de onde parou, não mexer no que foi posto à mão;
  · as duas fontes em ordem: livro novo passa pelas duas; quem só tinha passado pela Open Library vai só à Apple;
    a Apple fora do ar não atrapalha a Open Library, e o que faltou fica para a execução seguinte;
  · a mesma capa nunca fica em dois volumes de uma série;
  · a amostra (--testar): conta como capa só o que é mesmo uma imagem, e exige "não encontrada" para capa que não existe;
  · o que vai para o painel (src/capas.json): uma posição por linha do catálogo, em dia com o capas.tsv.
Não precisa de navegador."""
import contextlib, io, json, pathlib, sys, tempfile

QA = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(QA.parent))
import capas as C
import build_catalog as bc
from parse_catalog import parse

erros = []
def confere(cond, msg, extra=''):
    print(('ok    ' if cond else 'FALHOU'), msg + (f' — {extra}' if extra != '' and not cond else ''))
    if not cond: erros.append(msg)


# ───────── respostas gravadas ─────────
def doc(titulo, autor, capa=None, ed=None, alt=None):
    d = {'key': '/works/OL1W', 'title': titulo, 'author_name': [autor]}
    if capa: d['cover_i'] = capa
    if alt: d['author_alternative_name'] = alt
    if ed is not None:
        e = {'title': ed[0]}
        if ed[1]: e['cover_i'] = ed[1]
        if len(ed) > 2 and ed[2]: e['language'] = [ed[2]]
        d['editions'] = {'numFound': 1, 'docs': [e]}
    return d

CAVERNAS = [doc('The Caves of Steel', 'Isaac Asimov', 13790511, ('As Cavernas de Aço', 15138088, 'por'))]
SAPIENS = [doc('קיצור תולדות האנושות', 'Yuval Noah Harari', 8634250, ('Sapiens', 14540965, 'por'))]
FISICO = [doc('O Fisico', 'Noah Gordon', 12369732, ('O Fisico', 12369732))]
ROSA = [doc('Il nome della rosa', 'Umberto Eco', 8598263, ('O Nome da Rosa', 12385395, 'por')),
        doc('O nome da rosa', 'Umberto Eco', None, ('O nome da rosa', None, 'por')),
        doc('Pós-escrito a O nome da rosa', 'Umberto Eco')]
FUNDACAO = [doc("Foundation's Edge", 'Isaac Asimov', 9300695, ('Limites da Fundação', 14656431, 'por')),
            doc('Foundation', 'Isaac Asimov', 14612610, ('Fundação', 15111026, 'por')),
            doc('Box Fundação', 'Isaac Asimov', 15228268, ('Box Fundação', 15228268, 'por'))]
WATCHMEN = [doc('Absolute Watchmen', 'Alan Moore', 1001231, ('Absolute Watchmen', 1001231, 'eng')),
            doc('Watchmen', 'Alan Moore', 7774899, ('Watchmen', 14311997, 'por'))]
GUERRA_E_PAZ = [doc('Guerra e paz', 'Fulano de Tal', 111, ('Guerra e paz', 111, 'por')),
                doc('Война и мир', 'Лев Толстой', 12369940, ('Guerra e Paz', None, 'por'), alt=['Leo Tolstoy', 'Liev Tolstói', 'Tolstoi', 'León Tolstoi'])]

# ───────── 1 ▸ o que se procura ─────────
print('A CONSULTA')
q = lambda t, a: (C.consulta_de(t, a) or {}).get('q')
confere(q('As Cavernas de Aço', 'Isaac Asimov') == 'title:"As Cavernas de Aço" author:asimov', 'título inteiro e sobrenome do autor', q('As Cavernas de Aço', 'Isaac Asimov'))
confere(q('O Feiticeiro de Terramar (Ciclo Terramar, vol. 1)', 'Ursula K. Le Guin') == 'title:"O Feiticeiro de Terramar" author:guin', 'o que está entre parênteses não entra na consulta')
confere(C.consulta_de('As Cavernas de Aço', 'Isaac Asimov')['lang'] == 'pt', 'pede a edição em português')
confere(C.sobrenome('Allan e Barbara Pease') == 'pease' and C.sobrenome('Ram V e Evan Cagle') == 'cagle' and C.sobrenome('Homero') == 'homero',
        'sobrenome: o do primeiro autor com nome completo; nome único vale quando não há outro')
confere(C.sobrenome('Décio Henrique Franco e outros (orgs.)') == 'franco' and C.sobrenome('Martin Luther King Jr.') == 'king', '"e outros", "(orgs.)" e "Jr." não são sobrenome')
for autor in ('', 'Vários autores', 'Autor não informado', 'Tradição hindu'):
    confere(C.consulta_de('Um Livro Qualquer', autor) is None, f'sem autor certo não se procura: "{autor}"')
confere(C.consulta_de('1984 (em quadrinhos)', 'George Orwell') is None, 'adaptação em quadrinhos com um autor só: não se procura (a capa seria a do livro)')
confere(q('1984 (em quadrinhos)', 'George Orwell e Fido Nesti') == 'title:"1984" author:nesti', 'adaptação com dois autores: procura pelo da adaptação')
confere(C.consulta_so_titulo('Sapiens: Uma Breve História da Humanidade')['q'] == 'title:"Sapiens"', 'segunda tentativa: só o título principal')

# ───────── 2 ▸ o título confere? ─────────
print('O TÍTULO CONFERE?')
tc = C.titulo_confere
confere(tc('O Nome da Rosa', 'o nome da rosa') and tc('O Físico', 'O Fisico') and tc('O Nome da Rosa', 'Nome da Rosa'), 'acento, maiúscula e artigo inicial não contam')
confere(tc('Sapiens: Uma Breve História da Humanidade', 'Sapiens') and tc('Sapiens', 'Sapiens: uma breve história da humanidade'), 'um lado com subtítulo, o outro sem: é o mesmo livro')
confere(not tc('Fundação', 'Limites da Fundação') and not tc('Fundação', 'Box Fundação') and not tc('Watchmen', 'Absolute Watchmen'), 'título que só contém o nosso não serve')
confere(not tc('Batman: Ano Um', 'Batman', hq=True) and tc('Batman: Ano Um', 'Batman', hq=False), 'quadrinho: o subtítulo não pode faltar ("Batman: Ano Um" não é qualquer "Batman")')
confere(not tc('', 'Qualquer') and not tc('Qualquer', ''), 'título vazio nunca confere')

# ───────── 3 ▸ a capa escolhida ─────────
print('A CAPA ESCOLHIDA')
confere(C.escolher('As Cavernas de Aço', CAVERNAS) == (15138088, 'edicao'), 'obra em inglês, edição em português com o nosso título: a capa é a da edição', C.escolher('As Cavernas de Aço', CAVERNAS))
confere(C.escolher('Sapiens: Uma Breve História da Humanidade', SAPIENS) == (14540965, 'edicao'), 'edição sem o subtítulo: é a mesma')
confere(C.escolher('O Físico', FISICO) == (12369732, 'edicao'), 'edição sem língua declarada também serve')
confere(C.escolher('O Nome da Rosa', ROSA) == (12385395, 'edicao'), 'resultados sem capa são pulados')
confere(C.escolher('Fundação', FUNDACAO) == (15111026, 'edicao'), 'entre "Limites da Fundação", "Fundação" e "Box Fundação", fica a do título igual')
confere(C.escolher('Watchmen', WATCHMEN, hq=True) == (14311997, 'edicao'), 'quadrinho: "Absolute Watchmen" vem antes na resposta, mas não é o nosso título')
confere(C.escolher('Fundação', [doc('Foundation', 'Isaac Asimov', 14612610, ('Fundação', None, 'por'))]) == (14612610, 'obra'), 'edição nossa sem capa: vale a capa da obra, marcada como "obra"')
confere(C.escolher('Fundação', [doc('Fundação', 'Isaac Asimov', 222)]) == (222, 'obra'), 'sem edição na resposta: capa da obra, se o título da obra for o nosso')
confere(C.escolher('Fundação', [doc('Foundation', 'Isaac Asimov', 14612610, ('Foundation', 14612610, 'eng'))]) == (None, 'nao-achei'), 'nenhum título nosso entre os resultados: não achei')
confere(C.escolher('Fundação', []) == (None, 'nao-achei') and C.escolher('Fundação', None) == (None, 'nao-achei'), 'resposta vazia: não achei')
ordem = [doc('Foundation', 'Isaac Asimov', 5, ('Fundação', 6, 'eng')), doc('Foundation', 'Isaac Asimov', 7, ('Fundação', 8, 'por'))]
confere(C.escolher('Fundação', ordem) == (8, 'edicao'), 'edição em português ganha de uma em outra língua, mesmo vindo depois')


# ───────── 4 ▸ as duas tentativas ─────────
print('AS DUAS TENTATIVAS')
class Rede:
    """Responde às consultas com o que foi gravado; anota o que foi perguntado."""
    def __init__(self, respostas): self.respostas, self.feitas = respostas, []
    def __call__(self, params, limite):
        self.feitas.append(params['q'])
        r = self.respostas.get(params['q'])
        if isinstance(r, Exception): raise r
        return {'docs': r or []}

rede = Rede({'title:"As Cavernas de Aço" author:asimov': CAVERNAS})
confere(C.procurar('As Cavernas de Aço', 'Isaac Asimov', False, None, rede) == ('15138088', 'edicao') and len(rede.feitas) == 1, 'achou na primeira: uma consulta só')
rede = Rede({'title:"Guerra e Paz" author:tolstoi': [], 'title:"Guerra e Paz"': GUERRA_E_PAZ})
r = C.procurar('Guerra e Paz', 'Liev Tolstói', False, None, rede)
confere(r == ('12369940', 'obra') and rede.feitas == ['title:"Guerra e Paz" author:tolstoi', 'title:"Guerra e Paz"'],
        'autor escrito em outro alfabeto: a segunda consulta acha pelo título e confere o autor nos nomes alternativos', (r, rede.feitas))
confere(C.autor_confere('tolstoi', GUERRA_E_PAZ[1]) and not C.autor_confere('tolstoi', GUERRA_E_PAZ[0]), 'na segunda tentativa, o livro de outro autor com o mesmo título é recusado')
rede = Rede({})
confere(C.procurar('Livro Que Não Existe', 'Fulano de Tal', False, None, rede) == ('', 'nao-achei') and len(rede.feitas) == 2, 'nada nas duas: "nao-achei", sem capa')
rede = Rede({})
confere(C.procurar('Antologia', 'Vários autores', False, None, rede) == ('', 'sem-autor') and rede.feitas == [], 'sem autor: nenhuma consulta é feita')
rede = Rede({'title:"As Cavernas de Aço" author:asimov': OSError('rede fora')})
try: C.procurar('As Cavernas de Aço', 'Isaac Asimov', False, None, rede); levantou = False
except OSError: levantou = True
confere(levantou, 'consulta que falha levanta erro (o livro não é dado como "não achei")')

# ───────── 5 ▸ o capas.tsv ─────────
print('O ARQUIVO capas.tsv')
tmp = pathlib.Path(tempfile.mkdtemp(prefix='biblioteca-capas-'))
cat = tmp / 'catalogo.md'
cat.write_text('\n'.join([
    '# Catálogo de teste', '', '## 1. Ficção', '',
    '| Título | Autor | Tags |', '| --- | --- | --- |',
    '| As Cavernas de Aço | Isaac Asimov | #F |',
    '| Guerra e Paz | Liev Tolstói | #F |',
    '| Livro Que Não Existe | Fulano de Tal | #F |',
    '| Antologia de Contos | Vários autores | #F |',
    '| Capa Posta à Mão | Autora Tal | #F |',
    '| Fundação | Isaac Asimov | #F |', '']), encoding='utf-8')
livros = parse(cat.read_text(encoding='utf-8'))
confere([b['t'] for b in livros] == ['As Cavernas de Aço', 'Guerra e Paz', 'Livro Que Não Existe', 'Antologia de Contos', 'Capa Posta à Mão', 'Fundação'], 'o catálogo de teste tem as seis linhas', [b['t'] for b in livros])

tsv = tmp / 'capas.tsv'
tsv.write_text('titulo\tautor\tcapa\torigem\nCapa Posta à Mão\tAutora Tal\thttps://exemplo.org/capa.jpg\tmanual\nLivro Que Saiu\tAlguém\t999\tmanual\nOutro Que Saiu\tAlguém\t998\tedicao\n', encoding='utf-8')
C.CATALOGO, C.CAPAS = cat, tsv
RESPOSTAS = {'title:"As Cavernas de Aço" author:asimov': CAVERNAS, 'title:"Guerra e Paz" author:tolstoi': [], 'title:"Guerra e Paz"': GUERRA_E_PAZ,
             'title:"Fundação" author:asimov': OSError('rede fora')}
rede = Rede(RESPOSTAS)
real = C.buscar_json
C.buscar_json = rede
procurar_real = C.procurar
C.procurar = lambda t, a, hq, lim, buscar=None: procurar_real(t, a, hq, lim, rede)
class Apple:
    """Faz o papel da busca do iTunes: responde pelo termo consultado e anota o que foi perguntado."""
    def __init__(self, respostas=None): self.respostas, self.feitas = respostas or {}, []
    def __call__(self, params, limite):
        self.feitas.append(params['term'])
        r = self.respostas.get(params['term'])
        if isinstance(r, Exception): raise r
        return {'resultCount': len(r or []), 'results': r or []}
apple = Apple()                                                    # nesta parte, a Apple não tem nenhum dos livros
procurar_apple_real = C.procurar_apple
C.procurar_apple = lambda t, a, hq, lim, buscar=None: procurar_apple_real(t, a, hq, lim, apple)

def roda(*args):
    s = io.StringIO()
    with contextlib.redirect_stdout(s): codigo = C.main(['--pausa', '0', *args])
    return codigo, s.getvalue()

codigo, saida = roda('--conferir')
confere(codigo == 0 and '5 a procurar' in saida and rede.feitas == [] and 'Livro Que Saiu' in tsv.read_text(encoding='utf-8'), '--conferir conta o que falta e não consulta nem grava', saida.strip())
codigo, saida = roda()
linhas = {l.split('\t')[0]: l.split('\t')[2:] for l in tsv.read_text(encoding='utf-8').splitlines()[1:]}
confere(linhas.get('As Cavernas de Aço') == ['15138088', 'edicao'] and linhas.get('Guerra e Paz') == ['12369940', 'obra'], 'capas achadas: número e origem gravados', linhas)
confere(linhas.get('Livro Que Não Existe') == ['', 'nao-achei-2'] and linhas.get('Antologia de Contos') == ['', 'sem-autor'], 'sem capa: a linha fica, com o motivo ("nao-achei-2" = procurado nas duas fontes)', linhas)
confere(apple.feitas == ['Livro Que Não Existe tal'], 'só o que a Open Library não achou é procurado na Apple (o livro sem autor e o de capa posta à mão, não)', apple.feitas)
confere(linhas.get('Capa Posta à Mão') == ['https://exemplo.org/capa.jpg', 'manual'], 'capa posta à mão não é procurada nem trocada')
confere('Fundação' not in linhas and '1 consulta(s) falharam' in saida, 'consulta que falhou: o livro fica fora do arquivo, para a próxima execução', saida.strip().splitlines()[-2:])
confere(linhas.get('Livro Que Saiu') == ['999', 'manual'] and 'Outro Que Saiu' not in linhas, 'livro que saiu do catálogo: a linha só fica se foi posta à mão')
confere(list(linhas)[:5] == ['As Cavernas de Aço', 'Guerra e Paz', 'Livro Que Não Existe', 'Antologia de Contos', 'Capa Posta à Mão'], 'as linhas saem na ordem do catálogo', list(linhas))
texto1 = tsv.read_text(encoding='utf-8')
confere(C.texto_capas(livros, C.ler_capas(tsv)) == texto1, 'ler e gravar de novo dá o mesmo arquivo')

# retomar: só o que ficou sem resposta é procurado de novo
RESPOSTAS['title:"Fundação" author:asimov'] = FUNDACAO
rede.feitas.clear()
codigo, saida = roda()
confere(rede.feitas == ['title:"Fundação" author:asimov'] and '1 a procurar' in saida, 'segunda execução: só procura o que faltou', rede.feitas)
confere(C.ler_capas(tsv)[('fundacao', 'isaac asimov')]['capa'] == '15111026', 'e a capa que faltava entra')
rede.feitas.clear()
codigo, saida = roda()
confere(rede.feitas == [] and '0 a procurar' in saida, 'terceira execução: nada a procurar')
texto2 = tsv.read_text(encoding='utf-8')
rede.feitas.clear()
apple.feitas.clear()
codigo, saida = roda('--refazer')
confere(rede.feitas == ['title:"Livro Que Não Existe" author:tal', 'title:"Livro Que Não Existe"'] and apple.feitas == ['Livro Que Não Existe tal'] and tsv.read_text(encoding='utf-8') == texto2,
        '--refazer procura de novo, nas duas fontes, só os que não foram achados', (rede.feitas, apple.feitas))

# capa tirada à mão: a linha fica sem número e marcada "manual" — nunca mais é procurada, nem com --refazer
tsv.write_text(texto2.replace('Guerra e Paz\tLiev Tolstói\t12369940\tobra', 'Guerra e Paz\tLiev Tolstói\t\tmanual'), encoding='utf-8')
rede.feitas.clear()
codigo, saida = roda('--refazer')
linhas = {l.split('\t')[0]: l.split('\t')[2:] for l in tsv.read_text(encoding='utf-8').splitlines()[1:]}
confere(rede.feitas and not any('Guerra e Paz' in q for q in rede.feitas) and linhas.get('Guerra e Paz') == ['', 'manual'], 'capa tirada à mão (linha "manual" sem número): não é procurada de novo, nem com --refazer', (rede.feitas, linhas.get('Guerra e Paz')))
confere(C.para_o_painel(livros, C.ler_capas(tsv))[1] == 0, 'e o livro vai para o painel sem capa')

# prazo esgotado: nada é consultado, e o que já havia continua lá
tsv.write_text('titulo\tautor\tcapa\torigem\nAs Cavernas de Aço\tIsaac Asimov\t15138088\tedicao\n', encoding='utf-8')
rede.feitas.clear()
codigo, saida = roda('--minutos', '-1')
confere(rede.feitas == [] and 'ficaram para a próxima execução' in saida and C.ler_capas(tsv)[('as cavernas de aco', 'isaac asimov')]['capa'] == '15138088', 'acabou o tempo: para de procurar e mantém o que já tinha', saida.strip().splitlines()[-1:])

# rede fora do ar: desiste logo, não grava "não achei" para ninguém
cat.write_text('\n'.join(['# Catálogo de teste', '', '## 1. Ficção', '', '| Título | Autor | Tags |', '| --- | --- | --- |'] + [f'| Livro {n} | Autor Número{n} | #F |' for n in range(60)] + ['']), encoding='utf-8')
tsv.unlink()
class Fora:
    feitas = 0
    def __call__(self, params, limite): Fora.feitas += 1; raise OSError('rede fora')
C.procurar = lambda t, a, hq, lim, buscar=None: procurar_real(t, a, hq, lim, Fora())
apple.feitas.clear()
codigo, saida = roda()
confere(codigo == 1 and 'parei de procurar' in saida and 30 <= Fora.feitas <= 32, 'nenhuma consulta responde: para depois das 30 primeiras e avisa', (codigo, Fora.feitas))
confere('a Open Library não respondeu' in saida, 'e diz que o resto ficou para a próxima execução', saida.strip().splitlines()[-1:])
confere(tsv.read_text(encoding='utf-8').strip() == 'titulo\tautor\tcapa\torigem' and apple.feitas == [], 'e nenhum livro é dado como "não achei", nem levado à Apple')
C.procurar, C.procurar_apple, C.buscar_json = procurar_real, procurar_apple_real, real

# uma capa não serve a dois livros (volumes de uma série que casaram com a mesma edição)
serie = {('transurfing', 'z'): {'titulo': 'Transurfing', 'autor': 'Z', 'capa': '8729438', 'origem': 'edicao'},
         ('transurfing avante para o passado', 'z'): {'titulo': 'Transurfing: Avante para o Passado', 'autor': 'Z', 'capa': '8729438', 'origem': 'edicao'},
         ('transurfing macas caem ao ceu', 'z'): {'titulo': 'Transurfing: Maçãs Caem ao Céu', 'autor': 'Z', 'capa': '8729438', 'origem': 'edicao'},
         ('fundacao', 'a'): {'titulo': 'Fundação', 'autor': 'A', 'capa': '15111026', 'origem': 'edicao'},
         ('fundacao 2', 'a'): {'titulo': 'Fundação (edição de bolso)', 'autor': 'A', 'capa': '15111026', 'origem': 'obra'},
         ('sapiens', 'h'): {'titulo': 'Sapiens: Uma Breve História da Humanidade', 'autor': 'H', 'capa': '14540965', 'origem': 'edicao'},
         ('serie vol 1', 'm'): {'titulo': 'Série: Volume 1', 'autor': 'M', 'capa': '777', 'origem': 'manual'},
         ('serie vol 2', 'm'): {'titulo': 'Série: Volume 2', 'autor': 'M', 'capa': '777', 'origem': 'manual'}}
tiradas = C.sem_repetidas(serie)
confere(tiradas == 2 and serie[('transurfing', 'z')]['capa'] == '8729438' and serie[('transurfing macas caem ao ceu', 'z')] == {'titulo': 'Transurfing: Maçãs Caem ao Céu', 'autor': 'Z', 'capa': '', 'origem': 'nao-achei'},
        'mesma capa para os volumes de uma série: fica só no título sem subtítulo', tiradas)
confere(serie[('fundacao', 'a')]['capa'] == serie[('fundacao 2', 'a')]['capa'] == '15111026', 'duas linhas do mesmo livro (uma com parênteses) podem ter a mesma capa')
confere(serie[('sapiens', 'h')]['capa'] == '14540965', 'capa de um livro só, com subtítulo: fica')
confere(serie[('serie vol 1', 'm')]['capa'] == serie[('serie vol 2', 'm')]['capa'] == '777', 'capas postas à mão nunca saem, mesmo repetidas')
confere(C.sem_repetidas(serie) == 0, 'aplicar de novo não muda mais nada')

# ───────── 6 ▸ a segunda fonte: Apple Books ─────────
print('A SEGUNDA FONTE: APPLE BOOKS')
ARTE = lambda n: f'https://is1-ssl.mzstatic.com/image/thumb/Publication{n}/v4/aa/bb/cc/capa-{n}.jpg/100x100bb.jpg'       # como vem na resposta
NO_PAINEL = lambda n: f'https://is1-ssl.mzstatic.com/image/thumb/Publication{n}/v4/aa/bb/cc/capa-{n}.jpg/200x300bb.jpg'  # como é guardado
def ap(titulo, autor, arte, tipo='ebook'):
    return {'kind': tipo, 'trackName': titulo, 'artistName': autor, 'artworkUrl60': arte.replace('100x100bb', '60x60bb'), 'artworkUrl100': arte}

qa = lambda t, a: (C.consulta_apple(t, a) or {}).get('term')
confere(qa('Mamãe e o Sentido da Vida', 'Irvin D. Yalom') == 'Mamãe e o Sentido da Vida yalom', 'a consulta: título e sobrenome do autor', qa('Mamãe e o Sentido da Vida', 'Irvin D. Yalom'))
confere(qa('Sapiens: Uma Breve História da Humanidade', 'Yuval Noah Harari') == 'Sapiens harari' and qa('Herege (Busca do Graal, vol. 3)', 'Bernard Cornwell') == 'Herege cornwell', 'subtítulo e parênteses não entram na consulta')
pa = C.consulta_apple('Mamãe e o Sentido da Vida', 'Irvin D. Yalom')
confere(pa['country'] == 'br' and pa['media'] == 'ebook', 'procura na loja do Brasil, só entre os livros digitais', pa)
confere(all(C.consulta_apple('Um Livro Qualquer', a) is None for a in ('', 'Vários autores', 'Autor não informado')), 'sem autor certo não se procura, como na Open Library')
confere(C.consulta_apple('1984 (em quadrinhos)', 'George Orwell') is None and qa('1984 (em quadrinhos)', 'George Orwell e Fido Nesti') == '1984 nesti', 'adaptação em quadrinhos: só com o autor da adaptação')

YALOM = [ap('Mama a zmysel života', 'Irvin D. Yalom', ARTE(3)), ap('Mamãe e o sentido da vida', 'Irvin D. Yalom', ARTE(115))]
confere(C.escolher_apple('Mamãe e o Sentido da Vida', 'yalom', YALOM) == NO_PAINEL(115), 'fica o livro com o nosso título (a edição em outra língua vem antes na resposta e não serve)', C.escolher_apple('Mamãe e o Sentido da Vida', 'yalom', YALOM))
confere(C.escolher_apple('Mamãe e o Sentido da Vida', 'yalom', [ap('Mamãe e o sentido da vida', 'Outra Pessoa', ARTE(1))]) == '', 'mesmo título, outro autor: não serve')
confere(C.escolher_apple('Guerra e Paz', 'tolstoi', [ap('Guerra e paz', 'Leo Tolstoy', ARTE(2))]) == NO_PAINEL(2) and C.som('Dostoiévski') == C.som('Dostoievsky'), 'o mesmo autor em outra grafia (Tolstói · Tolstoy) serve')
SAPIENS_A = [ap('Sapiens: Uma breve história da humanidade', 'Yuval Noah Harari', ARTE(4)), ap('Sapiens', 'Yuval Noah Harari', ARTE(5))]
confere(C.escolher_apple('Sapiens', 'harari', SAPIENS_A) == NO_PAINEL(5) and C.escolher_apple('Sapiens', 'harari', SAPIENS_A[:1]) == NO_PAINEL(4), 'título igual ganha de título com subtítulo, mesmo vindo depois; subtítulo de um lado só também serve')
OUTROS = [ap('Fundação - Trilogia', 'Isaac Asimov', ARTE(6)), ap('Box Fundação', 'Isaac Asimov', ARTE(7)), ap('Fundação: Resumo do livro de Isaac Asimov', 'Isaac Asimov', ARTE(8))]
confere(C.escolher_apple('Fundação', 'asimov', OUTROS) == '', 'caixa, trilogia e resumo do livro não servem')
confere(C.escolher_apple('A Trilogia de Nova York', 'auster', [ap('A trilogia de Nova York', 'Paul Auster', ARTE(9))]) == NO_PAINEL(9), 'mas "trilogia" no nosso próprio título não atrapalha')
confere(C.escolher_apple('Batman: Ano Um', 'miller', [ap('Batman', 'Frank Miller', ARTE(10))], hq=True) == '', 'quadrinho: o subtítulo não pode faltar')
confere(C.escolher_apple('Sapiens', 'harari', [ap('Sapiens', 'Yuval Noah Harari', ARTE(11), tipo='audiobook')]) == '', 'o que não é livro digital (audiolivro) não serve')
r60 = {'kind': 'ebook', 'trackName': 'Sapiens', 'artistName': 'Yuval Noah Harari', 'artworkUrl60': ARTE(12).replace('100x100bb', '60x60bb')}
confere(C.escolher_apple('Sapiens', 'harari', [r60]) == NO_PAINEL(12), 'o endereço guardado é sempre o do tamanho que o painel usa (200 × 300), venha a resposta no tamanho que vier')
tortos = ['', 'http://is1-ssl.mzstatic.com/image/thumb/a/b.jpg/100x100bb.jpg', 'https://exemplo.org/image/thumb/a/b.jpg/100x100bb.jpg', 'https://is1-ssl.mzstatic.com/image/thumb/a/b.jpg/100x100bb.jpg"><script>',
          'https://is1-ssl.mzstatic.com/outra/coisa.jpg', 'https://is1-ssl.mzstatic.com.exemplo.org/image/thumb/a/b.jpg/100x100bb.jpg']
confere(all(C.escolher_apple('Sapiens', 'harari', [ap('Sapiens', 'Yuval Noah Harari', u)]) == '' for u in tortos), 'endereço que não tem a forma dos da Apple não é guardado (vazio, http, outro site, aspas)', [u for u in tortos if C.escolher_apple('Sapiens', 'harari', [ap('Sapiens', 'Yuval Noah Harari', u)])])
confere(C.escolher_apple('Sapiens', 'harari', None) == '' and C.escolher_apple('Sapiens', 'harari', ['texto solto', {}]) == '', 'resposta vazia ou torta: nada')

apl = Apple({'Mamãe e o Sentido da Vida yalom': YALOM})
confere(C.procurar_apple('Mamãe e o Sentido da Vida', 'Irvin D. Yalom', False, None, apl) == (NO_PAINEL(115), 'apple') and apl.feitas == ['Mamãe e o Sentido da Vida yalom'], 'achou: o endereço e a origem "apple", com uma consulta só')
confere(C.procurar_apple('Livro Que Não Existe', 'Fulano de Tal', False, None, Apple()) == ('', 'nao-achei-2'), 'não achou: "nao-achei-2", sem capa')
try: C.procurar_apple('Mamãe e o Sentido da Vida', 'Irvin D. Yalom', False, None, Apple({'Mamãe e o Sentido da Vida yalom': OSError('rede fora')})); levantou = False
except OSError: levantou = True
confere(levantou, 'consulta que falha levanta erro (o livro não é dado como "não achei")')

# a busca recusa quando as consultas vêm depressa demais: esperar e tentar de novo
import urllib.error
class Resposta:
    def __init__(self, corpo): self.corpo = corpo
    def read(self): return self.corpo
    def __enter__(self): return self
    def __exit__(self, *a): return False
class SemEspera:
    def espera(self): pass
def servidor(respostas):
    fila, pedidos = list(respostas), []
    def abre(req, timeout=None):
        pedidos.append(req.full_url)
        r = fila.pop(0)
        if isinstance(r, int): raise urllib.error.HTTPError(req.full_url, r, 'recusado', {}, None)
        return Resposta(json.dumps(r).encode('utf-8'))
    return abre, pedidos
abrir_url_real, esperas = C.urllib.request.urlopen, []
try:
    C.urllib.request.urlopen, pedidos = servidor([403, 429, {'resultCount': 0, 'results': []}])
    r = C.buscar_apple(pa, SemEspera(), dormir=esperas.append)
    confere(r == {'resultCount': 0, 'results': []} and esperas == [60, 120] and len(pedidos) == 3, 'busca recusada por excesso de consultas (403, 429): espera um minuto, depois dois, e tenta de novo', (esperas, len(pedidos)))
    confere(pedidos[0].startswith('https://itunes.apple.com/search?') and 'term=Mam%C3%A3e+e+o+Sentido+da+Vida+yalom' in pedidos[0] and 'country=br' in pedidos[0] and 'media=ebook' in pedidos[0], 'o endereço consultado é o da busca do iTunes', pedidos[0])
    C.urllib.request.urlopen, pedidos = servidor([403, 403, 403]); esperas.clear()
    try: C.buscar_apple(pa, SemEspera(), dormir=esperas.append); levantou = False
    except urllib.error.HTTPError: levantou = True
    confere(levantou and len(pedidos) == 3 and esperas == [60, 120], 'recusada três vezes: a consulta falha (e o livro fica para a próxima execução)', (len(pedidos), esperas))
    C.urllib.request.urlopen, pedidos = servidor([404, {}]); esperas.clear()
    try: C.buscar_apple(pa, SemEspera(), dormir=esperas.append); levantou = False
    except urllib.error.HTTPError: levantou = True
    confere(levantou and len(pedidos) == 1 and esperas == [], 'outro erro (404): não insiste')
finally:
    C.urllib.request.urlopen = abrir_url_real

# as duas fontes, em ordem, com o arquivo
print('AS DUAS FONTES, EM ORDEM')
def catalogo_de(linhas):
    cat.write_text('\n'.join(['# Catálogo de teste', '', '## 1. Ficção', '', '| Título | Autor | Tags |', '| --- | --- | --- |'] + [f'| {t} | {a} | #F |' for t, a in linhas] + ['']), encoding='utf-8')
def linhas_do_tsv(): return {l.split('\t')[0]: l.split('\t')[2:] for l in tsv.read_text(encoding='utf-8').splitlines()[1:]}
catalogo_de([('Mamãe e o Sentido da Vida', 'Irvin D. Yalom'), ('Livro Só da Open Library', 'Autora Um'), ('Livro Só da Apple', 'Autor Dois'), ('Livro de Lugar Nenhum', 'Autora Três'),
             ('Outro Sem Capa', 'Autor Quatro'), ('Já Procurado nas Duas', 'Autora Cinco'), ('Antologia', 'Vários autores')])
tsv.write_text('titulo\tautor\tcapa\torigem\nMamãe e o Sentido da Vida\tIrvin D. Yalom\t\tnao-achei\nOutro Sem Capa\tAutor Quatro\t\tnao-achei\nJá Procurado nas Duas\tAutora Cinco\t\tnao-achei-2\nAntologia\tVários autores\t\tsem-autor\n', encoding='utf-8')
rede = Rede({'title:"Livro Só da Open Library" author:um': [doc('Livro Só da Open Library', 'Autora Um', 501, ('Livro Só da Open Library', 502, 'por'))]})
apple = Apple({'Mamãe e o Sentido da Vida yalom': YALOM, 'Livro Só da Apple dois': [ap('Livro só da Apple', 'Autor Dois', ARTE(20))]})
C.procurar = lambda t, a, hq, lim, buscar=None: procurar_real(t, a, hq, lim, rede)
C.procurar_apple = lambda t, a, hq, lim, buscar=None: procurar_apple_real(t, a, hq, lim, apple)
codigo, saida = roda('--conferir')
confere('5 a procurar (2 só na Apple' in saida and rede.feitas == [] and apple.feitas == [], '--conferir: três livros novos e dois que só tinham passado pela Open Library', saida.strip())
codigo, saida = roda()
L = linhas_do_tsv()
confere(L.get('Mamãe e o Sentido da Vida') == [NO_PAINEL(115), 'apple'] and not any('Mamãe' in q or 'Outro Sem Capa' in q for q in rede.feitas),
        'livro que já tinha passado pela Open Library ("nao-achei"): vai só à Apple, e a capa entra com a origem "apple"', (L.get('Mamãe e o Sentido da Vida'), rede.feitas))
confere(L.get('Livro Só da Open Library') == ['502', 'edicao'] and 'Livro Só da Open Library um' not in apple.feitas, 'livro novo achado na Open Library: a Apple nem é consultada')
confere(L.get('Livro Só da Apple') == [NO_PAINEL(20), 'apple'] and 'title:"Livro Só da Apple" author:dois' in rede.feitas, 'livro novo que a Open Library não tem: a capa vem da Apple')
confere(L.get('Livro de Lugar Nenhum') == ['', 'nao-achei-2'] and L.get('Outro Sem Capa') == ['', 'nao-achei-2'], 'quem não está em nenhuma das duas fica "nao-achei-2"', (L.get('Livro de Lugar Nenhum'), L.get('Outro Sem Capa')))
confere(L.get('Já Procurado nas Duas') == ['', 'nao-achei-2'] and L.get('Antologia') == ['', 'sem-autor'] and not any('Procurado' in q or 'Antologia' in q for q in rede.feitas + apple.feitas),
        'quem já tinha passado pelas duas, ou não tem autor, não é procurado')
confere(sorted(apple.feitas) == ['Livro Só da Apple dois', 'Livro de Lugar Nenhum tres', 'Mamãe e o Sentido da Vida yalom', 'Outro Sem Capa quatro'] and codigo == 0, 'quatro consultas à Apple, uma por livro', sorted(apple.feitas))
confere('Resultado: 2 apple · 1 edicao · 3 nao-achei-2 · 1 sem-autor · 0 consulta(s) falharam' in saida, 'o resumo conta cada origem', saida.strip().splitlines()[-1:])
rede.feitas.clear(); apple.feitas.clear(); texto3 = tsv.read_text(encoding='utf-8')
codigo, saida = roda()
confere('0 a procurar' in saida and rede.feitas == [] and apple.feitas == [] and tsv.read_text(encoding='utf-8') == texto3, 'segunda execução: nada a procurar, nada muda')
codigo, saida = roda('--refazer')
confere(len(rede.feitas) == 6 and sorted(apple.feitas) == ['Já Procurado nas Duas cinco', 'Livro de Lugar Nenhum tres', 'Outro Sem Capa quatro'] and tsv.read_text(encoding='utf-8') == texto3,
        '--refazer: os três "nao-achei-2" voltam às duas fontes', (rede.feitas, apple.feitas))
confere(C.para_o_painel(parse(cat.read_text(encoding='utf-8')), C.ler_capas(tsv))[:3] == [NO_PAINEL(115), 502, NO_PAINEL(20)], 'para o painel: o número da Open Library ou o endereço da Apple')

# uma consulta à Apple falha no meio: só aquele livro fica para depois
apple = Apple({'Mamãe e o Sentido da Vida yalom': YALOM, 'Outro Sem Capa quatro': OSError('caiu')})
tsv.write_text('titulo\tautor\tcapa\torigem\nMamãe e o Sentido da Vida\tIrvin D. Yalom\t\tnao-achei\nOutro Sem Capa\tAutor Quatro\t\tnao-achei\n', encoding='utf-8')
catalogo_de([('Mamãe e o Sentido da Vida', 'Irvin D. Yalom'), ('Outro Sem Capa', 'Autor Quatro')])
codigo, saida = roda(); L = linhas_do_tsv()
confere(codigo == 0 and L.get('Mamãe e o Sentido da Vida') == [NO_PAINEL(115), 'apple'] and L.get('Outro Sem Capa') == ['', 'nao-achei'] and '1 consulta(s) falharam' in saida and 'falhou: Outro Sem Capa — Apple: OSError' in saida,
        'uma consulta à Apple que falha: o livro continua "nao-achei" (a próxima execução tenta de novo), os outros seguem', (codigo, L, saida.strip().splitlines()[-2:]))

# a Apple fora do ar: para de insistir nela, e a Open Library continua
antigos = [(f'Antigo {n}', f'Autora Velha{n}') for n in range(12)]
catalogo_de(antigos + [('Livro Só da Open Library', 'Autora Um'), ('Livro Novo Sem Capa', 'Autor Seis')])
tsv.write_text('titulo\tautor\tcapa\torigem\n' + ''.join(f'{t}\t{a}\t\tnao-achei\n' for t, a in antigos), encoding='utf-8')
class AppleFora:
    feitas = 0
    def __call__(self, params, limite): AppleFora.feitas += 1; raise OSError('recusado')
C.procurar_apple = lambda t, a, hq, lim, buscar=None: procurar_apple_real(t, a, hq, lim, AppleFora())
rede.feitas.clear()
codigo, saida = roda(); L = linhas_do_tsv()
confere(codigo == 1 and 'A Apple não respondeu a 5 consultas seguidas' in saida and 5 <= AppleFora.feitas <= 7, 'a Apple não responde: para de procurar nela depois de 5 falhas seguidas, e a execução termina com erro', (codigo, AppleFora.feitas))
confere(all(L.get(t) == ['', 'nao-achei'] for t, _ in antigos) and 'ficaram para a próxima execução (a Apple não respondeu)' in saida, 'os livros que só faltavam na Apple continuam como estavam, para a próxima execução', saida.strip().splitlines()[-1:])
confere(L.get('Livro Só da Open Library') == ['502', 'edicao'] and L.get('Livro Novo Sem Capa') == ['', 'nao-achei'], 'os livros novos passam pela Open Library do mesmo jeito; o que ela não achou fica "nao-achei", à espera da Apple', (L.get('Livro Só da Open Library'), L.get('Livro Novo Sem Capa')))
C.procurar, C.procurar_apple = procurar_real, procurar_apple_real

# a mesma capa da Apple em volumes de uma série
serie_a = {('saga', 'z'): {'titulo': 'Saga', 'autor': 'Z', 'capa': NO_PAINEL(30), 'origem': 'apple'},
           ('saga volume um', 'z'): {'titulo': 'Saga: Volume Um', 'autor': 'Z', 'capa': NO_PAINEL(30), 'origem': 'apple'}}
confere(C.sem_repetidas(serie_a) == 1 and serie_a[('saga', 'z')]['capa'] == NO_PAINEL(30) and serie_a[('saga volume um', 'z')] == {'titulo': 'Saga: Volume Um', 'autor': 'Z', 'capa': '', 'origem': 'nao-achei-2'},
        'capa da Apple repetida em volumes de uma série: sai do volume, que fica "nao-achei-2" (já passou pelas duas fontes)', serie_a)

# ───────── 7 ▸ a amostra: as capas guardadas abrem? ─────────
print('A AMOSTRA DAS CAPAS (--testar)')
JPEG = b'\xff\xd8\xff\xe0' + b'\x00' * 3000                       # o começo de uma imagem de verdade
EM_BRANCO = b'GIF89a' + b'\x00' * 37                                 # o quadradinho de 43 bytes que a Open Library manda quando não tem a capa
guardadas_t = {(str(i), 'x'): {'titulo': f'Livro {i}', 'autor': 'X', 'capa': str(1000 + i), 'origem': 'edicao'} for i in range(100)}
guardadas_t[('mao', 'x')] = {'titulo': 'À mão', 'autor': 'X', 'capa': 'https://exemplo.org/capa.jpg', 'origem': 'manual'}
guardadas_t[('sem', 'x')] = {'titulo': 'Sem capa', 'autor': 'X', 'capa': '', 'origem': 'nao-achei'}
class Imagens:
    """Faz o papel do site das capas: anota o que foi pedido e responde conforme o número."""
    def __init__(self, ruins=(), em_branco=(), inexistente=404): self.pedidos, self.ruins, self.em_branco, self.inexistente = [], set(ruins), set(em_branco), inexistente
    def __call__(self, url):
        self.pedidos.append(url); n = url.split('/b/id/')[1].split('-')[0]
        if n == C.INEXISTENTE: return (self.inexistente, '', b'') if self.inexistente != 200 else (200, 'image/gif', EM_BRANCO)
        if n in self.ruins: return 404, '', b''
        if n in self.em_branco: return 200, 'image/gif', EM_BRANCO
        return 200, 'image/jpeg', JPEG
im = Imagens(); r = C.testar(guardadas_t, 10, im, 0)
confere(r == (10, 10, [], True), 'todas abrem e a inexistente dá 404: amostra aprovada', r)
confere(len(im.pedidos) == 11 and all(u.startswith('https://covers.openlibrary.org/b/id/') and u.endswith('-M.jpg?default=false') for u in im.pedidos), 'pede no mesmo endereço que o painel usa (tamanho M, sem imagem substituta)', im.pedidos[:2])
numeros = [int(u.split('/b/id/')[1].split('-')[0]) for u in im.pedidos[:-1]]
confere(numeros == [1000, 1010, 1020, 1030, 1040, 1050, 1060, 1070, 1080, 1090], 'a amostra é espalhada pelo arquivo inteiro, e não só o começo', numeros)
confere(not any('exemplo.org' in u for u in im.pedidos), 'capas postas à mão (endereço completo) ficam fora da amostra')
im = Imagens(ruins={'1010', '1050'}); r = C.testar(guardadas_t, 10, im, 0)
confere(r[:2] == (8, 10) and [x[0] for x in r[2]] == ['1010', '1050'] and r[2][0][1] == 404, 'capa que não abre é contada e apontada pelo número', r)
im = Imagens(em_branco={'1020'}); r = C.testar(guardadas_t, 10, im, 0)
confere(r[:2] == (9, 10) and r[2][0][0] == '1020', 'o quadradinho em branco não conta como capa, mesmo vindo com resposta 200', r)
im = Imagens(inexistente=200); r = C.testar(guardadas_t, 10, im, 0)
confere(r[3] is False and r[0] == 10, 'se a capa inexistente não der 404, a amostra reprova (o painel mostraria um quadro em branco)', r)
r = C.testar(guardadas_t, 500, Imagens(), 0)
confere(r[:2] == (100, 100), 'pedir mais do que existe: testa todas, uma vez cada', r[:2])
confere(C.testar({}, 10, Imagens(), 0)[:2] == (0, 0), 'sem nenhuma capa guardada: nada a pedir')
C.CAPAS.write_text(C.texto_capas(livros, {(C.chave(b_['t']), C.chave(b_['a'])): {'titulo': b_['t'], 'autor': b_['a'], 'capa': str(2000 + i), 'origem': 'edicao'} for i, b_ in enumerate(livros)}), encoding='utf-8')
antes = C.CAPAS.read_text(encoding='utf-8'); abrir_real = C.abrir_imagem
C.abrir_imagem = Imagens(); codigo, saida = roda('--testar', '4')
confere(codigo == 0 and 'Amostra das capas: 4 de 4 abriram como imagem' in saida and 'responde "não encontrada": sim' in saida, '--testar: diz quantas abriram e termina bem', saida.strip().splitlines()[-1:])
C.abrir_imagem = Imagens(ruins={'2000', '2003'}); codigo, saida = roda('--testar', '6')
confere(codigo == 1 and '4 de 6 abriram' in saida and 'não abriu: capa 2000 — resposta 404' in saida, '--testar: menos de 9 em cada 10 abrindo, termina com erro e aponta quais', saida.strip().splitlines()[-3:])
C.abrir_imagem = Imagens(inexistente=200); codigo, saida = roda('--testar', '6')
confere(codigo == 1 and 'responde "não encontrada": NÃO' in saida, '--testar: capa inexistente sem 404 também termina com erro')
confere(C.CAPAS.read_text(encoding='utf-8') == antes, '--testar não grava nada')
C.abrir_imagem = abrir_real

# as capas da Apple entram na amostra pelo endereço guardado
guardadas_a = dict(guardadas_t)
for i in range(20): guardadas_a[(f'apple {i}', 'x')] = {'titulo': f'Da Apple {i}', 'autor': 'X', 'capa': NO_PAINEL(100 + i), 'origem': 'apple'}
class ImagensDasDuas(Imagens):
    def __call__(self, url):
        if '/b/id/' in url: return super().__call__(url)
        self.pedidos.append(url)
        return (404, '', b'') if url in self.ruins else (200, 'image/jpeg', JPEG)
im = ImagensDasDuas(); r = C.testar_apple(guardadas_a, 5, im, 0)
confere(r == (5, 5, []) and im.pedidos == [NO_PAINEL(100 + n) for n in (0, 4, 8, 12, 16)], 'amostra da Apple: pede o endereço guardado (o mesmo que o painel usa), espalhando pelo arquivo', (r, im.pedidos[:2]))
im = ImagensDasDuas(ruins={NO_PAINEL(104)}); r = C.testar_apple(guardadas_a, 5, im, 0)
confere(r[:2] == (4, 5) and r[2][0][:2] == (NO_PAINEL(104), 404), 'capa da Apple que não abre é contada e apontada pelo endereço', r)
confere(C.testar_apple(guardadas_t, 5, ImagensDasDuas(), 0) == (0, 0, []), 'sem capas da Apple: nada a pedir')
C.CAPAS.write_text(C.texto_capas(livros, {(C.chave(b_['t']), C.chave(b_['a'])): {'titulo': b_['t'], 'autor': b_['a'], 'capa': str(2000 + i) if i % 2 else NO_PAINEL(200 + i), 'origem': 'edicao' if i % 2 else 'apple'} for i, b_ in enumerate(livros)}), encoding='utf-8')
antes = C.CAPAS.read_text(encoding='utf-8')
C.abrir_imagem = ImagensDasDuas(); codigo, saida = roda('--testar', '3')
confere(codigo == 0 and 'Amostra das capas: 3 de 3 abriram como imagem' in saida and 'Amostra das capas da Apple: 3 de 3 abriram como imagem' in saida, '--testar: uma amostra de cada fonte', saida.strip().splitlines()[-2:])
C.abrir_imagem = ImagensDasDuas(ruins={NO_PAINEL(200)}); codigo, saida = roda('--testar', '3')
confere(codigo == 1 and 'Amostra das capas da Apple: 2 de 3' in saida and f'não abriu: {NO_PAINEL(200)} — resposta 404' in saida, '--testar: capas da Apple que não abrem também terminam com erro', saida.strip().splitlines()[-2:])
confere(C.CAPAS.read_text(encoding='utf-8') == antes, '--testar continua sem gravar nada')
C.abrir_imagem = abrir_real

# ───────── 8 ▸ o que vai para o painel ─────────
print('O QUE VAI PARA O PAINEL')
caps = {('a', 'x'): {'capa': '123'}, ('b', 'x'): {'capa': 'https://exemplo.org/b.jpg'}, ('c', 'x'): {'capa': ''}, ('d', 'x'): {'capa': 'http://sem-s.org/d.jpg'},
        ('e', 'x'): {'capa': 'https://exemplo.org/"><script>'}, ('f', 'x'): {'capa': '0'}, ('g', 'x'): {'capa': 'abc'}}
lista = C.para_o_painel([{'t': t, 'a': 'x'} for t in 'abcdefgh'], caps)
confere(lista == [123, 'https://exemplo.org/b.jpg', 0, 0, 0, 0, 0, 0], 'número, endereço https ou 0; o que não for isso (http, aspas, texto solto) vira 0', lista)
confere(C.endereco('123') == 'https://covers.openlibrary.org/b/id/123-M.jpg' and C.endereco('https://exemplo.org/b.jpg') == 'https://exemplo.org/b.jpg' and C.endereco('') == '', 'endereço da imagem de uma capa')

# o que está no repositório: src/capas.json em dia com catalogo/capas.tsv e com o catálogo
C.CATALOGO, C.CAPAS = bc.SRC, C.RAIZ / 'catalogo' / 'capas.tsv'
do_catalogo = parse(bc.SRC.read_text(encoding='utf-8'))
no_painel = json.loads(bc.DEST_CAPAS.read_text(encoding='utf-8')) if bc.DEST_CAPAS.exists() else None
confere(no_painel == C.para_o_painel(do_catalogo), 'src/capas.json está em dia com catalogo/capas.tsv (se falhar: python tools/atualizar.py)')
confere(no_painel is not None and len(no_painel) == len(json.loads(bc.DEST.read_text(encoding='utf-8'))), 'uma posição por linha de src/catalog.json')
guardadas = C.ler_capas()
confere(all(r['origem'] in C.ORIGENS for r in guardadas.values()), 'capas.tsv: toda origem é uma das conhecidas', sorted({r['origem'] for r in guardadas.values()} - C.ORIGENS))
confere(all((r['capa'] == '') == (r['origem'] in C.SEM_CAPA) for r in guardadas.values() if r['origem'] != 'manual'), 'capas.tsv: tem capa quem foi achado, e só quem foi achado')
confere(all(r['capa'].isdigit() for r in guardadas.values() if r['origem'] in ('edicao', 'obra')) and all(C.IMAGEM_APPLE.match(r['capa']) and r['capa'].endswith('/' + C.TAMANHO_APPLE) for r in guardadas.values() if r['origem'] == 'apple'),
        'capas.tsv: capa da Open Library é um número; capa da Apple é um endereço de imagem da Apple, no tamanho que o painel usa')
confere(all(r['capa'] == '' or r['capa'].isdigit() or r['capa'].lower().startswith('https://') for r in guardadas.values()), 'capas.tsv: a capa é um número ou um endereço https')
chaves = {(C.chave(b['t']), C.chave(b['a'])) for b in do_catalogo}
confere(all(k in chaves or r['origem'] == 'manual' for k, r in guardadas.items()), 'capas.tsv: toda linha é de um livro do catálogo')
import copy
confere(C.sem_repetidas(copy.deepcopy(guardadas)) == 0, 'capas.tsv: nenhuma capa repetida em volumes de uma série (se falhar: python tools/capas.py --arrumar)')
confere(C.texto_capas(do_catalogo, guardadas) == (C.CAPAS.read_text(encoding='utf-8') if C.CAPAS.exists() else C.texto_capas(do_catalogo, {})), 'capas.tsv: está na ordem do catálogo, sem linhas de livros que saíram')
print(f'   ({len(guardadas)} linhas no capas.tsv; {sum(1 for c in (no_painel or []) if c)} capas no painel)')

import shutil
shutil.rmtree(tmp, ignore_errors=True)
print('ERROS:', len(erros))
for e in erros: print('  ', e)
sys.exit(1 if erros else 0)
