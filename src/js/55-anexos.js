/* ───────────────────────── anotações do usuário: comentários, capa enviada e arquivos anexados ─────────────────────────
   Os comentários são texto curto e ficam no próprio livro (campo `com`), junto com o resto dos dados.
   O que pesa — a imagem da capa e os arquivos (resenha, relatório…) — fica à parte, no IndexedDB (o banco de dados do
   próprio navegador): o armazenamento local, onde estão os livros, é pequeno e é regravado inteiro a cada alteração.
   No livro fica só a chave de cada anexo (`cp`, `anx`). Nada sai do dispositivo; o backup (.json) leva os anexos junto.
   Sem armazenamento (pré-visualização em sandbox) os anexos valem só enquanto a página estiver aberta. */
const ANEXO_MAX = 5 * 1048576;                       // tamanho máximo de um arquivo anexado
const CAPA_MAX = [360, 540];                         // a capa enviada é reduzida para caber nisto (largura × altura, em pixels)
const fTam = n => (n < 1024 ? `${n} B` : n < 1048576 ? `${fInt(Math.round(n / 1024))} KB` : `${fDec(n / 1048576)} MB`);
const novaChave = () => (Date.now().toString(36) + Math.random().toString(36).slice(2, 10)).slice(0, 18);
/* formatos que são sempre o próprio livro (e não uma resenha ou relatório): anexá-los não marca “possui análise”.
   PDF fica de fora da lista de propósito — pode ser o livro que você tem, pode ser um documento seu. */
const LIVRO_DIGITAL = /\.(epub|cbz|cbr|mobi|azw3|azw|djvu|fb2|lit)$/i;
const ehTexto = (nome, mime) => /^text\//i.test(mime || '') || /\.(txt|md|markdown|csv|tsv|json|log|tex|rst|org|htm|html|xml|ya?ml)$/i.test(nome || '');

