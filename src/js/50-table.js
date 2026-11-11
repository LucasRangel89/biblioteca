/* ───────────────────────── tabela ordenável e filtrável ───────────────────────── */
const numCsv = v => (v == null || isNaN(v) ? '' : String(Math.round(v * 100) / 100).replace('.', ','));
const mudo = '<span class="mudo">—</span>';
// formato de um livro; no acervo, os dois ícones quando há o livro na estante e na biblioteca virtual
const fmtHtml = (b, t = 14) => { const fs = b.col === 'acervo' ? formatosDe(b) : b.fmt ? [b.fmt] : []; return fs.length ? `<span class="fmt">${fs.map(f => icone(ICONE_FMT[f] || 'livro', t)).join('')}${rotuloFmt(b)}</span>` : mudo; };
// a estrela de prioridade nunca fica sozinha em uma linha: anda junto com a última palavra do título
function tituloTop(b) {
  if (!b._top) return esc(b.t);
  const i = b.t.lastIndexOf(' '), est = `<i class="top" title="Prioridade (#top)">${icone('estrela', 12)}</i>`;
  return `${i > 0 ? esc(b.t.slice(0, i)) + ' ' : ''}<span class="nq">${esc(b.t.slice(i + 1))}${est}</span>`;
}
// temas de um livro: ficam de fora os marcadores de estrutura, as pendências, as camadas curatoriais (têm lugar próprio na ficha) e as marcas do usuário
const tagsTema = b => b.tags.filter(t => !TAGS_ESTRUTURA.has(t) && t !== 'verificar' && t !== 'sem-pt' && t !== TAG_ANALISE && !ehCamada(t));
const notaHtml = b => (temAnotacao(b) ? `<i class="tem-nota" title="${b.tags.includes(TAG_ANALISE) ? 'Possui análise' : 'Tem anotações suas'}">${icone(b.tags.includes(TAG_ANALISE) ? 'clipe' : 'nota', 12)}</i>` : '');
const ultCotacao = b => { let u = null; if (b.px) for (const f in b.px) { const p = b.px[f]; if (p.length && (u == null || p[p.length - 1][0] > u)) u = p[p.length - 1][0]; } return u; };
const ORD_LEIT = { lendo: 0, fila: 1, lido: 2, aband: 3, '': 4 }, ORD_SIT = { agora: 0, quase: 1, aguardar: 2, semalvo: 3, sem: 4 }, ORD_COL = { acervo: 0, desejo: 1, rec: 2 };

