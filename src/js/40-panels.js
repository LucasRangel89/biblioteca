/* ───────────────────────── painéis (KPIs, gráficos e listas) ───────────────────────── */
const maiuscula = s => s.charAt(0).toUpperCase() + s.slice(1);
const badgeSit = s => `<span class="sit sit-${s}">${SITUACOES[s].n}</span>`;
const pontos = n => `<span class="pts" aria-hidden="true">${[1, 2, 3].map(i => `<i${i <= n ? ' class="on"' : ''}></i>`).join('')}</span>`;
const estrelas = n => `<span class="estrelas" role="img" title="${n} de 5" aria-label="nota ${n} de 5">${[1, 2, 3, 4, 5].map(i => `<i${i <= n ? ' class="on"' : ''} aria-hidden="true">★</i>`).join('')}</span>`;
const varHtml = (v, bomSeCair = true) => (v == null || !isFinite(v) ? '<span class="mudo">—</span>' : `<span class="var ${Math.abs(v) < 0.0005 ? '' : (v < 0) === bomSeCair ? 'bom' : 'ruim'}">${Math.abs(v) < 0.0005 ? '0%' : fPct(v, true)}</span>`);

function cartao(def) {
  const el = document.createElement('section');
  el.className = 'card ' + (def.w || 'p-6'); el.id = 'p-' + def.id;
  el.innerHTML = `<header class="card-h"><div class="card-tt"><h3>${esc(def.tit)}</h3><p class="card-s"></p></div><div class="card-t"></div></header><div class="card-b"></div><div class="card-f legs"></div>`;
  return { el, sub: $('.card-s', el), tools: $('.card-t', el), corpo: $('.card-b', el), pe: $('.card-f', el) };
}
function segmento(host, opcoes, chave) {       // seletor de modo de um painel (guardado em S.ui)
  const el = document.createElement('div'); el.className = 'seg mini'; el.setAttribute('role', 'group');
  el.innerHTML = opcoes.map(([v, n]) => `<button type="button" data-v="${v}">${esc(n)}</button>`).join('');
  const marca = () => $$('button', el).forEach(b => b.setAttribute('aria-pressed', String(String(S.ui[chave]) === b.dataset.v)));
  el.addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; S.ui[chave] = /^\d+$/.test(b.dataset.v) ? +b.dataset.v : b.dataset.v; marca(); salvar(); render(); });
  marca(); host.appendChild(el);
}
const legendaFixa = (el, itens) => setHtml(el, itens.map(([n, cor]) => `<span class="leg"><i style="background:${cor}"></i>${esc(n)}</span>`).join(''));

/* ───────── KPIs ───────── */
function Kpis(host, defs) {
  host.innerHTML = defs.map(d => `<article class="kpi" data-k="${d.k}"><header><span class="kpi-i" style="--k:${d.cor || 'var(--accent)'}">${icone(d.ic, 17)}</span><span class="kpi-n">${esc(d.n)}</span></header><div class="kpi-v"><b class="num"></b><span class="kpi-sp"></span></div><div class="kpi-t"></div><p class="kpi-s"></p></article>`).join('');
  return vals => {
    for (const d of defs) {
      const el = $(`[data-k="${d.k}"]`, host), v = vals[d.k]; if (!v) continue;
      const b = $('.kpi-v b', el);
      if (v.txt != null) { if (b._a) b._a.parar(); b._v = null; b.textContent = v.txt; } else contarAte(b, v.v, v.fmt || fInt);
      setHtml($('.kpi-sp', el), v.spark ? spark(v.spark, { cor: d.cor || 'var(--accent)', zero: v.zero, w: 84, h: 30, degrau: v.degrau }) : '');
      setHtml($('.kpi-t', el), (v.tend ? `<span class="tend ${v.tend.cls}">${icone(v.tend.dir, 12)}${esc(v.tend.txt)}</span>` : '') + `<span class="cmp">${esc(v.cmp || '')}</span>`);
      const ks = $('.kpi-s', el); ks.textContent = v.sub || ''; ks.title = v.sub || '';
      b.title = v.dica || '';
    }
  };
}
/* legenda das tendências de preço: o histórico pode ter começado dentro da janela de comparação (ou hoje mesmo) */
const cmpPrecos = (c, normal, curto) => (c.refDe >= c.I.ate ? 'histórico começa hoje' : c.pxIni > c.I.cur.de ? curto || `desde ${fDiaMes(c.pxIni)}` : normal);
const K = {
  acervo(c) {
    const I = c.I, tot = c.ac.filter(b => adqDe(b) == null || adqDe(b) <= I.ate), novos = c.ac.filter(b => dentro(adqDe(b), I.cur)).length;
    const fis = tot.filter(temFisico).length, dig = tot.filter(temDigital).length, amb = tot.filter(b => posseDe(b) === 'ambos').length, aud = tot.filter(b => b.fmt === 'audio').length;
    const datado = c.ac.some(b => adqDe(b) != null);   // sem nenhuma data de aquisição não há como falar em crescimento
    return { v: tot.length, tend: datado ? tend(tot.length, tot.length - novos, 'alta') : null, cmp: datado ? `+${fInt(novos)} ${I.cmpC}` : tot.length ? 'sem datas de aquisição' : '', sub: [plural(fis, 'físico', 'físicos'), plural(dig, 'digital', 'digitais'), aud ? `${fInt(aud)} em áudio` : '', amb ? `${fInt(amb)} nos dois` : ''].filter(Boolean).join(' · '), spark: acumulado(baldes(I.de, I.ate, 20), c.ac, b => adqDe(b)) };
  },
  investido(c) {
    const I = c.I, val = soma(c.acP, b => pagoDe(b) || 0), pagos = c.acP.filter(b => pagoDe(b) > 0).length;
    const cur = soma(c.ac, b => (dentro(adqDe(b), I.cur) ? pagoDe(b) || 0 : 0)), ant = soma(c.ac, b => (dentro(adqDe(b), I.ant) ? pagoDe(b) || 0 : 0));
    const t = tend(cur, ant, 'neutro');   // sem valor nos dois períodos não há comparação (nem legenda de comparação)
    return { v: val, fmt: fBRL0, tend: t, cmp: t ? I.cmp : '', sub: pagos ? `${plural(pagos, 'compra', 'compras')} · média de ${fBRL(val / pagos)}` : 'nenhuma compra com valor registrado', spark: porBalde(baldes(I.de, I.ate, 20), c.ac, b => adqDe(b), b => pagoDe(b) || 0), zero: true };
  },
  leituras(c) {
    const I = c.I, n = c.lidosP.length;
    const cur = c.lidos.filter(b => dentro(b.lidoEm, I.cur)).length, ant = c.lidos.filter(b => dentro(b.lidoEm, I.ant)).length;
    const pg = soma(c.lidosP, b => b.pg || 0), notas = c.lidosP.filter(b => b.nota > 0);
    const fora = c.lidosP.filter(b => b.col !== 'acervo').length, nota = notas.length ? fDec(soma(notas, b => b.nota) / notas.length) : '';
    const sub = (fora ? [`${fInt(n - fora)} do acervo + ${fInt(fora)} de fora`, nota ? `nota ${nota}` : ''] : [pg ? `~${fInt(Math.round(pg / 100) * 100)} páginas` : '', nota ? `nota média ${nota}` : '']).filter(Boolean).join(' · ');
    const t = tend(cur, ant, 'alta');
    return { v: n, tend: t, cmp: t ? I.cmp : '', sub: sub || (n ? 'sem páginas ou notas registradas' : 'nenhuma leitura concluída no recorte'), spark: porBalde(baldes(I.de, I.ate, 20), c.lidos, b => b.lidoEm), zero: true };
  },
  cesta(c) {
    const I = c.I, comPx = c.des.filter(b => b.px);
    if (!comPx.length) return { txt: '—', sub: c.des.length ? `${plural(c.des.length, 'item', 'itens')} sem cotação registrada` : 'nenhum item na lista com estes filtros' };
    const hoje = c.cestaEm(I.ate), ref = c.cestaEm(c.refDe);
    // desconto sobre a capa: só entre os itens que têm as duas pontas (preço de hoje e preço de capa)
    const comCapa = comPx.filter(b => b.capa > 0 && c.px(b).hoje), capa = soma(comCapa, b => b.capa), eco = capa > 0 ? 1 - soma(comCapa, b => c.px(b).hoje.p) / capa : 0;
    const n = Math.min(24, I.ate - c.pxDe + 1), sp = [];
    for (let i = 0; i < n; i++) sp.push(c.cestaEm(Math.round(c.pxDe + (I.ate - c.pxDe) * (n < 2 ? 0 : i / (n - 1)))));
    return { v: hoje, fmt: fBRL0, tend: c.refDe < I.ate ? tend(hoje, ref, 'baixa') : null, cmp: cmpPrecos(c, I.cmpC), sub: `${plural(c.des.length, 'item', 'itens')}${eco > 0.005 ? ` · ${fPct(eco)} abaixo da capa` : ''}`, spark: sp };
  },
  oport(c, lista) {
    const I = c.I, arr = lista || c.des, sits = arr.map(b => c.px(b).sit), agora = sits.filter(s => s === 'agora').length, quase = sits.filter(s => s === 'quase').length;
    const antes = arr.filter(b => situacaoDe(b, c.refDe) === 'agora').length;
    const custo = soma(arr, b => { const x = c.px(b); return x.sit === 'agora' ? x.hoje.p : 0; });
    return { v: agora, tend: c.refDe < I.ate ? tendAbs(agora - antes, 'alta') : null, cmp: arr.some(b => b.px) ? cmpPrecos(c, I.tudo ? 'vs. 12 meses atrás' : 'vs. início do período', 'vs. 1ª cotação') : '', sub: `${agora ? fBRL0(custo) + ' no total · ' : ''}${fInt(quase)} quase lá` };
  },
  recs(c) {
    if (S.acervo !== 'tudo' && S.visao !== 'recs') return { txt: '—', sub: 'recomendações não têm formato definido' };
    const I = c.I, fila = c.rec.filter(b => b.leit !== 'lido' && (b.add == null || b.add <= I.ate)), novos = fila.filter(b => dentro(b.add, I.cur)).length;
    const datado = c.rec.some(b => b.add != null);
    return { v: fila.length, tend: datado ? tendAbs(novos, 'neutro') : null, cmp: datado ? `${novos === 1 ? 'incluída' : 'incluídas'} ${I.cmpC}` : '', sub: `${plural(fila.filter(b => b._top).length, 'prioridade marcada', 'prioridades marcadas')} com #top`, spark: acumulado(baldes(I.de, I.ate, 20), fila, b => b.add) };
  },
  fila(c) {
    const I = c.I, fila = c.ac.filter(b => b.leit !== 'lido' && b.leit !== 'aband'), lendo = c.ac.filter(b => b.leit === 'lendo').length, lidos = c.ac.filter(b => b.leit === 'lido').length;
    const entrou = c.ac.filter(b => dentro(adqDe(b), I.cur)).length, saiu = c.ac.filter(b => b.leit === 'lido' && dentro(b.lidoEm, I.cur)).length;
    const datado = c.ac.some(b => adqDe(b) != null || b.lidoEm != null);
    return { v: fila.length, tend: datado ? tendAbs(entrou - saiu, 'baixa') : null, cmp: datado ? I.cmpC : '', sub: `${fInt(lendo)} em leitura · ${c.ac.length ? fPct(lidos / c.ac.length) : '0%'} do acervo já lido` };
  },
};

