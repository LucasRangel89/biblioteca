"use client";

import * as React from "react";
import { AtividadeChart, ChartCard, DonutChart, EixosChart, InvestimentoChart } from "./charts";
import { TIPO_LABEL, topEixos, seriesAtividade, DIF_LABEL, type RangeInfo } from "@/lib/dashboard";
import type { BookRecord } from "@/lib/types";

const TIPOS = ["F", "NF", "poesia", "HQ", "antologia"];
const DIFS = [1, 2, 3];

export function OverviewTab({
  books,
  r,
  onToggleTipo,
  onToggleDif,
}: {
  books: BookRecord[];
  r: RangeInfo;
  onToggleTipo: (tipo: string) => void;
  onToggleDif: (dif: number) => void;
}) {
  const atividade = React.useMemo(() => seriesAtividade(books, r.months), [books, r.months]);
  const porTipo = React.useMemo(
    () =>
      TIPOS.map((t) => ({ nome: TIPO_LABEL[t], valor: books.filter((b) => b.tipo === t).length })).filter(
        (d) => d.valor > 0,
      ),
    [books],
  );
  const porDif = React.useMemo(
    () => DIFS.map((d) => ({ nome: DIF_LABEL[d], valor: books.filter((b) => b.dif === d).length })).filter((d) => d.valor > 0),
    [books],
  );
  const eixos = React.useMemo(() => topEixos(books, 8), [books]);

  return (
    <div className="grid grid-cols-1 gap-4 lg:grid-cols-12">
      <ChartCard
        titulo="Atividade da biblioteca"
        descricao="Aquisições físicas e virtuais e leituras concluídas por mês"
        className="lg:col-span-8"
        atraso={0.05}
      >
        <AtividadeChart data={atividade} />
      </ChartCard>

      <ChartCard
        titulo="Composição por tipo"
        descricao="Clique em um tipo para filtrar o painel"
        className="lg:col-span-4"
        atraso={0.1}
      >
        <DonutChart data={porTipo} rotuloCentro="obras" onSegmentClick={(nome) => onToggleTipo(nome)} />
      </ChartCard>

      <ChartCard
        titulo="Investimento mensal"
        descricao="Gasto com aquisições (R$) — linha do orçamento de referência"
        className="lg:col-span-4"
        atraso={0.15}
      >
        <InvestimentoChart data={atividade} />
      </ChartCard>

      <ChartCard
        titulo="Nível de dificuldade"
        descricao="Clique em um nível para filtrar o painel"
        className="lg:col-span-4"
        atraso={0.2}
      >
        <DonutChart
          data={porDif}
          rotuloCentro="obras"
          onSegmentClick={(nome) => {
            const d = DIFS.find((x) => DIF_LABEL[x] === nome);
            if (d != null) onToggleDif(d);
          }}
        />
      </ChartCard>

      <ChartCard
        titulo="Eixos mais presentes"
        descricao="Top 8 eixos temáticos após os filtros"
        className="lg:col-span-4"
        atraso={0.25}
      >
        <EixosChart data={eixos} />
      </ChartCard>
    </div>
  );
}
