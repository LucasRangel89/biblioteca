/* ───────────────────────── casca, filtros e inicialização ───────────────────────── */
const REG = {};
let CTX = null, pendente = 0, CHIPS = [];
const ctxAtual = () => CTX || (CTX = contexto());
const cfgAtual = () => ({ tema: S.tema, ocultar: S.ocultar, avisoVisto: S.avisoVisto, saiu: S.saiu || undefined, capas: S.capas, visao: S.visao, ui: S.ui, tam: Object.fromEntries(Object.entries(S.tab).map(([k, v]) => [k, v.tam])) });
/* salvar() agenda a gravação (várias alterações seguidas viram uma só); gravarJa() grava na hora — usada quando a página
   vai sair de cena, para o que acabou de ser digitado não se perder. */
let SUJO = false;
const gravarJa = () => { SUJO = false; const ok = Loja.gravar(serializar(cfgAtual())); pintarStatus(ok); };
const gravarDepois = debounce(gravarJa, 350);
const salvar = () => { SUJO = true; gravarDepois(); };

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
  pintarFora(); pintarCasca(c); pintarContagens(c);
  const aberto = $('.pop-w.aberto'); if (aberto) (aberto.id === 'pw-tema' ? posicionarTema : posicionarPop)(aberto);      // um número novo num botão pode ter empurrado a barra
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
  // cada botão leva o rótulo e, ao lado, quantos livros da tela ele mostra (ver pintarContagens)
  const chips = (grupo, ops) => `<div class="chips" data-grupo="${grupo}">${ops.map(([v, n, d]) => `<button type="button" class="chip" data-v="${esc(v)}"${d ? ` title="${esc(d)}"` : ''}><span>${esc(n)}</span><em></em></button>`).join('')}</div>`;
  // chave do grupo: aparece quando há dois marcadores ligados nele (ou quando o grupo já está em "todos")
  // opção do quadro "Ocultar": g = sit, tipo ou eixo; ao lado vai quantos livros ela esconde (ver pintarFora)
  const opF = (g, v, n) => `<label class="opt"><input type="checkbox" data-fora="${g}" value="${esc(v)}"><span>${esc(n)}</span><em></em></label>`;
  const chave = n => `<span class="seg mini tg-m" role="group" aria-label="Como combinar os marcadores de ${esc(n)}" hidden><button type="button" data-modo="ou" title="Soma: mostra os livros que têm qualquer um dos marcadores ligados neste grupo">qualquer um</button><button type="button" data-modo="e" title="Cruza: mostra só os livros que têm todos os marcadores ligados neste grupo">todos</button></span>`;
  $('#filtros').innerHTML = `
    <div class="f-linha">
      <button type="button" class="btn f-abrir" id="f-abrir">${icone('filtro', 15)}Filtros<span class="cont" id="f-n" hidden></span></button>
      <div class="f-painel" id="f-painel">
        <div class="f-ph"><b>Filtros</b><button type="button" class="lk" data-fora-abrir>ocultar categorias</button><button type="button" class="ib" data-fechar-folha aria-label="Fechar filtros">${icone('fechar')}</button></div>
        <div class="f-corpo">
          <div class="f-g" data-g="acervo"><span class="f-r">Acervo</span>${seg('f-acervo', 'Acervo', [['tudo', 'Tudo'], ['fisico', 'Física'], ['virtual', 'Virtual'], ['ambos', 'Nas duas']])}</div>
          <div class="f-g"><span class="f-r">Tipo</span>${seg('f-tipo', 'Tipo', [['', 'Todos'], ['F', 'Ficção'], ['NF', 'Não ficção'], ['HQ', 'HQ'], ['O', 'Outros']])}</div>
          <div class="f-g pop-w" id="pw-eixo"><button type="button" class="btn pop-b" aria-expanded="false" aria-controls="pop-eixo">Eixo<span class="cont" hidden></span>${icone('baixo', 14)}</button>
            <div class="pop" id="pop-eixo"><div class="pop-h"><b>Eixo temático</b><button type="button" class="lk" data-limpar="eixos">limpar</button></div><div class="pop-l">${EIXOS.slice(1).map((e, i) => `<label class="opt"><input type="checkbox" value="${i + 1}"><span>${esc(e.n)}</span><em></em></label>`).join('')}</div></div></div>
          <div class="f-g pop-w" id="pw-mais"><button type="button" class="btn pop-b" aria-expanded="false" aria-controls="pop-mais">${icone('filtro', 14)}Mais filtros<span class="cont" hidden></span>${icone('baixo', 14)}</button>
            <div class="pop largo" id="pop-mais"><div class="pop-h"><b>Mais filtros</b><button type="button" class="lk" data-limpar="mais">limpar</button></div>
              <div class="pop-l"><label class="opt so"><input type="checkbox" id="f-top"><span>${icone('estrela', 13)} Só prioridades (#top)</span><em id="f-top-n"></em></label>
              <span class="pop-r">Dificuldade</span>${chips('dif', [1, 2, 3].map(d => [d, NIVEIS[d].n]))}
              <span class="pop-r">Extensão</span>${chips('ext', [1, 2, 3].map(e => [e, EXTENSOES[e].n, EXTENSOES[e].d]))}
              <label class="busca-t pop-q">${icone('busca', 14)}<input type="search" id="f-tagq" placeholder="Procurar marcador" aria-label="Procurar marcador"></label>
              <p class="pop-n" id="f-regra">Dois marcadores do mesmo grupo somam os livros (um ou outro); de grupos diferentes, cruzam (um e outro). O número ao lado é quantos livros desta tela cada marcador mostra.</p>
              <div id="f-tags">${GRUPOS_TAG.map(([n, lista], i) => `<div class="tg-g" data-g="${i}"><div class="tg-h"><span class="pop-r">${esc(n)}</span>${chave(n)}</div>${chips('tags', lista.map(t => [t, maiuscula(rotCurto(t)), DICA_TAG[t] || '#' + t]))}</div>`).join('')}</div>
              <div class="f-per" id="f-per"><span class="pop-r">Período <small>pela data de aquisição ou de leitura</small></span>
                <div class="f-per-l">${seg('f-periodo', 'Período', PERIODOS).replace('class="seg"', 'class="seg mini"')}<button type="button" class="btn sm f-cal" id="f-cal" aria-expanded="false" title="Período personalizado">${icone('calendario', 14)}<span id="f-cal-r">Personalizar</span></button></div>
                <div class="f-custom" id="f-custom" hidden><label><span>de</span><input type="date" id="f-de" aria-label="Data inicial"></label><label><span>até</span><input type="date" id="f-ate" aria-label="Data final"></label></div></div></div></div></div>
          <div class="f-g pop-w" id="pw-fora"><button type="button" class="btn pop-b" aria-expanded="false" aria-controls="pop-fora" aria-label="Ocultar livros" title="Ocultar os livros de uma categoria em todas as telas">${icone('olhoOff', 14)}<span class="fo-rot">Ocultar</span><span class="cont" hidden></span>${icone('baixo', 14)}</button>
            <div class="pop largo" id="pop-fora"><div class="pop-h"><b>Ocultar</b><button type="button" class="lk" data-fora-limpar hidden>mostrar tudo</button></div>
              <p class="pop-n fo-n">O que você marcar aqui <b>sai de todas as telas</b> — listas, gráficos e contagens — até ser desmarcado. A escolha fica guardada neste navegador. O número ao lado é quantos livros cada opção esconde.</p>
              <span class="pop-r">Situação</span><div class="pop-l">${SIT_FORA.map(([v, n]) => opF('sit', v, n)).join('')}</div>
              <p class="pop-n fo-n">O que você já leu sai das listas, mas continua contando nas leituras concluídas e aparecendo nas trilhas de que faz parte.</p>
              <span class="pop-r">Tipo</span><div class="pop-l">${Object.entries(ROTULO_TIPO).map(([v, n]) => opF('tipo', v, n)).join('')}</div>
              <span class="pop-r">Eixo</span><div class="pop-l">${EIXOS.slice(1).map((e, i) => opF('eixo', i + 1, e.n)).join('')}</div>
              <span class="pop-r">Marcador</span>
              <label class="busca-t pop-q fo-q">${icone('busca', 14)}<input type="search" id="fo-tagq" placeholder="Procurar marcador para ocultar" aria-label="Procurar marcador para ocultar"></label>
              <div class="chips fo-tags" id="fo-tags"></div><p class="pop-n fo-n" id="fo-tags-n"></p></div></div>
        </div>
        <div class="f-pf"><button type="button" class="btn" data-limpar="tudo">Limpar tudo</button><button type="button" class="btn pri" data-fechar-folha id="f-ver">Ver resultados</button></div>
      </div>
    </div>
    <div class="f-ativos" id="f-ativos" hidden></div>
    <div class="f-fora" id="f-fora" role="note" hidden></div>`;
  const F = $('#filtros');
  $('#f-periodo').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; S.periodo = b.dataset.v; $('#f-custom').hidden = true; filtrosMudaram(); });
  $('#f-cal').addEventListener('click', () => {
    const cx = $('#f-custom'), abrir = cx.hidden;
    if (abrir) { if (S.de == null || S.ate == null) { const I = intervalo(); S.de = S.periodo === 'tudo' ? DB.hoje - 179 : I.de; S.ate = I.ate; } S.periodo = 'custom'; }
    else if (S.periodo === 'custom') S.periodo = 'tudo';
    cx.hidden = !abrir; filtrosMudaram(); if (abrir) $('#f-de').focus();
  });
  for (const id of ['f-de', 'f-ate']) $('#' + id).addEventListener('change', () => { let de = deIso($('#f-de').value), ate = deIso($('#f-ate').value); if (de == null || ate == null) return; if (de > ate) [de, ate] = [ate, de]; S.de = Math.min(de, DB.hoje); S.ate = Math.min(ate, DB.hoje); S.periodo = 'custom'; filtrosMudaram(); });
  $('#f-acervo').addEventListener('click', e => { const b = e.target.closest('button'); if (b) { S.acervo = b.dataset.v; filtrosMudaram(); } });
  $('#f-tipo').addEventListener('click', e => { const b = e.target.closest('button'); if (b) { S.tipo = b.dataset.v; filtrosMudaram(); } });
  $('#pop-eixo').addEventListener('change', e => { if (e.target.matches('input[type=checkbox]')) { alternar(S.eixos, +e.target.value); filtrosMudaram(); } });
  $('#f-top').addEventListener('change', e => { S.top = e.target.checked; filtrosMudaram(); });
  // os botões são guardados uma vez, com o que a busca e a contagem precisam: g = filtro (tags, dif, ext), v = valor, q = texto procurável
  CHIPS = $$('#pop-mais .chip').map(el => {
    const g = el.parentElement.dataset.grupo, tag = g === 'tags', v = tag ? el.dataset.v : +el.dataset.v, rot = $('span', el).textContent;
    return { el, g, v, rot, em: $('em', el), dica: el.title, q: norm(tag ? [rot, rotTag(v), v, DICA_TAG[v] || ''].join(' ') : rot) };
  });
  $('#pop-mais').addEventListener('click', e => {
    const m = e.target.closest('[data-modo]');
    if (m) {                                         // chave "qualquer um / todos" de um grupo: é preferência, fica guardada
      const nome = GRUPOS_TAG[+m.closest('.tg-g').dataset.g][0];
      if (m.dataset.modo === 'e') S.ui.cruzar[nome] = true; else delete S.ui.cruzar[nome];
      salvar(); filtrosMudaram(); return;
    }
    const b = e.target.closest('.chip'); if (!b) return; const g = b.parentElement.dataset.grupo; alternar(S[g], g === 'tags' ? b.dataset.v : +b.dataset.v); filtrosMudaram();
  });
  $('#f-tagq').addEventListener('input', e => { const q = norm(e.target.value.trim()); for (const c of CHIPS) if (c.g === 'tags') c.el.hidden = !!q && !c.q.includes(q); $$('#f-tags .tg-g').forEach(g => { g.hidden = !$$('.chip', g).some(c => !c.hidden); }); });
  // "Ocultar": cada opção marcada tira livros de todas as telas; é preferência, fica guardada (S.ui.fora)
  const foraMudou = () => { refazerFora(); salvar(); filtrosMudaram(); };
  const alternarFora = (g, v, liga) => { const l = S.ui.fora[g], k = l.indexOf(v); if (k < 0 && liga !== false) l.push(v); else if (k >= 0 && liga !== true) l.splice(k, 1); foraMudou(); };
  $('#pop-fora').addEventListener('change', e => { const i = e.target; if (i.matches('input[data-fora]')) alternarFora(i.dataset.fora, i.dataset.fora === 'eixo' ? +i.value : i.value, i.checked); });
  $('#fo-tags').addEventListener('click', e => { const b = e.target.closest('.chip'); if (b) alternarFora('tag', b.dataset.v); });
  $('#fo-tagq').addEventListener('input', () => { pintarFora(); ($('#fo-tags-n').textContent ? $('#fo-tags-n') : $('#fo-tags')).scrollIntoView({ block: 'nearest' }); });
  F.addEventListener('click', e => {
    if (e.target.closest('[data-fora-limpar]')) { const havia = FORA.n; S.ui.fora = lerFora(null); $('#fo-tagq').value = ''; foraMudou(); if (havia) toast('Nada mais está oculto.'); return; }
    if (e.target.closest('[data-fora-abrir]')) { abrirFora(); return; }
    const l = e.target.closest('[data-limpar]');
    if (l) { const x = l.dataset.limpar; if (x === 'eixos') S.eixos.clear(); else if (x === 'mais') { S.dif.clear(); S.ext.clear(); S.tags.clear(); S.top = false; S.periodo = 'tudo'; S.de = S.ate = null; $('#f-custom').hidden = true; } else { limparFiltros(true); $('#f-custom').hidden = true; } filtrosMudaram(); return; }
    const r = e.target.closest('[data-rm]');
    if (r) { const [g, v] = r.dataset.rm.split(':'); if (g === 'acervo') S.acervo = 'tudo'; else if (g === 'tipo') S.tipo = ''; else if (g === 'top') S.top = false; else if (g === 'periodo') { S.periodo = 'tudo'; S.de = S.ate = null; $('#f-custom').hidden = true; } else if (g === 'tags') S.tags.delete(v); else S[g].delete(+v); filtrosMudaram(); return; }
    const pb = e.target.closest('.pop-b');
    if (pb) {
      const w = pb.parentElement, abrir = !w.classList.contains('aberto'); fecharPops();
      if (abrir) {
        w.classList.add('aberto'); pb.setAttribute('aria-expanded', 'true'); posicionarPop(w);
      }
      return;
    }
    if (e.target.closest('[data-fechar-folha]')) folha(false);
  });
  $('#f-abrir').addEventListener('click', () => folha(true));
  // se a janela alargar com a folha aberta (tablet girado, janela redimensionada), fecha: no layout largo ela não existe e a página ficaria travada
  if (window.matchMedia) { const mq = matchMedia('(max-width: 820px)'), f = () => { if (!mq.matches) folha(false); }; if (mq.addEventListener) mq.addEventListener('change', f); else if (mq.addListener) mq.addListener(f); }
  document.addEventListener('pointerdown', e => { if (!e.target.closest('.pop-w')) fecharPops(); if (F.classList.contains('folha') && !e.target.closest('#f-painel, #f-abrir, #f-cal')) folha(false); });
}
/* mostra, na tabela da visão geral, os livros que o usuário criou ou editou (aba "Editados por você") */
function verEditados() {
  limparFiltros(true); $('#f-custom').hidden = true;
  S.tab.geral = Object.assign(S.tab.geral || {}, { aba: 'meus', q: '', pag: 0 });
  irPara('geral');
  const t = $('#p-tab-geral'); if (!t) return;
  const q = $('input[type=search]', t), aba = $('.abas [aria-selected="true"]', t); if (q) q.value = '';
  t.scrollIntoView({ block: 'start' });
  if (aba) aba.scrollIntoView({ block: 'nearest', inline: 'end' });      // no celular as abas rolam de lado: a escolhida tem de aparecer
}
// o quadro aberto não pode sair da janela pela direita: recua o quanto for preciso (sem passar da borda esquerda da barra)
function posicionarPop(w) {
  const pop = $('.pop', w); pop.style.left = '';
  const r = pop.getBoundingClientRect(), sobra = r.right - (document.documentElement.clientWidth - 12);
  if (sobra > 0) pop.style.left = -Math.min(sobra, Math.max(0, r.left - $('#filtros').getBoundingClientRect().left - 12)) + 'px';
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
  $$('#pop-eixo .opt input').forEach(inp => { inp.checked = S.eixos.has(+inp.value); });
  $('#f-top').checked = S.top;
  for (const c of CHIPS) c.el.setAttribute('aria-pressed', String(S[c.g].has(c.v)));
  // chave "qualquer um / todos": só aparece no grupo em que faz diferença — dois marcadores ligados — ou que já está em "todos"
  const sel = selTags();
  $$('#f-tags .tg-g').forEach(g => {
    const i = +g.dataset.g, e = cruza(i), s = sel.find(x => x.g === i), m = $('.tg-m', g);
    m.hidden = !(e || (s && s.ts.length > 1));
    $$('button', m).forEach(b => b.setAttribute('aria-pressed', String((b.dataset.modo === 'e') === e)));
  });
  const nMais = S.dif.size + S.ext.size + S.tags.size + (S.top ? 1 : 0) + (S.periodo !== 'tudo' ? 1 : 0), cont = (sel, n) => { const el = $(sel); el.hidden = !n; el.textContent = n; };
  cont('#pw-eixo .cont', S.eixos.size); cont('#pw-mais .cont', nMais); cont('#f-n', nFiltros());
  $('#pw-eixo').classList.toggle('ativo', S.eixos.size > 0); $('#pw-mais').classList.toggle('ativo', nMais > 0);
  // Filtros ativos: cada filtro vira um botão (clicar remove). Os que se somam ou se cruzam entre si vão juntos, com a palavra que diz como:
  // "A ou B" (qualquer um) ou "A e B" (todos); entre um conjunto e outro, vale sempre o cruzamento.
  const ch = []; let nAtivos = 0;
  const bt = (rm, txt) => `<button type="button" class="ativo" data-rm="${esc(rm)}" title="Remover filtro">${esc(txt)}${icone('fechar', 12)}</button>`;
  const junta = (bts, con) => { nAtivos += bts.length; if (bts.length) ch.push(bts.length > 1 ? `<span class="fa-g">${bts.join(`<i class="fa-c">${con}</i>`)}</span>` : bts[0]); };
  const add = (rm, txt) => junta([bt(rm, txt)]);
  if (S.acervo !== 'tudo' && S.visao !== 'recs') add('acervo:', ROTULO_ACERVO[S.acervo]);
  if (S.tipo) add('tipo:', { F: 'Ficção', NF: 'Não ficção', HQ: 'HQ', O: 'Poesia e outros' }[S.tipo]);
  junta([...S.eixos].sort((a, z) => a - z).map(e => bt('eixos:' + e, EIXOS[e].n)), 'ou');
  if (S.top) add('top:', 'Só prioridades');
  junta([...S.dif].map(d => bt('dif:' + d, 'Dificuldade ' + NIVEIS[d].n.toLowerCase())), 'ou');
  junta([...S.ext].map(e => bt('ext:' + e, 'Extensão ' + EXTENSOES[e].n.toLowerCase())), 'ou');
  for (const s of sel) junta(s.ts.map(t => bt('tags:' + t, ehCamada(t) || t === TAG_ANALISE ? maiuscula(rotTag(t)) : '#' + rotTag(t))), s.e ? 'e' : 'ou');
  if (S.periodo !== 'tudo') add('periodo:', custom ? `${fData(I.de)} – ${fData(I.ate)}` : 'Período: ' + (PERIODOS.find(([v]) => v === S.periodo) || ['', ''])[1].toLowerCase());
  const el = $('#f-ativos'); el.hidden = !nAtivos;
  setHtml(el, nAtivos ? `<span class="fa-r">Filtros ativos</span>${ch.join('')}${nAtivos > 1 ? '<button type="button" class="lk" data-limpar="tudo">limpar tudo</button>' : ''}` : '');
}
// os filtros ligados, em palavras — lidos de "Filtros ativos", para o papel dizer exatamente o que a tela diz
const filtrosEmTexto = () => { const el = $('#f-ativos'); return !el || el.hidden ? [] : [...el.children].filter(e => !e.matches('.fa-r, .lk')).map(e => (e.matches('.fa-g') ? [...e.children].map(x => x.textContent.trim()).join(' ') : e.textContent.trim())); };
/* Números dos filtros (ver contagens, em 30-state): quantos livros a lista desta tela mostra com cada opção ligada.
   A opção que não mostraria nenhum fica apagada — pela cor, não por opacidade, para continuar legível — e segue clicável. */
