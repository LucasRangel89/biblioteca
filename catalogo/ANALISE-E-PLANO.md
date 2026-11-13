# Análise independente e plano de próximos passos

Data: 12/11/2026. Análise escrita na branch `arena/aedc78d9-biblioteca`; registro operacional atualizado na
`arena/a44e06f7-biblioteca`.

Este arquivo tem duas partes. A **Parte A** foi escrita antes de ler a especificação enviada
(`Especificação tecnica - biblioteca.md`), a partir do repositório, dos scripts, dos testes e dos relatórios já
gerados. A **Parte B**, acrescentada depois, compara essa análise com a especificação e registra o que foi aceito,
adaptado ou recusado.

## Parte A — análise independente

### 1. Retrato do que existe hoje

O projeto já é um sistema pequeno, mas completo, de biblioteca pessoal:

- **Fonte única:** `catalogo/Biblioteca_Lucas_Catalogo_Mestre.md` + `biblioteca-virtual/inventario.tsv`.
- **Geração determinística:** `tools/atualizar.py` importa a biblioteca virtual, refaz os JSON de `src/` e monta
  `Biblioteca_Lucas_Dashboard.html`.
- **Painel estático de arquivo único:** HTML com CSS, dados, letras e JavaScript embutidos. Não há backend, banco de
  dados, login nem telemetria.
- **Dados do usuário no navegador:** leituras, comentários, anexos, capas enviadas e configurações ficam em
  `localStorage`/IndexedDB e saem por backup manual.
- **Capas:** 2.614 livros, 1.564 com capa (60%), 1.050 sem capa; 191 na fila de revisão. Fontes: Open Library,
  Apple Books e Google Books (terceira fonte ainda sem execução real). O robô `Buscar capas` foi desenhado para
  abrir PR, nunca publicar sozinho.
- **Sinopses:** 294 linhas pesquisadas, 292 com texto; ainda é uma fração pequena do catálogo.
- **Classificação:** 203 marcadores distintos; 29 linhas do catálogo com `#verificar`, 48 com `#sem-pt`, 245 HQs.
  O inventário tem 2.490 linhas e 27 marcações de conferência.
- **Testes:** 36 testes cadastrados no início desta análise (37 depois de acrescentar `fluxo_ci`). Os sem navegador
  rodam com Python puro; os de painel exigem Playwright + Chromium. A suíte de 36 testes ficou verde na rodada
  anterior; nesta rodada, a conferência local cobre os cinco testes rápidos.
- **Publicação:** GitHub Pages publica somente o HTML pronto quando algo entra em `main`. O workflow de capas é
  manual (`workflow_dispatch`) e propõe PR.

Números conferidos nesta rodada:

| Medida | Valor |
|---|---:|
| Livros no catálogo | 2.614 |
| Com capa | 1.564 |
| Sem capa | 1.050 |
| Fila de revisão de capas | 191 |
| Sinopses com texto | 292 |
| Linhas no inventário digital | 2.490 |
| Marcadores distintos | 203 |
| Testes cadastrados antes desta mudança | 36 |
| Testes cadastrados com `fluxo_ci` | 37 |
| Tamanho do HTML gerado | ~1.378 KB |

### 2. O que está forte e deve ser preservado

1. **Catálogo como fonte única.** Evita divergência entre painel, relatório e busca de capas.
2. **Painel sem backend.** Barato, privado, fácil de hospedar e de abrir offline. O custo é sincronização manual.
3. **Geração e testes antes de publicar.** O site não monta nada em produção; publica o artefato já testado.
4. **Busca de capas com revisão humana.** O robô abre PR; capas manuais não são sobrescritas; imagens não entram no
   repositório.
5. **Privacidade por padrão.** Nenhum dado anotado sai do navegador; capas podem ser desligadas; pedidos de imagem
   são o único tráfego externo do painel.
6. **Documentação viva.** `README.md` e `ROTEIRO.md` explicam o porquê das decisões, não só o comando.

### 3. Riscos e lacunas reais

#### 3.1. O laço operacional ainda não fechou

O workflow `Buscar capas` existe, mas a primeira execução real ainda não aconteceu. Nesta rodada, o PR #13 foi
mesclado para corrigir o contexto `runner.temp`; a tentativa de disparar o workflow via API retornou
`403 Resource not accessible by integration`. Isso não é falha do catálogo nem do painel: é permissão do token/integração
para disparar Actions. Enquanto isso não for resolvido, a terceira fonte (Google Books) continua sem prova real.

**Consequência:** não adianta adicionar mais fontes ou sofisticar a busca antes de fechar o ciclo
`buscar → testar → PR → revisar → main → site`.

#### 3.2. Não há CI de PR

Hoje o site publica quando entra em `main`, e os testes rodam a pedido ou dentro do robô de capas. Um PR comum pode
quebrar o painel sem barra vermelha automática. A etapa 5 do ROTEIRO já previa isso.

**Consequência:** o projeto depende demais de memória humana e de execuções locais.

#### 3.3. Dados pendentes dependem do usuário, não de mais código

Há títulos/autores a conferir, leituras reais ainda não registradas no catálogo, sinopses incompletas e dúvidas de
HQs/compactados. Nenhuma reescrita técnica resolve isso sozinha.

**Consequência:** o próximo ganho de qualidade vem de filas claras, importadores pequenos e relatórios acionáveis,
não de uma nova arquitetura.

#### 3.4. Sincronização entre aparelhos é o maior limite do modelo atual

Anotações ficam no navegador. Backup manual resolve preservação, mas não resolve uso contínuo em celular + computador.
Isso é uma limitação consciente, não um bug.

