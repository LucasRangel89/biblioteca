"""O gerador único de listagens da biblioteca virtual (tools/gerar_listagens.py).

Cria pastas fictícias, gera as listagens e confere o contrato do importador: uma listagem por pasta, nomes como
`dir /b`, CP850/CRLF, subpastas de série em pasta de HQ, subpasta que é outra biblioteca, pasta aninhada extra,
prévia sem gravar, repetição sem mudança, pasta ausente preservada e recusa de origem errada. Não toca no catálogo,
no inventário nem no painel. Confere também o wrapper de Windows e a fronteira de `referencias/`.
"""
import contextlib, io, pathlib, shutil, sys, tempfile

QA = pathlib.Path(__file__).resolve().parent
RAIZ = QA.parent.parent
sys.path.insert(0, str(QA.parent))
import gerar_listagens as G
import importar_digital as imp

erros = []


def confere(cond, msg, extra=''):
    print(('ok    ' if cond else 'FALHOU'), msg + (f' — {extra}' if extra != '' and not cond else ''))
    if not cond: erros.append(msg)


def toca(pasta, *nomes):
    pasta.mkdir(parents=True, exist_ok=True)
    for nome in nomes:
        (pasta / nome).write_bytes(b'x')


tmp = pathlib.Path(tempfile.mkdtemp(prefix='biblioteca-listagens-'))
origem, destino = tmp / 'biblioteca', tmp / 'listagens'
toca(origem / 'poesia', 'Coração - Autora.epub', 'capa.jpg', 'poesia.txte', 'gerador de nomes.bat')
(origem / 'poesia' / 'Outra pasta').mkdir()
(origem / 'poesia' / 'Outra pasta' / 'nao entra.txt').write_bytes(b'x')
toca(origem / 'HQs', 'solto.cbr', 'HQs.txte')
(origem / 'HQs' / '100 Balas').mkdir()
(origem / 'HQs' / 'Akira').mkdir()
toca(origem / 'HQs' / 'Mangás', 'naruto.cbz')
toca(origem / 'novashqs', 'solto.cbz')
toca(origem / 'novashqs' / 'novas', '1984 (em quadrinhos).pdf')
(origem / 'Vazia').mkdir()
destino.mkdir()
# mesma lista da poesia, em outra ordem e com acento em CP850: o gerador deve preservar os bytes
antigo_poesia = 'capa.jpg\r\nCoração - Autora.epub\r\n'.encode('cp850')
(destino / 'poesia.txte').write_bytes(antigo_poesia)
(destino / 'Sumiu.txte').write_bytes('arquivo antigo.pdf\r\n'.encode('cp850'))
(destino / 'Vazia.txte').write_bytes('tinha coisa.pdf\r\n'.encode('cp850'))

mapa = G.mapa_de_pastas(origem, ['HQs/Mangás=Mangás'])
confere(set(mapa) == {'poesia', 'HQs', 'Mangás', 'novashqs', 'novasHQSS', 'Vazia'},
        'o mapa acha as pastas imediatas, a subpasta conhecida novasHQSS e a pasta extra Mangás', sorted(mapa))
confere(G.mapa_de_pastas(origem, incluir_conhecidas=True) == mapa,
        '--incluir-conhecidas acha a pasta de mangás já conhecida sem digitar o caminho')
sem_mangas = tmp / 'sem-mangas'; (sem_mangas / 'HQs').mkdir(parents=True)
confere('Mangás' not in G.mapa_de_pastas(sem_mangas, incluir_conhecidas=True),
        '--incluir-conhecidas não reclama quando a pasta extra não existe')
confere(G.entradas_da_pasta(origem / 'poesia', 'poesia', {}) == ['capa.jpg', 'Coração - Autora.epub'],
        'pasta de livros: arquivos entram, subpasta e a própria listagem/gerador ficam de fora')
