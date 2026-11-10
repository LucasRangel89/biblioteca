/* ───────────────────────── casca, filtros e inicialização ───────────────────────── */
const REG = {};
let CTX = null, pendente = 0;
const ctxAtual = () => CTX || (CTX = contexto());
const cfgAtual = () => ({ tema: S.tema, ocultar: S.ocultar, avisoVisto: S.avisoVisto, visao: S.visao, ui: S.ui, tam: Object.fromEntries(Object.entries(S.tab).map(([k, v]) => [k, v.tam])) });
const salvar = debounce(() => { const ok = Loja.gravar(serializar(cfgAtual())); pintarStatus(ok); }, 350);

function montarVisao(v) {
  const sec = $('#v-' + v), def = VIS[v];
  const kp = document.createElement('div'); kp.className = 'kpis k' + def.kpis.length; sec.appendChild(kp);
  const grade = document.createElement('div'); grade.className = 'grade'; sec.appendChild(grade);
  const reg = { kpis: Kpis(kp, def.kpis), at: [] };
  for (const p of def.paineis()) { const k = cartao(p); grade.appendChild(k.el); reg.at.push(p.montar(k)); }
  const t = Tabela(v); grade.appendChild(t.el); reg.at.push(c => t.atualizar(c));
  REG[v] = reg;
}
function render() {
  const v = S.visao; if (!REG[v]) montarVisao(v);
  const c = CTX = contexto();
  REG[v].kpis(VIS[v].valores(c));
  for (const f of REG[v].at) f(c);
  pintarCasca(c);
  $$('.rolavel', $('#v-' + v)).forEach(marcarRolagem);
}
// listas com rolagem interna: esmaece a base enquanto houver mais itens abaixo
function marcarRolagem(el) { const rola = el.scrollHeight > el.clientHeight + 4; el.classList.toggle('rola', rola); el.classList.toggle('fim', !rola || el.scrollTop + el.clientHeight >= el.scrollHeight - 6); }
function filtrosMudaram() { sincronizarFiltros(); render(); if (Gaveta.id) desenharGaveta(); }
function irPara(v, inicial) {
  if (!VISOES[v]) v = 'geral';
  S.visao = v;
  $$('.visao').forEach(s => { s.hidden = s.id !== 'v-' + v; });
  $$('[data-ir]', $('#nav')).concat($$('[data-ir]', $('#nav-m'))).forEach(b => { if (b.dataset.ir === v) b.setAttribute('aria-current', 'page'); else b.removeAttribute('aria-current'); });
  $('#titulo').innerHTML = `<span class="t-l">${esc(VISOES[v].n)}</span><span class="t-c">${esc(v === 'desejos' ? 'Aquisições' : VISOES[v].n)}</span>`; $('#descricao').textContent = VISOES[v].d;
  document.title = `${VISOES[v].n} · Biblioteca do Lucas`;
  $('#filtros').classList.toggle('sem-acervo', v === 'recs');
  sincronizarFiltros(); render();
  if (!inicial) { window.scrollTo(0, 0); const sec = $('#v-' + v); sec.classList.remove('entra'); void sec.offsetWidth; sec.classList.add('entra'); salvar(); }
}