/* ───────── painéis compartilhados ───────── */
const rotEixoX = (d, span) => (span > 150 ? fMesAno(d) : fDiaMes(d));
function pEvolucao() {
  return { id: 'evolucao', w: 'p-8', tit: 'Evolução do acervo', montar(k) {
    segmento(k.tools, [['qtd', 'Livros'], ['valor', 'Valor']], 'evo');
    const g = GraficoLinha(k.corpo, { legenda: k.pe, rotulo: 'Evolução do acervo por formato' });
    return c => {
      const B = baldes(c.I.de, c.I.ate, 64), x = B.lista.map(b => b.f), val = S.ui.evo === 'valor', semData = c.ac.filter(b => adqDe(b) == null).length;
      const series = Object.keys(FORMATOS).map(f => ({ k: f, n: FORMATOS[f].n, cor: FORMATOS[f].cor, area: true, v: acumulado(B, c.ac.filter(b => b.fmt === f), b => adqDe(b), val ? b => pagoDe(b) || 0 : null) })).filter(s => s.v[s.v.length - 1] > 0);
      k.sub.textContent = `${val ? 'Valor investido acumulado' : 'Livros acumulados'} por formato · ${c.I.rot}${semData ? ` · ${plural(semData, 'livro sem data não entra', 'livros sem data não entram')}` : ''}`;
      g.atualizar({ x, series, empilhar: true, inteiro: !val, fmtY: val ? fBRL : fInt, fmtEixo: val ? fBRLc : fInt, rot: i => (B.g === 'dia' || B.g === 'semana' ? fDiaMes(x[i]) : B.g === 'ano' ? String(partes(x[i]).y) : fMesAno(x[i])), tit: i => 'Até ' + fData(x[i]), vazio: 'Nenhum livro com data de aquisição neste recorte. Edite um livro para informar quando ele chegou.' });
    };
  } };
}
function pComposicao() {
  return { id: 'composicao', w: 'p-4 m-6', tit: 'Composição do acervo', montar(k) {
    segmento(k.tools, [['fmt', 'Formato'], ['tipo', 'Tipo'], ['leit', 'Leitura']], 'compor');
    const g = GraficoRosca(k.corpo, { rotulo: 'Composição do acervo', aoClicar(key) {
      if (S.ui.compor === 'fmt') { const alvo = key === 'fisico' || key === 'ambos' ? key : 'virtual'; S.acervo = S.acervo === alvo ? 'tudo' : alvo; }
      else if (S.ui.compor === 'tipo') { const alvo = key === 'F' || key === 'NF' ? key : 'O'; S.tipo = S.tipo === alvo ? '' : alvo; }
      else return;
      filtrosMudaram();
    } });
    return c => {
      const m = S.ui.compor, mapa = m === 'fmt' ? POSSES : m === 'tipo' ? TIPOS : LEITURAS, cont = contarPor(c.acP, m === 'fmt' ? posseDe : m === 'tipo' ? b => b._tipo : b => b.leit);
      k.sub.textContent = `${c.I.tudo ? 'Todo o acervo' : 'Adquiridos ' + c.I.rot} · por ${m === 'fmt' ? 'formato' : m === 'tipo' ? 'tipo' : 'situação de leitura'}`;
      g.atualizar({ unidade: 'livros', fatias: Object.keys(mapa).map(key => ({ k: key, n: mapa[key].n, cor: mapa[key].cor, v: cont.get(key) || 0, filtravel: m !== 'leit' })), vazio: 'Nenhum livro do acervo neste recorte.' });
    };
  } };
}
function pAquisicoes() {
  return { id: 'aquisicoes', w: 'p-6 m-6', tit: 'Aquisições por período', montar(k) {
    segmento(k.tools, [['qtd', 'Livros'], ['valor', 'Valor']], 'aq');
    const g = GraficoBarras(k.corpo, { legenda: k.pe, rotulo: 'Aquisições por período e formato' });
    return c => {
      const B = baldes(c.I.de, c.I.ate, 24), val = S.ui.aq === 'valor', L = B.lista;
      k.sub.textContent = `${val ? 'Valor pago' : 'Livros adquiridos'} por ${L.length > 1 ? NOME_GRAN[B.g] + ' e ' : ''}formato · ${c.I.rot}`;
      g.atualizar({ rot: L.map(b => b.rot), tit: L.map(b => b.tit), parcial: L.length && L[L.length - 1].parcial ? L.length - 1 : -1, inteiro: !val, fmtY: val ? fBRL : fInt, fmtEixo: val ? fBRLc : fInt,
        series: Object.keys(FORMATOS).map(f => ({ k: f, n: FORMATOS[f].n, cor: FORMATOS[f].cor, v: porBalde(B, c.ac.filter(b => b.fmt === f), b => adqDe(b), val ? b => pagoDe(b) || 0 : null) })), vazio: 'Nenhuma aquisição com data neste recorte.' });
    };
  } };
}
function pCesta(w, id) {
  return { id: id || 'cesta', w: w || 'p-6', tit: 'Custo da cesta de aquisições', montar(k) {
    const g = GraficoLinha(k.corpo, { legenda: k.pe, rotulo: 'Custo da cesta de próximas aquisições ao longo do tempo' });
    return c => {
      const des = c.des.filter(b => b.px), ini = c.pxDe, fim = c.I.ate;
      const n = des.length && fim >= c.pxIni ? Math.min(90, fim - ini + 1) : 0, x = [];
      for (let i = 0; i < n; i++) x.push(Math.round(ini + (fim - ini) * (n < 2 ? 0 : i / (n - 1))));
      const ev = n ? eventosPromo(ini, fim) : [], alvo = soma(des, b => b.alvo || 0);
      k.sub.textContent = des.length ? `Soma do melhor preço de ${plural(des.length, 'item', 'itens')} da lista atual · ${c.I.tudo ? 'desde a primeira cotação' : c.I.rot}` : 'Soma do melhor preço de cada item da lista de compra';
      g.atualizar({ x, zero: false, fmtY: fBRL, fmtEixo: fBRLc, rot: i => rotEixoX(x[i], fim - ini), tit: i => fDiaMesAno(x[i]),
        series: [{ k: 'cesta', n: 'Melhor preço somado', cor: 'var(--accent)', area: true, larg: 2.2, v: x.map(d => c.cestaEm(d)) }],
        refs: alvo ? [{ v: alvo, n: 'alvos ' + fBRL0(alvo), leg: 'Soma dos preços-alvo', cor: 'var(--good)' }] : [],
        rodape: i => { const e = ev.find(e => x[i] >= e.de && x[i] <= e.ate); return e ? `<span>${esc(e.n)}</span>` : ''; },
        vazio: c.des.length ? 'Os itens da lista ainda não têm cotações neste período.' : 'A lista de próximas aquisições está vazia neste recorte.' });
    };
  } };
}
function pEixos(modo, w) {
  const tit = { geral: 'Catálogo por eixo temático', acervo: 'Acervo por eixo e leitura', recs: 'Recomendações por eixo' }[modo];
  return { id: 'eixos-' + modo, w, tit, montar(k) {
    const g = BarrasH(k.corpo, { aoClicar(e) { alternar(S.eixos, +e); filtrosMudaram(); } });
    return c => {
      const E = c.E, cont = arr => contarPor(arr, b => b.eixo);
      const grupos = modo === 'geral' ? [['Acervo', COLECOES.acervo.cor, cont(E.acP)], ['Próximas aquisições', COLECOES.desejo.cor, cont(E.des)], ['Recomendações', COLECOES.rec.cor, cont(E.recP)]]
        : modo === 'acervo' ? ['lido', 'lendo', 'fila', 'aband', ''].map(s => [LEITURAS[s].n, LEITURAS[s].cor, cont(E.acP.filter(b => b.leit === s))])
        : [['Prioridade (#top)', 'var(--accent)', cont(E.recP.filter(b => b._top && b.leit !== 'lido'))], ['Demais', 'var(--c4)', cont(E.recP.filter(b => !b._top && b.leit !== 'lido'))]];
      const usados = grupos.filter(gr => gr[2].size);
      const linhas = [];
      for (let e = 1; e <= 16; e++) linhas.push({ k: e, n: EIXOS[e].n, dica: EIXOS[e].l, ativo: S.eixos.has(e), segs: usados.map(gr => ({ n: gr[0], cor: gr[1], v: gr[2].get(e) || 0 })) });
      linhas.sort((a, z) => soma(z.segs, s => s.v) - soma(a.segs, s => s.v) || a.k - z.k);
      k.sub.textContent = (modo === 'geral' ? 'Livros por eixo e lista' : modo === 'acervo' ? 'Livros do acervo por situação de leitura' : 'Títulos sugeridos em cada eixo') + ' · clique para filtrar';
      legendaFixa(k.pe, usados.map(gr => [gr[0], gr[1]]));
      g.atualizar({ linhas, vazio: 'Nenhum livro neste recorte.' });
    };
  } };
}
const linhaLivro = (b, meio, fim) => `<button type="button" class="li" data-id="${b.id}"><span class="li-m"><b>${esc(b.t)}</b><span>${esc(b.a || 'Autor não informado')}</span></span>${meio || ''}${fim || ''}</button>`;
function pRanking() {
  return { id: 'ranking', w: 'p-5', tit: 'Melhores oportunidades', montar(k) {
    k.tools.innerHTML = `<button type="button" class="btn sm fantasma" data-ir="desejos">Ver lista${icone('dir', 14)}</button>`;
    k.corpo.classList.add('lista');
    return c => {
      const it = c.des.map(b => ({ b, x: c.px(b) })).filter(o => o.x.hoje && o.b.alvo).sort((a, z) => a.x.hoje.p / a.b.alvo - z.x.hoje.p / z.b.alvo).slice(0, 7);
      k.sub.textContent = 'Itens da lista de compra mais perto (ou abaixo) do preço-alvo';
      setHtml(k.corpo, it.length ? it.map(({ b, x }) => `<button type="button" class="li" data-id="${b.id}"><span class="li-m"><b>${esc(b.t)}</b><span>${esc(x.hoje.f)} · alvo ${fBRL0(b.alvo)}</span></span>` +
        `<span class="li-sp">${x.res ? spark(amostra(x.res.serie, x.res.de, x.res.ate, 20), { w: 60, h: 24, cor: SITUACOES[x.sit].cor, area: false }) : ''}</span>` +
        `<span class="li-pb"><b class="num">${fBRL(x.hoje.p)}</b>${badgeSit(x.sit)}</span></button>`).join('')
        : vazioHtml(c.des.length ? 'Defina um preço-alvo e registre cotações para ver as oportunidades.' : 'Nenhum item na lista de próximas aquisições neste recorte.'));
    };
  } };
}