confere(G.entradas_da_pasta(origem / 'HQs', 'HQs', {('HQs', 'Mangás'): 'Mangás', ('novashqs', 'novas'): 'novasHQSS'}) == ['100 Balas', 'Akira', 'solto.cbr'],
        'pasta de HQ: subpastas de série entram pelo nome; Mangás, que ganhou listagem própria, não é série')
confere(G.entradas_da_pasta(origem / 'novashqs', 'novashqs', imp.SUBPASTAS_LISTADAS) == ['solto.cbz'],
        'novashqs/novas não vira série: é a listagem novasHQSS')
confere(G.parse_incluir('HQs\\Mangás=Mangás') == (pathlib.Path('HQs/Mangás'), 'Mangás'),
        '--incluir aceita barra do Windows e nome explícito')
for ruim in ('../fora', '/absoluto', 'C:/fora', '', '.', '..'):
    try: G.caminho_relativo(ruim); levantou = False
    except ValueError: levantou = True
    confere(levantou, f'caminho relativo perigoso é recusado: {ruim!r}')
for ruim in ('HQs=', 'HQs=../fora', 'HQs=nome.txte'):
    try: G.parse_incluir(ruim); levantou = False
    except ValueError: levantou = True
    confere(levantou, f'--incluir com nome inválido é recusado: {ruim!r}')
conflito = tmp / 'conflito'
(conflito / 'Duplicada').mkdir(parents=True); (conflito / 'duplicada').mkdir()
try: G.mapa_de_pastas(conflito); levantou = False
except ValueError as e: levantou = 'duas pastas' in str(e)
confere(levantou, 'nomes que só diferem em maiúsculas não viram duas listagens em conflito')

s = io.StringIO()
with contextlib.redirect_stdout(s): codigo = G.main(['--origem', str(origem), '--destino', str(destino), '--incluir', 'HQs/Mangás=Mangás', '--conferir'])
confere(codigo == 0 and 'Nada foi gravado' in s.getvalue() and (destino / 'poesia.txte').read_bytes() == antigo_poesia
        and not (destino / 'HQs.txte').exists() and (destino / 'Sumiu.txte').exists(),
        '--conferir mostra a prévia e não grava nada', s.getvalue().strip())

rel = G.gerar(origem, destino, incluir=['HQs/Mangás=Mangás'])
confere(rel['inalteradas'] == ['poesia'] and (destino / 'poesia.txte').read_bytes() == antigo_poesia,
        'mesma lista de nomes preserva os bytes existentes, sem trocar ordem/encoding à toa', rel)
confere(set(rel['novas']) == {'HQs', 'Mangás', 'novashqs', 'novasHQSS'} and rel['vazias'] == ['Vazia'] and rel['sem_pasta'] == ['Sumiu'],
        'gera as novas, não sobrescreve pasta vazia sem --forcar e mantém listagem de pasta ausente', rel)
bruto = (destino / 'poesia.txte').read_bytes()
confere(bruto == antigo_poesia and (destino / 'HQs.txte').read_bytes().decode('cp850').splitlines() == ['100 Balas', 'Akira', 'solto.cbr']
        and b'\r\n' in (destino / 'HQs.txte').read_bytes(),
        'as listagens saem em CP850 com CRLF, como o importador já espera')
confere((destino / 'Mangás.txte').read_bytes().decode('cp850').splitlines() == ['naruto.cbz']
        and (destino / 'novasHQSS.txte').read_bytes().decode('cp850').splitlines() == ['1984 (em quadrinhos).pdf'],
        'Mangás e novasHQSS ganham listagem própria')
lidas = imp.ler_listagens(destino)
confere(lidas['HQs'] == ['100 Balas', 'Akira', 'solto.cbr'] and lidas['novasHQSS'] == ['1984 (em quadrinhos).pdf']
        and 'Mangás' not in lidas['HQs'] and lidas['Mangás'] == ['naruto.cbz'],
        'o importador lê as listagens geradas sem transformar Mangás em série de HQs', lidas)
