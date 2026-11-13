#!/usr/bin/env python3
"""Gera as listagens da biblioteca virtual a partir das pastas reais do computador.

    python tools/gerar_listagens.py --origem "D:\\Biblioteca" --conferir
    python tools/gerar_listagens.py --origem "D:\\Biblioteca"
    python tools/gerar_listagens.py --origem "D:\\Biblioteca" --incluir "HQs/Mangás=Mangás"
    python tools/gerar_listagens.py --origem "D:\\Biblioteca" --incluir-conhecidas

O que faz:
  · procura as pastas da biblioteca dentro de --origem (cada pasta imediata vira uma listagem);
  · gera `biblioteca-virtual/listagens/<nome>.txte`, no formato que tools/importar_digital.py já lê;
  · em pastas de quadrinhos, inclui o nome das subpastas de série; em pastas de livros, não;
  · conhece a subpasta que é outra biblioteca (`novashqs/novas` → `novasHQSS`);
  · com --incluir-conhecidas, também gera a pasta aninhada já conhecida `HQs/Mangás`, se ela existir;
    com --incluir, aceita outra pasta aninhada, ex.: `HQs/Mangás=Mangás`;
  · não apaga listagem de pasta que não foi encontrada, não mexe no inventário, no catálogo nem no painel;
  · --conferir só mostra o que mudaria; repetir sem mudança não grava nada;
  · grava em CP850/CRLF; se um nome não couber no CP850, usa UTF-8/CRLF para aquela listagem e avisa.

No Windows, o arquivo `Gerar listagens.bat` na raiz do repositório faz a mesma coisa com dois cliques:
primeiro mostra a prévia, pergunta se pode incluir a subpasta conhecida de mangás e depois pergunta se pode gravar.

A listagem é só o nome dos arquivos e subpastas, como `dir /b`. Título, autor, eixo e marcadores continuam
sendo trabalho do importador e do inventário; este script não tenta adivinhar nada disso.
"""
import argparse, os, pathlib, sys, tempfile

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import importar_digital as imp                                  # noqa: E402

DESTINO = imp.LISTAGENS
IGNORAR = {'gerador de nomes.bat', 'gerar listagens.bat', 'gerar_listagens.py', 'desktop.ini', 'thumbs.db', '.ds_store'}
EXTRAS_CONHECIDAS = ('HQs/Mangás=Mangás',)
CODIFICACOES = {'cp850': 'cp850', 'utf8': 'utf-8', 'utf-8': 'utf-8'}


def nome_ignorado(nome):
    """A própria listagem, o gerador e arquivos de sistema não entram na lista."""
    n = nome.lower()
    return n in IGNORAR or n.endswith(('.txte', '.bat'))


def entradas_da_pasta(pasta, listagem, subpastas_proprias):
    """Nomes que o `dir /b` mostraria para esta pasta da biblioteca, já sem listagem/gerador.
    Em pasta de quadrinhos, subpasta de série entra pelo nome; subpasta com listagem própria fica de fora
    (ela é gerada como outra listagem). Em pasta de livros, subpastas não entram: são outras pastas da biblioteca."""
    pasta = pathlib.Path(pasta)
    hq = imp.pasta_de_hq(listagem)
    proprias = {sub for (pai, sub), alvo in subpastas_proprias.items() if pai == listagem}
    nomes = []
    for filho in pasta.iterdir():
        nome = filho.name
        if nome_ignorado(nome):
            continue
        if filho.is_dir():
            if hq and nome not in proprias:
                nomes.append(nome)
            continue
        if filho.is_file():
            nomes.append(nome)
    return sorted(nomes, key=lambda s: (s.lower(), s))


def caminho_relativo(valor):
    """Caminho relativo dentro de --origem, aceitando barra do Windows ou barra normal."""
    texto = str(valor or '').strip().replace('\\', '/')
    partes = pathlib.PurePosixPath(texto)
    if (not texto or texto in ('.', '..') or partes.is_absolute() or not partes.parts
            or '..' in partes.parts or ':' in partes.parts[0] or any(c in texto for c in '\r\n\x00')):
        raise ValueError(f'caminho relativo inválido: {valor!r}')
    return pathlib.Path(*partes.parts)


def valida_nome_listagem(nome):
    if (not nome or nome in ('.', '..') or nome.lower().endswith('.txte') or nome != nome.strip()
            or nome.endswith('.') or any(c in nome for c in '/\\\r\n\x00')):
        raise ValueError(f'nome de listagem inválido: {nome!r}')


