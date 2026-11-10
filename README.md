# Biblioteca do Lucas

Um catálogo só para as duas bibliotecas — a **estante física** e a **biblioteca virtual** (os livros digitais) — e um
painel que mostra as duas juntas ou separadas.

- **Catálogo Mestre** (`catalogo/Biblioteca_Lucas_Catalogo_Mestre.md`): a fonte única. 2.560 linhas — o que tenho e o
  que foi recomendado.
- **Painel**: no ar em <https://lucasrangel89.github.io/biblioteca/>. É um único arquivo HTML
  (`Biblioteca_Lucas_Dashboard.html`), que também abre direto no navegador, sem internet e sem servidor.
- **Roteiro** (`ROTEIRO.md`): o que já foi feito, o que vem pela frente e o que depende de você, em linguagem simples.

| | Livros e quadrinhos |
| --- | ---: |
| Só na estante física | 73 |
| Na estante **e** na biblioteca virtual | 24 |
| Só na biblioteca virtual | 2.028 |
| Recomendações (ainda não tenho) | 435 |
| **Total no catálogo** | **2.560** |

Estante física: 97 livros. Biblioteca virtual: 2.052 obras — 1.809 livros e 243 quadrinhos — em 2.382 arquivos e 104
pastas de séries de quadrinhos.

## Como um livro é marcado

No catálogo, a posse é um marcador na linha do livro:

| Marcador | Significa |
| --- | --- |
| `#tenho-fisico` | está na estante (antes era `#ja-tenho`) |
| `#tenho-digital` | está na biblioteca virtual |
| os dois | tenho em papel e em arquivo |
| nenhum | é uma recomendação |

- **Seção 0** — a estante física.
- **Seções 1 a 16** — as recomendações, por eixo. As que já tenho em arquivo ganharam `#tenho-digital` e, no painel,
  aparecem no acervo.
- **Seção 17** — o resto da biblioteca virtual, livros e quadrinhos, separado nos mesmos 16 eixos. Esta seção é
  **gerada**: não a edite à mão, exceto para acrescentar marcadores a uma linha (eles são preservados).

**Quadrinhos** levam `#HQ`. Uma série é **uma linha só**, sejam quantas forem as edições guardadas. A adaptação de um
livro tem linha própria — *1984 (em quadrinhos)* — e não marca o livro original como `#tenho-digital`.

## Estrutura

| Caminho | O que é |
| --- | --- |
| `Biblioteca_Lucas_Dashboard.html` | O painel pronto (gerado; não edite à mão). É este arquivo que vai para o site |
| `.github/workflows/publicar-site.yml` | Publica o painel como site a cada mudança em `main` (ver "O site") |
| `.github/workflows/buscar-capas.yml` | Procura as capas dos livros na Open Library e grava `catalogo/capas.tsv`. Só roda quando pedido, pela aba Actions (ver "As capas") |
| `ROTEIRO.md` | As etapas de desenvolvimento e as pendências de cada uma |
| `catalogo/Biblioteca_Lucas_Catalogo_Mestre.md` | O Catálogo Mestre |
| `catalogo/renomeados.tsv` | O nome antigo de cada linha da estante ou das recomendações que teve título ou autor corrigido (ver "Corrigir o título ou o autor…") |
| `catalogo/capas.tsv` | A capa de cada livro: o número da imagem na Open Library, ou vazio quando não foi achada (ver "As capas") |
| `biblioteca-virtual/listagens/*.txte` | A lista de arquivos de cada pasta da biblioteca virtual (uma listagem por pasta) |
| `biblioteca-virtual/inventario.tsv` | Uma linha por arquivo (e por subpasta de série de quadrinhos), com título, autor, eixo e gênero **revisados** — é aqui que se corrige um livro digital |
| `biblioteca-virtual/RESUMO.md` | Relatório da última importação: o que entrou, o que falta conferir e o que ficou de fora (gerado) |
| `biblioteca-virtual/Biblioteca virtual.md` | A listagem original, como foi enviada (só para consulta; os acentos estão corrompidos) |
| `src/` | Fontes do painel: `index.html`, `styles.css`, `js/00-util.js` … `70-app.js`; `catalog.json` e `capas.json` (gerados) |
| `tools/atualizar.py` | Faz tudo de uma vez: importa a biblioteca virtual, converte o catálogo e monta o painel |
| `tools/importar_digital.py` | Listagens + inventário → Catálogo Mestre (seção 17 e `#tenho-digital`) e `RESUMO.md` |
| `tools/build_catalog.py` | Catálogo Mestre + inventário → `src/catalog.json`; `catalogo/capas.tsv` → `src/capas.json` (usa `parse_catalog.py`, `eixos.py` e `capas.py`) |
| `tools/build.py` | `src/` → `Biblioteca_Lucas_Dashboard.html`; confere que não sobrou referência externa |
| `tools/capas.py` | Busca das capas na Open Library → `catalogo/capas.tsv`. É o único script que precisa de internet; no GitHub, quem o roda é o serviço "Buscar capas" |
| `tools/qa/` | Testes automatizados |
| `referencias/` | Material antigo guardado só como referência (um painel de inspiração e um protótipo abandonado) |

