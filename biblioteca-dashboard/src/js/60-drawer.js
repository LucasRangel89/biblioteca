/* ───────────────────────── gaveta do livro, diálogos e ações ───────────────────────── */
function toast(msg, tipo) {
  const el = document.createElement('div'); el.className = 'toast ' + (tipo || 'ok');
  el.innerHTML = `${icone(tipo === 'aviso' ? 'info' : tipo === 'erro' ? 'fechar' : 'check', 15)}<span>${esc(msg)}</span>`;
  $('#toasts').appendChild(el);
  setTimeout(() => { el.classList.add('sai'); setTimeout(() => el.remove(), 350); }, 3600);
}
/* valor digitado → número (null se vazio, NaN se não der para entender). Aceita "45", "45,9", "R$ 1.234,56", "45.90";
   ponto seguido de exatamente três dígitos é milhar, como se escreve no Brasil ("1.250" = mil duzentos e cinquenta). */
const lerValor = s => {
  s = String(s ?? '').replace(/[R$\s]/g, ''); if (!s) return null;
  if (s.includes(',')) s = s.replace(/\./g, '').replace(',', '.');
  else if (/^\d{1,3}(\.\d{3})+$/.test(s)) s = s.replace(/\./g, '');
  return /^(\d+\.?\d*|\.\d+)$/.test(s) ? Math.round(parseFloat(s) * 100) / 100 : NaN;
};
const valorCampo = v => (v == null ? '' : String(v.toFixed(2)).replace('.', ','));
const travar = () => document.documentElement.classList.toggle('travado', !!$('.gaveta.on, .dlg.on, .filtros.folha'));

/* ───────── foco nas camadas (gaveta, diálogo e folha de filtros) ─────────
   Ao abrir, o foco entra na camada; o Tab circula só dentro dela; ao fechar, volta para onde estava.
   focar() insiste por alguns quadros porque um elemento que ainda está invisível (transição de abertura) recusa o foco. */
function focar(el, tentativas = 10) {
  if (!el || !document.contains(el)) return;
  try { el.focus({ preventScroll: true }); } catch (e) { /* nada */ }
  if (document.activeElement !== el && tentativas > 0) setTimeout(() => focar(el, tentativas - 1), 30);
}
const FOCAVEIS = 'a[href], button:not([disabled]), input:not([disabled]):not([type="hidden"]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';
document.addEventListener('keydown', e => {
  if (e.key !== 'Tab') return;
  const camada = $('#dlg.on .dlg-cx') || $('#gaveta.on .gv-p') || $('#filtros.folha #f-painel'); if (!camada) return;
  const itens = $$(FOCAVEIS, camada).filter(x => x.getClientRects().length), at = document.activeElement;
  if (!itens.length) { e.preventDefault(); return; }
  const pri = itens[0], ult = itens[itens.length - 1];
  if (!camada.contains(at) || (e.shiftKey ? at === pri || at === camada : at === ult)) { e.preventDefault(); (e.shiftKey ? ult : pri).focus(); }
});

/* ───────── diálogo genérico ───────── */
const Dlg = {
  botoes: [], antes: null,
  abrir({ titulo, corpo, botoes, largo, aoAbrir }) {
    const el = $('#dlg'); this.botoes = botoes || []; this.antes = document.activeElement;
    el.innerHTML = `<div class="dlg-fundo" data-fechar></div><div class="dlg-cx${largo ? ' largo' : ''}" role="dialog" aria-modal="true" aria-labelledby="dlg-t"><header><h2 id="dlg-t">${esc(titulo)}</h2><button type="button" class="ib" data-fechar aria-label="Fechar">${icone('fechar')}</button></header><div class="dlg-c">${corpo}</div>${this.botoes.length ? `<footer>${this.botoes.map((b, i) => `<button type="button" class="btn ${b.cls || ''}" data-b="${i}">${esc(b.n)}</button>`).join('')}</footer>` : ''}</div>`;
    el.classList.add('on'); el.setAttribute('aria-hidden', 'false'); travar();
    const c = $('.dlg-c', el); if (aoAbrir) aoAbrir(c);
    const foco = $('[data-foco]', el) || $('input:not([type=hidden]):not([type=checkbox]), select, textarea', c) || $('footer .btn.pri', el) || $('[data-fechar].ib', el);
    if (foco) setTimeout(() => focar(foco), 30);
  },
  fechar() { const el = $('#dlg'); if (!el.classList.contains('on')) return; el.classList.remove('on'); el.setAttribute('aria-hidden', 'true'); el.innerHTML = ''; travar(); if (this.antes && this.antes.focus) try { this.antes.focus(); } catch (e) { /* nada */ } },
  acionar(i) { const b = this.botoes[i]; if (!b) return; if (!b.acao || b.acao($('#dlg .dlg-c')) !== false) this.fechar(); },
};
function confirmar(titulo, msg, rotulo, acao, perigo) {
  Dlg.abrir({ titulo, corpo: `<p class="dlg-msg">${msg}</p>`, botoes: [{ n: 'Cancelar' }, { n: rotulo, cls: perigo ? 'perigo' : 'pri', acao }] });
}
const erroCampo = (inp, msg) => { inp.classList.add('erro'); inp.focus(); toast(msg, 'aviso'); inp.addEventListener('input', () => inp.classList.remove('erro'), { once: true }); return false; };

