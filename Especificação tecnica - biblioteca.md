Especificação tecnica \- biblioteca

# **BIBLIOTECA — ESPECIFICAÇÃO MESTRA DE EVOLUÇÃO DO PROJETO**

**Documento de orientação para agentes de desenvolvimento de software**  
**Projeto:** [LucasRangel89/biblioteca](https://github.com/LucasRangel89/biblioteca)  
**Versão da especificação:** 1.0  
**Data da auditoria de referência:** 12 de novembro de 2026  
**Tipo:** Especificação técnica, funcional, arquitetural e de UX/UI  
**Objetivo:** Orientar a evolução contínua do sistema, preservando sua identidade, arquitetura funcional e integridade dos dados.

---

# **1\. DIRETRIZ GERAL AO AGENTE**

Você atuará como engenheiro de software sênior, arquiteto de aplicações, especialista em UX/UI, acessibilidade, qualidade de software e modelagem de dados.

Sua missão é analisar, corrigir, otimizar e evoluir o projeto **Biblioteca**, transformando-o em uma aplicação de gerenciamento bibliográfico pessoal robusta, eficiente, intuitiva, visualmente refinada e sustentável a longo prazo.

A aplicação deve permitir que o usuário gerencie sua biblioteca física e digital, acompanhe suas leituras, organize futuras aquisições, controle despesas, consulte informações bibliográficas e obtenha recomendações contextualizadas.

A evolução deve ser orientada por qualidade e utilidade real, não pelo volume de funcionalidades.

## **1.1. Regra fundamental**

**Não reescreva o projeto sem justificativa técnica excepcional.**

O sistema já possui uma base funcional relevante, com geração de dashboard HTML, módulos JavaScript, catálogo bibliográfico, armazenamento local, anexos, temas visuais e testes automatizados.

A prioridade é preservar o que funciona, identificar fragilidades, corrigir problemas reais e implementar melhorias de maneira incremental.

Antes de qualquer alteração:

1. Inspecione o estado atual do repositório e confirme a estrutura de arquivos.  
2. Leia a documentação e identifique as fontes de dados oficiais.  
3. Entenda o fluxo de geração do catálogo e do dashboard.  
4. Identifique os módulos responsáveis pelas funcionalidades que serão modificadas.  
5. Verifique os testes existentes e estabeleça uma linha de base.  
6. Identifique riscos de perda, corrupção ou incompatibilidade de dados.  
7. Apresente um plano de implementação dividido em etapas.

Não presuma que a auditoria descreve perfeitamente o estado atual do código. Ela representa uma fotografia técnica do repositório em 12/11/2026. Confirme cada constatação antes de modificar a aplicação.

---

# **2\. VISÃO DO PRODUTO**

## **2.1. Conceito**

A Biblioteca deve funcionar como um sistema pessoal de gestão do conhecimento literário.

Não deve ser apenas um catálogo de livros. Deve integrar, de maneira coerente, cinco dimensões:

* **Acervo:** quais obras o usuário possui, em quais formatos e edições.  
* **Leitura:** o que está lendo, o que já leu e o que pretende ler.  
* **Descoberta:** recomendações, autores, séries, movimentos e relações literárias.  
* **Gestão:** aquisições, preços, despesas e planejamento financeiro.  
* **Conhecimento:** informações bibliográficas, notas, observações e histórico pessoal.

A experiência deve transmitir organização, profundidade cultural, personalidade e facilidade de utilização.

## **2.2. Objetivos principais**

1. Permitir a consulta rápida e confiável do acervo.  
2. Reduzir o esforço necessário para cadastrar, localizar e organizar livros.  
3. Acompanhar o histórico e o progresso de leitura.  
4. Facilitar a descoberta de novas obras.  
5. Organizar compras, preços e planejamento de aquisições.  
6. Preservar dados pessoais e anotações do usuário.  
7. Oferecer uma interface consistente em computadores, tablets e celulares.  
8. Garantir que os dados permaneçam íntegros durante atualizações e mudanças estruturais.  
9. Permitir a expansão futura sem exigir uma reescrita completa.

## **2.3. Perfil de utilização**

Considere um usuário individual, com uma biblioteca pessoal que pode crescer continuamente.

O usuário pode possuir:

* Livros físicos.  
* Livros digitais.  
* Histórias em quadrinhos.  
* Mangás e graphic novels.  
* Coleções e séries.  
* Obras de múltiplos volumes.  
* Edições diferentes de uma mesma obra.  
* Livros adquiridos, desejados ou já lidos.  
* Obras sem todos os metadados bibliográficos disponíveis.

O sistema deve lidar com registros incompletos sem impedir operações comuns.

---

# **3\. CONTEXTO TÉCNICO DO REPOSITÓRIO**

A auditoria identificou a seguinte estrutura geral. O agente deverá validá-la antes de iniciar qualquer implementação.

## **3.1. Arquitetura existente**

O projeto utiliza uma aplicação predominantemente estática, construída por meio de um pipeline Python que consolida recursos em um dashboard HTML autocontido.

Elementos identificados:

* `Biblioteca_Lucas_Dashboard.html`: artefato HTML compilado e principal resultado da aplicação.  
* `README.md`: documentação geral e histórico do projeto.  
* `ROTEIRO.md`: planejamento, histórico de desenvolvimento e backlog.  
* `src/index.html`: estrutura da interface.  
* `src/styles.css`: estilos, variáveis visuais, temas e responsividade.  
* `src/js/00-util.js`: utilitários.  
* `src/js/10-data.js`: dados, normalização e armazenamento.  
* `src/js/20-charts.js`: gráficos.  
* `src/js/30-state.js`: estado da aplicação.  
* `src/js/40-panels.js`: painéis.  
* `src/js/50-table.js`: tabelas.  
* `src/js/52-listas.js`: listas.  
* `src/js/55-anexos.js`: anexos e arquivos.  
* `src/js/60-drawer.js`: drawers e interações relacionadas.  
* `src/js/70-app.js`: inicialização e integração geral.  
* `tools/build.py`: compilação do dashboard.  
* `tools/atualizar.py`: atualização do catálogo e geração.  
* `tools/qa/`: testes automatizados.  
* `.github/workflows/publicar-site.yml`: publicação do site.  
* `.github/workflows/buscar-capas.yml`: fluxo de busca de capas.

Também foi identificado um protótipo anterior em:

`referencias/prototipo-nextjs`

A documentação existente indica que esse protótipo está abandonado.

## **3.2. Arquitetura que deve ser preservada inicialmente**

O modelo atual apresenta vantagens importantes:

* Aplicação sem dependência obrigatória de servidor.  
* Distribuição simples.  
* Carregamento local.  
* Separação entre fonte de dados, módulos de interface e artefato gerado.  
* Possibilidade de utilização offline, respeitadas as limitações do armazenamento local.  
* Privacidade dos dados pessoais mantidos no navegador.

A arquitetura estática deve continuar sendo a abordagem padrão enquanto atender às necessidades do produto.

**Não migre para React, Next.js, banco remoto ou outra arquitetura apenas por preferência tecnológica.**

Uma mudança arquitetural só deve ser proposta quando existir um requisito concreto que a arquitetura atual não consiga atender de forma satisfatória.

---

# **4\. PRINCÍPIOS OBRIGATÓRIOS DE DESENVOLVIMENTO**

Todas as implementações devem seguir estes princípios.

## **4.1. Integridade dos dados**

A integridade do acervo tem prioridade sobre velocidade de implementação ou conveniência do código.

Nenhuma atualização pode apagar registros, sobrescrever silenciosamente dados do usuário ou alterar relacionamentos bibliográficos de maneira não rastreável.

Antes de qualquer migração estrutural:

* Criar mecanismos de backup.  
* Definir estratégia de migração.  
* Testar com cópia dos dados existentes.  
* Verificar registros antes e depois.  
* Garantir que seja possível recuperar uma versão anterior.

## **4.2. Evolução incremental**

Divida as alterações em unidades pequenas e verificáveis.

Cada etapa deve:

1. Ter escopo delimitado.  
2. Modificar apenas os módulos necessários.  
3. Preservar compatibilidade com os demais módulos.  
4. Possuir testes.  
5. Ser documentada.  
6. Ser validada antes de iniciar a etapa seguinte.

Não combine alterações extensas de arquitetura, banco de dados e interface em uma única implementação sem necessidade.

## **4.3. Simplicidade**

Prefira soluções nativas, dependências reduzidas e estruturas compreensíveis.

Não introduza bibliotecas, serviços, frameworks ou camadas de abstração sem benefício concreto.

Evite:

* Duplicação de estado.  
* Lógica espalhada entre módulos.  
* Componentes excessivamente genéricos.  
* Dependências desnecessárias.  
* Funções muito extensas.  
* Acoplamento entre interface e persistência.  
* Soluções complexas para problemas que ainda não existem.

## **4.4. Consistência**

Toda nova funcionalidade deve respeitar:

* O sistema de design existente.  
* As convenções de nomenclatura.  
* A arquitetura de módulos.  
* O fluxo de dados.  
* Os padrões de interação.  
* Os padrões de acessibilidade.

## **4.5. Documentação**

Atualize a documentação correspondente sempre que uma alteração modificar:

* Comportamento.  
* Estrutura de dados.  
* Armazenamento.  
* Processo de build.  
* Testes.  
* Fluxo de utilização.  
* Regras de negócio.

Não deixe a documentação descrevendo um funcionamento que já não existe.

---

# **5\. DIAGNÓSTICO TÉCNICO E PONTOS DE ATENÇÃO**

Esta seção reúne os principais achados da auditoria. Antes de corrigir, confirme se o problema ainda existe.

## **5.1. Modelo de armazenamento**

**Situação identificada:**

O estado principal da aplicação é persistido em `localStorage`, aparentemente por meio de um único registro serializado. Os anexos são tratados separadamente com IndexedDB.

O mecanismo atual oferece simplicidade, mas apresenta riscos de crescimento e concorrência.

### **Problemas a resolver**

* Escrita de um volume crescente de dados em um único registro.  
* Operações síncronas de serialização e gravação.  
* Possibilidade de sobrescrita entre abas abertas simultaneamente.  
* Dependência de limites e disponibilidade de `localStorage`.  
* Separação entre dados principais e arquivos anexados.  
* Ausência de sincronização nativa entre dispositivos.

### **Diretriz**

Avaliar a migração progressiva do armazenamento estruturado principal para IndexedDB.

Não executar a migração de forma abrupta.

A solução deverá considerar:

* Repositório de persistência independente da interface.  
* Versionamento do banco.  
* Migrações explícitas.  
* Transações.  
* Tratamento de falhas.  
* Recuperação de dados.  
* Compatibilidade com versões anteriores.  
* Backup e restauração.  
* Tratamento de concorrência entre abas.

O `localStorage` poderá continuar sendo utilizado para configurações simples, preferências visuais e estado não crítico.

### **Critérios de aceite**

* A aplicação continua funcionando com os registros preexistentes.  
* A migração preserva todos os dados.  
* A falha de uma operação de gravação não deixa o estado parcialmente corrompido.  
* O usuário é informado quando o armazenamento está indisponível ou sem espaço.  
* O sistema não perde dados ao atualizar a página.  
* A concorrência entre abas é tratada ou explicitamente limitada.

## **5.2. Identificadores bibliográficos**

**Situação identificada:**

Parte das associações parece depender de posições em arrays e de combinações textuais de título e autor.

Isso funciona em catálogos controlados, mas se torna frágil quando há renomeações, duplicatas, mudanças na ordem dos registros e diferentes edições de uma mesma obra.

### **Diretriz**

Implementar identificadores persistentes.

O agente deverá estudar a estrutura existente e propor uma migração progressiva para identificadores independentes dos títulos e posições dos registros.

Modelo conceitual recomendado:

| Entidade | Identificador | Objetivo |
| ----- | ----- | ----- |
| Obra | `work_id` | Identificar a obra intelectual |
| Edição | `edition_id` | Identificar uma edição específica |
| Exemplar | `copy_id` | Identificar uma cópia física ou digital |
| Autor | `author_id` | Identificar um autor |
| Série | `series_id` | Identificar uma coleção ou série |
| Leitura | `reading_id` | Identificar uma experiência de leitura |

Essas entidades são uma direção de modelagem, não uma exigência de criar todas imediatamente.

### **Regras importantes**

* Título não deve ser chave primária.  
* Autor não deve ser chave primária.  
* ISBN não deve ser a única identificação de uma obra.  
* Obras sem ISBN devem ser aceitas.  
* Reimpressões e novas edições não devem criar automaticamente obras intelectualmente distintas.  
* Diferentes traduções devem poder ser associadas à mesma obra.  
* O registro de um exemplar deve ser independente do registro da obra.  
* Identificadores não devem mudar quando o título ou os metadados forem corrigidos.

### **Critérios de aceite**

* Reordenar o catálogo não altera associações.  
* Alterar um título não quebra relacionamentos.  
* É possível associar diversas edições à mesma obra.  
* Duplicatas podem ser identificadas e tratadas sem exclusão automática.  
* Registros incompletos continuam válidos.

## **5.3. Backup, importação e restauração**

**Situação identificada:**

A importação de backup pode substituir os dados existentes. O comportamento é perigoso caso o usuário não perceba que uma restauração substitui o estado atual.

### **Requisitos**

Criar um fluxo de backup e restauração com:

1. Exportação integral.  
2. Versionamento do formato.  
3. Data e hora de criação.  
4. Identificação da versão do aplicativo.  
5. Inclusão dos dados estruturados.  
6. Inclusão de anexos, quando aplicável.  
7. Validação do arquivo antes da importação.  
8. Pré-visualização da restauração.  
9. Confirmação explícita.  
10. Backup automático do estado anterior antes de substituição.

A importação deve oferecer dois modos:

**Substituir:** substitui integralmente os dados atuais, após confirmação e backup de segurança.

**Mesclar:** tenta combinar registros utilizando identificadores persistentes, com regras para duplicatas e conflitos.

A mesclagem só deve ser implementada depois que a identificação dos registros estiver suficientemente confiável.

Não criar uma mesclagem baseada exclusivamente em título e autor.

### **Critérios de aceite**

* Arquivos inválidos são rejeitados sem alterar o banco.  
* O usuário sabe se a operação vai substituir ou mesclar.  
* A aplicação cria um ponto de recuperação antes da substituição.  
* Uma restauração pode ser validada e auditada.  
* Anexos não são descartados silenciosamente.  
* O resultado informa quantos registros foram importados, atualizados, ignorados ou sinalizados como conflito.

## **5.4. Concorrência entre abas**

O agente deve avaliar o comportamento da aplicação quando duas ou mais abas são abertas simultaneamente.

Implementar comunicação ou detecção de mudanças, utilizando mecanismos como `BroadcastChannel` ou eventos de armazenamento, conforme a arquitetura escolhida.

O objetivo é evitar que uma aba sobrescreva silenciosamente alterações realizadas em outra.

Quando não for possível mesclar alterações automaticamente, informar o usuário de maneira clara.

## **5.5. Qualidade dos metadados**

A auditoria identificou registros pendentes e campos incompletos, incluindo obras sem autoria confirmada.

### **Requisitos**

Criar um processo de auditoria de catálogo que identifique:

* Obras sem autor.  
* Títulos duplicados.  
* Edições potencialmente duplicadas.  
* ISBN inválido.  
* ISBN repetido.  
* Campos essenciais vazios.  
* Categorias inconsistentes.  
* Autores sem associação válida.  
* Séries sem volumes ou ordenação.  
* Registros com dados provisórios.  
* Capas sem correspondência confirmada.  
* Obras sem classificação suficiente.

O sistema deverá distinguir ausência real de informação de erro de cadastro.

Não preencher campos automaticamente com informações especulativas.

### **Ferramentas recomendadas**

Criar relatórios de qualidade com:

* Total de registros.  
* Registros completos.  
* Registros incompletos.  
* Registros potencialmente duplicados.  
* Erros de validação.  
* Pendências que exigem intervenção humana.

### **Critério de aceite**

A aplicação deve permitir identificar problemas no catálogo sem alterar automaticamente os dados originais.

---

# **6\. ARQUITETURA FUTURA RECOMENDADA**

A arquitetura desejada deverá separar claramente quatro responsabilidades.

## **6.1. Camada de dados**

Responsável por:

* Catálogo.  
* Obras e edições.  
* Exemplares.  
* Autores e séries.  
* Histórico de leitura.  
* Coleções personalizadas.  
* Metadados.  
* Dados financeiros.  
* Anotações pessoais.

## **6.2. Camada de persistência**

Responsável por:

* IndexedDB.  
* Configurações locais.  
* Anexos.  
* Backup e restauração.  
* Migrações.  
* Eventual sincronização.

Nenhum módulo visual deverá manipular diretamente a estrutura interna do banco.

## **6.3. Camada de serviços**

Responsável por operações de domínio:

* Cadastro e edição.  
* Busca.  
* Filtros.  
* Organização.  
* Recomendações.  
* Controle financeiro.  
* Progresso de leitura.  
* Importação e exportação.

## **6.4. Camada de interface**

Responsável por:

* Navegação.  
* Componentes.  
* Tabelas.  
* Formulários.  
* Painéis.  
* Gráficos.  
* Feedbacks.  
* Acessibilidade.  
* Responsividade.

A interface deve consumir serviços, e não depender de detalhes de armazenamento.

---

# **7\. AUDITORIA E REDESENHO DE UX/UI**

A interface deve ser refinada sem descaracterizar a identidade visual do projeto.

As melhorias deverão ser orientadas por princípios reconhecidos de usabilidade, acessibilidade e design de interação.

Referenciais:

* Heurísticas de usabilidade de Jakob Nielsen.  
* WCAG 2.2 nível AA.  
* W3C ARIA Authoring Practices Guide.  
* Design responsivo.  
* Design centrado no usuário.  
* Feedback imediato e prevenção de erros.  
* Lei de Hick.  
* Lei de Fitts.  
* Consistência e padrões.  
* Reconhecimento em vez de memorização.  
* Progressive disclosure.  
* Design system e design tokens.

## **7.1. Navegação principal**

A auditoria identificou seis áreas principais:

* Visão geral.  
* Biblioteca.  
* Recomendações.  
* Finanças.  
* Próximas aquisições.  
* Preços.

### **Recomendação**

Preservar as funcionalidades, mas avaliar uma organização mais clara.

Estrutura conceitual sugerida:

**Biblioteca**

* Visão geral.  
* Acervo.  
* Autores e séries.  
* Coleções.

**Leituras**

* Estou lendo.  
* Quero ler.  
* Já li.  
* Histórico.

**Descoberta**

* Recomendações.  
* Exploração por temas.  
* Autores relacionados.

**Gestão**

* Finanças.  
* Próximas aquisições.  
* Comparação de preços.

A reorganização não deve resultar em uma navegação excessivamente profunda.

No celular, priorizar uma navegação simples e acessível, preservando as funcionalidades importantes.

### **Critérios de aceite**

* Todas as áreas continuam acessíveis.  
* Não há duplicação desnecessária de opções.  
* A navegação funciona por teclado.  
* A navegação móvel não prejudica o conteúdo.  
* O usuário identifica facilmente onde está.

## **7.2. Visão geral**

A página inicial deve responder rapidamente:

1. Qual é a situação atual da biblioteca?  
2. O que estou lendo?  
3. Quais são minhas próximas leituras?  
4. Quais são minhas próximas ações?  
5. Como está minha organização?

### **Recomendações**

Priorizar:

* Leitura em andamento.  
* Progresso de leitura.  
* Próxima leitura planejada.  
* Adições recentes.  
* Pendências de cadastro.  
* Próximas aquisições.  
* Indicadores essenciais do acervo.

Gráficos devem complementar a informação, não competir com ela.

Evitar um dashboard composto por muitos indicadores sem utilidade prática.

**A página inicial deve ser operacional, e não apenas estatística.**

## **7.3. Busca global**

A busca existente é um recurso importante e deve ser preservado.

Evoluções recomendadas:

* Busca por título.  
* Busca por autor.  
* Busca por ISBN.  
* Busca por editora.  
* Busca por série.  
* Busca por palavras-chave.  
* Busca por temas.  
* Busca tolerante a acentos e variações de caixa.  
* Histórico de pesquisas.  
* Sugestões relevantes.  
* Navegação por teclado.  
* Indicação clara do resultado selecionado.

A busca deve suportar registros incompletos e evitar resultados inconsistentes.

### **Acessibilidade**

A implementação atual deve ser revisada para cumprir o padrão de combobox do WAI-ARIA.

Verificar:

* Associação entre campo e lista.  
* `aria-expanded`.  
* `aria-controls`.  
* `aria-activedescendant`.  
* Identificadores únicos das opções.  
* `aria-selected`.  
* Anúncio adequado dos resultados.  
* Navegação completa por teclado.

O destaque visual de um resultado não é suficiente: o estado selecionado também deve ser exposto semanticamente.

## **7.4. Filtros**

O sistema possui recursos de filtragem relevantes, mas muitos filtros simultâneos podem aumentar a carga cognitiva.

Implementar organização progressiva em três níveis:

**Filtros rápidos**

* Autor.  
* Gênero.  
* Status de leitura.  
* Formato.  
* Série.  
* Ano.

**Filtros personalizados**

* Editora.  
* Idioma.  
* Faixa de páginas.  
* Nota.  
* Data de aquisição.  
* Preço.  
* Disponibilidade.  
* Classificação.

**Filtros avançados**

* Combinações complexas.  
* Múltiplas condições.  
* Inclusões e exclusões.  
* Intervalos.  
* Regras compostas.

### **Melhorias adicionais**

* Contador de resultados.  
* Botão para limpar filtros.  
* Indicação de filtros ativos.  
* Combinação de filtros preservada ao navegar.  
* Salvar pesquisas frequentes.  
* Nomear filtros personalizados.  
* Restaurar pesquisas salvas.

O sistema deve evitar que um filtro ativo passe despercebido.

## **7.5. Tabelas e listas**

A aplicação possui tabelas com paginação, ordenação, busca e exportação.

Preservar os recursos atuais.

Evoluções:

* Seleção múltipla.  
* Ações em lote.  
* Colunas configuráveis.  
* Largura ajustável de colunas, quando pertinente.  
* Ordenação persistente.  
* Visualização em lista.  
* Visualização em grade.  
* Visualização de estante.  
* Exportação contextual.  
* Feedback para operações concluídas.  
* Desfazer ações reversíveis.  
* Melhor experiência em telas pequenas.

### **Responsividade**

No celular, evitar tabelas com rolagem horizontal excessiva.

Utilizar cards ou visualizações compactas quando melhorarem a leitura.

Não simplesmente ocultar informações sem oferecer acesso alternativo.

## **7.6. Ações e feedbacks**

Toda ação importante deve produzir feedback compreensível.

Exemplos:

* Livro adicionado.  
* Alteração salva.  
* Registro excluído.  
* Backup concluído.  
* Filtros aplicados.  
* Erro de importação.  
* Dados recuperados.  
* Alteração não salva.

Operações destrutivas exigem confirmação adequada.

Operações reversíveis devem oferecer opção de desfazer sempre que viável.

Não utilizar alertas intrusivos indiscriminadamente.

## **7.7. Hierarquia visual**

A interface deve distinguir claramente:

* Título de página.  
* Título de seção.  
* Informação principal.  
* Informação secundária.  
* Metadados.  
* Ações primárias.  
* Ações secundárias.  
* Estados vazios.  
* Avisos e erros.

O usuário não deve precisar interpretar uma grande quantidade de elementos com o mesmo peso visual.

Aplicar consistência na escala tipográfica, espaçamento, ícones, alinhamentos e estados interativos.

---

# **8\. SISTEMA VISUAL E DESIGN SYSTEM**

A auditoria identificou uma base visual consistente, com variáveis CSS e diferentes temas.

A evolução deve preservar esse investimento.

## **8.1. Design tokens**

Manter tokens centralizados para:

* Cores.  
* Fundos.  
* Superfícies.  
* Bordas.  
* Tipografia.  
* Espaçamento.  
* Raios.  
* Sombras.  
* Elevação.  
* Estados.  
* Transições.  
* Dimensões.

Evitar valores repetidos e divergentes espalhados pela folha de estilo.

## **8.2. Temas**

Preservar os temas existentes, desde que funcionais e acessíveis.

A auditoria identificou tema padrão claro/escuro e temas literários adicionais.

Não adicionar temas apenas para aumentar a quantidade.

Cada tema novo deve apresentar:

* Boa legibilidade.  
* Contraste suficiente.  
* Componentes coerentes.  
* Estados interativos distinguíveis.  
* Compatibilidade com gráficos e tabelas.

## **8.3. Componentes**

Padronizar, conforme necessidade:

* Botões.  
* Inputs.  
* Selects.  
* Checkboxes.  
* Radios.  
* Modais.  
* Drawers.  
* Tooltips.  
* Badges.  
* Cards.  
* Tabelas.  
* Paginação.  
* Tabs.  
* Toasts.  
* Estados vazios.  
* Carregamento.  
* Avisos.  
* Mensagens de erro.

Cada componente deve ter estados previsíveis:

* Normal.  
* Hover.  
* Focus.  
* Active.  
* Disabled.  
* Loading.  
* Error.  
* Success.

Não criar componentes abstratos sem uma necessidade real de reutilização.

## **8.4. Consistência de ícones**

Utilizar uma linguagem visual consistente.

Evitar misturar ícones de estilos muito diferentes.

Ícones sem rótulos devem possuir nome acessível e, quando necessário, tooltip.

---

# **9\. ACESSIBILIDADE — REQUISITOS OBRIGATÓRIOS**

A acessibilidade deve ser tratada como requisito de qualidade, não como acabamento opcional.

O objetivo é alcançar conformidade prática com WCAG 2.2 nível AA.

## **9.1. Teclado**

Todas as funcionalidades relevantes devem ser acessíveis por teclado.

Testar:

* Tab.  
* Shift \+ Tab.  
* Enter.  
* Espaço.  
* Esc.  
* Setas direcionais.  
* Atalhos contextuais, quando existirem.

O foco deve ser sempre perceptível.

Não remover o outline sem substituição adequada.

## **9.2. Foco visível**

Implementar indicadores de foco consistentes e suficientemente contrastantes.

Garantir que o elemento focado não fique encoberto por cabeçalhos, drawers ou barras fixas.

## **9.3. Tamanho dos alvos**

Avaliar alvos interativos segundo WCAG 2.2, observando o critério de tamanho mínimo aplicável e suas exceções.

Em telas sensíveis ao toque, preferir alvos maiores e espaçamento adequado.

## **9.4. Tabs**

Revisar os componentes de abas utilizados em `src/js/50-table.js`.

Validar:

* `role="tablist"`.  
* `role="tab"`.  
* Associação com painéis.  
* `aria-selected`.  
* `aria-controls`.  
* Identificadores únicos.  
* Gerenciamento de foco.  
* Navegação por setas.  
* Alternância entre seleção automática ou manual, conforme o comportamento escolhido.

Implementar o padrão de abas do WAI-ARIA APG.

## **9.5. Combobox**

Revisar a busca global.

Garantir sincronização entre estado visual, estado de teclado e estado acessível.

## **9.6. Gráficos**

Os gráficos SVG devem possuir descrição acessível.

Entretanto, `role="img"` e `aria-label` isoladamente podem não fornecer informação suficiente.

Sempre que um gráfico transmitir dados relevantes, oferecer também:

* Resumo textual.  
* Valores principais.  
* Alternativa tabular quando pertinente.

## **9.7. Leitores de tela**

Testar pelo menos uma combinação de leitor de tela e navegador.

Sugestões:

* NVDA com Firefox.  
* NVDA com Chrome.  
* VoiceOver com Safari, quando disponível.

Se o ambiente do agente não permitir testes reais, documentar a limitação e realizar verificações automatizadas e manuais complementares.

## **9.8. Movimento**

Respeitar `prefers-reduced-motion`.

Animações devem auxiliar a compreensão e não prejudicar navegação ou leitura.

---

# **10\. NOVO MÓDULO: EXPERIÊNCIA DE LEITURA**

Este é um dos principais investimentos funcionais recomendados.

O sistema deve evoluir de um inventário bibliográfico para um diário pessoal de leitura.

## **10.1. Estados de leitura**

Distinguir claramente:

* Quero ler.  
* Lendo.  
* Pausado.  
* Concluído.  
* Abandonado.  
* Relido.

A situação de propriedade do livro deve ser independente da situação de leitura.

Um livro pode ser desejado sem ser adquirido, por exemplo.

## **10.2. Sessões de leitura**

Permitir registrar uma sessão contendo:

* Livro.  
* Data.  
* Página inicial.  
* Página final.  
* Tempo dedicado, opcional.  
* Observações.  
* Nota pessoal, opcional.

O sistema poderá calcular:

* Páginas lidas.  
* Progresso.  
* Ritmo médio.  
* Tempo total.  
* Histórico por obra.  
* Dias de leitura.

Os cálculos devem respeitar a disponibilidade e a qualidade dos dados informados.

Não presumir que todos os livros utilizam a mesma paginação em edições diferentes.

## **10.3. Metas**

Permitir metas flexíveis:

* Livros por ano.  
* Páginas por período.  
* Tempo de leitura.  
* Frequência de leitura.

As metas devem ser opcionais e não podem transformar a aplicação em uma ferramenta de cobrança excessiva.

## **10.4. Histórico**

Criar histórico de leituras, com possibilidade de consultar:

* Obras concluídas.  
* Datas de início e término.  
* Releituras.  
* Avaliações.  
* Observações.  
* Progresso anterior.

O histórico deve preservar registros antigos mesmo quando o livro é removido de uma lista atual.

## **10.5. Notas e anotações**

Permitir anotações associadas à obra ou à sessão de leitura.

Considerar:

* Comentários pessoais.  
* Citações curtas.  
* Ideias.  
* Perguntas.  
* Temas.  
* Relações com outras obras.

Anotações são dados pessoais: devem permanecer sob controle do usuário e ser incluídas no mecanismo de backup.

---

# **11\. NOVO MÓDULO: AUTORES, SÉRIES E RELAÇÕES BIBLIOGRÁFICAS**

Criar páginas ou visualizações dedicadas a autores e séries, caso a qualidade dos dados permita.

## **11.1. Perfil de autor**

Apresentar:

* Nome.  
* Biografia breve, quando disponível.  
* Nacionalidade, quando confirmada.  
* Período histórico.  
* Obras presentes no acervo.  
* Obras desejadas.  
* Séries associadas.  
* Gêneros e temas recorrentes.  
* Relações com outros autores.

Não inventar biografias, datas ou nacionalidades.

Informações externas devem possuir fonte ou indicação de origem.

## **11.2. Séries e coleções**

Possibilitar:

* Visualização de volumes.  
* Ordem de leitura.  
* Volumes adquiridos.  
* Volumes ausentes.  
* Volumes desejados.  
* Edições disponíveis.  
* Progresso da série.

Não confundir ordem de publicação, cronologia interna e ordem recomendada de leitura.

Quando esses conceitos forem diferentes, apresentá-los separadamente.

## **11.3. Obra e edição**

Uma obra pode ter diversas edições, traduções e formatos.

A interface deve evitar que o usuário confunda uma obra intelectual com um exemplar específico.

A implementação deve respeitar a estrutura de dados e não forçar uma modelagem excessivamente complexa antes de sua necessidade.

---

# **12\. RECOMENDAÇÕES E DESCOBERTA**

As recomendações devem ser explicáveis e contextualizadas.

Evitar simplesmente exibir uma lista de títulos sem justificar a relação com o interesse do usuário.

## **12.1. Critérios possíveis**

* Autores semelhantes.  
* Temas recorrentes.  
* Gêneros.  
* Períodos históricos.  
* Movimentos literários.  
* Obras já avaliadas positivamente.  
* Séries.  
* Relações históricas e intelectuais.  
* Obras complementares.  
* Lacunas temáticas do acervo.

## **12.2. Explicabilidade**

Cada sugestão deve apresentar uma razão compreensível.

Exemplo:

"Recomendado porque compartilha o interesse por romances históricos, ambientação medieval e narrativas de formação."

Não inventar relações literárias.

## **12.3. Controle pelo usuário**

Permitir:

* Salvar recomendação.  
* Marcar como não interessante.  
* Adicionar à lista de desejos.  
* Consultar obras semelhantes.  
* Informar que já possui ou leu o livro.

A recomendação deve respeitar o acervo para não sugerir repetidamente obras já adquiridas.

## **12.4. Enriquecimento bibliográfico externo**

Avaliar integração com serviços como Open Library e Google Books, desde que os termos de uso e as limitações técnicas permitam.

O enriquecimento deverá ser:

* Opcional.  
* Sob demanda.  
* Validado antes de gravar.  
* Compatível com registros já existentes.  
* Não destrutivo.  
* Transparente quanto à origem dos dados.

Não substituir automaticamente dados corrigidos manualmente pelo usuário.

Não depender de scraping indiscriminado.

---

# **13\. GESTÃO FINANCEIRA E AQUISIÇÕES**

A aplicação já possui áreas destinadas a finanças, próximas aquisições e preços.

A evolução deve manter essas funcionalidades simples e integradas ao acervo.

## **13.1. Aquisições**

Permitir organizar livros desejados segundo:

* Prioridade.  
* Faixa de preço.  
* Autor.  
* Série.  
* Categoria.  
* Motivo da aquisição.  
* Disponibilidade.  
* Urgência ou interesse.

## **13.2. Histórico financeiro**

Permitir registrar:

* Preço pago.  
* Data.  
* Loja.  
* Frete.  
* Desconto.  
* Forma de aquisição.  
* Estado do exemplar, se pertinente.

## **13.3. Comparação de preços**

Quando houver fonte confiável, apresentar:

* Loja.  
* Preço.  
* Frete, quando disponível.  
* Data da consulta.  
* Link de origem.  
* Disponibilidade, quando confirmada.

Não exibir como atual um preço antigo sem indicar a data.

## **13.4. Alertas de preço**

Uma possível evolução é monitorar preços de obras desejadas.

Entretanto, isso deve depender de serviços, APIs ou fontes cujo uso seja permitido.

Não implementar raspagem indiscriminada de lojas.

---

# **14\. EXPERIÊNCIA MOBILE E PWA**

A aplicação deve funcionar muito bem em dispositivos móveis, independentemente da implementação de PWA.

## **14.1. Responsividade**

Testar, no mínimo:

* 320 px.  
* 360 px.  
* 390 px.  
* 768 px.  
* 1024 px.  
* 1440 px.

Avaliar:

* Navegação.  
* Busca.  
* Tabelas.  
* Modais.  
* Drawers.  
* Cards.  
* Formulários.  
* Gráficos.  
* Botões.  
* Espaçamentos.

Evitar rolagem horizontal da página inteira.

## **14.2. PWA**

Avaliar posteriormente:

* Web App Manifest.  
* Ícones.  
* Instalação.  
* Service Worker.  
* Estratégias de cache.  
* Página offline.  
* Atualização de versão.

A implementação de PWA não equivale a sincronização entre dispositivos.

O agente não deve anunciar sincronização ou backup remoto apenas porque a aplicação pode ser instalada.

---

# **15\. SINCRONIZAÇÃO ENTRE DISPOSITIVOS**

A ausência de sincronização é uma limitação relevante, mas sua correção exige uma decisão arquitetural e de privacidade.

## **15.1. Diretriz**

Não introduzir sincronização remota implicitamente.

A aplicação deverá continuar funcionando localmente.

Antes de implementar sincronização, apresentar uma proposta técnica que contemple:

* Serviço de autenticação.  
* Banco remoto.  
* Identificação do usuário.  
* Criptografia em trânsito.  
* Proteção das informações armazenadas.  
* Política de conflitos.  
* Exclusão e recuperação.  
* Backup remoto.  
* Tratamento de falhas de rede.  
* Funcionamento offline.  
* Controle de concorrência.  
* Custos operacionais.  
* Política de privacidade.

## **15.2. Estratégia de sincronização**

O modelo deverá considerar alterações feitas em dispositivos diferentes.

Não assumir que a última gravação sempre deve vencer.

O usuário deve ter condições de identificar e resolver conflitos quando não houver regra segura de resolução automática.

## **15.3. Critérios de aceite**

* O sistema local funciona mesmo sem conexão.  
* Falhas de rede não removem dados locais.  
* Conflitos não são descartados silenciosamente.  
* O usuário entende quais dados estão sincronizados.  
* O mecanismo de sincronização possui testes específicos.

---

# **16\. PERFORMANCE**

A aplicação deve ser rápida e permanecer responsiva à medida que o acervo cresce.

A auditoria encontrou um HTML compilado de aproximadamente 1,4 MB. Esse tamanho, isoladamente, não comprova um problema de desempenho.

É necessário medir antes de otimizar.

## **16.1. Indicadores**

Utilizar Core Web Vitals como referência:

* LCP: até 2,5 segundos.  
* INP: até 200 milissegundos.  
* CLS: até 0,1.

Essas métricas devem ser avaliadas nas condições de teste apropriadas.

## **16.2. Medidas recomendadas**

* Evitar renderizações desnecessárias.  
* Otimizar consultas e filtros.  
* Reduzir trabalho síncrono na thread principal.  
* Implementar carregamento progressivo de conteúdo pesado.  
* Evitar carregar anexos desnecessariamente.  
* Preservar paginação.  
* Avaliar virtualização de listas somente quando necessário.  
* Otimizar imagens.  
* Monitorar o custo de inicialização do dashboard.

## **16.3. Regra**

Não otimizar por intuição.

Identificar o gargalo, medir, modificar e comparar.

---

# **17\. TESTES, QUALIDADE E CI/CD**

A automação de qualidade é uma das prioridades da evolução.

## **17.1. Estado identificado**

O projeto possui uma suíte considerável em `tools/qa/tudo.py`, com verificações de catálogo, armazenamento, interface, filtros, anexos, temas, acessibilidade e outros comportamentos.

A documentação informa que a execução completa pode levar aproximadamente 35 minutos e que os testes utilizam Chromium.

A auditoria também identificou que o workflow de publicação não executa a suíte completa antes de publicar.

## **17.2. Pipeline recomendado**

Separar testes conforme custo e finalidade.

**Nível 1 — validação rápida**

Executar em cada alteração e pull request:

* Sintaxe.  
* Build.  
* Validação de arquivos.  
* Validação do catálogo.  
* Testes unitários rápidos.  
* Verificação de imports.  
* Verificação de assets.

**Nível 2 — testes funcionais**

Executar testes de:

* Inicialização.  
* Busca.  
* Filtros.  
* Paginação.  
* Formulários.  
* Armazenamento.  
* Backup.  
* Importação.  
* Restauração.  
* Anexos.  
* Navegação.  
* Temas.

**Nível 3 — testes completos**

Executar a suíte de regressão integral.

**Nível 4 — acessibilidade e compatibilidade**

Avaliar:

* Contraste.  
* Navegação por teclado.  
* Leitores de tela.  
* Responsividade.  
* Browsers adicionais.  
* Movimento reduzido.  
* Alvos de toque.

## **17.3. Integração contínua**

Modificar o workflow de publicação para que a publicação dependa da conclusão dos testes essenciais.

A publicação não deve ocorrer se o build ou os testes críticos falharem.

A suíte completa pode ser executada em um job próprio, respeitando o tempo de execução.

Considerar cache de dependências e divisão de testes para reduzir o tempo de feedback.

## **17.4. Navegadores**

Não limitar permanentemente a validação ao Chromium.

Avaliar pelo menos:

* Chromium.  
* Firefox.  
* WebKit.

Nem todo teste precisa ser executado em todos os navegadores, mas as funcionalidades essenciais precisam ter cobertura multiplataforma.

## **17.5. Testes de regressão de dados**

Toda mudança no armazenamento deve conter testes para:

* Dados válidos.  
* Dados incompletos.  
* Dados antigos.  
* Duplicatas.  
* Registros sem ISBN.  
* Anexos.  
* Migrações.  
* Backup.  
* Restauração.  
* Falhas de persistência.

## **17.6. Critérios de publicação**

Uma versão só pode ser publicada quando:

* O build for concluído.  
* Os testes obrigatórios passarem.  
* Não houver erro crítico conhecido.  
* Os dados forem preservados.  
* A documentação estiver atualizada.  
* A versão gerada corresponder ao código-fonte validado.

---

# **18\. SEGURANÇA E PRIVACIDADE**

A aplicação possui uma característica valiosa: boa parte dos dados pessoais permanece no navegador do usuário.

Essa característica deve ser preservada sempre que possível.

## **18.1. Dados públicos e privados**

O repositório e o dashboard publicado podem expor informações bibliográficas.

Informações privadas, como notas pessoais, anotações e histórico detalhado, não devem ser incorporadas acidentalmente aos artefatos públicos.

O uso de `noindex` não constitui mecanismo de autenticação ou controle de acesso.

## **18.2. Regras**

* Não incluir notas pessoais na compilação pública.  
* Não incluir dados privados em arquivos versionados.  
* Não incluir backups em commits.  
* Não registrar informações pessoais desnecessárias em logs.  
* Não transmitir dados para terceiros sem necessidade e transparência.  
* Validar arquivos importados.  
* Escapar conteúdo apresentado na interface.  
* Evitar injeção de HTML.  
* Tratar conteúdo externo como não confiável.  
* Usar HTTPS em integrações remotas.  
* Manter dependências atualizadas e justificadas.

## **18.3. Protótipo Next.js abandonado**

Não recuperar ou reutilizar automaticamente o protótipo em `referencias/prototipo-nextjs`.

Antes de qualquer aproveitamento:

* Verificar dependências.  
* Verificar vulnerabilidades.  
* Verificar banco e arquivos locais.  
* Confirmar se existe código útil.  
* Identificar possíveis riscos de exposição de dados.

O protótipo não deve se tornar parte da aplicação sem uma decisão arquitetural explícita.

---

# **19\. ORGANIZAÇÃO DA DOCUMENTAÇÃO DO PROJETO**

A documentação atual deve ser revisada para reduzir duplicações e facilitar a manutenção.

O `README.md` e o `ROTEIRO.md` são extensos e misturam informações operacionais, histórico e planejamento.

Proposta de organização:

**README.md**

* Visão geral.  
* Funcionalidades.  
* Requisitos.  
* Instalação e execução.  
* Atualização.  
* Build.  
* Testes.  
* Estrutura do projeto.  
* Privacidade.  
* Backup.

**docs/ARQUITETURA.md**

* Arquitetura.  
* Fluxo dos dados.  
* Módulos.  
* Persistência.  
* Modelo de dados.  
* Integrações.

**docs/UX\_UI.md**

* Princípios de design.  
* Design tokens.  
* Componentes.  
* Navegação.  
* Responsividade.  
* Acessibilidade.

**docs/DADOS\_E\_BACKUP.md**

* Estrutura de dados.  
* Identificadores.  
* Migrações.  
* Backup.  
* Restauração.  
* Recuperação.

**docs/ROADMAP.md**

* Prioridades.  
* Backlog.  
* Funcionalidades planejadas.  
* Dependências.  
* Critérios de conclusão.

**CHANGELOG.md**

* Mudanças por versão.  
* Correções.  
* Melhorias.  
* Alterações incompatíveis.

Não apagar conteúdo histórico útil sem avaliar sua relevância.

A documentação deve possuir uma única fonte oficial para cada tipo de informação.

---

# **20\. ROADMAP DE IMPLEMENTAÇÃO**

A execução deve ocorrer por fases, com validação ao final de cada uma.

Não iniciar todas as fases em paralelo.

## **FASE 0 — Reconhecimento e linha de base**

**Prioridade: obrigatória**

Objetivos:

* Confirmar estado atual do repositório.  
* Mapear dados e dependências.  
* Identificar funcionalidades existentes.  
* Executar QA.  
* Registrar falhas pré-existentes.  
* Verificar arquivos gerados.  
* Identificar riscos para os dados.

Entregáveis:

* Diagnóstico atualizado.  
* Mapa de arquitetura.  
* Relatório de testes.  
* Plano de implementação ajustado.

Critério de conclusão:

O agente consegue explicar como os dados entram, são processados, armazenados, exibidos e exportados.

## **FASE 1 — Integridade e confiabilidade**

**Prioridade: P0 — máxima**

Objetivos:

1. Identificadores persistentes.  
2. Versionamento da estrutura de dados.  
3. Estratégia de migração.  
4. Backup seguro.  
5. Restauração com validação.  
6. Auditoria de qualidade do catálogo.  
7. Tratamento de concorrência entre abas.  
8. Testes de regressão.

Critérios de conclusão:

* Nenhum registro existente é perdido.  
* Identificadores são estáveis.  
* Migrações podem ser repetidas ou interrompidas de forma segura.  
* Backup e restauração são verificáveis.  
* A aplicação informa falhas relevantes.

## **FASE 2 — Persistência e arquitetura**

**Prioridade: P0 — máxima**

Objetivos:

* Isolar persistência da interface.  
* Avaliar e implementar IndexedDB como armazenamento estruturado principal.  
* Preservar compatibilidade.  
* Tratar limites de armazenamento.  
* Implementar transações.  
* Revisar anexos.  
* Criar camada de serviços.

Critérios de conclusão:

* A interface não manipula diretamente a estrutura interna do banco.  
* A migração preserva os dados.  
* O funcionamento continua local-first.  
* A aplicação permanece estável após atualização e reinicialização.

## **FASE 3 — CI/CD e qualidade**

**Prioridade: P0 — máxima**

Objetivos:

* Criar níveis de testes.  
* Executar testes críticos em pull requests.  
* Integrar validação ao workflow de publicação.  
* Expandir testes de acessibilidade.  
* Avaliar compatibilidade com outros navegadores.

Critérios de conclusão:

* Build inválido não é publicado.  
* Testes críticos são obrigatórios.  
* O histórico de execução é verificável.

## **FASE 4 — UX/UI e acessibilidade**

**Prioridade: P1 — alta**

Objetivos:

* Corrigir combobox.  
* Corrigir tabs.  
* Revisar foco e teclado.  
* Melhorar gráficos acessíveis.  
* Refinar navegação.  
* Aprimorar filtros.  
* Criar ações em lote.  
* Implementar desfazer em operações apropriadas.  
* Revisar experiência mobile.  
* Melhorar a visão geral.

Critérios de conclusão:

* Todas as ações principais podem ser realizadas por teclado.  
* A navegação é consistente.  
* A interface funciona em telas pequenas.  
* Filtros e resultados são compreensíveis.  
* Não há regressões visuais ou funcionais.

## **FASE 5 — Experiência de leitura**

**Prioridade: P1 — alta**

Objetivos:

* Estados de leitura independentes da propriedade.  
* Sessões de leitura.  
* Progresso.  
* Histórico.  
* Metas opcionais.  
* Notas e observações.

Critérios de conclusão:

* O usuário pode registrar, atualizar e consultar leituras.  
* O histórico é preservado.  
* As informações são incluídas no backup.  
* A interface permite acompanhar progresso sem complexidade excessiva.

## **FASE 6 — Autores, séries e descoberta**

**Prioridade: P1/P2**

Objetivos:

* Perfil de autores.  
* Organização de séries.  
* Relações entre obras.  
* Recomendações contextualizadas.  
* Listas personalizadas.

Critérios de conclusão:

* Os relacionamentos são consistentes.  
* As recomendações possuem justificativas.  
* O sistema não cria relações bibliográficas sem evidência.

## **FASE 7 — Recursos avançados**

**Prioridade: P2 — estratégica**

Avaliar:

* Enriquecimento bibliográfico por APIs.  
* PWA.  
* Sincronização entre dispositivos.  
* Alertas de preço.  
* Estatísticas avançadas.  
* Exportações ampliadas.  
* Integrações externas.

Cada recurso deverá ser precedido por uma análise de custo, privacidade, manutenção e benefício.

---

# **21\. BACKLOG CONSOLIDADO**

| ID | Implementação | Prioridade | Dependência |
| ----- | ----- | ----- | ----- |
| BIB-001 | Auditoria atualizada do repositório | P0 | Nenhuma |
| BIB-002 | Identificadores persistentes | P0 | BIB-001 |
| BIB-003 | Versionamento do banco | P0 | BIB-002 |
| BIB-004 | Migrações seguras | P0 | BIB-003 |
| BIB-005 | Backup com versão e validação | P0 | BIB-003 |
| BIB-006 | Restauração com pré-visualização | P0 | BIB-005 |
| BIB-007 | Relatório de qualidade do catálogo | P0 | BIB-001 |
| BIB-008 | Tratamento de concorrência entre abas | P0 | BIB-002 |
| BIB-009 | Camada de persistência independente | P0 | BIB-001 |
| BIB-010 | Migração estruturada para IndexedDB | P0 | BIB-009 |
| BIB-011 | Testes críticos no CI | P0 | BIB-001 |
| BIB-012 | Bloqueio de publicação em caso de falha | P0 | BIB-011 |
| BIB-013 | Correção de combobox acessível | P1 | BIB-001 |
| BIB-014 | Correção de navegação por tabs | P1 | BIB-001 |
| BIB-015 | Alternativas textuais para gráficos | P1 | BIB-001 |
| BIB-016 | Refinamento da navegação | P1 | BIB-001 |
| BIB-017 | Filtros em níveis progressivos | P1 | BIB-016 |
| BIB-018 | Pesquisas e filtros salvos | P1 | BIB-017 |
| BIB-019 | Ações em lote | P1 | BIB-001 |
| BIB-020 | Desfazer operações | P1 | BIB-002 |
| BIB-021 | Melhoria da visão geral | P1 | BIB-016 |
| BIB-022 | Estados de leitura | P1 | BIB-002 |
| BIB-023 | Sessões de leitura | P1 | BIB-022 |
| BIB-024 | Histórico de leitura | P1 | BIB-023 |
| BIB-025 | Metas de leitura | P2 | BIB-023 |
| BIB-026 | Notas e observações | P1 | BIB-022 |
| BIB-027 | Perfil de autores | P2 | BIB-002 |
| BIB-028 | Organização de séries | P2 | BIB-002 |
| BIB-029 | Recomendações contextualizadas | P2 | BIB-027 |
| BIB-030 | Coleções personalizadas | P2 | BIB-002 |
| BIB-031 | Enriquecimento bibliográfico | P2 | BIB-002 |
| BIB-032 | PWA | P2 | BIB-001 |
| BIB-033 | Proposta de sincronização | P2 | BIB-002 |
| BIB-034 | Monitoramento de preços | P2 | BIB-033 não obrigatório |
| BIB-035 | Revisão e reorganização da documentação | P1 | BIB-001 |

A prioridade poderá ser ajustada depois da Fase 0, desde que o agente justifique a mudança.

---

# **22\. CRITÉRIOS GERAIS DE ACEITE**

Toda implementação deve ser avaliada por estes critérios.

## **Funcionalidade**

* A funcionalidade faz o que foi especificado.  
* Os estados possíveis estão cobertos.  
* Erros são tratados.  
* Não há regressão de funcionalidades existentes.

## **Dados**

* Nenhum dado antigo é perdido.  
* Alterações são persistidas corretamente.  
* Migrações são seguras.  
* Backup e recuperação funcionam.  
* Relações entre registros permanecem válidas.

## **UX/UI**

* A interação é clara.  
* A hierarquia visual é consistente.  
* A operação é compreensível.  
* Os feedbacks são adequados.  
* O usuário não precisa memorizar informações desnecessárias.

## **Acessibilidade**

* Navegação por teclado funcional.  
* Foco visível.  
* Semântica correta.  
* Rótulos acessíveis.  
* Contraste adequado.  
* Estados compreensíveis por tecnologias assistivas.

## **Responsividade**

* Funciona em telas pequenas e grandes.  
* Não há elementos essenciais inacessíveis.  
* Formulários e tabelas são utilizáveis.  
* Não há sobreposição de conteúdo.

## **Performance**

* Não há regressões perceptíveis.  
* Consultas e renderizações são eficientes.  
* Métricas são medidas quando pertinente.

## **Manutenção**

* Código modular.  
* Nomenclatura consistente.  
* Documentação atualizada.  
* Testes automatizados.  
* Dependências justificadas.

---

# **23\. DIRETRIZES DE EXECUÇÃO PARA O AGENTE**

Estas instruções são obrigatórias durante toda a atuação.

## **23.1. Antes de codificar**

Não comece implementando diretamente a primeira ideia que parecer conveniente.

Primeiro:

1. Leia os arquivos relevantes.  
2. Identifique a lógica atual.  
3. Verifique dependências.  
4. Identifique efeitos colaterais.  
5. Confira os testes.  
6. Registre o estado inicial.

## **23.2. Durante a implementação**

* Faça alterações pequenas.  
* Evite duplicação.  
* Reutilize componentes existentes.  
* Não crie dependências sem justificativa.  
* Preserve funcionalidades.  
* Não altere dados manualmente por conveniência.  
* Não remova recursos sem autorização.  
* Não ignore erros de testes.  
* Não esconda problemas com exceções genéricas.  
* Não substitua conteúdo real por dados fictícios.  
* Não preencha metadados sem fonte confiável.

## **23.3. Ao modificar o armazenamento**

Antes de alterar qualquer estrutura persistente:

1. Identifique o formato atual.  
2. Faça uma cópia de segurança.  
3. Defina a nova estrutura.  
4. Implemente migração.  
5. Teste dados antigos.  
6. Teste dados incompletos.  
7. Teste falhas.  
8. Teste restauração.  
9. Compare quantidades e relacionamentos.  
10. Documente a mudança.

## **23.4. Ao modificar a interface**

Verifique:

* Desktop.  
* Mobile.  
* Tema claro.  
* Tema escuro.  
* Temas literários.  
* Teclado.  
* Foco.  
* Estados vazios.  
* Estados de erro.  
* Mensagens de sucesso.  
* Contraste.

Não considerar uma tela concluída apenas porque está visualmente agradável.

## **23.5. Ao concluir cada tarefa**

Apresentar um relatório contendo:

**1\. Implementação**  
O que foi alterado.

**2\. Arquivos**  
Quais arquivos foram modificados ou criados.

**3\. Justificativa**  
Qual problema foi resolvido e por quê.

**4\. Testes**  
Quais testes foram executados e seus resultados.

**5\. Integridade**  
Se houve alterações no modelo de dados e como sua segurança foi verificada.

**6\. Pendências**  
O que não foi realizado e por quê.

**7\. Próxima etapa**  
Qual tarefa tem maior prioridade e quais dependências possui.

Não declarar uma tarefa concluída quando os testes necessários não foram executados.

---

# **24\. O QUE NÃO FAZER**

As seguintes práticas são expressamente desencorajadas:

1. Reescrever toda a aplicação em outro framework sem necessidade comprovada.  
2. Recuperar o protótipo Next.js abandonado sem auditoria.  
3. Migrar o banco sem backup e mecanismo de rollback.  
4. Utilizar título e autor como identificadores únicos.  
5. Implementar sincronização remota sem definir privacidade e conflitos.  
6. Adicionar bibliotecas pesadas para funcionalidades simples.  
7. Criar dashboards excessivamente carregados.  
8. Adicionar gráficos sem utilidade para o usuário.  
9. Adicionar temas sem validação de acessibilidade.  
10. Remover funcionalidades para simplificar a implementação sem autorização.  
11. Fazer scraping de sites de forma indiscriminada.  
12. Sobrescrever metadados manuais com informações externas sem confirmação.  
13. Incluir anotações pessoais em artefatos públicos.  
14. Considerar `noindex` como mecanismo de segurança.  
15. Ignorar falhas de testes.  
16. Declarar sucesso sem validação.  
17. Modificar diretamente o HTML compilado em vez de alterar as fontes correspondentes.

---

# **25\. RESULTADO FINAL ESPERADO**

A evolução deverá produzir um sistema com as seguintes características:

**Confiável:** os dados pessoais são preservados, identificados e recuperáveis.

**Organizado:** obras, edições, exemplares, autores, séries e leituras possuem relacionamentos consistentes.

**Intuitivo:** as principais operações são simples e rápidas.

**Acessível:** a aplicação é utilizável por teclado e tecnologias assistivas.

**Responsivo:** a experiência é consistente em computadores e dispositivos móveis.

**Personalizado:** mantém uma identidade literária própria sem comprometer a usabilidade.

**Inteligente:** auxilia na descoberta de obras, na organização do acervo e no acompanhamento das leituras.

**Sustentável:** possui código modular, documentação clara, testes automatizados e processo de publicação confiável.

**Privado:** mantém o controle dos dados pessoais com o usuário e não expõe informações privadas por acidente.

**Expansível:** permite incorporar novos recursos sem exigir uma reescrita estrutural.

---

# **26\. PRIMEIRA TAREFA DO AGENTE**

Ao receber esta especificação, **não implemente imediatamente todas as funcionalidades.**

Sua primeira tarefa é executar a FASE 0\.

Entregue um relatório com:

1. Estado atual do repositório.  
2. Arquitetura real identificada.  
3. Fluxo de dados.  
4. Modelo de armazenamento atual.  
5. Pontos da auditoria que continuam válidos.  
6. Problemas que foram corrigidos desde a auditoria.  
7. Riscos adicionais identificados.  
8. Resultado da suíte de testes.  
9. Dependências entre as tarefas do backlog.  
10. Plano técnico da Fase 1\.

Depois dessa análise, prossiga para a implementação de BIB-002 a BIB-012, respeitando as dependências e os critérios de aceite.

**Não solicite autorização para cada pequena decisão técnica reversível.** Tome decisões coerentes com esta especificação, documente-as e prossiga.

Entretanto, não execute mudanças irreversíveis, não exclua dados, não introduza serviços externos pagos e não altere a política de privacidade sem apresentar previamente a justificativa e a proposta correspondente.

---

# **27\. PRINCÍPIO FINAL**

A Biblioteca não precisa se tornar uma aplicação maior para se tornar melhor.

A meta é construir uma ferramenta pessoal de referência: sólida na gestão dos dados, agradável na utilização, rica em possibilidades de descoberta e simples o suficiente para continuar sendo útil durante muitos anos.

**Priorize integridade, clareza, consistência e utilidade.**

A qualidade da evolução deve ser medida pelo quanto a aplicação se torna mais confiável e agradável de usar — não pela quantidade de código escrito ou funcionalidades adicionadas.