/* ───────── barra de filtros ───────── */
function montarFiltros() {
  const seg = (id, rot, ops) => `<div class="seg" id="${id}" role="group" aria-label="${rot}">${ops.map(([v, n]) => `<button type="button" data-v="${v}">${n}</button>`).join('')}</div>`;
  const chips = (grupo, ops) => `<div class="chips" data-grupo="${grupo}">${ops.map(([v, n, d]) => `<button type="button" class="chip" data-v="${v}"${d ? ` title="${d}"` : ''}>${n}</button>`).join('')}</div>`;
  $('#filtros').innerHTML = `
    <div class="f-linha">
      <div class="f-per">${seg('f-periodo', 'Período', PERIODOS)}<button type="button" class="btn f-cal" id="f-cal" aria-expanded="false" title="Período personalizado">${icone('calendario', 15)}<span id="f-cal-r">Personalizar</span></button></div>
      <button type="button" class="btn f-abrir" id="f-abrir">${icone('filtro', 15)}Filtros<span class="cont" id="f-n" hidden></span></button>
      <div class="f-painel" id="f-painel">
        <div class="f-ph"><b>Filtros</b><button type="button" class="ib" data-fechar-folha aria-label="Fechar filtros">${icone('fechar')}</button></div>
        <div class="f-corpo">
          <div class="f-g f-custom" id="f-custom" hidden><span class="f-r">Período</span><label><span>de</span><input type="date" id="f-de" aria-label="Data inicial"></label><label><span>até</span><input type="date" id="f-ate" aria-label="Data final"></label></div>
          <div class="f-g" data-g="acervo"><span class="f-r">Acervo</span>${seg('f-acervo', 'Acervo', [['tudo', 'Tudo'], ['fisico', 'Física'], ['virtual', 'Virtual']])}</div>
          <div class="f-g"><span class="f-r">Tipo</span>${seg('f-tipo', 'Tipo', [['', 'Todos'], ['F', 'Ficção'], ['NF', 'Não ficção'], ['O', 'Outros']])}</div>
          <div class="f-g pop-w" id="pw-eixo"><button type="button" class="btn pop-b" aria-expanded="false" aria-controls="pop-eixo">Eixo<span class="cont" hidden></span>${icone('baixo', 14)}</button>
            <div class="pop" id="pop-eixo"><div class="pop-h"><b>Eixo temático</b><button type="button" class="lk" data-limpar="eixos">limpar</button></div><div class="pop-l">${EIXOS.slice(1).map((e, i) => `<label class="opt"><input type="checkbox" value="${i + 1}"><span>${esc(e.n)}</span><em></em></label>`).join('')}</div></div></div>
          <div class="f-g pop-w" id="pw-mais"><button type="button" class="btn pop-b" aria-expanded="false" aria-controls="pop-mais">${icone('filtro', 14)}Mais filtros<span class="cont" hidden></span>${icone('baixo', 14)}</button>
            <div class="pop largo" id="pop-mais"><div class="pop-h"><b>Mais filtros</b><button type="button" class="lk" data-limpar="mais">limpar</button></div>
              <div class="pop-l"><label class="opt so"><input type="checkbox" id="f-top"><span>${icone('estrela', 13)} Só prioridades (#top)</span></label>
              <span class="pop-r">Dificuldade</span>${chips('dif', [1, 2, 3].map(d => [d, NIVEIS[d].n]))}
              <span class="pop-r">Extensão</span>${chips('ext', [1, 2, 3].map(e => [e, EXTENSOES[e].n, EXTENSOES[e].d]))}
              <label class="busca-t pop-q">${icone('busca', 14)}<input type="search" id="f-tagq" placeholder="Procurar marcador" aria-label="Procurar marcador"></label>
              <div id="f-tags">${GRUPOS_TAG.map(([n, lista]) => `<div class="tg-g"><span class="pop-r">${n}</span>${chips('tags', lista.map(t => [t, maiuscula(rotTag(t)), '#' + t]))}</div>`).join('')}</div></div></div></div>
        </div>
        <div class="f-pf"><button type="button" class="btn" data-limpar="tudo">Limpar tudo</button><button type="button" class="btn pri" data-fechar-folha id="f-ver">Ver resultados</button></div>
      </div>
    </div>
    <div class="f-ativos" id="f-ativos" hidden></div>`;
  const F = $('#filtros');
  $('#f-periodo').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; S.periodo = b.dataset.v; $('#f-custom').hidden = true; filtrosMudaram(); });
  $('#f-cal').addEventListener('click', () => {
    const cx = $('#f-custom'), abrir = cx.hidden;
    if (abrir) { if (S.de == null || S.ate == null) { const I = intervalo(); S.de = S.periodo === 'tudo' ? DB.hoje - 179 : I.de; S.ate = I.ate; } S.periodo = 'custom'; if (matchMedia('(max-width: 820px)').matches) folha(true, true); }
    else if (S.periodo === 'custom') S.periodo = 'tudo';
    cx.hidden = !abrir; filtrosMudaram(); if (abrir) $('#f-de').focus();
  });
  for (const id of ['f-de', 'f-ate']) $('#' + id).addEventListener('change', () => { let de = deIso($('#f-de').value), ate = deIso($('#f-ate').value); if (de == null || ate == null) return; if (de > ate) [de, ate] = [ate, de]; S.de = Math.min(de, DB.hoje); S.ate = Math.min(ate, DB.hoje); S.periodo = 'custom'; filtrosMudaram(); });
  $('#f-acervo').addEventListener('click', e => { const b = e.target.closest('button'); if (b) { S.acervo = b.dataset.v; filtrosMudaram(); } });
  $('#f-tipo').addEventListener('click', e => { const b = e.target.closest('button'); if (b) { S.tipo = b.dataset.v; filtrosMudaram(); } });
  $('#pop-eixo').addEventListener('change', e => { if (e.target.matches('input[type=checkbox]')) { alternar(S.eixos, +e.target.value); filtrosMudaram(); } });
  $('#f-top').addEventListener('change', e => { S.top = e.target.checked; filtrosMudaram(); });
  $('#pop-mais').addEventListener('click', e => { const b = e.target.closest('.chip'); if (!b) return; const g = b.parentElement.dataset.grupo; alternar(S[g], g === 'tags' ? b.dataset.v : +b.dataset.v); filtrosMudaram(); });
  $('#f-tagq').addEventListener('input', e => { const q = norm(e.target.value.trim()); $$('#f-tags .chip').forEach(c => { c.hidden = !!q && !norm(c.textContent + ' ' + c.dataset.v).includes(q); }); $$('#f-tags .tg-g').forEach(g => { g.hidden = !$$('.chip', g).some(c => !c.hidden); }); });
  F.addEventListener('click', e => {
    const l = e.target.closest('[data-limpar]');
    if (l) { const x = l.dataset.limpar; if (x === 'eixos') S.eixos.clear(); else if (x === 'mais') { S.dif.clear(); S.ext.clear(); S.tags.clear(); S.top = false; } else { limparFiltros(true); $('#f-custom').hidden = true; } filtrosMudaram(); return; }
    const r = e.target.closest('[data-rm]');
    if (r) { const [g, v] = r.dataset.rm.split(':'); if (g === 'acervo') S.acervo = 'tudo'; else if (g === 'tipo') S.tipo = ''; else if (g === 'top') S.top = false; else if (g === 'periodo') { S.periodo = 'tudo'; $('#f-custom').hidden = true; } else if (g === 'tags') S.tags.delete(v); else S[g].delete(+v); filtrosMudaram(); return; }
    const pb = e.target.closest('.pop-b');
    if (pb) { const w = pb.parentElement, abrir = !w.classList.contains('aberto'); fecharPops(); if (abrir) { w.classList.add('aberto'); pb.setAttribute('aria-expanded', 'true'); } return; }
    if (e.target.closest('[data-fechar-folha]')) folha(false);
  });
  $('#f-abrir').addEventListener('click', () => folha(true));
  // se a janela alargar com a folha aberta (tablet girado, janela redimensionada), fecha: no layout largo ela não existe e a página ficaria travada
  if (window.matchMedia) { const mq = matchMedia('(max-width: 820px)'), f = () => { if (!mq.matches) folha(false); }; if (mq.addEventListener) mq.addEventListener('change', f); else if (mq.addListener) mq.addListener(f); }
  document.addEventListener('pointerdown', e => { if (!e.target.closest('.pop-w')) fecharPops(); if (F.classList.contains('folha') && !e.target.closest('#f-painel, #f-abrir, #f-cal')) folha(false); });
}
const fecharPops = () => $$('.pop-w.aberto').forEach(w => { w.classList.remove('aberto'); $('.pop-b', w).setAttribute('aria-expanded', 'false'); });
/* folha de filtros (telas estreitas): comporta-se como um diálogo — recebe o foco ao abrir, prende o Tab (ver 60-drawer) e devolve o foco ao fechar */
function folha(abrir, semFoco) {
  const F = $('#filtros'), P = $('#f-painel'), era = F.classList.contains('folha');
  F.classList.toggle('folha', abrir); travar();
  if (abrir === era) return;
  if (abrir) { P.setAttribute('role', 'dialog'); P.setAttribute('aria-modal', 'true'); P.setAttribute('aria-label', 'Filtros'); P.tabIndex = -1; if (!semFoco) focar(P, 3); }
  else { const dentro = P.contains(document.activeElement); for (const a of ['role', 'aria-modal', 'aria-label', 'tabindex']) P.removeAttribute(a); if (dentro) focar($('#f-abrir'), 0); }
}
function sincronizarFiltros() {
  const I = intervalo(), marca = (id, v) => $$('#' + id + ' button').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.v === v)));
  marca('f-periodo', S.periodo === 'custom' ? '__' : S.periodo); marca('f-acervo', S.acervo); marca('f-tipo', S.tipo);
  const custom = S.periodo === 'custom';
  $('#f-cal').setAttribute('aria-pressed', String(custom)); $('#f-cal').setAttribute('aria-expanded', String(!$('#f-custom').hidden));
  $('#f-cal-r').textContent = custom ? `${fDiaMesAno(I.de)} – ${fDiaMesAno(I.ate)}` : 'Personalizar';
  if (custom) $('#f-custom').hidden = false;
  $('#f-de').value = iso(S.de); $('#f-ate').value = iso(S.ate); $('#f-de').max = $('#f-ate').max = iso(DB.hoje);
  // contagens por eixo ignorando o próprio filtro de eixo
  const base = DB.livros.filter(b => passaSeg(b, { semEixo: true, semAcervo: S.visao === 'recs' })), porEixo = contarPor(base, b => b.eixo);
  $$('#pop-eixo .opt').forEach(o => { const inp = $('input', o), e = +inp.value; inp.checked = S.eixos.has(e); $('em', o).textContent = fInt(porEixo.get(e) || 0); });
  $('#f-top').checked = S.top;
  $$('#pop-mais .chip').forEach(c => { const g = c.parentElement.dataset.grupo; c.setAttribute('aria-pressed', String(S[g].has(g === 'tags' ? c.dataset.v : +c.dataset.v))); });
  const nMais = S.dif.size + S.ext.size + S.tags.size + (S.top ? 1 : 0), cont = (sel, n) => { const el = $(sel); el.hidden = !n; el.textContent = n; };
  cont('#pw-eixo .cont', S.eixos.size); cont('#pw-mais .cont', nMais); cont('#f-n', nFiltros() + (custom ? 1 : 0));
  $('#pw-eixo').classList.toggle('ativo', S.eixos.size > 0); $('#pw-mais').classList.toggle('ativo', nMais > 0);
  // chips dos filtros ativos
  const ch = [], add = (rm, txt) => ch.push(`<button type="button" class="ativo" data-rm="${esc(rm)}" title="Remover filtro">${esc(txt)}${icone('fechar', 12)}</button>`);
  if (custom) add('periodo:', `${fData(I.de)} – ${fData(I.ate)}`);
  if (S.acervo !== 'tudo' && S.visao !== 'recs') add('acervo:', S.acervo === 'fisico' ? 'Biblioteca física' : 'Biblioteca virtual');
  if (S.tipo) add('tipo:', { F: 'Ficção', NF: 'Não ficção', O: 'Poesia, HQ e outros' }[S.tipo]);
  for (const e of [...S.eixos].sort((a, z) => a - z)) add('eixos:' + e, EIXOS[e].n);
  if (S.top) add('top:', 'Só prioridades');
  for (const d of S.dif) add('dif:' + d, 'Dificuldade ' + NIVEIS[d].n.toLowerCase());
  for (const e of S.ext) add('ext:' + e, 'Extensão ' + EXTENSOES[e].n.toLowerCase());
  for (const t of S.tags) add('tags:' + t, '#' + rotTag(t));
  const el = $('#f-ativos'); el.hidden = !ch.length;
  setHtml(el, ch.length ? `<span class="fa-r">Filtros ativos</span>${ch.join('')}${ch.length > 1 ? '<button type="button" class="lk" data-limpar="tudo">limpar tudo</button>' : ''}` : '');
}