/* ───────── arquivos (backup e CSV) ───────── */
function baixarArquivo(nome, txt, tipo) {
  if (!Loja.ok) {                             // pré-visualização em sandbox: downloads são bloqueados
    Dlg.abrir({ titulo: nome, largo: true, corpo: `<p class="nota">Esta pré-visualização bloqueia downloads. Copie o conteúdo abaixo ou abra o arquivo HTML direto no navegador para baixar normalmente.</p><textarea class="copia" readonly rows="12" data-foco>${esc(txt)}</textarea>`,
      botoes: [{ n: 'Fechar' }, { n: 'Selecionar tudo', cls: 'pri', acao: el => { $('textarea', el).select(); try { document.execCommand('copy'); toast('Conteúdo copiado.'); } catch (e) { /* nada */ } return false; } }] });
    return;
  }
  const url = URL.createObjectURL(new Blob([txt], { type: tipo })), a = document.createElement('a');
  a.href = url; a.download = nome; document.body.appendChild(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(url), 3000);
  toast('Arquivo gerado: ' + nome);
}
function importarBackup(arquivo) {
  const leitor = new FileReader();
  leitor.onerror = () => toast('Não foi possível ler o arquivo.', 'erro');
  leitor.onload = () => {
    let o; try { o = JSON.parse(String(leitor.result)); } catch (e) { o = null; }
    const livros = o && typeof o === 'object' && o.app === 'biblioteca-lucas' ? lerLivros(o.livros) : [];
    if (!livros.length) { toast('Este arquivo não é um backup válido do painel.', 'erro'); return; }
    const fora = o.livros.length - livros.length, quando = typeof o.salvoEm === 'string' && !isNaN(Date.parse(o.salvoEm)) ? ' · salvo em ' + esc(new Date(o.salvoEm).toLocaleString('pt-BR')) : '';
    confirmar('Importar backup', `Substituir os dados atuais pelos do arquivo <b>${esc(arquivo.name)}</b>?<br>${plural(livros.length, 'livro', 'livros')}${quando}${fora ? ` · ${plural(fora, 'registro ilegível será ignorado', 'registros ilegíveis serão ignorados')}` : ''}. Esta ação não pode ser desfeita.`, 'Importar', () => {
      DB.livros = livros; DB.exemplos = !!o.exemplos; DB.criadoEm = typeof o.criadoEm === 'number' && isFinite(o.criadoEm) ? o.criadoEm : DB.hoje; S.sel = '';
      salvar(); fecharGaveta(); filtrosMudaram(); toast('Backup importado.');
    });
  };
  leitor.readAsText(arquivo);
}
function dlgDados() {
  const meus = DB.livros.filter(b => b.u).length, cot = soma(DB.livros, b => (b.px ? soma(Object.values(b.px), pts => pts.filter(p => p[2]).length) : 0));
  Dlg.abrir({ titulo: 'Seus dados', largo: true, corpo: `
    <div class="dados">
      <div class="dd-st ${Loja.ok ? 'ok' : 'aviso'}">${icone(Loja.ok ? 'check' : 'info', 16)}<div><b>${Loja.ok ? 'Salvo neste navegador' : 'Pré-visualização: nada é salvo'}</b><span>${Loja.ok ? 'Tudo fica só neste dispositivo (armazenamento local do navegador). Nenhum dado é enviado para a internet.' : 'Este ambiente não permite gravar. Baixe o arquivo HTML e abra-o no navegador para que suas alterações fiquem salvas no seu dispositivo.'}</span></div></div>
      <dl class="dd-n"><div><dt>Livros</dt><dd>${fInt(DB.livros.length)}</dd></div><div><dt>Editados por você</dt><dd>${fInt(meus)}</dd></div><div><dt>Cotações suas</dt><dd>${fInt(cot)}</dd></div></dl>
      <section><h3>Backup</h3><p>Guarde uma cópia em arquivo ou leve seus dados para outro navegador.</p><div class="dd-b"><button type="button" class="btn" data-x="exportar">${icone('baixar', 15)}Exportar backup (.json)</button><button type="button" class="btn" data-x="importar">${icone('enviar', 15)}Importar backup…</button></div></section>
      <section><h3>Dados de exemplo</h3><p>Títulos, autores, marcadores, eixos e a estante física vêm do seu catálogo. Datas, valores pagos, e-books e audiolivros, leituras, notas, a lista de próximas aquisições e os históricos de preço são <b>simulados</b> para dar vida aos gráficos. ${DB.exemplos ? 'Ao limpar, fica só o que é do catálogo e o que você editou ou registrou.' : 'Eles foram removidos; você pode trazê-los de volta para explorar o painel.'}</p>
        <div class="dd-b">${DB.exemplos ? `<button type="button" class="btn" data-x="limpar">${icone('lixo', 15)}Limpar dados de exemplo</button>` : `<button type="button" class="btn" data-x="restaurar">${icone('desfazer', 15)}Restaurar dados de exemplo</button>`}</div></section>
      ${Loja.falha() ? `<section><h3>Cópia recuperada</h3><p>Em uma abertura anterior os dados salvos não puderam ser lidos e o painel recomeçou do catálogo. O conteúdo original ficou guardado aqui.</p><div class="dd-b"><button type="button" class="btn" data-x="falha-baixar">${icone('baixar', 15)}Baixar cópia (.json)</button><button type="button" class="btn" data-x="falha-descartar">${icone('lixo', 15)}Descartar cópia</button></div></section>` : ''}
      <section><h3>Recomeçar</h3><p>Apaga tudo o que foi salvo neste navegador e recarrega o catálogo original com os dados de exemplo.</p><div class="dd-b"><button type="button" class="btn perigo" data-x="zerar">${icone('lixo', 15)}Recomeçar do catálogo original</button></div></section>
    </div>`, botoes: [{ n: 'Fechar', cls: 'pri' }],
    aoAbrir(el) {
      el.addEventListener('click', e => {
        const b = e.target.closest('[data-x]'); if (!b) return; const x = b.dataset.x;
        if (x === 'exportar') baixarArquivo(`biblioteca-lucas-backup-${iso(DB.hoje)}.json`, JSON.stringify(serializar(cfgAtual())), 'application/json');
        else if (x === 'importar') { Dlg.fechar(); $('#arq').click(); }
        else if (x === 'falha-baixar') baixarArquivo(`biblioteca-lucas-copia-recuperada-${iso(DB.hoje)}.json`, Loja.falha() || '', 'application/json');
        else if (x === 'falha-descartar') { Loja.descartarFalha(); Dlg.fechar(); toast('Cópia descartada.'); }
        else if (x === 'limpar') confirmar('Limpar dados de exemplo', 'Remover todas as datas, valores, leituras, e-books/audiolivros, itens da lista de compra e históricos de preço <b>simulados</b>?<br>Ficam o catálogo, a estante física e tudo o que você editou ou registrou.', 'Limpar', () => { removerExemplos(); S.sel = ''; S.avisoVisto = true; salvar(); fecharGaveta(); filtrosMudaram(); toast('Dados de exemplo removidos.'); });
        else if (x === 'restaurar') confirmar('Restaurar dados de exemplo', 'Gerar novamente os dados simulados para os livros que você ainda não editou?', 'Restaurar', () => { restaurarExemplos(); S.sel = ''; salvar(); filtrosMudaram(); toast('Dados de exemplo restaurados.'); });
        else if (x === 'zerar') confirmar('Recomeçar do catálogo original', 'Apagar <b>todas</b> as suas edições, cotações e livros adicionados e voltar ao estado inicial? Esta ação não pode ser desfeita.', 'Apagar tudo', () => { Loja.limpar(); DB.livros = gerarExemplos(livrosDoCatalogo(), DB.hoje); DB.exemplos = true; DB.criadoEm = DB.hoje; S.sel = ''; S.avisoVisto = false; limparFiltros(true); salvar(); fecharGaveta(); filtrosMudaram(); toast('Painel reiniciado.'); }, true);
      });
    } });
}

