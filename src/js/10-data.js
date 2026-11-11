/* ───────────────────────── modelo de dados ───────────────────────── */
const EIXOS = [null,
  { n: 'Pré-história e origens', l: 'Pré-história, neandertais e origens' },
  { n: 'Ficção científica e fantasia', l: 'Ficção científica, fantasia e distopia' },
  { n: 'Clássicos universais', l: 'Clássicos universais e romances de ideias' },
  { n: 'Brasil, América Latina e lusofonia', l: 'América Latina, Brasil e lusofonia (ficção)' },
  { n: 'Ficção contemporânea', l: 'Ficção contemporânea e mundial' },
  { n: 'Romances históricos', l: 'Romances históricos' },
  { n: 'Horror, weird e mistério', l: 'Horror, weird fiction e mistério' },
  { n: 'Poesia e cartas', l: 'Poesia e cartas' },
  { n: 'Filosofia e ética', l: 'Filosofia, ética e existência (não ficção)' },
  { n: 'Mente e neurociência', l: 'Mente, consciência e neurociência' },
  { n: 'Política e economia', l: 'Política, poder, autoritarismo e economia' },
  { n: 'Sociedade e história', l: 'Sociedade, antropologia, cultura e história' },
  { n: 'Ciência e tecnologia', l: 'Ciência, tecnologia e futuro' },
  { n: 'Psicologia e psicanálise', l: 'Psicologia, psicanálise e comportamento' },
  { n: 'Espiritualidade', l: 'Espiritualidade, espiritismo e mistérios da consciência' },
  { n: 'Artes, escrita e parentalidade', l: 'Artes, escrita, cinema e parentalidade' },
];

const ROTULO_TAG = {
  F: 'ficção', NF: 'não ficção', HQ: 'HQ', poesia: 'poesia', antologia: 'antologia',
  d1: 'leve', d2: 'média', d3: 'exigente', e1: 'curta', e2: 'média', e3: 'longa',
  'ja-tenho': 'já tenho', 'tenho-fisico': 'tenho em físico', 'tenho-digital': 'tenho em digital', lido: 'lido', top: 'prioridade', verificar: 'a verificar', 'sem-pt': 'sem edição em PT',
  classico: 'clássico', contemporaneo: 'contemporâneo', BR: 'Brasil', RS: 'Rio Grande do Sul', portugal: 'Portugal', latam: 'América Latina',
  africa: 'África', asia: 'Ásia', 'europa-leste': 'Leste Europeu',
  etica: 'ética', politica: 'política', geopolitica: 'geopolítica', psicanalise: 'psicanálise', neurociencia: 'neurociência',
  consciencia: 'consciência', ciencia: 'ciência', ia: 'IA', historia: 'história', religiao: 'religião', mistica: 'mística',
  memoria: 'memória', raca: 'raça', genero: 'gênero', introducao: 'introdução', gestao: 'gestão', didatico: 'didático',
  'ficcao-cientifica': 'ficção científica', 'historia-alternativa': 'história alternativa', gotico: 'gótico', misterio: 'mistério',
  'thriller-medico': 'thriller médico', 'romance-historico': 'romance histórico', roma: 'Roma', 'pre-historia': 'pré-história',
  'regional-gaucho': 'regional gaúcho',
  fisica: 'física', tcc: 'TCC', 'psicologia-analitica': 'psicologia analítica', 'psicologia-humanista': 'psicologia humanista', 'psicologia-social': 'psicologia social',
  cronicas: 'crônicas', 'super-herois': 'super-heróis', manga: 'mangá', adaptacao: 'adaptação em quadrinhos', educacao: 'educação', matematica: 'matemática',
  programacao: 'programação', dados: 'dados e planilhas', enigmas: 'enigmas e mistérios', analise: 'possui análise',
  'rel-imortais': 'afins a Os Imortais', 'rel-widows-bay': 'Lovecraft e Widow’s Bay', 'rel-cornwell': 'afins a O Arqueiro / O Físico',
  'rel-asimov-clarke': 'Asimov e Clarke', 'rel-yalom': 'Yalom', 'rel-fromm': 'Fromm · autoritarismo',
};
const rotTag = t => ROTULO_TAG[t] || t.replace(/-/g, ' ');
const TAGS_ESTRUTURA = new Set(['F', 'NF', 'HQ', 'poesia', 'antologia', 'd1', 'd2', 'd3', 'e1', 'e2', 'e3', 'ja-tenho', 'tenho-fisico', 'tenho-digital', 'lido', 'top']);
const GRUPOS_TAG = [
  ['Gêneros', ['ficcao-cientifica', 'fantasia', 'distopia', 'utopia', 'historia-alternativa', 'horror', 'gotico', 'lovecraftiano', 'misterio', 'thriller', 'thriller-medico', 'romance-historico', 'medieval', 'antiguidade', 'roma', 'renascimento', 'pre-historia', 'neandertal', 'regional-gaucho', 'teatro', 'contos', 'cronicas', 'aventura', 'policial', 'faroeste', 'poesia', 'HQ', 'super-herois', 'manga', 'adaptacao', 'antologia']],
  ['Temas', ['filosofia', 'existencialismo', 'etica', 'politica', 'autoritarismo', 'economia', 'geopolitica', 'psicologia', 'psicanalise', 'psiquiatria', 'neurociencia', 'consciencia', 'ciencia', 'ia', 'historia', 'antropologia', 'sociologia', 'religiao', 'espiritualidade', 'espiritismo', 'umbanda', 'oriental', 'mistica', 'morte', 'memoria', 'identidade', 'raca', 'genero', 'colonialismo', 'ecologia', 'linguagem', 'guerra', 'testemunho', 'medicina', 'biografia', 'escrita', 'cinema', 'arte', 'parentalidade', 'humor', 'introducao', 'gestao', 'esporte', 'didatico', 'tecnologia', 'fisica', 'autoconhecimento', 'behaviorismo', 'tcc', 'psicometria', 'psicopatologia', 'psicologia-analitica', 'psicologia-humanista', 'psicologia-social', 'mitologia', 'educacao', 'biologia', 'matematica', 'programacao', 'dados', 'design', 'enigmas']],
  ['Época e origem', ['classico', 'contemporaneo', 'BR', 'RS', 'portugal', 'latam', 'africa', 'asia', 'europa-leste']],
  ['Afinidades', ['rel-imortais', 'rel-widows-bay', 'rel-cornwell', 'rel-asimov-clarke', 'rel-yalom', 'rel-fromm']],
];
/* Camadas curatoriais (seções 0 a 16 do catálogo): por que o livro importa e com o que ele conversa.
   p = prefixo do marcador (#q-…), n = nome na ficha do livro, g = nome do grupo nos filtros, r = prefixo do rótulo,
   v = { sufixo do marcador: [rótulo, o que reúne] }. */
