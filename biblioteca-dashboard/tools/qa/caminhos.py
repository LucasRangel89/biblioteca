"""Caminhos dos testes. Nada aqui depende de onde o repositório está nem do sistema operacional.

PAINEL / PAINEL_URL  o HTML final (gerado por tools/build.py na raiz do repositório)
TMP                  pasta de trabalho dos testes (capturas em TMP/shots, arquivos baixados, registros);
                     fica na pasta temporária do sistema, ou onde a variável de ambiente BIBLIOTECA_QA_TMP mandar
"""
import os, pathlib, sys, tempfile

QA = pathlib.Path(__file__).resolve().parent
RAIZ = QA.parent.parent
PAINEL = RAIZ / 'Biblioteca_Lucas_Dashboard.html'
PAINEL_URL = PAINEL.as_uri()
TMP = pathlib.Path(os.environ.get('BIBLIOTECA_QA_TMP') or pathlib.Path(tempfile.gettempdir()) / 'biblioteca-qa').resolve()
(TMP / 'shots').mkdir(parents=True, exist_ok=True)

if not PAINEL.exists():
    sys.exit(f'Não encontrei {PAINEL}. Gere o painel antes: python tools/build.py')

# saída sempre em UTF-8 (o console do Windows usa outra codificação e quebraria nos acentos)
for _saida in (sys.stdout, sys.stderr):
    try: _saida.reconfigure(encoding='utf-8', errors='replace')
    except Exception: pass
