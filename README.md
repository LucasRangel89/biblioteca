# Biblioteca do Lucas

Um catálogo só para as duas bibliotecas — a **estante física** e a **biblioteca virtual** (os livros digitais) — e um
painel que mostra as duas juntas ou separadas.

- **Catálogo Mestre** (`catalogo/Biblioteca_Lucas_Catalogo_Mestre.md`): a fonte única. 2.300 linhas — o que tenho e o
  que foi recomendado.
- **Painel** (`Biblioteca_Lucas_Dashboard.html`): um único arquivo HTML. Abra no navegador; funciona sem internet e sem
  servidor.

| | Livros |
| --- | ---: |
| Só na estante física | 73 |
| Na estante **e** na biblioteca virtual | 24 |
| Só na biblioteca virtual | 1.768 |
| Recomendações (ainda não tenho) | 435 |
| **Total no catálogo** | **2.300** |

Estante física: 97 livros. Biblioteca virtual: 1.792 livros em 2.148 arquivos.

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
- **Seção 17** — o resto da biblioteca virtual, separado nos mesmos 16 eixos. Esta seção é **gerada**: não a edite à
  mão, exceto para acrescentar marcadores a uma linha (eles são preservados).

## Estrutura

| Caminho | O que é |
| --- | --- |
| `Biblioteca_Lucas_Dashboard.html` | O painel pronto (gerado; não edite à mão) |
| `catalogo/Biblioteca_Lucas_Catalogo_Mestre.md` | O Catálogo Mestre |
| `biblioteca-virtual/listagens/*.txte` | A lista de arquivos de cada pasta da biblioteca virtual (uma listagem por pasta) |
| `biblioteca-virtual/inventario.tsv` | Uma linha por arquivo, com título, autor, eixo e gênero **revisados** — é aqui que se corrige um livro digital |
| `biblioteca-virtual/RESUMO.md` | Relatório da última importação: o que entrou e o que falta conferir (gerado) |
| `biblioteca-virtual/Biblioteca virtual.md` | A listagem original, como foi enviada (só para consulta; os acentos estão corrompidos) |
| `src/` | Fontes do painel: `index.html`, `styles.css`, `js/00-util.js` … `70-app.js`, `catalog.json` (gerado) |
| `tools/atualizar.py` | Faz tudo de uma vez: importa a biblioteca virtual, converte o catálogo e monta o painel |
| `tools/importar_digital.py` | Listagens + inventário → Catálogo Mestre (seção 17 e `#tenho-digital`) e `RESUMO.md` |
| `tools/build_catalog.py` | Catálogo Mestre + inventário → `src/catalog.json` (usa `parse_catalog.py` e `eixos.py`) |
| `tools/build.py` | `src/` → `Biblioteca_Lucas_Dashboard.html`; confere que não sobrou referência externa |
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

### Corrigir um livro digital

Corrija a linha no inventário e rode `python tools/atualizar.py`. As colunas:

| Coluna | Conteúdo |
| --- | --- |
| `pasta`, `arquivo`, `formato` | de onde veio (não mexa: é como o arquivo é reconhecido) |
| `tipo` | `livro` ou `hq` entram no catálogo; `apostila`, `periodico`, `artigo` e `outro` ficam só no inventário |
| `titulo`, `autor` | como devem aparecer |
| `catalogo` | quando o livro já existe no catálogo com outro título (outra tradução, um volume de série), o título de lá |
| `eixo`, `genero` | eixo temático (2 a 16) e F, NF ou poesia |
| `obs` | `novo`, `ausente`, `verificar` |

O painel acompanha a correção: o livro é reconhecido pelo arquivo, então o que você já tiver anotado nele (leitura,
nota) continua no lugar mesmo que o título mude.

### Chegou um livro na estante

Acrescente a linha na seção 0 do catálogo com `#tenho-fisico` (ou acrescente `#tenho-fisico` a uma recomendação) e
rode `python tools/atualizar.py`. Também dá para marcar pelo painel ("Já tenho" / "Editar"), mas aí a informação fica
só no navegador.

## O painel

- **Acervo: Tudo / Física / Virtual / Nas duas** — o filtro vale para todas as visões. O livro que está nas duas
  bibliotecas aparece como "Físico e digital".
- A gaveta de cada livro digital mostra **onde ele está**: pasta, formato, número de arquivos e, quando for outra
  edição, o título do arquivo.
- Os arquivos da biblioteca virtual **não têm data nem valor de compra**. Por isso entram nas contagens, mas não nos
  gráficos de evolução e de investimento; no filtro "Virtual", a compra do exemplar físico de um livro que está nas
  duas não é contada.
- **Real (do catálogo):** títulos, autores, marcadores, eixos, a estante e a biblioteca virtual.
- **Exemplo (gerado, semente fixa):** datas e valores de compra da estante, leituras e notas, a lista de próximas
  aquisições e os históricos de preço. Tudo isso é marcado na interface e sai com "Limpar dados de exemplo".