const CAMADAS = [
  { p: 'q', n: 'Pergunta central', g: 'Perguntas centrais', r: 'pergunta', v: {
    'o-que-e-humano': ['o que nos faz humanos?', 'Espécies, máquinas e limites da humanidade'], 'liberdade-e-obediencia': ['liberdade e obediência', 'Liberdade, medo e submissão à autoridade'],
    'sentido-e-como-viver': ['sentido e como viver', 'O que é uma vida boa? Sentido, propósito e ofício de viver'], 'morte-e-finitude': ['morte e finitude', 'A consciência da morte e o que vem (ou não) depois'],
    'identidade-e-eu': ['identidade e eu', 'Quem sou eu? Identidade, máscara, duplo e self'], 'poder-e-violencia': ['poder e violência', 'Como o poder se organiza, se legitima e se impõe'],
    'realidade-e-percepcao': ['realidade e percepção', 'O que é real? Percepção, simulação e labirintos'], 'memoria-e-esquecimento': ['memória e esquecimento', 'Memória pessoal e coletiva: o que lembramos e o que é apagado'],
    'fe-e-duvida': ['fé e dúvida', 'Fé, ceticismo, Deus e o sagrado'], 'alteridade-e-contato': ['alteridade e contato', 'O encontro com o radicalmente outro: espécies, culturas, línguas'],
    'culpa-e-justica': ['culpa e justiça', 'Crime, responsabilidade, castigo e justiça'], 'natureza-e-civilizacao': ['natureza e civilização', 'De onde viemos e para onde vamos'] } },
  { p: 'clima', n: 'Clima da leitura', g: 'Clima da leitura', r: 'clima', v: {
    claustrofobico: ['claustrofóbico', 'Opressivo, fechado, sem saída'], melancolico: ['melancólico', 'Perda, passagem do tempo, ternura triste'], onirico: ['onírico', 'Realidade que escorrega: sonho, fantasma, delírio'],
    aventura: ['de aventura', 'Ação, viagem, batalha e fôlego de saga'], cerebral: ['cerebral', 'Jogo de ideias, estrutura e quebra-cabeça intelectual'], 'cru-e-chocante': ['cru e chocante', 'Realismo duro, violência ou testemunho que não alivia'],
    subversivo: ['subversivo', 'Desmonta o senso comum, o cânone ou o poder'], emocionante: ['emocionante', 'Mexe com o coração'], comico: ['cômico', 'Humor, ironia e leveza inteligente'], contemplativo: ['contemplativo', 'Leitura lenta, para meditar e voltar'] } },
  { p: 'papel', n: 'Papel na biblioteca', g: 'Papel na biblioteca', r: 'papel', v: {
    'porta-de-entrada': ['porta de entrada', 'Melhor primeiro livro para entrar numa área'], 'leitura-relampago': ['leitura-relâmpago', 'Curto e potente: dá para ler em uma ou duas sentadas'], desafio: ['desafio', 'Leitura de fôlego: exige tempo, atenção ou bagagem'],
    contraponto: ['contraponto', 'Para ler com lupa ou ao lado de uma visão oposta'], ponte: ['ponte entre áreas', 'Cruza áreas diferentes e abre caminhos para outras leituras'], 'fonte-primaria': ['fonte primária', 'Texto fundacional, lido na origem'] } },
  { p: 'ponte', n: 'Ponte entre áreas', g: 'Pontes entre áreas', r: 'ponte', v: {
    'ciencia-e-fe': ['ciência e fé', 'Onde a ciência encontra (ou questiona) o sagrado'], 'psicanalise-e-politica': ['psicanálise e política', 'Psiquismo, massas e poder'], 'literatura-e-neurociencia': ['literatura e neurociência', 'O cérebro visto pela ficção e pela clínica'],
    'ficcao-e-filosofia': ['ficção e filosofia', 'Romances de ideias: filosofia em forma de enredo'], 'historia-e-ficcao': ['história e ficção', 'A história que a ficção reconstrói por dentro'], 'ecologia-e-colonialismo': ['ecologia e colonialismo', 'A exploração da terra e a dos povos andam juntas'],
    'corpo-e-poder': ['corpo e poder', 'Corpo, gênero e controle'], 'ia-e-humanidade': ['IA e humanidade', 'Máquinas, mentes artificiais e o que sobra de humano'] } },
  { p: 'cenario', n: 'Cenário', g: 'Cenários', r: 'cenário', v: {
    russia: ['Rússia', 'Rússia e mundo soviético'], 'nova-inglaterra': ['Nova Inglaterra', 'Costa, ilhas e vilas da Nova Inglaterra'], 'sertao-e-nordeste': ['sertão e Nordeste', 'Sertão e Nordeste do Brasil'],
    'espaco-profundo': ['espaço profundo', 'Espaço, naves e outros mundos'], 'ilha-e-isolamento': ['ilha e isolamento', 'Ilhas, expedições e lugares sem retorno'], 'guerra-mundial': ['guerras mundiais', 'As guerras mundiais e seus testemunhos'],
    'oriente-feudal': ['Oriente feudal', 'Japão, Ásia, mundo islâmico e rotas medievais'], 'futuro-proximo': ['futuro próximo', 'Futuros próximos e colapsos plausíveis'], 'cidade-pequena': ['cidade pequena', 'Cidade pequena, segredo grande'] } },
];
const DICA_TAG = {};                                // o que o marcador reúne (aparece ao passar o mouse)
const ROTULO_CURTO = {};                            // rótulo sem o nome da camada, para quando o grupo já diz qual é ("Clima da leitura › cerebral")
const rotCurto = t => ROTULO_CURTO[t] || rotTag(t);
for (const c of CAMADAS) {
  for (const k in c.v) { const t = c.p + '-' + k; ROTULO_TAG[t] = c.r + ': ' + c.v[k][0]; ROTULO_CURTO[t] = c.v[k][0]; DICA_TAG[t] = c.v[k][1]; }
  GRUPOS_TAG.push([c.g, Object.keys(c.v).map(k => c.p + '-' + k)]);
}
const camadaDe = t => CAMADAS.find(c => t.startsWith(c.p + '-') && c.v[t.slice(c.p.length + 1)]) || null;
const ehCamada = t => !!camadaDe(t) || t.startsWith('trilha-');
/* Trilhas de leitura (catalogo/trilhas.md): roteiros com os livros em ordem. Quem diz que um livro está na trilha é o
   marcador dele (#trilha-…); a lista da trilha diz a ordem. linhas = chaves das linhas do catálogo (ver chaveCat). */
const TRILHAS = TRILHAS_DADOS.map(([tag, nome, desc, linhas], i) => ({ n: i + 1, tag, nome, curto: nome.split(':')[0].trim(), desc, linhas: linhas.map(j => norm(CATALOGO[j][0]) + '|' + norm(CATALOGO[j][1])) }));
for (const t of TRILHAS) { ROTULO_TAG[t.tag] = 'trilha: ' + t.curto; ROTULO_CURTO[t.tag] = t.curto; DICA_TAG[t.tag] = t.nome; }
GRUPOS_TAG.push(['Trilhas de leitura', TRILHAS.map(t => t.tag)], ['Pendências', ['verificar', 'sem-pt']], ['Suas marcas', ['analise']]);
const TAG_ANALISE = 'analise';                      // "possui análise": posto no painel, na ficha do livro

const FORMATOS = {
  fisico: { n: 'Físico', cor: 'var(--c1)' },
  ebook: { n: 'Digital', cor: 'var(--c2)' },
  audio: { n: 'Audiolivro', cor: 'var(--c3)' },
};
/* posse: o livro pode estar na estante física, na biblioteca virtual (arquivo digital) ou nas duas — #tenho-fisico e #tenho-digital no catálogo */
const POSSES = {
  fisico: { n: 'Só físico', cor: 'var(--c1)' },
  ambos: { n: 'Físico e digital', cor: 'var(--c5)' },
  digital: { n: 'Só digital', cor: 'var(--c2)' },
  audio: { n: 'Audiolivro', cor: 'var(--c3)' },
};
const PLAT_DIGITAL = 'Biblioteca virtual';
const LEITURAS = {
  lido: { n: 'Lido', cor: 'var(--c6)' },
  lendo: { n: 'Lendo', cor: 'var(--c3)' },
  fila: { n: 'Na fila', cor: 'var(--c4)' },
  aband: { n: 'Abandonado', cor: 'var(--c8)' },
  '': { n: 'Não informado', cor: 'var(--c9)' },
};
const PRIORIDADES = { 1: { n: 'Alta', cor: 'var(--c1)' }, 2: { n: 'Média', cor: 'var(--c3)' }, 3: { n: 'Baixa', cor: 'var(--c4)' }, 0: { n: 'Sem prioridade', cor: 'var(--c9)' } };
const TIPOS = {
  F: { n: 'Ficção', cor: 'var(--c1)' }, NF: { n: 'Não ficção', cor: 'var(--c2)' }, P: { n: 'Poesia', cor: 'var(--c5)' },
  HQ: { n: 'HQ', cor: 'var(--c3)' }, ANT: { n: 'Antologia', cor: 'var(--c4)' }, X: { n: 'Sem tipo', cor: 'var(--c9)' },
};
/* filtro "Tipo": ficção, não ficção e HQ têm botão próprio; poesia, antologia e sem tipo ficam em "Outros" */
const tipoFiltro = t => (t === 'F' || t === 'NF' || t === 'HQ' ? t : 'O');
const NIVEIS = { 1: { n: 'Leve', cor: 'var(--c6)' }, 2: { n: 'Média', cor: 'var(--c3)' }, 3: { n: 'Exigente', cor: 'var(--c1)' }, 0: { n: 'Não informada', cor: 'var(--c9)' } };
const EXTENSOES = { 1: { n: 'Curta', d: 'até ~250 p.', cor: 'var(--c2)' }, 2: { n: 'Média', d: '~250–500 p.', cor: 'var(--c4)' }, 3: { n: 'Longa', d: '500+ p. ou série', cor: 'var(--c5)' }, 0: { n: 'Não informada', d: '', cor: 'var(--c9)' } };
const SITUACOES = { agora: { n: 'Comprar agora', cor: 'var(--good)' }, quase: { n: 'Quase lá', cor: 'var(--c3)' }, aguardar: { n: 'Aguardar', cor: 'var(--c9)' }, semalvo: { n: 'Sem alvo', cor: 'var(--c8)' }, sem: { n: 'Sem cotação', cor: 'var(--c8)' } };

