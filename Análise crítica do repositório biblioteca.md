# Análise crítica do repositório `biblioteca`

*Análise de 12/11/2026 · repositório LucasRangel89/biblioteca · inclui comparação com a "Especificação técnica - biblioteca.md"*

**Como foi feita.** O GitHub bloqueou a leitura direta da página, então clonei o repositório e li o código: README, os 10 módulos JS, o CSS, o pipeline Python, os workflows e a especificação da outra IA. Rodei o build e medi os dados do catálogo.

**Limites.** Não executei a suíte de testes (25–35 minutos, precisa de Chromium). Não abri o painel no navegador, então não medi desempenho real. Não vi seus dados pessoais, que ficam só no `localStorage` do seu navegador.

## 1. Visão geral

É um painel estático de uma biblioteca grande: 2.614 registros (97 volumes físicos, 2.049 obras digitais, 490 recomendações). Os dados saem de um Catálogo Mestre em Markdown, passam por um pipeline Python e viram um único HTML de 1,4 MB. São \~4.900 linhas de JS e CSS, sem framework e sem dependências, mais 80 scripts de QA.

Para um projeto pessoal, o rigor é incomum. As fraquezas estão menos no código do painel e mais em quatro áreas: persistência, processo de qualidade, qualidade dos dados e exposição pública.

## 2. Pontos fortes (verificados)

- **O build é reproduzível.** Rodei `tools/atualizar.py` e o HTML gerado ficou byte a byte igual ao commitado.
- **A reconciliação de dados é sofisticada.** Quando o catálogo muda, `conciliarCatalogo` liga seus dados salvos às linhas novas em 5 passes (nome atual, nome antigo via `renomeados.tsv`, título+autor, arquivo, identificador antigo). O catálogo não tem nenhum duplicado de título+autor.
- **Há rede de segurança contra corrupção.** Se os dados salvos não abrem, a cópia é preservada em `:falha` e o painel avisa. Anexos pesados vão para IndexedDB, e o backup `.json` os inclui.
- **O contraste é bom nos 8 temas.** Calculei WCAG para texto principal, secundário, terciário e botões de destaque: nenhum fica abaixo de 4,5:1.
- **Higiene de segurança no front.** Existe `esc()` e ele é usado nos pontos de `innerHTML` que inspecionei. O HTML tem `noindex` e `referrer: no-referrer`, e as fontes são embutidas (sem Google Fonts).
- **Documentação detalhada:** ROTEIRO, análise dos filtros e vistoria dos marcadores.
- **Dinheiro só na aba Finanças:** boa decisão de UX e de privacidade.

## 3. Pontos fracos

### Dados e persistência

1. **Seus dados vivem só em um navegador, em um único registro.** Todos os livros são gravados num único `localStorage` e regravados inteiros a cada alteração (debounce de 350 ms). Não há sincronização nem lembrete de backup. Se você limpar os dados do site, trocar de máquina ou o navegador expulsar o armazenamento, tudo some. Anotações, preços e leituras são o único dado insubstituível do projeto.
2. **Duas abas abertas sobrescrevem uma à outra.** Não encontrei `BroadcastChannel` nem evento `storage`.
3. **Importar backup substitui tudo.** Há confirmação com contagem de livros e data, o que é bom. Mas não vi cópia automática do estado anterior antes de substituir, nem opção de mesclar.
4. **O ID é posicional.** Livros do catálogo recebem `'c' + índice`, e as capas são indexadas pela posição (`CAPAS[i]`). A reconciliação mitiga bastante, mas depende de título+autor e de um `renomeados.tsv` mantido à mão. Um erro ali pode separar suas anotações do livro.

### Qualidade do catálogo

5. **73% do catálogo tem classificação estimada.** Dificuldade e extensão dos 1.910 livros digitais saíram do título e do autor; nenhum arquivo foi aberto. Os filtros de dificuldade e extensão funcionam sobre um dado frágil, e o README admite isso.
6. **Cobertura irregular:**
   - Capas: 60% no total (81% nas recomendações, 63% na estante, 53% no virtual).
   - Sinopses: 292 de 2.614 (11%).
   - As camadas `q-`/`clima-` cobrem 6–9% dos livros.
