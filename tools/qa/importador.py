"""O importador da biblioteca virtual (tools/importar_digital.py), numa cópia temporária dos dados:
repetir não muda nada; arquivo novo, arquivo ausente, marcador posto à mão, correção no inventário e --conferir;
a classificação (temas, dificuldade, extensão) que vem da coluna `marcadores` do inventário;
quadrinhos: subpasta de série, edição nova de série conhecida, série nova, adaptação com o título de um livro,
subpasta que é outra pasta com listagem própria.
E a conversão do catálogo para o painel (tools/build_catalog.py): src/catalog.json em dia; nomes antigos das linhas
corrigidas (catalogo/renomeados.tsv); trilhas de leitura (catalogo/trilhas.md); classificação de antes da vistoria
(catalogo/antes-da-vistoria.tsv); e o HTML pronto com tudo isso dentro. Não precisa de navegador."""
import contextlib, csv, io, json, pathlib, re, shutil, sys, tempfile

QA = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(QA.parent))
import importar_digital as imp
import build_catalog as bc
from parse_catalog import parse

erros = []
def confere(cond, msg):
    print(('ok    ' if cond else 'FALHOU'), msg)
    if not cond: erros.append(msg)

avisos_json = []
json_em_dia = bc.build(avisos_json) == json.loads(bc.DEST.read_text(encoding='utf-8'))      # antes de trocar os dados pela cópia

tmp = pathlib.Path(tempfile.mkdtemp(prefix='biblioteca-importador-'))
shutil.copytree(imp.LISTAGENS, tmp / 'listagens')
shutil.copy(imp.INVENTARIO, tmp / 'inventario.tsv')
shutil.copy(imp.CATALOGO, tmp / 'catalogo.md')
shutil.copy(imp.RESUMO, tmp / 'RESUMO.md')
imp.LISTAGENS, imp.INVENTARIO, imp.CATALOGO, imp.RESUMO = tmp / 'listagens', tmp / 'inventario.tsv', tmp / 'catalogo.md', tmp / 'RESUMO.md'

def roda(*args):
    s = io.StringIO()
    with contextlib.redirect_stdout(s): imp.main(list(args))
    return s.getvalue()
ler = lambda p: (tmp / p).read_text(encoding='utf-8')
livros = lambda: parse(ler('catalogo.md'))
def linha(titulo): return next((b for b in livros() if b['t'] == titulo), None)

# 1 ▸ o que está no repositório já é o resultado do importador
antes = {p: ler(p) for p in ('inventario.tsv', 'catalogo.md', 'RESUMO.md')}
saida = roda()
confere('Nada mudou.' in saida and all(ler(p) == antes[p] for p in antes), 'rodar de novo não muda nada')
L = livros()
confere(not any('ja-tenho' in b['tags'] for b in L), 'nenhum #ja-tenho sobrou')
confere(all('tenho-fisico' in b['tags'] for b in L if b['sec'] == 0), 'toda a seção 0 tem #tenho-fisico')
confere(all('tenho-digital' in b['tags'] and b.get('sub') for b in L if b['sec'] == 17), 'toda a seção 17 tem #tenho-digital e eixo')
chaves = [(imp.chave(b['t']), imp.chave(b['a'])) for b in L]
confere(len(set(chaves)) == len(chaves), 'nenhum livro repetido no catálogo')
obras = imp.obras_do_inventario(imp.ler_inventario(imp.INVENTARIO))
ligadas, soltas = imp.casar(obras, L)
confere(not soltas and len(ligadas) == len(obras), f'cada livro do inventário tem a sua linha no catálogo ({len(obras)})')
confere(sum('tenho-digital' in b['tags'] for b in L) == len(obras), 'e cada #tenho-digital tem arquivo no inventário')
sem_medida = [b['t'] for b in L if not {'d1', 'd2', 'd3'} & set(b['tags']) or not {'e1', 'e2', 'e3'} & set(b['tags'])]
confere(not sem_medida and 'Sem dificuldade nem extensão' not in antes['RESUMO.md'], 'todo livro do catálogo tem dificuldade e extensão' + (f': faltam em {sem_medida[:5]}' if sem_medida else ''))
pend = [r for r in imp.ler_inventario(imp.INVENTARIO) if imp.tem_obs(r, 'verificar') and not imp.tem_obs(r, 'ausente')]
trecho = antes['RESUMO.md'].split('\n## A verificar\n')[-1].split('\n## ')[0]
confere(len(pend) > 0 and trecho.count('\n- ') == len(pend) and all(f'{"subpasta" if r["formato"] == imp.FORMATO_PASTA else "arquivo"} `{r["pasta"]}\\{r["arquivo"]}`' in trecho for r in pend),
        f'o resumo diz a pasta e o nome exato do arquivo (ou da subpasta) de cada item a verificar ({len(pend)})')

