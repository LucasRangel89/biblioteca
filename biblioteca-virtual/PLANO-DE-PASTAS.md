# Como as pastas estão, e o que mudaria

Medido em 12/11/2026 em `biblioteca-virtual/inventario.tsv` — 2.405 arquivos e 105 subpastas, em 39 pastas de
primeiro nível. Nada aqui foi movido: é leitura da lista que já existe.

## O retrato em cinco linhas

- **Onze pastas concentram 1.716 arquivos (71 % da biblioteca)**: psicologia 240, Filosofia 224, `Pasta Livros` 170,
  ficção científica e fantasia 167, Sociedade e politica 154, tecnologia e informacao 147, psicanalise 141, HQs 137,
  autoconhecimento 123, ciencias 108, Contos e cronicas 105. **Sete pastas têm dez arquivos ou menos** (51 no total).
- **Só uma pasta usa subpasta**: as 105 subpastas de série dentro de `HQs`. Nos outros 38 assuntos, tudo está plano
  na raiz — e é por isso que a varredura de capas, que tentava reconhecer o livro pelo nome da pasta, se perdia: as
  pastas são categorias de prateleira, não séries.
- **`Pasta Livros` (170) não é um assunto, é o que sobrou**: 78 % dos arquivos dela têm eixo que já tem pasta própria.
- **A "mente" está em doze pastas** (psicologia, psicanalise, autoconhecimento, neurociências, psicologia analítica,
  social e cultural, TCC, clínica e psicopatologia, humanista, avaliação e psicometria, behaviorismo, e "historia
  fundamentos e introducoes psico"): 637 arquivos, e o catálogo chama 482 deles de eixo 14 ("Psicologia e
  psicanálise") — o mesmo rótulo que só 38 arquivos das outras 27 pastas carregam.
- **Tem pasta que é coleção, não assunto**: "Em 90 Minutos" são 61 arquivos, divididos em três pastas — `90min` (30),
  `Filosofia` (20) e `ciencias` (11).

## 1 · Esvaziar a `Pasta Livros` (170 arquivos, nenhuma decisão criativa)

Cada arquivo dela já tem um eixo conferido, e cada eixo já tem pasta. O destino, no volume:

| para | arquivos |
|---|---|
| `ficcao cientifica e fantasia` | 36 |
| `psicologia` | 20 |
| `suspense e thriller` | 19 |
| `Religiao espiritualidade e mitologia` | 15 |
| `literatura contemporanea e estrangeira` | 14 |
| `ficcao de guerra e historica` | 11 |
| `Filosofia` | 11 |
| `Contos e cronicas` | 10 |
| `historia` | 7 |
| `Sociedade e politica` · `tecnologia e informacao` | 4 + 4 |
| `autoconhecimento…` · `ciencias` · `poesia` | 3 + 2 + 1 |
| *(sem eixo — ficam na pasta até serem classificados)* | 13 |

A mesma limpeza vale para `pasta ficcao e literatura` (8 arquivos: 4 de ficção científica, 3 de suspense, 1 de
literatura contemporânea) e, com julgamento, para `nao ficcao` (23, dos quais 14 são eixo 9 — Filosofia) e
`classicos e epicos` (19, 12 deles eixo 3). No fim, ficam **duas pastas a menos** — `Pasta Livros` e
`pasta ficcao e literatura`, que não são assunto nenhum — e o que não tem eixo à espera dele.

## 2 · Quadrinhos: juntar as três pastas e subpastar as séries soltas

`HQs` (137 arquivos + 105 subpastas), `novashqs` (56, sem subpasta) e `novasHQSS` (43, sem subpasta) — 236 arquivos
de quadrinhos em três raízes, sendo que o costume da sua estante de quadrinhos **já é** `HQs/<série>`. Os grupos que
estão soltos na raiz e pedem subpasta própria, do maior para o menor:

- `HQs`: os futuros de liu cixin (14), earthdivers (9), b.p.d.p.: o diabo que você conhece (5), John Carpenter's
  Tales of Science Fiction (4), Kingsway Oeste (4), B.T.N. (3);
- `novashqs`: Coda (8), Silverhawks (7), A Fome e o Crepúsculo (3).

Mover essas nove séries para dentro de `HQs/<nome da série>` são **57 arquivos** que entram no desenho que já vale
para as outras 105 séries. Somando com o passo anterior, a biblioteca passa de três raízes de quadrinho para uma — que
é o que a estante de quadrinhos já é hoje, só que pela metade.

## 3 · Doze pastas de "mente" → duas, com subpastas

`psicologia` (240) e `psicanalise` (141) se sustentam sozinhas, e oito autores aparecem nas duas — Jung, Lacan, Freud
e companhia, lidos dos dois lados. Das dez pastas que sobram, sete são **abordagens com nome comprido**, não assuntos
novos (74 arquivos), e a oitava é um bloco de manuais de entrada (23). Noventa e sete arquivos que cabem como
subpastas de `psicologia`:

```
psicologia/
  analitica (16) · social e cultural (15) · cognitivo-comportamental (14) · clinica e psicopatologia (10)
  humanista e fenomenologica (9) · avaliacao e psicometria (5) · behaviorismo (5) · introducoes (23)
```

A oitava — hoje chamada `historia fundamentos e introducoes psico` — é a que mais atrapalha pelo nome: 22 dos 23
arquivos são eixo 14, é uma pasta de **introduções à psicologia**, não de história. Um nome enganoso pesa mais que a
falta de subpasta.

Das que ficam de fora, duas merecem conversa: `autoconhecimento e desenvolvimento pessoal` (123) é grande, mas 22 dos
seus arquivos são eixo 16 (escrita criativa, parentalidade, contar histórias) e mais 10 estão em
`tecnologia e informacao` — aí sim vale uma pasta nova, `escrita, narrativa e parentalidade`, com os 32. E
`Neurociencias e psicologia biologica`, que é eixo 10 em 30 dos seus 36 arquivos, faz mais sentido como
`psicologia/neurociencias` do que como pasta de primeiro nível.

**Atenção, e é a única coisa que precisa de código:** `tools/gerar_listagens.py` não desce em subpasta de pasta de
livro: ele olha só os filhos diretos de cada pasta e, em pasta de livro, ignora subpasta (o texto do próprio gerador
diz "em pastas de livros, subpastas não entram: são outras pastas da biblioteca"). **Enquanto isso não muda, criar
`psicologia/analitica/` e meter livros lá dentro faz o importador marcar aqueles arquivos como `ausente`** — eles
somem do catálogo. O atalho de hoje, `--incluir "psicologia/analitica=..."`, piora: a subpasta vira listagem própria e,
no inventário, uma pasta-mestre nova — o contrário do que se quer.

Portanto: o item 2 (quadrinhos) pode ser feito hoje, sem tocar em código. O item 3 e as subpastas de assunto pedem
primeiro uma rodada em `tools/gerar_listagens.py` + `tools/importar_digital.py`: a listagem passar a gravar o caminho
com a subpasta (`psicologia/analitica/Livro.epub`), o inventário ganhar a subpasta na coluna `pasta`, e `id_arquivo`
continuar sendo `pasta/arquivo` — nada do que foi conferido à mão é reescrito. É uma rodada pequena e eu faço se você
quiser; sem ela, a arrumação de assunto tem que ficar no primeiro nível.

## 4 · Coleção não é assunto: "Em 90 Minutos" está em três pastas

61 arquivos da mesma série editorial — 30 em `90min`, 20 em `Filosofia`, 11 em `ciencias`. As mini-biografias de
Strathern e companhia são lidas como coleção, não como disciplina, e hoje quem procura `Einstein em 90 Minutos` tem
que lembrar em qual assunto o arquivo caiu. Duas saídas, e a escolha é sua:

- **uma pasta só**: `colecao/90 minutos` com os 61, e as pastas de assunto ficam só com o que é do assunto; ou
- **subpasta dentro de cada assunto**: `Filosofia/90 minutos` (20) e `ciencias/90 minutos` (11), dissolvendo a
  `90min` (30) entre as duas — mantém o assunto como porta de entrada, com a coleção visível um nível abaixo.

Na mesma situação, em menor escala: `o livro d` (9 arquivos) — o nome veio truncado do `dir /b` e são "O Livro de …"
da Coleção Globo: Economia, Filosofia, História, Literatura, Política, Psicologia… É uma coleção, com uma pasta com o
nome inteiro (`colecao/o livro da globo`), não uma letra quebrada na raiz da biblioteca.

## 5 · Duplicatas, antes de qualquer mudança de estrutura

Na **mesma pasta**, 117 títulos têm o mesmo autor e o mesmo formato em dois ou três arquivos — 303 arquivos, 186
cópias sobrando. É quase sempre o mesmo download repetido com nome de gerador diferente:

```
Contos e cronicas · As Armas Secretas - Julio Cortazar.pdf
Contos e cronicas · As Armas Secretas - Julio Cortázar.pdf
Filosofia · CONCEITOS-CHAVE EM FILOSOFIA - LINGUAGEM (JOSÉ MEDINA) (Z-Library).pdf
Filosofia · Linguagem conceitos-chave em filosofia (José Medina) (Z-Library).pdf
```

Um deles é o caso que mais custa no dia a dia: o mesmo arquivo, em pastas diferentes — *Personalidade, Ideologia e
Psicopatologia Crítica* mora em `psicologia` **e** em `psicologia clinica e psicopatologia`. São 98 obras com cópia em
outra pasta; 173 têm as cópias juntas, na mesma pasta.

Vale deduplicar primeiro: é o único item desta lista que **diminui** a biblioteca, e cada cópia a menos é uma linha a
menos para conferir no inventário (e um nome a menos no mapa de capas, que hoje escolhe o primeiro arquivo da série).

## 6 · O que a arrumação não muda no painel

- **Nada do que você anotou se perde por mudar de pasta.** O painel religa os seus dados ao catálogo em três passos
  (os passos de `reconciliar`, em `src/js/10-data.js`): primeiro pela linha do catálogo, depois por título+autor, e só então
  pelo identificador `pasta/arquivo`. Os dois primeiros não dependem de pasta nenhuma. O terceiro muda quando o
  arquivo muda de casa — é por ele que um livro cujo título foi corrigido no inventário continua achando as anotações,
  então a arrumação se faz junto com uma rodada de `gerar_listagens` + `importar_digital`, e não depois de um backup exportado às pressas — e é por isso que se muda uma pasta por vez,
  lendo o `RESUMO.md` no fim.
- **O mapa que reconhece as capas usa só o NOME do arquivo** (`src/digitais.json`, embutido no painel): mover não
  desfaz nada; **renomear, sim** — o arquivo renomeado sai do mapa até a próxima geração.
- Depois de mexer nas pastas, no computador Windows: `Gerar listagens.bat` (ou `tools/gerar_listagens.py`) e, no
  repositório, `python tools/importar_digital.py` + `python tools/atualizar.py`. O `#tenho-digital` e a seção 17 são
  recalculados; nenhuma linha conferida do inventário é reescrita por decisão do robô.

## Por onde começar, se for um pouco de cada vez

1. duplicatas (item 5) — nada muda de lugar, só sobra menos;
2. esvaziar `Pasta Livros` e `pasta ficcao e literatura` (item 1) — 178 arquivos, nenhum precisa de decisão nova;
3. quadrinhos numa prateleira só (item 2) — 57 arquivos, e é o padrão que a estante já usa;
4. decidir a coleção "Em 90 Minutos" (item 4) — 61 arquivos, é gosto;
5. subpastas de assunto (item 3) — começa pelo código (o gerador descer em subpasta de livro), depois a mudança.
