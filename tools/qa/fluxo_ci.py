"""O CI rápido e a publicação condicionada, lidos como arquivo.

Não executa o GitHub Actions nem substitui a validação do YAML. Confere o desenho:
  · PRs e ramos de trabalho passam pelo nível rápido, sem permissão de escrita;
  · a conferência exige geração em dia, sintaxe JavaScript e os sete testes sem navegador;
  · a publicação depende dessa conferência, mas usa o HTML já commitado;
  · só o job de publicação recebe permissão para publicar;
  · runner.temp fica no passo, não no env do job (o GitHub rejeita o arquivo inteiro).
A leitura dos blocos preserva linhas em branco; não precisa instalar um leitor de YAML.
"""
import ast, pathlib, re, sys

QA = pathlib.Path(__file__).resolve().parent
RAIZ = QA.parent.parent
RAPIDOS = ('importador', 'gerar_listagens', 'busca_capas', 'auditoria_capas', 'fluxo_capas', 'capa_digital', 'fluxo_ci')
COMANDO = 'python3 tools/qa/tudo.py ' + ' '.join(RAPIDOS)
SINTAXE_JS = 'for f in src/js/*.js; do node --check "$f"; done'
erros = []


def confere(cond, msg, extra=''):
    print(('ok    ' if cond else 'FALHOU'), msg + (f' — {extra}' if extra != '' and not cond else ''))
    if not cond: erros.append(msg)


def sem_comentarios(texto):
    return '\n'.join(l for l in texto.splitlines() if not l.lstrip().startswith('#'))


def job(texto, nome):
    """O bloco de um job: termina na próxima chave fora da indentação de quatro espaços."""
    inicio = re.search(rf'^  {re.escape(nome)}:[^\n]*\n', texto, flags=re.M)
    if not inicio: return ''
    linhas = []
    for linha in texto[inicio.end():].splitlines(keepends=True):
        if linha.strip() and not linha.startswith('    '): break
        linhas.append(linha)
    return ''.join(linhas)


def runner_fora_do_env_do_job(texto):
    return not re.search(r'^    env:\n(?:      [^\n]*\n)*?      BIBLIOTECA_QA_TMP:.*runner\.', texto, flags=re.M)


ci = sem_comentarios((RAIZ / '.github' / 'workflows' / 'verificar.yml').read_text(encoding='utf-8'))
site = sem_comentarios((RAIZ / '.github' / 'workflows' / 'publicar-site.yml').read_text(encoding='utf-8'))
antes_ci, antes_site = ci.split('\njobs:', 1)[0], site.split('\njobs:', 1)[0]
rapido, conferir, publicar = job(ci, 'rapido'), job(site, 'conferir'), job(site, 'publicar')

print('CI RÁPIDO')
confere('name: Verificar' in antes_ci, 'existe um workflow de verificação')
confere(re.search(r'^  pull_request:', antes_ci, flags=re.M) is not None, 'roda em pull_request')
confere(re.search(r'^  push:\n    branches-ignore: \[main\]', antes_ci, flags=re.M) is not None,
        'roda nos ramos de trabalho, sem duplicar a publicação de main')
confere(re.search(r'^permissions:\n  contents: read\s*$', antes_ci, flags=re.M) is not None
        and not re.search(r': write\b', ci), 'o CI só lê o repositório; não publica nem mexe em PR')
confere(bool(rapido) and 'timeout-minutes: 15' in rapido, 'a conferência tem prazo de 15 minutos')
confere('actions/deploy-pages' not in ci and 'actions/upload-pages-artifact' not in ci, 'o CI não publica o site')
for nome, bloco in (('CI', rapido), ('site', conferir)):
    artigo = 'o' if nome == 'CI' else 'a conferência do'
    confere(re.search(r'python3 tools/atualizar\.py\n\s*git diff --exit-code', bloco) is not None,
            f'{artigo} {nome} exige que o HTML e os JSON gerados estejam em dia')
    confere(SINTAXE_JS in bloco, f'{artigo} {nome} confere a sintaxe dos módulos JavaScript')
    confere(COMANDO in bloco, f'{artigo} {nome} roda os sete testes rápidos, incluindo este desenho')
    confere(runner_fora_do_env_do_job(bloco), f'no {nome}, runner.temp fica no passo, não no env do job')

print('PUBLICAÇÃO CONDICIONADA')
confere(re.search(r'^  push:\n    branches: \[main\]', antes_site, flags=re.M) is not None
        and re.search(r'^  (pull_request|schedule):', antes_site, flags=re.M) is None
        and bool(conferir) and bool(publicar)
        and all("if: github.ref == 'refs/heads/main'" in b for b in (conferir, publicar)),
        'o site publica só a partir de main, inclusive quando o pedido é manual')
confere(bool(publicar) and re.search(r'^    needs: conferir\s*$', publicar, flags=re.M) is not None,
        'o job publicar depende do job conferir')
confere(re.search(r'^    permissions:\n      contents: read[^\n]*\n    steps:', conferir, flags=re.M) is not None
        and not re.search(r': write\b', conferir), 'a conferência antes do site também só lê o repositório')
confere(re.search(r'^permissions:\n  contents: read(?:[ \t]+#[^\n]*)?\n', antes_site, flags=re.M) is not None
        and re.search(r'^    permissions:\n      contents: read[^\n]*\n      pages: write[^\n]*\n      id-token: write[^\n]*\n', publicar, flags=re.M) is not None,
        'só o job de publicação recebe as permissões do GitHub Pages')
confere('cp Biblioteca_Lucas_Dashboard.html _site/index.html' in publicar
        and 'actions/deploy-pages@' in publicar and 'tools/atualizar.py' not in publicar,
        'publica o HTML versionado, não um artefato gerado na publicação')
confere(not any(cmd in ci + site for cmd in ('gh pr merge', 'gh pr close', 'git push')),
        'nenhum dos dois fluxos grava num ramo, mescla ou fecha PR')

print('COMANDOS CITADOS')
confere((RAIZ / 'tools' / 'atualizar.py').is_file() and all((QA / f'{t}.py').is_file() for t in RAPIDOS),
        'o gerador do painel e os sete scripts de teste existem')
arvore = ast.parse((QA / 'tudo.py').read_text(encoding='utf-8'))
cadastrados = next((ast.literal_eval(n.value) for n in arvore.body if isinstance(n, ast.Assign)
                    and any(isinstance(x, ast.Name) and x.id == 'TESTES' for x in n.targets)), [])
confere('fluxo_ci' in cadastrados and all(t in cadastrados for t in RAPIDOS),
        'a suíte completa também inclui o desenho do CI')

print('ERROS:', len(erros))
for e in erros: print('  ', e)
sys.exit(1 if erros else 0)
