"use client";

import * as React from "react";
import { CalendarRange, Check, ChevronDown, RotateCcw, Search, SlidersHorizontal, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Checkbox } from "@/components/ui/checkbox";
import { ScrollArea } from "@/components/ui/scroll-area";
import { cn } from "@/lib/utils";
import { TIMELINE_MONTHS, EIXOS, BOOKS } from "@/lib/catalog-data";
import {
  DIF_LABEL,
  TIPO_LABEL,
  filterBooks,
  mesLabelLongo,
  type Filtros,
  type Segmento,
} from "@/lib/dashboard";

const TIPOS = ["F", "NF", "poesia", "HQ", "antologia"];
const DIFS = [1, 2, 3];
const ORIGENS = [
  "Brasil", "Rio Grande do Sul", "América Latina", "Portugal",
  "África", "Ásia", "Europa Oriental", "Clássico", "Contemporâneo",
];
const SEGMENTOS: { chave: Segmento; rotulo: string }[] = [
  { chave: "fisica", rotulo: "Estante física" },
  { chave: "virtual", rotulo: "Biblioteca virtual" },
  { chave: "wishlist", rotulo: "Wishlist" },
];

function Chip({
  ativo,
  children,
  className,
  ...rest
}: React.ButtonHTMLAttributes<HTMLButtonElement> & { ativo?: boolean }) {
  return (
    <button
      type="button"
      {...rest}
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full border px-3 py-1.5 text-xs font-medium whitespace-nowrap transition-all duration-200",
        ativo
          ? "border-primary bg-primary text-primary-foreground shadow-sm"
          : "border-border/70 bg-card text-muted-foreground hover:border-primary/40 hover:text-foreground",
        className,
      )}
    >
      {children}
    </button>
  );
}

function MultiSelect({
  rotulo,
  opcoes,
  selecionados,
  onToggle,
  onLimpar,
  contagens,
}: {
  rotulo: string;
  opcoes: string[];
  selecionados: string[];
  onToggle: (op: string) => void;
  onLimpar: () => void;
  contagens?: Record<string, number>;
}) {
  const [aberto, setAberto] = React.useState(false);
  return (
    <Popover open={aberto} onOpenChange={setAberto}>
      <PopoverTrigger asChild>
        <Chip ativo={selecionados.length > 0}>
          {selecionados.length ? `${rotulo} (${selecionados.length})` : rotulo}
          <ChevronDown className="h-3 w-3 opacity-60" />
        </Chip>
      </PopoverTrigger>
      <PopoverContent align="start" className="w-64 p-0">
        <div className="flex items-center justify-between border-b border-border/60 px-3 py-2">
          <p className="text-xs font-semibold">{rotulo}</p>
          {selecionados.length > 0 && (
            <Button variant="ghost" size="sm" className="h-6 px-2 text-[11px] text-muted-foreground" onClick={onLimpar}>
              limpar
            </Button>
          )}
        </div>
        <ScrollArea className="h-60">
          <div className="space-y-0.5 p-2">
            {opcoes.map((op) => {
              const sel = selecionados.includes(op);
              return (
                <button
                  key={op}
                  type="button"
                  onClick={() => onToggle(op)}
                  className="flex w-full items-center justify-between gap-2 rounded-md px-2 py-1.5 text-left text-xs transition-colors hover:bg-muted"
                >
                  <span className="flex items-center gap-2">
                    <Checkbox checked={sel} className="pointer-events-none h-3.5 w-3.5" />
                    <span className="truncate">{op}</span>
                  </span>
                  {contagens?.[op] != null && (
                    <span className="text-[10px] tabular text-muted-foreground">{contagens[op]}</span>
                  )}
                </button>
              );
            })}
          </div>
        </ScrollArea>
      </PopoverContent>
    </Popover>
  );
}

