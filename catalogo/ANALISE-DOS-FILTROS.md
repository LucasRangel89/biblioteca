# Análise e meta-análise dos filtros e da categorização

Feita em 11/11/2026, sobre o catálogo como ficou nesta data: 2.614 linhas, 203 marcadores diferentes em uso.

> **O que mudou depois.** As propostas 1, 2 e 3 (parte 4) foram feitas no painel na rodada seguinte: cada botão de
> filtro mostra quantos livros tem, dois marcadores do mesmo grupo passaram a somar, e a psicologia ganhou um grupo de
> filtros só dela. Os números abaixo continuam sendo o retrato de 11/11/2026, de antes dessas mudanças; onde uma
> afirmação deixou de valer, há uma nota marcada **[depois]**.

- A **análise** (parte 1) olha os filtros por dentro: quantos livros cada um alcança, onde eles se repetem, onde
  deixam buracos e como se combinam.
- A **meta-análise** (parte 2) dá um passo atrás e pergunta quanto dá para confiar na categorização: de onde veio cada
  marca, o quanto fontes diferentes concordam, que vícios ela tem e para que cada filtro serve de fato.
- A parte 3 lista o que **já foi corrigido** nesta rodada; a parte 4, o que **proponho** e depende da sua decisão.

Todos os números saem de `python tools/analisar_marcadores.py`, que pode ser rodado de novo a qualquer momento.
É um retrato: quando o catálogo mudar, rode o script para ver os números do dia.

## Em uma página

1. **Os filtros alcançam os livros de forma muito desigual.** "Temas" alcança 71% do catálogo; "Gêneros", 35%; as
   cinco camadas (pergunta, clima, papel, ponte, cenário), entre 4% e 9% — e **nenhum** dos 1.910 livros da biblioteca
   virtual.
2. **A psicologia está apertada.** Um eixo só guarda 440 livros (17% do catálogo; 422 são seus). Nas suas pastas, a
   mesma área ocupa **doze** pastas diferentes. O seu jeito de arquivar é mais fino que o do catálogo.
   **[depois]** O eixo continua um só, mas os filtros ganharam um grupo da psicologia, com dez portas (proposta 3).
3. **O grupo "Temas" mistura três coisas**: a área (filosofia, psicologia), o assunto (morte, memória) e a forma do
   livro (introdução, didático, biografia). São 62 botões num grupo só.
   **[depois]** São 52: os dez da psicologia saíram para o grupo deles. A mistura continua (proposta 4, em aberto).
4. **Marcar dois botões do mesmo grupo quase sempre dá zero.** Os marcadores se combinam com "e"; por isso 73% dos
   pares de gêneros e de temas não têm nenhum livro, e o painel não avisa antes do clique.
   **[depois]** Dentro do grupo os marcadores passaram a somar, e cada botão diz quantos livros tem (propostas 1 e 2).
5. **Havia dois vocabulários.** 26 marcadores só existiam na biblioteca virtual: o filtro "Contos" achava 123 livros
   digitais e nenhum da estante. **Isto foi corrigido nesta rodada** (sobraram 10, que são próprios dos quadrinhos e
   da informática).
6. **Quanto confiar:** o eixo é o dado mais firme (as suas pastas e o catálogo concordam em 76% dos arquivos, e as
   divergências foram revistas uma a uma). A dificuldade e a extensão dos livros digitais são o dado mais frágil:
   uma fonte só, nenhum arquivo aberto, nenhuma conferência sua até agora.

O que eu faria primeiro: mostrar o número de livros ao lado de cada marcador (proposta 1), trocar o "e" por "ou"
dentro de um mesmo grupo (proposta 2) e dar à psicologia um grupo de filtros só dela (proposta 3). As três são
mudanças do painel; nenhuma mexe na classificação. **As três foram feitas na rodada seguinte** — o que ficou está na
parte 4.

---

## Parte 1 — Análise: o que os filtros fazem com os livros

### 1.1 O mapa

