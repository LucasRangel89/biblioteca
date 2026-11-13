"""A capa que vem dentro do arquivo: EPUB e CBZ abertos no navegador (54-capa-digital, 55-anexos, 56-lote-capas).

O painel tira a imagem da capa do próprio livro digital quando o usuário anexa o arquivo, e percorre uma pasta inteira
fazendo isso para muitos livros de uma vez — tudo no computador dele, sem internet. Este teste constrói EPUBs e CBZs de
verdade (pacotes .zip com índice, imagens em PNG, caminhos com "../", com "%20" e com acento) e roda contra eles o
código que vai no painel, no Node, sem navegador:

  · EPUB: a capa é a anunciada no índice (`properties="cover-image"`, `<meta name="cover">` pelo id do item ou pelo nome
    do arquivo); sem anúncio, a que tem "capa"/"cover" no nome — e nunca a primeira imagem do miolo;
  · CBZ: a que se anuncia como capa; senão, a primeira imagem na ordem dos números (001 antes de 010);
  · do pacote são lidos só a cauda, o índice e a entrada da capa: um livro de vários megabytes não entra inteiro na
    memória e o limite de anexação (5 MB) não trava a extração;
  · o que não é .epub/.cbz não é tocado; pacote truncado, índice em ZIP64, imagem ausente, SVG ou endereço externo
    devolvem nada — em silêncio, sem erro e sem rede —, mas com o MOTIVO, que é o que o quadro da varredura conta;
   · o EPUB anuncia a capa de três maneiras: properties="cover-image", <meta name="cover"> e a referência type="cover"
     do <guide> (o jeito dos livros convertidos por Calibre); com uma imagem só no pacote, ela é a capa;
  · o fluxo da ficha: a capa só entra em livro sem capa nenhuma (nem enviada, nem do catálogo), passa pelo reduzidor
    da "Enviar capa…" e é gravada como capa enviada (vale com as capas desligadas, entra no backup, sai com "Tirar a
    capa enviada"); anexar um arquivo que É o livro não marca "possui análise";
  · a varredura de pasta: reconhece o livro primeiro pelo mapa do inventário (DIGITAIS_NOMES), depois pelo casamento
    exato de título, deixa de lado ambíguos e livros que já têm capa, e não anexa arquivo nenhum;
  · a pasta da biblioteca é categoria de prateleira, não série: ela nunca entra na fase de "um título dentro do outro",
    que é o que fazia um lote inteiro virar "mais de um livro" sem nada ser lido.

O JavaScript executado aqui é o dos arquivos do painel, lido como está no repositório (mesma ordem do gerador). O que o
Node não tem — a tela e o banco do navegador — é imitado pelo mínimo: uma imagem que abre com o tamanho pedido, um
canvas que devolve um JPEG falso, um IndexedDB e um quadro de diálogo de mentirinha. O teste falha se alguém tentar
ir à internet.
"""
import json, pathlib, re, shutil, subprocess, sys, unicodedata, zipfile

QA = pathlib.Path(__file__).resolve().parent
RAIZ = QA.parent.parent
sys.path.insert(0, str(QA))
import caminhos                                     # noqa: E402
from relogio import png                              # noqa: E402

PACOTE = caminhos.TMP / 'capa-digital'
FIX = PACOTE / 'fix'
erros = []


def confere(cond, msg, extra=''):
    print(('ok    ' if cond else 'FALHOU'), msg + (f' — {extra}' if extra != '' and not cond else ''))
    if not cond:
        erros.append(msg)


def gravar(zf, nome, dados, comprimido=True, sistema=0):
    """um arquivo dentro do pacote; `sistema=3` faz o índice ganhar campos extras, como nos pacotes criados no Linux"""
    info = zipfile.ZipInfo(nome, date_time=(2026, 11, 12, 8, 30, 0))
    info.compress_type = zipfile.ZIP_DEFLATED if comprimido else zipfile.ZIP_STORED
    info.create_system = sistema
    zf.writestr(info, dados)


def item(id_, href, tipo='image/png', props=''):
    return '<item id="%s" href="%s" media-type="%s"%s/>' % (id_, href, tipo, ' properties="%s"' % props if props else '')


def esqueleto(zf, opf='OEBPS/package.opf', manifest='', metas='', container=True):
    """o miolo de um EPUB: o tipo do arquivo, o índice do livro e o manifesto com as imagens"""
    gravar(zf, 'mimetype', 'application/epub+zip', comprimido=False)
    if container:
        gravar(zf, 'META-INF/container.xml', '<?xml version="1.0"?><container xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
               '<rootfiles><rootfile full-path="%s" media-type="application/oebps-package+xml"/></rootfiles></container>' % opf)
    gravar(zf, opf, '<?xml version="1.0"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0"><metadata>%s</metadata>'
           '<manifest><item id="nav" href="toc.ncx" media-type="application/x-dtbncx+xml"/>%s</manifest>'
           '<spine toc="nav"/></package>' % (metas, manifest))
    gravar(zf, 'OEBPS/toc.ncx', '<ncx/>')
    gravar(zf, 'OEBPS/cap1.xhtml', '<html xmlns="http://www.w3.org/1999/xhtml"><body><p>texto do miolo</p></body></html>')


def epub(nome, *args, **kw):
    with zipfile.ZipFile(FIX / nome, 'w') as z:
        esqueleto(z, *args, **kw)


CAPA = png(20, 120, 200, 300, 420)                  # 300 × 420: a capa
OUTRA = png(200, 30, 30, 80, 100)                    # 80 × 100: qualquer outra imagem do pacote

print('OS PACOTES DE TESTE')
FIX.mkdir(parents=True, exist_ok=True)

# o índice anuncia a capa por <meta name="cover"> — e há uma imagem com "capa" no nome que NÃO é a capa: o anúncio
# manda no nome; a capa em si vem comprimida (deflate), como quase sempre
with zipfile.ZipFile(FIX / 'meta.epub', 'w') as z:
    esqueleto(z, manifest=item('img1', 'images/frente.png') + item('img2', 'images/capa-do-catalogo.png'),
              metas='<meta name="cover" content="img1"/>')
    gravar(z, 'OEBPS/images/frente.png', CAPA)
    gravar(z, 'OEBPS/images/capa-do-catalogo.png', OUTRA)
# properties="cover-image", aspa simples, caminho com %20, imagem sem compressão e campos extras no índice
with zipfile.ZipFile(FIX / 'properties.epub', 'w') as z:
    esqueleto(z, opf='OEBPS/meu livro.opf',
              manifest="<item id='i1' href='imagens/a%20capa.png' media-type='image/png' properties='cover-image'/>" + item('i2', 'imagens/mapa.png'))
    gravar(z, 'OEBPS/imagens/a capa.png', CAPA, comprimido=False, sistema=3)
    gravar(z, 'OEBPS/imagens/mapa.png', OUTRA)
# as duas maneiras de anunciar, apontando para imagens diferentes: properties vem primeiro
with zipfile.ZipFile(FIX / 'prioridade.epub', 'w') as z:
    esqueleto(z, manifest=item('a', 'images/pelo-nome.png') + item('b', 'images/anunciada.png', props='cover-image'),
              metas='<meta name="cover" content="a"/>')
    gravar(z, 'OEBPS/images/pelo-nome.png', OUTRA)
    gravar(z, 'OEBPS/images/anunciada.png', CAPA)
# alguns geradores põem no meta name="cover" o NOME DO ARQUIVO, e não o id do item
with zipfile.ZipFile(FIX / 'pelo-nome-do-arquivo.epub', 'w') as z:
    esqueleto(z, manifest=item('Image00001', 'images/frente.jpg', 'image/jpeg') + item('Image00002', 'images/capa-interior.png'),
              metas='<meta name="cover" content="frente.jpg"/>')
    gravar(z, 'OEBPS/images/frente.jpg', CAPA)
    gravar(z, 'OEBPS/images/capa-interior.png', OUTRA)
# sem anúncio nenhum: vale o nome
with zipfile.ZipFile(FIX / 'nome.epub', 'w') as z:
    esqueleto(z, manifest=item('p1', 'images/001.png') + item('cov', 'images/COVER.JPG', 'image/jpeg'))
    gravar(z, 'OEBPS/images/001.png', OUTRA)
    gravar(z, 'OEBPS/images/COVER.JPG', CAPA)
# só imagens de miolo: não escolhemos nenhuma
with zipfile.ZipFile(FIX / 'sem-capa.epub', 'w') as z:
    esqueleto(z, manifest=item('p1', 'images/001.png') + item('p2', 'images/002.png'))
    gravar(z, 'OEBPS/images/001.png', OUTRA)
    gravar(z, 'OEBPS/images/002.png', OUTRA)
