# Roteiro

O caminho de desenvolvimento da biblioteca, em etapas pequenas. Cada etapa é uma rodada de trabalho: você pede, o
trabalho é feito e testado, você aprova, e só então entra na versão oficial.

Este arquivo é atualizado ao fim de cada rodada. Para saber em que pé as coisas estão, basta ler a tabela abaixo.

**O painel está no ar:** <https://lucasrangel89.github.io/biblioteca/>

## Onde estamos

| Etapa | O que é | Situação |
| --- | --- | --- |
| 0 | Trazer a biblioteca virtual para o catálogo e para o painel | **Feita** (10/11/2026) |
| 1 | Conferir o que foi importado | **Quase pronta** — falta só o que depende de você (lista abaixo) |
| 2 | Decidir o que ficou de fora (quadrinhos, subpastas) | **Feita** (10/11/2026) — ficaram 13 perguntas para você (lista abaixo) |
| 3 | Trocar os dados de exemplo pelos seus | A fazer |
| 4 | Classificar os livros digitais novos | A fazer |
| 5 | Rotina à prova de erro | A fazer |
| 6 | Melhorias do painel | **Em parte** — o painel já abre por um endereço (10/11/2026) |

A ordem pode mudar: as etapas 2 a 6 não dependem umas das outras. Se alguma interessar mais, peça por ela.

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
- **Vale exportar um backup de vez em quando.** Limpar os dados de navegação do navegador apaga as anotações.
- **O endereço é público.** Quem o tiver vê a lista de livros, que já é pública no GitHub. O que você anota não sai
  do seu navegador.
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

*Na estante* (olhe a capa ou a folha de rosto):

| Livro no catálogo | A dúvida |
| --- | --- |
| *Noite do Sul*, de Érico Veríssimo | Não achei livro dele com esse título. A novela dele chama-se *Noite*. Qual é o título na capa? |
| *A Arte de Envelhecer*, de Irvin D. Yalom | O livro conhecido com esse título é de **Schopenhauer**. Quem é o autor na capa? |
| *Coraline*, de Neil Gaiman | É a história em quadrinhos (desenhos de P. Craig Russell) ou o romance ilustrado (Dave McKean)? |

*Na biblioteca virtual* (abra o arquivo e veja a primeira página; a pasta está entre parênteses):

| Arquivo | O que preciso saber |
| --- | --- |
| Linguagem e Cognição (`Filosofia`) | Autor |
| Engenharia Social (`Sociedade e politica`) | Autor e título completo |
| Manipulação (`autoconhecimento e desenvolvimento pessoal`) | Autor e título completo |
| Manual do Xaveco (`autoconhecimento e desenvolvimento pessoal`) | Autor |
| Linguagem: Os Segredos da Sedução… (`autoconhecimento e desenvolvimento pessoal`) | Autor |
| Tesouros Medievais (`historia`) | Autor |
| Psicologia e Sociologia (`psicologia social e cultural`) | Autor |
| El Proceso de Envejecimiento (`psicologia`) | Autor |
| Introdução à Psicologia, 6ª ed. (`historia fundamentos e introducoes psico`) | Autor (há mais de um livro com esse título) |
| Análise e Projeto de Sistemas (`tecnologia e informacao`) | Autor (há mais de um livro com esse título) |
| Ciclo Antarktos (`Terror e horror`) | É a antologia *The Antarktos Cycle* (Poe, Verne, Lovecraft e outros)? Em que língua? |
| Einstein, Freud e Relações Internacionais (`ciencias`) | É um livro ou um artigo de revista (umas 20 páginas)? |

*Entre as recomendações* há três linhas marcadas com `#verificar` desde antes da biblioteca virtual: *A Guerra do
Fogo* (J.-H. Rosny), *O Médico de Córdoba* (Herbert Le Porrier) e *A Tragédia e a Farsa* (Flávio Henrique Calheiros
Casimiro). Os três livros existem com esses títulos e autores; a marca fica até alguém confirmar a edição.

**Como responder.** Escreva na conversa, do jeito que for mais fácil: "Manipulação é de Fulano de Tal", "a Coraline
da estante é a HQ". A lista completa e sempre atualizada fica em `biblioteca-virtual/RESUMO.md`, na parte
"A verificar".

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
  estavam. As três listagens de HQs tinham 236 arquivos e 106 subpastas.
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

**O que continua de fora, e por quê:**

| O quê | Por quê |
| --- | --- |
| As edições dentro das 104 pastas de séries | A listagem só traz o nome da pasta. O catálogo sabe que você tem *Akira*; não sabe quantos volumes |
| Subpastas `Mangás` (dentro de HQs) e `novas` (dentro de NovasHQs) | Não têm listagem. Se quiser que entrem, rode o `gerador de nomes.bat` dentro de cada uma e envie |
| 4 arquivos compactados com o nome cortado: `BTN - Si______ra` (3 partes) e `Lo_____d - Mo_____no` | Não dá para saber o que são sem abrir |
| 2 revistas *Heavy Metal* | São periódicos; ficam só no inventário, como as outras revistas |
| `Revistas`, `Didáticos`, `Psicologia Aplicada e Popularização` | Estão vazias |
| 12 apostilas, 13 periódicos e 3 artigos | Não são livros |

**O que falta — e só você pode responder.** São onze obras que entraram com `#verificar` e mais duas dúvidas. Como
na etapa 1, o que ficar sem resposta continua marcado e não atrapalha nada. As onze estão na pasta `HQs`.

