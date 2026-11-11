#!/usr/bin/env python3
"""Mede os filtros e a categorização do catálogo: é de onde saem os números de catalogo/ANALISE-DOS-FILTROS.md.

    python tools/analisar_marcadores.py

Não grava nada. Lê o Catálogo Mestre, src/catalog.json (o eixo de cada linha), o inventário da biblioteca virtual (a
pasta de cada arquivo) e os grupos de marcadores do painel (src/js/10-data.js). Rode depois de `tools/atualizar.py`.
"""
import collections, csv, io, itertools, json, pathlib, re, sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from parse_catalog import parse, SRC                                   # noqa: E402

EIXOS = [None, 'Pré-história e origens', 'Ficção científica e fantasia', 'Clássicos universais', 'Brasil, América Latina e lusofonia',
         'Ficção contemporânea', 'Romances históricos', 'Horror, weird e mistério', 'Poesia e cartas', 'Filosofia e ética', 'Mente e neurociência',
         'Política e economia', 'Sociedade e história', 'Ciência e tecnologia', 'Psicologia e psicanálise', 'Espiritualidade', 'Artes, escrita e parentalidade']
CAMADAS = (('q', 'Perguntas centrais'), ('clima', 'Clima da leitura'), ('papel', 'Papel na biblioteca'), ('ponte', 'Pontes entre áreas'), ('cenario', 'Cenários'), ('trilha', 'Trilhas de leitura'))
# marcador mais específico → marcador mais geral que ele deveria (ou poderia) trazer junto
PAI_E_FILHO = [('thriller-medico', 'thriller'), ('roma', 'antiguidade'), ('regional-gaucho', 'RS'), ('RS', 'BR'), ('lovecraftiano', 'horror'), ('neandertal', 'pre-historia'),
               ('fisica', 'ciencia'), ('biologia', 'ciencia'), ('programacao', 'tecnologia'), ('ia', 'tecnologia'), ('tcc', 'psicologia'), ('psicologia-social', 'psicologia'),
               ('psicopatologia', 'psicologia'), ('psicanalise', 'psicologia'), ('psiquiatria', 'medicina'), ('existencialismo', 'filosofia'), ('etica', 'filosofia'),
               ('espiritismo', 'espiritualidade'), ('umbanda', 'espiritualidade'), ('mistica', 'espiritualidade'), ('geopolitica', 'politica'), ('autoritarismo', 'politica'),
               ('policial', 'misterio'), ('medieval', 'romance-historico'), ('distopia', 'ficcao-cientifica')]
MESMO_NOME = [('filosofia', 9), ('psicologia', 14), ('politica', 11), ('ciencia', 13), ('historia', 12), ('espiritualidade', 15), ('horror', 7), ('romance-historico', 6)]


def carregar():
    """As linhas do catálogo, cada uma com eixo, grupo (estante, recs, virtual), posse, tipo, dificuldade e extensão."""
    livros = parse(pathlib.Path(SRC).read_text(encoding='utf-8'))
    eixos = [r[4] for r in json.loads((RAIZ / 'src' / 'catalog.json').read_text(encoding='utf-8'))]
    assert len(eixos) == len(livros), 'src/catalog.json não acompanha o catálogo: rode tools/atualizar.py'
    for b, e in zip(livros, eixos):
        T = b['T'] = set(b['tags'])
        b['eixo'] = e
        b['g'] = 'estante' if b['sec'] == 0 else 'recs' if b['sec'] < 17 else 'virtual'
        b['tenho'] = bool(T & {'tenho-fisico', 'tenho-digital'})
        b['tipo'] = next((t for t in ('F', 'NF', 'poesia', 'HQ', 'antologia') if t in T), '')
        b['d'] = next((int(t[1]) for t in ('d1', 'd2', 'd3') if t in T), 0)
        b['e'] = next((int(t[1]) for t in ('e1', 'e2', 'e3') if t in T), 0)
    return livros


GRUPO_PSI = 'Psicologia: abordagens e áreas'      # as dez portas da psicologia: eram temas até a rodada 8 e continuam contando como tema nas medidas


