/* ───────────────────────── a capa que vem dentro do livro digital (EPUB e CBZ) ─────────────────────────
   EPUB e CBZ são arquivos .zip por dentro, e costumam trazer a capa entre os arquivos deles. Este módulo abre o pacote
   aqui no navegador e devolve a imagem — sem internet, sem enviar o arquivo a lugar nenhum e sem gravar nada: quem
   grava é o módulo das anotações (55-anexos), que passa a tratar esta imagem como uma capa enviada (vale mais que a do
   catálogo, entra no backup e pode ser tirada).
   · EPUB — a capa é a imagem que o índice do livro (o arquivo .opf) anuncia: properties="cover-image" no item, o
     <meta name="cover" content="…"> (por id do item ou pelo nome do arquivo) ou a referência type="cover" do <guide>,
     jeito dos EPUBs antigos e dos convertidos por Calibre; sem anúncio, vale a imagem com "capa"/"cover" no nome e,
     se o pacote tem uma imagem só, ela. Não adivinhamos pela primeira imagem de um pacote com muitas: a primeira
     costuma ser do miolo.
   · CBZ — a capa é a primeira imagem da história; uma que diga "cover" (ou "capa") no nome tem prioridade.
   · PDF fica de fora: não é um pacote .zip, e a "capa" de lá seria a primeira página, que precisa ser renderizada.
   Só os pedaços necessários são lidos (a cauda, o índice e a entrada da capa), então um livro de 200 MB não pesa na
   memória e o limite de anexação não trava a extração. O que der errado — pacote truncado, índice em ZIP64, imagem
   que não está lá — devolve { motivo: '…' } e anexar o arquivo não depende de nada daqui dar certo. */
const DIGITAL_CAPA = /\.(epub|cbz)$/i;                     // os formatos de que sabemos tirar a capa, pelo nome do arquivo
const IMG_FORMATO = { jpg: 'image/jpeg', jpeg: 'image/jpeg', png: 'image/png', webp: 'image/webp', gif: 'image/gif', bmp: 'image/bmp' };
const LIM_PACOTE = 16 * 1048576;                           // nenhuma imagem de capa precisa vir guardada num bloco maior que este
const LIM_INDICE = 8 * 1048576;                            // tamanho máximo do índice do pacote que nos dispomos a ler
const ZIP_FIM = 0x06054b50, ZIP_CD = 0x02014b50, ZIP_LOCAL = 0x04034b50;
const soNomeDoCaminho = c => String(c).split('/').pop() || '';
const formatoDaImagem = nome => IMG_FORMATO[(soNomeDoCaminho(nome).split('.').pop() || '').toLowerCase()] || '';

/* Fonte de bytes: um File do navegador (lido em pedaços, por fatia) ou um Uint8Array (o caminho dos testes). */
function fonteDe(arq) {
  if (arq instanceof Uint8Array) return { tam: arq.length, pedacos: 0, ler(i, n) { this.pedacos++; return Promise.resolve(arq.subarray(Math.min(i, arq.length), Math.min(i + n, arq.length))); } };
  return { tam: (arq && arq.size) || 0, pedacos: 0,
    ler(i, n) { this.pedacos++; return (arq.slice ? arq.slice(i, i + n) : arq).arrayBuffer().then(b => new Uint8Array(b)); } };
}

/* O índice do fim do pacote ("end of central directory") e, a partir dele, a lista de arquivos: nome, compressão,
   tamanho e posição de cada um. É por ele que se lê um .zip sem percorrer o pacote inteiro — e é a parte que um
   arquivo truncado, ou de outro formato, não tem. */
async function listarZip(f) {
  if (!f || !f.tam || f.tam < 22) return [];
  const janela = Math.min(f.tam, 66000), cauda = await f.ler(f.tam - janela, janela);
  const dv = new DataView(cauda.buffer, cauda.byteOffset, cauda.byteLength);
  let fim = -1;
  for (let i = cauda.length - 22; i >= 0; i--) if (dv.getUint32(i, true) === ZIP_FIM) { fim = i; break; }
  if (fim < 0) return [];
  const n = dv.getUint16(fim + 10, true), ini = dv.getUint32(fim + 16, true);
  if (n === 0xffff || ini === 0xffffffff || ini >= f.tam) return [];             // pacote grande demais (ZIP64): não lemos
  const dec = new TextDecoder(), out = [], bruto = (f.tam - janela) + fim - ini; // o índice termina onde começa o que achamos
  const corpo = await f.ler(ini, Math.min(Math.max(bruto, 0), LIM_INDICE));
  const d = new DataView(corpo.buffer, corpo.byteOffset, corpo.byteLength);
  for (let p = 0, i = 0; i < n && p + 46 <= corpo.length; i++) {
    if (d.getUint32(p, true) !== ZIP_CD) break;
    const nomeLen = d.getUint16(p + 28, true), extraLen = d.getUint16(p + 30, true), comLen = d.getUint16(p + 32, true);
    out.push({ nome: dec.decode(corpo.subarray(p + 46, p + 46 + nomeLen)).replace(/\\/g, '/'), metodo: d.getUint16(p + 10, true),
               tam: d.getUint32(p + 20, true), ini: d.getUint32(p + 42, true) });
    p += 46 + nomeLen + extraLen + comLen;
  }
  return out;
}

