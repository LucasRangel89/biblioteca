/* ───────────────────────── gráficos (SVG/HTML, sem bibliotecas) ───────────────────────── */
const SVGNS = 'http://www.w3.org/2000/svg';
const semMovimento = () => window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
const suave = t => 1 - Math.pow(1 - t, 3);
function animar(dur, passo, fim) {
  if (semMovimento() || dur <= 0) { passo(1); fim && fim(); return { parar() {} }; }
  let id = 0, t0 = 0, vivo = true;
  const tick = agora => {
    if (!vivo) return;
    if (!t0) t0 = agora;
    const t = Math.min(1, (agora - t0) / dur);
    passo(suave(t));
    if (t < 1) id = requestAnimationFrame(tick); else fim && fim();
  };
  id = requestAnimationFrame(tick);
  return { parar() { vivo = false; cancelAnimationFrame(id); } };
}
const lerp = (a, b, t) => a + (b - a) * t;
function reamostrar(arr, n) {                // adapta uma série antiga ao novo número de pontos
  if (!arr || !arr.length) return null;
  if (arr.length === n) return arr;
  const out = new Array(n);
  for (let i = 0; i < n; i++) {
    const p = n === 1 ? 0 : i / (n - 1) * (arr.length - 1), a = Math.floor(p), b = Math.min(arr.length - 1, a + 1);
    out[i] = arr[a] == null || arr[b] == null ? (arr[a] ?? arr[b]) : lerp(arr[a], arr[b], p - a);
  }
  return out;
}

/* dica flutuante compartilhada */
const Tip = {
  el: null,
  mostrar(html, x, y) {
    const el = this.el || (this.el = $('#tip'));
    el.innerHTML = html; el.classList.add('on');
    const r = el.getBoundingClientRect(), W = window.innerWidth, H = window.innerHeight;
    let l = x + 14, t = y + 16;
    if (l + r.width > W - 8) l = x - r.width - 14;
    if (l < 8) l = 8;
    if (t + r.height > H - 8) t = y - r.height - 12;
    if (t < 8) t = 8;
    el.style.transform = `translate(${Math.round(l)}px,${Math.round(t)}px)`;
  },
  ocultar() { if (this.el) this.el.classList.remove('on'); },
};
const tipHtml = (titulo, linhas, rodape) =>
  `<div class="tip-t">${esc(titulo)}</div>` +
  linhas.map(l => `<div class="tip-l${l.forte ? ' forte' : ''}"><i style="background:${l.cor || 'transparent'}"></i><span>${esc(l.n)}</span><b>${esc(l.v)}</b></div>`).join('') +
  (rodape ? `<div class="tip-f">${rodape}</div>` : '');

/* observa a largura dos contêineres para redesenhar */
const Redim = {
  itens: new Map(), obs: null,
  registrar(el, fn) {
    if (!this.obs && window.ResizeObserver) {
      this.obs = new ResizeObserver(ents => { for (const e of ents) { const it = this.itens.get(e.target); if (!it) continue; const w = Math.round(e.contentRect.width); if (w && w !== it.w) { it.w = w; it.fn(); } } });
    }
    this.itens.set(el, { fn, w: Math.round(el.clientWidth) });
    if (this.obs) this.obs.observe(el);
  },
};
const svgEl = (tag, attrs) => { const e = document.createElementNS(SVGNS, tag); if (attrs) for (const k in attrs) e.setAttribute(k, attrs[k]); return e; };
const vazioHtml = msg => `<div class="vazio"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg><span>${esc(msg)}</span></div>`;

