"""A amostragem da biblioteca virtual (etapa 4 — `catalogo/AMOSTRAGEM.md`).

O arquivo é a tabela de 40 livros sorteados que o dono responde para medir o erro da classificação dos 1.910
digitais (tema, dificuldade, tamanho). Ele é gerado por `tools/amostragem.py` e não deve ser editado à mão.

Confere que:
  · a tabela tem as 40 linhas, sem livro repetido, todas da seção 17;
  · o que a tabela diz de cada livro é exatamente o que está gravado no catálogo hoje (tema, dificuldade, tamanho);
  · todo arquivo citado na tabela existe no inventário — o dono nunca é mandado abrir um nome que não existe;
  · o gerador reproduz o arquivo (mesma semente) e o rodapé diz o total certo de digitais.
"""
import collections, re, sys

from caminhos import RAIZ

sys.path.insert(0, str(RAIZ / 'tools'))
import parse_catalog
import importar_digital as ID
import amostragem as AM

falhas = []


def ok(nome, cond, extra=''):
    print(('  ok   ' if cond else '  FALHA') + ' ' + nome + (' — ' + str(extra) if extra != '' else ''))
    if not cond:
        falhas.append(nome)


def rotulo_dos_marcadores(tags):
    dif = next((AM.DIF[t] for t in tags if t in AM.DIF), '—')
    ext = next((AM.EXT[t] for t in tags if t in AM.EXT), '—')
    return dif, ext


md = (RAIZ / 'catalogo' / 'AMOSTRAGEM.md').read_text(encoding='utf-8')
books = parse_catalog.parse(parse_catalog.SRC.read_text(encoding='utf-8'))
por_linha = {i: b for i, b in enumerate(books) if b['sec'] == AM.SECAO_DIGITAL}
nomes = AM.nomes_dos_eixos(books)
linhas_md = [l for l in md.splitlines() if re.match(r'^\| \d+ \| ', l)]
invent = [r['arquivo'] for r in ID.ler_inventario(ID.INVENTARIO)]
arquivos_existentes = collections.Counter(invent)

print('A. O arquivo catalogo/AMOSTRAGEM.md')
ok('tem 40 linhas de livro', len(linhas_md) == AM.TAMANHO, len(linhas_md))
ok('o rodapé diz o total de digitais de hoje', f'{len(por_linha):,}'.replace(',', '.') in md, len(por_linha))

print('B. Cada linha confere com o catálogo')
vistos = []
ruim_tema = ruim_rotulo = fora = 0
for l in linhas_md:
    celulas = [c.strip() for c in l.strip().strip('|').split('|')]
    n, livro, arquivo, tema, dif, ext = celulas
    m = re.match(r'“(.+)” \((.+?)\)', livro)
    achadas = [i for i, b in por_linha.items() if m and b['t'] == m.group(1)]
    if not achadas:
        fora += 1
        continue
    b = books[achadas[0]]
    vistos.append(achadas[0])
    if nomes.get(b['sub'], 'sem tema') != tema:
        ruim_tema += 1
    d, e = rotulo_dos_marcadores(b['tags'])
    if (d, e) != (dif, ext):
        ruim_rotulo += 1
ok('toda linha é de um livro da seção 17', fora == 0 and len(vistos) == len(linhas_md), fora)
ok('nenhum livro aparece duas vezes', len(set(vistos)) == len(vistos), collections.Counter(vistos).most_common(1))
ok('o tema gravado na tabela é o do catálogo', ruim_tema == 0, ruim_tema)
ok('dificuldade e tamanho da tabela são os dos marcadores', ruim_rotulo == 0, ruim_rotulo)
nomes_na_tabela = re.findall(r'`[^`*/\\]+/([^`/\\]+)`', '\n'.join(linhas_md))
faltando = [a for a in nomes_na_tabela if a not in arquivos_existentes]
ok('todo arquivo citado existe no inventário', not faltando, faltando[:3])

print('C. O gerador')
novo = AM.texto()
ok('rodar de novo com a mesma semente reproduz o arquivo', novo == md)
ok('a tabela sorteada tem 40 livros diferentes da seção 17',
   len(set(AM.tabela(AM.SEMENTE, AM.TAMANHO)[0])) == AM.TAMANHO)

print('FALHAS:', falhas)
