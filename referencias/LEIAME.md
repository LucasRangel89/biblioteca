# Referências guardadas (não são fonte ativa)

Este diretório é **arquivo de consulta/inspiração**. Nenhum script do painel, workflow ou teste ativo importa
`referencias/`. Nada aqui deve ser executado para gerar o painel, e nada aqui é fonte de dados do usuário.

## O que há aqui

| Caminho | O que é | Decisão desta revisão (12/11/2026) |
| --- | --- | --- |
| `catalogo-v3-enviado-2026-11-10.md` | A “versão 3” do catálogo enviada pelo usuário, de onde vieram as camadas e as trilhas | Histórico. A fonte ativa das trilhas é `catalogo/trilhas.md`; a do catálogo é `catalogo/Biblioteca_Lucas_Catalogo_Mestre.md` |
| `deepseek_html_20261110_d18471.html` | Painel de inspiração visual/funcional | Inspiração. Não é o painel publicado e não deve ser embutido no build |
| `prototipo-nextjs/` | Protótipo abandonado de outro desenho (Next.js/Prisma) | Lixo operacional, não risco de vazamento: o schema só tem `User`/`Post`, o banco de exemplo está vazio e o parser gera dados fictícios. Não recuperar, não migrar, não executar |

## Regras

- **Não executar** `prototipo-nextjs` nem seus scripts para atualizar a biblioteca.
- **Não importar** nada deste diretório em `tools/`, `src/` ou `.github/workflows/`.
- **Não usar** dados fictícios do protótipo como se fossem livros reais.
- Se um dia for remover fisicamente este diretório, fazer em PR próprio, conferindo antes que nada ativo o referencia;
  o histórico do Git preserva o conteúdo.

## Por que manter por enquanto

O catálogo v3 registra a origem de decisões já aprovadas (camadas e trilhas), e o HTML de inspiração ajuda a comparar
ideias sem reabrir o protótipo. O custo é ~1,0 MB de arquivos parados; o risco é alguém executá-los por engano. Este
LEIAME existe para tornar essa fronteira explícita.