function pintarContagens(c) {
  const k = contagens(c), nenhum = n => (n ? plural(n, 'livro', 'livros') : 'nenhum livro');
  $$('#pop-eixo .opt').forEach(o => { const inp = $('input', o), n = k.eixos.get(+inp.value) || 0; $('em', o).textContent = fInt(n); o.classList.toggle('zero', !n && !inp.checked); });
  $('#f-top-n').textContent = fInt(k.top); $('#f-top-n').parentElement.classList.toggle('zero', !k.top && !S.top);
  for (const x of CHIPS) {
    const n = (x.g === 'tags' ? k.tag.get(x.v) : k[x.g].get(x.v)) || 0, zero = !n && !S[x.g].has(x.v);
    if (x.n !== n) { x.n = n; x.em.textContent = fInt(n); x.el.dataset.n = n; x.el.setAttribute('aria-label', `${x.rot}: ${nenhum(n)}`); }
    if (x.zero !== zero) { x.zero = zero; x.el.classList.toggle('zero', zero); x.el.title = zero ? (x.dica ? x.dica + ' — ' : '') + 'nenhum livro nesta tela com os filtros atuais' : x.dica; }
  }
}

/* "Ocultar" (ver 30-state): marca as opções do quadro, põe ao lado de cada uma quantos livros ela esconde — no painel inteiro,
   sem olhar os filtros — e mantém o aviso, sempre à vista sob a barra, de quantos livros estão fora e por quê. */