O painel tem cerca de 225 botões de filtro: Acervo (4), Tipo (5), Eixo (16), Dificuldade (3), Extensão (3),
"Só prioridades" e 192 marcadores em doze grupos, além do período.

| Filtro | Valores | Alcança (do catálogo) | Na estante | Nas recomendações | Na biblioteca virtual |
| --- | ---: | ---: | ---: | ---: | ---: |
| Eixo, Tipo, Dificuldade, Extensão | 16 · 5 · 3 · 3 | 100% | 100% | 100% | 100% |
| Temas | 62 | 71% | 64% | 71% | 71% |
| Época e origem | 9 | 43% | 55% | 56% | 38% |
| Gêneros | 31 | 35% | 44% | 36% | 33% |
| Trilhas de leitura | 36 | 12% | 46% | 29% | 4% |
| Perguntas centrais | 12 | 9% | 10% | 36% | 0% |
| Afinidades | 6 | 6% | 16% | 20% | 1% |
| Clima da leitura | 10 | 6% | 11% | 25% | 0% |
| Papel na biblioteca | 6 | 5% | 6% | 22% | 0% |
| Pontes entre áreas | 8 | 4% | 7% | 17% | 0% |
| Cenários | 9 | 4% | 10% | 14% | 0% |

"Alcança" quer dizer: o livro tem pelo menos um marcador do grupo. Um filtro que alcança 5% dos livros nunca mostra
os outros 95%, por melhor que eles sejam.

Três leituras desta tabela:

- **Os quatro filtros de cima são os únicos completos.** Todo livro tem eixo, tipo, dificuldade e extensão.
- **"Gêneros" é um filtro de ficção** (ficção científica, horror, romance histórico…) e "Temas" é, na prática, um
  filtro de não ficção. Sobram **97 livros de ficção sem gênero nem tema**: *Madame Bovary*, *Moby Dick*, *Stoner*,
  *Os Miseráveis*. São a "ficção literária"; hoje só se chega a eles pelo eixo.
- **As camadas são um filtro das recomendações.** Vieram do arquivo "versão 3", que só tratava da estante e das
  recomendações. Para o que você tem em arquivo — 2.024 livros que não estão em papel — elas não existem.

### 1.2 Os eixos

| Eixo | Livros | % | Tenho | Não tenho |
| --- | ---: | ---: | ---: | ---: |
| 14 Psicologia e psicanálise | 440 | 16,8% | 422 | 18 |
| 2 Ficção científica e fantasia | 380 | 14,5% | 344 | 36 |
| 13 Ciência e tecnologia | 262 | 10,0% | 234 | 28 |
| 9 Filosofia e ética | 235 | 9,0% | 199 | 36 |
| 11 Política e economia | 208 | 8,0% | 167 | 41 |
| 7 Horror, weird e mistério | 178 | 6,8% | 133 | 45 |
| 12 Sociedade e história | 164 | 6,3% | 120 | 44 |
| 4 Brasil, América Latina e lusofonia | 150 | 5,7% | 113 | 37 |
| 15 Espiritualidade | 139 | 5,3% | 91 | 48 |
| 3 Clássicos universais | 95 | 3,6% | 53 | 42 |
| 6 Romances históricos | 88 | 3,4% | 48 | 40 |
| 10 Mente e neurociência | 88 | 3,4% | 67 | 21 |
| 5 Ficção contemporânea | 84 | 3,2% | 56 | 28 |
| 16 Artes, escrita e parentalidade | 70 | 2,7% | 60 | 10 |
| 1 Pré-história e origens | 18 | 0,7% | 5 | 13 |
| 8 Poesia e cartas | 15 | 0,6% | 12 | 3 |

- **O eixo é o melhor filtro do painel**: cada livro está em um e só um, e nenhum fica de fora.
- **Os tamanhos vão de 15 a 440.** Dois eixos (pré-história e poesia) cabem numa prateleira; um (psicologia) é uma
  biblioteca inteira. Um filtro que devolve 440 livros ajuda pouco.