/* ───────── ações sobre um livro ───────── */
const defTag = (b, t, on) => { const i = b.tags.indexOf(t); if (on && i < 0) b.tags.push(t); if (!on && i >= 0) b.tags.splice(i, 1); };
function tocar(b) {                            // o item passa a ser "do usuário": não é mais tratado como exemplo
  b.u = 1; b.demo = 0; defTag(b, 'ja-tenho', b.col === 'acervo'); defTag(b, 'lido', b.leit === 'lido'); derivar(b);
  salvar(); render(); if (Gaveta.id === b.id) desenharGaveta();
}
function registrarCotacao(b, loja, preco, d) {
  if (!b.px) b.px = {};
  const pts = b.px[loja] || (b.px[loja] = []), i = pts.findIndex(p => p[0] === d);
  if (i >= 0) pts[i] = [d, preco, 1]; else { pts.push([d, preco, 1]); pts.sort((a, z) => a[0] - z[0]); }
  if (b.col !== 'acervo') b.track = true;
  salvar(); render(); if (Gaveta.id === b.id) desenharGaveta();
}
function apagarCotacao(b, loja, d) {            // só as cotações do usuário (as de exemplo saem em "Limpar dados de exemplo")
  const pts = b.px && b.px[loja], i = pts ? pts.findIndex(p => p[0] === d && p[2]) : -1; if (i < 0) return;
  const p = pts[i];
  confirmar('Apagar cotação', `Apagar a cotação de <b>${fBRL(p[1])}</b> em ${esc(loja)}, de ${fData(d)}?`, 'Apagar', () => {
    pts.splice(i, 1); if (!pts.length) delete b.px[loja];
    if (!Object.keys(b.px).length) { b.px = null; if (b.col === 'rec') b.track = false; }
    salvar(); render(); if (Gaveta.id === b.id) desenharGaveta(); toast('Cotação apagada.');
  }, true);
}
function formCotacao(host, o) {
  const el = document.createElement('div'); el.className = 'form cot';
  el.innerHTML = `${o.comLivro ? '<label class="cp c2"><span>Livro</span><select data-c="livro" aria-label="Livro"></select></label>' : ''}
    <label class="cp"><span>Loja</span><select data-c="loja">${Object.keys(LOJAS).map(n => `<option>${n}</option>`).join('')}<option value="__outra">Outra…</option></select></label>
    <label class="cp" data-outra hidden><span>Nome da loja</span><input data-c="outra" type="text" maxlength="40" placeholder="Ex.: Livraria da Vila"></label>
    <label class="cp"><span>Preço (R$)</span><input data-c="preco" type="text" inputmode="decimal" placeholder="0,00" autocomplete="off"></label>
    <label class="cp"><span>Data</span><input data-c="data" type="date" value="${iso(DB.hoje)}" max="${iso(DB.hoje)}"></label>
    <div class="c2 cot-a"><button type="button" class="btn pri" data-c="ok">${icone('mais', 15)}Registrar cotação</button></div>
    <div class="c2 lojas-b"></div>`;
  host.appendChild(el);
  const g = n => $(`[data-c="${n}"]`, el), links = $('.lojas-b', el);
  let lista = o.fixo ? [o.fixo] : [], atual = o.fixo || null;
  const pintarLinks = () => setHtml(links, atual ? `<span class="lb-t">Conferir preço de “${esc(atual.t.length > 34 ? atual.t.slice(0, 32) + '…' : atual.t)}”</span><div class="lb">${linksLojas(atual).map(([n, u]) => `<a href="${esc(u)}" target="_blank" rel="noopener noreferrer">${esc(n)}${icone('externo', 12)}</a>`).join('')}</div>${Loja.ok ? '' : '<span class="lb-n">Na pré-visualização os links externos podem não abrir; funcionam com o arquivo aberto no navegador.</span>'}` : '');
  const preferida = () => { if (atual) g('loja').value = virtual(atual) ? 'Kindle' : 'Amazon'; g('outra').closest('[data-outra]').hidden = true; };
  g('loja').addEventListener('change', () => { const outra = g('loja').value === '__outra'; g('outra').closest('[data-outra]').hidden = !outra; if (outra) g('outra').focus(); });
  if (o.comLivro) g('livro').addEventListener('change', () => { atual = lista.find(b => b.id === g('livro').value) || null; if (atual) { preferida(); if (o.aoEscolher) o.aoEscolher(atual); S.sel = atual.id; render(); } });
  const enviar = () => {
    if (!atual) { toast('Escolha um livro para registrar a cotação.', 'aviso'); return; }
    const loja = g('loja').value === '__outra' ? g('outra').value.trim() : g('loja').value, preco = lerValor(g('preco').value), d = deIso(g('data').value);
    if (!loja) return erroCampo(g('outra'), 'Informe o nome da loja.');
    if (preco == null || isNaN(preco) || preco <= 0) return erroCampo(g('preco'), 'Informe um preço válido, por exemplo 49,90.');
    if (d == null || d > DB.hoje) return erroCampo(g('data'), 'Informe uma data até hoje.');
    const b = atual; if (o.aoSalvar) o.aoSalvar(b);
    registrarCotacao(b, loja, preco, d);
    g('preco').value = ''; toast(`Cotação registrada: ${fBRL(preco)} · ${loja}.`);
  };
  g('ok').addEventListener('click', enviar);
  el.addEventListener('keydown', e => { if (e.key === 'Enter' && e.target.tagName === 'INPUT') { e.preventDefault(); enviar(); } });
  if (o.fixo) { preferida(); pintarLinks(); }
  return { el, atualizar(livros, sel) {
    lista = livros; const mudou = !atual || !sel || atual.id !== sel.id; atual = sel || null;
    if (o.comLivro) { setHtml(g('livro'), livros.length ? livros.slice().sort((a, z) => a.t.localeCompare(z.t, 'pt-BR')).map(b => `<option value="${b.id}">${esc(b.t)}${b.px ? '' : ' · sem cotação'}</option>`).join('') : '<option value="">Nenhum item na lista de compra</option>'); g('livro').value = atual ? atual.id : ''; g('livro').disabled = !livros.length; }
    g('ok').disabled = !atual; if (mudou) preferida(); pintarLinks();
  } };
}
function dlgCotacao(b) {
  Dlg.abrir({ titulo: 'Registrar cotação', corpo: `<p class="dlg-sub"><b>${esc(b.t)}</b>${b.a ? ' · ' + esc(b.a) : ''}</p><div id="dlg-cot"></div><p class="nota">O painel não consulta as lojas sozinho. Abra a busca, confira o preço e anote aqui: cada cotação entra no histórico do livro.</p>`, botoes: [{ n: 'Concluir', cls: 'pri' }],
    aoAbrir(el) { formCotacao($('#dlg-cot', el), { fixo: b }); } });
}
const opcoes = (pares, atual) => pares.map(([v, n]) => `<option value="${esc(v)}"${String(v) === String(atual ?? '') ? ' selected' : ''}>${esc(n)}</option>`).join('');
const LISTA_LOJAS = () => { const s = new Set(['Amazon', 'Estante Virtual', 'Mercado Livre', 'Travessa', 'Kindle', 'Kobo', 'Google Play Livros', 'Audible', 'Storytel', 'Livraria', 'Sebo', 'Feira do Livro', 'Presente']); for (const b of DB.livros) if (b.loja) s.add(b.loja); return [...s]; };
function dlgComprei(b, jaTinha) {
  const x = b.px ? melhorEm(b, DB.hoje) : null, fmt = b.fmt || 'fisico';
  Dlg.abrir({ titulo: jaTinha ? 'Já tenho este livro' : 'Registrar compra', corpo: `<p class="dlg-sub"><b>${esc(b.t)}</b>${b.a ? ' · ' + esc(b.a) : ''}</p>
    <div class="form">
      <label class="cp"><span>Formato</span><select data-f="fmt">${opcoes(Object.keys(FORMATOS).map(f => [f, FORMATOS[f].n]), fmt)}</select></label>
      <label class="cp"><span>${jaTinha ? 'Adquirido em (opcional)' : 'Data da compra'}</span><input data-f="adq" type="date" value="${jaTinha ? '' : iso(DB.hoje)}" max="${iso(DB.hoje)}"></label>
      <label class="cp"><span>Loja ou origem</span><input data-f="loja" type="text" list="dl-lojas" maxlength="40" value="${esc(!jaTinha && x ? x.f : '')}"><datalist id="dl-lojas">${LISTA_LOJAS().map(n => `<option value="${esc(n)}">`).join('')}</datalist></label>
      <label class="cp"><span>Valor pago (R$)</span><input data-f="pago" type="text" inputmode="decimal" placeholder="0,00" value="${!jaTinha && x ? valorCampo(x.p) : ''}"></label>
      <label class="cp"><span>Condição</span><select data-f="cond">${opcoes([['novo', 'Novo'], ['usado', 'Usado'], ['presente', 'Presente']], !jaTinha && x && x.f === 'Estante Virtual' ? 'usado' : 'novo')}</select></label>
    </div>`, botoes: [{ n: 'Cancelar' }, { n: 'Adicionar ao acervo', cls: 'pri', acao(el) {
      const g = n => $(`[data-f="${n}"]`, el), pago = lerValor(g('pago').value), adq = deIso(g('adq').value);
      if (pago != null && isNaN(pago)) return erroCampo(g('pago'), 'Informe um valor válido, por exemplo 49,90.');
      if (adq != null && adq > DB.hoje) return erroCampo(g('adq'), 'A data não pode estar no futuro.');
      const loja = g('loja').value.trim(), f = g('fmt').value;
      Object.assign(b, { col: 'acervo', fmt: f, plat: f === 'fisico' ? '' : loja, adq, pago, loja, cond: g('cond').value, track: false, prio: 0, leit: b.leit === 'lido' ? 'lido' : 'fila' });
      if (b.add == null) b.add = adq;
      tocar(b); toast('Adicionado ao acervo.');
    } }] });
}
function dlgLido(b) {
  Dlg.abrir({ titulo: 'Concluir leitura', corpo: `<p class="dlg-sub"><b>${esc(b.t)}</b>${b.a ? ' · ' + esc(b.a) : ''}</p>
    <div class="form"><label class="cp"><span>Concluído em</span><input data-f="em" type="date" value="${iso(DB.hoje)}" max="${iso(DB.hoje)}"></label>
    <label class="cp"><span>Nota</span><select data-f="nota">${opcoes([[0, 'Sem nota'], [5, '★★★★★  excelente'], [4, '★★★★  muito bom'], [3, '★★★  bom'], [2, '★★  regular'], [1, '★  fraco']], b.nota || 0)}</select></label></div>`,
    botoes: [{ n: 'Cancelar' }, { n: 'Marcar como lido', cls: 'pri', acao(el) {
      const em = deIso($('[data-f="em"]', el).value); if (em != null && em > DB.hoje) return erroCampo($('[data-f="em"]', el), 'A data não pode estar no futuro.');
      Object.assign(b, { leit: 'lido', lidoEm: em, prog: 100, nota: +$('[data-f="nota"]', el).value }); tocar(b); toast('Leitura concluída.');
    } }] });
}
function dlgProgresso(b) {
  Dlg.abrir({ titulo: 'Atualizar progresso', corpo: `<p class="dlg-sub"><b>${esc(b.t)}</b></p><div class="form"><label class="cp c2"><span>Quanto já leu: <b id="pg-v">${b.prog || 0}%</b></span><input data-f="prog" type="range" min="0" max="100" step="1" value="${b.prog || 0}"></label></div>`,
    botoes: [{ n: 'Cancelar' }, { n: 'Salvar', cls: 'pri', acao(el) { b.prog = +$('[data-f="prog"]', el).value; b.leit = 'lendo'; tocar(b); } }],
    aoAbrir(el) { $('[data-f="prog"]', el).addEventListener('input', e => { $('#pg-v', el).textContent = e.target.value + '%'; }); } });
}
function acao(b, a) {
  if (a === 'comprei') dlgComprei(b, false);
  else if (a === 'tenho') dlgComprei(b, true);
  else if (a === 'lido') dlgLido(b);
  else if (a === 'progresso') dlgProgresso(b);
  else if (a === 'ler') { b.leit = 'lendo'; if (b.prog >= 100) b.prog = 0; tocar(b); toast('Boa leitura!'); }
  else if (a === 'desejar') { Object.assign(b, { col: 'desejo', prio: b._top ? 1 : 2, fmt: b.fmt || 'fisico', track: true }); if (b.add == null) b.add = DB.hoje; tocar(b); toast(b.alvo ? 'Adicionado às próximas aquisições.' : 'Adicionado. Defina um preço-alvo em “Editar”.'); }
  else if (a === 'tirar') { Object.assign(b, { col: 'rec', prio: 0, fmt: '' }); tocar(b); toast('Voltou para as recomendações.'); }
  else if (a === 'cotar') dlgCotacao(b);
  else if (a === 'parar') { b.track = false; tocar(b); toast('Monitoramento pausado. O histórico foi mantido.'); }
  else if (a === 'monitorar') { b.track = true; tocar(b); toast('Preço em monitoramento.'); }
  else if (a === 'editar') dlgLivro(b);
  else if (a === 'excluir') confirmar('Excluir livro', `Excluir <b>${esc(b.t)}</b> do painel? Esta ação não pode ser desfeita.`, 'Excluir', () => { DB.livros = DB.livros.filter(x => x !== b); fecharGaveta(); salvar(); render(); toast('Livro excluído.'); }, true);
}

