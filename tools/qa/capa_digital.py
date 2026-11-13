"""A capa que vem dentro do arquivo: EPUB e CBZ abertos no navegador (src/js/54-capa-digital.js e 55-anexos.js).

O painel tira a imagem da capa do próprio livro digital quando o usuário anexa o arquivo — sem internet, no
computador dele. Este teste constrói EPUBs e CBZs de verdade (pacotes .zip com índice, imagens em PNG, caminhos com
"../", com "%20" e com acento) e roda contra eles o código que vai no painel, no Node, sem navegador:

  · EPUB: a capa é a anunciada no índice (`properties="cover-image"`, ou `<meta name="cover">` apontando para o item);
    sem anúncio, a que tem "capa"/"cover" no nome — e nunca a primeira imagem do miolo;
  · CBZ: a que se anuncia como capa; senão, a primeira imagem na ordem dos números (001 antes de 010);
  · o que não é .epub/.cbz não é tocado; pacote truncado, índice em ZIP64, imagem que não está no pacote, endereço
    externo ou SVG devolvem nada — em silêncio, sem erro e sem rede;
  · lida a imagem, o resto é o fluxo de sempre: a anexação do arquivo continua igual, e a capa só entra quando o livro
    não tem nenhuma (nem enviada, nem do catálogo). Ela passa pelo mesmo reduzidor da "Enviar capa…" e é gravada como
    capa enviada — vale com as capas desligadas, entra no backup e sai com "Tirar a capa enviada".

O JavaScript executado aqui é o dos arquivos do painel, lido como está no repositório (mesma ordem do gerador). O que
o Node não tem — a tela e o banco do navegador — é imitado pelo mínimo: uma imagem que abre com o tamanho pedido, um
canvas que devolve um JPEG falso e um IndexedDB de mentirinha numa Mapa. O teste falha se alguém tentar ir à internet.
"""
import pathlib, re, shutil, subprocess, sys, zipfile

QA = pathlib.Path(__file__).resolve().parent
RAIZ = QA.parent.parent
sys.path.insert(0, str(QA))
import caminhos                                    # noqa: E402
from relogio import png                            # noqa: E402

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


CAPA = png(20, 120, 200, 300, 420)         # 300 × 420: a capa
OUTRA = png(200, 30, 30, 80, 100)           # 80 × 100: qualquer outra imagem do pacote

print('OS PACOTES DE TESTE')
FIX.mkdir(parents=True, exist_ok=True)

# o índice anuncia a capa por <meta name="cover"> — e há uma imagem com "capa" no nome que NÃO é a capa, para
# conferir que a anúncio manda sobre o nome; a capa em si vem comprimida (deflate), como quase sempre
with zipfile.ZipFile(FIX / 'meta.epub', 'w') as z:
    esqueleto(z, manifest=item('img1', 'images/frente.png') + item('img2', 'images/capa-do-catalogo.png'),
              metas='<meta name="cover" content="img1"/>')
    gravar(z, 'OEBPS/images/frente.png', CAPA)
    gravar(z, 'OEBPS/images/capa-do-catalogo.png', OUTRA)
# o <meta name="cover"> de alguns geradores (Calibre e parentes) traz o NOME DO ARQUIVO, não o id do item — e há
# uma imagem com "capa" no nome que é do miolo: a anunciada tem de vencer
with zipfile.ZipFile(FIX / 'pelo-nome-do-arquivo.epub', 'w') as z:
    esqueleto(z, manifest=item('Image00001', 'images/frente.jpg', 'image/jpeg') + item('Image00002', 'images/capa-interior.png'),
              metas='<meta name="cover" content="frente.jpg"/>')
    gravar(z, 'OEBPS/images/frente.jpg', CAPA)
    gravar(z, 'OEBPS/images/capa-interior.png', OUTRA)