- **A psicologia pede subdivisão — e você já a fez.** As suas pastas separam psicologia, psicanálise, psicologia
  analítica, cognitivo-comportamental, behaviorismo, humanista e fenomenológica, social e cultural, clínica e
  psicopatologia, avaliação e psicometria, história e introduções, neurociências, autoconhecimento. Os marcadores
  correspondentes já existem no catálogo (psicanálise 152, autoconhecimento 101, psicopatologia 41, psicologia social
  34, analítica 24, TCC 16, humanista 14, behaviorismo 13, psicometria 9), mas estão espalhados entre os 62 "Temas".
- **Os eixos da ficção se dividem por critérios diferentes**: gênero (ficção científica, horror, romance histórico),
  época (clássicos, contemporânea) e origem (Brasil e América Latina). Um romance brasileiro contemporâneo de horror
  caberia em três. A regra seguida — vale o traço mais marcante — funciona, mas explica por que "Brasil" (o
  marcador, 519 livros) é três vezes maior que o eixo 4 (150).

### 1.3 Dificuldade e extensão

| | Leve | Média | Exigente | Curta | Média | Longa |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Estante | 53% | 36% | 11% | 27% | 52% | 22% |
| Recomendações | 36% | 43% | 21% | 26% | 46% | 27% |
| Biblioteca virtual | 50% | 35% | 15% | 39% | 50% | 11% |

- Três níveis bastam, e nenhum está vazio: os dois filtros separam bem.
- **As recomendações são mais difíceis e mais longas do que o que você tem.** A lista de desejos é mais ambiciosa que
  a estante — vale lembrar disso ao escolher o que comprar (a ordem de compra já dá pontos a livro leve e curto).
- "Exigente e curta" quase não existe (53 livros); "leve e longa", também pouco (99). As duas réguas andam juntas,
  mas não são a mesma: em 1.486 livros o nível de uma não é o da outra.
- Na biblioteca virtual as duas são **estimativas** (ver a parte 2).

### 1.4 Marcadores grandes demais, pequenos demais, e de três tipos

- **Sete marcadores são amplos demais para filtrar sozinhos** (mais de 8% do catálogo): Brasil 519, clássico 486,
  filosofia 328, psicologia 328, política 268, HQ 245, introdução 215. Servem para cruzar com outro, não para achar.
- **Doze são pequenos demais** (menos de 10 livros): esporte 4, Leste Europeu 4, utopia 5, faroeste 6, mangá 6,
  teatro 7, identidade 7, neandertal 8, história alternativa 9, Renascimento 9, regional gaúcho 9, psicometria 9.
  Não atrapalham, mas ocupam um botão cada um. (Neandertal e regional gaúcho são pequenos e são seus: ficam.)
- **"Temas" junta três espécies de marcador:**
  - a *área*: filosofia, psicologia, política, ciência, história, religião…
  - o *assunto*: morte, memória, identidade, raça, gênero, guerra, IA…
  - a *forma ou o nível*: introdução (215), didático (166), biografia (76), humor (65), testemunho (29).
    Estes não dizem do que o livro trata, e sim como ele é.

  Quem procura "um livro introdutório de filosofia" tem de saber que a resposta está em dois botões do mesmo grupo.
- **"Clássico" e "contemporâneo" não são um par.** Há 486 clássicos e 53 contemporâneos; os outros 2.075 livros não
  são nem uma coisa nem outra. "Clássico" funciona como selo; "contemporâneo", hoje, quase não funciona.

### 1.5 O específico que não traz o geral

Quando um marcador é um caso particular de outro, espera-se que o filtro geral mostre os dois. Nem sempre mostra:

| Marcador específico | Deveria aparecer em | Aparece em | |
| --- | --- | ---: | --- |
| thriller médico | thriller | 19 de 19 | corrigido nesta rodada (eram 16) |
| Roma | Antiguidade | 20 de 20 | corrigido (eram 2) |
| IA (não ficção) | tecnologia | 42 de 48 | corrigido (eram 13); os 6 restantes são romances |
| regional gaúcho → RS → Brasil | | 100% | já estava certo |
| espiritismo | espiritualidade | 1 de 27 | proposta 5 |
| umbanda | espiritualidade | 0 de 17 | proposta 5 |
| mística | espiritualidade | 4 de 31 | proposta 5 |
| psicanálise | psicologia | 32 de 152 | proposta 3 |
| psiquiatria | medicina | 0 de 27 | proposta 5 |
| existencialismo | filosofia | 8 de 34 | muitos são romances; fica como está |
| policial | mistério | 0 de 22 | proposta 5: são sinônimos |

O caso mais enganoso é **"espiritualidade"**: o marcador (43 livros) tem o mesmo nome do eixo 15 (139 livros) e
alcança menos de um terço dele. Quem clica no marcador pensando no eixo perde Kardec, a umbanda e os místicos.
O mesmo acontece, em grau menor, com "ciência" (o marcador cobre metade do eixo 13) e "história" (pouco mais da
metade do eixo 12). Já "filosofia" e "romance histórico" coincidem quase inteiros com os seus eixos — ali o marcador
só repete o eixo.

### 1.6 Como os filtros se combinam

**[depois] Como é hoje** (propostas 1 e 2, feitas):

- Dentro de **Eixo**, **Dificuldade**, **Extensão** e de **cada grupo de marcadores**, marcar dois botões **soma**:
  "Rússia" e "Nova Inglaterra" mostram os 25 livros dos dois cenários.
- **Entre** grupos, **cruza**: "Rússia" ou "Nova Inglaterra", **e** "claustrofóbico", mostram 3 livros.
- Cada grupo de marcadores tem uma chave **qualquer um / todos**, que aparece quando há dois botões ligados nele. Em
  "todos", o grupo volta a cruzar: é assim que se pede "filosofia **e** introdução" (106 livros). A escolha fica
  guardada.
- Cada botão mostra **quantos livros** a lista da tela teria com ele ligado. O que não mostraria nenhum fica apagado
  — e continua clicável. Os filtros ativos dizem "ou" e "e".

**Como era em 11/11/2026**, quando esta análise foi feita:

- Dentro de **Eixo**, **Dificuldade** e **Extensão**, marcar dois botões **soma**: "leve" e "média" mostram os dois.
- Entre os **marcadores**, marcar dois botões **cruza**: mostra só os livros que têm os dois — mesmo quando os dois
  são do mesmo grupo. "Rússia" e "Nova Inglaterra" juntos não mostram nada, porque nenhum livro se passa nos dois.

| Grupo | Pares possíveis | Pares que não mostram nenhum livro |
| --- | ---: | ---: |
| Cenários | 36 | 97% |
| Trilhas de leitura | 630 | 97% |
| Pontes entre áreas | 28 | 93% |
| Clima da leitura | 45 | 87% |
| Perguntas centrais | 66 | 79% |
| Gêneros | 465 | 73% |
| Temas | 1.891 | 73% |
| Papel na biblioteca | 15 | 60% |
| Época e origem | 36 | 53% |

O cruzamento é o que permite refazer as "interseções" do arquivo versão 3 (horror **e** Nova Inglaterra). Mas, do
jeito que está, o segundo clique num mesmo grupo é quase sempre um beco sem saída — e **os botões não mostram
quantos livros têm**, então só se descobre depois de clicar.

---

## Parte 2 — Meta-análise: quanto confiar nesta categorização

### 2.1 De onde veio cada marca

