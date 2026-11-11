# Roteiro

O caminho de desenvolvimento da biblioteca, em etapas pequenas. Cada etapa é uma rodada de trabalho: você pede, o
trabalho é feito e testado, você aprova, e só então entra na versão oficial.

Este arquivo é atualizado ao fim de cada rodada. Para saber em que pé as coisas estão, basta ler a tabela abaixo.

**O painel está no ar:** <https://lucasrangel89.github.io/biblioteca/>

## Onde estamos

| Etapa | O que é | Situação |
| --- | --- | --- |
| 0 | Trazer a biblioteca virtual para o catálogo e para o painel | **Feita** (10/11/2026) |
| 1 | Conferir o que foi importado | **Quase pronta** — falta só o que depende de você (lista abaixo, com a pasta e o nome de cada arquivo) |
| 2 | Decidir o que ficou de fora (quadrinhos, subpastas) | **Feita** (10/11/2026) — ficaram 12 perguntas para você (lista abaixo) |
| 3 | Trocar os dados de exemplo pelos seus | **Em parte** (10/11/2026) — o painel já abre sem nada inventado; falta a sua lista de leituras |
| 4 | Classificar os livros digitais: a vistoria dos marcadores | **Feita** (11/11/2026) — falta a sua conferência por amostragem e quatro dúvidas (lista abaixo) |
| 5 | Rotina à prova de erro | A fazer |
| 6 | Melhorias do painel | **Em parte** (11/11/2026) — endereço próprio, guia Finanças, capas, só o título obrigatório, suas anotações, ordem de compra |
| 7 | A versão 3 do catálogo: camadas e trilhas de leitura | **Feita** (11/11/2026) |

A ordem pode mudar: as etapas que faltam não dependem umas das outras. Se alguma interessar mais, peça por ela.

**Onde procurar cada arquivo.** Nas listas de pendências deste roteiro, cada arquivo vem com a **pasta** e o **nome
exato**, escritos assim: `pasta\nome do arquivo`. A pasta é a da sua biblioteca virtual, com o mesmo nome da listagem
que você enviou. Dá para copiar o nome e colar na busca do Windows.

## Como funciona uma rodada

1. **Você pede**, com as suas palavras. Exemplos: "pode seguir para a próxima etapa", "atualize a biblioteca
   virtual", "o livro tal é do autor tal".
2. **O trabalho é feito e testado.** Você recebe um resumo do que mudou e, se houver, as perguntas que só você pode
   responder.
3. **Você aprova** escrevendo "pode enviar e fazer o merge". Enquanto isso não acontece, nada muda na versão oficial.
4. **O site se atualiza sozinho**, um ou dois minutos depois. Se ainda aparecer a versão antiga, recarregue a
   página. O que você anotou continua lá.

Não é preciso entender de programação para nenhuma das etapas. O que se pede de você é sempre uma decisão ou uma
informação que só você tem (o que está na sua estante, o que você já leu, o que há dentro de um arquivo).

### O site

O painel abre em <https://lucasrangel89.github.io/biblioteca/>, no computador ou no celular.

- **O que você anota fica no navegador em que anotou.** O site no computador, o site no celular e o arquivo aberto
  direto do computador guardam cada um os seus dados; um não enxerga os dos outros.
- **Para levar os dados de um lugar para outro:** no alto da tela, o botão "Seus dados" (o nome aparece ao parar o
  mouse sobre ele) → "Exportar backup (.json)". No outro lugar, "Seus dados" → "Importar backup…" e escolha o
  arquivo que foi baixado. É assim que o que estava no arquivo do computador vai para o site.
- **Vale exportar um backup de vez em quando.** Limpar os dados de navegação do navegador apaga as anotações —
  inclusive os comentários, as capas que você enviou e os arquivos que anexou. O backup leva tudo isso junto.
- **O endereço é público.** Quem o tiver vê a lista de livros, que já é pública no GitHub. O que você anota não sai
  do seu navegador.
- **O painel abre só com o que é seu.** Os dados de exemplo (leituras, datas e valores inventados) não vêm mais
  ligados. Se você já usava o site, eles somem sozinhos na primeira abertura depois de 10/11/2026, e o painel avisa
  (os detalhes estão na etapa 3, abaixo).