# properties="cover-image", atributos com aspa simples, caminho com %20, imagem guardada sem compressão e campos extras
with zipfile.ZipFile(FIX / 'properties.epub', 'w') as z:
    esqueleto(z, opf='OEBPS/meu livro.opf', manifest=item('i1', 'imagens/a%20capa.png', props='cover-image') + item('i2', 'imagens/mapa.png'))
    gravar(z, 'OEBPS/imagens/a capa.png', CAPA, comprimido=False, sistema=3)
    gravar(z, 'OEBPS/imagens/mapa.png', OUTRA)
# as duas maneiras de anunciar, apontando para imagens diferentes: properties vem primeiro
with zipfile.ZipFile(FIX / 'prioridade.epub', 'w') as z:
    esqueleto(z, manifest=item('a', 'images/pelo-nome.png') + item('b', 'images/anunciada.png', props='cover-image'),
              metas='<meta name="cover" content="a"/>')
    gravar(z, 'OEBPS/images/pelo-nome.png', OUTRA)
    gravar(z, 'OEBPS/images/anunciada.png', CAPA)
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
# o índice aponta para fora da pasta dele (../), e o pacote tem a imagem na raiz
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
# a capa anunciada é um SVG, e a que não está no pacote
with zipfile.ZipFile(FIX / 'svg.epub', 'w') as z:
    esqueleto(z, manifest=item('c', 'images/capa.svg', 'image/svg+xml'))
    gravar(z, 'OEBPS/images/capa.svg', b'<svg xmlns="http://www.w3.org/2000/svg"/>')
with zipfile.ZipFile(FIX / 'sumico.epub', 'w') as z:
    esqueleto(z, manifest=item('c', 'images/nao-existe.png'))
# CBZ: a ordem em que o pacote foi escrito é embaralhada, e a numeração é que manda
with zipfile.ZipFile(FIX / 'ordem.cbz', 'w') as z:
    for nome in ('010.jpg', '002.jpg', '001.jpg'):
        gravar(z, nome, CAPA if nome == '001.jpg' else OUTRA, sistema=3)
with zipfile.ZipFile(FIX / 'anunciada.cbz', 'w') as z:
    for nome in ('001.jpg', 'cover.png', 'pagina-02.jpg'):
        gravar(z, nome, CAPA if nome == 'cover.png' else OUTRA)
with zipfile.ZipFile(FIX / 'pastas.cbz', 'w') as z:
    for nome in ('História 2/001.jpg', 'História 1/003.jpg', 'História 1/002.png'):
        gravar(z, nome, CAPA if nome.endswith('002.png') else OUTRA)
with zipfile.ZipFile(FIX / 'so-texto.cbz', 'w') as z:
    gravar(z, 'info.txt', 'sem imagem aqui')
# pacotes que não dão
(FIX / 'ruim.epub').write_text('isto não é um pacote zip, de jeito nenhum', encoding='utf-8')
(FIX / 'truncado.epub').write_bytes((FIX / 'meta.epub').read_bytes()[:-60])
shutil.copy(FIX / 'anunciada.cbz', FIX / 'normal.zip')
shutil.copy(FIX / 'meta.epub', FIX / 'Capa MAIÚSCULA.EPUB')
(FIX / 'livro.epub.pdf').write_bytes(b'%PDF-1.4\n' + bytes(range(200)))
(FIX / 'esperado.png').write_bytes(CAPA)      # a mesma imagem que pomos dentro dos pacotes, para conferirmos byte a byte
print('  %d pacotes de teste prontos' % len(list(FIX.iterdir())))

