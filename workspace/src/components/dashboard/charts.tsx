"use client";

import * as React from "react";
import { motion } from "framer-motion";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ComposedChart,
  Line,
  LineChart,
  Pie,
  PieChart,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { BookOpen as BookOpenIcon } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import { fmtBRL, fmtInt, mesLabel, type MesAtividade } from "@/lib/dashboard";

// --chart-N já contém a cor completa em oklch(); usar var() diretamente.
// NÃO envolver em oklch(var(--chart-N)) — a substituição duplicada invalida a cor.
export const CORES = [
  "var(--chart-1)",
  "var(--chart-2)",
  "var(--chart-3)",
  "var(--chart-4)",
  "var(--chart-5)",
];

export const ORCAMENTO_REF = 300; // orçamento de referência mensal (R$)

// ---------------------------------------------------------------------------
// Card de gráfico
// ---------------------------------------------------------------------------

export function ChartCard({
  titulo,
  descricao,
  acoes,
  className,
  atraso = 0,
  children,
}: {
  titulo: string;
  descricao?: string;
  acoes?: React.ReactNode;
  className?: string;
  atraso?: number;
  children: React.ReactNode;
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.45, delay: atraso, ease: "easeOut" }}
      className={cn("h-full", className)}
    >
      <Card className="h-full border-border/60 shadow-sm">
        <CardContent className="flex h-full flex-col p-4 sm:p-5">
          <div className="mb-3 flex items-start justify-between gap-3">
            <div>
              <h3 className="text-sm font-semibold">{titulo}</h3>
              {descricao && <p className="mt-0.5 text-xs text-muted-foreground">{descricao}</p>}
            </div>
            {acoes}
          </div>
          <div className="min-h-0 flex-1">{children}</div>
        </CardContent>
      </Card>
    </motion.div>
  );
}

// ---------------------------------------------------------------------------
// Tooltip customizado
// ---------------------------------------------------------------------------

interface TipPayload {
  name?: string | number;
  value?: number | string;
  color?: string;
  dataKey?: string | number;
  payload?: Record<string, unknown>;
}

export function TooltipComp({
  active,
  payload,
  label,
  formatador,
  extra,
}: {
  active?: boolean;
  payload?: TipPayload[];
  label?: string | number;
  formatador?: (v: number) => string;
  extra?: (row: Record<string, unknown>) => string | null;
}) {
  if (!active || !payload?.length) return null;
  const linhas = payload.filter((p) => typeof p.value === "number");
  const extraTxt = extra ? extra((payload[0]?.payload ?? {}) as Record<string, unknown>) : null;
  return (
    <div className="rounded-lg border border-border/70 bg-popover px-3 py-2 text-xs shadow-lg">
      <p className="mb-1 font-semibold text-foreground">
        {typeof label === "string" && label.includes("-") ? mesLabel(label) : label}
      </p>
      <div className="space-y-0.5">
        {linhas.map((p, i) => (
          <div key={i} className="flex items-center justify-between gap-4">
            <span className="flex items-center gap-1.5 text-muted-foreground">
              <span className="h-2 w-2 rounded-full" style={{ background: p.color ?? "var(--primary)" }} />
              {p.name}
            </span>
            <span className="font-semibold tabular text-foreground">
              {formatador ? formatador(p.value as number) : fmtInt(p.value as number)}
            </span>
          </div>
        ))}
        {extraTxt && <p className="pt-1 text-[11px] text-muted-foreground">{extraTxt}</p>}
      </div>
    </div>
  );
}

const estiloEixo = {
  tick: { fontSize: 11, fill: "var(--muted-foreground)" },
  axisLine: false as const,
  tickLine: false as const,
};

// ---------------------------------------------------------------------------
// Atividade (barras físicas/virtuais + linha de leituras)
// ---------------------------------------------------------------------------

