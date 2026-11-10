"use client";

import * as React from "react";
import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useReactTable,
  type SortingState,
} from "@tanstack/react-table";
import {
  ArrowDown,
  ArrowUp,
  ArrowUpDown,
  BookMarked,
  ChevronLeft,
  ChevronRight,
  Star,
  Store,
  TabletSmartphone,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Badge } from "@/components/ui/badge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Sparkline, Vazio } from "./charts";
import { DIF_LABEL, EXT_LABEL, TIPO_LABEL, fmtBRL2, fmtInt, var30d, melhorLoja } from "@/lib/dashboard";
import type { BookRecord } from "@/lib/types";

const col = createColumnHelper<BookRecord>();

function Dots({ nivel }: { nivel: number }) {
  return (
    <span className="flex items-center gap-0.5" title={`${DIF_LABEL[nivel]}`}>
      {[1, 2, 3].map((i) => (
        <span
          key={i}
          className="h-1.5 w-1.5 rounded-full"
          style={{ background: i <= nivel ? "var(--primary)" : "var(--muted)" }}
        />
      ))}
    </span>
  );
}

function StatusBadge({ b }: { b: BookRecord }) {
  if (b.status === "wishlist") {
    return (
      <Badge variant="outline" className="gap-1 border-primary/40 bg-primary/10 px-1.5 text-[10px] font-medium text-primary">
        <BookMarked className="h-3 w-3" />
        Wishlist
      </Badge>
    );
  }
  if (b.formato === "virtual" || b.formato === "ebook") {
    return (
      <Badge variant="secondary" className="gap-1 px-1.5 text-[10px] font-medium">
        <TabletSmartphone className="h-3 w-3" />
        E-book
      </Badge>
    );
  }
  if (b.formato === "ambos") {
    return (
      <Badge variant="secondary" className="gap-1 px-1.5 text-[10px] font-medium">
        <TabletSmartphone className="h-3 w-3" />
        Físico + e-book
      </Badge>
    );
  }
  return (
    <Badge variant="secondary" className="px-1.5 text-[10px] font-medium">
      Estante
    </Badge>
  );
}

function LojasPopover({ b }: { b: BookRecord }) {
  if (!b.lojas?.length) return <span className="text-muted-foreground">—</span>;
  const melhor = melhorLoja(b);
  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button variant="ghost" size="icon" className="h-7 w-7 text-muted-foreground hover:text-foreground" aria-label={`Ver preços de ${b.titulo}`}>
          <Store className="h-4 w-4" />
        </Button>
      </PopoverTrigger>
      <PopoverContent align="end" className="w-64 p-0">
        <div className="border-b border-border/60 p-3">
          <p className="truncate text-xs font-semibold" title={b.titulo}>{b.titulo}</p>
          <p className="mt-0.5 truncate text-[11px] text-muted-foreground">{b.autor}</p>
          {b.historico && (
            <div className="mt-2">
              <Sparkline valores={b.historico} cor="var(--chart-2)" largura={232} altura={30} />
              <p className="mt-1 text-[10px] text-muted-foreground">histórico de 12 meses (melhor preço/mês)</p>
            </div>
          )}
        </div>
        <div className="space-y-1 p-2">
          {[...b.lojas]
            .sort((a, c) => a.preco - c.preco)
            .map((l) => (
              <div
                key={l.nome}
                className="flex items-center justify-between gap-2 rounded-md px-2 py-1 text-xs transition-colors hover:bg-muted"
              >
                <span className="flex min-w-0 items-center gap-1.5">
                  <TabletSmartphone className={cnTipo(l.tipo)} />
                  <span className="truncate">{l.nome}</span>
                  {melhor?.nome === l.nome && (
                    <Badge className="h-4 px-1 text-[9px]" style={{ background: "var(--success)", color: "white" }}>
                      melhor
                    </Badge>
                  )}
                </span>
                <span className="font-semibold tabular">{fmtBRL2(l.preco)}</span>
              </div>
            ))}
        </div>
      </PopoverContent>
    </Popover>
  );
}

function cnTipo(tipo: string) {
  return `h-3.5 w-3.5 shrink-0 ${tipo === "usado" ? "text-chart-5" : tipo === "ebook" ? "text-chart-2" : "text-muted-foreground"}`;
}

