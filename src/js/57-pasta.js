/* ───────────────────────── a pasta dos livros: achar e abrir os arquivos (Etapa 11, parte 1) ─────────────────────────
   No computador, o Chrome e o Edge deixam um site ler uma pasta que o usuário escolhe ("conectar a pasta"). O painel
   percorre a pasta e as subpastas, guarda só os NOMES do que encontrou e os cruza com os nomes de arquivo do catálogo
   (ARQUIVOS, que vem de biblioteca-virtual/inventario.tsv). Com isso a ficha de cada livro diz onde o arquivo está e,
   se for PDF, abre.
   · O painel só lê: o pedido feito ao navegador é de leitura. Nenhum arquivo e nenhum nome sai do aparelho.
   · O que fica guardado — a ligação com a pasta e a lista de nomes da última conferência — mora num banco à parte do
     navegador (IndexedDB "biblioteca-lucas-pasta"). Não entra no backup nem é mexido quando um backup é importado: é
     deste aparelho. "Recomeçar do catálogo original" apaga.
   · A cada visita o navegador pode pedir de novo a confirmação do acesso, e só aceita o pedido dentro de um clique.
   · Onde não há como (Firefox, Safari, iPhone, a prévia dentro de moldura), o painel explica em vez de oferecer. */

/* chave:inicio — A MESMA CONTA está em tools/build_catalog.py (miolo, extensao_de, chave_arquivo). Os nomes do catálogo
   vieram de listagens feitas pelo `dir` do Windows, que troca o que a página de código dele não tem (travessão por hífen,
   aspas curvas por retas, acento "solto" no lugar do combinado…). Por isso, quando o nome exato não aparece na pasta, vale
   a chave: só letras e algarismos, sem acento e em minúsculas, mais a extensão. tools/qa/pasta.py confere que as duas
   contas dão o mesmo resultado em todos os nomes do inventário. */
const SEM_DECOMPOSICAO = { 'ß': 'ss', 'æ': 'ae', 'œ': 'oe', 'ø': 'o', 'đ': 'd', 'ð': 'd', 'þ': 'th', 'ł': 'l', 'ı': 'i' };
const miolo = s => String(s ?? '').normalize('NFKD').toLowerCase().replace(/[^\p{L}\p{N}]+/gu, '').replace(/[ßæœøđðþłı]/g, c => SEM_DECOMPOSICAO[c]);
const extensaoDe = nome => { const m = /\.([A-Za-z0-9]{2,5})$/.exec(String(nome ?? '')); return m ? m[1].toLowerCase() : ''; };
const chaveArquivo = nome => { const e = extensaoDe(nome), k = miolo(e ? String(nome).slice(0, -e.length - 1) : nome); return k ? k + '.' + e : ''; };
/* chave:fim */

const EXT_LIVRO = new Set(ARQUIVOS.ext);                                   // extensões de arquivo de livro (as de tools/importar_digital.py)
const ordemNome = (a, b) => a.localeCompare(b, 'pt-BR', { numeric: true, sensitivity: 'base' }) || (a < b ? -1 : a > b ? 1 : 0);
// séries de quadrinhos guardadas em subpasta própria: [nome da subpasta, [linhas do catálogo]] (sexto item dos dados digitais)
const SERIES = (() => { const m = new Map(); CATALOGO.forEach((r, i) => { for (const s of (r[6] && r[6][5]) || []) { if (!m.has(s)) m.set(s, []); m.get(s).push(i); } }); return [...m]; })();
const N_DA_SERIE = new Map(SERIES.map((s, n) => [s[0], n]));
const MIN_SERIES_IRMAS = 3;      // uma pasta só vale como "a da série" se estiver ao lado de pelo menos outras duas com nome de série
const PASTA_DE_SISTEMA = /^(\$RECYCLE\.BIN|System Volume Information|\..*)$/i;      // lixeira, pastas do sistema e pastas ocultas: não se entra
const PAROU = new Error('conferência cancelada');
const LISTA_MAX = 150;           // quantas linhas de cada lista cabem na tela; o relatório (.txt) leva todas

/* dá para conectar uma pasta aqui? '' = sim; 'moldura' = o painel está dentro de outra página (a prévia); 'navegador' = não existe */
function semPasta() {
  let moldura; try { moldura = window.top !== window.self; } catch (e) { moldura = true; }
  return moldura ? 'moldura' : typeof window.showDirectoryPicker === 'function' ? '' : 'navegador';
}

/* ───────── o que fica guardado no navegador ───────── */
const CofrePasta = {
  banco: null,
  abrir() {                // promessa do banco aberto — ou de null, se o navegador não deixa gravar
    if (!this.banco) this.banco = new Promise(res => {
      if (!Loja.ok) { res(null); return; }
      let p; try { p = indexedDB.open('biblioteca-lucas-pasta', 1); } catch (e) { res(null); return; }
      p.onupgradeneeded = () => { if (!p.result.objectStoreNames.contains('pasta')) p.result.createObjectStore('pasta'); };
      p.onsuccess = () => { const db = p.result; db.onversionchange = () => { db.close(); this.banco = null; }; res(db); };
      p.onerror = p.onblocked = () => res(null);
    });
    return this.banco;
  },
  async op(modo, f) {      // roda f(tabela) numa transação; devolve [deu certo, o que o pedido trouxe]
    const db = await this.abrir(); if (!db) return [false];
    return new Promise(res => {
      let r; const tx = db.transaction('pasta', modo);
      tx.oncomplete = () => res([true, r ? r.result : undefined]);
      tx.onerror = tx.onabort = () => res([false]);
      try { r = f(tx.objectStore('pasta')); } catch (e) { res([false]); }
    });
  },
  async ler() { return (await this.op('readonly', t => t.get('raiz')))[1] || null; },
  async gravar(reg) { return (await this.op('readwrite', t => t.put(reg, 'raiz')))[0]; },
  async apagar() { return (await this.op('readwrite', t => t.delete('raiz')))[0]; },
};

