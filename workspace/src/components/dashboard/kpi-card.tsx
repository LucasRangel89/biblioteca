"use client";

import * as React from "react";
import { motion } from "framer-motion";
import {
  ArrowDownRight,
  ArrowUpRight,
  BookCheck,
  BookOpen,
  Library,
  Minus,
  TabletSmartphone,
  Tag,
  Wallet,
  type LucideIcon,
} from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { fmtBRL, fmtInt, type Kpi } from "@/lib/dashboard";

const ICONES: Record<string, LucideIcon> = {
  Library,
  BookOpen,
  TabletSmartphone,
  BookCheck,
  Wallet,
  Tag,
};

function useCountUp(valor: number, duracao = 800) {
  const [n, setN] = React.useState(0);
  const ref = React.useRef<number | null>(null);
  React.useEffect(() => {
    const inicio = performance.now();
    const de = n;
    const ate = valor;
    if (ref.current) cancelAnimationFrame(ref.current);
    const tick = (t: number) => {
      const p = Math.min(1, (t - inicio) / duracao);
      const eased = 1 - Math.pow(1 - p, 3);
      setN(de + (ate - de) * eased);
      if (p < 1) ref.current = requestAnimationFrame(tick);
    };
    ref.current = requestAnimationFrame(tick);
    return () => {
      if (ref.current) cancelAnimationFrame(ref.current);
    };
  }, [valor]);
  return n;
}

export function KpiCard({ kpi, indice }: { kpi: Kpi; indice: number }) {
  const animado = useCountUp(kpi.valor);
  const Icone = ICONES[kpi.icone] ?? Library;
  const valorExibido = kpi.formato === "brl" ? fmtBRL(animado) : fmtInt(Math.round(animado));

  // corrige formatação da tendência (percentual, não moeda)
  const tendenciaFmt =
    kpi.tendencia == null
      ? null
      : `${kpi.tendencia > 0 ? "+" : ""}${kpi.tendencia.toFixed(1).replace(".", ",")}%`;

  return (
    <motion.div
      initial={{ opacity: 0, y: 14 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: indice * 0.05 }}
    >
      <Card className="group relative overflow-hidden border-border/60 shadow-sm transition-all duration-300 hover:-translate-y-0.5 hover:shadow-md">
        <div
          className="pointer-events-none absolute -right-6 -top-6 h-20 w-20 rounded-full opacity-[0.08] transition-transform duration-500 group-hover:scale-150"
          style={{ background: "var(--primary)" }}
        />
        <CardContent className="p-4">
          <div className="flex items-center justify-between gap-2">
            <p className="text-xs font-medium tracking-wide text-muted-foreground">{kpi.rotulo}</p>
            <span
              className="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg"
              style={{ background: "color-mix(in oklch, var(--primary) 12%, transparent)", color: "var(--primary)" }}
            >
              <Icone className="h-3.5 w-3.5" />
            </span>
          </div>
          <div className="mt-2 flex flex-wrap items-baseline gap-x-2 gap-y-0.5">
            <p className="text-2xl font-bold tracking-tight tabular">{valorExibido}</p>
            {kpi.tendencia != null && (
              <span
                className="inline-flex items-center gap-0.5 text-[11px] font-semibold tabular"
                style={{
                  color:
                    Math.abs(kpi.tendencia) < 0.05
                      ? "var(--muted-foreground)"
                      : (kpi.quedaBoa ? kpi.tendencia < 0 : kpi.tendencia > 0)
                        ? "var(--success)"
                        : "var(--destructive)",
                }}
              >
                {kpi.tendencia > 0 ? (
                  <ArrowUpRight className="h-3 w-3" />
                ) : kpi.tendencia < 0 ? (
                  <ArrowDownRight className="h-3 w-3" />
                ) : (
                  <Minus className="h-3 w-3" />
                )}
                {tendenciaFmt}
              </span>
            )}
          </div>
          <p className="mt-1 text-[11px] leading-snug text-muted-foreground line-clamp-2">{kpi.subtitulo}</p>
        </CardContent>
      </Card>
    </motion.div>
  );
}