/* ───────── linhas / áreas ───────── */
let _uid = 0;
function GraficoLinha(host, opt = {}) {
  const id = 'gl' + (++_uid);
  const st = { d: null, ant: null, anim: null, ocultas: new Set(), geo: null };
  host.classList.add('ch', 'ch-linha');
  host.innerHTML = `<svg class="ch-svg" role="img" aria-label="${esc(opt.rotulo || 'Gráfico de linhas')}"><defs></defs><g class="g-grade"></g><g class="g-area"></g><g class="g-linha"></g><g class="g-pts"></g><g class="g-ref"></g><g class="g-x"></g><g class="g-y"></g><g class="g-hover" style="display:none"><line class="guia"/><g class="pts"></g></g><rect class="pega" fill="transparent"/></svg><div class="ch-vazio" hidden></div>`;
  const svg = $('svg', host), G = n => $('.' + n, svg), vazio = $('.ch-vazio', host);
  const altura = () => parseFloat(getComputedStyle(host).getPropertyValue('--ch-h')) || opt.altura || 260;

  function caminho(xs, ys, degrau) {
    let d = '', aberto = false;
    for (let i = 0; i < xs.length; i++) {
      if (ys[i] == null) { aberto = false; continue; }
      if (!aberto) { d += `M${xs[i].toFixed(1)},${ys[i].toFixed(1)}`; aberto = true; }
      else if (degrau) d += `H${xs[i].toFixed(1)}V${ys[i].toFixed(1)}`;
      else d += `L${xs[i].toFixed(1)},${ys[i].toFixed(1)}`;
    }
    return d;
  }
  function areaPath(xs, ys, base, degrau) {  // base: número (linha de base) ou vetor (camada inferior)
    let d = '', ini = -1;
    const fecha = fim => {
      const b = k => (Array.isArray(base) ? base[k] : base);
      if (degrau && !Array.isArray(base)) d += `V${b(fim).toFixed(1)}H${xs[ini].toFixed(1)}Z`;
      else { for (let k = fim; k >= ini; k--) d += `L${xs[k].toFixed(1)},${b(k).toFixed(1)}`; d += 'Z'; }
    };
    for (let i = 0; i < xs.length; i++) {
      if (ys[i] == null) { if (ini >= 0) { fecha(i - 1); ini = -1; } continue; }
      if (ini < 0) { ini = i; d += `M${xs[i].toFixed(1)},${ys[i].toFixed(1)}`; }
      else if (degrau) d += `H${xs[i].toFixed(1)}V${ys[i].toFixed(1)}`;
      else d += `L${xs[i].toFixed(1)},${ys[i].toFixed(1)}`;
    }
    if (ini >= 0) fecha(xs.length - 1);
    return d;
  }

  function desenhar(animado) {
    const d = st.d; if (!d) return;
    const W = host.clientWidth; if (!W) return;
    const H = altura();
    const series = d.series.filter(s => !st.ocultas.has(s.k));
    const N = d.x.length;
    const temDados = N > 0 && series.some(s => s.v.some(v => v != null));
    vazio.hidden = temDados; svg.style.visibility = temDados ? '' : 'hidden';
    // o tamanho vem antes de tudo: um <svg> sem tamanho mede 300 px, e o gráfico vazio estouraria um cartão mais estreito que isso
    svg.setAttribute('width', W); svg.setAttribute('height', H); svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
    if (!temDados) {
      const desligadas = N > 0 && d.series.some(s => st.ocultas.has(s.k) && s.v.some(v => v != null));   // vazio porque o usuário ocultou as séries
      vazio.innerHTML = vazioHtml(desligadas ? 'Todas as séries estão ocultas. Clique na legenda para mostrá-las de novo.' : d.vazio || 'Sem dados para o período e os filtros escolhidos.'); st.ant = null;
      if (desligadas) Legenda(); else if (opt.legenda) opt.legenda.innerHTML = '';
      return;
    }

    // empilhamento
    const topo = series.map(s => s.v.slice());
    if (d.empilhar) for (let k = 1; k < series.length; k++) for (let i = 0; i < N; i++) topo[k][i] = (topo[k - 1][i] || 0) + (series[k].v[i] || 0);
    let lo = Infinity, hi = -Infinity;
    for (const t of topo) for (const v of t) if (v != null) { if (v < lo) lo = v; if (v > hi) hi = v; }
    for (const r of d.refs || []) if (r.v != null) { lo = Math.min(lo, r.v); hi = Math.max(hi, r.v); }
    if (d.zero !== false) lo = Math.min(0, lo);
    else { const folga = (hi - lo || hi || 1) * 0.12; lo = Math.max(0, lo - folga); hi += folga * 0.5; }
    const esc_ = ticksBonitos(lo, hi, H < 220 ? 3 : 4, d.inteiro);
    const fmtE = d.fmtEixo || d.fmtY || fInt;
    const larguraRot = Math.max(...esc_.ticks.map(t => String(fmtE(t)).length)) * 6.2 + 12;
    const m = { l: Math.max(30, Math.min(78, larguraRot)), r: 14, t: 10, b: 26 };
    const iw = Math.max(10, W - m.l - m.r), ih = Math.max(10, H - m.t - m.b);
    const x0 = d.x[0], x1 = d.x[N - 1];
    const px = i => (N === 1 || x1 === x0 ? m.l + iw / 2 : m.l + (d.x[i] - x0) / (x1 - x0) * iw);
    const py = v => m.t + ih - (v - esc_.min) / (esc_.max - esc_.min) * ih;
    const xs = d.x.map((_, i) => px(i));
    const alvoY = topo.map(t => t.map(v => (v == null ? null : py(v))));
    const base = py(Math.max(esc_.min, 0));

    // grade + eixo y
    let g = '', gy = '';
    for (const t of esc_.ticks) { const y = py(t).toFixed(1); g += `<line x1="${m.l}" x2="${W - m.r}" y1="${y}" y2="${y}"/>`; gy += `<text x="${m.l - 8}" y="${y}" dy="3.5" text-anchor="end">${esc(fmtE(t))}</text>`; }
    G('g-grade').innerHTML = g; G('g-y').innerHTML = gy;
    // eixo x
    const maxT = Math.max(2, Math.floor(iw / 78)), passo = Math.max(1, Math.ceil((N - 1) / maxT));
    let gx = '';
    const idx = []; for (let i = 0; i < N; i += passo) idx.push(i);
    if (N > 1) {                                   // o último ponto sempre tem rótulo; os vizinhos que colidiriam com ele saem
      if (idx[idx.length - 1] !== N - 1) idx.push(N - 1);
      while (idx.length > 2 && xs[N - 1] - xs[idx[idx.length - 2]] < 76) idx.splice(idx.length - 2, 1);
    }
    idx.forEach((i, k) => { const anc = k === 0 && N > 1 ? 'start' : k === idx.length - 1 && N > 1 ? 'end' : 'middle'; gx += `<text x="${xs[i].toFixed(1)}" y="${H - 7}" text-anchor="${anc}">${esc(d.rot(i))}</text>`; });
    G('g-x').innerHTML = gx;
    // linhas de referência
    G('g-ref').innerHTML = (d.refs || []).filter(r => r.v != null).map(r => { const y = py(r.v).toFixed(1); return `<line x1="${m.l}" x2="${W - m.r}" y1="${y}" y2="${y}" style="stroke:${r.cor || 'var(--ink-3)'}"/><text x="${W - m.r - 4}" y="${y}" dy="-5" text-anchor="end" style="fill:${r.cor || 'var(--ink-3)'}">${esc(r.n)}</text>`; }).join('');

    // séries
    $('defs', svg).innerHTML = series.map((s, k) => `<linearGradient id="${id}-${k}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" style="stop-color:${s.cor};stop-opacity:${d.empilhar ? 0.5 : 0.26}"/><stop offset="1" style="stop-color:${s.cor};stop-opacity:${d.empilhar ? 0.22 : 0.02}"/></linearGradient>`).join('');
    G('g-area').innerHTML = series.map((s, k) => (s.area ? `<path fill="url(#${id}-${k})"/>` : '<path fill="none"/>')).join('');
    G('g-linha').innerHTML = series.map(s => `<path fill="none" style="stroke:${s.cor}" stroke-width="${s.larg || 2}" ${s.tracejado ? 'stroke-dasharray="5 4"' : ''} stroke-linejoin="round" stroke-linecap="round"/>`).join('');
    const pa = $$('path', G('g-area')), pl = $$('path', G('g-linha'));
    if (st.anim) st.anim.parar();
    const antes = st.ant || {};                           // posição atual de cada série (mesmo no meio de uma animação)
    const de = series.map((s, k) => { const r = antes[s.k] ? reamostrar(antes[s.k], N) : null; return alvoY[k].map((y, i) => (y == null ? null : r && r[i] != null ? r[i] : base)); });
    const pinta = t => {
      const cur = alvoY.map((ys, k) => ys.map((y, i) => (y == null ? null : lerp(de[k][i], y, t))));
      series.forEach((s, k) => {
        pl[k].setAttribute('d', caminho(xs, cur[k], s.degrau));
        if (s.area) pa[k].setAttribute('d', areaPath(xs, cur[k], d.empilhar && k > 0 ? cur[k - 1].map(v => (v == null ? base : v)) : base, s.degrau));
      });
      // ponto sem vizinho não forma linha: vira marcador (ex.: a primeira cotação registrada de um livro)
      let soltos = '';
      series.forEach((s, k) => { const ys = cur[k]; for (let i = 0; i < N; i++) if (ys[i] != null && (i === 0 || ys[i - 1] == null) && (i === N - 1 || ys[i + 1] == null)) soltos += `<circle cx="${xs[i].toFixed(1)}" cy="${ys[i].toFixed(1)}" r="4" style="fill:${s.cor}"/>`; });
      G('g-pts').innerHTML = soltos;
      st.ant = Object.fromEntries(series.map((s, k) => [s.k, cur[k]]));
    };
    if (animado) st.anim = animar(650, pinta); else pinta(1);
    st.geo = { xs, m, W, H, iw, ih, series, topo, alvoY };
    const pega = $('.pega', svg); pega.setAttribute('x', m.l - 6); pega.setAttribute('y', m.t); pega.setAttribute('width', iw + 12); pega.setAttribute('height', ih + 6);
    Legenda();
  }

  function Legenda() {
    const el = opt.legenda; if (!el || !st.d) return;
    el.innerHTML = st.d.series.map(s => `<button type="button" class="leg${st.ocultas.has(s.k) ? ' off' : ''}" data-k="${esc(s.k)}" aria-pressed="${!st.ocultas.has(s.k)}" title="Mostrar ou ocultar"><i style="background:${s.cor}"></i>${esc(s.n)}</button>`).join('') +
      (st.d.refs || []).filter(r => r.v != null && r.leg).map(r => `<span class="leg ref"><i style="border-color:${r.cor || 'var(--ink-3)'}"></i>${esc(r.leg)}</span>`).join('');
  }
  if (opt.legenda) opt.legenda.addEventListener('click', e => {
    const b = e.target.closest('button[data-k]'); if (!b || !st.d) return;
    const k = b.dataset.k;
    if (st.ocultas.has(k)) st.ocultas.delete(k); else if (st.d.series.length - st.ocultas.size > 1) st.ocultas.add(k);
    desenhar(true);
  });

  // interação
  const hov = G('g-hover');
  function mover(ev) {
    const geo = st.geo, d = st.d; if (!geo || !d) return;
    const r = svg.getBoundingClientRect(), x = ev.clientX - r.left;
    let i = 0, best = Infinity;
    for (let k = 0; k < geo.xs.length; k++) { const dist = Math.abs(geo.xs[k] - x); if (dist < best) { best = dist; i = k; } }
    hov.style.display = '';
    const guia = $('.guia', hov); guia.setAttribute('x1', geo.xs[i]); guia.setAttribute('x2', geo.xs[i]); guia.setAttribute('y1', geo.m.t); guia.setAttribute('y2', geo.m.t + geo.ih);
    $('.pts', hov).innerHTML = geo.series.map((s, k) => (geo.alvoY[k][i] == null ? '' : `<circle cx="${geo.xs[i].toFixed(1)}" cy="${geo.alvoY[k][i].toFixed(1)}" r="4" style="fill:${s.cor}"/>`)).join('');
    const fmt = d.fmtY || fInt;
    const linhas = geo.series.map(s => ({ n: s.n, v: s.v[i] == null ? '—' : fmt(s.v[i]), cor: s.cor, val: s.v[i] })).filter(l => l.val != null);
    if (d.ordenarDica) linhas.sort((a, b) => a.val - b.val);
    if (d.empilhar && geo.series.length > 1) linhas.push({ n: 'Total', v: fmt(geo.topo[geo.topo.length - 1][i] || 0), forte: true });
    Tip.mostrar(tipHtml(d.tit ? d.tit(i) : d.rot(i), linhas, d.rodape ? d.rodape(i) : ''), ev.clientX, ev.clientY);
  }
  const sair = () => { hov.style.display = 'none'; Tip.ocultar(); };
  const pega = $('.pega', svg);
  pega.addEventListener('pointermove', mover); pega.addEventListener('pointerdown', mover);
  pega.addEventListener('pointerleave', sair); pega.addEventListener('pointercancel', sair);
  Redim.registrar(host, () => desenhar(false));
  return { atualizar(d) { st.d = d; for (const k of [...st.ocultas]) if (!d.series.some(s => s.k === k)) st.ocultas.delete(k); desenhar(true); }, redesenhar() { desenhar(false); } };
}