- **As capas vêm da internet.** O site inteiro é um arquivo só; a única coisa que ele busca fora são as imagens das
  capas, num catálogo aberto de livros chamado Open Library. Sem internet, ou quando o livro não tem capa, aparece
  um desenho com a inicial do título. Quem preferir desliga as capas em "Seus dados".
- **O arquivo continua valendo.** O `Biblioteca_Lucas_Dashboard.html` do repositório é o mesmo painel e abre sem
  internet. Quem preferir usá-lo baixa o arquivo novo a cada rodada e põe no lugar do antigo, na mesma pasta e com o
  mesmo nome, depois de exportar um backup.

### Quando entrarem livros novos na biblioteca virtual

Isto não é uma etapa: pode ser feito a qualquer momento.

1. Na pasta que mudou, rode o `gerador de nomes.bat` para refazer a listagem.
2. No GitHub, abra `biblioteca-virtual/listagens`, clique em **Add file → Upload files** e envie a listagem, com o
   mesmo nome da anterior.
3. Peça: "atualize a biblioteca virtual".

Sem listagem nova não há o que atualizar: o catálogo já está igual às listagens guardadas.

Vale também para os **quadrinhos**. Edição nova de uma série que já está no catálogo entra sozinha na série; série
nova entra marcada para conferência.

---

## Etapa 1 — Conferir o que foi importado

**Por quê.** O título e o autor de cada livro digital foram deduzidos do nome do arquivo. Na maioria dos casos isso
basta; em alguns o nome não diz o autor, ou é vago demais.

**O que já foi feito** (10/11/2026):

- Dos 36 arquivos marcados para conferir, **24 foram identificados** por pesquisa (título completo e autor) e
  deixaram a lista. De 25 livros sem autor, sobraram 10.
- As ligações entre um arquivo e um livro do catálogo que têm título diferente (outra tradução, um volume de série)
  foram conferidas uma a uma. Estão todas certas.
- Em seis dessas ligações, o catálogo trazia um título traduzido ao pé da letra, que nenhuma edição em português
  tem. Essas **seis recomendações** passaram a ter o título da edição brasileira, que é a que você tem em arquivo:

  | Como estava | Como ficou |
  | --- | --- |
  | O Torno do Céu (Ursula K. Le Guin) | **A Curva do Sonho** |
  | O Nome do Mundo é Floresta (Ursula K. Le Guin) | **Floresta é o Nome do Mundo** |
  | Um Mago de Terramar (Ursula K. Le Guin) | **O Feiticeiro de Terramar** (Ciclo Terramar, vol. 1) |
  | Os Inconsoláveis (Kazuo Ishiguro) | **O Desconsolado** |
  | A Escolha da Vida (Noah Gordon) | **A Escolha da Dra. Cole** |
  | O Problema Spinoza (Irvin D. Yalom) | **O Enigma de Espinosa** |

  Quem procurar no painel pelo nome antigo ainda acha o livro, e a ficha dele diz como se chamava antes.
- Cinco livros da **estante** foram acertados: *Tecnologias e Ferramentas de Gestão (PLT 148)* (antes "148
  Tecnologias e Ferramentas de Gestão", sem autor), *Investigações Cognitivas* (os organizadores são Marcos Barbosa
  de Oliveira e Marta Kohl de Oliveira), *Cevando Mate* (é não ficção), *Megalomania de Freud* e *71 Segundos*
  (título e autor confirmados).

**O que falta — e só você pode responder.** Não precisa responder tudo de uma vez; o que ficar sem resposta continua
marcado com `#verificar` e não atrapalha nada.

*Na estante* — não há arquivo: é o livro de papel. Olhe a capa ou a folha de rosto:

| Livro no catálogo | A dúvida |
| --- | --- |
| *Noite do Sul*, de Érico Veríssimo | Não achei livro dele com esse título. A novela dele chama-se *Noite*. Qual é o título na capa? |
| *A Arte de Envelhecer*, de Irvin D. Yalom | O livro conhecido com esse título é de **Schopenhauer**. Quem é o autor na capa? |
| *Coraline*, de Neil Gaiman | O exemplar da estante é a história em quadrinhos (desenhos de P. Craig Russell) ou o romance ilustrado (Dave McKean)? O arquivo `HQs\Coraline.rar` é a história em quadrinhos |

