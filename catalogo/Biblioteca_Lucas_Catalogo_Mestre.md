# Biblioteca do Lucas — Catálogo mestre

Gerado em 09/11/2026. Consolida todos os livros citados na conversa (listas anteriores, estante física e as listas coladas), **sem repetições**. Cada livro aparece uma única vez, na seção do seu eixo principal; os demais eixos ficam nas tags.

Atualizado em 10/11/2026 com a **biblioteca virtual**: os livros digitais que já estavam aqui (na estante ou entre as recomendações) ganharam `#tenho-digital`, e os demais entraram na seção 17, separados pelos mesmos eixos. Essa parte é mantida por `tools/importar_digital.py` a partir de `biblioteca-virtual/inventario.tsv`; os números e as pendências ficam em `biblioteca-virtual/RESUMO.md`.

Os **quadrinhos** da biblioteca virtual entraram na mesma data, também na seção 17, com `#HQ`. Uma série é uma linha só, sejam quantas forem as edições guardadas. A adaptação de um livro tem linha própria, com "(em quadrinhos)" ou o nome da coleção no título, e não marca o livro original como `#tenho-digital`.

Revisto em 10/11/2026 (**vistoria dos marcadores**): as linhas da biblioteca virtual ganharam dificuldade, extensão, gênero e temas, livro a livro, e o eixo de 189 delas foi corrigido; 44 linhas das seções 0 a 16 tiveram dificuldade, extensão ou marcadores recalibrados; as recomendações foram conferidas de novo com os dois acervos. Entraram também as **camadas curatoriais** e as **trilhas de leitura** (vindas da versão 3 do catálogo). O que mudou, e por quê, está em `catalogo/VISTORIA.md`.

Revisto em 11/11/2026: entraram **60 recomendações novas**, todas com edição brasileira conferida; nove recomendações que constavam como `#sem-pt` já têm edição no Brasil (sete passaram a ter o título brasileiro); e há **16 trilhas novas**, montadas a partir do que está no acervo, com livros da biblioteca virtual. Os marcadores que só existiam na biblioteca virtual passaram a valer também nas seções 0 a 16, e as afinidades, para os livros digitais dos mesmos autores. A análise dos filtros e da categorização está em `catalogo/ANALISE-DOS-FILTROS.md`.

**Como o catálogo se divide:** a seção 0 é a **estante física**; as seções 1 a 16 são as **recomendações**, por eixo temático (as que você já tem em arquivo levam `#tenho-digital`); a seção 17 é a **biblioteca virtual** — o que há em arquivo e não estava nas seções anteriores.

Formato das linhas: `Título | Autor | Tags`. As tags usam `#` (compatível com Obsidian e Notion). Para classificar depois, filtre por qualquer tag.

## Legenda de tags

**Tipo:** `#F` ficção · `#NF` não ficção · `#poesia` · `#HQ` · `#antologia`

**Dificuldade:** `#d1` leve/acessível · `#d2` média · `#d3` exigente (densa, longa ou muito técnica)

**Extensão (aprox.):** `#e1` curta (até ~250 p.) · `#e2` média (~250–500 p.) · `#e3` longa (500+ p., ou série/trilogia)

**Posse:** `#tenho-fisico` (está na estante física — ou dentro de um volume que está nela, como três textos de Lovecraft da seção 7) · `#tenho-digital` (está na biblioteca virtual) · os dois juntos quando há o livro nos dois formatos · sem nenhum dos dois, é recomendação. O antigo `#ja-tenho` virou `#tenho-fisico`.

**Status e prioridade:** `#lido` (você disse que leu) · `#top` (marcado como prioridade nas listas) · `#verificar` (autor, título ou edição a conferir) · `#sem-pt` (título em inglês, sem edição brasileira confirmada)

**Época/origem:** `#classico` · `#contemporaneo` · `#BR` · `#RS` · `#portugal` · `#latam` · `#africa` · `#asia` · `#europa-leste`

**Temas:** `#filosofia` `#existencialismo` `#etica` `#politica` `#autoritarismo` `#economia` `#geopolitica` `#psicologia` `#psicanalise` `#neurociencia` `#consciencia` `#ciencia` `#ia` `#historia` `#antropologia` `#sociologia` `#religiao` `#espiritualidade` `#espiritismo` `#umbanda` `#oriental` `#mistica` `#morte` `#memoria` `#identidade` `#raca` `#genero` `#colonialismo` `#ecologia` `#linguagem` `#guerra` `#testemunho` `#medicina` `#biografia` `#escrita` `#cinema` `#arte` `#parentalidade` `#humor` `#introducao` `#psiquiatria` `#gestao` `#esporte` `#didatico` (manual/curso) `#mitologia` `#matematica` `#biologia` `#educacao` `#programacao` `#dados` (bancos de dados, planilhas, análise de dados) `#design` `#enigmas` (mistérios, conspirações e arqueologia alternativa)

**Gêneros:** `#ficcao-cientifica` `#fantasia` `#distopia` `#utopia` `#historia-alternativa` `#horror` `#gotico` `#lovecraftiano` `#misterio` `#thriller` `#thriller-medico` `#romance-historico` `#medieval` `#antiguidade` `#roma` `#renascimento` `#pre-historia` `#neandertal` `#regional-gaucho` `#teatro` `#contos` `#cronicas` `#aventura` `#policial` `#faroeste` `#super-herois` `#manga` `#adaptacao` (adaptação de um livro para os quadrinhos). `#antologia` e `#poesia` também aparecem ao lado de `#F` ou `#NF`, quando o livro é uma coletânea de vários autores ou mistura prosa e poesia.

**Biblioteca virtual** (seção 17): usa os mesmos marcadores do resto do catálogo. Os que entraram com ela — `#autoconhecimento` `#tecnologia` `#fisica` `#behaviorismo` `#tcc` `#psicometria` `#psicopatologia` `#psicologia-analitica` `#psicologia-humanista` `#psicologia-social`, `#contos`, `#cronicas`, `#aventura` — valem, desde 11/11/2026, para as seções 0 a 16 também. A dificuldade e a extensão dessas linhas são **estimativas** feitas em 10/11/2026 a partir do título, do autor e do tipo de obra — ninguém abriu os arquivos; confira por amostragem. Nos quadrinhos, a extensão diz o tamanho da obra: um álbum (`#e1`), uma minissérie encadernada (`#e2`) ou uma série longa (`#e3`).

**Afinidades (relacionados):** `#rel-imortais` (afins a Os Imortais/Os Herdeiros) · `#rel-widows-bay` (afins a Lovecraft e Widow's Bay) · `#rel-cornwell` (afins a O Arqueiro/O Físico) · `#rel-asimov-clarke` · `#rel-yalom` · `#rel-fromm` (autoritarismo e psicologia social). Os livros dos próprios autores levam a afinidade também na biblioteca virtual.

**Camadas curatoriais** (seções 0 a 16): dizem *por que* o livro importa e com o que ele conversa.
- **Pergunta central** `#q-…`: `#q-o-que-e-humano` · `#q-liberdade-e-obediencia` · `#q-sentido-e-como-viver` · `#q-morte-e-finitude` · `#q-identidade-e-eu` · `#q-poder-e-violencia` · `#q-realidade-e-percepcao` · `#q-memoria-e-esquecimento` · `#q-fe-e-duvida` · `#q-alteridade-e-contato` · `#q-culpa-e-justica` · `#q-natureza-e-civilizacao`
- **Clima da leitura** `#clima-…`: `claustrofobico` · `melancolico` · `onirico` · `aventura` · `cerebral` · `cru-e-chocante` · `subversivo` · `emocionante` · `comico` · `contemplativo`
- **Papel na biblioteca** `#papel-…`: `porta-de-entrada` (melhor primeiro livro de uma área) · `leitura-relampago` (curto e potente) · `desafio` (exige tempo, atenção ou bagagem) · `contraponto` (para ler ao lado de uma visão oposta) · `ponte` (cruza áreas) · `fonte-primaria` (texto fundacional)
- **Pontes entre áreas** `#ponte-…`: `ciencia-e-fe` · `psicanalise-e-politica` · `literatura-e-neurociencia` · `ficcao-e-filosofia` · `historia-e-ficcao` · `ecologia-e-colonialismo` · `corpo-e-poder` · `ia-e-humanidade`
- **Cenários** `#cenario-…`: `russia` · `nova-inglaterra` · `sertao-e-nordeste` · `espaco-profundo` · `ilha-e-isolamento` · `guerra-mundial` · `oriente-feudal` · `futuro-proximo` · `cidade-pequena`
- **Trilhas de leitura** `#trilha-…`: trinta e seis roteiros, com os livros em ordem. Vinte vieram da versão 3 do catálogo; dezesseis foram montados em 11/11/2026 a partir do acervo e incluem livros da biblioteca virtual. A lista de cada trilha está em `catalogo/trilhas.md`.

---

## 0. Estante física (tenho: físico)

| Título | Autor | Tags |
|---|---|---|
| Fundação | Isaac Asimov | #F #ficcao-cientifica #classico #d1 #e1 #tenho-fisico #tenho-digital #rel-asimov-clarke #clima-cerebral #cenario-espaco-profundo #trilha-ficcao-cientifica-classica |
| As Cavernas de Aço | Isaac Asimov | #F #ficcao-cientifica #misterio #classico #d1 #e2 #tenho-fisico #rel-asimov-clarke #cenario-espaco-profundo #trilha-ficcao-cientifica-classica |
| Contos da Taberna | Arthur C. Clarke | #F #ficcao-cientifica #humor #classico #contos #d1 #e1 #tenho-fisico #rel-asimov-clarke #clima-comico #trilha-ficcao-cientifica-classica |
| O Vento Solar | Arthur C. Clarke | #F #ficcao-cientifica #classico #contos #d1 #e1 #tenho-fisico #rel-asimov-clarke |
| 1984 | George Orwell | #F #distopia #autoritarismo #classico #d2 #e2 #tenho-fisico #tenho-digital #q-liberdade-e-obediencia #trilha-liberdade-e-autoritarismo #trilha-distopias |
| A Ilha | Aldous Huxley | #F #utopia #filosofia #classico #d2 #e2 #tenho-fisico #q-liberdade-e-obediencia #cenario-ilha-e-isolamento #trilha-distopias |
| Os Sertões | Euclides da Cunha | #NF #historia #BR #classico #d3 #e3 #tenho-fisico #papel-desafio #cenario-sertao-e-nordeste #trilha-brasil-profundo |
| Guerra e Paz | Liev Tolstói (na prateleira consta Dostoiévski; autor correto: Tolstói) | #F #romance-historico #guerra #classico #d3 #e3 #tenho-fisico #papel-desafio #ponte-historia-e-ficcao #cenario-russia #trilha-alma-russa |
| Bufo & Spallanzani | Rubem Fonseca | #F #misterio #BR #d2 #e2 #tenho-fisico #trilha-crime-a-brasileira |
| 20 Poemas de Amor e uma Canção Desesperada | Pablo Neruda | #poesia #latam #classico #d1 #e1 #tenho-fisico |
| Filhos do Éden (trilogia: Herdeiros de Atlântida · Anjos da Morte · Paraíso Perdido) | Eduardo Spohr | #F #fantasia #BR #d1 #e3 #tenho-fisico |
| O Herói Discreto | Mario Vargas Llosa | #F #latam #contemporaneo #d2 #e2 #tenho-fisico |
| Os Tambores Silenciosos | Josué Guimarães | #F #BR #RS #regional-gaucho #d2 #e1 #tenho-fisico #trilha-saga-gaucha |
| Camilo Mortágua | Josué Guimarães | #F #BR #RS #regional-gaucho #d2 #e2 #tenho-fisico #trilha-saga-gaucha |
| Cevando Mate | Glênio Fagundes | #NF #BR #RS #regional-gaucho #d1 #e1 #tenho-fisico #trilha-saga-gaucha |
| Porto de Histórias | Moacyr Scliar | #F #BR #RS #regional-gaucho #cronicas #d1 #e1 #tenho-fisico #trilha-saga-gaucha |
| O Continente (vol. 1 de O Tempo e o Vento) | Erico Veríssimo | #F #romance-historico #BR #RS #regional-gaucho #classico #d2 #e3 #tenho-fisico #ponte-historia-e-ficcao #trilha-saga-gaucha |
| Do Amor e Outros Demônios | Gabriel García Márquez | #F #latam #d2 #e1 #tenho-fisico #clima-onirico #trilha-realismo-magico |
| Notícia de um Sequestro (Noticia de un Secuestro) | Gabriel García Márquez | #NF #latam #testemunho #d2 #e2 #tenho-fisico |
| La Otra Orilla | Julio Cortázar | #F #latam #contos #d3 #e1 #tenho-fisico #trilha-realismo-magico |
| O Informe de Brodie | Jorge Luis Borges | #F #latam #classico #contos #d2 #e1 #tenho-fisico #tenho-digital #trilha-labirintos-de-borges |
| Blecaute | Marcelo Rubens Paiva | #F #BR #d1 #e1 #tenho-fisico |
| Tieta do Agreste | Jorge Amado | #F #BR #classico #d1 #e3 #tenho-fisico #cenario-sertao-e-nordeste |
| Ensaios e Anseios Crípticos | Paulo Leminski | #NF #poesia #linguagem #BR #d2 #e1 #tenho-fisico |
| O Cirurgião | Tess Gerritsen | #F #thriller-medico #thriller #d1 #e2 #tenho-fisico #trilha-plantao-noturno |
| Valsa Maldita | Tess Gerritsen | #F #thriller-medico #thriller #d1 #e2 #tenho-fisico |
| Erro Médico | Robin Cook | #F #thriller-medico #thriller #d1 #e2 #tenho-fisico #tenho-digital #trilha-plantao-noturno |
| Contos (Edgar Allan Poe) | Edgar Allan Poe | #F #horror #gotico #classico #contos #d2 #e2 #tenho-fisico #tenho-digital |
| Contos (H.P. Lovecraft) | H.P. Lovecraft | #F #horror #lovecraftiano #classico #contos #d2 #e2 #tenho-fisico #rel-widows-bay |
| Contos (Sir Arthur Conan Doyle) | Arthur Conan Doyle | #F #misterio #classico #contos #d1 #e2 #tenho-fisico |
| O Aprendiz de Assassino | Robin Hobb | #F #fantasia #d1 #e2 #tenho-fisico #tenho-digital #trilha-fantasia-de-folego |
| O Cavaleiro dos Sete Reinos | George R.R. Martin | #F #fantasia #d1 #e2 #tenho-fisico #trilha-fantasia-de-folego |
| Cartas de um Diabo a seu Aprendiz | C.S. Lewis | #F #religiao #humor #classico #d2 #e1 #tenho-fisico #tenho-digital #q-fe-e-duvida #clima-comico |
| História do Cerco de Lisboa | José Saramago | #F #portugal #romance-historico #d3 #e2 #tenho-fisico |
| A Peste | Albert Camus | #F #existencialismo #etica #classico #d2 #e2 #tenho-fisico #q-morte-e-finitude |
| O Xamã | Noah Gordon | #F #romance-historico #medicina #d1 #e3 #tenho-fisico #tenho-digital #rel-cornwell #trilha-bisturi-e-fe |
| O Profeta | Khalil Gibran | #F #poesia #espiritualidade #classico #d1 #e1 #tenho-fisico #q-sentido-e-como-viver #clima-contemplativo |
| Megalomania de Freud | Israel Rosenfield | #F #psicanalise #d2 #e1 #tenho-fisico |
| Mentiras no Divã | Irvin D. Yalom | #F #psicologia #d1 #e2 #tenho-fisico #rel-yalom |
| Mamãe e o Sentido da Vida | Irvin D. Yalom | #F #psicologia #existencialismo #contos #d1 #e2 #tenho-fisico #rel-yalom #q-sentido-e-como-viver |
| Quando Nietzsche Chorou | Irvin D. Yalom | #F #psicologia #filosofia #d1 #e2 #tenho-fisico #rel-yalom #papel-porta-de-entrada #ponte-ficcao-e-filosofia #trilha-yalom-nietzsche |
| O Homem e seus Símbolos | Carl G. Jung | #NF #psicologia #psicanalise #psicologia-analitica #d2 #e2 #tenho-fisico #tenho-digital #trilha-jung-para-comecar |
| Inteligência Emocional | Daniel Goleman | #NF #psicologia #autoconhecimento #d1 #e2 #tenho-fisico #tenho-digital |
| Investigações Cognitivas | Marcos Barbosa de Oliveira e Marta Kohl de Oliveira (orgs.) | #NF #psicologia #neurociencia #d2 #e1 #tenho-fisico |
| Desvendando os Segredos da Linguagem Corporal | Allan e Barbara Pease | #NF #psicologia #autoconhecimento #d1 #e2 #tenho-fisico #tenho-digital |
| Por que os Homens Fazem Sexo e as Mulheres Fazem Amor? | Allan e Barbara Pease | #NF #psicologia #autoconhecimento #d1 #e2 #tenho-fisico |
| Além do Bem e do Mal | Friedrich Nietzsche | #NF #filosofia #classico #d3 #e2 #tenho-fisico #tenho-digital #trilha-yalom-nietzsche |
| Ecce Homo | Friedrich Nietzsche | #NF #filosofia #classico #d3 #e1 #tenho-fisico #trilha-yalom-nietzsche |
| Filosofia: Novas Respostas para Antigas Questões | Nicholas Fearn | #NF #filosofia #introducao #d1 #e2 #tenho-fisico |
| Pensamento Crítico de A a Z | Nigel Warburton | #NF #filosofia #introducao #d1 #e1 #tenho-fisico #papel-porta-de-entrada |
| Sobre o que nos Perguntam os Grandes Filósofos | Leszek Kołakowski | #NF #filosofia #introducao #d2 #e2 #tenho-fisico |
| Convite à Filosofia | Marilena Chaui | #NF #filosofia #introducao #BR #d2 #e3 #tenho-fisico #tenho-digital |
| Se Liga na Filosofia | Globo Livros | #NF #filosofia #introducao #d1 #e1 #tenho-fisico #papel-porta-de-entrada |
| Grandes Questões da Ciência | Harriet Swain | #NF #ciencia #d1 #e2 #tenho-fisico |
| A Longa Marcha dos Grilos Canibais | Fernando Reinach | #NF #ciencia #BR #d1 #e2 #tenho-fisico #tenho-digital |
| O Futuro | Al Gore | #NF #politica #ciencia #contemporaneo #d2 #e3 #tenho-fisico |
| O Segundo Mundo | Parag Khanna | #NF #geopolitica #politica #d2 #e3 #tenho-fisico |
| O Novo Papel do Pai | Paul Raeburn | #NF #parentalidade #d1 #e2 #tenho-fisico #trilha-pai-em-construcao |
| Inteligência Emocional e a Arte de Educar Nossos Filhos (A Arte de Criar Nossos Filhos) | John Gottman e Joan Declaire | #NF #parentalidade #psicologia #d1 #e2 #tenho-fisico #trilha-pai-em-construcao |
| Primatas da Park Avenue | Wednesday Martin | #NF #sociologia #antropologia #humor #d1 #e2 #tenho-fisico #tenho-digital #clima-comico |
| Cem Anos de Solidão | Gabriel García Márquez | #F #latam #d2 #e2 #top #tenho-fisico #tenho-digital #clima-onirico #cenario-cidade-pequena #trilha-realismo-magico |
| Crime e Castigo | Fiódor Dostoiévski | #F #etica #existencialismo #classico #d2 #e3 #top #tenho-fisico #tenho-digital #q-culpa-e-justica #cenario-russia #trilha-alma-russa |
| Notas do Subsolo (Memórias do Subsolo) | Fiódor Dostoiévski | #F #existencialismo #classico #d2 #e1 #tenho-fisico #tenho-digital #clima-claustrofobico #ponte-ficcao-e-filosofia #cenario-russia #trilha-alma-russa |
| Assim Falou Zaratustra | Friedrich Nietzsche | #NF #filosofia #classico #d3 #e2 #tenho-fisico #tenho-digital #trilha-yalom-nietzsche |
| Psicologia das Massas e Análise do Eu | Sigmund Freud | #NF #psicanalise #autoritarismo #classico #psicologia-social #d2 #e1 #top #tenho-fisico #rel-fromm #q-liberdade-e-obediencia #ponte-psicanalise-e-politica #trilha-liberdade-e-autoritarismo #trilha-psicanalise-em-degraus |
| O Mundo de Sofia | Jostein Gaarder | #F #filosofia #introducao #d1 #e3 #tenho-fisico #tenho-digital #papel-porta-de-entrada #ponte-ficcao-e-filosofia #trilha-filosofia-em-doses |
| Lovecraft: Medo Clássico (volume único) | H.P. Lovecraft | #F #horror #lovecraftiano #classico #contos #d2 #e3 #tenho-fisico #rel-widows-bay #trilha-lovecraft-widows-bay |
| Rei do Inverno (Crônicas de Artur, vol. 1) | Bernard Cornwell | #F #romance-historico #medieval #guerra #d1 #e3 #tenho-fisico #tenho-digital #rel-cornwell #trilha-aco-e-fe |
| O Andarilho (Busca do Graal, vol. 2) | Bernard Cornwell | #F #romance-historico #medieval #guerra #d1 #e2 #tenho-fisico #rel-cornwell #trilha-aco-e-fe |
| Herege (Busca do Graal, vol. 3) | Bernard Cornwell | #F #romance-historico #medieval #religiao #d1 #e2 #tenho-fisico #rel-cornwell #q-fe-e-duvida #trilha-aco-e-fe |
| Médico de Cuerpos y Almas | Taylor Caldwell | #F #romance-historico #medicina #antiguidade #d1 #e3 #tenho-fisico #rel-cornwell #trilha-bisturi-e-fe |
| Apocalipse: A Batalha do Fim | Eduardo Spohr | #F #fantasia #BR #d1 #e3 #tenho-fisico |
| Coraline | Neil Gaiman e Dave (P. Craig) Russell | #HQ #fantasia #gotico #verificar #d1 #e1 #tenho-fisico #tenho-digital |
| O Livro do Cemitério | Neil Gaiman | #F #fantasia #gotico #d1 #e2 #tenho-fisico |
| Noite do Sul | Érico Veríssimo | #F #BR #RS #regional-gaucho #verificar #d2 #e2 #tenho-fisico #trilha-saga-gaucha |
| Comédias da Vida Pública | Luis Fernando Verissimo | #F #humor #BR #RS #politica #cronicas #d1 #e1 #tenho-fisico #clima-comico #trilha-saga-gaucha |
| Pantaleão e as Visitadoras | Mario Vargas Llosa | #F #latam #humor #d1 #e2 #tenho-fisico #clima-comico |
| A Ilha (Benchley) | Peter Benchley | #F #thriller #aventura #d1 #e2 #tenho-fisico #cenario-ilha-e-isolamento |
| O Plano Perfeito | Sidney Sheldon | #F #thriller #d1 #e2 #tenho-fisico |
| Corpo | Carlos Drummond de Andrade | #poesia #BR #classico #d2 #e1 #tenho-fisico |
| Invictus: Nelson Mandela e o Jogo que Uniu a África do Sul | John Carlin | #NF #historia #africa #politica #esporte #d1 #e2 #tenho-fisico #clima-emocionante |
| 71 Segundos: O Jogo de uma Vida | Luiz Zini Pires | #NF #esporte #BR #d1 #e1 #tenho-fisico |
| A Imperatriz de Ferro | Jung Chang | #NF #biografia #historia #asia #d2 #e3 #tenho-fisico |
| História da Riqueza no Brasil | Jorge Caldeira | #NF #historia #economia #BR #d2 #e3 #tenho-fisico #trilha-brasil-profundo |
| Sérgio Cabral: O Homem que Queria ser Rei | Hudson Corrêa | #NF #biografia #politica #BR #d1 #e2 #tenho-fisico |
| O Primeiro Ano: Como se Faz um Advogado | Scott Turow | #NF #biografia #d1 #e2 #tenho-fisico |
| Nietzsche Hoje | Viviane Mosé | #NF #filosofia #BR #d2 #e2 #tenho-fisico #trilha-yalom-nietzsche |
| A Arte de Envelhecer | Irvin D. Yalom (conforme a prateleira) | #NF #psicologia #verificar #d1 #e2 #tenho-fisico #rel-yalom #q-sentido-e-como-viver |
| As 5 Linguagens do Amor | Gary Chapman | #NF #psicologia #autoconhecimento #d1 #e1 #tenho-fisico |
| Superação e Equilíbrio Emocional | Leo Fraiman | #NF #psicologia #autoconhecimento #d1 #e2 #tenho-fisico |
| Estados Emocionais Alterados: Psiquiatria Espiritual | Cristina Neves | #NF #psiquiatria #espiritualidade #espiritismo #d2 #e2 #tenho-fisico #ponte-ciencia-e-fe #trilha-fronteiras-do-inexplicavel |
| Terapia Cognitivo-Comportamental na Prática Psiquiátrica | Paulo Knapp | #NF #psiquiatria #psicologia #didatico #tcc #d3 #e3 #tenho-fisico |
| Transtorno do Déficit de Atenção | Condemarin, Gorostegui e Milicic | #NF #psicologia #didatico #psicopatologia #d2 #e2 #tenho-fisico |
| Psicopatologia | David H. Barlow e V. Mark Durand | #NF #psiquiatria #psicologia #didatico #psicopatologia #d3 #e3 #tenho-fisico #tenho-digital |
| História da Psicologia Moderna | Duane P. Schultz e Sydney E. Schultz | #NF #psicologia #historia #didatico #d3 #e3 #tenho-fisico #tenho-digital #trilha-formacao-do-terapeuta |
| Teorias da Personalidade | Hall, Lindzey e Campbell | #NF #psicologia #didatico #d3 #e3 #tenho-fisico #trilha-formacao-do-terapeuta |
| Tecnologias e Ferramentas de Gestão (PLT 148) | Décio Henrique Franco e outros (orgs.) | #NF #gestao #didatico #d2 #e2 #tenho-fisico |

---

## 1. Pré-história, neandertais e origens

| Título | Autor | Tags |
|---|---|---|
| Os Imortais | Paulliny Tort | #F #pre-historia #neandertal #BR #contemporaneo #d3 #e2 #top #rel-imortais #tenho-digital #q-o-que-e-humano #trilha-origens |
| Os Herdeiros | William Golding | #F #pre-historia #neandertal #classico #d3 #e1 #rel-imortais #tenho-digital #q-o-que-e-humano #q-alteridade-e-contato #papel-leitura-relampago #trilha-origens |
| Erva Brava | Paulliny Tort | #F #BR #contemporaneo #d2 #e2 #rel-imortais |
| Senhor das Moscas | William Golding | #F #politica #classico #d2 #e1 #rel-imortais #tenho-digital #q-o-que-e-humano #q-natureza-e-civilizacao #cenario-ilha-e-isolamento |
| O Clã do Urso das Cavernas (Ayla, a Filha das Cavernas) | Jean M. Auel | #F #pre-historia #neandertal #d1 #e3 #top #rel-imortais #q-o-que-e-humano #papel-porta-de-entrada #trilha-origens |
| A Guerra do Fogo | J.-H. Rosny | #F #pre-historia #classico #verificar #d2 #e1 #rel-imortais |
| Antes de Adão | Jack London | #F #pre-historia #classico #d1 #e1 #rel-imortais #q-o-que-e-humano #trilha-origens |
| Hominídeos | Robert J. Sawyer | #F #neandertal #ficcao-cientifica #d1 #e2 #rel-imortais #q-o-que-e-humano |
| A Dança do Tigre (Dance of the Tiger) | Björn Kurtén | #F #neandertal #pre-historia #sem-pt #d2 #e2 #rel-imortais #q-o-que-e-humano |
| Shaman | Kim Stanley Robinson | #F #pre-historia #sem-pt #d2 #e2 #rel-imortais |
| The Last Neanderthal | Claire Cameron | #F #neandertal #pre-historia #sem-pt #d1 #e2 #rel-imortais #q-o-que-e-humano |
| Stonehenge | Bernard Cornwell | #F #pre-historia #romance-historico #d1 #e2 #rel-cornwell #tenho-digital |
| Ismael | Daniel Quinn | #F #filosofia #ecologia #d2 #e2 #top #rel-imortais #q-o-que-e-humano #q-natureza-e-civilizacao #clima-subversivo #papel-ponte #trilha-origens |
| Neandertal: À Procura de Genomas Perdidos | Svante Pääbo | #NF #ciencia #neandertal #biologia #pre-historia #d2 #e2 #rel-imortais #q-o-que-e-humano #trilha-origens |
| Kindred: Neanderthal Life, Love, Death and Art | Rebecca Wragg Sykes | #NF #neandertal #ciencia #sem-pt #pre-historia #d2 #e2 #rel-imortais #q-o-que-e-humano #trilha-origens |
| Sapiens: Uma Breve História da Humanidade | Yuval Noah Harari | #NF #historia #antropologia #d1 #e2 #rel-imortais #tenho-digital #q-o-que-e-humano #q-natureza-e-civilizacao #papel-porta-de-entrada #papel-contraponto |
| Armas, Germes e Aço | Jared Diamond | #NF #historia #antropologia #d2 #e3 #q-natureza-e-civilizacao |
| Círculo dos Dias | Ken Follett | #F #pre-historia #romance-historico #d1 #e2 #rel-cornwell #clima-aventura #ponte-historia-e-ficcao |

---

## 2. Ficção científica, fantasia e distopia

| Título | Autor | Tags |
|---|---|---|
| 2001: Uma Odisseia no Espaço | Arthur C. Clarke | #F #ficcao-cientifica #classico #d2 #e2 #rel-asimov-clarke #cenario-espaco-profundo #trilha-ficcao-cientifica-classica |
| O Fim da Infância | Arthur C. Clarke | #F #ficcao-cientifica #classico #d2 #e2 #rel-asimov-clarke #tenho-digital #cenario-espaco-profundo #trilha-ficcao-cientifica-classica |
| Eu, Robô | Isaac Asimov | #F #ficcao-cientifica #ia #classico #contos #d1 #e2 #rel-asimov-clarke #tenho-digital #papel-porta-de-entrada #ponte-ia-e-humanidade #trilha-ficcao-cientifica-classica #trilha-maquinas-que-pensam |
| Crônicas Marcianas | Ray Bradbury | #F #ficcao-cientifica #classico #contos #d1 #e2 |
| Fahrenheit 451 | Ray Bradbury | #F #distopia #classico #d1 #e1 #tenho-digital #q-liberdade-e-obediencia #papel-leitura-relampago #trilha-distopias #trilha-relampago |
| Um Estranho numa Terra Estranha | Robert A. Heinlein | #F #ficcao-cientifica #classico #d2 #e3 #tenho-digital |
| Nós | Ievguêni Zamiátin | #F #distopia #classico #d2 #e1 #tenho-digital #q-liberdade-e-obediencia #cenario-russia #trilha-distopias |
| Piquenique na Estrada | Irmãos Strugatski | #F #ficcao-cientifica #classico #d2 #e1 #q-alteridade-e-contato |
| Duna | Frank Herbert | #F #ficcao-cientifica #politica #classico #d2 #e3 #top #tenho-digital #clima-aventura #cenario-espaco-profundo #trilha-ficcao-cientifica-classica |
| Neuromancer | William Gibson | #F #ficcao-cientifica #ia #d2 #e2 #tenho-digital #ponte-ia-e-humanidade #cenario-futuro-proximo #trilha-ficcao-cientifica-classica |
| Hyperion | Dan Simmons | #F #ficcao-cientifica #d2 #e3 #tenho-digital #clima-aventura #cenario-espaco-profundo |
| O Problema dos Três Corpos | Cixin Liu | #F #ficcao-cientifica #asia #d2 #e2 #tenho-digital #clima-cerebral #cenario-espaco-profundo #trilha-ficcao-cientifica-classica |
| Androides Sonham com Ovelhas Elétricas? | Philip K. Dick | #F #ficcao-cientifica #consciencia #classico #d1 #e1 #tenho-digital #q-o-que-e-humano #ponte-ia-e-humanidade #cenario-futuro-proximo |
| O Homem do Castelo Alto | Philip K. Dick | #F #historia-alternativa #classico #d2 #e2 #q-realidade-e-percepcao |
| Solaris | Stanisław Lem | #F #ficcao-cientifica #consciencia #filosofia #classico #d2 #e2 #top #rel-imortais #tenho-digital #q-o-que-e-humano #q-realidade-e-percepcao #q-alteridade-e-contato #clima-onirico #papel-ponte #ponte-literatura-e-neurociencia #ponte-ficcao-e-filosofia #cenario-espaco-profundo #trilha-alteridade #trilha-ficcao-cientifica-classica #trilha-mente-e-cerebro |
| A Mão Esquerda da Escuridão | Ursula K. Le Guin | #F #ficcao-cientifica #genero #antropologia #classico #d2 #e2 #rel-imortais #tenho-digital #q-alteridade-e-contato #trilha-alteridade |
| Os Despossuídos | Ursula K. Le Guin | #F #ficcao-cientifica #politica #utopia #classico #d2 #e2 #rel-imortais #tenho-digital #q-alteridade-e-contato #ponte-ficcao-e-filosofia #cenario-espaco-profundo |
| Floresta é o Nome do Mundo | Ursula K. Le Guin | #F #ficcao-cientifica #colonialismo #ecologia #classico #d1 #e1 #rel-imortais #tenho-digital #q-alteridade-e-contato #q-natureza-e-civilizacao #ponte-ecologia-e-colonialismo #trilha-alteridade |
| A Curva do Sonho | Ursula K. Le Guin | #F #ficcao-cientifica #consciencia #classico #d2 #e1 #tenho-digital #q-realidade-e-percepcao #clima-onirico |
| O Feiticeiro de Terramar (Ciclo Terramar, vol. 1) | Ursula K. Le Guin | #F #fantasia #classico #d1 #e1 #tenho-digital #trilha-fantasia-de-folego |
| Despertar (Xenogênese) | Octavia E. Butler | #F #ficcao-cientifica #raca #d2 #e2 #rel-imortais #q-alteridade-e-contato #trilha-alteridade |
| A Parábola do Semeador | Octavia E. Butler | #F #distopia #ecologia #d2 #e2 #rel-imortais #q-natureza-e-civilizacao #ponte-ecologia-e-colonialismo #cenario-futuro-proximo |
| Kindred: Laços de Sangue | Octavia E. Butler | #F #raca #historia #d2 #e2 |
| A Máquina do Tempo | H.G. Wells | #F #ficcao-cientifica #classico #d1 #e1 #q-natureza-e-civilizacao #papel-leitura-relampago |
| O Guia do Mochileiro das Galáxias | Douglas Adams | #F #ficcao-cientifica #humor #d1 #e1 #clima-comico |
| Matadouro 5 | Kurt Vonnegut | #F #guerra #ficcao-cientifica #classico #d2 #e1 #cenario-guerra-mundial |
| Flores para Algernon | Daniel Keyes | #F #ficcao-cientifica #psicologia #classico #d1 #e1 #tenho-digital #q-o-que-e-humano #clima-emocionante #papel-leitura-relampago #ponte-literatura-e-neurociencia |
| A Invenção de Morel | Adolfo Bioy Casares | #F #latam #ficcao-cientifica #classico #d2 #e1 #tenho-digital #q-realidade-e-percepcao #clima-onirico #cenario-ilha-e-isolamento |
| As Cosmicômicas | Italo Calvino | #F #ficcao-cientifica #ciencia #classico #contos #d2 #e1 #rel-imortais #clima-onirico #clima-cerebral #papel-ponte |
| O Poder | Naomi Alderman | #F #distopia #genero #d1 #e2 #cenario-futuro-proximo |
| A Cidade e a Cidade | China Miéville | #F #misterio #ficcao-cientifica #d2 #e2 #tenho-digital #q-realidade-e-percepcao #clima-cerebral |
| Embassytown | China Miéville | #F #ficcao-cientifica #linguagem #d3 #e2 #q-alteridade-e-contato #clima-cerebral #cenario-espaco-profundo |
| Permutation City | Greg Egan | #F #ficcao-cientifica #consciencia #ia #sem-pt #d3 #e2 #q-identidade-e-eu #clima-cerebral #ponte-ia-e-humanidade |
| A História da Sua Vida e Outros Contos | Ted Chiang | #F #ficcao-cientifica #linguagem #contos #d2 #e2 #top #q-alteridade-e-contato #clima-cerebral #papel-ponte #trilha-alteridade |
| Exalação | Ted Chiang | #F #ficcao-cientifica #ia #contos #d2 #e2 #clima-cerebral |
| O Livro das Coisas Estranhas | Michel Faber | #F #ficcao-cientifica #religiao #d2 #e3 #q-fe-e-duvida #cenario-espaco-profundo |
| Os Empregados | Olga Ravn | #F #ficcao-cientifica #ia #d2 #e1 #q-o-que-e-humano #ponte-ia-e-humanidade #cenario-espaco-profundo |
| Klara e o Sol | Kazuo Ishiguro | #F #ia #contemporaneo #d1 #e2 #q-o-que-e-humano #clima-melancolico #ponte-literatura-e-neurociencia #ponte-ia-e-humanidade #cenario-futuro-proximo #trilha-maquinas-que-pensam |
| Não Me Abandone Jamais | Kazuo Ishiguro | #F #ficcao-cientifica #etica #contemporaneo #d1 #e2 #top #tenho-digital #q-o-que-e-humano #clima-melancolico #ponte-ia-e-humanidade #cenario-futuro-proximo |
| Frankenstein | Mary Shelley | #F #gotico #ficcao-cientifica #classico #d2 #e2 #q-o-que-e-humano #papel-ponte #ponte-ciencia-e-fe |
| A Estrada | Cormac McCarthy | #F #distopia #contemporaneo #d1 #e1 #top #rel-imortais #q-natureza-e-civilizacao #clima-melancolico #clima-emocionante #papel-porta-de-entrada #papel-leitura-relampago #cenario-futuro-proximo #trilha-relampago |
| Admirável Mundo Novo | Aldous Huxley | #F #distopia #classico #d2 #e2 #tenho-digital #q-liberdade-e-obediencia #trilha-distopias |
| A Revolução dos Bichos | George Orwell | #F #distopia #politica #classico #d1 #e1 #tenho-digital #q-liberdade-e-obediencia #clima-subversivo #papel-leitura-relampago #trilha-distopias |
| O Conto da Aia | Margaret Atwood | #F #distopia #genero #autoritarismo #d1 #e2 #tenho-digital #q-liberdade-e-obediencia #clima-subversivo #ponte-corpo-e-poder #cenario-futuro-proximo #trilha-distopias #trilha-corpo-genero-poder |
| Os Cães da Peste | Richard Adams | #F #etica #d2 #e2 #q-o-que-e-humano |
| The Mandibles | Lionel Shriver | #F #distopia #economia #sem-pt #d2 #e3 #cenario-futuro-proximo |
| A Parede | Marlen Haushofer | #F #distopia #d2 #e2 #q-natureza-e-civilizacao #clima-claustrofobico #cenario-ilha-e-isolamento |
| A Polícia da Memória | Yoko Ogawa | #F #distopia #memoria #asia #d1 #e2 #tenho-digital #q-memoria-e-esquecimento |
| O Senhor dos Anéis | J.R.R. Tolkien | #F #fantasia #classico #d2 #e3 #clima-aventura #trilha-fantasia-de-folego |
| O Nome do Vento | Patrick Rothfuss | #F #fantasia #d1 #e3 #tenho-digital #clima-aventura #trilha-fantasia-de-folego |
| O Último Desejo | Andrzej Sapkowski | #F #fantasia #d1 #e2 #clima-aventura |
| O Livro das Coisas Perdidas | John Connolly | #F #fantasia #gotico #d1 #e2 #clima-onirico |
| Jurassic Park | Michael Crichton | #F #ciencia #ficcao-cientifica #thriller #aventura #d1 #e2 #clima-aventura |
| Devoradores de Estrelas | Andy Weir | #F #ficcao-cientifica #ciencia #d1 #e2 #rel-asimov-clarke #q-alteridade-e-contato #clima-aventura #cenario-espaco-profundo |
| A Cidade e as Estrelas | Arthur C. Clarke | #F #ficcao-cientifica #classico #d1 #e2 #rel-asimov-clarke #q-natureza-e-civilizacao |
| Os Próprios Deuses | Isaac Asimov | #F #ficcao-cientifica #classico #d2 #e2 #rel-asimov-clarke #q-alteridade-e-contato |
| O Planeta dos Macacos | Pierre Boulle | #F #ficcao-cientifica #classico #d1 #e1 #rel-imortais #q-o-que-e-humano #papel-leitura-relampago |
| A Longa Viagem a um Pequeno Planeta Hostil | Becky Chambers | #F #ficcao-cientifica #d1 #e2 #q-alteridade-e-contato #clima-emocionante #cenario-espaco-profundo |
| Estação Onze | Emily St. John Mandel | #F #distopia #contemporaneo #d1 #e2 #q-memoria-e-esquecimento #clima-melancolico #cenario-futuro-proximo |
| Piranesi | Susanna Clarke | #F #fantasia #d1 #e1 #q-realidade-e-percepcao #clima-onirico #papel-leitura-relampago #trilha-labirintos-de-borges |
| Babel | R.F. Kuang | #F #fantasia #historia-alternativa #colonialismo #linguagem #d2 #e3 #q-poder-e-violencia #clima-subversivo |

---

## 3. Clássicos universais e romances de ideias

| Título | Autor | Tags |
|---|---|---|
| Dom Quixote | Miguel de Cervantes | #F #classico #d3 #e3 #tenho-digital #papel-desafio |
| A Divina Comédia | Dante Alighieri | #poesia #religiao #classico #d3 #e3 #tenho-digital #papel-desafio #papel-fonte-primaria |
| Odisseia | Homero | #F #antiguidade #classico #mitologia #d2 #e2 #papel-fonte-primaria |
| Édipo Rei | Sófocles | #F #antiguidade #teatro #classico #d1 #e1 #papel-leitura-relampago |
| Hamlet | William Shakespeare | #F #teatro #classico #d2 #e1 |
| Fausto | Johann W. von Goethe | #F #classico #d3 #e2 #tenho-digital #papel-desafio #ponte-ficcao-e-filosofia |
| Cândido | Voltaire | #F #filosofia #humor #classico #d1 #e1 #q-sentido-e-como-viver #clima-subversivo #clima-comico #papel-leitura-relampago #ponte-ficcao-e-filosofia #trilha-relampago |
| Anna Kariênina | Liev Tolstói | #F #classico #d2 #e3 #cenario-russia #trilha-alma-russa |
| A Morte de Ivan Ilitch | Liev Tolstói | #F #morte #existencialismo #classico #d1 #e1 #top #q-sentido-e-como-viver #q-morte-e-finitude #clima-melancolico #papel-leitura-relampago #cenario-russia #trilha-finitude #trilha-alma-russa |
| Os Irmãos Karamázov | Fiódor Dostoiévski | #F #religiao #etica #classico #d3 #e3 #top #q-fe-e-duvida #q-culpa-e-justica #papel-desafio #ponte-ficcao-e-filosofia #cenario-russia #trilha-alma-russa |
| O Idiota | Fiódor Dostoiévski | #F #classico #d3 #e3 #tenho-digital #cenario-russia |
| A Dama do Cachorrinho e Outros Contos | Anton Tchekhov | #F #classico #contos #d1 #e1 #cenario-russia |
| Um Dia na Vida de Ivan Deníssovitch | Alexandr Soljenítsin | #F #autoritarismo #classico #d1 #e1 #clima-cru-e-chocante #papel-leitura-relampago #cenario-russia #trilha-alma-russa |
| O Mestre e Margarida | Mikhail Bulgákov | #F #politica #europa-leste #classico #d2 #e2 #top #q-fe-e-duvida #clima-onirico #clima-subversivo #ponte-ficcao-e-filosofia #cenario-russia #trilha-alma-russa |
| Madame Bovary | Gustave Flaubert | #F #classico #d2 #e2 |
| Os Miseráveis | Victor Hugo | #F #classico #d2 #e3 |
| Em Busca do Tempo Perdido | Marcel Proust | #F #memoria #classico #d3 #e3 #q-memoria-e-esquecimento #papel-desafio |
| O Estrangeiro | Albert Camus | #F #existencialismo #classico #d1 #e1 #top #tenho-digital #q-culpa-e-justica #papel-leitura-relampago #ponte-ficcao-e-filosofia #trilha-relampago |
| A Queda | Albert Camus | #F #existencialismo #etica #classico #d2 #e1 #q-culpa-e-justica #papel-leitura-relampago #ponte-ficcao-e-filosofia |
| A Náusea | Jean-Paul Sartre | #F #existencialismo #classico #d2 #e2 #top #clima-claustrofobico #ponte-ficcao-e-filosofia |
| A Metamorfose | Franz Kafka | #F #existencialismo #classico #d2 #e1 #lido #clima-claustrofobico #papel-leitura-relampago #trilha-relampago |
| O Processo | Franz Kafka | #F #existencialismo #politica #classico #d2 #e2 #tenho-digital #q-liberdade-e-obediencia #q-culpa-e-justica #clima-claustrofobico |
| A Montanha Mágica | Thomas Mann | #F #classico #d3 #e3 #papel-desafio |
| Sidarta | Hermann Hesse | #F #espiritualidade #classico #d1 #e1 #q-sentido-e-como-viver #clima-contemplativo #papel-leitura-relampago #trilha-relampago |
| O Lobo da Estepe | Hermann Hesse | #F #existencialismo #psicologia #classico #d2 #e2 #q-identidade-e-eu |
| A Insustentável Leveza do Ser | Milan Kundera | #F #existencialismo #d2 #e2 #tenho-digital #q-sentido-e-como-viver |
| Ensaio sobre a Cegueira | José Saramago | #F #distopia #etica #d2 #e2 #top #q-liberdade-e-obediencia #clima-claustrofobico #ponte-literatura-e-neurociencia #trilha-distopias |
| O Homem Duplicado | José Saramago | #F #identidade #d1 #e2 #q-identidade-e-eu |
| O Perfume | Patrick Süskind | #F #romance-historico #d1 #e2 |
| Lolita | Vladimir Nabokov | #F #classico #d2 #e2 #clima-cru-e-chocante #clima-subversivo |
| Laranja Mecânica | Anthony Burgess | #F #distopia #classico #d2 #e1 #q-liberdade-e-obediencia #clima-cru-e-chocante #clima-subversivo #papel-leitura-relampago |
| Moby Dick | Herman Melville | #F #classico #d3 #e3 #papel-desafio |
| Coração das Trevas | Joseph Conrad | #F #colonialismo #classico #d2 #e1 #q-poder-e-violencia #q-alteridade-e-contato #clima-claustrofobico #ponte-ecologia-e-colonialismo #trilha-alteridade |
| O Morro dos Ventos Uivantes | Emily Brontë | #F #gotico #classico #d2 #e2 |
| Orgulho e Preconceito | Jane Austen | #F #classico #d1 #e2 |
| O Retrato de Dorian Gray | Oscar Wilde | #F #gotico #classico #d1 #e1 #papel-leitura-relampago |
| O Grande Gatsby | F. Scott Fitzgerald | #F #classico #d1 #e1 #papel-leitura-relampago |
| As Vinhas da Ira | John Steinbeck | #F #classico #d2 #e3 |
| O Sol é para Todos | Harper Lee | #F #raca #classico #d1 #e2 |
| O Apanhador no Campo de Centeio | J.D. Salinger | #F #classico #d1 #e1 |
| Pastoral Americana | Philip Roth | #F #contemporaneo #d2 #e2 |
| Amada | Toni Morrison | #F #raca #memoria #d3 #e2 #q-memoria-e-esquecimento #clima-cru-e-chocante #ponte-corpo-e-poder #trilha-corpo-genero-poder |
| Os Vestígios do Dia | Kazuo Ishiguro | #F #memoria #d1 #e2 #tenho-digital #q-sentido-e-como-viver #clima-melancolico |
| O Desconsolado | Kazuo Ishiguro | #F #memoria #d3 #e3 #tenho-digital #q-memoria-e-esquecimento |
| Stoner | John Williams | #F #d1 #e2 #q-sentido-e-como-viver #clima-melancolico |
| As Ondas | Virginia Woolf | #F #classico #d3 #e2 |
| A Elegância do Ouriço | Muriel Barbery | #F #d1 #e2 |
| A Biblioteca da Meia-Noite | Matt Haig | #F #fantasia #d1 #e2 #q-sentido-e-como-viver |
| O Grande Divórcio | C.S. Lewis | #F #religiao #classico #d1 #e1 #q-fe-e-duvida |
| A Redoma de Vidro | Sylvia Plath | #F #psicologia #genero #classico #d2 #e2 #q-identidade-e-eu #clima-claustrofobico |
| As Intermitências da Morte | José Saramago | #F #portugal #morte #humor #d2 #e1 #q-morte-e-finitude #clima-comico #trilha-cuidar-ate-o-fim |

---

## 4. América Latina, Brasil e lusofonia (ficção)

| Título | Autor | Tags |
|---|---|---|
| O Amor nos Tempos do Cólera | Gabriel García Márquez | #F #latam #d2 #e2 #tenho-digital |
| Crônica de uma Morte Anunciada | Gabriel García Márquez | #F #latam #d1 #e1 #tenho-digital #papel-leitura-relampago #cenario-cidade-pequena #trilha-realismo-magico #trilha-relampago |
| Pedro Páramo | Juan Rulfo | #F #latam #morte #d2 #e1 #top #q-morte-e-finitude #clima-onirico #papel-leitura-relampago #cenario-cidade-pequena #trilha-finitude #trilha-realismo-magico |
| A Casa dos Espíritos | Isabel Allende | #F #latam #d1 #e2 #clima-onirico #trilha-realismo-magico |
| A Festa do Bode | Mario Vargas Llosa | #F #latam #autoritarismo #romance-historico #d2 #e2 #q-poder-e-violencia #ponte-historia-e-ficcao |
| A Cidade e os Cachorros | Mario Vargas Llosa | #F #latam #d2 #e2 |
| Os Detetives Selvagens | Roberto Bolaño | #F #latam #d3 #e3 #tenho-digital #papel-desafio |
| O Jogo da Amarelinha | Julio Cortázar | #F #latam #d3 #e3 #papel-desafio #trilha-realismo-magico |
| O Aleph | Jorge Luis Borges | #F #latam #filosofia #classico #contos #d2 #e1 #tenho-digital #q-realidade-e-percepcao #clima-onirico #trilha-realismo-magico #trilha-labirintos-de-borges |
| Ficções | Jorge Luis Borges | #F #latam #filosofia #classico #contos #d2 #e1 #tenho-digital #q-realidade-e-percepcao #clima-onirico #clima-cerebral #ponte-ficcao-e-filosofia #trilha-labirintos-de-borges |
| O Túnel | Ernesto Sabato | #F #latam #psicologia #classico #d1 #e1 #clima-claustrofobico #papel-leitura-relampago |
| Grande Sertão: Veredas | João Guimarães Rosa | #F #BR #classico #d3 #e3 #top #clima-onirico #papel-desafio #cenario-sertao-e-nordeste #trilha-realismo-magico |
| Vidas Secas | Graciliano Ramos | #F #BR #classico #d1 #e1 #q-poder-e-violencia #papel-leitura-relampago #cenario-sertao-e-nordeste |
| A Paixão Segundo G.H. | Clarice Lispector | #F #BR #existencialismo #d3 #e1 #top #q-identidade-e-eu #ponte-literatura-e-neurociencia |
| Memórias Póstumas de Brás Cubas | Machado de Assis | #F #BR #classico #d2 #e1 #tenho-digital #clima-subversivo #clima-comico #papel-leitura-relampago |
| Dom Casmurro | Machado de Assis | #F #BR #classico #d1 #e1 #papel-leitura-relampago |
| O Cortiço | Aluísio Azevedo | #F #BR #classico #d1 #e1 |
| Macunaíma | Mário de Andrade | #F #BR #classico #d2 #e1 #clima-onirico #clima-subversivo |
| Capitães da Areia | Jorge Amado | #F #BR #classico #d1 #e2 #cenario-sertao-e-nordeste |
| Cidade de Deus | Paulo Lins | #F #BR #contemporaneo #d2 #e3 #q-poder-e-violencia #clima-cru-e-chocante |
| Dois Irmãos | Milton Hatoum | #F #BR #d1 #e1 |
| Torto Arado | Itamar Vieira Junior | #F #BR #raca #contemporaneo #d1 #e2 #tenho-digital #clima-emocionante #ponte-ecologia-e-colonialismo #cenario-sertao-e-nordeste #trilha-brasil-profundo |
| O Avesso da Pele | Jeferson Tenório | #F #BR #raca #contemporaneo #d1 #e1 #tenho-digital #clima-emocionante #trilha-porto-alegre-hoje |
| Lavoura Arcaica | Raduan Nassar | #F #BR #d3 #e1 #q-poder-e-violencia #clima-claustrofobico |
| A Grande Arte | Rubem Fonseca | #F #BR #misterio #d1 #e2 #trilha-crime-a-brasileira |
| Nove Noites | Bernardo Carvalho | #F #BR #misterio #antropologia #d2 #e2 #q-alteridade-e-contato |
| Incidente em Antares | Erico Veríssimo | #F #BR #RS #regional-gaucho #politica #d2 #e3 #cenario-cidade-pequena #trilha-saga-gaucha |
| Contos Gauchescos | Simões Lopes Neto | #F #BR #RS #regional-gaucho #classico #contos #d2 #e1 #trilha-saga-gaucha |
| Os Ratos | Dyonelio Machado | #F #BR #RS #classico #d1 #e1 #papel-leitura-relampago #trilha-saga-gaucha |
| O Centauro no Jardim | Moacyr Scliar | #F #BR #RS #d2 #e2 #trilha-saga-gaucha |
| Netto Perde Sua Alma | Tabajara Ruas | #F #BR #RS #romance-historico #d2 #e1 #ponte-historia-e-ficcao #trilha-saga-gaucha |
| Viva o Povo Brasileiro | João Ubaldo Ribeiro | #F #BR #romance-historico #d3 #e3 #ponte-historia-e-ficcao |
| Um Defeito de Cor | Ana Maria Gonçalves | #F #BR #romance-historico #raca #d2 #e3 #clima-emocionante #ponte-historia-e-ficcao #trilha-brasil-profundo |
| Boca do Inferno | Ana Miranda | #F #BR #romance-historico #d2 #e2 |
| Livro do Desassossego | Fernando Pessoa | #F #portugal #existencialismo #d3 #e3 #q-identidade-e-eu #clima-melancolico |
| Memorial do Convento | José Saramago | #F #portugal #romance-historico #d3 #e2 #ponte-historia-e-ficcao |
| O Vendedor de Passados | José Eduardo Agualusa | #F #africa #portugal #identidade #d1 #e1 #q-identidade-e-eu #q-memoria-e-esquecimento |
| Coração sem Medo | Itamar Vieira Junior | #F #BR #raca #contemporaneo #d1 #e2 #q-poder-e-violencia #clima-emocionante |
| Meridiana | Eliana Alves Cruz | #F #BR #raca #contemporaneo #d1 #e1 #q-identidade-e-eu |
| O Som do Rugido da Onça | Micheliny Verunschk | #F #BR #romance-historico #colonialismo #d2 #e1 #q-alteridade-e-contato #ponte-historia-e-ficcao |
| Os Supridores | José Falero | #F #BR #RS #humor #contemporaneo #d1 #e2 #clima-subversivo #trilha-porto-alegre-hoje |
| Marrom e Amarelo | Paulo Scott | #F #BR #RS #raca #contemporaneo #d2 #e1 #q-identidade-e-eu #trilha-porto-alegre-hoje |
| Barba Ensopada de Sangue | Daniel Galera | #F #BR #RS #contemporaneo #d2 #e2 #q-identidade-e-eu #clima-melancolico #trilha-porto-alegre-hoje |
| A Guerra do Fim do Mundo | Mario Vargas Llosa | #F #latam #romance-historico #guerra #religiao #d2 #e3 #q-fe-e-duvida #ponte-historia-e-ficcao #cenario-sertao-e-nordeste |
| O Filho de Mil Homens | Valter Hugo Mãe | #F #portugal #parentalidade #contemporaneo #d1 #e1 #clima-emocionante #trilha-pai-em-construcao |

---

## 5. Ficção contemporânea e mundial

| Título | Autor | Tags |
|---|---|---|
| A Vegetariana | Han Kang | #F #asia #d1 #e1 #top #tenho-digital #q-identidade-e-eu #clima-cru-e-chocante #papel-leitura-relampago #ponte-corpo-e-poder #trilha-corpo-genero-poder #trilha-relampago |
| Crônica do Pássaro de Corda | Haruki Murakami | #F #asia #d2 #e3 #tenho-digital #q-realidade-e-percepcao #clima-onirico |
| Atlas de Nuvens | David Mitchell | #F #ficcao-cientifica #d2 #e3 #q-identidade-e-eu |
| A Amiga Genial (tetralogia) | Elena Ferrante | #F #d1 #e3 |
| A Vida Mentirosa dos Adultos | Elena Ferrante | #F #d1 #e2 |
| Americanah | Chimamanda Ngozi Adichie | #F #africa #raca #d1 #e3 #q-identidade-e-eu #clima-emocionante |
| Meio Sol Amarelo | Chimamanda Ngozi Adichie | #F #africa #romance-historico #guerra #d2 #e3 #clima-emocionante #ponte-historia-e-ficcao |
| O Mundo se Despedaça | Chinua Achebe | #F #africa #colonialismo #classico #d1 #e1 #q-alteridade-e-contato #ponte-ecologia-e-colonialismo #trilha-alteridade |
| Vida e Época de Michael K. | J.M. Coetzee | #F #africa #autoritarismo #d2 #e1 #clima-cru-e-chocante |
| Desonra | J.M. Coetzee | #F #africa #d2 #e1 #q-culpa-e-justica #clima-cru-e-chocante |
| Homem Invisível | Ralph Ellison | #F #raca #classico #d2 #e3 #q-identidade-e-eu |
| O Vendido | Paul Beatty | #F #raca #humor #d3 #e2 #clima-subversivo #clima-comico |
| Maus | Art Spiegelman | #HQ #guerra #testemunho #d1 #e2 #tenho-digital #papel-leitura-relampago #cenario-guerra-mundial #trilha-quadrinhos-para-gente-grande |
| A Cidade das Damas | Christine de Pizan | #F #genero #medieval #classico #d2 #e2 #clima-subversivo #ponte-corpo-e-poder #trilha-corpo-genero-poder |
| Os Anéis de Saturno | W.G. Sebald | #F #memoria #historia #d3 #e2 #q-memoria-e-esquecimento #clima-melancolico |
| Um Equilíbrio Delicado | Rohinton Mistry | #F #asia #autoritarismo #d2 #e3 |
| O Deus das Pequenas Coisas | Arundhati Roy | #F #asia #d2 #e2 |
| Pachinko | Min Jin Lee | #F #asia #romance-historico #d1 #e3 #tenho-digital #clima-emocionante #ponte-historia-e-ficcao |
| O Leopardo | Giuseppe Tomasi di Lampedusa | #F #romance-historico #classico #d2 #e2 #tenho-digital #q-poder-e-violencia #clima-melancolico #ponte-historia-e-ficcao |
| A Conspiração contra a América | Philip Roth | #F #historia-alternativa #autoritarismo #d2 #e2 #cenario-guerra-mundial |
| Sobre os Ossos dos Mortos | Olga Tokarczuk | #F #misterio #ecologia #d2 #e2 #tenho-digital #cenario-cidade-pequena |
| O Testamento de Maria | Colm Tóibín | #F #religiao #d1 #e1 #q-fe-e-duvida |
| O Livro da Forma e do Vazio | Ruth Ozeki | #F #d2 #e3 #clima-melancolico |
| Gilead | Marilynne Robinson | #F #religiao #d2 #e2 #q-fe-e-duvida #clima-melancolico |
| O Gigante Enterrado | Kazuo Ishiguro | #F #fantasia #memoria #d2 #e2 #tenho-digital #q-memoria-e-esquecimento #clima-melancolico |
| Os Anos | Annie Ernaux | #F #memoria #d2 #e1 #q-identidade-e-eu #q-memoria-e-esquecimento #clima-melancolico |
| Se um Viajante numa Noite de Inverno | Italo Calvino | #F #d3 #e2 #q-realidade-e-percepcao #clima-cerebral |
| Fogo Pálido | Vladimir Nabokov | #F #d3 #e2 #q-realidade-e-percepcao #clima-cerebral |
| Ruído Branco | Don DeLillo | #F #d2 #e2 |
| O Assassino Cego | Margaret Atwood | #F #d2 #e3 #q-memoria-e-esquecimento |
| O Deserto dos Tártaros | Dino Buzzati | #F #classico #d2 #e2 #q-morte-e-finitude #clima-melancolico |
| The Memory of Animals | Claire Fuller | #F #sem-pt #d1 #e2 #q-memoria-e-esquecimento |
| Orbital | Samantha Harvey | #F #contemporaneo #d2 #e1 #q-natureza-e-civilizacao #clima-contemplativo #papel-leitura-relampago #cenario-espaco-profundo |
| Sátántangó | László Krasznahorkai | #F #europa-leste #d3 #e1 #clima-claustrofobico #papel-desafio |
| Lincoln no Limbo | George Saunders | #F #romance-historico #morte #d3 #e2 #q-morte-e-finitude #clima-onirico #ponte-historia-e-ficcao |

---

## 6. Romances históricos

| Título | Autor | Tags |
|---|---|---|
| O Arqueiro (Busca do Graal, vol. 1) | Bernard Cornwell | #F #romance-historico #medieval #guerra #d1 #e2 #lido #top #rel-cornwell #clima-aventura #trilha-aco-e-fe |
| O Físico | Noah Gordon | #F #romance-historico #medieval #medicina #d1 #e3 #lido #top #rel-cornwell #trilha-bisturi-e-fe |
| Os Pilares da Terra | Ken Follett | #F #romance-historico #medieval #d1 #e3 #top #rel-cornwell #tenho-digital #clima-aventura #papel-porta-de-entrada #trilha-aco-e-fe |
| Mundo sem Fim | Ken Follett | #F #romance-historico #medieval #medicina #d1 #e3 #rel-cornwell #tenho-digital #trilha-bisturi-e-fe |
| A Coluna de Fogo | Ken Follett | #F #romance-historico #religiao #d1 #e3 #rel-cornwell #tenho-digital |
| Crônicas Saxônicas (começa em O Último Reino) | Bernard Cornwell | #F #romance-historico #medieval #guerra #d1 #e3 #rel-cornwell #tenho-digital #clima-aventura #trilha-aco-e-fe |
| Crônicas de Artur, vols. 2 e 3 (O Inimigo de Deus · Excalibur) | Bernard Cornwell | #F #romance-historico #medieval #guerra #d1 #e3 #rel-cornwell #tenho-digital |
| Azincourt | Bernard Cornwell | #F #romance-historico #medieval #guerra #d1 #e2 #rel-cornwell #tenho-digital #clima-aventura #trilha-aco-e-fe |
| Série Sharpe | Bernard Cornwell | #F #romance-historico #guerra #d1 #e3 #rel-cornwell #tenho-digital #clima-aventura #trilha-aco-e-fe |
| O Último Judeu | Noah Gordon | #F #romance-historico #medieval #religiao #d1 #e2 #rel-cornwell #trilha-bisturi-e-fe |
| A Escolha da Dra. Cole | Noah Gordon | #F #medicina #d1 #e2 #rel-cornwell #tenho-digital |
| O Nome da Rosa | Umberto Eco | #F #romance-historico #medieval #misterio #filosofia #d3 #e3 #top #q-fe-e-duvida #clima-cerebral #papel-ponte #ponte-ciencia-e-fe |
| Baudolino | Umberto Eco | #F #romance-historico #medieval #d3 #e3 #clima-cerebral |
| O Rei de Ferro (Os Reis Malditos) | Maurice Druon | #F #romance-historico #medieval #d2 #e3 |
| The Sunne in Splendour | Sharon Kay Penman | #F #romance-historico #medieval #sem-pt #d2 #e3 |
| The Greatest Knight | Elizabeth Chadwick | #F #romance-historico #medieval #sem-pt #d1 #e3 |
| A Catedral do Mar | Ildefonso Falcones | #F #romance-historico #medieval #d1 #e3 |
| The Lymond Chronicles (série) | Dorothy Dunnett | #F #romance-historico #renascimento #sem-pt #d2 #e3 |
| Wolf Hall | Hilary Mantel | #F #romance-historico #renascimento #politica #d3 #e3 #q-poder-e-violencia #ponte-historia-e-ficcao |
| Eu, Cláudio | Robert Graves | #F #romance-historico #roma #classico #antiguidade #d2 #e2 #ponte-historia-e-ficcao #trilha-roma-por-dentro |
| Memórias de Adriano | Marguerite Yourcenar | #F #romance-historico #roma #classico #antiguidade #d3 #e2 #ponte-historia-e-ficcao #trilha-roma-por-dentro |
| Imperium | Robert Harris | #F #romance-historico #roma #politica #antiguidade #d1 #e2 #trilha-roma-por-dentro |
| Pompeia | Robert Harris | #F #romance-historico #roma #antiguidade #d1 #e2 |
| Os Portões de Roma (série Imperador) | Conn Iggulden | #F #romance-historico #roma #antiguidade #d1 #e2 #tenho-digital |
| O Lobo das Planícies (série Gêngis Khan) | Conn Iggulden | #F #romance-historico #asia #guerra #d1 #e2 #tenho-digital #cenario-oriente-feudal |
| O Primeiro Homem de Roma | Colleen McCullough | #F #romance-historico #roma #politica #antiguidade #d2 #e3 |
| Portões de Fogo | Steven Pressfield | #F #romance-historico #antiguidade #guerra #d2 #e2 #clima-aventura |
| O Menino Persa | Mary Renault | #F #romance-historico #antiguidade #d2 #e2 |
| Sob a Águia (Under the Eagle) | Simon Scarrow | #F #romance-historico #roma #guerra #antiguidade #d1 #e2 |
| Série Falco | Lindsey Davis | #F #romance-historico #roma #misterio #antiguidade #d1 #e3 |
| O Egípcio (Sinuhe) | Mika Waltari | #F #romance-historico #antiguidade #medicina #d2 #e3 #trilha-bisturi-e-fe |
| O Médico de Córdoba | Herbert Le Porrier | #F #romance-historico #medieval #medicina #verificar #d2 #e2 #cenario-oriente-feudal #trilha-bisturi-e-fe |
| O Viajante | Gary Jennings | #F #romance-historico #medieval #asia #d1 #e3 #clima-aventura #cenario-oriente-feudal |
| Shōgun | James Clavell | #F #romance-historico #asia #d2 #e3 #q-alteridade-e-contato #clima-aventura #cenario-oriente-feudal |
| Musashi | Eiji Yoshikawa | #F #romance-historico #asia #d2 #e3 #clima-aventura #cenario-oriente-feudal |
| Agonia e Êxtase | Irving Stone | #F #romance-historico #renascimento #arte #d1 #e3 |
| Os Três Mosqueteiros | Alexandre Dumas | #F #romance-historico #classico #aventura #d1 #e3 #clima-aventura |
| O Conde de Monte Cristo | Alexandre Dumas | #F #romance-historico #classico #aventura #d1 #e3 #clima-aventura |
| O Corcunda de Notre-Dame | Victor Hugo | #F #romance-historico #medieval #classico #d2 #e3 |
| Leão, o Africano | Amin Maalouf | #F #romance-historico #renascimento #africa #d2 #e2 #q-alteridade-e-contato #cenario-oriente-feudal |
| Meu Nome é Vermelho | Orhan Pamuk | #F #romance-historico #arte #d3 #e3 #cenario-oriente-feudal |
| O Capitão Alatriste | Arturo Pérez-Reverte | #F #romance-historico #aventura #d1 #e2 #clima-aventura |
| Mestre dos Mares | Patrick O'Brian | #F #romance-historico #guerra #aventura #d2 #e2 #clima-aventura |
| Kristin Lavransdatter | Sigrid Undset | #F #romance-historico #medieval #classico #d2 #e3 |
| A Menina que Roubava Livros | Markus Zusak | #F #guerra #d1 #e2 #clima-emocionante #cenario-guerra-mundial |
| Toda Luz que Não Podemos Ver | Anthony Doerr | #F #guerra #d1 #e3 #clima-emocionante #cenario-guerra-mundial |
| Suíte Francesa | Irène Némirovsky | #F #guerra #d2 #e2 #ponte-historia-e-ficcao #cenario-guerra-mundial |
| A Papisa Joana | Donna Woolfolk Cross | #F #romance-historico #medieval #religiao #medicina #genero #d1 #e2 #rel-cornwell #clima-aventura #ponte-historia-e-ficcao |
| O Crepúsculo e a Aurora | Ken Follett | #F #romance-historico #medieval #d1 #e3 #rel-cornwell #clima-aventura |
| Samarcanda | Amin Maalouf | #F #romance-historico #medieval #asia #d2 #e2 #ponte-historia-e-ficcao #cenario-oriente-feudal |

---

## 7. Horror, weird fiction e mistério

| Título | Autor | Tags |
|---|---|---|
| O Rei de Amarelo | Robert W. Chambers | #F #horror #lovecraftiano #classico #contos #d2 #e1 #top #rel-widows-bay #tenho-digital #trilha-lovecraft-widows-bay |
| O Grande Deus Pã | Arthur Machen | #F #horror #classico #d2 #e1 #rel-widows-bay |
| Os Salgueiros | Algernon Blackwood | #F #horror #classico #d2 #e1 #rel-widows-bay #trilha-lovecraft-widows-bay |
| O Wendigo | Algernon Blackwood | #F #horror #classico #d1 #e1 #rel-widows-bay |
| A Casa no Limite do Mundo | William Hope Hodgson | #F #horror #classico #d2 #e1 #rel-widows-bay #clima-claustrofobico #cenario-ilha-e-isolamento |
| A Terra da Noite | William Hope Hodgson | #F #horror #ficcao-cientifica #classico #d3 #e3 #rel-widows-bay #papel-desafio |
| Nas Montanhas da Loucura | H.P. Lovecraft | #F #horror #lovecraftiano #classico #d2 #e1 #top #tenho-fisico #rel-widows-bay |
| A Sombra sobre Innsmouth | H.P. Lovecraft | #F #horror #lovecraftiano #classico #d2 #e1 #top #tenho-fisico #rel-widows-bay #clima-claustrofobico #papel-porta-de-entrada #cenario-nova-inglaterra #cenario-cidade-pequena #trilha-lovecraft-widows-bay |
| O Chamado de Cthulhu | H.P. Lovecraft | #F #horror #lovecraftiano #classico #d2 #e1 #top #tenho-fisico #rel-widows-bay #tenho-digital |
| O Horror de Dunwich | H.P. Lovecraft | #F #horror #lovecraftiano #classico #d2 #e1 #rel-widows-bay #cenario-nova-inglaterra #cenario-cidade-pequena #trilha-lovecraft-widows-bay |
| O Caso de Charles Dexter Ward | H.P. Lovecraft | #F #horror #lovecraftiano #classico #d2 #e1 #rel-widows-bay #tenho-digital #cenario-nova-inglaterra |
| Um Sussurro nas Trevas | H.P. Lovecraft | #F #horror #lovecraftiano #classico #d2 #e1 #rel-widows-bay #cenario-nova-inglaterra |
| O Pescador | John Langan | #F #horror #lovecraftiano #d2 #e2 #top #rel-widows-bay #tenho-digital #trilha-lovecraft-widows-bay |
| A Balada de Black Tom | Victor LaValle | #F #horror #lovecraftiano #raca #d1 #e1 #rel-widows-bay |
| Território Lovecraft | Matt Ruff | #F #horror #lovecraftiano #raca #d2 #e2 #rel-widows-bay #trilha-lovecraft-widows-bay |
| Providence | Alan Moore | #HQ #horror #lovecraftiano #d3 #e3 #rel-widows-bay #cenario-nova-inglaterra |
| Gótico Mexicano | Silvia Moreno-Garcia | #F #horror #gotico #d1 #e2 #rel-widows-bay |
| Aniquilação (trilogia: Aniquilação · Autoridade · Aceitação) | Jeff VanderMeer | #F #horror #ficcao-cientifica #ecologia #d2 #e3 #rel-widows-bay #tenho-digital #q-alteridade-e-contato #ponte-ecologia-e-colonialismo #cenario-ilha-e-isolamento |
| The Croning | Laird Barron | #F #horror #lovecraftiano #sem-pt #d3 #e2 #rel-widows-bay |
| Canções de um Sonhador Morto & Escriba-Sinistro | Thomas Ligotti | #F #horror #contos #d3 #e2 #rel-widows-bay |
| Teatro Grottesco | Thomas Ligotti | #F #horror #sem-pt #contos #d3 #e2 #rel-widows-bay |
| Winter Tide | Ruthanna Emrys | #F #horror #lovecraftiano #sem-pt #d2 #e2 #rel-widows-bay #cenario-nova-inglaterra |
| The Night Ocean | Paul La Farge | #F #horror #lovecraftiano #sem-pt #d2 #e3 #rel-widows-bay |
| Trocas Macabras | Stephen King | #F #horror #d1 #e3 #rel-widows-bay #cenario-nova-inglaterra #cenario-cidade-pequena #trilha-lovecraft-widows-bay |
| A Hora do Vampiro | Stephen King | #F #horror #d1 #e3 #rel-widows-bay #cenario-nova-inglaterra #cenario-cidade-pequena #trilha-lovecraft-widows-bay |
| A Névoa | Stephen King | #F #horror #lovecraftiano #d1 #e1 #rel-widows-bay #cenario-nova-inglaterra #cenario-cidade-pequena |
| Revival | Stephen King | #F #horror #lovecraftiano #d1 #e2 #rel-widows-bay #cenario-nova-inglaterra |
| O Iluminado | Stephen King | #F #horror #d1 #e3 #clima-claustrofobico |
| O Outsider | Stephen King | #F #horror #misterio #d1 #e3 #rel-widows-bay #cenario-cidade-pequena |
| Ghost Story | Peter Straub | #F #horror #d2 #e3 #rel-widows-bay #cenario-cidade-pequena |
| Elementais | Michael McDowell | #F #horror #d1 #e2 #rel-widows-bay #cenario-cidade-pequena |
| The Fog | James Herbert | #F #horror #sem-pt #d1 #e2 #rel-widows-bay |
| The Hollow Places | T. Kingfisher | #F #horror #humor #sem-pt #d1 #e2 #rel-widows-bay #clima-comico #trilha-lovecraft-widows-bay |
| The Twisted Ones | T. Kingfisher | #F #horror #humor #sem-pt #d1 #e2 #rel-widows-bay #clima-comico |
| The Ceremonies | T.E.D. Klein | #F #horror #sem-pt #d3 #e3 #rel-widows-bay |
| O Terror | Dan Simmons | #F #horror #romance-historico #d2 #e3 #rel-widows-bay #clima-claustrofobico #ponte-historia-e-ficcao #cenario-ilha-e-isolamento |
| A Assombração da Casa da Colina | Shirley Jackson | #F #horror #gotico #classico #d2 #e1 #rel-widows-bay |
| Drácula | Bram Stoker | #F #horror #gotico #classico #d2 #e3 |
| O Médico e o Monstro | Robert Louis Stevenson | #F #gotico #classico #d1 #e1 |
| The Weird: A Compendium of Strange and Dark Stories | Ann e Jeff VanderMeer (orgs.) | #antologia #horror #sem-pt #contos #d2 #e3 #rel-widows-bay |
| Children of Lovecraft | Ellen Datlow (org.) | #antologia #horror #lovecraftiano #sem-pt #contos #d2 #e2 #rel-widows-bay |
| H.P. Lovecraft: Contra o Mundo, Contra a Vida | Michel Houellebecq | #NF #biografia #lovecraftiano #d2 #e1 #rel-widows-bay #trilha-lovecraft-widows-bay |
| I Am Providence | S.T. Joshi | #NF #biografia #lovecraftiano #sem-pt #d3 #e3 #rel-widows-bay #cenario-nova-inglaterra |
| O Silêncio dos Inocentes | Thomas Harris | #F #thriller #misterio #d1 #e2 #clima-cru-e-chocante |
| O Talentoso Ripley | Patricia Highsmith | #F #misterio #d1 #e2 |
| Assassinato no Expresso do Oriente | Agatha Christie | #F #misterio #classico #d1 #e1 |
| Sempre Vivemos no Castelo | Shirley Jackson | #F #horror #gotico #classico #d1 #e1 #rel-widows-bay #clima-claustrofobico #papel-leitura-relampago #cenario-nova-inglaterra #cenario-cidade-pequena |
| A Volta do Parafuso | Henry James | #F #horror #gotico #classico #d2 #e1 #rel-widows-bay #q-realidade-e-percepcao #papel-leitura-relampago |
| O Cemitério | Stephen King | #F #horror #morte #d1 #e2 #rel-widows-bay #q-morte-e-finitude #cenario-nova-inglaterra #cenario-cidade-pequena |
| Nossa Parte de Noite | Mariana Enriquez | #F #horror #lovecraftiano #latam #d2 #e3 #rel-widows-bay #q-poder-e-violencia #clima-cru-e-chocante |
| Mandíbula | Mónica Ojeda | #F #horror #latam #d3 #e2 #rel-widows-bay #clima-cru-e-chocante |
| Distância de Resgate | Samanta Schweblin | #F #horror #ecologia #latam #d2 #e1 #clima-claustrofobico #papel-leitura-relampago |

---

## 8. Poesia e cartas

| Título | Autor | Tags |
|---|---|---|
| Morte e Vida Severina | João Cabral de Melo Neto | #poesia #BR #classico #d2 #e1 #cenario-sertao-e-nordeste |
| Antologia Poética | Carlos Drummond de Andrade | #poesia #BR #classico #d2 #e2 |
| Cartas a um Jovem Poeta | Rainer Maria Rilke | #NF #poesia #escrita #classico #d1 #e1 #clima-contemplativo #papel-leitura-relampago |

---

## 9. Filosofia, ética e existência (não ficção)

| Título | Autor | Tags |
|---|---|---|
| Apologia de Sócrates | Platão | #NF #filosofia #antiguidade #classico #d2 #e1 #tenho-digital #papel-fonte-primaria #trilha-filosofia-em-doses |
| O Banquete | Platão | #NF #filosofia #antiguidade #classico #d2 #e1 #tenho-digital |
| Ética a Nicômaco | Aristóteles | #NF #filosofia #etica #antiguidade #classico #d3 #e2 #q-sentido-e-como-viver |
| Meditações | Marco Aurélio | #NF #filosofia #etica #roma #classico #antiguidade #d1 #e1 #top #tenho-digital #q-sentido-e-como-viver #clima-contemplativo #papel-porta-de-entrada #trilha-roma-por-dentro #trilha-filosofia-em-doses |
| Cartas a Lucílio | Sêneca | #NF #filosofia #etica #roma #classico #antiguidade #d1 #e2 #q-sentido-e-como-viver #trilha-roma-por-dentro |
| Manual de Epicteto | Epicteto | #NF #filosofia #etica #roma #classico #antiguidade #d1 #e1 #q-sentido-e-como-viver #clima-contemplativo #papel-leitura-relampago |
| Ensaios | Michel de Montaigne | #NF #filosofia #classico #d2 #e3 |
| Pensamentos | Blaise Pascal | #NF #filosofia #religiao #classico #d2 #e2 #q-fe-e-duvida |
| Confissões | Santo Agostinho | #NF #filosofia #religiao #classico #d3 #e2 #q-fe-e-duvida |
| Meditações Metafísicas | René Descartes | #NF #filosofia #classico #d2 #e1 #papel-fonte-primaria |
| Ética | Baruch Spinoza | #NF #filosofia #etica #classico #d3 #e2 #papel-desafio |
| Investigação sobre o Entendimento Humano | David Hume | #NF #filosofia #classico #d2 #e2 |
| Fundamentação da Metafísica dos Costumes | Immanuel Kant | #NF #filosofia #etica #classico #d3 #e1 |
| Crítica da Razão Pura | Immanuel Kant | #NF #filosofia #classico #d3 #e3 #papel-desafio |
| Sobre a Liberdade | John Stuart Mill | #NF #filosofia #politica #classico #d2 #e1 #q-liberdade-e-obediencia |
| O Mundo como Vontade e Representação | Arthur Schopenhauer | #NF #filosofia #classico #d3 #e3 #papel-desafio |
| Temor e Tremor | Søren Kierkegaard | #NF #filosofia #religiao #classico #d3 #e1 #q-fe-e-duvida |
| Genealogia da Moral | Friedrich Nietzsche | #NF #filosofia #etica #classico #d3 #e1 #top #tenho-digital #trilha-yalom-nietzsche |
| Crepúsculo dos Ídolos | Friedrich Nietzsche | #NF #filosofia #classico #d3 #e1 #tenho-digital #trilha-filosofia-em-doses |
| O Mito de Sísifo | Albert Camus | #NF #filosofia #existencialismo #classico #d2 #e1 #top #tenho-digital #q-sentido-e-como-viver #papel-porta-de-entrada #trilha-finitude #trilha-filosofia-em-doses |
| O Existencialismo é um Humanismo | Jean-Paul Sartre | #NF #existencialismo #classico #d2 #e1 #papel-porta-de-entrada |
| Por uma Moral da Ambiguidade | Simone de Beauvoir | #NF #existencialismo #etica #classico #d2 #e1 #top #trilha-corpo-genero-poder |
| Em Busca de Sentido | Viktor Frankl | #NF #existencialismo #psicologia #testemunho #classico #psicologia-humanista #d1 #e1 #top #q-sentido-e-como-viver #clima-emocionante #papel-porta-de-entrada #cenario-guerra-mundial #trilha-finitude #trilha-relampago |
| A Coragem de Ser | Paul Tillich | #NF #existencialismo #religiao #classico #d3 #e1 #q-fe-e-duvida |
| Uma Breve Introdução à Filosofia | Thomas Nagel | #NF #filosofia #introducao #d1 #e1 #papel-porta-de-entrada |
| O Sentido da Vida: Uma Breve Introdução | Terry Eagleton | #NF #filosofia #introducao #d1 #e1 #q-sentido-e-como-viver |
| História da Filosofia Ocidental | Bertrand Russell | #NF #filosofia #introducao #classico #d2 #e3 #tenho-digital |
| Elogio do Ócio | Bertrand Russell | #NF #filosofia #classico #d1 #e1 #q-sentido-e-como-viver #papel-leitura-relampago |
| Walden | Henry David Thoreau | #NF #filosofia #ecologia #classico #d2 #e2 #tenho-digital #q-sentido-e-como-viver #q-natureza-e-civilizacao #clima-contemplativo |
| Cristianismo Puro e Simples | C.S. Lewis | #NF #religiao #filosofia #classico #d1 #e1 #q-fe-e-duvida |
| Uma Teoria da Justiça | John Rawls | #NF #filosofia #politica #etica #d3 #e3 #q-culpa-e-justica |
| Justiça: O que é Fazer a Coisa Certa | Michael Sandel | #NF #filosofia #etica #d1 #e2 #q-culpa-e-justica #papel-porta-de-entrada |
| Reasons and Persons | Derek Parfit | #NF #filosofia #etica #identidade #sem-pt #d3 #e3 #q-identidade-e-eu #papel-desafio |
| A Soberania do Bem | Iris Murdoch | #NF #filosofia #etica #d2 #e1 |
| Upheavals of Thought | Martha C. Nussbaum | #NF #filosofia #etica #sem-pt #d3 #e3 |
| Creating Capabilities | Martha C. Nussbaum | #NF #filosofia #etica #politica #sem-pt #d2 #e1 |
| A Ideia de Justiça | Amartya Sen | #NF #filosofia #politica #economia #d3 #e3 #q-culpa-e-justica |
| Ética Prática | Peter Singer | #NF #filosofia #etica #d1 #e2 #papel-porta-de-entrada |
| The Limits of Morality | Shelly Kagan | #NF #filosofia #etica #sem-pt #d3 #e3 |
| A Paisagem Moral | Sam Harris | #NF #filosofia #etica #ciencia #d2 #e2 #tenho-digital #papel-contraponto |
| The Sources of Normativity | Christine Korsgaard | #NF #filosofia #etica #sem-pt #d3 #e2 |
| The Ethics of Identity | Kwame Anthony Appiah | #NF #filosofia #identidade #sem-pt #d2 #e2 #q-identidade-e-eu |
| As Fontes do Self | Charles Taylor | #NF #filosofia #identidade #historia #d3 #e3 #q-identidade-e-eu |
| The Myth of the Framework | Karl Popper | #NF #filosofia #ciencia #sem-pt #d3 #e2 |
| As Palavras e as Coisas | Michel Foucault | #NF #filosofia #historia #classico #d3 #e3 #papel-desafio |

---

## 10. Mente, consciência e neurociência

| Título | Autor | Tags |
|---|---|---|
| O Erro de Descartes | António Damásio | #NF #neurociencia #consciencia #d2 #e2 #tenho-digital #papel-ponte #ponte-literatura-e-neurociencia #trilha-mente-e-cerebro |
| A Consciência Explicada | Daniel C. Dennett | #NF #consciencia #filosofia #d3 #e3 #trilha-mente-e-cerebro |
| O Eu e Seu Cérebro | Karl Popper e John Eccles | #NF #consciencia #neurociencia #classico #d3 #e3 |
| The Conscious Mind | David J. Chalmers | #NF #consciencia #filosofia #sem-pt #d3 #e3 #papel-desafio |
| Reality+ | David J. Chalmers | #NF #consciencia #filosofia #ia #tecnologia #d2 #e3 #q-realidade-e-percepcao |
| The Mind's I | Douglas Hofstadter e Daniel Dennett | #NF #consciencia #ia #sem-pt #tecnologia #d2 #e2 |
| Gödel, Escher, Bach | Douglas Hofstadter | #NF #consciencia #ciencia #linguagem #matematica #d3 #e3 #q-realidade-e-percepcao #clima-cerebral #papel-desafio #papel-ponte #trilha-mente-e-cerebro |
| Being You | Anil Seth | #NF #consciencia #neurociencia #sem-pt #d2 #e2 #q-identidade-e-eu #q-realidade-e-percepcao #trilha-mente-e-cerebro |
| O Túnel do Ego | Thomas Metzinger | #NF #consciencia #filosofia #d3 #e2 #q-identidade-e-eu #trilha-mente-e-cerebro |
| Surfing Uncertainty | Andy Clark | #NF #neurociencia #consciencia #sem-pt #d3 #e3 |
| The Extended Mind | Annie Murphy Paul | #NF #neurociencia #psicologia #sem-pt #d1 #e2 |
| The Philosophical Baby | Alison Gopnik | #NF #psicologia #consciencia #sem-pt #d1 #e2 |
| Artificial You | Susan Schneider | #NF #consciencia #ia #sem-pt #tecnologia #d2 #e2 #q-identidade-e-eu |
| The Case Against Reality | Donald Hoffman | #NF #consciencia #ciencia #sem-pt #d2 #e2 #q-realidade-e-percepcao |
| The Master and His Emissary | Iain McGilchrist | #NF #neurociencia #historia #sem-pt #d3 #e3 #ponte-literatura-e-neurociencia |
| O Cérebro Ético | Michael S. Gazzaniga | #NF #neurociencia #etica #d2 #e2 |
| Incógnito: As Vidas Secretas do Cérebro | David Eagleman | #NF #neurociencia #d1 #e2 #ponte-literatura-e-neurociencia #trilha-mente-e-cerebro |
| O Homem que Confundiu sua Mulher com um Chapéu | Oliver Sacks | #NF #neurociencia #psicologia #d1 #e2 #q-identidade-e-eu #papel-ponte #ponte-literatura-e-neurociencia #trilha-mente-e-cerebro |
| Comporte-se: A Biologia Humana em Nosso Melhor e Pior | Robert Sapolsky | #NF #neurociencia #psicologia #ciencia #biologia #d3 #e3 #top #ponte-literatura-e-neurociencia #trilha-mente-e-cerebro |
| Determinados | Robert M. Sapolsky | #NF #neurociencia #filosofia #etica #ciencia #d3 #e3 #q-culpa-e-justica #q-liberdade-e-obediencia #papel-contraponto |
| Um Antropólogo em Marte | Oliver Sacks | #NF #neurociencia #psicologia #d1 #e2 #q-identidade-e-eu #ponte-literatura-e-neurociencia |
| Como Mudar Sua Mente | Michael Pollan | #NF #consciencia #neurociencia #psiquiatria #mistica #d1 #e2 #q-realidade-e-percepcao #ponte-ciencia-e-fe |

---

## 11. Política, poder, autoritarismo e economia

| Título | Autor | Tags |
|---|---|---|
| Origens do Totalitarismo | Hannah Arendt | #NF #politica #autoritarismo #classico #d3 #e3 #top #rel-fromm #tenho-digital #q-liberdade-e-obediencia #papel-desafio #cenario-guerra-mundial #trilha-liberdade-e-autoritarismo |
| A Condição Humana | Hannah Arendt | #NF #filosofia #politica #classico #d3 #e2 #top |
| Eichmann em Jerusalém | Hannah Arendt | #NF #politica #etica #testemunho #classico #d2 #e2 #q-liberdade-e-obediencia #q-culpa-e-justica #cenario-guerra-mundial #trilha-liberdade-e-autoritarismo |
| Sobre a Violência | Hannah Arendt | #NF #politica #classico #d2 #e1 #q-poder-e-violencia |
| O Medo à Liberdade | Erich Fromm | #NF #psicologia #autoritarismo #classico #psicologia-social #d2 #e2 #top #rel-fromm #q-liberdade-e-obediencia #ponte-psicanalise-e-politica #trilha-liberdade-e-autoritarismo |
| A Personalidade Autoritária | Adorno, Frenkel-Brunswik, Levinson e Sanford | #NF #psicologia #autoritarismo #classico #psicologia-social #d3 #e3 #rel-fromm #q-liberdade-e-obediencia #papel-desafio #ponte-psicanalise-e-politica |
| O Verdadeiro Crente | Eric Hoffer | #NF #psicologia #politica #classico #d2 #e1 #rel-fromm #q-liberdade-e-obediencia #ponte-psicanalise-e-politica #trilha-liberdade-e-autoritarismo |
| A Mente Moralista | Jonathan Haidt | #NF #psicologia #politica #etica #psicologia-social #d2 #e2 #top #rel-fromm #tenho-digital #papel-contraponto #trilha-brasil-politica-recente |
| Como Funciona o Fascismo | Jason Stanley | #NF #politica #autoritarismo #d1 #e1 #top #rel-fromm #tenho-digital #q-liberdade-e-obediencia #papel-porta-de-entrada #trilha-liberdade-e-autoritarismo |
| A Anatomia do Fascismo | Robert O. Paxton | #NF #politica #autoritarismo #historia #d2 #e2 #rel-fromm |
| O Fascismo Eterno | Umberto Eco | #NF #politica #autoritarismo #d1 #e1 #rel-fromm #q-liberdade-e-obediencia #papel-porta-de-entrada #papel-leitura-relampago #trilha-relampago |
| Crepúsculo da Democracia | Anne Applebaum | #NF #politica #autoritarismo #d1 #e2 #rel-fromm |
| A Era da Raiva | Pankaj Mishra | #NF #politica #historia #d2 #e3 #top #rel-fromm #trilha-liberdade-e-autoritarismo |
| Estranhos em Sua Própria Terra | Arlie Russell Hochschild | #NF #politica #sociologia #d1 #e2 #rel-fromm #papel-contraponto #trilha-brasil-politica-recente |
| O Caminho para a Não Liberdade | Timothy Snyder | #NF #politica #autoritarismo #d2 #e2 #rel-fromm |
| A Sociedade Aberta e Seus Inimigos | Karl Popper | #NF #politica #filosofia #classico #d3 #e3 #rel-fromm #q-liberdade-e-obediencia |
| O Ódio como Política (org.) | Esther Solano | #NF #politica #autoritarismo #BR #d1 #e1 #top #rel-fromm #tenho-digital #trilha-brasil-politica-recente |
| Menos Marx, Mais Mises | Camila Rocha | #NF #politica #BR #d2 #e2 #rel-fromm #trilha-brasil-politica-recente |
| O Mundo do Avesso | Letícia Cesarino | #NF #politica #antropologia #BR #ia #tecnologia #d3 #e2 #rel-fromm #papel-ponte #trilha-brasil-politica-recente |
| A Máquina do Ódio | Patrícia Campos Mello | #NF #politica #BR #testemunho #d1 #e2 #rel-fromm #tenho-digital #trilha-brasil-politica-recente |
| O Brasil Dobrou à Direita | Jairo Nicolau | #NF #politica #BR #d1 #e1 #rel-fromm #trilha-brasil-politica-recente |
| As Direitas nas Redes e nas Ruas (org.) | Esther Solano e Camila Rocha | #NF #politica #BR #d2 #e2 #rel-fromm #trilha-brasil-politica-recente |
| A Tragédia e a Farsa | Flávio Henrique Calheiros Casimiro | #NF #politica #BR #verificar #d3 #e2 #rel-fromm #trilha-brasil-politica-recente |
| Neoliberalismo como Gestão do Sofrimento Psíquico (orgs.) | Safatle, Silva Junior e Dunker | #NF #psicanalise #politica #BR #d3 #e2 #rel-fromm #tenho-digital #ponte-psicanalise-e-politica |
| A Nova Razão do Mundo | Pierre Dardot e Christian Laval | #NF #politica #economia #d3 #e2 #rel-fromm #papel-desafio |
| Realismo Capitalista | Mark Fisher | #NF #politica #economia #d1 #e1 #top #clima-subversivo #trilha-entender-o-presente |
| A Sociedade do Espetáculo | Guy Debord | #NF #politica #sociologia #classico #d3 #e1 #clima-subversivo #trilha-distopias |
| A Sociedade do Cansaço | Byung-Chul Han | #NF #filosofia #sociologia #d1 #e1 #top #tenho-digital #q-sentido-e-como-viver #papel-porta-de-entrada #ponte-psicanalise-e-politica #trilha-entender-o-presente |
| Vigiar e Punir | Michel Foucault | #NF #politica #filosofia #historia #classico #d3 #e3 #top #q-poder-e-violencia #papel-ponte #ponte-corpo-e-poder #trilha-corpo-genero-poder |
| História da Sexualidade I: A Vontade de Saber | Michel Foucault | #NF #filosofia #genero #classico #d3 #e1 #ponte-corpo-e-poder #trilha-corpo-genero-poder |
| Problemas de Gênero | Judith Butler | #NF #genero #filosofia #d3 #e2 #clima-subversivo #ponte-corpo-e-poder |
| Necropolítica | Achille Mbembe | #NF #politica #colonialismo #raca #d3 #e1 #q-poder-e-violencia #ponte-corpo-e-poder |
| Liberalismo Político | John Rawls | #NF #politica #filosofia #d3 #e3 |
| Filosofia Política Contemporânea | Will Kymlicka | #NF #politica #filosofia #introducao #d2 #e3 |
| O Príncipe | Nicolau Maquiavel | #NF #politica #classico #d1 #e1 #q-poder-e-violencia #papel-leitura-relampago #papel-fonte-primaria |
| Leviatã | Thomas Hobbes | #NF #politica #filosofia #classico #d3 #e3 #q-poder-e-violencia #papel-fonte-primaria |
| O Manifesto Comunista | Karl Marx e Friedrich Engels | #NF #politica #economia #classico #d1 #e1 #papel-fonte-primaria |
| A Riqueza das Nações | Adam Smith | #NF #economia #classico #d3 #e3 #papel-fonte-primaria |
| O Caminho da Servidão | Friedrich Hayek | #NF #economia #politica #classico #d2 #e2 #papel-contraponto #trilha-liberdade-e-autoritarismo |
| O Capital no Século XXI | Thomas Piketty | #NF #economia #sociologia #d2 #e3 |
| A Grande Transformação | Karl Polanyi | #NF #economia #historia #classico #d3 #e3 |
| A Tirania do Mérito | Michael Sandel | #NF #politica #etica #d1 #e2 #q-culpa-e-justica |
| Por que as Nações Fracassam | Daron Acemoglu e James Robinson | #NF #economia #politica #historia #d2 #e3 #q-poder-e-violencia |
| Prisioneiros da Geografia | Tim Marshall | #NF #geopolitica #historia #d1 #e2 |
| Sobre a Tirania | Timothy Snyder | #NF #politica #autoritarismo #historia #d1 #e1 #rel-fromm #q-liberdade-e-obediencia #papel-leitura-relampago #trilha-entender-o-presente |
| Biografia do Abismo | Felipe Nunes e Thomas Traumann | #NF #politica #BR #d1 #e1 #rel-fromm |
| Sobre o Autoritarismo Brasileiro | Lilia Schwarcz | #NF #politica #autoritarismo #historia #BR #d1 #e2 #rel-fromm #q-poder-e-violencia |
| Poder e Progresso | Daron Acemoglu e Simon Johnson | #NF #economia #politica #historia #tecnologia #ia #d2 #e3 #ponte-ia-e-humanidade |

---

## 12. Sociedade, antropologia, cultura e história

| Título | Autor | Tags |
|---|---|---|
| O Despertar de Tudo | David Graeber e David Wengrow | #NF #antropologia #historia #d2 #e3 #top #q-natureza-e-civilizacao #clima-subversivo #papel-ponte #trilha-origens |
| The WEIRDest People in the World | Joseph Henrich | #NF #antropologia #psicologia #historia #sem-pt #d3 #e3 |
| As Origens da Ordem Política | Francis Fukuyama | #NF #politica #historia #d2 #e3 #tenho-digital #q-poder-e-violencia |
| A Invenção das Tradições | Eric Hobsbawm e Terence Ranger | #NF #historia #sociologia #classico #d2 #e2 #q-memoria-e-esquecimento |
| A Era dos Extremos | Eric Hobsbawm | #NF #historia #classico #d2 #e3 #cenario-guerra-mundial |
| Orientalismo | Edward Said | #NF #colonialismo #historia #classico #d3 #e2 #q-alteridade-e-contato #clima-subversivo #ponte-ecologia-e-colonialismo #trilha-alteridade |
| Os Condenados da Terra | Frantz Fanon | #NF #colonialismo #politica #classico #d3 #e2 #q-poder-e-violencia #clima-subversivo #ponte-psicanalise-e-politica |
| Pele Negra, Máscaras Brancas | Frantz Fanon | #NF #colonialismo #raca #psicanalise #classico #d3 #e2 #q-identidade-e-eu #ponte-psicanalise-e-politica |
| O Segundo Sexo | Simone de Beauvoir | #NF #genero #filosofia #classico #d3 #e3 #clima-subversivo #ponte-corpo-e-poder #trilha-corpo-genero-poder |
| Pedagogia do Oprimido | Paulo Freire | #NF #politica #BR #classico #educacao #d2 #e2 #clima-subversivo |
| A Interpretação das Culturas | Clifford Geertz | #NF #antropologia #classico #d3 #e2 |
| Ensaio sobre a Dádiva | Marcel Mauss | #NF #antropologia #sociologia #classico #d2 #e1 |
| Tristes Trópicos | Claude Lévi-Strauss | #NF #antropologia #classico #d3 #e2 #q-alteridade-e-contato |
| A Representação do Eu na Vida Cotidiana | Erving Goffman | #NF #sociologia #psicologia #classico #d2 #e2 #q-identidade-e-eu |
| A Ética Protestante e o Espírito do Capitalismo | Max Weber | #NF #sociologia #religiao #classico #d3 #e2 |
| A Imaginação Sociológica | C. Wright Mills | #NF #sociologia #classico #d2 #e2 #tenho-digital |
| O Processo Civilizador | Norbert Elias | #NF #sociologia #historia #classico #d3 #e3 #q-poder-e-violencia #q-natureza-e-civilizacao |
| Modernidade Líquida | Zygmunt Bauman | #NF #sociologia #d2 #e2 #tenho-digital |
| A Construção Social da Realidade | Peter Berger e Thomas Luckmann | #NF #sociologia #classico #d3 #e2 #q-realidade-e-percepcao |
| Origens Culturais da Aquisição do Conhecimento Humano | Michael Tomasello | #NF #antropologia #psicologia #d3 #e2 |
| The Elephant in the Brain | Kevin Simler e Robin Hanson | #NF #psicologia #sociologia #sem-pt #d2 #e2 #papel-contraponto |
| O Cogumelo no Fim do Mundo | Anna Lowenhaupt Tsing | #NF #antropologia #ecologia #economia #d3 #e2 #q-natureza-e-civilizacao #ponte-ecologia-e-colonialismo |
| Ficar com o Problema | Donna Haraway | #NF #filosofia #ecologia #d3 #e2 #ponte-ecologia-e-colonialismo |
| The Posthuman | Rosi Braidotti | #NF #filosofia #ia #sem-pt #tecnologia #d3 #e2 |
| Da Próxima Vez, o Fogo | James Baldwin | #NF #raca #testemunho #classico #d1 #e1 #papel-leitura-relampago |
| Ideias para Adiar o Fim do Mundo | Ailton Krenak | #NF #ecologia #antropologia #BR #d1 #e1 #tenho-digital #q-natureza-e-civilizacao #ponte-ecologia-e-colonialismo #trilha-entender-o-presente |
| A Queda do Céu | Davi Kopenawa e Bruce Albert | #NF #antropologia #espiritualidade #BR #d3 #e3 #tenho-digital #q-alteridade-e-contato #ponte-ecologia-e-colonialismo |
| Histórias | Heródoto | #NF #historia #antiguidade #classico #d2 #e3 #papel-fonte-primaria |
| A Guerra do Peloponeso | Tucídides | #NF #historia #antiguidade #guerra #classico #d3 #e3 #papel-fonte-primaria |
| SPQR | Mary Beard | #NF #historia #roma #antiguidade #d2 #e3 #trilha-roma-por-dentro |
| Rubicon | Tom Holland | #NF #historia #roma #antiguidade #d1 #e2 #trilha-roma-por-dentro |
| Um Espelho Distante | Barbara Tuchman | #NF #historia #medieval #d2 #e3 |
| O Queijo e os Vermes | Carlo Ginzburg | #NF #historia #religiao #classico #d2 #e1 #q-fe-e-duvida #papel-ponte #ponte-ciencia-e-fe |
| A Invenção da Ciência | David Wootton | #NF #historia #ciencia #d3 #e3 |
| É Isto um Homem? | Primo Levi | #NF #guerra #testemunho #classico #d1 #e1 #top #clima-cru-e-chocante #papel-leitura-relampago #cenario-guerra-mundial |
| Hiroshima | John Hersey | #NF #guerra #testemunho #classico #d1 #e1 #clima-cru-e-chocante #cenario-guerra-mundial |
| Vozes de Tchernóbil | Svetlana Aleksiévitch | #NF #testemunho #historia #d2 #e2 #q-memoria-e-esquecimento #clima-cru-e-chocante #cenario-russia |
| O Diário de Anne Frank | Anne Frank | #NF #guerra #testemunho #classico #d1 #e1 #clima-emocionante #cenario-guerra-mundial |
| Longa Caminhada até a Liberdade | Nelson Mandela | #NF #biografia #africa #politica #d1 #e3 |
| O Estupro de Nanquim | Iris Chang | #NF #guerra #historia #asia #d2 #e2 #clima-cru-e-chocante #cenario-guerra-mundial |
| A Sangue Frio | Truman Capote | #NF #testemunho #misterio #classico #d1 #e2 #q-culpa-e-justica #clima-cru-e-chocante |
| Casa-Grande & Senzala | Gilberto Freyre | #NF #BR #historia #sociologia #classico #d3 #e3 #tenho-digital #papel-contraponto #trilha-brasil-profundo |
| Raízes do Brasil | Sérgio Buarque de Holanda | #NF #BR #historia #sociologia #classico #d2 #e2 #tenho-digital #trilha-brasil-profundo |
| Formação do Brasil Contemporâneo | Caio Prado Júnior | #NF #BR #historia #economia #classico #d3 #e2 #trilha-brasil-profundo |
| O Povo Brasileiro | Darcy Ribeiro | #NF #BR #antropologia #historia #d2 #e3 #tenho-digital #papel-porta-de-entrada #trilha-brasil-profundo |
| Quarto de Despejo | Carolina Maria de Jesus | #NF #BR #testemunho #raca #classico #d1 #e1 #top #clima-cru-e-chocante #clima-emocionante #trilha-brasil-profundo |
| As Veias Abertas da América Latina | Eduardo Galeano | #NF #latam #historia #economia #colonialismo #d2 #e3 #tenho-digital #papel-contraponto #ponte-ecologia-e-colonialismo |
| Brasil: Uma Biografia | Lilia Schwarcz e Heloisa Starling | #NF #BR #historia #d2 #e3 #tenho-digital #papel-porta-de-entrada |
| 1808 | Laurentino Gomes | #NF #BR #historia #d1 #e2 |
| Holocausto Brasileiro | Daniela Arbex | #NF #BR #testemunho #d1 #e2 #clima-cru-e-chocante #ponte-corpo-e-poder |
| Estação Carandiru | Drauzio Varella | #NF #BR #testemunho #d1 #e2 #clima-cru-e-chocante |
| Escravidão (trilogia) | Laurentino Gomes | #NF #BR #historia #raca #colonialismo #d1 #e3 #q-poder-e-violencia |
| O Pacto da Branquitude | Cida Bento | #NF #BR #raca #psicologia #sociologia #d1 #e1 |
| Na Ponta da Língua | Caetano W. Galindo | #NF #BR #linguagem #historia #d1 #e2 |

---

## 13. Ciência, tecnologia e futuro

| Título | Autor | Tags |
|---|---|---|
| A Origem das Espécies | Charles Darwin | #NF #ciencia #classico #biologia #d3 #e3 #papel-fonte-primaria |
| O Gene Egoísta | Richard Dawkins | #NF #ciencia #biologia #d2 #e2 #papel-porta-de-entrada |
| Cosmos | Carl Sagan | #NF #ciencia #classico #fisica #d1 #e2 #papel-porta-de-entrada |
| Pálido Ponto Azul | Carl Sagan | #NF #ciencia #classico #fisica #d1 #e2 #tenho-digital #trilha-do-quark-ao-cosmos |
| O Mundo Assombrado pelos Demônios | Carl Sagan | #NF #ciencia #filosofia #classico #d1 #e2 #top #tenho-digital #papel-contraponto #ponte-ciencia-e-fe #trilha-fronteiras-do-inexplicavel |
| O Senhor Está Brincando, Sr. Feynman! | Richard Feynman | #NF #ciencia #biografia #humor #fisica #d1 #e2 #clima-comico |
| A Falsa Medida do Homem | Stephen Jay Gould | #NF #ciencia #historia #classico #biologia #psicometria #d2 #e2 #tenho-digital #papel-ponte |
| A Estrutura das Revoluções Científicas | Thomas S. Kuhn | #NF #ciencia #filosofia #classico #d2 #e1 #top #papel-ponte |
| O Cisne Negro | Nassim Taleb | #NF #ciencia #economia #d2 #e2 |
| Uma Breve História do Tempo | Stephen Hawking | #NF #ciencia #fisica #d2 #e1 #tenho-digital #trilha-do-quark-ao-cosmos |
| Uma Breve História de Quase Tudo | Bill Bryson | #NF #ciencia #humor #d1 #e3 #clima-comico #papel-porta-de-entrada |
| A Sexta Extinção | Elizabeth Kolbert | #NF #ciencia #ecologia #biologia #d1 #e2 #q-natureza-e-civilizacao |
| O Gene | Siddhartha Mukherjee | #NF #ciencia #medicina #biologia #d2 #e3 |
| O Imperador de Todos os Males | Siddhartha Mukherjee | #NF #ciencia #medicina #historia #d2 #e3 #trilha-bisturi-e-fe |
| A Ordem do Tempo | Carlo Rovelli | #NF #ciencia #filosofia #fisica #d2 #e1 #q-realidade-e-percepcao |
| O Início da Infinidade | David Deutsch | #NF #ciencia #filosofia #fisica #d3 #e3 |
| A Informação | James Gleick | #NF #ciencia #historia #d2 #e3 |
| Superinteligência | Nick Bostrom | #NF #ia #filosofia #tecnologia #d3 #e2 #tenho-digital #ponte-ia-e-humanidade |
| Vida 3.0 | Max Tegmark | #NF #ia #ciencia #tecnologia #d2 #e2 #tenho-digital #ponte-ia-e-humanidade #trilha-maquinas-que-pensam |
| The Alignment Problem | Brian Christian | #NF #ia #etica #sem-pt #tecnologia #d2 #e3 #ponte-ia-e-humanidade |
| The Precipice | Toby Ord | #NF #ciencia #etica #sem-pt #d2 #e3 |
| A Era da Inteligência Artificial | Kissinger, Schmidt e Huttenlocher | #NF #ia #geopolitica #tecnologia #d1 #e2 |
| The Ethics of Information | Luciano Floridi | #NF #ia #etica #sem-pt #tecnologia #d3 #e3 |
| Oxford Handbook of Digital Ethics | Carissa Véliz (org.) | #NF #ia #etica #sem-pt #tecnologia #d3 #e3 |
| A Geração Superficial | Nicholas Carr | #NF #ia #psicologia #tecnologia #d1 #e2 #tenho-digital |
| A Sociedade Tecnológica | Jacques Ellul | #NF #filosofia #ia #classico #tecnologia #d3 #e3 |
| Cibernética e Sociedade | Norbert Wiener | #NF #ia #ciencia #classico #tecnologia #d2 #e2 #ponte-ia-e-humanidade |
| Algoritmos de Destruição em Massa | Cathy O'Neil | #NF #ia #etica #tecnologia #d1 #e2 #ponte-ia-e-humanidade |
| A Era do Capitalismo de Vigilância | Shoshana Zuboff | #NF #ia #politica #economia #tecnologia #d3 #e3 #ponte-ia-e-humanidade |
| Sete Breves Lições de Física | Carlo Rovelli | #NF #ciencia #fisica #d1 #e1 #papel-porta-de-entrada #papel-leitura-relampago #trilha-do-quark-ao-cosmos |
| Um Mundo Imenso | Ed Yong | #NF #ciencia #biologia #d2 #e3 #q-alteridade-e-contato #q-realidade-e-percepcao |
| A Canção da Célula | Siddhartha Mukherjee | #NF #ciencia #medicina #biologia #historia #d2 #e3 |
| O Império da IA | Karen Hao | #NF #ia #tecnologia #politica #economia #d2 #e2 #q-poder-e-violencia #ponte-ia-e-humanidade #trilha-maquinas-que-pensam |
| Mortais | Atul Gawande | #NF #medicina #morte #d1 #e2 #q-morte-e-finitude #trilha-cuidar-ate-o-fim |
| O Último Sopro de Vida | Paul Kalanithi | #NF #medicina #morte #biografia #testemunho #d1 #e1 #q-morte-e-finitude #q-sentido-e-como-viver #clima-emocionante #papel-leitura-relampago #trilha-cuidar-ate-o-fim |

---

## 14. Psicologia, psicanálise e comportamento

| Título | Autor | Tags |
|---|---|---|
| Rápido e Devagar: Duas Formas de Pensar | Daniel Kahneman | #NF #psicologia #economia #d2 #e3 #top #tenho-digital #papel-porta-de-entrada |
| As Armas da Persuasão | Robert Cialdini | #NF #psicologia #psicologia-social #d1 #e2 #tenho-digital |
| O Animal Social | Elliot Aronson | #NF #psicologia #sociologia #psicologia-social #d1 #e2 |
| O Efeito Lúcifer | Philip Zimbardo | #NF #psicologia #etica #psicologia-social #d2 #e3 #q-liberdade-e-obediencia |
| The Cultural Animal | Roy Baumeister | #NF #psicologia #antropologia #sem-pt #psicologia-social #d3 #e3 |
| Mistakes Were Made (But Not by Me) | Carol Tavris e Elliot Aronson | #NF #psicologia #sem-pt #psicologia-social #d1 #e2 |
| Tábula Rasa | Steven Pinker | #NF #psicologia #ciencia #d2 #e3 #q-o-que-e-humano #papel-contraponto |
| O Animal Moral | Robert Wright | #NF #psicologia #ciencia #etica #d2 #e3 #q-o-que-e-humano #papel-contraponto |
| O Mal-Estar na Civilização | Sigmund Freud | #NF #psicanalise #classico #d2 #e1 #rel-fromm #tenho-digital #q-natureza-e-civilizacao #papel-ponte #ponte-psicanalise-e-politica #trilha-psicanalise-em-degraus |
| A Negação da Morte | Ernest Becker | #NF #psicologia #morte #antropologia #classico #d3 #e2 #top #q-morte-e-finitude #papel-ponte #trilha-finitude |
| The Worm at the Core | Solomon, Greenberg e Pyszczynski | #NF #psicologia #morte #sem-pt #d2 #e2 #q-morte-e-finitude |
| A Vida Examinada | Stephen Grosz | #NF #psicanalise #psicologia #d1 #e1 |
| De Frente para o Sol: Como Superar o Terror da Morte | Irvin D. Yalom | #NF #psicologia #morte #existencialismo #d1 #e2 #rel-yalom #tenho-digital #q-morte-e-finitude #trilha-finitude #trilha-cuidar-ate-o-fim |
| O Enigma de Espinosa | Irvin D. Yalom | #F #filosofia #psicologia #d1 #e2 #rel-yalom #tenho-digital #clima-cerebral #ponte-ficcao-e-filosofia #trilha-yalom-nietzsche |
| A Cura de Schopenhauer | Irvin D. Yalom | #F #filosofia #psicologia #d1 #e2 #rel-yalom #clima-cerebral #ponte-ficcao-e-filosofia #trilha-yalom-nietzsche |
| A Arte de Amar | Erich Fromm | #NF #psicologia #classico #d1 #e1 #rel-fromm #tenho-digital |
| Flow | Mihaly Csikszentmihalyi | #NF #psicologia #psicologia-humanista #d1 #e2 #q-sentido-e-como-viver |
| O Carrasco do Amor | Irvin D. Yalom | #NF #psicologia #existencialismo #d1 #e2 #rel-yalom #papel-porta-de-entrada #trilha-formacao-do-terapeuta |
| Uma Hora de Conexão | Irvin D. Yalom e Benjamin Yalom | #NF #psicologia #existencialismo #d1 #e2 #rel-yalom #q-sentido-e-como-viver #trilha-formacao-do-terapeuta |
| Análise | Vera Iaconelli | #NF #psicanalise #biografia #BR #d1 #e1 #q-identidade-e-eu #trilha-psicanalise-em-degraus |
| Tornar-se Negro | Neusa Santos Souza | #NF #psicanalise #raca #BR #classico #d2 #e1 #q-identidade-e-eu #ponte-psicanalise-e-politica |
| O Corpo Guarda as Marcas | Bessel van der Kolk | #NF #psicologia #psiquiatria #neurociencia #psicopatologia #d2 #e2 |
| A Geração Ansiosa | Jonathan Haidt | #NF #psicologia #parentalidade #tecnologia #d1 #e2 #trilha-pai-em-construcao |
| Longe da Árvore | Andrew Solomon | #NF #psicologia #parentalidade #identidade #d2 #e3 #q-identidade-e-eu #q-alteridade-e-contato #papel-desafio |

---

## 15. Espiritualidade, espiritismo e mistérios da consciência

| Título | Autor | Tags |
|---|---|---|
| O Livro dos Espíritos | Allan Kardec | #NF #espiritismo #religiao #classico #d2 #e2 #top #papel-porta-de-entrada #papel-fonte-primaria #trilha-fronteiras-do-inexplicavel |
| O Livro dos Médiuns | Allan Kardec | #NF #espiritismo #classico #d2 #e2 #clima-onirico |
| O Evangelho Segundo o Espiritismo | Allan Kardec | #NF #espiritismo #religiao #classico #d1 #e2 |
| O Céu e o Inferno | Allan Kardec | #NF #espiritismo #morte #classico #d2 #e2 #q-morte-e-finitude |
| A Gênese | Allan Kardec | #NF #espiritismo #ciencia #classico #d2 #e2 #ponte-ciencia-e-fe |
| Nosso Lar | André Luiz / Chico Xavier | #F #espiritismo #morte #BR #d1 #e2 #top #q-morte-e-finitude #trilha-fronteiras-do-inexplicavel |
| Missionários da Luz | André Luiz / Chico Xavier | #F #espiritismo #BR #d2 #e2 |
| Libertação | André Luiz / Chico Xavier | #F #espiritismo #BR #d2 #e2 |
| Evolução em Dois Mundos | André Luiz / Chico Xavier e Waldo Vieira | #NF #espiritismo #BR #d3 #e2 |
| Memórias de um Suicida | Yvonne Pereira | #F #espiritismo #morte #BR #d2 #e3 |
| Violetas na Janela | Vera Lúcia Marinzeck de Carvalho | #F #espiritismo #BR #d1 #e2 |
| Há Dois Mil Anos... | Emmanuel / Chico Xavier | #F #espiritismo #romance-historico #roma #BR #antiguidade #d1 #e3 #ponte-historia-e-ficcao #trilha-roma-por-dentro |
| Diálogo com as Sombras | Hermínio C. Miranda | #NF #espiritismo #BR #d2 #e2 |
| As Vidas de Chico Xavier | Marcel Souto Maior | #NF #biografia #espiritismo #BR #d1 #e2 |
| Depois da Morte | Léon Denis | #NF #espiritismo #morte #classico #d2 #e2 #q-morte-e-finitude |
| A Morte e o Seu Mistério | Camille Flammarion | #NF #espiritismo #morte #classico #d2 #e3 #q-morte-e-finitude |
| Espírito, Perispírito e Alma | Hernani Guimarães Andrade | #NF #espiritismo #ciencia #BR #d3 #e2 #ponte-ciencia-e-fe |
| Doutrina e Teologia de Umbanda Sagrada | Rubens Saraceni | #NF #umbanda #religiao #BR #d2 #e2 |
| Umbanda de Todos Nós | W.W. da Matta e Silva | #NF #umbanda #BR #d2 #e2 |
| Mitologia dos Orixás | Reginaldo Prandi | #NF #umbanda #antropologia #BR #mitologia #d1 #e3 #tenho-digital #papel-porta-de-entrada #trilha-terreiro-e-encruzilhada |
| Orixás | Pierre Verger | #NF #umbanda #antropologia #arte #d2 #e2 #trilha-terreiro-e-encruzilhada |
| Os Nagô e a Morte | Juana Elbein dos Santos | #NF #umbanda #antropologia #morte #BR #d3 #e2 #q-morte-e-finitude #trilha-terreiro-e-encruzilhada |
| O Espírito da Intimidade | Malidoma Somé | #NF #espiritualidade #africa #antropologia #d2 #e2 |
| Bhagavad Gita | (tradição hindu) | #NF #oriental #espiritualidade #classico #d2 #e1 #top #tenho-digital #clima-contemplativo #papel-porta-de-entrada #papel-fonte-primaria |
| Os Upanixades | (tradição hindu) | #NF #oriental #filosofia #classico #d3 #e2 #papel-fonte-primaria |
| Yoga Sutras de Patanjali | Patanjali | #NF #oriental #mistica #classico #d3 #e1 #papel-fonte-primaria |
| Tao Te Ching | Lao Tsé | #NF #oriental #filosofia #classico #d2 #e1 #clima-contemplativo #papel-fonte-primaria |
| Dhammapada | (tradição budista) | #NF #oriental #espiritualidade #classico #d1 #e1 #clima-contemplativo #papel-porta-de-entrada |
| Livro Tibetano dos Mortos (Bardo Thödol) | (tradição tibetana) | #NF #oriental #morte #mistica #classico #d3 #e2 #q-morte-e-finitude #trilha-finitude |
| Autobiografia de um Iogue | Paramahansa Yogananda | #NF #oriental #biografia #espiritualidade #d1 #e2 |
| Eu Sou Aquilo | Nisargadatta Maharaj | #NF #oriental #espiritualidade #d3 #e2 |
| Chakras: Centros Energéticos de Transformação | Harish Johari | #NF #oriental #mistica #d2 #e2 #tenho-digital |
| Rodas da Vida (Wheels of Life) | Anodea Judith | #NF #mistica #psicologia #d1 #e2 |
| Fédon | Platão | #NF #filosofia #morte #antiguidade #classico #d2 #e1 #q-morte-e-finitude #trilha-finitude |
| Os Evangelhos Gnósticos | Elaine Pagels | #NF #religiao #historia #mistica #d2 #e2 #q-fe-e-duvida |
| A Conferência dos Pássaros | Farid ud-Din Attar | #NF #mistica #classico #d2 #e1 #clima-contemplativo |
| Do Céu e do Inferno | Emanuel Swedenborg | #NF #mistica #morte #classico #d3 #e2 #q-morte-e-finitude |
| A Cabala e seu Simbolismo | Gershom Scholem | #NF #mistica #religiao #d3 #e2 |
| A Voz do Silêncio | Helena Blavatsky | #NF #mistica #oriental #classico #d2 #e1 |
| Vida depois da Vida | Raymond Moody | #NF #morte #consciencia #classico #d1 #e1 #q-morte-e-finitude #ponte-ciencia-e-fe #trilha-fronteiras-do-inexplicavel |
| Consciência Além da Vida | Pim van Lommel | #NF #morte #consciencia #medicina #d2 #e2 #q-morte-e-finitude #ponte-ciencia-e-fe #trilha-fronteiras-do-inexplicavel |
| As Variedades da Experiência Religiosa | William James | #NF #psicologia #religiao #classico #d3 #e3 #papel-ponte #ponte-ciencia-e-fe #trilha-fronteiras-do-inexplicavel |
| Memórias, Sonhos, Reflexões | Carl G. Jung | #NF #psicologia #psicanalise #biografia #classico #psicologia-analitica #d2 #e2 #papel-ponte #ponte-ciencia-e-fe #trilha-fronteiras-do-inexplicavel #trilha-jung-para-comecar |
| Sobre a Morte e o Morrer | Elisabeth Kübler-Ross | #NF #morte #psicologia #classico #d1 #e2 #tenho-digital #q-morte-e-finitude #trilha-finitude #trilha-cuidar-ate-o-fim |
| O Tao da Física | Fritjof Capra | #NF #ciencia #oriental #classico #fisica #d2 #e2 #papel-contraponto #ponte-ciencia-e-fe |
| Por que as Pessoas Acreditam em Coisas Estranhas | Michael Shermer | #NF #ciencia #psicologia #d1 #e2 #tenho-digital #q-fe-e-duvida #papel-contraponto #ponte-ciencia-e-fe #trilha-fronteiras-do-inexplicavel |
| Spook: Science Tackles the Afterlife | Mary Roach | #NF #ciencia #morte #humor #sem-pt #d1 #e2 #q-morte-e-finitude #ponte-ciencia-e-fe |
| O Alquimista | Paulo Coelho | #F #espiritualidade #BR #d1 #e1 |
| O Jogo das Contas de Vidro | Hermann Hesse | #F #espiritualidade #filosofia #classico #d3 #e3 #ponte-ficcao-e-filosofia |
| A Última Tentação de Cristo | Nikos Kazantzákis | #F #religiao #classico #d2 #e3 #q-fe-e-duvida |
| A Morte é um Dia que Vale a Pena Viver | Ana Claudia Quintana Arantes | #NF #morte #medicina #BR #d1 #e1 #q-morte-e-finitude #clima-emocionante #papel-porta-de-entrada #trilha-cuidar-ate-o-fim |
| Muitas Vidas, Muitos Mestres | Brian Weiss | #NF #espiritualidade #psiquiatria #morte #d1 #e1 #ponte-ciencia-e-fe |
| Fogo no Mato: A Ciência Encantada das Macumbas | Luiz Antonio Simas e Luiz Rufino | #NF #umbanda #filosofia #BR #d2 #e1 #trilha-terreiro-e-encruzilhada |

---

## 16. Artes, escrita, cinema e parentalidade

| Título | Autor | Tags |
|---|---|---|
| Sobre a Escrita | Stephen King | #NF #escrita #biografia #d1 #e2 |
| Story | Robert McKee | #NF #escrita #cinema #d2 #e3 |
| O Herói de Mil Faces | Joseph Campbell | #NF #escrita #religiao #antropologia #classico #mitologia #d2 #e3 #tenho-digital #papel-ponte |
| Esculpindo o Tempo | Andrei Tarkovski | #NF #cinema #arte #classico #d3 #e2 |
| Hitchcock/Truffaut | François Truffaut | #NF #cinema #classico #d2 #e3 |
| Maneiras de Ver | John Berger | #NF #arte #classico #d1 #e1 |
| A História da Arte | E.H. Gombrich | #NF #arte #historia #classico #d1 #e3 |
| O Cérebro da Criança | Daniel Siegel e Tina Bryson | #NF #parentalidade #neurociencia #d1 #e2 #trilha-pai-em-construcao |
| Escrever Ficção | Luiz Antonio de Assis Brasil | #NF #escrita #BR #RS #d1 #e2 #papel-porta-de-entrada |
| A Criança e o seu Mundo | D.W. Winnicott | #NF #parentalidade #psicanalise #classico #d1 #e2 #trilha-pai-em-construcao |
| Manifesto Antimaternalista | Vera Iaconelli | #NF #psicanalise #parentalidade #genero #BR #d2 #e2 #ponte-corpo-e-poder |

---

## 17. Biblioteca virtual (tenho: digital)

Livros e quadrinhos da biblioteca virtual que não estavam nas seções anteriores, separados pelos mesmos eixos. Os que já estavam catalogados continuam na seção de origem e ganharam `#tenho-digital`. Os quadrinhos levam `#HQ`; uma série é uma linha só, sejam quantas forem as edições.

> Seção gerada por `tools/importar_digital.py` a partir de `biblioteca-virtual/inventario.tsv`. Para corrigir título, autor, eixo, dificuldade, extensão ou temas, corrija o inventário e rode o script; aqui, só `#lido` e `#top`, postos à mão, são preservados.

### 17.2 Ficção científica, fantasia e distopia

| Título | Autor | Tags |
|---|---|---|
| 18 Dias | Grant Morrison | #HQ #fantasia #mitologia #d2 #e1 #tenho-digital |
| 1984 (em quadrinhos) | George Orwell e Fido Nesti | #HQ #distopia #adaptacao #politica #classico #d1 #e2 #tenho-digital |
| 20 Mil Léguas Submarinas: Edição Comentada e Ilustrada | Júlio Verne | #F #ficcao-cientifica #aventura #classico #d1 #e2 #tenho-digital |
| 2001: Uma Odisseia no Espaço (em quadrinhos) | Jack Kirby | #HQ #ficcao-cientifica #adaptacao #d1 #e2 #tenho-digital |
| 20th Century Boys | Naoki Urasawa | #HQ #manga #ficcao-cientifica #misterio #asia #d1 #e3 #tenho-digital |
| A Cidade do Sol | Tommaso Campanella | #F #utopia #filosofia #classico #d2 #e1 #tenho-digital |
| A Cidade Inteira Dorme | Ray Bradbury | #F #contos #ficcao-cientifica #horror #d1 #e1 #tenho-digital |
| A Cidade Perdida de Marte | Ray Bradbury | #F #ficcao-cientifica #contos #d1 #e1 #tenho-digital |
| A Companhia Negra | Glen Cook | #F #fantasia #d2 #e2 #tenho-digital |
| A Cor da Magia | Terry Pratchett | #F #fantasia #humor #d1 #e1 #tenho-digital |
| A Filha do Império | Raymond E. Feist e Janny Wurts | #F #fantasia #d1 #e2 #tenho-digital |
| A Floresta Sombria | Cixin Liu | #F #ficcao-cientifica #asia #d2 #e2 #tenho-digital |
| A Fome e o Crepúsculo | G. Willow Wilson e Chris Wildgoose | #HQ #fantasia #d1 #e1 #tenho-digital |
| A Fúria do Assassino | Robin Hobb | #F #fantasia #d1 #e3 #tenho-digital |
| A Garra do Conciliador | Gene Wolfe | #F #ficcao-cientifica #fantasia #d3 #e2 #tenho-digital |
| A Guerra dos Reinos | Jason Aaron e Russell Dauterman | #HQ #super-herois #fantasia #d1 #e2 #tenho-digital |
| A História sem Fim | Michael Ende | #F #fantasia #classico #d1 #e2 #tenho-digital |
| A Liga da Lei (Mistborn: Segunda Era, vol. 1) | Brandon Sanderson | #F #fantasia #d1 #e2 #tenho-digital |
| A Máquina Diferencial | William Gibson e Bruce Sterling | #F #ficcao-cientifica #historia-alternativa #d2 #e2 #tenho-digital |
| A Morte da Terra | J.H. Rosny Aîné | #F #ficcao-cientifica #classico #d2 #e1 #tenho-digital |
| A Morte de X | Jeff Lemire, Charles Soule e Aaron Kuder | #HQ #super-herois #d1 #e1 #tenho-digital |
| A Música do Silêncio | Patrick Rothfuss | #F #fantasia #d1 #e1 #tenho-digital |
| A Nuvem | Neal Shusterman | #F #ficcao-cientifica #distopia #d1 #e2 #tenho-digital |
| A Quinta Estação | N.K. Jemisin | #F #fantasia #ficcao-cientifica #d2 #e2 #trilha-fantasia-de-folego #tenho-digital |
| A Redenção do Anjo Caído | Fabio Baptista | #F #fantasia #BR #d1 #e2 #tenho-digital |
| A Revolução dos Bichos (em quadrinhos) | George Orwell, Lillo Parra e Chairim Arrais | #HQ #adaptacao #distopia #politica #classico #BR #d1 #e1 #tenho-digital |
| A Saga de Elric, Livro 1 | Michael Moorcock | #F #fantasia #classico #d1 #e3 #tenho-digital |
| A Saga de Elric, Livro 2 | Michael Moorcock | #F #fantasia #classico #d1 #e3 #tenho-digital |
| A Senhora do Império | Raymond E. Feist e Janny Wurts | #F #fantasia #d1 #e3 #tenho-digital |
| A Serva do Império | Raymond E. Feist e Janny Wurts | #F #fantasia #d1 #e3 #tenho-digital |
| A Sombra do Torturador | Gene Wolfe | #F #ficcao-cientifica #fantasia #d3 #e2 #tenho-digital |
| A Torre | Jan Kounen, Omar Ladgham e Mr Fab | #HQ #ficcao-cientifica #distopia #d1 #e1 #tenho-digital |
| A Última Colônia | John Scalzi | #F #ficcao-cientifica #d1 #e2 #tenho-digital |
| Abaddon | Christophe Bec e Robert Carey | #HQ #ficcao-cientifica #horror #d1 #e1 #tenho-digital |
| Akira | Katsuhiro Otomo | #HQ #manga #ficcao-cientifica #distopia #classico #asia #d2 #e3 #trilha-quadrinhos-para-gente-grande #tenho-digital |
| Alerta de Risco | Neil Gaiman | #F #fantasia #contos #d1 #e2 #tenho-digital |
| Alerta Vermelho | Martha Wells | #F #ficcao-cientifica #d1 #e1 #tenho-digital |
| Aliens: Labyrinth | Jim Woodring e Kilian Plunkett | #HQ #ficcao-cientifica #horror #d1 #e1 #tenho-digital |
| Amanhã | Leo, Rodolphe e Louis Alloing | #HQ #ficcao-cientifica #d1 #e1 #tenho-digital |
| Androides Sonham com Ovelhas Elétricas? (em quadrinhos) | Philip K. Dick e Tony Parker | #HQ #ficcao-cientifica #adaptacao #d2 #e3 #tenho-digital |
| Anões | Nicolas Jarry e outros | #HQ #fantasia #d1 #e3 #tenho-digital |
| Antologia da Literatura Fantástica | Jorge Luis Borges, Adolfo Bioy Casares e Silvina Ocampo | #F #contos #fantasia #antologia #classico #latam #d2 #e2 #tenho-digital |
| As Brigadas Fantasma | John Scalzi | #F #ficcao-cientifica #d1 #e2 #tenho-digital |
| As Crônicas de Âmbar, tomo I | Roger Zelazny | #F #fantasia #classico #d1 #e3 #tenho-digital |
| As Crônicas de Âmbar, tomo II | Roger Zelazny | #F #fantasia #classico #d1 #e3 #tenho-digital |
| As Eras Perdidas | Jérôme Le Gris e Didier Poli | #HQ #fantasia #historia-alternativa #d1 #e1 #tenho-digital |
| As Sereias de Titã | Kurt Vonnegut | #F #ficcao-cientifica #humor #classico #d2 #e2 #tenho-digital |
| As Sombras de Si Mesmo (Mistborn: Segunda Era, vol. 2) | Brandon Sanderson | #F #fantasia #d1 #e2 #tenho-digital |
| As Trevas de Sethanon | Raymond E. Feist | #F #fantasia #d1 #e2 #tenho-digital |
| Asgard | Xavier Dorison e Ralph Meyer | #HQ #fantasia #mitologia #medieval #d1 #e1 #tenho-digital |
| Astronauta: Assimetria (Graphic MSP) | Danilo Beyruth | #HQ #ficcao-cientifica #BR #d1 #e1 #tenho-digital |
| Astronauta: Entropia (Graphic MSP) | Danilo Beyruth | #HQ #ficcao-cientifica #BR #d1 #e1 #tenho-digital |
| Batman | Vários autores | #HQ #super-herois #d1 #e3 #tenho-digital |
| Batman '89 | Sam Hamm e Joe Quinones | #HQ #super-herois #d1 #e1 #tenho-digital |
| Batman '89: Ecos | Sam Hamm e Joe Quinones | #HQ #super-herois #d1 #e1 #tenho-digital |
| Batman Absoluto | Scott Snyder e Nick Dragotta | #HQ #super-herois #d1 #e2 #tenho-digital |
| Batman: O Cavaleiro das Trevas III – A Raça Superior | Frank Miller, Brian Azzarello e Andy Kubert | #HQ #super-herois #d1 #e2 #tenho-digital |
| Batman: O Último Cavaleiro da Terra | Scott Snyder e Greg Capullo | #HQ #super-herois #distopia #d1 #e1 #tenho-digital |
| Batman: Padrões Sombrios | Dan Watters e Hayden Sherman | #HQ #super-herois #policial #d1 #e2 #tenho-digital |
| Bomba X | Vincent Brugeas e outros | #HQ #guerra #historia #d1 #e1 #tenho-digital |
| Bran Mak Morn: O Último Rei dos Pictos | Robert E. Howard | #F #fantasia #contos #classico #d1 #e2 #tenho-digital |
| Caçadores de Trolls | Guillermo del Toro e Daniel Kraus | #F #fantasia #horror #d1 #e2 #tenho-digital |
| Calamidade | Brandon Sanderson | #F #ficcao-cientifica #super-herois #d1 #e2 #tenho-digital |
| Cama de Gato | Kurt Vonnegut | #F #ficcao-cientifica #humor #classico #d2 #e2 #tenho-digital |
| Castelo de Areia | Pierre Oscar Lévy e Frederik Peeters | #HQ #ficcao-cientifica #misterio #d2 #e1 #tenho-digital |
| Cavaleiro vs. Samurai | David Dastmalchian e Fede Mele | #HQ #fantasia #aventura #d1 #e1 #tenho-digital |
| Cavalgada dos Quadrinhos Amaldiçoados | Vários autores | #HQ #horror #antologia #d1 #e2 #tenho-digital |
| Celestia | Manuele Fior | #HQ #ficcao-cientifica #d2 #e2 #tenho-digital |
| Charada: Ano Um | Paul Dano e Stevan Subic | #HQ #super-herois #policial #d1 #e2 #tenho-digital |
| Ciclo Terramar (volume único) | Ursula K. Le Guin | #F #fantasia #classico #d1 #e3 #tenho-digital |
| Cirurgião X | Sara Kenney e John Watkiss | #HQ #ficcao-cientifica #medicina #d1 #e1 #tenho-digital |
| Coda | Simon Spurrier e Matías Bergara | #HQ #fantasia #d1 #e2 #tenho-digital |
| Coleção Oficial de Graphic Novels Marvel (Salvat) | Vários autores | #HQ #super-herois #d1 #e3 #tenho-digital |
| Conan | Robert E. Howard | #F #fantasia #contos #classico #d1 #e2 #tenho-digital |
| Conan: A Torre do Elefante | Robert E. Howard | #HQ #fantasia #adaptacao #d1 #e1 #tenho-digital |
| Conan, o Bárbaro (em quadrinhos) | Vários autores | #HQ #fantasia #d1 #e3 #tenho-digital |
| Conan, o Bárbaro, Livro 1 | Robert E. Howard | #F #fantasia #contos #classico #d1 #e3 #tenho-digital |
| Conan, o Bárbaro, Livro 2 | Robert E. Howard | #F #fantasia #contos #classico #d1 #e3 #tenho-digital |
| Conan, o Cimério: Edição Definitiva, vol. 1 | Robert E. Howard | #F #fantasia #contos #classico #d1 #e3 #tenho-digital |
| Conan, o Sangue da Serpente | S.M. Stirling | #F #fantasia #d1 #e2 #tenho-digital |
| Condição Artificial | Martha Wells | #F #ficcao-cientifica #d1 #e1 #tenho-digital |
| Contágio | Vários autores | #HQ #super-herois #d1 #e2 #verificar #tenho-digital |
| Contato | Carl Sagan | #F #ficcao-cientifica #classico #d2 #e2 #tenho-digital |
| Contos do Multiverso Sombrio | Vários autores | #HQ #super-herois #d1 #e2 #tenho-digital |
| Coração de Aço | Brandon Sanderson | #F #ficcao-cientifica #super-herois #d1 #e2 #tenho-digital |
| Count Zero | William Gibson | #F #ficcao-cientifica #d2 #e2 #tenho-digital |
| Crise Final | Grant Morrison e J.G. Jones | #HQ #super-herois #d2 #e2 #tenho-digital |
| Crise Infinita | Geoff Johns e Phil Jimenez | #HQ #super-herois #d1 #e2 #tenho-digital |
| Crônicas de Espada e Feitiçaria | Gardner Dozois (org.) | #F #fantasia #antologia #contos #d1 #e3 #tenho-digital |
| Dark Engine | Ryan Burton e John Bivens | #HQ #fantasia #ficcao-cientifica #d1 #e1 #tenho-digital |
| Dawnrunner | Ram V e Evan Cagle | #HQ #ficcao-cientifica #d1 #e1 #tenho-digital |
| Deadpool: Dog Park | Stefan Petrucha | #F #super-herois #humor #d1 #e2 #tenho-digital |
| Deadpool Mata o Universo Marvel | Cullen Bunn e Dalibor Talajić | #HQ #super-herois #humor #d1 #e1 #tenho-digital |
| Deadpool vs. Velho Logan | Declan Shalvey e Mike Henderson | #HQ #super-herois #d1 #e1 #tenho-digital |
| Death Dealer: Mercador da Morte | Mitch Iverson e Stefano Martino | #HQ #fantasia #d1 #e1 #tenho-digital |
| Depois do Incal | Alejandro Jodorowsky e Moebius | #HQ #ficcao-cientifica #d2 #e1 #tenho-digital |
| Deuses Americanos (em quadrinhos) | Neil Gaiman, P. Craig Russell e Scott Hampton | #HQ #fantasia #adaptacao #d1 #e3 #tenho-digital |
| Dinossauros! | Arthur C. Clarke | #F #ficcao-cientifica #antologia #contos #d1 #e2 #rel-asimov-clarke #tenho-digital |
| Doadores de Sono | Karen Russell | #F #ficcao-cientifica #distopia #d2 #e1 #tenho-digital |
| Doutor Destino | Christopher Cantwell e Salvador Larroca | #HQ #super-herois #d1 #e2 #tenho-digital |
| Doutor Estranho: Sina dos Sonhos | Devin Grayson | #F #super-herois #fantasia #d1 #e2 #tenho-digital |
| Dragões do Crepúsculo do Outono | Margaret Weis e Tracy Hickman | #F #fantasia #d1 #e2 #tenho-digital |
| Earthdivers | Stephen Graham Jones e Davide Gianfelice | #HQ #ficcao-cientifica #historia-alternativa #d1 #e2 #tenho-digital |
| Elantris | Brandon Sanderson | #F #fantasia #d1 #e3 #tenho-digital |
| Elfos | Vários autores | #HQ #fantasia #d1 #e3 #tenho-digital |
| Elric de Melniboné | Michael Moorcock | #F #fantasia #classico #d1 #e1 #tenho-digital |
| Elric: Stormbringer | Michael Moorcock e P. Craig Russell | #HQ #fantasia #adaptacao #d1 #e1 #tenho-digital |
| Encontro com Rama | Arthur C. Clarke | #F #ficcao-cientifica #classico #d2 #e1 #rel-asimov-clarke #tenho-digital |
| Era de Ultron | Brian Michael Bendis e Bryan Hitch | #HQ #super-herois #d1 #e2 #tenho-digital |
| Escória | Carlos Trillo e Juan Giménez | #HQ #ficcao-cientifica #distopia #latam #d1 #e1 #tenho-digital |
| Espada da Galáxia | Marcelo Cassaro | #F #ficcao-cientifica #BR #d1 #e2 #tenho-digital |
| Espadas e Bruxas | Esteban Maroto | #HQ #fantasia #d1 #e1 #tenho-digital |
| Especial: As Espadas | (autor não informado) | #HQ #fantasia #d1 #e1 #verificar #tenho-digital |
| Estação Perdido | China Miéville | #F #fantasia #ficcao-cientifica #d3 #e3 #tenho-digital |
| Estado Elétrico | Simon Stålenhag | #F #ficcao-cientifica #distopia #d1 #e1 #tenho-digital |
| Ex Machina | Brian K. Vaughan e Tony Harris | #HQ #super-herois #politica #d2 #e3 #tenho-digital |
| Fábulas | Bill Willingham e Mark Buckingham | #HQ #fantasia #d1 #e3 #tenho-digital |
| Febre Tifoide | Clay McLeod Chapman | #HQ #super-herois #d1 #e1 #tenho-digital |
| Ficção de Polpa: Aventura! | Samir Machado de Machado (org.) | #F #antologia #contos #aventura #BR #d1 #e2 #tenho-digital |
| Ficção de Polpa, vol. 1 | Samir Machado de Machado (org.) | #F #antologia #contos #ficcao-cientifica #horror #BR #d1 #e2 #tenho-digital |
| Filhos da Degradação | Felipe Castilho | #F #fantasia #BR #d1 #e2 #tenho-digital |
| Forward | Blake Crouch, N.K. Jemisin e Veronica Roth | #F #contos #ficcao-cientifica #antologia #d1 #e1 #tenho-digital |
| Fumaça e Espelhos | Neil Gaiman | #F #contos #fantasia #horror #d1 #e2 #tenho-digital |
| Galápagos | Kurt Vonnegut | #F #ficcao-cientifica #humor #d2 #e2 #tenho-digital |
| Gamora | Nicole Perlman e Marco Checchetto | #HQ #super-herois #ficcao-cientifica #d1 #e1 #tenho-digital |
| Gavião Arqueiro | Vários autores | #HQ #super-herois #d1 #e2 #tenho-digital |
| Grandes Astros: Batman | Scott Snyder e John Romita Jr. | #HQ #super-herois #d1 #e2 #tenho-digital |
| Grandes Clássicos DC | Vários autores | #HQ #super-herois #classico #d1 #e3 #tenho-digital |
| Groo | Sergio Aragonés e Mark Evanier | #HQ #fantasia #humor #d1 #e3 #tenho-digital |
| Guerra Civil II | Brian Michael Bendis e David Marquez | #HQ #super-herois #d1 #e2 #tenho-digital |
| Guerra do Velho | John Scalzi | #F #ficcao-cientifica #d1 #e2 #tenho-digital |
| Guerra dos Reis | Dan Abnett, Andy Lanning e Paul Pelletier | #HQ #super-herois #ficcao-cientifica #d1 #e2 #tenho-digital |
| Guerreiro Eterno | Vários autores | #HQ #super-herois #d1 #e2 #tenho-digital |
| Habitat | Simon Roy | #HQ #ficcao-cientifica #d1 #e1 #verificar #tenho-digital |
| Hawkmoon | Jérôme Le Gris, Benoît Dellac e Didier Poli | #HQ #fantasia #adaptacao #d1 #e1 #tenho-digital |
| Herdeiros do Tempo | Adrian Tchaikovsky | #F #ficcao-cientifica #d2 #e3 #tenho-digital |
| Heróis em Crise | Tom King e Clay Mann | #HQ #super-herois #d1 #e2 #tenho-digital |
| Heróis Renascem | Vários autores | #HQ #super-herois #d1 #e3 #tenho-digital |
| História do Universo Marvel | Mark Waid e Javier Rodríguez | #HQ #super-herois #d1 #e1 #tenho-digital |
| Holy Avenger | Marcelo Cassaro e Erica Awano | #HQ #fantasia #manga #BR #d1 #e3 #tenho-digital |
| Homem-Aranha: Entre Trovões | Christopher L. Bennett | #F #super-herois #d1 #e2 #tenho-digital |
| Horizonte Negro | Philippe Pelaez e Benjamin Blasco-Martinez | #HQ #ficcao-cientifica #d1 #e1 #tenho-digital |
| Império Secreto | Nick Spencer e outros | #HQ #super-herois #politica #d1 #e2 #tenho-digital |
| Incríveis X-Men (2025) | Jed MacKay e Mahmud Asrar | #HQ #super-herois #d1 #e2 #tenho-digital |
| Infinito | Jonathan Hickman | #HQ #super-herois #ficcao-cientifica #d2 #e2 #tenho-digital |
| Inumanos vs. X-Men | Charles Soule e Jeff Lemire | #HQ #super-herois #d1 #e2 #tenho-digital |
| Invasores de Corpos | Jack Finney | #F #ficcao-cientifica #horror #classico #d1 #e1 #tenho-digital |
| John Carpenter's Tales of Science Fiction | Vários autores | #HQ #ficcao-cientifica #horror #antologia #d1 #e2 #tenho-digital |
| Kallocaína | Karin Boye | #F #distopia #classico #d2 #e1 #tenho-digital |
| Kingsway Oeste | Greg Pak e Mirko Colak | #HQ #faroeste #fantasia #historia-alternativa #d1 #e1 #tenho-digital |
| Klarion | Vários autores | #HQ #super-herois #fantasia #d1 #e1 #tenho-digital |
| Kull: Exílio da Atlântida | Robert E. Howard | #F #fantasia #contos #classico #d1 #e2 #tenho-digital |
| Lago de Fogo | Nathan Fairbairn e Matt Smith | #HQ #ficcao-cientifica #medieval #d1 #e1 #tenho-digital |
| Lázaro, Dê um Passo à Frente | Ray Bradbury | #F #ficcao-cientifica #contos #classico #d1 #e1 #tenho-digital |
| Leito de Morte | Joshua Williamson e Riley Rossmo | #HQ #aventura #d1 #e1 #tenho-digital |
| Lone Sloane | Philippe Druillet | #HQ #ficcao-cientifica #classico #d2 #e1 #tenho-digital |
| Longshot Salva o Universo Marvel | Christopher Hastings e Jacopo Camagni | #HQ #super-herois #humor #d1 #e1 #tenho-digital |
| Lua de Sangue (Dreamblood, vol. 1) | N.K. Jemisin | #F #fantasia #d2 #e2 #tenho-digital |
| Lugar Nenhum (em quadrinhos) | Neil Gaiman, Mike Carey e Glenn Fabry | #HQ #fantasia #adaptacao #d1 #e2 #tenho-digital |
| Mago: Aprendiz | Raymond E. Feist | #F #fantasia #d1 #e2 #trilha-fantasia-de-folego #tenho-digital |
| Mago: Espinho de Prata | Raymond E. Feist | #F #fantasia #d1 #e2 #tenho-digital |
| Mago: Mestre | Raymond E. Feist | #F #fantasia #d1 #e2 #tenho-digital |
| Marvel Knights: X-Men | Brahm Revel | #HQ #super-herois #d1 #e1 #tenho-digital |
| Matéria Escura | Blake Crouch | #F #ficcao-cientifica #thriller #d1 #e2 #tenho-digital |
| Meia-Noite e Apolo | Steve Orlando e Fernando Blanco | #HQ #super-herois #d1 #e1 #tenho-digital |
| Merlin: A Profecia | M.K. Hume | #F #fantasia #medieval #romance-historico #d1 #e2 #tenho-digital |
| Mestre Gil de Ham | J.R.R. Tolkien | #F #fantasia #humor #classico #d1 #e1 #tenho-digital |
| Metropolis | Thea von Harbou | #F #ficcao-cientifica #distopia #classico #d2 #e2 #tenho-digital |
| Mona Lisa Overdrive | William Gibson | #F #ficcao-cientifica #d2 #e2 #tenho-digital |
| Morbius: O Vampiro Vivo | Vários autores | #HQ #super-herois #horror #d1 #e2 #tenho-digital |
| Motoqueiro Fantasma Cósmico | Donny Cates e Dylan Burnett | #HQ #super-herois #humor #d1 #e1 #tenho-digital |
| Mulheres Perigosas | George R.R. Martin e Gardner Dozois (orgs.) | #F #contos #fantasia #antologia #d1 #e3 #tenho-digital |
| Na Floresta | Erin Hunter | #F #fantasia #d1 #e2 #tenho-digital |
| Natureza Brutal | Luciano Saracino e Ariel Olivetti | #HQ #fantasia #d1 #e1 #tenho-digital |
| Nós, os Mortos | Darko Macan e Igor Kordey | #HQ #horror #historia-alternativa #d1 #e2 #tenho-digital |
| Nós Somos a Cidade (Grandes Cidades, vol. 1) | N.K. Jemisin | #F #fantasia #d2 #e2 #tenho-digital |
| Nova | Samuel R. Delany | #F #ficcao-cientifica #classico #d2 #e2 #tenho-digital |
| Nove Amanhãs | Isaac Asimov | #F #contos #ficcao-cientifica #classico #d1 #e1 #rel-asimov-clarke #tenho-digital |
| O Anel dos Sete Mundos | Giovanni Gualdoni, Gabriele Clima e Matteo Piana | #HQ #fantasia #d1 #e2 #tenho-digital |
| O Ano do Dilúvio | Margaret Atwood | #F #ficcao-cientifica #distopia #d2 #e2 #tenho-digital |
| O Assassino do Rei | Robin Hobb | #F #fantasia #d1 #e3 #tenho-digital |
| O Cair da Noite | Isaac Asimov | #F #ficcao-cientifica #classico #d1 #e2 #rel-asimov-clarke #tenho-digital |
| O Ceifador | Neal Shusterman | #F #ficcao-cientifica #distopia #d1 #e2 #tenho-digital |
| O Cerco | Brian Michael Bendis e Olivier Coipel | #HQ #super-herois #d1 #e1 #tenho-digital |
| O Céu de Pedra | N.K. Jemisin | #F #fantasia #ficcao-cientifica #d2 #e2 #tenho-digital |
| O Conto da Aia (em quadrinhos) | Margaret Atwood e Renée Nault | #HQ #distopia #adaptacao #genero #d1 #e1 #tenho-digital |
| O Conto de Zoe | John Scalzi | #F #ficcao-cientifica #d1 #e2 #tenho-digital |
| O Coração é o Último a Morrer | Margaret Atwood | #F #distopia #humor #d1 #e2 #tenho-digital |
| O Dia das Trífides | John Wyndham | #F #ficcao-cientifica #classico #d1 #e2 #tenho-digital |
| O Enigma de Andrômeda | Michael Crichton | #F #ficcao-cientifica #thriller #classico #d1 #e2 #tenho-digital |
| O Espadachim de Carvão | Affonso Solano | #F #fantasia #BR #d1 #e2 #tenho-digital |
| O Fim da Eternidade | Isaac Asimov | #F #ficcao-cientifica #classico #d2 #e1 #rel-asimov-clarke #tenho-digital |
| O Fim da Morte | Cixin Liu | #F #ficcao-cientifica #asia #d3 #e3 #tenho-digital |
| O Fim de Todas as Coisas | John Scalzi | #F #ficcao-cientifica #d1 #e2 #tenho-digital |
| O Grande Silêncio e Outras Histórias | Ted Chiang | #F #contos #ficcao-cientifica #d2 #e1 #tenho-digital |
| O Império Final (Mistborn, vol. 1) | Brandon Sanderson | #F #fantasia #d1 #e3 #trilha-fantasia-de-folego #tenho-digital |
| O Incal Negro (O Incal, vol. 1) | Alejandro Jodorowsky e Moebius | #HQ #ficcao-cientifica #classico #d2 #e1 #tenho-digital |
| O Inimigo do Mundo (Trilogia da Tormenta, vol. 1) | Leonel Caldela | #F #fantasia #BR #d1 #e3 #tenho-digital |
| O Livro do Silêncio (Deuses de Dois Mundos, vol. 1) | P.J. Pereira | #F #fantasia #religiao #BR #d1 #e2 #tenho-digital |
| O Livro e a Espada | Antoine Rouaud | #F #fantasia #d1 #e2 #tenho-digital |
| O Longo Amanhã | Leigh Brackett | #F #ficcao-cientifica #distopia #classico #d1 #e1 #tenho-digital |
| O Macaco e a Essência | Aldous Huxley | #F #distopia #classico #d2 #e1 #tenho-digital |
| O Manual do Mago Frugal para Sobrevivência na Inglaterra Medieval | Brandon Sanderson | #F #fantasia #humor #d1 #e2 #tenho-digital |
| O Mundo de Rocannon | Ursula K. Le Guin | #F #ficcao-cientifica #classico #d1 #e1 #tenho-digital |
| O Navio Arcano | Robin Hobb | #F #fantasia #d1 #e3 #tenho-digital |
| O Outro Vento | Ursula K. Le Guin | #F #fantasia #d1 #e2 #tenho-digital |
| O Poço da Ascensão (Mistborn, vol. 2) | Brandon Sanderson | #F #fantasia #d1 #e3 #tenho-digital |
| O Portão do Obelisco | N.K. Jemisin | #F #fantasia #ficcao-cientifica #d2 #e2 #tenho-digital |
| O Príncipe de Westeros e Outras Histórias | George R.R. Martin e Gardner Dozois (orgs.) | #F #fantasia #antologia #contos #d1 #e3 #tenho-digital |
| O Próprio Medo | Matt Fraction e Stuart Immonen | #HQ #super-herois #d1 #e2 #tenho-digital |
| O Sentinela | Vários autores | #HQ #super-herois #d1 #e2 #tenho-digital |
| O Sol Desvelado | Isaac Asimov | #F #ficcao-cientifica #misterio #classico #d1 #e2 #rel-asimov-clarke #tenho-digital |
| O Temor do Sábio | Patrick Rothfuss | #F #fantasia #d2 #e3 #tenho-digital |
| O Timbre | Neal Shusterman | #F #ficcao-cientifica #distopia #d1 #e3 #tenho-digital |
| O Túmulo do Batman | Warren Ellis e Bryan Hitch | #HQ #super-herois #d1 #e2 #tenho-digital |
| O Último Deus | Phillip Kennedy Johnson e Riccardo Federici | #HQ #fantasia #d1 #e2 #tenho-digital |
| Ogiva | Bruno Zago e Guilherme Petreca | #HQ #ficcao-cientifica #BR #d1 #e1 #tenho-digital |
| Oryx e Crake | Margaret Atwood | #F #ficcao-cientifica #distopia #d2 #e2 #tenho-digital |
| Os Braceletes da Perdição (Mistborn: Segunda Era, vol. 3) | Brandon Sanderson | #F #fantasia #d1 #e2 #tenho-digital |
| Os Cem Mil Reinos (Trilogia Legado, vol. 1) | N.K. Jemisin | #F #fantasia #d1 #e2 #tenho-digital |
| Os Fabulosos X-Men | Vários autores | #HQ #super-herois #d1 #e2 #tenho-digital |
| Os Futuros de Liu Cixin | Liu Cixin e outros | #HQ #ficcao-cientifica #adaptacao #asia #d1 #e3 #tenho-digital |
| Os Invisíveis | Grant Morrison | #HQ #ficcao-cientifica #fantasia #d3 #e3 #tenho-digital |
| Os Pequenos Guardiões | David Petersen | #HQ #fantasia #aventura #d1 #e2 #tenho-digital |
| Os Reinos Partidos (Trilogia Legado, vol. 2) | N.K. Jemisin | #F #fantasia #d1 #e2 #tenho-digital |
| Patrulha do Destino | Vários autores | #HQ #super-herois #d2 #e3 #tenho-digital |
| Periféricos | William Gibson | #F #ficcao-cientifica #d3 #e2 #tenho-digital |
| Pines | Blake Crouch | #F #ficcao-cientifica #thriller #misterio #d1 #e2 #tenho-digital |
| Poeira Lunar | Arthur C. Clarke | #F #ficcao-cientifica #classico #d1 #e2 #rel-asimov-clarke #tenho-digital |
| Por Deus ou pelo Acaso | Becky Cloonan | #HQ #fantasia #horror #medieval #d1 #e1 #tenho-digital |
| Porto da Terra | Zack Kaplan e Andrea Mutti | #HQ #ficcao-cientifica #d1 #e2 #tenho-digital |
| Prince of Thorns | Mark Lawrence | #F #fantasia #d1 #e2 #tenho-digital |
| Protocolo Rebelde | Martha Wells | #F #ficcao-cientifica #d1 #e1 #tenho-digital |
| Quarteto Fantástico | Vários autores | #HQ #super-herois #d1 #e3 #tenho-digital |
| Rapa Nui | Mikaël e Fabrizio Russo | #HQ #aventura #historia #d1 #e1 #tenho-digital |
| Reconhecimento de Padrões | William Gibson | #F #ficcao-cientifica #thriller #d2 #e2 #tenho-digital |
| Recursão | Blake Crouch | #F #ficcao-cientifica #thriller #d1 #e2 #tenho-digital |
| Rei Conan: Lobos Além da Fronteira | Timothy Truman e Tomás Giorello | #HQ #fantasia #d1 #e1 #tenho-digital |
| Reino do Amanhã | Mark Waid e Alex Ross | #HQ #super-herois #classico #d2 #e1 #tenho-digital |
| Renascimento | Fred Duval e Emem | #HQ #ficcao-cientifica #d1 #e2 #tenho-digital |
| Ronin | Frank Miller | #HQ #ficcao-cientifica #classico #d2 #e2 #tenho-digital |
| Saga | Brian K. Vaughan e Fiona Staples | #HQ #ficcao-cientifica #fantasia #d1 #e3 #tenho-digital |
| Saída Estratégica | Martha Wells | #F #ficcao-cientifica #d1 #e1 #tenho-digital |
| Sandman | Neil Gaiman | #HQ #fantasia #horror #mitologia #classico #d2 #e3 #trilha-quadrinhos-para-gente-grande #tenho-digital |
| Santuário dos Ventos | George R.R. Martin | #F #fantasia #ficcao-cientifica #d1 #e2 #tenho-digital |
| Self/Made | Mathieu Groux e Eduardo Ferigato | #HQ #ficcao-cientifica #fantasia #d1 #e1 #tenho-digital |
| Senhor da Luz | Roger Zelazny | #F #ficcao-cientifica #fantasia #classico #d3 #e2 #tenho-digital |
| Senhor das Estrelas | Vários autores | #HQ #super-herois #ficcao-cientifica #d1 #e2 #tenho-digital |
| Seres Mágicos e Histórias Sombrias | Neil Gaiman (org.) | #F #contos #fantasia #antologia #d1 #e2 #tenho-digital |
| Sheltered | Ed Brisson e Johnnie Christmas | #HQ #thriller #distopia #d1 #e2 #tenho-digital |
| Siegfried | Alex Alice | #HQ #fantasia #mitologia #d1 #e2 #tenho-digital |
| SilverHawks | Ed Brisson e George Kambadais | #HQ #ficcao-cientifica #super-herois #d1 #e2 #tenho-digital |
| Skinbreaker | Robert Kirkman e David Finch | #HQ #fantasia #d1 #e2 #tenho-digital |
| Skulldigger e o Garoto Esqueleto | Jeff Lemire e Tonci Zonjic | #HQ #super-herois #policial #d1 #e1 #tenho-digital |
| Snow Crash | Neal Stephenson | #F #ficcao-cientifica #classico #d2 #e3 #tenho-digital |
| Solomon Kane | Robert E. Howard | #F #fantasia #horror #contos #classico #d1 #e2 #tenho-digital |
| Sombras do Sol (Dreamblood, vol. 2) | N.K. Jemisin | #F #fantasia #d2 #e2 #tenho-digital |
| Sonhos Elétricos | Philip K. Dick | #F #ficcao-cientifica #contos #d2 #e2 #tenho-digital |
| Spawn: The Dark Ages | Brian Holguin e Liam Sharp | #HQ #horror #medieval #fantasia #d1 #e2 #tenho-digital |
| Star Wars: Dívida de Honra | Chuck Wendig | #F #ficcao-cientifica #d1 #e2 #tenho-digital |
| Star Wars: Marcas da Guerra | Chuck Wendig | #F #ficcao-cientifica #d1 #e2 #tenho-digital |
| Superman vs. Apocalypse | Vários autores | #HQ #super-herois #d1 #e2 #tenho-digital |
| Surfista Prateado: Os Escravistas (Graphic Marvel, vol. 14) | Stan Lee e Keith Pollard | #HQ #super-herois #ficcao-cientifica #d1 #e1 #tenho-digital |
| Sword of Ages | Gabriel Rodríguez | #HQ #fantasia #d1 #e1 #tenho-digital |
| Tartarugas Ninja: O Último Ronin | Kevin Eastman, Peter Laird e Tom Waltz | #HQ #super-herois #aventura #d1 #e2 #tenho-digital |
| Tartarugas Ninja: O Último Ronin – Anos Perdidos | Kevin Eastman, Tom Waltz e S.L. Gallant | #HQ #super-herois #aventura #d1 #e1 #tenho-digital |
| Tehanu | Ursula K. Le Guin | #F #fantasia #classico #d1 #e1 #tenho-digital |
| Terra Proibida | Denis-Pierre Filippi e Patrick Laumond | #HQ #fantasia #d1 #e1 #tenho-digital |
| Território Fantasma | William Gibson | #F #ficcao-cientifica #thriller #d2 #e2 #tenho-digital |
| Thanos: Em Busca de Poder / Legado | Vários autores | #HQ #super-herois #d1 #e2 #tenho-digital |
| Thanos II | Vários autores | #HQ #super-herois #d1 #e2 #tenho-digital |
| The Realm | Seth M. Peck e Jeremy Haun | #HQ #fantasia #d1 #e2 #tenho-digital |
| Thor | Vários autores | #HQ #super-herois #mitologia #d1 #e3 #tenho-digital |
| Thor, vol. 5 | Jason Aaron e Mike del Mundo | #HQ #super-herois #mitologia #d1 #e1 #tenho-digital |
| Tokyo Ghost | Rick Remender e Sean Murphy | #HQ #ficcao-cientifica #distopia #d1 #e2 #tenho-digital |
| Tormenta de Fogo | Brandon Sanderson | #F #ficcao-cientifica #super-herois #d1 #e2 #tenho-digital |
| Torneio dos Campeões | Vários autores | #HQ #super-herois #d1 #e1 #tenho-digital |
| Transmetropolitan | Warren Ellis e Darick Robertson | #HQ #ficcao-cientifica #politica #humor #d2 #e3 #tenho-digital |
| Trilogia da Fundação (box: Fundação · Fundação e Império · Segunda Fundação) | Isaac Asimov | #F #ficcao-cientifica #classico #d2 #e3 #rel-asimov-clarke #tenho-digital |
| Trilogia do Sprawl (box: Neuromancer · Count Zero · Mona Lisa Overdrive) | William Gibson | #F #ficcao-cientifica #classico #d2 #e3 #tenho-digital |
| Trilogia dos Guardiões: Volume Único | I.M. Martins | #F #fantasia #BR #d1 #e3 #tenho-digital |
| Um Cântico para Leibowitz | Walter M. Miller Jr. | #F #ficcao-cientifica #distopia #religiao #classico #d2 #e2 #tenho-digital |
| Um Conto às Avessas de A Bela e a Fera | Liz Braswell | #F #fantasia #d1 #e2 #tenho-digital |
| Um Planeta Chamado Traição | Orson Scott Card | #F #ficcao-cientifica #d1 #e2 #tenho-digital |
| Uma Desolação Chamada Paz | Arkady Martine | #F #ficcao-cientifica #d2 #e2 #tenho-digital |
| Uma Lembrança Chamada Império | Arkady Martine | #F #ficcao-cientifica #d2 #e2 #tenho-digital |
| Utopia | Thomas More | #F #utopia #filosofia #politica #classico #d2 #e1 #tenho-digital |
| V de Vingança | Alan Moore e David Lloyd | #HQ #distopia #politica #classico #d2 #e2 #trilha-quadrinhos-para-gente-grande #tenho-digital |
| Vencer o Dragão | Barbara Hambly | #F #fantasia #d1 #e2 #tenho-digital |
| Viagem ao Centro da Terra (em quadrinhos) | Júlio Verne | #HQ #adaptacao #ficcao-cientifica #aventura #classico #d1 #e1 #tenho-digital |
| Viagem Fantástica | Isaac Asimov | #F #ficcao-cientifica #classico #d1 #e2 #rel-asimov-clarke #tenho-digital |
| Vilão Iniciante | John Scalzi | #F #ficcao-cientifica #humor #d1 #e2 #tenho-digital |
| Vingadores (2017) | Vários autores | #HQ #super-herois #d1 #e3 #tenho-digital |
| Vingadores: Sem Rumo | Al Ewing, Jim Zub e Mark Waid | #HQ #super-herois #d1 #e2 #tenho-digital |
| Vingadores: Todos Querem Dominar o Mundo | Dan Abnett | #F #super-herois #d1 #e2 #tenho-digital |
| Vingadores vs. X-Men | Vários autores | #HQ #super-herois #d1 #e2 #tenho-digital |
| Vingadores vs. X-Men: Consequências | Kieron Gillen | #HQ #super-herois #d1 #e1 #tenho-digital |
| Walden II: Uma Sociedade do Futuro | B.F. Skinner | #F #behaviorismo #utopia #classico #d2 #e2 #tenho-digital |
| Watchmen | Alan Moore e Dave Gibbons | #HQ #super-herois #politica #classico #d3 #e2 #trilha-quadrinhos-para-gente-grande #tenho-digital |
| Wayne de Gotham | Tracy Hickman | #F #super-herois #d1 #e2 #tenho-digital |
| Wild Cards: O Começo de Tudo | George R.R. Martin (org.) | #F #contos #ficcao-cientifica #super-herois #antologia #d1 #e2 #tenho-digital |
| WildC.A.T.s/X-Men | Vários autores | #HQ #super-herois #d1 #e1 #tenho-digital |
| Wolverine: Arma X | Marc Cerasini | #F #super-herois #d1 #e2 #tenho-digital |
| Wolverine: Inimigo do Estado | Mark Millar e John Romita Jr. | #HQ #super-herois #d1 #e2 #tenho-digital |
| X-Men: Massacre | Vários autores | #HQ #super-herois #d1 #e3 #tenho-digital |
| X-Men: Programa de Extermínio | Chris Claremont, Louise Simonson e Jim Lee | #HQ #super-herois #d1 #e2 #tenho-digital |
| Y: O Último Homem | Brian K. Vaughan e Pia Guerra | #HQ #ficcao-cientifica #distopia #genero #d1 #e3 #tenho-digital |

### 17.3 Clássicos universais e romances de ideias

| Título | Autor | Tags |
|---|---|---|
| A Arte de Amar | Ovídio | #F #roma #antiguidade #classico #d2 #e1 #tenho-digital |
| A Briga dos Dois Ivans | Nikolai Gógol | #F #classico #d1 #e1 #tenho-digital |
| A História de uma Mãe | Peter Madsen | #HQ #adaptacao #fantasia #classico #d1 #e1 #tenho-digital |
| A Ilha do Tesouro (em quadrinhos) | Robert Louis Stevenson | #HQ #adaptacao #aventura #classico #d1 #e1 #tenho-digital |
| A Mandrágora | Nicolau Maquiavel | #F #teatro #renascimento #humor #classico #d1 #e1 #tenho-digital |
| A Nascente | Ayn Rand | #F #filosofia #politica #d2 #e3 #tenho-digital |
| A Odisseia (em quadrinhos) | Homero | #HQ #adaptacao #antiguidade #mitologia #classico #d1 #e1 #tenho-digital |
| A Revolta de Atlas | Ayn Rand | #F #filosofia #politica #distopia #classico #d2 #e3 #tenho-digital |
| A Sabedoria dos Mitos: Afrodite | Luc Ferry e Clotilde Bruneau | #HQ #mitologia #antiguidade #adaptacao #d1 #e1 #tenho-digital |
| A Submissa e Outras Histórias | Fiódor Dostoiévski | #F #contos #classico #d2 #e1 #tenho-digital |
| A Tempestade (Shakespeare em Quadrinhos, vol. 4) | William Shakespeare, Lillo Parra e Jefferson Costa | #HQ #adaptacao #teatro #classico #BR #d1 #e1 #tenho-digital |
| A Volta ao Mundo em 80 Dias (em quadrinhos) | Júlio Verne | #HQ #adaptacao #aventura #classico #d1 #e1 #tenho-digital |
| Beowulf | Santiago García e David Rubín | #HQ #adaptacao #medieval #fantasia #classico #d1 #e1 #tenho-digital |
| Bola de Sebo e Outros Contos | Guy de Maupassant | #F #contos #classico #d1 #e1 #tenho-digital |
| Contos | Ernest Hemingway | #F #contos #classico #d2 #e3 #tenho-digital |
| Contos Completos | Liev Tolstói | #F #contos #classico #d2 #e3 #tenho-digital |
| Contos Escolhidos | Aldous Huxley | #F #contos #classico #d2 #e2 #tenho-digital |
| Contos Reunidos | Vladimir Nabokov | #F #contos #classico #d3 #e3 #tenho-digital |
| Contraponto | Aldous Huxley | #F #classico #d3 #e3 #tenho-digital |
| Diário de um Escritor: Meia Carta de um Sujeito | Fiódor Dostoiévski | #F #classico #d2 #e1 #tenho-digital |
| Duas Narrativas Fantásticas | Fiódor Dostoiévski | #F #contos #fantasia #classico #d2 #e1 #tenho-digital |
| Epopeia de Gilgamesh | Sin-léqi-unnínni | #F #antiguidade #mitologia #poesia #classico #d2 #e1 #tenho-digital |
| Essencial Franz Kafka | Franz Kafka | #F #contos #classico #d2 #e2 #tenho-digital |
| Folhas Inúteis | Aldous Huxley | #F #classico #d2 #e2 #tenho-digital |
| Fuga sem Fim | Joseph Roth | #F #classico #d2 #e1 #tenho-digital |
| Gente Pobre | Fiódor Dostoiévski | #F #classico #d2 #e1 #tenho-digital |
| Hamlet (Shakespeare em Quadrinhos) | William Shakespeare, Wellington Srbek e Alex Shibao | #HQ #adaptacao #teatro #classico #BR #d1 #e1 #tenho-digital |
| Mar de Histórias: Antologia do Conto Mundial, vol. 1: Das Origens à Idade Média | Aurélio Buarque de Holanda Ferreira e Paulo Rónai | #F #contos #antologia #classico #d2 #e2 #tenho-digital |
| Moby Dick (em quadrinhos) | Christophe Chabouté | #HQ #adaptacao #aventura #classico #d1 #e2 #tenho-digital |
| Noites Brancas | Fiódor Dostoiévski | #F #classico #d1 #e1 #tenho-digital |
| Nova Antologia do Conto Russo | Bruno Barretto Gomide (org.) | #F #contos #antologia #classico #d2 #e3 #tenho-digital |
| O Diabo | Liev Tolstói | #F #classico #d2 #e1 #tenho-digital |
| O Inferno de Dante | Paul Brizzi e Gaëtan Brizzi | #HQ #adaptacao #religiao #classico #d2 #e1 #tenho-digital |
| O Ladrão Honesto e Outras Histórias | Fiódor Dostoiévski | #F #contos #classico #d2 #e1 #tenho-digital |
| O Retrato | Nikolai Gógol | #F #contos #classico #d2 #e1 #tenho-digital |
| Os Sofrimentos do Jovem Werther | Johann W. von Goethe | #F #classico #d2 #e1 #tenho-digital |
| Pais e Filhos | Ivan Turguêniev | #F #classico #d2 #e2 #tenho-digital |
| Paraísos Artificiais | Charles Baudelaire | #NF #classico #d2 #e1 #tenho-digital |
| Rashômon e Outros Contos | Ryunosuke Akutagawa | #F #contos #classico #asia #d2 #e1 #tenho-digital |
| Rei Arthur e os Cavaleiros da Távola Redonda: Edição Comentada e Ilustrada | Howard Pyle | #F #fantasia #medieval #aventura #classico #d1 #e2 #tenho-digital |
| Sonho de uma Noite de Verão (Shakespeare em Quadrinhos) | William Shakespeare, Lillo Parra e Wanderson de Souza | #HQ #adaptacao #teatro #humor #classico #BR #d1 #e1 #tenho-digital |

### 17.4 América Latina, Brasil e lusofonia (ficção)

| Título | Autor | Tags |
|---|---|---|
| 108 Textos | Clarice Lispector | #F #cronicas #BR #d2 #e2 #tenho-digital |
| 2666 | Roberto Bolaño | #F #contemporaneo #latam #d3 #e3 #tenho-digital |
| 50 Contos de Machado de Assis | Machado de Assis | #F #contos #classico #BR #d2 #e3 #tenho-digital |
| 70 Historinhas | Carlos Drummond de Andrade | #F #cronicas #humor #BR #d1 #e1 #tenho-digital |
| A Bagagem do Viajante | José Saramago | #F #cronicas #portugal #d2 #e2 #tenho-digital |
| A Cartomante (Literatura Brasileira em Quadrinhos, vol. 4) | Machado de Assis e Jô Fevereiro | #HQ #adaptacao #classico #BR #d1 #e1 #tenho-digital |
| A Causa Secreta e Outros Contos | Machado de Assis | #F #contos #horror #classico #BR #d2 #e1 #tenho-digital |
| A Cegueira do Rio | Mia Couto | #F #contos #africa #d2 #e1 #tenho-digital |
| A Confissão da Leoa | Mia Couto | #F #contemporaneo #africa #d2 #e1 #tenho-digital |
| A Extraordinária Zona Norte | Alberto Mussa | #F #contos #BR #d2 #e1 #tenho-digital |
| A Face Oculta | Moacyr Scliar | #F #contos #BR #RS #d1 #e1 #tenho-digital |
| A Hora da Estrela | Clarice Lispector | #F #classico #BR #d2 #e1 #tenho-digital |
| A Hora do Diabo e Outros Contos | Fernando Pessoa | #F #contos #classico #portugal #d2 #e1 #tenho-digital |
| A Menina sem Palavra | Mia Couto | #F #contos #africa #d1 #e1 #tenho-digital |
| Acerto de Contas: Treze Histórias de Crime e Nova Literatura Latino-Americana | Daniel Galera e outros | #F #contos #policial #antologia #latam #d2 #e2 #tenho-digital |
| Agora é que São Elas | Paulo Leminski | #F #BR #d2 #e1 #tenho-digital |
| Agosto | Rubem Fonseca | #F #policial #romance-historico #BR #d2 #e2 #trilha-crime-a-brasileira #tenho-digital |
| Alguém que Anda por Aí | Julio Cortázar | #F #contos #latam #d2 #e1 #tenho-digital |
| Amálgama | Rubem Fonseca | #F #contos #policial #BR #d2 #e1 #tenho-digital |
| Andarilhos | R. Tavares | #F #contos #BR #d1 #e1 #tenho-digital |
| As Armas Secretas | Julio Cortázar | #F #contos #latam #d2 #e1 #tenho-digital |
| As Cem Melhores Crônicas Brasileiras | Joaquim Ferreira dos Santos (org.) | #F #cronicas #antologia #BR #d1 #e2 #tenho-digital |
| Bestiário | Julio Cortázar | #F #contos #fantasia #latam #d2 #e1 #tenho-digital |
| Canção para Ninar Menino Grande | Conceição Evaristo | #F #contos #raca #BR #d2 #e1 #tenho-digital |
| Caviar é uma Ova | Gregorio Duvivier | #F #cronicas #humor #BR #d1 #e1 #tenho-digital |
| Contos Completos | José Donoso | #F #contos #latam #d2 #e3 #tenho-digital |
| Contos do Nascer da Terra | Mia Couto | #F #contos #africa #d2 #e1 #tenho-digital |
| Crônicas de Bustos Domecq / Novos Contos de Bustos Domecq | Jorge Luis Borges e Adolfo Bioy Casares | #F #contos #humor #policial #latam #d2 #e2 #tenho-digital |
| Daytripper | Fábio Moon e Gabriel Bá | #HQ #morte #BR #d1 #e2 #trilha-quadrinhos-para-gente-grande #tenho-digital |
| De Onde Eles Vêm | Jeferson Tenório | #F #raca #contemporaneo #BR #RS #d1 #e1 #trilha-porto-alegre-hoje #tenho-digital |
| Dois Mortos e a Morte e Outras Histórias | Tanto Tupiassu | #F #contos #BR #d1 #e1 #tenho-digital |
| Doramar ou a Odisseia: Histórias | Itamar Vieira Junior | #F #contos #BR #d2 #e1 #tenho-digital |
| Doze Contos Peregrinos | Gabriel García Márquez | #F #contos #latam #d2 #e1 #tenho-digital |
| Enquanto a Noite Não Chega | Josué Guimarães | #F #contemporaneo #BR #RS #d1 #e1 #tenho-digital |
| Essa História Está Diferente | Ronaldo Bressane (org.) | #F #contos #antologia #BR #d1 #e1 #tenho-digital |
| Feliz Ano Velho | Marcelo Rubens Paiva | #NF #biografia #testemunho #contemporaneo #BR #d1 #e1 #tenho-digital |
| Ficções Amazônicas | Aparecida Vilaça e Francisco Vilaça Gaspar | #F #contos #antropologia #BR #d2 #e1 #tenho-digital |
| História Universal da Infâmia | Jorge Luis Borges | #F #contos #classico #latam #d2 #e1 #trilha-labirintos-de-borges #tenho-digital |
| Histórias da Meia-Noite | Machado de Assis | #F #contos #classico #BR #d2 #e1 #tenho-digital |
| Histórias de Cronópios e de Famas | Julio Cortázar | #F #contos #humor #latam #d2 #e1 #tenho-digital |
| Krakatoa | Veronica Stigger | #F #contemporaneo #BR #d2 #e1 #tenho-digital |
| Levantado do Chão | José Saramago | #F #contemporaneo #portugal #d3 #e2 #tenho-digital |
| Lituma nos Andes | Mario Vargas Llosa | #F #contemporaneo #latam #d2 #e2 #tenho-digital |
| Livro de Sonhos | Jorge Luis Borges | #F #contos #antologia #latam #d2 #e1 #trilha-labirintos-de-borges #tenho-digital |
| Louco: Fuga (Graphic MSP) | Rogério Coelho | #HQ #BR #d1 #e1 #tenho-digital |
| Luzes de Niterói | Marcello Quintanilha | #HQ #BR #d1 #e2 #tenho-digital |
| Manual Prático do Ódio | Ferréz | #F #BR #d1 #e2 #tenho-digital |
| Memórias de Minhas Putas Tristes | Gabriel García Márquez | #F #contemporaneo #latam #d1 #e1 #tenho-digital |
| Memórias Póstumas de Brás Cubas (Literatura Brasileira em Quadrinhos, vol. 2) | Machado de Assis, Maria Sonia Barbosa e Sebastião Seabra | #HQ #adaptacao #classico #BR #d1 #e1 #tenho-digital |
| Nihonjin | Oscar Nakasato | #F #romance-historico #BR #d1 #e1 #tenho-digital |
| Noturno do Chile | Roberto Bolaño | #F #contemporaneo #latam #d2 #e1 #tenho-digital |
| O Beijo no Asfalto (em quadrinhos) | Nelson Rodrigues, Arnaldo Branco e Gabriel Góes | #HQ #adaptacao #teatro #BR #d1 #e1 #tenho-digital |
| O Buraco na Parede | Rubem Fonseca | #F #contos #BR #d2 #e1 #tenho-digital |
| O Cobrador | Rubem Fonseca | #F #contos #policial #BR #d2 #e1 #trilha-crime-a-brasileira #tenho-digital |
| O Conto da Ilha Desconhecida | José Saramago | #F #contos #portugal #d1 #e1 #tenho-digital |
| O Falador | Mario Vargas Llosa | #F #contemporaneo #latam #d2 #e1 #tenho-digital |
| O Fazedor | Jorge Luis Borges | #F #contos #poesia #classico #latam #d3 #e1 #trilha-labirintos-de-borges #tenho-digital |
| O Gaúcho | José de Alencar | #F #regional-gaucho #classico #BR #RS #d2 #e2 #tenho-digital |
| O Inconsciente Corporativo e Outros Contos | Vinícius Portella | #F #contos #BR #d2 #e1 #tenho-digital |
| O Livro dos Abraços | Eduardo Galeano | #F #cronicas #latam #d1 #e2 #tenho-digital |
| O Livro dos Seres Imaginários | Jorge Luis Borges | #F #contos #fantasia #latam #d2 #e1 #trilha-labirintos-de-borges #tenho-digital |
| O Melhor de Rubem Fonseca | Rubem Fonseca | #F #contos #policial #BR #d2 #e2 #tenho-digital |
| O Ouro dos Tigres | Jorge Luis Borges | #poesia #latam #d3 #e1 #tenho-digital |
| O Outro, o Mesmo | Jorge Luis Borges | #poesia #classico #latam #d3 #e1 #tenho-digital |
| O Triste Fim de Policarpo Quaresma (Literatura Brasileira em Quadrinhos, vol. 1) | Lima Barreto, Ronaldo Antonelli e Francisco Vilachã | #HQ #adaptacao #classico #BR #d1 #e1 #tenho-digital |
| Os Cem Melhores Contos Brasileiros do Século | Italo Moriconi (org.) | #F #contos #antologia #BR #d2 #e3 #tenho-digital |
| Os Chefes / Os Filhotes | Mario Vargas Llosa | #F #contos #latam #d2 #e1 #tenho-digital |
| Os Conjurados | Jorge Luis Borges | #poesia #latam #d3 #e1 #tenho-digital |
| Os Dragões Não Conhecem o Paraíso | Caio Fernando Abreu | #F #contos #BR #RS #d2 #e1 #trilha-porto-alegre-hoje #tenho-digital |
| Os Prisioneiros | Rubem Fonseca | #F #contos #BR #d2 #e1 #tenho-digital |
| Pai, Pai | João Silvério Trevisan | #NF #biografia #testemunho #BR #d2 #e1 #tenho-digital |
| Pássaros na Boca e Sete Casas Vazias: Contos Reunidos | Samanta Schweblin | #F #contos #horror #latam #d2 #e2 #tenho-digital |
| Penadinho: Vida (Graphic MSP) | Paulo Crumbim e Cristina Eiko | #HQ #BR #d1 #e1 #tenho-digital |
| Pequenas Criaturas | Rubem Fonseca | #F #contos #BR #d2 #e2 #tenho-digital |
| Percatempos: Tudo que Faço Quando Não Sei o que Fazer | Gregorio Duvivier | #F #humor #poesia #BR #d1 #e1 #tenho-digital |
| Quincas Borba (em quadrinhos) | Machado de Assis | #HQ #adaptacao #classico #BR #d1 #e1 #tenho-digital |
| Rinha de Galos | María Fernanda Ampuero | #F #contos #latam #d2 #e1 #tenho-digital |
| Romance Negro | Rubem Fonseca | #F #policial #contos #BR #d2 #e1 #tenho-digital |
| Salvar o Fogo | Itamar Vieira Junior | #F #contemporaneo #BR #d2 #e2 #tenho-digital |
| Sete Monstros Brasileiros | Braulio Tavares | #F #contos #fantasia #horror #BR #d1 #e1 #tenho-digital |
| Talco de Vidro | Marcello Quintanilha | #HQ #BR #d2 #e1 #tenho-digital |
| Todos os Contos | Clarice Lispector | #F #contos #classico #BR #d3 #e3 #tenho-digital |
| Todos os Contos de Machado de Assis (box) | Machado de Assis | #F #contos #classico #BR #d2 #e3 #tenho-digital |
| Tudo é Rio | Carla Madeira | #F #contemporaneo #BR #d1 #e1 #tenho-digital |
| Tungstênio | Marcello Quintanilha | #HQ #policial #BR #d2 #e1 #trilha-quadrinhos-para-gente-grande #tenho-digital |
| Um Rio Chamado Tempo, uma Casa Chamada Terra | Mia Couto | #F #africa #d2 #e1 #tenho-digital |
| Um Sonho de Três Noites | Tiago Cabral | #F #contos #BR #d1 #e1 #tenho-digital |
| Vagamundo | Eduardo Galeano | #F #contos #latam #d1 #e1 #tenho-digital |
| Venenos de Deus, Remédios do Diabo | Mia Couto | #F #africa #d2 #e1 #tenho-digital |

### 17.5 Ficção contemporânea e mundial

| Título | Autor | Tags |
|---|---|---|
| 1Q84, vol. 1 | Haruki Murakami | #F #fantasia #contemporaneo #asia #d2 #e2 #tenho-digital |
| 20 Contos de Truman Capote | Truman Capote | #F #contos #classico #d2 #e2 #tenho-digital |
| A Chegada | Shaun Tan | #HQ #fantasia #d1 #e1 #trilha-quadrinhos-para-gente-grande #tenho-digital |
| A Dissociação | Nadia Yala Kisukidi | #F #contemporaneo #africa #d2 #e2 #tenho-digital |
| A Espera | Keum Suk Gendry-Kim | #HQ #guerra #historia #asia #d1 #e1 #tenho-digital |
| A Extraordinária Cozinha dos Livros | Kim Jee-Hye | #F #contemporaneo #asia #d1 #e2 #tenho-digital |
| A Fábrica | Hiroko Oyamada | #F #contemporaneo #asia #d2 #e1 #tenho-digital |
| A Inconveniente Loja de Conveniência | Kim Ho-yeon | #F #contemporaneo #asia #d1 #e2 #tenho-digital |
| A Mulher Mais Linda da Cidade | Charles Bukowski | #F #contos #d1 #e2 #tenho-digital |
| A Obsolescência Programada dos Nossos Sentimentos | Zidrou e Aimée de Jongh | #HQ #d1 #e1 #tenho-digital |
| A Papelaria Tsubaki | Ito Ogawa | #F #contemporaneo #asia #d1 #e2 #tenho-digital |
| A Vida | (autor não informado) | #HQ #d1 #e1 #verificar #tenho-digital |
| Ao Sul de Lugar Nenhum | Charles Bukowski | #F #contos #contemporaneo #d1 #e1 #tenho-digital |
| Atos Humanos | Han Kang | #F #testemunho #contemporaneo #asia #d2 #e1 #tenho-digital |
| Baratas | Scholastique Mukasonga | #NF #testemunho #biografia #contemporaneo #africa #d2 #e1 #tenho-digital |
| Blackbird | Pierre Maurel | #HQ #contemporaneo #d1 #e1 #tenho-digital |
| Caçando Carneiros | Haruki Murakami | #F #contemporaneo #asia #d2 #e2 #tenho-digital |
| Cidades da Planície | Cormac McCarthy | #F #faroeste #contemporaneo #d2 #e2 #tenho-digital |
| Conto de Areia | Jim Henson, Jerry Juhl e Ramón K. Pérez | #HQ #fantasia #aventura #d1 #e1 #tenho-digital |
| Cores Vivas | Patrice Lawrence | #F #contemporaneo #d1 #e2 #tenho-digital |
| Deus em Pessoa | Marc-Antoine Mathieu | #HQ #religiao #humor #filosofia #d2 #e1 #tenho-digital |
| Divertida Mente: Conduzida pelas Emoções | Elise Allen | #F #d1 #e1 #tenho-digital |
| Homens sem Mulheres | Haruki Murakami | #F #contos #asia #d2 #e1 #tenho-digital |
| Jerusalém | Alan Moore | #F #fantasia #contemporaneo #d3 #e3 #tenho-digital |
| Meridiano de Sangue | Cormac McCarthy | #F #faroeste #classico #d3 #e2 #tenho-digital |
| Meu Amigo Dahmer | Derf Backderf | #HQ #biografia #d1 #e1 #tenho-digital |
| Nossa Senhora do Nilo | Scholastique Mukasonga | #F #contemporaneo #africa #d2 #e1 #tenho-digital |
| Noturnos: Histórias de Música e Anoitecer | Kazuo Ishiguro | #F #contos #contemporaneo #d1 #e1 #tenho-digital |
| O Desertor | Abdulrazak Gurnah | #F #colonialismo #africa #d2 #e2 #tenho-digital |
| O Grande Caderno | Ágota Kristóf | #F #guerra #europa-leste #d2 #e1 #tenho-digital |
| O Lamento dos Rios | Ann Liang | #F #fantasia #contemporaneo #asia #d1 #e2 #tenho-digital |
| O Livro Branco | Han Kang | #F #contemporaneo #asia #d2 #e1 #tenho-digital |
| O Museu do Silêncio | Yoko Ogawa | #F #contemporaneo #asia #d2 #e2 #tenho-digital |
| O Pássaro Pintado | Jerzy Kosinski | #F #guerra #europa-leste #d2 #e1 #tenho-digital |
| O que Lhes Restou | Ghassan Kanafani | #F #guerra #d2 #e1 #tenho-digital |
| O Relatório de Brodeck | Manu Larcenet | #HQ #adaptacao #guerra #d2 #e2 #tenho-digital |
| Onde Vivem as Monstras | Aoko Matsuda | #F #contos #fantasia #genero #asia #d2 #e1 #tenho-digital |
| Os Impostos | (autor não informado) | #HQ #d1 #e1 #verificar #tenho-digital |
| Pílulas Azuis | Frederik Peeters | #HQ #biografia #medicina #d1 #e1 #tenho-digital |
| Primeira Pessoa do Singular | Haruki Murakami | #F #contos #asia #d2 #e1 #tenho-digital |
| Rádio Imaginação | Seiko Ito | #F #asia #d2 #e1 #tenho-digital |
| Relatos de um Gato Viajante | Hiro Arikawa | #F #contemporaneo #asia #d1 #e1 #tenho-digital |
| Sobrevidas | Abdulrazak Gurnah | #F #colonialismo #africa #d2 #e2 #tenho-digital |
| Solitário | Christophe Chabouté | #HQ #d1 #e2 #tenho-digital |
| Sono | Haruki Murakami | #F #contos #asia #d1 #e1 #tenho-digital |
| Tio Sam | Steve Darnall e Alex Ross | #HQ #politica #d2 #e1 #tenho-digital |
| Traço de Giz | Miguelanxo Prado | #HQ #misterio #d2 #e1 #tenho-digital |
| Um Artista do Mundo Flutuante | Kazuo Ishiguro | #F #asia #d2 #e1 #tenho-digital |
| Uma Visita dos Espíritos | Randall Kenan | #F #fantasia #raca #d2 #e2 #tenho-digital |

### 17.6 Romances históricos

| Título | Autor | Tags |
|---|---|---|
| 1356 (Busca do Graal, vol. 4) | Bernard Cornwell | #F #romance-historico #medieval #guerra #d1 #e2 #rel-cornwell #tenho-digital |
| A Lição de Anatomia | Nina Siegal | #F #romance-historico #arte #d2 #e2 #tenho-digital |
| Almas Divididas | Toby Clements | #F #romance-historico #medieval #guerra #d1 #e3 #tenho-digital |
| Barracuda | Jean Dufaux e Jérémy | #HQ #aventura #romance-historico #d1 #e2 #tenho-digital |
| Bórgia | Alejandro Jodorowsky e Milo Manara | #HQ #romance-historico #renascimento #d2 #e2 #tenho-digital |
| Cães do Rei | Martin Jensen | #F #romance-historico #medieval #misterio #d1 #e2 #tenho-digital |
| Civilizações | Laurent Binet | #F #historia-alternativa #d2 #e2 #tenho-digital |
| Como Tigres na Neve | Juhea Kim | #F #romance-historico #asia #d2 #e2 #tenho-digital |
| Desafiando a Morte | David Gilman | #F #romance-historico #medieval #guerra #d1 #e2 #tenho-digital |
| Hamnet | Maggie O'Farrell | #F #romance-historico #renascimento #d2 #e2 #tenho-digital |
| Herança de Sangue (Guerra das Rosas, vol. 3) | Conn Iggulden | #F #romance-historico #medieval #guerra #d1 #e2 #tenho-digital |
| Ira Dei | Vincent Brugeas e Ronan Toulhoat | #HQ #romance-historico #medieval #d1 #e2 #tenho-digital |
| Kingmaker: Uma Jornada no Inverno | Toby Clements | #F #romance-historico #medieval #guerra #d1 #e3 #tenho-digital |
| Lobo Solitário | Kazuo Koike e Goseki Kojima | #HQ #manga #romance-historico #classico #asia #d2 #e3 #tenho-digital |
| M, o Homem da Providência | Antonio Scurati | #F #romance-historico #autoritarismo #d3 #e3 #tenho-digital |
| Mestre da Guerra: Uma Lenda Forjada em Batalha | David Gilman | #F #romance-historico #medieval #guerra #d1 #e2 #tenho-digital |
| Miyamoto Musashi | Shotaro Ishinomori | #HQ #manga #biografia #romance-historico #asia #d1 #e2 #tenho-digital |
| O Abandono da Fé | Toby Clements | #F #romance-historico #medieval #guerra #d1 #e3 #tenho-digital |
| O Cirurgião de Almas | Luis Zueco | #F #romance-historico #medicina #d1 #e2 #tenho-digital |
| O Espelho e a Luz | Hilary Mantel | #F #romance-historico #renascimento #d3 #e3 #tenho-digital |
| O Forte | Bernard Cornwell | #F #romance-historico #guerra #d1 #e2 #rel-cornwell #tenho-digital |
| O Portão dos Mortos | David Gilman | #F #romance-historico #medieval #guerra #d1 #e2 #tenho-digital |
| O Procurador | Gianfranco Manfredi e Pedro Mauro | #HQ #romance-historico #d1 #e1 #tenho-digital |
| O Último Voo das Borboletas | Kan Takahama | #HQ #manga #romance-historico #asia #d1 #e1 #tenho-digital |
| Pássaros da Tempestade (Guerra das Rosas, vol. 1) | Conn Iggulden | #F #romance-historico #medieval #guerra #d1 #e2 #tenho-digital |
| Rebelde | Bernard Cornwell | #F #romance-historico #guerra #d1 #e2 #rel-cornwell #tenho-digital |
| Sangue de Víbora | David Gilman | #F #romance-historico #medieval #guerra #d1 #e2 #tenho-digital |
| Santo Guerreiro: Roma Invicta | Eduardo Spohr | #F #romance-historico #roma #fantasia #BR #antiguidade #d1 #e3 #tenho-digital |
| Santo Guerreiro: Ventos do Norte | Eduardo Spohr | #F #romance-historico #roma #fantasia #BR #antiguidade #d1 #e3 #tenho-digital |
| Trilogia Gatilho | Carlos Estefan e Pedro Mauro | #HQ #faroeste #BR #d1 #e2 #tenho-digital |
| Troia: O Romance de uma Guerra | Cláudio Moreno | #F #romance-historico #antiguidade #BR #RS #d1 #e2 #tenho-digital |
| Um Trem do Inferno | Alistair MacLean | #F #romance-historico #thriller #faroeste #aventura #d1 #e1 #tenho-digital |

### 17.7 Horror, weird fiction e mistério

| Título | Autor | Tags |
|---|---|---|
| 100 Balas | Brian Azzarello e Eduardo Risso | #HQ #policial #thriller #d1 #e3 #tenho-digital |
| A Baía dos Mortos | Edith Wharton | #F #contos #horror #gotico #classico #d2 #e1 #tenho-digital |
| A Causa Secreta e Outros Contos de Horror | Edgar Allan Poe, Machado de Assis e outros | #F #horror #contos #classico #d1 #e1 #tenho-digital |
| A Colônia | Ezekiel Boone | #F #horror #ficcao-cientifica #d1 #e2 #tenho-digital |
| A Enchente | Michael McDowell | #F #horror #gotico #d1 #e1 #tenho-digital |
| A Estrada Enluarada e Outras Histórias | Ambrose Bierce | #F #contos #horror #classico #d2 #e1 #tenho-digital |
| A Floresta das Árvores Retorcidas | Alexandre Callari | #F #horror #BR #d1 #e2 #tenho-digital |
| A Longa Marcha | Stephen King | #F #distopia #thriller #d1 #e2 #tenho-digital |
| A Mordida do Cão Morto | Tyler Boss | #HQ #misterio #d1 #e1 #tenho-digital |
| A Paciente Silenciosa | Alex Michaelides | #F #thriller #d1 #e2 #tenho-digital |
| A Última Casa da Rua Needless | Catriona Ward | #F #horror #thriller #d2 #e2 #tenho-digital |
| Antologia de Contos Extraordinários | Edgar Allan Poe | #F #contos #horror #misterio #classico #d2 #e2 #tenho-digital |
| Antologia H.P. Lovecraft | H.P. Lovecraft | #F #horror #lovecraftiano #contos #classico #d2 #e2 #rel-widows-bay #tenho-digital |
| Ar Frio (em quadrinhos) | Romeu Martins, Val Oliveira e Sandro Zambi | #HQ #adaptacao #horror #lovecraftiano #BR #d1 #e1 #tenho-digital |
| B.P.D.P.: O Diabo que Você Conhece | Mike Mignola, Scott Allie e Laurence Campbell | #HQ #horror #d1 #e2 #tenho-digital |
| Bedlam | Nick Spencer e Riley Rossmo | #HQ #horror #policial #d2 #e2 #tenho-digital |
| Black Hole | Charles Burns | #HQ #horror #d2 #e2 #tenho-digital |
| Britannia | Peter Milligan e Juan José Ryp | #HQ #horror #roma #romance-historico #antiguidade #d1 #e2 #tenho-digital |
| Cabo do Medo | John D. MacDonald | #F #thriller #d1 #e1 #tenho-digital |
| Caminhos Misteriosos | Jason Rubin e Tyler Kirkham | #HQ #fantasia #d1 #e1 #verificar #tenho-digital |
| Candyman | Clive Barker | #F #horror #d1 #e1 #tenho-digital |
| Carmilla | J. Sheridan Le Fanu | #F #horror #gotico #classico #d1 #e1 #tenho-digital |
| Casas Estranhas | Uketsu | #F #horror #misterio #asia #d1 #e1 #tenho-digital |
| Casas Estranhas 2 | Uketsu | #F #misterio #horror #asia #d1 #e2 #tenho-digital |
| Cego | Robin Cook | #F #thriller #thriller-medico #d1 #e2 #tenho-digital |
| Cérebro | Robin Cook | #F #thriller #thriller-medico #d1 #e2 #trilha-plantao-noturno #tenho-digital |
| Ciclo Antarktos (The Antarktos Cycle) | Robert M. Price (org.) | #F #horror #lovecraftiano #antologia #contos #d2 #e3 #verificar #tenho-digital |
| Coelho Morto / Olhos Mortos | Gerry Duggan e John McCrea | #HQ #policial #d1 #e2 #tenho-digital |
| Colheita Macabra | Tess Gerritsen | #F #thriller #thriller-medico #d1 #e2 #trilha-plantao-noturno #tenho-digital |
| Com Sangue | Stephen King | #F #horror #contos #d1 #e2 #tenho-digital |
| Coma | Robin Cook | #F #thriller #thriller-medico #d1 #e2 #trilha-plantao-noturno #tenho-digital |
| Como Vender uma Casa Assombrada | Grady Hendrix | #F #horror #humor #d1 #e2 #tenho-digital |
| Condado Maldito | Cullen Bunn e Tyler Crook | #HQ #horror #gotico #d1 #e2 #tenho-digital |
| Contos de Horror (Vertigo) | Vários autores | #HQ #horror #antologia #d1 #e2 #tenho-digital |
| Contos Fantásticos 01 | Vários autores | #F #contos #fantasia #antologia #d1 #e1 #tenho-digital |
| Contos Fantásticos 02 | Vários autores | #F #contos #fantasia #antologia #d1 #e1 #tenho-digital |
| Contos Fantásticos 03 | Vários autores | #F #contos #fantasia #antologia #d1 #e1 #tenho-digital |
| Coração Satânico | William Hjortsberg | #F #thriller #horror #policial #d1 #e2 #tenho-digital |
| Corpo Estranho | Robin Cook | #F #thriller #thriller-medico #d1 #e2 #tenho-digital |
| Corrente Sanguínea | Tess Gerritsen | #F #thriller #thriller-medico #d1 #e2 #tenho-digital |
| Cripta | Vários autores | #HQ #horror #antologia #classico #d1 #e3 #verificar #tenho-digital |
| Crise | Robin Cook | #F #thriller #thriller-medico #d1 #e2 #tenho-digital |
| Cura Fatal | Robin Cook | #F #thriller #thriller-medico #d1 #e2 #tenho-digital |
| Dias Perfeitos | Raphael Montes | #F #thriller #BR #d1 #e2 #trilha-crime-a-brasileira #tenho-digital |
| Do Inferno | Alan Moore e Eddie Campbell | #HQ #policial #romance-historico #horror #d3 #e3 #trilha-quadrinhos-para-gente-grande #tenho-digital |
| Dolores Claiborne | Stephen King | #F #thriller #d1 #e2 #tenho-digital |
| Esfinge | Robin Cook | #F #thriller #aventura #d1 #e2 #tenho-digital |
| Eu Sou a Lenda | Richard Matheson | #F #horror #ficcao-cientifica #classico #d1 #e1 #tenho-digital |
| Evil Dead | Vários autores | #HQ #horror #d1 #e2 #tenho-digital |
| Gélido | Tess Gerritsen | #F #thriller #thriller-medico #d1 #e2 #tenho-digital |
| Gravidade | Tess Gerritsen | #F #thriller #thriller-medico #ficcao-cientifica #d1 #e2 #trilha-plantao-noturno #tenho-digital |
| H.P. Lovecraft, vol. 2: Miskatonic Edition | H.P. Lovecraft | #F #horror #lovecraftiano #contos #classico #d2 #e3 #rel-widows-bay #tenho-digital |
| Hailstone | Rafael Scavone e Rafael de Latorre | #HQ #horror #faroeste #BR #d1 #e1 #tenho-digital |
| Hellblazer | Vários autores | #HQ #horror #d2 #e3 #tenho-digital |
| Hellboy | Mike Mignola | #HQ #horror #fantasia #d1 #e3 #tenho-digital |
| Hellraiser | Vários autores | #HQ #horror #d1 #e2 #tenho-digital |
| Hex | Thomas Olde Heuvelt | #F #horror #d1 #e2 #tenho-digital |
| Histórias Extraordinárias | Edgar Allan Poe | #F #contos #horror #misterio #classico #d2 #e2 #tenho-digital |
| Imagens Estranhas | Uketsu | #F #horror #misterio #asia #d1 #e2 #tenho-digital |
| Infiel | Pornsak Pichetshote e Aaron Campbell | #HQ #horror #raca #d1 #e1 #tenho-digital |
| Jantar Secreto | Raphael Montes | #F #thriller #horror #BR #d1 #e2 #trilha-crime-a-brasileira #tenho-digital |
| Lágrimas de Aço | S.A. Cosby | #F #thriller #policial #d1 #e2 #tenho-digital |
| Lovecraft | Hans Rodionoff, Keith Giffen e Enrique Breccia | #HQ #horror #lovecraftiano #biografia #d2 #e1 #verificar #tenho-digital |
| Manual das Donas de Casa Caçadoras de Vampiros | Grady Hendrix | #F #horror #humor #d1 #e2 #tenho-digital |
| Missa Negra: Ascensão | Theo Prasidis e Jodie Muir | #HQ #horror #d1 #e1 #tenho-digital |
| Monstro do Pântano | Vários autores | #HQ #horror #d2 #e3 #tenho-digital |
| Monstros | Barry Windsor-Smith | #HQ #horror #ficcao-cientifica #d2 #e2 #tenho-digital |
| Monstros São Meu Negócio | Cullen Bunn e Patrick Piazzalunga | #HQ #horror #humor #d1 #e1 #tenho-digital |
| Morte na Cornualha | Daniel Silva | #F #thriller #d1 #e2 #tenho-digital |
| Nas Montanhas da Loucura (em quadrinhos) | H.P. Lovecraft | #HQ #horror #lovecraftiano #adaptacao #d1 #e1 #rel-widows-bay #tenho-digital |
| Natureza Morta | Kay Chronister | #F #horror #d2 #e2 #tenho-digital |
| O Bazar dos Sonhos Ruins | Stephen King | #F #horror #contos #d1 #e3 #tenho-digital |
| O Bebê é Meu | Oyinkan Braithwaite | #F #thriller #africa #d1 #e1 #tenho-digital |
| O Comitê da Morte | Noah Gordon | #F #thriller #thriller-medico #d1 #e2 #rel-cornwell #trilha-plantao-noturno #tenho-digital |
| O Delator | Tess Gerritsen | #F #thriller #thriller-medico #d1 #e2 #tenho-digital |
| O Escaravelho de Ouro e Outros Contos | Edgar Allan Poe | #F #horror #contos #misterio #classico #d2 #e1 #tenho-digital |
| O Fio do Bisturi | Tess Gerritsen | #F #thriller #thriller-medico #d1 #e2 #tenho-digital |
| O Homem do Colorado | Stephen King | #F #thriller #misterio #d1 #e1 #tenho-digital |
| O Horror em Red Hook | H.P. Lovecraft | #F #horror #lovecraftiano #classico #d2 #e1 #rel-widows-bay #tenho-digital |
| O Jardim de Ossos | Tess Gerritsen | #F #thriller #thriller-medico #romance-historico #d1 #e2 #trilha-plantao-noturno #tenho-digital |
| O Papel de Parede Amarelo | Charlotte Perkins Gilman | #F #horror #gotico #genero #classico #d1 #e1 #tenho-digital |
| O Pátio | Alan Moore e Jacen Burrows | #HQ #horror #lovecraftiano #d2 #e1 #tenho-digital |
| O Sacrifício | Joe Hill | #F #horror #d1 #e3 #tenho-digital |
| O Selo Amarelo | Robert W. Chambers | #F #horror #contos #classico #d2 #e1 #tenho-digital |
| O Sorriso do Homem Mau e Outros Contos Policiais | Raphael Montes | #F #contos #policial #thriller #BR #d1 #e1 #tenho-digital |
| O Tiro Final e Outros Contos Sensacionais | Arthur Conan Doyle | #F #contos #misterio #classico #d1 #e1 #tenho-digital |
| O Vilarejo | Raphael Montes | #F #thriller #horror #contos #BR #d1 #e1 #tenho-digital |
| Os Crimes da Rua Morgue e Outras Histórias | Edgar Allan Poe | #F #horror #contos #misterio #classico #d2 #e1 #tenho-digital |
| Os Fantasmas da Baía Looking Glass | Catriona Ward | #F #horror #thriller #d2 #e2 #tenho-digital |
| Os Melhores Contos de H.P. Lovecraft | H.P. Lovecraft | #F #horror #lovecraftiano #contos #classico #d2 #e2 #rel-widows-bay #tenho-digital |
| Os Nomes das Coisas e Outros Contos Estranhos | Hugh Behm-Steinberg | #F #contos #d2 #e1 #tenho-digital |
| Out | Rob Williams e Will Conrad | #HQ #horror #guerra #d1 #e1 #tenho-digital |
| Papa-Capim: Noite Branca (Graphic MSP) | Marcela Godoy e Renato Guedes | #HQ #horror #BR #d1 #e1 #tenho-digital |
| Pestilência | Frank Tieri e Oleg Okunev | #HQ #horror #medieval #d1 #e1 #tenho-digital |
| Preacher | Garth Ennis e Steve Dillon | #HQ #horror #religiao #humor #d2 #e3 #tenho-digital |
| Protocolo Zero | Anthony McCarten | #F #thriller #d1 #e2 #tenho-digital |
| Rashomon | Victor Santos | #HQ #policial #asia #d1 #e1 #verificar #tenho-digital |
| Servidão Mental | Robin Cook | #F #thriller #thriller-medico #d1 #e2 #tenho-digital |
| Sete Anos de Escuridão | You-jeong Jeong | #F #thriller #asia #d2 #e2 #tenho-digital |
| Severed | Scott Snyder, Scott Tuft e Attila Futaki | #HQ #horror #d1 #e1 #tenho-digital |
| Sin City | Frank Miller | #HQ #policial #classico #d1 #e3 #tenho-digital |
| Slow Horses | Mick Herron | #F #thriller #d1 #e2 #tenho-digital |
| Sombras da Noite | Stephen King | #F #horror #contos #d1 #e2 #tenho-digital |
| Sombrio e Sangrento | Shawn Aldridge e Scott Godlewski | #HQ #horror #d1 #e1 #tenho-digital |
| Suicidas | Raphael Montes | #F #thriller #BR #d1 #e2 #trilha-crime-a-brasileira #tenho-digital |
| Todo Mundo Neste Trem é Suspeito | Benjamin Stevenson | #F #misterio #humor #d1 #e2 #tenho-digital |
| Tormenta | C.J. Tudor | #F #thriller #horror #d1 #e2 #tenho-digital |
| Torso | Brian Michael Bendis e Marc Andreyko | #HQ #policial #romance-historico #d2 #e2 #tenho-digital |
| Trilogia Lovecraft | (autor não informado) | #HQ #horror #lovecraftiano #d1 #e2 #verificar #tenho-digital |
| Um Estudo em Esmeralda | Neil Gaiman e Rafael Albuquerque | #HQ #misterio #lovecraftiano #adaptacao #d1 #e1 #tenho-digital |
| Um Passeio no Inferno | Garth Ennis e Goran Sudžuka | #HQ #horror #policial #d2 #e2 #tenho-digital |
| Uma Família Feliz | Raphael Montes | #F #thriller #BR #d1 #e2 #trilha-crime-a-brasileira #tenho-digital |
| Vendemos Nossas Almas | Grady Hendrix | #F #horror #d1 #e2 #tenho-digital |
| Vertigo: Contos Inquietantes | Vários autores | #HQ #horror #antologia #d1 #e1 #tenho-digital |
| Vertigo (Opera Graphica) | Vários autores | #HQ #horror #fantasia #antologia #d1 #e3 #tenho-digital |
| Vida Assistida | Tess Gerritsen | #F #thriller #thriller-medico #d1 #e2 #tenho-digital |
| Voo Fantasma | Bear Grylls | #F #thriller #aventura #d1 #e2 #tenho-digital |

### 17.8 Poesia e cartas

| Título | Autor | Tags |
|---|---|---|
| 200 Limeriques de Edward Lear para Ler e para Ver | Edward Lear | #poesia #humor #classico #d1 #e1 #tenho-digital |
| Canções, seguido de Sapato Florido e A Rua dos Cataventos | Mario Quintana | #poesia #classico #BR #RS #d1 #e1 #tenho-digital |
| Carta ao Pai | Franz Kafka | #NF #classico #d2 #e1 #tenho-digital |
| Distraídos Venceremos | Paulo Leminski | #poesia #BR #d1 #e1 #tenho-digital |
| Elogio da Sombra | Jorge Luis Borges | #poesia #latam #d2 #e1 #tenho-digital |
| Esconderijos do Tempo | Mario Quintana | #poesia #BR #RS #d1 #e1 #trilha-porto-alegre-hoje #tenho-digital |
| Não Me Deixe Só: Uma Lírica Americana | Claudia Rankine | #poesia #raca #d2 #e1 #tenho-digital |
| Rabo de Baleia | Alice Sant'Anna | #poesia #contemporaneo #BR #d2 #e1 #tenho-digital |
| Sonetos de Amor e Sacanagem | Gregorio Duvivier | #poesia #humor #BR #d1 #e1 #tenho-digital |

### 17.9 Filosofia, ética e existência (não ficção)

| Título | Autor | Tags |
|---|---|---|
| 100 Aforismos sobre o Amor e a Morte | Friedrich Nietzsche | #NF #filosofia #classico #d2 #e1 #tenho-digital |
| 1492: O Encobrimento do Outro: A Origem do Mito da Modernidade | Enrique Dussel | #NF #filosofia #colonialismo #historia #latam #d3 #e2 #tenho-digital |
| 38 Estratégias para Vencer Qualquer Debate | Arthur Schopenhauer | #NF #filosofia #classico #d1 #e1 #tenho-digital |
| 50 Clássicos da Filosofia | Tom Butler-Bowdon | #NF #filosofia #introducao #d1 #e2 #tenho-digital |
| A Arqueologia do Saber | Michel Foucault | #NF #filosofia #classico #d3 #e2 #tenho-digital |
| A Arte de Argumentar | Antonio Suarez Abreu | #NF #filosofia #linguagem #didatico #d1 #e1 #tenho-digital |
| A Arte de Viver | Epicteto | #NF #filosofia #etica #antiguidade #classico #d1 #e1 #tenho-digital |
| A Cabeça Bem-Feita | Edgar Morin | #NF #filosofia #educacao #d2 #e1 #tenho-digital |
| A Filosofia da Adúltera | Luiz Felipe Pondé | #NF #filosofia #BR #d1 #e1 #tenho-digital |
| A Filosofia entre a Religião e a Ciência | Bertrand Russell | #NF #filosofia #religiao #ciencia #d2 #e1 #tenho-digital |
| A Filosofia Explica Grandes Questões da Humanidade | Clóvis de Barros Filho e Júlio Pompeu | #NF #filosofia #introducao #BR #d1 #e1 #tenho-digital |
| A Filosofia Perene | Humberto Schubert Coelho | #NF #filosofia #religiao #mistica #d2 #e2 #tenho-digital |
| A Guerra dos Tronos e a Filosofia | William Irwin | #NF #filosofia #arte #d1 #e2 #tenho-digital |
| A História da Filosofia para Quem Tem Pressa | Lesley Levene | #NF #filosofia #introducao #d1 #e1 #tenho-digital |
| A Navalha de Ockham: O Princípio Filosófico que Libertou a Ciência e Ajudou a Explicar o Universo | Johnjoe McFadden | #NF #filosofia #ciencia #historia #d2 #e2 #tenho-digital |
| A Sociedade da Transparência | Byung-Chul Han | #NF #filosofia #d2 #e1 #tenho-digital |
| A Teoria Crítica | Marcos Nobre | #NF #filosofia #introducao #politica #d2 #e1 #tenho-digital |
| A Virtude do Egoísmo | Ayn Rand | #NF #filosofia #etica #politica #d2 #e1 #tenho-digital |
| A Vontade de Poder | Friedrich Nietzsche | #NF #filosofia #classico #d3 #e3 #tenho-digital |
| Adorno/Horkheimer e a Dialética do Esclarecimento | Rodrigo Duarte | #NF #filosofia #introducao #d2 #e1 #tenho-digital |
| Afirmar-se com Nietzsche | Balthasar Thomass | #NF #filosofia #introducao #d1 #e1 #tenho-digital |
| Agonia do Eros | Byung-Chul Han | #NF #filosofia #d2 #e1 #tenho-digital |
| Algunos Pareceres de Nietzsche | Jorge Luis Borges | #NF #filosofia #d2 #e1 #tenho-digital |
| Aristóteles em 90 Minutos | Paul Strathern | #NF #introducao #filosofia #biografia #d1 #e1 #tenho-digital |
| As Dores do Mundo | Arthur Schopenhauer | #NF #filosofia #classico #d2 #e1 #tenho-digital |
| As Estrelas Descem à Terra | Theodor W. Adorno | #NF #filosofia #sociologia #d3 #e1 #tenho-digital |
| As Máximas de Ptahhotep | Ptahhotep | #NF #filosofia #etica #antiguidade #classico #d1 #e1 #tenho-digital |
| As Vantagens do Pessimismo e o Perigo da Falsa Esperança | Roger Scruton | #NF #filosofia #politica #d2 #e1 #tenho-digital |
| Atrás do Pensamento: A Filosofia de Clarice Lispector | Marcia Sá Cavalcante Schuback | #NF #filosofia #escrita #BR #d3 #e2 #tenho-digital |
| Berkeley em 90 Minutos | Paul Strathern | #NF #introducao #filosofia #biografia #d1 #e1 #tenho-digital |
| Bom Entretenimento | Byung-Chul Han | #NF #filosofia #d2 #e1 #tenho-digital |
| Caosmose: Um Novo Paradigma Estético | Félix Guattari | #NF #filosofia #psicanalise #d3 #e1 #tenho-digital |
| Carta sobre a Felicidade (a Meneceu) | Epicuro | #NF #filosofia #etica #antiguidade #classico #d1 #e1 #tenho-digital |
| Ceticismo | Plínio Junqueira Smith | #NF #filosofia #introducao #d2 #e1 #tenho-digital |
| Como Estudar Filosofia: Guia Prático para Estudantes | Clare Saunders e outros | #NF #filosofia #didatico #d1 #e1 #tenho-digital |
| Como Ler Lacan | Slavoj Žižek | #NF #filosofia #psicanalise #d2 #e1 #tenho-digital |
| Curso Livre Marx-Engels: A Criação Destruidora | José Paulo Netto (org.) | #NF #filosofia #politica #economia #d2 #e2 #tenho-digital |
| Da Árvore ao Labirinto: Estudos Históricos sobre o Signo e a Interpretação | Umberto Eco | #NF #filosofia #linguagem #d3 #e3 #tenho-digital |
| Derrida em 90 Minutos | Paul Strathern | #NF #introducao #filosofia #biografia #d1 #e1 #tenho-digital |
| Desapegar-se com Schopenhauer | Céline Belloq | #NF #filosofia #introducao #d1 #e1 #tenho-digital |
| Descomplicando a Filosofia: Conceitos Básicos e Grandes Pensadores | Alessandro Cavallari | #NF #filosofia #introducao #d1 #e2 #tenho-digital |
| Deus ou Seja a Natureza: Spinoza e os Novos Paradigmas da Física | Roberto Leon Ponczek | #NF #filosofia #ciencia #fisica #d3 #e2 #tenho-digital |
| Dez Erros Filosóficos | Mortimer J. Adler | #NF #filosofia #d2 #e1 #tenho-digital |
| Dialética do Esclarecimento | Theodor W. Adorno e Max Horkheimer | #NF #filosofia #sociologia #classico #d3 #e2 #tenho-digital |
| Discurso de Metafísica e Outros Textos | Gottfried Wilhelm Leibniz | #NF #filosofia #classico #d3 #e1 #tenho-digital |
| Do Romantismo a Nietzsche: Rupturas e Transformações na Filosofia do Século XIX | Clademir Luís Araldi | #NF #filosofia #d2 #e1 #tenho-digital |
| Dossiê Nietzsche | Daniel Rodrigues Aurélio | #NF #filosofia #introducao #d1 #e1 #tenho-digital |
| Em Defesa das Causas Perdidas | Slavoj Žižek | #NF #filosofia #politica #d3 #e3 #tenho-digital |
| Ensaios sobre a Moralidade | Maria Clara Dias | #NF #filosofia #etica #d2 #e2 #tenho-digital |
| Ensaios sobre Mortos-Vivos: The Walking Dead e Outras Metáforas | Rodrigo Gonsalves e Diego Penha (orgs.) | #NF #filosofia #cinema #d2 #e2 #tenho-digital |
| Espinosa: Uma Filosofia da Liberdade | Marilena Chaui | #NF #filosofia #introducao #BR #d2 #e1 #tenho-digital |
| Estética | Kathrin H. Rosenfield | #NF #filosofia #arte #introducao #d2 #e1 #tenho-digital |
| Estudos sobre o Amor | José Ortega y Gasset | #NF #filosofia #d2 #e1 #tenho-digital |
| Ética da Virtude | Stan van Hooft | #NF #filosofia #etica #introducao #d2 #e2 #tenho-digital |
| Ética e Pós-verdade | Christian Dunker, Cristovão Tezza e Julián Fuks | #NF #filosofia #etica #politica #BR #d2 #e1 #tenho-digital |
| Existencialismo | Jack Reynolds | #NF #filosofia #existencialismo #introducao #d2 #e2 #tenho-digital |
| Fenomenologia | David R. Cerbone | #NF #filosofia #introducao #d2 #e2 #tenho-digital |
| Filosofia Antiga (Série Investigação Filosófica) | Vários autores | #NF #filosofia #antiguidade #d3 #e2 #tenho-digital |
| Filosofia Antiga: Uma Introdução Contemporânea | Christopher Shields | #NF #filosofia #antiguidade #introducao #d2 #e2 #tenho-digital |
| Filosofia da Biologia | Karla Chediak | #NF #filosofia #ciencia #introducao #d2 #e1 #tenho-digital |
| Filosofia da Ciência | Alberto Oliva | #NF #filosofia #ciencia #introducao #d2 #e1 #tenho-digital |
| Filosofia da História | Rossano Pecoraro | #NF #filosofia #historia #introducao #d2 #e1 #tenho-digital |
| Filosofia da Linguagem | Claudio Costa | #NF #filosofia #linguagem #introducao #d2 #e1 #tenho-digital |
| Filosofia da Mente | Claudio Costa | #NF #filosofia #consciencia #introducao #d2 #e1 #tenho-digital |
| Filosofia da Natureza | Márcia Gonçalves | #NF #filosofia #introducao #d2 #e1 #tenho-digital |
| Filosofia em 60 Segundos | Andrew Pessin | #NF #filosofia #introducao #d1 #e1 #tenho-digital |
| Filosofia: Os Autores, as Obras | Jacqueline Russ | #NF #filosofia #introducao #didatico #d2 #e3 #tenho-digital |
| Filosofia para a Vida | Jules Evans | #NF #filosofia #etica #autoconhecimento #d1 #e2 #tenho-digital |
| Filosofia para Corajosos | Luiz Felipe Pondé | #NF #filosofia #BR #d1 #e1 #tenho-digital |
| Filosofia para Ocupados | Lesley Levene | #NF #filosofia #introducao #d1 #e1 #tenho-digital |
| Filosofia sem as Partes Chatas | Alain Stephen | #NF #filosofia #introducao #d1 #e1 #tenho-digital |
| Filosofia: Textos Fundamentais Comentados | Laurence Bonjour e Ann Baker | #NF #filosofia #didatico #d3 #e3 #tenho-digital |
| Filosofias Africanas: Uma Introdução | Nei Lopes e Luiz Antonio Simas | #NF #filosofia #introducao #BR #africa #d2 #e1 #trilha-terreiro-e-encruzilhada #tenho-digital |
| Foucault em 90 Minutos | Paul Strathern | #NF #introducao #filosofia #biografia #d1 #e1 #tenho-digital |
| Grandes Pensadores | The School of Life | #NF #filosofia #introducao #d1 #e2 #tenho-digital |
| Guia Politicamente Incorreto da Filosofia | Luiz Felipe Pondé | #NF #filosofia #BR #d1 #e1 #tenho-digital |
| Hannah Arendt | Adriano Correia | #NF #filosofia #introducao #politica #d2 #e1 #tenho-digital |
| Hegel e a Fenomenologia do Espírito | Paulo Gaspar de Meneses | #NF #filosofia #introducao #d3 #e1 #tenho-digital |
| Hegel e o Oculto: Uma Abordagem Materialista, vol. 1 | Lucas Hades-Kaeté | #NF #filosofia #mistica #d3 #e2 #tenho-digital |
| Hegel em 90 Minutos | Paul Strathern | #NF #introducao #filosofia #biografia #d1 #e1 #tenho-digital |
| Hegelianismo | Robert Sinnerbrink | #NF #filosofia #introducao #d3 #e2 #tenho-digital |
| Heidegger em 90 Minutos | Paul Strathern | #NF #introducao #filosofia #biografia #d1 #e1 #tenho-digital |
| Hermenêutica | Lawrence K. Schmidt | #NF #filosofia #introducao #d2 #e2 #tenho-digital |
| História da Filosofia Moderna, vol. 1 | Luciano De Crescenzo | #NF #filosofia #introducao #humor #d1 #e1 #tenho-digital |
| História da Filosofia Moderna, vol. 2 | Luciano De Crescenzo | #NF #filosofia #introducao #humor #d1 #e1 #tenho-digital |
| História do Pensamento Ocidental: A Aventura dos Pré-Socráticos a Wittgenstein | Bertrand Russell | #NF #filosofia #introducao #historia #d2 #e3 #tenho-digital |
| Hobbes e a Liberdade | Julio Bernardes | #NF #filosofia #politica #introducao #d2 #e1 #tenho-digital |
| Humano, Demasiado Humano II | Friedrich Nietzsche | #NF #filosofia #classico #d3 #e2 #tenho-digital |
| Hume | Leonardo Sartori Porto | #NF #filosofia #introducao #d2 #e1 #tenho-digital |
| Hume em 90 Minutos | Paul Strathern | #NF #introducao #filosofia #biografia #d1 #e1 #tenho-digital |
| Imposturas Intelectuais | Alan Sokal e Jean Bricmont | #NF #filosofia #ciencia #d2 #e2 #tenho-digital |
| Infocracia: Digitalização e a Crise da Democracia | Byung-Chul Han | #NF #filosofia #politica #d2 #e1 #trilha-entender-o-presente #tenho-digital |
| Iniciação à Filosofia | Marilena Chaui | #NF #filosofia #introducao #didatico #BR #d1 #e2 #tenho-digital |
| Iniciação à História da Filosofia: Dos Pré-Socráticos a Wittgenstein | Danilo Marcondes | #NF #filosofia #introducao #didatico #BR #d2 #e2 #tenho-digital |
| Inteligência Artificial (Como Ler Filosofia) | João de Fernandes Teixeira | #NF #filosofia #ia #introducao #tecnologia #d2 #e1 #tenho-digital |
| Introdução à Filosofia | Marly N. Peres | #NF #filosofia #introducao #d1 #e1 #tenho-digital |
| John Stuart Mill e a Liberdade | Mauro Cardoso Simões | #NF #filosofia #politica #introducao #d2 #e1 #tenho-digital |
| Kant e a Crítica da Razão Pura | Vinicius Berlendis de Figueiredo | #NF #filosofia #introducao #d3 #e1 #tenho-digital |
| Kierkegaard | Jorge M. de Almeida e Alvaro L.M. Valls | #NF #filosofia #existencialismo #introducao #d2 #e1 #tenho-digital |
| Kierkegaard em 90 Minutos | Paul Strathern | #NF #introducao #filosofia #biografia #d1 #e1 #tenho-digital |
| Lacrimae Rerum | Slavoj Žižek | #NF #filosofia #cinema #d2 #e2 #tenho-digital |
| Leibniz e a Linguagem | Vivianne de Castilho Moreira | #NF #filosofia #linguagem #d3 #e1 #tenho-digital |
| Leibniz em 90 Minutos | Paul Strathern | #NF #introducao #filosofia #biografia #d1 #e1 #tenho-digital |
| Lições sobre os Pré-platônicos | Friedrich Nietzsche | #NF #filosofia #antiguidade #classico #d3 #e2 #tenho-digital |
| Linguagem: Conceitos-Chave em Filosofia | José Medina | #NF #filosofia #linguagem #introducao #d2 #e2 #tenho-digital |
| Linguagem e Cognição | (autor não informado) | #NF #filosofia #linguagem #d2 #e2 #verificar #tenho-digital |
| Linguagem e Mente: Pensamentos Atuais sobre Antigos Problemas | Noam Chomsky | #NF #filosofia #linguagem #d3 #e2 #tenho-digital |
| Livro da Alma | Avicena (Ibn Sina) | #NF #filosofia #medieval #classico #d3 #e2 #tenho-digital |
| Maquiavel em 90 Minutos | Paul Strathern | #NF #introducao #filosofia #biografia #politica #d1 #e1 #tenho-digital |
| Marx em 90 Minutos | Paul Strathern | #NF #introducao #filosofia #biografia #politica #d1 #e1 #tenho-digital |
| Marxismo | Geoff Boucher | #NF #filosofia #politica #introducao #d2 #e2 #tenho-digital |
| Mente: Conceitos-Chave em Filosofia | Eric Matthews | #NF #filosofia #consciencia #introducao #d2 #e2 #tenho-digital |
| Metafísica: Conceitos-Chave em Filosofia | Brian Garrett | #NF #filosofia #introducao #d2 #e2 #tenho-digital |
| Naturalismo | Jack Ritchie | #NF #filosofia #ciencia #introducao #d2 #e2 #tenho-digital |
| Nem Anjos Nem Demônios | Mario Sergio Cortella e Monja Coen | #NF #filosofia #etica #espiritualidade #BR #d1 #e1 #tenho-digital |
| Nietzsche | Nelson Boeira | #NF #filosofia #introducao #d2 #e1 #tenho-digital |
| Nietzsche e a Filosofia Budista | Antoine Panaïoti | #NF #filosofia #oriental #d3 #e2 #tenho-digital |
| Nietzsche e a Grande Política da Linguagem | Viviane Mosé | #NF #filosofia #linguagem #BR #d3 #e2 #tenho-digital |
| Nietzsche em 90 Minutos | Paul Strathern | #NF #introducao #filosofia #biografia #d1 #e1 #trilha-filosofia-em-doses #tenho-digital |
| Nietzsche (em quadrinhos) | Michel Onfray e Maximilien Le Roy | #HQ #biografia #filosofia #d1 #e1 #tenho-digital |
| Nietzscheanismo | Ashley Woodward | #NF #filosofia #introducao #d2 #e2 #tenho-digital |
| Niilismo | Rossano Pecoraro | #NF #filosofia #existencialismo #introducao #d2 #e1 #tenho-digital |
| No Enxame | Byung-Chul Han | #NF #filosofia #d2 #e1 #tenho-digital |
| Nos Labirintos da Moral | Mario Sergio Cortella e Yves de La Taille | #NF #filosofia #etica #BR #d1 #e1 #tenho-digital |
| O Anti-Édipo | Gilles Deleuze e Félix Guattari | #NF #filosofia #psicanalise #politica #d3 #e3 #tenho-digital |
| O Anticristo e Ditirambos de Dionísio | Friedrich Nietzsche | #NF #filosofia #religiao #classico #d2 #e1 #tenho-digital |
| O Cinema Pensa: Uma Introdução à Filosofia Através dos Filmes | Julio Cabrera | #NF #filosofia #cinema #d2 #e2 #tenho-digital |
| O Fantástico Mundo da Filosofia | Michael F. Patton | #NF #filosofia #introducao #d1 #e1 #tenho-digital |
| O Filósofo Ignorante | Voltaire | #NF #filosofia #classico #d2 #e1 #tenho-digital |
| O Hobbit e a Filosofia | William Irwin | #NF #filosofia #arte #d1 #e2 #tenho-digital |
| O Homem que Sabe | Viviane Mosé | #NF #filosofia #psicologia #BR #d2 #e2 #tenho-digital |
| O Império do Sentido | François Dosse | #NF #filosofia #historia #d3 #e3 #tenho-digital |
| O Livro da Filosofia | Vários autores | #NF #introducao #filosofia #d1 #e2 #tenho-digital |
| O que é Filosofia | José Ortega y Gasset | #NF #filosofia #d2 #e2 #tenho-digital |
| O que é Ideologia | Marilena Chaui | #NF #filosofia #politica #introducao #BR #d1 #e1 #tenho-digital |
| O que é Poder | Byung-Chul Han | #NF #filosofia #politica #d2 #e1 #tenho-digital |
| O que é Semiótica | Lucia Santaella | #NF #filosofia #linguagem #introducao #BR #d2 #e1 #tenho-digital |
| O Sentido do Pensar: A Filosofia Desafia a Inteligência Artificial | Markus Gabriel | #NF #filosofia #ia #tecnologia #d3 #e2 #tenho-digital |
| Oito Ensaios sobre Cultura Latino-Americana e Libertação (1965-1991) | Enrique Dussel | #NF #filosofia #colonialismo #latam #d3 #e2 #tenho-digital |
| Ontologia | Susana de Castro | #NF #filosofia #introducao #d2 #e1 #tenho-digital |
| Os Analectos | Confúcio | #NF #filosofia #oriental #etica #classico #d2 #e1 #tenho-digital |
| Palácio de Cristal: Para uma Teoria Filosófica da Globalização | Peter Sloterdijk | #NF #filosofia #politica #d3 #e2 #tenho-digital |
| Pape Satàn Aleppe: Crônicas de uma Sociedade Líquida | Umberto Eco | #NF #filosofia #cronicas #d1 #e2 #tenho-digital |
| Platão em 90 Minutos | Paul Strathern | #NF #introducao #filosofia #biografia #d1 #e1 #trilha-filosofia-em-doses #tenho-digital |
| Por que Amamos | Renato Noguera | #NF #filosofia #BR #d1 #e1 #tenho-digital |
| Pós-estruturalismo | James Williams | #NF #filosofia #introducao #d3 #e2 #tenho-digital |
| Primeiros Passos em Filosofia Antiga | Marly N. Peres | #NF #filosofia #antiguidade #introducao #d1 #e1 #tenho-digital |
| Provérbios de Confúcio | Willian Castro | #NF #filosofia #oriental #etica #d1 #e1 #tenho-digital |
| Psicopolítica | Byung-Chul Han | #NF #filosofia #politica #d2 #e1 #trilha-entender-o-presente #tenho-digital |
| Racionalismo | Charlie Huenemann | #NF #filosofia #introducao #d2 #e2 #tenho-digital |
| Rousseau em 90 Minutos | Paul Strathern | #NF #introducao #filosofia #biografia #politica #d1 #e1 #tenho-digital |
| Santo Agostinho em 90 Minutos | Paul Strathern | #NF #introducao #filosofia #biografia #religiao #d1 #e1 #tenho-digital |
| São Tomás de Aquino em 90 Minutos | Paul Strathern | #NF #introducao #filosofia #biografia #religiao #d1 #e1 #tenho-digital |
| Sartre em 90 Minutos | Paul Strathern | #NF #introducao #filosofia #biografia #existencialismo #d1 #e1 #trilha-filosofia-em-doses #tenho-digital |
| Schelling | Leonardo Alves Vieira | #NF #filosofia #introducao #d3 #e1 #tenho-digital |
| Schopenhauer | Jair Barboza | #NF #filosofia #introducao #d2 #e1 #tenho-digital |
| Schopenhauer em 90 Minutos | Paul Strathern | #NF #introducao #filosofia #biografia #d1 #e1 #tenho-digital |
| Ser Livre com Sartre | Frédéric Allouche | #NF #filosofia #existencialismo #introducao #d1 #e1 #tenho-digital |
| Signos | Maurice Merleau-Ponty | #NF #filosofia #linguagem #d3 #e2 #tenho-digital |
| Sobre a Brevidade da Vida | Sêneca | #NF #filosofia #etica #roma #classico #antiguidade #d1 #e1 #tenho-digital |
| Sociedade Paliativa | Byung-Chul Han | #NF #filosofia #d2 #e1 #tenho-digital |
| Sócrates | Clóvis de Barros Filho | #NF #filosofia #introducao #BR #d1 #e1 #tenho-digital |
| Sócrates Encontra Descartes | Peter Kreeft | #NF #filosofia #d1 #e1 #tenho-digital |
| Sócrates Encontra Marx | Peter Kreeft | #NF #filosofia #politica #d1 #e1 #tenho-digital |
| Spinoza em 90 Minutos | Paul Strathern | #NF #introducao #filosofia #biografia #d1 #e1 #tenho-digital |
| Teoria do Conhecimento | Alberto Oliva | #NF #filosofia #introducao #d2 #e1 #tenho-digital |
| Teoria do Conhecimento | Johannes Hessen | #NF #filosofia #d2 #e1 #tenho-digital |
| Textos Básicos de Ética: De Platão a Foucault | Danilo Marcondes | #NF #filosofia #etica #didatico #d2 #e1 #tenho-digital |
| Textos Básicos de Filosofia da Ciência: A Revolução Científica | Danilo Marcondes | #NF #filosofia #ciencia #didatico #d2 #e1 #tenho-digital |
| Textos Básicos de Filosofia: Dos Pré-Socráticos a Wittgenstein | Danilo Marcondes | #NF #filosofia #didatico #d2 #e1 #tenho-digital |
| Textos Básicos de Linguagem: De Platão a Foucault | Danilo Marcondes | #NF #filosofia #linguagem #didatico #d2 #e1 #tenho-digital |
| Textos Selecionados de Filosofia Latino-Americana I | Vários autores | #NF #filosofia #latam #d3 #e2 #tenho-digital |
| Tigres no Espelho e Outros Textos | George Steiner | #NF #filosofia #escrita #d3 #e2 #tenho-digital |
| Tudo o que Você Precisa Saber sobre Filosofia | Paul Kleinman | #NF #filosofia #introducao #d1 #e2 #tenho-digital |
| Uma Breve História da Filosofia | Nigel Warburton | #NF #filosofia #introducao #d1 #e2 #trilha-filosofia-em-doses #tenho-digital |
| Utilitarismo | Tim Mulgan | #NF #filosofia #etica #introducao #d2 #e2 #tenho-digital |
| Violência | Slavoj Žižek | #NF #filosofia #politica #d2 #e1 #tenho-digital |
| Viver Apaixonadamente com Kierkegaard | Damien Clerget-Gurnaud | #NF #filosofia #existencialismo #introducao #d1 #e1 #tenho-digital |
| Wittgenstein e o Tractatus | Edgar Marques | #NF #filosofia #introducao #d3 #e1 #tenho-digital |
| Wittgenstein em 90 Minutos | Paul Strathern | #NF #introducao #filosofia #biografia #d1 #e1 #tenho-digital |

### 17.10 Mente, consciência e neurociência

| Título | Autor | Tags |
|---|---|---|
| A Anatomia da Violência: As Raízes Biológicas da Criminalidade | Adrian Raine | #NF #psicologia #neurociencia #d2 #e2 #tenho-digital |
| A Arte de Esquecer: Cérebro e Memória | Iván Izquierdo | #NF #neurociencia #memoria #BR #d1 #e1 #tenho-digital |
| A Consciência: Uma Viagem pelo Cérebro | Ronald Fiuza | #NF #neurociencia #consciencia #BR #d2 #e2 #tenho-digital |
| A Estranha Ordem das Coisas: As Origens Biológicas dos Sentimentos e da Cultura | António Damásio | #NF #ciencia #neurociencia #biologia #consciencia #d3 #e2 #tenho-digital |
| A Ilusão do Eu | Chris Niebauer | #NF #consciencia #neurociencia #espiritualidade #d1 #e1 #tenho-digital |
| A Mente Assombrada | Oliver Sacks | #NF #neurociencia #d1 #e2 #tenho-digital |
| A Vantagem Humana: Como Nosso Cérebro se Tornou Superpoderoso | Suzana Herculano-Houzel | #NF #ciencia #neurociencia #biologia #BR #d2 #e2 #tenho-digital |
| Bases Biológicas do Comportamento: Introdução à Neurociência | Marcus Lira Brandão | #NF #neurociencia #didatico #BR #d2 #e2 #tenho-digital |
| Bases Biológicas dos Transtornos Psiquiátricos: Uma Abordagem Translacional | Flávio Kapczinski, João Quevedo e Iván Izquierdo | #NF #neurociencia #psiquiatria #BR #d3 #e2 #tenho-digital |
| Cem Bilhões de Neurônios: Conceitos Fundamentais de Neurociência | Roberto Lent | #NF #neurociencia #didatico #BR #d2 #e3 #tenho-digital |
| Cérebro e Crença | Michael Shermer | #NF #psicologia #neurociencia #religiao #d2 #e2 #tenho-digital |
| Cérebro: Uma Biografia | David Eagleman | #NF #neurociencia #d1 #e2 #tenho-digital |
| Cognição, Neuropsicologia e Aprendizagem | Vitor da Fonseca | #NF #neurociencia #educacao #d2 #e2 #tenho-digital |
| Como Criar uma Mente: Os Segredos do Pensamento Humano | Ray Kurzweil | #NF #ia #neurociencia #tecnologia #d2 #e2 #tenho-digital |
| Do que é Feito o Pensamento: A Língua como Janela para a Natureza Humana | Steven Pinker | #NF #psicologia #linguagem #d2 #e3 #tenho-digital |
| E o Cérebro Criou o Homem | António Damásio | #NF #neurociencia #consciencia #d3 #e2 #tenho-digital |
| Elástico: Como o Pensamento Flexível Pode Mudar Nossas Vidas | Leonard Mlodinow | #NF #neurociencia #psicologia #d1 #e2 #tenho-digital |
| Em Busca de Espinosa | António Damásio | #NF #filosofia #neurociencia #d2 #e2 #tenho-digital |
| Emocional: A Nova Neurociência dos Afetos | Leonard Mlodinow | #NF #psicologia #neurociencia #d1 #e2 #tenho-digital |
| Filosofia da Mente: Neurociência, Cognição e Comportamento | João de Fernandes Teixeira | #NF #neurociencia #filosofia #consciencia #BR #d2 #e2 #tenho-digital |
| Fundamentos de Neuropsicologia | Alexander R. Luria | #NF #neurociencia #classico #d3 #e2 #tenho-digital |
| Limiar | Sidarta Ribeiro | #NF #ciencia #neurociencia #BR #d1 #e1 #tenho-digital |
| Manual de Psicologia Cognitiva | Michael W. Eysenck | #NF #psicologia #didatico #d3 #e3 #tenho-digital |
| Mente, Cérebro e Cognição | João de Fernandes Teixeira | #NF #psicologia #filosofia #consciencia #BR #d2 #e1 #tenho-digital |
| Neuroanatomia Funcional | Angelo Machado | #NF #neurociencia #medicina #didatico #BR #d3 #e2 #tenho-digital |
| Neurobiologia dos Transtornos Psiquiátricos | João Quevedo | #NF #neurociencia #psiquiatria #BR #d3 #e2 #tenho-digital |
| Neurociência da Mente e do Comportamento | Roberto Lent | #NF #neurociencia #didatico #BR #d3 #e2 #tenho-digital |
| Neurociência para Leigos | Frank Amthor | #NF #neurociencia #introducao #d1 #e2 #tenho-digital |
| Neurociências: Desvendando o Sistema Nervoso | Mark F. Bear, Barry W. Connors e Michael A. Paradiso | #NF #neurociencia #didatico #d3 #e3 #tenho-digital |
| Neurociências Ilustrada | Claudia Krebs, Joanne Weinberg e Elizabeth Akesson | #NF #neurociencia #didatico #d2 #e2 #tenho-digital |
| Neurofisiologia | Rithiele Cristina de Oliveira | #NF #neurociencia #didatico #d2 #e1 #tenho-digital |
| Neuropsicologia | Katia Dumard | #NF #neurociencia #d2 #e2 #tenho-digital |
| Neuropsicologia: Aplicações Clínicas | Leandro F. Malloy-Diniz e outros (orgs.) | #NF #neurociencia #didatico #BR #d3 #e2 #tenho-digital |
| Neuropsicologia Clínica | Alfredo Ardila | #NF #neurociencia #d3 #e2 #tenho-digital |
| Neuropsicologia do Desenvolvimento: Infância e Adolescência | Jerusa Fumagalli de Salles e Vitor Geraldi Haase | #NF #neurociencia #BR #d3 #e2 #tenho-digital |
| Neuropsicologia Forense | Andrea Stracciari e Angelo Bianchi | #NF #neurociencia #d3 #e2 #tenho-digital |
| Neuropsicologia Forense | Antonio de Pádua Serafim e Fabiana Saffi | #NF #neurociencia #BR #d3 #e2 #tenho-digital |
| Neuropsicologia Hoje | Flávia Heloísa dos Santos e outros (orgs.) | #NF #neurociencia #BR #d3 #e2 #tenho-digital |
| Neuropsicologia sem Neura: Uma Introdução à Neuropsicologia para Curiosos | Bruno Santos Souza e Camila Nogueira Marchetti | #NF #neurociencia #introducao #BR #d1 #e1 #tenho-digital |
| Neuropsicologia: Teoria e Prática | Daniel Fuentes e outros (orgs.) | #NF #neurociencia #didatico #BR #d3 #e2 #tenho-digital |
| O Cérebro Imperfeito | Dean Buonomano | #NF #neurociencia #d1 #e2 #tenho-digital |
| O Cérebro Leitor | Maryanne Wolf | #NF #psicologia #neurociencia #linguagem #educacao #d2 #e2 #tenho-digital |
| O Cérebro no Mundo Digital | Maryanne Wolf | #NF #psicologia #neurociencia #tecnologia #educacao #d2 #e2 #tenho-digital |
| O Cérebro Quântico: As Novas Descobertas da Neurociência e a Próxima Geração de Seres Humanos | Jeffrey Satinover | #NF #ciencia #fisica #neurociencia #consciencia #d2 #e2 #tenho-digital |
| O Cérebro que Não Sabia de Nada | Dean Burnett | #NF #neurociencia #humor #d1 #e2 #tenho-digital |
| O Estilo Emocional do Cérebro | Richard J. Davidson e Sharon Begley | #NF #psicologia #neurociencia #d1 #e2 #tenho-digital |
| O Futuro da Mente: A Busca Científica para Entender, Aprimorar e Potencializar a Mente | Michio Kaku | #NF #neurociencia #ciencia #d1 #e2 #tenho-digital |
| O Mistério da Consciência | António Damásio | #NF #neurociencia #consciencia #d3 #e2 #tenho-digital |
| O Olhar da Mente | Oliver Sacks | #NF #neurociencia #d1 #e2 #tenho-digital |
| O Oráculo da Noite: A História e a Ciência do Sonho | Sidarta Ribeiro | #NF #ciencia #neurociencia #historia #BR #d2 #e2 #tenho-digital |
| O Poder Curativo do Nervo Vago | Stanley Rosenberg | #NF #neurociencia #medicina #autoconhecimento #d1 #e2 #tenho-digital |
| O que o Cérebro Tem para Contar: Desvendando os Mistérios da Natureza Humana | V.S. Ramachandran | #NF #neurociencia #d2 #e3 #tenho-digital |
| Os Dragões do Éden | Carl Sagan | #NF #ciencia #neurociencia #biologia #classico #d2 #e2 #tenho-digital |
| Outras Mentes: O Polvo e a Origem da Consciência | Peter Godfrey-Smith | #NF #consciencia #biologia #filosofia #d2 #e2 #tenho-digital |
| Por que Guardar Segredo é Difícil e Outras Curiosidades da Neurociência do Cotidiano | Suzana Herculano-Houzel | #NF #ciencia #neurociencia #BR #d1 #e1 #tenho-digital |
| Por que Nós Dormimos: A Nova Ciência do Sono e do Sonho | Matthew Walker | #NF #ciencia #neurociencia #medicina #d1 #e2 #tenho-digital |
| Princípios de Neurociências | Eric R. Kandel e outros | #NF #neurociencia #didatico #d3 #e3 #tenho-digital |
| Psicologia Cognitiva | Robert J. Sternberg | #NF #psicologia #didatico #d3 #e3 #tenho-digital |
| Racionalidade: O que é, por que Parece Estar em Falta, por que é Importante | Steven Pinker | #NF #psicologia #ciencia #d2 #e2 #tenho-digital |
| Sentir e Saber | António Damásio | #NF #neurociencia #consciencia #d2 #e1 #tenho-digital |
| Sexo na Cabeça | Kayt Sukel | #NF #psicologia #neurociencia #d1 #e2 #tenho-digital |
| Subliminar: Como o Inconsciente Influencia Nossas Vidas | Leonard Mlodinow | #NF #psicologia #neurociencia #d1 #e2 #tenho-digital |
| Tipos de Mentes: Rumo a uma Compreensão da Consciência | Daniel C. Dennett | #NF #filosofia #consciencia #d2 #e1 #tenho-digital |
| Um Preço Muito Alto: A Jornada de um Neurocientista que Desafia Nossa Visão sobre Drogas | Carl Hart | #NF #neurociencia #politica #biografia #d1 #e2 #tenho-digital |
| Viagem Extraordinária ao Centro do Cérebro | Jean-Didier Vincent | #NF #ciencia #neurociencia #d2 #e2 #tenho-digital |

### 17.11 Política, poder, autoritarismo e economia

| Título | Autor | Tags |
|---|---|---|
| 17 Contradições e o Fim do Capitalismo | David Harvey | #NF #politica #economia #d3 #e2 #tenho-digital |
| 8 Estratégias de Marketing para Crescer: Dicas Práticas para Desenvolver seu Negócio | Philip Kotler e Milton Kotler | #NF #gestao #d1 #e1 #tenho-digital |
| A Arte da Inteligência: Os Bastidores da CIA e do FBI | Henry A. Crumpton | #NF #geopolitica #biografia #d1 #e2 #tenho-digital |
| A Arte da Quarentena para Principiantes | Christian Dunker | #NF #politica #psicanalise #BR #d1 #e1 #tenho-digital |
| A Cidade Inteligente: Tecnologias Urbanas e Democracia | Evgeny Morozov | #NF #tecnologia #politica #d2 #e1 #tenho-digital |
| A Curvatura da Banana: Quem Tem um Projeto de Nação para o Brasil? | Marcos Costa | #NF #politica #BR #d1 #e2 #tenho-digital |
| A Diplomacia na Construção do Brasil: 1750–2016 | Rubens Ricupero | #NF #politica #historia #geopolitica #BR #d3 #e3 #tenho-digital |
| A Era da Ilusão: A Diplomacia Nuclear em Tempos Traiçoeiros | Mohamed ElBaradei | #NF #politica #geopolitica #d2 #e2 #tenho-digital |
| A Globalização da Comunicação | Armand Mattelart | #NF #politica #sociologia #d2 #e1 #tenho-digital |
| A Invisibilidade da Desigualdade Brasileira | Jessé Souza (org.) | #NF #politica #sociologia #BR #d3 #e2 #tenho-digital |
| A Jornada do Empreendedor: O Herói da Nossa Era | Edson Marqueto Rigonatti, Laura Mello Constantini e Martino Bagini | #NF #gestao #d1 #e2 #tenho-digital |
| A Medida do Possível: Saúde, Risco e Tecnobiociências | Luis David Castiel | #NF #politica #medicina #sociologia #BR #d3 #e2 #tenho-digital |
| A Mídia | Noam Chomsky | #NF #politica #d1 #e1 #tenho-digital |
| A Passo de Caranguejo: Guerras Quentes e o Populismo da Mídia | Umberto Eco | #NF #politica #cronicas #d1 #e2 #tenho-digital |
| A Política no Banco dos Réus | Fábio Kerche e Marjorie Marona | #NF #politica #BR #d2 #e2 #tenho-digital |
| A Questão Palestina: Guerra, Política e Relações Internacionais | Marcelo Buzetto | #NF #politica #geopolitica #d2 #e1 #tenho-digital |
| A Sociedade Anárquica | Hedley Bull | #NF #politica #geopolitica #classico #d3 #e2 #tenho-digital |
| À Sombra do Poder: Bastidores da Crise que Derrubou Dilma Rousseff | Rodrigo de Almeida | #NF #politica #BR #d1 #e2 #tenho-digital |
| A Vida Não é Útil | Ailton Krenak | #NF #politica #ecologia #BR #d1 #e1 #trilha-entender-o-presente #tenho-digital |
| Administração de Serviços: Operações, Estratégia e Tecnologia da Informação | James A. Fitzsimmons e Mona J. Fitzsimmons | #NF #tecnologia #gestao #didatico #d3 #e3 #tenho-digital |
| África: Geohistória, Geopolítica e Relações Internacionais | Therezinha de Castro | #NF #politica #geopolitica #BR #africa #d2 #e2 #tenho-digital |
| Antologia da Maldade: Um Dicionário de Citações, Associações Ilícitas e Ligações Perigosas | Gustavo H.B. Franco e Fabio Giambiagi | #NF #politica #economia #humor #BR #d1 #e2 #tenho-digital |
| As Armas da Crítica | Emir Sader e Ivana Jinkings (orgs.) | #NF #politica #classico #d3 #e2 #tenho-digital |
| As Ideias Conservadoras | João Pereira Coutinho | #NF #politica #d1 #e1 #tenho-digital |
| As Transições e os Choques: O que Aprendemos e o que Ainda Temos de Aprender com a Crise Financeira | Martin Wolf | #NF #politica #economia #d3 #e3 #tenho-digital |
| Bala Perdida: A Violência Policial no Brasil e os Desafios para sua Superação | Bernardo Kucinski e outros | #NF #politica #BR #d1 #e1 #tenho-digital |
| Brasil dos Humilhados: Uma Denúncia da Ideologia Elitista | Jessé Souza | #NF #politica #sociologia #BR #d2 #e1 #tenho-digital |
| Brasil: Mito Fundador e Sociedade Autoritária | Marilena Chaui | #NF #politica #autoritarismo #BR #d2 #e1 #tenho-digital |
| Brasil: Os Frutos da Guerra | Neill Lochery | #NF #politica #historia #guerra #BR #d2 #e2 #tenho-digital |
| Brasil: Raízes do Atraso | Fabio Giambiagi | #NF #politica #economia #BR #d2 #e2 #tenho-digital |
| Carcereiros | Drauzio Varella | #NF #politica #testemunho #BR #d1 #e1 #tenho-digital |
| Cidades Rebeldes | Slavoj Žižek e outros | #NF #politica #BR #d2 #e1 #tenho-digital |
| Collected Papers, vol. 1: Technology, War and Fascism | Herbert Marcuse | #NF #politica #filosofia #d3 #e2 #tenho-digital |
| Colonialismo Digital: Por uma Crítica Hacker-Fanoniana | Deivison Faustino e Walter Lippold | #NF #politica #tecnologia #colonialismo #BR #d2 #e1 #tenho-digital |
| Comando Vermelho | Carlos Amorim | #NF #politica #BR #d1 #e2 #tenho-digital |
| Comece pelo Porquê | Simon Sinek | #NF #autoconhecimento #gestao #d1 #e2 #tenho-digital |
| Como a Democracia Chega ao Fim | David Runciman | #NF #politica #d2 #e2 #tenho-digital |
| Como as Democracias Morrem | Steven Levitsky e Daniel Ziblatt | #NF #politica #autoritarismo #d1 #e2 #trilha-entender-o-presente #tenho-digital |
| Como Esmagar o Fascismo | Leon Trotsky | #NF #politica #autoritarismo #classico #d2 #e1 #tenho-digital |
| Como Morrem os Pobres e Outros Ensaios | George Orwell | #NF #politica #cronicas #classico #d1 #e2 #tenho-digital |
| Como o Mundo Funciona: Um Guia Científico para o Passado, o Presente e o Futuro | Vaclav Smil | #NF #politica #ciencia #economia #d2 #e2 #tenho-digital |
| Complexo de Vira-Lata: Análise da Humilhação Brasileira | Marcia Tiburi | #NF #politica #BR #d2 #e1 #tenho-digital |
| Contágio: Por que as Coisas Pegam | Jonah Berger | #NF #gestao #psicologia #d1 #e2 #tenho-digital |
| Crash: Uma Breve História da Economia | Alexandre Versignassi | #NF #politica #economia #historia #BR #d1 #e2 #tenho-digital |
| Cultura Gaúcha e Separatismo no Rio Grande do Sul | Caroline Kraus Luvizotto | #NF #politica #sociologia #BR #RS #d2 #e1 #tenho-digital |
| Democracia em Colapso? | Marilena Chaui, Antonio Carlos Mazzeo e outros | #NF #politica #BR #d2 #e2 #tenho-digital |
| Democracia em Risco? 22 Ensaios sobre o Brasil Hoje | Vários autores | #NF #politica #BR #d2 #e2 #tenho-digital |
| Democracia Participativa e as Novas Tecnologias de Informação e Comunicação: Desafios e Perspectivas | Maurício Gentil Monteiro | #NF #tecnologia #politica #d2 #e2 #tenho-digital |
| Dicionário da República | Lilia Schwarcz e Heloisa Starling (orgs.) | #NF #politica #historia #BR #d2 #e3 #tenho-digital |
| Diplomacia, Diplomatas e Política Externa: Aspectos do Processo de Institucionalização do Itamaraty | Zairo Borges Cheibub | #NF #politica #geopolitica #BR #d3 #e2 #tenho-digital |
| Direita e Esquerda: Razões e Significados de uma Distinção Política | Norberto Bobbio | #NF #politica #classico #d2 #e1 #tenho-digital |
| Discurso sobre a Origem da Desigualdade entre os Homens | Jean-Jacques Rousseau | #NF #politica #filosofia #classico #d2 #e1 #tenho-digital |
| Do Povo para o Povo: Uma Nova História da Democracia | Roger Osborne | #NF #politica #historia #d2 #e2 #tenho-digital |
| Economia Política Internacional: Fundamentos Teóricos e as Relações Internacionais do Brasil | Reinaldo Gonçalves | #NF #politica #economia #geopolitica #BR #d3 #e2 #tenho-digital |
| Einstein, Freud e Relações Internacionais: Guerra e Paz num Diálogo Interdisciplinar | Luis Henrique Beust | #NF #geopolitica #psicanalise #d2 #e1 #verificar #tenho-digital |
| Energia e Civilização: Uma História | Vaclav Smil | #NF #politica #historia #ciencia #economia #d3 #e3 #tenho-digital |
| Engenharia Social | (autor não informado) | #NF #politica #d2 #e2 #verificar #tenho-digital |
| Eros e Civilização | Herbert Marcuse | #NF #politica #filosofia #psicanalise #classico #d3 #e2 #tenho-digital |
| Escritos Políticos | Frantz Fanon | #NF #politica #colonialismo #raca #d2 #e2 #tenho-digital |
| Estado e Forma Política | Alysson Leandro Mascaro | #NF #politica #filosofia #BR #d3 #e1 #tenho-digital |
| Falando de Política sem Politiquês | Carlito Neto | #NF #politica #introducao #BR #d1 #e1 #tenho-digital |
| Freakonomics: O Lado Oculto e Inesperado de Tudo que nos Afeta | Steven D. Levitt e Stephen J. Dubner | #NF #politica #economia #d1 #e2 #tenho-digital |
| Geografia e Geopolítica da América do Sul: Integrações e Conflitos | Wanderley Messias da Costa e Daniel Bruno Vasconcelos | #NF #politica #geopolitica #latam #d3 #e2 #tenho-digital |
| Geografia e Geopolítica: Ensaios e Resenhas | José William Vesentini | #NF #politica #geopolitica #BR #d2 #e2 #tenho-digital |
| Geografia Política e Geopolítica: Discursos sobre o Território e o Poder | Wanderley Messias da Costa | #NF #politica #geopolitica #BR #d3 #e2 #tenho-digital |
| Geopolítica da Rússia Contemporânea | Aleksandr Dugin | #NF #politica #geopolitica #d3 #e2 #tenho-digital |
| Geopolítica: Do Pensamento Clássico aos Conflitos Contemporâneos | Augusto W.M. Teixeira Júnior | #NF #politica #geopolitica #d3 #e2 #tenho-digital |
| Geopolítica e Política Exterior: Estados Unidos, Brasil e América do Sul | Luiz Alberto Moniz Bandeira | #NF #politica #geopolitica #BR #latam #d3 #e3 #tenho-digital |
| Gestão de Mudanças Organizacionais na Prática | Lorena Peixoto de Sousa (org.) | #NF #gestao #d2 #e2 #tenho-digital |
| Gestão de Processos | Fabiano Gonçalves dos Santos | #NF #gestao #d2 #e1 #tenho-digital |
| Gestão de Recursos Humanos: Ontem, Hoje e Amanhã | Allan Claudius Queiroz Barbosa e André Ofenhejm Mascarenhas | #NF #gestao #d2 #e2 #tenho-digital |
| Gestão Estratégica de Pessoas: Evolução, Teoria e Crítica | André Ofenhejm Mascarenhas | #NF #gestao #d3 #e2 #tenho-digital |
| Globalização: As Consequências Humanas | Zygmunt Bauman | #NF #politica #sociologia #d2 #e1 #tenho-digital |
| Golpe de Estado: O Espírito e a Herança de 1964 Ainda Ameaçam o Brasil | Palmério Dória e Mylton Severiano | #NF #politica #historia #autoritarismo #BR #d1 #e2 #tenho-digital |
| Gramsci, Materialismo Histórico e Relações Internacionais | Stephen Gill | #NF #politica #geopolitica #d3 #e3 #tenho-digital |
| História da Paz | Demétrio Magnoli | #NF #politica #historia #geopolitica #d2 #e3 #tenho-digital |
| História das Guerras | Demétrio Magnoli | #NF #politica #historia #guerra #d2 #e3 #tenho-digital |
| História das Relações Internacionais Contemporâneas | José Flávio Sombra Saraiva (org.) | #NF #politica #historia #geopolitica #d3 #e2 #tenho-digital |
| História das Relações Internacionais do Brasil | Francisco Doratioto e Carlos Vidigal | #NF #politica #geopolitica #historia #BR #d2 #e2 #tenho-digital |
| História das Relações Internacionais I: A Pax Britannica e o Mundo do Século XIX | Antônio Carlos Lessa | #NF #politica #geopolitica #historia #d2 #e1 #tenho-digital |
| História das Relações Internacionais II: O Século XX, do Declínio Europeu à Era Global | Christian Lohbauer | #NF #politica #geopolitica #historia #d2 #e1 #tenho-digital |
| História das Relações Internacionais: Teorias e Processos | Mônica Leite Lessa e Williams da Silva Gonçalves | #NF #politica #geopolitica #historia #d2 #e2 #tenho-digital |
| Homens em Tempos Sombrios | Hannah Arendt | #NF #politica #biografia #filosofia #d3 #e2 #tenho-digital |
| La Piel de la Cultura | Derrick de Kerckhove | #NF #politica #tecnologia #sociologia #d2 #e2 #tenho-digital |
| Liberdade para Ser Livre | Hannah Arendt | #NF #politica #filosofia #d2 #e1 #tenho-digital |
| Liderança: Seus Primeiros Passos para Ser o Líder | Frederico Aranha e Jefferson Lisboa Melo | #NF #autoconhecimento #gestao #BR #d1 #e1 #tenho-digital |
| Liderar a Mudança | John P. Kotter | #NF #gestao #d1 #e1 #tenho-digital |
| Manifestações Ideológicas do Autoritarismo Brasileiro | Marilena Chaui | #NF #politica #autoritarismo #BR #d3 #e2 #tenho-digital |
| Manual de Filosofia Política: A História do Pensamento Político Ocidental | Hugo Brandão | #NF #politica #filosofia #introducao #d2 #e2 #tenho-digital |
| Marketing 4.0 | Philip Kotler, Hermawan Kartajaya e Iwan Setiawan | #NF #tecnologia #gestao #d1 #e1 #tenho-digital |
| Marketing 5.0: Tecnologia para a Humanidade | Philip Kotler, Hermawan Kartajaya e Iwan Setiawan | #NF #tecnologia #gestao #d1 #e2 #tenho-digital |
| Marx: Uma Biografia em Quadrinhos | Corinne Maier e Anne Simon | #HQ #biografia #politica #d1 #e1 #tenho-digital |
| Mensalão: O Julgamento do Maior Caso de Corrupção da História Política Brasileira | Merval Pereira | #NF #politica #BR #d1 #e2 #tenho-digital |
| Multilateralismo nas Relações Internacionais | Elena Lazarou | #NF #politica #geopolitica #d2 #e1 #tenho-digital |
| Neuromarketing | Darren Bridger | #NF #gestao #psicologia #neurociencia #d1 #e2 #tenho-digital |
| O Brasil no Espectro de uma Guerra Híbrida | Piero C. Leirner | #NF #politica #geopolitica #BR #d3 #e2 #tenho-digital |
| O Capital em Quadrinhos, vol. 1 | K. Ploeckinger e G. Wolfram | #HQ #economia #politica #introducao #adaptacao #d1 #e1 #tenho-digital |
| O Capital para Crianças | Liliana Fortuny e Joan Riera | #NF #politica #economia #d1 #e1 #tenho-digital |
| O Espetáculo da Corrupção: Como um Sistema Corrupto e o Modo de Combatê-lo Estão Destruindo o País | Walfrido Warde | #NF #politica #BR #d2 #e2 #tenho-digital |
| O Fim da Guerra: A Maconha e a Criação de um Novo Sistema para Lidar com as Drogas | Denis Russo Burgierman | #NF #politica #BR #d1 #e2 #tenho-digital |
| O Futuro da Geografia: Como o Poder e a Política no Espaço Transformarão o Mundo | Tim Marshall | #NF #geopolitica #politica #d1 #e2 #tenho-digital |
| O Grande Debate: Edmund Burke, Thomas Paine e o Nascimento da Esquerda e da Direita | Yuval Levin | #NF #politica #filosofia #historia #d2 #e2 #tenho-digital |
| O Grande Experimento | Marcel Novaes | #NF #politica #historia #d2 #e2 #tenho-digital |
| O Livro da Economia | Vários autores | #NF #introducao #economia #d1 #e2 #tenho-digital |
| O Livro da Política | Vários autores | #NF #introducao #politica #d1 #e2 #tenho-digital |
| O Livro de Ouro das Revoluções: Movimentos Políticos que Mudaram o Mundo | Mark Almond | #NF #politica #historia #d1 #e2 #tenho-digital |
| O Livro dos Negócios | Vários autores | #NF #introducao #economia #gestao #d1 #e2 #tenho-digital |
| O Livro Urgente da Política Brasileira | Alessandro Nicoli de Mattos | #NF #politica #introducao #BR #d1 #e2 #tenho-digital |
| O Minotauro Global: A Verdadeira Origem da Crise Financeira e o Futuro da Economia Global | Yanis Varoufakis | #NF #politica #economia #d2 #e2 #tenho-digital |
| O Mundo em 2050: As Grandes Tendências Globais e o que Podemos Esperar do Futuro | Hamish McRae | #NF #politica #economia #d1 #e2 #tenho-digital |
| O Negócio do Jair | Juliana Dal Piva | #NF #politica #BR #d1 #e2 #tenho-digital |
| O Ódio à Democracia | Jacques Rancière | #NF #politica #filosofia #d3 #e1 #tenho-digital |
| O Populismo Reacionário: Ascensão e Legado do Bolsonarismo | Christian Lynch e Paulo Henrique Cassimiro | #NF #politica #autoritarismo #BR #d2 #e2 #tenho-digital |
| O Povo contra a Democracia: Por que Nossa Liberdade Corre Perigo e como Salvá-la | Yascha Mounk | #NF #politica #autoritarismo #d2 #e2 #tenho-digital |
| O Retorno do Pêndulo: Sobre a Psicanálise e o Futuro do Mundo Líquido | Zygmunt Bauman e Gustavo Dessal | #NF #politica #psicanalise #sociologia #d2 #e1 #tenho-digital |
| O Sujeito Incômodo: O Centro Ausente da Ontologia Política | Slavoj Žižek | #NF #politica #filosofia #psicanalise #d3 #e3 #tenho-digital |
| Ordem e Decadência Política: Da Revolução Industrial à Globalização da Democracia | Francis Fukuyama | #NF #politica #historia #d2 #e3 #tenho-digital |
| Os Argentinos | Ariel Palacios | #NF #politica #latam #d1 #e2 #tenho-digital |
| Os Arquivos Snowden: A História Secreta do Homem Mais Procurado do Mundo | Luke Harding | #NF #politica #tecnologia #d1 #e2 #tenho-digital |
| Os Clássicos da Política | Francisco C. Weffort (org.) | #NF #politica #filosofia #didatico #classico #d2 #e2 #tenho-digital |
| Os Engenheiros do Caos | Giuliano da Empoli | #NF #politica #tecnologia #autoritarismo #d1 #e1 #trilha-entender-o-presente #tenho-digital |
| Os Líderes e as Massas: Escritos de 1921 a 1926 | Antonio Gramsci | #NF #politica #classico #d3 #e2 #tenho-digital |
| Palestina | Joe Sacco | #HQ #politica #guerra #testemunho #d2 #e2 #trilha-quadrinhos-para-gente-grande #tenho-digital |
| Partidos Políticos no Brasil (1945-2000) | Rogerio Augusto Schmitt | #NF #politica #BR #d2 #e1 #tenho-digital |
| Pepe Mujica: Simplesmente Humano | Allan Percy | #NF #politica #biografia #latam #d1 #e1 #tenho-digital |
| Política: Conceitos-Chave em Filosofia | Iain Mackenzie | #NF #politica #filosofia #introducao #d2 #e2 #tenho-digital |
| Política: Nós Também Sabemos Fazer | Clóvis de Barros Filho | #NF #politica #BR #d1 #e1 #tenho-digital |
| Política: Para Não Ser Idiota | Mario Sergio Cortella e Renato Janine Ribeiro | #NF #politica #BR #d1 #e1 #tenho-digital |
| Políticas e Sistema de Saúde no Brasil | Lígia Giovanella e outros (orgs.) | #NF #politica #medicina #didatico #BR #d3 #e3 #tenho-digital |
| Ponto-final | Marcos Nobre | #NF #politica #BR #d1 #e1 #tenho-digital |
| Populismo e Negacionismo | Uriã Fancelli | #NF #politica #autoritarismo #BR #d2 #e1 #tenho-digital |
| Por uma Outra Globalização: Do Pensamento Único à Consciência Universal | Milton Santos | #NF #politica #geopolitica #economia #BR #d2 #e1 #tenho-digital |
| Princípios de Marketing | Philip Kotler e Gary Armstrong | #NF #gestao #didatico #d2 #e3 #tenho-digital |
| Psicologia do Bolsonarismo: Por que Tantas Pessoas se Curvam ao Mito | Diogo Bogéa | #NF #politica #psicologia #autoritarismo #BR #d2 #e1 #tenho-digital |
| Quem Sabe Faz a Hora!: Iniciativas Decisivas para Gestão e Liderança | Mario Sergio Cortella | #NF #autoconhecimento #gestao #BR #d1 #e1 #tenho-digital |
| Quem Tem Medo da Geopolítica? | Leonel Itaussu Almeida Mello | #NF #politica #geopolitica #BR #d2 #e1 #tenho-digital |
| Racismo e Cultura | Frantz Fanon | #NF #politica #raca #colonialismo #d2 #e1 #tenho-digital |
| Racismo Estrutural | Silvio Almeida | #NF #politica #raca #BR #d2 #e1 #tenho-digital |
| Rap e Política: Percepções da Vida Social Brasileira | Roberto Camargos | #NF #politica #arte #BR #d2 #e1 #tenho-digital |
| Reflexões sobre a Peste: Ensaios em Tempos de Pandemia | Giorgio Agamben | #NF #politica #filosofia #d2 #e1 #tenho-digital |
| Reflexões sobre a Revolução na França | Edmund Burke | #NF #politica #historia #filosofia #classico #d3 #e2 #tenho-digital |
| Relações Internacionais do Mundo Árabe: Os Desafios para a Realização da Utopia Pan-Arabista | Silvia Regina Ferabolli | #NF #politica #geopolitica #d3 #e2 #tenho-digital |
| Relações Internacionais: Olhares Cruzados | Corival Alves do Carmo e outros (orgs.) | #NF #politica #geopolitica #d2 #e2 #tenho-digital |
| Relações Internacionais: Perspectivas Francesas | Carlos R.S. Milani (org.) | #NF #politica #geopolitica #d3 #e2 #tenho-digital |
| Relações Internacionais: Teoria e História | Demétrio Magnoli | #NF #politica #geopolitica #historia #d2 #e2 #tenho-digital |
| Simulacro e Poder: Uma Análise da Mídia | Marilena Chaui | #NF #politica #BR #d2 #e1 #tenho-digital |
| Tecnofeudalismo | Yanis Varoufakis | #NF #politica #economia #tecnologia #d2 #e2 #tenho-digital |
| Teoria das Relações Internacionais | Thales Castro | #NF #politica #geopolitica #didatico #d2 #e3 #tenho-digital |
| Teorias da Comunicação de Massa | Melvin DeFleur e Sandra Ball-Rokeach | #NF #politica #sociologia #d3 #e2 #tenho-digital |
| Teorias das Relações Internacionais: Correntes e Debates | João Pontes Nogueira e Nizar Messari | #NF #politica #geopolitica #didatico #d2 #e2 #tenho-digital |
| Terrorismo Ocidental | Noam Chomsky e Andre Vltchek | #NF #politica #geopolitica #d1 #e1 #tenho-digital |
| Todo Império Perecerá: Teoria das Relações Internacionais | Jean-Baptiste Duroselle | #NF #politica #geopolitica #historia #d3 #e3 #tenho-digital |
| Tormenta | Thaís Oyama | #NF #politica #BR #d1 #e2 #tenho-digital |
| Trabalho e Mundialização do Capital: A Nova Degradação do Trabalho na Era da Globalização | Giovanni Alves | #NF #politica #economia #sociologia #BR #d3 #e2 #tenho-digital |
| Tudo o que Você Precisou Desaprender para Virar um Idiota | Meteoro Brasil | #NF #politica #BR #d1 #e2 #tenho-digital |
| Um País Partido: 2014, a Eleição Mais Suja da História | Marco Antonio Villa | #NF #politica #BR #d1 #e2 #tenho-digital |
| Uma Ecologia Decolonial | Malcom Ferdinand | #NF #politica #ecologia #colonialismo #raca #d3 #e2 #tenho-digital |

### 17.12 Sociedade, antropologia, cultura e história

| Título | Autor | Tags |
|---|---|---|
| 100 Mistérios da Humanidade | National Geographic | #NF #historia #enigmas #d1 #e2 #tenho-digital |
| 1964: Visões Críticas do Golpe | Caio Navarro de Toledo (org.) | #NF #historia #autoritarismo #politica #BR #d2 #e2 #tenho-digital |
| 44 Cartas do Mundo Líquido Moderno | Zygmunt Bauman | #NF #sociologia #d1 #e1 #trilha-entender-o-presente #tenho-digital |
| 50 Grandes Ideias da Humanidade que Você Precisa Conhecer | Ben Dupré | #NF #historia #introducao #filosofia #d1 #e2 #tenho-digital |
| 50 Pensadores que Formaram o Mundo Moderno | Stephen Trombley | #NF #historia #filosofia #introducao #d2 #e2 #tenho-digital |
| A Biblioteca Desaparecida | Luciano Canfora | #NF #historia #antiguidade #d2 #e1 #tenho-digital |
| A Conquista da América | Tzvetan Todorov | #NF #historia #colonialismo #classico #latam #d3 #e2 #tenho-digital |
| A Cultura do Narcisismo | Christopher Lasch | #NF #psicologia #sociologia #classico #d3 #e2 #tenho-digital |
| A Elite do Atraso: Da Escravidão à Lava Jato | Jessé Souza | #NF #historia #sociologia #politica #BR #d2 #e2 #tenho-digital |
| A Fabulosa História do Hospital: Da Idade Média aos Dias de Hoje | Jean-Noël Fabiani | #NF #historia #medicina #d1 #e2 #tenho-digital |
| A Guardiã de Todas as Coisas | Michael S. Malone | #NF #historia #memoria #ciencia #d2 #e2 #tenho-digital |
| A História da Ciência para Quem Tem Pressa | Nicola Chalton e Meredith MacArdle | #NF #historia #introducao #ciencia #d1 #e1 #tenho-digital |
| A História da Humanidade | Hendrik Willem van Loon | #NF #historia #classico #d1 #e3 #tenho-digital |
| A História do Brasil para Quem Tem Pressa | Marcos Costa | #NF #historia #introducao #BR #d1 #e1 #tenho-digital |
| A História do Cinema para Quem Tem Pressa | Celso Sabadin | #NF #historia #introducao #cinema #d1 #e1 #tenho-digital |
| A História do Mundo para Quem Tem Pressa | Emma Marriott | #NF #historia #introducao #d1 #e1 #tenho-digital |
| A História do Século 20 para Quem Tem Pressa | Nicola Chalton e Meredith MacArdle | #NF #historia #introducao #d1 #e1 #tenho-digital |
| A História do Universo para Quem Tem Pressa | Colin Stuart | #NF #historia #introducao #ciencia #d1 #e1 #tenho-digital |
| A História e suas Epidemias: A Convivência do Homem com os Microorganismos | Stefan Cunha Ujvari | #NF #historia #medicina #d2 #e2 #tenho-digital |
| A História Secreta da Raça Humana | Michael A. Cremo e Richard L. Thompson | #NF #historia #enigmas #d2 #e2 #tenho-digital |
| A Mais Breve História da Europa | John Hirst | #NF #historia #introducao #d1 #e1 #tenho-digital |
| A Maldição da Noz-Moscada | Amitav Ghosh | #NF #historia #colonialismo #ecologia #d2 #e2 #tenho-digital |
| A Máquina de Uriel | Robert Lomas | #NF #historia #mistica #enigmas #d2 #e2 #tenho-digital |
| A Medida do Mundo | Robert P. Crease | #NF #historia #ciencia #d2 #e2 #tenho-digital |
| A Terra Dá, a Terra Quer | Antonio Bispo dos Santos | #NF #raca #ecologia #antropologia #BR #d1 #e1 #tenho-digital |
| A Vida Louca dos Revolucionários | Demétrio Magnoli | #NF #historia #biografia #politica #d1 #e2 #tenho-digital |
| A Virada | Stephen Greenblatt | #NF #historia #renascimento #filosofia #d2 #e2 #tenho-digital |
| Análise de Discurso Crítica e Comunicação: Percursos Teórico e Pragmático de Discurso, Mídia e Política | Laerte Magalhães | #NF #linguagem #politica #d3 #e2 #tenho-digital |
| Análise de Discurso: Princípios e Procedimentos | Eni Orlandi | #NF #linguagem #didatico #d2 #e1 #tenho-digital |
| Antropologia Cultural | Franz Boas | #NF #antropologia #classico #d2 #e1 #tenho-digital |
| Antropologia da Criança | Clarice Cohn | #NF #antropologia #introducao #BR #d1 #e1 #tenho-digital |
| Antropologia da Política | Karina Kuschnir | #NF #antropologia #politica #introducao #BR #d2 #e1 #tenho-digital |
| Antropologia e Imagem | Andrea Barbosa | #NF #antropologia #arte #introducao #BR #d2 #e1 #tenho-digital |
| Antropologia e Nutrição: Um Diálogo Possível | Ana Maria Canesqui e Rosa Wanda Diez Garcia (orgs.) | #NF #antropologia #medicina #BR #d3 #e2 #tenho-digital |
| Antropologia Estrutural | Claude Lévi-Strauss | #NF #antropologia #classico #d3 #e2 #tenho-digital |
| Aprendendo a Pensar com a Sociologia | Zygmunt Bauman | #NF #sociologia #introducao #d2 #e2 #tenho-digital |
| As 100 Maiores Catástrofes da História | Stephen J. Spignesi | #NF #historia #introducao #d1 #e2 #tenho-digital |
| As 100 Maiores Invenções da História: Uma Classificação Cronológica | Tom Philbin | #NF #historia #introducao #tecnologia #d1 #e2 #tenho-digital |
| As 100 Piores Ideias da História | Michael N. Smith e Eric Kasum | #NF #historia #introducao #humor #d1 #e2 #tenho-digital |
| As Relíquias Sagradas de Hitler | Sidney D. Kirkpatrick | #NF #historia #guerra #enigmas #d1 #e2 #tenho-digital |
| As Teorias da Comunicação | Francisco Rüdiger | #NF #sociologia #d2 #e2 #tenho-digital |
| Casa-Grande & Senzala em Quadrinhos | Gilberto Freyre | #HQ #adaptacao #historia #sociologia #BR #d1 #e1 #tenho-digital |
| Comunicação e Análise do Discurso | Roseli Figaro | #NF #linguagem #d2 #e2 #tenho-digital |
| Conceitos Essenciais da Sociologia | Anthony Giddens e Philip W. Sutton | #NF #sociologia #introducao #didatico #d2 #e2 #tenho-digital |
| De Pernas pro Ar | Eduardo Galeano | #NF #historia #politica #latam #d1 #e2 #tenho-digital |
| Evolucionismo Cultural | Celso Castro (org.) | #NF #antropologia #classico #d3 #e1 #tenho-digital |
| Futebol ao Sol e à Sombra | Eduardo Galeano | #NF #historia #esporte #latam #d1 #e2 #tenho-digital |
| Futuro Ancestral | Ailton Krenak | #NF #ecologia #antropologia #BR #d1 #e1 #tenho-digital |
| Grandes Mistérios da História: A Teoria da Conspiração e os Segredos por Trás dos Acontecimentos | Sérgio Pereira Couto | #NF #historia #enigmas #d1 #e1 #tenho-digital |
| Heróis da História | Will Durant | #NF #historia #biografia #d2 #e2 #tenho-digital |
| História da Vida | Edmac Lima Trigueiro | #NF #historia #d2 #e2 #tenho-digital |
| História da Vida Privada | Philippe Ariès e Georges Duby (orgs.) | #NF #historia #d3 #e3 #tenho-digital |
| História do Futuro: O Horizonte do Brasil no Século XXI | Míriam Leitão | #NF #historia #economia #politica #BR #d2 #e3 #tenho-digital |
| História do Mundo em 6 Copos | Tom Standage | #NF #historia #d1 #e2 #tenho-digital |
| Introdução à Antropologia | Igor Machado | #NF #antropologia #introducao #BR #d1 #e1 #tenho-digital |
| Introdução à Linguística, vol. 1: Domínios e Fronteiras | Fernanda Mussalim e Anna Christina Bentes (orgs.) | #NF #linguagem #didatico #d2 #e2 #tenho-digital |
| Introdução à Linguística, vol. 2: Domínios e Fronteiras | Fernanda Mussalim e Anna Christina Bentes (orgs.) | #NF #linguagem #didatico #d2 #e2 #tenho-digital |
| Introdução à Linguística, vol. 3: Fundamentos Epistemológicos | Fernanda Mussalim e Anna Christina Bentes (orgs.) | #NF #linguagem #didatico #d3 #e2 #tenho-digital |
| Linguagem: A História da Maior Invenção da Humanidade | Daniel L. Everett | #NF #linguagem #antropologia #d2 #e2 #tenho-digital |
| Linguagem, Discurso e Sociedade: Caminhos que se Entrecruzam | Vários autores | #NF #linguagem #sociologia #d2 #e2 #tenho-digital |
| Lutando na Espanha | George Orwell | #NF #historia #guerra #testemunho #politica #classico #d2 #e2 #tenho-digital |
| Manual de Sociologia da Religião | Roberto Cipriani | #NF #sociologia #religiao #d3 #e2 #tenho-digital |
| Meu Destino é Ser Onça | Alberto Mussa | #NF #mitologia #antropologia #BR #d2 #e2 #tenho-digital |
| Mulheres | Eduardo Galeano | #NF #historia #genero #latam #d1 #e1 #tenho-digital |
| Na Natureza Selvagem | Jon Krakauer | #NF #biografia #aventura #d1 #e1 #tenho-digital |
| O Fantasma Chinês | Christoph Giesen | #NF #historia #geopolitica #asia #d2 #e2 #tenho-digital |
| O Livro da História | Vários autores | #NF #introducao #historia #d1 #e2 #tenho-digital |
| O Livro da Sociologia | Vários autores | #NF #introducao #sociologia #d1 #e2 #tenho-digital |
| O Livro do Amor, vol. 1 | Regina Navarro Lins | #NF #historia #genero #BR #d2 #e2 #tenho-digital |
| O Mapa Fantasma | Steven Johnson | #NF #historia #medicina #ciencia #d1 #e2 #tenho-digital |
| O Nazista e o Psiquiatra | Jack El-Hai | #NF #historia #guerra #psiquiatria #d1 #e2 #tenho-digital |
| O Novo Iluminismo: Em Defesa da Razão, da Ciência e do Humanismo | Steven Pinker | #NF #ciencia #filosofia #historia #politica #d2 #e3 #tenho-digital |
| O Perigo de uma História Única | Chimamanda Ngozi Adichie | #NF #raca #africa #d1 #e1 #tenho-digital |
| O Poder da Identidade | Manuel Castells | #NF #sociologia #identidade #d3 #e3 #tenho-digital |
| Onde Nascem os Gênios | Eric Weiner | #NF #historia #biografia #d1 #e2 #tenho-digital |
| Os 100 Maiores Mistérios do Mundo: A Mais Completa Lista sobre Coisas Estranhas e Inexplicáveis | Stephen J. Spignesi | #NF #enigmas #d1 #e2 #tenho-digital |
| Os Crimes de Napoleão | Claude Ribbe | #NF #historia #colonialismo #raca #d2 #e1 #tenho-digital |
| Os Demônios de Loudun | Aldous Huxley | #NF #historia #religiao #d3 #e2 #tenho-digital |
| Para Toda a Eternidade | Caitlin Doughty | #NF #morte #antropologia #d1 #e2 #tenho-digital |
| Perdidos em Shangri-la | Mitchell Zuckoff | #NF #historia #guerra #aventura #d1 #e2 #tenho-digital |
| Questões Fundamentais da Sociologia: Indivíduo e Sociedade | Georg Simmel | #NF #sociologia #classico #d3 #e1 #tenho-digital |
| Sapiens (em quadrinhos) | Yuval Noah Harari, David Vandermeulen e Daniel Casanave | #HQ #historia #antropologia #adaptacao #d1 #e2 #tenho-digital |
| Ser Republicano no Brasil Colônia: A História de uma Tradição Esquecida | Heloisa Starling | #NF #historia #politica #BR #d3 #e2 #tenho-digital |
| Sociedades Secretas | Sérgio Pereira Couto | #NF #historia #enigmas #d1 #e1 #tenho-digital |
| Sociolinguística Interacional: Antropologia, Linguística e Sociologia em Análise do Discurso | Branca Telles Ribeiro e Pedro M. Garcez (orgs.) | #NF #antropologia #sociologia #linguagem #d3 #e2 #tenho-digital |
| Sociologia para Leigos | Jay Gabler | #NF #sociologia #introducao #d1 #e2 #tenho-digital |
| Sonho Manifesto: Dez Exercícios Urgentes de Otimismo Apocalíptico | Sidarta Ribeiro | #NF #politica #ecologia #BR #d1 #e1 #tenho-digital |
| Tesouros Medievais | (autor não informado) | #NF #historia #medieval #d2 #e2 #verificar #tenho-digital |
| Textos Básicos de Antropologia: Cem Anos de Tradição | Celso Castro (org.) | #NF #antropologia #didatico #d2 #e2 #tenho-digital |
| Textos Básicos de Sociologia: De Karl Marx a Zygmunt Bauman | Celso Castro (org.) | #NF #sociologia #didatico #d2 #e2 #tenho-digital |
| Titãs da História: Os Gigantes que Mudaram o Nosso Mundo | Simon Sebag Montefiore | #NF #historia #biografia #d1 #e3 #tenho-digital |
| Três Vezes Brasil | Alberto da Costa e Silva | #NF #historia #BR #d2 #e1 #tenho-digital |
| Tudo sobre o Amor | bell hooks | #NF #genero #d1 #e1 #tenho-digital |
| Uma Breve História da Linguagem | Steven Roger Fischer | #NF #linguagem #historia #d1 #e2 #tenho-digital |
| Uma Breve História do Conhecimento | Charles Van Doren | #NF #historia #d2 #e3 #tenho-digital |
| Uma Breve História do Homem: Progresso e Declínio | Hans-Hermann Hoppe | #NF #historia #politica #economia #d2 #e1 #tenho-digital |
| Uma Breve História do Mundo em 50 Animais | Jacob F. Field | #NF #historia #introducao #d1 #e2 #tenho-digital |
| Uma Breve História do Mundo em 50 Livros | Daniel Smith | #NF #historia #introducao #d1 #e2 #tenho-digital |
| Uma Breve História do Mundo em 50 Lugares | Jacob F. Field | #NF #historia #introducao #d1 #e2 #tenho-digital |
| Uma História Comestível da Humanidade | Tom Standage | #NF #historia #d1 #e2 #tenho-digital |
| Uma História do Mundo em Doze Mapas | Jerry Brotton | #NF #historia #ciencia #d3 #e3 #tenho-digital |

### 17.13 Ciência, tecnologia e futuro

| Título | Autor | Tags |
|---|---|---|
| 100 Coisas Essenciais que Não Sabia que Não Sabia: Perceba o Mundo Através da Matemática | John D. Barrow | #NF #ciencia #matematica #d1 #e2 #tenho-digital |
| 17 Equações que Mudaram o Mundo | Ian Stewart | #NF #ciencia #matematica #d2 #e2 #tenho-digital |
| 20 Episódios da História da Matemática: Dos Primeiros Artefatos à Invenção do Cálculo | Frederico Andries Lopes | #NF #ciencia #matematica #historia #BR #d2 #e1 #tenho-digital |
| 2041: Como a Inteligência Artificial Vai Mudar sua Vida nas Próximas Décadas | Kai-Fu Lee e Chen Qiufan | #NF #ia #tecnologia #d1 #e2 #trilha-maquinas-que-pensam #tenho-digital |
| 50 Ideias de Biologia que Você Precisa Conhecer | J.V. Chamary | #NF #ciencia #biologia #introducao #d1 #e1 #tenho-digital |
| 50 Ideias de Física Quântica | Joanne Baker | #NF #ciencia #fisica #introducao #d1 #e2 #tenho-digital |
| 60 Jogos para o Pensamento Lógico, vol. 1 | Aury de Sá Leite | #NF #matematica #didatico #d1 #e1 #tenho-digital |
| A Assustadora História da Medicina | Richard Gordon | #NF #ciencia #medicina #historia #humor #d1 #e2 #tenho-digital |
| A Ciência Médica de House | Andrew Holtz | #NF #ciencia #medicina #d1 #e2 #tenho-digital |
| A Conquista Social da Terra | Edward O. Wilson | #NF #ciencia #biologia #antropologia #d2 #e2 #tenho-digital |
| A Criação | Edward O. Wilson | #NF #ciencia #biologia #ecologia #religiao #d1 #e1 #tenho-digital |
| A Dança do Universo | Marcelo Gleiser | #NF #ciencia #fisica #historia #BR #d2 #e2 #trilha-do-quark-ao-cosmos #tenho-digital |
| A Dupla Hélice | James D. Watson | #NF #ciencia #biologia #biografia #classico #d1 #e1 #tenho-digital |
| A Era das Máquinas Espirituais | Ray Kurzweil | #NF #tecnologia #ia #d2 #e2 #tenho-digital |
| A Física do Futuro | Michio Kaku | #NF #ciencia #fisica #tecnologia #d1 #e2 #tenho-digital |
| A Guide to the Project Management Body of Knowledge (PMBOK Guide) | Project Management Institute | #NF #tecnologia #gestao #didatico #d3 #e3 #tenho-digital |
| A História da Ciência por seus Grandes Nomes | John Farndon | #NF #ciencia #historia #biografia #d1 #e2 #tenho-digital |
| A História da Humanidade Contada pelos Vírus | Stefan Cunha Ujvari | #NF #ciencia #medicina #historia #BR #d1 #e2 #tenho-digital |
| A Ilha do Conhecimento: Os Limites da Ciência e a Busca por Sentido | Marcelo Gleiser | #NF #ciencia #fisica #filosofia #BR #d2 #e2 #tenho-digital |
| A Impostura Científica em Dez Lições | Michel de Pracontal | #NF #ciencia #d2 #e2 #tenho-digital |
| A Incrível Viagem das Plantas | Stefano Mancuso | #NF #ciencia #biologia #ecologia #d1 #e1 #tenho-digital |
| A Inteligência Artificial | Wilson Luiz Sanvito | #NF #ia #tecnologia #BR #d2 #e1 #tenho-digital |
| A Invenção da Natureza | Andrea Wulf | #NF #ciencia #biografia #ecologia #historia #d2 #e3 #tenho-digital |
| A Magia da Realidade | Richard Dawkins | #NF #ciencia #biologia #d1 #e2 #tenho-digital |
| A Música dos Números Primos | Marcus du Sautoy | #NF #ciencia #matematica #d2 #e2 #tenho-digital |
| A Nova Era Tecnológica: Redes Sociais, Realidade Virtual e Inteligência Artificial | Caio Garrido | #NF #ia #BR #tecnologia #d1 #e1 #tenho-digital |
| A Próxima Onda: Inteligência Artificial, Poder e o Maior Dilema do Século XXI | Mustafa Suleyman e Michael Bhaskar | #NF #ia #politica #tecnologia #d2 #e2 #trilha-maquinas-que-pensam #tenho-digital |
| A Realidade Oculta: Universos Paralelos e as Leis Profundas do Cosmo | Brian Greene | #NF #ciencia #fisica #d3 #e2 #tenho-digital |
| A Singularidade Está Mais Próxima: A Fusão do Ser Humano com o Poder da Inteligência Artificial | Ray Kurzweil | #NF #ia #tecnologia #d2 #e3 #tenho-digital |
| A Vida no Limite: A Ciência da Sobrevivência | Frances M. Ashcroft | #NF #ciencia #biologia #medicina #d2 #e2 #tenho-digital |
| Administração de Banco de Dados | Fábio Caiut | #NF #tecnologia #dados #didatico #d2 #e2 #tenho-digital |
| Álgebra I para Leigos | Mary Jane Sterling | #NF #matematica #didatico #d1 #e2 #tenho-digital |
| Álgebra Linear e suas Aplicações | David C. Lay, Steven R. Lay e Judi J. McDonald | #NF #matematica #didatico #d3 #e3 #tenho-digital |
| Algoritmos: Teoria e Prática | Thomas H. Cormen e outros | #NF #tecnologia #programacao #didatico #d3 #e3 #tenho-digital |
| Alice no País do Quantum | Robert Gilmore | #NF #ciencia #fisica #introducao #d1 #e1 #tenho-digital |
| Amazon AWS: Descomplicando a Computação na Nuvem | Jonathan Lamim Antunes | #NF #tecnologia #programacao #d2 #e1 #tenho-digital |
| Análise e Projeto de Sistemas | (autor não informado) | #NF #tecnologia #programacao #didatico #d2 #e2 #verificar #tenho-digital |
| Aprenda Python Básico: Rápido e Fácil de Entender | Felipe Galvão | #NF #tecnologia #programacao #didatico #d1 #e1 #tenho-digital |
| Arquimedes e a Alavanca em 90 Minutos | Paul Strathern | #NF #introducao #ciencia #biografia #d1 #e1 #tenho-digital |
| Astrofísica para Apressados | Neil deGrasse Tyson | #NF #ciencia #fisica #d1 #e1 #trilha-do-quark-ao-cosmos #tenho-digital |
| Até o Fim do Tempo | Brian Greene | #NF #ciencia #fisica #d2 #e2 #trilha-do-quark-ao-cosmos #tenho-digital |
| Batendo à Porta do Céu | Lisa Randall | #NF #ciencia #fisica #d3 #e2 #tenho-digital |
| BI2: Business Intelligence | Carlos Barbieri | #NF #tecnologia #dados #gestao #d2 #e2 #tenho-digital |
| Big Data | Viktor Mayer-Schönberger e Kenneth Cukier | #NF #tecnologia #dados #d1 #e2 #tenho-digital |
| Big Data e Internet das Coisas | Larissa Kakizaki de Alcantara | #NF #tecnologia #dados #d2 #e1 #tenho-digital |
| Bilhões e Bilhões | Carl Sagan | #NF #ciencia #fisica #ecologia #d1 #e2 #tenho-digital |
| Bohr e a Teoria Quântica em 90 Minutos | Paul Strathern | #NF #introducao #ciencia #biografia #fisica #d1 #e1 #tenho-digital |
| Breves Respostas para Grandes Questões | Stephen Hawking | #NF #ciencia #fisica #d1 #e1 #trilha-do-quark-ao-cosmos #tenho-digital |
| Business Intelligence: Implementar do Jeito Certo e a Custo Zero | Ronaldo Braghittoni | #NF #tecnologia #dados #gestao #d2 #e1 #tenho-digital |
| Ciência da Computação e Tecnologias Digitais | Ernane Rosa Martins (org.) | #NF #tecnologia #d2 #e2 #tenho-digital |
| Ciência da Computação: Uma Visão Abrangente | J. Glenn Brookshear | #NF #tecnologia #programacao #didatico #d2 #e3 #tenho-digital |
| Ciência e Liberdade: Democracia, Razão e Leis da Natureza | Timothy Ferris | #NF #ciencia #politica #historia #d2 #e2 #tenho-digital |
| Ciência no Cotidiano | Natalia Pasternak | #NF #ciencia #BR #d1 #e1 #tenho-digital |
| Ciência X Espiritualidade: Dois Pensadores, Duas Visões de Mundo | Deepak Chopra e Leonard Mlodinow | #NF #ciencia #espiritualidade #fisica #consciencia #d2 #e2 #tenho-digital |
| Computação, Cognição, Semiose | João Queiroz, Ângelo Loula e Ricardo Gudwin (orgs.) | #NF #tecnologia #ia #filosofia #linguagem #d3 #e2 #tenho-digital |
| Contra a Realidade: A Negação da Ciência | Natalia Pasternak | #NF #ciencia #politica #BR #d1 #e2 #tenho-digital |
| Criação Imperfeita | Marcelo Gleiser | #NF #ciencia #fisica #BR #d2 #e2 #tenho-digital |
| Crick, Watson e o DNA em 90 Minutos | Paul Strathern | #NF #introducao #ciencia #biografia #d1 #e1 #tenho-digital |
| Crónicas del Espacio | Neil deGrasse Tyson | #NF #ciencia #fisica #d1 #e2 #tenho-digital |
| Curie e a Radioatividade em 90 Minutos | Paul Strathern | #NF #introducao #ciencia #biografia #d1 #e1 #tenho-digital |
| Curiosidade Mórbida: A Ciência e a Vida Secreta dos Cadáveres | Mary Roach | #NF #ciencia #medicina #morte #humor #d1 #e2 #tenho-digital |
| Da Cabeça aos Pés: Histórias do Corpo Humano | Gavin Francis | #NF #ciencia #medicina #d1 #e2 #tenho-digital |
| Dados Demais!: Como Desenvolver Habilidades Analíticas para Resolver Problemas Complexos, Reduzir Riscos e Decidir Melhor | Thomas H. Davenport e Jinho Kim | #NF #tecnologia #dados #gestao #d1 #e2 #tenho-digital |
| Darwin e a Evolução em 90 Minutos | Paul Strathern | #NF #introducao #ciencia #biografia #d1 #e1 #tenho-digital |
| Darwin sem Frescura | Reinaldo José Lopes | #NF #ciencia #biologia #BR #d1 #e2 #tenho-digital |
| De Onde Vêm as Boas Ideias | Steven Johnson | #NF #ciencia #tecnologia #historia #d1 #e2 #tenho-digital |
| De Primatas a Astronautas: A Jornada do Homem em Busca do Conhecimento | Leonard Mlodinow | #NF #ciencia #historia #d1 #e2 #tenho-digital |
| Decisões de Investimentos em Tecnologia da Informação: Vencendo os Desafios da Avaliação de Projetos em TI | Jocildo Correia Neto | #NF #tecnologia #gestao #d2 #e2 #tenho-digital |
| Design para Quem Não é Designer: Noções Básicas de Planejamento Visual | Robin Williams | #NF #tecnologia #design #d1 #e1 #tenho-digital |
| Diversidade da Vida | Edward O. Wilson | #NF #ciencia #biologia #ecologia #d2 #e2 #tenho-digital |
| Do Big Bang ao Universo Eterno | Mário Novello | #NF #ciencia #fisica #BR #d2 #e1 #tenho-digital |
| Einstein e a Relatividade em 90 Minutos | Paul Strathern | #NF #introducao #ciencia #biografia #fisica #d1 #e1 #tenho-digital |
| Em Busca do Infinito: Uma História da Matemática dos Primeiros Números à Teoria do Caos | Ian Stewart | #NF #ciencia #matematica #historia #d2 #e2 #tenho-digital |
| Engenharia de Software | Ian Sommerville | #NF #tecnologia #programacao #didatico #d3 #e3 #tenho-digital |
| Engenharia de Software | Roger S. Pressman e Bruce R. Maxim | #NF #tecnologia #programacao #didatico #d3 #e3 #tenho-digital |
| Engenharia de Software | Roque Maitino Neto | #NF #tecnologia #programacao #didatico #d2 #e2 #tenho-digital |
| Engenharia de Software: Produtos | Wilson de Pádua Paula Filho | #NF #tecnologia #programacao #didatico #d3 #e3 #tenho-digital |
| Engenharia de Software: Projetos e Processos | Wilson de Pádua Paula Filho | #NF #tecnologia #programacao #didatico #d3 #e3 #tenho-digital |
| Entendendo Algoritmos | Aditya Y. Bhargava | #NF #tecnologia #programacao #d1 #e2 #tenho-digital |
| Epigenética | Richard C. Francis | #NF #ciencia #biologia #d2 #e1 #tenho-digital |
| Estatística: O que é, para que Serve, como Funciona | Charles Wheelan | #NF #matematica #dados #d1 #e2 #tenho-digital |
| Estatística Usando Excel | Juan Carlos Lapponi | #NF #tecnologia #matematica #dados #didatico #d2 #e2 #tenho-digital |
| Estratégia de Governança de Tecnologia de Informação | Rosa Maria de Moura Albertin | #NF #tecnologia #gestao #d2 #e2 #tenho-digital |
| Estratégia de UX | Jaime Levy | #NF #tecnologia #design #gestao #d2 #e2 #tenho-digital |
| Evolução em Quatro Dimensões: DNA, Comportamento e a História da Vida | Eva Jablonka e Marion J. Lamb | #NF #ciencia #biologia #d3 #e3 #tenho-digital |
| Excel (2 em 1): Do Básico ao Intermediário | Luiz Felipe Araujo | #NF #tecnologia #dados #didatico #d1 #e1 #tenho-digital |
| Excel Calcula Tudo: Passo a Passo Ilustrado | Matilde Ferreira e Saulo Lima | #NF #tecnologia #dados #didatico #d1 #e1 #tenho-digital |
| Excel: Módulo Avançado | Luiz Felipe Araujo | #NF #tecnologia #dados #didatico #d2 #e1 #tenho-digital |
| Excel para o Dia a Dia: Seus Primeiros Passos no Mundo das Planilhas | Welton Calil | #NF #tecnologia #dados #didatico #d1 #e1 #tenho-digital |
| Fundamentos da Inteligência Artificial | João Luís Garcia Rosa | #NF #tecnologia #ia #didatico #d2 #e2 #tenho-digital |
| Fundamentos de Governança de TI | Edson Roberto Gaseta | #NF #tecnologia #gestao #didatico #d2 #e1 #tenho-digital |
| Fundamentos de Sistemas de Informação | Edmir Prado | #NF #tecnologia #didatico #d2 #e2 #tenho-digital |
| Fundamentos do COBIT 5 | Luiz Claudio Diogo Reis | #NF #tecnologia #gestao #didatico #d2 #e1 #tenho-digital |
| Fundamentos do Scrum | Rodrigo Alves Costa | #NF #tecnologia #gestao #d1 #e1 #tenho-digital |
| Galileu e o Sistema Solar em 90 Minutos | Paul Strathern | #NF #introducao #ciencia #biografia #d1 #e1 #tenho-digital |
| Gerência de Redes de Computadores | Mauro Tapajós Santos | #NF #tecnologia #didatico #d2 #e2 #tenho-digital |
| Gerenciamento de Projetos de Tecnologia da Informação | Marconi Fabio Vieira | #NF #tecnologia #gestao #d2 #e2 #tenho-digital |
| Gerenciamento de Projetos de TI | Rodrigo Costa | #NF #tecnologia #gestao #d2 #e1 #tenho-digital |
| Gerenciamento de Serviços de TI | Felício Cestari Filho | #NF #tecnologia #gestao #didatico #d2 #e1 #tenho-digital |
| Gestão da Segurança da Informação: NBR 27001 e NBR 27002 | Flavia Estélia Silva Coelho | #NF #tecnologia #gestao #didatico #d2 #e2 #tenho-digital |
| Gestão de Riscos de TI: NBR 27005 | Edson Kowask Bezerra | #NF #tecnologia #gestao #didatico #d2 #e1 #tenho-digital |
| Gestão Digital | Ellen Salomão | #NF #tecnologia #gestao #d1 #e2 #tenho-digital |
| Guia Brasileiro de Análise de Dados | Cláudio D. Shikida e Leonardo Monasterio | #NF #tecnologia #dados #economia #BR #d2 #e2 #tenho-digital |
| Guia de Sobrevivência na Natureza | Dave Canterbury | #NF #didatico #d1 #e2 #tenho-digital |
| Guia do Scrum | Ken Schwaber e Jeff Sutherland | #NF #tecnologia #gestao #d1 #e1 #tenho-digital |
| Guia Mangá de Banco de Dados | Mana Takahashi e Shoko Azuma | #NF #tecnologia #dados #didatico #d1 #e1 #tenho-digital |
| Guia Prático de Metodologias Ativas com Uso de Tecnologias Digitais da Informação e Comunicação | Alexandre José de Carvalho Silva | #NF #tecnologia #educacao #d1 #e1 #tenho-digital |
| Hawking e os Buracos Negros em 90 Minutos | Paul Strathern | #NF #ciencia #fisica #biografia #introducao #d1 #e1 #tenho-digital |
| Hiperespaço: Uma Odisseia Científica Através de Universos Paralelos, Empenamentos do Tempo e a Décima Dimensão | Michio Kaku | #NF #ciencia #fisica #d2 #e2 #tenho-digital |
| Homo Biologicus: Como a Biologia Explica a Natureza Humana | Pier Vincenzo Piazza | #NF #ciencia #biologia #psicologia #d2 #e2 #tenho-digital |
| Homo Deus | Yuval Noah Harari | #NF #ia #historia #filosofia #tecnologia #d1 #e2 #tenho-digital |
| Hooked (Engajado): Como Construir Produtos e Serviços Formadores de Hábitos | Nir Eyal | #NF #tecnologia #psicologia #gestao #d1 #e1 #tenho-digital |
| HTML5 e CSS3: Domine a Web do Futuro | Lucas Mazza | #NF #tecnologia #programacao #didatico #d1 #e1 #tenho-digital |
| Impérios da Comunicação: Do Telefone à Internet, da ATT ao Google | Tim Wu | #NF #tecnologia #historia #economia #d2 #e2 #tenho-digital |
| Incríveis Passatempos Matemáticos | Ian Stewart | #NF #matematica #d1 #e2 #tenho-digital |
| Informática: Conceitos Básicos | Fernando Velloso | #NF #tecnologia #didatico #d1 #e2 #tenho-digital |
| Inspirado: Como Criar Produtos de Tecnologia que os Clientes Amam | Marty Cagan | #NF #tecnologia #gestao #design #d1 #e2 #tenho-digital |
| Inteligência Artificial | Cristiano Roberto Franco | #NF #ia #tecnologia #didatico #BR #d2 #e2 #tenho-digital |
| Inteligência Artificial | George F. Luger | #NF #ia #tecnologia #didatico #d3 #e3 #tenho-digital |
| Inteligência Artificial | Kai-Fu Lee | #NF #ia #tecnologia #geopolitica #d1 #e2 #tenho-digital |
| Inteligência Artificial: 10 Coisas que Deve Saber | Tim Rocktäschel | #NF #ia #introducao #tecnologia #d1 #e1 #tenho-digital |
| Inteligência Artificial a Nosso Favor | Stuart Russell | #NF #ia #tecnologia #d2 #e2 #trilha-maquinas-que-pensam #tenho-digital |
| Inteligência Artificial Aplicada: Uma Abordagem Introdutória | Luciano Frontino de Medeiros | #NF #ia #tecnologia #didatico #BR #d2 #e2 #tenho-digital |
| Inteligência Artificial: Uma Abordagem de Aprendizado de Máquina | Katti Faceli, Ana Carolina Lorena, João Gama e outros | #NF #ia #tecnologia #didatico #programacao #BR #d3 #e2 #tenho-digital |
| Inteligência Emocional para Gerenciamento de Projetos | Anthony Mersino | #NF #tecnologia #gestao #psicologia #d1 #e2 #tenho-digital |
| Introdução à Física em Quadrinhos | S.T. Butler e Robert Raymond | #HQ #ciencia #fisica #introducao #d1 #e1 #tenho-digital |
| Introdução à Programação: 500 Algoritmos Resolvidos | Anita Lopes e Guto Garcia | #NF #tecnologia #programacao #didatico #d2 #e2 #tenho-digital |
| Introdução à Programação e aos Algoritmos | João Araujo Ribeiro | #NF #tecnologia #programacao #didatico #d2 #e1 #tenho-digital |
| Introdução a Sistemas de Bancos de Dados | C.J. Date | #NF #tecnologia #dados #didatico #d3 #e3 #tenho-digital |
| Introdução e Boas Práticas em UX Design | Fabrício Teixeira | #NF #tecnologia #design #d1 #e1 #tenho-digital |
| ITIL: Guia de Implantação | Paulo Sergio Cougo | #NF #tecnologia #gestao #didatico #d2 #e2 #tenho-digital |
| ITIL V3 Fundamentos | Felício Cestari Filho | #NF #tecnologia #gestao #didatico #d2 #e1 #tenho-digital |
| Leis da Psicologia Aplicadas a UX | Jon Yablonski | #NF #tecnologia #design #psicologia #d1 #e1 #tenho-digital |
| Lógica para Computação | Flávio Soares Corrêa da Silva | #NF #tecnologia #matematica #programacao #didatico #d3 #e2 #tenho-digital |
| Maneiras de Ser: Animais, Plantas, Máquinas: A Busca por uma Inteligência Planetária | James Bridle | #NF #ciencia #ecologia #ia #tecnologia #d2 #e2 #tenho-digital |
| Manual de Medicina Legal | Delton Croce Junior | #NF #medicina #didatico #d3 #e3 #tenho-digital |
| Manual de Sobrevivência do Novo Programador: Dicas Pragmáticas para sua Evolução Profissional | Josh Carter | #NF #tecnologia #programacao #d1 #e1 #tenho-digital |
| Matemática Discreta: Uma Introdução | Edward Scheinerman | #NF #ciencia #matematica #didatico #d3 #e3 #tenho-digital |
| Medicina do Amanhã | Pedro Schestatsky | #NF #ciencia #medicina #tecnologia #BR #d1 #e2 #tenho-digital |
| Medicina dos Horrores | Lindsey Fitzharris | #NF #ciencia #medicina #historia #d1 #e2 #tenho-digital |
| Medicina Macabra | Thomas Morris | #NF #ciencia #medicina #historia #humor #d1 #e2 #tenho-digital |
| Medicina Macabra 2 | Lydia Kang | #NF #ciencia #medicina #historia #humor #d1 #e2 #tenho-digital |
| Mentes Brilhantes Não Pensam Igual | Marcelo Gleiser | #NF #ciencia #filosofia #BR #d2 #e2 #tenho-digital |
| Métodos Ágeis e Gestão de Serviços de TI | Bruno Souza de Oliveira | #NF #tecnologia #gestao #d2 #e1 #tenho-digital |
| Microbiologia para Leigos | Jennifer Stearns, Michael Surette e Julienne Kaiser | #NF #ciencia #biologia #didatico #d2 #e2 #tenho-digital |
| Modelagem de Banco de Dados | Paulo Henrique Cayres | #NF #tecnologia #dados #didatico #d2 #e1 #tenho-digital |
| Mundos Paralelos: Uma Jornada Através da Criação, das Dimensões Superiores e do Futuro do Cosmo | Michio Kaku | #NF #ciencia #fisica #d2 #e2 #tenho-digital |
| MySQL: Comece com o Principal Banco de Dados Open Source do Mercado | Vinícius Carvalho | #NF #tecnologia #dados #programacao #didatico #d1 #e1 #tenho-digital |
| Newton e a Gravidade em 90 Minutos | Paul Strathern | #NF #introducao #ciencia #biografia #fisica #d1 #e1 #tenho-digital |
| Nexus: Uma Breve História das Redes de Informação, da Idade da Pedra à Inteligência Artificial | Yuval Noah Harari | #NF #ia #historia #tecnologia #d2 #e3 #tenho-digital |
| Noções de Estatística para Concursos | Anderson Meneses | #NF #matematica #didatico #d2 #e1 #tenho-digital |
| O Algoritmo Mestre: Como a Busca pelo Algoritmo de Machine Learning Definitivo Recriará Nosso Mundo | Pedro Domingos | #NF #tecnologia #ia #d2 #e2 #trilha-maquinas-que-pensam #tenho-digital |
| O Andar do Bêbado: Como o Acaso Determina Nossas Vidas | Leonard Mlodinow | #NF #ciencia #matematica #d1 #e2 #tenho-digital |
| O Caldeirão Azul | Marcelo Gleiser | #NF #ciencia #fisica #BR #d1 #e2 #tenho-digital |
| O Caminho para o Sucesso com Power BI | Leonardo Karpinski | #NF #tecnologia #dados #didatico #d1 #e1 #tenho-digital |
| O Capelão do Diabo | Richard Dawkins | #NF #ciencia #biologia #religiao #d2 #e2 #tenho-digital |
| O Cerne da Matéria | Rogerio Rosenfeld | #NF #ciencia #fisica #BR #d2 #e2 #tenho-digital |
| O Colapso de Tudo | John Casti | #NF #ciencia #tecnologia #d1 #e2 #tenho-digital |
| O Design do Dia a Dia | Donald A. Norman | #NF #tecnologia #design #psicologia #d1 #e2 #tenho-digital |
| O Design do Futuro | Donald A. Norman | #NF #tecnologia #design #d1 #e1 #tenho-digital |
| O Discreto Charme do Intestino | Giulia Enders | #NF #ciencia #medicina #biologia #d1 #e2 #tenho-digital |
| O Enigma Quântico: O Encontro da Física com a Consciência | Bruce Rosenblum e Fred Kuttner | #NF #ciencia #fisica #consciencia #d2 #e2 #tenho-digital |
| O Futuro do Espaço-Tempo | Stephen Hawking | #NF #ciencia #fisica #d2 #e1 #tenho-digital |
| O Grande Projeto | Stephen Hawking e Leonard Mlodinow | #NF #ciencia #fisica #d2 #e1 #tenho-digital |
| O Guia Completo das Plantas Medicinais | David Hoffmann | #NF #ciencia #medicina #didatico #d1 #e2 #tenho-digital |
| O Humano Mais Humano: O que a Inteligência Artificial nos Ensina sobre a Vida | Brian Christian | #NF #ia #filosofia #tecnologia #d2 #e2 #tenho-digital |
| O Inverno Nuclear | Carl Sagan | #NF #ciencia #guerra #ecologia #d2 #e2 #tenho-digital |
| O Livro dos Humanos: A História de como nos Tornamos Quem Somos | Adam Rutherford | #NF #ciencia #biologia #antropologia #d1 #e2 #tenho-digital |
| O Maior Espetáculo da Terra | Richard Dawkins | #NF #ciencia #biologia #d2 #e2 #tenho-digital |
| O Mínimo que Você Precisa Saber sobre Banco de Dados e SQL: Uma Abordagem Prática e Muito Simples | Tiago P. Ribeiro | #NF #tecnologia #dados #didatico #d1 #e1 #tenho-digital |
| O Mosquito: A Incrível História do Maior Predador da Humanidade | Timothy C. Winegard | #NF #ciencia #historia #medicina #d2 #e3 #tenho-digital |
| O Poder do Pensamento Matemático | Jordan Ellenberg | #NF #ciencia #matematica #d2 #e3 #tenho-digital |
| O Polegar do Violinista | Sam Kean | #NF #ciencia #biologia #historia #d1 #e2 #tenho-digital |
| O Programador Pragmático | Andrew Hunt e David Thomas | #NF #tecnologia #programacao #d2 #e2 #tenho-digital |
| O que os Médicos Não Contam | Matt McCarthy | #NF #ciencia #medicina #testemunho #d1 #e2 #tenho-digital |
| O Rio que Saía do Éden | Richard Dawkins | #NF #ciencia #biologia #d2 #e1 #tenho-digital |
| O Tecido do Cosmo | Brian Greene | #NF #ciencia #fisica #d3 #e3 #tenho-digital |
| O Tempo que o Tempo Tem: Por que o Ano Tem 12 Meses e Outras Curiosidades sobre o Calendário | Alexandre Cherman e Fernando Vieira | #NF #ciencia #historia #BR #d1 #e1 #tenho-digital |
| O Universo Elegante | Brian Greene | #NF #ciencia #fisica #d3 #e2 #trilha-do-quark-ao-cosmos #tenho-digital |
| O Universo numa Casca de Noz | Stephen Hawking | #NF #ciencia #fisica #d2 #e1 #tenho-digital |
| Origens: Catorze Bilhões de Anos de Evolução Cósmica | Neil deGrasse Tyson e Donald Goldsmith | #NF #ciencia #fisica #d2 #e2 #tenho-digital |
| Os 100 Maiores Cientistas da História: Uma Classificação dos Cientistas Mais Influentes do Passado e do Presente | John Simmons | #NF #ciencia #biografia #historia #d1 #e3 #tenho-digital |
| Os 11 Maiores Mistérios do Universo | Reinaldo José Lopes | #NF #ciencia #fisica #BR #d1 #e1 #tenho-digital |
| Os Maiores Problemas Matemáticos de Todos os Tempos | Ian Stewart | #NF #matematica #d3 #e2 #tenho-digital |
| Os Números Não Mentem: 71 Histórias para Entender o Mundo | Vaclav Smil | #NF #ciencia #economia #matematica #d1 #e2 #tenho-digital |
| Os Simpsons e a Ciência | Paul Halpern | #NF #ciencia #humor #d1 #e2 #tenho-digital |
| Pandemias: A Humanidade em Risco | Stefan Cunha Ujvari | #NF #ciencia #medicina #BR #d1 #e1 #tenho-digital |
| Para Explicar o Mundo: A Descoberta da Ciência Moderna | Steven Weinberg | #NF #ciencia #fisica #historia #d2 #e2 #tenho-digital |
| Pegando Fogo: Por que Cozinhar nos Tornou Humanos | Richard Wrangham | #NF #ciencia #biologia #antropologia #d2 #e2 #tenho-digital |
| People Analytics para Leigos | Mike West | #NF #tecnologia #dados #gestao #d1 #e2 #tenho-digital |
| Pequenas Maravilhas | Idan Ben-Barak | #NF #ciencia #biologia #d1 #e1 #tenho-digital |
| Pitágoras e seu Teorema em 90 Minutos | Paul Strathern | #NF #introducao #ciencia #biografia #d1 #e1 #tenho-digital |
| PL/SQL: Domine a Linguagem do Banco de Dados Oracle | Eduardo Gonçalves | #NF #tecnologia #dados #programacao #didatico #d2 #e2 #tenho-digital |
| Planejamento e Gestão Estratégica de TI | Ian Lawrence Webster | #NF #tecnologia #gestao #d2 #e2 #tenho-digital |
| Plantas Medicinais | Mara Zélia de Almeida | #NF #ciencia #medicina #BR #d2 #e1 #tenho-digital |
| Princípios de Design e Padrões de Projeto | Robert C. Martin | #NF #tecnologia #programacao #d3 #e2 #tenho-digital |
| Princípios Universais do Design | William Lidwell, Kritina Holden e Jill Butler | #NF #tecnologia #design #d1 #e2 #tenho-digital |
| Projeto e Modelagem de Banco de Dados | Toby Teorey | #NF #tecnologia #dados #didatico #d3 #e2 #tenho-digital |
| Python na Prática, vol. 2: Aprenda Python Através de Exercícios Comentados | Fernando Feltrin | #NF #tecnologia #programacao #didatico #d1 #e2 #tenho-digital |
| Redação Estratégica para UX | Torrey Podmajersky | #NF #tecnologia #design #escrita #d1 #e1 #tenho-digital |
| Redes de Computadores | José Wagner Bungart | #NF #tecnologia #didatico #d2 #e1 #tenho-digital |
| Refém do Algoritmo | Madhumita Murgia | #NF #ia #tecnologia #d1 #e2 #tenho-digital |
| Scrum: A Arte de Fazer o Dobro do Trabalho na Metade do Tempo | Jeff Sutherland | #NF #tecnologia #gestao #d1 #e1 #tenho-digital |
| Scrum: Gestão Ágil para Projetos de Sucesso | Rafael Sabbagh | #NF #tecnologia #gestao #d1 #e2 #tenho-digital |
| Segurança de Redes e Sistemas | Ivo de Carvalho Peixinho | #NF #tecnologia #didatico #d2 #e2 #tenho-digital |
| Sistemas de Banco de Dados | Ramez Elmasri e Shamkant B. Navathe | #NF #tecnologia #dados #didatico #d3 #e3 #tenho-digital |
| Sistemas de Gerenciamento de Banco de Dados | Raghu Ramakrishnan e Johannes Gehrke | #NF #tecnologia #dados #didatico #d3 #e3 #tenho-digital |
| Sprint | Jake Knapp, John Zeratsky e Braden Kowitz | #NF #tecnologia #gestao #design #d1 #e2 #tenho-digital |
| SQL: Curso Prático | Celso Henrique Poderoso de Oliveira | #NF #tecnologia #dados #programacao #didatico #d2 #e2 #tenho-digital |
| SQL: Uma Abordagem para Banco de Dados Oracle | Eduardo Gonçalves | #NF #tecnologia #dados #programacao #didatico #d2 #e2 #tenho-digital |
| Stephen Hawking: Histórias de Física e de uma Amizade | Leonard Mlodinow | #NF #ciencia #fisica #biografia #d1 #e2 #tenho-digital |
| Storytelling com Dados | Cole Nussbaumer Knaflic | #NF #tecnologia #dados #design #d1 #e2 #tenho-digital |
| Tecnologia da Informação e Comunicação | Luis Hernan Contreras Pinochet | #NF #tecnologia #didatico #d2 #e2 #tenho-digital |
| Tecnologias de Redes sem Fio | Omar Branquinho | #NF #tecnologia #didatico #d2 #e1 #tenho-digital |
| The Missing Link: An Introduction to Web Development and Programming | Michael Mendez | #NF #tecnologia #programacao #didatico #d1 #e2 #tenho-digital |
| Todo Mundo Mente: O que a Internet e os Dados Dizem sobre Quem Realmente Somos | Seth Stephens-Davidowitz | #NF #tecnologia #dados #psicologia #sociologia #d1 #e2 #tenho-digital |
| Transformação Digital: Repensando o seu Negócio para a Era Digital | David L. Rogers | #NF #tecnologia #gestao #d1 #e2 #tenho-digital |
| Tudo o que Você Precisa Saber sobre Ciência | Federico Kukso | #NF #ciencia #introducao #d1 #e2 #tenho-digital |
| Turing e o Computador em 90 Minutos | Paul Strathern | #NF #introducao #ciencia #biografia #tecnologia #d1 #e1 #trilha-maquinas-que-pensam #tenho-digital |
| Uma Nova História do Tempo | Stephen Hawking e Leonard Mlodinow | #NF #ciencia #fisica #d1 #e1 #tenho-digital |
| Use a Cabeça! SQL | Lynn Beighley | #NF #tecnologia #dados #programacao #didatico #d1 #e3 #tenho-digital |
| UX Estratégico: Design Aplicado a Ecossistema de Produtos | Gabriel Pinheiro Maciel da Silva | #NF #tecnologia #design #gestao #d2 #e1 #tenho-digital |
| Variedades da Experiência Científica | Carl Sagan | #NF #ciencia #religiao #fisica #d2 #e2 #tenho-digital |
| Você Sabia? Mais de 400 Coisas que Você Deveria Saber | Lukas Marques e Daniel Molo | #NF #ciencia #introducao #BR #d1 #e1 #tenho-digital |

### 17.14 Psicologia, psicanálise e comportamento

| Título | Autor | Tags |
|---|---|---|
| 1001 Frases de Grandes Pensadores | Danilo E. Barba | #NF #autoconhecimento #filosofia #d1 #e1 #tenho-digital |
| 101 Técnicas da Terapia Cognitivo-Comportamental | Jaquelini Conceição e Gabriela Bueno (orgs.) | #NF #psicologia #tcc #didatico #BR #d1 #e2 #tenho-digital |
| 12 Regras para a Vida: Um Antídoto para o Caos | Jordan B. Peterson | #NF #autoconhecimento #psicologia #d2 #e2 #tenho-digital |
| 365 Citações para Implementar em sua Vida | I.C. Robledo | #NF #autoconhecimento #d1 #e1 #tenho-digital |
| 50 Ideias de Psicologia que Você Precisa Conhecer | Adrian Furnham | #NF #psicologia #introducao #d1 #e2 #tenho-digital |
| 500 Frases de Grandes Pensadores | Sidney Vieira | #NF #autoconhecimento #filosofia #d1 #e1 #tenho-digital |
| A Análise e o Arquivo | Elisabeth Roudinesco | #NF #psicanalise #historia #d2 #e1 #tenho-digital |
| A Arquitetura do Eu: Psicoterapia, Meditação e Exercícios para o Cérebro | Leonardo Mascaro | #NF #psicologia #autoconhecimento #neurociencia #BR #d1 #e2 #tenho-digital |
| A Arte da Sedução | Robert Greene | #NF #autoconhecimento #d1 #e3 #tenho-digital |
| A Coragem de Não Agradar | Ichiro Kishimi e Fumitake Koga | #NF #autoconhecimento #psicologia #filosofia #d1 #e2 #tenho-digital |
| A Depressão como Mal-Estar Contemporâneo | Leandro A.T. Tavares | #NF #psicologia #psicopatologia #BR #d2 #e1 #tenho-digital |
| A Descoberta do Inconsciente: Do Desejo ao Sintoma | Antônio Quinet | #NF #psicanalise #introducao #BR #d2 #e1 #tenho-digital |
| A Descoberta do Inconsciente Social: Contribuição ao Redirecionamento da Psicanálise | Erich Fromm | #NF #psicanalise #psicologia-social #d2 #e1 #rel-fromm #tenho-digital |
| A Dor Física: Uma Teoria Psicanalítica da Dor Corporal | J.-D. Nasio | #NF #psicanalise #d2 #e1 #tenho-digital |
| A Entrevista Psiquiátrica na Prática Clínica | Roger A. MacKinnon, Robert Michels e Peter J. Buckley | #NF #psiquiatria #psicologia #didatico #d3 #e3 #tenho-digital |
| A Estranheza da Psicanálise | Antônio Quinet | #NF #psicanalise #BR #d3 #e2 #tenho-digital |
| A Experiência da Mesa: O Segredo para Criar Relacionamentos Profundos | Devi Titus | #NF #autoconhecimento #religiao #d1 #e1 #tenho-digital |
| A Família | Jacques Lacan | #NF #psicanalise #classico #d3 #e1 #tenho-digital |
| A Família em Desordem | Elisabeth Roudinesco | #NF #psicologia #psicanalise #sociologia #historia #d2 #e2 #tenho-digital |
| A Fantasia | J.-D. Nasio | #NF #psicanalise #d2 #e1 #tenho-digital |
| A Fascinante Construção do Eu | Augusto Cury | #NF #autoconhecimento #BR #d1 #e1 #tenho-digital |
| A Função do Orgasmo | Wilhelm Reich | #NF #psicologia #psicanalise #classico #d2 #e2 #tenho-digital |
| A Gestalt-terapia | Chantal Masquelier-Savatier | #NF #psicologia #psicologia-humanista #introducao #d2 #e1 #tenho-digital |
| A Inibição Intelectual na Psicanálise | Ana Lydia Santiago | #NF #psicanalise #educacao #BR #d3 #e2 #tenho-digital |
| A Interpretação | Laéria Fontenele | #NF #psicologia #psicanalise #introducao #BR #d2 #e1 #tenho-digital |
| A Interpretação dos Sonhos | Sigmund Freud | #NF #psicanalise #classico #d3 #e3 #trilha-psicanalise-em-degraus #tenho-digital |
| A Jornada de Ser Humano | Magda Lopes | #NF #autoconhecimento #d1 #e2 #tenho-digital |
| A Linguagem Corporal do Amor | Allan e Barbara Pease | #NF #autoconhecimento #d1 #e2 #tenho-digital |
| A Linguagem Corporal no Trabalho | Allan e Barbara Pease | #NF #autoconhecimento #gestao #d1 #e2 #tenho-digital |
| A Linguagem Secreta do Carisma | Vanessa Van Edwards | #NF #autoconhecimento #d1 #e2 #tenho-digital |
| A Lógica da Emoção | Manoelita Dias dos Santos | #NF #psicanalise #psicologia #BR #d2 #e2 #tenho-digital |
| A Mais Pura Verdade sobre a Desonestidade | Dan Ariely | #NF #autoconhecimento #psicologia #psicologia-social #d1 #e2 #tenho-digital |
| A Natureza Comportamental da Mente: Behaviorismo Radical e Filosofia da Mente | Diego Zilio | #NF #psicologia #behaviorismo #filosofia #BR #d3 #e2 #tenho-digital |
| A Neurose Obsessiva | Maria Anita Carneiro Ribeiro | #NF #psicanalise #psicopatologia #introducao #BR #d2 #e1 #tenho-digital |
| A Parte Obscura de Nós Mesmos | Elisabeth Roudinesco | #NF #psicanalise #psicologia #historia #d2 #e1 #tenho-digital |
| A Psicanálise dos Contos de Fadas | Bruno Bettelheim | #NF #psicanalise #parentalidade #classico #d2 #e2 #tenho-digital |
| A Psicanálise na Terra do Nunca | Diana Lichtenstein Corso e Mário Corso | #NF #psicanalise #arte #BR #RS #d2 #e2 #tenho-digital |
| A Psicanálise, Novamente | MD Magno | #NF #psicanalise #BR #d3 #e2 #tenho-digital |
| A Psicologia como Ciência Histórica | Alexander R. Luria | #NF #psicologia #introducao #historia #d3 #e1 #tenho-digital |
| A Psicologia da Inteligência | Jean Piaget | #NF #psicologia #educacao #classico #d3 #e2 #tenho-digital |
| A Psicologia da Mídia Social | Ciáran McMahon | #NF #psicologia #tecnologia #psicologia-social #d1 #e1 #tenho-digital |
| A Psicologia das Emoções: O Fascínio do Rosto Humano | A. Freitas-Magalhães | #NF #psicologia #d2 #e2 #tenho-digital |
| A Psicologia de C.G. Jung: Uma Introdução às Obras Completas | Jolande Jacobi | #NF #psicologia #psicologia-analitica #introducao #d2 #e2 #trilha-jung-para-comecar #tenho-digital |
| A Psicologia Vai ao Cinema | Skip Dine Young | #NF #psicologia #cinema #d1 #e2 #tenho-digital |
| A Psicose | Andréa M.C. Guerra | #NF #psicanalise #psicopatologia #introducao #BR #d2 #e1 #tenho-digital |
| A Revolução Sexual | Wilhelm Reich | #NF #psicologia #psicanalise #politica #classico #d2 #e2 #tenho-digital |
| A Sublimação | Clarissa Metzger | #NF #psicanalise #introducao #BR #d2 #e1 #tenho-digital |
| A Sublimação | Orlando Cruxên | #NF #psicanalise #psicologia #introducao #BR #d2 #e1 #tenho-digital |
| A Técnica Pomodoro | Francesco Cirillo | #NF #autoconhecimento #gestao #d1 #e1 #tenho-digital |
| A Terapia Cognitivo-Comportamental Baseada em Evidências | Deborah Dobson e Keith S. Dobson | #NF #psicologia #tcc #d3 #e2 #tenho-digital |
| A Transferência: Uma Viagem Rumo ao Continente Negro | Denise Maurano | #NF #psicanalise #introducao #d2 #e1 #tenho-digital |
| Agilidade Emocional | Susan David | #NF #autoconhecimento #psicologia #d1 #e2 #tenho-digital |
| Além da Ordem: Mais 12 Regras para a Vida | Jordan B. Peterson | #NF #autoconhecimento #psicologia #d2 #e2 #tenho-digital |
| Alienação e Liberdade | Frantz Fanon | #NF #psiquiatria #colonialismo #raca #politica #d3 #e3 #tenho-digital |
| Alienação Parental | Fábio Vieira Figueiredo e Georgios Alexandridis | #NF #psicologia #parentalidade #BR #d2 #e1 #tenho-digital |
| AmaZonas: A Psicanálise de A a Z | MD Magno | #NF #psicanalise #BR #d3 #e3 #tenho-digital |
| Amor, Culpa e Reparação e Outros Trabalhos (1921-1945) | Melanie Klein | #NF #psicologia #psicanalise #classico #d3 #e3 #tenho-digital |
| Análise Comportamental Clínica: Aspectos Teóricos e Estudos de Caso | Ana Karina C.R. de-Farias (org.) | #NF #psicologia #behaviorismo #didatico #BR #d3 #e2 #tenho-digital |
| Análise Psicanalítica de Discursos: Perspectivas Lacanianas | Christian Dunker, Clarice Pimentel Paulon e J. Guillermo Milán-Ramos | #NF #psicanalise #linguagem #BR #d3 #e2 #tenho-digital |
| Angústia | Sonia Leite | #NF #psicanalise #introducao #BR #d2 #e1 #tenho-digital |
| Animus e Anima | Emma Jung | #NF #psicologia #psicologia-analitica #genero #classico #d2 #e1 #tenho-digital |
| Aprendendo a Terapia Cognitivo-Comportamental: Um Guia Ilustrado | Jesse H. Wright, Monica R. Basco e Michael E. Thase | #NF #psicologia #tcc #didatico #d2 #e2 #tenho-digital |
| Aprendendo Inteligência: Manual de Instruções do Cérebro para Estudantes em Geral | Pierluigi Piazzi | #NF #autoconhecimento #educacao #BR #d1 #e1 #tenho-digital |
| Armadilhas da Química Amorosa | Bruno Luiz Avelino Cardoso e Kelly Paim | #NF #psicologia #tcc #autoconhecimento #BR #d1 #e1 #tenho-digital |
| Arquivos da Loucura | Vera Portocarrero | #NF #psicologia #psiquiatria #historia #BR #d3 #e1 #tenho-digital |
| Arte e Psicanálise | Tania Rivera | #NF #psicanalise #arte #introducao #BR #d2 #e1 #tenho-digital |
| Arte e Psicanálise: Estética e Clínica Geral | MD Magno | #NF #psicanalise #arte #BR #d3 #e2 #tenho-digital |
| As Dimensões do Gozo | Patrick Valas | #NF #psicologia #psicanalise #d3 #e1 #tenho-digital |
| As Ferramentas Intelectuais dos Gênios | I.C. Robledo | #NF #autoconhecimento #d1 #e1 #tenho-digital |
| As Mulheres Primeiro | Ian Kerner | #NF #autoconhecimento #d1 #e2 #tenho-digital |
| As Opiniões e as Crenças | Gustave Le Bon | #NF #psicologia #psicologia-social #classico #d2 #e2 #tenho-digital |
| As Raízes da Psicologia Social Moderna (1872-1954) | Robert M. Farr | #NF #psicologia #psicologia-social #historia #d3 #e2 #tenho-digital |
| As Várias Faces da Psicologia Fenomenológico-Existencial | Valdemar Augusto Angerami-Camon (org.) | #NF #psicologia #psicologia-humanista #existencialismo #BR #d2 #e2 #tenho-digital |
| Avaliação Psicológica da Inteligência e da Personalidade | Claudio Simon Hutz, Denise Ruschel Bandeira e Clarissa Marceli Trentini (orgs.) | #NF #psicologia #psicometria #didatico #BR #d3 #e2 #tenho-digital |
| Avaliação Psicológica: Guia para Estudantes e Profissionais de Psicologia | Rodolfo A.M. Ambiel e outros (orgs.) | #NF #psicologia #psicometria #didatico #BR #d2 #e2 #tenho-digital |
| Bíblia da Sedução | Alex Hilgert | #NF #autoconhecimento #d1 #e2 #tenho-digital |
| Cada Dia Mais Perto | Irvin D. Yalom e Ginny Elkin | #NF #psicologia #existencialismo #testemunho #d1 #e2 #rel-yalom #tenho-digital |
| Cão Farejador: Ensaios sobre Jung e Simondon | Amnéris Maroni | #NF #psicologia #psicologia-analitica #filosofia #d3 #e2 #tenho-digital |
| Cartas a um Jovem Terapeuta | Contardo Calligaris | #NF #psicologia #psicanalise #BR #d1 #e1 #trilha-formacao-do-terapeuta #tenho-digital |
| Cartas de um Terapeuta para os seus Momentos de Crise | Alexandre Coimbra Amaral | #NF #psicologia #autoconhecimento #BR #d1 #e2 #tenho-digital |
| Cartografias do Feminino | Joel Birman | #NF #psicologia #psicanalise #genero #BR #d3 #e2 #tenho-digital |
| Casos Clínicos do DSM-5 | John W. Barnhill | #NF #psiquiatria #psicopatologia #didatico #d2 #e2 #tenho-digital |
| Cercado de Idiotas | Thomas Erikson | #NF #autoconhecimento #psicologia #d1 #e2 #tenho-digital |
| Ciência e Comportamento Humano | B.F. Skinner | #NF #psicologia #behaviorismo #classico #d3 #e2 #tenho-digital |
| Ciência Marxista do Sujeito: Uma Introdução à Psicologia Crítica, vol. 1 | Klaus Holzkamp | #NF #psicologia #politica #d3 #e2 #tenho-digital |
| Ciência Psicológica | Michael S. Gazzaniga e Todd F. Heatherton | #NF #psicologia #introducao #didatico #d2 #e3 #tenho-digital |
| Cinco Lições sobre a Teoria de Jacques Lacan | J.-D. Nasio | #NF #psicanalise #introducao #d2 #e1 #trilha-psicanalise-em-degraus #tenho-digital |
| Cinema e Loucura: Conhecendo os Transtornos Mentais Através dos Filmes | J. Landeira-Fernandez e Elie Cheniaux | #NF #psicologia #psicopatologia #cinema #BR #d1 #e2 #tenho-digital |
| Cinema, Imagem e Psicanálise | Tania Rivera | #NF #psicanalise #cinema #BR #d2 #e1 #tenho-digital |
| Clínica Humanista-Fenomenológica: Estudos em Psicoterapia e Psicopatologia Crítica | Virginia Moreira | #NF #psicologia #psicologia-humanista #psicopatologia #BR #d3 #e2 #tenho-digital |
| Código da Atração | Eduardo Santorini | #NF #autoconhecimento #BR #d1 #e1 #tenho-digital |
| Como Aumentar a Testosterona de Forma Natural | Editora Mente Livre | #NF #autoconhecimento #medicina #d1 #e1 #tenho-digital |
| Como Convencer Alguém em 90 Segundos | Nicholas Boothman | #NF #autoconhecimento #d1 #e1 #tenho-digital |
| Como Fazer Amigos e Influenciar Pessoas | Dale Carnegie | #NF #autoconhecimento #classico #d1 #e2 #tenho-digital |
| Como Trabalha um Psicanalista | J.-D. Nasio | #NF #psicanalise #d2 #e1 #trilha-psicanalise-em-degraus #tenho-digital |
| Compêndio de Psiquiatria: Ciência do Comportamento e Psiquiatria Clínica | Benjamin J. Sadock, Virginia A. Sadock e Pedro Ruiz | #NF #psiquiatria #psicopatologia #didatico #d3 #e3 #tenho-digital |
| Compreender o Behaviorismo | William M. Baum | #NF #psicologia #behaviorismo #d2 #e2 #tenho-digital |
| Comunicação Não-Violenta | Marshall B. Rosenberg | #NF #psicologia #autoconhecimento #d1 #e2 #tenho-digital |
| Conversas Difíceis | Douglas Stone, Bruce Patton e Sheila Heen | #NF #psicologia #autoconhecimento #d1 #e2 #tenho-digital |
| Crenças Extraordinárias: Uma Abordagem Histórica de um Problema Psicológico | Peter Lamont | #NF #psicologia #historia #enigmas #d2 #e2 #tenho-digital |
| Crescimento Pessoal: As 59 Falácias Lógicas Mais Poderosas | Steve Allen | #NF #autoconhecimento #filosofia #d1 #e1 #tenho-digital |
| Criaturas de um Dia | Irvin D. Yalom | #NF #psicologia #existencialismo #morte #d1 #e1 #rel-yalom #tenho-digital |
| Crítica dos Fundamentos da Psicologia: A Psicologia e a Psicanálise | Georges Politzer | #NF #psicanalise #filosofia #classico #d3 #e2 #tenho-digital |
| De Pessoa para Pessoa: O Problema de Ser Humano | Carl R. Rogers e Barry Stevens | #NF #psicologia #psicologia-humanista #classico #d2 #e2 #tenho-digital |
| Decifrando os Temperamentos Humanos | Mestre Gabriel Amorim | #NF #psicologia #autoconhecimento #BR #d1 #e1 #tenho-digital |
| Defesas do Ego: Leitura Didática de seus Mecanismos | Wilson Castello de Almeida | #NF #psicanalise #didatico #BR #d2 #e1 #tenho-digital |
| Deleuze and Psychoanalysis | Leen De Bolle | #NF #psicanalise #filosofia #d3 #e1 #tenho-digital |
| Desafios para a Técnica Psicanalítica | José Carlos Garcia | #NF #psicanalise #d3 #e2 #tenho-digital |
| Descolonizando a Psicologia: Contribuições para uma Prática Popular | Wesley Henrique Alves da Rocha (org.) | #NF #psicologia #politica #colonialismo #BR #d2 #e2 #tenho-digital |
| Descubra seus Pontos Fortes | Marcus Buckingham | #NF #autoconhecimento #gestao #d1 #e2 #tenho-digital |
| Desenvolvimento Humano | Diane E. Papalia e Ruth D. Feldman | #NF #psicologia #didatico #d2 #e3 #tenho-digital |
| Desinformação | Dan Ariely | #NF #psicologia #psicologia-social #d1 #e2 #tenho-digital |
| Dicionário de Símbolos Arquétipos | Berg Fausto | #NF #psicologia #psicologia-analitica #mitologia #d1 #e2 #tenho-digital |
| Dicionário Enciclopédico de Psicanálise: O Legado de Freud e Lacan | Pierre Kaufmann (org.) | #NF #psicanalise #didatico #d3 #e3 #tenho-digital |
| Discurso e Psicanálise: A-versão do Sentido | Juliana Santana Cavallari, Lauro José Siqueira Baldini e Marcos Aurelio Barbai | #NF #psicanalise #linguagem #BR #d3 #e2 #tenho-digital |
| Ditos e Escritos, vol. 1: Problematização do Sujeito: Psicologia, Psiquiatria e Psicanálise | Michel Foucault | #NF #psicologia #filosofia #psiquiatria #d3 #e2 #tenho-digital |
| Do Ato ao Pensamento: Ensaio de Psicologia Comparada | Henri Wallon | #NF #psicologia #educacao #classico #d3 #e2 #tenho-digital |
| Doença Mental e Psicologia | Michel Foucault | #NF #psicologia #filosofia #psiquiatria #classico #d2 #e1 #tenho-digital |
| DSM-5: Manual Diagnóstico e Estatístico de Transtornos Mentais | American Psychiatric Association | #NF #psiquiatria #psicopatologia #didatico #d3 #e3 #tenho-digital |
| El Proceso de Envejecimiento | (autor não informado) | #NF #psicologia #d2 #e2 #verificar #tenho-digital |
| Em Defesa da Psicanálise | Elisabeth Roudinesco | #NF #psicanalise #d2 #e1 #tenho-digital |
| Emergências Psiquiátricas | João Quevedo e André F. Carvalho (orgs.) | #NF #psicologia #psiquiatria #didatico #BR #d3 #e2 #tenho-digital |
| Encontro Marcado com a Loucura: Ensinando e Aprendendo Psicopatologia | Tânia Cociuffo | #NF #psicologia #psicopatologia #didatico #BR #d2 #e1 #tenho-digital |
| Ensaios de Psicanálise e Filosofia | Jean Hyppolite | #NF #psicanalise #filosofia #d3 #e1 #tenho-digital |
| Ensaios sobre Psicologia Social e Psicanálise | Theodor W. Adorno | #NF #psicologia #psicologia-social #psicanalise #sociologia #d3 #e1 #tenho-digital |
| Enviesados | Rian Dutra | #NF #psicologia #design #d1 #e2 #tenho-digital |
| Escritos sobre a Psicologia do Inconsciente, vol. 2 | Sigmund Freud | #NF #psicanalise #classico #d3 #e2 #tenho-digital |
| Essencialismo | Greg McKeown | #NF #autoconhecimento #d1 #e2 #tenho-digital |
| Estatística sem Matemática para Psicologia | Christine P. Dancey e John Reidy | #NF #psicologia #matematica #didatico #d2 #e3 #tenho-digital |
| Estou Falando com as Paredes | Jacques Lacan | #NF #psicanalise #d3 #e1 #tenho-digital |
| Estruturas da Mente: A Teoria das Inteligências Múltiplas | Howard Gardner | #NF #psicologia #educacao #classico #d2 #e2 #tenho-digital |
| Estudos sobre a História do Comportamento | Lev S. Vigotski e Alexander R. Luria | #NF #psicologia #classico #d3 #e2 #tenho-digital |
| Evasivas Admiráveis | Theodore Dalrymple | #NF #psicologia #d2 #e1 #tenho-digital |
| Fadas no Divã: Psicanálise nas Histórias Infantis | Diana Lichtenstein Corso e Mário Corso | #NF #psicanalise #parentalidade #BR #RS #d2 #e2 #tenho-digital |
| Formas de Investigação Clínica em Psicologia | Walter Trinca | #NF #psicologia #psicopatologia #BR #d3 #e2 #tenho-digital |
| Frases Up: 250 Frases para Motivar e Iluminar o seu Dia | Vários autores | #NF #autoconhecimento #d1 #e1 #tenho-digital |
| Freud, Criador da Psicanálise | Marco Antonio Coutinho Jorge e Nadiá Paulo Ferreira | #NF #psicanalise #introducao #biografia #BR #d1 #e1 #trilha-psicanalise-em-degraus #tenho-digital |
| Freud e a Cocaína: A História do Uso da Droga nos Primórdios da Psicanálise | David Cohen | #NF #psicanalise #historia #biografia #d1 #e2 #tenho-digital |
| Freud e a Filosofia | Joel Birman | #NF #psicanalise #filosofia #introducao #BR #d2 #e1 #tenho-digital |
| Freud e a Perversão | Patrick Valas | #NF #psicanalise #psicopatologia #d3 #e1 #tenho-digital |
| Freud e o Inconsciente | Luiz Alfredo Garcia-Roza | #NF #psicanalise #introducao #BR #d2 #e2 #tenho-digital |
| Freud: Mas por que Tanto Ódio? | Elisabeth Roudinesco | #NF #psicanalise #d2 #e1 #tenho-digital |
| Fundamentos da Psicanálise de Freud a Lacan, vol. 1: As Bases Conceituais | Marco Antonio Coutinho Jorge | #NF #psicanalise #psicologia #didatico #BR #d3 #e2 #tenho-digital |
| Fundamentos da Psicanálise de Freud a Lacan, vol. 2: A Clínica da Fantasia | Marco Antonio Coutinho Jorge | #NF #psicanalise #didatico #BR #d3 #e2 #tenho-digital |
| Fundamentos da Psicanálise de Freud a Lacan, vol. 3: A Prática Analítica | Marco Antonio Coutinho Jorge | #NF #psicanalise #didatico #BR #d3 #e2 #tenho-digital |
| Fundamentos da Psicologia do Esporte e do Exercício | Robert S. Weinberg e Daniel Gould | #NF #psicologia #esporte #didatico #d2 #e3 #tenho-digital |
| Fundamentos de Psicopatologia Fenomenológica e Daseinsanalyse | Roberto Schmidlin | #NF #psicologia #psicologia-humanista #psicopatologia #filosofia #d3 #e2 #tenho-digital |
| Fundamentos Psicanalíticos: Teoria, Técnica e Clínica | David E. Zimerman | #NF #psicanalise #didatico #BR #RS #d2 #e3 #tenho-digital |
| Habilidades Sociais, Desenvolvimento e Aprendizagem | Almir Del Prette e Zilda A.P. Del Prette (orgs.) | #NF #psicologia #educacao #BR #d3 #e2 #tenho-digital |
| He | Robert A. Johnson | #NF #psicologia #psicologia-analitica #d1 #e1 #trilha-jung-para-comecar #tenho-digital |
| Heranças Invisíveis do Abandono Afetivo: Um Estudo Psicanalítico sobre as Dimensões da Experiência Traumática | Daniel Schor | #NF #psicanalise #d3 #e2 #tenho-digital |
| História Bizarra da Psicologia | Raquel Sodré | #NF #psicologia #historia #humor #BR #d1 #e1 #tenho-digital |
| História da Psicologia Moderna | C. James Goodwin | #NF #psicologia #introducao #historia #didatico #d2 #e3 #tenho-digital |
| História da Psicologia: Rumos e Percursos | Ana Maria Jacó-Vilela, Arthur Arruda Leal Ferreira e Francisco Teixeira Portugal (orgs.) | #NF #psicologia #introducao #historia #didatico #BR #d3 #e3 #tenho-digital |
| História da Psicologia sem as Partes Chatas | Joel Levy | #NF #psicologia #introducao #historia #humor #d1 #e1 #trilha-formacao-do-terapeuta #tenho-digital |
| Imitação: Seu Lugar na Psicanálise | Paulo de Carvalho Ribeiro | #NF #psicanalise #BR #d3 #e2 #tenho-digital |
| (In)distraível | Nir Eyal | #NF #autoconhecimento #d1 #e2 #tenho-digital |
| Inconsciente Social | Carla Penna | #NF #psicanalise #psicologia-social #d3 #e2 #tenho-digital |
| Inovações em Terapia Cognitivo-Comportamental | Amy Wenzel | #NF #psicologia #tcc #d3 #e2 #tenho-digital |
| Instrumentação Psicológica | Luiz Pasquali | #NF #psicologia #psicometria #didatico #BR #d3 #e3 #tenho-digital |
| Inteligência do Carisma: A Nova Ciência por Trás do Poder de Atrair e Influenciar | Heni Ozi Cukier | #NF #autoconhecimento #BR #d1 #e2 #tenho-digital |
| Inteligência e Aprendizagem: Desafios Mentais | Vandi Dogado e Sandra Cristina Melchior | #NF #autoconhecimento #educacao #BR #d1 #e1 #tenho-digital |
| Inteligências Múltiplas ao Redor do Mundo | Howard Gardner | #NF #psicologia #educacao #d2 #e3 #tenho-digital |
| Interfaces da Psicanálise | Renato Mezan | #NF #psicanalise #BR #d3 #e3 #tenho-digital |
| Introdução à Epistemologia da Psicologia | Hilton Japiassu | #NF #psicologia #filosofia #BR #d3 #e1 #tenho-digital |
| Introdução a Jacques Lacan | Vladimir Safatle | #NF #psicanalise #introducao #d2 #e1 #trilha-psicanalise-em-degraus #tenho-digital |
| Introdução à Psicologia | Robert S. Feldman | #NF #psicologia #introducao #didatico #d2 #e3 #tenho-digital |
| Introdução à Psicologia (6ª ed.) | (autor não informado) | #NF #psicologia #introducao #didatico #d2 #e3 #verificar #tenho-digital |
| Introdução à Psicologia das Diferenças Individuais | Carmen Flores-Mendoza e Roberto Colom (orgs.) | #NF #psicologia #psicometria #didatico #BR #d3 #e2 #tenho-digital |
| Introdução à Psicologia do Ser | Abraham Maslow | #NF #psicologia #psicologia-humanista #classico #d2 #e2 #tenho-digital |
| Introdução à Psicologia Fenomenológica: A Nova Psicologia de Edmund Husserl | Tommy Akira Goto | #NF #psicologia #psicologia-humanista #filosofia #BR #d3 #e2 #tenho-digital |
| Introdução à Psicologia Forense | Paula Inez Cunha Gomide e Sérgio Said Staut Júnior (orgs.) | #NF #psicologia #didatico #BR #d2 #e2 #tenho-digital |
| Introdução à Psicologia Junguiana | Heráclito Pinheiro | #NF #psicologia #psicologia-analitica #introducao #BR #d1 #e1 #trilha-jung-para-comecar #tenho-digital |
| Introdução à Topologia de Lacan | J.-D. Nasio | #NF #psicanalise #d3 #e1 #tenho-digital |
| Introdução às Obras de Freud, Ferenczi, Groddeck, Klein, Winnicott, Dolto, Lacan | J.-D. Nasio (org.) | #NF #psicanalise #introducao #d2 #e2 #tenho-digital |
| Introdução Clínica a Freud | Bruce Fink | #NF #psicanalise #introducao #d2 #e2 #tenho-digital |
| Introdução Clínica à Psicanálise Lacaniana | Bruce Fink | #NF #psicanalise #introducao #d2 #e2 #trilha-psicanalise-em-degraus #tenho-digital |
| Já Entendi: Como Aprender Mais e Melhor Estudando Sozinho | Gladys Mariotto | #NF #autoconhecimento #educacao #BR #d1 #e1 #tenho-digital |
| Jean Piaget no Século XXI: Escritos de Epistemologia e Psicologia Genéticas | Adrián Oscar Dongo Montoya (org.) | #NF #psicologia #educacao #BR #d3 #e2 #tenho-digital |
| Jung e a Construção da Psicologia Moderna: O Sonho de uma Ciência | Sonu Shamdasani | #NF #psicologia #psicologia-analitica #historia #d3 #e3 #tenho-digital |
| Jung e o Tarô: Uma Jornada Arquetípica | Sallie Nichols | #NF #psicologia #psicologia-analitica #mistica #d2 #e2 #tenho-digital |
| Jung: Na Fronteira do Espírito | José Carlos Leal | #NF #psicologia #psicologia-analitica #espiritualidade #BR #d2 #e2 #tenho-digital |
| Jung: Vida e Obra | Nise da Silveira | #NF #psicologia #psicologia-analitica #introducao #biografia #classico #BR #d1 #e1 #trilha-jung-para-comecar #tenho-digital |
| Kafka para Sobrecarregados | Allan Percy | #NF #autoconhecimento #d1 #e1 #tenho-digital |
| Lacan: La Formation Du Concept de Sujet | Bertrand Ogilvie | #NF #psicanalise #filosofia #d3 #e1 #tenho-digital |
| Lacan, o Grande Freudiano | Marco Antonio Coutinho Jorge e Nadiá Paulo Ferreira | #NF #psicanalise #introducao #biografia #BR #d1 #e1 #tenho-digital |
| Ler Freud: Guia de Leitura da Obra de Sigmund Freud | Jean-Michel Quinodoz | #NF #psicanalise #introducao #didatico #d2 #e2 #tenho-digital |
| Lições sobre os Sete Conceitos Cruciais da Psicanálise | J.-D. Nasio | #NF #psicanalise #introducao #d2 #e1 #tenho-digital |
| Linguagem e Psicanálise | Leila Longo | #NF #psicanalise #linguagem #introducao #BR #d2 #e1 #tenho-digital |
| Linguagem: Os Segredos da Sedução pela Poderosa Força das Palavras | (autor não informado) | #NF #autoconhecimento #d1 #e1 #verificar #tenho-digital |
| Mal-estar na Atualidade: A Psicanálise e as Novas Formas de Subjetivação | Joel Birman | #NF #psicanalise #d3 #e2 #tenho-digital |
| Mal-estar, Sofrimento e Sintoma: Uma Psicopatologia do Brasil entre Muros | Christian Dunker | #NF #psicologia #psicanalise #psicopatologia #BR #d3 #e2 #tenho-digital |
| Manipulação | (autor não informado) | #NF #autoconhecimento #d1 #e1 #verificar #tenho-digital |
| Manual Clínico dos Transtornos Psicológicos | David H. Barlow | #NF #psicologia #tcc #psicopatologia #didatico #d3 #e3 #tenho-digital |
| Manual de Persuasão do FBI | Jack Shafer | #NF #autoconhecimento #psicologia-social #d1 #e2 #tenho-digital |
| Manual de Psicologia Hospitalar: O Mapa da Doença | Alfredo Simonetti | #NF #psicologia #medicina #BR #d2 #e1 #tenho-digital |
| Manual de Psicopatologia | Elie Cheniaux | #NF #psicologia #psicopatologia #didatico #psiquiatria #BR #d2 #e2 #trilha-formacao-do-terapeuta #tenho-digital |
| Manual de Técnica Psicanalítica: Uma Re-visão | David E. Zimerman | #NF #psicanalise #didatico #BR #RS #d2 #e3 #tenho-digital |
| Manual do Homem Moderno | J.F. Rozza | #NF #autoconhecimento #BR #d1 #e1 #tenho-digital |
| Manual do Xaveco: Como Conquistar uma Mulher | (autor não informado) | #NF #autoconhecimento #d1 #e1 #verificar #tenho-digital |
| Manual do Xavequeiro | Fabiano Rampazzo | #NF #autoconhecimento #humor #BR #d1 #e1 #tenho-digital |
| Mapas do Significado: A Arquitetura da Crença | Jordan B. Peterson | #NF #psicologia #mitologia #religiao #d3 #e3 #tenho-digital |
| Memórias de um Doente dos Nervos | Daniel Paul Schreber | #NF #psicologia #psicanalise #psiquiatria #testemunho #classico #d3 #e2 #tenho-digital |
| Mentes Ansiosas: O Medo e a Ansiedade Nossos de Cada Dia | Ana Beatriz Barbosa Silva | #NF #psicologia #psicopatologia #BR #d1 #e2 #tenho-digital |
| Mentes Consumistas: Do Consumismo à Compulsão por Compras | Ana Beatriz Barbosa Silva | #NF #psicologia #psicopatologia #BR #d1 #e2 #tenho-digital |
| Mentes Depressivas: As Três Dimensões da Doença do Século | Ana Beatriz Barbosa Silva | #NF #psicologia #psicopatologia #BR #d1 #e2 #tenho-digital |
| Mentes Impiedosas | Taj Nathan | #NF #psicologia #psiquiatria #d1 #e2 #tenho-digital |
| Mentes Inquietas: TDAH: Desatenção, Hiperatividade e Impulsividade | Ana Beatriz Barbosa Silva | #NF #psicologia #psicopatologia #BR #d1 #e2 #tenho-digital |
| Mentes Maquiavélicas: A Psicologia da Manipulação | Tamás Bereczkei | #NF #psicologia #psicologia-social #d2 #e2 #tenho-digital |
| Mentes Perigosas: O Psicopata Mora ao Lado | Ana Beatriz Barbosa Silva | #NF #psicologia #psicopatologia #BR #d1 #e2 #tenho-digital |
| Mentes que Amam Demais: O Jeito Borderline de Ser | Ana Beatriz Barbosa Silva | #NF #psicologia #psicopatologia #BR #d1 #e2 #tenho-digital |
| Metamorfoses do Corpo: Uma Pedagogia Freudiana | Sherrine Njaine Borges | #NF #psicologia #psicanalise #BR #d3 #e2 #tenho-digital |
| Mind, Self and Society | George Herbert Mead | #NF #psicologia #psicologia-social #sociologia #classico #d3 #e2 #tenho-digital |
| Mindset: A Nova Psicologia do Sucesso | Carol S. Dweck | #NF #autoconhecimento #psicologia #educacao #d1 #e2 #tenho-digital |
| Mito e Psicanálise | Ana Vicentini de Azevedo | #NF #psicanalise #mitologia #introducao #BR #d2 #e1 #tenho-digital |
| Modificação de Comportamento: O que é e como Fazer | Garry Martin e Joseph Pear | #NF #psicologia #behaviorismo #didatico #d2 #e3 #tenho-digital |
| Nação Dopamina | Anna Lembke | #NF #psicologia #neurociencia #autoconhecimento #d1 #e2 #tenho-digital |
| Não Acredite em Tudo que Você Sente | Robert L. Leahy | #NF #psicologia #tcc #autoconhecimento #d1 #e2 #tenho-digital |
| Não Minta pra Mim: Psicologia da Mentira e Linguagem Corporal | Paulo Sérgio de Camargo | #NF #psicologia #BR #d1 #e1 #tenho-digital |
| Narcisismo e Transformação do Caráter | Nathan Schwartz-Salant | #NF #psicologia #psicologia-analitica #d3 #e2 #tenho-digital |
| Natureza Humana | Donald Winnicott | #NF #psicologia #psicanalise #classico #d3 #e2 #tenho-digital |
| Negocie como se sua Vida Dependesse Disso | Chris Voss e Tahl Raz | #NF #autoconhecimento #gestao #d1 #e2 #tenho-digital |
| Neurose e Não Neurose | Marion Minerbo | #NF #psicanalise #psicopatologia #d3 #e2 #tenho-digital |
| Neurose, Psicose, Perversão | Sigmund Freud | #NF #psicanalise #psicopatologia #classico #d3 #e2 #tenho-digital |
| No Círculo Cínico, ou Caro Lacan, por que Negar a Psicanálise aos Canalhas? | Ricardo Goldenberg | #NF #psicanalise #BR #d3 #e1 #tenho-digital |
| Normose: A Patologia da Normalidade | Pierre Weil, Jean-Yves Leloup e Roberto Crema | #NF #psicologia #espiritualidade #d2 #e1 #tenho-digital |
| O Animal Social | David Brooks | #NF #psicologia #psicologia-social #d1 #e2 #tenho-digital |
| O Cavaleiro Preso na Armadura | Robert Fisher | #F #autoconhecimento #d1 #e1 #tenho-digital |
| O Cérebro de Buda | Rick Hanson | #NF #psicologia #neurociencia #espiritualidade #autoconhecimento #d1 #e2 #tenho-digital |
| O Cérebro e a Inteligência Emocional | Daniel Goleman | #NF #psicologia #neurociencia #d1 #e1 #tenho-digital |
| O Código da Conquista | J.F. Rozza | #NF #autoconhecimento #BR #d1 #e1 #tenho-digital |
| O Código da Inteligência | Augusto Cury | #NF #autoconhecimento #BR #d1 #e2 #tenho-digital |
| O Comportamento Verbal | B.F. Skinner | #NF #psicologia #behaviorismo #linguagem #classico #d3 #e3 #tenho-digital |
| O Conceito de Sujeito | Luciano Elia | #NF #psicanalise #introducao #d2 #e1 #tenho-digital |
| O Demônio do Meio-dia: Uma Anatomia da Depressão | Andrew Solomon | #NF #psicologia #psicopatologia #testemunho #d2 #e3 #tenho-digital |
| O Desafio de Mudar o seu Estilo de Vida | Neil Strauss | #NF #autoconhecimento #d1 #e2 #tenho-digital |
| O Desejo e sua Interpretação | Jacques Lacan | #NF #psicanalise #d3 #e3 #tenho-digital |
| O Desenvolvimento da Personalidade | Carl G. Jung | #NF #psicologia #psicologia-analitica #educacao #classico #d3 #e2 #tenho-digital |
| O Despertar do Fator Alpha | J.F. Rozza | #NF #autoconhecimento #BR #d1 #e1 #tenho-digital |
| O Dogma de Cristo e Outros Ensaios sobre Religião, Psicologia e Cultura | Erich Fromm | #NF #psicologia #psicanalise #religiao #d2 #e2 #rel-fromm #tenho-digital |
| O Efeito Gaslight | Robin Stern | #NF #autoconhecimento #psicologia #d1 #e2 #tenho-digital |
| O Futuro de uma Ilusão | Sigmund Freud | #NF #psicanalise #religiao #classico #d2 #e1 #tenho-digital |
| O Inconsciente a Céu Aberto da Psicose | Colette Soler | #NF #psicologia #psicanalise #psicopatologia #d3 #e2 #tenho-digital |
| O Jogo das Sombras | Connie Zweig e Steve Wolf | #NF #autoconhecimento #psicologia #psicologia-analitica #d2 #e2 #tenho-digital |
| O Livro da Dor e do Amor | J.-D. Nasio | #NF #psicanalise #d2 #e1 #tenho-digital |
| O Livro da Psicologia | Vários autores | #NF #introducao #psicologia #d1 #e2 #tenho-digital |
| O Livro de Lilith | Barbara Black Koltuv | #NF #psicologia #psicologia-analitica #mitologia #genero #d2 #e1 #tenho-digital |
| O Livro Negro da Psicanálise: Viver e Pensar Melhor sem Freud | Catherine Meyer (org.) | #NF #psicanalise #d2 #e3 #tenho-digital |
| O Mal-Estar na Civilização: As Obrigações do Desejo na Era da Globalização | Nina Saroldi | #NF #psicologia #psicanalise #introducao #BR #d2 #e1 #tenho-digital |
| O Manto de Noé: Ensaio sobre a Paternidade | Philippe Julien | #NF #psicologia #psicanalise #parentalidade #d3 #e1 #tenho-digital |
| O Mensageiro Milionário | Brendon Burchard | #NF #autoconhecimento #gestao #d1 #e2 #tenho-digital |
| O Mentalista | Thorsten Havener | #NF #autoconhecimento #d1 #e2 #tenho-digital |
| O Método Fácil para Largar a Pornografia | Hackauthor | #NF #autoconhecimento #d1 #e1 #tenho-digital |
| O Mito da Liberdade | B.F. Skinner | #NF #psicologia #behaviorismo #politica #classico #d2 #e1 #tenho-digital |
| O Paciente, o Terapeuta e o Estado | Elisabeth Roudinesco | #NF #politica #psicanalise #d2 #e1 #tenho-digital |
| O Pai e sua Função em Psicanálise | Joël Dor | #NF #psicanalise #d3 #e1 #tenho-digital |
| O Palhaço e o Psicanalista | Christian Dunker e Cláudio Thebas | #NF #psicanalise #autoconhecimento #BR #d1 #e2 #tenho-digital |
| O Poder da Energia | Brendon Burchard | #NF #autoconhecimento #d1 #e2 #tenho-digital |
| O Poder da Persuasão | Robert Cialdini | #NF #autoconhecimento #psicologia #psicologia-social #d1 #e2 #tenho-digital |
| O Poder do Hábito | Charles Duhigg | #NF #autoconhecimento #psicologia #d1 #e2 #tenho-digital |
| O Prazer de Ler Freud | J.-D. Nasio | #NF #psicanalise #introducao #d1 #e1 #trilha-psicanalise-em-degraus #tenho-digital |
| O que é Psicanálise | Fabio Herrmann | #NF #psicanalise #introducao #BR #d1 #e1 #tenho-digital |
| O que é um Homem? Psicanálise e História da Masculinidade no Ocidente | Pedro Ambra | #NF #psicanalise #genero #historia #BR #d3 #e2 #tenho-digital |
| O que nos Faz Bons ou Maus | Paul Bloom | #NF #psicologia #etica #d1 #e2 #tenho-digital |
| O Saber do Psicanalista | Jacques Lacan | #NF #psicanalise #d3 #e1 #tenho-digital |
| O Significante Imaginário: Psicanálise e Cinema | Christian Metz | #NF #psicanalise #cinema #d3 #e2 #tenho-digital |
| O Sujeito no Labirinto: Um Ensaio Psicológico | José Antônio Damásio Abib | #NF #psicologia #filosofia #BR #d3 #e2 #tenho-digital |
| O Teste do Psicopata: Uma Viagem pela Indústria da Loucura | Jon Ronson | #NF #psicologia #psiquiatria #humor #d1 #e2 #tenho-digital |
| Obras Completas (ed. Imago; vols. 1, 2, 5, 10–17, 19, 21 e 23) | Sigmund Freud | #NF #psicanalise #classico #d3 #e3 #tenho-digital |
| Observações sobre um Planeta Nervoso | Matt Haig | #NF #autoconhecimento #psicologia #d1 #e2 #tenho-digital |
| Olhe nos Meus Olhos | John Elder Robison | #NF #psicologia #testemunho #biografia #d1 #e2 #tenho-digital |
| Os 7 Níveis da Consciência | Rodrigo Duprat | #NF #espiritualidade #autoconhecimento #consciencia #d1 #e1 #tenho-digital |
| Os Delírios da Razão | Magali Gouveia Engel | #NF #psicologia #psiquiatria #historia #BR #d3 #e2 #tenho-digital |
| Os Desafios da Terapia | Irvin D. Yalom | #NF #psicologia #existencialismo #d1 #e2 #rel-yalom #trilha-formacao-do-terapeuta #tenho-digital |
| Os Deuses e o Homem: Uma Nova Psicologia da Vida e dos Amores Masculinos | Jean Shinoda Bolen | #NF #psicologia #psicologia-analitica #mitologia #genero #d1 #e2 #tenho-digital |
| Os Grandes Casos de Psicose | J.-D. Nasio | #NF #psicanalise #psicopatologia #d2 #e2 #tenho-digital |
| Os Homens no Meu Divã: Histórias Reais de Sexo, Amor e Psicoterapia | Brandy Engler e David Rensin | #NF #psicologia #d1 #e2 #tenho-digital |
| Os Olhos de Laura | J.-D. Nasio | #NF #psicanalise #d3 #e1 #tenho-digital |
| Os Pensadores: Pavlov, Skinner | Ivan Pavlov e B.F. Skinner | #NF #psicologia #behaviorismo #classico #d3 #e2 #tenho-digital |
| Os Quatro Vínculos | David E. Zimerman | #NF #psicanalise #d2 #e2 #tenho-digital |
| Oscar Wilde para Inquietos | Allan Percy | #NF #autoconhecimento #d1 #e1 #tenho-digital |
| Pais Brilhantes, Professores Fascinantes | Augusto Cury | #NF #psicologia #parentalidade #educacao #autoconhecimento #BR #d1 #e1 #tenho-digital |
| Paixão da Ignorância: A Escuta entre Psicanálise e Educação | Christian Dunker | #NF #psicanalise #educacao #BR #d2 #e2 #tenho-digital |
| Para Além do Falo: Uma Crítica a Lacan | Teresa Brennan | #NF #psicanalise #genero #d3 #e2 #tenho-digital |
| Para que Serve a Psicanálise? | Denise Maurano | #NF #psicanalise #introducao #BR #d1 #e1 #tenho-digital |
| Para um Homem Novo, uma Nova Psicologia: A Psicologia da Libertação: De Che Guevara a Martín-Baró | Edgar Barrero Cuellar | #NF #psicologia #politica #psicologia-social #latam #d2 #e2 #tenho-digital |
| Patologias do Social: Arqueologias do Sofrimento Psíquico | Vladimir Safatle, Nelson da Silva Junior e Christian Dunker (orgs.) | #NF #psicologia #psicologia-social #psicanalise #politica #BR #d3 #e2 #tenho-digital |
| Pérolas para a Vida: 5.000 Citações | John Blanchard | #NF #autoconhecimento #religiao #d1 #e3 #tenho-digital |
| Personalidade, Ideologia e Psicopatologia Crítica | Virginia Moreira e Tod Sloan | #NF #psicologia #psicopatologia #politica #BR #d3 #e2 #tenho-digital |
| Persuasão, PNL e Hipnose Aplicadas à Sedução | Rafael B. Correa | #NF #autoconhecimento #BR #d1 #e1 #tenho-digital |
| Perversão | Flávio Carvalho Ferraz | #NF #psicanalise #psicopatologia #d2 #e1 #tenho-digital |
| Piaget, Vygotsky, Wallon: Teorias Psicogenéticas em Discussão | Yves de La Taille, Marta Kohl de Oliveira e Heloysa Dantas | #NF #psicologia #educacao #BR #d2 #e1 #tenho-digital |
| Playbook: O Manual da Conquista | Barney Stinson | #NF #autoconhecimento #humor #d1 #e1 #tenho-digital |
| PNL: Programação Neurolinguística | Steve Andreas | #NF #autoconhecimento #d1 #e2 #tenho-digital |
| Poker: A Essência do Texas Hold'em | Carlos Mavca | #NF #didatico #d1 #e1 #tenho-digital |
| Por que Crianças Matam | Gitta Sereny | #NF #psicologia #biografia #d2 #e2 #tenho-digital |
| Por que os Homens Mentem e as Mulheres Choram? | Allan e Barbara Pease | #NF #psicologia #autoconhecimento #genero #humor #d1 #e2 #tenho-digital |
| Princípios Básicos de Análise do Comportamento | Márcio Borges Moreira e Carlos Augusto de Medeiros | #NF #psicologia #behaviorismo #didatico #BR #d2 #e2 #tenho-digital |
| Projeto para uma Psicologia Científica: Freud e as Neurociências | Benilton Bezerra Jr. | #NF #psicanalise #neurociencia #introducao #BR #d2 #e1 #tenho-digital |
| Psicanálise: A Clínica do Real | Jorge Forbes (org.) | #NF #psicanalise #BR #d3 #e2 #tenho-digital |
| Psicanálise: Ciência ou Contraciência? | Hilton Japiassu | #NF #psicanalise #filosofia #BR #d3 #e2 #tenho-digital |
| Psicanálise com Crianças | Teresinha Costa | #NF #psicanalise #introducao #BR #d2 #e1 #tenho-digital |
| Psicanálise & Polética | MD Magno | #NF #psicanalise #BR #d3 #e2 #tenho-digital |
| Psicanálise e Política: Uma Nova Leitura do Populismo | Christian Hoffmann e Joel Birman | #NF #psicanalise #politica #d3 #e1 #tenho-digital |
| Psicanálise e Vida Covidiana: Desamparo Coletivo, Experiência Individual | Ana de Staal (org.) | #NF #psicanalise #d2 #e2 #tenho-digital |
| Psicanálise em Perguntas e Respostas | David E. Zimerman | #NF #psicanalise #introducao #BR #RS #d1 #e2 #tenho-digital |
| Psicodiagnóstico | Claudio Simon Hutz e Denise Ruschel Bandeira | #NF #psicologia #psicometria #didatico #BR #d3 #e2 #tenho-digital |
| Psicologia | Henry Gleitman, Alan J. Fridlund e Daniel Reisberg | #NF #psicologia #introducao #didatico #d2 #e3 #tenho-digital |
| Psicologia Alquímica | James Hillman | #NF #psicologia #psicologia-analitica #mistica #d3 #e2 #tenho-digital |
| Psicologia como Filosofia, Filosofia como Psicologia: Artigos e Avaliações 2006-2019 | Michael Starks | #NF #psicologia #filosofia #d3 #e3 #tenho-digital |
| Psicologia da Arca da Aliança | Adão José Gonçalves da Cruz | #NF #psicologia #religiao #d2 #e2 #tenho-digital |
| Psicologia da Criatividade | Todd Lubart | #NF #psicologia #arte #d2 #e1 #tenho-digital |
| Psicologia da Saúde: Teoria, Intervenção e Pesquisa | Railda Fernandes Alves (org.) | #NF #psicologia #medicina #BR #d3 #e2 #tenho-digital |
| Psicologia das Massas e Análise do Eu: Solidão e Multidão | Ricardo Goldenberg | #NF #psicanalise #introducao #psicologia-social #BR #d2 #e1 #tenho-digital |
| Psicologia das Multidões | Gustave Le Bon | #NF #psicologia #psicologia-social #politica #classico #d2 #e1 #tenho-digital |
| Psicologia de Massas do Fascismo | Wilhelm Reich | #NF #psicologia #psicanalise #politica #autoritarismo #classico #d3 #e2 #tenho-digital |
| Psicologia do Crime | Odon Ramos Maranhão | #NF #psicologia #BR #d2 #e1 #tenho-digital |
| Psicologia do Inconsciente | Carl G. Jung | #NF #psicologia #psicologia-analitica #classico #d3 #e1 #trilha-jung-para-comecar #tenho-digital |
| Psicologia do Jogo | Daniil B. Elkonin | #NF #psicologia #educacao #classico #d3 #e2 #tenho-digital |
| Psicologia do Sexo | Havelock Ellis | #NF #psicologia #classico #d2 #e2 #tenho-digital |
| Psicologia do Sono | Juan Moises de la Serna | #NF #psicologia #neurociencia #d1 #e1 #tenho-digital |
| Psicologia e Religião | Carl G. Jung | #NF #psicologia #psicologia-analitica #religiao #classico #d3 #e1 #trilha-jung-para-comecar #tenho-digital |
| Psicologia e Religião Oriental | Carl G. Jung | #NF #psicologia #psicologia-analitica #religiao #oriental #classico #d3 #e1 #tenho-digital |
| Psicologia e Sociologia | (autor não informado) | #NF #psicologia #psicologia-social #d2 #e2 #verificar #tenho-digital |
| Psicologia Evolucionista | Armando Correa de Siqueira Neto | #NF #psicologia #biologia #BR #d2 #e1 #tenho-digital |
| Psicologia Existencial | Rollo May | #NF #psicologia #psicologia-humanista #existencialismo #d2 #e1 #tenho-digital |
| Psicologia Fácil | Ana Mercês Bahia Bock, Odair Furtado e Maria de Lourdes Trassi Teixeira | #NF #psicologia #introducao #didatico #BR #d1 #e2 #tenho-digital |
| Psicologia Fenomenológica Existencial: A Prática Psicológica à Luz de Heidegger | Paulo Eduardo Rodrigues Alves Evangelista | #NF #psicologia #psicologia-humanista #filosofia #existencialismo #BR #d3 #e2 #tenho-digital |
| Psicologia Forense: Pesquisa, Prática Clínica e Aplicações | Matthew T. Huss | #NF #psicologia #psicopatologia #didatico #d2 #e3 #tenho-digital |
| Psicologia Hospitalar: Teoria e Prática | Fernanda Alves Rodrigues Trucharte e outros | #NF #psicologia #medicina #BR #d2 #e2 #tenho-digital |
| Psicologia para Concursos e Graduação | Leticia Azzolin Becker | #NF #psicologia #introducao #didatico #BR #d1 #e2 #tenho-digital |
| Psicologia para Leigos | Adam Cash | #NF #psicologia #introducao #d1 #e2 #tenho-digital |
| Psicologia, PNL e Hipnose Aplicada à Sedução | Rafael B. Correa | #NF #autoconhecimento #BR #d1 #e1 #tenho-digital |
| Psicologia Positiva | José H. Barros de Oliveira | #NF #psicologia #psicologia-humanista #d2 #e2 #tenho-digital |
| Psicologia Social | David G. Myers | #NF #psicologia #psicologia-social #didatico #d2 #e3 #tenho-digital |
| Psicologia Social Contemporânea | Maria da Graça Corrêa Jacques e outros | #NF #psicologia #psicologia-social #didatico #BR #d2 #e2 #tenho-digital |
| Psicologia Social e Pessoalidade | Mary Jane P. Spink | #NF #psicologia #psicologia-social #BR #d3 #e2 #tenho-digital |
| Psicologia Social: Principais Temas e Vertentes | Cláudio V. Torres e Elaine R. Neiva (orgs.) | #NF #psicologia #psicologia-social #didatico #BR #d3 #e2 #tenho-digital |
| Psicologia, Subjetividade e Políticas Públicas | Ana Mercês Bahia Bock e Maria da Graça M. Gonçalves | #NF #psicologia #politica #psicologia-social #BR #d2 #e2 #tenho-digital |
| Psicologias: Uma Introdução ao Estudo de Psicologia | Ana Mercês Bahia Bock, Odair Furtado e Maria de Lourdes Trassi Teixeira | #NF #psicologia #introducao #didatico #BR #d1 #e2 #trilha-formacao-do-terapeuta #tenho-digital |
| Psicometria | Claudio Simon Hutz, Denise Ruschel Bandeira e Clarissa Marceli Trentini (orgs.) | #NF #psicologia #psicometria #didatico #BR #d3 #e2 #tenho-digital |
| Psicometria e Estatística Aplicada à Neuropsicologia Clínica | Laiss Bertola | #NF #psicologia #psicometria #matematica #neurociencia #BR #d3 #e2 #tenho-digital |
| Psicopatas do Cotidiano | Katia Mecler | #NF #psicologia #psicopatologia #BR #d1 #e2 #tenho-digital |
| Psicopatologia | Susan Krauss Whitbourne e Richard P. Halgin | #NF #psicologia #psicopatologia #didatico #d2 #e3 #tenho-digital |
| Psicopatologia Crítica: Guia Didático para Estudantes e Profissionais de Psicologia | Rogério Paes Henriques | #NF #psicologia #psicopatologia #didatico #BR #d2 #e2 #tenho-digital |
| Psicopatologia e Semiologia dos Transtornos Mentais | Paulo Dalgalarrondo | #NF #psicologia #psicopatologia #didatico #psiquiatria #BR #d3 #e3 #tenho-digital |
| Psicopatologia Lacaniana, vol. 1: Semiologia | Antônio Teixeira e Heloisa Caldas (orgs.) | #NF #psicanalise #psicopatologia #BR #d3 #e2 #tenho-digital |
| Psicopolítica e Psicopatologia do Trabalho | Fernanda Sousa-Duarte, Ana Magnólia Mendes e Emílio Peres Facas (orgs.) | #NF #psicologia #politica #BR #d3 #e2 #tenho-digital |
| Psicoterapia Positiva: Manual do Terapeuta | Tayyab Rashid e Martin Seligman | #NF #psicologia #didatico #psicologia-humanista #d2 #e3 #tenho-digital |
| Psicoterapias: Abordagens Atuais | Aristides Volpato Cordioli e Eugenio Horacio Grevet (orgs.) | #NF #psicologia #introducao #didatico #BR #RS #d3 #e3 #trilha-formacao-do-terapeuta #tenho-digital |
| Psicoterapias Cognitivo-Comportamentais: Um Diálogo com a Psiquiatria | Bernard Rangé (org.) | #NF #psicologia #tcc #didatico #psiquiatria #BR #d3 #e3 #tenho-digital |
| Re-Vendo a Psicologia | James Hillman | #NF #psicologia #psicologia-analitica #d3 #e2 #tenho-digital |
| Reinvenção da Intimidade | Christian Dunker | #NF #psicologia #psicanalise #BR #d2 #e2 #tenho-digital |
| Relacionamento para Leigos | Frederico Mattos | #NF #autoconhecimento #BR #d1 #e2 #tenho-digital |
| Religião, Psicopatologia e Saúde Mental | Paulo Dalgalarrondo | #NF #psicologia #psicopatologia #religiao #psiquiatria #BR #d3 #e2 #tenho-digital |
| Revolução na Psicologia: Da Alienação à Emancipação | Ian Parker | #NF #psicologia #politica #d3 #e2 #tenho-digital |
| Ruído | (autor não informado) | #NF #psicologia #d2 #e2 #verificar #tenho-digital |
| Seu Cérebro na Pornografia: Pornografia na Internet e a Ciência Emergente do Vício | Gary Wilson | #NF #autoconhecimento #neurociencia #d1 #e1 #tenho-digital |
| She | Robert A. Johnson | #NF #psicologia #psicologia-analitica #d1 #e1 #tenho-digital |
| Shoshana Felman e a Coisa Literária: Escrita, Loucura e Psicanálise | Lucia Castello Branco | #NF #psicanalise #escrita #BR #d3 #e2 #tenho-digital |
| Só Freud Explica | Joel Levy | #NF #psicanalise #introducao #d1 #e1 #trilha-psicanalise-em-degraus #tenho-digital |
| Sobre Comportamento e Cognição (vols. 1–6) | Vários autores | #NF #psicologia #behaviorismo #tcc #BR #d3 #e3 #tenho-digital |
| Sobre Ética e Psicanálise | Maria Rita Kehl | #NF #psicanalise #etica #BR #d2 #e1 #tenho-digital |
| Sobre o Behaviorismo | B.F. Skinner | #NF #psicologia #behaviorismo #classico #d2 #e2 #tenho-digital |
| Solidão | Anthony Storr | #NF #autoconhecimento #psicologia #psicanalise #d2 #e2 #tenho-digital |
| Sonho e Mito: Um Estudo sobre a Psicologia dos Povos | Karl Abraham | #NF #psicologia #psicanalise #mitologia #classico #d3 #e1 #tenho-digital |
| Sonhos Confinados | Christian Dunker e outros | #NF #psicologia #psicanalise #BR #d2 #e2 #tenho-digital |
| Subversão | Alex Silva Dias | #NF #psicologia #d2 #e2 #tenho-digital |
| Sujeitos da Psicanálise | Thomas Ogden | #NF #psicanalise #d3 #e2 #tenho-digital |
| Talvez Você Deva Conversar com Alguém: Uma Terapeuta, o Terapeuta Dela e a Vida de Todos Nós | Lori Gottlieb | #NF #psicologia #testemunho #d1 #e2 #tenho-digital |
| Técnicas de Terapia Cognitiva: Manual do Terapeuta | Robert L. Leahy | #NF #psicologia #tcc #didatico #d2 #e2 #tenho-digital |
| Temas Clássicos de Psicologia sob a Ótica da Análise do Comportamento | Maria Martha Costa Hübner e Márcio Borges Moreira (orgs.) | #NF #psicologia #behaviorismo #BR #d3 #e2 #tenho-digital |
| Teorias da Personalidade | Duane P. Schultz e Sydney E. Schultz | #NF #psicologia #didatico #d2 #e3 #tenho-digital |
| Teorias da Personalidade | Jess Feist, Gregory J. Feist e Tomi-Ann Roberts | #NF #psicologia #didatico #d2 #e3 #tenho-digital |
| Terapia Cognitiva dos Transtornos da Personalidade | Aaron T. Beck, Arthur Freeman e Denise D. Davis | #NF #psicologia #tcc #psicopatologia #d3 #e2 #tenho-digital |
| Terapia Cognitiva para Desafios Clínicos: O que Fazer Quando o Básico Não Funciona | Judith S. Beck | #NF #psicologia #tcc #d3 #e2 #tenho-digital |
| Terapia Cognitivo-Comportamental para Leigos | Rhena Branch e Rob Willson | #NF #psicologia #tcc #autoconhecimento #d1 #e2 #tenho-digital |
| Terapia Cognitivo-Comportamental: Teoria e Prática | Judith S. Beck | #NF #psicologia #tcc #didatico #d2 #e2 #tenho-digital |
| Terapia do Esquema: Guia de Técnicas Cognitivo-Comportamentais Inovadoras | Jeffrey E. Young, Janet S. Klosko e Marjorie E. Weishaar | #NF #psicologia #tcc #didatico #d3 #e3 #tenho-digital |
| Testagem e Avaliação Psicológica: Introdução a Testes e Medidas | Ronald Jay Cohen, Mark E. Swerdlik e Edward D. Sturman | #NF #psicologia #psicometria #didatico #d3 #e3 #tenho-digital |
| The Concept of Science as a Defense Against Psychoanalysis | Marcus Bowman | #NF #psicologia #psicanalise #filosofia #d3 #e2 #tenho-digital |
| The Mystery Method: O Manual de Artes Venusianas | Mystery | #NF #autoconhecimento #d1 #e2 #tenho-digital |
| The Psychology of Revolution | Gustave Le Bon | #NF #psicologia #psicologia-social #politica #classico #d2 #e2 #tenho-digital |
| The Psychology of Socialism | Gustave Le Bon | #NF #psicologia #psicologia-social #politica #classico #d2 #e2 #tenho-digital |
| Tornar-se Pessoa | Carl R. Rogers | #NF #psicologia #psicologia-humanista #classico #d2 #e2 #tenho-digital |
| Transtornos da Personalidade | Mario Rodrigues Louzã Neto e Táki Athanássios Cordás (orgs.) | #NF #psicologia #psiquiatria #psicopatologia #BR #d3 #e2 #tenho-digital |
| Treinamento Cerebral: 79 Jogos e Enigmas Lógicos | Thiago Correa | #NF #autoconhecimento #matematica #d1 #e1 #tenho-digital |
| Tudo o que Você Precisa Saber sobre Psicanálise | Silvia Ons | #NF #psicanalise #introducao #d1 #e1 #tenho-digital |
| Tudo o que Você Precisa Saber sobre Psicologia | Paul Kleinman | #NF #psicologia #introducao #d1 #e2 #tenho-digital |
| Uma Biografia da Depressão | Christian Dunker | #NF #psicologia #psicanalise #psicopatologia #historia #BR #d2 #e2 #tenho-digital |
| Uma Força para o Bem | Daniel Goleman | #NF #autoconhecimento #espiritualidade #etica #d1 #e2 #tenho-digital |
| Uma Questão de Vida e Morte | Irvin D. Yalom e Marilyn Yalom | #NF #psicologia #morte #testemunho #d1 #e2 #rel-yalom #trilha-cuidar-ate-o-fim #tenho-digital |
| Velut Luna: A Clínica Geral da Nova Psicanálise | MD Magno | #NF #psicanalise #BR #d3 #e2 #tenho-digital |
| Vínculo Fantasma: Os Relacionamentos Voláteis da Atualidade | Tatiana Paranaguá | #NF #psicologia #BR #d1 #e1 #tenho-digital |
| Virtudes do Medo | Gavin de Becker | #NF #psicologia #autoconhecimento #d1 #e2 #tenho-digital |
| Visionários: Como Tomar as Decisões que Mais Importam | Steven Johnson | #NF #autoconhecimento #psicologia #d1 #e2 #tenho-digital |
| Vocabulário Contemporâneo de Psicanálise | David E. Zimerman | #NF #psicanalise #didatico #BR #RS #d2 #e3 #tenho-digital |
| Vygotski: A Construção de uma Psicologia Marxista | Silvana Calvo Tuleski | #NF #psicologia #politica #educacao #BR #d3 #e2 #tenho-digital |
| We | Robert A. Johnson | #NF #psicologia #psicologia-analitica #d1 #e1 #tenho-digital |

### 17.15 Espiritualidade, espiritismo e mistérios da consciência

| Título | Autor | Tags |
|---|---|---|
| 108 Contos e Parábolas Orientais | Monja Coen | #NF #espiritualidade #oriental #contos #BR #d1 #e1 #tenho-digital |
| A Anunciação da Umbanda: Como Tudo Começou | Eliana Pacco | #NF #religiao #umbanda #BR #d1 #e1 #tenho-digital |
| A Arte da Cura a Distância: Técnicas Rosacruzes / Concentração e Memorização | H. Spencer Lewis e Sar Alden | #NF #religiao #mistica #d1 #e1 #tenho-digital |
| A Erva do Diabo | Carlos Castaneda | #NF #religiao #mistica #antropologia #espiritualidade #classico #d2 #e2 #tenho-digital |
| A Física da Alma | Amit Goswami | #NF #religiao #espiritualidade #consciencia #fisica #d2 #e2 #tenho-digital |
| A Força dos Mitos | Janer Cristaldo | #NF #religiao #mitologia #BR #RS #d2 #e2 #tenho-digital |
| A Nova Era | Roger Bottini Paranhos | #NF #religiao #espiritismo #BR #d1 #e2 #tenho-digital |
| A Semente de Mostarda | Osho | #NF #religiao #espiritualidade #oriental #d1 #e2 #tenho-digital |
| Amor de Pai | Max Lucado | #NF #religiao #d1 #e1 #tenho-digital |
| As 100 Melhores Histórias da Bíblia | A.S. Franchini e Carmen Seganfredo | #NF #religiao #BR #RS #d1 #e3 #tenho-digital |
| As 100 Melhores Histórias da Mitologia | A.S. Franchini e Carmen Seganfredo | #NF #religiao #mitologia #antiguidade #BR #RS #d1 #e2 #tenho-digital |
| As 100 Melhores Lendas do Folclore Brasileiro | A.S. Franchini | #F #religiao #mitologia #contos #BR #d1 #e2 #tenho-digital |
| As Grandes Histórias da Mitologia Greco-Romana | A.S. Franchini e Carmen Seganfredo | #NF #religiao #mitologia #antiguidade #roma #BR #RS #d1 #e2 #tenho-digital |
| As Mais Belas Parábolas de Todos os Tempos | Alexandre Rangel (org.) | #NF #religiao #contos #d1 #e2 #tenho-digital |
| As Portas da Percepção e Céu e Inferno | Aldous Huxley | #NF #consciencia #mistica #classico #d2 #e1 #tenho-digital |
| Astrologia, Psicologia e os Quatro Elementos | Stephen Arroyo | #NF #psicologia #mistica #d1 #e2 #tenho-digital |
| Caderno de Espiritualidade: Viver a Partir do Silêncio | Anselm Grün | #NF #espiritualidade #religiao #d1 #e1 #tenho-digital |
| Ciência da Religião Aplicada: Ensaios pela Autonomia e Aplicação Profissional | Fábio L. Stern e Matheus Oliva da Costa (orgs.) | #NF #religiao #BR #d3 #e2 #tenho-digital |
| Civilizações Intraterrestres | Grupo Espírita Servos de Jesus | #NF #religiao #espiritismo #enigmas #BR #d1 #e2 #tenho-digital |
| Comentários sobre Biologia, Psicologia e Política da Religião | Michael Starks | #NF #religiao #biologia #psicologia #politica #d3 #e2 #tenho-digital |
| Consciência Quântica | Amit Goswami | #NF #religiao #consciencia #fisica #espiritualidade #d2 #e2 #tenho-digital |
| Contos Chineses | Fernando Corrêa da Silva | #F #religiao #mitologia #contos #asia #d1 #e1 #tenho-digital |
| Contos Fantásticos Filipinos: Igorot, Moro, Povos de Mindanau e Cristianizados | Mabel Cook Cole | #F #contos #mitologia #asia #d1 #e1 #tenho-digital |
| Contos Indígenas Brasileiros | Daniel Munduruku | #F #religiao #mitologia #contos #antropologia #BR #d1 #e1 #tenho-digital |
| Contos Japoneses | Antônio Nojiri e Kikuo Furuno | #F #religiao #mitologia #contos #asia #d1 #e1 #tenho-digital |
| Crônicas de Além-Túmulo | Humberto de Campos / Chico Xavier | #NF #religiao #espiritismo #cronicas #BR #d1 #e2 #tenho-digital |
| Da Criação do Mundo e Outros Escritos | Fílon de Alexandria | #NF #religiao #filosofia #antiguidade #classico #d3 #e2 #tenho-digital |
| Despertar: Um Guia para a Espiritualidade sem Religião | Sam Harris | #NF #espiritualidade #consciencia #neurociencia #d2 #e2 #tenho-digital |
| Deus | José Laércio do Egito | #NF #espiritualidade #mistica #BR #d2 #e2 #tenho-digital |
| Deus: Como Ele Nasceu | Reinaldo José Lopes | #NF #religiao #historia #BR #d1 #e1 #tenho-digital |
| Fé | João Batista Libânio | #NF #religiao #BR #d2 #e1 #tenho-digital |
| Fisiologia da Alma | Ramatís / Hercílio Maes | #NF #espiritismo #BR #d2 #e2 #tenho-digital |
| Guia do Praticante de Umbanda: Perguntas e Respostas, Ensaios Teóricos | Douglas Rainho | #NF #religiao #umbanda #BR #d1 #e2 #tenho-digital |
| Guia Ilustrado Zahar: Mitologia | Philip Wilkinson e Neil Philip | #NF #religiao #mitologia #introducao #d1 #e2 #tenho-digital |
| História do Espiritismo | Arthur Conan Doyle | #NF #religiao #espiritismo #historia #classico #d2 #e2 #tenho-digital |
| Inocência, Conhecimento e Encantamento | Osho | #NF #espiritualidade #oriental #d1 #e2 #tenho-digital |
| Introdução à Mitologia | Marly N. Peres | #NF #mitologia #introducao #d1 #e1 #tenho-digital |
| Jornada do Espírito | James Van Praagh | #NF #religiao #espiritismo #d1 #e2 #tenho-digital |
| Lendas Africanas dos Orixás | Pierre Verger | #NF #religiao #mitologia #umbanda #BR #africa #d1 #e1 #trilha-terreiro-e-encruzilhada #tenho-digital |
| Lendas e Fábulas Brasileiras para Crianças | Jossi Borges | #F #religiao #mitologia #contos #BR #d1 #e1 #tenho-digital |
| Manual de Umbanda para Iniciantes | Diamantino Fernandes Trindade | #NF #religiao #umbanda #introducao #BR #d1 #e1 #tenho-digital |
| Mentes Interligadas | Dean Radin | #NF #consciencia #enigmas #d2 #e2 #tenho-digital |
| Métodos de Concentração | Grigori Grabovoi | #NF #mistica #d1 #e1 #tenho-digital |
| Minha Grande Teoria de Tudo: Despertar | Thomas Campbell | #NF #consciencia #espiritualidade #d2 #e3 #tenho-digital |
| Mitologia: Deuses, Heróis e Lendas | Maurício Horta, José Francisco Botelho e Salvador Nogueira | #NF #religiao #mitologia #introducao #BR #d1 #e2 #tenho-digital |
| Murmúrio das Estrelas Matutinas | Vadim Zeland | #NF #espiritualidade #autoconhecimento #d1 #e1 #tenho-digital |
| No Rumo do Mundo de Regeneração | Divaldo Pereira Franco | #NF #religiao #espiritismo #BR #d1 #e2 #tenho-digital |
| Noites Gregas: Histórias, Mitos e Encantos do Mundo Antigo | Cláudio Moreno | #NF #mitologia #antiguidade #BR #RS #d1 #e2 #tenho-digital |
| O Ativista Quântico: Princípios da Física Quântica para Transformar o Mundo e a Nós Mesmos | Amit Goswami | #NF #religiao #espiritualidade #fisica #consciencia #d2 #e2 #tenho-digital |
| O Caibalion | Três Iniciados | #NF #religiao #mistica #classico #d2 #e1 #tenho-digital |
| O Espiritismo, a Magia e as Sete Linhas de Umbanda | Leal de Souza | #NF #religiao #umbanda #espiritismo #classico #BR #d2 #e1 #tenho-digital |
| O Hábito da Intuição: O que a Ciência, a Psicologia e a Mediunidade nos Ensinam sobre Confiar na Nossa Voz Interior | Elizabeth Greenwood | #NF #espiritualidade #psicologia #d1 #e2 #tenho-digital |
| O Livro das Religiões | Vários autores | #NF #introducao #religiao #d1 #e2 #tenho-digital |
| O Livro dos Homens | Osho | #NF #religiao #espiritualidade #d1 #e2 #tenho-digital |
| O Poder do Mito | Joseph Campbell | #NF #mitologia #religiao #classico #d2 #e2 #tenho-digital |
| O Poder do Silêncio | Carlos Castaneda | #NF #mistica #espiritualidade #d2 #e2 #tenho-digital |
| O que é o Espiritismo | Allan Kardec | #NF #religiao #espiritismo #introducao #classico #d1 #e1 #tenho-digital |
| O Ser | José Laércio do Egito | #NF #espiritualidade #mistica #BR #d2 #e2 #tenho-digital |
| O Triângulo das Bermudas | Charles Berlitz | #NF #enigmas #d1 #e2 #tenho-digital |
| Os 7 Temperamentos Humanos | Geoffrey Hodson | #NF #mistica #d1 #e1 #tenho-digital |
| Os Chakras | C.W. Leadbeater | #NF #religiao #mistica #oriental #classico #d2 #e1 #tenho-digital |
| Os Ensinamentos Secretos de Todos os Tempos | Manly P. Hall | #NF #mistica #religiao #d3 #e3 #tenho-digital |
| Os Orixás na Umbanda para Leigos e Iniciantes | Eliana Pacco | #NF #religiao #umbanda #introducao #BR #d1 #e1 #tenho-digital |
| Os Quatro Compromissos | Don Miguel Ruiz | #NF #autoconhecimento #espiritualidade #d1 #e1 #tenho-digital |
| Psicologia Quântica: Como o Software Cerebral Programa Você e o seu Mundo | Robert Anton Wilson | #NF #consciencia #mistica #d2 #e2 #tenho-digital |
| Quatro Contos de Sabedoria dos Povos Africanos | Fabrice Alodji | #F #contos #mitologia #africa #d1 #e1 #tenho-digital |
| Religião: Conceitos-Chave em Filosofia | Brendan Sweetman | #NF #religiao #filosofia #introducao #d2 #e2 #tenho-digital |
| Ressonância Harmônica | Hélio Couto | #NF #religiao #mistica #BR #d1 #e2 #tenho-digital |
| Sexo, Desvio e Danação | Jeffrey Richards | #NF #religiao #historia #medieval #genero #d2 #e2 #tenho-digital |
| Sexo e Religião | Dag Øistein Endsjø | #NF #religiao #historia #genero #d2 #e2 #tenho-digital |
| Somos Todos Filhos dos Deuses | Erich von Däniken | #NF #enigmas #d1 #e2 #tenho-digital |
| Transurfing | Vadim Zeland | #NF #espiritualidade #autoconhecimento #d1 #e1 #tenho-digital |
| Transurfing: Avante para o Passado | Vadim Zeland | #NF #espiritualidade #autoconhecimento #d1 #e1 #tenho-digital |
| Transurfing: Dirigindo sua Realidade | Vadim Zeland | #NF #espiritualidade #autoconhecimento #d1 #e1 #tenho-digital |
| Transurfing: Maçãs Caem ao Céu | Vadim Zeland | #NF #espiritualidade #autoconhecimento #d1 #e1 #tenho-digital |
| Tratado de Psicologia Revolucionária | Samael Aun Weor | #NF #mistica #d2 #e1 #tenho-digital |
| Umbanda Astrológica | Carlos Lima | #NF #religiao #umbanda #mistica #BR #d1 #e1 #tenho-digital |
| Umbanda de A a Z | Norberto Peixoto | #NF #religiao #umbanda #BR #d1 #e2 #tenho-digital |
| Umbanda: Orixás e Entidades | Marcelo Alonso Morais | #NF #religiao #umbanda #BR #d1 #e2 #tenho-digital |
| Umbanda, Religião Brasileira: Um Guia para Leigos e Iniciantes | Flávia Pinto | #NF #religiao #umbanda #introducao #BR #d1 #e1 #trilha-terreiro-e-encruzilhada #tenho-digital |
| Umbandas: Uma História do Brasil | Luiz Antonio Simas | #NF #religiao #umbanda #historia #BR #d2 #e2 #trilha-terreiro-e-encruzilhada #tenho-digital |
| Wabi Sabi: A Sabedoria Japonesa de Apreciar o Imperfeito | Nobuo Suzuki | #NF #espiritualidade #oriental #autoconhecimento #d1 #e1 #tenho-digital |
| Zen em Quadrinhos | Tsai Chih Chung | #HQ #espiritualidade #oriental #filosofia #asia #d1 #e1 #tenho-digital |

### 17.16 Artes, escrita, cinema e parentalidade

| Título | Autor | Tags |
|---|---|---|
| 100 Exercícios de Escrita Criativa, vol. 1: Iniciantes | Mário Falcão | #NF #escrita #didatico #BR #d1 #e1 #tenho-digital |
| 1001 Atividades para Fazer com suas Crianças | Carly Waller Krueger | #NF #parentalidade #d1 #e2 #tenho-digital |
| 5 Lições de Storytelling | James McSill | #NF #escrita #d1 #e1 #tenho-digital |
| 50 Fatos que Mudaram a História do Rock | Paolo Hewitt | #NF #historia #arte #d1 #e2 #tenho-digital |
| A Civilização do Espetáculo | Mario Vargas Llosa | #NF #arte #sociologia #latam #d2 #e1 #tenho-digital |
| A Fotografia Minimalista | Antony Zacharias | #NF #arte #didatico #d1 #e1 #tenho-digital |
| A Orgia Perpétua | Mario Vargas Llosa | #NF #arte #escrita #latam #d3 #e2 #tenho-digital |
| A República Cantada: Do Choro ao Funk, a História do Brasil Através da Música | André Diniz e Diogo Cunha | #NF #arte #historia #BR #d1 #e2 #tenho-digital |
| Brevidade Inteligente: O Poder de Dizer Muito com Poucas Palavras | Jim VandeHei, Mike Allen e Roy Schwartz | #NF #escrita #gestao #d1 #e1 #tenho-digital |
| Brincadeiras Criativas para o seu Bebê | Christopher Clouder e Janni Nicol | #NF #parentalidade #d1 #e1 #tenho-digital |
| Brincar com Tradição: Jogos Tradicionais para Crianças | Patrícia Pereira Santos | #NF #parentalidade #d1 #e1 #tenho-digital |
| Clases de Literatura | Julio Cortázar | #NF #arte #escrita #latam #d2 #e2 #tenho-digital |
| Como Criar Histórias: Um Guia Prático para Escritores | Ursula K. Le Guin | #NF #escrita #didatico #d1 #e1 #tenho-digital |
| Como Educar um Viking: O Segredo dos Países Nórdicos para Criar Crianças Felizes, Saudáveis e Independentes | Helen Russell | #NF #parentalidade #d1 #e2 #tenho-digital |
| Como Falar para seu Filho Ouvir e como Ouvir para seu Filho Falar | Adele Faber e Elaine Mazlish | #NF #parentalidade #d1 #e2 #trilha-pai-em-construcao #tenho-digital |
| Como Ficar Sozinho | Jonathan Franzen | #NF #escrita #d2 #e2 #tenho-digital |
| Como Ler Livros: O Guia Clássico para a Leitura Inteligente | Mortimer J. Adler e Charles Van Doren | #NF #escrita #educacao #classico #d2 #e2 #tenho-digital |
| Como Ouvir as Crianças e Responder às suas Perguntas Mais Difíceis | Claude Halmos | #NF #parentalidade #psicanalise #d1 #e1 #tenho-digital |
| Como Star Wars Conquistou o Universo: O Passado, Presente e o Futuro da Franquia Multibilionária | Chris Taylor | #NF #arte #cinema #d1 #e3 #tenho-digital |
| Como Ver um Filme | Ana Maria Bahiana | #NF #arte #cinema #BR #d1 #e1 #tenho-digital |
| Crianças Dinamarquesas: O que as Pessoas Mais Felizes do Mundo Sabem sobre Criar Filhos Confiantes e Capazes | Jessica Joelle Alexander e Iben Dissing Sandahl | #NF #parentalidade #d1 #e1 #tenho-digital |
| Crianças Francesas Não Fazem Manha | Pamela Druckerman | #NF #parentalidade #d1 #e2 #tenho-digital |
| Crianças Inteligentes: 100 Ideias de Brincadeiras Criativas para Crianças de 2 a 5 Anos | Julian Chomet e Caroline Fertleman | #NF #parentalidade #d1 #e1 #tenho-digital |
| Crônicas de Pai | Leo Aversa | #NF #parentalidade #cronicas #humor #BR #d1 #e1 #trilha-pai-em-construcao #tenho-digital |
| Ensaio Autobiográfico | Jorge Luis Borges | #NF #arte #biografia #escrita #latam #d1 #e1 #tenho-digital |
| Filosofando no Cinema | Ollivier Pourriol | #NF #arte #cinema #filosofia #d2 #e2 #tenho-digital |
| Guia Único das Ciências Humanas na Redação: Como Trabalhar o Repertório Sociocultural | Nelson Adrian | #NF #escrita #didatico #educacao #BR #d1 #e2 #tenho-digital |
| Homens Difíceis: Os Bastidores do Processo Criativo de Breaking Bad, Família Soprano, Mad Men e Outras Séries Revolucionárias | Brett Martin | #NF #arte #cinema #d1 #e2 #tenho-digital |
| Lobisomem: O Apocalipse – Livro da Wyrm | Brian Campbell, Sam Inabinet e outros | #NF #fantasia #horror #d1 #e2 #tenho-digital |
| Machado e Borges e Outros Ensaios sobre Machado de Assis | Luis Augusto Fischer | #NF #arte #escrita #BR #RS #d3 #e2 #tenho-digital |
| Marvel Universe: Map by Map | Nick Jones | #NF #super-herois #arte #d1 #e2 #tenho-digital |
| Meu Pai Fala Cada uma | Justin Halpern | #NF #parentalidade #humor #d1 #e1 #tenho-digital |
| Modus Operandi: Guia de True Crime | Carol Moreira e Mabê Bonafé | #NF #arte #BR #d1 #e2 #tenho-digital |
| O Ato Criativo | Rick Rubin | #NF #arte #d1 #e2 #tenho-digital |
| O Guia Completo do Storytelling | Fernando Palacios e Martha Terenzzo | #NF #escrita #gestao #BR #d1 #e2 #tenho-digital |
| O Livro da Literatura | Vários autores | #NF #introducao #escrita #d1 #e2 #tenho-digital |
| O Livro que Você Gostaria que seus Pais Tivessem Lido | Philippa Perry | #NF #parentalidade #psicologia #d1 #e2 #trilha-pai-em-construcao #tenho-digital |
| O Papai é Pop | Marcos Piangers | #NF #parentalidade #cronicas #humor #BR #RS #d1 #e1 #trilha-pai-em-construcao #tenho-digital |
| O Papai é Pop 2 | Marcos Piangers | #NF #parentalidade #cronicas #humor #BR #RS #d1 #e1 #tenho-digital |
| O Poder da Arte | Simon Schama | #NF #arte #historia #biografia #d2 #e3 #tenho-digital |
| Obra Crítica | Julio Cortázar | #NF #arte #escrita #latam #d3 #e3 #tenho-digital |
| Outras Inquisições | Jorge Luis Borges | #NF #arte #escrita #filosofia #classico #latam #d3 #e2 #trilha-labirintos-de-borges #tenho-digital |
| Pequenas Resistências | Rivka Galchen | #NF #parentalidade #escrita #d1 #e1 #tenho-digital |
| Questão de Ênfase | Susan Sontag | #NF #arte #escrita #d2 #e2 #tenho-digital |
| Sem Tempo a Perder | Ursula K. Le Guin | #NF #escrita #d1 #e1 #tenho-digital |
| Storytelling: A Arte de Contar Histórias | Jéssica Milato | #NF #escrita #gestao #d1 #e1 #tenho-digital |
| Storytelling: Aprenda a Contar Histórias com Steve Jobs, Papa Francisco, Churchill e Outras Lendas da Liderança | Carmine Gallo | #NF #escrita #gestao #d1 #e2 #tenho-digital |
| Storytelling: Cativando com a Narrativa | José Antonio Ramalho | #NF #escrita #gestao #d1 #e1 #tenho-digital |
| Storytelling: Como Contar Histórias que Vendem | Gilson Santos | #NF #escrita #gestao #d1 #e1 #tenho-digital |
| Storytelling: Como Contar Histórias sobre Marcas que Não Têm uma Boa História para Contar | Umehara Parente | #NF #escrita #gestao #d1 #e1 #tenho-digital |
| Storytelling: Histórias que Deixam Marcas | Adilson Xavier | #NF #escrita #gestao #d1 #e2 #tenho-digital |
| Storytelling na Prática: 10 Regras Simples para Contar uma Boa História | Dana Norris | #NF #escrita #gestao #d1 #e1 #tenho-digital |
| Storytelling Revelado: Descubra os Segredos das Narrativas Mais Influentes do Mundo | Cria School | #NF #escrita #gestao #d1 #e1 #tenho-digital |
| The Art of Rick and Morty | Justin Roiland | #NF #arte #ficcao-cientifica #humor #d1 #e1 #tenho-digital |
| Tradução, Transposição e Adaptação Intersemióticas | Daniela Aguiar e João Queiroz | #NF #arte #linguagem #d3 #e2 #tenho-digital |
| Uma Introdução à História do Design | Rafael Cardoso | #NF #design #arte #historia #d2 #e2 #tenho-digital |
| Vida: 4 Biografias | Paulo Leminski | #NF #arte #biografia #BR #d2 #e2 #tenho-digital |

---

## Como usar este catálogo

- **Filtrar por tag** (Obsidian: busca `tag:#d1 tag:#e1`; Notion: importe o `.md`/CSV e crie propriedades; Excel: colar como tabela e filtrar a coluna Tags).
- **Combinações úteis:** `#top #d1` (prioridades fáceis) · `#tenho-fisico #d3` (os pesados que já estão na prateleira) · `#tenho-fisico #tenho-digital` (tenho nos dois formatos) · `#tenho-digital #psicanalise` (o que há de psicanálise na biblioteca virtual) · `#HQ #tenho-digital` (os quadrinhos da biblioteca virtual) · `#rel-imortais #F` (afins a Os Imortais) · `#trilha-alma-russa` (um roteiro pronto) · `#q-morte-e-finitude #F` (uma pergunta, em ficção) · `#papel-porta-de-entrada #d1` (portas de entrada fáceis) · `#tenho-digital #d1 #e1` (leituras rápidas que já estão em arquivo) · `#BR #RS` (gaúchos) · `#sem-pt` (títulos para conferir edição) · `#verificar` (dados a confirmar).
- **Observações de dados:** na prateleira, *Guerra e Paz* aparece com autoria de Dostoiévski, mas é de Tolstói; *Notas do Subsolo* é a tradução do mesmo livro conhecido como *Memórias do Subsolo*; *O Xamã* e *Xamã* são o mesmo livro; *A Ilha* tem dois títulos diferentes (Huxley e Benchley). Itens com `#verificar` precisam de conferência de autor, título ou edição.
- **Biblioteca virtual:** a seção 17 é gerada; para corrigir um livro digital — título, autor, eixo, tipo, dificuldade, extensão ou temas —, edite a linha dele em `biblioteca-virtual/inventario.tsv` (os marcadores ficam na coluna `marcadores`, sem o `#`) e rode `python tools/atualizar.py`. Na seção 17, só `#lido` e `#top` são postos à mão. Quando o arquivo tem um título e o catálogo outro (edição ou tradução diferente), a ligação fica na coluna `catalogo` do inventário e aparece em `biblioteca-virtual/RESUMO.md`.
- **Título ou autor corrigido:** ao corrigir o título ou o autor de uma linha das seções 0 a 16, registre o nome antigo em `catalogo/renomeados.tsv` (título antigo, autor antigo, título novo, autor novo). Assim o painel reencontra o livro, mantém o que já foi anotado nele e continua a achá-lo pelo nome antigo.