def parse_incluir(valor):
    """`HQs/Mangás` → (HQs/Mangás, Mangás); `HQs/Mangás=Mangás` → o nome pedido."""
    texto = str(valor or '').strip()
    if '=' in texto:
        rel, nome = texto.split('=', 1)
        rel, nome = caminho_relativo(rel), nome.strip()
        try:
            valida_nome_listagem(nome)
        except ValueError as e:
            raise ValueError(f'nome de listagem inválido em --incluir: {valor!r}') from e
        return rel, nome
    rel = caminho_relativo(texto)
    valida_nome_listagem(rel.name)
    return rel, rel.name


def mapa_de_pastas(origem, incluir=(), incluir_conhecidas=False):
    """{nome da listagem: pasta real}. Pastas imediatas de --origem, a subpasta conhecida `novashqs/novas`,
    as pastas pedidas em --incluir e, com --incluir-conhecidas, as extras conhecidas que existirem.
    Conflito de nome (ou de nome que só difere em maiúsculas) para duas pastas diferentes é erro, não sobrescrita."""
    origem = pathlib.Path(origem)
    if not origem.is_dir():
        raise ValueError(f'a pasta de origem não existe: {origem}')
    mapa, vistos = {}, {}

    def acrescenta(nome, pasta):
        valida_nome_listagem(nome)
        k = nome.casefold()
        if k in vistos and mapa[vistos[k]] != pasta:
            raise ValueError(f'o nome de listagem {nome!r} aponta para duas pastas: {mapa[vistos[k]]} e {pasta}')
        vistos[k] = nome
        mapa[nome] = pasta

    for filho in sorted(origem.iterdir(), key=lambda p: p.name.lower()):
        if filho.is_dir() and not filho.name.startswith('.'):
            acrescenta(filho.name, filho)
    for (pai, sub), alvo in imp.SUBPASTAS_LISTADAS.items():
        pasta = origem / pai / sub
        if pasta.is_dir():
            acrescenta(alvo, pasta)
    pedidos = list(incluir)
    if incluir_conhecidas:
        for valor in EXTRAS_CONHECIDAS:
            rel, _ = parse_incluir(valor)
            if (origem / rel).is_dir():
                pedidos.append(valor)
    for valor in pedidos:
        rel, nome = parse_incluir(valor)
        pasta = origem / rel
        if not pasta.is_dir():
            raise ValueError(f'pasta pedida em --incluir não existe: {pasta}')
        acrescenta(nome, pasta)
    return dict(sorted(mapa.items(), key=lambda par: par[0].lower()))


def bytes_listagem(nomes, codificacao='cp850'):
    if codificacao not in CODIFICACOES:
        raise ValueError(f'codificação não suportada: {codificacao!r}')
    for nome in nomes:
        if any(c in nome for c in '\r\n\x00'):
            raise ValueError(f'nome com quebra de linha ou caractere de controle: {nome!r}')
    texto = '\r\n'.join(nomes) + ('\r\n' if nomes else '')
    return texto.encode(CODIFICACOES[codificacao])


def linhas_existentes(caminho):
    if not caminho.exists():
        return None
    return [l.strip() for l in imp.ler_texto(caminho).replace('\r', '').split('\n') if l.strip()]