/* ───────── barras verticais (empilhadas) ───────── */
function GraficoBarras(host, opt = {}) {
  const st = { d: null, ant: new Map(), anim: null, geo: null };
  host.classList.add('ch', 'ch-barras');
  host.innerHTML = `<svg class="ch-svg" role="img" aria-label="${esc(opt.rotulo || 'Gráfico de barras')}"><g class="g-grade"></g><rect class="faixa" style="display:none"/><g class="g-barras"></g><g class="g-x"></g><g class="g-y"></g><rect class="pega" fill="transparent"/></svg><div class="ch-vazio" hidden></div>`;
  const svg = $('svg', host), G = n => $('.' + n, svg), vazio = $('.ch-vazio', host), faixa = $('.faixa', svg);
  const altura = () => parseFloat(getComputedStyle(host).getPropertyValue('--ch-h')) || opt.altura || 240;

  function desenhar(animado) {
    const d = st.d; if (!d) return;
    const W = host.clientWidth; if (!W) return;
    const H = altura(), N = d.rot.length;
    const totais = d.rot.map((_, i) => soma(d.series, s => s.v[i] || 0));
    const temDados = N > 0 && totais.some(t => t > 0);
    vazio.hidden = temDados; svg.style.visibility = temDados ? '' : 'hidden';
    svg.setAttribute('width', W); svg.setAttribute('height', H); svg.setAttribute('viewBox', `0 0 ${W} ${H}`);      // antes de tudo, como no gráfico de linhas
    if (!temDados) { vazio.innerHTML = vazioHtml(d.vazio || 'Sem movimentação no período.'); st.ant = new Map(); if (opt.legenda) opt.legenda.innerHTML = ''; return; }
    const esc_ = ticksBonitos(0, Math.max(...totais), H < 220 ? 3 : 4, d.inteiro);
    const fmtE = d.fmtEixo || d.fmtY || fInt;
    const larguraRot = Math.max(...esc_.ticks.map(t => String(fmtE(t)).length)) * 6.2 + 12;
    const m = { l: Math.max(28, Math.min(78, larguraRot)), r: 8, t: 10, b: 26 };
    const iw = Math.max(10, W - m.l - m.r), ih = Math.max(10, H - m.t - m.b);
    const banda = iw / N, lb = Math.max(3, Math.min(38, banda * 0.66));
    const py = v => m.t + ih - (v / esc_.max) * ih;
    let g = '', gy = '';
    for (const t of esc_.ticks) { const y = py(t).toFixed(1); g += `<line x1="${m.l}" x2="${W - m.r}" y1="${y}" y2="${y}"/>`; gy += `<text x="${m.l - 8}" y="${y}" dy="3.5" text-anchor="end">${esc(fmtE(t))}</text>`; }
    G('g-grade').innerHTML = g; G('g-y').innerHTML = gy;
    const cadaX = Math.max(1, Math.ceil(N / Math.max(2, Math.floor(iw / 56))));
    let gx = '';
    for (let i = 0; i < N; i++) if ((N - 1 - i) % cadaX === 0) gx += `<text x="${(m.l + banda * (i + 0.5)).toFixed(1)}" y="${H - 7}" text-anchor="middle">${esc(d.rot[i])}</text>`;
    G('g-x').innerHTML = gx;

    const alvo = [], novo = new Map();
    let html = '';
    for (let i = 0; i < N; i++) {
      let acum = 0;
      const x = m.l + banda * (i + 0.5) - lb / 2;
      d.series.forEach(s => {
        const v = s.v[i] || 0; if (v <= 0) return;
        const y1 = py(acum + v), y0 = py(acum); acum += v;
        const hh = Math.max(1.5, y0 - y1 - (acum < totais[i] ? 1.5 : 0));
        const chave = s.k + ':' + i, a = st.ant.get(chave);
        alvo.push({ y: y1 + (acum < totais[i] ? 1.5 : 0), h: hh, de: a || { y: m.t + ih, h: 0 } });
        novo.set(chave, { y: y1 + (acum < totais[i] ? 1.5 : 0), h: hh });
        html += `<rect x="${x.toFixed(1)}" width="${lb.toFixed(1)}" rx="${Math.min(3.5, lb / 3).toFixed(1)}" style="fill:${s.cor}${d.parcial === i ? ';opacity:.55' : ''}"/>`;
      });
    }
    G('g-barras').innerHTML = html;
    const rects = $$('rect', G('g-barras'));
    const pinta = t => { rects.forEach((r, k) => { const a = alvo[k]; r.setAttribute('y', lerp(a.de.y, a.y, t).toFixed(1)); r.setAttribute('height', Math.max(0, lerp(a.de.h, a.h, t)).toFixed(1)); }); };
    if (st.anim) st.anim.parar();
    if (animado) st.anim = animar(600, pinta); else pinta(1);
    st.ant = novo;
    st.geo = { m, banda, iw, ih, N, totais };
    const pega = $('.pega', svg); pega.setAttribute('x', m.l); pega.setAttribute('y', m.t); pega.setAttribute('width', iw); pega.setAttribute('height', ih + 4);
    Legenda();
  }
  function Legenda() {
    const el = opt.legenda; if (!el || !st.d) return;
    el.innerHTML = st.d.series.map(s => `<span class="leg"><i style="background:${s.cor}"></i>${esc(s.n)}</span>`).join('');
  }
  function mover(ev) {
    const geo = st.geo, d = st.d; if (!geo || !d) return;
    const r = svg.getBoundingClientRect(), x = ev.clientX - r.left;
    const i = clamp(Math.floor((x - geo.m.l) / geo.banda), 0, geo.N - 1);
    faixa.style.display = ''; faixa.setAttribute('x', geo.m.l + geo.banda * i + 1); faixa.setAttribute('y', geo.m.t); faixa.setAttribute('width', Math.max(0, geo.banda - 2)); faixa.setAttribute('height', geo.ih); faixa.setAttribute('rx', 6);
    const fmt = d.fmtY || fInt;
    const linhas = d.series.filter(s => (s.v[i] || 0) > 0).map(s => ({ n: s.n, v: fmt(s.v[i]), cor: s.cor }));
    if (d.series.length > 1 || !linhas.length) linhas.push({ n: 'Total', v: fmt(geo.totais[i]), forte: true });
    const extra = (d.parcial === i ? '<span>período em andamento</span>' : '') + (d.rodape ? d.rodape(i) : '');
    Tip.mostrar(tipHtml(d.tit ? d.tit[i] : d.rot[i], linhas, extra), ev.clientX, ev.clientY);
  }
  const sair = () => { faixa.style.display = 'none'; Tip.ocultar(); };
  const pega = $('.pega', svg);
  pega.addEventListener('pointermove', mover); pega.addEventListener('pointerdown', mover);
  pega.addEventListener('pointerleave', sair); pega.addEventListener('pointercancel', sair);
  Redim.registrar(host, () => desenhar(false));
  return { atualizar(d) { st.d = d; desenhar(true); }, redesenhar() { desenhar(false); } };
}

