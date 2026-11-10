/* ───────────────────────── ícones, estado, filtros e recortes ───────────────────────── */
const IC = {
  painel: '<rect x="3" y="3" width="7" height="9" rx="1.5"/><rect x="14" y="3" width="7" height="5" rx="1.5"/><rect x="14" y="12" width="7" height="9" rx="1.5"/><rect x="3" y="16" width="7" height="5" rx="1.5"/>',
  estante: '<path d="m16 6 4 14"/><path d="M12 6v14"/><path d="M8 8v12"/><path d="M4 4v16"/>',
  bussola: '<circle cx="12" cy="12" r="10"/><path d="m16.24 7.76-2.12 6.36-6.36 2.12 2.12-6.36z"/>',
  sacola: '<path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><path d="M3 6h18"/><path d="M16 10a4 4 0 0 1-8 0"/>',
  etiqueta: '<path d="M12.6 2.6A2 2 0 0 0 11.2 2H4a2 2 0 0 0-2 2v7.2a2 2 0 0 0 .6 1.4l8.7 8.7a2.4 2.4 0 0 0 3.4 0l6.6-6.6a2.4 2.4 0 0 0 0-3.4z"/><circle cx="7.5" cy="7.5" r=".6" fill="currentColor"/>',
  busca: '<circle cx="11" cy="11" r="7.5"/><path d="m21 21-4.3-4.3"/>',
  sol: '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M6.3 17.7l-1.4 1.4M19.1 4.9l-1.4 1.4"/>',
  lua: '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9z"/>',
  olho: '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="3"/>',
  olhoOff: '<path d="M9.9 9.9a3 3 0 1 0 4.2 4.2"/><path d="M10.7 5.1A10.4 10.4 0 0 1 12 5c6.5 0 10 7 10 7a13.2 13.2 0 0 1-1.7 2.7"/><path d="M6.6 6.6A13.5 13.5 0 0 0 2 12s3.5 7 10 7a9.7 9.7 0 0 0 5.4-1.6"/><path d="m2 2 20 20"/>',
  mais: '<path d="M5 12h14M12 5v14"/>',
  fechar: '<path d="M18 6 6 18M6 6l12 12"/>',
  filtro: '<path d="M21 4h-7M10 4H3M21 12h-9M8 12H3M21 20h-5M12 20H3M14 2v4M8 10v4M16 18v4"/>',
  baixar: '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/><path d="M12 15V3"/>',
  enviar: '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m17 8-5-5-5 5"/><path d="M12 3v12"/>',
  estrela: '<path d="M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5L2.5 9.4l6.6-.9z"/>',
  livro: '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>',
  check: '<path d="M20 6 9 17l-5-5"/>',
  relogio: '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
  externo: '<path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>',
  lapis: '<path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5z"/>',
  lixo: '<path d="M3 6h18"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/><path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>',
  sino: '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>',
  baixo: '<path d="m6 9 6 6 6-6"/>',
  esq: '<path d="m15 18-6-6 6-6"/>',
  dir: '<path d="m9 18 6-6-6-6"/>',
  info: '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/>',
  dados: '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14a9 3 0 0 0 18 0V5"/><path d="M3 12a9 3 0 0 0 18 0"/>',
  carteira: '<path d="M21 12V7H5a2 2 0 0 1 0-4h14v4"/><path d="M3 5v14a2 2 0 0 0 2 2h16v-5"/><path d="M18 12a2 2 0 0 0 0 4h4v-4z"/>',
  raio: '<path d="M13 2 3 14h9l-1 8 10-12h-9z"/>',
  queda: '<path d="m22 17-8.5-8.5-5 5L2 7"/><path d="M16 17h6v-6"/>',
  alta: '<path d="m22 7-8.5 8.5-5-5L2 17"/><path d="M16 7h6v6"/>',
  marcador: '<path d="m19 21-7-4-7 4V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>',
  lista: '<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>',
  sortear: '<path d="M2 18h1.4c1.3 0 2.5-.6 3.3-1.7l6.1-8.6c.7-1.1 2-1.7 3.3-1.7H22"/><path d="m18 2 4 4-4 4"/><path d="M2 6h1.9c1.5 0 2.9.9 3.6 2.2"/><path d="M22 18h-5.9c-1.3 0-2.6-.7-3.3-1.8l-.5-.8"/><path d="m18 14 4 4-4 4"/>',
  fone: '<path d="M3 14h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-7a9 9 0 0 1 18 0v7a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3"/>',
  tablet: '<rect x="5" y="2" width="14" height="20" rx="2"/><path d="M12 18h.01"/>',
  calendario: '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
  cima: '<path d="m5 12 7-7 7 7"/><path d="M12 19V5"/>',
  abaixo: '<path d="M12 5v14"/><path d="m19 12-7 7-7-7"/>',
  reta: '<path d="M5 12h14"/>',
  pilha: '<path d="m12 2 10 5-10 5L2 7z"/><path d="m2 12 10 5 10-5"/><path d="m2 17 10 5 10-5"/>',
  alvo: '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
  desfazer: '<path d="M3 7v6h6"/><path d="M21 17a9 9 0 0 0-9-9 9 9 0 0 0-6 2.3L3 13"/>',
};
const icone = (n, t = 18) => `<svg class="ic" width="${t}" height="${t}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${IC[n] || ''}</svg>`;
const ICONE_FMT = { fisico: 'livro', ebook: 'tablet', audio: 'fone' };

