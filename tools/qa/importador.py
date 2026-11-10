"""O importador da biblioteca virtual (tools/importar_digital.py), numa cópia temporária dos dados:
repetir não muda nada; arquivo novo, arquivo ausente, marcador posto à mão, correção no inventário e --conferir.
Não precisa de navegador."""
import contextlib, io, pathlib, shutil, sys, tempfile

QA = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(QA.parent))
import importar_digital as imp
from parse_catalog import parse

erros = []
def confere(cond, msg):
    print(('ok    ' if cond else 'FALHOU'), msg)
    if not cond: erros.append(msg)

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

shutil.rmtree(tmp, ignore_errors=True)
print('ERROS:', len(erros))
for e in erros: print('  ', e)
sys.exit(1 if erros else 0)