*Na biblioteca virtual* — abra o arquivo e veja a primeira página:

| Livro no catálogo | Arquivo a abrir (pasta e nome exato) | O que preciso saber |
| --- | --- | --- |
| Linguagem e Cognição | `Filosofia\LINGUAGEM E COGNIÇÃO.pdf` | Autor |
| Engenharia Social | `Sociedade e politica\engenhariasocial.pdf` | Autor e título completo |
| Manipulação | `autoconhecimento e desenvolvimento pessoal\manipulacao.pdf` | Autor e título completo |
| Manual do Xaveco: Como Conquistar uma Mulher | `autoconhecimento e desenvolvimento pessoal\manualdoxaveco-comoconquistarumamulher.pdf` | Autor |
| Linguagem: Os Segredos da Sedução pela Poderosa Força das Palavras | `autoconhecimento e desenvolvimento pessoal\linguagem-ossegredosdaseduopelaforadaspalavras.pdf` | Autor |
| Tesouros Medievais | `historia\tesouros medievais.pdf` | Autor |
| Psicologia e Sociologia | `psicologia social e cultural\psicologia e sociologia.pdf` | Autor |
| El Proceso de Envejecimiento | `psicologia\El proceso de envejecimiento.pdf` | Autor |
| Introdução à Psicologia (6ª ed.) | `historia fundamentos e introducoes psico\Introdução à Psicologia 6ª Edição.pdf` | Autor (há mais de um livro com esse título) |
| Análise e Projeto de Sistemas | `tecnologia e informacao\Análise e projeto de sistemas ( etc.) (Z-Library).epub` | Autor (há mais de um livro com esse título) |
| Ciclo Antarktos (The Antarktos Cycle) | `Terror e horror\Antarktos Ciclo - Edgar Allan Poe.pdf` | É a antologia *The Antarktos Cycle* (Poe, Verne, Lovecraft e outros)? Em que língua? |
| Einstein, Freud e Relações Internacionais | `ciencias\Einstein, Freud e Relações Internacionais ( PDFDrive ).pdf` | É um livro ou um artigo de revista (umas 20 páginas)? |

*Entre as recomendações* há três linhas marcadas com `#verificar` desde antes da biblioteca virtual: *A Guerra do
Fogo* (J.-H. Rosny), *O Médico de Córdoba* (Herbert Le Porrier) e *A Tragédia e a Farsa* (Flávio Henrique Calheiros
Casimiro). **Não há arquivo para abrir:** são livros que você não tem. Os três existem com esses títulos e autores; a
marca fica até alguém confirmar a edição — ou sai, se você disser que pode sair.

**Como responder.** Escreva na conversa, do jeito que for mais fácil: "Manipulação é de Fulano de Tal", "a Coraline
da estante é a HQ". A lista completa e sempre atualizada fica em `biblioteca-virtual/RESUMO.md`, na parte
"A verificar" — também com a pasta e o nome exato de cada arquivo.

**Pronta quando** as listas acima estiverem vazias (ou você disser que o que sobrou pode ficar como está).

## Etapa 2 — Decidir o que ficou de fora

**Por quê.** Nem tudo o que está nas pastas tinha entrado no catálogo: faltavam os quadrinhos, três subpastas sem
listagem e o que não é livro.

**O que você decidiu** (10/11/2026):

- **Quadrinhos entram, uma linha por série.** *Sandman* é uma linha, sejam quantas forem as edições guardadas.
- **As três subpastas sem listagem estão vazias** (`Revistas`, `Didáticos`, `Psicologia Aplicada e Popularização`).
  Não há o que importar delas.
- **O que não é livro continua só no inventário** (apostilas, revistas, artigos).

**O que foi feito** (10/11/2026):

- **243 quadrinhos estão no catálogo**, todos com o marcador `#HQ`: 241 novos, mais *Coraline* e *Maus*, que já
  estavam. As três listagens de HQs tinham 236 arquivos e 106 subpastas. (Hoje são 244: a vistoria dos marcadores,
  na etapa 4, achou mais um, *Blackbird*, guardado numa pasta de livros.)