**Consequência:** qualquer proposta de sincronização precisa ser tratada como mudança de produto, com custo,
privacidade e migração explícitos. Não deve entrar escondida numa "auditoria".

#### 3.5. O arquivo único começa a ficar grande

~1,4 MB ainda é aceitável para um painel pessoal, mas crescerá com sinopses, temas e dados. O risco não é o tamanho
em si; é perder a capacidade de gerar, testar e diffar com clareza.

**Consequência:** manter build determinístico, testes de tamanho/estrutura e separação clara entre fonte e gerado.

#### 3.6. A especificação enviada pode ser útil, mas não é autoridade

O arquivo enviado deve ser tratado como proposta. O repositório já tem restrições combinadas: catálogo fonte única,
nada sem teste, privacidade, sem scraping de lojas, estimativa marcada como estimativa, aprovação humana.

**Consequência:** comparar item a item; aceitar o que reforça essas restrições, recusar o que as enfraquece.

### 4. Plano independente recomendado

Ordem por valor e risco. Cada item deve virar PR pequeno, testável e reversível.

#### P0 — Fechar o ciclo das capas e colocar CI no lugar

1. **Resolver a permissão de disparo do Actions** (ou disparar manualmente pela UI) e rodar a primeira busca real.
   - Critério: execução do `Buscar capas` termina, abre PR ou explica por que não havia mudança.
   - Se o token não puder disparar, registrar o passo manual e não fingir automação completa.
2. **CI de PR e push em branches de trabalho** com duas camadas:
   - rápida: importador, busca de capas, auditoria, fluxos de capas e CI, build determinístico, `node --check`;
   - completa: suíte com navegador, manual ou nightly, porque é cara.
   - Critério: PR fica vermelho se quebrar geração ou testes rápidos; para recusar o merge, a proteção de `main`
     precisa marcar essa verificação como obrigatória. O site continua publicando só de `main`, após a conferência.
3. **Gerador único de listagens** da biblioteca virtual, substituindo a rotina de `.bat` por pasta.
   - Critério: um comando gera todas as listagens; teste com fixture; não altera catálogo sozinho.

#### P1 — Filas de qualidade que dependem de resposta humana

4. **Relatório único de pendências** (ou consolidar os existentes) com:
   - `#verificar` por seção/arquivo;
   - capas sem autor certo;
   - sinopses faltantes por lote;
   - leituras reais ainda não registradas;
   - compactados/HQs que precisam de decisão.
   - Critério: o usuário consegue responder por lote; o relatório não inventa resposta.
5. **Importador de leituras reais** para o catálogo (`#lido`, data opcional, nota opcional).
   - Critério: uma lista simples enviada pelo usuário vira catálogo, não só `localStorage`.
   - Isso desbloqueia a gamificação sem inventar histórico.
6. **Lote pequeno de sinopses** com o mesmo processo já aprovado: pesquisa, fonte, data, texto curto, revisão.
   - Critério: cada lote tem teste/contagem e não mistura fonte duvidosa com fato.

#### P2 — Melhorias de produto depois que os dados reais entrarem

7. **Gamificação leve** conforme desenho já discutido: meta anual em páginas, ritmo sem cobrança, marcos que só se
   ganham, vocabulário do tema. Depende das leituras reais.
8. **Finanças mais coerentes:** juntar próximas aquisições/preços dentro de Finanças, se o usuário confirmar;
   manter preço como cotação humana enquanto não houver serviço confiável.
9. **"Tenho digital, quero físico"** como estado explícito, se isso representar melhor a coleção.
10. **Anotações fora do navegador** apenas como decisão separada: exportação/importação melhorada primeiro;
    sincronização real só com desenho aprovado.

#### P3 — Não fazer agora

- Reescrever o painel em framework/SPA só por moda.
- Criar backend/login/banco antes de haver necessidade comprovada de sincronização.
- Scraping de lojas para preço automático.
- Adicionar mais fontes de capa antes da primeira execução real da terceira fonte.
- Gamificação baseada em sequência de dias ou dívida de leitura.
- Misturar dados de exemplo com dados reais.

### 5. Critério de sucesso da próxima rodada

A próxima rodada é boa se:

1. o workflow das capas roda de verdade ou o bloqueio de permissão fica documentado com caminho manual claro;
2. todo PR passa por CI rápido;
3. o usuário recebe uma fila menor e mais respondível de pendências;
4. nenhuma decisão de produto grande é tomada sem aprovação explícita;
5. o painel continua estático, privado, gerado do catálogo e testado.

## Parte B — comparação com a especificação enviada

A especificação (`Especificação tecnica - biblioteca.md`, 12/11/2026) foi lida **depois** da Parte A. Ela é boa como
mapa de evolução, mas é larga demais para virar um único PR. O próprio documento manda confirmar cada achado antes de
mudar; vários achados já estavam endereçados ou precisam ser reinterpretados à luz do que o repositório faz hoje.

### O que eu aceito e sobe de prioridade

- **CI em PR e publicação condicionada a testes.** É o BIB-011/BIB-012 e também a etapa 5 do ROTEIRO. Entra agora,
  porque é barato, não mexe em dados do usuário e fecha o laço operacional.
- **Auditoria de qualidade sem alterar dados.** O princípio do BIB-007 é certo. O projeto já tem auditoria de capas;
  o próximo passo é consolidar pendências de catálogo, não criar uma migração.
- **Backup/restauração mais seguros.** Direção correta, mas deve vir em PR próprio, com teste de dados antigos e
  confirmação explícita. Não entra junto com CI.
