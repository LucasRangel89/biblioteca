"use client";

import * as React from "react";
import { motion } from "framer-motion";
import {
  ArrowDown,
  ArrowDownUp,
  ArrowUp,
  LineChart as LineChartIcon,
  Store,
  Tag,
  TrendingDown,
} from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { ChartCard, CORES, PrecoChart, Sparkline, Vazio, type SeriePreco } from "./charts";
import { PRICE_MONTHS } from "@/lib/catalog-data";
import { fmtBRL2, fmtInt, melhorLoja, mesLabel, oportunidade, var30d, type RangeInfo } from "@/lib/dashboard";
import { cn } from "@/lib/utils";
import type { BookRecord } from "@/lib/types";

function MiniKpi({ rotulo, valor, icone: Icone, detalhe }: { rotulo: string; valor: string; icone: React.ElementType; detalhe?: string }) {
  return (
    <div className="flex items-center gap-3 rounded-xl border border-border/60 bg-card p-3 shadow-sm">
      <span
        className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg"
        style={{ background: "color-mix(in oklch, var(--chart-2) 15%, transparent)", color: "var(--chart-2)" }}
      >
        <Icone className="h-4 w-4" />
      </span>
      <div className="min-w-0">
        <p className="text-[11px] text-muted-foreground">{rotulo}</p>
        <p className="truncate text-base font-bold tabular">{valor}</p>
        {detalhe && <p className="truncate text-[10px] text-muted-foreground">{detalhe}</p>}
      </div>
    </div>
  );
}

function StatusBadge({ b }: { b: BookRecord }) {
  const { status, label } = oportunidade(b);
  const estilo: Record<string, { bg: string; fg: string }> = {
    comprar: { bg: "color-mix(in oklch, var(--success) 18%, transparent)", fg: "var(--success)" },
    promocao: { bg: "color-mix(in oklch, var(--chart-1) 18%, transparent)", fg: "var(--chart-1)" },
    aguardar: { bg: "var(--muted)", fg: "var(--muted-foreground)" },
  };
  const e = estilo[status];
  return (
    <Badge className="border-transparent px-2 text-[10px] font-semibold" style={{ background: e.bg, color: e.fg }}>
      {label}
    </Badge>
  );
}

type SortKey = "titulo" | "preco" | "var30" | "alvo";

