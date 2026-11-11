/* ───────────────────────── listas para levar: imprimir e copiar como texto ─────────────────────────
   Uma "folha" é uma lista do painel pronta para sair dele — a tabela que está na tela (com os filtros, a aba, a busca e a
   ordem dela) ou uma trilha de leitura:
     { titulo, desc, meta: [linhas do cabeçalho], cols: [[nome, classe]], numerar,
       itens: [{ ok: já li, top: é prioridade, cel: [texto de cada coluna], txt: a linha na versão em texto }], notas: [linhas] }
   "Imprimir" monta a folha em #impressao — um bloco que só existe no papel — e abre a caixa de impressão do navegador, que
   também salva em PDF. "Copiar" põe a mesma lista, em texto simples e numerada, na área de transferência.
   Nada sai do navegador: quem leva a lista para fora é o usuário. */
const PAGINAS_SEM_PERGUNTAR = 8;        // folha maior que isso: o painel diz quantas páginas são e pergunta antes de imprimir
/* Quantas páginas A4 a folha dá, mais ou menos. Em vez de chutar pelo número de linhas (um título comprido ocupa duas), a
   folha é montada fora da tela, na largura útil do papel, e medida. A altura útil de cada página desconta as margens (as do
   @page, em styles.css), o cabeçalho da tabela, que se repete, e a sobra da linha que não coube inteira (ver listas.py). */
const PAGINA_UTIL_MM = 297 - 14 - 15 - 9;
function paginasDaFolha(f) {
  const el = $('#impressao'), antes = el.innerHTML;
  el.innerHTML = folhaHtml(f); el.classList.add('medindo');
  const mm = el.offsetHeight * 25.4 / 96;
  el.classList.remove('medindo'); el.innerHTML = antes;
  return Math.max(1, Math.ceil(mm / PAGINA_UTIL_MM));
}
const marcaDaFolha = () => 'Biblioteca do Lucas · ' + fData(DB.hoje);

// a estrela de prioridade e o visto de "já li" são desenhados (não são letras): saem iguais em qualquer máquina, com qualquer fonte
const ESTRELA_FOLHA = `<svg class="imp-e" viewBox="0 0 24 24" aria-hidden="true">${IC.estrela}</svg>`;
function folhaHtml(f) {
  const cols = (f.numerar ? [['Nº', 'n']] : []).concat(f.cols);
  const linha = (it, i) => `<tr><td class="q"><span class="imp-q${it.ok ? ' ok' : ''}"></span></td>${f.numerar ? `<td class="n">${i + 1}</td>` : ''}${it.cel.map((c, j) => `<td class="${f.cols[j][1]}">${esc(c)}${it.top && f.cols[j][1] === 't' ? ESTRELA_FOLHA : ''}</td>`).join('')}</tr>`;
  const legenda = [f.itens.some(it => it.top) ? `${ESTRELA_FOLHA} prioridade` : '', f.itens.some(it => it.ok) ? '<span class="imp-q ok"></span> já li' : ''].filter(Boolean);
  return `<p class="imp-m">${esc(marcaDaFolha())}</p><h1>${esc(f.titulo)}</h1>${f.desc ? `<p class="imp-d">${esc(f.desc)}</p>` : ''}${f.meta.map(l => `<p class="imp-i">${esc(l)}</p>`).join('')}
    <table class="imp-l"><thead><tr><th class="q"></th>${cols.map(c => `<th class="${c[1]}">${esc(c[0])}</th>`).join('')}</tr></thead><tbody>${f.itens.map(linha).join('')}</tbody></table>
    ${legenda.length ? `<p class="imp-n imp-leg">${legenda.join('<i></i>')}</p>` : ''}${(f.notas || []).map(l => `<p class="imp-n">${esc(l)}</p>`).join('')}`;
}
const folhaTexto = f => [f.titulo, marcaDaFolha()].concat(f.desc ? [f.desc] : [], f.meta).join('\n') + '\n\n' + f.itens.map((it, i) => `${i + 1}. ${it.txt}`).join('\n') + ((f.notas || []).length ? '\n\n' + f.notas.join('\n') : '') + '\n';

// a lista num campo de texto, para copiar à mão: quando o navegador não deixa copiar nem imprimir sozinho
function folhaNaMao(f, titulo, recado) {
  Dlg.abrir({ titulo, largo: true, corpo: `<p class="nota">${recado}</p><textarea class="copia" readonly rows="14" data-foco aria-label="A lista, em texto">${esc(folhaTexto(f))}</textarea>`,
    botoes: [{ n: 'Fechar' }, { n: 'Selecionar tudo', cls: 'pri', acao: el => { $('textarea', el).select(); try { if (document.execCommand('copy')) toast('Lista copiada.'); } catch (e) { /* fica selecionada: Ctrl+C copia */ } return false; } }] });
}

/* Imprimir. A folha fica montada até o navegador avisar que a impressão terminou; aí some, e a página volta a ser a de sempre.
   Enquanto ela existe, o título da página é o da lista — é o nome que o navegador sugere para o PDF. */