| Parte do catálogo | Linhas | Quem classificou, e como | Você conferiu? |
| --- | ---: | --- | --- |
| Estante física | 97 | Títulos passados por você; classificação feita por inteligência artificial em 09/11/2026; 44 linhas (da estante e das recomendações) recalibradas na vistoria | Em parte: correções pontuais |
| Recomendações | 607 | Listas montadas em conversa com inteligência artificial; as 60 desta rodada foram escolhidas entre livros com edição brasileira | Não |
| Camadas e as 20 primeiras trilhas | 442 linhas | Vieram prontas do arquivo "versão 3", feito fora daqui | Não se sabe |
| Biblioteca virtual | 1.910 | Título e autor deduzidos do nome do arquivo (e pesquisados quando o nome não bastava); eixo, tipo, dificuldade, extensão e temas estimados na vistoria de 10/11/2026, sem abrir nenhum arquivo | Não |
| As 16 trilhas novas | 140 livros | Montadas nesta rodada a partir do que há no acervo | Não |

Em resumo: **a categorização inteira foi feita por máquina, em poucos dias, e ainda não passou por uma conferência
sua.** Isso não a torna errada; torna-a não verificada. Em 73% das linhas (as 1.910 da biblioteca virtual) a
dificuldade e a extensão são palpites informados.

### 2.2 Três medidas de concordância

Não há gabarito para conferir a classificação. Mas há três lugares em que duas fontes independentes falam do mesmo
livro, e dá para medir o quanto concordam.

**a) As suas pastas × os eixos do catálogo.** Você arquivou 2.423 livros e quadrinhos em 38 pastas; o catálogo os
distribuiu em 16 eixos sem obedecer às pastas. **Em 76% dos casos, o livro está no eixo principal da sua pasta.**

- Nas pastas de assunto, a concordância é alta: psicanálise 100%, terror e horror 100%, religião 95%, ficção de
  guerra e histórica 96%, ficção científica e fantasia 93%, sociedade e política 87%, história 86%, filosofia 83%.
- É baixa nas pastas que não são de assunto: "pasta livros" (23%), "o livro d" (33%), "novasHQSS" (37%),
  "autoconhecimento e desenvolvimento pessoal" (58%), "Contos e crônicas" (59%). São pastas por forma, por coleção
  ou por ordem de chegada; ali o catálogo acrescenta informação, em vez de discordar.
- A pasta "psicologia" (238 arquivos) fica em 76%: 14% dela foi para "Mente e neurociência". É uma fronteira
  discutível — um manual de neuropsicologia é psicologia ou neurociência? —, e a única grande.

**b) A vistoria × a primeira classificação.** Na vistoria de 10/11, 189 das 1.910 linhas digitais mudaram de eixo
(10%), 29 tinham o tipo errado (1,5%) e 44 das 644 linhas da estante e das recomendações foram recalibradas (7%).
Uma segunda passada corrige de um a dez por cento, conforme o dado. É a ordem de grandeza do erro que se deve
esperar do que ainda não foi revisto.

**c) Esta rodada × o vocabulário.** Sem tirar nenhum marcador, entraram 107 marcadores em linhas da estante e das
recomendações e 47 em linhas da biblioteca virtual. Não eram erros: eram **omissões** — o livro era de contos e não
dizia; falava de física e não dizia. A categorização peca mais por faltar do que por errar.

**Leitura das três medidas, do mais firme ao mais frágil:**

| Dado | Confiança | Por quê |
| --- | --- | --- |
| Tipo (ficção, não ficção, HQ) | Alta | Erro medido de 1,5%, já corrigido |
| Eixo | Alta | Duas fontes independentes concordam em três de cada quatro livros; as divergências foram revistas |
| Posse (tenho, não tenho) | Alta | Sai das listagens das suas pastas, não de estimativa |
| Temas e gêneros | Média | Poucos erros, muitas omissões; melhorou nesta rodada |
| Camadas | Média | Critério de outra pessoa (ou máquina), nunca conferido; coerente no que cobre |
| Dificuldade e extensão da estante e das recomendações | Média | Livros conhecidos; 7% recalibrados |
| Dificuldade e extensão da biblioteca virtual | **Baixa** | Uma fonte só, pelo título; nenhum arquivo aberto; nenhuma conferência |

### 2.3 Os vícios conhecidos