- **O título e o autor de cada um foram identificados por pesquisa.** O nome dos arquivos traz só o título, às vezes
  abreviado: `Btmn Pdrs Smbrs` é *Batman: Padrões Sombrios*. Nas pastas de um personagem com histórias de várias fases
  (*Batman*, *Thor*, *Hellblazer*), o autor ficou "Vários autores".
- **20 livros em prosa estavam guardados nas pastas de quadrinhos** e entraram como livros: romances da Marvel, *Snow
  Crash*, *Invasores de Corpos*, contos de Robert E. Howard, um livro de arte de *Rick and Morty*. Um deles, *Solomon
  Kane*, já estava no catálogo e só ganhou mais uma edição.
- **A adaptação de um livro tem linha própria**, com "(em quadrinhos)" no título: *1984 (em quadrinhos)*, *Moby Dick
  (em quadrinhos)*. Ter a adaptação não marca o livro original como "tenho em digital".
- **No painel:** o filtro **Tipo** ganhou o botão **HQ**; a ficha de um quadrinho mostra a subpasta em que as edições
  estão; a busca acha a série também pelo nome da subpasta.
- **A listagem `novasHQSS` é a da subpasta `novas`**, que fica dentro de NovasHQs (resposta sua, em 10/11/2026). Essa
  subpasta, portanto, já entrou inteira. Para atualizá-la, envie a listagem nova com o mesmo nome, `novasHQSS`.

**O que continua de fora, e por quê:**

| O quê | Por quê |
| --- | --- |
| As edições dentro das 104 pastas de séries | A listagem só traz o nome da pasta. O catálogo sabe que você tem *Akira*; não sabe quantos volumes |
| Subpasta `Mangás` (dentro de HQs) | Não tem listagem. Se quiser que entre, rode o `gerador de nomes.bat` dentro dela e envie |
| 4 arquivos compactados com o nome cortado: `BTN - Si______ra` (3 partes) e `Lo_____d - Mo_____no` | Não dá para saber o que são sem abrir |
| 2 revistas *Heavy Metal* | São periódicos; ficam só no inventário, como as outras revistas |
| `Revistas`, `Didáticos`, `Psicologia Aplicada e Popularização` | Estão vazias |
| 12 apostilas, 13 periódicos e 3 artigos | Não são livros |

**O que falta — e só você pode responder.** São onze obras que entraram com `#verificar` e mais uma dúvida. Como na
etapa 1, o que ficar sem resposta continua marcado e não atrapalha nada. Está tudo na pasta `HQs`.

| No catálogo | O que abrir (pasta e nome exato) | A dúvida |
| --- | --- | --- |
| *A Vida* | arquivo `HQs\A Vida.pdf` | Quem é o autor? |
| *Os Impostos* | arquivo `HQs\Os Impostos.cbr` | Quem é o autor? |
| *Especial: As Espadas* | arquivo `HQs\Especial - As Espadas.cbr` | É um especial de qual série? Quem é o autor? |
| *Trilogia Lovecraft* | subpasta `HQs\Trilogia Lovecraft` | Quais são os três títulos, e de quem? |
| *Lovecraft* | subpasta `HQs\Lovecraft` | É a HQ *Lovecraft*, de Hans Rodionoff, Keith Giffen e Enrique Breccia? Ou são adaptações de contos? |
| *Caminhos Misteriosos* | subpasta `HQs\Caminhos Misteriosos` | É *Mysterious Ways*, de Jason Rubin e Tyler Kirkham? |
| *Contágio* | subpasta `HQs\Contágio` | É a saga do Batman (1996) ou a minissérie da Marvel (2019)? |
| *Cripta* | subpasta `HQs\Cripta` | Qual revista é? |
| *Habitat* | arquivo `HQs\Habitat.cbr` | É a de Simon Roy? |
| *Rashomon* | arquivo `HQs\Rashomon.rar` | É a de Victor Santos? |
| *Ruído* | arquivo `HQs\Ruído ( etc.) (Z-Library).epub` | É o livro de Daniel Kahneman (*Ruído: Uma Falha no Julgamento Humano*) ou um quadrinho? Entrou como livro |

**Os quatro arquivos compactados de nome cortado** estão fora do catálogo. Se souber o que são, diga, que eles entram:

| O que abrir (pasta e nome exato) | A dúvida |
| --- | --- |
| `HQs\BTN - Si______ra - 01 de 03.rar`, `HQs\BTN - Si______ra - 02 de 03.rar` e `HQs\BTN - Si______ra - 03 de 03.rar` | São as três partes de um mesmo quadrinho. Qual? |
| `HQs\Lo_____d - Mo_____no.rar` | Qual quadrinho é? |

**Pronta quando** cada pasta da biblioteca virtual estiver no catálogo ou tiver a decisão de ficar de fora anotada.
Está: o que entrou e o que ficou de fora estão nas listas acima, e em `biblioteca-virtual/RESUMO.md`.

## Etapa 3 — Trocar os dados de exemplo pelos seus

**Feito** (10/11/2026): **o painel abre sem nenhum número inventado.** As leituras, as datas e os valores de exemplo
saíram; ficou só o catálogo — que, de leituras, sabe de duas: *O Arqueiro* e *O Físico*. Sem compras registradas, a
guia Finanças fica zerada, e cada gráfico vazio diz o que falta para ele se preencher.

- **Se você já usava o site:** na primeira abertura depois desta mudança os dados de exemplo somem sozinhos, uma
  única vez, e o painel avisa.
- **Os livros que você criou ou editou ficam como estavam.** Se a edição foi num livro que trazia data ou valor de
  exemplo, esses números continuam nele: o painel não tem como saber quais você digitou. O aviso mostra quais são
  esses livros, para você conferir. Se eram só testes, "Seus dados" → "Recomeçar do catálogo original" apaga tudo.
- **Para ver os gráficos cheios:** "Seus dados" → "Ver com dados de exemplo". Sai no mesmo lugar, em "Limpar dados de
  exemplo", sem mexer no que você registrou.

**Falta, de você:** uma lista simples do que já leu e do que está lendo — pode ser de memória, sem datas. Se lembrar
de preços ou de quando comprou algum livro da estante, melhor, mas não é necessário. Também dá para marcar direto no
painel ("Já li", "Começar a ler"); aí a informação fica só no navegador em que foi marcada.

**O que será feito com a lista:** os lidos entram no catálogo (`#lido`), para não dependerem do navegador.

**Pronta quando** as suas leituras estiverem no catálogo.

## Etapa 4 — Classificar os livros digitais: a vistoria dos marcadores

**Feita** (entrou em 11/11/2026). O relatório completo, com as listas do que mudou, está em `catalogo/VISTORIA.md`;
ele leva a data de 10/11/2026, o dia em que a vistoria foi feita.

**Por quê.** Os livros que entraram pela biblioteca virtual não tinham dificuldade, extensão nem temas, e o eixo de
cada um vinha da pasta em que o arquivo estava. Não dava para filtrar a biblioteca virtual como se filtra a estante.

**O que foi feito:**

- **As 1.910 linhas da biblioteca virtual foram olhadas uma a uma.** Cada uma ganhou dificuldade (leve, média ou
  exigente), extensão (curta, média ou longa), gênero e temas. Os quadrinhos ganharam o gênero (super-heróis, terror,
  ficção científica, mangá…).
- **189 livros mudaram de eixo**, porque a pasta enganava. "Psicologia, psicanálise e comportamento" tinha 473 livros
  e ficou com 399; "Mente, consciência e neurociência" passou de 32 para 65.
- **29 livros tinham o tipo errado**: *Contato*, de Carl Sagan, constava como não ficção; *A Máquina de Uriel*, como
  ficção. Um deles, *Blackbird*, é um quadrinho que estava numa pasta de livros.
- **44 linhas da estante e das recomendações** tiveram dificuldade, extensão ou temas acertados com a mesma régua.
- **Três obras apareciam duas vezes** e viraram uma linha cada: *Sobrevidas* e *Vidas Seguintes* (o mesmo romance de
  Abdulrazak Gurnah, na edição brasileira e na portuguesa); *O Estilo Emocional do Cérebro* e *El Perfil Emocional de
  tu Cerebro* (em português e em espanhol); *A Próxima Onda*, com dois subtítulos.
- **Três recomendações você já tinha**, com outro título: *The Fisherman* é *O Pescador*; *Olhando para o Sol* é *De
  Frente para o Sol*; e *O Chamado de Cthulhu* está dentro de uma coletânea. Agora aparecem como "tenho em digital".
  As recomendações que você não tem passaram de 435 para **432**.