let desfazerFolha = null;
function imprimirFolha(f) {
  const n = f.itens.length;
  if (!n) { toast('Não há linhas para imprimir.', 'aviso'); return; }
  // pré-visualização dentro de outra página, sem armazenamento: ali o navegador ignora o pedido de impressão, sem avisar
  if (!Loja.ok && window.top !== window.self) { folhaNaMao(f, 'Imprimir a lista', 'Esta pré-visualização não deixa imprimir. Abra o painel direto no navegador — ou copie a lista abaixo e cole num editor de texto.'); return; }
  const ir = () => {
    if (desfazerFolha) desfazerFolha();
    const el = $('#impressao'), raiz = document.documentElement, titulo = document.title;
    el.innerHTML = folhaHtml(f); raiz.classList.add('imprimindo'); document.title = `${f.titulo} — Biblioteca do Lucas`;
    const fim = desfazerFolha = () => {
      if (desfazerFolha !== fim) return;
      desfazerFolha = null; raiz.classList.remove('imprimindo'); el.innerHTML = ''; document.title = titulo;
      window.removeEventListener('afterprint', fim); document.removeEventListener('pointerdown', fim, true); document.removeEventListener('keydown', fim, true);
    };
    window.addEventListener('afterprint', fim);
    // há navegador de celular que não avisa o fim da impressão: o primeiro toque ou tecla depois dela desfaz a folha
    setTimeout(() => { if (desfazerFolha === fim) { document.addEventListener('pointerdown', fim, true); document.addEventListener('keydown', fim, true); } }, 800);
    try { window.print(); } catch (e) { fim(); toast('Este navegador não abriu a caixa de impressão.', 'aviso'); }
  };
  const pags = n > 60 ? paginasDaFolha(f) : 1;        // até 60 linhas não chega perto do limite: nem mede
  if (pags > PAGINAS_SEM_PERGUNTAR) confirmar('Imprimir uma lista longa', `Esta lista tem <b>${fInt(n)} livros</b>: no papel, umas <b>${fInt(pags)} páginas</b>. Para uma folha menor, filtre a lista antes de imprimir.`, 'Imprimir assim mesmo', () => { setTimeout(ir, 60); });
  else ir();
}

/* Copiar como texto. Primeiro pela área de transferência do navegador; se ele não deixar (página aberta de um arquivo num
   navegador antigo, pré-visualização), pelo comando antigo; se nem assim, mostra o texto para copiar à mão. */
function copiarFolha(f) {
  const n = f.itens.length;
  if (!n) { toast('Não há linhas para copiar.', 'aviso'); return; }
  const txt = folhaTexto(f), pronto = () => toast(`Lista copiada: ${plural(n, 'livro', 'livros')}. Agora é só colar onde quiser.`);
  const antigo = () => {
    const foco = document.activeElement, ta = document.createElement('textarea');
    ta.value = txt; ta.setAttribute('readonly', ''); ta.setAttribute('aria-hidden', 'true'); ta.tabIndex = -1; ta.style.cssText = 'position:fixed;top:0;left:0;width:1px;height:1px;opacity:0';
    document.body.appendChild(ta); ta.select();
    let ok = false; try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
    ta.remove(); if (foco && foco.focus) try { foco.focus({ preventScroll: true }); } catch (e) { /* nada */ }
    return ok;
  };
  const resto = () => { if (antigo()) pronto(); else folhaNaMao(f, 'Copiar a lista', 'O navegador não deixou copiar sozinho. Use “Selecionar tudo” e copie (Ctrl+C).'); };
  // dentro de uma página que proíbe a área de transferência (pré-visualizações), nem se pede: o navegador registraria um erro
  const politica = document.permissionsPolicy || document.featurePolicy;
  let barrada = false; try { barrada = !!politica && !!politica.allowsFeature && !politica.allowsFeature('clipboard-write'); } catch (e) { barrada = false; }
  let p = null;
  if (!barrada) try { p = navigator.clipboard && navigator.clipboard.writeText ? navigator.clipboard.writeText(txt) : null; } catch (e) { p = null; }
  if (p && p.then) p.then(pronto, resto); else resto();
}

/* a folha de uma trilha de leitura: os livros na ordem do roteiro, com o que tenho, o que li e o que falta */
function folhaDaTrilha(t, x) {
  return { titulo: `Trilha ${t.n} · ${t.nome}`, desc: t.desc, meta: [maiuscula(frasesTrilha(x))], numerar: true, cols: [['Título', 't'], ['Autor', 'a'], ['Situação', 'x']],
    itens: x.vis.map(b => { const rot = estadoNaTrilha(b)[1]; return { ok: b.leit === 'lido', cel: [b.t, b.a || '', rot], txt: `${b.t}${b.a ? ' — ' + b.a : ''} (${rot.toLowerCase()})` }; }),
    notas: ['A ordem é a sugerida no catálogo da biblioteca.'].concat(x.esc ? [`${x.esc === 1 ? 'Não entra 1 livro desta trilha, que está oculto' : `Não entram ${x.esc} livros desta trilha, que estão ocultos`} (${regrasFora().join(' · ')}).`] : []) };
}
