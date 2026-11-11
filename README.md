# Biblioteca do Lucas

Um catálogo só para as duas bibliotecas — a **estante física** e a **biblioteca virtual** (os livros digitais) — e um
painel que mostra as duas juntas ou separadas.

- **Catálogo Mestre** (`catalogo/Biblioteca_Lucas_Catalogo_Mestre.md`): a fonte única. 2.614 linhas — o que tenho e o
  que foi recomendado.
- **Painel**: no ar em <https://lucasrangel89.github.io/biblioteca/>. É um único arquivo HTML
  (`Biblioteca_Lucas_Dashboard.html`), que também abre direto no navegador, sem internet e sem servidor.
- **Roteiro** (`ROTEIRO.md`): o que já foi feito, o que vem pela frente e o que depende de você, em linguagem simples.

| | Livros e quadrinhos |
| --- | ---: |
| Só na estante física | 75 |
| Na estante **e** na biblioteca virtual | 25 |
| Só na biblioteca virtual | 2.024 |
| Recomendações (ainda não tenho) | 490 |
| **Total no catálogo** | **2.614** |

Estante física: 97 volumes. No catálogo são 100 linhas em papel, porque três textos de Lovecraft que estavam entre as
recomendações (*O Chamado de Cthulhu*, *Nas Montanhas da Loucura*, *A Sombra sobre Innsmouth*) estão dentro de um
desses volumes: levam `#tenho-fisico`, e a ficha de cada um diz que não é um volume à parte.

Biblioteca virtual: 2.049 obras — 1.805 livros e 244 quadrinhos — em 2.382 arquivos e 104 pastas de séries de
quadrinhos.

## Como um livro é marcado

No catálogo, a posse é um marcador na linha do livro:

| Marcador | Significa |
| --- | --- |
| `#tenho-fisico` | está na estante, ou dentro de um volume que está nela (antes era `#ja-tenho`) |
| `#tenho-digital` | está na biblioteca virtual |
| os dois | tenho em papel e em arquivo |
| nenhum | é uma recomendação |

- **Seção 0** — a estante física.
- **Seções 1 a 16** — as recomendações, por eixo. As que já tenho em arquivo ganharam `#tenho-digital` e, no painel,
  aparecem no acervo.
- **Seção 17** — o resto da biblioteca virtual, livros e quadrinhos, separado nos mesmos 16 eixos. Esta seção é
  **gerada** a partir do inventário: para mudar título, autor, eixo ou marcadores de uma linha, mude o inventário
  (ver "Corrigir um livro digital"). Postos à mão na linha, só `#lido` e `#top` são preservados.

**Quadrinhos** levam `#HQ`. Uma série é **uma linha só**, sejam quantas forem as edições guardadas. A adaptação de um
livro tem linha própria — *1984 (em quadrinhos)* — e não marca o livro original como `#tenho-digital`.

Além da posse, cada linha leva a **classificação** do livro. A legenda completa está no começo do catálogo.

| Marcadores | Dizem |
| --- | --- |
| `#F` `#NF` `#HQ` `#poesia` `#antologia` | o tipo |
| `#d1` `#d2` `#d3` | a dificuldade: leve, média, exigente |
| `#e1` `#e2` `#e3` | a extensão: até ~250 páginas, de ~250 a ~500, acima de 500 (ou série) |
| `#filosofia`, `#horror`, `#BR`, `#classico`… | temas, gêneros, época e origem |
| `#q-…` `#clima-…` `#papel-…` `#ponte-…` `#cenario-…` | as **camadas**: a pergunta central do livro, o clima da leitura, o papel dele na biblioteca, as áreas que ele cruza e o cenário (só nas seções 0 a 16) |
| `#trilha-…` | o livro faz parte de uma **trilha de leitura** (`catalogo/trilhas.md`) |
| `#top` `#lido` | prioridade sua; já lido |
| `#verificar` `#sem-pt` | pendências: dados a conferir; sem edição em português confirmada |

Todo livro tem tipo, dificuldade e extensão. Os da biblioteca virtual foram classificados na **vistoria** de
10/11/2026 (`catalogo/VISTORIA.md`): a dificuldade e a extensão deles são **estimativas** feitas a partir do título,
do autor e do tipo de obra — nenhum arquivo foi aberto.

## Estrutura