# o <guide type="cover"> é como os EPUBs 2 e os convertidos por Calibre anunciam a capa: sem <meta name="cover">
with zipfile.ZipFile(FIX / 'guia.epub', 'w') as z:
    gravar(z, 'mimetype', 'application/epub+zip', comprimido=False)
    gravar(z, 'META-INF/container.xml', '<?xml version="1.0"?><container><rootfiles><rootfile full-path="OEBPS/package.opf"'
           ' media-type="application/oebps-package+xml"/></rootfiles></container>')
    gravar(z, 'OEBPS/package.opf', '<?xml version="1.0"?><package xmlns="http://www.idpf.org/2007/opf" version="2.0"><metadata/>'
           '<manifest>' + item('c1', 'images/frente.jpg', 'image/jpeg') + item('t1', 'text/cap1.xhtml', 'application/xhtml+xml')
           + '</manifest><spine toc="ncx"/><guide><reference type="cover" title="Cover" href="images/frente.jpg"/></guide></package>')
    gravar(z, 'OEBPS/text/cap1.xhtml', '<html xmlns="http://www.w3.org/1999/xhtml"><body><p>miolo</p></body></html>')
    gravar(z, 'OEBPS/images/frente.jpg', CAPA)
# o guia apontando para uma PÁGINA (é o que muitos conversores fazem): não é licença de pegar a primeira imagem do miolo
with zipfile.ZipFile(FIX / 'guia-pagina.epub', 'w') as z:
    gravar(z, 'mimetype', 'application/epub+zip', comprimido=False)
    gravar(z, 'META-INF/container.xml', '<?xml version="1.0"?><container><rootfiles><rootfile full-path="OEBPS/package.opf"'
           ' media-type="application/oebps-package+xml"/></rootfiles></container>')
    gravar(z, 'OEBPS/package.opf', '<?xml version="1.0"?><package xmlns="http://www.idpf.org/2007/opf" version="2.0"><metadata/>'
           '<manifest>' + item('i1', 'images/001.png') + item('t1', 'text/cap1.xhtml', 'application/xhtml+xml')
           + '</manifest><spine toc="ncx"/><guide><reference type="cover" href="text/cap1.xhtml"/></guide></package>')
    gravar(z, 'OEBPS/text/cap1.xhtml', '<html xmlns="http://www.w3.org/1999/xhtml"><body><p>miolo</p></body></html>')
    gravar(z, 'OEBPS/images/001.png', OUTRA)
# pacote com uma imagem só, sem anúncio: ela é a capa (é o que sai de um conversor simples)
with zipfile.ZipFile(FIX / 'imagem-unica.epub', 'w') as z:
    esqueleto(z, manifest=item('i1', 'images/img001.png'))
    gravar(z, 'OEBPS/images/img001.png', CAPA)
# a capa anunciada está no pacote, mas não é uma imagem que o navegador consiga abrir
with zipfile.ZipFile(FIX / 'capa-quebrada.epub', 'w') as z:
    esqueleto(z, manifest=item('c1', 'images/frente.png', props='cover-image'))
    gravar(z, 'OEBPS/images/frente.png', b'eu queria ser um png')
# o índice aponta para fora da pasta dele (../../), e o pacote tem a imagem na raiz
with zipfile.ZipFile(FIX / 'para-cima.epub', 'w') as z:
    esqueleto(z, opf='Livro/miolo/content.opf', manifest=item('c', '../../imagens/acima.png', props='cover-image'))
    gravar(z, 'imagens/acima.png', CAPA)
# a capa anunciada está fora do arquivo: não buscamos na internet
with zipfile.ZipFile(FIX / 'so-externo.epub', 'w') as z:
    esqueleto(z, manifest=item('c', 'https://exemplo.com/capa.png'))
# sem container.xml: com um único índice dá para achar, com dois não adivinhamos
with zipfile.ZipFile(FIX / 'opf-unico.epub', 'w') as z:
    gravar(z, 'mimetype', 'application/epub+zip', comprimido=False)
    gravar(z, 'Livro/content.opf', '<package><manifest>' + item('c', 'img/capa.png') + '</manifest></package>')
    gravar(z, 'Livro/img/capa.png', CAPA)
with zipfile.ZipFile(FIX / 'dois-opf.epub', 'w') as z:
    gravar(z, 'mimetype', 'application/epub+zip', comprimido=False)
    gravar(z, 'a.opf', '<package><manifest>' + item('c', 'capa.png') + '</manifest></package>')
    gravar(z, 'b.opf', '<package><manifest>' + item('c', 'capa.png') + '</manifest></package>')
# a capa anunciada é um SVG; e a anunciada pode não estar no pacote
with zipfile.ZipFile(FIX / 'svg.epub', 'w') as z:
    esqueleto(z, manifest=item('c', 'images/capa.svg', 'image/svg+xml'))
    gravar(z, 'OEBPS/images/capa.svg', b'<svg xmlns="http://www.w3.org/2000/svg"/>')
with zipfile.ZipFile(FIX / 'sumico.epub', 'w') as z:
    esqueleto(z, manifest=item('c', 'images/nao-existe.png'))
# CBZ: a ordem em que o pacote foi escrito é embaralhada, e a numeração é que manda
with zipfile.ZipFile(FIX / 'ordem.cbz', 'w') as z:
    for n in ('010.jpg', '002.jpg', '001.jpg'):
        gravar(z, n, CAPA if n == '001.jpg' else OUTRA, sistema=3)
with zipfile.ZipFile(FIX / 'anunciada.cbz', 'w') as z:
    for n in ('001.jpg', 'cover.png', 'pagina-02.jpg'):
        gravar(z, n, CAPA if n == 'cover.png' else OUTRA)
with zipfile.ZipFile(FIX / 'pastas.cbz', 'w') as z:
    for n in ('História 2/001.jpg', 'História 1/003.jpg', 'História 1/002.png'):
        gravar(z, n, CAPA if n.endswith('002.png') else OUTRA)
with zipfile.ZipFile(FIX / 'so-texto.cbz', 'w') as z:
    gravar(z, 'info.txt', 'sem imagem aqui')
# um EPUB grande: a capa está no fim, depois de um miolo pesado — serve para conferir que o arquivo não é lido inteiro,
# e que ele passa do limite de 5 MB da anexação sem impedir a extração
with zipfile.ZipFile(FIX / 'grande.epub', 'w') as z:
    esqueleto(z, manifest=item('c', 'images/pesado.png', props='cover-image'))
    for i in range(8):
        gravar(z, 'OEBPS/miolo%d.bin' % i, bytes(700 * 1024), comprimido=False)
    gravar(z, 'OEBPS/images/pesado.png', CAPA)
# pacotes que não dão
(FIX / 'ruim.epub').write_text('isto não é um pacote zip, de jeito nenhum', encoding='utf-8')
(FIX / 'truncado.epub').write_bytes((FIX / 'meta.epub').read_bytes()[:-60])
shutil.copy(FIX / 'anunciada.cbz', FIX / 'normal.zip')
shutil.copy(FIX / 'meta.epub', FIX / 'Capa MAIÚSCULA.EPUB')
(FIX / 'livro.epub.pdf').write_bytes(b'%PDF-1.4\n' + bytes(range(200)))
(FIX / 'esperado.png').write_bytes(CAPA)             # a mesma imagem posta dentro dos pacotes, para conferir byte a byte
print('  %d pacotes de teste prontos (o maior com %.1f MB)' % (len(list(FIX.iterdir())), (FIX / 'grande.epub').stat().st_size / 1048576))