7. **15 obras sem autor, 29 com `#verificar` e 48 sem edição em português confirmada.**
8. **Só 3 livros têm `#lido` no catálogo.** O estado de leitura real fica no seu navegador, então não sei se o módulo de leitura é usado. Se for pouco usado, vale perguntar por quê antes de construir mais coisas em cima dele.

### Processo e engenharia

9. **O CI não testa nada antes de publicar.** `publicar-site.yml` só copia o HTML para o Pages. O comentário diz que o painel é "testado antes de entrar em main", mas isso depende de você rodar a suíte à mão.
10. **O histórico do Git tem 1 commit** ("Add files via upload"). Três testes (`posse`, `inicio`, `vistoria`) dependem de painéis antigos no histórico e passam a pular essas partes. Você também perdeu a capacidade de reverter e de ver o que mudou.
11. **Sobra lixo no repositório.** \~1,2 MB em `referencias/`: um protótipo Next.js abandonado (o `custom.db` dele tem tabelas vazias, então não vi risco de vazamento) e um HTML da DeepSeek. Em `tools/qa/` há scripts como `run1`…`run13`, `func3`…`func8` e `medir`, `medir2`, `medir3`, que dificultam a manutenção.
12. **JS global, sem módulos, lint ou tipos.** Os 10 arquivos concatenados compartilham escopo, e `10-data.js` e `60-drawer.js` têm linhas de 300+ caracteres. É manutenível enquanto só você mexe, mas frágil para refatorar.
13. **Versões das Actions não verificadas** (`checkout@v7`, `upload-pages-artifact@v5`, `deploy-pages@v5`): a API do GitHub limitou minhas requisições. Confira que existem.

### Privacidade

14. **O repositório e o site são públicos**, e `noindex` não é controle de acesso. Estão expostos o catálogo, os 2.382 nomes de arquivo da biblioteca virtual (`inventario.tsv`, `listagens/`) e o que você marcou como `#top`. Você pode estar confortável com isso, mas o README descreve o painel como "pessoal e privado", e isso não é verdade para o catálogo.
15. **As capas vêm da Open Library e da Apple Books em tempo de execução.** Essas lojas veem o que você abre; o rodapé avisa isso, e há um botão para desligar as capas.

## 4. Auditoria de UX/UI e design

**O que está bom**

- Skip link, `lang="pt-BR"`, `aria-current` na navegação e `scope="col"` nas tabelas.
- Temas coerentes, variáveis de cor organizadas e viewport com `viewport-fit=cover`.
- Folha de filtros no celular, filtros com contagem por opção e aviso permanente de livros ocultos.
- Impressão e CSV das listas filtradas inteiras, não só da página visível.

**Problemas**

| # | Achado | Gravidade |
| --- | --- | --- |
| U1 | **Combobox da busca incompleto.** Tem `role="combobox"` e `listbox`, mas não encontrei `aria-activedescendant`. A opção "ativa" é só uma classe CSS, então leitor de tela não anuncia o item navegado. | Alta |
| U2 | **Abas da tabela (`role="tab"`) sem o padrão completo.** Vi `aria-selected`, mas não confirmei foco por setas nem `tabpanel` associado. Vale testar com teclado. | Média |
| U3 | **Gráficos só têm `aria-label` curto.** Sem tabela alternativa nem resumo dos dados. | Média |
| U4 | **Alvos de toque pequenos.** Botões e chips têm 24–28 px de altura. Passa no mínimo de 24 px da WCAG 2.2, mas é apertado no celular. | Média |
| U5 | **Filtros pesados.** O grupo "Temas" tinha 62 botões e hoje tem 52, misturando área, assunto e forma do livro. A análise de 11/11 já apontava isso. | Média |
| U6 | **Sem suporte a `forced-colors`** (alto contraste do Windows) e só 1 bloco de `prefers-reduced-motion`. | Baixa |
| U7 | **Nada indica quando foi o último backup,** e não há lembrete (ligado ao risco 1). | Alta |
| U8 | **8 temas muito visuais.** Passam no contraste, mas cada tema novo aumenta o CSS (95 KB) e a superfície de teste. | Baixa |

## 5. Recomendações priorizadas

### P0 — proteger seus dados (1–2 dias)