| Caminho | O que é |
| --- | --- |
| `Biblioteca_Lucas_Dashboard.html` | O painel pronto (gerado; não edite à mão). É este arquivo que vai para o site |
| `.github/workflows/publicar-site.yml` | Publica o painel como site a cada mudança em `main` (ver "O site") |
| `.github/workflows/buscar-capas.yml` | Procura as capas dos livros na Open Library e na Apple Books e grava `catalogo/capas.tsv`. Só roda quando pedido, pela aba Actions (ver "As capas") |
| `ROTEIRO.md` | As etapas de desenvolvimento e as pendências de cada uma |
| `catalogo/Biblioteca_Lucas_Catalogo_Mestre.md` | O Catálogo Mestre |
| `catalogo/renomeados.tsv` | O nome antigo de cada linha da estante ou das recomendações que teve título ou autor corrigido (ver "Corrigir o título ou o autor…") |
| `catalogo/capas.tsv` | A capa de cada livro: o número da imagem na Open Library, o endereço da imagem na Apple Books, ou vazio quando não foi achada (ver "As capas") |
| `catalogo/trilhas.md` | As 36 trilhas de leitura: nome, marcador, descrição e os livros, em ordem (ver "Trilhas de leitura") |
| `catalogo/ANALISE-DOS-FILTROS.md` | Análise e meta-análise dos filtros e da categorização, de 11/11/2026: o que cada filtro alcança, quanto confiar em cada dado, o que foi corrigido e o que fica proposto. Os números saem de `tools/analisar_marcadores.py` |
| `catalogo/VISTORIA.md` | Relatório da vistoria dos marcadores de 10/11/2026: o que foi conferido, o que mudou e as dúvidas que ficaram. É um retrato daquela data; não é refeito pelas ferramentas |
| `catalogo/antes-da-vistoria.tsv` | A classificação que 289 linhas tinham antes da vistoria. O painel precisa dela para atualizar os livros de quem já tinha anotações (ver "Quando a classificação muda no catálogo"). **Não apague nem refaça** |
| `biblioteca-virtual/listagens/*.txte` | A lista de arquivos de cada pasta da biblioteca virtual (uma listagem por pasta) |
| `biblioteca-virtual/inventario.tsv` | Uma linha por arquivo (e por subpasta de série de quadrinhos), com título, autor, eixo, gênero e marcadores **revisados** — é aqui que se corrige um livro digital |
| `biblioteca-virtual/RESUMO.md` | Relatório da última importação: o que entrou, o que falta conferir e o que ficou de fora (gerado) |
| `biblioteca-virtual/Biblioteca virtual.md` | A listagem original, como foi enviada (só para consulta; os acentos estão corrompidos) |
| `src/` | Fontes do painel: `index.html`, `styles.css`, `js/00-util.js` … `70-app.js`; `catalog.json`, `capas.json`, `trilhas.json` e `antes.json` (gerados) |
| `tools/atualizar.py` | Faz tudo de uma vez: importa a biblioteca virtual, converte o catálogo e monta o painel |
| `tools/importar_digital.py` | Listagens + inventário → Catálogo Mestre (seção 17 e `#tenho-digital`) e `RESUMO.md` |
| `tools/build_catalog.py` | Catálogo Mestre + inventário → `src/catalog.json`; `catalogo/capas.tsv` → `src/capas.json`; `catalogo/trilhas.md` → `src/trilhas.json`; `catalogo/antes-da-vistoria.tsv` → `src/antes.json` (usa `parse_catalog.py`, `eixos.py` e `capas.py`). O que não bate sai como `AVISO:` |
| `tools/build.py` | `src/` → `Biblioteca_Lucas_Dashboard.html`; confere que não sobrou referência externa |
| `tools/capas.py` | Busca das capas na Open Library e, para o que ela não tem, na Apple Books → `catalogo/capas.tsv`. É o único script que precisa de internet; no GitHub, quem o roda é o serviço "Buscar capas" |
| `tools/analisar_marcadores.py` | Mede os filtros e a categorização (alcance de cada grupo, marcadores raros e amplos, pastas × eixos…). Só mostra; não grava nada |
| `tools/qa/` | Testes automatizados |
| `referencias/` | Material guardado só como referência: um painel de inspiração, um protótipo abandonado e `catalogo-v3-enviado-2026-11-10.md`, a "versão 3" do catálogo, de onde vieram as camadas e as trilhas (nada lê esse arquivo) |

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
   poesia), preencha `marcadores` (temas, dificuldade e extensão: `filosofia etica d2 e1`), apague o `novo` e rode de
   novo. Enquanto `marcadores` estiver vazia, a linha do catálogo leva só o marcador padrão da pasta, e a obra aparece
   no `RESUMO.md`, em "Sem dificuldade nem extensão".
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
| `marcadores` | a classificação da obra, separada por espaços, com ou sem `#`: temas, `d1`–`d3`, `e1`–`e3`. Posse, `verificar`, `lido` e `top` não vão aqui (os dois últimos são postos à mão na linha do catálogo). Se a obra tem mais de um arquivo, vale a soma do que as linhas dizem |
| `obs` | `novo`, `ausente`, `verificar` |

