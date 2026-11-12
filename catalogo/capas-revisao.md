# Capas: auditoria e fila de revisão

Gerado por `python tools/auditar_capas.py` (ou `python tools/capas.py --auditar`). Não edite à mão:
depois de mexer em `catalogo/capas.tsv` ou no catálogo, rode o script de novo.

Os números são os do painel: o cruzamento do catálogo com o `capas.tsv` é o mesmo que gera `src/capas.json`.
Nada aqui consulta a internet. Para saber se as imagens ainda abrem: `python tools/auditar_capas.py --rede 40`.

## Resumo

- 2.614 livros no catálogo · 1.564 com capa (60%) · 1.050 sem capa
- 191 livros na fila de revisão · 0 ainda sem linha no capas.tsv · 0 linhas de livros que saíram do catálogo

## De onde vêm as capas

| Origem | Livros | O que significa |
|---|---|---|
| `nao-achei-2` | 967 | Procurada na Open Library e na Apple, sem resultado |
| `apple` | 780 | Apple Books: capa do livro digital no Brasil |
| `edicao` | 752 | Open Library: capa da edição com o nosso título |
| `sem-autor` | 83 | Não procurada: sem autor certo |
| `obra` | 32 | Open Library: capa da obra (pode ser de outra edição) |

## Por parte da biblioteca

| Parte | Livros | Com capa | Sem capa | Com capa (%) |
|---|---|---|---|---|
| Estante física | 97 | 61 | 36 | 63% |
| Recomendações | 607 | 494 | 113 | 81% |
| Biblioteca virtual | 1.910 | 1.009 | 901 | 53% |

## Por eixo temático

Da pior para a melhor cobertura: onde vale a pena procurar primeiro.

| Eixo | Livros | Com capa | Sem capa | Com capa (%) |
|---|---|---|---|---|
| 14. Psicologia, psicanálise e comportamento | 440 | 211 | 229 | 48% |
| 2. Ficção científica, fantasia e distopia | 380 | 194 | 186 | 51% |
| 15. Espiritualidade, espiritismo e mistérios da consciência | 139 | 74 | 65 | 53% |
| 13. Ciência, tecnologia e futuro | 262 | 140 | 122 | 53% |
| 10. Mente, consciência e neurociência | 88 | 50 | 38 | 57% |
| 16. Artes, escrita, cinema e parentalidade | 70 | 40 | 30 | 57% |
| 11. Política, poder, autoritarismo e economia | 208 | 126 | 82 | 61% |
| 12. Sociedade, antropologia, cultura e história | 164 | 107 | 57 | 65% |
| 9. Filosofia, ética e existência (não ficção) | 235 | 155 | 80 | 66% |
| 1. Pré-história, neandertais e origens | 18 | 12 | 6 | 67% |
| 7. Horror, weird fiction e mistério | 178 | 119 | 59 | 67% |
| 6. Romances históricos | 88 | 61 | 27 | 69% |
| 5. Ficção contemporânea e mundial | 84 | 64 | 20 | 76% |
| 3. Clássicos universais e romances de ideias | 95 | 76 | 19 | 80% |
| 8. Poesia e cartas | 15 | 12 | 3 | 80% |
| 4. América Latina, Brasil e lusofonia (ficção) | 150 | 123 | 27 | 82% |

## Por tipo de livro

| Tipo | Livros | Com capa | Sem capa | Com capa (%) |
|---|---|---|---|---|
| Ficção | 741 | 592 | 149 | 80% |
| Não ficção | 1.583 | 889 | 694 | 56% |
| Poesia | 22 | 16 | 6 | 73% |
| Quadrinhos e mangás | 245 | 58 | 187 | 24% |
| Antologias e coletâneas | 23 | 9 | 14 | 39% |

## Fila de revisão (191 livros)

Um livro pode aparecer em mais de um grupo. A ordem dos grupos é a da urgência: primeiro o que está
quebrado, depois o que pode estar errado, por último o que é pendência do catálogo.

### Pode ser capa de outra edição (32)

**O que fazer:** Procurar a edição brasileira; se achar, pôr o endereço e escrever `manual` na origem.