HARNESS = r'''
/* O harness roda o JavaScript do painel de verdade: lê os módulos, junta-os na mesma ordem do gerador e os executa
   com o mínimo de tela imitada. Cada checagem imprime uma linha; a linha ERROS no fim é o que lê o tudo.py. */
import fs from 'node:fs';
import path from 'node:path';

const RAIZ = process.argv[2], FIX = process.argv[3];
const erros = [];
const ok = (cond, nome, extra) => { console.log((cond ? 'ok    ' : 'FALHOU') + ' ' + nome + (!cond && extra !== undefined ? ' — ' + JSON.stringify(extra).slice(0, 400) : '')); if (!cond) erros.push(nome); };

/* ---------- a tela, o banco e o quadro de diálogo imitados ---------- */
let imagem = { w: 600, h: 900 };                      // o tamanho natural que o navegador veria na imagem extraída
let canvasVisto = null;
const document = { createElement: () => (canvasVisto = { width: 0, height: 0, getContext: () => ({ fillStyle: '', fillRect() {}, imageSmoothingQuality: '', drawImage() {} }), toDataURL: () => 'data:image/jpeg;base64,QUVB' }) };
class Image { set src(_) { this.naturalWidth = imagem.w; this.naturalHeight = imagem.h; setTimeout(() => this.onload && this.onload(), 0); } }
const URL = { createObjectURL: () => 'blob:fake', revokeObjectURL() {} };
class FileReader { readAsDataURL() { this.result = 'data:application/octet-stream;base64,QUJB'; setTimeout(() => this.onload && this.onload(), 0); } }
let rede = 0;
globalThis.fetch = globalThis.XMLHttpRequest = function () { rede++; throw new Error('este teste não pode ir à internet'); };

const banco = new Map();                               // o IndexedDB de mentirinha: a tabela `anexos`, chave `k`
const pedido = resultado => ({ result: resultado });
const tabela = { put: r => { banco.set(r.k, r); return pedido(); }, get: k => pedido(banco.get(k) || null), delete: k => { banco.delete(k); return pedido(); },
                 clear: () => pedido(), getAllKeys: () => pedido([...banco.keys()]) };
const dbFalso = { transaction: () => { const tx = { objectStore: () => tabela }; setTimeout(() => tx.oncomplete && tx.oncomplete(), 0); return tx; } };

const ltSt = { textContent: '', isConnected: true };   // a linha de progresso do quadro da varredura
const ltFora = { hidden: true, innerHTML: '', isConnected: true };      // a lista dos arquivos que ficaram de fora
const $ = sel => (sel === '#lt-st' ? ltSt : sel === '#lt-fora' ? ltFora : null);
let dlgAberto = null;
const Dlg = { abrir(o) { dlgAberto = o; if (o.aoAbrir) o.aoAbrir({ querySelector: s => (s === '#lt-st' ? ltSt : s === '#lt-fora' ? ltFora : null) }); }, fechar() { dlgAberto = null; } };
const mapaDoInventario = {};                             // o DIGITAIS_NOMES de mentirinha: cada bloco põe o que precisa

const livros = [];
let avisos = [];
let desenhos = 0, gravacoes = 0;
const DB = { hoje: 20261112, livros };                       // o array do painel: tudo o que um teste cria entra nele, e é este que o módulo lê
const porId = id => DB.livros.find(b => b.id === id) || null;
const tocar = b => { b.u = 1; desenhos++; };
const toast = m => avisos.push(m);
const render = () => {}, desenharGaveta = () => {}, Gaveta = { id: null };
const defTag = (b, t, on) => { const i = b.tags.indexOf(t); if (on && i < 0) b.tags.push(t); if (!on && i >= 0) b.tags.splice(i, 1); };
const marcarMeu = b => { b.u = 1; };
const derivar = () => {}, salvar = () => { gravacoes++; };
const fInt = n => String(n), fDec = n => String(n);
const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const plural = (n, um, v) => `${n} ${n === 1 ? um : v}`;
const norm = s => String(s ?? '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
const Loja = { ok: true }, MAX_ANEXOS = 8, MAX_COMENTARIO = 5000, TAG_ANALISE = 'analise';
const temCapa = b => !!b._img;                          // como no painel: o catálogo diz se há capa (desligada ou não)

const fonte = ['54-capa-digital.js', '55-anexos.js', '56-lote-capas.js'].map(f => fs.readFileSync(path.join(RAIZ, 'src', 'js', f), 'utf8')).join('\n');
const rodar = new Function('DB', 'porId', 'tocar', 'toast', 'render', 'desenharGaveta', 'Gaveta', '$', 'MAX_ANEXOS', 'MAX_COMENTARIO', 'TAG_ANALISE',
  'defTag', 'marcarMeu', 'derivar', 'salvar', 'fInt', 'fDec', 'esc', 'plural', 'norm', 'Loja', 'temCapa', 'document', 'Image', 'URL', 'FileReader', 'bancoFalso', 'Dlg', 'DIGITAIS_NOMES',
  fonte + '\nAnexos.banco = Promise.resolve(bancoFalso); return { Notas, Anexos, LoteCapas, planejarLote, chaveDeNome, capaDoDigital, fonteDe, listarZip, bytesDaEntrada, textoDaEntrada, caminhoRelativo, capaAnunciadaEpub, capaDoCbz, reduzirImagem, DIGITAL_CAPA, LIVRO_DIGITAL, LOTE_MAX };');
const M = rodar(DB, porId, tocar, toast, render, desenharGaveta, Gaveta, $, MAX_ANEXOS, MAX_COMENTARIO, TAG_ANALISE,
  defTag, marcarMeu, derivar, salvar, fInt, fDec, esc, plural, norm, Loja, temCapa, document, Image, URL, FileReader, dbFalso, Dlg, mapaDoInventario);

const espera = () => new Promise(r => setTimeout(r, 60));
const bytesDo = nome => fs.readFileSync(path.join(FIX, nome));
/* um File do navegador: nome, tamanho e fatias lidas sob demanda (é assim que o painel lê um arquivo grande) */
function arquivoFake(nome, apelido) {
  const buf = bytesDo(nome), fatias = [];
  const pedaco = (a, b) => {                                   // como o navegador: um buffer do tamanho exato do pedaço lido
    const s = buf.subarray(Math.min(a, buf.length), Math.min(b, buf.length)), fora = new ArrayBuffer(s.length);
    new Uint8Array(fora).set(s); return fora;
  };
  return { name: apelido || nome, size: buf.length, type: '', __fatias: fatias,
           slice(a, b) { fatias.push([a, b]); return { arrayBuffer: async () => pedaco(a, b) }; },
           arrayBuffer: async () => pedaco(0, buf.length) };
}
const escolhido = async arq => { const r = await M.capaDoDigital(arq); return r && r.blob ? r.nome : null; };
const motivoDo = async arq => { const r = await M.capaDoDigital(arq); return (r && r.motivo) || 'veio capa'; };
const porNome = (nome, apelido) => arquivoFake(nome, apelido);

/* ---------- o que o módulo escolhe ---------- */
console.log('EPUB');
ok(await escolhido(porNome('meta.epub')) === 'frente.png', 'a capa é a imagem anunciada no índice (<meta name="cover">), não a que tem "capa" no nome', await escolhido(porNome('meta.epub')));
ok(await escolhido(porNome('properties.epub')) === 'a capa.png', 'properties="cover-image" é lido, com aspa simples, %20 e campos extras no índice', await escolhido(porNome('properties.epub')));
ok(await escolhido(porNome('prioridade.epub')) === 'anunciada.png', 'anunciada de duas maneiras: properties vem antes do <meta name="cover">', await escolhido(porNome('prioridade.epub')));
ok(await escolhido(porNome('pelo-nome-do-arquivo.epub')) === 'frente.jpg', 'meta name="cover" apontando pelo nome do arquivo (com extensão) também é entendido', await escolhido(porNome('pelo-nome-do-arquivo.epub')));
ok(await escolhido(porNome('nome.epub')) === 'COVER.JPG', 'sem anúncio no índice, vale a imagem com "cover" no nome', await escolhido(porNome('nome.epub')));
ok(await escolhido(porNome('sem-capa.epub')) === null, 'EPUB com imagens só de miolo: nenhuma é escolhida (adivinhar seria pôr o miolo na capa)', await escolhido(porNome('sem-capa.epub')));
ok(await escolhido(porNome('para-cima.epub')) === 'acima.png', 'índice apontando para fora da pasta (../../) é resolvido', await escolhido(porNome('para-cima.epub')));
ok(await escolhido(porNome('so-externo.epub')) === null, 'capa apontando para um endereço de fora: nada é buscado', await escolhido(porNome('so-externo.epub')));
ok(await escolhido(porNome('opf-unico.epub')) === 'capa.png', 'EPUB sem container.xml: havendo um único índice, ele é lido', await escolhido(porNome('opf-unico.epub')));
ok(await escolhido(porNome('dois-opf.epub')) === null, 'EPUB sem container.xml e com dois índices: não adivinhamos qual é o livro', await escolhido(porNome('dois-opf.epub')));
ok(await escolhido(porNome('svg.epub')) === null, 'capa anunciada em SVG: não serve, o navegador não a reduziria para o tamanho de capa', await escolhido(porNome('svg.epub')));
ok(await escolhido(porNome('sumico.epub')) === null, 'a imagem anunciada não está no pacote: nada é feito', await escolhido(porNome('sumico.epub')));
ok(await escolhido(porNome('guia.epub')) === 'frente.jpg', 'a referência type="cover" do <guide> é entendida (EPUBs 2 e livros do Calibre)', await escolhido(porNome('guia.epub')));
ok(await escolhido(porNome('guia-pagina.epub')) === null, 'o guia apontando para uma página não é licença de pegar a primeira imagem do miolo', await escolhido(porNome('guia-pagina.epub')));
ok(await escolhido(porNome('imagem-unica.epub')) === 'img001.png', 'EPUB com uma imagem só no pacote: ela é a capa', await escolhido(porNome('imagem-unica.epub')));
ok(await escolhido(porNome('Capa MAIÚSCULA.EPUB')) === 'frente.png', 'o nome do livro digital vale em qualquer grafia (Capa MAIÚSCULA.EPUB)', await escolhido(porNome('Capa MAIÚSCULA.EPUB')));
console.log('POR QUE NÃO VEIO CAPA');
ok(await motivoDo(porNome('sem-capa.epub')) === 'sem capa dentro', 'livro sem capa dentro do pacote: o motivo diz isso, em vez de um nada mudo', await motivoDo(porNome('sem-capa.epub')));
ok(await motivoDo(porNome('guia-pagina.epub')) === 'sem capa dentro', 'pacote que só tem miolo: sem capa dentro', await motivoDo(porNome('guia-pagina.epub')));
ok(await motivoDo(porNome('sumico.epub')) === 'capa fora do pacote', 'a capa anunciada não está no pacote: o motivo diz isso', await motivoDo(porNome('sumico.epub')));
ok(await motivoDo(porNome('dois-opf.epub')) === 'sem capa dentro', 'dois índices e nenhum container.xml: nada é adivinhado, e o motivo é dito', await motivoDo(porNome('dois-opf.epub')));
ok((await motivoDo(porNome('ruim.epub'))) === 'pacote ilegível', 'pacote que não abre: ilegível, e o arquivo fica em paz', await motivoDo(porNome('ruim.epub')));
ok(await motivoDo(porNome('livro.epub.pdf')) === 'não é EPUB nem CBZ', 'PDF não é aberto, e a razão é dita', await motivoDo(porNome('livro.epub.pdf')));

console.log('CBZ');
ok(await escolhido(porNome('ordem.cbz')) === '001.jpg', 'a primeira imagem da história, na ordem dos números (001 antes de 010)', await escolhido(porNome('ordem.cbz')));
ok(await escolhido(porNome('anunciada.cbz')) === 'cover.png', 'uma imagem que se anuncia como capa vem antes da primeira página', await escolhido(porNome('anunciada.cbz')));
ok(await escolhido(porNome('pastas.cbz')) === '002.png', 'CBZ em pastas: a primeira imagem da primeira pasta, em ordem', await escolhido(porNome('pastas.cbz')));
ok(await escolhido(porNome('so-texto.cbz')) === null, 'CBZ sem imagem: devolve nada', await escolhido(porNome('so-texto.cbz')));

console.log('O QUE NÃO É LIVRO DIGITAL');
for (const nome of ['ruim.epub', 'truncado.epub', 'normal.zip', 'livro.epub.pdf'])
  ok(await escolhido(porNome(nome)) === null, 'pacote que não dá para ler não vira erro nem aviso: ' + nome);
ok(rede === 0, 'nada foi buscado na internet ao ler os pacotes', rede);

/* ---------- ler só o que interessa ---------- */
console.log('SÓ OS PEDAÇOS NECESSÁRIOS');
const g = porNome('grande.epub');
const achada = await M.capaDoDigital(g);
const lido = g.__fatias.reduce((s, [a, b]) => s + (b - a), 0);
ok(achada && achada.nome === 'pesado.png', 'a capa é achada num EPUB de vários megabytes', achada && achada.nome);
ok(g.size > 5 * 1048576 && lido < 200000, `o arquivo tem ${(g.size / 1048576).toFixed(1)} MB e foram lidos ${(lido / 1024).toFixed(0)} KB — nada é carregado inteiro`, [g.size, lido]);
ok(g.__fatias.every(([a, b]) => b - a <= 66000), 'nenhuma leitura passa de uma janela pequena', g.__fatias.map(([a, b]) => b - a));
const v = new Uint8Array(bytesDo('properties.epub'));
const f = M.fonteDe(v);
const lista = await M.listarZip(f);
ok(lista.length === 7 && lista.some(e => e.nome === 'OEBPS/imagens/a capa.png') && lista.every(e => e.tam > 0),
   'o índice do pacote é lido inteiro: sete arquivos, com nome, tamanho e posição', lista.map(e => [e.nome, e.tam, e.metodo]));
ok(lista.find(e => e.nome === 'OEBPS/imagens/a capa.png').metodo === 0 && lista.find(e => e.nome === 'OEBPS/cap1.xhtml').metodo === 8,
   'os dois jeitos de guardar são entendidos: sem compressão (stored) e comprimido (deflate)');
const lida = await M.bytesDaEntrada(f, lista.find(e => e.nome === 'OEBPS/imagens/a capa.png'));
ok(lida && Buffer.from(lida).equals(fs.readFileSync(path.join(FIX, 'esperado.png'))), 'a imagem que sai do pacote é a que foi posta nele, byte a byte');
const textoOpf = await M.textoDaEntrada(f, lista.find(e => e.nome.endsWith('.opf')));
ok(/cover-image/.test(textoOpf) && textoOpf.length > 100, 'um texto do pacote (o índice) é lido descomprimido', textoOpf.length);
ok(await M.bytesDaEntrada(f, { nome: 'x.png', metodo: 0, tam: 20 * 1048576, ini: 0 }) === null, 'um bloco declarado com mais de 16 MB é recusado antes de ser lido');
ok(await M.bytesDaEntrada(f, { nome: 'x.png', metodo: 99, tam: 10, ini: lista[0].ini }) === null, 'compressão que não é stored nem deflate: nada é lido');
ok(await M.bytesDaEntrada(f, { nome: 'x.png', metodo: 8, tam: 10, ini: lista[0].ini + 3 }) === null, 'posição que não é o começo de um cabeçalho local: nada é lido');
ok(await M.bytesDaEntrada(f, { nome: 'x.png', metodo: 0, tam: v.length * 3, ini: lista[0].ini }) === null, 'tamanho que o arquivo não confirma (pacote truncado): nada é lido');
ok((await M.listarZip(M.fonteDe(new Uint8Array(bytesDo('truncado.epub'))))).length === 0, 'pacote sem o índice do fim: a lista vem vazia');
ok(M.caminhoRelativo('Livro/a.opf', 'img/../imagens/capa%20grande.png') === 'Livro/imagens/capa grande.png',
   'caminho relativo: a pasta do índice, o ".." e o %20', M.caminhoRelativo('Livro/a.opf', 'img/../imagens/capa%20grande.png'));
ok(M.caminhoRelativo('Livro/miolo/c.opf', '../../imagens/acima.png') === 'imagens/acima.png',
   'dois ".." sobem as duas pastas do índice e param na raiz do pacote', M.caminhoRelativo('Livro/miolo/c.opf', '../../imagens/acima.png'));
ok(M.caminhoRelativo('a/opf.opf', 'https://x.com/capa.png') === '' && M.caminhoRelativo('a/opf.opf', '') === '',
   'endereço de fora e referência vazia não viram caminho');
ok(M.capaAnunciadaEpub('<package><manifest>' + '<item id="c" href="c.png" media-type="image/svg+xml"/><item id="h" href="c.html" media-type="text/html"/>' + '</manifest></package>', 'a.opf') === '',
   'item de texto ou de SVG não é capa');
ok(M.capaDoCbz(['z/002.jpg', 'a/010.jpg', 'a/003.jpg']) === 'a/003.jpg', 'CBZ: os números do nome são entendidos como números', M.capaDoCbz(['z/002.jpg', 'a/010.jpg', 'a/003.jpg']));
ok(M.capaDoCbz(['notas.txt', 'info.json']) === '', 'CBZ: nada que não seja imagem entra na conta');
ok(M.DIGITAL_CAPA.test('Livro.EPUB') && M.DIGITAL_CAPA.test('hq.CBZ') && !M.DIGITAL_CAPA.test('livro.pdf') && !M.DIGITAL_CAPA.test('capa.epub.png'),
   'pelo nome, só .epub e .cbz — e nada que só pareça');

/* ---------- a ficha: anexar arquivo e capa ---------- */
const novoLivro = (id, extra) => { const b = Object.assign({ id, t: 'Título ' + id, a: 'Autor', tags: [], leit: '', notas: {}, u: 0 }, extra || {}); DB.livros.push(b); return b; };
async function anexa(livro, arq, antes) {
  banco.clear(); M.Anexos.capas.clear(); avisos = []; desenhos = 0;
  if (antes) antes();
  M.Notas.id = livro.id;
  await M.Notas.anexar(arq);
  return { livro, avisos: avisos.slice(), banco: [...banco.values()] };
}

console.log('ANEXAR UM EPUB A UM LIVRO SEM CAPA');
let r = await anexa(novoLivro('a1'), porNome('meta.epub'));
let capa = r.banco.find(x => x.tipo === 'capa');
ok(r.avisos[r.avisos.length - 1] === 'Arquivo anexado. A capa que estava dentro do arquivo virou a capa do livro.',
   'a ficha diz o que aconteceu, sem falar em análise', r.avisos);
ok(r.banco.filter(x => x.tipo === 'arquivo').length === 1 && r.banco.find(x => x.tipo === 'arquivo').nome === 'meta.epub',
   'o arquivo continuou sendo anexado do jeito de sempre', r.banco.map(x => [x.tipo, x.nome]));
ok(!!r.livro.cp && capa && capa.livro === 'a1' && capa.nome === 'capa de frente.png' && capa.mime === 'image/jpeg',
   'a imagem é gravada como capa enviada, ligada ao livro', capa && { nome: capa.nome, mime: capa.mime, livro: capa.livro });
ok(canvasVisto && canvasVisto.width === 360 && canvasVisto.height === 540, 'ela passou pelo reduzidor da "Enviar capa…": 600 × 900 viraram 360 × 540', canvasVisto);
ok(M.Anexos.capas.get(r.livro.cp) === capa.dados && /^data:image\/jpeg;base64,/.test(capa.dados) && capa.tam > 0,
   'a capa vai para a memória (a tela a desenha sem esperar) e para o banco do navegador', capa && capa.tam);
ok(capa.tam === Math.round((capa.dados.length - 23) * 0.75), 'o tamanho anotado é o da imagem reduzida, não o do arquivo', capa.tam);
ok(desenhos === 1, 'a tela é redesenhada uma vez, com a capa já no lugar', desenhos);

console.log('O EPUB DE 4 MB: GRANDE DEMAIS PARA GUARDAR, BOM DEMAIS PARA IGNORAR');
r = await anexa(novoLivro('a6'), porNome('grande.epub'));
capa = r.banco.find(x => x.tipo === 'capa');
ok(r.banco.filter(x => x.tipo === 'arquivo').length === 0, 'o arquivo não é guardado (passa do limite), mas nada é recusado em silêncio', r.banco.map(x => [x.tipo, x.nome]));
ok(!!r.livro.cp && !!capa && /grande demais/.test(r.avisos[0]) && /capa dele foi lida/.test(r.avisos[0]),
   'a capa é lida do arquivo grande e o aviso explica os dois lados', r.avisos);

console.log('A MARCA "POSSUI ANÁLISE"');
r = await anexa(novoLivro('a7'), porNome('meta.epub'));
ok(!r.livro.tags.includes('analise'), 'anexar o próprio livro digital não marca "possui análise"', r.livro.tags);
r = await anexa(novoLivro('a8'), { name: 'resenha.txt', size: 80, type: 'text/plain', arrayBuffer: async () => new ArrayBuffer(80) });
ok(r.livro.tags.includes('analise') && r.avisos[0] === 'Arquivo anexado. O livro foi marcado com “possui análise”.',
   'um arquivo seu (resenha, relatório) continua marcando', [r.livro.tags, r.avisos]);
r = await anexa(novoLivro('a9'), { name: 'fichamento.pdf', size: 80, type: 'application/pdf', arrayBuffer: async () => new ArrayBuffer(80) });
ok(r.livro.tags.includes('analise'), 'um PDF anexado continua sendo um documento seu: marca', r.livro.tags);
r = await anexa(novoLivro('b0'), porNome('grande.epub'), () => { novoLivro('ignorado'); });
r = await anexa(novoLivro('b9'), porNome('meta.epub'), () => { });
ok(r.livro.cp, 'o livro sem capa anexado de novo também ganha a sua', r.livro.cp);
const cheio = novoLivro('c0', { anx: Array.from({ length: 8 }, (_, i) => ['k' + i, 'nota-' + i + '.md', 10, 20261112, 'text/markdown']) });
r = await anexa(cheio, porNome('meta.epub'));
ok(cheio.anx.length === 8 && !r.banco.some(x => x.tipo === 'arquivo' && x.nome === 'meta.epub') && !!cheio.cp &&
   /já guarda 8 arquivos/.test(r.avisos[0]),
   'com os oito arquivos cheios, o arquivo não entra — a capa, sim, e o aviso diz isso', [cheio.anx.length, r.avisos]);

console.log('OUTRAS IMAGENS E OUTROS LIVROS');
imagem = { w: 900, h: 600 };
r = await anexa(novoLivro('a2'), porNome('nome.epub'));
ok(canvasVisto.width === 360 && canvasVisto.height === 240, 'imagem larga é reduzida para caber em 360 × 540 sem deformar', canvasVisto);
imagem = { w: 600, h: 900 };
r = await anexa(novoLivro('a3'), porNome('sem-capa.epub'));
ok(!r.livro.cp && !r.banco.some(x => x.tipo === 'capa') && r.avisos[r.avisos.length - 1] === 'Arquivo anexado.',
   'EPUB sem capa: o arquivo é anexado, nada muda na ficha e nenhum aviso é dado', r.avisos);
r = await anexa(novoLivro('a4'), porNome('so-texto.cbz'));
ok(!r.livro.cp && r.banco.length === 1, 'CBZ sem imagem: mesma coisa — o arquivo entra, a capa fica como está', r.banco.map(x => x.tipo));
r = await anexa(novoLivro('a5'), porNome('ordem.cbz'));
ok(!!r.livro.cp && r.banco.find(x => x.tipo === 'capa').nome === 'capa de 001.jpg', 'CBZ anexado também ganha a capa do arquivo', r.banco.map(x => [x.tipo, x.nome]));

console.log('O QUE NÃO É TROCADO');
r = await anexa(novoLivro('b1', { cp: 'chave-velha' }), porNome('meta.epub'), () => banco.set('chave-velha', { k: 'chave-velha', livro: 'b1', tipo: 'capa', dados: 'data:image/jpeg;base64,VELHA' }));
ok(r.livro.cp === 'chave-velha' && !r.banco.some(x => x.tipo === 'capa' && x.k !== 'chave-velha') && !r.avisos.some(a => a.includes('virou a capa do livro')),
   'a capa que o usuário enviou continua no lugar (e não se acumula uma segunda, nem se fala dela)', [r.livro.cp, r.avisos]);
r = await anexa(novoLivro('b2', { _img: 12345 }), porNome('meta.epub'));
ok(!r.livro.cp && r.banco.filter(x => x.tipo === 'capa').length === 0, 'livro que já tem capa no catálogo não ganha a do arquivo', r.livro.cp);
r = await anexa(novoLivro('b3'), porNome('livro.epub.pdf'));
ok(!r.livro.cp && r.livro.tags.includes('analise') && r.avisos[0] === 'Arquivo anexado. O livro foi marcado com “possui análise”.',
   'PDF: não é aberto como pacote, e continua marcando "possui análise" (pode ser um documento seu)', r.avisos);

console.log('AS DUAS CORRIDAS');
const c1 = novoLivro('c1');
banco.clear(); M.Anexos.capas.clear(); avisos = []; desenhos = 0; M.Notas.id = c1.id;
await M.Notas.anexar({ name: 'meta.epub', size: 1000, type: '', arrayBuffer: async () => { DB.livros.splice(DB.livros.findIndex(b => b.id === 'c1'), 1); const s = bytesDo('meta.epub'), fora = new ArrayBuffer(s.length); new Uint8Array(fora).set(s); return fora; } });
await espera();
ok(banco.size === 0 && desenhos === 0 && !avisos.length,
   'se o livro saiu do painel enquanto o arquivo era lido, nada fica gravado, nada é redesenhado e nenhum aviso é dado', [banco.size, desenhos, avisos]);
const e1 = novoLivro('e1');
banco.clear(); M.Anexos.capas.clear(); avisos = []; desenhos = 0; M.Notas.id = e1.id;
await M.Notas.anexar({ name: 'meta.epub', size: 1000, type: '', arrayBuffer: async () => {
  e1.cp = 'de-fora'; banco.set('de-fora', { k: 'de-fora', livro: 'e1', tipo: 'capa', dados: 'data:image/jpeg;base64,FORA' });
  const s = bytesDo('meta.epub'), fora = new ArrayBuffer(s.length); new Uint8Array(fora).set(s); return fora;
} });
await espera();
ok(e1.cp === 'de-fora' && [...banco.values()].filter(x => x.tipo === 'capa').length === 1,
   'se o usuário enviou uma capa durante a leitura, a extraída não é gravada nem anunciada', [e1.cp, [...banco.keys()]]);

console.log('ENVIAR CAPA (o mesmo caminho de gravação)');
const d1 = novoLivro('d1');
banco.clear(); M.Anexos.capas.clear(); avisos = []; M.Notas.id = d1.id;
await M.Notas.enviarCapa({ name: 'minha.png', size: 10, type: 'image/png', arrayBuffer: async () => new ArrayBuffer(10) });
const primeira = d1.cp;
ok(!!primeira && avisos[0] === 'Capa enviada.' && banco.get(primeira).nome === 'minha.png', 'enviar a capa continua igual: grava, avisa e mostra', [avisos, primeira]);
await M.Notas.enviarCapa({ name: 'outra.png', size: 10, type: 'image/png', arrayBuffer: async () => new ArrayBuffer(10) });
await espera();
ok(d1.cp !== primeira && banco.get(d1.cp).nome === 'outra.png' && !banco.get(primeira) && avisos[1] === 'Capa trocada.',
   'trocar a capa: a nova entra no lugar da antiga, que sai do banco', [d1.cp, [...banco.keys()]]);
M.Notas.id = null;
ok(rede === 0, 'nada foi buscado na internet no fluxo da ficha', rede);

/* ---------- a varredura da pasta ---------- */
console.log('A PASTA PERCORRIDA');
ok(M.chaveDeNome('03 - A Cura de Schopenhauer.epub') === 'a cura de schopenhauer', 'numeração de edição sai do caminho', M.chaveDeNome('03 - A Cura de Schopenhauer.epub'));
ok(M.chaveDeNome('Tartarugas Ninja 001 (2019).cbz') === 'tartarugas ninja', 'número no fim e o ano entre parênteses também', M.chaveDeNome('Tartarugas Ninja 001 (2019).cbz'));
ok(M.chaveDeNome('v02 O Nome da Rosa.CBZ') === 'o nome da rosa', 'prefixo de volume, e a grafia que for', M.chaveDeNome('v02 O Nome da Rosa.CBZ'));
const prateleira = [
  novoLivro('p1', { t: 'A Cura de Schopenhauer' }),
  novoLivro('p2', { t: 'O Nome da Rosa' }),
  novoLivro('p3', { t: 'Tartarugas Ninja' }),
  novoLivro('p4', { t: 'Ecce Homo' }),
  novoLivro('p5', { t: 'Quando Nietzsche Chorou' }),
  novoLivro('p6', { t: 'A Cura de Schopenhauer' }),        // homônimo: ambíguo de propósito
  novoLivro('p7', { t: 'Um Livro Que Ninguém Tem', _img: 999 }),   // já tem capa no catálogo
  novoLivro('p8', { t: 'Série Nova' }),
];
const arquivo = caminho => Object.assign(arquivoFake(/\.cbz$/i.test(caminho) ? 'ordem.cbz' : 'meta.epub'), { name: caminho.split('/').pop(), webkitRelativePath: caminho });
const lote = [
  arquivo('Biblioteca/03 - A Cura de Schopenhauer.epub'),
  arquivo('Biblioteca/HQs/Tartarugas Ninja/Tartarugas Ninja 001 (2019).cbz'),
  arquivo('Biblioteca/v02 O Nome da Rosa.CBZ'),
  arquivo('Biblioteca/Ecce Homo - Friedrich Nietzsche.epub'),
  arquivo('Biblioteca/Quando Nietzsche Chorou (Nietzsche, Friedrich).epub'),
  arquivo('Biblioteca/Um Livro Que Ninguém Tem.epub'),
  arquivo('Biblioteca/A Série Nova 004.cbz'),
  arquivo('Biblioteca/Série Nova/A Série Nova 007.cbz'),
  arquivo('Biblioteca/Qualquer Coisa Totalmente De Fora.epub'),
  { name: 'contratapa.jpg', size: 400, type: 'image/jpeg' },
  { name: 'livro.epub.pdf', size: 900, type: 'application/pdf' },
  { name: 'Ecce Homo copia.epub', size: 0, type: '' },
];
const plano = M.planejarLote(lote, prateleira);
const porLivro = Object.fromEntries(plano.pares.map(p => [p.livro.t, p.arq.name]));
ok(plano.totais.digitais === 9 && plano.totais.arquivos === 12, 'só EPUB e CBZ com conteúdo entram na conta', plano.totais);
ok(!porLivro['A Cura de Schopenhauer'], 'título duplicado no catálogo: nenhum dos dois recebe a capa', Object.keys(porLivro));
ok(porLivro['Tartarugas Ninja'] === 'Tartarugas Ninja 001 (2019).cbz', 'edição dentro da pasta da série acha a série', porLivro);
ok(porLivro['O Nome da Rosa'] === 'v02 O Nome da Rosa.CBZ', 'CBZ com o nome em grafia mista e prefixo de volume', porLivro);
ok(porLivro['Ecce Homo'] === 'Ecce Homo - Friedrich Nietzsche.epub', 'título + autor no nome do arquivo é reconhecido (sem palpite: um só livro bate)', porLivro);
ok(porLivro['Quando Nietzsche Chorou'] === 'Quando Nietzsche Chorou (Nietzsche, Friedrich).epub', 'parênteses no nome não impedem o casamento', porLivro);
ok(plano.semLivro.some(x => /Qualquer Coisa/.test(x.nome)), 'nome que não bate com nada fica de fora, sem adivinhação', plano.semLivro);
ok(plano.ambigueis.length === 1 && /mais de um/.test(plano.ambigueis[0].motivo) && plano.ambigueis[0].nome === '03 - A Cura de Schopenhauer.epub',
   'título que bate em dois livros é deixado em paz, e o motivo fica registrado', plano.ambigueis);
ok(plano.pares.every(p => !p.livro._img) && plano.semLivro.some(x => x.nome === 'Um Livro Que Ninguém Tem.epub'),
   'livro que já tem capa do catálogo não é tocado: fica entre os que não acharam livro', plano.pares.map(p => p.livro.t));
ok(plano.semLivro.some(x => /Um Livro Que Ninguém Tem/.test(x.nome)) && !plano.comCapa.length, 'um nome fora do mapa é contado como sem livro, não como erro', plano.semLivro.map(x => x.nome));
ok(!plano.pares.some(p => p.livro.t === 'Série Nova' && p.arq.name !== 'A Série Nova 004.cbz'),
   'a primeira imagem da série fica; as outras edições são contadas à parte', plano.repetidos);
ok(plano.repetidos.length === 1 && plano.repetidos[0] === 'A Série Nova 007.cbz', 'a segunda edição da série é contada como repetida', plano.repetidos);
ok(plano.pares.length === 5, 'cinco livros aproveitados de uma vez', plano.pares.map(p => p.livro.t));

console.log('A VARREDURA NA TELA');
banco.clear(); M.Anexos.capas.clear(); avisos = []; gravacoes = 0; ltSt.textContent = '';
await M.LoteCapas.rodar(lote);
const gravadas = [...banco.values()].filter(x => x.tipo === 'capa');
ok(gravadas.length === 5 && gravadas.every(x => x.nome.startsWith('capa de ')) && [...banco.values()].every(x => x.tipo === 'capa'),
   'uma capa por livro reconhecido, e arquivo nenhum foi anexado', [gravadas.map(x => [x.livro, x.nome]), [...banco.keys()].length]);
ok(prateleira.filter(b => b.cp).length === 5 && prateleira.every(b => !b.tags.includes('analise')),
   'os cinco livros passam a ter capa, e nenhum é marcado como tendo análise', prateleira.map(b => [b.t, b.cp ? 'capa' : '-']));
ok(prateleira.filter(b => b.cp).every(b => b.u === 1), 'o livro com capa nova entra em "Editados por você"', prateleira.filter(b => b.cp).map(b => b.u));
ok(/5 capas encontradas em 5 arquivos lidos/.test(ltSt.textContent) && /exporte o backup/.test(ltSt.textContent), 'o quadro diz o resultado e lembra o backup', ltSt.textContent);
ok(avisos.length === 1 && /5 capas encontradas/.test(avisos[0]) && /mais de um livro/.test(avisos[0]),
   'e o aviso de canto resume, contando inclusive o que foi deixado em paz', avisos);
ok(gravacoes >= 1 && M.LoteCapas.emCurso === false, 'os dados são gravados e a varredura se declara terminada', gravacoes);
ok(rede === 0, 'a varredura inteira não fez nenhuma requisição', rede);
banco.clear(); avisos = []; dlgAberto = null;
await M.LoteCapas.rodar([{ name: 'qualquer.txt', size: 10 }]);
ok(avisos.length === 1 && /Nenhum EPUB ou CBZ na pasta/.test(avisos[0]) && dlgAberto === null,
   'pasta sem livro digital: só o aviso, sem abrir quadro nenhum', avisos);
banco.clear(); avisos = [];
await M.LoteCapas.rodar([{ name: 'Desconhecido Totalmente.xyz.epub', size: 1000, slice: (a, b) => ({ arrayBuffer: async () => new ArrayBuffer(0) }) }]);
ok(avisos.length === 1 && /nenhum corresponde a um dos/.test(avisos[0]) && /inventario[.]tsv/.test(avisos[0]),
   'nada reconhecido entre os livros sem capa: o aviso explica e aponta a lista', avisos);

/* ---------- o mapa do inventário: o que o nome do arquivo não diz, a lista dele diz ---------- */
console.log('O MAPA DO INVENTARIO');
DB.livros.length = 0;
const estante = [
  novoLivro('c0', { t: 'A Física da Alma', a: 'Amit Goswami' }),                 // nome truncado e sujo: só o mapa casa
  novoLivro('c1', { t: 'A Mente e o Cérebro' }),                                  // casamento exato pelo título
  novoLivro('c2', { t: 'A Mente' }),                                              // não leva nada: o outro bate inteiro
  novoLivro('c3', { t: 'Chakras e Mediunidade' }),                                // título dentro do nome do arquivo
  novoLivro('c4', { t: 'As Grandes Histórias da Mitologia', _img: 777 }),          // já tem capa: nada é trocado
  novoLivro('c5', { t: 'Psicologia da Inteligência' }),
  novoLivro('c6', { t: 'Psicologia das Massas' }),
  novoLivro('c7', { t: 'O Livro Sem Capa Dentro' }),                             // casado, mas o pacote não traz capa
];
const sujo = (nome, pasta, pacote) => Object.assign(arquivoFake(pacote || (/\\.cbz$/i.test(nome) ? 'ordem.cbz' : 'meta.epub')),
  { name: nome, webkitRelativePath: pasta + '/' + nome });
mapaDoInventario[norm('A Fisica d - Amit Goswami (z-library.sk, 1lib.sk, z-lib.sk).epub')] = 0;
mapaDoInventario[norm('box trilogia kingsbridge os pilares da terra (ken follett).epub')] = 4;
mapaDoInventario[norm('o livro sem capa dentro (autoria desconhecida).epub')] = 7;
const loteInv = [
  sujo('A Fisica d - Amit Goswami (z-library.sk, 1lib.sk, z-lib.sk).epub', 'Religião, Espiritualidade e Mitologia'),
  sujo('A Mente e o Cérebro.epub', 'psicologia'),
  sujo('Apostila de Chakras e Mediunidade (autoria desconhecida).epub', 'psicologia'),
  sujo('Algum Livro Qualquer de Uma Pasta Cheia de Mentes.epub', 'psicologia'),
  sujo('box trilogia kingsbridge os pilares da terra (ken follett).epub', 'Religião, Espiritualidade e Mitologia'),
  sujo('o livro sem capa dentro (autoria desconhecida).epub', 'psicologia', 'sem-capa.epub'),   // casou, mas o pacote não traz capa
];
const planoInv = M.planejarLote(loteInv, DB.livros);
const porIdInv = Object.fromEntries(planoInv.pares.map(p => [p.livro.id, p.arq.name]));
ok(planoInv.pares.length === 4 && porIdInv.c0 && porIdInv.c1 && porIdInv.c3 && porIdInv.c7,
   'quatro livros aproveitados: o mapa reconhece o nome truncado, e o título continua valendo', planoInv.pares.map(p => p.livro.id));
ok(planoInv.pares.filter(p => p.certo).length === 2, 'dois vieram direto da lista da biblioteca virtual, sem palpite', planoInv.pares.filter(p => p.certo).map(p => p.livro.id));
ok(planoInv.ambigueis.length === 0, 'a categoria da prateleira não vira ambiguidade: "psicologia" deixa de casar com tudo que começa por "Psicologia…"', planoInv.ambigueis);
ok(planoInv.semLivro.length === 1 && /Algum Livro Qualquer/.test(planoInv.semLivro[0].nome) && /nenhum livro sem capa/.test(planoInv.semLivro[0].motivo),
   'o que não está no mapa e não bate com nenhum título fica em paz, contado como está', planoInv.semLivro);
ok(planoInv.comCapa.length === 1 && /box trilogia/.test(planoInv.comCapa[0]) && !planoInv.pares.some(p => p.livro.id === 'c4'),
   'livro que já tem capa é reconhecido pelo nome e não é tocado', [planoInv.comCapa, Object.keys(porIdInv)]);
ok(estante.filter(b => b.id === 'c2').every(b => !b.cp) && !planoInv.pares.some(p => p.livro.id === 'c2'),
   'o título que é pedaço de outro não leva a capa do vizinho', planoInv.pares.map(p => p.livro.id));

console.log('O RESUMO POR ESTAGIO');
banco.clear(); M.Anexos.capas.clear(); avisos = []; ltSt.textContent = ''; ltFora.hidden = true; ltFora.innerHTML = '';
await M.LoteCapas.rodar(loteInv);
ok(/3 capas encontradas em 4 arquivos lidos/.test(ltSt.textContent) && !/4 capas/.test(ltSt.textContent),
   'o quadro separa o que foi lido do que virou capa', ltSt.textContent);
ok(/1 arquivo · sem capa dentro/.test(ltSt.textContent), 'a varredura diz quantos casaram mas não traziam capa', ltSt.textContent);
ok(/1 arquivo de livro que já tem capa/.test(ltSt.textContent),
   'e diz os que já tinham capa, sem misturar as duas coisas', ltSt.textContent);
ok(/fora, sem livro certo/.test(ltFora.innerHTML) && /Algum Livro Qualquer/.test(ltFora.innerHTML),
   'os nomes que não soubemos ligar a um livro aparecem, para a lista ser corrigida', ltFora.innerHTML);
ok([...banco.values()].filter(x => x.tipo === 'capa').length === 3 && estante.filter(b => b.cp).length === 3,
   'as três capas do lote do inventário são gravadas, e mais nada', [banco.size, estante.filter(b => b.cp).map(b => b.id)]);
ok(estante.find(b => b.id === 'c4')._img === 777 && !estante.find(b => b.id === 'c4').cp, 'a capa que já estava lá continua a mesma', estante.find(b => b.id === 'c4')._img);

/* um pacote cuja imagem o navegador não abre: o estágio diz isso, e o livro fica sem capa como estava */
console.log('A IMAGEM QUE NÃO ABRE');
const antes = imagem; imagem = { w: 0, h: 0 };
DB.livros.forEach(b => { b.cp = ''; });          // a estante volta ao estado de antes: o que se testa aqui é o que acontece quando a imagem não abre
banco.clear(); M.Anexos.capas.clear(); avisos = []; ltSt.textContent = '';
await M.LoteCapas.rodar([sujo('A Mente e o Cérebro.epub', 'psicologia')]);
imagem = antes;
ok(/0 capas encontradas em 1 arquivo lido/.test(ltSt.textContent) && /1 arquivo · imagem que não abriu/.test(ltSt.textContent),
   'imagem que não abre é contada como tal, e não como "nenhum livro"', ltSt.textContent);
ok(banco.size === 0 && !estante.find(b => b.id === 'c2').cp, 'e o livro fica sem capa, como estava', [banco.size, estante.find(b => b.id === 'c2').cp]);


console.log('ERROS: ' + erros.length);
for (const e of erros) console.log('   ' + e);
process.exit(erros.length ? 1 : 0);
'''