/* ───────── casca: navegação, cabeçalho, avisos ───────── */
function pintarStatus(ok) {
  const el = $('#st-dados'); if (!el) return;
  const bom = Loja.ok && ok !== false;
  el.className = 'st ' + (bom ? 'ok' : 'aviso');
  el.innerHTML = `<i></i><span><b>${bom ? 'Salvo neste navegador' : Loja.ok ? 'Não foi possível salvar' : 'Pré-visualização'}</b><em>${bom ? 'dados só neste dispositivo' : Loja.ok ? 'armazenamento cheio ou bloqueado' : 'alterações não são salvas'}</em></span>`;
  el.title = 'Seus dados: backup, importação e dados de exemplo';
}
function pintarCasca(c) {
  $('#b-exemplo').hidden = !DB.exemplos;
  const av = $('#aviso'), mostrar = DB.exemplos && !S.avisoVisto;
  av.hidden = !mostrar;
  if (mostrar) setHtml(av, `<span class="av-i">${icone('info', 18)}</span><div><b>Seu catálogo é real; o movimento é de exemplo.</b><p>Os ${fInt(DB.livros.filter(b => b.sec >= 0).length)} títulos, autores, marcadores, eixos e a estante física vieram do seu catálogo. Datas, valores pagos, e-books e audiolivros, leituras, a lista de próximas aquisições e os históricos de preço são <b>simulados</b> para dar vida aos gráficos, e os preços não vêm das lojas: entram por cotações que você registra.</p></div><div class="av-a"><button type="button" class="btn sm" data-av="dados">Gerenciar dados</button><button type="button" class="btn sm pri" data-av="ok">Entendi</button></div>`);
  $('#rodape-n').textContent = `${plural(DB.livros.length, 'livro', 'livros')} · ${c.I.tudo ? 'todo o histórico' : c.I.rot}${nFiltros() ? ' · ' + plural(nFiltros(), 'filtro ativo', 'filtros ativos') : ''}`;
}
function aplicarTema() {
  const t = S.tema || (window.matchMedia && matchMedia('(prefers-color-scheme: dark)').matches ? 'escuro' : 'claro');
  document.documentElement.dataset.tema = t;
  const b = $('#b-tema'); b.innerHTML = icone(t === 'escuro' ? 'sol' : 'lua'); b.setAttribute('aria-label', t === 'escuro' ? 'Usar tema claro' : 'Usar tema escuro'); b.title = b.getAttribute('aria-label');
  const m = $('meta[name="theme-color"]'); if (m) m.content = t === 'escuro' ? '#141310' : '#F5F3EE';
}
function aplicarOlho() {
  OCULTAR_VALORES = S.ocultar;
  const b = $('#b-olho'); b.innerHTML = icone(S.ocultar ? 'olhoOff' : 'olho'); b.setAttribute('aria-pressed', String(S.ocultar)); b.setAttribute('aria-label', S.ocultar ? 'Mostrar valores em reais' : 'Ocultar valores em reais'); b.title = b.getAttribute('aria-label');
}
function montarCasca() {
  const item = v => `<button type="button" data-ir="${v}">${icone(VISOES[v].ic, 19)}<span class="nv-l">${VISOES[v].n}</span><span class="nv-c">${VISOES[v].c}</span></button>`;
  $('#nav').innerHTML = ORDEM_VISOES.map(item).join(''); $('#nav-m').innerHTML = ORDEM_VISOES.map(item).join('');
  $('#b-dados').innerHTML = icone('dados'); $('#b-novo').innerHTML = icone('mais', 16) + '<span>Novo livro</span>';
  document.addEventListener('click', e => {
    const ir = e.target.closest('[data-ir]'); if (ir) { irPara(ir.dataset.ir); return; }
    const li = e.target.closest('.li[data-id]'); if (li) { abrirLivro(li.dataset.id); return; }
    const sl = e.target.closest('[data-sel]'); if (sl) { selecionarPreco(sl.dataset.sel); return; }
    const av = e.target.closest('[data-av]'); if (av) { if (av.dataset.av === 'ok') { S.avisoVisto = true; salvar(); pintarCasca(ctxAtual()); } else dlgDados(); }
  });
  $('#b-tema').addEventListener('click', () => { S.tema = document.documentElement.dataset.tema === 'escuro' ? 'claro' : 'escuro'; aplicarTema(); salvar(); });
  $('#b-olho').addEventListener('click', () => { S.ocultar = !S.ocultar; aplicarOlho(); salvar(); render(); if (Gaveta.id) desenharGaveta(); });
  $('#b-dados').addEventListener('click', dlgDados); $('#st-dados').addEventListener('click', dlgDados); $('#b-exemplo').addEventListener('click', dlgDados);
  $('#b-novo').addEventListener('click', () => dlgLivro(null));
  $('#arq').addEventListener('change', e => { const f = e.target.files && e.target.files[0]; if (f) importarBackup(f); e.target.value = ''; });
  $('#dlg').addEventListener('click', e => { if (e.target.closest('[data-fechar]')) { Dlg.fechar(); return; } const b = e.target.closest('footer [data-b]'); if (b) Dlg.acionar(+b.dataset.b); });
  $('#dlg').addEventListener('keydown', e => { if (e.key === 'Enter' && e.target.tagName === 'INPUT' && !e.target.closest('.cot') && e.target.type !== 'checkbox') { const i = Dlg.botoes.findIndex(b => /pri|perigo/.test(b.cls || '')); if (i >= 0) { e.preventDefault(); Dlg.acionar(i); } } });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      if ($('#dlg').classList.contains('on')) Dlg.fechar(); else if ($('.pop-w.aberto')) fecharPops(); else if ($('#filtros').classList.contains('folha')) folha(false);
      else if (!$('#q-r').hidden) fecharBusca(); else if ($('#gaveta').classList.contains('on')) fecharGaveta();
    } else if (e.key === '/' && !e.ctrlKey && !e.metaKey && !/^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName) && !$('.dlg.on')) { e.preventDefault(); $('#q').focus(); }
  });
  window.addEventListener('scroll', () => Tip.ocultar(), { passive: true });
  document.addEventListener('scroll', e => { const t = e.target; if (t && t.classList && t.classList.contains('rolavel')) marcarRolagem(t); }, { passive: true, capture: true });
  montarBusca();
}