1. **Lembrete e atalho de backup.** Mostrar "último backup há X dias" e exportar em um clique. É o item de maior retorno e menor risco.
2. **Cópia de segurança automática antes de importar/substituir,** guardada em IndexedDB com a última versão.
3. **Aviso entre abas** com `BroadcastChannel`: "outra aba alterou os dados, recarregue". Não precisa de mesclagem.
4. **Pedir armazenamento persistente** (`navigator.storage.persist()`) e avisar quando o espaço estiver perto do limite.
5. **Decidir o que é público.** Torne o repositório privado, ou tire o inventário de arquivos e as listagens do repositório público, ou mantenha tudo e ajuste o texto do README.

### P1 — processo (1 dia)

6. **Criar um workflow de CI** que reconstrua o HTML, compare com o commitado e rode um subconjunto rápido de testes (importador, catálogo, a11y) antes de publicar.
7. **Parar de subir arquivos pela web.** Usar git com commits pequenos para ter histórico de verdade.
8. **Limpar `referencias/` e `tools/qa/`,** movendo o que ainda importa para `archive/` ou apagando; o Git guarda o resto.
9. **Estabilizar os identificadores:** gerar um ID por livro no catálogo (hash curto do título+autor original, gravado no `.md`) em vez de `c`+posição, mantendo `renomeados.tsv` só como ponte.

### P2 — UX e acessibilidade (2–3 dias)

10. Corrigir o combobox com `aria-activedescendant` e anunciar a contagem de resultados.
11. Completar o padrão de abas (setas, `tabpanel`) ou trocar por botões simples.
12. Dar a cada gráfico uma tabela alternativa ou um resumo textual.
13. Subir os alvos de toque no celular para \~40–44 px, mantendo a densidade no desktop.
14. Separar o grupo "Temas" em área, assunto e forma.
15. Adicionar `forced-colors` e revisar `prefers-reduced-motion`.

### P3 — dados (contínuo)

16. Fazer a conferência por amostragem de 40 livros que a sua própria análise de filtros propõe, para medir quanto errou a dificuldade/extensão estimada.
17. Resolver os 15 sem autor e os 29 `#verificar`.
18. Priorizar sinopses para `#top` e para o que está em trilhas (301 livros), em vez de tentar os 2.614.

### Opcional, só se doer

19. Migrar o registro principal para IndexedDB (pesa só se o `localStorage` estourar).
20. Sincronização entre dispositivos: hoje há exportar e importar, e para um usuário só isso pode bastar.

## 6. Comparação com a especificação da outra IA

**Onde concordamos** (confirmei no código):

- Persistência em `localStorage` único e risco entre abas.
- O CI não executa a suíte de testes.
- O combobox e as abas precisam de ARIA.
- O backup precisa de versionamento e validação.
- O protótipo Next.js deve ficar fora, e `noindex` não é segurança.

**Onde a especificação erra ou exagera:**

- **IDs.** Diz que as associações dependem de posição e título+autor. É em parte verdade, mas ignora que a reconciliação em 5 passes já mitiga isso. O problema é real, porém menor do que o tom sugere.
- **Escopo.** São 35 itens de backlog, com PWA, perfis de autor, sincronização, metas e monitoramento de preços. Isso é um produto novo para um app de um usuário só. A própria especificação diz que deve preferir qualidade a volume e depois propõe 7 fases.
- **É um prompt, não uma análise.** O texto é dirigido a um agente, com "não faça X" e critérios de aceite genéricos. Não mediu nada: cobertura de capas e sinopses, quantidade de `#lido`, estado do histórico do Git, build reproduzível, contraste dos temas.
- **Nada sobre o histórico do Git** com 1 commit nem sobre os 80 scripts de QA bagunçados.
- **Protótipo.** Trata `referencias/prototipo-nextjs` como risco de exposição. O banco dele está vazio; é lixo, não vazamento.

**O que vale aproveitar dela:**

- A separação em camadas (dados, persistência, serviços, interface).
- O relatório de qualidade do catálogo (BIB-007), que você praticamente já tem em `analisar_marcadores.py` e `capas-revisao.md`.
- Filtros e buscas salvos, e desfazer operações.
- A ordem "integridade antes de funcionalidade": é o mesmo princípio do meu P0.

## 7. Se só desse para fazer três coisas

1. **Lembrete de backup + cópia automática antes de importar.** É onde um erro custa mais.
2. **CI que reconstrói e compara o HTML e roda os testes rápidos,** mais commits de verdade.
3. **Decidir o que fica público.**