(PACOTE / 'harness.mjs').write_text(HARNESS, encoding='utf-8')

print('RODANDO O JAVASCRIPT DO PAINEL NO NODE')
node = shutil.which('node')
if not node:
    print('  (pulado: o Node não está neste computador — sem ele a parte executada do teste não roda)')
else:
    r = subprocess.run([node, str(PACOTE / 'harness.mjs'), str(RAIZ), str(FIX)], capture_output=True, text=True, timeout=600)
    saida = (r.stdout or '') + (('\n' + r.stderr) if r.stderr.strip() else '')
    print(saida.rstrip())
    confere(r.returncode == 0 and bool(re.search(r'^ERROS: 0$', saida, flags=re.M)), 'o JavaScript do painel extrai a capa, faz a ficha e percorre a pasta', (r.returncode, saida[-900:]))
    n = len([l for l in saida.splitlines() if l.startswith(('ok', 'FALHOU'))])
    confere(n >= 110, 'a checagem executou as %d previsões do teste (pacote, ficha e pasta)' % n, n)

print('O QUE FICA NO ARQUIVO (o desenho do fluxo)')
mod = (RAIZ / 'src' / 'js' / '54-capa-digital.js').read_text(encoding='utf-8')
anx = (RAIZ / 'src' / 'js' / '55-anexos.js').read_text(encoding='utf-8')
lote = (RAIZ / 'src' / 'js' / '56-lote-capas.js').read_text(encoding='utf-8')
pai = (RAIZ / 'src' / 'js' / '60-drawer.js').read_text(encoding='utf-8')
confere("const DIGITAL_CAPA = /\\.(epub|cbz)$/i;" in mod, 'só EPUB e CBZ são abertos — PDF fica de fora, como combinado')
confere(not re.search(r'\bfetch\s*\(|XMLHttpRequest|document\.|window\.|localStorage|indexedDB', mod),
        'o módulo que abre o pacote não toca a tela, nem o armazenamento, nem a internet: é por isso que dá para testá-lo sem navegador')