/* lojas / fontes de preço */
const LOJAS = {
  'Amazon': { tipo: 'fisico', cor: 'var(--c3)' },
  'Estante Virtual': { tipo: 'fisico', cor: 'var(--c2)' },
  'Mercado Livre': { tipo: 'fisico', cor: 'var(--c4)' },
  'Travessa': { tipo: 'fisico', cor: 'var(--c5)' },
  'Kindle': { tipo: 'virtual', cor: 'var(--c7)' },
};
const CORES_EXTRA = ['var(--c6)', 'var(--c1)', 'var(--c8)', 'var(--c9)'];
const tipoFonte = n => (LOJAS[n] ? LOJAS[n].tipo : /kindle|kobo|e-?book|play|audible|digital|storytel/i.test(n) ? 'virtual' : 'fisico');
const corFonte = n => { if (LOJAS[n]) return LOJAS[n].cor; return CORES_EXTRA[hashStr(n) % CORES_EXTRA.length]; };

/* campos derivados das tags (cache em propriedades _x, que não são salvas) */
function derivar(b) {
  const T = b.tags;
  b._tipo = T.includes('F') ? 'F' : T.includes('NF') ? 'NF' : T.includes('poesia') ? 'P' : T.includes('HQ') ? 'HQ' : T.includes('antologia') ? 'ANT' : 'X';
  b._d = T.includes('d1') ? 1 : T.includes('d2') ? 2 : T.includes('d3') ? 3 : 0;
  b._e = T.includes('e1') ? 1 : T.includes('e2') ? 2 : T.includes('e3') ? 3 : 0;
  b._top = T.includes('top');
  const g = b._dg;                               // biblioteca virtual: [formatos, nº de arquivos, pastas, títulos das edições, ids dos arquivos, subpastas da série?]
  // a busca também acha o livro pelo nome que ele tinha antes de ser corrigido no catálogo
  b._busca = norm(b.t + ' ' + b.a + ' ' + T.map(rotTag).join(' ') + ' ' + T.join(' ') + ' ' + (EIXOS[b.eixo] ? EIXOS[b.eixo].n : '') + (g ? ' ' + g[0] + ' ' + (g[2] || []).join(' ') + ' ' + (g[3] || []).join(' ') + ' ' + (g[5] || []).join(' ') : '') + (b._ant ? ' ' + b._ant.map(n => n.join(' ')).join(' ') : '') + (b.com ? ' ' + b.com : '') + (b.anx ? ' ' + b.anx.map(a => a[1]).join(' ') : ''));
  return b;
}
const virtual = b => b.fmt === 'ebook' || b.fmt === 'audio';
const temFisico = b => b.col === 'acervo' && b.fmt === 'fisico';
const temDigital = b => !!b._dg || b.tags.includes('tenho-digital') || (b.col === 'acervo' && b.fmt === 'ebook');   // arquivo na biblioteca virtual ou livro digital comprado
const posseDe = b => (b.col !== 'acervo' ? '' : b.fmt === 'audio' ? 'audio' : b.fmt === 'fisico' ? (temDigital(b) ? 'ambos' : 'fisico') : 'digital');
const formatosDe = b => (b.col !== 'acervo' ? [] : b.fmt === 'fisico' && temDigital(b) ? ['fisico', 'ebook'] : [b.fmt || 'fisico']);
const soDigital = b => b.col === 'acervo' && b.fmt === 'ebook' && b.tags.includes('tenho-digital');                // está só na biblioteca virtual: sem compra a simular
const rotuloFmt = b => (posseDe(b) === 'ambos' ? POSSES.ambos.n : b.fmt && FORMATOS[b.fmt] ? FORMATOS[b.fmt].n : '');

function novoLivro(o) {
  return derivar(Object.assign({
    id: '', t: '', a: '', tags: [], sec: -1, eixo: 5, obs: '',
    col: 'rec', fmt: '', plat: '', adq: null, pago: null, loja: '', cond: '',
    add: null, leit: '', lidoEm: null, prog: 0, nota: 0, pg: 0,
    prio: 0, alvo: null, capa: null, track: false, px: null, demo: 0, u: 0,
    com: '',        // comentários do usuário sobre o livro (ficha do livro)
    cp: '',         // capa enviada pelo usuário: chave da imagem guardada no navegador (ver Anexos); '' = usa a do catálogo
    anx: null,      // arquivos anexados (resenha, relatório…): [[chave, nome, tamanho em bytes, dia, tipo], …]; o conteúdo fica em Anexos
    cl: '',         // classificação que o catálogo dava ao livro quando ele foi editado ou conciliado pela última vez (ver mesclarClasse)
    o: '',          // linha do catálogo de onde o livro veio (ver chaveCat); '' = criado no painel
    arq: '',        // identificadores dos arquivos da biblioteca virtual (reconhecem o livro se o título mudar no catálogo)
    _dg: null,      // dados da biblioteca virtual; vêm sempre do catálogo embutido e não são salvos
    _ant: null,     // [[título, autor], …] que a linha do catálogo já teve (catalogo/renomeados.tsv); também vêm do catálogo e não são salvos
    _img: 0,        // imagem da capa: número na Open Library ou endereço https (catalogo/capas.tsv); vem do catálogo e não é salva
  }, o));
}
const MAX_COMENTARIO = 5000, MAX_ANEXOS = 8;
const chaveAnexo = v => (typeof v === 'string' && /^[a-z0-9]{6,24}$/.test(v) ? v : '');
const temAnotacao = b => !!(b.com || (b.anx && b.anx.length) || b.tags.includes(TAG_ANALISE));
/* Registro vindo de fora (armazenamento do navegador ou arquivo de backup): devolve um livro íntegro, ou null.
   Nada aqui confia no formato: um arquivo editado à mão não pode travar o painel. */