- **No painel:** os filtros de dificuldade e extensão passaram a alcançar a biblioteca virtual inteira, e os temas
  novos entraram nos filtros. Se você já tinha mexido em algum livro no painel, o que você mudou ficou como estava; o
  resto acompanhou a vistoria.

**A régua.** Dificuldade: leve, média, exigente (densa, técnica ou que pede bagagem). Extensão: até ~250 páginas, de
~250 a ~500, acima de 500 ou série.

**O limite — e é importante.** Nenhum arquivo foi aberto. A dificuldade e a extensão dos livros digitais são
**estimativas** a partir do título, do autor e do tipo de obra. Em livro conhecido, a margem de erro é pequena; em
título obscuro, é um palpite informado.

**De você:**

1. **Conferir por amostragem.** Pegue uns 30 livros que você conhece, veja no painel a dificuldade e a extensão de
   cada um e diga onde a régua errou ("o livro tal é longo, não médio").
2. **Quatro dúvidas** que só se resolvem abrindo o arquivo e olhando o sumário:

| A dúvida | O que abrir (pasta e nome exato) |
| --- | --- |
| *O Chamado de Cthulhu* passou a "tenho em digital" por causa de uma coletânea. O conto está mesmo nela? | `Terror e horror\Biblioteca Lovecraft - Vol. 1 - O chamado de Cthulhu e outras histórias (H. P. Lovecraft [Lovecraft, H. P.]) (Z-Library).pdf` |
| *Nas Montanhas da Loucura*, *A Sombra sobre Innsmouth*, *O Horror de Dunwich* e *Um Sussurro nas Trevas* continuam como recomendações, mas é provável que estejam dentro das coletâneas de Lovecraft que você tem. Quais estão? | `Terror e horror\H. P. Lovecraft - Vol. 2 - Miskatonic Edition (H. P. Lovecraft) (Z-Library).epub`, `Terror e horror\Os melhores contos de H.P. Lovecraft - H.P.pdf`, `Terror e horror\Antologia H. P. Lovecraft - H. P. Lovecraft.pdf`, o arquivo da linha de cima e, na estante, *Lovecraft: Medo Clássico* |
| *A Metamorfose*, de Kafka, continua como recomendação. Está dentro da coletânea que você tem? | `autoconhecimento e desenvolvimento pessoal\Essencial - Franz Kafka.pdf` |
| Dois arquivos de Rafael B. Correa parecem ser o mesmo livro com títulos diferentes. São? | `autoconhecimento e desenvolvimento pessoal\persuasopnlehipnoseaplicadasseduo.pdf` e `autoconhecimento e desenvolvimento pessoal\Rafael B. Correa - Psicologia, PNL e Hipnose Aplicada a Sedução.pdf` |

**Quando entrarem livros novos:** eles chegam sem dificuldade, extensão e temas, e são classificados na mesma rodada
em que a biblioteca virtual for atualizada.

**Pronta quando** der para filtrar a biblioteca virtual por dificuldade e extensão, como já dá com a estante. Dá.

## Etapa 5 — Rotina à prova de erro

**Por quê.** Hoje os testes rodam a pedido; nada impede que uma mudança futura quebre o painel sem ninguém notar. E
atualizar as listagens pede um `gerador de nomes.bat` em cada pasta.

**O que será feito:** os testes passam a rodar sozinhos no GitHub a cada mudança; um único arquivo gera todas as
listagens de uma vez; o material antigo guardado em `referencias/` é revisto.

**De você:** aprovar, e testar o gerador novo uma vez no seu computador.

**Pronta quando** atualizar a biblioteca virtual for: dois cliques, um envio, um pedido.

## Etapa 6 — Melhorias do painel

**Feito** (10/11/2026):

- **O painel abre por um endereço**, inclusive no celular, em vez de ser um arquivo a baixar (ver "O site", acima).
- **Guia Finanças.** Tudo o que é dinheiro — quanto foi investido, preço médio, gastos por período e por loja, as
  compras registradas — saiu da Visão geral e da Biblioteca e foi para uma guia própria.