const Pasta = {
  pronta: false,       // já se sabe o que estava guardado no navegador
  raiz: null,          // a pasta conectada (FileSystemDirectoryHandle); null = nenhuma
  nome: '', quando: 0, // o nome dela e o momento da última conferência
  dirs: [], arqs: [],  // a última conferência: pastas (cada uma, a lista de nomes desde a raiz) e arquivos [nº da pasta, nome]
  erros: [],           // pastas que não deu para ler
  lembrada: false,     // o navegador guardou a ligação (volta na próxima visita)
  perm: '',            // o que o navegador diz do acesso: 'granted', 'prompt' ou 'denied'
  lendo: null,         // conferência em andamento: { nome, arqs, dirs, parar }
  res: null, num: null,// o cruzamento com o catálogo (cruzarPasta) e os números dele (numerosPasta)
  urls: [],            // endereços (blob:) dos arquivos abertos nesta visita
};

const permissaoDe = async h => { try { return h.queryPermission ? await h.queryPermission({ mode: 'read' }) : 'granted'; } catch (e) { return 'prompt'; } };
// o pedido só é aceito dentro de um clique; fora dele o navegador recusa, e continua valendo "falta confirmar"
const pedirPermissao = async h => { try { return h.requestPermission ? await h.requestPermission({ mode: 'read' }) : 'granted'; } catch (e) { return 'prompt'; } };

/* ───────── percorrer a pasta ───────── */
async function varrerPasta(raiz, estado) {
  const dirs = [[]], arqs = [], erros = [];
  const descer = async (h, k) => {
    const subs = [], nomes = [];
    try {
      for await (const [nome, f] of h.entries()) {
        if (estado.parar) throw PAROU;
        if (f.kind === 'directory') { if (!PASTA_DE_SISTEMA.test(nome)) subs.push([nome, f]); } else nomes.push(nome);
      }
    } catch (e) { if (e === PAROU) throw e; erros.push(dirs[k].join('\\') || raiz.name); }
    nomes.sort(ordemNome); for (const n of nomes) arqs.push([k, n]);
    estado.arqs = arqs.length; estado.dirs = dirs.length; pintarAndamento();
    subs.sort((a, b) => ordemNome(a[0], b[0]));
    for (const [nome, f] of subs) { dirs.push(dirs[k].concat(nome)); await descer(f, dirs.length - 1); }
  };
  await descer(raiz, 0);
  return { dirs, arqs, erros };
}

/* ───────── cruzar a pasta com o catálogo ─────────
   Cada nome do catálogo (e cada nome que fica só no inventário) é procurado entre os arquivos de livro da pasta:
   primeiro pelo nome exato; o que sobrar, pela chave. O que está dentro da subpasta de uma série de quadrinhos e não
   é arquivo do catálogo conta como edição da série. O resto dos arquivos de livro é "novo": está na pasta e o catálogo
   não conhece. Devolve posições: em ARQUIVOS (achados), em SERIES (series) e em `arqs` (o que foi achado). */