1. **O título engana.** Título de cara acadêmica puxa para "exigente"; título simpático, para "leve". Um manual
   claro e um ensaio curto e difícil ficam trocados.
2. **Autor famoso é bem classificado; autor obscuro é palpite.** A margem de erro não é a mesma no catálogo todo:
   é pequena nos 500 livros que todo mundo conhece e grande nas teses, coletâneas e edições de autor.
3. **O meio atrai.** Metade dos livros tem extensão "média", 37% têm dificuldade "média". Parte disso é verdade;
   parte é o refúgio de quem não sabe.
4. **"Clássico" mede fama, não época.** E, sem um par que funcione, não separa o catálogo em dois.
5. **A ficção ganha gênero; a não ficção ganha tema.** Por isso "Gêneros" alcança um terço dos livros, e 97 romances
   não têm nenhum dos dois.
6. **As camadas têm dono.** Refletem as perguntas de quem montou a versão 3 — humano, liberdade, morte, sentido —
   e a lista de recomendações de então. Cobrem 36% das recomendações, 10% da estante e nada do digital.
7. **O catálogo cresceu em camadas, e cada uma trouxe o seu vocabulário.** Era o caso dos 26 marcadores que só
   existiam na biblioteca virtual. A tendência volta a cada entrada de livros, se ninguém olhar.

### 2.4 Para que serve cada filtro

| O que você quer fazer | Filtros que servem | Como estão |
| --- | --- | --- |
| Achar um livro que já tem | Busca, Acervo, Eixo, Tipo | Completos |
| Ver o formato da biblioteca | Eixo, Tipo, gráficos | Completos |
| Escolher a próxima leitura entre o que tem | Dificuldade, Extensão, Clima, Papel, Pergunta, Trilhas | Dificuldade e extensão cobrem tudo, mas são estimativa no digital; **clima, papel e pergunta não cobrem nada do digital**; as trilhas agora cobrem 81 livros digitais |
| Decidir o que comprar | Prioridade, ordem de compra, Trilhas, "sem edição em português" | Bons; nove livros marcados como sem edição já tinham edição brasileira (corrigido) |
| Explorar um assunto | Temas, Gêneros, Afinidades | Alcance médio; melhorou nesta rodada |

**O achado principal da meta-análise está na terceira linha.** Os filtros mais úteis para decidir o que ler hoje à
noite — o clima da leitura, o papel do livro, a pergunta que ele faz — existem para 9% do catálogo, quase todo
feito de livros que você **não** tem. Os 2.024 livros que só existem em arquivo, que são 95% do seu acervo, só podem
ser escolhidos por eixo, tema, dificuldade e extensão. As 16 trilhas novas atacam esse problema por um lado; a
proposta 7 o ataca de frente.

### 2.5 O que a categorização diz de você

Com as ressalvas acima, o catálogo desenha um leitor:

- **Dono de uma biblioteca digital.** Dos 2.124 livros seus, 2.024 só existem em arquivo; a estante são 97 volumes.
- **Mais de não ficção que de ficção** (1.585 contra 766 linhas, fora 245 quadrinhos).
- **Com um centro de gravidade claro:** psicologia, psicanálise e mente somam 528 livros, um em cada cinco. Em
  volta, ficção científica e fantasia (380), ciência (262), filosofia (235) e política (208).
- **Que lê em português e do Brasil:** 519 livros brasileiros, um em cada cinco.
- **Que guarda mais leve do que deseja:** metade do que tem é "leve"; nas recomendações, o "exigente" dobra.
- **Com gostos bem marcados nas pontas:** Lovecraft e o horror de cidade pequena, romance histórico de guerra e de
  medicina, Asimov e Clarke, Yalom, o Rio Grande do Sul, os neandertais.

Foi a partir desse retrato que as 16 trilhas novas e as 60 recomendações desta rodada foram escolhidas.

### 2.6 Os limites desta análise

