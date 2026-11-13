/* ───────────────────────── capas para muitos livros de uma vez, lidas da própria pasta ─────────────────────────
   Faltam capas e há arquivos sobrando na pasta. Este módulo percorre uma pasta escolhida pelo usuário, reconhece o
   livro de cada EPUB e CBZ pelo nome (o do arquivo ou o da pasta em que ele está) e põe a capa que vem dentro do
   arquivo no painel — todos de uma vez, sem internet: só os pedaços do pacote onde a capa mora são lidos, e nada é
   enviado a lugar nenhum.
   · só entra em livro que não tem capa nenhuma: quem tem capa enviada ou capa no catálogo é deixado em paz;
   · o arquivo em si não é guardado (aqui só se aproveita a capa); se o usuário quiser o arquivo junto do livro, anexa
     um por um na ficha;
   · um título nunca é adivinhado: quem reconhece o arquivo é o inventário da biblioteca (biblioteca-virtual/
     inventario.tsv, embutido como DIGITAIS_NOMES), onde o par "arquivo ↔ livro" foi conferido à mão. O que está fora
     dele só entra por casamento EXATO de título, e a pasta só vale nesse caso — as pastas da biblioteca são categorias
     de prateleira ("Filosofia", "psicologia"), não séries, e uma palavra dali bate em dezenas de livros;
   · no fim, a varredura diz em que ponto cada arquivo parou: capa lida, pacote sem capa dentro, pacote ilegível,
     imagem que não abriu, nenhum livro sem capa com esse nome, mais de um livro. Um "0 capas" mudo não diz nada;
   · um limite por execução (LOTE_MAX) mantém o backup e o banco do navegador em tamanho saudável — basta rodar de novo.
   O que faz o trabalho pesado está em 54-capa-digital (abrir o pacote) e em 55-anexos (guardar a capa e a
   lista de formatos que são o próprio livro). */
const LOTE_MAX = 400;                                                        // capas aproveitadas por execução
const CHAVE_MIN = 10;                                                        // "um título dentro do outro" só vale a partir disto
const LOTE_FASES = ['sem capa dentro', 'pacote ilegível', 'capa fora do pacote', 'capa grande demais', 'imagem que não abriu'];
                                                                             // os motivos que capaDoDigital devolve, na ordem em que aparecem no resumo