function cruzarPasta(dirs, arqs) {
  const junta = (m, k, v) => { const l = m.get(k); if (l) l.push(v); else m.set(k, [v]); };
  const nCat = ARQUIVOS.arquivos.length, conhecidos = ARQUIVOS.arquivos.concat(ARQUIVOS.fora).map(a => a[0].normalize('NFC'));
  const porNome = new Map(), porChave = new Map(), livros = [], outros = [];
  arqs.forEach((a, d) => {
    const nome = a[1].normalize('NFC');
    if (!EXT_LIVRO.has(extensaoDe(nome))) { outros.push(d); return; }
    livros.push(d); junta(porNome, nome, d); junta(porChave, chaveArquivo(nome), d);
  });
  const achados = conhecidos.map(n => (porNome.get(n) || []).slice()), dono = new Map();
  achados.forEach((l, i) => l.forEach(d => dono.set(d, i)));
  // pela chave: só para o nome que não apareceu exato, e só com arquivos que não são, eles mesmos, um nome conhecido
  const pendentes = new Map();
  conhecidos.forEach((n, i) => { if (!achados[i].length) { const k = chaveArquivo(n); if (k) junta(pendentes, k, i); } });
  for (const [k, is] of pendentes) (porChave.get(k) || []).filter(d => !dono.has(d)).forEach((d, j) => { const i = is[Math.min(j, is.length - 1)]; achados[i].push(d); dono.set(d, i); });
  // séries: a pasta com o nome da subpasta (pela chave), ao lado de outras pastas com nome de série; vale para tudo o que há dentro
  const chaveSerie = new Map(SERIES.map((s, n) => [miolo(s[0]), n])), posicao = new Map(dirs.map((p, k) => [p.join('\u0000'), k]));
  const mae = dirs.map(p => (p.length ? posicao.get(p.slice(0, -1).join('\u0000')) : -1));
  const candidata = dirs.map(p => { const n = p.length ? chaveSerie.get(miolo(p[p.length - 1])) : undefined; return n == null ? -1 : n; });
  const irmas = new Map(); candidata.forEach((s, k) => { if (s >= 0) irmas.set(mae[k], (irmas.get(mae[k]) || 0) + 1); });
  const series = SERIES.map(() => ({ dirs: [], arqs: [], outros: 0 })), serieDe = [];
  dirs.forEach((p, k) => {                                   // as pastas vêm em ordem: a mãe sempre antes das filhas
    const herdada = k ? serieDe[mae[k]] : -1;
    serieDe[k] = herdada >= 0 ? herdada : candidata[k] >= 0 && irmas.get(mae[k]) >= MIN_SERIES_IRMAS ? candidata[k] : -1;
    if (serieDe[k] >= 0 && herdada < 0) series[serieDe[k]].dirs.push(k);
  });
  const novos = [], soltos = [];
  for (const d of livros) { if (dono.has(d)) continue; const s = serieDe[arqs[d][0]]; if (s >= 0) series[s].arqs.push(d); else novos.push(d); }
  for (const d of outros) { const s = serieDe[arqs[d][0]]; if (s >= 0) series[s].outros++; else soltos.push(d); }
  return { achados, nCat, series, novos, outros: soltos, nLivros: livros.length };
}
const ehPdf = d => extensaoDe(Pasta.arqs[d][1]) === 'pdf';
function numerosPasta(r) {
  const cat = ARQUIVOS.arquivos, n = cat.length; let achados = 0, menos = 0, mais = 0, fora = 0;
  for (let i = 0; i < n; i++) { const a = r.achados[i].length, e = cat[i][1].length; if (a) achados++; if (a && a < e) menos++; if (a > e) mais++; }
  for (let i = n; i < r.achados.length; i++) if (r.achados[i].length) fora++;
  // por livro: tem ao menos um arquivo (ou a pasta da série)? tem ao menos um PDF?
  let livros = 0, comAlgo = 0, comPdf = 0;
  CATALOGO.forEach((linha, i) => {
    if (!linha[6]) return; livros++;
    const dele = (ARQ_DA_LINHA.get(i) || []).flatMap(x => r.achados[x]), ss = (linha[6][5] || []).map(s => r.series[N_DA_SERIE.get(s)]);
    if (dele.length || ss.some(s => s.dirs.length)) comAlgo++;
    if (dele.some(ehPdf) || ss.some(s => s.arqs.some(ehPdf))) comPdf++;
  });
  return { arquivos: n, achados, faltam: n - achados, menos, mais, fora: ARQUIVOS.fora.length, foraAchados: fora,
    series: SERIES.length, seriesAchadas: r.series.filter(s => s.dirs.length).length, edicoes: soma(r.series, s => s.arqs.length),
    novos: r.novos.length, outros: r.outros.length, livros, comAlgo, comPdf, naPasta: Pasta.arqs.length, pastas: Pasta.dirs.length, deLivro: r.nLivros };
}
function adotarPasta(raiz, o) {
  Pasta.raiz = raiz; Pasta.nome = raiz.name || 'a pasta escolhida'; Pasta.quando = o.quando; Pasta.dirs = o.dirs; Pasta.arqs = o.arqs; Pasta.erros = o.erros || [];
  Pasta.res = cruzarPasta(Pasta.dirs, Pasta.arqs); Pasta.num = numerosPasta(Pasta.res);
}
const registroValido = o => !!o && o.v === 1 && !!o.raiz && o.raiz.kind === 'directory' && Array.isArray(o.dirs) && o.dirs.every(Array.isArray) && Array.isArray(o.arqs)
  && o.arqs.every(a => Array.isArray(a) && Number.isInteger(a[0]) && a[0] >= 0 && a[0] < o.dirs.length && typeof a[1] === 'string');