| Livro | Autor | Onde | Capa | Por que está aqui |
|---|---|---|---|---|
| Notícia de um Sequestro (Noticia de un Secuestro) | Gabriel García Márquez | Estante física · eixo 12 | 10096625 | capa da obra na Open Library: pode ser de uma edição em outra língua |
| O Profeta | Khalil Gibran | Estante física · eixo 15 | 13124341 | capa da obra na Open Library: pode ser de uma edição em outra língua |
| Crônicas Marcianas | Ray Bradbury | Recomendações · eixo 2 | 9346537 | capa da obra na Open Library: pode ser de uma edição em outra língua |
| O Lobo da Estepe | Hermann Hesse | Recomendações · eixo 3 | 3221083 | capa da obra na Open Library: pode ser de uma edição em outra língua |
| As Ondas | Virginia Woolf | Recomendações · eixo 3 | 119517 | capa da obra na Open Library: pode ser de uma edição em outra língua |
| Contos Gauchescos | Simões Lopes Neto | Recomendações · eixo 4 | 12030920 | capa da obra na Open Library: pode ser de uma edição em outra língua |
| Ruído Branco | Don DeLillo | Recomendações · eixo 5 | 94015 | capa da obra na Open Library: pode ser de uma edição em outra língua |
| O Assassino Cego | Margaret Atwood | Recomendações · eixo 5 | 11041760 | capa da obra na Open Library: pode ser de uma edição em outra língua |
| Os Três Mosqueteiros | Alexandre Dumas | Recomendações · eixo 6 | 11929973 | capa da obra na Open Library: pode ser de uma edição em outra língua |
| O Grande Deus Pã | Arthur Machen | Recomendações · eixo 7 | 921610 | capa da obra na Open Library: pode ser de uma edição em outra língua |
| O Pescador | John Langan | Recomendações · eixo 7 | 10327331 | capa da obra na Open Library: pode ser de uma edição em outra língua |
| Revival | Stephen King | Recomendações · eixo 7 | 14652892 | capa da obra na Open Library: pode ser de uma edição em outra língua |
| Assassinato no Expresso do Oriente | Agatha Christie | Recomendações · eixo 7 | 11100465 | capa da obra na Open Library: pode ser de uma edição em outra língua |
| The Myth of the Framework | Karl Popper | Recomendações · eixo 9 | 13717354 | capa da obra na Open Library: pode ser de uma edição em outra língua |
| Casa-Grande & Senzala | Gilberto Freyre | Recomendações · eixo 12 | 7150131 | capa da obra na Open Library: pode ser de uma edição em outra língua |
| O Gene Egoísta | Richard Dawkins | Recomendações · eixo 13 | 133936 | capa da obra na Open Library: pode ser de uma edição em outra língua |
| A Cabala e seu Simbolismo | Gershom Scholem | Recomendações · eixo 15 | 581696 | capa da obra na Open Library: pode ser de uma edição em outra língua |
| Story | Robert McKee | Recomendações · eixo 16 | 38437 | capa da obra na Open Library: pode ser de uma edição em outra língua |
| 20th Century Boys | Naoki Urasawa | Biblioteca virtual · eixo 2 | 10521307 | capa da obra na Open Library: pode ser de uma edição em outra língua |
| Akira | Katsuhiro Otomo | Biblioteca virtual · eixo 2 | 882869 | capa da obra na Open Library: pode ser de uma edição em outra língua |
| Contos | Ernest Hemingway | Biblioteca virtual · eixo 3 | 13834065 | capa da obra na Open Library: pode ser de uma edição em outra língua |
| Os Prisioneiros | Rubem Fonseca | Biblioteca virtual · eixo 4 | 9327859 | capa da obra na Open Library: pode ser de uma edição em outra língua |
| Pequenas Criaturas | Rubem Fonseca | Biblioteca virtual · eixo 4 | 1052446 | capa da obra na Open Library: pode ser de uma edição em outra língua |
| Rinha de Galos | María Fernanda Ampuero | Biblioteca virtual · eixo 4 | 10227192 | capa da obra na Open Library: pode ser de uma edição em outra língua |
| Meu Amigo Dahmer | Derf Backderf | Biblioteca virtual · eixo 5 | 14388898 | capa da obra na Open Library: pode ser de uma edição em outra língua |
| 1356 (Busca do Graal, vol. 4) | Bernard Cornwell | Biblioteca virtual · eixo 6 | 10311632 | capa da obra na Open Library: pode ser de uma edição em outra língua |
| Elogio da Sombra | Jorge Luis Borges | Biblioteca virtual · eixo 8 | 13847866 | capa da obra na Open Library: pode ser de uma edição em outra língua |
| Textos Básicos de Filosofia: Dos Pré-Socráticos a Wittgenstein | Danilo Marcondes | Biblioteca virtual · eixo 9 | 12370706 | capa da obra na Open Library: pode ser de uma edição em outra língua |
| Elástico: Como o Pensamento Flexível Pode Mudar Nossas Vidas | Leonard Mlodinow | Biblioteca virtual · eixo 10 | 8799893 | capa da obra na Open Library: pode ser de uma edição em outra língua |
| La Piel de la Cultura | Derrick de Kerckhove | Biblioteca virtual · eixo 11 | 13988340 | capa da obra na Open Library: pode ser de uma edição em outra língua |
| Uma Nova História do Tempo | Stephen Hawking e Leonard Mlodinow | Biblioteca virtual · eixo 13 | 1283677 | capa da obra na Open Library: pode ser de uma edição em outra língua |
| Mentes Inquietas: TDAH: Desatenção, Hiperatividade e Impulsividade | Ana Beatriz Barbosa Silva | Biblioteca virtual · eixo 14 | 12458849 | capa da obra na Open Library: pode ser de uma edição em outra língua |

### Autoria a conferir (149)

**O que fazer:** Corrigir o autor no Catálogo Mestre; sem autor certo a busca não procura.

