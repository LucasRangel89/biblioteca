"""O importador da biblioteca virtual (tools/importar_digital.py), numa cópia temporária dos dados:
repetir não muda nada; arquivo novo, arquivo ausente, marcador posto à mão, correção no inventário e --conferir.
E a conversão do catálogo para o painel (tools/build_catalog.py): src/catalog.json em dia; nomes antigos das linhas
corrigidas (catalogo/renomeados.tsv). Não precisa de navegador."""
import contextlib, io, json, pathlib, shutil, sys, tempfile

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

# 8 ▸ o que vai para o painel: src/catalog.json em dia, e o nome antigo das linhas corrigidas no catálogo
confere(json_em_dia and not avisos_json, 'src/catalog.json está em dia com o catálogo e o inventário, sem avisos' + (': ' + ' | '.join(avisos_json) if avisos_json else ''))
dados = json.loads(bc.DEST.read_text(encoding='utf-8'))
forma = all(len(r) in (6, 7, 8) and (len(r) < 7 or r[6] is None or len(r[6]) == 5) and (len(r) < 8 or (r[7] and all(len(n) == 2 for n in n8)))
            for r in dados for n8 in [r[7] if len(r) > 7 else []])
confere(forma and not any(len(r) == 7 and r[6] is None for r in dados), 'cada linha do JSON tem 6 campos, mais os dados digitais e os nomes antigos quando existem')
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

shutil.rmtree(tmp, ignore_errors=True)
print('ERROS:', len(erros))
for e in erros: print('  ', e)
sys.exit(1 if erros else 0)