- Ela **conta marcadores; não lê livros**. Diz que um filtro alcança pouco, não que um livro está mal classificado.
- **Não sabe quais filtros você usa.** O painel não registra cliques — e não deve registrar. Se um filtro que
  critiquei é o que você mais usa, a sua experiência vale mais que a contagem.
- As medidas de concordância são **indícios**, não uma auditoria. A auditoria de verdade é a proposta 8.

---

## Parte 3 — O que já foi corrigido nesta rodada

Só acréscimos: nenhum marcador foi tirado de nenhum livro, e o que você já tinha mexido no painel fica como estava.

| O quê | Quanto | Efeito |
| --- | ---: | --- |
| Marcadores que só existiam na biblioteca virtual, levados à estante e às recomendações | 74 marcadores em 72 linhas | "Contos" passa a achar *Ficções* e *O Aleph*; "Física", *Cosmos* e *Uma Breve História do Tempo*; "Psicologia social", *O Efeito Lúcifer* e *A Mente Moralista*. De 26 marcadores exclusivos, sobraram 10 |
| Afinidades para os livros digitais dos mesmos autores | 26 linhas | "Asimov e Clarke" mostra também *O Fim da Eternidade* e *Encontro com Rama*; "Yalom", os quatro que você tem em arquivo |
| Thriller médico é thriller; Roma é Antiguidade; livro sobre IA é de tecnologia | 54 marcadores | O filtro geral passa a mostrar o caso particular |
| Recomendações marcadas "sem edição em português" que já têm edição brasileira | 9 linhas | Sete ganharam o título brasileiro (*Elementais*, *A Soberania do Bem*, *O Cogumelo no Fim do Mundo*…); as nove sobem na ordem de compra |
| Trilhas com livros da biblioteca virtual | 81 livros | Antes, nenhum livro digital estava em trilha alguma |

---

## Parte 4 — Propostas (a decisão é sua)

Em ordem do que eu faria primeiro. As três primeiras mexem só no painel; as outras, na classificação.

**1. Mostrar o número de livros ao lado de cada marcador, e apagar o botão que daria zero.**
Ganho: acaba o clique no escuro; o painel passa a dizer, sozinho, quais combinações existem. Trabalho: pequeno.
Risco: nenhum para os dados.

> **Feita.** O número aparece em todos os filtros — marcadores, eixo, dificuldade, extensão e "só prioridades" — e é
> sempre o tamanho que a lista da tela teria depois do clique: na guia Biblioteca conta só o acervo; nas
> Recomendações, só o que não está nele; com outros filtros ligados, conta dentro deles. O botão que daria zero fica
> apagado pela cor e pelo contorno tracejado, e continua clicável.

**2. Dentro de um mesmo grupo, somar ("ou"); entre grupos, cruzar ("e").**
"Rússia" e "Nova Inglaterra" mostrariam os dois cenários; "Rússia" e "melancólico" continuariam cruzando. É como as
lojas e as bibliotecas fazem. Ganho: o segundo clique deixa de ser um beco. Custo: perde-se o cruzamento de dois
temas entre si (filosofia **e** ciência) — dá para manter uma chave "todos / qualquer um" no grupo "Temas".
Trabalho: médio.

> **Feita**, com uma diferença para melhor: a chave "qualquer um / todos" existe em **todos** os grupos, não só em
> "Temas". Ela aparece quando há dois marcadores ligados no grupo, e a escolha fica guardada. Nada do que o cruzamento
> permitia se perdeu: horror **e** Nova Inglaterra continua sendo um cruzamento entre grupos (12 livros); filosofia
> **e** ciência, um grupo em "todos" (18). Os filtros ativos mostram "ou" e "e", e o quadro "Temas e camadas" das
> recomendações segue a mesma regra — as barras não somem mais quando uma é clicada.

**3. Um grupo de filtros só para a psicologia.**
"Psicologia: abordagens e áreas", com o que já existe: psicanálise, TCC, behaviorismo, analítica, humanista, social,
psicopatologia, psicometria, neurociência, autoconhecimento — na ordem das suas pastas. Ganho: o eixo de 440 livros
passa a ter dez portas. Trabalho: pequeno no painel; médio se for para conferir os marcadores com as pastas.