- **O período foi para dentro de "Mais filtros"**, e a barra de filtros ficou mais curta.
- **Só o título é obrigatório.** Data de aquisição, loja, valor e data de leitura são opcionais em todos os
  formulários: dá para dizer "já tenho" sem dizer quanto custou, e "já li" sem dizer quando.
- **Capas.** 761 dos 2.554 livros aparecem com a capa; os outros, com um desenho com a inicial do título. A busca só
  aceita uma capa quando o título e o autor conferem, e o catálogo de onde elas vêm (Open Library) tem poucas
  edições brasileiras — por isso não são mais.

**Feito** (11/11/2026):

- **Suas anotações.** Na ficha de cada livro (clique no livro, em qualquer lista) há uma parte nova:
  - **Comentários:** um campo para escrever o que quiser sobre o livro. Salva sozinho.
  - **Possui análise:** uma caixa para marcar que você tem resenha, relatório ou fichamento dele. Em "Mais filtros" →
    "Suas marcas", dá para ver só esses livros. A aba "Com anotações", nas tabelas, lista os livros que têm
    comentário, arquivo ou análise.
  - **Anexar arquivo…:** guarda a resenha, o relatório ou outro texto junto do livro (até 8 arquivos por livro, de até
    5 MB cada). Arquivos de texto abrem ali mesmo; qualquer um pode ser baixado de volta.
  - **Enviar capa…:** uma imagem sua passa a ser a capa do livro.
- **Isso tudo fica no seu navegador**, como as leituras e as notas: não vai para a internet nem para o GitHub, e o
  computador não enxerga o que foi posto no celular. O backup ("Seus dados" → "Exportar backup") leva os comentários,
  as capas e os arquivos junto — vale exportar depois de anexar algo que você não queira perder.
- **O que comprar primeiro.** Nas guias Recomendações e Próximas aquisições, as recomendações que você ainda não tem
  aparecem numa ordem sugerida, com o motivo ao lado ("prioridade sua", "é o que falta para fechar a trilha tal",
  "porta de entrada da área", "leve e curta"). Um botão ao lado põe o livro na lista de compra. A ordem se refaz
  sozinha quando você compra ou lê um livro. **É uma sugestão, e não olha preços.**

**Acompanhar preços: o que dá e o que não dá.** O painel **não consulta as lojas**, e não é por falta de fazer: ele é
uma página que roda dentro do seu navegador, e os navegadores não deixam uma página ler o conteúdo de outra (a da
Amazon, por exemplo). Hoje o caminho é: na ficha do livro, "Buscar nas lojas" abre a loja já na busca daquele livro;
você vê o preço e registra em "Monitorar preço" ou "Registrar cotação". A partir daí o painel guarda o histórico,
mostra quando o preço fica abaixo do seu alvo e compara as lojas.

Para os preços entrarem sozinhos seria preciso um serviço rodando fora do painel — no próprio GitHub, uma vez por
dia —, que consultasse as lojas e gravasse os preços. Dá para tentar, mas não dá para prometer: cada loja teria de ser
testada, e várias dificultam a consulta automática. Se interessar, vira uma etapa.

Ideias em aberto; você escolhe quais valem a pena.

- **Preços automáticos:** o serviço descrito acima, começando por uma loja, para ver se funciona.
- **Mais capas:** procurar as que faltam em outra fonte. (Uma a uma, você já pode enviar a capa pelo painel.)
- **Juntar "Próximas aquisições" e "Preços" dentro de Finanças:** hoje são três guias que falam de dinheiro.
- **"Tenho em digital, quero o físico":** hoje um livro ou está no acervo ou está na lista de compras, nunca nos dois.
- **Anotações fora do navegador:** hoje leituras, notas, comentários e arquivos ficam guardados só no navegador em
  que foram feitos, e o backup é manual. Por isso o computador e o celular não mostram as mesmas anotações.

## Etapa 7 — A versão 3 do catálogo: camadas e trilhas de leitura

**Feita** (11/11/2026).

**O que chegou.** Em 10/11/2026 você enviou ao repositório o arquivo `Biblioteca_Lucas_Catalogo_Mestre (2).md`: a
"versão 3" do catálogo, feita fora daqui. Os 644 livros da estante e das recomendações eram os mesmos daqui, mas como
estavam antes das correções das etapas 1 e 2; por isso o arquivo não podia simplesmente tomar o lugar do catálogo. Foi
comparado livro a livro, e o que ele tinha de novo veio para cá.