function lerLivro(o, usados) {
  if (!o || typeof o !== 'object' || Array.isArray(o) || typeof o.t !== 'string' || !o.t.trim()) return null;
  const txt = (v, max) => (typeof v === 'string' ? v.slice(0, max) : '');
  const num = (v, min, max) => (typeof v === 'number' && isFinite(v) && v >= min && v <= max ? v : null);
  const dia = v => { const d = num(v, -200000, 200000); return d == null ? null : Math.round(d); };
  const de = (v, lista, padrao) => (lista.includes(v) ? v : padrao);
  let id = txt(o.id, 40).replace(/[^\w-]/g, '');
  if (!id || usados.has(id)) { let k = usados.size; do id = 'u' + (k++).toString(36) + 'x'; while (usados.has(id)); }
  usados.add(id);
  let px = null;
  if (o.px && typeof o.px === 'object' && !Array.isArray(o.px)) {
    for (const f of Object.keys(o.px).slice(0, 40)) {
      const nome = f.trim().slice(0, 40), porDia = new Map();
      if (!nome || !Array.isArray(o.px[f])) continue;
      for (const q of o.px[f]) { if (!Array.isArray(q)) continue; const d = dia(q[0]), v = num(q[1], 0.01, 1e6); if (d != null && v != null) porDia.set(d, q[2] ? [d, v, 1] : [d, v]); }
      if (porDia.size) (px || (px = {}))[nome] = [...porDia.values()].sort((a, z) => a[0] - z[0]);
    }
  }
  const col = de(o.col, ['acervo', 'desejo', 'rec'], 'rec');
  const anx = (Array.isArray(o.anx) ? o.anx : []).map(a => (Array.isArray(a) && chaveAnexo(a[0]) ? [a[0], txt(a[1], 120).trim() || 'arquivo', Math.round(num(a[2], 0, 1e9) ?? 0), dia(a[3]), txt(a[4], 80)] : null)).filter(Boolean).slice(0, MAX_ANEXOS);
  return novoLivro({
    id, t: o.t.trim().slice(0, 200), a: txt(o.a, 160), obs: txt(o.obs, 2000),
    com: txt(o.com, MAX_COMENTARIO), cp: chaveAnexo(o.cp), anx: anx.length ? anx : null, cl: txt(o.cl, 1500),
    tags: Array.isArray(o.tags) ? [...new Set(o.tags.filter(t => typeof t === 'string' && t && t.length <= 60))].slice(0, 60) : [],
    sec: num(o.sec, -1, 99) ?? -1, eixo: Math.round(num(o.eixo, 1, EIXOS.length - 1) ?? 5),
    col, fmt: de(o.fmt, Object.keys(FORMATOS), col === 'acervo' ? 'fisico' : ''), plat: txt(o.plat, 40), loja: txt(o.loja, 60), cond: txt(o.cond, 20),
    adq: dia(o.adq), add: dia(o.add), lidoEm: dia(o.lidoEm), pago: num(o.pago, 0, 1e6), alvo: num(o.alvo, 0.01, 1e6), capa: num(o.capa, 0.01, 1e6),
    leit: de(o.leit, Object.keys(LEITURAS), ''), prog: Math.round(num(o.prog, 0, 100) ?? 0), nota: Math.round(num(o.nota, 0, 5) ?? 0), pg: Math.round(num(o.pg, 0, 1e5) ?? 0),
    prio: Math.round(num(o.prio, 0, 3) ?? 0), track: !!o.track, px, demo: o.demo ? 1 : 0, u: o.u ? 1 : 0, o: txt(o.o, 400), arq: txt(o.arq, 400).replace(/[^a-z0-9 ]/g, ''),
  });
}
const lerLivros = lista => { const usados = new Set(); return (Array.isArray(lista) ? lista : []).map(o => lerLivro(o, usados)).filter(Boolean); };