| No catálogo | A dúvida |
| --- | --- |
| *A Vida* (arquivo `A Vida.pdf`) | Quem é o autor? |
| *Os Impostos* (arquivo `Os Impostos.cbr`) | Quem é o autor? |
| *Especial: As Espadas* (arquivo `Especial - As Espadas.cbr`) | É um especial de qual série? Quem é o autor? |
| *Trilogia Lovecraft* (subpasta) | Quais são os três títulos, e de quem? |
| *Lovecraft* (subpasta) | É a HQ *Lovecraft*, de Hans Rodionoff, Keith Giffen e Enrique Breccia? Ou são adaptações de contos? |
| *Caminhos Misteriosos* (subpasta) | É *Mysterious Ways*, de Jason Rubin e Tyler Kirkham? |
| *Contágio* (subpasta) | É a saga do Batman (1996) ou a minissérie da Marvel (2019)? |
| *Cripta* (subpasta) | Qual revista é? |
| *Habitat* (arquivo `Habitat.cbr`) | É a de Simon Roy? |
| *Rashomon* (arquivo `Rashomon.rar`) | É a de Victor Santos? |
| *Ruído* (arquivo `Ruído ( etc.) (Z-Library).epub`) | É o livro de Daniel Kahneman (*Ruído: Uma Falha no Julgamento Humano*) ou um quadrinho? Entrou como livro |

- **A listagem `novasHQSS` é de qual pasta?** Ela não aparece dentro de nenhuma outra. Se for a subpasta `novas`, de
  NovasHQs, então essa subpasta já entrou e não falta nada dela.
- **Os quatro arquivos compactados de nome cortado:** se souber o que são, diga, que eles entram.

**Pronta quando** cada pasta da biblioteca virtual estiver no catálogo ou tiver a decisão de ficar de fora anotada.
Está: o que entrou e o que ficou de fora estão nas listas acima, e em `biblioteca-virtual/RESUMO.md`.

## Etapa 3 — Trocar os dados de exemplo pelos seus

**Por quê.** As leituras, as datas e os valores de compra que o painel mostra hoje são **inventados**, só para os
gráficos não ficarem vazios (o painel avisa disso). De verdade, o catálogo só sabe de dois livros lidos: *O Arqueiro*
e *O Físico*.

**De você:** uma lista simples do que já leu e do que está lendo — pode ser de memória, sem datas. Se lembrar de
preços ou de quando comprou algum livro da estante, melhor, mas não é necessário.

**O que será feito:** os lidos entram no catálogo (`#lido`), para não dependerem do navegador; o painel passa a abrir
com os seus dados, e os de exemplo saem.

**Pronta quando** o painel abrir sem nenhum número inventado.

## Etapa 4 — Classificar os livros digitais novos

**Por quê.** Os 1.675 livros que entraram pela biblioteca virtual não têm dificuldade (`#d`), extensão (`#e`) nem
prioridade, e o eixo de cada um veio da pasta em que o arquivo estava — 473 deles caíram em "Psicologia, psicanálise e
comportamento", que é larga demais para ajudar a escolher a próxima leitura. Os 241 quadrinhos têm só o marcador
`#HQ`: falta dizer o gênero de cada um (super-heróis, ficção científica, terror, biografia…).

**O que será feito:** dificuldade e extensão estimadas livro a livro; eixos revistos; a psicologia dividida em grupos
menores; o gênero dos quadrinhos marcado.

**De você:** conferir por amostragem (uns 30 livros que você conhece) e dizer se a classificação faz sentido.

**Pronta quando** der para filtrar a biblioteca virtual por dificuldade e extensão, como já dá com a estante.

## Etapa 5 — Rotina à prova de erro

**Por quê.** Hoje os testes rodam a pedido; nada impede que uma mudança futura quebre o painel sem ninguém notar. E
atualizar as listagens pede um `gerador de nomes.bat` em cada pasta.

**O que será feito:** os testes passam a rodar sozinhos no GitHub a cada mudança; um único arquivo gera todas as
listagens de uma vez; o material antigo guardado em `referencias/` é revisto.

**De você:** aprovar, e testar o gerador novo uma vez no seu computador.

**Pronta quando** atualizar a biblioteca virtual for: dois cliques, um envio, um pedido.

## Etapa 6 — Melhorias do painel

**Feito** (10/11/2026): **o painel abre por um endereço**, inclusive no celular, em vez de ser um arquivo a baixar
(ver "O site", acima).

Ideias em aberto; você escolhe quais valem a pena.

- **"Tenho em digital, quero o físico":** hoje um livro ou está no acervo ou está na lista de compras, nunca nos dois.
- **Anotações fora do navegador:** hoje leituras e notas ficam guardadas só no navegador em que foram feitas, e o
  backup é manual. Por isso o computador e o celular não mostram as mesmas anotações.

---

## Combinados

- **O catálogo é a fonte única.** O painel é gerado a partir dele e nunca é editado à mão.
- **Nada entra sem teste e sem a sua aprovação.**
- **O que você anota no painel é seu e é preservado.** Quando um título ou autor é corrigido no catálogo, o painel
  reencontra o livro e mantém as anotações (os detalhes estão no `README.md`).
- **Na dúvida, fica marcado.** Título ou autor incerto leva `#verificar` em vez de um palpite.
- **Quadrinhos: uma linha por série**, sejam quantas forem as edições guardadas.
- **O que não é livro nem quadrinho fica só no inventário** (apostilas, revistas, artigos), fora do catálogo e do
  painel.