const COLS = {
  titulo: { n: 'Título', cls: 'c-tit', ord: b => norm(b.t), csv: b => b.t,
    html: b => `<span class="tt-c">${capaHtml(b)}<span class="tt" title="${esc(b.t)}"><b>${tituloTop(b)}</b><span>${esc(b.a || 'Autor não informado')}${notaHtml(b)}</span></span></span>` },
  autor: { n: 'Autor', oculto: true, csv: b => b.a },
  lista: { n: 'Lista', ord: b => ORD_COL[b.col], csv: b => COLECOES[b.col].n, html: b => `<span class="pill col-${b.col}">${COLECOES[b.col].n}</span>` },
  eixo: { n: 'Eixo', cls: 'c-eixo', ord: b => b.eixo, csv: b => (EIXOS[b.eixo] ? EIXOS[b.eixo].n : ''), html: b => (EIXOS[b.eixo] ? esc(EIXOS[b.eixo].n) : mudo) },
  tipo: { n: 'Tipo', ord: b => TIPOS[b._tipo].n, csv: b => TIPOS[b._tipo].n, html: b => TIPOS[b._tipo].n },
  fmt: { n: 'Formato', ord: b => rotuloFmt(b), csv: b => rotuloFmt(b), html: b => fmtHtml(b) },
  dif: { n: 'Dificuldade', ord: b => b._d || null, csv: b => (b._d ? NIVEIS[b._d].n : ''), html: b => (b._d ? `${pontos(b._d)}<span class="pt-r">${NIVEIS[b._d].n}</span>` : mudo) },
  ext: { n: 'Extensão', ord: b => b._e || null, csv: b => (b._e ? EXTENSOES[b._e].n : ''), html: b => (b._e ? `${pontos(b._e)}<span class="pt-r">${EXTENSOES[b._e].n}</span>` : mudo) },
  folego: { n: 'Dificuldade', ord: b => (b._d ? b._d * 10 + b._e : null), csv: b => (b._d ? NIVEIS[b._d].n : ''), dica: 'Dificuldade e extensão da leitura',
    html: b => (b._d || b._e ? `${b._d ? pontos(b._d) + '<span class="pt-r">' + NIVEIS[b._d].n + '</span>' : mudo}<span class="sub">${b._e ? 'extensão ' + EXTENSOES[b._e].n.toLowerCase() : 'extensão não informada'}</span>` : mudo) },
  extCsv: { n: 'Extensão', oculto: true, csv: b => (b._e ? EXTENSOES[b._e].n : '') },
  data: { n: 'Data', num: true, ord: b => dataDe(b), csv: b => iso(dataDe(b)), html: b => (dataDe(b) == null ? mudo : fData(dataDe(b))), dica: 'Aquisição (acervo) ou inclusão na lista' },
  adq: { n: 'Aquisição', num: true, dica: 'Data em que o livro entrou no acervo', ord: b => adqDe(b), csv: b => iso(adqDe(b)), html: b => (adqDe(b) == null ? mudo : fData(adqDe(b))) },
  add: { n: 'Inclusão', num: true, dica: 'Data em que o livro entrou na lista', ord: b => b.add, csv: b => iso(b.add), html: b => (b.add == null ? mudo : fData(b.add)) },
  origem: { n: 'Origem', ord: b => lojaDe(b) || '', csv: b => lojaDe(b) || '', html: b => (lojaDe(b) ? esc(b.loja) + (b.cond === 'usado' ? '<span class="sub">usado</span>' : '') : mudo) },
  cond: { n: 'Condição', ord: b => b.cond || '', csv: b => ({ novo: 'Novo', usado: 'Usado', presente: 'Presente' })[b.cond] || '', html: b => ({ novo: 'Novo', usado: 'Usado', presente: 'Presente' })[b.cond] || mudo },
  pago: { n: 'Pago', num: true, ord: b => pagoDe(b), csv: b => numCsv(pagoDe(b)), html: b => (pagoDe(b) == null ? mudo : pagoDe(b) === 0 ? `<span class="mudo">${b.cond === 'presente' ? 'presente' : 'gratuito'}</span>` : fBRL(b.pago)) },
  leit: { n: 'Leitura', ord: b => ORD_LEIT[b.leit], csv: b => (b.leit ? LEITURAS[b.leit].n : ''),
    html: b => (!b.leit ? mudo : `<span class="pill leit-${b.leit}">${LEITURAS[b.leit].n}${b.leit === 'lendo' || b.leit === 'aband' ? ` · ${b.prog || 0}%` : ''}</span>${b.leit === 'lido' && b.lidoEm != null ? `<span class="sub">${fData(b.lidoEm)}</span>` : ''}`) },
  nota: { n: 'Nota', ord: b => b.nota || null, csv: b => b.nota || '', html: b => (b.nota ? estrelas(b.nota) : mudo) },
  pg: { n: 'Páginas', num: true, ord: b => b.pg || null, csv: b => b.pg || '', html: b => (b.pg ? (b.demo ? '~' : '') + fInt(b.pg) : mudo) },
  tags: { n: 'Temas', cls: 'c-tags', csv: b => tagsTema(b).map(rotTag).join(', '), html: b => {
      const t = tagsTema(b); if (!t.length) return mudo;
      const chip = x => `<span class="tag">${esc(rotTag(x))}</span>`, v = t.slice(0, 2);
      // o "+N" nunca fica sozinho numa linha: anda junto com o último marcador
      return t.length > 2 ? `${v.slice(0, -1).map(chip).join('')}<span class="nq">${chip(v[v.length - 1])}<span class="tag mais" title="${esc(t.slice(2).map(rotTag).join(', '))}">+${t.length - 2}</span></span>` : v.map(chip).join('');
    } },
  pend: { n: 'Pendência', oculto: true, csv: b => ['sem-pt', 'verificar'].filter(t => b.tags.includes(t)).map(rotTag).join(', ') },
  camadas: { n: 'Camadas e trilhas', oculto: true, csv: b => b.tags.filter(ehCamada).map(rotTag).join(', ') },
  analise: { n: 'Possui análise', oculto: true, csv: b => (b.tags.includes(TAG_ANALISE) ? 'sim' : '') },
  coment: { n: 'Comentários', oculto: true, csv: b => b.com || '' },
  // ordem de compra sugerida (ver ordemDeCompra): posição entre as recomendações que ainda não tenho, com o motivo resumido
  compra: { n: 'Ordem de compra', cls: 'c-oc', dica: 'Ordem de compra sugerida entre as recomendações que ainda não tenho', ord: (b, c) => { const o = c.compra.de.get(b.id); return o ? o.pos : null; },
    csv: (b, c) => { const o = c.compra.de.get(b.id); return o ? o.pos : ''; },
    html: (b, c) => { const o = c.compra.de.get(b.id); return o ? `<b class="num">${o.pos}º</b><span class="sub" title="${esc(o.motivos.join(' · '))}">${esc(o.curtos.slice(0, 2).join(' · ') || '—')}</span>` : mudo; } },
  motivos: { n: 'Motivos da ordem', oculto: true, csv: (b, c) => { const o = c.compra.de.get(b.id); return o ? o.motivos.join(' · ') : ''; } },
  prio: { n: 'Prioridade', ord: b => b.prio || 9, csv: b => PRIORIDADES[b.prio || 0].n, html: b => `<span class="prio p${b.prio || 0}"><i></i>${PRIORIDADES[b.prio || 0].n}</span>` },
  melhor: { n: 'Melhor preço', num: true, ord: (b, c) => (c.px(b).hoje ? c.px(b).hoje.p : null), csv: (b, c) => numCsv(c.px(b).hoje ? c.px(b).hoje.p : null),
    html: (b, c) => { const h = c.px(b).hoje; return h ? `<b class="num">${fBRL(h.p)}</b><span class="sub">${esc(h.f)}</span>` : mudo; } },
  loja: { n: 'Loja', oculto: true, csv: (b, c) => (c.px(b).hoje ? c.px(b).hoje.f : '') },
  alvo: { n: 'Alvo', num: true, ord: b => b.alvo, csv: b => numCsv(b.alvo), html: b => (b.alvo ? fBRL(b.alvo) : mudo) },
  difAlvo: { n: 'vs. alvo', num: true, ord: (b, c) => (c.px(b).hoje && b.alvo ? c.px(b).hoje.p / b.alvo - 1 : null), csv: (b, c) => numCsv(c.px(b).hoje && b.alvo ? (c.px(b).hoje.p / b.alvo - 1) * 100 : null),
    html: (b, c) => varHtml(c.px(b).hoje && b.alvo ? c.px(b).hoje.p / b.alvo - 1 : null), dica: 'Melhor preço de hoje em relação ao preço-alvo' },
  min: { n: 'Mín. no período', num: true, ord: (b, c) => (c.px(b).res ? c.px(b).res.min : null), csv: (b, c) => numCsv(c.px(b).res ? c.px(b).res.min : null),
    html: (b, c) => { const r = c.px(b).res; return r ? `${fBRL(r.min)}<span class="sub">${fDiaMes(r.minDia)} · ${esc(r.minFonte)}</span>` : mudo; } },
  faixa: { n: 'Faixa no período', num: true, ord: (b, c) => (c.px(b).res ? c.px(b).res.min : null), dica: 'Menor e maior valor do melhor preço no período',
    html: (b, c) => { const r = c.px(b).res; return r ? `${fBRL(r.min)} – ${fBRL(r.max)}<span class="sub">mín. ${fDiaMes(r.minDia)} · ${esc(r.minFonte)}</span>` : mudo; } },
  minCsv: { n: 'Mínimo no período', oculto: true, csv: (b, c) => numCsv(c.px(b).res ? c.px(b).res.min : null) },
  maxCsv: { n: 'Máximo no período', oculto: true, csv: (b, c) => numCsv(c.px(b).res ? c.px(b).res.max : null) },
  max: { n: 'Máx.', num: true, ord: (b, c) => (c.px(b).res ? c.px(b).res.max : null), csv: (b, c) => numCsv(c.px(b).res ? c.px(b).res.max : null), html: (b, c) => (c.px(b).res ? fBRL(c.px(b).res.max) : mudo) },
  varP: { n: 'Variação', num: true, ord: (b, c) => (c.px(b).res ? c.px(b).res.var : null), csv: (b, c) => numCsv(c.px(b).res ? c.px(b).res.var * 100 : null), html: (b, c) => varHtml(c.px(b).res ? c.px(b).res.var : null), dica: 'Variação do melhor preço no período' },
  spark: { n: 'Tendência', cls: 'c-spark', html: (b, c) => { const r = c.px(b).res; return r ? spark(amostra(r.serie, r.de, r.ate, 24), { w: 84, h: 26, cor: SITUACOES[c.px(b).sit].cor, area: false }) : mudo; } },
  sit: { n: 'Situação', ord: (b, c) => ORD_SIT[c.px(b).sit], csv: (b, c) => SITUACOES[c.px(b).sit].n, html: (b, c) => badgeSit(c.px(b).sit) },
  ult: { n: 'Atualizado', num: true, dica: 'Data da última cotação registrada', ord: b => ultCotacao(b), csv: b => iso(ultCotacao(b)), html: (b, c) => { const u = ultCotacao(b); if (u == null) return mudo; const n = c.T - u; return `${fData(u)}<span class="sub">${n <= 0 ? 'hoje' : n === 1 ? 'ontem' : 'há ' + plural(n, 'dia', 'dias')}</span>`; } },
  valor: { n: 'Valor', num: true, ord: (b, c) => (b.col === 'acervo' ? pagoDe(b) : c.px(b).hoje ? c.px(b).hoje.p : null), csv: (b, c) => numCsv(b.col === 'acervo' ? pagoDe(b) : c.px(b).hoje ? c.px(b).hoje.p : null), dica: 'Valor pago (acervo) ou melhor preço de hoje (itens acompanhados)',
    html: (b, c) => { if (b.col === 'acervo') return pagoDe(b) == null ? mudo : pagoDe(b) === 0 ? `<span class="mudo">${b.cond === 'presente' ? 'presente' : 'gratuito'}</span>` : `${fBRL(b.pago)}<span class="sub">pago</span>`; const h = c.px(b).hoje; return h ? `${fBRL(h.p)}<span class="sub">melhor preço</span>` : mudo; } },
};