/* ───────── formulário de livro (novo / editar) ───────── */
function dlgLivro(b) {
  const novo = !b, o = b || novoLivro({ col: { biblioteca: 'acervo', desejos: 'desejo' }[S.visao] || 'rec', fmt: S.visao === 'recs' || S.visao === 'geral' ? '' : 'fisico', eixo: S.eixos.size === 1 ? [...S.eixos][0] : 5 });
  const v = x => esc(x ?? ''), outras = o.tags.filter(t => !TAGS_ESTRUTURA.has(t)).join(' ');
  Dlg.abrir({ titulo: novo ? 'Novo livro' : 'Editar livro', largo: true, corpo: `
    <div class="form" id="f-livro">
      <label class="cp c2"><span>Título</span><input data-f="t" type="text" maxlength="200" value="${v(o.t)}"></label>
      <label class="cp c2"><span>Autor</span><input data-f="a" type="text" maxlength="160" value="${v(o.a)}"></label>
      <label class="cp"><span>Lista</span><select data-f="col">${opcoes([['acervo', 'Acervo (já tenho)'], ['desejo', 'Próximas aquisições'], ['rec', 'Recomendações']], o.col)}</select></label>
      <label class="cp"><span>Eixo temático</span><select data-f="eixo">${opcoes(EIXOS.slice(1).map((e, i) => [i + 1, e.n]), o.eixo)}</select></label>
      <label class="cp c3"><span>Tipo</span><select data-f="tipo">${opcoes([['F', 'Ficção'], ['NF', 'Não ficção'], ['P', 'Poesia'], ['HQ', 'HQ'], ['ANT', 'Antologia'], ['X', 'Não informado']], o._tipo)}</select></label>
      <label class="cp c3"><span>Dificuldade</span><select data-f="d">${opcoes([[0, 'Não informada'], [1, 'Leve'], [2, 'Média'], [3, 'Exigente']], o._d)}</select></label>
      <label class="cp c3"><span>Extensão</span><select data-f="e">${opcoes([[0, 'Não informada'], [1, 'Curta (até ~250 p.)'], [2, 'Média (~250–500 p.)'], [3, 'Longa (500+ p. ou série)']], o._e)}</select></label>
      <fieldset class="c2 grp" data-g="acervo"><legend>No acervo</legend>
        <label class="cp c3"><span>Formato</span><select data-f="fmt">${opcoes(Object.keys(FORMATOS).map(f => [f, FORMATOS[f].n]), o.fmt || 'fisico')}</select></label>
        <label class="cp c3"><span>Adquirido em</span><input data-f="adq" type="date" value="${iso(o.adq)}" max="${iso(DB.hoje)}"></label>
        <label class="cp c3"><span>Valor pago (R$)</span><input data-f="pago" type="text" inputmode="decimal" placeholder="0,00" value="${valorCampo(o.pago)}"></label>
        <label class="cp c3"><span>Loja ou origem</span><input data-f="loja" type="text" list="dl-lojas" maxlength="40" value="${v(o.loja)}"><datalist id="dl-lojas">${LISTA_LOJAS().map(n => `<option value="${esc(n)}">`).join('')}</datalist></label>
        <label class="cp c3"><span>Condição</span><select data-f="cond">${opcoes([['', 'Não informada'], ['novo', 'Novo'], ['usado', 'Usado'], ['presente', 'Presente']], o.cond)}</select></label>
        <label class="cp c3"><span>Páginas</span><input data-f="pg" type="number" min="0" max="9999" inputmode="numeric" value="${o.pg || ''}"></label>
        <label class="cp c3"><span>Leitura</span><select data-f="leit">${opcoes([['', 'Não informada'], ['fila', 'Na fila'], ['lendo', 'Lendo'], ['lido', 'Lido'], ['aband', 'Abandonado']], o.leit)}</select></label>
        <label class="cp c3"><span>Progresso (%)</span><input data-f="prog" type="number" min="0" max="100" inputmode="numeric" value="${o.prog || ''}"></label>
        <label class="cp c3"><span>Concluído em</span><input data-f="lidoEm" type="date" value="${iso(o.lidoEm)}" max="${iso(DB.hoje)}"></label>
        <label class="cp c3"><span>Nota</span><select data-f="nota">${opcoes([[0, 'Sem nota'], [5, '★★★★★'], [4, '★★★★'], [3, '★★★'], [2, '★★'], [1, '★']], o.nota || 0)}</select></label>
      </fieldset>
      <fieldset class="c2 grp" data-g="desejo"><legend>Na lista de compra</legend>
        <label class="cp c3"><span>Prioridade</span><select data-f="prio">${opcoes([[1, 'Alta'], [2, 'Média'], [3, 'Baixa']], o.prio || 2)}</select></label>
        <label class="cp c3"><span>Formato desejado</span><select data-f="fmtD">${opcoes(Object.keys(FORMATOS).map(f => [f, FORMATOS[f].n]), o.fmt || 'fisico')}</select></label>
        <label class="cp c3"><span>Preço-alvo (R$)</span><input data-f="alvo" type="text" inputmode="decimal" placeholder="0,00" value="${valorCampo(o.alvo)}"></label>
        <label class="cp c3"><span>Preço de capa (R$)</span><input data-f="capa" type="text" inputmode="decimal" placeholder="opcional" value="${valorCampo(o.capa)}"></label>
      </fieldset>
      <fieldset class="c2 grp" data-g="rec"><legend>Na lista de recomendações</legend>
        <label class="cp c3"><span>Preço-alvo (R$)</span><input data-f="alvoR" type="text" inputmode="decimal" placeholder="opcional" value="${valorCampo(o.alvo)}"></label>
        <label class="cp chk c3x"><input data-f="top" type="checkbox"${o._top ? ' checked' : ''}><span>Prioridade de leitura (#top)</span></label>
      </fieldset>
      <label class="cp c2"><span>Marcadores <small>separados por espaço, sem #</small></span><input data-f="tags" type="text" value="${v(outras)}" autocomplete="off" spellcheck="false"></label>
      <label class="cp c2"><span>Observações</span><textarea data-f="obs" rows="2" maxlength="600">${v(o.obs)}</textarea></label>
    </div>`,
    botoes: [{ n: 'Cancelar' }, { n: novo ? 'Adicionar livro' : 'Salvar alterações', cls: 'pri', acao(el) {
      const g = n => $(`[data-f="${n}"]`, el), val = n => g(n).value.trim(), t = val('t');
      if (!t) return erroCampo(g('t'), 'Informe o título do livro.');
      const col = val('col'), dinheiro = {};
      for (const n of col === 'acervo' ? ['pago'] : col === 'desejo' ? ['alvo', 'capa'] : ['alvoR']) { dinheiro[n] = lerValor(val(n)); if (dinheiro[n] != null && isNaN(dinheiro[n])) return erroCampo(g(n), 'Informe um valor válido, por exemplo 49,90.'); }
      const x = b || novoLivro({ id: 'u' + Date.now().toString(36) + Math.floor(Math.random() * 1e3), sec: -1 });
      const conhecidas = new Map(); for (const y of DB.livros) for (const tg of y.tags) conhecidas.set(tg.toLowerCase(), tg);
      const extras = val('tags').split(/[\s,;]+/).map(s => s.replace(/^#/, '')).filter(Boolean).map(s => conhecidas.get(s.toLowerCase()) || norm(s).replace(/[^a-z0-9-]/g, '')).filter(s => s && !TAGS_ESTRUTURA.has(s));
      const TIPO_TAGS = ['F', 'NF', 'poesia', 'HQ', 'antologia'], tipoSel = val('tipo');
      const tipoTags = tipoSel === x._tipo && !novo ? x.tags.filter(s => TIPO_TAGS.includes(s)) : ({ F: ['F'], NF: ['NF'], P: ['poesia'], HQ: ['HQ'], ANT: ['antologia'], X: [] })[tipoSel];
      const d = +val('d'), e = +val('e'), top = col === 'rec' ? g('top').checked : x.tags.includes('top');
      x.t = t; x.a = val('a'); x.col = col; x.eixo = +val('eixo') || 5; x.obs = val('obs');
      x.tags = [...new Set([...tipoTags, d ? 'd' + d : '', e ? 'e' + e : '', ...extras, top ? 'top' : ''].filter(Boolean))];
      if (col === 'acervo') {
        const leit = val('leit'), f = val('fmt'), loja = val('loja');
        Object.assign(x, { fmt: f, loja, plat: f === 'fisico' ? '' : loja, adq: deIso(val('adq')), pago: dinheiro.pago, cond: val('cond'), pg: clamp(+val('pg') || 0, 0, 9999), leit, prog: leit === 'lido' ? 100 : clamp(Math.round(+val('prog') || 0), 0, 100), lidoEm: leit === 'lido' ? deIso(val('lidoEm')) : null, nota: +val('nota') || 0, prio: 0, track: false });
        if (x.add == null) x.add = x.adq;
      } else {
        Object.assign(x, { adq: null, pago: null, loja: '', plat: '', cond: '' });
        if (col === 'desejo') Object.assign(x, { prio: +val('prio') || 2, fmt: val('fmtD'), alvo: dinheiro.alvo, capa: dinheiro.capa, track: true });
        else Object.assign(x, { prio: 0, fmt: '', alvo: dinheiro.alvoR });
        if (x.add == null && (novo || col === 'desejo')) x.add = DB.hoje;
      }
      if (novo) DB.livros.push(x);
      tocar(x); toast(novo ? 'Livro adicionado.' : 'Alterações salvas.');
      if (novo) abrirLivro(x.id);
    } }],
    aoAbrir(el) {
      const sel = $('[data-f="col"]', el), troca = () => $$('[data-g]', el).forEach(f => { f.hidden = f.dataset.g !== sel.value; });
      sel.addEventListener('change', troca); troca();
    } });
}

/* ───────── gaveta de detalhes ───────── */
const Gaveta = { id: null, graf: null, antes: null };
function montarGaveta() {
  const el = $('#gaveta');
  el.innerHTML = `<div class="gv-fundo" data-fechar></div><aside class="gv-p" role="dialog" aria-modal="true" aria-label="Detalhes do livro" tabindex="-1">
    <header class="gv-h"><div class="gv-k" id="gv-k"></div><button type="button" class="ib" data-fechar aria-label="Fechar detalhes">${icone('fechar')}</button></header>
    <div class="gv-c"><div id="gv-topo"></div><div id="gv-estado"></div>
      <section id="gv-px" hidden><div class="gv-st"><h4>Preços</h4><span id="gv-pxs"></span></div><div id="gv-graf"></div><div class="legs" id="gv-leg"></div><div id="gv-fontes"></div></section>
      <div id="gv-resto"></div></div>
    <footer class="gv-a" id="gv-acoes"></footer></aside>`;
  Gaveta.graf = GraficoLinha($('#gv-graf'), { legenda: $('#gv-leg'), rotulo: 'Histórico de preço deste livro' });
  el.addEventListener('click', e => {
    if (e.target.closest('[data-fechar]')) { fecharGaveta(); return; }
    const b = porId(Gaveta.id); if (!b) return;
    const a = e.target.closest('[data-acao]'); if (a) { acao(b, a.dataset.acao); return; }
    const ap = e.target.closest('[data-apagar]'); if (ap) { apagarCotacao(b, ap.dataset.apagar, +ap.dataset.dia); return; }
    const tg = e.target.closest('[data-tag]'); if (tg) { fecharGaveta(); limparFiltros(false); S.tags.add(tg.dataset.tag); if (b.col === 'rec' && S.visao !== 'geral') irPara('recs'); else filtrosMudaram(); toast(`Filtrando por #${tg.dataset.tag}.`); return; }
    const ex = e.target.closest('[data-eixo]'); if (ex) { fecharGaveta(); limparFiltros(false); S.eixos.add(+ex.dataset.eixo); filtrosMudaram(); }
  });
}
function abrirLivro(id) {
  if (!porId(id)) return;
  const el = $('#gaveta'), aberta = el.classList.contains('on');
  if (!aberta) Gaveta.antes = document.activeElement;
  Gaveta.id = id; el.classList.add('on'); el.setAttribute('aria-hidden', 'false'); travar();
  desenharGaveta(); $('.gv-c', el).scrollTop = 0;
  if (!aberta) setTimeout(() => focar($('.gv-p', el)), 30);
}
function fecharGaveta() {
  const el = $('#gaveta'); if (!el.classList.contains('on')) return;
  el.classList.remove('on'); el.setAttribute('aria-hidden', 'true'); Gaveta.id = null; travar(); Tip.ocultar();
  if (Gaveta.antes && Gaveta.antes.focus && document.contains(Gaveta.antes)) try { Gaveta.antes.focus(); } catch (e) { /* nada */ }
}
function desenharGaveta() {
  const b = porId(Gaveta.id); if (!b) { fecharGaveta(); return; }
  const c = ctxAtual(), I = c.I, T = DB.hoje, x = c.px(b), fato = (r, v) => (v == null || v === '' ? '' : `<div><dt>${r}</dt><dd>${v}</dd></div>`);
  $('#gv-k').innerHTML = `<span class="pill col-${b.col}">${COLECOES[b.col].n}</span>${b.demo ? '<span class="pill ex" title="Datas, valores e preços deste item são simulados">dados de exemplo</span>' : ''}`;
  $('#gv-topo').innerHTML = `<h2>${esc(b.t)}</h2><p class="gv-a2">${esc(b.a || 'Autor não informado')}</p>
    <div class="gv-ch"><button type="button" class="tag lig" data-eixo="${b.eixo}" title="Filtrar por este eixo">${EIXOS[b.eixo] ? esc(EIXOS[b.eixo].n) : 'Sem eixo'}</button><span class="tag">${TIPOS[b._tipo].n}</span>${b._d ? `<span class="tag">${pontos(b._d)}${NIVEIS[b._d].n}</span>` : ''}${b._e ? `<span class="tag" title="${EXTENSOES[b._e].d}">${EXTENSOES[b._e].n} · ${EXTENSOES[b._e].d}</span>` : ''}${b._top ? `<span class="tag dest">${icone('estrela', 12)}Prioridade</span>` : ''}${b.tags.includes('sem-pt') ? '<span class="tag av">Sem edição em PT</span>' : ''}${b.tags.includes('verificar') ? '<span class="tag av">A verificar</span>' : ''}</div>`;
  let f = '';
  if (b.col === 'acervo') {
    f += fato('Formato', `<span class="fmt">${icone(ICONE_FMT[b.fmt] || 'livro', 14)}${FORMATOS[b.fmt] ? FORMATOS[b.fmt].n : '—'}</span>${b.plat ? ` <span class="mudo">· ${esc(b.plat)}</span>` : ''}`);
    f += fato('Adquirido em', b.adq == null ? '<span class="mudo">sem data</span>' : fData(b.adq));
    f += fato('Origem', b.loja ? esc(b.loja) + (b.cond && b.cond !== 'presente' ? ` <span class="mudo">· ${b.cond}</span>` : '') : '');
    f += fato('Valor pago', b.pago == null ? '' : b.pago === 0 ? (b.cond === 'presente' ? 'Presente' : 'Gratuito') : fBRL(b.pago));
    f += fato('Leitura', b.leit ? `<span class="pill leit-${b.leit}">${LEITURAS[b.leit].n}</span>${b.leit === 'lendo' || b.leit === 'aband' ? `<span class="li-prog gv"><span class="barra"><i style="width:${clamp(b.prog || 0, 0, 100)}%"></i></span><b class="num">${b.prog || 0}%</b></span>` : ''}` : '<span class="mudo">não informada</span>');
    if (b.leit === 'lido') { f += fato('Concluído em', b.lidoEm == null ? '<span class="mudo">sem data</span>' : fData(b.lidoEm)); f += fato('Nota', b.nota ? estrelas(b.nota) : ''); }
    f += fato('Páginas', b.pg ? (b.demo ? '~' : '') + fInt(b.pg) : '');
  } else {
    if (b.col === 'desejo') { f += fato('Prioridade', `<span class="prio p${b.prio || 0}"><i></i>${PRIORIDADES[b.prio || 0].n}</span>`); f += fato('Formato desejado', `<span class="fmt">${icone(ICONE_FMT[b.fmt] || 'livro', 14)}${FORMATOS[b.fmt] ? FORMATOS[b.fmt].n : 'Físico'}</span>`); }
    if (b.leit === 'lido') f += fato('Leitura', `<span class="pill leit-lido">Lido</span>`);
    f += fato('Melhor preço', x.hoje ? `<b class="num">${fBRL(x.hoje.p)}</b><span class="sub">${esc(x.hoje.f)}</span>` : b.col === 'desejo' ? '<span class="mudo">sem cotação</span>' : '');
    f += fato('Preço-alvo', b.alvo ? fBRL(b.alvo) : b.col === 'desejo' ? '<span class="mudo">não definido</span>' : '');
    if (x.hoje) f += fato('Situação', badgeSit(x.sit));
    f += fato('Preço de capa', b.capa ? fBRL(b.capa) + (b.demo ? ' <span class="mudo">· estimado</span>' : '') : '');
    f += fato('Incluído em', b.add == null ? '' : fData(b.add));
    if (b.col === 'rec' && b.px) f += fato('Monitoramento', b.track ? 'Ativo' : 'Pausado');
  }
  $('#gv-estado').innerHTML = f ? `<dl class="fatos">${f}</dl>` : '';

  const sec = $('#gv-px'), fontes = b.px ? Object.keys(b.px).filter(n => b.px[n].length) : [];
  sec.hidden = !fontes.length;
  if (!fontes.length) $('#gv-fontes').innerHTML = '';          // não deixa sobras do livro aberto antes
  if (fontes.length) {
    const prim = Math.min(...fontes.map(n => b.px[n][0][0])), ini = Math.max(I.de, prim), fim = I.ate, doFmt = fontesDe(b);
    let xs = [];
    if (fim >= ini) { const dias = new Set([ini, fim]); for (const n of fontes) for (const p of b.px[n]) if (p[0] > ini && p[0] < fim) dias.add(p[0]); xs = [...dias].sort((a, z) => a - z); }
    if (xs.length > 300) { const passo = xs.length / 300, y = []; for (let i = 0; i < 300; i++) y.push(xs[Math.floor(i * passo)]); y[y.length - 1] = xs[xs.length - 1]; xs = y; }
    $('#gv-pxs').textContent = (b.col === 'acervo' ? 'de quando estava na lista · ' : '') + (I.tudo ? 'desde a primeira cotação' : I.rot);
    Gaveta.graf.atualizar({ x: xs, zero: false, ordenarDica: true, fmtY: fBRL, fmtEixo: fBRLc, rot: i => rotEixoX(xs[i], fim - ini), tit: i => fDiaMesAno(xs[i]),
      series: fontes.map(n => ({ k: n, n, cor: corFonte(n), degrau: true, larg: 1.8, tracejado: !doFmt.includes(n), v: xs.map(d => { const o = precoEm(b.px[n], d); return o ? o[1] : null; }) })),
      refs: b.alvo ? [{ v: b.alvo, n: 'alvo', leg: 'Preço-alvo', cor: 'var(--good)' }] : [], vazio: 'Sem cotações neste período.' });
    const ord = fontes.map(n => ({ n, o: precoEm(b.px[n], T) })).filter(y => y.o).sort((a, z) => a.o[1] - z.o[1]), melhor = b.col !== 'acervo' && x.hoje ? x.hoje.f : null;
    $('#gv-fontes').innerHTML = `<table class="fontes"><thead><tr><th>Loja</th><th class="num">Último preço</th><th class="num">Cotado em</th></tr></thead><tbody>${ord.map(y => `<tr${y.n === melhor ? ' class="melhor"' : ''}><td><i class="pt" style="background:${corFonte(y.n)}"></i>${esc(y.n)}${doFmt.includes(y.n) ? '' : `<span class="mudo"> · ${tipoFonte(y.n) === 'virtual' ? 'e-book' : 'físico'}</span>`}</td><td class="num"><b>${fBRL(y.o[1])}</b></td><td class="num">${fData(y.o[0])}<span class="sub">${y.o[2] ? `cotação sua · <button type="button" class="lnk" data-apagar="${esc(y.n)}" data-dia="${y.o[0]}" aria-label="Apagar esta cotação de ${esc(y.n)}">apagar</button>` : 'exemplo'}</span></td></tr>`).join('')}</tbody></table>
      ${b.col === 'acervo' ? '' : `<button type="button" class="btn sm" data-acao="cotar">${icone('mais', 14)}Registrar cotação</button>`}`;
  }
  const outras = b.tags.filter(t => !['F', 'NF', 'd1', 'd2', 'd3', 'e1', 'e2', 'e3', 'top', 'ja-tenho', 'lido', 'sem-pt', 'verificar'].includes(t));
  $('#gv-resto').innerHTML = (b.col !== 'acervo' ? `<section><div class="gv-st"><h4>Buscar nas lojas</h4></div><div class="lb">${linksLojas(b).map(([n, u]) => `<a href="${esc(u)}" target="_blank" rel="noopener noreferrer">${esc(n)}${icone('externo', 12)}</a>`).join('')}</div>${Loja.ok ? '' : '<p class="nota">Na pré-visualização os links externos podem não abrir; funcionam com o arquivo aberto no navegador.</p>'}</section>` : '') +
    (outras.length ? `<section><div class="gv-st"><h4>Marcadores</h4><span>clique para filtrar</span></div><div class="gv-tags">${outras.map(t => `<button type="button" class="tag lig" data-tag="${esc(t)}">${esc(rotTag(t))}</button>`).join('')}</div></section>` : '') +
    (b.obs ? `<section><div class="gv-st"><h4>Observações</h4></div><p class="gv-obs">${esc(b.obs)}</p></section>` : '') +
    (b.demo ? `<p class="nota ex">${icone('info', 14)}<span>Título, autor, marcadores e eixo vêm do seu catálogo. ${b.col === 'acervo' ? 'Data, valor, origem, leitura e páginas' : b.px ? 'Datas, preço-alvo e histórico de preços' : 'A data de inclusão e as páginas'} deste item são <b>dados de exemplo</b>. Ao editar ou usar uma das ações abaixo, o item passa a ser tratado como seu.</span></p>` : '');
  const bt = (a, n, ic, cls) => `<button type="button" class="btn ${cls || ''}" data-acao="${a}">${ic ? icone(ic, 15) : ''}${n}</button>`;
  let ac = '';
  if (b.col === 'rec') ac = bt('desejar', 'Quero comprar', 'sacola', 'pri') + bt('tenho', 'Já tenho', 'check') + (b.px ? (b.track ? bt('parar', 'Pausar preço', 'sino') : bt('monitorar', 'Monitorar preço', 'sino')) : bt('cotar', 'Monitorar preço', 'sino'));
  else if (b.col === 'desejo') ac = bt('comprei', 'Comprei', 'check', 'pri') + (fontes.length ? '' : bt('cotar', 'Registrar cotação', 'etiqueta')) + bt('tirar', 'Tirar da lista', 'desfazer');
  else if (b.leit === 'lendo') ac = bt('lido', 'Concluir leitura', 'check', 'pri') + bt('progresso', 'Progresso', 'relogio');
  else if (b.leit === 'lido') ac = bt('ler', 'Reler', 'livro');
  else ac = bt('ler', 'Começar a ler', 'livro', 'pri') + bt('lido', 'Já li', 'check');
  $('#gv-acoes').innerHTML = ac + '<span class="esp"></span>' + (b.id[0] === 'u' ? `<button type="button" class="ib" data-acao="excluir" aria-label="Excluir livro" title="Excluir livro">${icone('lixo', 16)}</button>` : '') + bt('editar', 'Editar', 'lapis', 'fantasma');
}