def _gravar_atomico(caminho, dados):
    """Escreve em arquivo temporário no mesmo destino e só então substitui a listagem."""
    fd, temp = tempfile.mkstemp(dir=str(caminho.parent), prefix='.gerar-', suffix='.tmp')
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(dados)
        os.replace(temp, caminho)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def gerar(origem, destino=DESTINO, conferir=False, codificacao='cp850', incluir=(), forcar=False, incluir_conhecidas=False):
    """Gera (ou só confere) as listagens. Devolve um relatório com novas, alteradas, inalteradas, vazias,
    esvaziadas, sem_pasta e utf8. Não apaga listagem de pasta ausente. Recusa origem que não parece a biblioteca
    quando já há listagens conhecidas, a menos que --forcar. Pasta vazia que sobrescreveria listagem não vazia
    também espera --forcar. Prepara todos os bytes antes de gravar, para erro de nome/codificação não deixar metade."""
    if codificacao not in CODIFICACOES:
        raise ValueError(f'codificação não suportada: {codificacao!r}')
    destino = pathlib.Path(destino)
    mapa = mapa_de_pastas(origem, incluir, incluir_conhecidas)
    existentes = {p.stem: p for p in destino.glob('*.txte')} if destino.exists() else {}
    if existentes and not forcar and not (set(mapa) & set(existentes)):
        raise ValueError('nenhuma pasta encontrada casa com as listagens que já existem; confira --origem '
                         '(ou use --forcar se for mesmo uma biblioteca nova)')
    relatorio = {'novas': [], 'alteradas': [], 'inalteradas': [], 'vazias': [], 'esvaziadas': [], 'utf8': [],
                 'sem_pasta': sorted(set(existentes) - set(mapa), key=str.lower)}
    subpastas_proprias = dict(imp.subpastas_listadas(set(mapa) | set(existentes)))
    for valor in incluir:                                         # pasta aninhada que também é biblioteca não é série da pasta pai
        caminho_rel, nome_listagem = parse_incluir(valor)
        if len(caminho_rel.parts) >= 2:
            subpastas_proprias[(caminho_rel.parts[0], caminho_rel.parts[1])] = nome_listagem
    if incluir_conhecidas:
        for valor in EXTRAS_CONHECIDAS:
            caminho_rel, nome_listagem = parse_incluir(valor)
            if (pathlib.Path(origem) / caminho_rel).is_dir() and len(caminho_rel.parts) >= 2:
                subpastas_proprias[(caminho_rel.parts[0], caminho_rel.parts[1])] = nome_listagem
    pendentes = []
    for nome, pasta in mapa.items():
        entradas = entradas_da_pasta(pasta, nome, subpastas_proprias)
        caminho = destino / f'{nome}.txte'
        atuais = linhas_existentes(caminho)
        if atuais is not None and set(atuais) == set(entradas):
            relatorio['inalteradas'].append(nome)                 # mesma lista: preserva bytes/ordem/encoding
            continue
        if not entradas and atuais:
            if not forcar:
                relatorio['vazias'].append(nome)
                continue
            relatorio['esvaziadas'].append(nome)
        try:
            novo = bytes_listagem(entradas, codificacao)
        except UnicodeEncodeError:
            if codificacao != 'cp850':
                raise
            novo = bytes_listagem(entradas, 'utf-8')              # nome fora do CP850: UTF-8, que o importador já lê
            usou_utf8 = True
        else:
            usou_utf8 = False
        if caminho.exists() and caminho.read_bytes() == novo:
            relatorio['inalteradas'].append(nome)
            continue
        relatorio['novas' if atuais is None else 'alteradas'].append(nome)
        if usou_utf8:
            relatorio['utf8'].append(nome)
        pendentes.append((caminho, novo))
    if not conferir and pendentes:
        destino.mkdir(parents=True, exist_ok=True)
        for caminho, novo in pendentes:
            _gravar_atomico(caminho, novo)
    return relatorio


def texto_relatorio(rel, conferir=False):
    acao = 'gravaria' if conferir else 'gravou'
    L = [f'Listagens: {len(rel["novas"])} nova(s), {len(rel["alteradas"])} alterada(s), {len(rel["inalteradas"])} sem mudança.']
    for nome in rel['novas']:
        L.append(f'  nova: {nome}.txte')
    for nome in rel['alteradas']:
        L.append(f'  {acao}: {nome}.txte')
    for nome in rel['vazias']:
        L.append(f'  pasta vazia (não sobrescrita sem --forcar): {nome}.txte')
    for nome in rel.get('esvaziadas', []):
        L.append(f'  pasta vazia: {"esvaziaria" if conferir else "esvaziou"} {nome}.txte (--forcar)')
    for nome in rel.get('utf8', []):
        L.append(f'  nome fora do CP850: {nome}.txte em UTF-8')
    for nome in rel['sem_pasta']:
        L.append(f'  pasta não encontrada (listagem mantida): {nome}.txte')
    L.append('Nada foi gravado.' if conferir else 'Pronto. Envie a pasta biblioteca-virtual/listagens para o GitHub e peça para atualizar a biblioteca virtual.')
    return '\n'.join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description='Gera as listagens da biblioteca virtual sem mexer no catálogo, inventário ou painel.')
    ap.add_argument('--origem', required=True, help='pasta raiz da biblioteca virtual no seu computador')
    ap.add_argument('--destino', default=str(DESTINO), help='pasta das listagens no repositório')
    ap.add_argument('--conferir', action='store_true', help='só mostra o que mudaria; não grava')
    ap.add_argument('--incluir', action='append', default=[], help='pasta aninhada extra: RELATIVO ou RELATIVO=NOME (ex.: HQs/Mangás=Mangás)')
    ap.add_argument('--incluir-conhecidas', action='store_true', help='inclui as pastas aninhadas já conhecidas que existirem (hoje: HQs/Mangás)')
    ap.add_argument('--utf8', action='store_true', help='grava em UTF-8 em vez de CP850 (o importador lê os dois)')
    ap.add_argument('--forcar', action='store_true', help='permite origem sem pastas conhecidas e sobrescrita por pasta vazia')
    args = ap.parse_args(argv)
    try:
        rel = gerar(args.origem, args.destino, args.conferir, 'utf-8' if args.utf8 else 'cp850',
                    args.incluir, args.forcar, args.incluir_conhecidas)
    except (ValueError, OSError, UnicodeError, LookupError) as e:
        print(f'Não foi possível gerar: {e}')
        return 2
    print(texto_relatorio(rel, args.conferir))
    return 0


if __name__ == '__main__':
    sys.exit(main())