/* red: colunas de que a tabela abre mão quando aperta (2 sai primeiro, 4 por último); continuam na gaveta e no CSV.
   mob: como cada coluna aparece quando as linhas viram cartões (b = selo no canto, x = oculta, s = largura em sextos). */
const TABELAS = {
  geral: { tit: 'Todos os livros', cols: ['titulo', 'autor', 'lista', 'eixo', 'tipo', 'fmt', 'folego', 'extCsv', 'leit', 'data', 'camadas', 'analise', 'coment'], ord: 'data', dir: -1, linhas: c => c.acP.concat(c.des, c.recP), mob: { b: 'lista', x: ['tipo', 'folego'], s: { eixo: 4 } }, red: { fmt: 3, tipo: 4 },
    abas: [['todos', 'Todos'], ['acervo', 'Acervo', b => b.col === 'acervo'], ['desejo', 'Próximas aquisições', b => b.col === 'desejo'], ['rec', 'Recomendações', b => b.col === 'rec'], ['notas', 'Com anotações', b => temAnotacao(b)], ['meus', 'Editados por você', b => !!b.u]] },
  biblioteca: { tit: 'Livros do acervo', cols: ['titulo', 'autor', 'fmt', 'eixo', 'adq', 'origem', 'leit', 'nota', 'pg', 'analise', 'coment'], ord: 'adq', dir: -1, linhas: c => c.acP, mob: { b: 'leit', x: ['eixo', 'pg'] }, red: { pg: 2, nota: 3, origem: 4 },
    abas: [['todos', 'Todos'], ['lendo', 'Lendo', b => b.leit === 'lendo'], ['fila', 'Na fila', b => b.leit === 'fila' || b.leit === ''], ['lido', 'Lidos', b => b.leit === 'lido'], ['aband', 'Abandonados', b => b.leit === 'aband'], ['notas', 'Com anotações', b => temAnotacao(b)]] },
  recs: { tit: 'Lista de recomendações', cols: ['titulo', 'autor', 'compra', 'motivos', 'eixo', 'tipo', 'dif', 'ext', 'tags', 'pend', 'camadas', 'analise', 'coment', 'add'], ord: 'eixo', dir: 1, linhas: c => c.recP, mob: { x: ['tipo', 'add'], s: { eixo: 4, tags: 4 } }, red: { add: 2, tipo: 3, ext: 4 },
    // as abas temáticas contam só a fila (o que ainda não foi lido), como os indicadores do topo; as lidas têm aba própria
    abas: [['todos', 'Todas'], ['top', 'Prioridades', b => b._top && b.leit !== 'lido'], ['leves', 'Leves e curtas', b => b._d === 1 && b._e === 1 && b.leit !== 'lido'], ['sempt', 'Sem edição em PT', b => b.tags.includes('sem-pt') && b.leit !== 'lido'], ['verif', 'A verificar', b => b.tags.includes('verificar') && b.leit !== 'lido'], ['monit', 'Monitoradas', b => rastreado(b)], ['lidos', 'Já lidas', b => b.leit === 'lido']] },
  // Finanças: só os livros do acervo com alguma informação de compra (valor ou origem); valores não aparecem nas outras tabelas
  financas: { tit: 'Compras registradas', cols: ['titulo', 'autor', 'fmt', 'adq', 'origem', 'cond', 'pago'], ord: 'pago', dir: -1, linhas: c => c.acP.filter(b => pagoDe(b) != null || !!lojaDe(b)), mob: { x: ['fmt'] }, red: { fmt: 3, cond: 4 },
    vazio: 'Nenhuma compra registrada ainda. Para registrar, abra um livro do acervo e use “Editar”: valor pago, loja e data são opcionais — preencha só o que souber.',
    abas: [['todos', 'Todas'], ['pagas', 'Com valor', b => pagoDe(b) > 0], ['gratis', 'Presentes e gratuitos', b => pagoDe(b) === 0], ['semvalor', 'Sem valor', b => pagoDe(b) == null]] },
  desejos: { tit: 'Lista de próximas aquisições', cols: ['titulo', 'autor', 'prio', 'fmt', 'melhor', 'loja', 'alvo', 'difAlvo', 'min', 'spark', 'sit'], ord: 'difAlvo', dir: 1, linhas: c => c.des, mob: { b: 'sit', x: ['fmt'], s: { min: 4 } }, red: { fmt: 2, spark: 3, min: 4 },
    vazio: 'A lista está vazia. Para pôr um livro aqui, use o botão da sacola em “O que comprar primeiro”, logo acima, ou abra uma recomendação e use “Quero comprar”.',
    abas: [['todos', 'Todos'], ['agora', 'Comprar agora', (b, c) => c.px(b).sit === 'agora'], ['quase', 'Quase lá', (b, c) => c.px(b).sit === 'quase'], ['aguardar', 'Aguardar', (b, c) => !['agora', 'quase'].includes(c.px(b).sit)]] },
  precos: { tit: 'Itens acompanhados', cols: ['titulo', 'autor', 'lista', 'melhor', 'loja', 'alvo', 'varP', 'faixa', 'minCsv', 'maxCsv', 'sit', 'ult'], ord: 'varP', dir: 1, linhas: c => c.rast, mob: { b: 'sit', x: ['lista', 'ult'], s: { faixa: 6 } }, red: { lista: 2, ult: 4 },
    vazio: 'Nenhum preço acompanhado ainda. Os preços entram pelas cotações que você registra: abra uma recomendação e use “Monitorar preço”.',
    abas: [['todos', 'Todos'], ['desejo', 'Lista de compra', b => b.col === 'desejo'], ['monit', 'Só monitorados', b => b.col !== 'desejo'], ['queda', 'Em queda', (b, c) => c.px(b).res && c.px(b).res.var < -0.005], ['alta', 'Em alta', (b, c) => c.px(b).res && c.px(b).res.var > 0.005]] },
};

