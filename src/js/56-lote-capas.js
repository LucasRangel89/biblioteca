/* ───────────────────────── capas para muitos livros de uma vez, lidas da própria pasta ─────────────────────────
   Faltam capas e há arquivos sobrando na pasta. Este módulo percorre uma pasta escolhida pelo usuário, reconhece o
   livro de cada EPUB e CBZ pelo nome (o do arquivo ou o da pasta em que ele está) e põe a capa que vem dentro do
   arquivo no painel — todos de uma vez, sem internet: só os pedaços do pacote onde a capa mora são lidos, e nada é
   enviado a lugar nenhum.
   · só entra em livro que não tem capa nenhuma: quem tem capa enviada ou capa no catálogo é deixado em paz;
   · o arquivo em si não é guardado (aqui só se aproveita a capa); se o usuário quiser o arquivo junto do livro, anexa
     um por um na ficha;
   · um título nunca é adivinhado: nomes que não batem, ou que batem em mais de um livro, ficam de fora e são contados;
   · um limite por execução (LOTE_MAX) mantém o backup e o banco do navegador em tamanho saudável — basta rodar de novo.
   O que faz o trabalho pesado está em 54-capa-digital (abrir o pacote) e em 55-anexos (guardar a capa e a
   lista de formatos que são o próprio livro). */
const LOTE_MAX = 400;                                                        // capas aproveitadas por execução
const CHAVE_MIN = 10;                                                        // "um título dentro do outro" só vale a partir disto

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

/* arquivos da pasta → o que dá para aproveitar: pares {arquivo, livro}, e o que ficou de fora com o motivo */
function planejarLote(arquivos, livros) {
  const digitais = (arquivos || []).filter(a => a && DIGITAL_CAPA.test(a.name || '') && a.size > 0);
  const semCapa = (livros || []).filter(b => !b.cp && !temCapa(b));
  const chaves = semCapa.map(b => ({ b, c: chaveDeNome(b.t) })).filter(x => x.c);
  const exatas = new Map();
  for (const x of chaves) { const l = exatas.get(x.c) || []; l.push(x.b); exatas.set(x.c, l); }
  const usados = new Set(), pares = [], ambigueis = [], semLivro = [], repetidos = [];
  for (const a of digitais) {
    const partes = caminhoDoArquivo(a).split('/'), base = partes.pop() || a.name;
    const chavesDoArquivo = [chaveDeNome(base), partes.length ? chaveDeNome(partes.pop()) : ''].filter(Boolean);
    let escolha = null, motivo = '';
    for (const c of chavesDoArquivo) {                          // primeiro o que bate exatamente com um título do catálogo
      const l = exatas.get(c) || [];
      if (l.length === 1) { escolha = l[0]; break; }
      if (l.length > 1) { motivo = 'mais de um livro tem este título'; break; }
    }
    if (!escolha && !motivo) {                                  // e, se não bate, um título dentro do outro (nomes longos o bastante)
      for (const c of chavesDoArquivo) {
        const batem = [...new Set(chaves.filter(x => { const [curto, longo] = x.c.length <= c.length ? [x.c, c] : [c, x.c];   // um título que abre o nome do arquivo, ou aparece dentro dele
          return longo.startsWith(curto) ? curto.length >= 6 : curto.length >= CHAVE_MIN && longo.includes(curto);
        }).map(x => x.b.id))];
        if (batem.length === 1) { escolha = semCapa.find(b => b.id === batem[0]); break; }
        if (batem.length > 1) { motivo = 'mais de um livro combina com este nome'; break; }
      }
    }
    if (escolha && usados.has(escolha.id)) { repetidos.push(a.name); continue; }   // a primeira imagem da série fica, as outras não
    if (escolha) { usados.add(escolha.id); pares.push({ arq: a, livro: escolha }); }
    else (motivo ? ambigueis : semLivro).push({ nome: a.name, motivo });
  }
  return { pares, ambigueis, semLivro, repetidos, totais: { arquivos: (arquivos || []).length, digitais: digitais.length, semCapa: semCapa.length } };
}