/* ───────── conectar, conferir de novo, esquecer ───────── */
async function carregarPasta() {                 // ao abrir o painel: o que o navegador tinha guardado
  try {
    if (!semPasta()) {
      const o = await CofrePasta.ler();
      if (registroValido(o)) { adotarPasta(o.raiz, o); Pasta.lembrada = true; Pasta.perm = await permissaoDe(o.raiz); }
    }
  } catch (e) { /* um registro que não dá para ler vale como nenhum */ }
  Pasta.pronta = true; pastaMudou();
}
async function conferirPasta(raiz) {             // percorre, cruza com o catálogo e guarda
  if (Pasta.lendo) return;
  Pasta.lendo = { nome: raiz.name || 'a pasta escolhida', arqs: 0, dirs: 1, parar: false }; pastaMudou();
  try {
    const o = await varrerPasta(raiz, Pasta.lendo); o.quando = Date.now();
    adotarPasta(raiz, o); Pasta.perm = 'granted';
    Pasta.lembrada = await CofrePasta.gravar({ v: 1, raiz, nome: Pasta.nome, quando: o.quando, dirs: o.dirs, arqs: o.arqs, erros: o.erros });
    const n = Pasta.num; toast(`Pasta conferida: achei ${fInt(n.achados)} dos ${fInt(n.arquivos)} arquivos do catálogo.`);
  } catch (e) { if (e !== PAROU) toast('Não foi possível ler a pasta. Tente de novo ou escolha outra.', 'erro'); }
  Pasta.lendo = null; pastaMudou();
  if ($('#dp')) focar($('#dp [data-foco]'));
}
async function conectarPasta() {                 // precisa vir de um clique: o navegador abre a janela de escolher a pasta
  if (semPasta() || Pasta.lendo) return;
  let raiz;
  try { raiz = await window.showDirectoryPicker({ id: 'biblioteca-livros', mode: 'read' }); }
  catch (e) { if (!e || e.name !== 'AbortError') toast('O navegador não abriu a janela de escolher a pasta. Tente de novo.', 'erro'); return; }
  await conferirPasta(raiz);
}
async function acessoAPasta() {                  // o navegador deixa ler agora? Se faltar a confirmação, pede (só dentro de um clique)
  if (!Pasta.raiz) return false;
  let p = await permissaoDe(Pasta.raiz);
  if (p !== 'granted') p = await pedirPermissao(Pasta.raiz);
  const mudou = p !== Pasta.perm; Pasta.perm = p; if (mudou) pastaMudou();
  return p === 'granted';
}
const avisoSemAcesso = () => toast(Pasta.perm === 'denied' ? 'Sem a sua permissão o navegador não deixa o painel ler a pasta.' : 'O navegador quer confirmar o acesso à pasta. Clique de novo.', 'aviso');
async function reconferirPasta() {
  if (!Pasta.raiz || Pasta.lendo) return;
  if (!(await acessoAPasta())) { avisoSemAcesso(); return; }
  await conferirPasta(Pasta.raiz);
}
async function esquecerPasta() {
  Pasta.urls.forEach(u => URL.revokeObjectURL(u));
  Object.assign(Pasta, { raiz: null, nome: '', quando: 0, dirs: [], arqs: [], erros: [], lembrada: false, perm: '', res: null, num: null, urls: [] });
  await CofrePasta.apagar(); pastaMudou();
}

/* ───────── abrir um arquivo (por enquanto, PDF: no leitor do próprio navegador, numa aba nova) ───────── */
async function arquivoDaPasta(d) {               // o arquivo de número d da última conferência; dá erro se não estiver mais lá
  const [k, nome] = Pasta.arqs[d]; let h = Pasta.raiz;
  for (const parte of Pasta.dirs[k]) h = await h.getDirectoryHandle(parte);
  return (await h.getFileHandle(nome)).getFile();
}
function escreverAba(aba, titulo, url) {
  const t = esc(titulo), d = aba.document;
  d.open();
  d.write(`<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>${t} — Biblioteca do Lucas</title>`
    + '<style>html,body{height:100%;margin:0;background:#3b3d40;color:#ece9e2;font:16px/1.5 system-ui,sans-serif}iframe{display:block;width:100%;height:100%;border:0}p{margin:0;padding:28px}</style></head>'
    + `<body>${url ? `<iframe src="${esc(url)}" title="${t}"></iframe>` : `<p>Abrindo ${t}…</p>`}</body></html>`);
  d.close();
}
async function abrirDaPasta(d, titulo) {
  if (!Pasta.raiz || !Pasta.arqs[d]) return;
  const nome = Pasta.arqs[d][1];
  // O navegador só abre uma aba a pedido de um clique, e o pedido vale por poucos segundos. Com o acesso já confirmado,
  // a aba abre agora e o arquivo chega em seguida; sem ele, primeiro vem a pergunta do navegador — e, se a resposta
  // demorar, a aba já não abre: o painel pede mais um clique.
  let aba = null;
  if (Pasta.perm === 'granted') { try { aba = window.open('', '_blank'); } catch (e) { aba = null; } if (aba) escreverAba(aba, titulo, ''); }
  const desistir = () => { if (aba) try { aba.close(); } catch (e) { /* nada */ } };
  try {
    if (!(await acessoAPasta())) { desistir(); avisoSemAcesso(); return; }
    const arq = await arquivoDaPasta(d), url = URL.createObjectURL(arq.type === 'application/pdf' ? arq : arq.slice(0, arq.size, 'application/pdf'));
    Pasta.urls.push(url);
    if (!aba) { try { aba = window.open('', '_blank'); } catch (e) { aba = null; } }
    if (!aba) { toast('Acesso confirmado. Clique em “Abrir” mais uma vez — se a aba não abrir, permita pop-ups para este site.', 'aviso'); return; }
    escreverAba(aba, titulo, url);
  } catch (e) {
    desistir();
    toast(e && e.name === 'NotFoundError' ? `Não achei mais “${nome}” onde ele estava. Abra “Pasta dos livros” e use “Procurar de novo”.` : `Não foi possível abrir “${nome}”.`, e && e.name === 'NotFoundError' ? 'aviso' : 'erro');
  }
}