# 2 ▸ --conferir não grava
with open(tmp / 'listagens' / 'poesia.txte', 'ab') as f: f.write('Poemas Novos - Fulano de Tal.epub\r\n'.encode('cp850'))
saida = roda('--conferir')
confere('Mudaria' in saida and all(ler(p) == antes[p] for p in antes), '--conferir avisa e não grava')

# 3 ▸ arquivo novo: entra no inventário como "novo" e no catálogo com #verificar
saida = roda()
inv = imp.ler_inventario(imp.INVENTARIO)
novo = [r for r in inv if r['arquivo'] == 'Poemas Novos - Fulano de Tal.epub']
confere(len(novo) == 1 and novo[0]['titulo'] == 'Poemas Novos' and novo[0]['autor'] == 'Fulano de Tal' and novo[0]['obs'] == 'novo' and novo[0]['eixo'] == '8', 'arquivo novo entra no inventário, marcado "novo"')
b = linha('Poemas Novos')
confere(bool(b) and b['sec'] == 17 and b['sub'] == 8 and b['tags'] == ['poesia', 'verificar', 'tenho-digital'], 'e no catálogo, na seção 17.8, com #verificar')
confere('Poemas Novos' in ler('RESUMO.md') and 'Nada mudou.' in roda(), 'aparece no resumo; repetir não muda nada')

# 4 ▸ marcador posto à mão na seção 17 sobrevive; correção no inventário vale
md = ler('catalogo.md').replace('| Poemas Novos | Fulano de Tal | #poesia #verificar #tenho-digital |', '| Poemas Novos | Fulano de Tal | #poesia #lido #top #verificar #tenho-digital |')
(tmp / 'catalogo.md').write_text(md, encoding='utf-8', newline='\n')
for r in inv:
    if r['arquivo'] == 'Poemas Novos - Fulano de Tal.epub': r['obs'] = ''
(tmp / 'inventario.tsv').write_text(imp.texto_inventario(inv), encoding='utf-8', newline='\n')
roda()
confere(linha('Poemas Novos')['tags'] == ['poesia', 'lido', 'top', 'tenho-digital'], 'marcadores postos à mão ficam; #verificar sai quando o inventário é revisado')

# 4b ▸ a classificação (temas, dificuldade, extensão) vem da coluna `marcadores` do inventário; na linha, à mão, só #lido e #top
confere('\n## Sem dificuldade nem extensão\n' in ler('RESUMO.md') and '- Poemas Novos — Fulano de Tal · pasta `poesia`' in ler('RESUMO.md'), 'obra ainda sem classificação no inventário aparece no resumo, em "Sem dificuldade nem extensão"')
inv = imp.ler_inventario(imp.INVENTARIO)
for r in inv:
    if r['arquivo'] == 'Poemas Novos - Fulano de Tal.epub': r['marcadores'] = 'BR #d1 e1 verificar tenho-fisico lido'      # o que não é classificação é ignorado
(tmp / 'inventario.tsv').write_text(imp.texto_inventario(inv), encoding='utf-8', newline='\n')
md = ler('catalogo.md').replace('| Poemas Novos | Fulano de Tal | #poesia #lido #top #tenho-digital |', '| Poemas Novos | Fulano de Tal | #poesia #tema-posto-a-mao #top #tenho-digital |')
(tmp / 'catalogo.md').write_text(md, encoding='utf-8', newline='\n')
roda()
confere(linha('Poemas Novos')['tags'] == ['poesia', 'BR', 'd1', 'e1', 'top', 'tenho-digital'], 'a linha leva o tipo, a classificação do inventário, o #top posto à mão e a posse; tema posto à mão na seção 17 não fica')
confere('Sem dificuldade nem extensão' not in ler('RESUMO.md') and 'Nada mudou.' in roda(), 'classificada, a obra sai da lista do resumo; repetir não muda nada')
obra = lambda **k: dict({'t': 'Um Título', 'a': 'Alguém', 'verificar': False, 'marcadores': []}, **k)
confere(imp.tags_da_obra(obra(genero='NF', pastas=['fisica e astronomia'])) == ['NF', 'ciencia', 'fisica', 'tenho-digital']
        and imp.tags_da_obra(obra(genero='F', pastas=['fisica e astronomia'])) == ['F', 'tenho-digital']
        and imp.tags_da_obra(obra(genero='NF', pastas=['fisica e astronomia'], marcadores=['cosmologia', 'd2', 'e2'], verificar=True), ('lido', 'outro')) == ['NF', 'cosmologia', 'd2', 'e2', 'lido', 'verificar', 'tenho-digital'],
        'sem classificação valem os marcadores padrão da pasta (menos para o livro guardado na pasta de outro gênero); com classificação, só ela')