/* ───────── rosca ───────── */
function GraficoRosca(host, opt = {}) {
  const R = 74, C = 2 * Math.PI * R;
  const st = { d: null, fatias: new Map(), geo: [], ativo: null };
  host.classList.add('rosca');
  host.innerHTML = `<div class="rosca-g"><svg viewBox="0 0 200 200" role="img" aria-label="${esc(opt.rotulo || 'Gráfico de rosca')}"><circle class="trilho" cx="100" cy="100" r="${R}" fill="none"/><g class="fatias" transform="rotate(-90 100 100)"></g></svg><div class="rosca-c"><b></b><span></span></div></div><ul class="rosca-l"></ul><div class="ch-vazio" hidden></div>`;
  const svg = $('svg', host), gf = $('.fatias', host), centro = $('.rosca-c', host), lista = $('.rosca-l', host), vazio = $('.ch-vazio', host);

  const txtCentro = (t, r) => { const b = $('b', centro); b.textContent = t; b.classList.toggle('longo', String(t).length > 6); $('span', centro).textContent = r; };
  function centroPadrao() { const d = st.d; txtCentro(d.fmtTotal ? d.fmtTotal(d.total) : fInt(d.total), d.unidade || ''); centro.classList.remove('foco'); }
  function focar(k, ev) {
    st.ativo = k;
    for (const [kk, el] of st.fatias) el.classList.toggle('on', kk === k);
    gf.classList.toggle('dim', k != null);
    $$('li', lista).forEach(li => li.classList.toggle('on', li.dataset.k === String(k)));
    if (k == null) { centroPadrao(); Tip.ocultar(); return; }
    const f = st.d.fatias.find(x => String(x.k) === String(k)); if (!f) return;
    const fmt = st.d.fmt || fInt;
    txtCentro(fPct(f.v / st.d.total), f.n); centro.classList.add('foco');
    if (ev) Tip.mostrar(tipHtml(f.n, [{ n: st.d.unidade || 'valor', v: fmt(f.v), cor: f.cor }, { n: 'participação', v: fPct(f.v / st.d.total) }], opt.aoClicar && f.filtravel !== false ? '<span>clique para filtrar</span>' : ''), ev.clientX, ev.clientY);
  }
  function atualizar(d) {
    st.d = d;
    const fat = d.fatias.filter(f => f.v > 0);
    d.total = soma(fat, f => f.v);
    const tem = d.total > 0;
    vazio.hidden = tem; $('.rosca-g', host).style.display = tem ? '' : 'none'; lista.style.display = tem ? '' : 'none';
    if (!tem) { vazio.innerHTML = vazioHtml(d.vazio || 'Nada por aqui com os filtros atuais.'); for (const el of st.fatias.values()) el.remove(); st.fatias.clear(); return; }
    const folga = fat.length > 1 ? 2.5 : 0;
    let ini = 0; const vistos = new Set(); st.geo = [];
    for (const f of fat) {
      const k = String(f.k), comp = f.v / d.total * C, len = Math.max(0.01, comp - folga);
      let el = st.fatias.get(k);
      if (!el) {
        el = svgEl('circle', { class: 'fatia', cx: 100, cy: 100, r: R, fill: 'none' });
        el.style.strokeDasharray = `0.01 ${C}`; el.style.strokeDashoffset = String(-ini);
        gf.appendChild(el); st.fatias.set(k, el);
        el.getBoundingClientRect();                      // força o estado inicial antes da transição
      }
      el.style.stroke = f.cor; el.style.strokeDasharray = `${len.toFixed(2)} ${(C - len).toFixed(2)}`; el.style.strokeDashoffset = (-ini).toFixed(2);
      st.geo.push({ k, a: ini / C, b: (ini + comp) / C });
      ini += comp; vistos.add(k);
    }
    for (const [k, el] of [...st.fatias]) if (!vistos.has(k)) { el.style.strokeDasharray = `0.01 ${C}`; st.fatias.delete(k); setTimeout(() => el.remove(), 500); }
    const fmt = d.fmt || fInt;
    lista.innerHTML = fat.map(f => `<li data-k="${esc(f.k)}" class="${f.ativo ? 'sel' : ''}" ${opt.aoClicar && f.filtravel !== false ? 'role="button" tabindex="0"' : ''}><i style="background:${f.cor}"></i><span>${esc(f.n)}</span><b>${esc(fmt(f.v))}</b><em>${fPct(f.v / d.total)}</em></li>`).join('');
    st.ativo = null; gf.classList.remove('dim'); for (const el of st.fatias.values()) el.classList.remove('on');
    centroPadrao();
  }
  function fatiaEm(ev) {
    const r = svg.getBoundingClientRect(), s = 200 / r.width, dx = (ev.clientX - r.left) * s - 100, dy = (ev.clientY - r.top) * s - 100, dist = Math.hypot(dx, dy);
    if (dist < R - 17 || dist > R + 17) return null;
    let ang = Math.atan2(dy, dx) + Math.PI / 2; if (ang < 0) ang += 2 * Math.PI;
    const fr = ang / (2 * Math.PI), g = st.geo.find(x => fr >= x.a && fr < x.b);
    return g ? g.k : null;
  }
  const clicavel = k => { if (k == null || !opt.aoClicar) return false; const f = st.d.fatias.find(x => String(x.k) === String(k)); return !!f && f.filtravel !== false; };
  svg.addEventListener('pointermove', ev => { const k = fatiaEm(ev); if (k !== st.ativo || k != null) focar(k, ev); svg.style.cursor = clicavel(k) ? 'pointer' : ''; });
  svg.addEventListener('pointerleave', () => focar(null));
  svg.addEventListener('click', ev => { const k = fatiaEm(ev); if (clicavel(k)) { Tip.ocultar(); opt.aoClicar(k, st.d); } });
  lista.addEventListener('pointerover', ev => { const li = ev.target.closest('li'); if (li) focar(li.dataset.k); });
  lista.addEventListener('pointerleave', () => focar(null));
  lista.addEventListener('click', ev => { const li = ev.target.closest('li[role]'); if (li && opt.aoClicar) opt.aoClicar(li.dataset.k, st.d); });
  lista.addEventListener('keydown', ev => { if (ev.key !== 'Enter' && ev.key !== ' ') return; const li = ev.target.closest('li[role]'); if (li && opt.aoClicar) { ev.preventDefault(); opt.aoClicar(li.dataset.k, st.d); } });
  return { atualizar };
}