antes = {p.name: p.read_bytes() for p in destino.glob('*.txte')}
rel2 = G.gerar(origem, destino, incluir=['HQs/Mangás=Mangás'])
confere(not rel2['novas'] and not rel2['alteradas'] and {p.name: p.read_bytes() for p in destino.glob('*.txte')} == antes,
        'rodar de novo não muda nada', rel2)
rel3 = G.gerar(origem, destino, incluir=['HQs/Mangás=Mangás'], forcar=True)
confere((destino / 'Vazia.txte').read_bytes() == b'' and 'Vazia' in rel3['alteradas'] and rel3['esvaziadas'] == ['Vazia'],
        'com --forcar, pasta vazia pode esvaziar a listagem, e o relatório diz isso', rel3)
toca(origem / 'Unicode', 'Café 📚.epub')
rel4 = G.gerar(origem, destino, incluir=['HQs/Mangás=Mangás'])
confere(rel4['novas'] == ['Unicode'] and rel4['utf8'] == ['Unicode']
        and imp.ler_listagens(destino)['Unicode'] == ['Café 📚.epub'],
        'nome fora do CP850 vira UTF-8 com aviso, e o importador lê', rel4)
antes_unicode = (destino / 'Unicode.txte').read_bytes()
rel5 = G.gerar(origem, destino, incluir=['HQs/Mangás=Mangás'])
confere(not rel5['novas'] and not rel5['alteradas'] and not rel5['utf8']
        and (destino / 'Unicode.txte').read_bytes() == antes_unicode and not list(destino.glob('*.tmp')),
        'a listagem UTF-8 também fica imóvel na repetição, sem temporário sobrando', rel5)
s = io.StringIO()
with contextlib.redirect_stdout(s): codigo = G.main(['--origem', str(origem), '--destino', str(destino), '--incluir-conhecidas', '--conferir'])
confere(codigo == 0 and 'Nada foi gravado' in s.getvalue(), '--incluir-conhecidas funciona pela linha de comando')

errada = tmp / 'errada'; (errada / 'Nada a ver').mkdir(parents=True)
try: G.gerar(errada, destino); levantou = False
except ValueError as e: levantou = 'nenhuma pasta encontrada casa' in str(e)
confere(levantou, 'origem que não parece a biblioteca é recusada quando já há listagens conhecidas')
s = io.StringIO()
with contextlib.redirect_stdout(s): codigo = G.main(['--origem', str(tmp / 'nao-existe'), '--destino', str(destino)])
confere(codigo == 2 and 'Não foi possível gerar' in s.getvalue(), 'origem inexistente devolve erro claro')

bat = (RAIZ / 'Gerar listagens.bat').read_text(encoding='utf-8')
confere('tools\\gerar_listagens.py' in bat and bat.find('--conferir') < bat.rfind('tools\\gerar_listagens.py')
        and 'CONFIRMA' in bat and '--incluir-conhecidas' in bat and 'atualizar.py' not in bat and 'importar_digital.py' not in bat,
        'o wrapper de Windows mostra a prévia, pergunta antes de gravar e não chama o importador/painel')
confere((RAIZ / 'referencias' / 'LEIAME.md').is_file(), 'referencias/ tem LEIAME de guarda e fronteira')
ativos = [p for p in list((RAIZ / 'tools').rglob('*.py')) + list((RAIZ / 'src').rglob('*')) + list((RAIZ / '.github').rglob('*.yml'))
          if p.is_file() and p.suffix in ('.py', '.js', '.html', '.css', '.yml') and 'referencias/' in p.read_text(encoding='utf-8', errors='ignore')
          and p.resolve() != (QA / 'gerar_listagens.py').resolve()]
confere(not ativos, 'nenhum código ativo importa ou lê referencias/', [str(p.relative_to(RAIZ)) for p in ativos])

shutil.rmtree(tmp, ignore_errors=True)
print('ERROS:', len(erros))
for e in erros: print('  ', e)
sys.exit(1 if erros else 0)