arquivo = lambda nome, marcadores: dict(pasta='Filosofia', arquivo=nome, formato=nome.rsplit('.', 1)[1], tipo='livro', titulo='Obra em Dois Formatos', autor='Autora', catalogo='', eixo='9', genero='NF', marcadores=marcadores, obs='')
duas = imp.obras_do_inventario([arquivo('a.epub', 'filosofia d2 e1'), arquivo('a.pdf', '#filosofia etica d2')])
confere([o['marcadores'] for o in duas.values()] == [['filosofia', 'd2', 'e1', 'etica']], 'dois arquivos da mesma obra: a classificação junta o que as duas linhas dizem, sem repetir')
tabela = list(csv.reader(io.StringIO(ler('inventario.tsv'), newline=''), delimiter='\t')); c = tabela[0].index('marcadores')
texto = io.StringIO(newline=''); csv.writer(texto, delimiter='\t', lineterminator='\n').writerows([l[:c] + l[c + 1:] for l in tabela])
(tmp / 'inventario-antigo.tsv').write_text(texto.getvalue(), encoding='utf-8', newline='\n')
antigo = imp.ler_inventario(tmp / 'inventario-antigo.tsv')
confere(len(antigo) == len(inv) and all(r['marcadores'] == '' for r in antigo) and imp.texto_inventario(antigo).split('\n')[0].split('\t') == imp.COLUNAS,
        'inventário sem a coluna `marcadores` (como era antes da vistoria) ainda é lido; ao gravar, a coluna aparece, vazia')
(tmp / 'inventario-ruim.tsv').write_text('pasta\tarquivo\tformato\tmarcadores\nx\ty.pdf\tpdf\td1\n', encoding='utf-8', newline='\n')
try: imp.ler_inventario(tmp / 'inventario-ruim.tsv'); parou = ''
except SystemExit as e: parou = str(e)
confere('faltam as colunas tipo, titulo, autor, catalogo, eixo, genero, obs' in parou, 'sem uma coluna obrigatória o importador para e diz quais faltam')

# 5 ▸ arquivo que some da listagem: "ausente" no inventário, fora do catálogo; se voltar, volta
bruto = (tmp / 'listagens' / 'poesia.txte').read_bytes()
(tmp / 'listagens' / 'poesia.txte').write_bytes(bruto.replace('Poemas Novos - Fulano de Tal.epub\r\n'.encode('cp850'), b''))
roda()
r = next(r for r in imp.ler_inventario(imp.INVENTARIO) if r['arquivo'] == 'Poemas Novos - Fulano de Tal.epub')
confere(r['obs'] == 'ausente' and linha('Poemas Novos') is None, 'arquivo que sumiu fica "ausente" e sai do catálogo')
confere('Marcadores que ficaram sem linha' in ler('RESUMO.md'), 'o resumo avisa dos marcadores que ficaram sem linha')
(tmp / 'listagens' / 'poesia.txte').write_bytes(bruto)
roda()
confere(linha('Poemas Novos') is not None, 'se o arquivo volta, o livro volta')

# 6 ▸ livro digital que já está no catálogo: marca a linha existente em vez de criar outra
with open(tmp / 'listagens' / 'Filosofia.txte', 'ab') as f: f.write('O Mito de Sísifo - Albert Camus.epub\r\n'.encode('cp850'))
n = len(livros())
jatinha = 'tenho-digital' in linha('O Mito de Sísifo')['tags']
roda()
b = linha('O Mito de Sísifo')
confere(b['sec'] != 17 and 'tenho-digital' in b['tags'] and len(livros()) == n, 'livro já catalogado ganha #tenho-digital na linha que já existia' + (' (já tinha)' if jatinha else ''))

# 7 ▸ listagem em UTF-8 (em vez de CP850) também é lida
(tmp / 'listagens' / 'poesia.txte').write_bytes(bruto.decode('cp850').encode('utf-8'))
confere('Nada mudou.' in roda(), 'listagem em UTF-8 é lida do mesmo jeito')