| Livro | Autor | Onde | Capa | Por que está aqui |
|---|---|---|---|---|
| Guerra e Paz | Liev Tolstói (na prateleira consta Dostoiévski; autor correto: Tolstói) | Estante física · eixo 6 | 12369940 | autor com uma anotação entre parênteses |
| Investigações Cognitivas | Marcos Barbosa de Oliveira e Marta Kohl de Oliveira (orgs.) | Estante física · eixo 10 | (sem capa) | autor com uma anotação entre parênteses |
| Coraline | Neil Gaiman e Dave (P. Craig) Russell | Estante física · eixo 2 | 15272781 | autor com uma anotação entre parênteses |
| A Arte de Envelhecer | Irvin D. Yalom (conforme a prateleira) | Estante física · eixo 14 | (sem capa) | autor com uma anotação entre parênteses |
| Tecnologias e Ferramentas de Gestão (PLT 148) | Décio Henrique Franco e outros (orgs.) | Estante física · eixo 11 | (sem capa) | autor com uma anotação entre parênteses |
| The Weird: A Compendium of Strange and Dark Stories | Ann e Jeff VanderMeer (orgs.) | Recomendações · eixo 7 | 8655714 | autor com uma anotação entre parênteses |
| Children of Lovecraft | Ellen Datlow (org.) | Recomendações · eixo 7 | 15233460 | autor com uma anotação entre parênteses |
| Oxford Handbook of Digital Ethics | Carissa Véliz (org.) | Recomendações · eixo 13 | 14561083 | autor com uma anotação entre parênteses |
| Bhagavad Gita | (tradição hindu) | Recomendações · eixo 15 | (sem capa) | sem autor certo |
| Os Upanixades | (tradição hindu) | Recomendações · eixo 15 | (sem capa) | sem autor certo |
| Dhammapada | (tradição budista) | Recomendações · eixo 15 | (sem capa) | sem autor certo |
| Livro Tibetano dos Mortos (Bardo Thödol) | (tradição tibetana) | Recomendações · eixo 15 | (sem capa) | sem autor certo |
| Batman | Vários autores | Biblioteca virtual · eixo 2 | (sem capa) | sem autor certo |
| Cavalgada dos Quadrinhos Amaldiçoados | Vários autores | Biblioteca virtual · eixo 2 | (sem capa) | sem autor certo |
| Coleção Oficial de Graphic Novels Marvel (Salvat) | Vários autores | Biblioteca virtual · eixo 2 | (sem capa) | sem autor certo |
| Conan, o Bárbaro (em quadrinhos) | Vários autores | Biblioteca virtual · eixo 2 | (sem capa) | sem autor certo |
| Contágio | Vários autores | Biblioteca virtual · eixo 2 | (sem capa) | sem autor certo |
| Contos do Multiverso Sombrio | Vários autores | Biblioteca virtual · eixo 2 | (sem capa) | sem autor certo |
| Crônicas de Espada e Feitiçaria | Gardner Dozois (org.) | Biblioteca virtual · eixo 2 | (sem capa) | autor com uma anotação entre parênteses |
| Elfos | Vários autores | Biblioteca virtual · eixo 2 | (sem capa) | sem autor certo |
| Especial: As Espadas | (autor não informado) | Biblioteca virtual · eixo 2 | (sem capa) | sem autor certo |
| Ficção de Polpa: Aventura! | Samir Machado de Machado (org.) | Biblioteca virtual · eixo 2 | (sem capa) | autor com uma anotação entre parênteses |
| Ficção de Polpa, vol. 1 | Samir Machado de Machado (org.) | Biblioteca virtual · eixo 2 | (sem capa) | autor com uma anotação entre parênteses |
| Gavião Arqueiro | Vários autores | Biblioteca virtual · eixo 2 | (sem capa) | sem autor certo |
| Grandes Clássicos DC | Vários autores | Biblioteca virtual · eixo 2 | (sem capa) | sem autor certo |
| Guerreiro Eterno | Vários autores | Biblioteca virtual · eixo 2 | (sem capa) | sem autor certo |
| Heróis Renascem | Vários autores | Biblioteca virtual · eixo 2 | (sem capa) | sem autor certo |
| John Carpenter's Tales of Science Fiction | Vários autores | Biblioteca virtual · eixo 2 | (sem capa) | sem autor certo |
| Klarion | Vários autores | Biblioteca virtual · eixo 2 | (sem capa) | sem autor certo |
| Morbius: O Vampiro Vivo | Vários autores | Biblioteca virtual · eixo 2 | (sem capa) | sem autor certo |
| Mulheres Perigosas | George R.R. Martin e Gardner Dozois (orgs.) | Biblioteca virtual · eixo 2 | (sem capa) | autor com uma anotação entre parênteses |
| O Príncipe de Westeros e Outras Histórias | George R.R. Martin e Gardner Dozois (orgs.) | Biblioteca virtual · eixo 2 | (sem capa) | autor com uma anotação entre parênteses |
| O Sentinela | Vários autores | Biblioteca virtual · eixo 2 | (sem capa) | sem autor certo |
| Os Fabulosos X-Men | Vários autores | Biblioteca virtual · eixo 2 | (sem capa) | sem autor certo |
| Patrulha do Destino | Vários autores | Biblioteca virtual · eixo 2 | (sem capa) | sem autor certo |
| Quarteto Fantástico | Vários autores | Biblioteca virtual · eixo 2 | (sem capa) | sem autor certo |
| Senhor das Estrelas | Vários autores | Biblioteca virtual · eixo 2 | (sem capa) | sem autor certo |
| Seres Mágicos e Histórias Sombrias | Neil Gaiman (org.) | Biblioteca virtual · eixo 2 | (sem capa) | autor com uma anotação entre parênteses |
| Superman vs. Apocalypse | Vários autores | Biblioteca virtual · eixo 2 | (sem capa) | sem autor certo |
| Thanos: Em Busca de Poder / Legado | Vários autores | Biblioteca virtual · eixo 2 | (sem capa) | sem autor certo |
| Thanos II | Vários autores | Biblioteca virtual · eixo 2 | (sem capa) | sem autor certo |
| Thor | Vários autores | Biblioteca virtual · eixo 2 | (sem capa) | sem autor certo |
| Torneio dos Campeões | Vários autores | Biblioteca virtual · eixo 2 | (sem capa) | sem autor certo |
| Vingadores (2017) | Vários autores | Biblioteca virtual · eixo 2 | (sem capa) | sem autor certo |
| Vingadores vs. X-Men | Vários autores | Biblioteca virtual · eixo 2 | (sem capa) | sem autor certo |
| Wild Cards: O Começo de Tudo | George R.R. Martin (org.) | Biblioteca virtual · eixo 2 | 15126267 | autor com uma anotação entre parênteses |
| WildC.A.T.s/X-Men | Vários autores | Biblioteca virtual · eixo 2 | (sem capa) | sem autor certo |
| X-Men: Massacre | Vários autores | Biblioteca virtual · eixo 2 | (sem capa) | sem autor certo |
| Nova Antologia do Conto Russo | Bruno Barretto Gomide (org.) | Biblioteca virtual · eixo 3 | (sem capa) | autor com uma anotação entre parênteses |
| As Cem Melhores Crônicas Brasileiras | Joaquim Ferreira dos Santos (org.) | Biblioteca virtual · eixo 4 | 14309478 | autor com uma anotação entre parênteses |
| Essa História Está Diferente | Ronaldo Bressane (org.) | Biblioteca virtual · eixo 4 | https://is1-ssl.mzstatic.com/image/thumb/Publication69/v4/3c/8e/5e/3c8e5ec3-0468-a4ac-502e-5d7c39bbde75/1013930258.jpg/200x300bb.jpg | autor com uma anotação entre parênteses |
| Os Cem Melhores Contos Brasileiros do Século | Italo Moriconi (org.) | Biblioteca virtual · eixo 4 | 13131571 | autor com uma anotação entre parênteses |
| A Vida | (autor não informado) | Biblioteca virtual · eixo 5 | (sem capa) | sem autor certo |
| Os Impostos | (autor não informado) | Biblioteca virtual · eixo 5 | (sem capa) | sem autor certo |
| Ciclo Antarktos (The Antarktos Cycle) | Robert M. Price (org.) | Biblioteca virtual · eixo 7 | (sem capa) | autor com uma anotação entre parênteses |
| Contos de Horror (Vertigo) | Vários autores | Biblioteca virtual · eixo 7 | (sem capa) | sem autor certo |
| Contos Fantásticos 01 | Vários autores | Biblioteca virtual · eixo 7 | (sem capa) | sem autor certo |
| Contos Fantásticos 02 | Vários autores | Biblioteca virtual · eixo 7 | (sem capa) | sem autor certo |
| Contos Fantásticos 03 | Vários autores | Biblioteca virtual · eixo 7 | (sem capa) | sem autor certo |
| Cripta | Vários autores | Biblioteca virtual · eixo 7 | (sem capa) | sem autor certo |
| Evil Dead | Vários autores | Biblioteca virtual · eixo 7 | (sem capa) | sem autor certo |
| Hellblazer | Vários autores | Biblioteca virtual · eixo 7 | (sem capa) | sem autor certo |
| Hellraiser | Vários autores | Biblioteca virtual · eixo 7 | (sem capa) | sem autor certo |
| Monstro do Pântano | Vários autores | Biblioteca virtual · eixo 7 | (sem capa) | sem autor certo |
| Trilogia Lovecraft | (autor não informado) | Biblioteca virtual · eixo 7 | (sem capa) | sem autor certo |
| Vertigo: Contos Inquietantes | Vários autores | Biblioteca virtual · eixo 7 | (sem capa) | sem autor certo |
| Vertigo (Opera Graphica) | Vários autores | Biblioteca virtual · eixo 7 | (sem capa) | sem autor certo |
| Curso Livre Marx-Engels: A Criação Destruidora | José Paulo Netto (org.) | Biblioteca virtual · eixo 9 | https://is1-ssl.mzstatic.com/image/thumb/Publication118/v4/3e/67/f5/3e67f5d9-b184-4d95-9680-ab03b90c7a4e/1023190604.jpg/200x300bb.jpg | autor com uma anotação entre parênteses |
| Ensaios sobre Mortos-Vivos: The Walking Dead e Outras Metáforas | Rodrigo Gonsalves e Diego Penha (orgs.) | Biblioteca virtual · eixo 9 | https://is1-ssl.mzstatic.com/image/thumb/Publication123/v4/2e/22/eb/2e22eb1b-7153-4e4d-6d9b-b2a105cf6d5d/1031222076.jpg/200x300bb.jpg | autor com uma anotação entre parênteses |
| Filosofia Antiga (Série Investigação Filosófica) | Vários autores | Biblioteca virtual · eixo 9 | (sem capa) | sem autor certo |
| Linguagem e Cognição | (autor não informado) | Biblioteca virtual · eixo 9 | (sem capa) | sem autor certo |
| Livro da Alma | Avicena (Ibn Sina) | Biblioteca virtual · eixo 9 | (sem capa) | autor com uma anotação entre parênteses |
| O Livro da Filosofia | Vários autores | Biblioteca virtual · eixo 9 | (sem capa) | sem autor certo |
| Textos Selecionados de Filosofia Latino-Americana I | Vários autores | Biblioteca virtual · eixo 9 | (sem capa) | sem autor certo |
| Neuropsicologia: Aplicações Clínicas | Leandro F. Malloy-Diniz e outros (orgs.) | Biblioteca virtual · eixo 10 | (sem capa) | autor com uma anotação entre parênteses |
| Neuropsicologia Hoje | Flávia Heloísa dos Santos e outros (orgs.) | Biblioteca virtual · eixo 10 | https://is1-ssl.mzstatic.com/image/thumb/Publication111/v4/0e/0b/ac/0e0bac98-2133-9eb5-948a-4d8ced4ef95d/9788582712214.jpg/200x300bb.jpg | autor com uma anotação entre parênteses |
| Neuropsicologia: Teoria e Prática | Daniel Fuentes e outros (orgs.) | Biblioteca virtual · eixo 10 | (sem capa) | autor com uma anotação entre parênteses |
| A Invisibilidade da Desigualdade Brasileira | Jessé Souza (org.) | Biblioteca virtual · eixo 11 | (sem capa) | autor com uma anotação entre parênteses |
| As Armas da Crítica | Emir Sader e Ivana Jinkings (orgs.) | Biblioteca virtual · eixo 11 | (sem capa) | autor com uma anotação entre parênteses |
| Democracia em Risco? 22 Ensaios sobre o Brasil Hoje | Vários autores | Biblioteca virtual · eixo 11 | (sem capa) | sem autor certo |
| Dicionário da República | Lilia Schwarcz e Heloisa Starling (orgs.) | Biblioteca virtual · eixo 11 | https://is1-ssl.mzstatic.com/image/thumb/Publication123/v4/30/d9/6a/30d96a0b-57fd-953f-f469-afc56d1a44bb/1029791702.jpg/200x300bb.jpg | autor com uma anotação entre parênteses |
| Engenharia Social | (autor não informado) | Biblioteca virtual · eixo 11 | (sem capa) | sem autor certo |
| Gestão de Mudanças Organizacionais na Prática | Lorena Peixoto de Sousa (org.) | Biblioteca virtual · eixo 11 | (sem capa) | autor com uma anotação entre parênteses |
| História das Relações Internacionais Contemporâneas | José Flávio Sombra Saraiva (org.) | Biblioteca virtual · eixo 11 | (sem capa) | autor com uma anotação entre parênteses |
| O Livro da Economia | Vários autores | Biblioteca virtual · eixo 11 | (sem capa) | sem autor certo |
| O Livro da Política | Vários autores | Biblioteca virtual · eixo 11 | (sem capa) | sem autor certo |
| O Livro dos Negócios | Vários autores | Biblioteca virtual · eixo 11 | (sem capa) | sem autor certo |
| Os Clássicos da Política | Francisco C. Weffort (org.) | Biblioteca virtual · eixo 11 | (sem capa) | autor com uma anotação entre parênteses |
| Políticas e Sistema de Saúde no Brasil | Lígia Giovanella e outros (orgs.) | Biblioteca virtual · eixo 11 | (sem capa) | autor com uma anotação entre parênteses |
| Relações Internacionais: Olhares Cruzados | Corival Alves do Carmo e outros (orgs.) | Biblioteca virtual · eixo 11 | https://is1-ssl.mzstatic.com/image/thumb/Publication1/v4/c6/9c/f4/c69cf402-1504-1024-9618-8a9c315fc785/1093-Relacoes_internacionais_olhares_cruzados.jpg/200x300bb.jpg | autor com uma anotação entre parênteses |
| Relações Internacionais: Perspectivas Francesas | Carlos R.S. Milani (org.) | Biblioteca virtual · eixo 11 | (sem capa) | autor com uma anotação entre parênteses |
| 1964: Visões Críticas do Golpe | Caio Navarro de Toledo (org.) | Biblioteca virtual · eixo 12 | 4919342 | autor com uma anotação entre parênteses |
| Antropologia e Nutrição: Um Diálogo Possível | Ana Maria Canesqui e Rosa Wanda Diez Garcia (orgs.) | Biblioteca virtual · eixo 12 | (sem capa) | autor com uma anotação entre parênteses |
| Evolucionismo Cultural | Celso Castro (org.) | Biblioteca virtual · eixo 12 | https://is1-ssl.mzstatic.com/image/thumb/Publication114/v4/5f/42/e3/5f42e386-733c-07d6-b87b-073195319f75/1013363310.jpg/200x300bb.jpg | autor com uma anotação entre parênteses |
| História da Vida Privada | Philippe Ariès e Georges Duby (orgs.) | Biblioteca virtual · eixo 12 | (sem capa) | autor com uma anotação entre parênteses |
| Introdução à Linguística, vol. 1: Domínios e Fronteiras | Fernanda Mussalim e Anna Christina Bentes (orgs.) | Biblioteca virtual · eixo 12 | (sem capa) | autor com uma anotação entre parênteses |
| Introdução à Linguística, vol. 2: Domínios e Fronteiras | Fernanda Mussalim e Anna Christina Bentes (orgs.) | Biblioteca virtual · eixo 12 | (sem capa) | autor com uma anotação entre parênteses |
| Introdução à Linguística, vol. 3: Fundamentos Epistemológicos | Fernanda Mussalim e Anna Christina Bentes (orgs.) | Biblioteca virtual · eixo 12 | (sem capa) | autor com uma anotação entre parênteses |
| Linguagem, Discurso e Sociedade: Caminhos que se Entrecruzam | Vários autores | Biblioteca virtual · eixo 12 | (sem capa) | sem autor certo |
| O Livro da História | Vários autores | Biblioteca virtual · eixo 12 | (sem capa) | sem autor certo |
| O Livro da Sociologia | Vários autores | Biblioteca virtual · eixo 12 | (sem capa) | sem autor certo |
| Sociolinguística Interacional: Antropologia, Linguística e Sociologia em Análise do Discurso | Branca Telles Ribeiro e Pedro M. Garcez (orgs.) | Biblioteca virtual · eixo 12 | (sem capa) | autor com uma anotação entre parênteses |
| Tesouros Medievais | (autor não informado) | Biblioteca virtual · eixo 12 | (sem capa) | sem autor certo |
| Textos Básicos de Antropologia: Cem Anos de Tradição | Celso Castro (org.) | Biblioteca virtual · eixo 12 | https://is1-ssl.mzstatic.com/image/thumb/Publication114/v4/f2/ce/34/f2ce3485-27c0-84ea-7779-54211e755eb8/1016010140.jpg/200x300bb.jpg | autor com uma anotação entre parênteses |
| Textos Básicos de Sociologia: De Karl Marx a Zygmunt Bauman | Celso Castro (org.) | Biblioteca virtual · eixo 12 | https://is1-ssl.mzstatic.com/image/thumb/Publication114/v4/b2/8a/09/b28a09e3-c6fc-4753-ba97-7fc2b1e4ca5e/1013367428.jpg/200x300bb.jpg | autor com uma anotação entre parênteses |
| Análise e Projeto de Sistemas | (autor não informado) | Biblioteca virtual · eixo 13 | (sem capa) | sem autor certo |
| Ciência da Computação e Tecnologias Digitais | Ernane Rosa Martins (org.) | Biblioteca virtual · eixo 13 | (sem capa) | autor com uma anotação entre parênteses |
| Computação, Cognição, Semiose | João Queiroz, Ângelo Loula e Ricardo Gudwin (orgs.) | Biblioteca virtual · eixo 13 | (sem capa) | autor com uma anotação entre parênteses |
| 101 Técnicas da Terapia Cognitivo-Comportamental | Jaquelini Conceição e Gabriela Bueno (orgs.) | Biblioteca virtual · eixo 14 | (sem capa) | autor com uma anotação entre parênteses |
| Análise Comportamental Clínica: Aspectos Teóricos e Estudos de Caso | Ana Karina C.R. de-Farias (org.) | Biblioteca virtual · eixo 14 | (sem capa) | autor com uma anotação entre parênteses |
| As Várias Faces da Psicologia Fenomenológico-Existencial | Valdemar Augusto Angerami-Camon (org.) | Biblioteca virtual · eixo 14 | (sem capa) | autor com uma anotação entre parênteses |
| Avaliação Psicológica da Inteligência e da Personalidade | Claudio Simon Hutz, Denise Ruschel Bandeira e Clarissa Marceli Trentini (orgs.) | Biblioteca virtual · eixo 14 | https://is1-ssl.mzstatic.com/image/thumb/Publication115/v4/62/a5/f6/62a5f6d0-a0f4-e9da-877d-37852309e26d/HUTZ-Avaliacao_Psi_Intel_Personalidade_a.jpg/200x300bb.jpg | autor com uma anotação entre parênteses |
| Avaliação Psicológica: Guia para Estudantes e Profissionais de Psicologia | Rodolfo A.M. Ambiel e outros (orgs.) | Biblioteca virtual · eixo 14 | (sem capa) | autor com uma anotação entre parênteses |
| Descolonizando a Psicologia: Contribuições para uma Prática Popular | Wesley Henrique Alves da Rocha (org.) | Biblioteca virtual · eixo 14 | (sem capa) | autor com uma anotação entre parênteses |
| Dicionário Enciclopédico de Psicanálise: O Legado de Freud e Lacan | Pierre Kaufmann (org.) | Biblioteca virtual · eixo 14 | (sem capa) | autor com uma anotação entre parênteses |
| El Proceso de Envejecimiento | (autor não informado) | Biblioteca virtual · eixo 14 | (sem capa) | sem autor certo |
| Emergências Psiquiátricas | João Quevedo e André F. Carvalho (orgs.) | Biblioteca virtual · eixo 14 | https://is1-ssl.mzstatic.com/image/thumb/Publication113/v4/92/39/83/9239834e-8fe7-8f77-2eb7-8a1f2a2a04da/9788582715970.jpg/200x300bb.jpg | autor com uma anotação entre parênteses |
| Frases Up: 250 Frases para Motivar e Iluminar o seu Dia | Vários autores | Biblioteca virtual · eixo 14 | (sem capa) | sem autor certo |
| Habilidades Sociais, Desenvolvimento e Aprendizagem | Almir Del Prette e Zilda A.P. Del Prette (orgs.) | Biblioteca virtual · eixo 14 | (sem capa) | autor com uma anotação entre parênteses |
| História da Psicologia: Rumos e Percursos | Ana Maria Jacó-Vilela, Arthur Arruda Leal Ferreira e Francisco Teixeira Portugal (orgs.) | Biblioteca virtual · eixo 14 | https://is1-ssl.mzstatic.com/image/thumb/Publication62/v4/03/90/d4/0390d4e7-2884-df82-6b76-9e792fa1cdeb/1024091637.jpg/200x300bb.jpg | autor com uma anotação entre parênteses |
| Introdução à Psicologia (6ª ed.) | (autor não informado) | Biblioteca virtual · eixo 14 | (sem capa) | sem autor certo |
| Introdução à Psicologia das Diferenças Individuais | Carmen Flores-Mendoza e Roberto Colom (orgs.) | Biblioteca virtual · eixo 14 | (sem capa) | autor com uma anotação entre parênteses |
| Introdução à Psicologia Forense | Paula Inez Cunha Gomide e Sérgio Said Staut Júnior (orgs.) | Biblioteca virtual · eixo 14 | (sem capa) | autor com uma anotação entre parênteses |
| Introdução às Obras de Freud, Ferenczi, Groddeck, Klein, Winnicott, Dolto, Lacan | J.-D. Nasio (org.) | Biblioteca virtual · eixo 14 | https://is1-ssl.mzstatic.com/image/thumb/Publication114/v4/4d/eb/b4/4debb4df-3b64-e0a7-8864-d6ff057d13a5/1013364425.jpg/200x300bb.jpg | autor com uma anotação entre parênteses |
| Jean Piaget no Século XXI: Escritos de Epistemologia e Psicologia Genéticas | Adrián Oscar Dongo Montoya (org.) | Biblioteca virtual · eixo 14 | (sem capa) | autor com uma anotação entre parênteses |
| Linguagem: Os Segredos da Sedução pela Poderosa Força das Palavras | (autor não informado) | Biblioteca virtual · eixo 14 | (sem capa) | sem autor certo |
| Manipulação | (autor não informado) | Biblioteca virtual · eixo 14 | (sem capa) | sem autor certo |
| Manual do Xaveco: Como Conquistar uma Mulher | (autor não informado) | Biblioteca virtual · eixo 14 | (sem capa) | sem autor certo |
| O Livro da Psicologia | Vários autores | Biblioteca virtual · eixo 14 | (sem capa) | sem autor certo |
| O Livro Negro da Psicanálise: Viver e Pensar Melhor sem Freud | Catherine Meyer (org.) | Biblioteca virtual · eixo 14 | (sem capa) | autor com uma anotação entre parênteses |
| Patologias do Social: Arqueologias do Sofrimento Psíquico | Vladimir Safatle, Nelson da Silva Junior e Christian Dunker (orgs.) | Biblioteca virtual · eixo 14 | https://is1-ssl.mzstatic.com/image/thumb/Publication118/v4/e7/69/50/e76950e0-4065-e76b-cf43-71e06b00ea59/1024511287.jpg/200x300bb.jpg | autor com uma anotação entre parênteses |
| Psicanálise: A Clínica do Real | Jorge Forbes (org.) | Biblioteca virtual · eixo 14 | (sem capa) | autor com uma anotação entre parênteses |
| Psicanálise e Vida Covidiana: Desamparo Coletivo, Experiência Individual | Ana de Staal (org.) | Biblioteca virtual · eixo 14 | https://is1-ssl.mzstatic.com/image/thumb/Publication124/v4/f3/4b/b3/f34bb3de-3df9-bd4f-6f3c-4e596def58d9/1033195379.jpg/200x300bb.jpg | autor com uma anotação entre parênteses |
| Psicologia da Saúde: Teoria, Intervenção e Pesquisa | Railda Fernandes Alves (org.) | Biblioteca virtual · eixo 14 | (sem capa) | autor com uma anotação entre parênteses |
| Psicologia e Sociologia | (autor não informado) | Biblioteca virtual · eixo 14 | (sem capa) | sem autor certo |
| Psicologia Social: Principais Temas e Vertentes | Cláudio V. Torres e Elaine R. Neiva (orgs.) | Biblioteca virtual · eixo 14 | (sem capa) | autor com uma anotação entre parênteses |
| Psicometria | Claudio Simon Hutz, Denise Ruschel Bandeira e Clarissa Marceli Trentini (orgs.) | Biblioteca virtual · eixo 14 | https://is1-ssl.mzstatic.com/image/thumb/Publication124/v4/af/81/52/af8152f3-2ebf-1443-5049-fb4ade1dea7c/9788582712368.jpg/200x300bb.jpg | autor com uma anotação entre parênteses |
| Psicopatologia Lacaniana, vol. 1: Semiologia | Antônio Teixeira e Heloisa Caldas (orgs.) | Biblioteca virtual · eixo 14 | (sem capa) | autor com uma anotação entre parênteses |
| Psicopolítica e Psicopatologia do Trabalho | Fernanda Sousa-Duarte, Ana Magnólia Mendes e Emílio Peres Facas (orgs.) | Biblioteca virtual · eixo 14 | (sem capa) | autor com uma anotação entre parênteses |
| Psicoterapias: Abordagens Atuais | Aristides Volpato Cordioli e Eugenio Horacio Grevet (orgs.) | Biblioteca virtual · eixo 14 | https://is1-ssl.mzstatic.com/image/thumb/Publication128/v4/1c/85/4f/1c854f92-7483-011b-d43c-58f620785333/9788582715284.jpg/200x300bb.jpg | autor com uma anotação entre parênteses |
| Psicoterapias Cognitivo-Comportamentais: Um Diálogo com a Psiquiatria | Bernard Rangé (org.) | Biblioteca virtual · eixo 14 | (sem capa) | autor com uma anotação entre parênteses |
| Ruído | (autor não informado) | Biblioteca virtual · eixo 14 | (sem capa) | sem autor certo |
| Sobre Comportamento e Cognição (vols. 1–6) | Vários autores | Biblioteca virtual · eixo 14 | (sem capa) | sem autor certo |
| Temas Clássicos de Psicologia sob a Ótica da Análise do Comportamento | Maria Martha Costa Hübner e Márcio Borges Moreira (orgs.) | Biblioteca virtual · eixo 14 | (sem capa) | autor com uma anotação entre parênteses |
| Transtornos da Personalidade | Mario Rodrigues Louzã Neto e Táki Athanássios Cordás (orgs.) | Biblioteca virtual · eixo 14 | 10492002 | autor com uma anotação entre parênteses |
| As Mais Belas Parábolas de Todos os Tempos | Alexandre Rangel (org.) | Biblioteca virtual · eixo 15 | (sem capa) | autor com uma anotação entre parênteses |
| Ciência da Religião Aplicada: Ensaios pela Autonomia e Aplicação Profissional | Fábio L. Stern e Matheus Oliva da Costa (orgs.) | Biblioteca virtual · eixo 15 | (sem capa) | autor com uma anotação entre parênteses |
| O Livro das Religiões | Vários autores | Biblioteca virtual · eixo 15 | (sem capa) | sem autor certo |
| O Livro da Literatura | Vários autores | Biblioteca virtual · eixo 16 | (sem capa) | sem autor certo |