/* ───────── biblioteca ───────── */
function pAdqLidos() {
  return { id: 'adq-lidos', w: 'p-8', tit: 'Adquiridos × lidos', montar(k) {
    const g = GraficoLinha(k.corpo, { legenda: k.pe, rotulo: 'Livros adquiridos e livros lidos, acumulados' });
    return c => {
      const B = baldes(c.I.de, c.I.ate, 64), x = B.lista.map(b => b.f);
      const adq = acumulado(B, c.ac, b => adqDe(b)), lid = acumulado(B, c.ac.filter(b => b.leit === 'lido'), b => b.lidoEm);
      const tem = adq.length && adq[adq.length - 1] > 0;
      k.sub.textContent = `Acumulado no acervo · a distância entre as linhas é a fila de leitura · ${c.I.rot}`;
      g.atualizar({ x: tem ? x : [], inteiro: true, zero: c.I.tudo, rot: i => (B.g === 'dia' || B.g === 'semana' ? fDiaMes(x[i]) : B.g === 'ano' ? String(partes(x[i]).y) : fMesAno(x[i])), tit: i => 'Até ' + fData(x[i]),
        series: tem ? [{ k: 'adq', n: 'Adquiridos', cor: 'var(--c2)', area: true, v: adq }, { k: 'lidos', n: 'Lidos', cor: 'var(--c6)', area: true, v: lid }] : [],
        rodape: i => `<span>${fInt(Math.max(0, adq[i] - lid[i]))} por ler</span>`, vazio: 'Nenhum livro com data de aquisição neste recorte.' });
    };
  } };
}
function pStatus() {
  return { id: 'status', w: 'p-4 m-6', tit: 'Situação de leitura', montar(k) {
    const g = GraficoRosca(k.corpo, { rotulo: 'Situação de leitura do acervo' });
    return c => {
      const cont = contarPor(c.acP, b => b.leit);
      k.sub.textContent = c.I.tudo ? 'Todo o acervo' : 'Livros adquiridos ' + c.I.rot;
      g.atualizar({ unidade: 'livros', fatias: Object.keys(LEITURAS).map(s => ({ k: s || 'nd', n: LEITURAS[s].n, cor: LEITURAS[s].cor, v: cont.get(s) || 0, filtravel: false })), vazio: 'Nenhum livro do acervo neste recorte.' });
    };
  } };
}
function pLeituras() {
  return { id: 'leituras', w: 'p-6 m-6', tit: 'Leituras concluídas', montar(k) {
    const g = GraficoBarras(k.corpo, { legenda: k.pe, rotulo: 'Leituras concluídas por período e formato' });
    return c => {
      const B = baldes(c.I.de, c.I.ate, 24), L = B.lista, semData = c.lidos.filter(b => b.lidoEm == null).length;
      k.sub.textContent = `Livros terminados por ${L.length > 1 ? NOME_GRAN[B.g] + ' e ' : ''}formato · ${c.I.rot}${semData && c.I.tudo ? ` · ${plural(semData, 'lido sem data', 'lidos sem data')}` : ''}`;
      g.atualizar({ rot: L.map(b => b.rot), tit: L.map(b => b.tit), parcial: L.length && L[L.length - 1].parcial ? L.length - 1 : -1, inteiro: true,
        series: Object.keys(FORMATOS).map(f => ({ k: f, n: FORMATOS[f].n, cor: FORMATOS[f].cor, v: porBalde(B, c.lidos.filter(b => b.fmt === f), b => b.lidoEm) })), vazio: 'Nenhuma leitura concluída com data neste recorte.' });
    };
  } };
}
function pOrigens() {
  return { id: 'origens', w: 'p-6 m-6', tit: 'Onde comprei', montar(k) {
    segmento(k.tools, [['qtd', 'Livros'], ['valor', 'Valor']], 'origem');
    const g = BarrasH(k.corpo, {});
    return c => {
      const val = S.ui.origem === 'valor', m = new Map();
      for (const b of c.acP) { if (!lojaDe(b)) continue; const o = m.get(b.loja) || { n: 0, v: 0, f: {} }; o.n++; o.v += pagoDe(b) || 0; o.f[b.fmt] = (o.f[b.fmt] || 0) + (val ? pagoDe(b) || 0 : 1); m.set(b.loja, o); }
      const linhas = [...m].sort((a, z) => (val ? z[1].v - a[1].v : z[1].n - a[1].n)).slice(0, 10).map(([loja, o]) => ({ k: loja, n: loja, segs: Object.keys(FORMATOS).map(f => ({ n: FORMATOS[f].n, cor: FORMATOS[f].cor, v: o.f[f] || 0 })), rodape: `<span>${plural(o.n, 'livro', 'livros')} · ${fBRL(o.v)}${o.n ? ' · média ' + fBRL(o.v / o.n) : ''}</span>` }));
      k.sub.textContent = `${val ? 'Valor pago' : 'Livros'} por loja ou origem · ${c.I.rot}`;
      legendaFixa(k.pe, Object.keys(FORMATOS).filter(f => linhas.some(l => l.segs.some(s => s.n === FORMATOS[f].n && s.v > 0))).map(f => [FORMATOS[f].n, FORMATOS[f].cor]));
      g.atualizar({ linhas, fmt: val ? fBRL0 : fInt, vazio: 'Nenhuma origem registrada neste recorte. Informe a loja ao editar um livro.' });
    };
  } };
}
function pLendo() {
  return { id: 'lendo', w: 'p-5 m-6', tit: 'Na cabeceira', montar(k) {
    k.corpo.classList.add('lista');
    return c => {
      const lendo = c.ac.filter(b => b.leit === 'lendo').sort((a, z) => (z.prog || 0) - (a.prog || 0)).slice(0, 4);
      const ult = c.lidosP.filter(b => b.lidoEm != null).sort((a, z) => z.lidoEm - a.lidoEm).slice(0, 5);
      k.sub.textContent = 'Em leitura agora e últimas leituras concluídas' + (c.I.tudo ? '' : ' ' + c.I.rot);
      let h = '';
      if (lendo.length) h += '<h4 class="li-t">Lendo agora</h4>' + lendo.map(b => linhaLivro(b, '', `<span class="li-prog" title="${b.prog || 0}% lido"><span class="barra"><i style="width:${clamp(b.prog || 0, 0, 100)}%"></i></span><b class="num">${b.prog || 0}%</b></span><span class="fmt so-ic" title="${FORMATOS[b.fmt] ? FORMATOS[b.fmt].n : ''}">${icone(ICONE_FMT[b.fmt] || 'livro', 15)}</span>`)).join('');
      if (ult.length) h += '<h4 class="li-t">Concluídas</h4>' + ult.map(b => linhaLivro(b, '', `<span class="li-v"><b>${b.nota ? estrelas(b.nota) : '<span class="mudo">sem nota</span>'}</b><span>${fData(b.lidoEm)}</span></span>`)).join('');
      setHtml(k.corpo, h || vazioHtml('Nada em leitura nem leituras concluídas neste recorte. Abra um livro do acervo e use “Começar a ler”.'));
    };
  } };
}