const VISOES = {
  geral: { n: 'Visão geral', c: 'Geral', d: 'Panorama da biblioteca, das leituras e das recomendações', ic: 'painel' },
  biblioteca: { n: 'Biblioteca', c: 'Biblioteca', d: 'Estante física e biblioteca virtual, e as suas leituras', ic: 'estante' },
  recs: { n: 'Recomendações', c: 'Recomend.', d: 'O catálogo de leituras sugeridas, por eixo, tema e fôlego', ic: 'bussola' },
  // tudo o que é dinheiro mora daqui para baixo: nada de valores na Visão geral nem na Biblioteca
  financas: { n: 'Finanças', c: 'Finanças', d: 'Quanto foi investido, onde, e o custo da lista de compra', ic: 'carteira' },
  desejos: { n: 'Próximas aquisições', c: 'Aquisições', d: 'Lista de compra com prioridade, preço-alvo e melhor oferta', ic: 'sacola' },
  precos: { n: 'Preços', c: 'Preços', d: 'Histórico de cotações por loja, alertas e variações', ic: 'etiqueta' },
};
const ORDEM_VISOES = Object.keys(VISOES);
const PERIODOS = [['30d', '30 dias'], ['90d', '90 dias'], ['12m', '12 meses'], ['ano', 'Este ano'], ['tudo', 'Tudo']];
const ROTULO_ACERVO = { fisico: 'Biblioteca física', virtual: 'Biblioteca virtual', ambos: 'Nas duas: físico e digital' };
const COLECOES = {
  acervo: { n: 'Acervo', cor: 'var(--c2)' },
  desejo: { n: 'Próxima aquisição', cor: 'var(--c1)' },
  rec: { n: 'Recomendação', cor: 'var(--c9)' },
};

const S = {
  visao: 'geral',
  periodo: 'tudo', de: null, ate: null,
  acervo: 'tudo',   // tudo | fisico (estante) | virtual (digital ou áudio) | ambos (tenho em físico e em digital)
  tipo: '', eixos: new Set(), dif: new Set(), ext: new Set(), tags: new Set(), top: false,
  tema: '', ocultar: false, avisoVisto: false, sel: '',
  tab: {},
  ui: { compor: 'fmt', temas: 1, prio: 'valor', sorteio: 0 },
};
const nFiltros = () => (S.acervo !== 'tudo' && S.visao !== 'recs' ? 1 : 0) + (S.tipo ? 1 : 0) + S.eixos.size + S.dif.size + S.ext.size + S.tags.size + (S.top ? 1 : 0) + (S.periodo !== 'tudo' ? 1 : 0);
function limparFiltros(tambemPeriodo) {
  S.acervo = 'tudo'; S.tipo = ''; S.eixos.clear(); S.dif.clear(); S.ext.clear(); S.tags.clear(); S.top = false;
  if (tambemPeriodo) { S.periodo = 'tudo'; S.de = S.ate = null; }
}
const alternar = (conj, v) => { if (conj.has(v)) conj.delete(v); else conj.add(v); };

/* filtros de segmento (o período é tratado à parte, porque filtra eventos e não livros) */
function passaSeg(b, o = {}) {
  if (!o.semAcervo && S.acervo !== 'tudo') {
    // no acervo vale o que eu tenho (um livro pode estar nas duas bibliotecas); nas listas, o formato desejado
    const ac = b.col === 'acervo', f = b.fmt || (b.px ? 'fisico' : '');
    const fis = f === 'fisico', vir = ac ? temDigital(b) || f === 'audio' : f === 'ebook' || f === 'audio';
    if (!(S.acervo === 'fisico' ? fis : S.acervo === 'virtual' ? vir : fis && vir)) return false;
  }
  if (S.tipo && tipoFiltro(b._tipo) !== S.tipo) return false;
  if (!o.semEixo && S.eixos.size && !S.eixos.has(b.eixo)) return false;
  if (!o.semDE) { if (S.dif.size && !S.dif.has(b._d)) return false; if (S.ext.size && !S.ext.has(b._e)) return false; }
  if (!o.semTags && S.tags.size) for (const t of S.tags) if (!b.tags.includes(t)) return false;
  if (S.top && !b._top) return false;
  return true;
}

