# Biblioteca do Lucas — painel

Painel pessoal de biblioteca em **um único arquivo HTML**: `Biblioteca_Lucas_Dashboard.html`. Abra-o no navegador;
ele funciona sem internet e sem servidor. CSS, dados e scripts vão embutidos, e os dados do usuário ficam no
`localStorage` do navegador (chave `biblioteca-lucas:v1`).

## Estrutura

| Caminho | O que é |
| --- | --- |
| `Biblioteca_Lucas_Dashboard.html` | O painel pronto (gerado por `tools/build.py`; não edite à mão) |
| `catalogo/Biblioteca_Lucas_Catalogo_Mestre.md` | Catálogo Mestre: a fonte dos títulos, autores, marcadores e eixos |
| `src/index.html` | Esqueleto da página (o build injeta estilos, catálogo e scripts) |
| `src/styles.css` | Todos os estilos; temas claro e escuro por variáveis |
| `src/js/00-util.js` … `70-app.js` | Módulos, concatenados em ordem alfabética dentro de uma única função |
| `src/catalog.json` | Catálogo convertido: 644 linhas `[título, autor, tags, seção, eixo, observação]` (gerado) |
| `tools/build_catalog.py` | Lê o Catálogo Mestre e gera `src/catalog.json` (usa `parse_catalog.py` e `eixos.py`) |
| `tools/build.py` | Monta o HTML final e confere que não sobrou nenhuma referência externa |
| `tools/qa/` | Testes automatizados (Playwright) |

Módulos: `00-util` (datas, formatos) · `10-data` (livros, catálogo, exemplos, armazenamento) · `20-charts` (gráficos SVG) ·
`30-state` (filtros, período, contexto) · `40-panels` (indicadores e painéis de cada visão) · `50-table` (tabelas e CSV) ·
`60-drawer` (gaveta do livro, diálogos, cotações, backup) · `70-app` (navegação, filtros, inicialização).

## Reconstruir

Só precisa de Python 3 (testado com o 3.13); nenhuma biblioteca extra.

```bash
python tools/build_catalog.py   # só quando o Catálogo Mestre mudar
python tools/build.py           # gera Biblioteca_Lucas_Dashboard.html na raiz
```

Os caminhos são relativos ao repositório, então os comandos funcionam de qualquer pasta e em qualquer sistema.
Para converter outro arquivo de catálogo, aponte a variável de ambiente `CATALOGO` para ele.

## O que é real e o que é exemplo

- **Real (do catálogo):** títulos, autores, marcadores, eixos temáticos, a estante física (97 livros) e as recomendações.
- **Exemplo (gerado, semente fixa):** datas e valores de compra, e-books e audiolivros, leituras e notas, a lista de
  próximas aquisições e os históricos de preço. Tudo isso é marcado na interface e sai com “Limpar dados de exemplo”.
- **Preços:** o painel não consulta lojas. Cada preço é uma cotação registrada pelo usuário (há atalhos de busca por loja).

## Testes

```bash
pip install playwright pillow
python -m playwright install chromium   # no Linux, se faltarem bibliotecas: python -m playwright install-deps chromium
python tools/qa/tudo.py                 # ~10 min; termina com "TUDO CERTO"
python tools/qa/tudo.py foco a11y       # só alguns
```

Os testes abrem o HTML final por `file://` e fixam o relógio em 09/11/2026 (`relogio.py`), porque os dados de exemplo
são gerados a partir da data de hoje. Capturas de tela e registros vão para a pasta temporária do sistema
(`biblioteca-qa/`; o caminho aparece no fim da execução) ou para onde a variável `BIBLIOTECA_QA_TMP` indicar.
Só foram rodados no Chromium.

| Script | Cobre |
| --- | --- |
| `func3` … `func8` | Cotações, novo livro, limpar/restaurar exemplos, exportar/importar, períodos, filtros, CSV, dados corrompidos, rede de segurança |
| `valores`, `resto` | Leitura de valores digitados; excluir livro; período invertido; importação com registros ilegíveis |
| `limpo` | Painel só com o catálogo (sem exemplos): indicadores, legendas e estados vazios |
| `foco`, `a11y` | Foco e Tab nas camadas; ids duplicados, nomes acessíveis, rótulos, contraste AA nos dois temas |
| `varredura` | Clica em tudo, em todas as visões, nos dois temas e no celular, à procura de erros |
| `sandbox` | Página dentro de um iframe isolado (sem `localStorage`): funciona em memória |
| `medir3`, `tabs`, `largo` | Larguras de 2560 a 820 px: colunas das tabelas, quebras e estouros |
| `run1`, `run5` … `run13` | Capturas de tela para conferência visual (não entram no `tudo.py`) |
| `caminhos`, `relogio`, `shot`, `crop`, `msheet` | Apoio: caminhos, relógio fixo, capturas e recortes |
