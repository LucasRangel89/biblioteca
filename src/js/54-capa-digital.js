/* ───────────────────────── a capa que vem dentro do livro digital (EPUB e CBZ) ─────────────────────────
   EPUB e CBZ são arquivos .zip por dentro, e costumam trazer a capa entre os arquivos deles. Este módulo abre o pacote
   aqui no navegador e devolve a imagem — sem internet, sem enviar o arquivo a lugar nenhum e sem gravar nada: quem
   grava é o módulo das anotações (55-anexos), que passa a tratar esta imagem como uma capa enviada (vale mais que a do
   catálogo, entra no backup e pode ser tirada).
   · EPUB — a capa é a imagem que o índice do livro (o arquivo .opf) anuncia: properties="cover-image" no item, ou
     <meta name="cover" content="…"> apontando para ele; sem anúncio, uma imagem com "capa"/"cover" no nome. Não
     adivinhamos pela primeira imagem: um EPUB tem muitas, e a primeira costuma ser do miolo.
   · CBZ — a capa é a primeira imagem da história; uma que diga "cover" (ou "capa") no nome tem prioridade.
   · PDF fica de fora: não é um pacote .zip, e a "capa" de lá seria a primeira página, que precisa ser renderizada.
   O que der errado — pacote truncado, índice em ZIP64, imagem que não está lá — devolve null em silêncio: anexar o
   arquivo não depende de nada daqui dar certo. */
const DIGITAL_CAPA = /\.(epub|cbz)$/i;                     // os formatos de que sabemos tirar a capa, pelo nome do arquivo
const IMG_FORMATO = { jpg: 'image/jpeg', jpeg: 'image/jpeg', png: 'image/png', webp: 'image/webp', gif: 'image/gif', bmp: 'image/bmp' };
const LIM_PACOTE = 16 * 1048576;                           // nenhuma imagem de capa precisa vir guardada num bloco maior que este
const soNomeDoCaminho = c => String(c).split('/').pop() || '';
const formatoDaImagem = nome => IMG_FORMATO[(soNomeDoCaminho(nome).split('.').pop() || '').toLowerCase()] || '';

/* o arquivo inteiro em bytes: File.arrayBuffer() é o caminho de hoje; FileReader, o reserva */
async function bytesDoArquivo(arq) {
  if (arq && arq.arrayBuffer) return new Uint8Array(await arq.arrayBuffer());
  return await new Promise((res, rej) => {
    const l = new FileReader();
    l.onload = () => res(new Uint8Array(l.result));
    l.onerror = () => rej(l.error || new Error('não foi possível ler o arquivo'));
    l.readAsArrayBuffer(arq);
  });
}

/* O índice do fim do pacote ("end of central directory"): nome, compressão, tamanho e posição de cada arquivo. É por
   ele que se lê um .zip sem percorrer o pacote inteiro — e é a parte que um arquivo truncado ou de outro formato não tem. */
function listarZip(v) {
  const dv = new DataView(v.buffer, v.byteOffset, v.byteLength);
  let fim = -1;
  for (let i = v.length - 22; i >= Math.max(0, v.length - 66000); i--) if (dv.getUint32(i, true) === 0x06054b50) { fim = i; break; }
  if (fim < 0) return [];
  const n = dv.getUint16(fim + 10, true), ini = dv.getUint32(fim + 16, true);
  if (n === 0xffff || ini === 0xffffffff) return [];                                 // pacote grande demais (ZIP64): não lemos
  const dec = new TextDecoder(), out = [];                                           // nomes em UTF-8 (ou cp437: o decodificador tolera)
  for (let p = ini, i = 0; i < n && p + 46 <= v.length; i++) {
    if (dv.getUint32(p, true) !== 0x02014b50) break;
    const nomeLen = dv.getUint16(p + 28, true), extraLen = dv.getUint16(p + 30, true), comLen = dv.getUint16(p + 32, true);
    out.push({ nome: dec.decode(v.subarray(p + 46, p + 46 + nomeLen)).replace(/\\/g, '/'), metodo: dv.getUint16(p + 10, true),
               tam: dv.getUint32(p + 20, true), ini: dv.getUint32(p + 42, true) });
    p += 46 + nomeLen + extraLen + comLen;
  }
  return out;
}

/* Os bytes de uma entrada, antes de descomprimir. O cabeçalho local repete o nome do arquivo e traz os campos extras,
   e é ele que diz onde o conteúdo começa; o tamanho vem do índice (em pacote escrito às pressas o cabeçalho local vem zerado). */
