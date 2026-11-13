"""Roda toda a verificação do painel e diz, no fim, se passou.

Uso:  python tools/qa/tudo.py                          (todos os testes, ~25 min)
      python tools/qa/tudo.py foco a11y                (só os citados)
      python tools/qa/tudo.py importador busca_capas   (só os citados, sem navegador)
Requisitos (uma vez): pip install playwright pillow  &&  python -m playwright install chromium

Um teste passa quando termina sem erro e a linha de resumo dele não acusa nada. Três testes (`posse`, `inicio` e
`vistoria`) tiram painéis antigos do histórico do Git; numa cópia do repositório sem o histórico inteiro eles pulam
essas partes.
Isso não é falha, mas também não é o teste completo: a linha do teste ganha "[partes puladas: N]" e o fim avisa.
"""
import os, re, subprocess, sys, time
from caminhos import QA, TMP

TESTES = ['importador', 'gerar_listagens', 'busca_capas', 'auditoria_capas', 'fluxo_capas', 'capa_digital', 'fluxo_ci', 'medir3', 'limpo', 'inicio', 'posse', 'opcionais', 'leitura_de_fora', 'anotacoes', 'trilhas', 'filtros', 'ocultar', 'listas', 'sinopses', 'temas', 'vistoria', 'capas_painel', 'financas', 'foco', 'janela_baixa', 'func3', 'func4', 'func5', 'func6', 'func7', 'func8', 'sandbox', 'site', 'run7', 'run9', 'valores', 'resto', 'a11y', 'varredura']
RUIM = re.compile(r'ERROS: [1-9]|erros: [1-9]|FALHAS: \[[^\]]|AVISOS: [1-9]|PROBLEMAS: \{[^}]')
RESUMO = re.compile(r'^(ERROS|FALHAS|AVISOS|PROBLEMAS)\b|erros:')
PULADO = re.compile(r'^\s*\(pulado:', re.M)              # como os testes anunciam uma parte que não puderam fazer

pedidos = sys.argv[1:] or TESTES
desconhecidos = [n for n in pedidos if not (QA / f'{n}.py').exists()]
if desconhecidos: sys.exit(f'Teste que não existe: {", ".join(desconhecidos)}. Os que existem: {", ".join(TESTES)}')
texto = lambda x: x.decode('utf-8', 'replace') if isinstance(x, bytes) else (x or '')
amb = dict(os.environ, PYTHONUTF8='1', PYTHONIOENCODING='utf-8')
falhas = []; puladas = {}
for nome in pedidos:
    inicio = time.time()
    try:
        r = subprocess.run([sys.executable, str(QA / f'{nome}.py')], cwd=str(QA), env=amb, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=900)
        saida, codigo = r.stdout + r.stderr, r.returncode
    except subprocess.TimeoutExpired as e:
        saida, codigo = texto(e.stdout) + texto(e.stderr) + '\n[tempo esgotado]', 124
    (TMP / f'log-{nome}.txt').write_text(saida, encoding='utf-8')
    resumo = ' '.join(l.strip() for l in saida.splitlines() if RESUMO.search(l))
    ok = codigo == 0 and bool(resumo) and not RUIM.search(resumo)
    if not ok: falhas.append(nome)
    n = len(PULADO.findall(saida))
    if n: puladas[nome] = n
    print(f'{"ok   " if ok else "FALHA"} {nome:12} {time.time() - inicio:4.0f}s  {resumo[:150]}{f"  [partes puladas: {n}]" if n else ""}', flush=True)
print()
print('TUDO CERTO' if not falhas else f'HÁ FALHAS: {", ".join(falhas)}')
if puladas:
    print(f'ATENÇÃO — partes puladas em: {", ".join(f"{k} ({v})" for k, v in puladas.items())}. Esses testes não rodaram por inteiro:')
    print('  eles tiram painéis antigos do histórico do Git, e esta cópia do repositório não tem o histórico todo.')
    print('  Para completar: git fetch --unshallow   (e rode de novo os testes citados; o motivo de cada parte está no registro)')
print(f'Registros e capturas em: {TMP}')
sys.exit(1 if falhas else 0)