HARNESS = r'''
/* O harness roda o JavaScript do painel de verdade: lê os dois módulos, junta-os na mesma ordem do gerador e os
   executa com o mínimo de tela imitada. Cada checagem imprime uma linha; a linha ERROS no fim é o que lê o tudo.py. */
import fs from 'node:fs';
import path from 'node:path';

const RAIZ = process.argv[2], FIX = process.argv[3];
const erros = [];
const ok = (cond, nome, extra) => { console.log((cond ? 'ok    ' : 'FALHOU') + ' ' + nome + (!cond && extra !== undefined ? ' — ' + JSON.stringify(extra).slice(0, 400) : '')); if (!cond) erros.push(nome); };

/* ---------- a tela e o banco imitados, o mínimo para o módulo rodar ---------- */
let imagem = { w: 600, h: 900 };                     // o tamanho natural que o navegador veria na imagem extraída
let canvasVisto = null;
const document = { createElement: () => (canvasVisto = { width: 0, height: 0, getContext: () => ({ fillStyle: '', fillRect() {}, imageSmoothingQuality: '', drawImage() {} }), toDataURL: () => 'data:image/jpeg;base64,QUVB' }) };
class Image { set src(_) { this.naturalWidth = imagem.w; this.naturalHeight = imagem.h; setTimeout(() => this.onload && this.onload(), 0); } }
const URL = { createObjectURL: () => 'blob:fake', revokeObjectURL() {} };
class FileReader { readAsDataURL() { this.result = 'data:application/octet-stream;base64,QUJB'; setTimeout(() => this.onload && this.onload(), 0); } }
let rede = 0;
globalThis.fetch = globalThis.XMLHttpRequest = function () { rede++; throw new Error('este teste não pode ir à internet'); };

const banco = new Map();                              // o IndexedDB de mentirinha: a tabela `anexos`, chave `k`
const pedido = resultado => ({ result: resultado });
const tabela = { put: r => { banco.set(r.k, r); return pedido(); }, get: k => pedido(banco.get(k) || null), delete: k => { banco.delete(k); return pedido(); },
                 clear: () => pedido(), getAllKeys: () => pedido([...banco.keys()]) };
const dbFalso = { transaction: () => { const tx = { objectStore: () => tabela }; setTimeout(() => tx.oncomplete && tx.oncomplete(), 0); return tx; } };

let livros = [], avisos = [], desenhos = 0;
const porId = id => livros.find(b => b.id === id) || null;
const tocar = b => { b.u = 1; desenhos++; };
const toast = m => avisos.push(m);
const render = () => {}, desenharGaveta = () => {}, $ = () => null, Gaveta = { id: null };
const defTag = (b, t, on) => { const i = b.tags.indexOf(t); if (on && i < 0) b.tags.push(t); if (!on && i >= 0) b.tags.splice(i, 1); };
const marcarMeu = () => {}, derivar = () => {}, salvar = () => {}, fInt = n => String(n), fDec = n => String(n);
const Loja = { ok: true }, DB = { hoje: 20261112, livros }, MAX_ANEXOS = 8, MAX_COMENTARIO = 5000, TAG_ANALISE = 'analise';
const temCapa = b => !!b._img;                         // como no painel: o catálogo diz se há capa (desligada ou não)

const fonte = ['54-capa-digital.js', '55-anexos.js'].map(f => fs.readFileSync(path.join(RAIZ, 'src', 'js', f), 'utf8')).join('\n');
const rodar = new Function('DB', 'porId', 'tocar', 'toast', 'render', 'desenharGaveta', 'Gaveta', '$', 'MAX_ANEXOS', 'MAX_COMENTARIO', 'TAG_ANALISE',
  'defTag', 'marcarMeu', 'derivar', 'salvar', 'fInt', 'fDec', 'Loja', 'temCapa', 'document', 'Image', 'URL', 'FileReader', 'bancoFalso',
  fonte + '\nAnexos.banco = Promise.resolve(bancoFalso); return { Notas, Anexos, capaDoDigital, listarZip, blocoDoZip, caminhoRelativo, capaAnunciadaEpub, capaDoCbz, reduzirImagem, DIGITAL_CAPA };');
const espera = () => new Promise(r => setTimeout(r, 60));
const any_virou = lista => lista.some(a => a.includes('virou a capa do livro'));
const M = rodar(DB, porId, tocar, toast, render, desenharGaveta, Gaveta, $, MAX_ANEXOS, MAX_COMENTARIO, TAG_ANALISE,
  defTag, marcarMeu, derivar, salvar, fInt, fDec, Loja, temCapa, document, Image, URL, FileReader, dbFalso);

const arquivoFake = nome => { const buf = fs.readFileSync(path.join(FIX, nome)); const ab = buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.length); return { name: nome, size: buf.length, type: '', arrayBuffer: async () => ab }; };
const escolhido = async nome => { const r = await M.capaDoDigital(arquivoFake(nome)); return r ? r.nome : null; };
/* ---------- o que o módulo escolhe ---------- */
console.log('EPUB');
ok(await escolhido('meta.epub') === 'frente.png', 'a capa é a imagem anunciada no índice (<meta name="cover">), não a que tem "capa" no nome', await escolhido('meta.epub'));
ok(await escolhido('pelo-nome-do-arquivo.epub') === 'frente.jpg', 'meta name="cover" apontando pelo nome do arquivo também é entendido', await escolhido('pelo-nome-do-arquivo.epub'));
ok(await escolhido('properties.epub') === 'a capa.png', 'properties="cover-image" é lido, com aspa simples, %20 e campos extras no índice', await escolhido('properties.epub'));
ok(await escolhido('prioridade.epub') === 'anunciada.png', 'anunciada de duas maneiras: properties vem antes do <meta name="cover">', await escolhido('prioridade.epub'));
ok(await escolhido('nome.epub') === 'COVER.JPG', 'sem anúncio no índice, vale a imagem com "cover" no nome', await escolhido('nome.epub'));
ok(await escolhido('sem-capa.epub') === null, 'EPUB com imagens só de miolo: nenhuma é escolhida (adivinhar seria pôr o miolo na capa)', await escolhido('sem-capa.epub'));
ok(await escolhido('para-cima.epub') === 'acima.png', 'índice apontando para fora da pasta (../../) é resolvido', await escolhido('para-cima.epub'));
ok(await escolhido('so-externo.epub') === null, 'capa apontando para um endereço de fora: nada é buscado', await escolhido('so-externo.epub'));
ok(await escolhido('opf-unico.epub') === 'capa.png', 'EPUB sem container.xml: havendo um único índice, ele é lido', await escolhido('opf-unico.epub'));
ok(await escolhido('dois-opf.epub') === null, 'EPUB sem container.xml e com dois índices: não adivinhamos qual é o livro', await escolhido('dois-opf.epub'));
ok(await escolhido('svg.epub') === null, 'capa anunciada em SVG: não serve, o navegador não a reduziria para o tamanho de capa', await escolhido('svg.epub'));
ok(await escolhido('sumico.epub') === null, 'a imagem anunciada não está no pacote: nada é feito', await escolhido('sumico.epub'));
ok(await escolhido('Capa MAIÚSCULA.EPUB') === 'frente.png', 'o nome do livro digital vale em qualquer grafia e com espaço (Capa MAIÚSCULA.EPUB)', await escolhido('Capa MAIÚSCULA.EPUB'));

console.log('CBZ');
ok(await escolhido('ordem.cbz') === '001.jpg', 'a primeira imagem da história, na ordem dos números (001 antes de 010)', await escolhido('ordem.cbz'));
ok(await escolhido('anunciada.cbz') === 'cover.png', 'uma imagem que se anuncia como capa vem antes da primeira página', await escolhido('anunciada.cbz'));
ok(await escolhido('pastas.cbz') === '002.png', 'CBZ em pastas: a primeira imagem da primeira pasta, em ordem', await escolhido('pastas.cbz'));
ok(await escolhido('so-texto.cbz') === null, 'CBZ sem imagem: devolve nada', await escolhido('so-texto.cbz'));

console.log('O QUE NÃO É LIVRO DIGITAL');
for (const nome of ['ruim.epub', 'truncado.epub', 'normal.zip', 'livro.epub.pdf'])
  ok(await M.capaDoDigital(arquivoFake(nome)) === null, 'pacote que não dá para ler não vira erro nem aviso: ' + nome);
ok(rede === 0, 'nada foi buscado na internet ao ler os pacotes', rede);

/* ---------- as peças, conferidas uma a uma ---------- */
console.log('O PACOTE POR DENTRO');
const v = new Uint8Array(fs.readFileSync(path.join(FIX, 'properties.epub')));
const lista = M.listarZip(v);
ok(lista.length === 7 && lista.some(e => e.nome === 'OEBPS/imagens/a capa.png') && lista.every(e => e.tam > 0),
   'o índice do pacote é lido inteiro: sete arquivos, com nome, tamanho e posição', lista.map(e => [e.nome, e.tam, e.metodo]));
ok(lista.find(e => e.nome === 'OEBPS/imagens/a capa.png').metodo === 0 && lista.find(e => e.nome === 'OEBPS/cap1.xhtml').metodo === 8,
   'os dois jeitos de guardar são entendidos: sem compressão (stored) e comprimido (deflate)');
const lida = await M.blocoDoZip(v, lista.find(e => e.nome === 'OEBPS/imagens/a capa.png'));
ok(lida && Buffer.from(lida).equals(fs.readFileSync(path.join(FIX, 'esperado.png'))), 'a imagem que sai do pacote é a que foi posta nele, byte a byte');
ok(await M.blocoDoZip(v, { nome: 'x.png', metodo: 0, tam: 20 * 1048576, ini: 0 }) === null, 'um bloco declarado com mais de 16 MB é recusado antes de ser lido');
ok(await M.blocoDoZip(v, { nome: 'x.png', metodo: 99, tam: 10, ini: lista[0].ini }) === null, 'compressão que não é stored nem deflate: nada é lido');
ok(await M.blocoDoZip(v, { nome: 'x.png', metodo: 8, tam: 10, ini: lista[0].ini }) === null, 'entrada que o índice promete mas o cabeçalho não confirma: nada é lido');
ok(M.caminhoRelativo('Livro/a.opf', 'img/../imagens/capa%20grande.png') === 'Livro/imagens/capa grande.png',
   'caminho relativo: a pasta do índice, o ".." e o %20', M.caminhoRelativo('Livro/a.opf', 'img/../imagens/capa%20grande.png'));
ok(M.caminhoRelativo('Livro/miolo/c.opf', '../../imagens/acima.png') === 'imagens/acima.png',
   'dois ".." sobem as duas pastas do índice e param na raiz do pacote', M.caminhoRelativo('Livro/miolo/c.opf', '../../imagens/acima.png'));
ok(M.caminhoRelativo('a/opf.opf', 'https://x.com/capa.png') === '' && M.caminhoRelativo('a/opf.opf', '') === '',
   'endereço de fora e referência vazia não viram caminho', M.caminhoRelativo('a/opf.opf', 'ftp://x/capa.png'));
ok(M.capaAnunciadaEpub('<package><manifest>' + '<item id="c" href="c.png" media-type="image/svg+xml"/><item id="h" href="c.html" media-type="text/html"/>' + '</manifest></package>', 'a.opf') === '',
   'item de texto ou de SVG não é capa');
ok(M.capaDoCbz(['z/002.jpg', 'a/010.jpg', 'a/003.jpg']) === 'a/003.jpg', 'CBZ: os números do nome são entendidos como números', M.capaDoCbz(['z/002.jpg', 'a/010.jpg', 'a/003.jpg']));
ok(M.capaDoCbz(['notas.txt', 'info.json']) === '', 'CBZ: nada que não seja imagem entra na conta');
ok(M.DIGITAL_CAPA.test('Livro.EPUB') && M.DIGITAL_CAPA.test('hq.CBZ') && !M.DIGITAL_CAPA.test('livro.pdf') && !M.DIGITAL_CAPA.test('capa.epub.png'),
   'pelo nome, só .epub e .cbz — e nada que só pareça');

/* ---------- o fluxo da ficha, com o módulo das anotações ---------- */
const novoLivro = (id, extra) => { const b = Object.assign({ id, t: 'Título ' + id, a: 'Autor', tags: [], leit: '', notas: {}, u: 0 }, extra || {}); livros.push(b); return b; };
async function anexa(livro, nome, antes) {
  banco.clear(); M.Anexos.capas.clear(); avisos = []; desenhos = 0;
  if (antes) antes();
  M.Notas.id = livro.id;
  await M.Notas.anexar(arquivoFake(nome));
  return { livro, avisos: avisos.slice(), banco: [...banco.values()] };
}

console.log('ANEXAR UM EPUB A UM LIVRO SEM CAPA');
let r = await anexa(novoLivro('a1'), 'meta.epub');
let capa = r.banco.find(x => x.tipo === 'capa');
ok(r.avisos[r.avisos.length - 1] === 'Arquivo anexado. O livro foi marcado com “possui análise”. A capa que estava dentro do arquivo virou a capa do livro.',
   'a ficha diz que a capa veio do arquivo', r.avisos);
ok(r.banco.filter(x => x.tipo === 'arquivo').length === 1 && r.banco.find(x => x.tipo === 'arquivo').nome === 'meta.epub',
   'o arquivo continuou sendo anexado do jeito de sempre', r.banco.map(x => [x.tipo, x.nome]));
ok(!!r.livro.cp && capa && capa.livro === 'a1' && capa.nome === 'capa de frente.png' && capa.mime === 'image/jpeg',
   'a imagem é gravada como capa enviada, ligada ao livro', capa && { nome: capa.nome, mime: capa.mime, livro: capa.livro });
ok(canvasVisto && canvasVisto.width === 360 && canvasVisto.height === 540, 'ela passou pelo reduzidor da "Enviar capa…": 600 × 900 viraram 360 × 540', canvasVisto);
ok(M.Anexos.capas.get(r.livro.cp) === capa.dados && /^data:image\/jpeg;base64,/.test(capa.dados) && capa.tam > 0,
   'a capa vai para a memória (a tela a desenha sem esperar) e para o banco do navegador', capa && capa.tam);
ok(desenhos === 1, 'a tela é redesenhada uma vez, com a capa já no lugar', desenhos);
ok(capa.tam === Math.round((capa.dados.length - 23) * 0.75), 'o tamanho anotado é o da imagem reduzida, não o do arquivo', capa.tam);

console.log('OUTRAS IMAGENS E OUTROS LIVROS');
imagem = { w: 900, h: 600 };
r = await anexa(novoLivro('a2'), 'nome.epub');
ok(canvasVisto.width === 360 && canvasVisto.height === 240, 'imagem larga é reduzida para caber em 360 × 540 sem deformar', canvasVisto);
imagem = { w: 600, h: 900 };
r = await anexa(novoLivro('a3'), 'sem-capa.epub');
ok(!r.livro.cp && !r.banco.some(x => x.tipo === 'capa') && r.avisos[r.avisos.length - 1] === 'Arquivo anexado. O livro foi marcado com “possui análise”.',
   'EPUB sem capa: o arquivo é anexado, nada muda na ficha e nenhum aviso é dado', r.avisos);
r = await anexa(novoLivro('a4'), 'so-texto.cbz');
ok(!r.livro.cp && r.banco.length === 1, 'CBZ sem imagem: mesma coisa — o arquivo entra, a capa fica como está', r.banco.map(x => x.tipo));
r = await anexa(novoLivro('a5'), 'ordem.cbz');
ok(!!r.livro.cp && r.banco.find(x => x.tipo === 'capa').nome === 'capa de 001.jpg', 'CBZ anexado também ganha a capa do arquivo', r.banco.map(x => [x.tipo, x.nome]));

console.log('O QUE NÃO É TROCADO');
r = await anexa(novoLivro('b1', { cp: 'chave-velha' }), 'meta.epub', () => banco.set('chave-velha', { k: 'chave-velha', livro: 'b1', tipo: 'capa', dados: 'data:image/jpeg;base64,VELHA' }));
ok(r.livro.cp === 'chave-velha' && !r.banco.some(x => x.tipo === 'capa' && x.k !== 'chave-velha') && !any_virou(r.avisos),
   'a capa que o usuário enviou continua no lugar (e não se acumula uma segunda, nem se fala dela)', [r.livro.cp, r.avisos]);
r = await anexa(novoLivro('b2', { _img: 12345 }), 'meta.epub');
ok(!r.livro.cp && r.banco.filter(x => x.tipo === 'capa').length === 0, 'livro que já tem capa no catálogo não ganha a do arquivo', r.livro.cp);
r = await anexa(novoLivro('b3'), 'livro.epub.pdf');
ok(!r.livro.cp && r.avisos[r.avisos.length - 1] === 'Arquivo anexado. O livro foi marcado com “possui análise”.', 'anexar um PDF continua exatamente como era', r.avisos);
console.log('O LIVRO SAI DO PAINEL NO MEIO DA LEITURA');
const c1 = novoLivro('c1');
banco.clear(); M.Anexos.capas.clear(); avisos = []; desenhos = 0;
M.Notas.id = c1.id;
await M.Notas.anexar({ name: 'meta.epub', size: 1000, type: '', arrayBuffer: async () => { livros = livros.filter(b => b.id !== 'c1'); const buf = fs.readFileSync(path.join(FIX, 'meta.epub')); return buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.length); } });
await espera();                                    // o que sobrou é apagado em seguida, sem esperar por ninguém (como no painel)
ok(banco.size === 0 && desenhos === 0 && !avisos.length,
   'se o livro saiu do painel enquanto o arquivo era lido, nada fica gravado, nada é redesenhado e nenhum aviso é dado', [banco.size, desenhos, avisos]);

console.log('O USUÁRIO ENVIA UMA CAPA ENQUANTO O ARQUIVO É LIDO');
const e1 = novoLivro('e1');
banco.clear(); M.Anexos.capas.clear(); avisos = []; desenhos = 0; M.Notas.id = e1.id;
await M.Notas.anexar({ name: 'meta.epub', size: 1000, type: '', arrayBuffer: async () => {      // o clique em "Enviar capa…" aconteceu no meio da leitura
  e1.cp = 'de-fora'; banco.set('de-fora', { k: 'de-fora', livro: 'e1', tipo: 'capa', dados: 'data:image/jpeg;base64,FORA' });
  const buf = fs.readFileSync(path.join(FIX, 'meta.epub')); return buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.length);
} });
await espera();
ok(e1.cp === 'de-fora' && [...banco.values()].filter(x => x.tipo === 'capa').length === 1 && !any_virou(avisos),
   'a capa enviada pelo usuário vale: a extraída não é gravada e nada é anunciado', [e1.cp, [...banco.keys()], avisos]);

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
await M.Notas.enviarCapa({ name: 'x.png', size: 1, type: 'image/png', arrayBuffer: async () => new ArrayBuffer(1) });
ok(rede === 0, 'nada foi buscado na internet no fluxo da ficha', rede);

console.log('ERROS: ' + erros.length);
for (const e of erros) console.log('   ' + e);
process.exit(erros.length ? 1 : 0);
'''