# 8 ▸ quadrinhos: nas pastas de HQ cada subpasta é uma série; no catálogo, uma série é uma linha só
inv = imp.ler_inventario(imp.INVENTARIO)
hq = [r for r in inv if r['tipo'] == 'hq']
series = [r for r in hq if r['formato'] == imp.FORMATO_PASTA]
confere(len(series) > 50 and not any(imp.tem_obs(r, 'ausente') for r in hq), f'as subpastas de séries estão no inventário e nenhuma consta como ausente ({len(series)})')
confere(all(r['genero'] == 'HQ' for r in hq) and all(imp.pasta_de_hq(r['pasta']) for r in series), 'toda linha de quadrinho tem gênero HQ; subpasta de série, só nas pastas de quadrinhos')
# a subpasta "novas", de novashqs, não é uma série: é outra pasta, e a listagem dela chama-se novasHQSS
bruto_novas = (tmp / 'listagens' / 'novashqs.txte').read_bytes()
resumo = ler('RESUMO.md')
fora = next((l for l in resumo.splitlines() if l.startswith(('- Subpasta sem listagem', '- Subpastas sem listagem'))), '')
confere(b'\r\nnovas\r\n' in bruto_novas and not any(r['pasta'] == 'novashqs' and r['arquivo'] == 'novas' for r in inv)
        and any(r['pasta'] == 'novasHQSS' for r in inv) and linha('novas') is None
        and '`novas`, de `novashqs`, tem listagem própria, `novasHQSS`' in resumo and 'novas' not in fora and '`HQs/Mangás`' in fora,
        'subpasta com listagem própria ("novas" = novasHQSS) não vira série nem consta como "sem listagem"; o resumo diz onde ela está')
confere(imp.subpastas_listadas({'novashqs', 'novasHQSS'}) == {('novashqs', 'novas'): 'novasHQSS'} and imp.subpastas_listadas({'novashqs', 'HQs'}) == {},
        'a regra só vale enquanto a listagem da subpasta existir')
sem_linha = [o['t'] for (kt, ka), o in obras.items() if o['genero'] == 'HQ' and not any(imp.chave(x['t']) == kt and 'HQ' in x['tags'] for x in L)]
confere(not sem_linha, 'cada quadrinho do inventário está numa linha #HQ do catálogo' + (f': {sem_linha[:5]}' if sem_linha else ''))
nomes = {'Coda #03 [Ndrangheta & Yugifan].cbr': 'Coda', 'Earthdivers 004 (2023) (QI).cbz': 'Earthdivers', 'As.Eras.Perdidas.01(Ndrangheta&Yugifan).cbr': 'As Eras Perdidas',
         'Rapa Nui v2 (QI).cbz': 'Rapa Nui', 'Elfos - Livro II [Ndrangheta & DecKArte].cbr': 'Elfos', 'Batman 89 #06 (2022) (SQ&ZF).cbr': 'Batman 89',
         '100 Balas (13 de 15)': '100 Balas', 'Heróis Renascem[HQ Torrent]': 'Heróis Renascem', '18 Dias (2015)-20241229T204405Z-001.zip': '18 Dias',
         'Asgard.01de02.Pe.de.Ferro(Yugifan).cbr': 'Asgard', 'Charada - Ano Um #01 (Shinobi-2022).cbr': 'Charada: Ano Um', 'Vortex 2.0.cbr': 'Vortex 2.0',
         'Graphic Marvel 14 - Os Escravistas.rar.cbr': 'Graphic Marvel 14: Os Escravistas', '2001 Odisseia no espaço': '2001 Odisseia no Espaço'}
errados = {n: imp.deduzir_hq(n)[0] for n, t in nomes.items() if imp.chave(imp.deduzir_hq(n)[0]) != imp.chave(t)}
confere(not errados and imp.deduzir_hq('Celestia (Manuele Fior) (Z-Library).pdf') == ('Celestia', 'Manuele Fior'),
        'o nome da série sai do nome do arquivo ou da subpasta, sem ano, grupo e número da edição' + (f': {errados}' if errados else ''))

def acrescenta(listagem, *linhas_novas):
    with open(tmp / 'listagens' / f'{listagem}.txte', 'ab') as f:
        f.write(''.join(l + '\r\n' for l in linhas_novas).encode('cp850'))
do_inv = lambda arquivo: next((r for r in imp.ler_inventario(imp.INVENTARIO) if r['arquivo'] == arquivo), None)
coda = next(r for r in hq if r['titulo'] == 'Coda')
n = len(livros())
acrescenta('novashqs', 'Coda #99 [Outro Grupo].cbr')
saida = roda()
r = do_inv('Coda #99 [Outro Grupo].cbr')
confere(bool(r) and (r['tipo'], r['titulo'], r['autor'], r['eixo'], r['obs']) == ('hq', 'Coda', coda['autor'], coda['eixo'], '') and len(livros()) == n
        and 'mais uma edição' in saida, 'edição nova de uma série conhecida entra na série, sem linha nova no catálogo e sem nada a revisar')