/* ───────── busca rápida ───────── */
const fecharBusca = () => { $('#q-r').hidden = true; $('#q').setAttribute('aria-expanded', 'false'); };
function montarBusca() {
  const q = $('#q'), r = $('#q-r'); let foco = -1, itens = [];
  const pintar = () => {
    const txt = norm(q.value.trim()), termos = txt.split(/\s+/).filter(Boolean);
    if (!termos.length) { fecharBusca(); return; }
    const nota = b => { const t = norm(b.t), a = norm(b.a); return t.startsWith(txt) ? 0 : t.includes(txt) ? 1 : a.includes(txt) ? 2 : 3; };
    const achados = DB.livros.filter(b => termos.every(t => b._busca.includes(t)));
    itens = achados.map(b => [b, nota(b)]).sort((a, z) => a[1] - z[1] || a[0].t.localeCompare(z[0].t, 'pt-BR')).slice(0, 8).map(x => x[0]);
    foco = itens.length ? 0 : -1;
    r.innerHTML = itens.length ? itens.map((b, i) => `<button type="button" role="option" class="qr${i === foco ? ' foco' : ''}" data-id="${b.id}"><span class="tt"><b>${esc(b.t)}</b><span>${esc(b.a || 'Autor não informado')}</span></span><span class="pill col-${b.col}">${COLECOES[b.col].n}</span></button>`).join('') + (achados.length > itens.length ? `<span class="qr-n">+ ${fInt(achados.length - itens.length)} resultados · refine a busca ou use o filtro da tabela</span>` : '') : '<span class="qr-n">Nenhum livro encontrado.</span>';
    r.hidden = false; q.setAttribute('aria-expanded', 'true');
  };
  const abrir = id => { fecharBusca(); q.value = ''; q.blur(); abrirLivro(id); };
  q.addEventListener('input', debounce(pintar, 90));
  q.addEventListener('focus', () => { if (q.value.trim()) pintar(); });
  q.addEventListener('keydown', e => {
    if (r.hidden || !itens.length) return;
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') { e.preventDefault(); foco = (foco + (e.key === 'ArrowDown' ? 1 : -1) + itens.length) % itens.length; $$('.qr', r).forEach((el, i) => el.classList.toggle('foco', i === foco)); }
    else if (e.key === 'Enter' && foco >= 0) { e.preventDefault(); abrir(itens[foco].id); }
  });
  r.addEventListener('click', e => { const b = e.target.closest('.qr'); if (b) abrir(b.dataset.id); });
  document.addEventListener('pointerdown', e => { if (!e.target.closest('#busca')) fecharBusca(); });
}

