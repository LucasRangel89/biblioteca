#!/usr/bin/env python3
"""Deriva os marcadores de trilha no Catálogo Mestre gerado, sem alterar o inventário.

A lista ordenada em catalogo/trilhas.md é a fonte de verdade. Todas as referências são
validadas por título e autor antes de gerar qualquer alteração; o importador aplica o
resultado ao catálogo que ele próprio gera. Tags que não são de trilha são preservadas.
"""
import collections
import pathlib
import re
import unicodedata

RAIZ = pathlib.Path(__file__).resolve().parent.parent
TRILHAS = RAIZ / 'catalogo' / 'trilhas.md'


def chave(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s.strip()) if not '\u0300' <= c <= '\u036f').lower()


def autor(s):
    # Mesmas equivalências explícitas usadas na apresentação pelo build_catalog.
    aliases = {
        'liev tolstoi (na prateleira consta dostoievski; autor correto: tolstoi)': 'liev tolstoi',
        'irvin d. yalom (conforme a prateleira)': 'irvin d. yalom',
        '(tradicao hindu)': 'tradicao hindu', '(tradicao budista)': 'tradicao budista',
        '(tradicao tibetana)': 'tradicao tibetana', '(autor nao informado)': '',
    }
    s = chave(s)
    return aliases.get(s, s)


def sincronizar(md, texto):
    """Retorna (catálogo sincronizado, mudanças); levanta ValueError antes de gravar."""
    linhas = md.split('\n')
    livros, sec = collections.defaultdict(list), None
    for i, linha in enumerate(linhas):
        m = re.match(r'^##\s+(\d+)\.\s', linha)
        if m:
            sec = int(m.group(1))
        elif linha.startswith('## '):
            sec = None
        elif sec is not None and linha.startswith('|'):
            c = [x.strip() for x in linha.strip().strip('|').split('|')]
            if len(c) == 3 and c[0] not in ('Título', '---') and set(c[0]) != {'-'}:
                livros[(chave(c[0]), autor(c[1]))].append((i, c))
    desejadas, vistos, trilha, itens = collections.defaultdict(set), set(), None, set()
    em_secao = False
    for linha in texto.splitlines():
        if re.match(r'^##\s+\d+\.\s+', linha):
            if em_secao and (not trilha or not itens):
                raise ValueError('trilha sem marcador ou sem itens')
            em_secao, trilha, itens = True, None, set()
        m = re.match(r'^`#(trilha-[a-z0-9-]+)`\s*$', linha)
        if m:
            if not em_secao or trilha:
                raise ValueError('marcador fora de trilha ou múltiplos marcadores na mesma trilha')
            trilha = m.group(1)
            if trilha in vistos:
                raise ValueError(f'marcador repetido: #{trilha}')
            vistos.add(trilha)
        m = re.match(r'^\d+\.\s+(.+?)\s+\|\s+(.+?)\s*$', linha)
        if m:
            if not trilha:
                raise ValueError(f'item sem marcador de trilha: {linha}')
            k = (chave(m.group(1)), autor(m.group(2)))
            candidatos = livros.get(k, [])
            if len(candidatos) != 1:
                raise ValueError(f'item sem correspondência única no catálogo: {linha} ({len(candidatos)} encontrados)')
            if k in itens:
                raise ValueError(f'item repetido em #{trilha}: {linha}')
            itens.add(k)
            desejadas[candidatos[0][0]].add(trilha)
    if not vistos:
        raise ValueError('nenhuma trilha encontrada')
    if em_secao and (not trilha or not itens):
        raise ValueError('trilha sem marcador ou sem itens')
    mudancas = []
    for registros in livros.values():
        for i, c in registros:
            antigas = [t.lstrip('#') for t in c[2].split() if t.startswith('#')]
            novas = [t for t in antigas if not t.startswith('trilha-')] + sorted(desejadas[i])
            if antigas != novas:
                mudancas.append((c[0], c[1], sorted(set(novas) - set(antigas)), sorted(set(antigas) - set(novas))))
                linhas[i] = '| ' + ' | '.join((c[0], c[1], ' '.join('#' + t for t in novas))) + ' |'
    return '\n'.join(linhas), mudancas