export function FilterBar({
  filtros,
  setFiltros,
  totalVisivel,
}: {
  filtros: Filtros;
  setFiltros: React.Dispatch<React.SetStateAction<Filtros>>;
  totalVisivel: number;
}) {
  const [expandido, setExpandido] = React.useState(false);

  const patch = (p: Partial<Filtros>) => setFiltros((f) => ({ ...f, ...p }));

  const contSegs = React.useMemo(() => {
    const base = filterBooks(BOOKS, { ...filtros, segmentos: [] } as Filtros);
    const m: Record<string, number> = {};
    for (const s of SEGMENTOS) {
      m[s.rotulo] =
        s.chave === "fisica"
          ? base.filter((b) => b.status === "estante" && b.formato !== "virtual").length
          : s.chave === "virtual"
            ? base.filter((b) => b.status === "estante" && b.formato !== "fisico").length
            : base.filter((b) => b.status === "wishlist").length;
    }
    return m;
  }, [filtros]);

  const ativos: { rotulo: string; remover: () => void }[] = [];
  if (filtros.busca.trim())
    ativos.push({ rotulo: `“${filtros.busca.trim()}”`, remover: () => patch({ busca: "" }) });
  for (const s of filtros.segmentos)
    ativos.push({
      rotulo: SEGMENTOS.find((x) => x.chave === s)?.rotulo ?? s,
      remover: () => patch({ segmentos: filtros.segmentos.filter((x) => x !== s) }),
    });
  for (const t of filtros.tipos)
    ativos.push({ rotulo: TIPO_LABEL[t] ?? t, remover: () => patch({ tipos: filtros.tipos.filter((x) => x !== t) }) });
  for (const e of filtros.eixos)
    ativos.push({ rotulo: e, remover: () => patch({ eixos: filtros.eixos.filter((x) => x !== e) }) });
  for (const d of filtros.difs)
    ativos.push({ rotulo: DIF_LABEL[d], remover: () => patch({ difs: filtros.difs.filter((x) => x !== d) }) });
  for (const o of filtros.origens)
    ativos.push({ rotulo: o, remover: () => patch({ origens: filtros.origens.filter((x) => x !== o) }) });

  const haFiltro =
    ativos.length > 0 ||
    filtros.segmentos.length > 0 ||
    filtros.tipos.length > 0 ||
    filtros.eixos.length > 0 ||
    filtros.difs.length > 0 ||
    filtros.origens.length > 0;

  return (
    <section aria-label="Filtros" className="rounded-xl border border-border/60 bg-card/70 p-3 shadow-sm backdrop-blur">
      {/* Linha 1: busca + período */}
      <div className="flex flex-col gap-2 lg:flex-row lg:items-center">
        <div className="relative flex-1 lg:max-w-64">
          <Search className="absolute left-2.5 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            value={filtros.busca}
            onChange={(e) => patch({ busca: e.target.value })}
            placeholder="Buscar título, autor, tema…"
            className="h-9 rounded-full border-border/70 bg-background pl-9 text-sm"
            aria-label="Buscar no catálogo"
          />
        </div>

        <div className="flex flex-wrap items-center gap-1.5">
          <CalendarRange className="h-4 w-4 text-muted-foreground" />
          {(["3m", "6m", "12m", "tudo"] as const).map((m) => (
            <Chip key={m} ativo={filtros.rangeMode === m} onClick={() => patch({ rangeMode: m })}>
              {m === "tudo" ? "Tudo" : m.toUpperCase()}
            </Chip>
          ))}
          <Popover>
            <PopoverTrigger asChild>
              <Chip ativo={filtros.rangeMode === "custom"}>
                {filtros.rangeMode === "custom"
                  ? `${filtros.rangeFrom} → ${filtros.rangeTo}`.replace(/-/g, "/")
                  : "Personalizado"}
              </Chip>
            </PopoverTrigger>
            <PopoverContent align="start" className="w-72 p-3">
              <p className="mb-2 text-xs font-semibold">Período personalizado</p>
              <div className="grid grid-cols-2 gap-2">
                <label className="space-y-1">
                  <span className="text-[11px] text-muted-foreground">De</span>
                  <select
                    value={filtros.rangeFrom}
                    onChange={(e) => patch({ rangeMode: "custom", rangeFrom: e.target.value })}
                    className="h-8 w-full rounded-md border border-border/70 bg-background px-2 text-xs"
                  >
                    {TIMELINE_MONTHS.map((m) => (
                      <option key={m} value={m}>
                        {mesLabelLongo(m)}
                      </option>
                    ))}
                  </select>
                </label>
                <label className="space-y-1">
                  <span className="text-[11px] text-muted-foreground">Até</span>
                  <select
                    value={filtros.rangeTo}
                    onChange={(e) => patch({ rangeMode: "custom", rangeTo: e.target.value })}
                    className="h-8 w-full rounded-md border border-border/70 bg-background px-2 text-xs"
                  >
                    {TIMELINE_MONTHS.map((m) => (
                      <option key={m} value={m}>
                        {mesLabelLongo(m)}
                      </option>
                    ))}
                  </select>
                </label>
              </div>
              <p className="mt-2 text-[11px] text-muted-foreground">
                Mês fechado mais recente: nov/2026 (dados de amostra).
              </p>
            </PopoverContent>
          </Popover>

          <span className="ml-auto flex items-center gap-2 lg:ml-3">
            <span className="hidden text-[11px] tabular text-muted-foreground sm:inline">
              {totalVisivel} de {BOOKS.length} obras
            </span>
            <Chip ativo={expandido} onClick={() => setExpandido((v) => !v)}>
              <SlidersHorizontal className="h-3 w-3" />
              Mais
              <ChevronDown className={cn("h-3 w-3 transition-transform", expandido && "rotate-180")} />
            </Chip>
            {haFiltro && (
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setFiltros((f) => ({ ...f, ...{
                  busca: "", tipos: [], eixos: [], difs: [], segmentos: [], origens: [],
                } }))}
                className="h-7 gap-1 rounded-full px-2 text-[11px] text-muted-foreground hover:text-foreground"
                aria-label="Limpar filtros"
              >
                <RotateCcw className="h-3 w-3" />
                Limpar
              </Button>
            )}
          </span>
        </div>
      </div>

      {/* Linha 2: segmentos */}
      <div className="mt-2 flex flex-wrap items-center gap-1.5">
        {SEGMENTOS.map((s) => (
          <Chip
            key={s.chave}
            ativo={filtros.segmentos.includes(s.chave)}
            onClick={() =>
              patch({
                segmentos: filtros.segmentos.includes(s.chave)
                  ? filtros.segmentos.filter((x) => x !== s.chave)
                  : [...filtros.segmentos, s.chave],
              })
            }
          >
            {s.rotulo}
            <span
              className={cn(
                "rounded-full px-1.5 py-0.5 text-[10px] tabular",
                filtros.segmentos.includes(s.chave) ? "bg-primary-foreground/20" : "bg-muted text-muted-foreground",
              )}
            >
              {contSegs[s.rotulo] ?? 0}
            </span>
          </Chip>
        ))}
      </div>

      {/* Linha 3 (expansível): tipo, dificuldade, eixo, origem */}
      {expandido && (
        <div className="mt-2 flex flex-wrap items-center gap-1.5 border-t border-border/50 pt-2">
          {TIPOS.map((t) => (
            <Chip
              key={t}
              ativo={filtros.tipos.includes(t)}
              onClick={() =>
                patch({ tipos: filtros.tipos.includes(t) ? filtros.tipos.filter((x) => x !== t) : [...filtros.tipos, t] })
              }
            >
              {TIPO_LABEL[t]}
            </Chip>
          ))}
          <span className="mx-1 h-4 w-px bg-border" aria-hidden />
          {DIFS.map((d) => (
            <Chip
              key={d}
              ativo={filtros.difs.includes(d)}
              onClick={() =>
                patch({ difs: filtros.difs.includes(d) ? filtros.difs.filter((x) => x !== d) : [...filtros.difs, d] })
              }
            >
              {DIF_LABEL[d]}
            </Chip>
          ))}
          <span className="mx-1 h-4 w-px bg-border" aria-hidden />
          <MultiSelect
            rotulo="Eixo temático"
            opcoes={EIXOS}
            selecionados={filtros.eixos}
            onToggle={(op) =>
              patch({ eixos: filtros.eixos.includes(op) ? filtros.eixos.filter((x) => x !== op) : [...filtros.eixos, op] })
            }
            onLimpar={() => patch({ eixos: [] })}
          />
          <MultiSelect
            rotulo="Origem"
            opcoes={ORIGENS}
            selecionados={filtros.origens}
            onToggle={(op) =>
              patch({
                origens: filtros.origens.includes(op) ? filtros.origens.filter((x) => x !== op) : [...filtros.origens, op],
              })
            }
            onLimpar={() => patch({ origens: [] })}
          />
        </div>
      )}

      {/* Filtros ativos */}
      {ativos.length > 0 && (
        <div className="mt-2 flex flex-wrap items-center gap-1.5 border-t border-border/50 pt-2">
          <Check className="h-3 w-3 text-muted-foreground" />
          {ativos.map((a, i) => (
            <button
              key={i}
              type="button"
              onClick={a.remover}
              className="group inline-flex items-center gap-1 rounded-full border border-primary/30 bg-primary/10 px-2 py-0.5 text-[11px] font-medium text-primary transition-colors hover:bg-primary/20"
            >
              <span className="max-w-40 truncate">{a.rotulo}</span>
              <X className="h-3 w-3 opacity-60 transition-opacity group-hover:opacity-100" />
            </button>
          ))}
        </div>
      )}
    </section>
  );
}