export function PricesTab({ books, r }: { books: BookRecord[]; r: RangeInfo }) {
  const wishlist = React.useMemo(() => books.filter((b) => b.status === "wishlist" && b.historico), [books]);

  // livros com maiores quedas (para seleção inicial e chips)
  const quedas = React.useMemo(
    () =>
      [...wishlist]
        .sort((a, b) => (b.precoMedia12m ?? 0) - (b.precoAtual ?? 0) - ((a.precoMedia12m ?? 0) - (a.precoAtual ?? 0)))
        .slice(0, 12),
    [wishlist],
  );

  const [selecionados, setSelecionados] = React.useState<string[]>(() => quedas.slice(0, 3).map((b) => b.id));
  const [sortKey, setSortKey] = React.useState<SortKey>("var30");
  const [sortDesc, setSortDesc] = React.useState(false);
  const [pagina, setPagina] = React.useState(0);
  const POR_PAGINA = 10;

  React.useEffect(() => {
    setSelecionados((sel) => (sel.length ? sel : quedas.slice(0, 3).map((b) => b.id)));
  }, [quedas]);

  React.useEffect(() => setPagina(0), [books, sortKey, sortDesc]);

  const sliceStart = PRICE_MONTHS.length - r.priceMonths.length;

  const series: SeriePreco[] = React.useMemo(() => {
    const selecionadosLivros = selecionados
      .map((id) => wishlist.find((b) => b.id === id))
      .filter((b): b is BookRecord => !!b);
    const s = selecionadosLivros.map((b, i) => ({
      id: b.id,
      nome: b.titulo.length > 26 ? `${b.titulo.slice(0, 25)}…` : b.titulo,
      valores: (b.historico ?? []).slice(sliceStart),
      cor: CORES[i % CORES.length],
    }));
    if (wishlist.length) {
      const media = r.priceMonths.map((_, i) => {
        const vals = wishlist
          .map((b) => b.historico?.[sliceStart + i])
          .filter((v): v is number => typeof v === "number");
        return vals.length ? Math.round((vals.reduce((a, x) => a + x, 0) / vals.length) * 100) / 100 : null;
      });
      s.push({ id: "__media", nome: "Média da wishlist", valores: media, cor: "var(--muted-foreground)", destacada: true });
    }
    return s;
  }, [selecionados, wishlist, r.priceMonths, sliceStart]);

  const comprarAgora = wishlist.filter((b) => oportunidade(b).status === "comprar").length;
  const varMedia = wishlist.length
    ? wishlist.reduce((a, b) => a + (var30d(b) ?? 0), 0) / wishlist.length
    : 0;

  const ordenados = React.useMemo(() => {
    const arr = [...wishlist];
    switch (sortKey) {
      case "titulo":
        arr.sort((a, b) => a.titulo.localeCompare(b.titulo));
        break;
      case "preco":
        arr.sort((a, b) => (a.precoAtual ?? 0) - (b.precoAtual ?? 0));
        break;
      case "var30":
        arr.sort((a, b) => (var30d(a) ?? 0) - (var30d(b) ?? 0));
        break;
      case "alvo":
        arr.sort((a, b) => (a.precoAlvo ?? 0) - (b.precoAlvo ?? 0));
        break;
    }
    return sortDesc ? arr.reverse() : arr;
  }, [wishlist, sortKey, sortDesc]);

  const paginas = Math.max(1, Math.ceil(ordenados.length / POR_PAGINA));
  const visiveis = ordenados.slice(pagina * POR_PAGINA, (pagina + 1) * POR_PAGINA);

  const toggleSelecionado = (id: string) => {
    setSelecionados((sel) =>
      sel.includes(id) ? sel.filter((x) => x !== id) : sel.length >= 5 ? [...sel.slice(1), id] : [...sel, id],
    );
  };

  const headerSort = (key: SortKey, rotulo: string) => (
    <button
      type="button"
      onClick={() => {
        if (sortKey === key) setSortDesc((d) => !d);
        else {
          setSortKey(key);
          setSortDesc(false);
        }
      }}
      className="inline-flex items-center gap-1 text-[11px] font-semibold transition-colors hover:text-foreground"
    >
      {rotulo}
      {sortKey === key ? (
        sortDesc ? <ArrowDown className="h-3 w-3 text-primary" /> : <ArrowUp className="h-3 w-3 text-primary" />
      ) : (
        <ArrowDownUp className="h-3 w-3 opacity-40" />
      )}
    </button>
  );

  if (!wishlist.length) {
    return <Vazio mensagem="Nenhum título monitorado com os filtros atuais." icone={Tag} />;
  }

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
        <MiniKpi rotulo="Títulos monitorados" valor={fmtInt(wishlist.length)} icone={Tag} detalhe="wishlist com 12 meses de histórico" />
        <MiniKpi rotulo="Comprar agora" valor={fmtInt(comprarAgora)} icone={TrendingDown} detalhe="preço no alvo ou abaixo" />
        <MiniKpi
          rotulo="Variação média 30d"
          valor={`${varMedia > 0 ? "+" : ""}${varMedia.toFixed(1).replace(".", ",")}%`}
          icone={varMedia <= 0 ? TrendingDown : ArrowUp}
          detalhe="frente amarela = alta"
        />
        <MiniKpi
          rotulo="Janela de histórico"
          valor={`${r.priceMonths.length} ${r.priceMonths.length === 1 ? "mês" : "meses"}`}
          icone={LineChartIcon}
          detalhe={`${mesLabel(r.priceMonths[0])} – ${mesLabel(r.priceMonths[r.priceMonths.length - 1])}`}
        />
      </div>

      <ChartCard
        titulo="Evolução de preços online"
        descricao="Selecione até 5 títulos (maiores quedas em destaque) — a linha tracejada é a média da wishlist"
        atraso={0.05}
      >
        <div className="mb-3 flex flex-wrap gap-1.5">
          {quedas.map((b) => {
            const idxSel = selecionados.indexOf(b.id);
            const cor = idxSel >= 0 ? CORES[idxSel % CORES.length] : null;
            return (
              <button
                key={b.id}
                type="button"
                onClick={() => toggleSelecionado(b.id)}
                className={cn(
                  "inline-flex max-w-full items-center gap-1.5 rounded-full border px-2.5 py-1 text-[11px] font-medium transition-all",
                  cor ? "border-transparent text-foreground shadow-sm" : "border-border/70 text-muted-foreground hover:border-primary/40",
                )}
                style={cor ? { background: `color-mix(in oklch, ${cor} 14%, transparent)` } : undefined}
                title={b.titulo}
              >
                <span className="h-2 w-2 shrink-0 rounded-full" style={{ background: cor ?? "var(--muted-foreground)" }} />
                <span className="max-w-44 truncate">{b.titulo}</span>
                <span className="tabular opacity-70">{fmtBRL2(b.precoAtual ?? 0)}</span>
              </button>
            );
          })}
        </div>
        <PrecoChart meses={r.priceMonths} series={series} />
      </ChartCard>

      <div className="rounded-xl border border-border/60 bg-card shadow-sm">
        <div className="flex flex-wrap items-center justify-between gap-2 border-b border-border/60 bg-muted/40 px-4 py-2.5">
          <p className="text-xs font-semibold">Oportunidades de compra</p>
          <p className="text-[11px] text-muted-foreground">
            {fmtInt(ordenados.length)} títulos · ordenação por coluna
          </p>
        </div>
        <div className="scrollbar-thin overflow-x-auto">
          <table className="w-full min-w-[720px] text-sm">
            <thead>
              <tr className="border-b border-border/60 text-left text-muted-foreground">
                <th className="px-4 py-2">{headerSort("titulo", "Título")}</th>
                <th className="hidden px-3 py-2 md:table-cell">Melhor loja</th>
                <th className="px-3 py-2 text-right">{headerSort("preco", "Preço atual")}</th>
                <th className="px-3 py-2 text-right">{headerSort("var30", "Δ 30d")}</th>
                <th className="hidden px-3 py-2 text-right sm:table-cell">Mín. 12m</th>
                <th className="px-3 py-2 text-right">{headerSort("alvo", "Alvo")}</th>
                <th className="px-3 py-2">Status</th>
                <th className="hidden px-3 py-2 lg:table-cell">Tendência</th>
                <th className="px-3 py-2" />
              </tr>
            </thead>
            <tbody>
              {visiveis.map((b) => {
                const loja = melhorLoja(b);
                const v = var30d(b);
                const corIdx = selecionados.indexOf(b.id);
                return (
                  <motion.tr
                    key={b.id}
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="border-b border-border/40 transition-colors last:border-0 hover:bg-muted/30"
                  >
                    <td className="max-w-[220px] px-4 py-2.5">
                      <p className="truncate font-medium" title={b.titulo}>{b.titulo}</p>
                      <p className="truncate text-[11px] text-muted-foreground">{b.autor}</p>
                    </td>
                    <td className="hidden px-3 py-2.5 md:table-cell">
                      {loja && (
                        <span className="flex items-center gap-1.5 text-xs text-muted-foreground">
                          <Store className="h-3.5 w-3.5 shrink-0" style={{ color: loja.tipo === "usado" ? "var(--chart-5)" : loja.tipo === "ebook" ? "var(--chart-2)" : "var(--muted-foreground)" }} />
                          <span className="max-w-40 truncate">{loja.nome}</span>
                        </span>
                      )}
                    </td>
                    <td className="px-3 py-2.5 text-right font-semibold tabular">{fmtBRL2(b.precoAtual ?? 0)}</td>
                    <td className="px-3 py-2.5 text-right">
                      {v == null ? (
                        <span className="text-muted-foreground">—</span>
                      ) : (
                        <span
                          className="font-semibold tabular"
                          style={{ color: Math.abs(v) < 0.1 ? "var(--muted-foreground)" : v < 0 ? "var(--success)" : "var(--destructive)" }}
                        >
                          {v > 0 ? "+" : ""}
                          {v.toFixed(1).replace(".", ",")}%
                        </span>
                      )}
                    </td>
                    <td className="hidden px-3 py-2.5 text-right text-muted-foreground tabular sm:table-cell">
                      {fmtBRL2(b.precoMin12m ?? 0)}
                    </td>
                    <td className="px-3 py-2.5 text-right text-muted-foreground tabular">{fmtBRL2(b.precoAlvo ?? 0)}</td>
                    <td className="px-3 py-2.5"><StatusBadge b={b} /></td>
                    <td className="hidden px-3 py-2.5 lg:table-cell">
                      <Sparkline
                        valores={(b.historico ?? []).slice(sliceStart)}
                        largura={84}
                        altura={26}
                        cor={corIdx >= 0 ? CORES[corIdx % CORES.length] : "var(--chart-2)"}
                      />
                    </td>
                    <td className="px-3 py-2.5 text-right">
                      <Popover>
                        <PopoverTrigger asChild>
                          <Button variant="ghost" size="icon" className="h-7 w-7 text-muted-foreground" aria-label={`Comparar lojas de ${b.titulo}`}>
                            <Store className="h-4 w-4" />
                          </Button>
                        </PopoverTrigger>
                        <PopoverContent align="end" className="w-56 p-2">
                          <p className="truncate px-2 pb-1 text-xs font-semibold" title={b.titulo}>{b.titulo}</p>
                          {[...(b.lojas ?? [])]
                            .sort((a, c) => a.preco - c.preco)
                            .map((l) => (
                              <div key={l.nome} className="flex items-center justify-between gap-2 rounded-md px-2 py-1 text-xs hover:bg-muted">
                                <span className="truncate text-muted-foreground">{l.nome}</span>
                                <span className="font-semibold tabular">{fmtBRL2(l.preco)}</span>
                              </div>
                            ))}
                        </PopoverContent>
                      </Popover>
                    </td>
                  </motion.tr>
                );
              })}
            </tbody>
          </table>
        </div>
        <div className="flex items-center justify-between border-t border-border/60 px-4 py-2">
          <p className="text-[11px] text-muted-foreground">
            Página {pagina + 1} de {paginas}
          </p>
          <div className="flex gap-1">
            <Button variant="outline" size="sm" className="h-7" disabled={pagina === 0} onClick={() => setPagina((p) => p - 1)}>
              Anterior
            </Button>
            <Button variant="outline" size="sm" className="h-7" disabled={pagina >= paginas - 1} onClick={() => setPagina((p) => p + 1)}>
              Próxima
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
