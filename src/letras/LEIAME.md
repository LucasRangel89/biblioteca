# Letras dos temas

As letras que os temas do painel usam nos títulos e na sinopse. `tools/build.py` põe cada arquivo desta pasta dentro
do painel (`Biblioteca_Lucas_Dashboard.html`), para o tema ficar igual em qualquer aparelho — sem depender das fontes
instaladas e sem buscar nada na internet.

| Tema | Letra | Arquivos | De quem é |
| --- | --- | --- | --- |
| Lovecraft | IM Fell English | `im-fell-english-latin-400-normal.woff2` | Igino Marini, 2007 — recriação dos tipos de John Fell, do século XVII |
| Sherlock Holmes | Libre Baskerville | `libre-baskerville-latin-400-normal.woff2`, `…-600-normal.woff2` | The Libre Baskerville Project Authors (Impallari Type), 2012 |
| Moby Dick | Old Standard TT | `old-standard-tt-latin-400-normal.woff2`, `…-700-normal.woff2` | The Old Standard Project Authors (Alexey Kryukov), 2011 |

As três são **fontes livres**, sob a SIL Open Font License 1.1, que permite usar, copiar e embutir, desde que a
licença acompanhe a fonte e ela não seja vendida sozinha. O texto da licença de cada uma está aqui, em
`<letra>-LICENSE.txt`, com o aviso de direitos autorais do autor.

Os arquivos vieram do pacote `@fontsource/<letra>` (versão 5.3.0), que redistribui as fontes do Google Fonts. São
recortes só com o **alfabeto latino** — todas as letras e sinais do português —, para pesar pouco: os cinco arquivos
somam cerca de 150 KB e acrescentam uns 200 KB ao painel. Um sinal que a letra não tenha (o "ł" de Kołakowski, por
exemplo) é desenhado pela letra seguinte da lista do tema, que é uma letra do sistema.

## Para pôr outra letra

1. Copie para cá o arquivo `.woff2`, com o nome no padrão `familia-latin-peso-estilo.woff2`, e a licença, como
   `familia-LICENSE.txt`.
2. Acrescente a família em `FAMILIAS`, em `tools/build.py`.
3. Use o nome da família no começo de `--serif`, no bloco do tema em `src/styles.css`.
4. `python tools/build.py`. Ele reclama se a letra estiver na pasta e não no estilo, ou o contrário.

O teste `tools/qa/temas.py` confere que cada letra está no painel, idêntica ao arquivo, e que tem licença.