acrescenta('HQs', 'Monstress', 'Monstress #01 (2015) (Grupo).cbz', 'Batman - Ano Um.cbr', 'capa.jpg')
acrescenta('poesia', 'Uma Subpasta de Poesia')
roda()
r, r2, r3 = do_inv('Monstress'), do_inv('Monstress #01 (2015) (Grupo).cbz'), do_inv('Batman - Ano Um.cbr')
confere(bool(r and r2) and (r['tipo'], r['formato'], r['titulo'], r['genero'], r['obs']) == ('hq', 'pasta', 'Monstress', 'HQ', 'novo') and (r2['formato'], r2['titulo'], r2['obs']) == ('cbz', 'Monstress', 'novo'),
        'série nova (a subpasta e um arquivo solto) entra como quadrinho, marcada "novo"')
b = [x for x in livros() if x['t'] == 'Monstress']
confere(len(b) == 1 and b[0]['sec'] == 17 and b[0]['tags'] == ['HQ', 'verificar', 'tenho-digital'], 'e vira uma linha só no catálogo, #HQ, com #verificar')
confere(bool(r3) and r3['obs'] == 'novo' and imp.chave(r3['titulo']) == 'batman ano um', 'um nome parecido não basta: “Batman - Ano Um” não entra na série “Batman”')
confere(do_inv('capa.jpg') is None and do_inv('Uma Subpasta de Poesia') is None and '`HQs/capa.jpg`' in ler('RESUMO.md'),
        'arquivo de outro tipo e subpasta de pasta de livros não entram; o resumo cita o arquivo ignorado')
# adaptação em quadrinhos com o título de um livro que está no catálogo como recomendação: o livro não passa a "tenho em digital"
alvo = next(x for x in livros() if x['sec'] not in (0, 17) and 'tenho-digital' not in x['tags'] and 'HQ' not in x['tags'] and x['t'].replace(' ', '').isalpha()
            and sum(imp.chave(y['t']) == imp.chave(x['t']) for y in L) == 1)
acrescenta('HQs', alvo['t'])
roda()
mesmos = [x for x in livros() if imp.chave(x['t']) == imp.chave(alvo['t'])]
confere(len(mesmos) == 2 and [x for x in mesmos if x['sec'] != 17][0]['tags'] == alvo['tags'] and 'HQ' in [x for x in mesmos if x['sec'] == 17][0]['tags'],
        f'quadrinho com o título de um livro do catálogo (“{alvo["t"]}”) ganha linha própria; o livro não é marcado como digital')
bruto = (tmp / 'listagens' / 'HQs.txte').read_bytes()
confere(b'\r\nAkira\r\n' in bruto and linha('Akira') is not None, 'a série “Akira” está numa subpasta da listagem e no catálogo')
(tmp / 'listagens' / 'HQs.txte').write_bytes(bruto.replace(b'\r\nAkira\r\n', b'\r\n'))
roda()
confere(do_inv('Akira')['obs'] == 'ausente' and linha('Akira') is None and 'Nada mudou.' in roda(), 'subpasta que some da listagem fica "ausente" e a série sai do catálogo')
(tmp / 'listagens' / 'novasHQSS.txte').rename(tmp / 'novasHQSS.guardada')
roda()
r = next((x for x in imp.ler_inventario(imp.INVENTARIO) if x['pasta'] == 'novashqs' and x['arquivo'] == 'novas'), None)
confere(bool(r) and (r['formato'], r['tipo'], r['obs']) == ('pasta', 'hq', 'novo') and 'novashqs/novas' in ler('RESUMO.md'),
        'sem a listagem da subpasta, "novas" volta ao inventário, marcada "novo": não some sem aviso')

# 9 ▸ o que vai para o painel: src/catalog.json em dia, e o nome antigo das linhas corrigidas no catálogo
confere(json_em_dia and not avisos_json, 'src/catalog.json está em dia com o catálogo e o inventário, sem avisos' + (': ' + ' | '.join(avisos_json) if avisos_json else ''))
dados = json.loads(bc.DEST.read_text(encoding='utf-8'))
digital_ok = lambda d: d is None or (len(d) in (5, 6) and isinstance(d[1], int) and (len(d) == 5 or (d[5] and all(isinstance(x, str) for x in d[5]))) and (d[1] > 0 or len(d) == 6))
forma = all(len(r) in (6, 7, 8) and (len(r) < 7 or digital_ok(r[6])) and (len(r) < 8 or (r[7] and all(len(n) == 2 for n in n8)))
            for r in dados for n8 in [r[7] if len(r) > 7 else []])
