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
