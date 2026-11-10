/* ───────────────────────── utilidades ───────────────────────── */
const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const soma = (arr, f) => { let s = 0; for (const x of arr) s += f ? f(x) : x; return s; };
const norm = s => String(s ?? '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();

/* datas: tudo é "número do dia" (dias desde 1970-01-01, em UTC) para evitar surpresas de fuso */
const DIA_MS = 864e5;
const dia = (y, m, d) => Math.round(Date.UTC(y, m - 1, d) / DIA_MS);
const hojeDia = () => { const n = new Date(); return dia(n.getFullYear(), n.getMonth() + 1, n.getDate()); };
const deDia = n => new Date(n * DIA_MS);
const partes = n => { const d = deDia(n); return { y: d.getUTCFullYear(), m: d.getUTCMonth() + 1, d: d.getUTCDate(), w: d.getUTCDay() }; };
const iso = n => (n == null ? '' : deDia(n).toISOString().slice(0, 10));
const deIso = s => { const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(s || ''); return m ? dia(+m[1], +m[2], +m[3]) : null; };
const MESES = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez'];
const MESES_L = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'];
const p2 = n => String(n).padStart(2, '0');
const fData = n => { if (n == null) return '—'; const p = partes(n); return `${p2(p.d)}/${p2(p.m)}/${p.y}`; };
const fDiaMes = n => { const p = partes(n); return `${p2(p.d)} ${MESES[p.m - 1]}`; };
const fDiaMesAno = n => { const p = partes(n); return `${p2(p.d)} ${MESES[p.m - 1]} ${p.y}`; };
const fMesAno = n => { const p = partes(n); return `${MESES[p.m - 1]}/${String(p.y).slice(2)}`; };
const fMesLongo = n => { const p = partes(n); return `${MESES_L[p.m - 1]} de ${p.y}`; };
const somaMeses = (n, k) => {            // desloca k meses mantendo o dia (limitado ao fim do mês)
  const p = partes(n); const y = p.y + Math.floor((p.m - 1 + k) / 12); const m = ((p.m - 1 + k) % 12 + 12) % 12 + 1;
  const ult = partes(dia(y, m + 1, 0)).d; return dia(y, m, Math.min(p.d, ult));
};

/* números */
const nfInt = new Intl.NumberFormat('pt-BR', { maximumFractionDigits: 0 });
const nfDec1 = new Intl.NumberFormat('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 });
const nfBRL = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' });
const nfBRL0 = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL', maximumFractionDigits: 0 });
let OCULTAR_VALORES = false;
const fInt = v => nfInt.format(v);
const fDec = v => nfDec1.format(v);
const fBRL = v => (v == null || isNaN(v) ? '—' : OCULTAR_VALORES ? 'R$ •••' : nfBRL.format(v));
const fBRL0 = v => (v == null || isNaN(v) ? '—' : OCULTAR_VALORES ? 'R$ •••' : nfBRL0.format(v));
const fBRLc = v => {                     // compacto para eixos de gráfico
  if (OCULTAR_VALORES) return '•••';
  if (Math.abs(v) >= 10000) return 'R$ ' + nfDec1.format(v / 1000).replace(',0', '') + ' mil';
  if (Math.abs(v) >= 1000) return 'R$ ' + nfDec1.format(v / 1000) + ' mil';
  return 'R$ ' + nfInt.format(v);
};
const fPct = (v, sinal) => (v == null || !isFinite(v) ? '—' : (sinal && v > 0 ? '+' : '') + nfDec1.format(v * 100).replace(/,0$/, '') + '%');
const plural = (n, um, varios) => `${fInt(n)} ${n === 1 ? um : varios}`;

/* aleatoriedade determinística (para os dados de exemplo) */
function hashStr(s) { let h = 2166136261; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; }
function mulberry32(a) {
  return function () { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
}

/* escalas "redondas" para eixos */
function ticksBonitos(min, max, n = 4, inteiro = false) {
  if (!isFinite(min) || !isFinite(max)) { min = 0; max = 1; }
  if (max === min) max = min + (min === 0 ? 1 : Math.abs(min) * 0.2);
  const bruto = (max - min) / n, pot = Math.pow(10, Math.floor(Math.log10(bruto))), r = bruto / pot;
  let passo = (r <= 1 ? 1 : r <= 2 ? 2 : r <= 2.5 ? 2.5 : r <= 5 ? 5 : 10) * pot;
  if (inteiro) passo = Math.max(1, Math.round(passo));
  const lo = Math.floor(min / passo) * passo, hi = Math.ceil(max / passo) * passo, t = [];
  for (let v = lo; v <= hi + passo * 1e-6; v += passo) t.push(Math.round(v * 1e6) / 1e6);
  return { min: lo, max: hi, passo, ticks: t };
}

/* baldes de tempo: escolhe a granularidade mais fina que caiba em maxN */
function baldes(de, ate, maxN) {
  const dias = ate - de + 1;
  const est = { dia: dias, semana: dias / 7 + 1, mes: dias / 30.4 + 1, trimestre: dias / 91 + 1, ano: dias / 365 + 1 };
  let g = 'ano';
  for (const k of ['dia', 'semana', 'mes', 'trimestre', 'ano']) if (est[k] <= maxN) { g = k; break; }
  const lista = [];
  let ini;
  const p = partes(de);
  if (g === 'dia') ini = de;
  else if (g === 'semana') ini = de - ((p.w + 6) % 7);
  else if (g === 'mes') ini = dia(p.y, p.m, 1);
  else if (g === 'trimestre') ini = dia(p.y, Math.floor((p.m - 1) / 3) * 3 + 1, 1);
  else ini = dia(p.y, 1, 1);
  let guarda = 0;
  while (ini <= ate && guarda++ < 5000) {
    const q = partes(ini);
    let fim, rot, tit;
    if (g === 'dia') { fim = ini; rot = fDiaMes(ini); tit = fDiaMesAno(ini); }
    else if (g === 'semana') { fim = ini + 6; rot = fDiaMes(Math.max(ini, de)); tit = `Semana de ${fData(Math.max(ini, de))}`; }
    else if (g === 'mes') { fim = dia(q.y, q.m + 1, 0); rot = fMesAno(ini); tit = fMesLongo(ini); }
    else if (g === 'trimestre') { fim = dia(q.y, q.m + 3, 0); const t = Math.floor((q.m - 1) / 3) + 1; rot = `T${t}/${String(q.y).slice(2)}`; tit = `${t}º trimestre de ${q.y}`; }
    else { fim = dia(q.y, 12, 31); rot = String(q.y); tit = String(q.y); }
    lista.push({ i: Math.max(ini, de), f: Math.min(fim, ate), rot, tit, parcial: fim > ate });
    ini = fim + 1;
  }
  return { g, lista };
}
const NOME_GRAN = { dia: 'dia', semana: 'semana', mes: 'mês', trimestre: 'trimestre', ano: 'ano' };

/* debounce simples */
function debounce(fn, ms) { let t; return (...a) => { clearTimeout(t); t = setTimeout(() => fn(...a), ms); }; }
