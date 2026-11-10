"use client";

import * as React from "react";
import { motion } from "framer-motion";
import {
  BookOpenCheck,
  LayoutDashboard,
  LibraryBig,
  LineChart as LineChartIcon,
  Lock,
  ShoppingCart,
  Sparkles,
} from "lucide-react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { ThemeToggle } from "@/components/theme-provider";
import { useToast } from "@/hooks/use-toast";
import { FilterBar } from "@/components/dashboard/filters";
import { KpiCard } from "@/components/dashboard/kpi-card";
import { OverviewTab } from "@/components/dashboard/overview";
import { CatalogTable } from "@/components/dashboard/catalog-table";
import { RecommendationsTab } from "@/components/dashboard/recommendations";
import { AcquisitionsTab, type ItemPlano } from "@/components/dashboard/acquisitions";
import { PricesTab } from "@/components/dashboard/prices";
import { BOOKS, TIMELINE_MONTHS } from "@/lib/catalog-data";
import {
  DEFAULT_FILTROS,
  TIPO_LABEL,
  computeKpis,
  filterBooks,
  mesLabel,
  rangeInfo,
  type Filtros,
} from "@/lib/dashboard";
import type { BookRecord } from "@/lib/types";

const CHAVE_TIPO = Object.fromEntries(Object.entries(TIPO_LABEL).map(([k, v]) => [v, k]));
const PROXIMO_MES = (() => {
  const [a, m] = TIMELINE_MONTHS[TIMELINE_MONTHS.length - 1].split("-").map(Number);
  return m === 12 ? `${a + 1}-01` : `${a}-${String(m + 1).padStart(2, "0")}`;
})();