export function AtividadeChart({ data }: { data: MesAtividade[] }) {
  const legendas = [
    { nome: "Aquisições físicas", cor: CORES[0] },
    { nome: "E-books comprados", cor: CORES[1] },
    { nome: "Leituras concluídas", cor: CORES[2] },
  ];
  return (
    <div className="flex h-full flex-col">
      <div className="h-[220px] sm:h-[240px]">
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart data={data} margin={{ top: 6, right: 4, left: -18, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" vertical={false} />
            <XAxis dataKey="mes" tickFormatter={mesLabel} {...estiloEixo} interval="preserveStartEnd" />
            <YAxis yAxisId="esq" allowDecimals={false} {...estiloEixo} />
            <YAxis yAxisId="dir" orientation="right" allowDecimals={false} {...estiloEixo} />
            <Tooltip
              cursor={{ fill: "color-mix(in oklch, var(--primary) 6%, transparent)" }}
              content={(props) => (
                <TooltipComp
                  {...props}
                  formatador={(v) => fmtInt(v)}
                  extra={(row) =>
                    `Investimento no mês: ${fmtBRL(Number(row.investimento ?? 0))}`
                  }
                />
              )}
            />
            <Bar yAxisId="esq" dataKey="fisicas" name="Aquisições físicas" fill={CORES[0]} radius={[4, 4, 0, 0]} maxBarSize={18} animationDuration={700} />
            <Bar yAxisId="esq" dataKey="virtuais" name="E-books comprados" fill={CORES[1]} radius={[4, 4, 0, 0]} maxBarSize={18} animationDuration={700} />
            <Line
              yAxisId="dir"
              type="monotone"
              dataKey="leituras"
              name="Leituras concluídas"
              stroke={CORES[2]}
              strokeWidth={2.5}
              dot={false}
              activeDot={{ r: 4, strokeWidth: 0 }}
              animationDuration={800}
            />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
      <div className="mt-2 flex flex-wrap items-center gap-x-4 gap-y-1">
        {legendas.map((l) => (
          <span key={l.nome} className="flex items-center gap-1.5 text-[11px] text-muted-foreground">
            <span className="h-2 w-2 rounded-full" style={{ background: l.cor }} />
            {l.nome}
          </span>
        ))}
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Investimento mensal (barras)
// ---------------------------------------------------------------------------

export function InvestimentoChart({ data }: { data: MesAtividade[] }) {
  return (
    <div className="h-[240px]">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 6, right: 4, left: -14, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" vertical={false} />
          <XAxis dataKey="mes" tickFormatter={mesLabel} {...estiloEixo} interval="preserveStartEnd" />
          <YAxis
            {...estiloEixo}
            tickFormatter={(v: number) => (v >= 1000 ? `R$ ${(v / 1000).toLocaleString("pt-BR", { maximumFractionDigits: 1 })}k` : `R$ ${v}`)}
          />
          <Tooltip
            cursor={{ fill: "color-mix(in oklch, var(--primary) 6%, transparent)" }}
            content={(props) => <TooltipComp {...props} formatador={(v) => fmtBRL(v)} />}
          />
          <ReferenceLine
            y={ORCAMENTO_REF}
            stroke="var(--muted-foreground)"
            strokeDasharray="4 4"
            label={{ value: "orçamento", position: "insideTopRight", fontSize: 10, fill: "var(--muted-foreground)" }}
          />
          <Bar dataKey="investimento" name="Investido" fill={CORES[0]} radius={[5, 5, 0, 0]} maxBarSize={26} animationDuration={700} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Donut (rosca) com legenda e drill-down
// ---------------------------------------------------------------------------

export function DonutChart({
  data,
  onSegmentClick,
  rotuloCentro,
}: {
  data: { nome: string; valor: number }[];
  onSegmentClick?: (nome: string) => void;
  rotuloCentro?: string;
}) {
  const total = data.reduce((a, d) => a + d.valor, 0);
  return (
    <div className="flex h-full flex-col gap-3 sm:flex-row sm:items-center">
      <div className="relative mx-auto h-[190px] w-[190px] shrink-0">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              dataKey="valor"
              nameKey="nome"
              innerRadius="62%"
              outerRadius="86%"
              paddingAngle={2}
              cornerRadius={6}
              onClick={(_: unknown, i: number) => onSegmentClick?.(data[i].nome)}
              animationDuration={700}
              cursor={onSegmentClick ? "pointer" : "default"}
            >
              {data.map((_, i) => (
                <Cell key={i} fill={CORES[i % CORES.length]} />
              ))}
            </Pie>
            <Tooltip content={(props) => <TooltipComp {...props} />} />
          </PieChart>
        </ResponsiveContainer>
        <div className="pointer-events-none absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-2xl font-bold tabular">{fmtInt(total)}</span>
          <span className="max-w-[110px] text-center text-[10px] leading-tight text-muted-foreground">
            {rotuloCentro ?? "obras"}
          </span>
        </div>
      </div>
      <div className="min-w-0 flex-1 space-y-1">
        {data.map((d, i) => (
          <button
            key={d.nome}
            type="button"
            onClick={() => onSegmentClick?.(d.nome)}
            className={cn(
              "flex w-full items-center justify-between gap-2 rounded-md px-2 py-1 text-left text-xs transition-colors",
              onSegmentClick && "cursor-pointer hover:bg-muted/70",
            )}
            aria-label={`Filtrar por ${d.nome}`}
          >
            <span className="flex min-w-0 items-center gap-2">
              <span className="h-2.5 w-2.5 shrink-0 rounded-full" style={{ background: CORES[i % CORES.length] }} />
              <span className="truncate text-muted-foreground">{d.nome}</span>
            </span>
            <span className="font-semibold tabular">{fmtInt(d.valor)}</span>
          </button>
        ))}
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Barras horizontais (eixos temáticos)
// ---------------------------------------------------------------------------

export function EixosChart({ data }: { data: { nome: string; valor: number }[] }) {
  const altura = Math.max(180, data.length * 30 + 10);
  const trunc = (s: string) => (s.length > 26 ? `${s.slice(0, 25)}…` : s);
  return (
    <div style={{ height: altura }} className="w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} layout="vertical" margin={{ top: 0, right: 30, left: 0, bottom: 0 }}>
          <XAxis type="number" hide />
          <YAxis
            type="category"
            dataKey="nome"
            width={150}
            tickFormatter={trunc}
            tick={{ fontSize: 11, fill: "var(--muted-foreground)" }}
            axisLine={false}
            tickLine={false}
          />
          <Tooltip
            cursor={{ fill: "color-mix(in oklch, var(--primary) 6%, transparent)" }}
            content={(props) => <TooltipComp {...props} />}
          />
          <Bar dataKey="valor" name="Obras" fill={CORES[1]} radius={[0, 4, 4, 0]} maxBarSize={16} animationDuration={700}>
            {data.map((_, i) => (
              <Cell key={i} fill={i === 0 ? CORES[0] : CORES[1]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Evolução de preços (linhas múltiplas)
// ---------------------------------------------------------------------------

export interface SeriePreco {
  id: string;
  nome: string;
  valores: (number | null)[];
  cor: string;
  destacada?: boolean;
}

export function PrecoChart({
  meses,
  series,
}: {
  meses: string[];
  series: SeriePreco[];
}) {
  const rows = React.useMemo(() => {
    const r: Record<string, number | string | null>[] = meses.map((m, i) => {
      const row: Record<string, number | string | null> = { mes: m };
      for (const s of series) row[s.id] = s.valores[i] ?? null;
      return row;
    });
    return r;
  }, [meses, series]);

  return (
    <div className="h-[260px]">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={rows} margin={{ top: 6, right: 6, left: -12, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" vertical={false} />
          <XAxis dataKey="mes" tickFormatter={mesLabel} {...estiloEixo} interval="preserveStartEnd" />
          <YAxis
            {...estiloEixo}
            tickFormatter={(v: number) => `R$ ${Math.round(v)}`}
          />
          <Tooltip
            content={(props) => <TooltipComp {...props} formatador={(v) => fmtBRL(v)} />}
          />
          {series.map((s) => (
            <Line
              key={s.id}
              type="monotone"
              dataKey={s.id}
              name={s.nome}
              stroke={s.cor}
              strokeWidth={s.destacada ? 1.5 : 2.5}
              strokeDasharray={s.destacada ? "5 4" : undefined}
              dot={false}
              activeDot={{ r: 4, strokeWidth: 0 }}
              connectNulls
              animationDuration={800}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Sparkline (mini-linha para tabelas e cards)
// ---------------------------------------------------------------------------

export function Sparkline({
  valores,
  largura = 88,
  altura = 26,
  cor,
  area = true,
}: {
  valores: number[];
  largura?: number;
  altura?: number;
  cor?: string;
  area?: boolean;
}) {
  if (!valores.length) return null;
  const stroke = cor ?? CORES[2];
  const min = Math.min(...valores);
  const max = Math.max(...valores);
  const span = max - min || 1;
  const passo = valores.length > 1 ? largura / (valores.length - 1) : largura;
  const pts = valores.map((v, i) => [i * passo, altura - 2 - ((v - min) / span) * (altura - 6)] as const);

  let path = `M ${pts[0][0]},${pts[0][1]}`;
  for (let i = 1; i < pts.length; i++) {
    const [x0, y0] = pts[i - 1];
    const [x1, y1] = pts[i];
    const cx = (x0 + x1) / 2;
    path += ` C ${cx},${y0} ${cx},${y1} ${x1},${y1}`;
  }
  const idArea = `spark-${Math.round(min * 1000)}-${valores.length}-${Math.round(max * 1000)}`;
  return (
    <svg width={largura} height={altura} viewBox={`0 0 ${largura} ${altura}`} className="overflow-visible" aria-hidden>
      <defs>
        <linearGradient id={idArea} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor={stroke} stopOpacity="0.35" />
          <stop offset="100%" stopColor={stroke} stopOpacity="0" />
        </linearGradient>
      </defs>
      {area && <path d={`${path} L ${pts[pts.length - 1][0]},${altura} L 0,${altura} Z`} fill={`url(#${idArea})`} />}
      <path d={path} fill="none" stroke={stroke} strokeWidth="1.75" strokeLinecap="round" />
      <circle cx={pts[pts.length - 1][0]} cy={pts[pts.length - 1][1]} r="2.2" fill={stroke} />
    </svg>
  );
}

// ---------------------------------------------------------------------------
// Anel de score
// ---------------------------------------------------------------------------

export function ScoreRing({ score, tamanho = 44 }: { score: number; tamanho?: number }) {
  const r = tamanho / 2 - 4;
  const circ = 2 * Math.PI * r;
  const off = circ * (1 - score / 100);
  const cor = score >= 85 ? "var(--success)" : score >= 70 ? "var(--chart-1)" : "var(--muted-foreground)";
  return (
    <div className="relative shrink-0" style={{ width: tamanho, height: tamanho }}>
      <svg width={tamanho} height={tamanho} className="-rotate-90">
        <circle cx={tamanho / 2} cy={tamanho / 2} r={r} fill="none" stroke="var(--muted)" strokeWidth="4" />
        <circle
          cx={tamanho / 2}
          cy={tamanho / 2}
          r={r}
          fill="none"
          stroke={cor}
          strokeWidth="4"
          strokeLinecap="round"
          strokeDasharray={circ}
          strokeDashoffset={off}
          style={{ transition: "stroke-dashoffset 0.8s ease" }}
        />
      </svg>
      <span
        className="absolute inset-0 flex items-center justify-center text-xs font-bold tabular"
        style={{ color: cor }}
      >
        {score}
      </span>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Vazio
// ---------------------------------------------------------------------------

export function Vazio({ mensagem, icone: Icone }: { mensagem: string; icone?: React.ElementType }) {
  const I = Icone ?? BookOpenIcon;
  return (
    <div className="flex flex-col items-center justify-center gap-2 py-12 text-center">
      <span className="flex h-12 w-12 items-center justify-center rounded-full bg-muted">
        <I className="h-6 w-6 text-muted-foreground" />
      </span>
      <p className="max-w-xs text-sm text-muted-foreground">{mensagem}</p>
    </div>
  );
}