/* ───────── recomendações ───────── */
function pMatriz() {
  return { id: 'matriz', w: 'p-5 m-6', tit: 'Fôlego de leitura', montar(k) {
    let h = '<div class="matriz"><span class="mz-q"><span>extensão →</span><span>dificuldade ↓</span></span>' + [1, 2, 3].map(e => `<span class="mz-h"><b>${EXTENSOES[e].n}</b><em>${EXTENSOES[e].d}</em></span>`).join('');
    for (const d of [1, 2, 3]) { h += `<span class="mz-r">${NIVEIS[d].n}</span>`; for (const e of [1, 2, 3]) h += `<button type="button" class="mz" data-d="${d}" data-e="${e}"><b class="num">0</b><span></span></button>`; }
    k.corpo.innerHTML = h + '</div>';
    const cels = $$('.mz', k.corpo);
    k.corpo.addEventListener('click', ev => {
      const b = ev.target.closest('.mz'); if (!b) return;
      const d = +b.dataset.d, e = +b.dataset.e, mesmo = S.dif.size === 1 && S.dif.has(d) && S.ext.size === 1 && S.ext.has(e);
      S.dif.clear(); S.ext.clear(); if (!mesmo) { S.dif.add(d); S.ext.add(e); }
      filtrosMudaram();
    });
    return c => {
      const base = c.DE.recP.filter(b => b.leit !== 'lido'), m = {}; let max = 1;
      for (const b of base) { if (!b._d || !b._e) continue; const key = b._d + '-' + b._e; m[key] = (m[key] || 0) + 1; if (m[key] > max) max = m[key]; }
      k.sub.textContent = 'Dificuldade × extensão das recomendações · clique numa célula para filtrar';
      for (const el of cels) {
        const d = +el.dataset.d, e = +el.dataset.e, n = m[d + '-' + e] || 0, sel = S.dif.has(d) && S.ext.has(e), filtrado = S.dif.size > 0 || S.ext.size > 0;
        el.style.setProperty('--i', (n / max).toFixed(3));
        el.classList.toggle('sel', sel); el.classList.toggle('fora', filtrado && !sel); el.setAttribute('aria-pressed', String(sel));
        el.title = `${NIVEIS[d].n} · ${EXTENSOES[e].n.toLowerCase()} (${EXTENSOES[e].d}): ${plural(n, 'título', 'títulos')}`;
        contarAte($('b', el), n, fInt); $('span', el).textContent = base.length ? fPct(n / base.length) : '';
      }
    };
  } };
}
function pTipoRecs() {
  return { id: 'tipo-recs', w: 'p-4 m-6', tit: 'Ficção × não ficção', montar(k) {
    const g = GraficoRosca(k.corpo, { rotulo: 'Recomendações por tipo', aoClicar(key) { const alvo = key === 'F' || key === 'NF' ? key : 'O'; S.tipo = S.tipo === alvo ? '' : alvo; filtrosMudaram(); } });
    return c => {
      const cont = contarPor(c.recP.filter(b => b.leit !== 'lido'), b => b._tipo);     // a fila: o que ainda não foi lido
      k.sub.textContent = 'Recomendações por tipo' + (c.I.tudo ? '' : ' · incluídas ' + c.I.rot);
      g.atualizar({ unidade: 'títulos', fatias: Object.keys(TIPOS).map(t => ({ k: t, n: TIPOS[t].n, cor: TIPOS[t].cor, v: cont.get(t) || 0 })), vazio: 'Nenhuma recomendação neste recorte.' });
    };
  } };
}
function pTemas() {
  return { id: 'temas', w: 'p-4 m-6', tit: 'Temas e trilhas', montar(k) {
    segmento(k.tools, [[0, 'Gêneros'], [1, 'Temas'], [2, 'Origem'], [3, 'Trilhas']], 'temas');
    const g = BarrasH(k.corpo, { aoClicar(t) { alternar(S.tags, t); filtrosMudaram(); } });
    return c => {
      const lista = GRUPOS_TAG[S.ui.temas] ? GRUPOS_TAG[S.ui.temas][1] : GRUPOS_TAG[1][1], cont = new Map();
      for (const b of c.recP) if (b.leit !== 'lido') for (const t of b.tags) if (lista.includes(t)) cont.set(t, (cont.get(t) || 0) + 1);
      k.sub.textContent = 'Marcadores mais frequentes nas recomendações · clique para filtrar';
      g.atualizar({ linhas: [...cont].sort((a, z) => z[1] - a[1]).slice(0, 9).map(([t, n]) => ({ k: t, n: maiuscula(rotTag(t)), dica: '#' + t, ativo: S.tags.has(t), segs: [{ n: 'recomendações', cor: 'var(--c2)', v: n }] })), vazio: 'Nenhum marcador deste grupo no recorte atual.' });
    };
  } };
}
function pSugestoes() {
  return { id: 'sugestoes', w: 'p-4 m-6', tit: 'Sugestões da vez', montar(k) {
    k.tools.innerHTML = `<button type="button" class="btn sm" data-sortear>${icone('sortear', 14)}Sortear</button>`;
    k.tools.addEventListener('click', e => { if (e.target.closest('[data-sortear]')) { S.ui.sorteio = (S.ui.sorteio || 0) + 1; render(); } });
    k.corpo.classList.add('lista');
    return c => {
      const r = mulberry32(hashStr('sug|' + (S.ui.sorteio || 0) + '|' + c.T));
      const esc5 = c.recP.filter(b => b.leit !== 'lido').map(b => [b, (b._top ? 0.5 : 0) + r()]).sort((a, z) => z[1] - a[1]).slice(0, 5).map(x => x[0]);
      k.sub.textContent = 'Cinco títulos do recorte atual, com preferência pelas prioridades';
      setHtml(k.corpo, esc5.length ? esc5.map(b => linhaLivro(b, '', `<span class="li-v"><b>${pontos(b._d)}</b><span>${b._d ? NIVEIS[b._d].n.toLowerCase() : '—'} · ${b._e ? EXTENSOES[b._e].n.toLowerCase() : '—'}</span></span>${b._top ? `<span class="top" title="Prioridade (#top)">${icone('estrela', 14)}</span>` : '<span class="top vazio"></span>'}`)).join('') : vazioHtml('Nenhuma recomendação neste recorte.'));
    };
  } };
}

