"use client";

import * as React from "react";
import { motion } from "framer-motion";
import { CalendarClock, Lightbulb, ShoppingCart, Sparkles, TrendingDown, TrendingUp } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { ScoreRing, Sparkline, Vazio } from "./charts";
import { DIF_LABEL, TIPO_LABEL, fmtBRL2, melhorLoja, mesLabel, var30d } from "@/lib/dashboard";
import type { BookRecord } from "@/lib/types";

export function RecommendationsTab({
  books,
  planejadosIds,
  onPlanejar,
}: {
  books: BookRecord[];
  planejadosIds: Set<string>;
  onPlanejar: (b: BookRecord) => void;
}) {
  const recomendados = React.useMemo(
    () =>
      books
        .filter((b) => b.status === "wishlist" && b.matchScore != null)
        .sort((a, b) => (b.matchScore ?? 0) - (a.matchScore ?? 0))
        .slice(0, 24),
    [books],
  );

  if (!recomendados.length) {
    return (
      <Vazio
        mensagem="Sem recomendações para os filtros atuais. A justa de livros aguarda novas trilhas…"
        icone={Sparkles}
      />
    );
  }

  return (
    <div>
      <p className="mb-4 max-w-2xl text-xs text-muted-foreground">
        Ranking por <strong className="text-foreground">score de afinidade</strong> — calculado a partir das suas
        prioridades (#top), trilhas, autores e eixos mais lidos, nível de dificuldade e disponibilidade de edição
        brasileira.
      </p>
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3">
        {recomendados.map((b, i) => (
          <RecCard key={b.id} b={b} indice={i} planejado={planejadosIds.has(b.id)} onPlanejar={onPlanejar} />
        ))}
      </div>
    </div>
  );
}

function RecCard({
  b,
  indice,
  planejado,
  onPlanejar,
}: {
  b: BookRecord;
  indice: number;
  planejado: boolean;
  onPlanejar: (b: BookRecord) => void;
}) {
  const loja = melhorLoja(b);
  const v30 = var30d(b);

  return (
    <motion.div
      initial={{ opacity: 0, y: 18 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: Math.min(indice * 0.04, 0.4) }}
      className="group flex h-full flex-col rounded-xl border border-border/60 bg-card p-4 shadow-sm transition-all duration-300 hover:-translate-y-0.5 hover:shadow-md"
    >
      <div className="flex items-start gap-3">
        <ScoreRing score={b.matchScore ?? 0} />
        <div className="min-w-0 flex-1">
          <p className="truncate font-semibold leading-tight" title={b.titulo}>
            {b.titulo}
          </p>
          <p className="truncate text-xs text-muted-foreground">{b.autor}</p>
        </div>
      </div>

      <div className="mt-2.5 flex flex-wrap gap-1">
        <Badge variant="outline" className="max-w-full truncate px-1.5 text-[10px] text-muted-foreground">
          {b.eixo}
        </Badge>
        <Badge variant="secondary" className="px-1.5 text-[10px]">{TIPO_LABEL[b.tipo]}</Badge>
        <Badge variant="secondary" className="px-1.5 text-[10px]">{DIF_LABEL[b.dif]}</Badge>
        {b.trilha && (
          <Badge className="px-1.5 text-[10px]" style={{ background: "color-mix(in oklch, var(--chart-4) 18%, transparent)", color: "var(--accent-foreground)" }}>
            <Sparkles className="mr-0.5 h-2.5 w-2.5" />
            {b.trilha}
          </Badge>
        )}
      </div>

      <ul className="mt-3 flex-1 space-y-1">
        {(b.motivos ?? []).slice(0, 3).map((m, i) => (
          <li key={i} className="flex items-start gap-1.5 text-[11px] leading-snug text-muted-foreground">
            <Lightbulb className="mt-0.5 h-3 w-3 shrink-0 text-chart-1" />
            <span>{m}</span>
          </li>
        ))}
      </ul>

      <div className="mt-3 flex items-center justify-between gap-2 border-t border-border/60 pt-3">
        <div className="min-w-0">
          {loja && (
            <p className="truncate text-[10px] text-muted-foreground" title={`${loja.nome} · ${loja.tipo}`}>
              melhor: {loja.nome}
            </p>
          )}
          <p className="flex items-baseline gap-1.5">
            <span className="text-sm font-bold tabular">{fmtBRL2(b.precoAtual ?? 0)}</span>
            {v30 != null && Math.abs(v30) >= 0.1 && (
              <span
                className="inline-flex items-center text-[10px] font-semibold tabular"
                style={{ color: v30 < 0 ? "var(--success)" : "var(--destructive)" }}
              >
                {v30 < 0 ? <TrendingDown className="h-3 w-3" /> : <TrendingUp className="h-3 w-3" />}
                {Math.abs(v30).toFixed(0)}%
              </span>
            )}
          </p>
        </div>
        {b.historico && <Sparkline valores={b.historico} largura={72} altura={24} cor="var(--chart-2)" />}
      </div>

      <Popover>
        <PopoverTrigger asChild>
          <Button variant="outline" size="sm" className="mt-2 h-8 w-full justify-center gap-1.5 text-xs">
            Ver lojas ({b.lojas?.length ?? 0})
          </Button>
        </PopoverTrigger>
        <PopoverContent align="center" className="w-56 p-2">
          <div className="space-y-1">
            {[...(b.lojas ?? [])]
              .sort((a, c) => a.preco - c.preco)
              .map((l) => (
                <div key={l.nome} className="flex items-center justify-between gap-2 rounded-md px-2 py-1 text-xs hover:bg-muted">
                  <span className="truncate text-muted-foreground">{l.nome}</span>
                  <span className="font-semibold tabular">{fmtBRL2(l.preco)}</span>
                </div>
              ))}
          </div>
        </PopoverContent>
      </Popover>

      {planejado ? (
        <Badge className="mt-2 h-8 w-full justify-center gap-1.5 text-xs" variant="secondary">
          <CalendarClock className="h-3.5 w-3.5" />
          Planejado · {mesLabel(b.planejadoMes ?? "2026-12")}
        </Badge>
      ) : (
        <Button
          size="sm"
          className="mt-2 h-8 w-full justify-center gap-1.5 text-xs"
          onClick={() => onPlanejar(b)}
        >
          <ShoppingCart className="h-3.5 w-3.5" />
          Planejar aquisição
        </Button>
      )}
    </motion.div>
  );
}