O painel acompanha a correção: o livro é reconhecido pelo arquivo, então o que você já tiver anotado nele (leitura,
nota) continua no lugar mesmo que o título mude.

### Mudar a classificação de um livro

- **Estante e recomendações (seções 0 a 16):** mude os marcadores na linha do catálogo.
- **Biblioteca virtual (seção 17):** mude a coluna `marcadores` (ou `eixo`, ou `genero`) no inventário.

Depois, `python tools/atualizar.py`. No painel, quem já tinha editado o livro não perde o que fez (ver "Quando a
classificação muda no catálogo").

### Trilhas de leitura

Uma trilha é uma lista de livros em ordem, com nome e descrição, em `catalogo/trilhas.md`:

```
## 37. Nome da Trilha

`#trilha-nome-da-trilha`

Uma ou duas frases dizendo o que a trilha percorre.

1. Título do Primeiro Livro | Autor
2. Título do Segundo Livro | Autor
```

Cada livro da lista leva também o marcador da trilha na sua linha do catálogo — as duas coisas têm de bater. Para pôr
ou tirar um livro, mude a lista **e** o marcador; `python tools/atualizar.py` avisa (`AVISO: trilhas.md: …`) quando um
livro está na lista sem o marcador, tem o marcador sem estar na lista, ou não é uma linha do catálogo. O título é
escrito como no catálogo.

São 36 trilhas. As 20 primeiras vieram da "versão 3" do catálogo e só têm livros das seções 0 a 16. As de 21 a 36
foram montadas em 11/11/2026 a partir do acervo e têm livros da biblioteca virtual: nesses, o marcador da trilha vai
na coluna `marcadores` do inventário, como o resto da classificação deles — e não na linha da seção 17, que é gerada.

### Entraram recomendações novas

Acrescente a linha no fim da tabela da seção do eixo (1 a 16), com tipo, temas, dificuldade e extensão:
`| Título | Autor | #NF #psicologia #d1 #e2 |`. Use o título da edição brasileira; só leva `#sem-pt` o livro que não
tem edição em português. Depois, `python tools/atualizar.py` e, para a capa, o serviço "Buscar capas" (ver "As capas").
Se o livro já estiver na biblioteca virtual, o importador avisa: a linha ganha `#tenho-digital` em vez de repetir.

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
- **Os marcadores vêm em grupos:** gêneros, temas, época e origem, afinidades, as cinco camadas (perguntas centrais,
  clima da leitura, papel na biblioteca, pontes entre áreas, cenários), trilhas de leitura, pendências e "Suas
  marcas" (hoje, só "possui análise"). Dificuldade e extensão filtram também a biblioteca virtual.
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
  Um arquivo aberto no navegador não tem como ler as páginas das lojas; para acompanhar preços sozinho seria preciso
  um serviço rodando fora do painel (ver `ROTEIRO.md`, etapa 6).

### Suas anotações

Na ficha de cada livro, a parte **Suas anotações** guarda o que é seu sobre ele:

- **Comentários:** um campo de texto de até 5.000 caracteres, salvo sozinho enquanto você escreve.
- **Possui análise:** uma caixa para dizer que você tem resenha, relatório ou fichamento do livro. É marcada sozinha
  quando um arquivo é anexado e pode ser marcada ou desmarcada à mão. Em "Mais filtros" → "Suas marcas" → "possui
  análise", filtra esses livros em qualquer guia.
- **Arquivos:** "Anexar arquivo…" aceita qualquer tipo, até 5 MB cada e até 8 por livro. Os de texto (`.txt`, `.md`,
  `.csv`, `.html`…) abrem ali mesmo; todos podem ser baixados de volta ou removidos.
- **Capa:** "Enviar capa…" põe uma imagem sua no lugar da capa do catálogo (ou do desenho com a inicial). A imagem é
  reduzida para caber em 360 × 540 pixels. "Tirar a capa enviada" volta à anterior.

A aba **Com anotações**, nas tabelas da Visão geral e da Biblioteca, lista os livros com comentário, arquivo ou
"possui análise"; nas tabelas, um ícone ao lado do título marca esses livros. O CSV leva as colunas "Possui análise" e
"Comentários".

**Onde isso fica.** No navegador, como o resto: os comentários junto com os livros; os arquivos e as capas, que pesam
mais, no IndexedDB (banco `biblioteca-lucas`, tabela `anexos`). Nada vai para a internet nem para o repositório. O
**backup** (`.json`) leva os anexos junto — pode ficar grande —, e importá-lo troca os anexos guardados pelos do
backup; um backup antigo, sem anexos, não mexe nos que já estão guardados. Limpar os dados de navegação apaga tudo:
vale exportar um backup de vez em quando.

### Camadas, trilhas e ordem de compra

- **Por que ler** (na ficha): as camadas do livro — a pergunta central, o clima, o papel na biblioteca, as pontes e o
  cenário — e as trilhas de que ele faz parte, com a posição nelas. Cada camada é um filtro: um toque mostra os
  outros livros com a mesma marca. O nome de uma trilha abre a trilha.
- **Trilhas de leitura** (guia Recomendações): as 36 trilhas, com o que você já tem e já leu de cada uma e uma barra
  de andamento. Abrir uma trilha mostra os livros na ordem, o que falta comprar e um atalho para vê-los na tabela.
  "Falta" o livro que não está no acervo nem foi lido.
- **Temas e camadas** (guia Recomendações): os marcadores mais frequentes de cada grupo, à escolha.
- **O que comprar primeiro** (guias Recomendações e Próximas aquisições): as recomendações que você ainda não tem, na
  ordem sugerida, com o motivo ao lado e um botão que põe o livro na lista de compra. A tabela das recomendações tem
  a coluna "Ordem de compra", e a ficha de cada recomendação diz a posição dela.

A ordem de compra é uma **sugestão**, calculada pelo painel com o que o catálogo e as suas anotações dizem — por isso
muda sozinha quando você compra ou lê um livro. Cada recomendação soma pontos:

| Motivo | Pontos |
| --- | ---: |
| prioridade sua (`#top`) | 40 |
| está numa trilha | 8 a 30, conforme o quanto da trilha você já tem ou leu |
| é o único livro que falta para fechar a trilha (ou um dos dois que faltam) | +15 (+8) |
| está em mais de uma trilha | +4 por trilha a mais |
| porta de entrada de uma área (`#papel-porta-de-entrada`) | 12 |
| leitura-relâmpago (`#papel-leitura-relampago`) | 6 |
| leve (`#d1`) ou média (`#d2`) | 6 ou 3 |
| curta (`#e1`) ou média (`#e2`) | 6 ou 3 |
| sem edição em português (`#sem-pt`) | −15 |
| dados a conferir (`#verificar`) | −10 |

No empate, vem antes o livro mais leve e depois o mais curto. **A ordem não olha preços** (o painel não os conhece);
os pesos estão em `ordemDeCompra`, em `src/js/30-state.js`.

### Quando a classificação muda no catálogo

O painel guarda no navegador os livros em que você mexeu ("Editar", "Já li", "Quero comprar"…). Quando chega um
catálogo com outra classificação — como o da vistoria —, cada um desses livros é comparado com a linha nova:

- o que você **não** mudou (eixo, tipo, dificuldade, extensão, cada marcador) passa a seguir o catálogo;
- o que você pôs, tirou ou trocou fica como você deixou;
- leitura, notas, datas, valores, comentários e anexos nunca são tocados.

A última regra vale nos dois sentidos: se o catálogo passa a dizer `#lido` ou `#tenho-fisico` de um livro em que o
usuário já tinha mexido no painel, fica o que está no navegador. Ele acerta pela ficha: "Já tenho", "Já li" (que
existe também para o livro que não está no acervo) ou "Não li".

Para saber o que foi mudado por você, o painel guarda em cada livro editado a classificação que o catálogo dava a ele
naquele momento. Os painéis publicados até 10/11/2026 não guardavam isso; para quem já tinha livros editados antes, a
classificação antiga vem de `catalogo/antes-da-vistoria.tsv` — as 289 linhas em que a vistoria trocou ou tirou alguma
coisa (nas outras ela só acrescentou, e não há o que desfazer). Por isso esse arquivo **não deve ser apagado nem
refeito**: alguém pode abrir o painel novo com dados guardados há muito tempo. Se um livro dele sair do catálogo,
`build_catalog.py` avisa, e a linha desse livro pode ser apagada.

Quando duas linhas do catálogo viram uma só (duas edições da mesma obra, ou a recomendação que era o mesmo livro de um
arquivo), a linha fica com a que você tinha editado. Se tinha editado as duas, a segunda continua no painel como um
livro à parte: nada se perde. Uma recomendação que estava na lista de compra e agora consta como "tenho em digital"
continua na lista de compra, com o aviso de que há o arquivo.

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

Os dados do usuário ficam no `localStorage` do navegador (chave `biblioteca-lucas:v1`) e, os arquivos anexados e as
capas enviadas, no IndexedDB (banco `biblioteca-lucas`); o backup é pelo botão "Seus dados". **O que já estava salvo
por uma versão anterior é mantido:** os livros que você criou ou editou continuam, e o painel avisa quantos livros
entraram ou saíram com o catálogo novo.

O arquivo do painel mudou de lugar (saiu de `biblioteca-dashboard/` para a raiz). Se, ao abri-lo no lugar novo, o que
você tinha anotado não aparecer — há navegadores que guardam os dados por caminho de arquivo —, ponha o painel novo no
mesmo lugar e com o mesmo nome do antigo, ou exporte um backup no antigo (botão de dados) e importe no novo: a
importação faz a mesma conciliação.

### As capas

O painel mostra a capa do livro nas listas, nas tabelas e na ficha. Hoje **1.564 dos 2.614** livros têm capa (60 dos
97 da estante, 494 das 607 linhas de recomendações, 1.009 dos 1.910 da biblioteca virtual); os outros aparecem com um
desenho com a inicial do título. Até 11/11/2026 eram 761, todas da primeira fonte.

- **De onde vêm.** De dois catálogos de livros na internet, nesta ordem:
  1. a [Open Library](https://openlibrary.org), um catálogo aberto (784 capas). Tem poucas edições brasileiras;
  2. a **Apple Books**, a loja de livros digitais da Apple, consultada pela busca pública do iTunes na loja do Brasil
     (780 capas). Só é procurada para o que a Open Library não achou. Traz a capa do livro digital em português que
     está à venda: quase sempre a da edição brasileira, às vezes a da edição de Portugal.

  Nenhuma imagem fica no repositório: `catalogo/capas.tsv` guarda só o número da capa (Open Library) ou o endereço da
  imagem (Apple), e o navegador busca a imagem em `covers.openlibrary.org` ou em `is…-ssl.mzstatic.com` quando ela
  aparece na tela. São os únicos pedidos que o painel faz à internet; nada do que foi anotado vai junto, e o pedido
  não diz de que página veio. Sem internet, ou se a imagem faltar, fica o desenho. Em "Seus dados" há uma chave
  para desligar as capas.
- **Por que não são todas.** A busca só aceita uma capa quando o título **e** o autor conferem com os do catálogo.
  Fica sem capa o livro que não está em nenhum dos dois catálogos com esse título — é o caso de muita edição antiga,
  de teses e de quadrinhos —, o livro sem autor certo (ou de "Vários autores") e a adaptação em quadrinhos com um
  autor só: nesses dois últimos casos nem se procura, porque o resultado não seria confiável. Os volumes de uma
  série nunca ficam com a mesma capa. A capa da Apple é a do livro digital à venda hoje: pode não ser a da edição que
  está na sua estante. Na busca de 11/11/2026, 967 livros não foram achados em nenhuma das duas fontes e 83 não foram
  procurados; entre os 245 quadrinhos, só 58 têm capa.
- **Procurar de novo** (depois de entrarem livros, por exemplo): no GitHub, aba **Actions** → **Buscar capas** →
  **Run workflow**. O serviço procura só o que falta — os livros novos, nas duas fontes, e os que só tinham passado
  pela primeira —, grava `catalogo/capas.tsv` e, no fim, pede 40 capas de cada fonte para conferir se as imagens
  abrem; o resumo aparece na página da execução. Marcando "refazer", tenta de novo, nas duas fontes, os que não foram
  achados. A busca da Apple aceita cerca de 20 consultas por minuto: mil livros levam perto de uma hora; se o tempo
  acabar, basta rodar de novo, que ele continua de onde parou. O serviço não monta o painel: as capas novas aparecem
  depois de `python tools/atualizar.py`, numa rodada.
- **O que a coluna `origem` diz:** `edicao` e `obra`, capa da Open Library (a da edição com o nosso título, ou a da
  obra em outra língua); `apple`, capa da Apple Books; `manual`, posta à mão; `nao-achei`, procurada só na Open
  Library (falta a Apple); `nao-achei-2`, procurada nas duas; `sem-autor`, não procurada.
- **Corrigir uma capa errada:** em `catalogo/capas.tsv`, troque o número da linha (ou ponha o endereço `https://…` de
  uma imagem) e escreva `manual` na coluna `origem` — a busca nunca mexe nessas linhas. Para um livro ficar sem
  capa, apague o número e deixe `manual`. Depois, `python tools/atualizar.py`. Para a busca procurar de novo a capa de
  um livro só, apague a linha dele em `catalogo/capas.tsv`: na execução seguinte ele conta como livro novo.
- **Ou envie a capa pelo painel:** na ficha do livro, "Suas anotações" → "Enviar capa…". Essa imagem fica guardada no
  seu navegador (e no backup), vale só para você e aparece mesmo com as capas desligadas — não é pedida à internet.

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

Módulos: `00-util` (datas, formatos) · `10-data` (livros, posse, marcadores, trilhas, conciliação com o catálogo,
exemplos, armazenamento) · `20-charts` (gráficos SVG) · `30-state` (filtros, período, contexto, andamento das trilhas,
ordem de compra) · `40-panels` (indicadores e painéis) · `50-table` (tabelas e CSV) · `55-anexos` (comentários, capa
enviada, arquivos anexados, backup com anexos) · `60-drawer` (gaveta do livro, formulários, cotações, importação) ·
`70-app` (navegação, inicialização).

## Testes

```bash
python tools/qa/tudo.py importador busca_capas   # os dois que não precisam de navegador
pip install playwright pillow
python -m playwright install chromium   # no Linux, se faltarem bibliotecas: python -m playwright install-deps chromium
python tools/qa/tudo.py                 # tudo, ~20 min; termina com "TUDO CERTO"
python tools/qa/tudo.py posse func6     # só alguns
```

Os testes de navegador abrem o HTML final por `file://` (o `site` também o serve por HTTP, como no GitHub Pages).
Para darem sempre o mesmo resultado, `relogio.py` fixa o relógio em 09/11/2026 — os dados de exemplo são gerados a
partir da data de hoje — e responde aos pedidos de capa ali mesmo, sem ir à internet. A maioria abre o painel com
`?exemplo=1`, para ter números a conferir; `limpo`, `inicio`, `opcionais`, `anotacoes`, `trilhas`, `vistoria`,
`capas_painel` e `financas` abrem-no como ele é. Capturas e registros vão para a pasta temporária do sistema
(`biblioteca-qa/`) ou para onde a variável `BIBLIOTECA_QA_TMP` indicar. Só foram rodados no Chromium.

**A fonte da máquina muda as medidas.** Os testes de largura no celular (`posse`, `financas`) conferem que os nomes da
barra de baixo e os botões do filtro Tipo cabem em telas de 320 a 412 px. Foram calibrados com Open Sans. Numa máquina
em que o navegador de teste só encontra uma letra bem mais larga — DejaVu Sans, a única instalada em muito Linux —,
esses dois testes acusam estouro sem que o painel tenha mudado; a linha `FALHA` mostra a fonte usada
(`relogio.fonte_usada`). Nenhum celular de verdade foi medido: o que os testes garantem é a largura com Open Sans.

`posse`, `inicio` e `vistoria` tiram painéis antigos do histórico do Git. Numa cópia do repositório sem o histórico
inteiro, essas partes são puladas: o teste não falha, mas o `tudo.py` marca a linha dele com "[partes puladas: N]" e
avisa no fim, em vez de dar o teste por completo. `git fetch --unshallow` traz o histórico que falta.

| Script | Cobre |
| --- | --- |
| `importador` | Leitura das listagens, arquivo novo e ausente, casamento com o catálogo, seção 17, execução repetida sem mudanças; a classificação que vem da coluna `marcadores` do inventário (e o inventário antigo, sem ela); a pasta e o nome do arquivo de cada item a verificar, no resumo; quadrinhos (subpasta de série, edição nova de série conhecida, série nova, adaptação com o título de um livro, subpasta com listagem própria); `src/catalog.json` em dia com o catálogo; `renomeados.tsv`; as trilhas (`trilhas.md` × marcadores das linhas, com os avisos; um livro da biblioteca virtual numa trilha); `antes-da-vistoria.tsv`; o HTML pronto em dia com `src/`; `analisar_marcadores.py` roda e conta o catálogo inteiro |
| `posse` | Físico × digital × nos dois: indicadores, gaveta, formulário, filtros, cartão no celular; quadrinhos (filtro "HQ", gaveta de uma série guardada em subpasta, busca pelo nome da subpasta, os cinco botões do filtro Tipo no celular); **migração do que o painel anterior salvou** no navegador e de um backup exportado por ele; livro anotado no painel e depois corrigido no catálogo ou no inventário (os painéis antigos são tirados do histórico do Git) |
| `busca_capas` | A busca de capas (`tools/capas.py`), sem internet. Open Library: a consulta feita para cada livro, a capa escolhida (edição em português antes da capa da obra), a segunda tentativa só pelo título. Apple Books: a consulta, o resultado que serve (título e autor conferem; caixa, trilogia, resumo e audiolivro não), o endereço da imagem, a espera quando a busca recusa por excesso de consultas. As duas em ordem: livro novo passa pelas duas; quem só tinha passado pela primeira vai só à segunda; a Apple fora do ar não atrapalha a Open Library. O `capas.tsv` (retomar de onde parou, não mexer no que foi posto à mão, a mesma capa em volumes de uma série), a amostra de `--testar` nas duas fontes; `src/capas.json` em dia com `catalogo/capas.tsv` |
| `inicio` | Como o painel abre e os dados de exemplo: primeira abertura só com o catálogo; "Ver com dados de exemplo", "Limpar dados de exemplo" e "Recomeçar"; o endereço com `?exemplo=1`; **a saída dos exemplos de fábrica** para quem usava o painel anterior — sem edições, com um e com três livros editados, no computador e no celular, e com o painel que estava no ar antes da mudança (tirado do histórico do Git) |
| `leitura_de_fora` | "Já li" para o livro que não está no acervo (emprestado, de biblioteca, perdido): a ficha da recomendação e a do item da lista de compra oferecem o botão; a leitura conta como "de fora", o livro sai da fila de recomendações e da ordem de compra e a trilha o dá por feito; data e nota opcionais; "Não li" desfaz, também no livro que o catálogo traz como lido; a recomendação lida que vai para a lista de compra e é comprada continua lida; os botões da ficha na largura do celular |
| `opcionais` | Só o título é obrigatório: "Novo livro", "Já tenho", "Comprei", "Já li" e "Terminei hoje" sem data, loja ou valor; o que a ficha, os indicadores, Finanças, o CSV e o backup mostram nesses casos; data futura e valor ilegível recusados |
| `anotacoes` | "Suas anotações" na ficha: comentário (salvo sozinho, limite de tamanho), "possui análise" (à mão e ao anexar; o filtro e a aba "Com anotações"), arquivos (anexar, abrir, baixar, remover; limites de tamanho e de quantidade), capa enviada (reduzida, vale com as capas desligadas, tirar); o que fica no `localStorage` e no IndexedDB; backup com anexos (exportar, importar noutro navegador, backup antigo sem anexos); CSV; celular; página em sandbox |
| `trilhas` | Camadas e trilhas: os grupos de marcadores nos filtros; "Por que ler" na ficha; o painel das trilhas e a ficha de uma trilha (o que tenho, o que li, o que falta); "O que comprar primeiro" e a coluna "Ordem de compra" (a ordem, os motivos, o botão para a lista de compra; a ordem se refaz quando um livro é comprado); "Temas e camadas"; celular |
| `vistoria` | O catálogo revisto no painel (todo livro com tipo, eixo, dificuldade e extensão; os marcadores novos nos filtros) e **o que acontece com quem já tinha livros editados**: com o painel anterior, tirado do Git, edita oito livros e abre o painel novo — o que não foi mexido acompanha a vistoria, o que foi mexido fica; duas edições que viraram uma linha; a recomendação que mudou de título. Depois, o catálogo muda de novo em quatro livros (só no catálogo, só no painel, nos dois, em nada) |
| `capas_painel` | As capas no painel, com uma lista de capas conhecida: tabela, listas e ficha; capa da Open Library, capa da Apple Books e capa posta à mão; imagem que falta (nas duas fontes); o que o navegador pede, e quando; a chave "Mostrar as capas"; a capa do catálogo não é guardada nem aceita de um backup; endereços inválidos; celular |
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
`opcionais`, `leitura_de_fora`, `financas`, `capas_painel`, `trilhas` e `vistoria` comparam o painel com contagens do
catálogo atual (2.124 livros no acervo, 487 recomendações na fila, 461 com os dados de exemplo etc.). Quando entrarem
livros, rode-os, confira os valores impressos nas linhas `FALHA` e atualize os literais. Os dados de exemplo são
sorteados a partir do catálogo: mudar a dificuldade ou a extensão de um livro da estante muda também os valores em
reais que `func6`, `financas`, `inicio` e `limpo` esperam.

## O que ainda pede conferência

A lista do que só o dono da biblioteca pode responder está em `ROTEIRO.md` (etapas 1, 2 e 4), com a pasta e o nome
exato do arquivo a abrir em cada caso. A mesma lista, sempre em dia, sai em `biblioteca-virtual/RESUMO.md`, na parte
"A verificar". Em resumo:

- **27 linhas com `verificar`** no inventário — 12 arquivos de livros (eram 36) e 15 linhas das pastas de quadrinhos:
  o nome do arquivo não diz o autor, ou é vago demais para identificar a obra sem abri-la. **15 obras continuam sem
  autor** (10 livros que já estavam, mais 1 livro e 4 quadrinhos).
- **A classificação da biblioteca virtual é estimada.** Dificuldade, extensão e temas das 1.910 linhas da seção 17
  saíram do título, do autor e do tipo de obra; nenhum arquivo foi aberto. Pede uma conferência por amostragem.
- **Dúvidas da vistoria** (`catalogo/VISTORIA.md`): dois arquivos de Rafael B. Correa que parecem ser o mesmo livro;
  e em qual dos dois livros de Lovecraft da estante (*Contos* ou *Lovecraft: Medo Clássico*) estão *O Chamado de
  Cthulhu*, *Nas Montanhas da Loucura* e *A Sombra sobre Innsmouth* — e se *O Horror de Dunwich* e *Um Sussurro nas
  Trevas*, que continuam como recomendações, também estão nele.
- **A categorização ainda não foi conferida pelo dono.** `catalogo/ANALISE-DOS-FILTROS.md` diz quanto confiar em cada
  dado e propõe uma conferência por amostragem de 40 livros.
- **3 livros da estante** com `#verificar`: *Noite do Sul* (Érico Veríssimo), *A Arte de Envelhecer* (na prateleira
  consta Irvin D. Yalom) e *Coraline* (HQ ou romance ilustrado?). E **3 recomendações** marcadas desde antes da
  biblioteca virtual.
- As ligações de um arquivo com um livro do catálogo de título diferente (outra tradução, um volume de série) foram
  conferidas; estão listadas no `RESUMO.md`, em "Edições com título diferente do catálogo". Seis recomendações que
  estavam com um título traduzido ao pé da letra passaram a ter o da edição brasileira (ver `catalogo/renomeados.tsv`).
- **Quadrinhos:** as três listagens de HQs foram importadas: 243 quadrinhos e 20 livros em prosa que estavam nas
  mesmas pastas. Onze deles levam `#verificar` (a lista está no `ROTEIRO.md`, etapa 2). O 244º quadrinho é
  *Blackbird*, que estava numa pasta de livros.
- **O que ficou de fora dos quadrinhos:** as edições dentro das 104 pastas de séries (a listagem só traz o nome da
  pasta); a subpasta `Mangás` (em `HQs`), que não tem listagem; quatro arquivos compactados com o nome cortado
  (`BTN - Si______ra`, em três partes, e `Lo_____d - Mo_____no`); duas revistas *Heavy Metal*.
- **Subpastas vazias** (informação do dono da biblioteca): `Revistas` (dentro de `pasta livros`), `Didáticos` e
  `Psicologia Aplicada e Popularização` (dentro de `psicologia`). Aparecem nas listagens como pastas; não há o que
  importar delas.
- **Não são livros** (ficam só no inventário): 12 apostilas, 13 periódicos, 3 artigos e 8 outros (entre eles os quatro
  arquivos compactados e a subpasta sem listagem).