function fatiaZip(v, e) {
  const dv = new DataView(v.buffer, v.byteOffset, v.byteLength);
  if (!e || e.ini + 30 > v.length || dv.getUint32(e.ini, true) !== 0x04034b50) return null;
  const ini = e.ini + 30 + dv.getUint16(e.ini + 26, true) + dv.getUint16(e.ini + 28, true);
  if (ini + e.tam > v.length) return null;
  return v.subarray(ini, ini + e.tam);
}

/* O conteúdo de uma entrada, descomprimido. "stored" (0) já vem pronto; "deflate" (8) é o que o navegador sabe abrir
   com DecompressionStream — o mesmo descompressor usado para baixar arquivos, sem biblioteca nenhuma. */
async function blocoDoZip(v, e) {
  if (!e || !e.tam || e.tam > LIM_PACOTE) return null;
  const bruto = fatiaZip(v, e); if (!bruto) return null;
  if (e.metodo === 0) return bruto;
  if (e.metodo !== 8 || typeof DecompressionStream !== 'function') return null;
  try {
    const s = new Blob([bruto]).stream().pipeThrough(new DecompressionStream('deflate-raw'));
    const fora = new Uint8Array(await new Response(s).arrayBuffer());
    return fora.length && fora.length <= 64 * 1048576 ? fora : null;                 // nada aqui precisa descomprimir mais que isto
  } catch (err) { return null; }
}
const textoDoZip = async (v, e) => { const b = await blocoDoZip(v, e); return b ? new TextDecoder().decode(b) : ''; };

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

/* A imagem que o índice do EPUB (.opf) anuncia como capa, no caminho relativo a esse índice — ou '' quando não anuncia */
function capaAnunciadaEpub(txt, base) {
  const etiquetas = re => [...String(txt).matchAll(re)].map(m => atributosDe(m[0]));
  const imagens = etiquetas(/<item\b[^>]*>/gi).filter(i => i.href && /^image\//i.test(i['media-type'] || ''));
  if (!imagens.length) return '';
  const idCapa = ((etiquetas(/<meta\b[^>]*>/gi).find(m => /^cover$/i.test(m.name || '')) || {}).content || '').trim().toLowerCase();
  const semExtensao = s => String(s).replace(/\.[a-z0-9]+$/i, '');
  const escolhida = imagens.find(i => /(^|\s)cover-image(\s|$)/i.test(i.properties || ''))
    || (idCapa ? imagens.find(i => (i.id || '').toLowerCase() === idCapa) : null)
    // quem escreve ali o nome do arquivo (com ou sem extensão), e não o id do item
    || (idCapa ? imagens.find(i => { const n = soNomeDoCaminho(i.href).toLowerCase(); return n === idCapa || semExtensao(n) === semExtensao(idCapa); }) : null)
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

/* Arquivo (File) de um EPUB ou CBZ → { blob, nome } com a imagem da capa, ou null quando não há nada aproveitável. */
async function capaDoDigital(arq) {
  try {
    const nome = (arq && arq.name) || '';
    if (!DIGITAL_CAPA.test(nome)) return null;
    const v = await bytesDoArquivo(arq);
    if (!v || v.length < 22) return null;
    const lista = listarZip(v); if (!lista.length) return null;
    const caminhos = lista.map(e => e.nome);
    const porCaminho = new Map(caminhos.map((c, i) => [c.toLowerCase(), i]));        // o pacote pode grafar as maiúsculas de outro jeito
    let alvo = '';
    if (/\.epub$/i.test(nome)) {
      let opf = '';
      const c = porCaminho.get('meta-inf/container.xml');                            // container.xml diz onde está o índice do livro
      if (c != null) opf = caminhoRelativo('', (/full-path\s*=\s*["']([^"']*)["']/i.exec(await textoDoZip(v, lista[c])) || [])[1] || '');
      if (!opf) { const soOpf = caminhos.filter(n => /\.opf$/i.test(n)); if (soOpf.length !== 1) return null; opf = soOpf[0]; }
      const oi = porCaminho.get(opf.toLowerCase()); if (oi == null) return null;
      alvo = capaAnunciadaEpub(await textoDoZip(v, lista[oi]), opf);
    } else {
      alvo = capaDoCbz(caminhos);
    }
    if (!alvo) return null;
    const i = porCaminho.get(alvo.toLowerCase()); if (i == null) return null;
    const e = lista[i]; if (!formatoDaImagem(e.nome)) return null;
    const dados = await blocoDoZip(v, e); if (!dados) return null;
    return { blob: new Blob([dados], { type: formatoDaImagem(e.nome) }), nome: soNomeDoCaminho(e.nome) };
  } catch (err) { return null; }                                                      // arquivo danificado ou formato que não sabemos ler: segue sem capa, sem aviso
}