export default function Page() {
  const [filtros, setFiltros] = React.useState<Filtros>(DEFAULT_FILTROS);
  const [extras, setExtras] = React.useState<{ id: string; mes: string; preco: number }[]>([]);
  const [removidos, setRemovidos] = React.useState<Set<string>>(new Set());
  const { toast } = useToast();

  const filtrados = React.useMemo(() => filterBooks(BOOKS, filtros), [filtros]);
  const r = React.useMemo(() => rangeInfo(filtros), [filtros]);
  const kpis = React.useMemo(() => computeKpis(filtrados, r), [filtrados, r]);

  const plano: ItemPlano[] = React.useMemo(() => {
    const base = filtrados
      .filter(
        (b) => b.status === "wishlist" && b.planejadoMes && !removidos.has(b.id),
      )
      .map((b) => ({ b, mes: b.planejadoMes!, preco: b.planejadoPreco ?? b.precoAtual ?? 0, extra: false }));
    const novos = extras
      .map((e) => {
        const b = filtrados.find((x) => x.id === e.id);
        return b ? { b, mes: e.mes, preco: e.preco, extra: true } : null;
      })
      .filter((x): x is ItemPlano => !!x);
    return [...base, ...novos];
  }, [filtrados, extras, removidos]);

  const planejadosIds = React.useMemo(() => new Set(plano.map((p) => p.b.id)), [plano]);

  const onPlanejar = (b: BookRecord) => {
    setExtras((xs) => (xs.some((x) => x.id === b.id) ? xs : [...xs, { id: b.id, mes: PROXIMO_MES, preco: b.precoAtual ?? 0 }]));
    toast({
      title: "Adicionado às próximas aquisições",
      description: `«${b.titulo}» planejado para ${mesLabel(PROXIMO_MES)} (~R$ ${(b.precoAtual ?? 0).toFixed(2).replace(".", ",")}).`,
    });
  };

  const onRemoverPlano = (id: string) => {
    if (extras.some((x) => x.id === id)) {
      setExtras((xs) => xs.filter((x) => x.id !== id));
    } else {
      setRemovidos((s) => new Set(s).add(id));
    }
  };

  const onToggleTipo = (label: string) => {
    const chave = CHAVE_TIPO[label] ?? label;
    setFiltros((f) => ({
      ...f,
      tipos: f.tipos.includes(chave) ? f.tipos.filter((x) => x !== chave) : [...f.tipos, chave],
    }));
  };

  const onToggleDif = (d: number) => {
    setFiltros((f) => ({
      ...f,
      difs: f.difs.includes(d) ? f.difs.filter((x) => x !== d) : [...f.difs, d],
    }));
  };

  const wishlistFiltrada = React.useMemo(() => filtrados.filter((b) => b.status === "wishlist"), [filtrados]);

  return (
    <div className="flex min-h-screen flex-col">
      <header className="sticky top-0 z-40 border-b border-border/60 bg-background/80 backdrop-blur-md">
        <div className="mx-auto flex h-16 max-w-7xl items-center gap-3 px-4 sm:px-6">
          <div
            className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl shadow-sm"
            style={{ background: "linear-gradient(135deg, oklch(0.62 0.13 55), oklch(0.52 0.13 45))" }}
            aria-hidden
          >
            <BookOpenCheck className="h-5 w-5 text-white" />
          </div>
          <div className="min-w-0">
            <h1 className="truncate text-base font-bold leading-tight sm:text-lg">Biblioteca do Lucas</h1>
            <p className="hidden truncate text-[11px] text-muted-foreground sm:block">
              Estante física · e-books · recomendações · próximas aquisições · preços online
            </p>
          </div>
          <div className="ml-auto flex items-center gap-2">
            <Badge variant="outline" className="hidden gap-1 border-border/60 bg-card/70 px-2 py-1 text-[10px] text-muted-foreground sm:inline-flex">
              <Lock className="h-3 w-3" />
              uso pessoal · dados locais
            </Badge>
            <ThemeToggle />
          </div>
        </div>
      </header>

      <main className="mx-auto w-full max-w-7xl flex-1 space-y-5 px-4 py-6 sm:px-6">
        <FilterBar filtros={filtros} setFiltros={setFiltros} totalVisivel={filtrados.length} />

        <section aria-label="Indicadores principais" className="grid grid-cols-2 gap-3 md:grid-cols-3 xl:grid-cols-6">
          {kpis.map((k, i) => (
            <KpiCard key={k.chave} kpi={k} indice={i} />
          ))}
        </section>

        <Tabs defaultValue="visao-geral" className="gap-5">
          <div className="scrollbar-thin overflow-x-auto">
            <TabsList className="h-10 w-full min-w-max justify-start gap-1 rounded-xl border border-border/60 bg-card/70 p-1 sm:w-auto sm:justify-center">
              {[
                { valor: "visao-geral", rotulo: "Visão geral", Icone: LayoutDashboard },
                { valor: "catalogo", rotulo: "Catálogo", Icone: LibraryBig },
                { valor: "recomendacoes", rotulo: "Recomendações", Icone: Sparkles },
                { valor: "aquisicoes", rotulo: "Aquisições", Icone: ShoppingCart },
                { valor: "precos", rotulo: "Preços", Icone: LineChartIcon },
              ].map(({ valor, rotulo, Icone }) => (
                <TabsTrigger
                  key={valor}
                  value={valor}
                  className="h-8 gap-1.5 rounded-lg px-3 text-xs data-[state=active]:shadow-sm sm:text-[13px]"
                >
                  <Icone className="h-4 w-4" />
                  <span className="hidden sm:inline">{rotulo}</span>
                  <span className="sm:hidden">{rotulo.split(" ")[0]}</span>
                </TabsTrigger>
              ))}
            </TabsList>
          </div>

          <TabsContent value="visao-geral" className="mt-0">
            <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.3 }}>
              <OverviewTab books={filtrados} r={r} onToggleTipo={onToggleTipo} onToggleDif={onToggleDif} />
            </motion.div>
          </TabsContent>
          <TabsContent value="catalogo" className="mt-0">
            <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.3 }}>
              <CatalogTable books={filtrados} />
            </motion.div>
          </TabsContent>
          <TabsContent value="recomendacoes" className="mt-0">
            <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.3 }}>
              <RecommendationsTab books={filtrados} planejadosIds={planejadosIds} onPlanejar={onPlanejar} />
            </motion.div>
          </TabsContent>
          <TabsContent value="aquisicoes" className="mt-0">
            <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.3 }}>
              <AcquisitionsTab itens={plano} onRemover={onRemoverPlano} />
            </motion.div>
          </TabsContent>
          <TabsContent value="precos" className="mt-0">
            <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.3 }}>
              <PricesTab books={wishlistFiltrada} r={r} />
            </motion.div>
          </TabsContent>
        </Tabs>
      </main>

      <footer className="mt-auto border-t border-border/60 bg-card/40">
        <div className="mx-auto flex max-w-7xl flex-col gap-1 px-4 py-3 text-[11px] text-muted-foreground sm:flex-row sm:items-center sm:justify-between sm:px-6">
          <p>Biblioteca do Lucas · painel pessoal e privado</p>
          <p>Dados de amostra derivados do catálogo mestre · atualizado em nov/2026</p>
        </div>
      </footer>
    </div>
  );
}