## Dia a dia

Só precisa de Python 3; nenhuma biblioteca extra. Os comandos funcionam de qualquer pasta.

```bash
python tools/atualizar.py              # importa, converte e monta o painel
python tools/atualizar.py --conferir   # só mostra o que a importação mudaria; não grava nada
```

Rodar de novo sem ter mudado nada não altera nenhum arquivo.

### Entraram livros novos na biblioteca virtual

1. Refaça a listagem da pasta que mudou e ponha em `biblioteca-virtual/listagens/`, com o nome da pasta
   (no Windows, dentro da pasta: `dir /b > "nome da pasta.txte"`). Para uma pasta nova, basta uma listagem nova.
2. `python tools/atualizar.py`.
3. Cada arquivo novo entra no inventário com a observação `novo`, e título e autor **deduzidos do nome do arquivo**.
   Abra `biblioteca-virtual/inventario.tsv`, confira essas linhas (título, autor, `eixo` de 2 a 16, `genero` F, NF ou
   poesia), apague o `novo` e rode de novo.
4. Arquivo que sumiu da listagem recebe `ausente`: a linha fica no inventário e o livro sai do catálogo.

### Entraram quadrinhos novos

O caminho é o mesmo: listagem nova da pasta, `python tools/atualizar.py`. O que muda nas pastas de quadrinhos (`HQs`,
`novashqs`, `novasHQSS` e qualquer listagem com "hq", "mangá", "quadrinho" ou "gibi" no nome):

- **Cada subpasta é uma série** e vira uma linha do inventário, com `formato` = `pasta`. A listagem só traz o nome
  da subpasta: o catálogo sabe que a série existe, não quantas edições há lá dentro.
- **Edição nova de uma série que já está no inventário entra sozinha na série**, sem nada a revisar: o nome da série é
  tirado do nome do arquivo, sem o grupo que digitalizou, o ano e o número da edição (`Coda #08 [Grupo].cbr` → *Coda*).
  Só vale nome igual: `Batman - Ano Um` não entra na série *Batman*.
- **Série nova** entra com `tipo` = `hq`, a observação `novo` e sem eixo; no catálogo, fica em "17.0 A classificar"
  até a linha ser revisada. Se a mesma série tem arquivos soltos e uma subpasta, dê às linhas o mesmo título e o mesmo
  autor: é isso que as junta numa obra só.
- **Livro em prosa guardado numa pasta de quadrinhos** (um romance, um livro de arte): troque o `tipo` para `livro`
  e o `genero` para F ou NF.
- **Adaptação de um livro:** ponha "(em quadrinhos)" no título. Mesmo sem isso, um quadrinho nunca se liga a uma linha
  do catálogo que não tenha `#HQ`.