confere(forma and not any(len(r) == 7 and r[6] is None for r in dados), 'cada linha do JSON tem 6 campos, mais os dados digitais (com as subpastas das séries) e os nomes antigos quando existem')
so_pasta = [r for r in dados if len(r) > 6 and r[6] and r[6][1] == 0]
confere(len(so_pasta) > 50 and all(r[6][0] == '' and 'HQ' in r[2].split() for r in so_pasta), f'série que só existe como subpasta vai ao painel sem formato de arquivo ({len(so_pasta)})')
autor = lambda a: bc.AUTOR_FIX[a][0] if a in bc.AUTOR_FIX else a
reais = [[b['t'], autor(b['a'])] for b in parse(antes['catalogo.md'])]
n = sum(1 for l in bc.RENOMEADOS.read_text(encoding='utf-8-sig').splitlines()[1:] if l.strip())
av = []; ant = bc.nomes_antigos(reais, av)
confere(not av and sum(len(v) for v in ant.values()) == n and sum(len(r[7]) for r in dados if len(r) > 7) == n, f'renomeados.tsv: cada nome antigo ({n}) chega à sua linha no painel')

def renomeados(*linhas_tsv):
    (tmp / 'renomeados.tsv').write_text('titulo_antigo\tautor_antigo\ttitulo_novo\tautor_novo\n' + ''.join(l + '\n' for l in linhas_tsv), encoding='utf-8', newline='\n')
    bc.RENOMEADOS, av = tmp / 'renomeados.tsv', []
    return bc.nomes_antigos([['Livro Novo', 'Autora'], ['Outro', ''], ['Ímpar', 'José']], av), av
confere(renomeados('Livro Velho\tAutora\tLivro Novo\tAutora') == ({0: [['Livro Velho', 'Autora']]}, []), 'linha renomeada leva o nome antigo')
confere(renomeados('Mais Velho\tAutora\tLivro Velho\tAutora', 'Livro Velho\tAutora\tLivro Novo\tAutora') == ({0: [['Mais Velho', 'Autora'], ['Livro Velho', 'Autora']]}, []), 'renomeada duas vezes: os dois nomes antigos levam à linha atual')
confere(renomeados('Sem Dono\t(autor não informado)\tOutro\t(autor não informado)') == ({1: [['Sem Dono', '']]}, []), '"(autor não informado)" vale como autor vazio, como no painel')
r, av = renomeados('Antigo\tX\tNão Existe\tY')
confere(r == {} and len(av) == 1 and 'não achei' in av[0], 'nome novo que não está no catálogo: aviso')
r, av = renomeados('Outro\t\tLivro Novo\tAutora')
confere(r == {} and len(av) == 1 and 'ainda é uma linha' in av[0], 'nome antigo que ainda é de outro livro: ignorado, com aviso')
confere(renomeados('impar\tjose\tÍmpar\tJosé') == ({}, []), 'só acento ou maiúscula: para o painel é o mesmo nome, nada a fazer')

# 10 ▸ as trilhas de leitura (catalogo/trilhas.md): a lista de cada trilha e o marcador #trilha-… nas linhas dos livros
L0 = parse(antes['catalogo.md']); av = []; tr = bc.ler_trilhas(L0, av)
confere(len(tr) == 36 and not av and tr == json.loads(bc.DEST_TRILHAS.read_text(encoding='utf-8')), 'as 36 trilhas são lidas sem avisos, e src/trilhas.json está em dia' + (': ' + ' | '.join(av[:3]) if av else ''))
confere(all(sorted(t[3]) == [i for i, b in enumerate(L0) if t[0] in b['tags']] and len(set(t[3])) == len(t[3]) >= 3 for t in tr), 'a lista de cada trilha são exatamente as linhas do catálogo que levam o marcador dela')
confere(all(t[1] and 30 < len(t[2]) < 400 and '|' not in t[2] and '#' not in t[2] for t in tr) and len({t[0] for t in tr}) == len({t[1] for t in tr}) == 36, 'cada trilha tem nome, marcador próprio e uma descrição curta, sem tabela nem marcador colados')

def trilhas(texto, linhas):
    (tmp / 'trilhas.md').write_text(texto, encoding='utf-8', newline='\n'); av = []
    return bc.ler_trilhas(linhas, av, tmp / 'trilhas.md'), av