/* estado "real": apenas o que o catálogo afirma (estante física, biblioteca virtual, #lido, #top) */
function estadoBase(b) {
  const fis = b.tags.includes('tenho-fisico') || b.tags.includes('ja-tenho'), dig = b.tags.includes('tenho-digital');
  Object.assign(b, {
    col: fis || dig ? 'acervo' : 'rec', fmt: fis ? 'fisico' : dig ? 'ebook' : '', plat: !fis && dig ? PLAT_DIGITAL : '', adq: null, pago: null, loja: '', cond: '',
    add: null, leit: b.tags.includes('lido') ? 'lido' : '', lidoEm: null, prog: 0, nota: 0, pg: 0,
    prio: 0, alvo: null, capa: null, track: false, demo: 0,
  });
  if (b.px) { for (const f in b.px) { b.px[f] = b.px[f].filter(p => p[2]); if (!b.px[f].length) delete b.px[f]; } if (!Object.keys(b.px).length) b.px = null; else b.track = true; }
  return b;
}
const chaveCat = r => norm(r[0]) + '|' + norm(r[1]);
const chaveLivro = b => norm(b.t) + '|' + norm(b.a);
const tagsCat = r => r[2].split(' ').filter(Boolean);
const doCatalogo = (r, id) => estadoBase(novoLivro({ id, t: r[0], a: r[1], tags: tagsCat(r), sec: r[3], eixo: r[4], obs: r[5] || '', o: chaveCat(r), arq: r[6] ? r[6][4] : '', _dg: r[6] || null, _ant: r[7] || null }));
function livrosDoCatalogo() { return CATALOGO.map((r, i) => { const b = doCatalogo(r, 'c' + i); b._img = CAPAS[i] || 0; return b; }); }
/* imagem da capa: endereço da imagem do livro, ou '' (sem capa achada, livro criado no painel, ou capas desligadas) */
let MOSTRAR_CAPAS = true;
const enderecoCapa = c => (!c ? '' : typeof c === 'number' ? (c > 0 ? `https://covers.openlibrary.org/b/id/${Math.round(c)}-M.jpg?default=false` : '') : typeof c === 'string' && /^https:\/\//i.test(c) ? c : '');
const temCapa = b => !!enderecoCapa(b._img);                                 // há capa no catálogo (mostrada ou não)
const capaPropria = b => (b.cp && Anexos.capas.get(b.cp)) || '';            // imagem que o usuário enviou (fica no navegador; ver Anexos)
// o que vai para a tela: a capa enviada pelo usuário, sempre; senão a do catálogo — ou nada, com as capas desligadas
const urlCapa = b => capaPropria(b) || (MOSTRAR_CAPAS ? enderecoCapa(b._img) : '');

/* os marcadores de posse acompanham a lista e o formato do livro (e o que o catálogo diz da biblioteca virtual) */
const defTag = (b, t, on) => { const i = b.tags.indexOf(t); if (on && i < 0) b.tags.push(t); if (!on && i >= 0) b.tags.splice(i, 1); };
function marcarPosse(b) {
  const ac = b.col === 'acervo';
  defTag(b, 'tenho-digital', !!b._dg || (ac && (b.fmt === 'ebook' || (b.fmt === 'fisico' && b.tags.includes('tenho-digital')))));
  defTag(b, 'tenho-fisico', ac && b.fmt === 'fisico');
  defTag(b, 'ja-tenho', false);
}

/* ───────── classificação: o que o catálogo diz × o que foi mexido no painel ─────────
   A classificação de um livro é o eixo mais os marcadores, fora os de posse e de leitura (que seguem a lista, o formato e a
   leitura do livro). Num livro editado no painel, `cl` guarda a classificação que o catálogo dava quando o livro foi editado
   pela primeira vez ou conciliado pela última: é a base para saber, depois, o que mudou no catálogo e o que mudou no painel. */
const TAGS_SITUACAO = ['tenho-fisico', 'tenho-digital', 'ja-tenho', 'lido'];
const GRUPOS_UNICOS = [['F', 'NF', 'HQ', 'poesia', 'antologia'], ['d1', 'd2', 'd3'], ['e1', 'e2', 'e3']];   // tipo, dificuldade e extensão: uma resposta por grupo
const classeCat = r => r[4] + '|' + tagsCat(r).filter(t => !TAGS_SITUACAO.includes(t)).join(' ');
const lerClasse = s => { const i = (s || '').indexOf('|'); return i < 1 ? null : { eixo: +s.slice(0, i), tags: s.slice(i + 1).split(' ').filter(Boolean) }; };
/* Dados gravados por um painel de antes de 10/11/2026 não trazem `cl`. Para as linhas em que a vistoria daquele dia trocou
   ou tirou alguma coisa, a classificação antiga vem embutida (CLASSE_ANTES, de catalogo/antes-da-vistoria.tsv). */
let BASE_ANTIGA = null;
const classeAntiga = k => { if (!BASE_ANTIGA) BASE_ANTIGA = new Map(CLASSE_ANTES.map(([i, e, t]) => [chaveCat(CATALOGO[i]), e + '|' + t])); return BASE_ANTIGA.get(k) || ''; };
let LINHAS_CAT = null;
const linhaCat = b => { if (!b.o) return null; if (!LINHAS_CAT) LINHAS_CAT = new Map(CATALOGO.map(r => [chaveCat(r), r])); return LINHAS_CAT.get(b.o) || null; };
/* O livro passa a ser "do usuário" (editado no painel): guarda a classificação que o catálogo dá a ele agora. */
function marcarMeu(b) { if (!b.u) { const r = linhaCat(b); b.cl = r ? classeCat(r) : ''; } b.u = 1; b.demo = 0; }
/* Livro editado no painel × linha nova do catálogo (r). O que o usuário não mexeu acompanha o catálogo; o que ele pôs, tirou
   ou trocou fica como ele deixou. Sem base (dados gravados por um painel antigo, que não a guardava) nada é desfeito:
   o catálogo só acrescenta — o que falta ao livro entra, o que ele já tem fica. */
function mesclarClasse(b, r, base) {
  const fora = t => !TAGS_SITUACAO.includes(t), unico = new Set(GRUPOS_UNICOS.flat()), antes = base ? base.tags : [];
  const cat = tagsCat(r).filter(fora), minhas = b.tags.filter(fora), iguais = (x, y) => x.length === y.length && x.every(t => y.includes(t));
  let novas = [];
  for (const g of GRUPOS_UNICOS) { const meu = minhas.filter(t => g.includes(t)), era = antes.filter(t => g.includes(t)); novas = novas.concat(iguais(meu, era) ? cat.filter(t => g.includes(t)) : meu); }
  const postas = minhas.filter(t => !unico.has(t) && !antes.includes(t)), tiradas = antes.filter(t => !unico.has(t) && !minhas.includes(t));
  novas = novas.concat(cat.filter(t => !unico.has(t) && !tiradas.includes(t)), postas);
  if (base && b.eixo === base.eixo) b.eixo = r[4];
  b.tags = [...new Set(novas)].concat(b.tags.filter(t => !fora(t)));
}

/* ───────── catálogo novo × dados salvos ─────────
   Os livros ficam guardados no navegador. Quando o painel chega com outro catálogo (livros novos, a biblioteca virtual,
   títulos corrigidos), os dados salvos são conciliados com ele:
   · o que nunca foi editado no painel passa a seguir o catálogo novo;
   · o que foi editado fica como está — o catálogo acrescenta posse (#tenho-fisico, #tenho-digital), corrige título e
     autor que não tenham sido mudados no painel, retira o #verificar que já foi resolvido e atualiza a classificação
     (eixo, tipo, dificuldade, extensão e temas) naquilo que o usuário não mexeu (ver mesclarClasse);
   · linhas novas entram; linhas que saíram do catálogo sem nunca terem sido editadas saem;
   · se duas linhas antigas viraram uma só, ela fica com a que o usuário editou. */
const ASSINATURA = CATALOGO.length + '.' + hashStr(JSON.stringify(CATALOGO)).toString(36);
function anexarDigital(livros) {
  const linhas = new Map(CATALOGO.map((r, i) => [chaveCat(r), i]));
  for (const b of livros) {
    const i = b.o ? linhas.get(b.o) : undefined, r = i == null ? null : CATALOGO[i]; b._dg = (r && r[6]) || null; b._ant = (r && r[7]) || null; b._img = (r && CAPAS[i]) || 0; if (b._dg) b.arq = b._dg[4];
    if (b.u && !b.cl && r) b.cl = classeCat(r);       // dados de um painel antigo: daqui em diante a base é o catálogo de agora
    derivar(b);
  }
}
function conciliarCatalogo(livros) {
  // ant: os nomes que a linha já teve (título ou autor corrigido no catálogo — catalogo/renomeados.tsv)
  const linhas = CATALOGO.map((r, i) => ({ r, i, k: chaveCat(r), ant: (r[7] || []).map(chaveCat), b: null })), soltos = new Set(livros);
  // liga cada linha do catálogo a um livro salvo, do vínculo mais forte para o mais fraco
  const passo = (chavesDoLivro, chavesDaLinha, serve) => {
    const indice = new Map();
    for (const b of soltos) for (const k of chavesDoLivro(b)) if (k && !indice.has(k)) indice.set(k, b);
    for (const x of linhas) {
      if (x.b) continue;
      for (const k of chavesDaLinha(x)) { const b = indice.get(k); if (b && soltos.has(b) && (!serve || serve(b, x))) { x.b = b; soltos.delete(b); break; } }
    }
  };
  passo(b => [b.o], x => [x.k].concat(x.ant));                                            // 1 ▸ a mesma linha de antes (pelo nome atual ou por um antigo)
  passo(b => [chaveLivro(b)], x => [x.k].concat(x.ant));                                  // 2 ▸ mesmo título e autor (dados antigos; livro criado no painel)
  passo(b => (b.arq ? b.arq.split(' ') : []), x => (x.r[6] && x.r[6][4] ? x.r[6][4].split(' ') : []));   // 3 ▸ mesmo arquivo: título corrigido no inventário
  passo(b => [b.u && !b.o ? b.id : ''], x => ['c' + x.i], (b, x) => b.sec === x.r[3]);    // 4 ▸ dados antigos: livro do catálogo renomeado no painel
  // 5 ▸ duas entradas antigas viraram uma linha só (edições juntadas, recomendação que era o mesmo livro de um arquivo): a linha
  //     fica com a entrada em que o usuário mexeu, e a outra — que só repetia o catálogo — sai. Sem isto, o que ele anotou ficaria
  //     num livro solto, fora do catálogo, ao lado da linha nova.
  for (const b of [...soltos]) {
    if (!b.u) continue;
    const minhas = new Set([b.o, chaveLivro(b)].concat(b.arq ? b.arq.split(' ') : []).filter(Boolean));
    const x = linhas.find(y => y.b && !y.b.u && ([y.k].concat(y.ant).some(k => minhas.has(k)) || (y.r[6] && y.r[6][4] ? y.r[6][4].split(' ') : []).some(k => minhas.has(k))));
    if (x) { soltos.add(x.b); x.b = b; soltos.delete(b); }
  }
  const usados = new Set(livros.map(b => b.id)), novos = [];
  for (const x of linhas) {
    const r = x.r, b = x.b, tags = tagsCat(r);
    if (!b) { let id = 'c' + x.i; while (usados.has(id)) id += 'n'; usados.add(id); novos.push(doCatalogo(r, id)); continue; }
    if (!b.u) Object.assign(b, { t: r[0], a: r[1], tags, sec: r[3], eixo: r[4], obs: r[5] || '' });
    else {
      if (chaveLivro(b) === (b.o || x.k) || x.ant.includes(chaveLivro(b))) { b.t = r[0]; b.a = r[1]; }   // título e autor não foram mexidos no painel: valem os do catálogo
      b.sec = r[3];
      mesclarClasse(b, r, lerClasse(b.cl) || (b.o ? lerClasse(classeAntiga(x.k)) : null));   // b.o: o livro já vinha do catálogo (não foi criado no painel)
      if (!tags.includes('verificar')) defTag(b, 'verificar', false);
      const fis = tags.includes('tenho-fisico'), dig = tags.includes('tenho-digital'), tinhaEbook = b.col === 'acervo' && b.fmt === 'ebook';
      if (dig || (fis && tinhaEbook)) defTag(b, 'tenho-digital', true);
      if (fis && !(b.col === 'acervo' && b.fmt === 'fisico')) Object.assign(b, { col: 'acervo', fmt: 'fisico', plat: '', prio: 0, track: false, leit: b.leit || 'fila' });
      else if (dig && b.col === 'rec') Object.assign(b, { col: 'acervo', fmt: 'ebook', plat: PLAT_DIGITAL });
    }
    b.o = x.k; b.arq = r[6] ? r[6][4] : ''; b.cl = b.u ? classeCat(r) : '';
  }
  const ficam = livros.filter(b => !soltos.has(b) || b.u || b.sec < 0);
  return { livros: ficam.concat(novos), novos: novos.length, saidos: livros.length - ficam.length };
}
/* depois de abrir dados salvos ou de importar um backup: concilia com o catálogo embutido, se for outro, e religa a biblioteca virtual */
function ajustarAoCatalogo(assinatura) {
  DB.novidade = null;
  if (assinatura === ASSINATURA) { anexarDigital(DB.livros); return; }
  const r = conciliarCatalogo(DB.livros);
  DB.livros = r.livros; anexarDigital(DB.livros);
  for (const b of DB.livros) { if (b.u) { marcarPosse(b); derivar(b); } else estadoBase(b); }
  if (DB.exemplos) gerarExemplos(DB.livros, DB.hoje);
  DB.novidade = { novos: r.novos, saidos: r.saidos };
}
function textoNovidade() {
  const n = DB.novidade; if (!n || (!n.novos && !n.saidos)) return '';
  return ` O catálogo mudou: ${[n.novos ? plural(n.novos, 'livro entrou', 'livros entraram') : '', n.saidos ? plural(n.saidos, 'saiu', 'saíram') : ''].filter(Boolean).join(' e ')}.`;
}

/* ───────────────────────── preços ───────────────────────── */
function precoEm(pts, d) {                 // último preço observado até o dia d
  let lo = 0, hi = pts.length - 1, r = -1;
  while (lo <= hi) { const m = (lo + hi) >> 1; if (pts[m][0] <= d) { r = m; lo = m + 1; } else hi = m - 1; }
  return r < 0 ? null : pts[r];
}
const modoDe = b => (virtual(b) ? 'virtual' : 'fisico');
function fontesDe(b, modo) {
  if (!b.px) return [];
  const todas = Object.keys(b.px);
  if (modo === 'todos') return todas;
  const m = todas.filter(f => tipoFonte(f) === (modo || modoDe(b)));
  return m.length ? m : todas;
}
function melhorEm(b, d, modo) {            // menor preço entre as fontes do formato desejado, na data d
  let best = null;
  for (const f of fontesDe(b, modo)) { const o = precoEm(b.px[f], d); if (o && (!best || o[1] < best.p)) best = { p: o[1], f, d: o[0] }; }
  return best;
}
function resumoPrecos(b, de, ate, modo) {  // mínimo, média e variação do melhor preço no intervalo
  const fontes = fontesDe(b, modo);
  if (!fontes.length) return null;
  const dias = new Set([ate]);
  let primeiro = Infinity;
  for (const f of fontes) { const pts = b.px[f]; if (pts.length) primeiro = Math.min(primeiro, pts[0][0]); for (const p of pts) if (p[0] >= de && p[0] <= ate) dias.add(p[0]); }
  if (!isFinite(primeiro) || primeiro > ate) return null;
  const ini = Math.max(de, primeiro); dias.add(ini);
  const ord = [...dias].filter(d => d >= ini).sort((a, b) => a - b);
  let min = Infinity, minDia = null, minFonte = '', max = -Infinity, area = 0;
  const serie = [];
  for (let i = 0; i < ord.length; i++) {
    const m = melhorEm(b, ord[i], modo); if (!m) continue;
    serie.push([ord[i], m.p]);
    if (m.p < min) { min = m.p; minDia = ord[i]; minFonte = m.f; }
    if (m.p > max) max = m.p;
    const prox = i + 1 < ord.length ? ord[i + 1] : ord[i] + 1; area += m.p * (prox - ord[i]);
  }
  if (!serie.length) return null;
  const a = serie[0][1], z = serie[serie.length - 1][1];
  return { ini: a, fim: z, min, minDia, minFonte, max, media: area / (ord[ord.length - 1] + 1 - ord[0]), var: a ? (z - a) / a : 0, serie, de: ini, ate };
}
function situacaoDe(b, d) {
  const m = b.px ? melhorEm(b, d) : null;
  if (!m) return 'sem';
  if (b.alvo == null) return 'semalvo';
  return m.p <= b.alvo ? 'agora' : m.p <= b.alvo * 1.1 ? 'quase' : 'aguardar';
}

/* ───────────────────────── dados de exemplo ─────────────────────────
   O catálogo (títulos, autores, tags, estante física, #lido, #top) é real.
   A biblioteca virtual também é real: os arquivos vêm do inventário, pelo catálogo.
   Tudo o que este gerador produz — datas e valores pagos da estante, leituras,
   lista de próximas aquisições e histórico de preços — é SIMULADO de forma
   determinística, só para dar vida ao painel.                               */
const PERFIL_LOJA = {
  'Amazon': { base: [0.66, 0.86], hold: [5, 18], vol: 0.055, bf: [0.78, 0.9], cons: [0.86, 0.95], prime: [0.84, 0.93], flash: 0.03, cent: 'livre' },
  'Estante Virtual': { base: [0.48, 0.92], hold: [6, 20], vol: 0.075, cent: 'meio' },
  'Mercado Livre': { base: [0.68, 0.94], hold: [6, 20], vol: 0.065, bf: [0.85, 0.94], cons: [0.9, 0.96], cent: 'livre' },
  'Travessa': { base: [0.88, 1.0], hold: [45, 110], vol: 0.035, bf: [0.8, 0.9], cons: [0.88, 0.94], cent: '90' },
  'Kindle': { base: [0.42, 0.66], hold: [35, 90], vol: 0.05, bf: [0.6, 0.85], prime: [0.7, 0.9], flash: 0.012, corte: [0.35, 0.6], cent: '90' },
};
function blackFriday(y) {                  // sexta-feira seguinte à 4ª quinta-feira de novembro
  const w1 = deDia(dia(y, 11, 1)).getUTCDay();
  return dia(y, 11, 1 + ((4 - w1 + 7) % 7) + 21 + 1);
}
function eventosPromo(de, ate) {
  const out = [];
  for (let y = partes(de).y; y <= partes(ate).y; y++) {
    const bf = blackFriday(y);
    out.push({ k: 'cons', n: 'Semana do Consumidor', de: dia(y, 3, 10), ate: dia(y, 3, 17) });
    out.push({ k: 'prime', n: 'Prime Day', de: dia(y, 7, 8), ate: dia(y, 7, 14) });
    out.push({ k: 'bf', n: 'Black Friday', de: bf - 6, ate: bf + 3 });
  }
  return out.filter(e => e.ate >= de && e.de <= ate);
}
function paginasAprox(b) {
  const r = mulberry32(hashStr('pg|' + b.t)); const e = b._e || 2;
  const [lo, hi] = e === 1 ? [96, 248] : e === 2 ? [256, 496] : [504, 1088];
  return Math.round((lo + r() * (hi - lo)) / 8) * 8;
}
function precoCapa(b) {
  const r = mulberry32(hashStr('capa|' + b.t)); const T = b.tags, e = b._e || 2;
  let lo, hi;
  if (T.includes('didatico')) [lo, hi] = [159, 329];
  else if (/trilogia|tetralogia|[Ss]érie|vols\./.test(b.t)) [lo, hi] = [149, 249];
  else if (e === 1) [lo, hi] = [34, 59];
  else if (e === 2) [lo, hi] = [54, 89];
  else [lo, hi] = [79, 139];
  if (T.includes('sem-pt')) { lo *= 1.7; hi *= 1.6; }
  else if (T.includes('classico') && e < 3) { lo *= 0.85; hi *= 0.85; }
  if (T.includes('HQ')) { lo = Math.max(lo, 64); hi = Math.max(hi, 119); }
  return Math.floor((lo + r() * (hi - lo)) / 5) * 5 + 4.9;
}

function gerarExemplos(livros, T) {
  const R = mulberry32(20261109);
  const rnd = (a, b) => a + R() * (b - a);
  const int = (a, b) => Math.floor(rnd(a, b + 1));
  const pesos = pares => { let s = 0; for (const p of pares) s += p[1]; let r = R() * s; for (const p of pares) { if ((r -= p[1]) <= 0) return p[0]; } return pares[pares.length - 1][0]; };
  const emb = arr => { const a = arr.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(R() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  const tem = (b, t) => b.tags.includes(t);
  // não mexe no que o usuário editou, nem no que está só na biblioteca virtual (arquivos de verdade, sem compra a simular)
  const base = livros.filter(b => !b.u && !soDigital(b));
  for (const b of base) { b.pg = paginasAprox(b); b.demo = 1; }

  /* 1 ▸ estante física: quando e onde cada livro foi comprado */
  const estante = base.filter(b => tem(b, 'tenho-fisico'));
  const PESO_MES = [1.0, 0.7, 1.0, 0.9, 0.9, 0.8, 1.1, 0.9, 0.8, 1.2, 2.2, 1.5];
  const faixas = [[5400, 2190, 0.37], [2190, 1460, 0.135], [1460, 730, 0.175], [730, 365, 0.145], [365, 1, 0.175]];
  const fixos = estante.filter(b => tem(b, 'didatico') || tem(b, 'parentalidade'));
  const vagas = [];
  faixas.forEach((f, i) => { let n = Math.round(f[2] * estante.length) - (i === 1 ? fixos.length : 0); for (let k = 0; k < n; k++) vagas.push(i); });
  const resto = emb(estante.filter(b => !fixos.includes(b)));
  const plano = fixos.map(b => [b, 1]).concat(resto.map((b, i) => [b, vagas[i] != null ? vagas[i] : 0]));
  const dataNaFaixa = (a, z) => { for (let k = 0; k < 24; k++) { const d = T - int(z, a); if (R() * 2.2 < PESO_MES[partes(d).m - 1]) return d; } return T - int(z, a); };
  for (const [b, fx] of plano) {
    let d = dataNaFaixa(faixas[fx][0], faixas[fx][1]);
    const ano = partes(d).y;
    let origem = ano < 2014
      ? pesos([['Livraria', 55], ['Sebo', 25], ['Feira do Livro', 12], ['Presente', 8]])
      : pesos([['Amazon', 40], ['Estante Virtual', 16], ['Livraria', 13], ['Feira do Livro', 12], ['Sebo', 7], ['Mercado Livre', 4], ['Presente', 8]]);
    if (tem(b, 'didatico')) origem = pesos([['Amazon', 50], ['Livraria', 35], ['Estante Virtual', 15]]);
    if (origem === 'Feira do Livro') {                          // a feira acontece entre o fim de outubro e meados de novembro
      let y = ano; let a = dia(y, 10, 30), z = dia(y, 11, 15);
      if (a > T - 1) { y--; a = dia(y, 10, 30); z = dia(y, 11, 15); }
      d = int(a, Math.min(z, T - 1));
    }
    const capa = precoCapa(b), anos = (T - d) / 365.25, defl = Math.pow(1.055, -anos);
    const fator = { 'Amazon': [0.72, 0.9], 'Estante Virtual': [0.36, 0.6], 'Sebo': [0.3, 0.55], 'Livraria': [0.95, 1], 'Feira do Livro': [0.75, 0.85], 'Mercado Livre': [0.7, 0.9] }[origem];
    const cond = origem === 'Presente' ? 'presente' : (origem === 'Sebo' || origem === 'Estante Virtual') ? 'usado' : 'novo';
    let pago = 0;
    if (fator) { pago = capa * defl * rnd(fator[0], fator[1]); pago = cond === 'usado' ? Math.max(5, Math.round(pago)) : Math.floor(pago) + 0.9; }
    Object.assign(b, { col: 'acervo', fmt: 'fisico', plat: '', adq: d, add: d, pago, loja: origem, cond });
  }

  /* 2 ▸ biblioteca virtual: é a de verdade (vem do catálogo); nada é simulado. Sobram, para as listas abaixo, os livros que não tenho */
  const livres = base.filter(b => b.col === 'rec' && !tem(b, 'lido'));
  const usados = new Set();
  const toma = (lista, n) => { const out = []; for (const b of emb(lista)) { if (out.length >= n) break; if (!usados.has(b)) { usados.add(b); out.push(b); } } return out; };
  const semTop = b => !tem(b, 'top');

  /* 3 ▸ leituras: uma linha do tempo de conclusões (ritmo de ~2 livros/mês hoje, mais lento no passado),
         atribuída a livros que já estavam no acervo naquela data — de preferência os comprados há pouco */
  const acervo = base.filter(b => b.col === 'acervo' && b.adq != null);
  const primeira = acervo.length ? Math.min(...acervo.map(b => b.adq)) : T;
  const fins = [];
  for (let d = T - int(2, 9); d > primeira + 40;) {
    fins.push(d);
    const anos = (T - d) / 365;
    const media = anos < 1 ? 14.5 : anos < 2 ? 17 : anos < 4 ? 40 : anos < 8 ? 85 : 150;
    d -= Math.max(3, Math.round(media * rnd(0.45, 1.6)));
  }
  // só a estante entra nesta simulação (a biblioteca virtual não tem datas): sem um teto, o ritmo acima a daria quase toda por lida
  for (const teto = Math.round(acervo.length * 0.6); fins.length > teto;) fins.splice(Math.floor(R() * fins.length), 1);
  fins.reverse();
  for (const b of acervo) b.leit = 'fila';
  for (const d of fins) {
    const cand = acervo.filter(b => b.leit === 'fila' && b.adq <= d - 4);
    if (!cand.length) continue;
    const w = cand.map(b => (Math.exp(-(d - b.adq) / 240) + 0.07) * (b._d === 3 ? 0.45 : 1) * (tem(b, 'didatico') ? 0.3 : 1) * (b.fmt === 'audio' ? 2.2 : 1) * (b._e === 3 ? 0.8 : 1));
    let r = R() * soma(w), k = 0; while (k < cand.length - 1 && (r -= w[k]) > 0) k++;
    Object.assign(cand[k], { leit: 'lido', lidoEm: d, prog: 100, nota: pesos([[5, 34], [4, 44], [3, 18], [2, 4]]) });
  }
  emb(acervo.filter(b => b.leit === 'fila' && T - b.adq > 240)).slice(0, 5).forEach(b => Object.assign(b, { leit: 'aband', prog: int(8, 40) }));
  const recentes = emb(acervo.filter(b => b.leit === 'fila' && T - b.adq < 200));
  const lendo = recentes.slice(0, 3);
  lendo.forEach(b => Object.assign(b, { leit: 'lendo', prog: int(14, 86) }));

  /* 4 ▸ recomendações: quando entraram na lista (em lotes, por eixo) */
  const lotes = {};
  for (let e = 1; e <= 16; e++) lotes[e] = [T - int(330, 600), T - int(125, 330), T - int(8, 125)];
  for (const b of base) if (b.col === 'rec') { const L = lotes[b.eixo] || lotes[5]; b.add = Math.min(T - 1, pesos([[L[0], 45], [L[1], 35], [L[2], 20]]) + int(0, 3)); }

  /* 5 ▸ próximas aquisições (a partir das prioridades #top) + itens só monitorados */
  const eventos = eventosPromo(T - 560, T);
  const arred = (v, c) => c === '90' ? Math.max(1.9, Math.floor(v) + 0.9) : c === 'meio' ? Math.max(4, Math.round(v * 2) / 2) : Math.round(v * 100) / 100;
  const serie = (fonte, capa, importado, r) => {
    const P = PERFIL_LOJA[fonte], q = (a, z) => a + r() * (z - a), ini = T - 548;
    const b0 = importado && fonte === 'Amazon' ? capa * q(0.8, 1.0) : capa * q(P.base[0], P.base[1]);
    let nivel = b0 * q(0.94, 1.04), prox = ini, promoAte = -1, promoF = 1, atual = null, ultDia = -99;
    const fEv = {}, pts = [];
    for (let d = ini; d <= T; d++) {
      if (d >= prox) {
        const alvo = b0 * Math.pow(1.06, (d - ini) / 365);
        nivel += (alvo - nivel) * 0.35;
        nivel *= Math.exp((r() + r() + r() - 1.5) * P.vol * 1.7);
        const dur = Math.round(q(P.hold[0], P.hold[1])); prox = d + dur;
        if (P.flash && r() < P.flash * dur / 7) { promoAte = d + Math.round(q(3, 8)); promoF = P.corte ? q(P.corte[0], P.corte[1]) : q(0.78, 0.9); }
      }
      let f = 1;
      for (const ev of eventos) if (d >= ev.de && d <= ev.ate && P[ev.k]) {
        const k = ev.k + ev.de; if (!(k in fEv)) fEv[k] = r() < 0.72 ? q(P[ev.k][0], P[ev.k][1]) : 1;
        f = Math.min(f, fEv[k]);
      }
      if (d <= promoAte) f = Math.min(f, promoF);
      const p = arred(nivel * f, P.cent);
      if (atual === null || p !== atual || d - ultDia >= 7 || d === T) { pts.push([d, p]); atual = p; ultDia = d; }
    }
    return pts;
  };
  const precificar = b => {
    const r = mulberry32(hashStr('px|' + b.t)), imp = tem(b, 'sem-pt');
    b.capa = precoCapa(b); b.track = true;
    const fontes = imp
      ? ['Amazon'].concat(r() < 0.85 || b.fmt === 'ebook' ? ['Kindle'] : [], r() < 0.2 ? ['Estante Virtual'] : [], r() < 0.2 ? ['Mercado Livre'] : [])
      : ['Amazon'].concat(r() < 0.92 ? ['Estante Virtual'] : [], r() < 0.85 ? ['Mercado Livre'] : [], r() < 0.7 ? ['Travessa'] : [], r() < 0.7 || b.fmt === 'ebook' ? ['Kindle'] : []);
    const px = {}; for (const f of fontes) px[f] = serie(f, b.capa, imp, r);
    // cotações registradas pelo usuário sobrevivem à regeneração e valem mais que o exemplo do mesmo dia
    if (b.px) for (const f in b.px) { const meus = b.px[f].filter(p => p[2]); if (meus.length) { const dias = new Set(meus.map(p => p[0])); px[f] = (px[f] || []).filter(p => !dias.has(p[0])).concat(meus).sort((a, z) => a[0] - z[0]); } }
    b.px = px;
  };
  const candTop = emb(livres.filter(b => tem(b, 'top') && !usados.has(b)));
  const porEixo = {}, desejos = [];
  for (const b of candTop) { if (desejos.length >= 26) break; if ((porEixo[b.eixo] = (porEixo[b.eixo] || 0) + 1) > 4) continue; desejos.push(b); usados.add(b); }
  const mediana = (b, dias) => { const v = resumoPrecos(b, T - dias, T).serie.map(p => p[1]).sort((a, z) => a - z); return v[v.length >> 1]; };
  const alvoDe = (b, a, z) => Math.max(9.9, Math.round((Math.round(mediana(b, 180) * rnd(a, z) / 5) * 5 - 0.1) * 100) / 100);
  desejos.forEach((b, i) => {
    b.col = 'desejo'; b.prio = i < 8 ? 1 : i < 18 ? 2 : 3;
    b.fmt = tem(b, 'sem-pt') ? 'ebook' : (R() < 0.12 ? 'ebook' : 'fisico');
    b.add = T - int(4, 330);
    precificar(b);
    b.alvo = alvoDe(b, 0.84, 0.97);          // "compro quando ficar uns 10% abaixo do preço de costume"
  });
  const monitorados = toma(livres.filter(b => semTop(b) && b._e >= 2 && b.col === 'rec'), 12);
  monitorados.forEach(b => { b.fmt = ''; precificar(b); b.alvo = alvoDe(b, 0.8, 0.95); });
  // algumas ofertas "de agora": queda recente na loja mais barata, para baixo do preço-alvo
  emb(desejos).slice(0, 6).concat(emb(monitorados).slice(0, 2)).forEach(b => {
    const n = int(1, 6), k = rnd(0.87, 0.985);
    if (Object.values(b.px).some(serie => serie.some(q => q[2]))) return;   // série com cotação do usuário não é retocada
    const m = melhorEm(b, T), pts = b.px[m.f];
    const p = arred(b.alvo * k, PERFIL_LOJA[m.f].cent);
    while (pts.length && pts[pts.length - 1][0] >= T - n) pts.pop();
    pts.push([T - n, p], [T, p]);
  });
  return livros;
}

/* ───────────────────────── armazenamento local ───────────────────────── */
const CHAVE = 'biblioteca-lucas:v1';
const Loja = {
  ok: false, erro: '',
  testar() { try { const k = '__t' + Math.random(); localStorage.setItem(k, '1'); localStorage.removeItem(k); this.ok = true; } catch (e) { this.ok = false; this.erro = String(e && e.name || e); } return this.ok; },
  ler() { if (!this.ok) return null; try { const s = localStorage.getItem(CHAVE); return s ? JSON.parse(s) : null; } catch (e) { return null; } },
  gravar(obj) { if (!this.ok) return false; try { localStorage.setItem(CHAVE, JSON.stringify(obj)); return true; } catch (e) { this.erro = String(e && e.name || e); return false; } },
  limpar() { if (this.ok) try { localStorage.removeItem(CHAVE); } catch (e) { /* nada */ } },
  // cópia guardada quando os dados salvos não puderam ser abertos (ver a rede de segurança em 70-app.js)
  falha() { if (!this.ok) return null; try { return localStorage.getItem(CHAVE + ':falha'); } catch (e) { return null; } },
  descartarFalha() { try { localStorage.removeItem(CHAVE + ':falha'); } catch (e) { /* nada */ } },
};
// O que é gravado de cada livro: nada de campos derivados (_…) nem de campos vazios — lerLivro devolve o valor padrão de quem falta.
// Com os mais de dois mil livros da biblioteca virtual, isso corta o que vai para o armazenamento do navegador quase pela metade.
const ZERO_PADRAO = new Set(['prog', 'nota', 'pg', 'prio', 'demo', 'u']);
const limpo = b => { const o = {}; for (const k in b) { const v = b[k]; if (k[0] === '_' || v === null || v === '' || v === false || (v === 0 && ZERO_PADRAO.has(k))) continue; o[k] = v; } return o; };

/* Dados de exemplo (datas, valores, leituras e preços simulados): o painel abre SEM eles — mostra só o que o catálogo
   afirma e o que foi registrado no painel. Eles só entram quando pedidos: em "Seus dados" ou abrindo o endereço com
   ?exemplo no fim (é assim que os testes abrem o painel). Quem tinha exemplos guardados por um painel antigo, em que
   eles vinham de fábrica, fica só com o que é seu na primeira abertura (DB.saiuExemplo → aviso). */
const DB = { livros: [], exemplos: false, hoje: 0, criadoEm: 0, novidade: null, saiuExemplo: 0 };
const PEDE_EXEMPLO = (() => { try { return /[?&]exemplo(=|&|$)/.test(location.search); } catch (e) { return false; } })();
// `demo` acompanha `exemplos` no que é gravado: diz que os exemplos foram pedidos (os painéis antigos gravavam só `exemplos`)
function serializar(cfg) { return { app: 'biblioteca-lucas', v: 1, cat: ASSINATURA, salvoEm: new Date().toISOString(), exemplos: DB.exemplos, demo: DB.exemplos ? 1 : undefined, criadoEm: DB.criadoEm, cfg: cfg || {}, livros: DB.livros.map(limpo) }; }
function carregarDB() {
  DB.hoje = hojeDia();
  Loja.testar();
  const salvo = Loja.ler();
  const livros = salvo && typeof salvo === 'object' && salvo.app === 'biblioteca-lucas' ? lerLivros(salvo.livros) : [];
  if (livros.length) {
    DB.livros = livros; DB.exemplos = !!salvo.exemplos; DB.criadoEm = typeof salvo.criadoEm === 'number' && isFinite(salvo.criadoEm) ? salvo.criadoEm : DB.hoje;
    if (DB.exemplos && !salvo.demo && !PEDE_EXEMPLO) { DB.saiuExemplo = 1 + DB.livros.filter(b => b.u).length; removerExemplos(); }   // exemplos de fábrica de um painel antigo: saem
    ajustarAoCatalogo(salvo.cat);
    return salvo.cfg && typeof salvo.cfg === 'object' ? salvo.cfg : {};
  }
  DB.livros = livrosDoCatalogo(); DB.exemplos = false; DB.criadoEm = DB.hoje;
  if (PEDE_EXEMPLO) { gerarExemplos(DB.livros, DB.hoje); DB.exemplos = true; }
  return {};
}
function removerExemplos() {
  for (const b of DB.livros) {
    if (!b.u) { estadoBase(b); continue; }
    if (b.px) {                               // itens editados ficam, mas sem as cotações simuladas
      for (const f in b.px) { b.px[f] = b.px[f].filter(p => p[2]); if (!b.px[f].length) delete b.px[f]; }
      if (!Object.keys(b.px).length) { b.px = null; if (b.col === 'rec') b.track = false; }
    }
  }
  DB.exemplos = false;
}
function restaurarExemplos() {
  for (const b of DB.livros) if (!b.u) estadoBase(b);
  gerarExemplos(DB.livros, DB.hoje); DB.exemplos = true;
}
const porId = id => DB.livros.find(b => b.id === id);