/* ───────── o que cada livro tem na pasta ───────── */
const ondeEsta = (d, sep = ' › ') => { const p = Pasta.dirs[Pasta.arqs[d][0]]; return p.length ? p.join(sep) : ''; };
function arquivosDoLivro(b) {
  const r = Pasta.res, g = b._dg;
  const arqs = (b._arq || []).map(n => { const a = ARQUIVOS.arquivos[n]; return { n, nome: a[0], ext: extensaoDe(a[0]), pastas: a[1].map(p => ARQUIVOS.pastas[p]), onde: r ? r.achados[n] : [] }; }).sort((x, y) => ordemNome(x.nome, y.nome));
  const series = ((g && g[5]) || []).map(nome => { const s = r && N_DA_SERIE.has(nome) ? r.series[N_DA_SERIE.get(nome)] : null; return { nome, dirs: s ? s.dirs : [], arqs: s ? s.arqs : [], outros: s ? s.outros : 0 }; });
  return { arqs, series };
}
const semExt = nome => { const e = extensaoDe(nome); return e ? nome.slice(0, -e.length - 1) : nome; };
const NOTA_SO_PDF = 'Por enquanto o painel abre só PDF. O leitor dos outros formatos ainda vai chegar.';
function htmlArquivos(b) {
  const { arqs, series } = arquivosDoLivro(b); if (!arqs.length && !series.length) return '';
  const motivo = semPasta(), lig = !!Pasta.res, varios = arqs.length + soma(series, s => s.arqs.length) > 1;
  const botao = (d, nome) => (extensaoDe(nome) === 'pdf'
    ? `<button type="button" class="btn sm" data-abrir="${d}" data-tit="${esc(varios ? semExt(nome) : b.t)}" aria-label="Abrir ${esc(nome)}">${icone('externo', 13)}Abrir</button>`
    : `<span class="ga-x" title="${NOTA_SO_PDF}">${esc(extensaoDe(nome).toUpperCase())} ainda não abre aqui</span>`);
  const linha = a => {
    const d = a.onde[0], achou = d != null, onde = achou ? ondeEsta(d) : '';
    const info = !lig ? '' : achou ? `${onde ? 'em ' + esc(onde) : 'solto na pasta'}${a.onde.length > 1 ? ` · e mais ${plural(a.onde.length - 1, 'cópia', 'cópias')}` : ''}` : 'não achei na pasta';
    return `<li class="ga${lig ? (achou ? ' ok' : ' falta') : ''}"><span class="ga-n">${icone(lig && !achou ? 'info' : 'arquivo', 14)}<span><b>${esc(a.nome)}</b>${info ? `<small${a.onde.length > 1 ? ` title="${esc(a.onde.map(x => ondeEsta(x) || 'solto na pasta').join('\n'))}"` : ''}>${info}</small>` : ''}</span></span>${achou ? botao(d, a.nome) : ''}</li>`;
  };
  const lista = arqs.length ? `<ul class="ga-l">${arqs.map(linha).join('')}</ul>` : '';
  const edicao = d => { const nome = Pasta.arqs[d][1]; return `<li class="ga ok"><span class="ga-n">${icone('arquivo', 14)}<span><b>${esc(nome)}</b></span></span>${botao(d, nome)}</li>`; };
  const serie = s => {
    if (!lig) return '';
    if (!s.dirs.length) return `<p class="ga-s falta">${icone('info', 14)}<span>Subpasta <b>${esc(s.nome)}</b>: não achei na pasta.</span></p>`;
    const onde = s.dirs.map(k => Pasta.dirs[k].join(' › ')).join(' e '), conta = s.arqs.length ? plural(s.arqs.length, 'arquivo', 'arquivos') : s.outros ? `${plural(s.outros, 'arquivo', 'arquivos')} de outro tipo (imagens, por exemplo)` : 'vazia';
    return `<details class="ga-s" data-k="${esc(s.nome)}"><summary><span>Subpasta <b>${esc(s.nome)}</b>: ${conta}</span><small>em ${esc(onde)}</small></summary>${s.arqs.length ? `<ul class="ga-l">${s.arqs.slice().sort((x, y) => ordemNome(Pasta.arqs[x][1], Pasta.arqs[y][1])).map(edicao).join('')}</ul>` : ''}</details>`;
  };
  // muitos arquivos: a lista vem recolhida
  const corpo = arqs.length > 4 ? `<details class="ga-s" data-k="·arquivos"${lig ? ' open' : ''}><summary><span>${plural(arqs.length, 'arquivo', 'arquivos')}</span></summary>${lista}</details>` : lista;
  let estado, pe;
  if (Pasta.lendo) { estado = 'lendo a pasta…'; pe = ''; }
  else if (lig) {
    estado = `pasta ${esc(Pasta.nome)}`;
    pe = `<p class="nota">Conferida em ${fQuando(Pasta.quando)}.${Pasta.perm === 'granted' ? '' : ' Ao abrir, o navegador pede que você confirme o acesso à pasta.'} <button type="button" class="lnk" data-pasta="ver">Ver a pasta dos livros</button></p>`;
  } else if (motivo === 'moldura') { estado = 'pasta não conectada'; pe = '<p class="nota">Para abrir os arquivos daqui é preciso conectar a pasta dos livros, e isso só funciona com o painel numa aba própria — não dentro desta moldura.</p>'; }
  else if (motivo) { estado = ''; pe = '<p class="nota">Abrir daqui, por enquanto, só no computador: com o Chrome ou o Edge e a pasta dos livros conectada.</p>'; }
  else { estado = 'pasta não conectada'; pe = `<div class="ga-b"><button type="button" class="btn sm" data-pasta="conectar">${icone('pasta', 14)}Conectar a pasta dos livros…</button></div><p class="nota">Com a pasta conectada, o painel acha cada arquivo pelo nome e abre os PDFs daqui. Os arquivos não saem do aparelho.</p>`; }
  return `<div class="gv-st"><h4 id="gv-arqs-t">Arquivos</h4><span>${estado}</span></div>${corpo}${series.map(serie).join('')}${pe}`;
}
const fQuando = ms => { const d = new Date(ms); return `${p2(d.getDate())}/${p2(d.getMonth() + 1)}/${d.getFullYear()}, às ${p2(d.getHours())}h${p2(d.getMinutes())}`; };
function pintarArquivos() {                      // a seção "Arquivos" da ficha aberta
  const sec = $('#gv-arqs'); if (!sec) return;
  const b = porId(Gaveta.id), html = b && Pasta.pronta ? htmlArquivos(b) : '';
  if (sec._h === html) return;
  const abertos = new Set($$('details[open]', sec).map(x => x.dataset.k)), tinha = sec._h != null, foco = sec.contains(document.activeElement) ? document.activeElement.dataset : null;
  sec._h = html; sec.innerHTML = html; sec.hidden = !html;
  if (tinha) for (const x of $$('details', sec)) if (abertos.has(x.dataset.k)) x.open = true;
  if (foco) focar($(foco.abrir ? `[data-abrir="${foco.abrir}"]` : '[data-pasta], [data-abrir]', sec) || $('#gaveta .gv-p'));
}