/* A compra registrada num livro que tenho em papel (data, valor, origem) é a do exemplar físico. No recorte "Virtual" ela não conta:
   os arquivos da biblioteca virtual não têm data nem preço, e somá-la faria a biblioteca virtual parecer comprada. */
const compraConta = b => S.acervo !== 'virtual' || b.col !== 'acervo' || b.fmt !== 'fisico';
const adqDe = b => (compraConta(b) ? b.adq : null);
const pagoDe = b => (compraConta(b) ? b.pago : null);
const lojaDe = b => (compraConta(b) ? b.loja : '');
const dataDe = b => (b.col === 'acervo' ? adqDe(b) : b.add);

const dentro = (d, r) => d != null && d >= r.de && d <= r.ate;
function primeiroDia() {
  let m = Infinity;
  for (const b of DB.livros) for (const d of [b.adq, b.add, b.lidoEm]) if (d != null && d < m) m = d;
  return isFinite(m) ? m : somaMeses(DB.hoje, -12) + 1;
}
function intervalo() {
  const T = DB.hoje, ano = partes(T).y;
  let p = S.periodo;
  if (p === 'custom' && (S.de == null || S.ate == null)) p = 'tudo';
  let de, ate = T, cur, ant, cmp, cmpC, rot;
  if (p === '30d') { de = T - 29; rot = 'últimos 30 dias'; }
  else if (p === '90d') { de = T - 89; rot = 'últimos 90 dias'; }
  else if (p === '12m') { de = somaMeses(T, -12) + 1; rot = 'últimos 12 meses'; }
  else if (p === 'ano') { de = dia(ano, 1, 1); rot = 'em ' + ano; }
  else if (p === 'custom') { de = Math.min(S.de, S.ate); ate = Math.max(S.de, S.ate); rot = `de ${fData(de)} a ${fData(ate)}`; }
  else { de = Math.min(primeiroDia(), T); rot = 'todo o histórico'; }
  const n = ate - de + 1, tudo = p === 'tudo';
  if (tudo) { cur = { de: somaMeses(T, -12) + 1, ate: T }; ant = { de: somaMeses(T, -24) + 1, ate: somaMeses(T, -12) }; cmp = 'últ. 12 meses vs. 12 anteriores'; cmpC = 'em 12 meses'; }
  else if (p === 'ano') { cur = { de, ate }; ant = { de: dia(ano - 1, 1, 1), ate: somaMeses(T, -12) }; cmp = 'vs. mesmo período de ' + (ano - 1); cmpC = 'no ano'; }
  else { cur = { de, ate }; ant = { de: de - n, ate: de - 1 }; cmp = p === '12m' ? 'vs. 12 meses anteriores' : `vs. ${fInt(n)} dias anteriores`; cmpC = 'no período'; }
  return { p, de, ate, n, tudo, cur, ant, cmp, cmpC, rot };
}

/* itens com acompanhamento de preço: tudo o que está na lista de compra + recomendações monitoradas */
const rastreado = b => !!b.px && b.col !== 'acervo' && (b.col === 'desejo' || b.track);
function precoBase(b, d) {                   // melhor preço em d; antes da 1ª cotação, usa a 1ª cotação
  const m = melhorEm(b, d); if (m) return m.p;
  let p = null, dd = Infinity;
  for (const f of fontesDe(b)) { const x = b.px[f][0]; if (x && x[0] < dd) { dd = x[0]; p = x[1]; } }
  return p;
}
const temCotacaoPropria = b => !!b.px && Object.values(b.px).some(pts => pts.some(p => p[2]));