(PACOTE).mkdir(parents=True, exist_ok=True)
(PACOTE / 'harness.mjs').write_text(HARNESS, encoding='utf-8')

print('RODANDO O JAVASCRIPT DO PAINEL NO NODE')
node = shutil.which('node')
saida = ''
if not node:
    print('  (pulado: o Node não está neste computador — sem ele a parte executada do teste não roda)')
else:
    r = subprocess.run([node, str(PACOTE / 'harness.mjs'), str(RAIZ), str(FIX)], capture_output=True, text=True, timeout=300)
    saida = (r.stdout or '') + (('\n' + r.stderr) if r.stderr.strip() else '')
    print(saida.rstrip())
    confere(r.returncode == 0 and bool(re.search(r'^ERROS: 0$', saida, flags=re.M)), 'o JavaScript do painel Extrai a capa e faz o fluxo da ficha', (r.returncode, saida[-800:]))
    n = len([l for l in saida.splitlines() if l.startswith(('ok', 'FALHOU'))])
    confere(n >= 36, 'a checagem executou as %d previsões do teste (EPUB, CBZ, pacote e ficha)' % n, n)

print('O QUE FICA NO ARQUIVO (o desenho do fluxo)')
mod = (RAIZ / 'src' / 'js' / '54-capa-digital.js').read_text(encoding='utf-8')
anx = (RAIZ / 'src' / 'js' / '55-anexos.js').read_text(encoding='utf-8')
confere("const DIGITAL_CAPA = /\\.(epub|cbz)$/i;" in mod, 'só EPUB e CBZ são abertos — PDF fica de fora, como combinado')
confere(not re.search(r'\bfetch\s*\(|XMLHttpRequest|document\.|window\.|localStorage|indexedDB', mod),
        'o módulo que abre o pacote não toca a tela, nem o armazenamento, nem a internet: é por isso que dá para testá-lo sem navegador')