confere('catch (err) { return null; }' in mod, 'o que der errado no pacote devolve nada, em silêncio')
confere('const janela = Math.min(f.tam, 66000)' in mod and 'e.tam > LIM_PACOTE' in mod,
        'a leitura é por fatias: a cauda, o índice e a entrada da capa — nunca o arquivo inteiro')
confere('if (b.cp || temCapa(b) || !DIGITAL_CAPA.test(arq.name' in anx,
        'a capa do arquivo só entra quando o livro não tem capa nenhuma (nem enviada, nem do catálogo)')
trecho = anx[anx.index('async anexar(arq)'):anx.index('async capaDoArquivoDigital')]
confere('if (fora && !(digital && !vazio))' in trecho and "const capa = await this.capaDoArquivoDigital(arq, b);" in trecho,
        'um EPUB/CBZ acima do limite de anexação continua dando a capa, sem guardar o arquivo')
confere("const LIVRO_DIGITAL = /\\.(epub|cbz|cbr|mobi|azw3|azw|djvu|fb2|lit)$/i;" in anx and 'pdf' not in anx.split('LIVRO_DIGITAL = ')[1].split('\n')[0],
        'PDF continua marcando (pode ser documento seu); os formatos que são sempre o livro, não')
confere('const marcou = anexado && !LIVRO_DIGITAL.test(nome)' in anx and 'if (marcou) defTag(b, TAG_ANALISE, true);' in anx,
        'anexar o próprio livro digital não marca "possui análise"; um arquivo seu, sim')