function recorte(I, o) {
  const seg = DB.livros.filter(b => passaSeg(b, Object.assign({ semAcervo: S.visao === 'recs' }, o)));
  const ac = [], des = [], rec = [];
  for (const b of seg) (b.col === 'acervo' ? ac : b.col === 'desejo' ? des : rec).push(b);
  return { seg, ac, des, rec, acP: I.tudo ? ac : ac.filter(b => dentro(adqDe(b), I)), recP: I.tudo ? rec : rec.filter(b => dentro(b.add, I)) };
}
function contexto() {
  const I = intervalo(), c = recorte(I, {});
  c.I = I; c.T = DB.hoje;
  c.lidos = c.seg.filter(b => b.leit === 'lido');
  c.lidosP = I.tudo ? c.lidos : c.lidos.filter(b => dentro(b.lidoEm, I));
  c.rast = c.seg.filter(rastreado);
  let E, DE;
  Object.defineProperty(c, 'E', { get: () => E || (E = recorte(I, { semEixo: true })) });      // ignora o filtro de eixo (gráficos-seletores)
  Object.defineProperty(c, 'DE', { get: () => DE || (DE = recorte(I, { semDE: true })) });     // ignora dificuldade/extensão (matriz)
  let ini = Infinity;
  for (const b of c.rast) for (const f in b.px) if (b.px[f].length && b.px[f][0][0] < ini) ini = b.px[f][0][0];
  c.pxIni = isFinite(ini) ? ini : I.ate;
  c.pxDe = Math.min(I.ate, Math.max(I.de, c.pxIni));       // início efetivo do recorte de preços
  c.refDe = Math.min(I.ate, Math.max(I.cur.de, c.pxIni));  // base de comparação das tendências de preço
  const cache = new Map();
  c.px = b => {
    let r = cache.get(b.id);
    if (!r) { r = b.px ? { hoje: melhorEm(b, I.ate), sit: situacaoDe(b, I.ate), res: resumoPrecos(b, c.pxDe, I.ate), ref: precoBase(b, c.refDe) } : { hoje: null, sit: 'sem', res: null, ref: null }; cache.set(b.id, r); }
    return r;
  };
  c.cestaEm = d => soma(c.des, b => (b.px ? precoBase(b, d) || 0 : 0));
  return c;
}

/* agregações por período */
function idxBalde(lista, d) { let lo = 0, hi = lista.length - 1; while (lo <= hi) { const m = (lo + hi) >> 1; if (d < lista[m].i) hi = m - 1; else if (d > lista[m].f) lo = m + 1; else return m; } return -1; }
function porBalde(B, itens, dataDe, valorDe) {
  const v = new Array(B.lista.length).fill(0);
  for (const it of itens) { const d = dataDe(it); if (d == null) continue; const i = idxBalde(B.lista, d); if (i >= 0) v[i] += valorDe ? valorDe(it) : 1; }
  return v;
}
function acumulado(B, itens, dataDe, valorDe) {      // total acumulado ao fim de cada balde (inclui o que veio antes do intervalo)
  const v = new Array(B.lista.length).fill(0), ini = B.lista.length ? B.lista[0].i : 0;
  let base = 0;
  for (const it of itens) { const d = dataDe(it); if (d == null) continue; const x = valorDe ? valorDe(it) : 1; if (d < ini) base += x; else { const i = idxBalde(B.lista, d); if (i >= 0) v[i] += x; } }
  let s = base; return v.map(x => (s += x));
}
const contarPor = (arr, f) => { const m = new Map(); for (const x of arr) { const k = f(x); m.set(k, (m.get(k) || 0) + 1); } return m; };

/* tendências */
function tend(atual, ant, sentido) {         // sentido: 'alta' (subir é bom), 'baixa' (cair é bom) ou 'neutro'
  if (atual == null || ant == null || (!atual && !ant)) return null;     // nada antes e nada agora: não há tendência a mostrar
  const dif = atual - ant, dir = Math.abs(dif) < 1e-9 ? 'reta' : dif > 0 ? 'cima' : 'abaixo';
  const cls = dir === 'reta' || sentido === 'neutro' ? 'neutro' : (dir === 'cima') === (sentido === 'alta') ? 'bom' : 'ruim';
  return { dir, cls, txt: !ant ? (dif > 0 ? 'novo' : '0%') : fPct(Math.abs(dif / ant)) };
}
function tendAbs(dif, sentido, fmt) {
  const dir = Math.abs(dif) < 1e-9 ? 'reta' : dif > 0 ? 'cima' : 'abaixo';
  const cls = dir === 'reta' || sentido === 'neutro' ? 'neutro' : (dir === 'cima') === (sentido === 'alta') ? 'bom' : 'ruim';
  return { dir, cls, txt: (fmt || fInt)(Math.abs(dif)) };
}

/* busca nas lojas (links de pesquisa; o painel não consulta preços sozinho) */
function linksLojas(b) {
  const titulo = b.t.replace(/\s*\([^)]*\)\s*/g, ' ').replace(/\s+/g, ' ').trim();
  const q = encodeURIComponent((titulo + ' ' + (b.a || '')).trim());
  const slug = norm(titulo + ' ' + (b.a || '')).replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
  return [
    ['Amazon', `https://www.amazon.com.br/s?k=${q}&i=stripbooks`],
    ['Kindle', `https://www.amazon.com.br/s?k=${q}&i=digital-text`],
    ['Estante Virtual', `https://www.estantevirtual.com.br/busca?q=${q}`],
    ['Mercado Livre', `https://lista.mercadolivre.com.br/${slug}`],
    ['Travessa', `https://www.travessa.com.br/Busca.aspx?d=1&bt=${encodeURIComponent(titulo)}`],
    ['Google Shopping', `https://www.google.com/search?tbm=shop&q=${q}`],
  ];
}