confere('return { blob:' in mod and 'catch (err) { return null; }' in mod, 'o que der errado no pacote devolve nada, em silêncio')
confere('if (b.cp || temCapa(b) || !DIGITAL_CAPA.test(arq.name' in anx,
        'a capa do arquivo só entra quando o livro não tem capa nenhuma (nem enviada, nem do catálogo)')
trecho = anx[anx.index('async anexar(arq)'):anx.index('async capaDoArquivoDigital')]
confere('await this.capaDoArquivoDigital(arq, b)' in trecho and trecho.index('capaDoArquivoDigital') < trecho.index("tipo: 'arquivo'"),
        'a imagem é lida antes de qualquer gravação: se o livro saiu do painel no meio, nada é gravado')
confere(trecho.count('tocar(b); toast(') == 1 and 'A capa que estava dentro do arquivo virou a capa do livro.' in trecho,
        'a mensagem de sempre continua no lugar, e a da capa só é acrescentada quando ela existe')
confere('const [kc] = await this.gravarCapa(b, capa.dados, capa.nome);' in anx and 'else if (kc) { b.cp = kc; virouCapa = true; }' in anx,
        'a capa extraída é gravada pelo mesmo caminho da capa enviada: vale com as capas desligadas, entra no backup e sai com "Tirar a capa enviada"')
confere('if (capa && !b.cp)' in anx and 'Anexos.apagar([kc]).catch(() => {})' in anx and 'virouCapa ? ' in anx,
        'se o livro ganhou uma capa enquanto o arquivo era lido, a extraída não é gravada nem anunciada')
confere(anx.count('async gravarCapa(b, dados, nome)') == 1 and "await this.gravarCapa(b, dados, arq.name || 'capa')" in anx,
        '"Enviar capa…" e a capa do arquivo usam a mesma gravação — não há segunda maneira de guardar uma capa')
confere('nome: String(nome || \'capa\').slice(0, 120)' in anx and "mime: 'image/jpeg'" in anx, 'a capa do arquivo é guardada como JPEG reduzido, com o nome do arquivo de origem')
confere('54-capa-digital' in (RAIZ / 'README.md').read_text(encoding='utf-8'), 'o README conhece o módulo novo')

shutil.rmtree(PACOTE, ignore_errors=True)
print('ERROS:', len(erros))
for e in erros:
    print('  ', e)
sys.exit(1 if erros else 0)