LT = [{'t': 'Livro Um', 'a': 'Ana', 'tags': ['F', 'trilha-teste']}, {'t': 'Livro Dois', 'a': 'Bia', 'tags': ['F', 'trilha-teste']}, {'t': 'Livro Três', 'a': 'Caio', 'tags': ['F']}, {'t': 'Livro Um', 'a': 'Outro', 'tags': ['F']}]
confere(trilhas('# Trilhas\n\nTexto de abertura.\n\n## 1. Trilha de Teste\n\n`#trilha-teste`\n\nUma descrição\nem duas linhas.\n\n1. Livro Dois | Bia\n2. Livro Um | Ana\n', LT)
        == ([['trilha-teste', 'Trilha de Teste', 'Uma descrição em duas linhas.', [1, 0]]], []), 'trilha: marcador, nome, descrição e os livros na ordem da lista (com dois títulos iguais, vale o autor)')
r, av = trilhas('## 1. Trilha de Teste\n\n`#trilha-teste`\n\nDescrição.\n\n1. Livro Um | Ana\n2. Livro Três | Caio\n3. Não Existe | Ninguém\n', LT)
confere(r[0][3] == [0, 2] and len(av) == 3 and any('“Não Existe” (Trilha de Teste) não é uma linha do catálogo' in a for a in av)
        and any('“Livro Três” está na lista da trilha, mas a linha não tem o marcador #trilha-teste' in a for a in av)
        and any('“Livro Dois” tem o marcador, mas não está na lista da trilha #trilha-teste' in a for a in av), 'lista e marcadores que não batem: um aviso para cada diferença')
r, av = trilhas('## 1. Sem Marcador\n\nDescrição.\n\n1. Livro Três | Caio\n', LT)
confere(r == [] and len(av) == 2 and 'a trilha “Sem Marcador” está sem marcador' in av[0] and 'o marcador #trilha-teste não corresponde a nenhuma trilha' in av[1], 'trilha sem marcador não entra, com aviso; marcador de uma trilha que não está no arquivo, também')
confere(bc.ler_trilhas(LT[2:], [], tmp / 'nao-existe.md') == [], 'sem o arquivo das trilhas, o painel fica sem trilhas (e sem erro)')
# um livro da seção 17 numa trilha: o marcador vem do inventário, como o resto da classificação dele
inv = imp.ler_inventario(imp.INVENTARIO)
for r in inv:
    if r['arquivo'] == 'Poemas Novos - Fulano de Tal.epub': r['marcadores'] = 'BR d1 e1 trilha-teste'
(tmp / 'inventario.tsv').write_text(imp.texto_inventario(inv), encoding='utf-8', newline='\n')
roda(); LV = livros()
r, av = trilhas('## 1. Trilha de Teste\n\n`#trilha-teste`\n\nDescrição.\n\n1. Poemas Novos | Fulano de Tal\n', LV)
confere(len(r) == 1 and [(LV[i]['t'], LV[i]['sec']) for i in r[0][3]] == [('Poemas Novos', 17)] and 'trilha-teste' in linha('Poemas Novos')['tags'] and not any('trilha-teste' in a or 'Poemas Novos' in a for a in av),
        'livro da biblioteca virtual numa trilha: o marcador posto na coluna `marcadores` do inventário chega à linha, e a trilha o encontra')

# 11 ▸ a classificação de antes da vistoria (catalogo/antes-da-vistoria.tsv): a base de quem já tinha livros editados no painel
av = []; ca = bc.classe_anterior(dados, av)
n = sum(1 for r in csv.DictReader(io.StringIO(bc.ANTES.read_text(encoding='utf-8-sig'), newline=''), delimiter='\t') if (r.get('titulo') or '').strip())
confere(n > 200 and len(ca) == n and not av and ca == json.loads(bc.DEST_ANTES.read_text(encoding='utf-8')), f'cada linha do arquivo ({n}) é achada no catálogo de hoje, sem avisos, e src/antes.json está em dia' + (': ' + ' | '.join(av[:3]) if av else ''))
situacao = {'tenho-fisico', 'tenho-digital', 'ja-tenho', 'lido'}
confere([x[0] for x in ca] == sorted({x[0] for x in ca}) and all(1 <= e <= 16 and '#' not in m and not situacao & set(m.split()) for _, e, m in ca), 'uma entrada por linha, com eixo de 1 a 16 e só marcadores de classificação (sem posse nem leitura)')
confere(all(e != dados[i][4] or not set(m.split()) <= set(dados[i][2].split()) for i, e, m in ca), 'só estão ali as linhas em que a vistoria trocou ou tirou alguma coisa (onde ela só acrescentou, o painel não precisa de base)')