- **Subpasta que é outra pasta, com listagem própria:** `novas`, dentro de `novashqs`, é a listagem `novasHQSS`
  (informação do dono da biblioteca). Ela não vira série nem linha do inventário; o que há nela entra por essa
  listagem. A relação está em `SUBPASTAS_LISTADAS`, no começo de `tools/importar_digital.py`; se a listagem da
  subpasta for apagada, a subpasta volta a aparecer no inventário, marcada `novo`.

### Corrigir um livro digital

Corrija a linha no inventário e rode `python tools/atualizar.py`. As colunas:

| Coluna | Conteúdo |
| --- | --- |
| `pasta`, `arquivo`, `formato` | de onde veio (não mexa: é como o arquivo é reconhecido). `formato` = `pasta` é a subpasta de uma série de quadrinhos |
| `tipo` | `livro` ou `hq` entram no catálogo; `apostila`, `periodico`, `artigo` e `outro` ficam só no inventário |
| `titulo`, `autor` | como devem aparecer. Linhas com o mesmo título e o mesmo autor são a mesma obra (dois formatos de um livro; as edições de uma série) |
| `catalogo` | quando o livro já existe no catálogo com outro título (outra tradução, um volume de série), o título de lá |
| `eixo`, `genero` | eixo temático (2 a 16) e F, NF, poesia ou HQ |
| `obs` | `novo`, `ausente`, `verificar` |

O painel acompanha a correção: o livro é reconhecido pelo arquivo, então o que você já tiver anotado nele (leitura,
nota) continua no lugar mesmo que o título mude.

### Corrigir o título ou o autor de um livro da estante ou de uma recomendação

1. Corrija a linha no catálogo.
2. Acrescente uma linha a `catalogo/renomeados.tsv`, com as quatro colunas separadas por tabulação: título antigo,
   autor antigo, título novo, autor novo — escritos como estavam e como ficaram no catálogo.
3. `python tools/atualizar.py`.

O passo 2 existe por causa do que fica guardado no navegador. O painel liga as suas anotações (leitura, nota, preço)
a uma linha do catálogo pelo título e pelo autor; se um dos dois muda, a ligação se perde, e um livro que você já
tinha anotado apareceria **duas vezes**: uma com o nome antigo e as anotações, outra com o nome novo e vazia. Com o
nome antigo registrado, o painel reencontra o livro e só troca o nome. Além disso, a busca continua achando o livro
pelo nome antigo, e a gaveta dele mostra o **título anterior**. Se o nome novo não bater com nenhuma linha do catálogo,
`build_catalog.py` avisa (`AVISO: renomeados.tsv: …`).

As linhas do arquivo não devem ser apagadas depois: alguém pode abrir o painel novo com dados guardados há muito
tempo. Livros da biblioteca virtual não precisam disto — são reconhecidos pelo arquivo.

### Chegou um livro na estante

Acrescente a linha na seção 0 do catálogo com `#tenho-fisico` (ou acrescente `#tenho-fisico` a uma recomendação) e
rode `python tools/atualizar.py`. Também dá para marcar pelo painel ("Já tenho" / "Editar"), mas aí a informação fica
só no navegador.

## O painel

Seis guias: **Visão geral**, **Biblioteca**, **Recomendações**, **Finanças**, **Próximas aquisições** e **Preços**.

- **Acervo: Tudo / Física / Virtual / Nas duas** — o filtro vale para todas as guias. O livro que está nas duas
  bibliotecas aparece como "Físico e digital".
- **Tipo: Todos / Ficção / Não ficção / HQ / Outros** — "Outros" são poesia, antologias e o que não tem tipo. A busca
  também acha um quadrinho pelo nome da subpasta ("Marvel Salvat").
- **Mais filtros** reúne prioridade, dificuldade, extensão, marcadores e o **período** (30 dias, 90 dias, 12 meses,
  este ano, tudo, ou datas à escolha). O período vale pela data de aquisição ou de leitura; sem escolha, o painel
  mostra todo o histórico. No celular, os filtros ficam na folha "Filtros".