> **Feita no painel.** O grupo vem logo depois de "Temas", na ordem das suas pastas: Psicanálise 152 · TCC 16 ·
> Behaviorismo 13 · Analítica (Jung) 24 · Humanista 14 · Social 34 · Psicopatologia 41 · Psicometria 9 ·
> Neurociência 84 · Autoconhecimento 101. Os dez saíram de "Temas" (62 → 52 botões), porque cada marcador mora num
> grupo só: é o grupo que diz se dois marcadores somam ou cruzam. **Nenhum marcador de livro foi mudado.**
>
> Conferi os marcadores com as pastas, só olhando. Em nove das dez pastas, quase todo arquivo já tem o marcador da
> porta: 236 de 251 (psicanálise 138 de 141, neurociências 30 de 36, as outras sete com um ou nenhum de fora). O que
> falta são apostilas, um artigo, quatro manuais de psiquiatria guardados em "Neurociencias" e três de psicologia
> cognitiva guardados com a TCC. A exceção é "autoconhecimento e desenvolvimento pessoal", uma pasta mista: 69 de
> 123 — o resto é escrita, criação de filhos, argumentação e jogos de lógica, e está certo não levar o marcador.
>
> O que as dez portas **não** alcançam: 99 dos 440 livros do eixo. Deles, 97 só têm o marcador geral "psicologia"
> (manuais, introduções, os livros de Yalom). As suas pastas "psicologia" (240 arquivos) e "historia fundamentos e
> introducoes psico" (23) não têm porta própria: quem as acha é o marcador "Psicologia", que ficou em "Temas".

**4. Separar "Temas" em três grupos: Áreas, Assuntos e Forma.**
"Forma" ficaria com introdução, didático, biografia, testemunho, humor, contos, crônicas, teatro, antologia.
Ganho: 62 botões viram três grupos legíveis; "introdução a…" vira um cruzamento natural. Trabalho: pequeno.

**5. Acertar os nomes que enganam.**
Juntar "policial" e "mistério" (são o mesmo, em vocabulários diferentes); fazer "espiritualidade" incluir espiritismo,
umbanda e mística, ou trocar o nome do marcador; pôr psiquiatria dentro de medicina; decidir o destino de
"contemporâneo" (completar ou tirar). Ganho: o filtro faz o que o nome promete. Trabalho: pequeno. Risco: baixo —
aqui haveria troca de marcadores, não só acréscimo.

**6. Um marcador para a ficção literária.**
Para os 97 romances sem gênero nem tema. Ganho: "Gêneros" passa a alcançar toda a ficção. Trabalho: pequeno.

**7. Levar "clima" e "papel" aos livros digitais de ficção.**
São cerca de 400 romances e coletâneas, mais 242 quadrinhos. É a proposta de maior ganho — o filtro mais útil para
escolher a próxima leitura passaria a valer para o que você tem — e a de maior trabalho. Seria, como na vistoria,
uma estimativa: boa nos livros conhecidos, incerta nos outros. Pode ser feita por partes (primeiro ficção científica
e fantasia, depois horror, depois o resto).

**8. A conferência por amostragem, com método.**
Eu sorteio 40 livros da biblioteca virtual — metade que você provavelmente leu ou conhece, espalhados pelos eixos e
pelos três níveis de dificuldade — e você responde, para cada um, três coisas: o eixo está certo? a dificuldade? a
extensão? Com 40 respostas dá para dizer "a dificuldade acerta em tantos por cento" e decidir se vale refazer.
Ganho: troca "não verificado" por um número. Trabalho: dez minutos seus.

O que **não** proponho: mexer nos eixos (são o que há de mais firme, e mudar um eixo move centenas de livros de
lugar no painel) nem tirar os marcadores pequenos que são seus, como "neandertal" e "regional gaúcho".