/* ───────── próximas aquisições ───────── */
function pPrioridade() {
  return { id: 'prioridade', w: 'p-4 m-6', tit: 'Cesta por prioridade', montar(k) {
    segmento(k.tools, [['valor', 'Valor'], ['itens', 'Itens']], 'prio');
    const g = GraficoRosca(k.corpo, { rotulo: 'Cesta de aquisições por prioridade' });
    return c => {
      const val = S.ui.prio === 'valor';
      k.sub.textContent = val ? 'Melhor preço de hoje somado por prioridade' : 'Itens da lista por prioridade';
      g.atualizar({ unidade: val ? 'na cesta' : 'itens', fmt: val ? fBRL0 : fInt, fmtTotal: val ? fBRL0 : fInt, vazio: c.des.length ? 'Os itens da lista ainda não têm cotação.' : 'A lista de próximas aquisições está vazia neste recorte.',
        fatias: [1, 2, 3, 0].map(p => ({ k: 'p' + p, n: PRIORIDADES[p].n, cor: PRIORIDADES[p].cor, filtravel: false, v: soma(c.des.filter(b => (b.prio || 0) === p), b => (val ? (c.px(b).hoje ? c.px(b).hoje.p : 0) : 1)) })) });
    };
  } };
}
function pDistancia() {
  return { id: 'distancia', w: 'p-7', tit: 'Distância até o preço-alvo', montar(k) {
    k.corpo.classList.add('rolavel');
    const g = BarrasDiv(k.corpo, { dicaClique: 'clique para abrir o livro', aoClicar: id => abrirLivro(id) });
    return c => {
      k.sub.textContent = 'Melhor preço de hoje em relação ao alvo · à esquerda, já vale comprar';
      g.atualizar({ linhas: c.des.map(b => ({ b, x: c.px(b) })).filter(o => o.x.hoje && o.b.alvo).map(({ b, x }) => ({ k: b.id, n: b.t, v: x.hoje.p / b.alvo - 1, dica: [{ n: 'Melhor preço · ' + x.hoje.f, v: fBRL(x.hoje.p) }, { n: 'Preço-alvo', v: fBRL(b.alvo) }, { n: 'Diferença', v: fBRL(x.hoje.p - b.alvo), forte: true }] })).sort((a, z) => a.v - z.v),
        vazio: c.des.length ? 'Defina preços-alvo e registre cotações para comparar.' : 'A lista de próximas aquisições está vazia neste recorte.' });
    };
  } };
}
function pLojasBaratas() {
  return { id: 'lojas', w: 'p-5 m-6', tit: 'Onde está mais barato', montar(k) {
    const g = BarrasH(k.corpo, {});
    const extra = document.createElement('div'); extra.className = 'resumo-fmt'; k.corpo.appendChild(extra);
    return c => {
      const m = new Map();
      for (const b of c.des) { const x = c.px(b); if (!x.hoje) continue; const o = m.get(x.hoje.f) || { n: 0, v: 0 }; o.n++; o.v += x.hoje.p; m.set(x.hoje.f, o); }
      k.sub.textContent = 'Loja com o melhor preço de hoje para cada item da lista';
      g.atualizar({ linhas: [...m].sort((a, z) => z[1].n - a[1].n).map(([f, o]) => ({ k: f, n: f, segs: [{ n: 'itens mais baratos aqui', cor: corFonte(f), v: o.n }], rodape: `<span>${fBRL(o.v)} somados</span>` })), vazio: 'Sem cotações para comparar lojas.' });
      let barato = 0, caro = 0, comp = 0;             // quanto custa não comparar: melhor × pior loja de cada item
      for (const b of c.des) {
        const x = c.px(b); if (!x.hoje) continue;
        const ps = fontesDe(b).map(f => precoEm(b.px[f], c.I.ate)).filter(Boolean).map(o => o[1]); if (ps.length < 2) continue;
        comp++; barato += x.hoje.p; caro += Math.max(...ps);
      }
      const porFmt = contarPor(c.des, b => b.fmt || 'fisico');
      setHtml(extra, (comp && caro > barato ? `<span class="rf-t">Vale comparar · ${plural(comp, 'item cotado', 'itens cotados')} em 2 ou mais lojas</span><span class="pr-i"><em>Na mais barata</em><b class="num">${fBRL0(barato)}</b></span><span class="pr-i"><em>Na mais cara</em><b class="num">${fBRL0(caro)}</b></span><span class="pr-i"><em>Diferença</em><b class="num bom">${fBRL0(caro - barato)}</b><span>${fPct(1 - barato / caro)} a menos</span></span>` : '') +
        (c.des.length ? '<span class="rf-t">Formato desejado</span>' + Object.keys(FORMATOS).filter(f => porFmt.get(f)).map(f => `<span class="rf"><span class="fmt">${icone(ICONE_FMT[f], 15)}${FORMATOS[f].n}</span><b class="num">${fInt(porFmt.get(f))}</b></span>`).join('') : ''));
    };
  } };
}