/* nome de arquivo ou de pasta → chave de comparação: sem extensão, sem numeração de edição, sem o ano, minúsculo e sem acento */
function chaveDeNome(s) {
  let x = String(s || '').replace(/\.[a-z0-9]{1,6}$/i, ' ');
  x = x.replace(/[([]\s*(?:19|20)\d\d\s*[)\]]\s*$/g, ' ');
  x = norm(x).replace(/[^a-z0-9]+/g, ' ').trim();
  x = x.replace(/^(?:v|t|no|n|#)?\d{1,4}\s+/, '').replace(/^\d{1,4}\s*[-–]\s*/, '').replace(/\s*[-–]\s*\d{1,4}$/, '');
  x = x.replace(/\s+\d{1,4}(?:\s+de\s+\d{1,4})?$/, '');
  return x.replace(/\s+/g, ' ').trim();
}
const caminhoDoArquivo = a => String((a && (a.webkitRelativePath || a.path)) || (a && a.name) || '').replace(/\\/g, '/');

/* arquivos da pasta → o que dá para aproveitar: pares {arquivo, livro}, e o que ficou de fora, com o motivo.
   Duas etapas, e a segunda é curta de propósito:
   1. DIGITAIS_NOMES — {nome do arquivo normalizado: posição da linha no catálogo} gerado do inventário por
      tools/build_catalog.py. O nome ali foi conferido à mão uma vez, então ele vale mais que qualquer heurística, e o
      mapa só contém livros sem capa: um arquivo que não está nele é de um livro que já tem capa (ou que ninguém
      conferiu) e não tem o que fazer aqui.
   2. o casamento exato com o título de um livro sem capa, pelo nome do arquivo ou pelo nome da pasta em que ele está
      (a pasta vale só para série guardada em pasta própria, e só quando bate inteiro). Sem isso, o arquivo é contado
      como não reconhecido — nunca lido por suposição. */
function planejarLote(arquivos, livros) {
  const digitais = (arquivos || []).filter(a => a && DIGITAL_CAPA.test(a.name || '') && a.size > 0);
  const semCapa = (livros || []).filter(b => !b.cp && !temCapa(b));
  const porLinha = new Map();                                          // 'c37' é a linha 37 do catálogo: é por ela que o mapa aponta
  for (const b of semCapa) { const m = /^c(\d+)$/.exec(b.id || ''); if (m) porLinha.set(+m[1], b); }   // o id de um livro do catálogo é 'c' + a posição da linha
  const mapa = (typeof DIGITAIS_NOMES === 'object' && DIGITAIS_NOMES) || {};
  const chaves = semCapa.map(b => ({ b, c: chaveDeNome(b.t) })).filter(x => x.c);
  const exatas = new Map();
  for (const x of chaves) { const l = exatas.get(x.c) || []; l.push(x.b); exatas.set(x.c, l); }
  const usados = new Set(), pares = [], ambigueis = [], semLivro = [], repetidos = [], comCapa = [];
  for (const a of digitais) {
    const partes = caminhoDoArquivo(a).split('/'), base = partes.pop() || a.name;
    const i = mapa[norm(base)];
    if (typeof i === 'number') {                                       // etapa 1: o inventário reconheceu o arquivo
      const b = porLinha.get(i);
      if (!b) { comCapa.push(a.name); continue; }                      // a linha não está mais entre as sem capa (capa chegada entretanto, ou mapa desatualizado)
      if (usados.has(b.id)) { repetidos.push(a.name); continue; }      // dois arquivos para o mesmo livro: fica o primeiro
      usados.add(b.id); pares.push({ arq: a, livro: b, certo: true }); continue;
    }
    const chavesDoArquivo = [chaveDeNome(base), partes.length ? chaveDeNome(partes[partes.length - 1]) : ''].filter(Boolean);
    let escolha = null, motivo = '';
    for (const c of new Set(chavesDoArquivo)) {                        // etapa 2: só comparação exata, nome do arquivo e depois a pasta
      const l = exatas.get(c) || [];
      if (l.length === 1) { escolha = l[0]; break; }
      if (l.length > 1 && !motivo) motivo = 'mais de um livro tem este título';
    }
    if (!escolha && !motivo) {                                         // um título dentro do nome do arquivo, quando o nome é longo o bastante — nunca pelo nome da pasta
      const c = chavesDoArquivo[0];
      if (c) {
        const batem = [...new Set(chaves.filter(x => { const [curto, longo] = x.c.length <= c.length ? [x.c, c] : [c, x.c];
          return longo.startsWith(curto) ? curto.length >= 6 : curto.length >= CHAVE_MIN && longo.includes(curto);
        }).map(x => x.b.id))];
        if (batem.length === 1) escolha = semCapa.find(b => b.id === batem[0]);
        else if (batem.length > 1) motivo = 'mais de um livro combina com este nome';
      }
    }
    if (escolha && usados.has(escolha.id)) { repetidos.push(a.name); continue; }   // a primeira capa da série fica, as outras não
    if (escolha) { usados.add(escolha.id); pares.push({ arq: a, livro: escolha }); }
    else (motivo ? ambigueis : semLivro).push({ nome: a.name, motivo: motivo || 'nenhum livro sem capa com este nome' });
  }
  return { pares, ambigueis, semLivro, repetidos, comCapa, totais: { arquivos: (arquivos || []).length, digitais: digitais.length, semCapa: semCapa.length } };
}

const LoteCapas = {
  emCurso: false, parar: false, st: null, fora: null,
  escolher() {
    if (this.emCurso) { toast('A busca por capas já está em andamento.', 'aviso'); return; }
    const i = document.createElement('input');
    i.type = 'file'; i.hidden = true; i.multiple = true; i.setAttribute('aria-hidden', 'true'); i.setAttribute('webkitdirectory', ''); i.setAttribute('directory', '');
    if (!('webkitdirectory' in i)) { toast('Este navegador não permite escolher uma pasta inteira. Na ficha de cada livro, “Anexar arquivo…” aceita o EPUB ou o CBZ dele, e a capa é lida do mesmo jeito.', 'aviso'); return; }
    i.addEventListener('change', () => { const arqs = [...(i.files || [])]; i.remove(); this.rodar(arqs); });      // o input sai de cena: a lista fica só na memória
    document.body.appendChild(i); i.click();
  },
  async rodar(arquivos) {
    const plano = planejarLote(arquivos, DB.livros);
    if (!plano.totais.arquivos) { toast('A pasta escolhida não tem arquivo nenhum.', 'aviso'); return; }
    if (!plano.totais.digitais) { toast(`Nenhum EPUB ou CBZ na pasta escolhida (${plural(plano.totais.arquivos, 'arquivo', 'arquivos')}).`, 'aviso'); return; }
    if (!plano.pares.length) {
      toast(plano.totais.semCapa ? `Foram ${plural(plano.totais.digitais, 'livro digital', 'livros digitais')} na pasta, mas nenhum corresponde a um dos ${fInt(plano.totais.semCapa)} livros sem capa: o nome dos arquivos não está na lista da biblioteca virtual (biblioteca-virtual/inventario.tsv) e não bate com nenhum título. Rode tools/importar_digital.py e depois tools/build.py, e tente de novo.` : 'Todos os livros do painel já têm capa.', 'aviso');
      return;
    }
    const lote = plano.pares.slice(0, LOTE_MAX), faltam = plano.pares.length - lote.length;
    this.emCurso = true; this.parar = false;
    Dlg.abrir({ titulo: 'Buscando as capas nos seus arquivos', largo: true, corpo:
      `<p class="dlg-sub">${plural(lote.length, 'livro', 'livros')} para percorrer · a capa é lida do próprio arquivo, neste navegador, e nada é enviado à internet.</p>
       <p class="nota" id="lt-st" role="status" aria-live="polite">Lendo…</p>
       <p class="nota" id="lt-fora" hidden></p>
       <p class="nota">Só entram EPUB e CBZ de livro sem capa: uma capa enviada por você ou vinda do catálogo nunca é trocada, e os outros formatos ficam quietos. O arquivo em si continua fora do painel — aqui se aproveita apenas a capa. ${faltam ? `Por enquanto são ${fInt(LOTE_MAX)} por execução: ${plural(faltam, 'livro fica', 'livros ficam')} para a próxima — basta rodar de novo.` : ''}</p>`,
      botoes: [{ n: 'Parar', acao: () => { LoteCapas.parar = true; return false; } }, { n: 'Fechar', cls: 'pri' }],
      aoAbrir(el) { LoteCapas.st = $('#lt-st', el); LoteCapas.fora = $('#lt-fora', el); } });
    let feitos = [], lidos = 0;
    const fases = {};                                                  // em que ponto cada arquivo parou: é o que o resumo conta
    const marca = m => { fases[m] = (fases[m] || 0) + 1; };
    try {
      for (const p of lote) {
        if (this.parar || !this.st || !this.st.isConnected) { this.parar = true; break; }   // fechar o quadro interrompe: nada continua às escondidas
        lidos++;
        if (p.livro.cp) continue;                                        // o livro ganhou capa pelo caminho de sempre entretanto
        const achada = await capaDoDigital(p.arq);
        if (!achada || !achada.blob) { marca((achada && achada.motivo) || 'pacote ilegível'); continue; }   // casou com o livro, mas o pacote não traz nada aproveitável: o livro fica como está, e aparece no resumo
        try {
          const dados = await reduzirImagem(achada.blob);
          if (p.livro.cp) { marca('o livro já tinha capa quando fomos guardar'); continue; }
          const [k] = await Notas.gravarCapa(p.livro, dados, 'capa de ' + achada.nome);
          if (k && !p.livro.cp) { p.livro.cp = k; marcarMeu(p.livro); feitos.push(p.livro.t); }
          else marca('não coube no arquivo de anotações');
        } catch (e) { marca('imagem que não abriu'); }                 // o navegador não conseguiu recortar/redimensionar: o livro fica sem capa, como estava
        if (this.st) this.st.textContent = `Lidos ${fInt(lidos)} de ${fInt(lote.length)} · ${plural(feitos.length, 'capa encontrada', 'capas encontradas')}${feitos.length ? ': ' + esc(feitos[feitos.length - 1]) : ''}`;
        if (!(lidos % 20)) salvar();                                     // o que já foi achado fica gravado, mesmo se a aba se fechar
        await new Promise(r => setTimeout(r, 0));                        // respira: a tela não congela durante a varredura
      }
    } finally { this.emCurso = false; }                                // o que quer que aconteça, o painel volta a deixar buscar
    salvar(); render(); if (Gaveta.id) desenharGaveta();
    const dasFases = LOTE_FASES.concat(Object.keys(fases).filter(m => !LOTE_FASES.includes(m)))
      .filter(m => fases[m]).map(m => `${plural(fases[m], 'arquivo', 'arquivos')} · ${m}`);
    const resumo = `${plural(feitos.length, 'capa encontrada', 'capas encontradas')} em ${plural(lidos, 'arquivo lido', 'arquivos lidos')}`
      + (this.parar && lidos < lote.length ? ` · parado antes do fim, ${fInt(lote.length - lidos)} ficaram para depois` : '')
      + (plano.comCapa.length ? ` · ${plural(plano.comCapa.length, 'arquivo', 'arquivos')} de livro que já tem capa` : '')
      + (plano.repetidos.length ? ` · ${plural(plano.repetidos.length, 'arquivo repetido', 'arquivos repetidos')} (o mesmo livro mais de uma vez)` : '')
      + (plano.ambigueis.length ? ` · ${plural(plano.ambigueis.length, 'nome com mais de um livro', 'nomes com mais de um livro')} deixados em paz` : '')
      + (plano.semLivro.length ? ` · ${plural(plano.semLivro.length, 'arquivo', 'arquivos')} sem livro correspondente` : '')
      + (dasFases.length ? ' · ' + dasFases.join(' · ') : '');
    if (this.st) this.st.textContent = resumo + (feitos.length ? ' · exporte o backup em “Seus dados” para levar as capas junto.' : '');
    const ficouFora = plano.semLivro.concat(plano.ambigueis).slice(0, 12);
    const elFora = this.fora && this.fora.isConnected ? this.fora : null;   // a lista dos que ficaram de fora vive no quadro: fechou o quadro, fechou a conta
    if (elFora && ficouFora.length) {                                  // os nomes que não conseguimos ligar a um livro: é olhando-os que a lista dele (e o mapa) se corrigem
      elFora.hidden = false;
      elFora.innerHTML = `<b>${plural(plano.semLivro.length + plano.ambigueis.length, 'arquivo ficou', 'arquivos ficaram')} fora, sem livro certo:</b> `
        + ficouFora.map(x => esc(`${x.nome} — ${x.motivo}`)).join(' · ')
        + (plano.semLivro.length + plano.ambigueis.length > ficouFora.length ? ` · e mais ${fInt(plano.semLivro.length + plano.ambigueis.length - ficouFora.length)}` : '')
        + '. Um nome que não está na lista da biblioteca virtual é deixado em paz de propósito: nada é casado por suposição.';
    }
    toast(resumo + (Loja.ok ? '' : ' — nesta pré-visualização nada é gravado: as capas valem até fechar a página') + '.', feitos.length ? 'ok' : 'aviso');
  },
};