**O que foi aproveitado:**

- **As camadas, em 442 livros:** a pergunta central do livro (12 perguntas: "o que é humano?", "liberdade e
  obediência"…), o clima da leitura (10), o papel na biblioteca (6: porta de entrada, leitura-relâmpago, desafio…),
  as pontes entre áreas (8) e os cenários (9). Entraram como marcadores nas linhas do catálogo.
- **As 20 trilhas de leitura**, com 169 livros em ordem ("Alma Russa", "Do Aviso ao Espelho"…). Estão em
  `catalogo/trilhas.md`.

**Onde isso aparece no painel:**

- **Na ficha de cada livro**, a parte "Por que ler" mostra as camadas dele e as trilhas de que faz parte.
- **Nos filtros**, cada camada virou um grupo. Marcar dois marcadores mostra os livros que têm os dois — é assim que
  se refazem os "cruzamentos" que o arquivo trazia prontos.
- **Na guia Recomendações**, o quadro "Trilhas de leitura" mostra, de cada trilha, quantos livros você tem, quantos
  leu e o que falta. Abrir uma trilha mostra os livros na ordem. Hoje, numa delas não falta comprar nada ("Aço e
  Fé"), e duas estão a um livro de fechar ("Das Estrelas à Rede" e "Divã e Martelo").
- **A ordem de compra** (etapa 6) usa as trilhas e as camadas: o livro que fecha uma trilha sobe na lista.

**O que não foi aproveitado, e por quê:**

| No arquivo enviado | Por que ficou de fora |
| --- | --- |
| As marcas de posse e formato (`#a-adquirir`, `#ja-tenho`, `#fmt-…`, `#novo-digital`) | Aqui a posse já é `#tenho-fisico` e `#tenho-digital`, conferida com as listagens das pastas. No arquivo, 24 livros que você tem apareciam como se não tivesse |
| A parte "Acervo digital" | Era a biblioteca virtual tirada direto dos nomes dos arquivos: 249 livros sem autor e nenhum quadrinho. A daqui já passou pelas etapas 1, 2 e 4 |
| "Interseções", "Cruzamentos" e o índice das camadas | São listas prontas, que envelhecem a cada livro novo. No painel o mesmo resultado sai dos filtros, sempre em dia |

**Onde ficou o arquivo.** Em `referencias/catalogo-v3-enviado-2026-11-10.md`, com o conteúdo intacto: mudaram só a
pasta e o nome. Nada o lê; está guardado para consulta.

**Pronta quando** as camadas e as trilhas estiverem no catálogo e no painel, e o arquivo enviado tiver saído da pasta
principal. Estão.

---

## Combinados

- **O catálogo é a fonte única.** O painel é gerado a partir dele e nunca é editado à mão.
- **Nada entra sem teste e sem a sua aprovação.**
- **O que você anota no painel é seu e é preservado.** Quando um título ou autor é corrigido no catálogo, o painel
  reencontra o livro e mantém as anotações. Quando a classificação de um livro muda no catálogo, o que você tinha
  mudado à mão fica como você deixou (os detalhes estão no `README.md`).
- **Comentários, capas enviadas e arquivos anexados ficam só no navegador.** O backup leva tudo junto.
- **O painel não inventa nada.** Só mostra o catálogo e o que você registrou; dados de exemplo, só se você pedir.
- **Só o título é obrigatório.** Datas, valores e lojas entram quando você souber e quiser.
- **Na dúvida, fica marcado.** Título ou autor incerto leva `#verificar` em vez de um palpite.
- **Estimativa é dita como estimativa.** A dificuldade e a extensão dos livros digitais foram estimadas sem abrir os
  arquivos; a ordem de compra é uma sugestão. Nenhuma das duas é apresentada como fato.
- **O painel não consulta lojas.** Todo preço é uma cotação registrada por você.
- **Quadrinhos: uma linha por série**, sejam quantas forem as edições guardadas.
- **O que não é livro nem quadrinho fica só no inventário** (apostilas, revistas, artigos), fora do catálogo e do
  painel.