/* ───────── barras horizontais (HTML) ───────── */
function BarrasH(host, opt = {}) {
  const st = { d: null, linhas: new Map() };
  host.classList.add('hbar');
  const corpo = document.createElement('div'); corpo.className = 'hbar-c'; host.appendChild(corpo);
  const vazio = document.createElement('div'); vazio.className = 'ch-vazio'; vazio.hidden = true; host.appendChild(vazio);
  function atualizar(d) {
    st.d = d;
    const max = d.max || Math.max(1, ...d.linhas.map(l => l.total != null ? l.total : soma(l.segs, s => s.v)));
    const tem = d.linhas.some(l => soma(l.segs, s => s.v) > 0);
    vazio.hidden = tem; corpo.style.display = tem ? '' : 'none';
    if (!tem) { vazio.innerHTML = vazioHtml(d.vazio || 'Nada por aqui com os filtros atuais.'); return; }
    const fmt = d.fmt || fInt, vistos = new Set();
    d.linhas.forEach((l, pos) => {
      const k = String(l.k); vistos.add(k);
      const total = l.total != null ? l.total : soma(l.segs, s => s.v);
      let el = st.linhas.get(k), novo = false;
      if (!el) {
        el = document.createElement(opt.aoClicar ? 'button' : 'div'); if (opt.aoClicar) el.type = 'button';
        el.className = 'hb'; el.dataset.k = k;
        el.innerHTML = '<span class="hb-n"></span><span class="hb-t"></span><span class="hb-v"></span>';
        st.linhas.set(k, el); novo = true;
      }
      if (corpo.children[pos] !== el) corpo.insertBefore(el, corpo.children[pos] || null);
      el.classList.toggle('sel', !!l.ativo); el.classList.toggle('zero', total === 0);
      $('.hb-n', el).textContent = l.n; $('.hb-n', el).title = l.dica || l.n;
      $('.hb-v', el).textContent = l.rotV != null ? l.rotV : fmt(total);
      const t = $('.hb-t', el);
      while (t.children.length < l.segs.length) { const i = document.createElement('i'); i.style.width = '0%'; t.appendChild(i); }
      while (t.children.length > l.segs.length) t.lastChild.remove();
      const aplica = () => l.segs.forEach((s, j) => { const i = t.children[j]; i.style.background = s.cor; i.style.width = (s.v / max * 100).toFixed(2) + '%'; });
      if (novo && !semMovimento()) requestAnimationFrame(() => requestAnimationFrame(aplica)); else aplica();
    });
    for (const [k, el] of [...st.linhas]) if (!vistos.has(k)) { el.remove(); st.linhas.delete(k); }
    host.classList.toggle('tem-sel', d.linhas.some(l => l.ativo));
  }
  const dica = ev => {
    const el = ev.target.closest('.hb'); if (!el || !st.d) return;
    const l = st.d.linhas.find(x => String(x.k) === el.dataset.k); if (!l) return;
    const fmt = st.d.fmt || fInt, linhas = l.segs.filter(s => s.v > 0 || l.segs.length === 1).map(s => ({ n: s.n, v: fmt(s.v), cor: s.cor }));
    if (l.segs.length > 1) linhas.push({ n: 'Total', v: fmt(soma(l.segs, s => s.v)), forte: true });
    Tip.mostrar(tipHtml(l.dica || l.n, linhas, (l.rodape || '') + (opt.aoClicar ? `<span>${l.ativo ? 'clique para remover o filtro' : 'clique para filtrar'}</span>` : '')), ev.clientX, ev.clientY);
  };
  corpo.addEventListener('pointermove', dica);
  corpo.addEventListener('pointerleave', () => Tip.ocultar());
  if (opt.aoClicar) corpo.addEventListener('click', ev => { const el = ev.target.closest('.hb'); if (el) { Tip.ocultar(); opt.aoClicar(el.dataset.k); } });
  return { atualizar };
}