- **Dinheiro tem lugar próprio.** Visão geral, Biblioteca e Recomendações não mostram valores. **Finanças** reúne o
  que foi investido, o preço médio pago, os gastos por período e por loja e a tabela das compras registradas;
  Próximas aquisições e Preços continuam com a lista de compra e as cotações.
- A gaveta de cada livro digital mostra **onde ele está**: pasta, formato, número de arquivos e, quando for outra
  edição, o título do arquivo. Na de uma série de quadrinhos guardada em pasta própria, o nome da subpasta.
- **Só o título é obrigatório.** Data de aquisição, loja, valor, condição e data de leitura são opcionais em todos os
  formulários ("Novo livro", "Editar", "Já tenho", "Comprei", "Já li"). O que não foi informado aparece como "sem
  data" ou fica fora da conta: um livro sem valor não entra no investimento; uma leitura sem data conta como
  leitura, mas não aparece nos gráficos por mês nem quando há um período escolhido.
- Os arquivos da biblioteca virtual **não têm data nem valor de compra**. Por isso entram nas contagens, mas não nos
  gráficos de evolução e de investimento; no filtro "Virtual", a compra do exemplar físico de um livro que está nas
  duas não é contada.
- **Preços:** o painel não consulta lojas. Cada preço é uma cotação registrada à mão (há atalhos de busca por loja).

### O que o painel mostra ao abrir

**Só o que é seu:** o catálogo (títulos, autores, marcadores, eixos, a estante e a biblioteca virtual) e o que você
registrar. Nada é inventado: sem compras registradas, Finanças fica zerada e cada gráfico diz o que falta para ele se
preencher.

Os **dados de exemplo** (datas e valores de compra, leituras, notas, lista de próximas aquisições e históricos de
preço simulados, com semente fixa) só entram **a pedido**: botão "Seus dados" → "Ver com dados de exemplo". Enquanto
estão ligados, o painel avisa no alto da tela; saem em "Limpar dados de exemplo", sem mexer no que você registrou.

**Quem usava a versão anterior**, que abria com os exemplos ligados: na primeira abertura do painel novo os exemplos
saem sozinhos, uma única vez, com aviso. Os livros que a pessoa criou ou editou enquanto os exemplos estavam ligados
ficam como estavam — podem trazer datas ou valores de exemplo misturados ao que foi anotado, porque o painel não tem
como separar um do outro. O aviso leva até esses livros (lista "Editados por você"); se eram só testes, "Seus dados" →
"Recomeçar do catálogo original" apaga tudo.

Os dados do usuário ficam no `localStorage` do navegador (chave `biblioteca-lucas:v1`); o backup é pelo botão "Seus
dados". **O que já estava salvo por uma versão anterior é mantido:** os livros que você criou ou editou continuam, e o
painel avisa quantos livros entraram com o catálogo novo.

O arquivo do painel mudou de lugar (saiu de `biblioteca-dashboard/` para a raiz). Se, ao abri-lo no lugar novo, o que
você tinha anotado não aparecer — há navegadores que guardam os dados por caminho de arquivo —, ponha o painel novo no
mesmo lugar e com o mesmo nome do antigo, ou exporte um backup no antigo (botão de dados) e importe no novo: a
importação faz a mesma conciliação.

### As capas

O painel mostra a capa do livro nas listas, nas tabelas e na ficha. Hoje **762 dos 2.560** livros têm capa; os outros
aparecem com um desenho com a inicial do título.

