#!/usr/bin/env python3
"""Atualiza tudo de uma vez: biblioteca virtual → catálogo → painel.

    python tools/atualizar.py              importa a biblioteca virtual, refaz os dados e o painel
    python tools/atualizar.py --conferir   só mostra o que a importação mudaria; não grava nada

Passos (cada um também roda sozinho):
  1. importar_digital.py   listagens + inventário → Catálogo Mestre (seção 17 e marcadores #tenho-digital) e RESUMO.md
  2. build_catalog.py      Catálogo Mestre + inventário → src/catalog.json; catalogo/capas.tsv → src/capas.json
                           e src/capas-fontes.json; biblioteca-virtual/inventario.tsv → src/digitais.json (os nomes de
                           arquivo que o painel reconhece na varredura de pasta); catalogo/trilhas.md → src/trilhas.json;
                           catalogo/antes-da-vistoria.tsv → src/antes.json; catalogo/sinopses.tsv → src/sinopses.json
  3. build.py              src/ → Biblioteca_Lucas_Dashboard.html
"""
import pathlib, subprocess, sys

AQUI = pathlib.Path(__file__).resolve().parent


def rodar(script, *args):
    print(f'── {script} {" ".join(args)}'.rstrip(), flush=True)
    r = subprocess.run([sys.executable, '-B', str(AQUI / script), *args])
    if r.returncode:
        sys.exit(f'{script} falhou (código {r.returncode}); nada depois dele foi executado.')


if __name__ == '__main__':
    desconhecidos = [a for a in sys.argv[1:] if a != '--conferir']
    if desconhecidos:
        sys.exit(__doc__)
    if '--conferir' in sys.argv[1:]:
        rodar('importar_digital.py', '--conferir')
    else:
        rodar('importar_digital.py')
        rodar('build_catalog.py')
        rodar('build.py')