/* ───────── barras divergentes (variação %) ───────── */
function BarrasDiv(host, opt = {}) {
  const st = { d: null, linhas: new Map() };
  host.classList.add('dbar');
  const corpo = document.createElement('div'); corpo.className = 'dbar-c'; host.appendChild(corpo);
  const vazio = document.createElement('div'); vazio.className = 'ch-vazio'; vazio.hidden = true; host.appendChild(vazio);
  function atualizar(d) {
    st.d = d;
    const tem = d.linhas.length > 0;
    vazio.hidden = tem; corpo.style.display = tem ? '' : 'none';
    if (!tem) { vazio.innerHTML = vazioHtml(d.vazio || 'Sem cotações no período.'); return; }
    const max = Math.max(0.01, ...d.linhas.map(l => Math.abs(l.v))), vistos = new Set();
    d.linhas.forEach((l, pos) => {
      const k = String(l.k); vistos.add(k);
      let el = st.linhas.get(k), novo = false;
      if (!el) {
        el = document.createElement('button'); el.type = 'button'; el.className = 'db'; el.dataset.k = k;
        el.innerHTML = '<span class="db-n"></span><span class="db-t"><i style="width:0%"></i></span><span class="db-v"></span>';
        st.linhas.set(k, el); novo = true;
      }
      if (corpo.children[pos] !== el) corpo.insertBefore(el, corpo.children[pos] || null);
      const neg = l.v < 0, zero = Math.abs(l.v) < 0.0005;
      el.classList.toggle('sel', !!l.ativo);
      $('.db-n', el).textContent = l.n;
      const v = $('.db-v', el); v.textContent = zero ? '0%' : fPct(l.v, true); v.className = 'db-v ' + (zero ? '' : neg ? 'bom' : 'ruim');
      const i = $('i', el); i.className = neg ? 'neg' : 'pos';
      const aplica = () => { i.style.width = (zero ? 0 : Math.max(0.6, Math.abs(l.v) / max * 50)).toFixed(2) + '%'; };
      if (novo && !semMovimento()) requestAnimationFrame(() => requestAnimationFrame(aplica)); else aplica();
    });
    for (const [k, el] of [...st.linhas]) if (!vistos.has(k)) { el.remove(); st.linhas.delete(k); }
  }
  corpo.addEventListener('pointermove', ev => {
    const el = ev.target.closest('.db'); if (!el || !st.d) return;
    const l = st.d.linhas.find(x => String(x.k) === el.dataset.k); if (!l) return;
    Tip.mostrar(tipHtml(l.n, l.dica || [], opt.dicaClique ? `<span>${opt.dicaClique}</span>` : ''), ev.clientX, ev.clientY);
  });
  corpo.addEventListener('pointerleave', () => Tip.ocultar());
  corpo.addEventListener('click', ev => { const el = ev.target.closest('.db'); if (el && opt.aoClicar) { Tip.ocultar(); opt.aoClicar(el.dataset.k); } });
  return { atualizar };
}