/* O conteúdo de uma entrada, lido do arquivo: o cabeçalho local (30 bytes) repete o nome e traz os campos extras, e é
   ele que diz onde o conteúdo começa; o tamanho vem do índice (num pacote escrito às pressas o cabeçalho local vem
   zerado). "stored" já vem pronto; "deflate" é o que o navegador abre com DecompressionStream — sem biblioteca. */
async function bytesDaEntrada(f, e) {
  if (!f || !e || !e.tam || e.tam > LIM_PACOTE || e.ini + 30 > f.tam) return null;
  const cab = await f.ler(e.ini, 30);
  if (cab.length < 30 || new DataView(cab.buffer, cab.byteOffset, cab.byteLength).getUint32(0, true) !== ZIP_LOCAL) return null;
  const dv = new DataView(cab.buffer, cab.byteOffset, cab.byteLength);
  const ini = e.ini + 30 + dv.getUint16(26, true) + dv.getUint16(28, true);
  if (ini + e.tam > f.tam) return null;
  const bruto = await f.ler(ini, e.tam);
  if (bruto.length !== e.tam) return null;                                        // pacote truncado: nada é descomprimido pela metade
  if (e.metodo === 0) return bruto;
  if (e.metodo !== 8 || typeof DecompressionStream !== 'function') return null;
  try {
    const s = new Blob([bruto]).stream().pipeThrough(new DecompressionStream('deflate-raw'));
    const fora = new Uint8Array(await new Response(s).arrayBuffer());
    return fora.length && fora.length <= 64 * 1048576 ? fora : null;               // nada aqui precisa descomprimir mais que isto
  } catch (err) { return null; }
}
const textoDaEntrada = async (f, e) => { const b = await bytesDaEntrada(f, e); return b ? new TextDecoder().decode(b) : ''; };

/* atributos de uma etiqueta XML, em minúsculas: o índice do EPUB escreve as aspas e a ordem como quer */
function atributosDe(tag) {
  const a = {};
  for (const p of String(tag).matchAll(/([a-zA-Z:-]+)\s*=\s*"([^"]*)"|([a-zA-Z:-]+)\s*=\s*'([^']*)'/g)) a[(p[1] || p[3]).toLowerCase()] = (p[2] !== undefined ? p[2] : p[4]).trim();
  return a;
}

/* O caminho de um arquivo dentro do pacote, a partir de quem o referenceou: o índice do EPUB usa caminhos relativos,
   às vezes escapados (%20), às vezes saindo da pasta com "../". Um endereço de fora (http:…) não é lido. */
function caminhoRelativo(base, ref) {
  let r = String(ref || '').split('#')[0].split('?')[0].trim();
  if (!r || /^[a-z][a-z0-9+.-]*:/i.test(r)) return '';
  try { r = decodeURIComponent(r); } catch (err) { /* nome com % solto: fica como está */ }
  const caminho = r.startsWith('/') ? r.slice(1) : base.slice(0, base.lastIndexOf('/') + 1) + r;
  const fora = [];
  for (const parte of caminho.split('/')) { if (!parte || parte === '.') continue; if (parte === '..') fora.pop(); else fora.push(parte); }
  return fora.join('/');
}

/* A imagem que o índice do EPUB (.opf) anuncia como capa, no caminho relativo a esse índice — ou '' quando não anuncia.
   Depois do properties e do <meta name="cover"> vem a referência type="cover" do <guide>: é como os EPUBs 2 e os
   arquivos baixados anunciam a capa, e quem só olha o <meta> devolve null para um livro com a capa bem anunciada. */