/* ───────── início ───────── */
function iniciar() {
  const cfg = carregarDB();
  // enquanto nada foi editado, os exemplos acompanham a data de hoje (assim os gráficos nunca "envelhecem")
  if (DB.exemplos && DB.criadoEm !== DB.hoje && !DB.livros.some(b => b.u || temCotacaoPropria(b))) { DB.livros = gerarExemplos(livrosDoCatalogo(), DB.hoje); DB.criadoEm = DB.hoje; }
  S.tema = cfg.tema === 'claro' || cfg.tema === 'escuro' ? cfg.tema : ''; S.ocultar = !!cfg.ocultar; S.avisoVisto = !!cfg.avisoVisto;
  if (cfg.visao && VISOES[cfg.visao]) S.visao = cfg.visao;
  if (cfg.ui && typeof cfg.ui === 'object') Object.assign(S.ui, cfg.ui);
  if (cfg.tam) for (const k in cfg.tam) if (TABELAS[k] && [10, 25, 50, 100].includes(cfg.tam[k])) S.tab[k] = { tam: cfg.tam[k] };
  montarCasca(); montarFiltros(); montarGaveta(); aplicarTema(); aplicarOlho(); pintarStatus(true);
  if (window.matchMedia) { const mq = matchMedia('(prefers-color-scheme: dark)'), f = () => { if (!S.tema) aplicarTema(); }; if (mq.addEventListener) mq.addEventListener('change', f); }
  irPara(S.visao, true);
  document.documentElement.classList.add('pronto');
  try { if (sessionStorage.getItem('bl-falha')) { sessionStorage.removeItem('bl-falha'); toast('Os dados salvos não puderam ser abertos e o painel recomeçou do catálogo. A cópia do que havia está em “Seus dados”.', 'aviso');
    // a recarga da rede de segurança abre no topo (ver abaixo); depois disso a rolagem volta a ser lembrada pelo navegador
    const volta = () => setTimeout(() => { try { history.scrollRestoration = 'auto'; } catch (e) { /* nada */ } }, 600);
    if (document.readyState === 'complete') volta(); else window.addEventListener('load', volta, { once: true });
  } } catch (e) { /* nada */ }
}
try { iniciar(); }
catch (erro) {
  // Rede de segurança: se os dados salvos impedirem a abertura, guarda uma cópia e recomeça do catálogo (em vez de uma tela em branco).
  let bruto = null; try { bruto = localStorage.getItem(CHAVE); } catch (e) { /* sem armazenamento */ }
  if (bruto) { try { localStorage.setItem(CHAVE + ':falha', bruto); sessionStorage.setItem('bl-falha', '1'); } catch (e) { /* sem espaço: segue sem a cópia */ }
    // o aviso inicial volta a aparecer e empurraria a página: sem isto o navegador "restaura" a rolagem no meio do painel
    try { history.scrollRestoration = 'manual'; } catch (e) { /* nada */ }
    try { localStorage.removeItem(CHAVE); location.reload(); } catch (e) { /* nada */ } }
  else { document.documentElement.classList.add('pronto'); throw erro; }
}