- **Preços:** o painel não consulta lojas. Cada preço é uma cotação registrada à mão (há atalhos de busca por loja).

Os dados do usuário ficam no `localStorage` do navegador (chave `biblioteca-lucas:v1`); o backup é pelo botão de dados.
**O que já estava salvo pela versão anterior é mantido:** ao abrir o painel novo, os livros que você criou ou editou
continuam como estavam, e o painel avisa quantos livros entraram com o catálogo novo.

O arquivo do painel mudou de lugar (saiu de `biblioteca-dashboard/` para a raiz). Se, ao abri-lo no lugar novo, o que
você tinha anotado não aparecer — há navegadores que guardam os dados por caminho de arquivo —, ponha o painel novo no
mesmo lugar e com o mesmo nome do antigo, ou exporte um backup no antigo (botão de dados) e importe no novo: a
importação faz a mesma conciliação.

Módulos: `00-util` (datas, formatos) · `10-data` (livros, posse, conciliação com o catálogo, exemplos, armazenamento) ·
`20-charts` (gráficos SVG) · `30-state` (filtros, período, contexto) · `40-panels` (indicadores e painéis) ·
`50-table` (tabelas e CSV) · `60-drawer` (gaveta do livro, formulários, cotações, backup) · `70-app` (navegação,
inicialização).

## Testes

```bash
python tools/qa/tudo.py importador      # o importador; não precisa de navegador
pip install playwright pillow
python -m playwright install chromium   # no Linux, se faltarem bibliotecas: python -m playwright install-deps chromium
python tools/qa/tudo.py                 # tudo, ~12 min; termina com "TUDO CERTO"
python tools/qa/tudo.py posse func6     # só alguns
```

Os testes de navegador abrem o HTML final por `file://` e fixam o relógio em 09/11/2026 (`relogio.py`), porque os dados
de exemplo são gerados a partir da data de hoje. Capturas e registros vão para a pasta temporária do sistema
(`biblioteca-qa/`) ou para onde a variável `BIBLIOTECA_QA_TMP` indicar. Só foram rodados no Chromium.

| Script | Cobre |
| --- | --- |
| `importador` | Leitura das listagens, arquivo novo e ausente, casamento com o catálogo, seção 17, execução repetida sem mudanças |
| `posse` | Físico × digital × nos dois: indicadores, gaveta, formulário, filtros, cartão no celular; **migração do que o painel anterior salvou** no navegador e de um backup exportado por ele (o painel antigo é tirado do histórico do Git) |
| `func3` … `func8` | Cotações, novo livro, limpar/restaurar exemplos, exportar/importar, períodos, filtros, CSV, dados corrompidos |
| `valores`, `resto` | Valores digitados; excluir livro; período invertido; importação com registros ilegíveis |
| `limpo` | Painel só com o catálogo (sem exemplos): indicadores, legendas e estados vazios |
| `foco`, `a11y` | Foco e Tab nas camadas; ids duplicados, nomes acessíveis, rótulos, contraste AA nos dois temas |
| `varredura` | Clica em tudo, em todas as visões, nos dois temas e no celular, à procura de erros |
| `sandbox` | Página dentro de um iframe isolado (sem `localStorage`): funciona em memória |
| `medir3`, `tabs`, `largo` | Larguras de 2560 a 820 px: colunas das tabelas, quebras e estouros |
| `run1`, `run5` … `run13` | Capturas de tela para conferência visual (só `run7` e `run9` entram no `tudo.py`) |

**Depois de mudar o catálogo, alguns testes precisam de números novos.** `func6`, `limpo` e `posse` comparam o painel
com contagens do catálogo atual (1.865 livros no acervo, 407 recomendações na fila etc.). Quando entrarem livros,
rode os três, confira os valores impressos nas linhas `FALHA` e atualize os literais.

## O que ainda pede conferência

Está tudo listado em `biblioteca-virtual/RESUMO.md`. Em resumo:

- **36 arquivos com `verificar`** no inventário: título ou autor deduzido com pouca segurança, ou casamento com o
  catálogo por outra tradução (por exemplo, o arquivo "A Curva do Sonho" foi ligado a *O Torno do Céu*).
- **25 livros sem autor** identificado.
- **Quadrinhos:** as três listagens de HQs estão guardadas, mas não foram importadas em bloco; só *Coraline* e *Maus*
  têm linha no inventário.
- **Subpastas sem listagem:** `Revistas` (dentro de `pasta livros`), `Didáticos` e `Psicologia Aplicada e
  Popularização` (dentro de `psicologia`) aparecem nas listagens como pastas, mas a lista do que há nelas não veio.
- **Não são livros** (ficam só no inventário): 12 apostilas, 11 periódicos, 3 artigos e 3 outros.