/* ───────── preços ───────── */
function livroSel(c) {
  let b = c.rast.find(x => x.id === S.sel);
  if (!b) b = c.rast.find(x => c.px(x).sit === 'agora') || c.rast[0] || null;
  S.sel = b ? b.id : '';
  return b;
}
function pPrecoLoja() {
  return { id: 'px-loja', w: 'p-8', tit: 'Preço por loja', montar(k) {
    k.tools.innerHTML = '<label class="sel-w"><span class="so-leitor">Livro acompanhado</span><select aria-label="Livro acompanhado"></select></label>';
    const sel = $('select', k.tools);
    sel.addEventListener('change', () => { S.sel = sel.value; render(); });
    const g = GraficoLinha(k.corpo, { legenda: k.pe, rotulo: 'Histórico de preço por loja' });
    const res = document.createElement('div'); res.className = 'px-res'; k.corpo.after(res);
    res.addEventListener('click', e => { const b = e.target.closest('[data-id]'); if (b) abrirLivro(b.dataset.id); });
    return c => {
      const b = livroSel(c), ord = arr => arr.slice().sort((a, z) => a.t.localeCompare(z.t, 'pt-BR'));
      const grupo = (n, arr) => (arr.length ? `<optgroup label="${n}">${ord(arr).map(x => `<option value="${x.id}">${esc(x.t)}</option>`).join('')}</optgroup>` : '');
      setHtml(sel, grupo('Próximas aquisições', c.rast.filter(x => x.col === 'desejo')) + grupo('Recomendações monitoradas', c.rast.filter(x => x.col !== 'desejo')));
      sel.value = b ? b.id : ''; sel.disabled = !b; sel.parentNode.hidden = !b;
      if (!b) { k.sub.textContent = 'Histórico de cotações de um livro, loja a loja'; setHtml(res, ''); g.atualizar({ x: [], series: [], rot: () => '', vazio: 'Nenhum item com cotações neste recorte. Abra um livro e use “Registrar cotação” para começar a acompanhar.' }); return; }
      const fontes = Object.keys(b.px).filter(f => b.px[f].length), prim = Math.min(...fontes.map(f => b.px[f][0][0])), ini = Math.max(c.I.de, prim), fim = c.I.ate;
      let x = [];
      if (fim >= ini) { const dias = new Set([ini, fim]); for (const f of fontes) for (const p of b.px[f]) if (p[0] > ini && p[0] < fim) dias.add(p[0]); x = [...dias].sort((a, z) => a - z); }
      if (x.length > 420) { const passo = x.length / 420, y = []; for (let i = 0; i < 420; i++) y.push(x[Math.floor(i * passo)]); y[y.length - 1] = x[x.length - 1]; x = y; }
      const doFmt = fontesDe(b), ev = x.length ? eventosPromo(ini, fim) : [], xp = c.px(b);
      k.sub.textContent = `${b.t}${b.a ? ' — ' + b.a : ''} · ${c.I.tudo ? 'desde a primeira cotação' : c.I.rot}`;
      g.atualizar({ x, zero: false, ordenarDica: true, fmtY: fBRL, fmtEixo: fBRLc, rot: i => rotEixoX(x[i], fim - ini), tit: i => fDiaMesAno(x[i]),
        series: fontes.map(f => ({ k: f, n: f + (doFmt.includes(f) ? '' : tipoFonte(f) === 'virtual' ? ' (e-book)' : ' (físico)'), cor: corFonte(f), degrau: true, larg: 2, tracejado: !doFmt.includes(f), v: x.map(d => { const o = precoEm(b.px[f], d); return o ? o[1] : null; }) })),
        refs: b.alvo ? [{ v: b.alvo, n: 'alvo ' + fBRL(b.alvo), leg: 'Preço-alvo', cor: 'var(--good)' }] : [],
        rodape: i => { const e = ev.find(e => x[i] >= e.de && x[i] <= e.ate); return e ? `<span>${esc(e.n)}</span>` : ''; }, vazio: 'Este livro ainda não tinha cotações neste período.' });
      setHtml(res, xp.hoje ? `<span class="pr-i"><em>Melhor preço</em><b class="num">${fBRL(xp.hoje.p)}</b><span>${esc(xp.hoje.f)}</span></span>` +
        (xp.res ? `<span class="pr-i"><em>Mínimo no período</em><b class="num">${fBRL(xp.res.min)}</b><span>${fDiaMes(xp.res.minDia)} · ${esc(xp.res.minFonte)}</span></span><span class="pr-i"><em>Variação</em><b>${varHtml(xp.res.var)}</b><span>melhor preço</span></span>` : '') +
        `<span class="pr-i"><em>Preço-alvo</em><b class="num">${b.alvo ? fBRL(b.alvo) : '—'}</b><span>${badgeSit(xp.sit)}</span></span><button type="button" class="btn sm" data-id="${b.id}">Abrir livro${icone('dir', 14)}</button>` : '');
    };
  } };
}
function pAlertas() {
  return { id: 'alertas', w: 'p-4 m-6', tit: 'Alertas de preço', montar(k) {
    k.corpo.classList.add('lista', 'rolavel');
    return c => {
      const T = c.I.ate, al = [];
      for (const b of c.rast) {
        const x = c.px(b); if (!x.hoje) continue;
        const s7 = melhorEm(b, T - 7), v7 = s7 ? x.hoje.p / s7.p - 1 : 0, r180 = resumoPrecos(b, T - 180, T), onde = `${fBRL(x.hoje.p)} · ${x.hoje.f}`;
        if (x.sit === 'agora') al.push({ b, ic: 'alvo', cls: 'bom', t: x.hoje.p < b.alvo - 0.005 ? `${fPct(1 - x.hoje.p / b.alvo)} abaixo do alvo de ${fBRL0(b.alvo)}` : `No preço-alvo de ${fBRL0(b.alvo)}`, d: onde, o: x.hoje.p / b.alvo });
        else if (v7 <= -0.08) al.push({ b, ic: 'queda', cls: 'bom', t: `Caiu ${fPct(-v7)} em 7 dias`, d: onde, o: 2 + v7 });
        else if (r180 && x.hoje.p <= r180.min + 0.005 && r180.max > r180.min * 1.04) al.push({ b, ic: 'queda', cls: 'bom', t: 'Menor preço em 6 meses', d: onde, o: 2.5 });
        else if (x.sit === 'quase') al.push({ b, ic: 'relogio', cls: 'aviso', t: `Faltam ${fBRL(x.hoje.p - b.alvo)} para o alvo`, d: onde, o: 3 + x.hoje.p / b.alvo });
        else if (v7 >= 0.08) al.push({ b, ic: 'alta', cls: 'ruim', t: `Subiu ${fPct(v7)} em 7 dias`, d: onde, o: 6 - v7 });
      }
      al.sort((a, z) => a.o - z.o);
      k.sub.textContent = al.length ? `${plural(al.length, 'aviso', 'avisos')} em ${fData(T)}` : 'Quedas, altas e itens perto do alvo';
      setHtml(k.corpo, al.length ? al.map(a => `<button type="button" class="li al" data-sel="${a.b.id}"><span class="al-i ${a.cls}">${icone(a.ic, 15)}</span><span class="li-m"><b>${esc(a.b.t)}</b><span class="al-t ${a.cls}">${esc(a.t)}</span><span class="al-d">${esc(a.d)}</span></span></button>`).join('') : vazioHtml(c.rast.length ? 'Nenhum movimento relevante: nada abaixo do alvo nem variações acima de 8% na semana.' : 'Sem itens acompanhados neste recorte.'));
    };
  } };
}
function pVariacao() {
  return { id: 'variacao', w: 'p-7', tit: 'Variação do melhor preço', montar(k) {
    k.corpo.classList.add('rolavel');
    const g = BarrasDiv(k.corpo, { dicaClique: 'clique para ver o histórico por loja', aoClicar: id => selecionarPreco(id) });
    return c => {
      k.sub.textContent = `Do início ao fim do período, por item acompanhado · ${c.I.tudo ? 'desde a primeira cotação' : c.I.rot}`;
      g.atualizar({ linhas: c.rast.map(b => ({ b, r: c.px(b).res })).filter(o => o.r).map(({ b, r }) => ({ k: b.id, n: b.t, v: r.var, ativo: b.id === S.sel, dica: [{ n: 'Início · ' + fData(r.de), v: fBRL(r.ini) }, { n: 'Fim · ' + fData(r.ate), v: fBRL(r.fim) }, { n: 'Mínimo · ' + r.minFonte, v: fBRL(r.min) }, { n: 'Média', v: fBRL(r.media) }] })).sort((a, z) => a.v - z.v), vazio: 'Sem cotações no período para calcular variações.' });
    };
  } };
}
function pCotacao() {
  return { id: 'cotacao', w: 'p-5 m-6', tit: 'Registrar cotação', montar(k) {
    k.sub.textContent = 'O painel não consulta lojas: confira o preço e anote aqui';
    // a lista traz também quem ainda não tem nenhuma cotação (é aqui que a primeira entra)
    let novo = '';
    const f = formCotacao(k.corpo, { comLivro: true, aoEscolher(b) { novo = b.id; }, aoSalvar(b) { S.sel = b.id; novo = ''; } });
    return c => {
      const lista = c.seg.filter(b => b.col === 'desejo' || (b.col === 'rec' && b.track));
      f.atualizar(lista, lista.find(b => b.id === novo && !rastreado(b)) || livroSel(c) || lista[0] || null);
    };
  } };
}
function selecionarPreco(id) {
  S.sel = id; render();
  const el = $('#p-px-loja'); if (el && el.getBoundingClientRect().top < 0) el.scrollIntoView({ behavior: semMovimento() ? 'auto' : 'smooth', block: 'start' });
}

