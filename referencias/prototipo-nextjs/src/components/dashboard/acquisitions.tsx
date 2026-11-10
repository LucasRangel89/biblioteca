"use client";

import * as React from "react";
import { motion } from "framer-motion";
import {
  Bar,
  BarChart,
  CartesianGrid,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { CalendarPlus, PackageOpen, PiggyBank, Star, Trash2, TrendingDown } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ChartCard, CORES, ORCAMENTO_REF, TooltipComp, Vazio } from "./charts";
import { fmtBRL, fmtBRL2, fmtInt, melhorLoja, mesLabel, mesLabelLongo } from "@/lib/dashboard";
import type { BookRecord } from "@/lib/types";

export interface ItemPlano {
  b: BookRecord;
  mes: string;
  preco: number;
  extra: boolean;
}

function MiniKpi({ rotulo, valor, icone: Icone, detalhe }: { rotulo: string; valor: string; icone: React.ElementType; detalhe?: string }) {
  return (
    <div className="flex items-center gap-3 rounded-xl border border-border/60 bg-card p-3 shadow-sm">
      <span
        className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg"
        style={{ background: "color-mix(in oklch, var(--primary) 12%, transparent)", color: "var(--primary)" }}
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

export function AcquisitionsTab({
  itens,
  onRemover,
}: {
  itens: ItemPlano[];
  onRemover: (id: string) => void;
}) {
  const porMes = React.useMemo(() => {
    const m = new Map<string, ItemPlano[]>();
    for (const it of itens) {
      if (!m.has(it.mes)) m.set(it.mes, []);
      m.get(it.mes)!.push(it);
    }
    return [...m.entries()].sort(([a], [b]) => a.localeCompare(b));
  }, [itens]);

  const chartData = React.useMemo(
    () =>
      porMes.map(([mes, lista]) => ({
        mes,
        total: Math.round(lista.reduce((a, it) => a + it.preco, 0) * 100) / 100,
      })),
    [porMes],
  );

  const total = itens.reduce((a, it) => a + it.preco, 0);
  const economia = itens.reduce(
    (a, it) => a + Math.max(0, (it.b.precoMedia12m ?? 0) - it.preco),
    0,
  );
  const mesMaisCaro = chartData.length
    ? chartData.reduce((a, b) => (b.total > a.total ? b : a))
    : null;

  if (!itens.length) {
    return (
      <Vazio
        mensagem="Nenhuma aquisição planejada com os filtros atuais. Adicione títulos pela aba Recomendações."
        icone={PackageOpen}
      />
    );
  }

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
        <MiniKpi rotulo="Investimento planejado" valor={fmtBRL(total)} icone={CalendarPlus} detalhe={`${fmtInt(itens.length)} títulos`} />
        <MiniKpi rotulo="Economia vs preço médio" valor={fmtBRL(economia)} icone={PiggyBank} detalhe="comprando no melhor preço atual" />
        <MiniKpi
          rotulo="Mês mais pesado"
          valor={mesMaisCaro ? mesLabel(mesMaisCaro.mes) : "—"}
          icone={TrendingDown}
          detalhe={mesMaisCaro ? fmtBRL(mesMaisCaro.total) : undefined}
        />
        <MiniKpi
          rotulo="Orçamento de referência"
          valor={fmtBRL(ORCAMENTO_REF)}
          icone={PiggyBank}
          detalhe={`${itens.length > 0 ? Math.ceil(total / ORCAMENTO_REF) : 0} parcelas mensais ideais`}
        />
      </div>

      <ChartCard
        titulo="Investimento planejado por mês"
        descricao="Custos estimados das próximas aquisições (melhor preço atual de cada título)"
        atraso={0.05}
      >
        <div className="h-[230px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} margin={{ top: 6, right: 4, left: -14, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" vertical={false} />
              <XAxis
                dataKey="mes"
                tickFormatter={mesLabel}
                tick={{ fontSize: 11, fill: "var(--muted-foreground)" }}
                axisLine={false}
                tickLine={false}
              />
              <YAxis
                tick={{ fontSize: 11, fill: "var(--muted-foreground)" }}
                axisLine={false}
                tickLine={false}
                tickFormatter={(v: number) => (v >= 1000 ? `R$ ${(v / 1000).toLocaleString("pt-BR", { maximumFractionDigits: 1 })}k` : `R$ ${v}`)}
              />
              <Tooltip cursor={{ fill: "color-mix(in oklch, var(--primary) 6%, transparent)" }} content={(props) => <TooltipComp {...props} formatador={(v) => fmtBRL(v)} />} />
              <ReferenceLine
                y={ORCAMENTO_REF}
                stroke="var(--muted-foreground)"
                strokeDasharray="4 4"
                label={{ value: "orçamento", position: "insideTopRight", fontSize: 10, fill: "var(--muted-foreground)" }}
              />
              <Bar dataKey="total" name="Planejado" fill={CORES[0]} radius={[5, 5, 0, 0]} maxBarSize={34} animationDuration={700} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </ChartCard>

      <div className="space-y-4">
        {porMes.map(([mes, lista], idx) => {
          const totalMes = lista.reduce((a, it) => a + it.preco, 0);
          return (
            <motion.div
              key={mes}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.35, delay: Math.min(idx * 0.05, 0.3) }}
              className="overflow-hidden rounded-xl border border-border/60 bg-card shadow-sm"
            >
              <div className="flex items-center justify-between gap-2 border-b border-border/60 bg-muted/40 px-4 py-2">
                <h4 className="text-xs font-semibold">{mesLabelLongo(mes)}</h4>
                <span className="text-xs tabular text-muted-foreground">
                  {lista.length} {lista.length === 1 ? "título" : "títulos"} ·{" "}
                  <strong className="text-foreground">{fmtBRL(totalMes)}</strong>
                </span>
              </div>
              <ul className="divide-y divide-border/50">
                {lista.map((it) => {
                  const loja = melhorLoja(it.b);
                  return (
                    <li
                      key={it.b.id}
                      className="flex items-center gap-3 px-4 py-2.5 transition-colors hover:bg-muted/30"
                    >
                      <div className="min-w-0 flex-1">
                        <p className="flex items-center gap-1.5 truncate text-sm font-medium">
                          <span className="truncate" title={it.b.titulo}>{it.b.titulo}</span>
                          {it.b.top && (
                            <Star className="h-3 w-3 shrink-0 fill-current" style={{ color: "var(--chart-1)" }} title="Prioridade #top" />
                          )}
                          {it.extra && <Badge className="h-4 px-1 text-[9px]">novo</Badge>}
                        </p>
                        <p className="truncate text-[11px] text-muted-foreground">
                          {it.b.autor}
                          {loja && <> · melhor preço em <span className="text-foreground/80">{loja.nome}</span></>}
                        </p>
                      </div>
                      <span className="text-sm font-semibold tabular">{fmtBRL2(it.preco)}</span>
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-7 w-7 text-muted-foreground hover:text-destructive"
                        onClick={() => onRemover(it.b.id)}
                        aria-label={`Remover ${it.b.titulo} do plano`}
                        title="Remover do plano"
                      >
                        <Trash2 className="h-3.5 w-3.5" />
                      </Button>
                    </li>
                  );
                })}
              </ul>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