export function CatalogTable({ books }: { books: BookRecord[] }) {
  const [sorting, setSorting] = React.useState<SortingState>([{ id: "titulo", desc: false }]);
  const [pagination, setPagination] = React.useState({ pageIndex: 0, pageSize: 10 });

  React.useEffect(() => {
    setPagination((p) => ({ ...p, pageIndex: 0 }));
  }, [books]);

  const columns = React.useMemo(
    () => [
      col.accessor("titulo", {
        header: "Título",
        cell: (i) => (
          <div className="max-w-[180px] sm:max-w-[260px]">
            <p className="truncate font-medium" title={i.getValue()}>
              {i.getValue()}
            </p>
            <p className="truncate text-[11px] text-muted-foreground md:hidden">{i.row.original.autor}</p>
          </div>
        ),
      }),
      col.accessor("autor", {
        header: "Autor",
        cell: (i) => (
          <p className="max-w-[140px] truncate text-muted-foreground" title={i.getValue()}>
            {i.getValue()}
          </p>
        ),
      }),
      col.accessor("eixo", {
        header: "Eixo",
        cell: (i) => (
          <p className="max-w-[150px] truncate text-xs text-muted-foreground" title={i.getValue()}>
            {i.getValue()}
          </p>
        ),
      }),
      col.accessor("tipo", {
        header: "Tipo",
        cell: (i) => (
          <Badge variant="outline" className="px-1.5 text-[10px] font-medium text-muted-foreground">
            {TIPO_LABEL[i.getValue()] ?? i.getValue()}
          </Badge>
        ),
      }),
      col.accessor("dif", {
        header: "Dif.",
        cell: (i) => <Dots nivel={i.getValue()} />,
        sortingFn: "basic",
      }),
      col.accessor("ext", {
        header: "Ext.",
        cell: (i) => (
          <span className="text-[10px] text-muted-foreground" title={`Extensão: ${EXT_LABEL[i.getValue()]}`}>
            {EXT_LABEL[i.getValue()]}
          </span>
        ),
      }),
      col.accessor("status", {
        header: "Status",
        cell: (i) => <StatusBadge b={i.row.original} />,
        sortingFn: (a, b) => a.original.status.localeCompare(b.original.status),
      }),
      col.accessor((b) => b.nota, {
        id: "nota",
        header: "Nota",
        cell: (i) =>
          i.getValue() != null ? (
            <span className="inline-flex items-center gap-0.5 text-xs font-semibold">
              <Star className="h-3 w-3 fill-current" style={{ color: "var(--chart-1)" }} />
              {String(i.getValue()).replace(".", ",")}
            </span>
          ) : (
            <span className="text-muted-foreground">—</span>
          ),
      }),
      col.accessor((b) => b.precoAtual ?? b.valorPago, {
        id: "preco",
        header: "Preço",
        cell: (i) => {
          const b = i.row.original;
          if (b.status === "wishlist") {
            const m = melhorLoja(b);
            return (
              <span className="font-semibold tabular" title={`Melhor: ${m?.nome ?? "—"}`}>
                {fmtBRL2(i.getValue() ?? 0)}
              </span>
            );
          }
          if (i.getValue() != null) {
            return (
              <span className="text-muted-foreground tabular" title="Valor pago na aquisição">
                {fmtBRL2(i.getValue())}
              </span>
            );
          }
          return <span className="text-muted-foreground">—</span>;
        },
      }),
      col.accessor((b) => var30d(b), {
        id: "var30d",
        header: "Δ 30d",
        cell: (i) => {
          const v = i.getValue();
          if (v == null) return <span className="text-muted-foreground">—</span>;
          const boa = v < 0;
          return (
            <span
              className="text-xs font-semibold tabular"
              style={{ color: Math.abs(v) < 0.1 ? "var(--muted-foreground)" : boa ? "var(--success)" : "var(--destructive)" }}
            >
              {v > 0 ? "+" : ""}
              {v.toFixed(1).replace(".", ",")}%
            </span>
          );
        },
      }),
      col.accessor((b) => b.matchScore, {
        id: "match",
        header: "Match",
        cell: (i) => {
          const v = i.getValue();
          if (v == null) return <span className="text-muted-foreground">—</span>;
          return (
            <div className="flex items-center gap-2">
              <div className="h-1.5 w-12 overflow-hidden rounded-full bg-muted">
                <div
                  className="h-full rounded-full transition-all duration-700"
                  style={{
                    width: `${v}%`,
                    background: v >= 85 ? "var(--success)" : v >= 70 ? "var(--chart-1)" : "var(--muted-foreground)",
                  }}
                />
              </div>
              <span className="text-[10px] tabular text-muted-foreground">{v}</span>
            </div>
          );
        },
      }),
      col.display({
        id: "acoes",
        header: "",
        cell: (i) => (
          <div className="flex justify-end">
            <LojasPopover b={i.row.original} />
          </div>
        ),
      }),
    ],
    [],
  );

  const table = useReactTable({
    data: books,
    columns,
    state: { sorting, pagination },
    onSortingChange: setSorting,
    onPaginationChange: setPagination,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
  });

  if (!books.length) {
    return <Vazio mensagem="Nenhuma obra encontrada com os filtros atuais. Ajuste os filtros acima para ver o catálogo." />;
  }

  const page = table.getState().pagination.pageIndex;
  const pageCount = table.getPageCount();
  const first = page * pagination.pageSize + 1;
  const last = Math.min(books.length, (page + 1) * pagination.pageSize);

  return (
    <div>
      <div className="mb-3 flex flex-wrap items-center justify-between gap-2">
        <p className="text-xs text-muted-foreground">
          <span className="font-semibold text-foreground">{fmtInt(books.length)}</span> obras · ordenáveis por qualquer
          coluna
        </p>
        <label className="flex items-center gap-1.5 text-xs text-muted-foreground">
          Por página
          <select
            value={pagination.pageSize}
            onChange={(e) => setPagination({ pageIndex: 0, pageSize: Number(e.target.value) })}
            className="h-7 rounded-md border border-border/70 bg-background px-1.5 text-xs"
            aria-label="Obras por página"
          >
            {[10, 20, 50].map((n) => (
              <option key={n} value={n}>
                {n}
              </option>
            ))}
          </select>
        </label>
      </div>

      <div className="scrollbar-thin overflow-x-auto rounded-lg border border-border/60">
        <Table className="min-w-[760px]">
          <TableHeader>
            <TableRow className="bg-muted/50 hover:bg-muted/50">
              {table.getHeaderGroups()[0].headers.map((header) => (
                <TableHead
                  key={header.id}
                  className={
                    header.column.getCanSort()
                      ? "cursor-pointer select-none whitespace-nowrap text-[11px] font-semibold"
                      : "text-[11px] font-semibold"
                  }
                  onClick={header.column.getToggleSortingHandler()}
                  title={header.column.getCanSort() ? "Clique para ordenar" : undefined}
                >
                  <span className="inline-flex items-center gap-1">
                    {flexRender(header.column.columnDef.header, header.getContext())}
                    {header.column.getIsSorted() === "asc" ? (
                      <ArrowUp className="h-3 w-3 text-primary" />
                    ) : header.column.getIsSorted() === "desc" ? (
                      <ArrowDown className="h-3 w-3 text-primary" />
                    ) : (
                      header.column.getCanSort() && <ArrowUpDown className="h-3 w-3 opacity-40" />
                    )}
                  </span>
                </TableHead>
              ))}
            </TableRow>
          </TableHeader>
          <TableBody>
            {table.getRowModel().rows.map((row) => (
              <TableRow key={row.id} className="transition-colors hover:bg-muted/40">
                {row.getVisibleCells().map((cell) => (
                  <TableCell
                    key={cell.id}
                    className={
                      cell.column.id === "autor"
                        ? "hidden md:table-cell"
                        : cell.column.id === "eixo"
                          ? "hidden lg:table-cell"
                          : cell.column.id === "nota"
                            ? "hidden xl:table-cell"
                            : cell.column.id === "ext"
                              ? "hidden lg:table-cell"
                              : cell.column.id === "var30d"
                                ? "hidden sm:table-cell"
                                : cell.column.id === "match"
                                  ? "hidden md:table-cell"
                                  : ""
                    }
                  >
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>

      <div className="mt-3 flex items-center justify-between gap-2">
        <p className="text-xs text-muted-foreground">
          Mostrando {first}–{last} de {fmtInt(books.length)}
        </p>
        <div className="flex items-center gap-1">
          <Button variant="outline" size="icon" className="h-7 w-7" disabled={!table.getCanPreviousPage()} onClick={() => table.previousPage()} aria-label="Página anterior">
            <ChevronLeft className="h-4 w-4" />
          </Button>
          <span className="px-2 text-xs tabular text-muted-foreground">
            {page + 1} / {pageCount}
          </span>
          <Button variant="outline" size="icon" className="h-7 w-7" disabled={!table.getCanNextPage()} onClick={() => table.nextPage()} aria-label="Próxima página">
            <ChevronRight className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  );
}
