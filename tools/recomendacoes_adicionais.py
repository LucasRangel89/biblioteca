"""Acrescenta ao catálogo gerado recomendações declaradas em TSV, sem editar o catálogo à mão."""
import csv
import pathlib
import re
from parse_catalog import parse
from sincronizar_trilhas import chave, autor

FONTE = pathlib.Path(__file__).resolve().parent.parent / 'catalogo' / 'recomendacoes-adicionais.tsv'


def incluir(md, caminho=FONTE):
    if not pathlib.Path(caminho).exists():
        return md
    with open(caminho, encoding='utf-8', newline='') as f:
        rows = list(csv.DictReader(f, delimiter='\t'))
    linhas = md.split('\n')
    existentes = {(chave(b['t']), autor(b['a'])) for b in parse(md)}
    for r in rows:
        t, a, sec, tags = (r.get(k, '').strip() for k in ('titulo', 'autor', 'secao', 'tags'))
        if not t or not a or '|' in t or '|' in a or not re.fullmatch(r'[1-9]|1[0-6]', sec) or not re.fullmatch(r'[A-Za-z0-9-]+(?: [A-Za-z0-9-]+)*', tags):
            raise ValueError(f'recomendação adicional inválida: {r}')
        k = (chave(t), autor(a))
        if k in existentes:
            continue
        ini = next((i for i, l in enumerate(linhas) if re.match(r'^##\s+' + sec + r'\.\s', l)), None)
        if ini is None:
            raise ValueError(f'seção {sec} não encontrada para {t}')
        fim = next((i for i in range(ini + 1, len(linhas)) if linhas[i].startswith('## ')), len(linhas))
        pos = [i for i in range(ini + 1, fim) if linhas[i].startswith('|') and len(linhas[i].strip().strip('|').split('|')) == 3]
        if not pos:
            raise ValueError(f'seção {sec} não tem tabela para {t}')
        linhas.insert(pos[-1] + 1, '| ' + ' | '.join((t, a, ' '.join('#' + tag for tag in tags.split()))) + ' |')
        existentes.add(k)
    return '\n'.join(linhas)