def antes_tsv(*linhas_tsv):
    (tmp / 'antes.tsv').write_text('titulo\tautor\teixo\tmarcadores\n' + ''.join(l + '\n' for l in linhas_tsv), encoding='utf-8', newline='\n'); av = []
    return bc.classe_anterior([['Livro Novo', 'Autora', 'F d1', 1, 2, ''], ['Outro', '', 'NF', 17, 9, '', None, [['Outro Velho', '']]]], av, tmp / 'antes.tsv'), av
confere(antes_tsv('Livro Novo\tAutora\t3\t#NF #d2  historia') == ([[0, 3, 'NF d2 historia']], []), 'linha achada pelo título e autor: posição, eixo e marcadores de antes')
confere(antes_tsv('Outro Velho\t\t12\tNF') == ([[1, 12, 'NF']], []), 'linha que mudou de nome depois da vistoria é achada pelo nome antigo')
r, av = antes_tsv('Sumiu\tAlguém\t3\tF')
confere(r == [] and len(av) == 1 and '“Sumiu” (Alguém) não é mais uma linha do catálogo' in av[0], 'livro que saiu do catálogo: ignorado, com aviso')
r, av = antes_tsv('Livro Novo\tAutora\t0\tF', 'Outro\t\tdezessete\tNF')
confere(r == [] and len(av) == 2 and all('esperado: 1 a 16' in a for a in av), 'eixo que não vai de 1 a 16: ignorado, com aviso')
confere(antes_tsv('Livro Novo\tAutora\t3\tF', 'Livro Novo\tAutora\t5\tNF') == ([[0, 3, 'F']], []), 'linha repetida: vale a primeira')
confere(bc.classe_anterior(dados, [], tmp / 'nao-existe.tsv') == [], 'sem o arquivo, nenhuma base antiga (e sem erro)')

# 12 ▸ o painel pronto leva o que está em src/: quem muda o catálogo e não refaz o HTML é avisado aqui
html = (QA.parent.parent / 'Biblioteca_Lucas_Dashboard.html').read_text(encoding='utf-8')
def embutido(nome):
    m = re.search(r'^const %s = (.*);$' % nome, html, re.M)
    return json.loads(m.group(1)) if m else None
confere(embutido('CATALOGO') == dados and embutido('TRILHAS_DADOS') == tr and embutido('CLASSE_ANTES') == ca,
        'Biblioteca_Lucas_Dashboard.html leva o catálogo, as trilhas e a classificação de antes que estão em src/ (se falhar: python tools/atualizar.py)')

# 13 ▸ a medição dos filtros (tools/analisar_marcadores.py): de onde saem os números de catalogo/ANALISE-DOS-FILTROS.md
import analisar_marcadores as am
LA = am.carregar(); GA = am.grupos_do_painel(LA); medida = am.medir()
confere(len(LA) == len(dados) and f'CATÁLOGO: {len(LA)} linhas' in medida and all(k in medida for k in ('COBERTURA', 'ESPECÍFICO × GERAL', 'EIXOS', 'DIFICULDADE E EXTENSÃO', 'PASTA DO DONO')),
        'analisar_marcadores.py mede o catálogo inteiro: alcance dos filtros, eixos, dificuldade e extensão, pastas × eixos')
confere(len(GA['Gêneros']) > 20 and len(GA['Temas']) > 40 and len(GA[am.GRUPO_PSI]) == 10 and len(GA['Trilhas de leitura']) == len(tr) and all(1 <= b['eixo'] <= 16 and b['d'] and b['e'] and b['tipo'] for b in LA),
        'os grupos medidos são os do painel, e toda linha do catálogo tem tipo, eixo, dificuldade e extensão')
usados = {t for b in LA for t in b['tags']}
sem_uso = [t for g in ('Gêneros', 'Temas', am.GRUPO_PSI, 'Época e origem', 'Afinidades') for t in GA[g] if t not in usados]
confere(not sem_uso, 'todo marcador que o painel oferece nos filtros está em uso em algum livro' + (': ' + ', '.join(sem_uso[:5]) if sem_uso else ''))
nos_grupos = [t for itens in GA.values() for t in itens]; repetidos = sorted({t for t in nos_grupos if nos_grupos.count(t) > 1})
confere(not repetidos, 'cada marcador mora num grupo de filtros só (é o grupo que diz se dois marcadores somam ou cruzam)' + (': ' + ', '.join(repetidos[:5]) if repetidos else ''))

shutil.rmtree(tmp, ignore_errors=True)
print('ERROS:', len(erros))
for e in erros: print('  ', e)
sys.exit(1 if erros else 0)