const Anexos = {
  capas: new Map(),        // chave → imagem (data:…) das capas enviadas, já na memória: a tela se desenha sem esperar pelo banco
  mem: new Map(),          // sem IndexedDB: os anexos ficam aqui, só enquanto a página está aberta
  banco: null,
  abrir() {                // promessa do banco aberto — ou de null, se o navegador não deixa gravar
    if (!this.banco) this.banco = new Promise(res => {
      if (!Loja.ok) { res(null); return; }
      const tentar = (versao, vezes) => {
        let p; try { p = versao ? indexedDB.open('biblioteca-lucas', versao) : indexedDB.open('biblioteca-lucas'); } catch (e) { res(null); return; }
        p.onupgradeneeded = () => { if (!p.result.objectStoreNames.contains('anexos')) p.result.createObjectStore('anexos', { keyPath: 'k' }); };
        p.onsuccess = () => {
          const db = p.result;
          // um banco com este nome, mas sem a tabela (criado por outra página do mesmo endereço): sobe a versão para criá-la
          if (!db.objectStoreNames.contains('anexos')) { const v = db.version + 1; db.close(); if (vezes > 2) res(null); else tentar(v, vezes + 1); return; }
          db.onversionchange = () => { db.close(); this.banco = null; };     // outra aba vai mexer na estrutura: solta o banco e reabre no próximo uso
          res(db);
        };
        p.onerror = () => res(null);
      };
      tentar(0, 0);
    });
    return this.banco;
  },
  async op(modo, f) {      // roda f(tabela) numa transação e devolve o que os pedidos trouxeram
    const db = await this.abrir();
    return new Promise((res, rej) => {
      let r; const tx = db.transaction('anexos', modo);
      tx.oncomplete = () => res(Array.isArray(r) ? r.map(p => p.result) : r ? r.result : undefined);
      tx.onerror = tx.onabort = () => rej(tx.error || new Error('o navegador recusou a gravação'));
      try { r = f(tx.objectStore('anexos')); } catch (e) { rej(e); }
    });
  },
  async gravar(reg) { if (await this.abrir()) await this.op('readwrite', t => t.put(reg)); else this.mem.set(reg.k, reg); },
  async varios(chaves) { if (!chaves.length) return []; return (await this.abrir()) ? this.op('readonly', t => chaves.map(k => t.get(k))) : chaves.map(k => this.mem.get(k)); },
  async ler(k) { return (await this.varios([k]))[0] || null; },
  async chaves() { return (await this.abrir()) ? this.op('readonly', t => t.getAllKeys()) : [...this.mem.keys()]; },
  async apagar(chaves) { for (const k of chaves) { this.capas.delete(k); this.mem.delete(k); } if (chaves.length && (await this.abrir())) await this.op('readwrite', t => { chaves.forEach(k => t.delete(k)); }); },
  async limpar() { this.capas.clear(); this.mem.clear(); if (await this.abrir()) await this.op('readwrite', t => { t.clear(); }); },
};
const chavesDe = b => (b.cp ? [b.cp] : []).concat((b.anx || []).map(a => a[0]));
/* traz para a memória as capas enviadas pelo usuário e redesenha a tela quando elas chegam */
async function carregarCapas() {
  const quero = [...new Set(DB.livros.map(b => b.cp).filter(Boolean))]; Anexos.capas.clear();
  if (!quero.length) return;
  let n = 0;
  try { for (const r of await Anexos.varios(quero)) if (r && r.tipo === 'capa' && typeof r.dados === 'string' && /^data:image\//.test(r.dados)) { Anexos.capas.set(r.k, r.dados); n++; } } catch (e) { /* sem o banco, ficam as capas do catálogo */ }
  if (n) { render(); if (Gaveta.id) desenharGaveta(); }
}

/* ───────── arquivos: ler, reduzir, mostrar, baixar ───────── */
const lerArquivo = arq => new Promise((res, rej) => { const l = new FileReader(); l.onload = () => res(String(l.result)); l.onerror = () => rej(l.error || new Error('leitura')); l.readAsDataURL(arq); });
/* imagem escolhida → JPEG pequeno (data:…), do tamanho de uma capa: cabe no navegador e abre na hora */
async function reduzirImagem(arq) {
  const url = URL.createObjectURL(arq);
  try {
    const im = await new Promise((res, rej) => { const i = new Image(); i.onload = () => res(i); i.onerror = () => rej(new Error('imagem')); i.src = url; });
    const w = im.naturalWidth, h = im.naturalHeight; if (!w || !h) throw new Error('imagem');
    const k = Math.min(1, CAPA_MAX[0] / w, CAPA_MAX[1] / h), cv = document.createElement('canvas');
    cv.width = Math.max(1, Math.round(w * k)); cv.height = Math.max(1, Math.round(h * k));
    const g = cv.getContext('2d'); g.fillStyle = '#fff'; g.fillRect(0, 0, cv.width, cv.height);     // fundo branco: o JPEG não tem transparência
    g.imageSmoothingQuality = 'high'; g.drawImage(im, 0, 0, cv.width, cv.height);
    const dados = cv.toDataURL('image/jpeg', 0.84);
    if (!/^data:image\/jpeg;base64,/.test(dados)) throw new Error('imagem');
    return dados;
  } finally { URL.revokeObjectURL(url); }
}
const bytesDe = dados => { const bin = atob(dados.slice(dados.indexOf(',') + 1)), v = new Uint8Array(bin.length); for (let i = 0; i < bin.length; i++) v[i] = bin.charCodeAt(i); return v; };
/* conteúdo de um anexo de texto. UTF-8 é o comum; arquivos antigos do Windows vêm em UTF-16 ou em Windows-1252 */
function textoDoAnexo(dados) {
  const v = bytesDe(dados);
  if (v[0] === 0xFF && v[1] === 0xFE) return new TextDecoder('utf-16le').decode(v.subarray(2));
  if (v[0] === 0xFE && v[1] === 0xFF) return new TextDecoder('utf-16be').decode(v.subarray(2));
  try { return new TextDecoder('utf-8', { fatal: true }).decode(v); } catch (e) { return new TextDecoder('windows-1252').decode(v); }
}
function baixarAnexo(nome, dados) {
  if (!Loja.ok) { toast('Esta pré-visualização bloqueia downloads. No painel aberto no navegador o arquivo baixa normalmente.', 'aviso'); return; }
  const tipo = (/^data:([^;,]*)/.exec(dados) || [])[1] || 'application/octet-stream';
  const url = URL.createObjectURL(new Blob([bytesDe(dados)], { type: tipo })), a = document.createElement('a');
  a.href = url; a.download = nome; document.body.appendChild(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(url), 3000);
  toast('Arquivo baixado: ' + nome);
}

/* ───────── backup: os anexos vão e voltam junto com os livros ───────── */
async function exportarBackup() {
  const o = serializar(cfgAtual()), chaves = DB.livros.flatMap(chavesDe);
  try { o.anexos = (await Anexos.varios(chaves)).filter(Boolean).map(r => ({ k: r.k, livro: r.livro, tipo: r.tipo, nome: r.nome, mime: r.mime, tam: r.tam, dia: r.dia, dados: r.dados })); }
  catch (e) { toast('Não foi possível ler as capas e os arquivos anexados: este backup leva só os dados dos livros.', 'aviso'); }   // sem o campo `anexos`, importar este arquivo não mexe nos anexos que estão no navegador
  baixarArquivo(`biblioteca-lucas-backup-${iso(DB.hoje)}.json`, JSON.stringify(o), 'application/json');
}
/* anexos de um arquivo de backup: só passa o que está inteiro (nada aqui confia no formato) */
function lerAnexos(lista) {
  const out = [], vistos = new Set(), txt = (v, n) => (typeof v === 'string' ? v.slice(0, n) : '');
  for (const r of Array.isArray(lista) ? lista : []) {
    if (!r || typeof r !== 'object' || !chaveAnexo(r.k) || vistos.has(r.k) || typeof r.dados !== 'string' || r.dados.length > ANEXO_MAX * 1.4 + 400) continue;
    const tipo = r.tipo === 'capa' ? 'capa' : 'arquivo', ini = r.dados.slice(0, 200);
    if (!(tipo === 'capa' ? /^data:image\/(jpeg|png|webp|gif);base64,/ : /^data:[^,]{0,120};base64,/).test(ini)) continue;
    vistos.add(r.k);
    out.push({ k: r.k, livro: txt(r.livro, 40), tipo, nome: txt(r.nome, 120), mime: txt(r.mime, 80), tam: typeof r.tam === 'number' && isFinite(r.tam) && r.tam >= 0 ? Math.round(r.tam) : 0, dia: typeof r.dia === 'number' && isFinite(r.dia) ? Math.round(r.dia) : null, dados: r.dados });
  }
  return out;
}
/* Depois de trocar os livros pelos de um backup: os anexos do arquivo substituem os que estavam no navegador.
   Um backup sem o campo `anexos` (feito por um painel antigo, ou quando o banco não pôde ser lido) não mexe neles.
   No fim, nenhum livro fica apontando para um anexo que não existe. */
async function restaurarAnexos(o) {
  let existentes;
  try {
    if (Array.isArray(o.anexos)) { const lista = lerAnexos(o.anexos); await Anexos.limpar(); for (const r of lista) await Anexos.gravar(r); existentes = new Set(lista.map(r => r.k)); }
    else existentes = new Set(await Anexos.chaves());
  } catch (e) { existentes = new Set(); toast('As capas e os arquivos do backup não puderam ser guardados neste navegador.', 'aviso'); }
  let mudou = false;
  for (const b of DB.livros) {
    if (b.cp && !existentes.has(b.cp)) { b.cp = ''; mudou = true; }
    if (b.anx && b.anx.some(a => !existentes.has(a[0]))) { b.anx = b.anx.filter(a => existentes.has(a[0])); if (!b.anx.length) b.anx = null; derivar(b); mudou = true; }
  }
  if (mudou) salvar();
  // o que sobrou no banco e nenhum livro usa (anexos dos dados que acabaram de ser substituídos) sai
  const usados = new Set(DB.livros.flatMap(chavesDe));
  Anexos.apagar([...existentes].filter(k => !usados.has(k))).catch(() => {});
  await carregarCapas();
  render(); if (Gaveta.id) desenharGaveta();
}

/* ───────── "Suas anotações", na ficha do livro ─────────
   A seção é montada uma vez e só troca de conteúdo quando muda o livro: o que está sendo digitado não se perde quando o
   resto da ficha é redesenhado. O comentário é gravado sozinho — ao parar de digitar, ao sair do campo e ao fechar a ficha. */
const Notas = {
  id: null, relogio: 0,
  montar(sec) {
    sec.innerHTML = `<div class="gv-st"><h4 id="nt-t">Suas anotações</h4><span id="nt-st" role="status" aria-live="polite"></span></div>
      <textarea id="nt-com" rows="3" maxlength="${MAX_COMENTARIO}" aria-label="Comentários sobre este livro" placeholder="Escreva aqui seus comentários sobre este livro: impressões, trechos, por que ler (ou não)…"></textarea>
      <p class="nt-cont" id="nt-cont" hidden></p>
      <label class="opt so nt-an"><input type="checkbox" id="nt-an"><span>Possui análise <small>resenha, relatório, fichamento…</small></span></label>
      <ul class="nt-arqs" id="nt-arqs" aria-label="Arquivos anexados"></ul>
      <div class="nt-b"><button type="button" class="btn sm" data-nt="anexar">${icone('clipe', 14)}Anexar arquivo…</button><button type="button" class="btn sm" data-nt="capa">${icone('imagem', 14)}<span id="nt-capa-r">Enviar capa…</span></button><button type="button" class="btn sm" data-nt="sem-capa" hidden>${icone('desfazer', 14)}Tirar a capa enviada</button></div>
      <p class="nota" id="nt-n"></p>
      <input type="file" id="nt-f-arq" hidden aria-hidden="true" tabindex="-1"><input type="file" id="nt-f-capa" accept="image/*" hidden aria-hidden="true" tabindex="-1">`;
    const ta = $('#nt-com', sec), atrasado = debounce(() => this.guardar(), 700);
    ta.addEventListener('input', () => { this.contar(); atrasado(); });
    ta.addEventListener('change', () => this.guardar());
    $('#nt-an', sec).addEventListener('change', e => { const b = porId(this.id); if (!b) return; this.guardar(); defTag(b, TAG_ANALISE, e.target.checked); tocar(b); this.estado(e.target.checked ? 'Marcado: possui análise' : 'Marca retirada'); });
    sec.addEventListener('click', e => {
      const bt = e.target.closest('[data-nt]'); if (!bt) return; const x = bt.dataset.nt;
      if (x === 'anexar') $('#nt-f-arq', sec).click(); else if (x === 'capa') $('#nt-f-capa', sec).click();
      else if (x === 'sem-capa') this.tirarCapa(); else if (x === 'abrir') this.abrir(bt.dataset.k); else if (x === 'baixar') this.baixar(bt.dataset.k); else if (x === 'tirar') this.tirar(bt.dataset.k);
    });
    $('#nt-f-arq', sec).addEventListener('change', e => { const f = e.target.files && e.target.files[0]; e.target.value = ''; if (f) this.anexar(f); });
    $('#nt-f-capa', sec).addEventListener('change', e => { const f = e.target.files && e.target.files[0]; e.target.value = ''; if (f) this.enviarCapa(f); });
  },
  estado(msg) { const el = $('#nt-st'); if (!el) return; el.textContent = msg; clearTimeout(this.relogio); if (msg) this.relogio = setTimeout(() => { el.textContent = ''; }, 2600); },
  contar() { const ta = $('#nt-com'), el = $('#nt-cont'), n = ta.value.length; el.hidden = n < MAX_COMENTARIO * 0.9; if (!el.hidden) el.textContent = `${fInt(n)} de ${fInt(MAX_COMENTARIO)} caracteres. Para textos longos, anexe um arquivo.`; },
  /* grava o comentário que está no campo, se mudou. Não redesenha a ficha: quem estava clicando num botão dela não perde o clique. */
  guardar() {
    const b = porId(this.id), ta = $('#nt-com'); if (!b || !ta) return;
    const v = ta.value.slice(0, MAX_COMENTARIO).replace(/\s+$/, '');
    if (v === (b.com || '')) return;
    const aparece = !b.u || !v !== !b.com;        // o livro entra em (ou sai de) "Com anotações" e "Editados por você": as tabelas mudam
    b.com = v; marcarMeu(b); derivar(b); salvar();
    this.estado(v ? 'Comentário salvo' : 'Comentário apagado');
    if (aparece) render();
  },
  fechar() { this.guardar(); this.id = null; },
  desenhar(b) {
    const ta = $('#nt-com'); if (!ta) return;
    if (this.id !== b.id) { this.guardar(); this.id = b.id; ta.value = b.com || ''; this.estado(''); this.contar(); }
    $('#nt-an').checked = b.tags.includes(TAG_ANALISE);
    const an = b.anx || [];
    setHtml($('#nt-arqs'), an.map(a => `<li><span class="nt-a" title="${esc(a[1])}">${icone('clipe', 14)}<b>${esc(a[1])}</b><small>${fTam(a[2])}${a[3] != null ? ' · ' + fData(a[3]) : ''}</small></span><span class="nt-ab">${ehTexto(a[1], a[4]) ? `<button type="button" class="lnk" data-nt="abrir" data-k="${a[0]}" aria-label="Abrir ${esc(a[1])}">abrir</button>` : ''}<button type="button" class="lnk" data-nt="baixar" data-k="${a[0]}" aria-label="Baixar ${esc(a[1])}">baixar</button><button type="button" class="lnk" data-nt="tirar" data-k="${a[0]}" aria-label="Remover ${esc(a[1])}">remover</button></span></li>`).join(''));
    $('#nt-arqs').hidden = !an.length;
    $('#nt-capa-r').textContent = b.cp ? 'Trocar a capa…' : urlCapa(b) ? 'Enviar outra capa…' : 'Enviar capa…';
    $('[data-nt="sem-capa"]').hidden = !b.cp;
    $('#nt-n').textContent = Loja.ok ? 'Comentários, capa e arquivos ficam só neste navegador e entram no backup (em “Seus dados”).' : 'Pré-visualização: o que você anotar aqui vale só até fechar a página.';
  },
  async podeGuardar() {
    if (Loja.ok && !(await Anexos.abrir())) { toast('Este navegador não deixou guardar arquivos (janela anônima ou armazenamento bloqueado). Nada foi anexado.', 'erro'); return false; }
    return true;
  },
  async anexar(arq) {
    const b = porId(this.id); if (!b) return;
    const nome = (arq.name || 'arquivo').slice(0, 120), mime = (arq.type || '').slice(0, 80);
    const digital = DIGITAL_CAPA.test(nome);                               // EPUB/CBZ: dá para ler a capa sem guardar o arquivo
    const vazio = !arq.size, grande = arq.size > ANEXO_MAX, cheios = (b.anx || []).length >= MAX_ANEXOS;
    const fora = vazio ? 'Este arquivo está vazio.'
      : cheios ? `Cada livro guarda até ${MAX_ANEXOS} arquivos. Remova um para anexar outro.`
      : grande ? `O arquivo tem ${fTam(arq.size)}; o limite é de ${fTam(ANEXO_MAX)} por arquivo.` : '';
    if (fora && !(digital && !vazio)) { toast(fora, 'aviso'); return; }   // o que não é livro digital obedece às regras de sempre
    if (!(await this.podeGuardar())) return;
    const capa = await this.capaDoArquivoDigital(arq, b);                  // só a leitura, no computador: nenhum limite de tamanho a atrapalha
    let anexado = false;
    if (!fora) {
      const k = novaChave();
      try { await Anexos.gravar({ k, livro: b.id, tipo: 'arquivo', nome, mime, tam: arq.size, dia: DB.hoje, dados: await lerArquivo(arq) }); }
      catch (e) { toast('Não foi possível guardar o arquivo neste navegador (sem espaço, ou o arquivo não pôde ser lido).', 'erro'); return; }
      if (porId(b.id) !== b) { Anexos.apagar([k]); return; }               // o livro saiu do painel enquanto o arquivo era lido
      if (this.id === b.id) this.guardar();
      (b.anx || (b.anx = [])).push([k, nome, arq.size, DB.hoje, mime]);
      anexado = true;
    }
    let virouCapa = false;
    if (capa && !b.cp) {                        // o livro ganhou uma capa enquanto o arquivo era lido? então a nossa não entra
      const [kc] = await this.gravarCapa(b, capa.dados, capa.nome);
      if (kc && b.cp) Anexos.apagar([kc]).catch(() => {});
      else if (kc) { b.cp = kc; virouCapa = true; }
    }
    if (!anexado && !virouCapa) { toast(fora, 'aviso'); return; }          // nada mudou na ficha: o motivo, dito como sempre foi
    const marcou = anexado && !LIVRO_DIGITAL.test(nome) && !b.tags.includes(TAG_ANALISE);   // um arquivo seu é análise; o próprio livro digital, não
    if (marcou) defTag(b, TAG_ANALISE, true);
    tocar(b);
    toast((anexado ? (marcou ? 'Arquivo anexado. O livro foi marcado com “possui análise”.' : 'Arquivo anexado.')
      : grande ? `O arquivo é grande demais para ficar guardado aqui (${fTam(arq.size)}; o limite é ${fTam(ANEXO_MAX)}) — mas a capa dele foi lida e virou a capa do livro.`
      : `Este livro já guarda ${MAX_ANEXOS} arquivos, então ele não foi anexado — mas a capa dele foi lida e virou a capa do livro.`)
      + (virouCapa && anexado ? ' A capa que estava dentro do arquivo virou a capa do livro.' : ''));
  },
  /* EPUB e CBZ trazem a capa dentro do arquivo (ver 54-capa-digital): usamos a imagem, lida aqui no navegador, sem
     internet. Só quando o livro está sem capa nenhuma — nem uma enviada, nem a do catálogo —, para nunca trocar uma
     capa que já existe pela que vem no arquivo. Não achou nada, ou o navegador não abriu a imagem? Fica como estava, sem aviso. */
  async capaDoArquivoDigital(arq, b) {
    if (b.cp || temCapa(b) || !DIGITAL_CAPA.test(arq.name || '')) return null;
    const achada = await capaDoDigital(arq); if (!achada) return null;
    try { return { nome: 'capa de ' + achada.nome, dados: await reduzirImagem(achada.blob) }; } catch (e) { return null; }
  },
  /* guarda uma imagem como capa do livro: é assim que ela vale mais que a do catálogo, aparece com as capas desligadas,
     entra no backup e pode ser tirada na ficha. Devolve [chave do anexo, motivo da recusa] — vazio quando deu certo. */
  async gravarCapa(b, dados, nome) {
    const k = novaChave();
    try { await Anexos.gravar({ k, livro: b.id, tipo: 'capa', nome: String(nome || 'capa').slice(0, 120), mime: 'image/jpeg', tam: Math.round((dados.length - 23) * 0.75), dia: DB.hoje, dados }); }
    catch (e) { return ['', 'navegador']; }
    if (porId(b.id) !== b) { Anexos.apagar([k]).catch(() => {}); return ['', 'saiu']; }      // o livro saiu do painel enquanto a imagem era lida
    Anexos.capas.set(k, dados);
    return [k, ''];
  },
  async enviarCapa(arq) {
    const b = porId(this.id); if (!b) return;
    if (!(await this.podeGuardar())) return;
    let dados; try { dados = await reduzirImagem(arq); } catch (e) { toast('Não consegui abrir este arquivo como imagem. Use uma foto ou imagem em JPG, PNG ou WebP.', 'erro'); return; }
    const antiga = b.cp, [k, motivo] = await this.gravarCapa(b, dados, arq.name || 'capa');
    if (!k) { if (motivo === 'navegador') toast('Não foi possível guardar a imagem neste navegador (sem espaço ou armazenamento bloqueado).', 'erro'); return; }
    if (this.id === b.id) this.guardar();
    b.cp = k; if (antiga) Anexos.apagar([antiga]).catch(() => {});
    tocar(b); toast(antiga ? 'Capa trocada.' : 'Capa enviada.');
  },
  tirarCapa() {
    const b = porId(this.id); if (!b || !b.cp) return;
    const k = b.cp; b.cp = ''; Anexos.apagar([k]).catch(() => {});
    tocar(b); toast(urlCapa(b) ? 'Capa enviada removida: voltou a do catálogo.' : 'Capa enviada removida.');
  },
  async pegar(k) {         // [linha do anexo no livro, registro guardado] — avisa se o conteúdo não está mais no navegador
    const b = porId(this.id), a = b && (b.anx || []).find(x => x[0] === k); if (!a) return [];
    let reg = null; try { reg = await Anexos.ler(k); } catch (e) { /* tratado abaixo */ }
    if (!reg || typeof reg.dados !== 'string') { toast('O conteúdo deste arquivo não está mais guardado neste navegador. Remova-o da lista e anexe de novo.', 'aviso'); return []; }
    return [a, reg, b];
  },
  async abrir(k) {
    const [a, reg, b] = await this.pegar(k); if (!a) return;
    let txt; try { txt = textoDoAnexo(reg.dados); } catch (e) { baixarAnexo(a[1], reg.dados); return; }
    const corte = 200000;
    Dlg.abrir({ titulo: a[1], largo: true, corpo: `<p class="dlg-sub">Anexo de <b>${esc(b.t)}</b> · ${fTam(a[2])}${a[3] != null ? ' · anexado em ' + fData(a[3]) : ''}</p><pre class="anexo-txt" tabindex="0" data-foco>${esc(txt.slice(0, corte))}</pre>${txt.length > corte ? '<p class="nota">O arquivo é longo: aqui aparece só o começo. Baixe para ler inteiro.</p>' : ''}`,
      botoes: [{ n: 'Baixar', acao: () => { baixarAnexo(a[1], reg.dados); return false; } }, { n: 'Fechar', cls: 'pri' }] });
  },
  async baixar(k) { const [a, reg] = await this.pegar(k); if (a) baixarAnexo(a[1], reg.dados); },
  tirar(k) {
    const b = porId(this.id), a = b && (b.anx || []).find(x => x[0] === k); if (!a) return;
    confirmar('Remover arquivo', `Remover <b>${esc(a[1])}</b> deste livro? O arquivo sai do painel (o original, no seu computador, não é tocado).`, 'Remover', () => {
      b.anx = b.anx.filter(x => x[0] !== k); if (!b.anx.length) b.anx = null;
      Anexos.apagar([k]).catch(() => {});
      tocar(b); toast(!b.anx && b.tags.includes(TAG_ANALISE) ? 'Arquivo removido. A marca “possui análise” continua: desmarque se não valer mais.' : 'Arquivo removido.');
    }, true);
  },
};