confere('if (!anexado && !virouCapa)' in anx, 'quando nada entra, o motivo é dito com as palavras de sempre')
confere("const [kc] = await this.gravarCapa(b, capa.dados, capa.nome);" in anx and 'if (kc && b.cp) Anexos.apagar([kc]).catch(() => {});' in anx,
        'a capa extraída é gravada pelo mesmo caminho da capa enviada, e não entra se o livro ganhou uma entretanto')
confere(anx.count('async gravarCapa(b, dados, nome)') == 1 and "await this.gravarCapa(b, dados, arq.name || 'capa')" in anx,
        '"Enviar capa…" e a capa do arquivo usam a mesma gravação — não há segunda maneira de guardar uma capa')
confere("const LOTE_MAX = 400;" in lote and 'plano.pares.slice(0, LOTE_MAX)' in lote,
        'a varredura tem limite por execução (o backup cresce com as capas)')
confere(not re.search(r'\bfetch\s*\(|XMLHttpRequest|localStorage|indexedDB|tipo:\s*\'arquivo\'', lote),
        'a varredura não vai à internet, não grava nada direto e não anexa arquivo nenhum')
confere('if (p.livro.cp) continue;' in lote and 'marcarMeu(p.livro); feitos.push' in lote,
        'quem já ganhou capa é pulado, e o livro com capa nova passa a ser "do usuário"')