function capaAnunciadaEpub(txt, base) {
  const etiquetas = re => [...String(txt).matchAll(re)].map(m => atributosDe(m[0]));
  // um item declarado image/svg+xml não concorre: o navegador não reduziria um vetor para o tamanho de capa
  const imagens = etiquetas(/<item\b[^>]*>/gi).filter(i => i.href && /^image\//i.test(i['media-type'] || '') && !/svg/i.test(i['media-type'] || ''));
  if (!imagens.length) return '';
  const idCapa = ((etiquetas(/<meta\b[^>]*>/gi).find(m => /^cover$/i.test(m.name || '')) || {}).content || '').trim().toLowerCase();
  const doGuia = ((etiquetas(/<reference\b[^>]*>/gi).find(m => /^cover$/i.test(m.type || '')) || {}).href || '').trim();
  const semExtensao = s => String(s).replace(/\.[a-z0-9]+$/i, '');
  const escolhida = imagens.find(i => /(^|\s)cover-image(\s|$)/i.test(i.properties || ''))
    || (idCapa ? imagens.find(i => (i.id || '').toLowerCase() === idCapa) : null)
    // quem escreve ali o nome do arquivo (com ou sem extensão), e não o id do item
    || (idCapa ? imagens.find(i => { const n = soNomeDoCaminho(i.href).toLowerCase(); return n === idCapa || semExtensao(n) === semExtensao(idCapa); }) : null)
    // o <guide> aponta para um href, que pode ser o próprio item da lista ou um arquivo de imagem avulso
    || (doGuia ? imagens.find(i => caminhoRelativo(base, i.href) === caminhoRelativo(base, doGuia)) : null)
    || (doGuia && !idCapa ? (formatoDaImagem(doGuia) ? [{ href: doGuia }] : null) : null)   // muitos guias apontam para uma página, não para a imagem: nesse caso não vale
    || (!idCapa && !doGuia && imagens.length === 1 && formatoDaImagem(imagens[0].href) ? imagens[0] : null)   // (só vale um formato que o navegador consiga reduzir)               // pacote com uma imagem só: ela é a capa
    || imagens.find(i => /(^|[^a-z])(capa|cover)([^a-z]|$)/i.test(`${i.id || ''} ${i.href || ''}`))    // o costume, quando ninguém anunciou
    || null;
  return escolhida ? caminhoRelativo(base, escolhida.href) : '';
}

/* A capa de um CBZ: a imagem que se apresenta como capa; senão, a primeira da lista, na ordem em que o pacote veio */
function capaDoCbz(caminhos) {
  const imagens = caminhos.filter(n => formatoDaImagem(n));
  return imagens.find(n => /(^|[^a-z])(capa|cover)([^a-z]|$)/i.test(soNomeDoCaminho(n)))
    || imagens.slice().sort((a, b) => a.toLowerCase().localeCompare(b.toLowerCase(), 'en', { numeric: true }))[0] || '';
}

/* Arquivo (File) de um EPUB ou CBZ → { blob, nome } com a imagem da capa, ou { motivo: '…' } quando não há nada
   aproveitável. O motivo não serve para a ficha (que fica em silêncio) e sim para o quadro da varredura em lote, que
   precisa dizer "este arquivo não traz capa" em vez de um "0 capas" mudo. */
async function capaDoDigital(arq) {
  const pacote = { motivo: 'pacote ilegível' }, vazias = { motivo: 'sem capa dentro' };
  try {
    const nome = (arq && arq.name) || '';
    if (!DIGITAL_CAPA.test(nome)) return { motivo: 'não é EPUB nem CBZ' };
    const f = fonteDe(arq);
    if (f.tam < 22) return pacote;
    const lista = await listarZip(f); if (!lista.length) return pacote;
    const caminhos = lista.map(e => e.nome);
    const porCaminho = new Map(caminhos.map((c, i) => [c.toLowerCase(), i]));      // o pacote pode grafar as maiúsculas de outro jeito
    let alvo = '';
    if (/\.epub$/i.test(nome)) {
      let opf = '';
      const c = porCaminho.get('meta-inf/container.xml');                          // container.xml diz onde está o índice do livro
      if (c != null) opf = caminhoRelativo('', (/full-path\s*=\s*["']([^"']*)["']/i.exec(await textoDaEntrada(f, lista[c])) || [])[1] || '');
      if (!opf) { const soOpf = caminhos.filter(n => /\.opf$/i.test(n)); if (soOpf.length !== 1) return vazias; opf = soOpf[0]; }
      const oi = porCaminho.get(opf.toLowerCase()); if (oi == null) return pacote;
      alvo = capaAnunciadaEpub(await textoDaEntrada(f, lista[oi]), opf);
    } else {
      alvo = capaDoCbz(caminhos);
    }
    if (!alvo) return vazias;
    const i = porCaminho.get(alvo.toLowerCase()); if (i == null) return { motivo: 'capa fora do pacote' };
    const e = lista[i], tipo = formatoDaImagem(e.nome);
    if (!tipo) return vazias;
    const dados = await bytesDaEntrada(f, e);
    if (!dados || !dados.length) return e.tam > LIM_PACOTE ? { motivo: 'capa grande demais' } : { motivo: 'imagem que não abriu' };
    return { blob: new Blob([dados], { type: tipo }), nome: soNomeDoCaminho(e.nome) };
  } catch (err) { return pacote; }                                                  // arquivo danificado ou formato que não sabemos ler: segue sem capa, sem aviso
}
