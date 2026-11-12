"""O robô das capas (.github/workflows/buscar-capas.yml): o desenho do fluxo, conferido no arquivo.

Não dá para rodar o GitHub Actions daqui. O que este teste garante é o que se pode conferir lendo o arquivo — e é
justamente onde um erro seria caro:
  · o robô só roda quando alguém manda (nada de gatilho por push ou por relógio);
  · ele NUNCA grava no ramo em que rodou: cria um ramo capas/… e abre um Pull Request para revisão;
  · a ordem é buscar → ver se mudou → conferir e amostrar → montar o painel → auditar → testar → abrir o PR;
  · os testes rodam antes do PR, e um teste falhando deixa o PR como rascunho (e a execução, vermelha);
  · nada de merge automático, em lugar nenhum;
  · o site continua sendo publicado só a partir de `main`, pelo outro serviço;
  · o tempo da busca cabe no tempo da execução, e uma busca por vez.
Também confere que os comandos citados no arquivo existem e aceitam as opções que ele passa.
A sintaxe do YAML foi conferida quando o arquivo foi escrito; aqui as checagens são sobre o texto.
"""
import pathlib, re, subprocess, sys

QA = pathlib.Path(__file__).resolve().parent
RAIZ = QA.parent.parent
sys.path.insert(0, str(QA.parent))
import capas as C

erros = []


def confere(cond, msg, extra=''):
    print(('ok    ' if cond else 'FALHOU'), msg + (f' — {extra}' if extra != '' and not cond else ''))
    if not cond: erros.append(msg)


ARQ = RAIZ / '.github' / 'workflows' / 'buscar-capas.yml'
SITE = RAIZ / '.github' / 'workflows' / 'publicar-site.yml'
txt = ARQ.read_text(encoding='utf-8')
sem_comentarios = '\n'.join(l for l in txt.splitlines() if not l.lstrip().startswith('#'))
passos = [(m.group(1), m.start()) for m in re.finditer(r'^      - name: (.+)$', txt, flags=re.M)]
nomes = [n for n, _ in passos]
corpo = {n: txt[i:(passos[k + 1][1] if k + 1 < len(passos) else len(txt))] for k, (n, i) in enumerate(passos)}

print('QUANDO O ROBÔ RODA')
confere('workflow_dispatch:' in sem_comentarios and not re.search(r'^\s{2}(push|schedule|pull_request):', sem_comentarios, flags=re.M),
        'só roda quando alguém manda: sem gatilho por push, por relógio ou por PR')
confere(re.search(r'concurrency:\s*\n\s*group: capas-', txt) is not None, 'uma busca por vez em cada ramo')
confere(re.search(r'timeout-minutes: (\d+)', txt) is not None and int(re.search(r'timeout-minutes: (\d+)', txt).group(1)) <= 360, 'a execução tem prazo (e cabe no limite do GitHub)')
busca_min = int(re.search(r'--minutos (\d+)', txt).group(1))
confere(busca_min + 45 < int(re.search(r'timeout-minutes: (\d+)', txt).group(1)), 'o tempo da busca deixa folga para montar o painel, testar e abrir o PR', busca_min)

print('O QUE ELE PODE FAZER')
confere(re.search(r'permissions:\s*\n\s*contents: write[^\n]*\n\s*pull-requests: write', txt) is not None, 'permissão para gravar um ramo e abrir PR — e nada mais')
confere('gh pr merge' not in txt and 'gh pr close' not in txt and '--auto' not in txt, 'em nenhum lugar há merge, fechamento de PR ou merge automático')
confere('git push origin "HEAD:$GITHUB_REF_NAME"' not in txt and 'git push origin "$GITHUB_REF_NAME"' not in txt, 'não grava no ramo em que rodou')
confere('RAMO="capas/' in txt and 'git switch -c "$RAMO"' in txt and 'git push origin "$RAMO"' in txt, 'cria um ramo capas/… e grava nele')
confere('gh pr create --base "$BASE" --head "$RAMO"' in txt and 'BASE: ${{ github.ref_name }}' in txt, 'abre o PR do ramo novo para o ramo em que a busca rodou')
confere('pull-requests: write' not in SITE.read_text(encoding='utf-8'), 'o serviço do site não ganhou poder de mexer em PR')

print('A ORDEM DOS PASSOS')
esperado = ['Baixar o repositório', 'Procurar as capas', 'Ver se há alguma mudança', 'Conferir o arquivo e as imagens (amostra)',
            'Montar o painel com as capas novas', 'Refazer a auditoria das capas', 'Preparar os testes', 'Rodar os testes', 'Abrir o Pull Request']
confere(nomes == esperado, 'buscar → ver se mudou → conferir e amostrar → montar → auditar → testar → abrir o PR', nomes)
confere(all("steps.mudou.outputs.mudou == 'sim'" in corpo[n] for n in nomes[3:]), 'sem mudança no capas.tsv, nada disso roda: nenhum PR vazio')
confere('git diff --quiet -- catalogo/capas.tsv' in corpo['Ver se há alguma mudança'], 'a decisão de abrir PR sai da diferença no capas.tsv')