/* ───────── definição de cada visão ───────── */
const VIS = {
  geral: {
    kpis: [
      { k: 'acervo', n: 'Acervo', ic: 'estante', cor: 'var(--c2)' }, { k: 'investido', n: 'Investido', ic: 'carteira', cor: 'var(--c1)' },
      { k: 'leituras', n: 'Leituras concluídas', ic: 'livro', cor: 'var(--c6)' }, { k: 'cesta', n: 'Cesta de aquisições', ic: 'sacola', cor: 'var(--c1)' },
      { k: 'oport', n: 'Abaixo do preço-alvo', ic: 'alvo', cor: 'var(--good)' }, { k: 'recs', n: 'Recomendações na fila', ic: 'bussola', cor: 'var(--c4)' },
    ],
    valores: c => ({ acervo: K.acervo(c), investido: K.investido(c), leituras: K.leituras(c), cesta: K.cesta(c), oport: K.oport(c), recs: K.recs(c) }),
    paineis: () => [pEvolucao(), pComposicao(), pAquisicoes(), pCesta('p-6'), pEixos('geral', 'p-7'), pRanking()],
  },
  biblioteca: {
    kpis: [
      { k: 'acervo', n: 'Livros no acervo', ic: 'estante', cor: 'var(--c2)' }, { k: 'investido', n: 'Investido', ic: 'carteira', cor: 'var(--c1)' },
      { k: 'leituras', n: 'Leituras concluídas', ic: 'livro', cor: 'var(--c6)' }, { k: 'fila', n: 'Por ler', ic: 'pilha', cor: 'var(--c4)' },
    ],
    valores: c => ({ acervo: K.acervo(c), investido: K.investido(c), leituras: K.leituras(c), fila: K.fila(c) }),
    paineis: () => [pAdqLidos(), pStatus(), pLeituras(), pOrigens(), pEixos('acervo', 'p-7'), pLendo()],
  },
  recs: {
    kpis: [
      { k: 'recs', n: 'Recomendações na fila', ic: 'bussola', cor: 'var(--c4)' }, { k: 'top', n: 'Prioridades', ic: 'estrela', cor: 'var(--c3)' },
      { k: 'leves', n: 'Leves e curtas', ic: 'raio', cor: 'var(--c6)' }, { k: 'pend', n: 'Pendências', ic: 'info', cor: 'var(--c8)' },
    ],
    valores(c) {
      const fila = c.rec.filter(b => b.leit !== 'lido'), top = fila.filter(b => b._top).length, topDes = c.des.filter(b => b._top).length;
      const leves = fila.filter(b => b._d === 1 && b._e === 1).length, semPt = fila.filter(b => b.tags.includes('sem-pt')).length, verif = fila.filter(b => b.tags.includes('verificar')).length;
      return {
        recs: K.recs(c),
        top: { v: top, cmp: fila.length ? fPct(top / fila.length) + ' da fila' : '', sub: topDes ? `${topDes === 1 ? 'outra 1 já está' : 'outras ' + fInt(topDes) + ' já estão'} na lista de compra` : 'marcadas com #top no catálogo' },
        leves: { v: leves, cmp: fila.length ? fPct(leves / fila.length) + ' da fila' : '', sub: 'leitura leve, até ~250 páginas' },
        pend: { v: semPt + verif, cmp: '', sub: `${fInt(semPt)} sem edição em PT · ${fInt(verif)} a verificar` },
      };
    },
    paineis: () => [pEixos('recs', 'p-7'), pMatriz(), pTipoRecs(), pTemas(), pSugestoes()],
  },
  desejos: {
    kpis: [
      { k: 'itens', n: 'Itens na lista', ic: 'lista', cor: 'var(--c4)' }, { k: 'cesta', n: 'Custo da cesta hoje', ic: 'sacola', cor: 'var(--c1)' },
      { k: 'oport', n: 'Prontos para comprar', ic: 'alvo', cor: 'var(--good)' }, { k: 'minimo', n: 'Cesta no menor preço', ic: 'queda', cor: 'var(--c2)' },
    ],
    valores(c) {
      const I = c.I, novos = c.des.filter(b => dentro(b.add, I.cur)).length, pr = p => c.des.filter(b => (b.prio || 0) === p).length;
      const comRes = c.des.filter(b => c.px(b).res), min = soma(comRes, b => c.px(b).res.min), hoje = soma(comRes, b => c.px(b).res.fim);
      return {
        itens: { v: c.des.length, tend: c.des.some(b => b.add != null) ? tendAbs(novos, 'neutro') : null, cmp: c.des.some(b => b.add != null) ? `${novos === 1 ? 'incluído' : 'incluídos'} ${I.cmpC}` : '', sub: `${fInt(pr(1))} alta · ${fInt(pr(2))} média · ${fInt(pr(3))} baixa` },
        cesta: K.cesta(c), oport: K.oport(c),
        minimo: comRes.length ? { v: min, fmt: fBRL0, cmp: `menor preço de cada item ${I.tudo ? 'no histórico' : I.rot}`, sub: hoje - min > 0.5 ? `${fBRL0(hoje - min)} abaixo do custo de hoje` : 'igual ao custo de hoje' } : { txt: '—', sub: 'sem cotações no período' },
      };
    },
    paineis: () => [pCesta('p-8', 'cesta-lista'), pPrioridade(), pDistancia(), pLojasBaratas()],
  },
  precos: {
    kpis: [
      { k: 'monit', n: 'Itens acompanhados', ic: 'sino', cor: 'var(--c4)' }, { k: 'oport', n: 'Abaixo do preço-alvo', ic: 'alvo', cor: 'var(--good)' },
      { k: 'queda', n: 'Maior queda', ic: 'queda', cor: 'var(--c2)' }, { k: 'cot', n: 'Cotações registradas', ic: 'etiqueta', cor: 'var(--c1)' },
    ],
    valores(c) {
      const I = c.I, nDes = c.rast.filter(b => b.col === 'desejo').length, lojas = new Set();
      let n = 0, meus = 0, ult = null;
      for (const b of c.rast) for (const f in b.px) { lojas.add(f); for (const p of b.px[f]) { if (p[0] >= c.pxDe && p[0] <= I.ate) { n++; if (p[2]) meus++; } if (p[0] <= I.ate && (ult == null || p[0] > ult)) ult = p[0]; } }
      const quedas = c.rast.map(b => ({ b, r: c.px(b).res })).filter(o => o.r && o.r.var < -0.0005).sort((a, z) => a.r.var - z.r.var), q = quedas[0];
      return {
        monit: c.rast.length ? { v: c.rast.length, cmp: `em ${plural(lojas.size, 'loja', 'lojas')}`, sub: `${fInt(nDes)} da lista · ${fInt(c.rast.length - nDes)} só monitorados` } : { v: 0, sub: 'nenhum livro com cotação' },
        oport: K.oport(c, c.rast),
        queda: q ? { txt: fPct(q.r.var, true), cmp: `${fBRL(q.r.ini)} → ${fBRL(q.r.fim)}`, sub: q.b.t, dica: q.b.t } : { txt: '—', sub: c.rast.length ? 'nenhum item ficou mais barato no período' : 'sem itens acompanhados' },
        cot: { v: n, cmp: I.tudo ? 'em todo o histórico' : I.rot, sub: ult != null ? `${meus ? fInt(meus) + (meus === 1 ? ' sua' : ' suas') : 'nenhuma sua'} · última em ${fDiaMes(ult)}` : 'nenhuma cotação ainda' },
      };
    },
    paineis: () => [pPrecoLoja(), pAlertas(), pVariacao(), pCotacao()],
  },
};