- **Acessibilidade como requisito.** O projeto já tem `foco` e `a11y`; melhorias de combobox/tabs devem ser medidas
  contra esses testes, não refeitas por intuição.
- **Não reescrever, não recuperar o protótipo Next.js, não fazer scraping de lojas, não sincronizar escondido.**
  Isso já é combinado do projeto e permanece.

### O que eu adapto

- **Identificadores persistentes (BIB-002).** A direção é boa, mas o catálogo atual não é um banco relacional: é Markdown
  com três colunas, conciliação por `renomeados.tsv` e testes de migração. Trocar a chave agora seria uma mudança de
  formato com risco alto e benefício imediato menor do que CI/filas. Fica como proposta separada: primeiro desenhar
  `id` estável e compatibilidade, depois migrar.
- **IndexedDB como armazenamento principal (BIB-009/BIB-010).** Faz sentido se o volume de anotações crescer ou se a
  concorrência entre abas virar problema real. Hoje o painel tem backup, testes de armazenamento e modo sandbox.
  A migração não entra sem medição, plano de rollback e teste de restauração.
- **Concorrência entre abas (BIB-008).** Vale investigar com teste reproduzível. Se houver sobrescrita silenciosa,
  corrigir primeiro com aviso/bloqueio simples; só depois pensar em mesclagem.
- **Roadmap e documentação (BIB-035).** Em vez de espalhar já em cinco arquivos, este arquivo faz o papel de análise
  comparada. A divisão documental pode vir depois, sem apagar histórico.

### O que eu recuso ou deixo para decisão de produto

- **Executar BIB-002 a BIB-012 em sequência agora.** Misturaria formato de dados, persistência, UI e CI no mesmo
  momento. O risco de perda de dados é maior do que o ganho.
- **Sincronização remota, PWA, alertas de preço, perfil de autor e séries complexas.** São possibilidades, não
  necessidade comprovada. Dependem de decisão do usuário e de dados reais.
- **Metas/sequências de leitura que cobram visita diária.** Contrariam o desenho já aprovado de gamificação leve.
- **Otimização de performance por intuição.** O HTML de ~1,4 MB não é, por si, prova de gargalo. Medir antes.

### Decisão para esta rodada

1. Mesclar o PR #13, que corrigia o workflow das capas.
2. Tentar disparar `Buscar capas` em `main`. Se a integração não tiver permissão, documentar o bloqueio e o caminho
   manual, sem fingir que a busca rodou.
3. Implementar **CI rápido** e **publicação condicionada** (BIB-011/BIB-012), com teste estático do fluxo.
4. Registrar esta análise comparada no repositório.
5. Deixar identificadores, IndexedDB, backup avançado e UX profunda como próximos PRs, não como mudança silenciosa.

### Estado operacional das capas nesta rodada

- PR #13: **mesclado** em `main` (`cb02a31`).
- Workflow `Buscar capas`: **não disparado pela API**. As tentativas retornaram
  `403 Resource not accessible by integration`. O token/conexão atual consegue ler workflows e mesclar PRs, mas não
  criar `workflow_dispatch`. Caminho manual: Actions → **Buscar capas** → **Run workflow** em `main`, ou reconectar o
  GitHub no Arena com permissão para disparar Actions.
- Para a primeira execução real, manter os padrões: não refazer, usar Google Books, limite vazio e suíte completa
  desmarcada. O resultado esperado é um PR de capas para revisar, ou a mensagem de que nada mudou — não uma
  publicação direta no site.

### Conferência local desta mudança

- `python3 tools/atualizar.py`: os arquivos gerados continuam idênticos às fontes.
- `node --check` em todos os módulos de `src/js/`: sem erro de sintaxe.
- Os três workflows foram lidos com PyYAML e seus blocos `run` passaram por `bash -n` (validação local com uma
  dependência temporária; o CI e `fluxo_ci.py` não passam a exigir PyYAML).
- `python3 tools/qa/tudo.py importador busca_capas auditoria_capas fluxo_capas fluxo_ci`: **cinco testes, zero erros**.
- A suíte completa não foi repetida nesta rodada: este ambiente não tem o venv/Chromium da rodada anterior. Nenhum
  módulo do painel, dado do catálogo ou tema foi alterado; a mudança é de CI, testes do fluxo e documentação.
- A leitura da proteção de `main` também retornou 403. Não foi possível conferir ou ligar verificações obrigatórias;
  isso fica explícito no README e no ROTEIRO, em vez de prometer um bloqueio de merge que ainda não foi configurado.
- O PR desta mudança fica aberto para aprovação. **Não foi mesclado e não publicou o site.**

### Registro operacional posterior — PR #14 e primeiras buscas manuais

Esta seção atualiza o estado sem apagar o retrato anterior.

- **PR #14:** mesclada em `main` (`d7d0c20`) após aprovação explícita. A publicação passou pelo job `conferir` e
  publicou o mesmo HTML versionado; o CI rápido ficou verde nos gatilhos de push e de PR.