print('O QUE CADA PASSO RODA')
confere('tools/capas.py --minutos' in corpo['Procurar as capas'] and '--refazer' in corpo['Procurar as capas'] and '--sem-google' in corpo['Procurar as capas'],
        'a busca aceita as três escolhas da tela: refazer, limite e ficar sem o Google')
confere("&& '' ||" not in txt, 'nenhuma escolha da tela usa "condição && \'\' || valor": no GitHub isso devolve o valor mesmo com a condição verdadeira (o certo é negar a condição)')
confere("${{ !inputs.google && '--sem-google' || '' }}" in txt and "${{ !inputs.suite_completa &&" in txt, 'as duas escolhas invertidas (sem Google, suíte completa) estão escritas do jeito que funciona')
confere('tools/capas.py --conferir' in corpo['Conferir o arquivo e as imagens (amostra)'] and 'tools/capas.py --testar 40' in corpo['Conferir o arquivo e as imagens (amostra)'],
        'confere o arquivo e pede 40 imagens de cada fonte')
confere('tools/atualizar.py' in corpo['Montar o painel com as capas novas'], 'o painel é montado com as capas novas (catálogo → dados → HTML)')
confere('tools/auditar_capas.py' in corpo['Refazer a auditoria das capas'] and '--conferir' in corpo['Refazer a auditoria das capas'] and '--rede 40' in corpo['Refazer a auditoria das capas'],
        'a auditoria é refeita, conferida e ainda pede 40 imagens')
confere('playwright' in corpo['Preparar os testes'] and 'playwright install' in corpo['Preparar os testes'], 'o navegador dos testes é instalado antes de rodá-los')
testes = corpo['Rodar os testes']
confere('tools/qa/tudo.py' in testes and all(t in testes for t in ('importador', 'busca_capas', 'auditoria_capas', 'capas_painel')),
        'os testes das capas e do painel rodam de verdade (e a suíte inteira é uma opção)', testes.strip().splitlines()[:3])
confere('BIBLIOTECA_QA_TMP: ${{ runner.temp }}/biblioteca-qa' in testes, 'os registros dos testes ficam fora do repositório')
confere(not re.search(r'^    env:\n(?:      [^\n]*\n)*?      BIBLIOTECA_QA_TMP:.*runner\.', txt, flags=re.M),
        'runner.temp não aparece no env do job: esse contexto só existe dentro dos passos; no job, o GitHub rejeita o arquivo inteiro')
pr = corpo['Abrir o Pull Request']
confere("if [ \"$CODIGO_TESTES\" != 0 ]; then rascunho='--draft'" in pr, 'teste falhando: o PR nasce como rascunho, para ninguém aprovar por engano')
confere('$rascunho' in pr and 'exit 1' in pr, 'e a execução termina em vermelho')
confere('Nada foi publicado' in pr and 'catalogo/capas-revisao.md' in pr and 'git diff --stat' in pr, 'o corpo do PR diz o que mudou, traz o retrato das capas e lembra que nada foi publicado')
confere('Allow GitHub Actions to create and approve pull requests' in pr and '/compare/' in pr, 'se o GitHub não deixar abrir o PR, o aviso diz como resolver e onde abrir à mão')

print('O SITE CONTINUA ESPERANDO APROVAÇÃO')
site = SITE.read_text(encoding='utf-8')
confere(re.search(r'push:\s*\n\s*branches: \[main\]', site) is not None, 'o site só é publicado quando algo entra em main')
site_sem_comentarios = '\n'.join(l for l in site.splitlines() if not l.lstrip().startswith('#'))
confere('tools/atualizar.py' not in site_sem_comentarios and 'tools/capas.py' not in site_sem_comentarios, 'e o serviço do site não gera nem procura nada: publica o arquivo que já está no repositório')

print('OS COMANDOS CITADOS EXISTEM')
for nome in ('capas.py', 'auditar_capas.py', 'atualizar.py', 'qa/tudo.py'):
    confere((RAIZ / 'tools' / nome).exists(), f'tools/{nome} existe')
ajuda = C.__doc__
for opcao in ('--minutos', '--refazer', '--sem-google', '--limite', '--conferir', '--testar', '--auditar', '--candidatos'):
    confere(opcao in ajuda, f'o capas.py documenta {opcao}')
import auditar_capas as A
for opcao in ('--conferir', '--rede', '--resumo'):
    confere(opcao in A.__doc__, f'o auditar_capas.py documenta {opcao}')
r = subprocess.run([sys.executable, str(RAIZ / 'tools' / 'auditar_capas.py'), '--conferir'], capture_output=True, text=True)
confere(r.returncode == 0 and 'em dia' in r.stdout, 'a auditoria que o robô roda passa no repositório como ele está', r.stdout.strip())

print('ERROS:', len(erros))
for e in erros: print('  ', e)
sys.exit(1 if erros else 0)