/* ───────── o botão da barra lateral ───────── */
function pintarPasta() {
  const el = $('#st-pasta'); if (!el) return;
  const motivo = semPasta(), n = Pasta.num;
  const a = n ? `Pasta ${Pasta.nome}` : 'Pasta dos livros';
  const b = Pasta.lendo ? 'lendo a pasta…' : n ? `${fInt(n.achados)} de ${fInt(n.arquivos)} achados` : motivo ? 'não disponível aqui' : 'não conectada';
  el.className = 'st pasta' + (n && !Pasta.lendo ? ' ok' : '');
  setHtml(el, `${icone('pasta', 17)}<span><b>${esc(a)}</b><em>${esc(b)}</em></span>`);
  el.title = `${a}: ${b}`; el.setAttribute('aria-label', `${a}: ${b}`);
}
function pastaMudou() { pintarPasta(); if ($('#dp')) pintarDlgPasta(); pintarArquivos(); }
function pintarAndamento() {                     // durante a conferência só os números mudam (o botão "Cancelar" não perde o foco)
  const l = Pasta.lendo, a = $('#pd-na'), d = $('#pd-nd'); if (!l || !a || !d) return;
  a.textContent = fInt(l.arqs); d.textContent = fInt(l.dirs);
}

/* ───────── o diálogo "Pasta dos livros": conectar e ver o que foi achado e o que faltou ───────── */
function listasDaPasta() {                       // as listas do relatório, cada uma como { t, v: [[linha, detalhe]], nota }
  const r = Pasta.res, n = Pasta.num, cat = ARQUIVOS.arquivos, livro = i => { const c = CATALOGO[i]; return c[0] + (c[1] ? ' — ' + c[1] : ''); };
  const caminho = d => (ondeEsta(d, '\\') ? ondeEsta(d, '\\') + '\\' : '') + Pasta.arqs[d][1];
  const faltam = cat.map((a, i) => (r.achados[i].length ? null : [a[0], `${a[2].length > 1 ? 'livros' : 'livro'}: ${a[2].map(livro).join(' · ')} · nas listagens: ${a[1].map(p => ARQUIVOS.pastas[p]).join(' e ')}`])).filter(Boolean);
  const novos = r.novos.map(d => [Pasta.arqs[d][1], ondeEsta(d, '\\') ? 'em ' + ondeEsta(d, '\\') : 'solto na pasta']);
  const formatos = ds => { const m = new Map(); for (const d of ds) { const e = extensaoDe(Pasta.arqs[d][1]); m.set(e, (m.get(e) || 0) + 1); } return [...m].sort((x, y) => y[1] - x[1] || ordemNome(x[0], y[0])).map(x => `${x[1]} ${x[0].toUpperCase()}`).join(', '); };
  const porNome = (x, y) => ordemNome(x[0], y[0]);
  const seriesFora = SERIES.map((s, k) => (r.series[k].dirs.length ? null : [s[0], `série: ${s[1].map(livro).join(' · ')}`])).filter(Boolean).sort(porNome);
  const seriesAchadas = SERIES.map((s, k) => { const x = r.series[k]; return x.dirs.length ? [s[0], `${x.arqs.length ? plural(x.arqs.length, 'arquivo', 'arquivos') + ' (' + formatos(x.arqs) + ')' : 'nenhum arquivo de livro'}${x.outros ? ` · ${plural(x.outros, 'arquivo', 'arquivos')} de outro tipo` : ''} · em ${x.dirs.map(d => Pasta.dirs[d].join('\\')).join(' e ')}`] : null; }).filter(Boolean).sort(porNome);
  const copias = cat.map((a, i) => { const tem = r.achados[i].length, esp = a[1].length; return tem && tem !== esp ? [a[0], `as listagens mostram ${plural(esp, 'cópia', 'cópias')}; na pasta há ${tem}: ${r.achados[i].map(d => ondeEsta(d, '\\') || '(solto)').join(' · ')}`] : null; }).filter(Boolean);
  const fora = ARQUIVOS.fora.map((a, j) => [a[0], `${a[2]} · ${r.achados[n.arquivos + j].length ? 'achado' : 'não achado'}`]);
  const tipos = new Map(); for (const d of r.outros) { const e = extensaoDe(Pasta.arqs[d][1]) || '(sem extensão)'; tipos.set(e, (tipos.get(e) || 0) + 1); }
  const outros = [...tipos].sort((x, y) => y[1] - x[1] || ordemNome(x[0], y[0])).map(x => [x[0] === '(sem extensão)' ? x[0] : '.' + x[0], plural(x[1], 'arquivo', 'arquivos')]);
  return [
    { k: 'faltam', t: 'Não achei na pasta', v: faltam, nota: 'Arquivos que o catálogo conhece e que não apareceram em nenhuma subpasta. Pode ser um arquivo que mudou de nome, saiu da pasta ou está fora dela.' },
    { k: 'novos', t: 'Na pasta, mas não no catálogo', v: novos, nota: 'Arquivos de livro que estão na pasta e que o catálogo ainda não conhece. Entram no catálogo pela rotina de sempre: a listagem da pasta e o pedido “atualize a biblioteca virtual”.' },
    { k: 'series-fora', t: 'Séries em subpasta que não achei', v: seriesFora, nota: 'Séries de quadrinhos que o catálogo dá como guardadas numa subpasta só delas.' },
    { k: 'series', t: 'Séries em subpasta achadas', v: seriesAchadas, nota: 'O que há dentro de cada subpasta de série — as listagens não mostravam.' },
    { k: 'copias', t: 'Cópias a mais ou a menos', v: copias, nota: 'O arquivo foi achado, mas em número diferente do que as listagens mostram.' },
    { k: 'fora', t: 'Só no inventário', v: fora, nota: 'Apostilas, revistas e artigos: ficam fora do catálogo por decisão sua.' },
    { k: 'outros', t: 'Outros arquivos, por tipo', v: outros, total: r.outros.length, nota: 'O que não é arquivo de livro: as listagens, o gerador de nomes, imagens…' },
    { k: 'erros', t: 'Pastas que não deu para ler', v: Pasta.erros.map(e => [e, '']), nota: 'O navegador não deixou ler estas pastas; o que há nelas não entrou na conta.' },
  ];
}
function relatorioPasta() {
  const n = Pasta.num, L = [];
  L.push('Biblioteca do Lucas — a pasta dos livros', '', `Pasta: ${Pasta.nome}`, `Conferida em ${fQuando(Pasta.quando)}`,
    `Na pasta: ${plural(n.naPasta, 'arquivo', 'arquivos')} em ${plural(n.pastas, 'pasta', 'pastas')} (${fInt(n.deLivro)} de livro)`, '', 'RESUMO',
    `  Arquivos do catálogo: ${fInt(n.arquivos)} · achados: ${fInt(n.achados)} · não achados: ${fInt(n.faltam)}`,
    `  Livros digitais do catálogo: ${fInt(n.livros)} · com ao menos um arquivo na pasta: ${fInt(n.comAlgo)} · com PDF para abrir: ${fInt(n.comPdf)}`,
    `  Séries de quadrinhos em subpasta: ${fInt(n.series)} · achadas: ${fInt(n.seriesAchadas)} · arquivos dentro delas: ${fInt(n.edicoes)}`,
    `  Na pasta, mas não no catálogo: ${fInt(n.novos)}`,
    `  Só no inventário (apostilas, revistas, artigos): ${fInt(n.fora)} · achados: ${fInt(n.foraAchados)}`,
    `  Outros arquivos (não são de livro): ${fInt(n.outros)}`);
  for (const l of listasDaPasta()) {
    L.push('', `${l.t.toUpperCase()} (${fInt(l.total != null ? l.total : l.v.length)})`);
    if (!l.v.length) L.push('  (nenhum)');
    for (const [a, b] of l.v) { L.push('  ' + a); if (b) L.push('      ' + b); }
  }
  return '\ufeff' + L.join('\r\n') + '\r\n';
}
function corpoDlgPasta() {
  const motivo = semPasta(), n = Pasta.num, l = Pasta.lendo;
  if (l) return `<div class="pd-lendo" role="status" aria-live="polite"><i aria-hidden="true"></i><span>Lendo a pasta <b>${esc(l.nome)}</b>… <b class="num" id="pd-na">${fInt(l.arqs)}</b> arquivos em <b class="num" id="pd-nd">${fInt(l.dirs)}</b> pastas</span></div><div class="dd-b"><button type="button" class="btn" data-pd="parar" data-foco>Cancelar</button></div>`;
  if (motivo && !n) return `<div class="dd-st aviso">${icone('info', 16)}<div><b>Aqui não dá para conectar a pasta</b><span>${motivo === 'moldura'
    ? 'O painel está dentro de outra página (a prévia). O navegador só deixa escolher uma pasta com o painel aberto numa aba própria.'
    : 'Este navegador não deixa um site ler uma pasta do aparelho. Funciona no Chrome e no Edge do computador.'}</span></div></div>
    <p class="pd-p">Com a pasta conectada, o painel acha cada livro pelo nome do arquivo, mostra o que achou e o que faltou, e abre os PDFs direto da ficha. No celular e no tablet, o caminho previsto é escolher o arquivo na hora de ler — ainda vai chegar.</p>`;
  if (!n) return `<p class="pd-p">Escolha a pasta principal dos seus livros. O painel percorre as subpastas, acha cada livro do catálogo pelo <b>nome do arquivo</b> e mostra o que achou e o que faltou. Depois disso, a ficha de cada livro ganha o botão “Abrir” — por enquanto, para PDF.</p>
    <ul class="pd-reg"><li>O painel <b>só lê</b>: não muda, não move e não apaga nada.</li><li><b>Nada sai do aparelho</b>: nem os arquivos, nem os nomes deles.</li><li>O navegador vai perguntar se o site pode ver os arquivos da pasta. Nas próximas visitas, ele pode pedir que você confirme de novo.</li></ul>
    <div class="dd-b"><button type="button" class="btn pri" data-pd="conectar" data-foco>${icone('pasta', 15)}Conectar a pasta…</button></div>
    ${/Android/i.test(navigator.userAgent) ? '<p class="nota">No Android, o navegador só alcança pastas guardadas no próprio aparelho (não as do Drive) e esquece a permissão a cada visita.</p>' : ''}`;
  const pouco = n.achados < n.arquivos * 0.2, listas = listasDaPasta().filter(x => x.v.length);
  const lista = x => `<details class="pd-l" data-k="${x.k}"><summary><span>${esc(x.t)}</span><b class="num">${fInt(x.total != null ? x.total : x.v.length)}</b></summary><p class="nota">${esc(x.nota)}</p><ul>${x.v.slice(0, LISTA_MAX).map(([a, b]) => `<li><b>${esc(a)}</b>${b ? `<small>${esc(b)}</small>` : ''}</li>`).join('')}</ul>${x.v.length > LISTA_MAX ? `<p class="nota">… e mais ${fInt(x.v.length - LISTA_MAX)}. A lista inteira está no relatório.</p>` : ''}</details>`;
  return `<div class="dd-st ${pouco ? 'aviso' : 'ok'}">${icone(pouco ? 'info' : 'check', 16)}<div><b tabindex="-1" data-foco>Pasta “${esc(Pasta.nome)}” conectada</b><span>Conferida em ${fQuando(Pasta.quando)}: ${plural(n.naPasta, 'arquivo', 'arquivos')} em ${plural(n.pastas, 'pasta', 'pastas')}. O painel só lê os nomes; nada sai do aparelho.${pouco ? ' <b>Quase nada do catálogo está aqui:</b> se esta não for a pasta principal dos livros, troque de pasta.' : ''}</span></div></div>
    ${Pasta.lembrada ? '' : '<p class="nota">Este navegador não deixou guardar a ligação com a pasta (janela anônima ou armazenamento bloqueado): ela vale até a página ser fechada.</p>'}
    ${Pasta.perm === 'granted' ? '' : `<p class="nota" id="pd-perm">Nesta visita o navegador ainda não confirmou o acesso à pasta. Ele pergunta quando você abrir um arquivo ou procurar de novo; o que está abaixo é o que foi achado em ${fQuando(Pasta.quando)}.</p>`}
    <dl class="dd-n pd-n"><div><dt>Arquivos do catálogo achados</dt><dd data-n="achados">${fInt(n.achados)}<small> de ${fInt(n.arquivos)}</small></dd></div><div><dt>Não achados</dt><dd data-n="faltam">${fInt(n.faltam)}</dd></div><div><dt>Na pasta, fora do catálogo</dt><dd data-n="novos">${fInt(n.novos)}</dd></div><div><dt>Livros com PDF para abrir</dt><dd data-n="pdf">${fInt(n.comPdf)}</dd></div></dl>
    <p class="pd-p" id="pd-frase">Dos ${fInt(n.livros)} livros digitais do catálogo, <b>${fInt(n.comAlgo)}</b> têm ao menos um arquivo nesta pasta. Das ${fInt(n.series)} séries de quadrinhos guardadas em subpasta, achei <b>${fInt(n.seriesAchadas)}</b>${n.edicoes ? `, com ${plural(n.edicoes, 'arquivo', 'arquivos')} dentro` : ''}.</p>
    <div class="dd-b"><button type="button" class="btn" data-pd="reconferir">${icone('girar', 15)}Procurar de novo</button><button type="button" class="btn" data-pd="relatorio">${icone('baixar', 15)}Baixar o relatório (.txt)</button><button type="button" class="btn" data-pd="conectar">${icone('pasta', 15)}Trocar de pasta…</button><button type="button" class="btn" data-pd="esquecer">${icone('fechar', 15)}Desconectar</button></div>
    ${listas.length ? `<section class="pd-ls"><h3>O que achei e o que faltou</h3>${listas.map(lista).join('')}</section>` : ''}`;
}
function pintarDlgPasta() {
  const el = $('#dp'); if (!el) return;
  const html = corpoDlgPasta(); if (el._h === html) return;
  const abertos = new Set($$('details[open]', el).map(x => x.dataset.k));
  el._h = html; el.innerHTML = html;
  for (const x of $$('details', el)) if (abertos.has(x.dataset.k)) x.open = true;
}
function dlgPasta() {
  Dlg.abrir({ titulo: 'Pasta dos livros', largo: true, corpo: '<div class="dados pasta-d" id="dp"></div>', botoes: [{ n: 'Fechar', cls: 'pri' }],
    aoAbrir(c) {
      pintarDlgPasta();
      c.addEventListener('click', e => {
        const b = e.target.closest('[data-pd]'); if (!b) return; const x = b.dataset.pd;
        if (x === 'conectar') conectarPasta();
        else if (x === 'parar') { if (Pasta.lendo) Pasta.lendo.parar = true; }
        else if (x === 'reconferir') reconferirPasta();
        else if (x === 'relatorio') baixarArquivo(`biblioteca-lucas-pasta-${iso(hojeDia())}.txt`, relatorioPasta(), 'text/plain;charset=utf-8');
        else if (x === 'esquecer') esquecerPasta().then(() => { toast('Pasta desconectada. Nada foi mexido nos arquivos.'); focar($('#dp [data-foco]')); });
      });
    } });
}