def grupos_do_painel(livros):
    """{nome do grupo de filtros: [marcadores]}, como no painel (GRUPOS_TAG, em src/js/10-data.js), mais as camadas."""
    js = (RAIZ / 'src' / 'js' / '10-data.js').read_text(encoding='utf-8')
    m = re.search(r'const GRUPOS_TAG = \[(.*?)\n\];', js, re.S)
    g = {nome: re.findall(r"'([^']+)'", itens) for nome, itens in re.findall(r"\['([^']+)', \[([^\]]*)\]\]", m.group(1))}
    for prefixo, nome in CAMADAS:
        g[nome] = sorted({t for b in livros for t in b['T'] if t.startswith(prefixo + '-')})
    return g


def pct(n, total):
    return 100 * n / total if total else 0.0


def medir():
    L = livros = carregar()
    G = grupos_do_painel(livros)
    N = len(L)
    cont = collections.Counter(t for b in L for t in b['T'])
    com = {t: {i for i, b in enumerate(L) if t in b['T']} for t in cont}
    sub = lambda g: [b for b in L if b['g'] == g]
    out = []
    p = out.append

    p(f'CATÁLOGO: {N} linhas — estante {len(sub("estante"))} · recomendações (seções 1 a 16) {len(sub("recs"))} · biblioteca virtual (seção 17) {len(sub("virtual"))}')
    p(f'  tenho {sum(b["tenho"] for b in L)} · não tenho {sum(not b["tenho"] for b in L)} · marcadores diferentes em uso: {len(cont)}')

    p('\nCOBERTURA — livros com pelo menos um marcador do grupo: valores | total | estante | recomendações | virtual | pares do grupo sem nenhum livro')
    for nome, itens in G.items():
        S, usados = set(itens), [t for t in itens if cont[t]]
        c = lambda bs: pct(sum(1 for b in bs if b['T'] & S), len(bs))
        pares = list(itertools.combinations(usados, 2))
        vazios = sum(1 for a, b in pares if not (com[a] & com[b]))
        p(f'  {nome:30} {len(itens):3} | {c(L):5.1f}% | {c(sub("estante")):5.1f}% | {c(sub("recs")):5.1f}% | {c(sub("virtual")):5.1f}% | {pct(vazios, len(pares)):3.0f}% de {len(pares)}')
    descr = set(G['Gêneros']) | set(G['Temas']) | set(G[GRUPO_PSI])
    semnada = [b for b in L if not (b['T'] & descr)]
    p(f'  sem gênero nem tema: {len(semnada)} linhas — ' + ', '.join(f'{k or "sem tipo"} {v}' for k, v in collections.Counter(b['tipo'] for b in semnada).most_common()))
    for g in ('estante', 'recs', 'virtual'):
        p(f'  gêneros + temas por livro ({g}): média {sum(len(b["T"] & descr) for b in sub(g)) / len(sub(g)):.2f}')

    todos = [t for nome in ('Gêneros', 'Temas', GRUPO_PSI, 'Época e origem', 'Afinidades') for t in G[nome]]
    p('\nMARCADORES RAROS (menos de 10 livros): ' + ' · '.join(f'{t} {cont[t]}' for t in sorted(todos, key=lambda t: cont[t]) if cont[t] < 10))
    p(f'MARCADORES AMPLOS (mais de 8% do catálogo = {round(0.08 * N)} livros): ' + ' · '.join(f'{t} {cont[t]}' for t in sorted(todos, key=lambda t: -cont[t]) if cont[t] > 0.08 * N))
    fora = collections.Counter(t for b in L if b['g'] != 'virtual' for t in b['T'])
    dentro = collections.Counter(t for b in L if b['g'] == 'virtual' for t in b['T'])
    p('SÓ NA BIBLIOTECA VIRTUAL: ' + (' · '.join(f'{t} {dentro[t]}' for t in sorted(todos, key=lambda t: -dentro[t]) if dentro[t] and not fora[t]) or 'nenhum'))
    p('SÓ NAS SEÇÕES 0 A 16: ' + (' · '.join(f'{t} {fora[t]}' for t in sorted(todos, key=lambda t: -fora[t]) if fora[t] and not dentro[t]) or 'nenhum'))

    p('\nESPECÍFICO × GERAL — dos livros com o marcador específico, quantos têm também o geral')
    for filho, pai in PAI_E_FILHO:
        if cont[filho]:
            p(f'  {filho:18} → {pai:18} {len(com[filho] & com.get(pai, set())):4} de {cont[filho]:<4} ({pct(len(com[filho] & com.get(pai, set())), cont[filho]):3.0f}%)')
    p('\nMARCADOR × EIXO DE MESMO NOME — marcador | livros | dentro do eixo | livros do eixo sem o marcador')
    for tag, e in MESMO_NOME:
        no_eixo = [b for b in L if b['eixo'] == e]
        p(f'  {tag:18} {cont[tag]:4} | {pct(sum(1 for i in com[tag] if L[i]["eixo"] == e), cont[tag]):3.0f}% | eixo {e} ({EIXOS[e]}): {len(no_eixo)} livros, {sum(tag not in b["T"] for b in no_eixo)} sem o marcador')

    p('\nEIXOS — total | % do catálogo | tenho | não tenho')
    for e in range(1, 17):
        bs = [b for b in L if b['eixo'] == e]
        p(f'  {e:2} {EIXOS[e]:36} {len(bs):4} | {pct(len(bs), N):4.1f}% | {sum(b["tenho"] for b in bs):4} | {sum(not b["tenho"] for b in bs):3}')

    p('\nDIFICULDADE E EXTENSÃO')
    for g in ('estante', 'recs', 'virtual'):
        bs = sub(g)
        d, e = collections.Counter(b['d'] for b in bs), collections.Counter(b['e'] for b in bs)
        p(f'  {g:8} leve {pct(d[1], len(bs)):3.0f}% · média {pct(d[2], len(bs)):3.0f}% · exigente {pct(d[3], len(bs)):3.0f}% | curta {pct(e[1], len(bs)):3.0f}% · média {pct(e[2], len(bs)):3.0f}% · longa {pct(e[3], len(bs)):3.0f}%')
    de = collections.Counter((b['d'], b['e']) for b in L)
    for d in (1, 2, 3):
        p(f'  d{d}: ' + ' · '.join(f'e{e} {de[(d, e)]:4}' for e in (1, 2, 3)))

    inv = RAIZ / 'biblioteca-virtual' / 'inventario.tsv'
    if inv.exists():
        pastas = collections.defaultdict(collections.Counter)
        for r in csv.DictReader(io.StringIO(inv.read_text(encoding='utf-8-sig'), newline=''), delimiter='\t'):
            if r['tipo'] in ('livro', 'hq') and r['eixo'].isdigit() and 'ausente' not in r['obs']:
                pastas[r['pasta']][int(r['eixo'])] += 1
        total = sum(sum(c.values()) for c in pastas.values())
        principal = sum(c.most_common(1)[0][1] for c in pastas.values())
        p(f'\nPASTA DO DONO × EIXO DO CATÁLOGO: {len(pastas)} pastas, {total} arquivos; {principal} ({pct(principal, total):.0f}%) estão no eixo principal da sua pasta')
        for pasta, c in sorted(pastas.items(), key=lambda x: -sum(x[1].values())):
            n, (e1, n1) = sum(c.values()), c.most_common(1)[0]
            p(f'  {pasta[:44]:44} {n:4} arquivos | {pct(n1, n):3.0f}% no eixo {e1:2} ({EIXOS[e1]}) | espalhados por {len(c)} eixos')
    return '\n'.join(out)


def main():
    for saida in (sys.stdout, sys.stderr):
        try: saida.reconfigure(encoding='utf-8', errors='replace')
        except Exception: pass
    print(medir())
    return 0


if __name__ == '__main__':
    sys.exit(main())