### Título a conferir (30)

**O que fazer:** Conferir o título no Catálogo Mestre (nome cortado, volume sem número ou #verificar).

| Livro | Autor | Onde | Capa | Por que está aqui |
|---|---|---|---|---|
| Coraline | Neil Gaiman e Dave (P. Craig) Russell | Estante física · eixo 2 | 15272781 | marcado #verificar no catálogo |
| Noite do Sul | Érico Veríssimo | Estante física · eixo 4 | (sem capa) | marcado #verificar no catálogo |
| A Arte de Envelhecer | Irvin D. Yalom (conforme a prateleira) | Estante física · eixo 14 | (sem capa) | marcado #verificar no catálogo |
| A Guerra do Fogo | J.-H. Rosny | Recomendações · eixo 1 | (sem capa) | marcado #verificar no catálogo |
| O Médico de Córdoba | Herbert Le Porrier | Recomendações · eixo 6 | (sem capa) | marcado #verificar no catálogo |
| A Tragédia e a Farsa | Flávio Henrique Calheiros Casimiro | Recomendações · eixo 11 | (sem capa) | marcado #verificar no catálogo |
| Há Dois Mil Anos... | Emmanuel / Chico Xavier | Recomendações · eixo 15 | 10582350 | título parece cortado |
| Contágio | Vários autores | Biblioteca virtual · eixo 2 | (sem capa) | marcado #verificar no catálogo |
| Especial: As Espadas | (autor não informado) | Biblioteca virtual · eixo 2 | (sem capa) | marcado #verificar no catálogo |
| Habitat | Simon Roy | Biblioteca virtual · eixo 2 | 15151772 | marcado #verificar no catálogo |
| A Vida | (autor não informado) | Biblioteca virtual · eixo 5 | (sem capa) | marcado #verificar no catálogo |
| Os Impostos | (autor não informado) | Biblioteca virtual · eixo 5 | (sem capa) | marcado #verificar no catálogo |
| Caminhos Misteriosos | Jason Rubin e Tyler Kirkham | Biblioteca virtual · eixo 7 | (sem capa) | marcado #verificar no catálogo |
| Ciclo Antarktos (The Antarktos Cycle) | Robert M. Price (org.) | Biblioteca virtual · eixo 7 | (sem capa) | marcado #verificar no catálogo |
| Cripta | Vários autores | Biblioteca virtual · eixo 7 | (sem capa) | marcado #verificar no catálogo |
| Lovecraft | Hans Rodionoff, Keith Giffen e Enrique Breccia | Biblioteca virtual · eixo 7 | 15202628 | marcado #verificar no catálogo |
| Rashomon | Victor Santos | Biblioteca virtual · eixo 7 | 14511222 | marcado #verificar no catálogo |
| Trilogia Lovecraft | (autor não informado) | Biblioteca virtual · eixo 7 | (sem capa) | marcado #verificar no catálogo |
| Linguagem e Cognição | (autor não informado) | Biblioteca virtual · eixo 9 | (sem capa) | marcado #verificar no catálogo |
| Einstein, Freud e Relações Internacionais: Guerra e Paz num Diálogo Interdisciplinar | Luis Henrique Beust | Biblioteca virtual · eixo 11 | (sem capa) | marcado #verificar no catálogo |
| Engenharia Social | (autor não informado) | Biblioteca virtual · eixo 11 | (sem capa) | marcado #verificar no catálogo |
| Tesouros Medievais | (autor não informado) | Biblioteca virtual · eixo 12 | (sem capa) | marcado #verificar no catálogo |
| Análise e Projeto de Sistemas | (autor não informado) | Biblioteca virtual · eixo 13 | (sem capa) | marcado #verificar no catálogo |
| El Proceso de Envejecimiento | (autor não informado) | Biblioteca virtual · eixo 14 | (sem capa) | marcado #verificar no catálogo |
| Introdução à Psicologia (6ª ed.) | (autor não informado) | Biblioteca virtual · eixo 14 | (sem capa) | marcado #verificar no catálogo |
| Linguagem: Os Segredos da Sedução pela Poderosa Força das Palavras | (autor não informado) | Biblioteca virtual · eixo 14 | (sem capa) | marcado #verificar no catálogo |
| Manipulação | (autor não informado) | Biblioteca virtual · eixo 14 | (sem capa) | marcado #verificar no catálogo |
| Manual do Xaveco: Como Conquistar uma Mulher | (autor não informado) | Biblioteca virtual · eixo 14 | (sem capa) | marcado #verificar no catálogo |
| Psicologia e Sociologia | (autor não informado) | Biblioteca virtual · eixo 14 | (sem capa) | marcado #verificar no catálogo |
| Ruído | (autor não informado) | Biblioteca virtual · eixo 14 | (sem capa) | marcado #verificar no catálogo |

## Sem capa: onde estão (1.050 livros)

Não é erro: é o que ainda falta. Quem já passou pelas fontes e não foi achado precisa de outra fonte ou de
uma escolha à mão; quem está sem autor certo precisa de correção no Catálogo Mestre antes de qualquer busca.

| Situação | Livros | O que falta |
|---|---|---|
| Procurada na Open Library e na Apple, sem resultado | 967 | outra fonte, ou escolher à mão |
| Não procurada: sem autor certo | 83 | corrigir o autor no catálogo |

### Sem autor certo (83)

Estes dependem do catálogo, não da busca: com o autor certo, a próxima execução já procura a capa.

| Livro | Autor no catálogo | Onde |
|---|---|---|
| Bhagavad Gita | (tradição hindu) | Recomendações · eixo 15 |
| Os Upanixades | (tradição hindu) | Recomendações · eixo 15 |
| Dhammapada | (tradição budista) | Recomendações · eixo 15 |
| Livro Tibetano dos Mortos (Bardo Thödol) | (tradição tibetana) | Recomendações · eixo 15 |
| 2001: Uma Odisseia no Espaço (em quadrinhos) | Jack Kirby | Biblioteca virtual · eixo 2 |
| Batman | Vários autores | Biblioteca virtual · eixo 2 |
| Cavalgada dos Quadrinhos Amaldiçoados | Vários autores | Biblioteca virtual · eixo 2 |
| Coleção Oficial de Graphic Novels Marvel (Salvat) | Vários autores | Biblioteca virtual · eixo 2 |
| Conan, o Bárbaro (em quadrinhos) | Vários autores | Biblioteca virtual · eixo 2 |
| Contágio | Vários autores | Biblioteca virtual · eixo 2 |
| Contos do Multiverso Sombrio | Vários autores | Biblioteca virtual · eixo 2 |
| Elfos | Vários autores | Biblioteca virtual · eixo 2 |
| Especial: As Espadas | (autor não informado) | Biblioteca virtual · eixo 2 |
| Gavião Arqueiro | Vários autores | Biblioteca virtual · eixo 2 |
| Grandes Clássicos DC | Vários autores | Biblioteca virtual · eixo 2 |
| Guerreiro Eterno | Vários autores | Biblioteca virtual · eixo 2 |
| Heróis Renascem | Vários autores | Biblioteca virtual · eixo 2 |
| John Carpenter's Tales of Science Fiction | Vários autores | Biblioteca virtual · eixo 2 |
| Klarion | Vários autores | Biblioteca virtual · eixo 2 |
| Morbius: O Vampiro Vivo | Vários autores | Biblioteca virtual · eixo 2 |
| O Sentinela | Vários autores | Biblioteca virtual · eixo 2 |
| Os Fabulosos X-Men | Vários autores | Biblioteca virtual · eixo 2 |
| Patrulha do Destino | Vários autores | Biblioteca virtual · eixo 2 |
| Quarteto Fantástico | Vários autores | Biblioteca virtual · eixo 2 |
| Senhor das Estrelas | Vários autores | Biblioteca virtual · eixo 2 |
| Superman vs. Apocalypse | Vários autores | Biblioteca virtual · eixo 2 |
| Thanos: Em Busca de Poder / Legado | Vários autores | Biblioteca virtual · eixo 2 |
| Thanos II | Vários autores | Biblioteca virtual · eixo 2 |
| Thor | Vários autores | Biblioteca virtual · eixo 2 |
| Torneio dos Campeões | Vários autores | Biblioteca virtual · eixo 2 |
| Viagem ao Centro da Terra (em quadrinhos) | Júlio Verne | Biblioteca virtual · eixo 2 |
| Vingadores (2017) | Vários autores | Biblioteca virtual · eixo 2 |
| Vingadores vs. X-Men | Vários autores | Biblioteca virtual · eixo 2 |
| WildC.A.T.s/X-Men | Vários autores | Biblioteca virtual · eixo 2 |
| X-Men: Massacre | Vários autores | Biblioteca virtual · eixo 2 |
| A Ilha do Tesouro (em quadrinhos) | Robert Louis Stevenson | Biblioteca virtual · eixo 3 |
| A Odisseia (em quadrinhos) | Homero | Biblioteca virtual · eixo 3 |
| A Volta ao Mundo em 80 Dias (em quadrinhos) | Júlio Verne | Biblioteca virtual · eixo 3 |
| Moby Dick (em quadrinhos) | Christophe Chabouté | Biblioteca virtual · eixo 3 |
| Quincas Borba (em quadrinhos) | Machado de Assis | Biblioteca virtual · eixo 4 |
| A Vida | (autor não informado) | Biblioteca virtual · eixo 5 |
| Os Impostos | (autor não informado) | Biblioteca virtual · eixo 5 |
| Contos de Horror (Vertigo) | Vários autores | Biblioteca virtual · eixo 7 |
| Contos Fantásticos 01 | Vários autores | Biblioteca virtual · eixo 7 |
| Contos Fantásticos 02 | Vários autores | Biblioteca virtual · eixo 7 |
| Contos Fantásticos 03 | Vários autores | Biblioteca virtual · eixo 7 |
| Cripta | Vários autores | Biblioteca virtual · eixo 7 |
| Evil Dead | Vários autores | Biblioteca virtual · eixo 7 |
| Hellblazer | Vários autores | Biblioteca virtual · eixo 7 |
| Hellraiser | Vários autores | Biblioteca virtual · eixo 7 |
| Monstro do Pântano | Vários autores | Biblioteca virtual · eixo 7 |
| Nas Montanhas da Loucura (em quadrinhos) | H.P. Lovecraft | Biblioteca virtual · eixo 7 |
| Trilogia Lovecraft | (autor não informado) | Biblioteca virtual · eixo 7 |
| Vertigo: Contos Inquietantes | Vários autores | Biblioteca virtual · eixo 7 |
| Vertigo (Opera Graphica) | Vários autores | Biblioteca virtual · eixo 7 |
| Filosofia Antiga (Série Investigação Filosófica) | Vários autores | Biblioteca virtual · eixo 9 |
| Linguagem e Cognição | (autor não informado) | Biblioteca virtual · eixo 9 |
| O Livro da Filosofia | Vários autores | Biblioteca virtual · eixo 9 |
| Textos Selecionados de Filosofia Latino-Americana I | Vários autores | Biblioteca virtual · eixo 9 |
| Democracia em Risco? 22 Ensaios sobre o Brasil Hoje | Vários autores | Biblioteca virtual · eixo 11 |
| Engenharia Social | (autor não informado) | Biblioteca virtual · eixo 11 |
| O Livro da Economia | Vários autores | Biblioteca virtual · eixo 11 |
| O Livro da Política | Vários autores | Biblioteca virtual · eixo 11 |
| O Livro dos Negócios | Vários autores | Biblioteca virtual · eixo 11 |
| Casa-Grande & Senzala em Quadrinhos | Gilberto Freyre | Biblioteca virtual · eixo 12 |
| Linguagem, Discurso e Sociedade: Caminhos que se Entrecruzam | Vários autores | Biblioteca virtual · eixo 12 |
| O Livro da História | Vários autores | Biblioteca virtual · eixo 12 |
| O Livro da Sociologia | Vários autores | Biblioteca virtual · eixo 12 |
| Tesouros Medievais | (autor não informado) | Biblioteca virtual · eixo 12 |
| Análise e Projeto de Sistemas | (autor não informado) | Biblioteca virtual · eixo 13 |
| El Proceso de Envejecimiento | (autor não informado) | Biblioteca virtual · eixo 14 |
| Frases Up: 250 Frases para Motivar e Iluminar o seu Dia | Vários autores | Biblioteca virtual · eixo 14 |
| Introdução à Psicologia (6ª ed.) | (autor não informado) | Biblioteca virtual · eixo 14 |
| Linguagem: Os Segredos da Sedução pela Poderosa Força das Palavras | (autor não informado) | Biblioteca virtual · eixo 14 |
| Manipulação | (autor não informado) | Biblioteca virtual · eixo 14 |
| Manual do Xaveco: Como Conquistar uma Mulher | (autor não informado) | Biblioteca virtual · eixo 14 |
| O Livro da Psicologia | Vários autores | Biblioteca virtual · eixo 14 |
| Psicologia e Sociologia | (autor não informado) | Biblioteca virtual · eixo 14 |
| Ruído | (autor não informado) | Biblioteca virtual · eixo 14 |
| Sobre Comportamento e Cognição (vols. 1–6) | Vários autores | Biblioteca virtual · eixo 14 |
| O Livro das Religiões | Vários autores | Biblioteca virtual · eixo 15 |
| Zen em Quadrinhos | Tsai Chih Chung | Biblioteca virtual · eixo 15 |
| O Livro da Literatura | Vários autores | Biblioteca virtual · eixo 16 |

## Como corrigir uma capa

1. Abra `catalogo/capas.tsv` e ache a linha do livro (o arquivo está na ordem do catálogo).
2. Ponha o número da capa na Open Library ou o endereço `https://…` da imagem.
3. Escreva `manual` na coluna `origem`: assim a busca nunca troca a sua escolha.
4. Rode `python tools/atualizar.py` para o painel receber a mudança, e `python tools/auditar_capas.py` para refazer este relatório.

Para ver o que cada fonte devolveria antes de escolher:
`python tools/capas.py --candidatos "Título" --autor "Nome"` (ou `--isbn 978…`, com o número da edição na mão).