- **De onde vêm.** Da [Open Library](https://openlibrary.org), um catálogo aberto de livros. Nenhuma imagem fica no
  repositório: `catalogo/capas.tsv` guarda só o número da capa de cada livro, e o navegador busca a imagem em
  `covers.openlibrary.org` quando ela aparece na tela. É o único pedido que o painel faz à internet, e nada do que
  foi anotado vai junto. Sem internet, ou se a imagem faltar, fica o desenho. Em "Seus dados" há uma chave para
  desligar as capas.
- **Por que só 762.** A busca só aceita uma capa quando o título **e** o autor conferem com os do catálogo, de
  preferência a de uma edição em português — e as edições brasileiras são minoria na Open Library. Livro sem autor
  certo (ou de "Vários autores") e adaptação em quadrinhos com um autor só não são procurados: o resultado não seria
  confiável. Os volumes de uma série nunca ficam com a mesma capa.
- **Procurar de novo** (depois de entrarem livros, por exemplo): no GitHub, aba **Actions** → **Buscar capas** →
  **Run workflow**. O serviço procura só os livros que ainda não foram procurados (marcando "refazer", também os que
  não tinham sido achados), grava `catalogo/capas.tsv` e, no fim, pede 40 das capas guardadas para conferir se as
  imagens abrem — o resultado ("40 de 40 abriram como imagem") aparece na página da execução. Ele não monta o
  painel: as capas novas aparecem depois de `python tools/atualizar.py`, numa rodada.
- **Corrigir uma capa errada:** em `catalogo/capas.tsv`, troque o número da linha (ou ponha o endereço `https://…` de
  uma imagem) e escreva `manual` na coluna `origem` — a busca nunca mexe nessas linhas. Para um livro ficar sem
  capa, apague o número e deixe `manual`. Depois, `python tools/atualizar.py`.

### O site

O painel está publicado em <https://lucasrangel89.github.io/biblioteca/> (GitHub Pages). É o mesmo arquivo, sem nada a
mais: `.github/workflows/publicar-site.yml` copia `Biblioteca_Lucas_Dashboard.html` para a página inicial do site.

- **Quando o site muda.** A cada mudança em `main`, sozinho, em um ou dois minutos. O navegador pode mostrar a versão
  anterior por mais alguns minutos; recarregar a página resolve. Para publicar de novo à mão: no GitHub, aba
  **Actions** → **Publicar o site** → **Run workflow**.
- **O site mostra o painel que está no repositório**, não o catálogo. Mudar o catálogo sem rodar
  `python tools/atualizar.py` não muda o site.
- **Os dados continuam no navegador**, e cada endereço tem os seus: o que foi anotado no arquivo aberto do computador
  não aparece no site, nem o do computador no celular. Para levar de um para o outro: botão "Seus dados" →
  "Exportar backup (.json)" num, "Importar backup…" no outro.
- **O endereço é público.** Quem o tiver vê o catálogo — o mesmo que já está neste repositório. Leituras, notas e
  preços não saem do navegador de quem os anotou. A página pede aos buscadores que não a listem (`noindex`).
- **O site vem inteiro num arquivo só.** Depois de aberto, a única coisa que ele pede à internet são as imagens das
  capas (ver "As capas"); o pedido não diz de que página veio.
- **Para mostrar o painel a alguém com os gráficos cheios:** o endereço terminado em `?exemplo=1` abre com os dados de
  exemplo. Só vale num navegador que ainda não tem nada salvo — no seu, os exemplos nunca se misturam ao que é seu
  sem você pedir.

Módulos: `00-util` (datas, formatos) · `10-data` (livros, posse, conciliação com o catálogo, exemplos, armazenamento) ·
`20-charts` (gráficos SVG) · `30-state` (filtros, período, contexto) · `40-panels` (indicadores e painéis) ·
`50-table` (tabelas e CSV) · `60-drawer` (gaveta do livro, formulários, cotações, backup) · `70-app` (navegação,
inicialização).

## Testes

```bash
python tools/qa/tudo.py importador busca_capas   # os dois que não precisam de navegador
pip install playwright pillow
python -m playwright install chromium   # no Linux, se faltarem bibliotecas: python -m playwright install-deps chromium
python tools/qa/tudo.py                 # tudo, ~16 min; termina com "TUDO CERTO"
python tools/qa/tudo.py posse func6     # só alguns
```

Os testes de navegador abrem o HTML final por `file://` (o `site` também o serve por HTTP, como no GitHub Pages).
Para darem sempre o mesmo resultado, `relogio.py` fixa o relógio em 09/11/2026 — os dados de exemplo são gerados a
partir da data de hoje — e responde aos pedidos de capa ali mesmo, sem ir à internet. A maioria abre o painel com
`?exemplo=1`, para ter números a conferir; `limpo`, `inicio`, `opcionais`, `capas_painel` e `financas` abrem-no como
ele é. Capturas e registros vão para a pasta temporária do sistema (`biblioteca-qa/`) ou para onde a variável
`BIBLIOTECA_QA_TMP` indicar. Só foram rodados no Chromium.

`posse` e `inicio` tiram painéis antigos do histórico do Git. Numa cópia do repositório sem o histórico inteiro, essas
partes são puladas: o teste não falha, mas o `tudo.py` marca a linha dele com "[partes puladas: N]" e avisa no fim, em
vez de dar o teste por completo. `git fetch --unshallow` traz o histórico que falta.

| Script | Cobre |
| --- | --- |
| `importador` | Leitura das listagens, arquivo novo e ausente, casamento com o catálogo, seção 17, execução repetida sem mudanças; quadrinhos (subpasta de série, edição nova de série conhecida, série nova, adaptação com o título de um livro, subpasta com listagem própria); `src/catalog.json` em dia com o catálogo; `renomeados.tsv` |
| `posse` | Físico × digital × nos dois: indicadores, gaveta, formulário, filtros, cartão no celular; quadrinhos (filtro "HQ", gaveta de uma série guardada em subpasta, busca pelo nome da subpasta, os cinco botões do filtro Tipo no celular); **migração do que o painel anterior salvou** no navegador e de um backup exportado por ele; livro anotado no painel e depois corrigido no catálogo ou no inventário (os painéis antigos são tirados do histórico do Git) |
| `busca_capas` | A busca de capas (`tools/capas.py`), sem internet: a consulta feita para cada livro, a capa escolhida (edição em português antes da capa da obra), a segunda tentativa só pelo título, o `capas.tsv` (retomar de onde parou, não mexer no que foi posto à mão, a mesma capa em volumes de uma série), a amostra de `--testar`; `src/capas.json` em dia com `catalogo/capas.tsv` |
| `inicio` | Como o painel abre e os dados de exemplo: primeira abertura só com o catálogo; "Ver com dados de exemplo", "Limpar dados de exemplo" e "Recomeçar"; o endereço com `?exemplo=1`; **a saída dos exemplos de fábrica** para quem usava o painel anterior — sem edições, com um e com três livros editados, no computador e no celular, e com o painel que estava no ar antes da mudança (tirado do histórico do Git) |
| `opcionais` | Só o título é obrigatório: "Novo livro", "Já tenho", "Comprei", "Já li" e "Terminei hoje" sem data, loja ou valor; o que a ficha, os indicadores, Finanças, o CSV e o backup mostram nesses casos; data futura e valor ilegível recusados |
| `capas_painel` | As capas no painel, com uma lista de capas conhecida: tabela, listas e ficha; imagem que falta; o que o navegador pede, e quando; a chave "Mostrar as capas"; a capa não é guardada nem aceita de um backup; endereços inválidos; celular |
| `financas` | A guia Finanças e a navegação: nenhum valor em reais em Visão geral, Biblioteca e Recomendações; indicadores, cartões e tabela de Finanças, com e sem compras; ocultar valores; as seis guias numa linha só no celular (412 a 320 px) e nenhuma guia estourando a largura da tela |
| `func3` … `func8` | Cotações, novo livro, limpar/restaurar exemplos, exportar/importar, períodos (dentro de "Mais filtros"), filtros, Finanças, CSV, dados corrompidos |
| `valores`, `resto` | Valores digitados; excluir livro; período invertido; importação com registros ilegíveis |
| `limpo` | Painel só com o catálogo, sem exemplos — depois de "Limpar dados de exemplo" e como ele abre: indicadores, legendas e estados vazios de todas as guias; a guia Preços sem nenhum livro para cotar (o quadro "Registrar cotação" explica como começar e só vira formulário quando há o que cotar) |
| `foco`, `a11y` | Foco e Tab nas camadas; ids duplicados, nomes acessíveis, rótulos, contraste AA nos dois temas e alvos de toque no celular — em todas as guias, fichas e diálogos, com os dados de exemplo e só com o catálogo (é onde aparecem os estados vazios e as abas zeradas) |
| `varredura` | Clica em tudo, em todas as visões, nos dois temas e no celular, à procura de erros |
| `sandbox` | Página dentro de um iframe isolado (sem `localStorage`): funciona em memória |
| `site` | O painel servido por HTTP, de dentro de uma pasta, como no site: vem inteiro numa única requisição (de fora, só as imagens das capas, pedidas sem dizer de que página vieram), abre sem exemplos — e com eles pelo endereço `?exemplo=1` —, guarda os dados, exporta o backup e importa o que foi feito no arquivo |
| `medir3`, `tabs`, `largo` | Larguras de 2560 a 820 px: colunas das tabelas, quebras e estouros |
| `run1`, `run5` … `run13` | Capturas de tela para conferência visual (só `run7` e `run9` entram no `tudo.py`) |

**Depois de mudar o catálogo, alguns testes precisam de números novos.** `func6`, `limpo`, `posse`, `inicio`,
`opcionais`, `financas` e `capas_painel` comparam o painel com contagens do catálogo atual (2.125 livros no acervo,
433 recomendações na fila, 407 com os dados de exemplo etc.). Quando entrarem livros, rode-os, confira os valores
impressos nas linhas `FALHA` e atualize os literais.

## O que ainda pede conferência

A lista do que só o dono da biblioteca pode responder está em `ROTEIRO.md` (etapas 1 e 2); o detalhe por arquivo, em
`biblioteca-virtual/RESUMO.md`. Em resumo:

- **27 linhas com `verificar`** no inventário — 12 arquivos de livros (eram 36) e 15 linhas das pastas de quadrinhos:
  o nome do arquivo não diz o autor, ou é vago demais para identificar a obra sem abri-la. **15 obras continuam sem
  autor** (10 livros que já estavam, mais 1 livro e 4 quadrinhos).
- **3 livros da estante** com `#verificar`: *Noite do Sul* (Érico Veríssimo), *A Arte de Envelhecer* (na prateleira
  consta Irvin D. Yalom) e *Coraline* (HQ ou romance ilustrado?). E **3 recomendações** marcadas desde antes da
  biblioteca virtual.
- As ligações de um arquivo com um livro do catálogo de título diferente (outra tradução, um volume de série) foram
  conferidas; estão listadas no `RESUMO.md`, em "Edições com título diferente do catálogo". Seis recomendações que
  estavam com um título traduzido ao pé da letra passaram a ter o da edição brasileira (ver `catalogo/renomeados.tsv`).
- **Quadrinhos:** as três listagens de HQs foram importadas: 243 quadrinhos e 20 livros em prosa que estavam nas
  mesmas pastas. Onze deles levam `#verificar` (a lista está no `ROTEIRO.md`, etapa 2).
- **O que ficou de fora dos quadrinhos:** as edições dentro das 104 pastas de séries (a listagem só traz o nome da
  pasta); a subpasta `Mangás` (em `HQs`), que não tem listagem; quatro arquivos compactados com o nome cortado
  (`BTN - Si______ra`, em três partes, e `Lo_____d - Mo_____no`); duas revistas *Heavy Metal*.
- **Subpastas vazias** (informação do dono da biblioteca): `Revistas` (dentro de `pasta livros`), `Didáticos` e
  `Psicologia Aplicada e Popularização` (dentro de `psicologia`). Aparecem nas listagens como pastas; não há o que
  importar delas.
- **Não são livros** (ficam só no inventário): 12 apostilas, 13 periódicos, 3 artigos e 8 outros (entre eles os quatro
  arquivos compactados e a subpasta sem listagem).