function Tabela(visao) {
  const cfg = TABELAS[visao], k = cartao({ id: 'tab-' + visao, w: 'p-12 card-tab', tit: cfg.tit });
  const estreita = !!window.matchMedia && matchMedia('(max-width: 700px)').matches, mob = cfg.mob || {};
  const st = S.tab[visao] = Object.assign({ aba: 'todos', q: '', ord: cfg.ord, dir: cfg.dir, pag: 0, tam: estreita ? 10 : 25 }, S.tab[visao]);
  const cols = cfg.cols.map(id => Object.assign({ id }, COLS[id])), vis = cols.filter(x => !x.oculto);
  for (const x of vis) x.mcls = (x.id === mob.b ? ' m-b' : (mob.x || []).includes(x.id) ? ' m-x' : mob.s && mob.s[x.id] ? ' m-' + mob.s[x.id] : '') + (cfg.red && cfg.red[x.id] ? ' r-' + cfg.red[x.id] : '');
  k.tools.innerHTML = `<label class="busca-t">${icone('busca', 15)}<input type="search" placeholder="Filtrar por título, autor ou tema" aria-label="Filtrar a tabela" value="${esc(st.q)}"></label>
    <label class="ord-m"><span>Ordenar</span><select aria-label="Ordenar por">${vis.filter(x => x.ord).map(x => `<option value="${x.id}">${esc(x.n)}</option>`).join('')}</select><button type="button" class="ib" data-dir aria-label="Inverter a ordem">${icone('cima', 15)}</button></label>
    <button type="button" class="btn sm" data-csv title="Exportar as linhas filtradas em CSV">${icone('baixar', 15)}<span>CSV</span></button>`;
  k.corpo.innerHTML = `<div class="abas" role="tablist" aria-label="Recortes rápidos"></div>
    <div class="tb-w"><table class="tb"><thead><tr>${vis.map(x => `<th scope="col" class="${x.num ? 'num ' : ''}${x.cls || ''}${cfg.red && cfg.red[x.id] ? ' r-' + cfg.red[x.id] : ''}" data-c="${x.id}"${x.dica ? ` title="${esc(x.dica)}"` : ''}>${x.ord ? `<button type="button">${esc(x.n)}<span class="so">${icone('cima', 12)}</span></button>` : esc(x.n)}</th>`).join('')}</tr></thead><tbody></tbody></table><div class="ch-vazio" hidden></div></div>`;
  k.pe.className = 'card-f tb-pe';
  k.pe.innerHTML = `<span class="tb-info"></span><div class="pag"><label class="tam"><span>por página</span><select aria-label="Linhas por página">${[10, 25, 50, 100].map(n => `<option${n === st.tam ? ' selected' : ''}>${n}</option>`).join('')}</select></label><button type="button" class="ib" data-p="-1" aria-label="Página anterior">${icone('esq', 16)}</button><span class="pag-n"></span><button type="button" class="ib" data-p="1" aria-label="Próxima página">${icone('dir', 16)}</button></div>`;
  const abasEl = $('.abas', k.corpo), tbody = $('tbody', k.corpo), vazio = $('.ch-vazio', k.corpo), busca = $('input[type=search]', k.tools), ordSel = $('.ord-m select', k.tools);
  let ctx = null, base = [], filtradas = [];

  function desenhar() {
    if (!ctx) return;
    const q = norm(st.q.trim()), termos = q ? q.split(/\s+/) : [];
    const porBusca = termos.length ? base.filter(b => termos.every(t => b._busca.includes(t))) : base;
    if (!cfg.abas.some(a => a[0] === st.aba)) st.aba = 'todos';
    setHtml(abasEl, cfg.abas.map(([id, n, f]) => { const qt = f ? porBusca.filter(b => f(b, ctx)).length : porBusca.length; return `<button type="button" role="tab" data-a="${id}" aria-selected="${st.aba === id}"${qt === 0 && st.aba !== id ? ' class="zero"' : ''}>${esc(n)}<span class="cont">${fInt(qt)}</span></button>`; }).join(''));
    const aba = cfg.abas.find(a => a[0] === st.aba);
    filtradas = aba[2] ? porBusca.filter(b => aba[2](b, ctx)) : porBusca.slice();
    const col = cols.find(x => x.id === st.ord && x.ord) || cols[0], nulo = v => v == null || v === '' || (typeof v === 'number' && isNaN(v));
    const chaves = new Map(filtradas.map(b => [b, col.ord(b, ctx)]));
    filtradas.sort((a, z) => {
      const x = chaves.get(a), y = chaves.get(z);
      if (nulo(x) || nulo(y)) return (nulo(x) ? 1 : 0) - (nulo(y) ? 1 : 0) || a._busca.localeCompare(z._busca);
      return ((typeof x === 'string' ? x.localeCompare(y, 'pt-BR') : x - y) * st.dir) || a._busca.localeCompare(z._busca);
    });
    const total = filtradas.length, pags = Math.max(1, Math.ceil(total / st.tam));
    st.pag = clamp(st.pag, 0, pags - 1);
    const fatia = filtradas.slice(st.pag * st.tam, (st.pag + 1) * st.tam);
    setHtml(tbody, fatia.map(b => `<tr data-id="${b.id}" tabindex="0"${mob.b ? ' class="tem-b"' : ''}>${vis.map(x => { const h = x.html(b, ctx); return `<td class="${x.num ? 'num ' : ''}${x.cls || ''}${x.mcls}${h === mudo ? ' vz' : ''}" data-rot="${esc(x.n)}">${h}</td>`; }).join('')}</tr>`).join(''));
    vazio.hidden = total > 0; $('table', k.corpo).style.display = total ? '' : 'none';
    if (!total) {
      // se o que caberia aqui está oculto ("Ocultar", na barra de filtros), é isso que a lista vazia tem de dizer
      const oc = FORA.n ? cfg.linhas(ctx.comOcultos).filter(b => oculto(b) && termos.every(t => b._busca.includes(t)) && (!aba[2] || aba[2](b, ctx))).length : 0;
      vazio.innerHTML = vazioHtml(oc ? (oc === 1 ? 'O único livro que caberia aqui está oculto. Para vê-lo' : `Os ${fInt(oc)} livros que caberiam aqui estão ocultos. Para vê-los`) + ', use “Ocultar”, na barra de filtros.'
        : base.length ? 'Nenhuma linha combina com a busca ou a aba escolhida.' : cfg.vazio && !nFiltros() ? cfg.vazio : ctx.I.tudo ? 'Nenhum livro com os filtros atuais.' : 'Nada neste período com os filtros atuais. Itens sem data só aparecem em “Tudo”.');
      vazio.dataset.ocultos = oc;
    }
    $$('th', k.corpo).forEach(th => { const on = th.dataset.c === col.id; th.setAttribute('aria-sort', on ? (st.dir > 0 ? 'ascending' : 'descending') : 'none'); th.classList.toggle('ord', on); th.classList.toggle('desc', on && st.dir < 0); });
    ordSel.value = col.id; $('[data-dir]', k.tools).classList.toggle('desc', st.dir < 0);
    $('.tb-info', k.pe).textContent = total ? `${fInt(st.pag * st.tam + 1)}–${fInt(Math.min(total, (st.pag + 1) * st.tam))} de ${plural(total, 'livro', 'livros')}${total !== base.length ? ` (de ${fInt(base.length)} no recorte)` : ''}` : 'Nenhum livro';
    $('.pag-n', k.pe).textContent = `${st.pag + 1} / ${pags}`;
    $('[data-p="-1"]', k.pe).disabled = st.pag <= 0; $('[data-p="1"]', k.pe).disabled = st.pag >= pags - 1;
    k.sub.textContent = cfg.sub ? cfg.sub(ctx) : `Clique numa linha para abrir o livro · ${ctx.I.tudo ? 'todo o histórico' : ctx.I.rot}`;
  }
  const ordenarPor = id => { if (st.ord === id) st.dir = -st.dir; else { st.ord = id; st.dir = COLS[id].num ? -1 : 1; } st.pag = 0; desenhar(); };
  abasEl.addEventListener('click', e => { const b = e.target.closest('[data-a]'); if (!b) return; st.aba = b.dataset.a; st.pag = 0; desenhar(); });
  busca.addEventListener('input', debounce(() => { st.q = busca.value; st.pag = 0; desenhar(); }, 120));
  $('thead', k.corpo).addEventListener('click', e => { const th = e.target.closest('th'); if (th && e.target.closest('button')) ordenarPor(th.dataset.c); });
  ordSel.addEventListener('change', () => { st.ord = ordSel.value; st.dir = COLS[st.ord].num ? -1 : 1; st.pag = 0; desenhar(); });
  $('[data-dir]', k.tools).addEventListener('click', () => { st.dir = -st.dir; st.pag = 0; desenhar(); });
  k.pe.addEventListener('click', e => { const b = e.target.closest('[data-p]'); if (!b || b.disabled) return; st.pag += +b.dataset.p; desenhar(); k.el.scrollIntoView({ block: 'nearest' }); });
  $('.tam select', k.pe).addEventListener('change', e => { st.tam = +e.target.value; st.pag = 0; salvar(); desenhar(); });
  tbody.addEventListener('click', e => { const tr = e.target.closest('tr[data-id]'); if (tr) abrirLivro(tr.dataset.id); });
  tbody.addEventListener('keydown', e => { if (e.key !== 'Enter' && e.key !== ' ') return; const tr = e.target.closest('tr[data-id]'); if (tr) { e.preventDefault(); abrirLivro(tr.dataset.id); } });
  $('[data-csv]', k.tools).addEventListener('click', () => {
    if (!filtradas.length) { toast('Não há linhas para exportar.', 'aviso'); return; }
    const cs = cols.filter(x => x.csv), cel = v => { const s = String(v ?? ''); return /[";\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s; };
    const txt = '\ufeff' + [cs.map(x => cel(x.n)).join(';')].concat(filtradas.map(b => cs.map(x => cel(x.csv(b, ctx))).join(';'))).join('\r\n');
    baixarArquivo(`biblioteca-${visao}-${iso(DB.hoje)}.csv`, txt, 'text/csv;charset=utf-8');
  });
  return { el: k.el, atualizar(c) { ctx = c; base = cfg.linhas(c); desenhar(); } };
}