/* ───────── minigráfico ───────── */
function spark(vals, o = {}) {
  const w = o.w || 96, h = o.h || 28, cor = o.cor || 'var(--accent)';
  const v = vals.filter(x => x != null);
  if (v.length < 2) return `<svg class="spark" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" aria-hidden="true"><line x1="2" x2="${w - 2}" y1="${h / 2}" y2="${h / 2}" stroke="var(--line-2)" stroke-dasharray="2 3"/></svg>`;
  let lo = Math.min(...v), hi = Math.max(...v); if (o.zero) lo = Math.min(0, lo); if (hi === lo) { hi += 1; lo -= 1; }
  const n = vals.length, X = i => 2 + i / (n - 1) * (w - 6), Y = x => 3 + (1 - (x - lo) / (hi - lo)) * (h - 6);
  let d = '', ult = null, prim = null;
  vals.forEach((x, i) => {
    if (x == null) return;
    const a = X(i).toFixed(1), b = Y(x).toFixed(1);
    if (prim == null) { prim = i; d += `M${a},${b}`; } else d += o.degrau ? `H${a}V${b}` : `L${a},${b}`;
    ult = i;
  });
  const area = o.area === false ? '' : `<path d="${d}L${X(ult).toFixed(1)},${h}L${X(prim).toFixed(1)},${h}Z" style="fill:${cor}" opacity=".12"/>`;
  return `<svg class="spark" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" aria-hidden="true">${area}<path d="${d}" fill="none" style="stroke:${cor}" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round"/><circle cx="${X(ult).toFixed(1)}" cy="${Y(vals[ult]).toFixed(1)}" r="2.3" style="fill:${cor}"/></svg>`;
}

/* número que "conta" até o novo valor */
function contarAte(el, valor, fmt) {
  const de = el._v != null && isFinite(el._v) ? el._v : 0;
  if (el._a) el._a.parar();
  el._v = valor;
  if (valor == null || !isFinite(valor)) { el.textContent = '—'; return; }
  if (de === valor) { el.textContent = fmt(valor); return; }
  el._a = animar(550, t => { el.textContent = fmt(lerp(de, valor, t)); }, () => { el.textContent = fmt(valor); });
}

/* troca o HTML só quando ele muda (evita piscar listas a cada atualização) */
function setHtml(el, html) { if (el._h !== html) { el._h = html; el.innerHTML = html; } }
function amostra(serie, de, ate, n) {         // reamostra uma série em degraus [[dia, valor], …] em n pontos igualmente espaçados
  const out = []; let j = 0;
  for (let k = 0; k < n; k++) {
    const d = n < 2 ? ate : de + (ate - de) * k / (n - 1);
    while (j + 1 < serie.length && serie[j + 1][0] <= d) j++;
    out.push(serie.length && serie[j][0] <= d ? serie[j][1] : serie.length ? serie[0][1] : null);
  }
  return out;
}