let MARCS = null;
function pintarFora() {
  const f = S.ui.fora, inc = (m, k) => m.set(k, (m.get(k) || 0) + 1), k = { sit: new Map(), tipo: new Map(), eixo: new Map(), tag: new Map() };
  let n = 0;
  for (const b of DB.livros) { if (oculto(b)) n++; for (const x of SIT_FORA) if (x[2](b)) inc(k.sit, x[0]); inc(k.tipo, tipoFiltro(b._tipo)); inc(k.eixo, b.eixo); for (const t of b.tags) inc(k.tag, t); }
  FORA.livros = n;
  $$('#pop-fora input[data-fora]').forEach(i => { const g = i.dataset.fora, v = g === 'eixo' ? +i.value : i.value, q = k[g].get(v) || 0; i.checked = f[g].includes(v); $('em', i.parentElement).textContent = fInt(q); i.parentElement.classList.toggle('zero', !q && !i.checked); });
  // marcadores: os ocultos ficam sempre à vista (clicar tira); a busca traz os outros
  if (!MARCS) MARCS = CHIPS.filter(c => c.g === 'tags').map(c => ({ v: c.v, rot: c.rot, q: c.q, dica: c.dica }));
  const q = norm($('#fo-tagq').value.trim()), todos = q ? MARCS.filter(m => m.q.includes(q) && !f.tag.includes(m.v)) : [], achados = todos.slice(0, 24);
  const de = v => MARCS.find(m => m.v === v) || { v, rot: maiuscula(rotTag(v)), dica: '#' + v };
  const chip = (m, on) => `<button type="button" class="chip" data-v="${esc(m.v)}" aria-pressed="${on}" title="${esc((m.dica ? m.dica + ' — ' : '') + (on ? 'clique para voltar a mostrar' : 'clique para ocultar'))}"><span>${esc(m.rot)}</span><em>${fInt(k.tag.get(m.v) || 0)}</em></button>`;
  setHtml($('#fo-tags'), f.tag.map(v => chip(de(v), true)).join('') + achados.map(m => chip(m, false)).join(''));
  $('#fo-tags-n').textContent = q ? (!todos.length ? 'Nenhum marcador com esse nome.' : todos.length > achados.length ? `Mostrando ${achados.length} de ${todos.length}: refine a busca.` : '') : f.tag.length ? '' : 'Digite para achar um marcador: gênero, tema, trilha, cenário…';
  const cont = $('#pw-fora .cont'); cont.hidden = !FORA.n; cont.textContent = FORA.n;
  $('#pw-fora').classList.toggle('ativo', FORA.n > 0); $('#pop-fora [data-fora-limpar]').hidden = !FORA.n;
  const av = $('#f-fora'); av.hidden = !FORA.n;
  if (!FORA.n) return;
  setHtml(av, `<span class="ff-t">${icone('olhoOff', 15)}<b>${n ? plural(n, 'livro oculto', 'livros ocultos') : 'Nenhum livro oculto por enquanto'}</b><span class="ff-r">${esc(regrasFora().join(' · '))}</span></span><span class="ff-a"><button type="button" class="lk" data-fora-abrir>mudar</button><button type="button" class="lk" data-fora-limpar>mostrar todos</button></span>`);
}
/* abre as opções de "Ocultar": o quadro, na tela larga; a folha de filtros, rolada até elas, na estreita */
function abrirFora() {
  const w = $('#pw-fora');
  if (window.matchMedia && matchMedia('(max-width: 820px)').matches) { folha(true, true); setTimeout(() => { w.scrollIntoView({ block: 'start' }); focar($('input', w), 3); }, 80); return; }
  if (!w.classList.contains('aberto')) $('.pop-b', w).click();
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
  const av = $('#aviso'), mostrar = !S.avisoVisto;
  av.classList.toggle('inicio', !DB.exemplos);
  // sem exemplos: um recado, uma vez, dizendo de onde vêm os números e como registrar o resto.
  // S.saiu > 0: os exemplos de um painel antigo acabaram de sair (S.saiu - 1 = quantos livros editados ficaram como estavam)
  if (mostrar && !DB.exemplos) {
    const como = 'Leituras, datas e valores aparecem conforme você registra: abra um livro e use <b>Já li</b>, <b>Começar a ler</b> ou <b>Editar</b>. Nada disso é obrigatório — nem as datas.';
    const meus = S.saiu > 1 ? S.saiu - 1 : 0;
    setHtml(av, `<span class="av-i">${icone('info', 18)}</span><div>` + (S.saiu
      ? `<b>Os dados de exemplo saíram.</b><p>As leituras, datas e valores inventados que o painel mostrava foram retirados: agora só aparece o que é seu. ${como}</p>` +
        (meus ? `<p>${meus === 1 ? 'O livro que você criou ou editou' : 'Os ' + fInt(meus) + ' livros que você criou ou editou'} enquanto os exemplos estavam ligados <b>${meus === 1 ? 'ficou como estava' : 'ficaram como estavam'}</b>: ${meus === 1 ? 'pode' : 'podem'} trazer datas ou valores de exemplo misturados ao que você anotou. Se eram só testes, use <b>Recomeçar do catálogo original</b>, em <b>Seus dados</b>.</p>` : '')
      : `<b>Aqui só aparece o que é seu.</b><p>Os ${fInt(DB.livros.filter(b => b.sec >= 0).length)} títulos, a estante física e a biblioteca virtual vieram do seu catálogo. ${como}</p>`) +
      `</div><div class="av-a">${meus ? `<button type="button" class="btn sm" data-av="meus">Ver ${meus === 1 ? 'esse livro' : 'esses livros'}</button>` : ''}<button type="button" class="btn sm pri" data-av="ok">Entendi</button></div>`);
  }
  av.hidden = !mostrar;
  if (mostrar && DB.exemplos) setHtml(av, `<span class="av-i">${icone('info', 18)}</span><div><b>Seu catálogo é real; o movimento é de exemplo.</b><p>Os ${fInt(DB.livros.filter(b => b.sec >= 0).length)} títulos, autores, marcadores, eixos, a estante física e a biblioteca virtual vieram do seu catálogo. Datas e valores pagos, leituras, a lista de próximas aquisições e os históricos de preço são <b>simulados</b> para dar vida aos gráficos, e os preços não vêm das lojas: entram por cotações que você registra.</p></div><div class="av-a"><button type="button" class="btn sm" data-av="dados">Gerenciar dados</button><button type="button" class="btn sm pri" data-av="ok">Entendi</button></div>`);
  $('#rodape-n').textContent = `${plural(DB.livros.length, 'livro', 'livros')}${FORA.livros ? ' · ' + plural(FORA.livros, 'oculto', 'ocultos') : ''} · ${c.I.tudo ? 'todo o histórico' : c.I.rot}${nFiltros() ? ' · ' + plural(nFiltros(), 'filtro ativo', 'filtros ativos') : ''}`;
}
/* ───────── temas ───────── */
// o tema em uso: o escolhido ou, sem escolha, o padrão que acompanha o sistema (claro ou escuro)
const temaAtual = () => TEMAS.find(t => t.id === (S.tema || (window.matchMedia && matchMedia('(prefers-color-scheme: dark)').matches ? 'escuro' : 'claro'))) || TEMAS[0];
function aplicarTema() {
  const t = temaAtual();
  document.documentElement.dataset.tema = t.id;
  const b = $('#b-tema'); b.setAttribute('aria-label', `Aparência: tema ${t.n}. Trocar o tema`); b.title = 'Trocar o tema do painel';
  const m = $('meta[name="theme-color"]'); if (m) m.content = t.cor;
  for (const o of $$('#pop-tema [data-tema-id]')) { const on = o.dataset.temaId === t.id; o.setAttribute('aria-checked', String(on)); o.tabIndex = on ? 0 : -1; }
}
// o quadro dos temas abre para a esquerda do botão; em tela estreita, não pode sair pela borda esquerda
function posicionarTema() {
  const pop = $('#pop-tema'); pop.style.right = '';
  const r = pop.getBoundingClientRect(); if (r.left < 12) pop.style.right = Math.round(r.left - 12) + 'px';
}
function montarTemas() {
  const w = $('#pw-tema'), b = $('#b-tema'), pop = $('#pop-tema');
  b.innerHTML = icone('paleta');
  // a amostra e o nome de cada tema levam [data-tema]: dentro deles valem as cores e a letra do próprio tema
  pop.innerHTML = `<div class="pop-h"><b id="tema-t">Aparência</b></div>
    <div class="temas" role="radiogroup" aria-labelledby="tema-t">${TEMAS.map(t => `<button type="button" class="tema-o" role="radio" aria-checked="false" tabindex="-1" data-tema-id="${t.id}">
      <span class="tema-am" data-tema="${t.id}" aria-hidden="true"><i></i><i></i><i></i><i></i></span>
      <span class="tema-tx"><b class="tema-n" data-tema="${t.id}">${t.n}</b><em>${t.d}</em></span>${icone('check', 16)}</button>`).join('')}</div>
    <p class="pop-n">Troca as cores e a letra dos títulos. A escolha fica guardada neste navegador.</p>`;
  const escolher = id => { S.tema = id; aplicarTema(); salvar(); };
  b.addEventListener('click', () => {
    const abrir = !w.classList.contains('aberto'); fecharPops(); if (!abrir) return;
    w.classList.add('aberto'); b.setAttribute('aria-expanded', 'true'); posicionarTema();
    const o = $('[aria-checked="true"]', pop); if (o) o.focus({ preventScroll: true });
  });
  pop.addEventListener('click', e => { const o = e.target.closest('[data-tema-id]'); if (o) escolher(o.dataset.temaId); });
  // como num grupo de opções: as setas andam e já escolhem (a página muda na hora); Esc fecha e devolve o foco ao botão
  pop.addEventListener('keydown', e => {
    if (e.key === 'Escape') { e.stopPropagation(); fecharPops(); b.focus(); return; }
    const os = $$('[data-tema-id]', pop), i = os.indexOf(document.activeElement); if (i < 0) return;
    const j = e.key === 'ArrowDown' || e.key === 'ArrowRight' ? (i + 1) % os.length : e.key === 'ArrowUp' || e.key === 'ArrowLeft' ? (i + os.length - 1) % os.length : e.key === 'Home' ? 0 : e.key === 'End' ? os.length - 1 : -1;
    if (j < 0) return;
    e.preventDefault(); escolher(os[j].dataset.temaId); os[j].focus();
  });
  w.addEventListener('focusout', e => { if (w.classList.contains('aberto') && e.relatedTarget && !w.contains(e.relatedTarget)) fecharPops(); });
  // imprimir a página (Ctrl+P) num tema escuro sairia com letra clara em papel branco: no papel vale o padrão claro
  window.addEventListener('beforeprint', () => { if (temaAtual().clima === 'escuro') document.documentElement.dataset.tema = 'claro'; });
  window.addEventListener('afterprint', aplicarTema);
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
    const av = e.target.closest('[data-av]'); if (av) {
      if (av.dataset.av === 'ok') { S.avisoVisto = true; S.saiu = 0; salvar(); pintarCasca(ctxAtual()); }
      else if (av.dataset.av === 'meus') verEditados();
      else dlgDados();
    }
  });
  montarTemas();
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
    r.innerHTML = itens.length ? itens.map((b, i) => `<button type="button" role="option" class="qr${i === foco ? ' foco' : ''}" data-id="${b.id}"><span class="tt"><b>${esc(b.t)}</b><span>${esc(b.a || 'Autor não informado')}${oculto(b) ? ' · fora das listas (oculto)' : ''}</span></span><span class="pill col-${b.col}">${COLECOES[b.col].n}</span></button>`).join('') + (achados.length > itens.length ? `<span class="qr-n">+ ${fInt(achados.length - itens.length)} resultados · refine a busca ou use o filtro da tabela</span>` : '') : '<span class="qr-n">Nenhum livro encontrado.</span>';
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
  S.tema = TEMAS.some(t => t.id === cfg.tema) ? cfg.tema : ''; S.ocultar = !!cfg.ocultar; S.avisoVisto = !!cfg.avisoVisto;
  S.capas = cfg.capas !== false; MOSTRAR_CAPAS = S.capas;
  // os exemplos de um painel antigo acabaram de sair: o recado inicial volta, agora contando isso, e fica até o "Entendi"
  S.saiu = DB.saiuExemplo || (cfg.saiu > 0 && !DB.exemplos ? Math.round(+cfg.saiu) || 0 : 0);
  if (DB.saiuExemplo) S.avisoVisto = false;
  // imagem de capa que não carregou (sem rede, capa retirada do ar): some, e fica o desenho com a inicial do título
  document.addEventListener('error', e => { const im = e.target; if (im && im.tagName === 'IMG' && im.parentElement && im.parentElement.classList.contains('capa')) { const c = im.parentElement; if (c.classList.contains('g')) c.remove(); else im.remove(); } }, true);
  if (cfg.visao && VISOES[cfg.visao]) S.visao = cfg.visao;
  if (cfg.ui && typeof cfg.ui === 'object') Object.assign(S.ui, cfg.ui);
  S.ui.fora = lerFora(S.ui.fora); refazerFora();      // "Ocultar": só valem regras que existem
  // "Temas e camadas": até a rodada 7 guardava-se a posição do grupo na lista; agora, o nome (a lista ganhou um grupo no meio)
  if (typeof S.ui.temas === 'number') S.ui.temas = GRUPOS_TAG_V1[S.ui.temas] || 'Temas';
  if (grupoTag(S.ui.temas) < 0) S.ui.temas = 'Temas';
  // chaves "todos" dos grupos de marcadores: só valem as de grupos que existem
  S.ui.cruzar = S.ui.cruzar && typeof S.ui.cruzar === 'object' && !Array.isArray(S.ui.cruzar) ? Object.fromEntries(GRUPOS_TAG.filter(g => S.ui.cruzar[g[0]] === true).map(g => [g[0], true])) : {};
  if (cfg.tam) for (const k in cfg.tam) if (TABELAS[k] && [10, 25, 50, 100].includes(cfg.tam[k])) S.tab[k] = { tam: cfg.tam[k] };
  montarCasca(); montarFiltros(); montarGaveta(); aplicarTema(); aplicarOlho(); pintarStatus(true);
  if (window.matchMedia) { const mq = matchMedia('(prefers-color-scheme: dark)'), f = () => { if (!S.tema) aplicarTema(); }; if (mq.addEventListener) mq.addEventListener('change', f); }
  irPara(S.visao, true);
  document.documentElement.classList.add('pronto');
  carregarCapas();                                  // capas enviadas pelo usuário: chegam do banco do navegador e a tela é redesenhada
  // a página vai sair de cena (aba fechada, outro aplicativo no telefone): grava o comentário em edição e o que estiver pendente
  const fechando = () => { Notas.guardar(); if (SUJO) gravarJa(); };
  window.addEventListener('pagehide', fechando);
  document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'hidden') fechando(); });
  // o painel chegou com outro catálogo: os dados salvos já foram conciliados (ver conciliarCatalogo); grava e avisa
  if (DB.novidade) { salvar(); if (textoNovidade()) toast(textoNovidade().trim() + ' O que você editou no painel foi mantido.'); }
  // os dados de exemplo de um painel antigo saíram (ver carregarDB): grava e avisa
  if (DB.saiuExemplo) { salvar(); toast('Os dados de exemplo saíram: agora o painel mostra só o que é seu.'); }
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
