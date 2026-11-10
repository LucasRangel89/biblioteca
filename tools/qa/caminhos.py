"""Caminhos dos testes. Nada aqui depende de onde o repositório está nem do sistema operacional.

PAINEL               o HTML final (gerado por tools/build.py na raiz do repositório)
PAINEL_URL           o painel COM os dados de exemplo (endereço terminado em ?exemplo=1): é o que quase todos os testes
                     abrem, porque os números esperados neles saem dos dados simulados
PAINEL_LIMPO         o painel como o usuário o abre: sem exemplos, só o catálogo e o que for registrado
TMP                  pasta de trabalho dos testes (capturas em TMP/shots, arquivos baixados, registros);
                     fica na pasta temporária do sistema, ou onde a variável de ambiente BIBLIOTECA_QA_TMP mandar
"""
import os, pathlib, sys, tempfile

QA = pathlib.Path(__file__).resolve().parent
RAIZ = QA.parent.parent
PAINEL = RAIZ / 'Biblioteca_Lucas_Dashboard.html'
PAINEL_LIMPO = PAINEL.as_uri()
PAINEL_URL = PAINEL_LIMPO + '?exemplo=1'
TMP = pathlib.Path(os.environ.get('BIBLIOTECA_QA_TMP') or pathlib.Path(tempfile.gettempdir()) / 'biblioteca-qa').resolve()
(TMP / 'shots').mkdir(parents=True, exist_ok=True)

if not PAINEL.exists():
    sys.exit(f'Não encontrei {PAINEL}. Gere o painel antes: python tools/build.py')

# saída sempre em UTF-8 (o console do Windows usa outra codificação e quebraria nos acentos)
for _saida in (sys.stdout, sys.stderr):
    try: _saida.reconfigure(encoding='utf-8', errors='replace')
    except Exception: pass