confere("!this.st || !this.st.isConnected" in lote, 'fechar o quadro interrompe a varredura: nada continua às escondidas')
confere('data-x="lote"' in pai and 'Buscar capas numa pasta de arquivos…' in pai and "LoteCapas.escolher()" in pai,
        'o botão está no quadro "Seus dados", junto das capas')
confere('Este navegador não permite escolher uma pasta inteira' in lote,
        'num navegador sem escolha de pasta, o caminho da ficha continua indicado')
confere('54-capa-digital' in (RAIZ / 'README.md').read_text(encoding='utf-8') and '56-lote-capas' in (RAIZ / 'README.md').read_text(encoding='utf-8'),
        'o README conhece os módulos novos')

# ─────────── o mapa dos nomes: o contrato entre o inventário, o gerador e o painel ───────────
print('O MAPA DOS NOMES (inventário → src/digitais.json → painel)')
norm_js = lambda s: ''.join(c for c in unicodedata.normalize('NFD', s) if not '\u0300' <= c <= '\u036f').lower()
mapa = json.loads((RAIZ / 'src' / 'digitais.json').read_text(encoding='utf-8'))
cat = json.loads((RAIZ / 'src' / 'catalog.json').read_text(encoding='utf-8'))
capas = json.loads((RAIZ / 'src' / 'capas.json').read_text(encoding='utf-8'))
linhas = [l.split('\t') for l in (RAIZ / 'biblioteca-virtual' / 'inventario.tsv').read_text(encoding='utf-8').splitlines()[1:]]
reais = {norm_js(r[1]).strip() for r in linhas if len(r) > 2 and r[2].lower() in ('epub', 'cbz')}
confere(len(mapa) > 250 and set(mapa) <= reais,
        'todo nome do mapa é um arquivo que existe na biblioteca virtual, grafado como o painel o normaliza', len(mapa))
