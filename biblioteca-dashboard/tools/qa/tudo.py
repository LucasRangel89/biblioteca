"""Roda toda a verificação do painel e diz, no fim, se passou.

Uso:  python tools/qa/tudo.py            (todos os testes, ~10 min)
      python tools/qa/tudo.py foco a11y  (só os citados)
Requisitos (uma vez): pip install playwright pillow  &&  python -m playwright install chromium
"""
import os, re, subprocess, sys, time
from caminhos import QA, TMP

TESTES = ['medir3', 'limpo', 'foco', 'func3', 'func4', 'func5', 'func6', 'func7', 'func8', 'sandbox', 'run7', 'run9', 'valores', 'resto', 'a11y', 'varredura']
RUIM = re.compile(r'ERROS: [1-9]|erros: [1-9]|FALHAS: \[[^\]]|AVISOS: [1-9]|PROBLEMAS: \{[^}]')
RESUMO = re.compile(r'^(ERROS|FALHAS|AVISOS|PROBLEMAS)\b|erros:')

pedidos = sys.argv[1:] or TESTES
amb = dict(os.environ, PYTHONUTF8='1', PYTHONIOENCODING='utf-8')
falhas = []
for nome in pedidos:
    inicio = time.time()
    try:
        r = subprocess.run([sys.executable, str(QA / f'{nome}.py')], cwd=str(QA), env=amb, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=900)
        saida, codigo = r.stdout + r.stderr, r.returncode
    except subprocess.TimeoutExpired as e:
        saida, codigo = (e.stdout or '') + '\n[tempo esgotado]', 124
    (TMP / f'log-{nome}.txt').write_text(saida, encoding='utf-8')
    resumo = ' '.join(l.strip() for l in saida.splitlines() if RESUMO.search(l))
    ok = codigo == 0 and bool(resumo) and not RUIM.search(resumo)
    if not ok: falhas.append(nome)
    print(f'{"ok   " if ok else "FALHA"} {nome:10} {time.time() - inicio:4.0f}s  {resumo[:150]}', flush=True)
print()
print('TUDO CERTO' if not falhas else f'HÁ FALHAS: {", ".join(falhas)}')
print(f'Registros e capturas em: {TMP}')
sys.exit(1 if falhas else 0)
