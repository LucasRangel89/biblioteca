#!/usr/bin/env python3
"""Relatório somente de leitura: posse, dificuldades, sinopses e volumes a conferir.

Uso: python tools/revisar_trilhas.py [--abaixo-posse 0.67]
Não reordena nem altera trilhas; os dados gerados precisam estar atualizados.
"""
import argparse
import json
import pathlib
import re

RAIZ = pathlib.Path(__file__).resolve().parent.parent


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--abaixo-posse', type=float, default=1.0,
                   help='mostrar trilhas com proporção de posse abaixo deste valor (padrão: 1)')
    args = p.parse_args()
    if not 0 <= args.abaixo_posse <= 1:
        p.error('--abaixo-posse deve estar entre 0 e 1')
    ler = lambda nome: json.loads((RAIZ / 'src' / nome).read_text(encoding='utf-8'))
    livros, trilhas = ler('catalog.json'), ler('trilhas.json')
    sinopses = {i for i, _ in ler('sinopses.json')}
    por_livro = {}
    for tag, nome, desc, ids in trilhas:
        for i in ids:
            por_livro.setdefault(i, set()).add(tag)
    print('Relatório de revisão — posse estimada pelos marcadores do catálogo gerado; não consulta o navegador.')
    for tag, nome, desc, ids in trilhas:
        tags = [set(livros[i][2].split()) for i in ids]
        tenho = sum(bool(t & {'tenho-fisico', 'tenho-digital'}) for t in tags)
        if not ids or tenho / len(ids) >= args.abaixo_posse:
            continue
        ds = [next((int(x[1:]) for x in t if x in {'d1', 'd2', 'd3'}), None) for t in tags]
        saltos = any(a is not None and b is not None and b < a for a, b in zip(ds, ds[1:]))
        repetidos = sum(len(por_livro[i]) > 1 for i in ids)
        sem_sinopse = sum(i not in sinopses for i in ids)
        verificar = sum('verificar' in t for t in tags)
        volumes = [livros[i][0] for i in ids if re.search(r'\bvol(?:ume)?\.?\s*\d', livros[i][0], re.I)]
        print(f'\n{nome} (#{tag}) — posse {tenho}/{len(ids)} · {repetidos} em outras trilhas · {sem_sinopse} sem sinopse · {verificar} a verificar')
        if saltos:
            print('  Dificuldade não monotônica (pode ser escolha curatorial).')
        if volumes:
            print('  Volumes para conferir sequência/edição: ' + '; '.join(volumes))
        faltam = [livros[i][0] for i, t in zip(ids, tags) if not t & {'tenho-fisico', 'tenho-digital'}]
        if faltam:
            print('  Sem posse no catálogo: ' + '; '.join(faltam))


if __name__ == '__main__':
    main()