- **Disparo manual:** o usuário conseguiu acionar `Buscar capas` pela interface do GitHub. As execuções
  [#9](https://github.com/LucasRangel89/biblioteca/actions/runs/43303124412) e
  [#10](https://github.com/LucasRangel89/biblioteca/actions/runs/43305090974) rodaram em `main`, por
  `workflow_dispatch`, e terminaram com conclusão `success` do GitHub.
- **O que o sucesso não dizia:** as anotações das duas execuções registram o mesmo resultado:
  `780 apple · 752 edicao · 967 nao-achei-2 · 32 obra · 83 sem-autor · 7 consulta(s) falharam · 33 ficaram para a
  próxima execução (o Google Books não respondeu)`. Os passos de amostra, montagem, auditoria, testes e PR foram
  pulados porque `catalogo/capas.tsv` não mudou. Não houve PR de capas nem capa nova.
- **Conferência do arquivo:** o blob de `catalogo/capas.tsv` em `main` continua `0d87a03b5076f2cc6e6e79b7bcf00111c20a6c30`;
  o catálogo segue com 2.614 livros e 1.564 capas. O Google Books ainda não teve uma consulta bem-sucedida em produção.
- **Causa raiz do verde enganoso:** `capas.py` já devolvia código 1 quando o Google desistia, mas o passo da busca no
  workflow guardava esse código e terminava com `exit 0` para preservar capas parciais. A conferência desse código só
  acontecia dentro do passo de abrir PR; sem mudança, esse passo nem rodava.
- **Correção proposta nesta rodada:** a saída inteira da busca vai para o resumo da execução; fonte com falha gera
  aviso; um passo final `if: always()` confere o código da busca mesmo sem mudança; se houver mudança, qualquer falha
  de busca, amostra, auditoria ou testes deixa o PR em rascunho e a execução vermelha. O teste `fluxo_capas` cobre o
  desenho, e a conferência local exercitou o passo final com códigos de sucesso, falha, ausência e valor inválido.
- **Próximo passo seguro:** depois de aprovado e mesclado, repetir uma busca curta (limite 40) em `main` para ler o
  motivo concreto da recusa do Google no resumo. Não repetir às cegas nem marcar os 967 livros como procurados no
  Google enquanto a fonte não responder.
- **Proteção de `main`:** continua pendente de configuração no GitHub; o workflow não liga verificação obrigatória
  sozinho.

### Registro operacional posterior — PR #15 e caminho gratuito das capas

- **PR #15:** mesclada em `main` (`fb2d70a`) após aprovação explícita. A publicação seguinte passou
  (run `43310223733`); o site continua em <https://lucasrangel89.github.io/biblioteca/>.
- **Decisão de custo:** o projeto é totalmente gratuito. ISBNdb e qualquer assinatura/API paga foram descartados.
  O caminho aprovado é: chave opcional do Google Books, ISBN só quando conferido no exemplar, piloto pequeno do
  Internet Archive e medição em amostra antes de expandir.
- **Implementado nesta branch (`arena/107c0160-biblioteca`):**
  - `catalogo/isbns.tsv` opcional, começando só com cabeçalho; título/autor precisam casar com o catálogo, ISBN precisa
    fechar na conta de conferência e a fonte da conferência é obrigatória. Nenhum ISBN é inferido de outra edição.
  - Open Library por ISBN exato (`api/books`, `jscmd=data`) e Google por ISBN antes de título/autor; ISBN-10 e ISBN-13
    da mesma edição casam. Erro de rede não vira “não achei”.
  - Chave opcional `GOOGLE_BOOKS_API_KEY` em secret do GitHub, enviada no cabeçalho `X-Goog-Api-Key`; motivo de recusa
    vai ao resumo com a chave ocultada. Sem chave, a consulta pública continua sendo tentada.
  - Internet Archive apenas como piloto de leitura (`--piloto N` e `--candidatos … --arquivo`): candidatos/miniaturas
    para revisão humana, nunca casamento automático, nunca gravação em `capas.tsv`, fora do robô `Buscar capas`.
  - Painel e documentação passam a citar as três fontes gratuitas; a chave “Mostrar as capas” e a privacidade continuam.
- **Conferência local:** `python3 tools/atualizar.py` regenerou o painel sem mudar catálogo/capas; `node --check` passou
  em todos os módulos JS; os cinco testes rápidos (`importador`, `busca_capas`, `auditoria_capas`, `fluxo_capas`,
  `fluxo_ci`) passaram com zero erros; YAML dos três workflows e `bash -n` dos blocos `run` passaram. A suíte com
  navegador não foi repetida aqui (sem Playwright/Chromium neste ambiente); o teste `capas_painel` foi atualizado para
  exigir também a menção ao Google Books em “Seus dados”.
- **O que não foi feito:** nenhuma busca real nova, nenhum dispatch (a API continua devolvendo 403), nenhum merge desta
  mudança, nenhuma publicação. O Google Books ainda não teve uma consulta bem-sucedida em produção.
- **PR desta mudança:** [#16](https://github.com/LucasRangel89/biblioteca/pull/16), **mesclado** em `main` (`f8a0d50`)
  após aprovação explícita. O CI rápido do PR passou (run `43318662762`); a publicação seguinte também passou
  (run `43319394942`).
- **Próximo passo seguro:** rodar `Buscar capas` em `main` com limite 40 e ler o motivo no resumo. Só então medir o
  piloto/ISBN numa amostra de cerca de 100 livros sem capa. Gerador único de listagens e revisão de `referencias/`
  continuam como próximos PRs da Etapa 5, para não misturar escopos.

## Parte C — análise independente antes de ler “Análise crítica do repositório biblioteca.md”

Data: 12/11/2026, depois do merge do PR #16 (`f8a0d50`) e da publicação bem-sucedida do site
(run `43319394942`). Esta parte foi escrita **antes** de abrir o novo documento enviado pelo usuário; o documento
entra depois apenas como conjunto de recomendações a comparar, não como ordem de execução.

### Retrato conferido agora

- Catálogo/painel: 2.614 livros, 1.564 capas, 1.050 sem capa; `catalogo/isbns.tsv` existe e está vazio; nenhuma capa
  nova foi produzida pelo PR #16. O próximo teste real das capas continua sendo o dispatch manual com limite 40.
- Biblioteca virtual: 38 listagens `.txte`, 2.490 linhas de inventário, 38 pastas no inventário. O importador é
  determinístico e já sabe ler CP850, UTF-8 e UTF-16; a lacuna operacional é **produzir** as listagens no computador
  do usuário sem depender de um `dir /b` manual por pasta.
- Etapa 5: CI rápido e publicação condicionada estão no ar; ainda faltam gerador único de listagens, revisão de
  `referencias/` e proteção obrigatória de `main` (esta última é configuração do GitHub, não código).
- `referencias/`: nenhum script, workflow ou módulo do painel importa esse diretório. O protótipo Nextjs tem schema
  Prisma só com `User`/`Post`, banco de exemplo vazio e parser que gera dados fictícios; não há dado real do usuário
  ali que justifique migração. O HTML de inspiração e o catálogo v3 são histórico/inspiração, não fonte ativa.
- Privacidade e custo: o painel continua estático, anotações só no navegador, capas desligáveis, sem imagem no
  repositório e sem serviço pago. Qualquer proposta que quebre isso deve ser recusada ou redesenhada.

### Decisão independente de prioridade

1. **Gerador único de listagens** é o próximo maior ganho para o usuário leigo: fecha a Etapa 5 (“dois cliques, um
   envio, um pedido”), reduz erro de encoding/nome de arquivo e não toca no catálogo nem no painel. Deve ser pequeno,
   testável com pastas fictícias, idempotente e explícito sobre o que gerou/ignorou. Não deve tentar adivinhar título,
   autor nem classificação: isso continua sendo trabalho do importador/inventário.
2. **Revisão de `referencias/`** vem junto apenas como documentação/decisão de guarda: declarar o que é histórico,
   o que não deve ser executado e o que não é fonte de dados. Não recuperar o protótipo, não migrar banco vazio.
3. **Capas** ficam aguardando o teste real curto em `main`; não adicionar mais fonte nem expandir piloto antes de medir.
4. Filas de pendências, leituras reais e sinopses continuam importantes, mas dependem de respostas do usuário ou de
   lote próprio; não misturar com o gerador.

### Riscos que o gerador precisa cobrir

- Não sobrescrever listagem errada por engano: gerar em destino explícito, mostrar prévia com `--conferir` e só
  gravar quando o conteúdo mudar.
- Preservar o contrato do importador: uma listagem por pasta, nomes de arquivo/subpasta como o `dir /b` mostraria,
  extensão `.txte`, compatível com CP850/CRLF ou UTF-8; não incluir a própria listagem nem o gerador.
- Pastas de HQ: subpastas de série entram pelo nome; subpasta que é outra biblioteca (`novashqs/novas` →
  `novasHQSS`) precisa de regra explícita, não heurística silenciosa.
- Pasta nova ou subpasta sem listagem (ex.: `HQs/Mangás`) deve aparecer como decisão/aviso, não entrar calada nem
  sumir. O gerador não deve transformar toda subpasta de série em pasta da biblioteca.
- Windows sem Python no PATH: se houver wrapper `.bat`, ele deve ser mínimo e apontar erro claro; a lógica testável
  fica em Python. Nenhum wrapper pode alterar catálogo, inventário ou painel.

## Parte D — comparação com “Análise crítica do repositório biblioteca.md”

O documento foi lido **depois** da Parte C. Ele é útil como auditoria externa e como lista de recomendações; não é
ordem de execução. Vários achados são reais, outros já foram corrigidos nas rodadas anteriores, e alguns números
precisam de correção no estado atual.

### O que conferi e aceito

- **Persistência é o maior risco de perda irreversível.** O painel grava um registro único em `localStorage`, não há
  `BroadcastChannel`/evento `storage`, não há lembrete de backup nem cópia automática antes de importar. A cópia
  `:falha` só cobre corrupção de leitura, não substituição por backup. Aceito como **próximo PR de produto**, com
  testes de navegador e cuidado de migração.
- **Exposição pública.** O README já diz que o endereço é público, mas a meta description do HTML ainda chamava o
  painel de “pessoal e privado”. Isso é enganoso: catálogo, inventário e listagens estão no repositório público.
  Corrigir o texto é barato e entra agora; tornar o repositório privado ou remover listagens é decisão do dono.
- **Acessibilidade.** A busca rápida tem `role="combobox"` sem `aria-activedescendant`; as abas têm `aria-selected`
  mas não o padrão completo de teclado/setas. São dívidas reais, para PR próprio com teste de navegador.
- **`referencias/` é peso morto operacional.** Nenhum código ativo importa o diretório; o protótipo não tem dados
  reais. Revisar e documentar a guarda entra agora; não recuperar o protótipo.
- **Qualidade de dados.** 15 sem autor, 29 `#verificar`, 48 `#sem-pt`, 3 `#lido` no catálogo, sinopses ainda pequenas.
  Continua verdadeiro; depende de filas e respostas humanas, não de mais arquitetura.

### O que já está resolvido ou precisa de correção

- **“CI não testa nada antes de publicar” está desatualizado.** Desde o PR #14, `publicar-site.yml` tem job
  `conferir` que roda `tools/atualizar.py`, `git diff --exit-code`, `node --check` e os testes rápidos antes de
  `publicar`; `verificar.yml` roda em PR e ramos de trabalho.
- **“Histórico com 1 commit” não descreve o estado remoto atual.** Este checkout é raso (`shallow`), mas o remoto já
  tem PRs e merges (#12 a #16). A limitação local de histórico continua afetando `posse`, `inicio` e `vistoria`.
- **Versões das Actions.** `checkout@v7`, `upload-pages-artifact@v5` e `deploy-pages@v5` estão em uso e as execuções
  reais recentes passaram; não há evidência atual de versão inexistente.
- **Números de limpeza.** Antes desta rodada eram 55 arquivos `.py` em `tools/qa/` (não 80); com o novo teste do
  gerador, 56. `referencias/` tem ~1,0 MB (não 1,2 MB). A bagunça de nomes `run*`/`func*`/`medir*` é real, mas não
  justifica apagar testes sem inventário e substituição.
- **Capas.** O documento cita só Open Library e Apple; o estado atual já tem Google Books como terceira fonte
  gratuita, ISBN conferido opcional e piloto do Internet Archive só de leitura (PR #16).

### O que adapto ou recuso nesta rodada

- **Não fazer tudo do P0 ao mesmo tempo.** Backup/abas/persistência tocam no dado mais precioso do usuário e exigem
  suíte de navegador; não misturo isso com gerador de listagens e revisão de referências.
- **Não tornar o repositório privado nem remover listagens automaticamente.** Isso mudaria acesso e fluxo de
  atualização; fica como decisão explícita do dono. Por ora, corrigir a linguagem para não prometer privacidade do
  catálogo.
- **Não migrar para IndexedDB, não criar ID estável agora, não refatorar JS global.** São mudanças maiores, com
  migração e risco; ficam para desenho próprio.
- **Não apagar `referencias/` nem testes antigos às cegas.** Documentar o que é arquivo morto e impedir uso acidental
  é suficiente nesta rodada; remoção física pode vir depois, com histórico preservado.

### Decisão final para esta rodada

Preparo uma mudança pequena da **Etapa 5**: gerador único de listagens em Python (com wrapper mínimo para Windows),
revisão documental de `referencias/`, correção da meta description pública e testes. Depois disso, o próximo PR de
produto segue a recomendação P0 do documento: **lembrete/atalho de backup e cópia automática antes de importar**, com
testes de navegador. A busca real curta das capas (limite 40) continua pendente de disparo manual na UI.

### Registro operacional desta rodada

- **Implementado:** `tools/gerar_listagens.py`, `Gerar listagens.bat`, `tools/qa/gerar_listagens.py`,
  `referencias/LEIAME.md`, a meta description pública em `src/index.html`, o cadastro do teste novo em `tools/qa/tudo.py`
  e os dois workflows (`verificar.yml` e `publicar-site.yml`). O nível rápido passa de cinco para **seis testes**; a
  suíte completa, de 37 para **38**. Nenhuma listagem real, inventário, catálogo ou capa foi alterada.
- **Conferência local:** `python3 tools/qa/gerar_listagens.py` passou com zero erros; `python3 tools/atualizar.py`
  regenerou o painel e `--conferir` não propôs mudança; `node --check` passou nos módulos JS; os seis testes rápidos
  passaram; YAML dos workflows e `bash -n` dos blocos `run` passaram. A suíte com navegador não foi repetida aqui
  (sem Playwright/Chromium neste ambiente). O `.bat` foi conferido como texto/contrato, não executado em Windows real.
- **Envio:** a rodada anterior ficou bloqueada porque a branch antiga já tinha PR mesclado/fechado. Com o Continue,
  o trabalho foi reaplicado na branch ativa `arena/2a25f33b-biblioteca` e enviado no PR
  [#17](https://github.com/LucasRangel89/biblioteca/pull/17). Nenhum merge ou publicação automática.
- **O que não foi feito:** nenhum dispatch de capas, nenhuma remoção física de `referencias/` ou de testes antigos,
  nenhuma mudança de persistência/IndexedDB/abas.

### Registro operacional da rodada da capa dentro do arquivo

- **Gatilho.** O `Buscar capas` manual (execução 43428251481) falhou de novo: sete consultas sem resposta do Google
  Books e 43 livros empurrados para a próxima execução. Nada mudou no site. Como 1.050 livros estão sem capa e muitos
  deles existem como arquivo, abrimos outra frente: ler a capa de dentro do próprio arquivo, no navegador.
- **Decisão registrada:** só **EPUB e CBZ** (escolha explícita do dono do projeto). PDF fica de fora — não é pacote
  `.zip` e a "capa" de lá seria a primeira página renderizada. Nenhuma fonte paga, nenhum raspador de loja, nenhuma
  imagem no repositório, nenhuma chave no painel.
- **Implementado** no PR [#19](https://github.com/LucasRangel89/biblioteca/pull/19) (branch `arena/8f7427a5-biblioteca`,
  commit `de3280c`): `src/js/54-capa-digital.js` (novo, abre o pacote e acha a capa anunciada), `src/js/55-anexos.js`
  (usa a imagem no lugar de nenhuma capa, pelo mesmo reduzidor e pela mesma gravação da "Enviar capa…", com o
  `gravarCapa` compartilhado), `tools/qa/capa_digital.py` (novo teste rápido), cadastro nos `tudo.py`/`fluxo_ci.py`
  e nos dois workflows, `README.md` e `ROTEIRO.md` (Etapa 11, parte 5, e o princípio de privacidade).
- **Regras que valem:** a capa do arquivo só entra em livro sem capa enviada e sem capa no catálogo; SVG, endereço
  externo, bloco acima de 16 MB, pacote truncado ou em ZIP64 devolvem nada em silêncio; o EPUB é lido pelo índice
  anunciado (`cover-image`, `meta name="cover"`, nome "capa"/"cover") e nunca pela primeira imagem do miolo; no CBZ
  vale a anunciada e, sem isso, a primeira imagem em ordem numérica.
- **Conferência local:** os sete testes rápidos passaram (`TUDO CERTO`), com 54 previsões executadas no Node contra 21
  pacotes montados pelo teste; `node --check` em cada módulo e no pacote juntado (11 módulos); `python tools/atualizar.py`
  regenerou o painel (1390 KB) e `--conferir` não propôs mudança; `git diff --check` limpo.
- **Não conferido aqui:** a suíte com navegador (`anotacoes` e as outras) — sem Chromium neste ambiente. O `anotacoes.py`
  não foi alterado justamente para não mexer às cegas num teste que não posso rodar.
- **Pendente do dono do projeto:** aprovar (ou não) o merge do #19; quando o Google Books responder, rodar o
  `Buscar capas` pela interface (Actions → **Buscar capas** → **Run workflow**, limite **40**).

### Registro operacional — rodada 2 da capa dentro do arquivo (feedback do teste no painel)

- **O que o dono do projeto relatou** (testado na pré-visualização, 12/11/2026): a extração funcionou — *"a capa subiu
  na mesma hora"* — mas apareceram três coisas: o **limite de 5 MB** da anexação travava antes de qualquer leitura
  (os primeiros EPUBs nem chegavam a ser abertos), o card ficava marcado como **"possui análise"** quando o arquivo é
  o próprio livro, e a confirmação explícita de que **livro com capa não deve ser substituído**. O pedido novo aprovado
  foi o **botão que percorre a pasta** e extrai as capas de uma vez.
- **Decisões desta rodada:**
  1. **Leitura por fatias** (`54-capa-digital.js`): o pacote é aberto pela cauda (o índice do fim), depois só a entrada
     da capa é lida. Um EPUB de 5,6 MB custa poucas dezenas de KB lidos; o arquivo nunca entra inteiro na memória.
  2. **EPUB/CBZ acima do limite dão a capa sem serem guardados** (`55-anexos.js`): o arquivo não entra em "Suas
     anotações" (o limite de 5 MB é do armazenamento e do backup), mas a capa é lida e aplicada, e o aviso diz os dois
     lados. Regras de sempre intactas para os outros tipos (mensagem idêntica, conferida no `capa_digital`).
  3. **"Possui análise" só para arquivo seu**: `.epub`, `.cbz`, `.cbr`, `.mobi`, `.azw3`, `.djvu`, `.fb2` não marcam
     mais. **PDF continua marcando**, de propósito — pode ser o livro ou um documento seu, e a extensão sozinha não diz.
  4. **`56-lote-capas.js`** (novo): "Seus dados" → "Capas dos livros" → **"Buscar capas numa pasta de arquivos…"**.
     Escolhe-se a pasta (`webkitdirectory`, sem permissão especial e sem servidor); o livro é reconhecido pelo nome do
     arquivo ou da pasta, com a numeração de edição e o ano removidos; casa exato ou título que abre o nome. Ambíguo ou
     sem correspondência fica de fora e é contado no resumo. 400 livros por execução (o backup cresce com as capas) —
     rodar de novo para os demais. Quadro com andamento, botão "Parar", fechar o quadro interrompe, grava a cada 20.
- **Arquivos:** `src/js/54-capa-digital.js`, `src/js/55-anexos.js`, `src/js/56-lote-capas.js` (novo),
  `src/js/60-drawer.js` (o botão no quadro "Seus dados"), `tools/qa/capa_digital.py`, `README.md`, `ROTEIRO.md`
  (Etapa 11, parte 5). Nenhum dado do acervo, catálogo, inventário ou listagem foi tocado.
- **Conferência local:** `capa_digital` com **91 previsões** executadas no Node (pacote, ficha e varredura de pasta) e
  os sete testes rápidos `TUDO CERTO`; `node --check` em cada módulo e no pacote juntado (12 módulos);
  `python tools/atualizar.py` → 1401 KB e `--conferir` "Nada mudou"; `git diff --check` limpo. A suíte com navegador
  continua sem poder rodar aqui (sem Chromium) — `anotacoes` não foi alterado e suas mensagens esperadas continuam
  valendo (PDF e `.txt`/`.md` marcam, `grande.bin` dá a mesma mensagem de sempre).
- **Aprovação:** o merge do PR #19 foi autorizado pelo dono do projeto nesta rodada ("feito isso, pode mergear"), com a
  condição de que a varredura de pasta estivesse pronta — está.

### Registro operacional — rodada 3 da capa dentro do arquivo (a varredura real não achou capa nenhuma)

- **O que o dono do projeto viu (12/11/2026):** escolheu a pasta `Religião, Espiritualidade e Mitologia`, a varredura
  percorreu os arquivos e devolveu **"0 capas encontradas"**, com `55 arquivos sem livro correspondente` e `133 nomes
  com mais de um livro`. Nada foi aproveitado, e o quadro não dizia por quê.
- **A causa, medida nos dados dele** (1121 arquivos `.epub`/`.cbz` no inventário): o casamento olhava o nome do
  **arquivo e o nome da pasta** nas duas fases, inclusive na frouxa ("um título dentro do outro"). As pastas da
  biblioteca são **categorias de prateleira** — `psicologia`, `Filosofia`, `ficcao cientifica e fantasia` — e uma
  palavra dessas bate em dezenas de títulos: `psicologia` (10 caracteres, o mínimo da fase frouxa) abre
  `Psicologia da criatividade`, `Psicologia das massas`, `Psicologia do bolsonarismo`…, então quase tudo da pasta virava
  "ambíguo" e era descartado. Somava-se a isso um `break` no primeiro ambíguo, que jogava fora o casamento limpo que a
  outra chave (o nome do arquivo) teria dado, e o fato de a imagem achada não aparecer em lugar nenhum do resumo.
  No recorte dos 313 arquivos que interessavam (livros sem capa), a regra antiga acertava 252, perdia 27 e descartava
  34 à toa.
- **O conserto: o painel para de adivinhar e consulta a própria lista dele.** `biblioteca-virtual/inventario.tsv` já
  traz, linha por linha, o par "arquivo ↔ livro" conferido à mão uma vez. `tools/build_catalog.py` (função
  `nomes_digitais`) gera `src/digitais.json` — `{nome do arquivo normalizado: posição da linha no catálogo}` — só com
  `.epub`/`.cbz` e só de livros **ainda sem capa**; `tools/build.py` confere cada nome e cada posição e embute o mapa
  como `const DIGITAIS_NOMES` (325 nomes, 24 KB). Um nome que pertence a duas linhas fica fora do mapa e vira `AVISO`
  na geração (hoje são dois box sets). Na varredura, o mapa decide primeiro; o que está fora dele passa pelo casamento
  exato de título, e a **pasta só vale nesse modo exato** (série em pasta própria) — nunca na fase frouxa, que agora
  olha apenas o nome do arquivo. Um arquivo sem correspondência limpa é contado e deixado em paz.
- **O resumo diz em que ponto cada arquivo parou**: capa guardada, `sem capa dentro`, `pacote ilegível`,
  `capa fora do pacote`, `capa grande demais`, `imagem que não abriu`, livro que já tem capa, mais de um livro, nenhum
  livro — e lista até doze nomes que não soubemos ligar a um livro, com o motivo ao lado, porque é por eles que se
  corrige o inventário. Para isso, `capaDoDigital` (54) passou a devolver `{ motivo: '…' }` em vez de `null`, e a ficha
  continua ignorando o motivo (nada a dizer ali).
- **Dois sinais de capa que faltavam no EPUB** (aparecem nos arquivos reais baixados): a referência
  `type="cover"` do `<guide>` — o jeito dos EPUBs 2 e dos convertidos por Calibre, que não escrevem
  `<meta name="cover">` — e um pacote com **uma imagem só**, que é a capa dela. Item declarado `image/svg+xml` continua
  fora de concorrência, e um `<guide>` apontando para uma página (não para imagem) não dá licença de pegar o miolo.
- **O que isso rende na prática:** o mapa alcança **261 dos 1050** livros sem capa (325 arquivos; linhas de série
  agrupam mais de um arquivo, e a primeira capa fica), tudo numa execução só (o teto é 400). Nenhum arquivo é movido,
  nenhuma capa existente é trocada, nada sai do navegador.
- **Arquivos:** `tools/build_catalog.py` (novo `nomes_digitais`, `DIGITAL_LIDO`, `DEST_DIGITAIS`), `tools/build.py`
  (valida e injeta `DIGITAIS_NOMES`), `tools/atualizar.py` (o passo novo na descrição), `src/digitais.json` (gerado,
  versionado), `src/js/54-capa-digital.js`, `src/js/55-anexos.js`, `src/js/56-lote-capas.js`, `tools/qa/capa_digital.py`,
  `README.md`, `ROTEIRO.md` (Etapa 11, parte 5).
- **Conferência local:** `capa_digital` com **146 previsões** (116 no Node), `fluxo_ci` `TUDO CERTO` (sete testes);
  `node --check` em cada módulo; `python3 tools/build_catalog.py` + `python3 tools/build.py` → 1432 KB;
  `python3 tools/atualizar.py --conferir` → `Nada mudou.`; `git diff --check` limpo. A suíte com navegador continua sem
  rodar aqui (o Playwright do ambiente não veio nesta rodada) — quem a executa é o CI do PR.

### Registro operacional — o teto de 400 (pergunta do dono do projeto, 13/11/2026)

- **Pergunta:** "e se a pasta tiver mais que 400?" O teto corta a **leitura**, não a varredura: a pasta é percorrida
  inteira, tudo o que é reconhecido entra no plano, e só os 400 primeiros são abertos — o resto fica para a próxima
  execução, sem nada perdido de vista e sem nada adivinhado.
- **O ajuste (PR #21):** o aviso existia, mas só numa parte do painel — a nota miúda do alto do quadro dizia
  "400 por execução: N ficam para a próxima", e a linha de resumo do fim, que é o que se lê quando a varredura acaba,
  ficava muda sobre isso. O resumo passou a fechar com `· N livros ficam para a próxima execução (o teto é de 400 por
  vez)`, e o comentário do `LOTE_MAX` diz agora "livros LIDOS por execução — a pasta é percorrida inteira". O README e
  o ROTEIRO (Etapa 11, parte 5) dizem o mesmo. Repetir a varredura é o caminho normal: os que já receberam capa saem
  da lista sozinhos, porque passam a ter capa — não há estado nenhum a limpar entre uma execução e outra.
- **Teste:** um plano com 410 livros e 410 arquivos confere que todos os 410 são planejados (nada é perdido de
  vista) e que o corte é só de leitura; outra checagem confere no arquivo que o resumo do fim carrega o "ficam para a
  próxima". `capa_digital` sobe para **146 previsões** (116 no Node).
- **Antes disto:** o PR #20 (o casamento pelo inventário, os estágios do resumo e o `<guide>`) foi mesclado com
  aprovação explícita do dono do projeto e publicado em `https://lucasrangel89.github.io/biblioteca/`
  (`main` em `9b3e0b8`; o `Publicar o site` rodou em 37s e o HTML publicado é o do repositório).