confere(all(k == norm_js(k).strip() for k in mapa), 'as chaves já estão na forma que o norm do painel produz (passar o norm duas vezes não muda nada)')
confere(all(k.endswith(('.epub', '.cbz')) for k in mapa), 'só EPUB e CBZ entram no mapa: PDF e os outros formatos ficam de fora')
confere(all(isinstance(v, int) and 0 <= v < len(cat) and not capas[v] for v in mapa.values()),
        'o mapa só aponta para linhas do catálogo que ainda não têm capa — por isso o lote não encosta em quem já tem')
html = (RAIZ / 'Biblioteca_Lucas_Dashboard.html').read_text(encoding='utf-8')
confere('const DIGITAIS_NOMES = ' + json.dumps(mapa, ensure_ascii=False, separators=(',', ':')) + ';' in html,
        'o painel embute o mapa inteiro: nada é lido do disco nem da internet na hora de reconhecer um arquivo')
confere("const mapa = (typeof DIGITAIS_NOMES === 'object' && DIGITAIS_NOMES) || {};" in lote and 'const i = mapa[norm(base)];' in lote,
        'a varredura consulta o mapa pelo nome do arquivo, antes de qualquer heurística')
confere('nunca pelo nome da pasta' in lote and 'const c = chavesDoArquivo[0];' in lote,
        'a fase de "um título dentro do outro" olha só o nome do arquivo: a pasta é categoria de prateleira')
confere("if (l.length > 1 && !motivo) motivo =" in lote,
        'um nome ambíguo não descarta o que a outra chave teria casado limpo')
confere("return { blob: new Blob([dados], { type: tipo }), nome: soNomeDoCaminho(e.nome) };" in mod and "if (!alvo) return vazias;" in mod,
        'o que não virou capa devolve o motivo, e é ele que o resumo conta')

shutil.rmtree(PACOTE, ignore_errors=True)
print('ERROS:', len(erros))
for e in erros:
    print('  ', e)
sys.exit(1 if erros else 0)