const LoteCapas = {
  emCurso: false, parar: false, st: null,
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
      toast(plano.totais.semCapa ? `Foram ${plural(plano.totais.digitais, 'livro digital', 'livros digitais')} na pasta, mas nenhum foi reconhecido entre os ${fInt(plano.totais.semCapa)} livros sem capa. Confira o nome dos arquivos.` : 'Todos os livros do painel já têm capa.', 'aviso');
      return;
    }
    const lote = plano.pares.slice(0, LOTE_MAX), faltam = plano.pares.length - lote.length;
    this.emCurso = true; this.parar = false;
    Dlg.abrir({ titulo: 'Buscando as capas nos seus arquivos', largo: true, corpo:
      `<p class="dlg-sub">${plural(lote.length, 'livro', 'livros')} para percorrer · a capa é lida do próprio arquivo, neste navegador, e nada é enviado à internet.</p>
       <p class="nota" id="lt-st" role="status" aria-live="polite">Lendo…</p>
       <p class="nota">Só entram livros sem capa: uma capa enviada por você ou vinda do catálogo nunca é trocada. O arquivo em si continua fora do painel — aqui se aproveita apenas a capa. ${faltam ? `Por enquanto são ${fInt(LOTE_MAX)} por execução: ${plural(faltam, 'livro fica', 'livros ficam')} para a próxima — basta rodar de novo.` : ''}</p>`,
      botoes: [{ n: 'Parar', acao: () => { LoteCapas.parar = true; return false; } }, { n: 'Fechar', cls: 'pri' }],
      aoAbrir(el) { LoteCapas.st = $('#lt-st', el); } });
    let feitos = [], lidos = 0;
    try {
      for (const p of lote) {
        if (this.parar || !this.st || !this.st.isConnected) { this.parar = true; break; }   // fechar o quadro interrompe: nada continua às escondidas
        lidos++;
        if (p.livro.cp) continue;                                        // o livro ganhou capa pelo caminho de sempre entretanto
        const achada = await capaDoDigital(p.arq);
        if (achada && !p.livro.cp) {
          try {
            const dados = await reduzirImagem(achada.blob);
            const [k] = await Notas.gravarCapa(p.livro, dados, 'capa de ' + achada.nome);
            if (k && !p.livro.cp) { p.livro.cp = k; marcarMeu(p.livro); feitos.push(p.livro.t); }
          } catch (e) { /* imagem que o navegador não abre: o livro fica sem capa, como estava */ }
        }
        if (this.st) this.st.textContent = `Lidos ${fInt(lidos)} de ${fInt(lote.length)} · ${plural(feitos.length, 'capa encontrada', 'capas encontradas')}${feitos.length ? ': ' + esc(feitos[feitos.length - 1]) : ''}`;
        if (!(lidos % 20)) salvar();                                     // o que já foi achado fica gravado, mesmo se a aba se fechar
        await new Promise(r => setTimeout(r, 0));                        // respira: a tela não congela durante a varredura
      }
    } finally { this.emCurso = false; }                                // o que quer que aconteça, o painel volta a deixar buscar
    salvar(); render(); if (Gaveta.id) desenharGaveta();
    const resumo = `${plural(feitos.length, 'capa encontrada', 'capas encontradas')} em ${plural(lidos, 'arquivo lido', 'arquivos lidos')}`
      + (this.parar && lidos < lote.length ? ` · parado antes do fim, ${fInt(lote.length - lidos)} ficaram para depois` : '')
      + (plano.ambigueis.length ? ` · ${plural(plano.ambigueis.length, 'nome com mais de um livro', 'nomes com mais de um livro')} deixados em paz` : '')
      + (plano.semLivro.length ? ` · ${plural(plano.semLivro.length, 'arquivo', 'arquivos')} sem livro correspondente` : '');
    if (this.st) this.st.textContent = resumo + (feitos.length ? ' · exporte o backup em “Seus dados” para levar as capas junto.' : '');
    toast(resumo + (Loja.ok ? '' : ' — nesta pré-visualização nada é gravado: as capas valem até fechar a página') + '.', feitos.length ? 'ok' : 'aviso');
  },
};
