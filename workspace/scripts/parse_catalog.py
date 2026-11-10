#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera src/lib/catalog-data.ts a partir do catálogo mestre do Lucas,
enriquecendo com dados de amostra realistas (determinísticos, seed fixa):
leituras, aquisições físicas/virtuais, histórico e comparação de preços online,
próximas aquisições e recomendações com score de afinidade."""
import json
import random
import re
import unicodedata
from pathlib import Path

SRC = Path("/home/z/my-project/upload/Biblioteca_Lucas_Catalogo_Mestre.md")
OUT = Path("/home/z/my-project/src/lib/catalog-data.ts")
OUT_TYPES = Path("/home/z/my-project/src/lib/types.ts")

random.seed(20261109)

HOJE = "2026-11-09"

# Meses da linha do tempo (eventos: aquisições e leituras)
TIMELINE_MONTHS = [f"2025-{m:02d}" for m in range(6, 13)] + [f"2026-{m:02d}" for m in range(1, 12)]
# Histórico de preços: 12 meses terminando em 2026-11
PRICE_MONTHS = ["2025-12"] + [f"2026-{m:02d}" for m in range(1, 12)]

SECTION_EIXO = {
    "0": None,  # estante -> inferido por tags
    "1": "Pré-história e origens",
    "2": "Ficção científica, fantasia e distopia",
    "3": "Clássicos universais",
    "4": "Brasil e América Latina",
    "5": "Ficção contemporânea",
    "6": "Romances históricos",
    "7": "Horror, weird e mistério",
    "8": "Poesia e cartas",
    "9": "Filosofia, ética e existência",
    "10": "Mente e consciência",
    "11": "Política, poder e economia",
    "12": "Sociedade, antropologia e história",
    "13": "Ciência, tecnologia e futuro",
    "14": "Psicologia e comportamento",
    "15": "Espiritualidade e consciência",
    "16": "Artes, escrita e vida prática",
}

EIXO_ORDER = [
    "Pré-história e origens",
    "Ficção científica, fantasia e distopia",
    "Clássicos universais",
    "Brasil e América Latina",
    "Ficção contemporânea",
    "Romances históricos",
    "Horror, weird e mistério",
    "Poesia e cartas",
    "Filosofia, ética e existência",
    "Mente e consciência",
    "Psicologia e comportamento",
    "Política, poder e economia",
    "Sociedade, antropologia e história",
    "Ciência, tecnologia e futuro",
    "Espiritualidade e consciência",
    "Artes, escrita e vida prática",
]

ORIGEM_TAGS = {"BR", "RS", "latam", "portugal", "africa", "asia", "europa-leste", "classico", "contemporaneo"}
ORIGEM_LABEL = {
    "BR": "Brasil", "RS": "Rio Grande do Sul", "latam": "América Latina", "portugal": "Portugal",
    "africa": "África", "asia": "Ásia", "europa-leste": "Europa Oriental",
    "classico": "Clássico", "contemporaneo": "Contemporâneo",
}
TRILHA_LABEL = {
    "rel-imortais": "Pré-história & neandertais", "rel-widows-bay": "Lovecraft & weird",
    "rel-cornwell": "Romances históricos", "rel-asimov-clarke": "Asimov & Clarke",
    "rel-yalom": "Yalom & psicologia", "rel-fromm": "Autoritarismo & mente social",
}

LOJAS_NOVAS = ["Amazon.com.br", "Livraria Cultura", "Mercado Livre", "Saraiva", "Estante Virtual"]
LOJA_EBOOK = "Amazon Kindle"
LOJA_USADO = "Estante Virtual (usado)"


def strip_paren_note(autor: str) -> str:
    a = re.sub(r"\s*\(na prateleira.*?\)", "", autor)
    a = re.sub(r"\s*\(conforme a prateleira\)", "", a)
    a = a.strip(" ;")
    if a == "(autor não informado)" or not a:
        a = "Autor não informado"
    return a.strip() or autor.strip()


def parse_catalog():
    text = SRC.read_text(encoding="utf-8")
    lines = text.split("\n")
    section = None
    books = []
    for ln in lines:
        m_sec = re.match(r"^## (\d+)\. ", ln)
        if m_sec:
            section = m_sec.group(1)
            continue
        if section is None or not ln.startswith("|"):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) < 3 or cells[0].lower() in ("título", "titulo", "title"):
            continue
        if set(cells[0]) <= set("-: "):
            continue
        titulo, autor_raw, tags_raw = cells[0], cells[1], cells[2]
        tags = re.findall(r"#([\wçãéáíóúâêôõà-]+)", tags_raw)
        titulo = titulo.strip()
        autor = strip_paren_note(autor_raw)
        books.append({"titulo": titulo, "autor": autor, "tags": tags, "section": section})
    return books


def tipo_of(tags):
    for t in ("F", "NF", "poesia", "HQ", "antologia"):
        if t in tags:
            return t
    return "NF"


def dif_of(tags):
    for t in ("d1", "d2", "d3"):
        if t in tags:
            return int(t[1])
    return 2


def ext_of(tags):
    for t in ("e1", "e2", "e3"):
        if t in tags:
            return int(t[1])
    return 2


def eixo_of(b):
    tags = b["tags"]

    def has(*xs):
        return any(t in tags for t in xs)

    if has("ficcao-cientifica", "fantasia", "distopia", "utopia", "historia-alternativa"):
        return "Ficção científica, fantasia e distopia"
    if has("horror", "lovecraftiano", "gotico"):
        return "Horror, weird e mistério"
    if has("thriller", "thriller-medico", "misterio"):
        return "Horror, weird e mistério"
    if has("espiritismo", "umbanda", "espiritualidade", "oriental", "mistica", "religiao"):
        return "Espiritualidade e consciência"
    if has("psicologia", "psicanalise", "psiquiatria", "neurociencia"):
        return "Psicologia e comportamento"
    if has("filosofia", "existencialismo", "etica"):
        return "Filosofia, ética e existência"
    if has("politica", "autoritarismo", "economia", "geopolitica"):
        return "Política, poder e economia"
    if has("ciencia", "ia"):
        return "Ciência, tecnologia e futuro"
    if has("romance-historico", "medieval", "roma", "antiguidade", "renascimento"):
        return "Romances históricos"
    if has("historia", "antropologia", "sociologia", "testemunho", "biografia"):
        return "Sociedade, antropologia e história"
    if has("latam", "BR", "RS", "regional-gaucho", "portugal"):
        return "Brasil e América Latina"
    if has("poesia"):
        return "Poesia e cartas"
    if has("guerra"):
        return "Sociedade, antropologia e história"
    if has("antiguidade", "teatro"):
        return "Clássicos universais"
    return "Ficção contemporânea"


def norm_key(s):
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s.lower() if c.isalnum() or c == " ").strip()


def price_seed(b):
    """Preço base realista (R$) conforme extensão/dificuldade/origem."""
    tags = b["tags"]
    base = {1: random.uniform(24.9, 44.9), 2: random.uniform(34.9, 74.9), 3: random.uniform(54.9, 129.9)}[b["ext"]]
    if "classico" in tags:
        base *= random.uniform(0.55, 0.8)
    if b["dif"] == 3:
        base *= 1.15
    if "sem-pt" in tags:
        base *= random.uniform(1.35, 1.85)
    return round(base) - 0.1  # termina em ,90


def month_weight(m):
    """Peso de aquisição/leitura por mês (ritmo crescente, picos de promoção)."""
    idx = TIMELINE_MONTHS.index(m)
    w = 1.0 + 0.18 * idx
    mm = int(m.split("-")[1])
    if mm == 11:
        w *= 1.6   # Black Friday
    if mm in (1, 7):
        w *= 1.25  # férias
    return w


def pick_month(lo=0, hi=None, weighter=None):
    hi = len(TIMELINE_MONTHS) if hi is None else hi
    pool = TIMELINE_MONTHS[lo:hi]
    ws = [weighter(m) if weighter else 1 for m in pool]
    r = random.uniform(0, sum(ws))
    acc = 0
    for m, w in zip(pool, ws):
        acc += w
        if acc >= r:
            return m
    return pool[-1]


def main():
    raw = parse_catalog()
    seen = {}
    for b in raw:
        k = norm_key(b["titulo"]) + "|" + norm_key(b["autor"])
        if k not in seen:
            seen[k] = b
    books = list(seen.values())

    for b in books:
        b["tipo"] = tipo_of(b["tags"])
        b["dif"] = dif_of(b["tags"])
        b["ext"] = ext_of(b["tags"])
        b["eixo"] = SECTION_EIXO[b["section"]] or eixo_of(b)
        b["top"] = "top" in b["tags"]
        b["verificar"] = "verificar" in b["tags"]
        b["semPt"] = "sem-pt" in b["tags"]
        b["lido_tag"] = "lido" in b["tags"]
        b["tenho_tag"] = "ja-tenho" in b["tags"]
        b["trilha"] = next((t for t in b["tags"] if t.startswith("rel-")), None)
        b["origem"] = [ORIGEM_LABEL[t] for t in b["tags"] if t in ORIGEM_TAGS]
        b["temas"] = [t for t in b["tags"] if t not in ORIGEM_TAGS and not t.startswith("rel-")
                      and t not in ("F", "NF", "poesia", "HQ", "antologia", "d1", "d2", "d3",
                                    "e1", "e2", "e3", "ja-tenho", "lido", "top", "verificar", "sem-pt")]

    owned = [b for b in books if b["tenho_tag"] or b["lido_tag"]]
    wishlist = [b for b in books if b not in owned]

    # ---- propriedade: estante física + e-books (biblioteca virtual) ----
    for b in owned:
        b["status"] = "estante"
        b["formato"] = "fisico"

    # Alguns da estante também têm e-book ("ambos")
    ambos_pool = [b for b in owned if b["dif"] == 1 or b["ext"] == 1]
    for b in random.sample(ambos_pool, k=min(9, len(ambos_pool))):
        b["formato"] = "ambos"

    # Biblioteca virtual: parte da wishlist virou e-book nos últimos meses
    def virtual_weight(b):
        w = 1.0
        if b["top"]:
            w += 1.4
        if b["dif"] == 1:
            w += 0.8
        if b["ext"] == 1:
            w += 0.6
        if b["semPt"]:
            w += 1.2  # compra e-book de títulos sem edição PT-BR
        if "filosofia" in b["tags"] or "psicologia" in b["tags"] or "ia" in b["tags"]:
            w += 0.5
        return w

    vpool = sorted(wishlist, key=lambda b: random.uniform(0, virtual_weight(b)), reverse=True)
    virtuais = vpool[:46]
    for b in virtuais:
        b["status"] = "estante"
        b["formato"] = "virtual"
        wishlist.remove(b)

    # datas de aquisição dos físicos (~64 dentro da janela; resto = antes)
    fis_window = [b for b in owned if b["formato"] in ("fisico", "ambos")]
    n_fis = min(64, len(fis_window))
    for b in random.sample(fis_window, n_fis):
        b["dataAquisicao"] = pick_month(weighter=month_weight)
    for b in owned:
        b.setdefault("dataAquisicao", None)

    # e-books: últimos 12 meses (a partir de dez/2025), picos de promoção
    lo_virt = TIMELINE_MONTHS.index("2025-12")
    for b in virtuais:
        b["dataAquisicao"] = pick_month(lo=lo_virt, weighter=month_weight)

    # valor pago
    for b in owned:
        base = price_seed(b)
        if b["formato"] == "virtual":
            b["valorPago"] = round(random.uniform(9.9, 44.9), 2)
        else:
            b["valorPago"] = round(base * random.uniform(0.55, 0.92), 2)
        b["dataLeitura"] = None
        b["nota"] = None

    # ---- leituras concluídas (ritmo crescente) ----
    pace = [1, 1, 2, 1, 3, 2, 1, 3, 2, 2, 4, 3, 2, 4, 3, 5, 4, 2]  # por mês da timeline
    pool_lidos = [b for b in owned if b["lido_tag"] or b["dif"] != 3]
    random.shuffle(pool_lidos)
    usado = set()
    for m, qtd in zip(TIMELINE_MONTHS, pace):
        espaco = 0
        while qtd > 0 and espaco < 4:
            cand = next((b for b in pool_lidos if b["titulo"] not in usado and
                         (b.get("dataAquisicao") is None or b.get("dataAquisicao") <= m)), None)
            if cand is None:
                break
            usado.add(cand["titulo"])
            cand["dataLeitura"] = m
            cand["nota"] = round(random.uniform(3.6, 5.0), 1)
            pool_lidos.remove(cand)
            qtd -= 1
            espaco += 1

    # ---- wishlist: preços online + histórico 12 meses ----
    for b in wishlist:
        b["status"] = "wishlist"
        b["formato"] = "ebook" if (b["semPt"] and random.random() < 0.5) else ("fisico" if random.random() < 0.75 else "ebook")
        base = price_seed(b)
        lojas = []
        n_novas = random.choice((2, 3))
        for loja in random.sample(LOJAS_NOVAS, n_novas):
            p = base * random.uniform(0.94, 1.12)
            lojas.append({"nome": loja, "preco": round(p, 2), "tipo": "novo"})
        lojas.append({"nome": LOJA_USADO, "preco": round(base * random.uniform(0.42, 0.72), 2), "tipo": "usado"})
        if b["tipo"] not in ("HQ", "antologia"):
            lojas.append({"nome": LOJA_EBOOK, "preco": round(base * random.uniform(0.55, 0.8), 2), "tipo": "ebook"})
        best = min(l["preco"] for l in lojas)

        # histórico 12 meses do melhor preço
        hist = []
        p = base * random.uniform(1.02, 1.12)
        for m in PRICE_MONTHS:
            p *= random.uniform(0.965, 1.035)
            if m == "2025-12":
                p *= 0.88  # Black Friday 2025
            if m == "2026-10":
                p *= random.uniform(0.93, 0.99)
            hist.append(round(p, 2))
        hist[-1] = min(hist[-1], best)
        b["lojas"] = lojas
        b["precoAtual"] = best
        b["historico"] = hist
        b["precoMedia12m"] = round(sum(hist) / len(hist), 2)
        b["precoAnterior30d"] = hist[-2]
        b["precoMin12m"] = min(hist)
        b["precoAlvo"] = round(min(hist) * 0.92 + 0.9, 2)

    # ---- recomendações: score + motivos ----
    eixos_lidos = {}
    for b in owned:
        if b.get("dataLeitura"):
            eixos_lidos[b["eixo"]] = eixos_lidos.get(b["eixo"], 0) + 1
    top_eixos = {e for e, _ in sorted(eixos_lidos.items(), key=lambda kv: -kv[1])[:5]}
    trilha_owned = {}
    for b in owned:
        if b["trilha"]:
            trilha_owned[b["trilha"]] = trilha_owned.get(b["trilha"], 0) + 1
    autores_owned = {norm_key(b["autor"]) for b in owned}

    for b in wishlist:
        score = random.uniform(52, 60)
        motivos = []
        if b["top"]:
            score += 26
            motivos.append("Marcado como prioridade nas suas listas (#top)")
        if b["trilha"] and b["trilha"] in trilha_owned:
            score += 13
            motivos.append(f"Você já tem {trilha_owned[b['trilha']]} livros da trilha «{TRILHA_LABEL[b['trilha']]}»")
        if norm_key(b["autor"]) in autores_owned:
            score += 11
            motivos.append(f"Você já tem outros livros de {b['autor']}")
        if b["eixo"] in top_eixos:
            score += 7
            motivos.append(f"Combina com um dos seus eixos mais lidos ({b['eixo'].lower()})")
        if b["dif"] == 1:
            score += 4
        if b["dif"] == 3:
            score -= 4
        if b["ext"] == 1:
            score += 3
            if b["dif"] == 1:
                motivos.append("Leitura leve e curta — boa entre livros densos")
        if b["semPt"]:
            score -= 7
            motivos.append("Sem edição brasileira confirmada — considere e-book ou importação")
        if b["verificar"]:
            score -= 5
            motivos.append("Verificar autor/título/edição antes de comprar")
        if len(motivos) < 2:
            motivos.append("Alta afinidade temática com sua estante")
        b["matchScore"] = int(max(41, min(99, score)))
        b["motivos"] = motivos[:3]
        b["planejadoMes"] = None
        b["planejadoPreco"] = None

    # ---- próximas aquisições planejadas (16 títulos) ----
    cand_plan = sorted([b for b in wishlist if b["matchScore"] >= 70],
                       key=lambda b: (-b["matchScore"], random.random()))
    plan_months = ["2026-12", "2026-12", "2027-01", "2027-01", "2027-02", "2027-02",
                    "2027-03", "2027-03", "2027-03", "2027-04", "2027-04", "2027-05",
                    "2027-05", "2027-06", "2027-06", "2027-06"]
    for b, m in zip(cand_plan[:16], plan_months):
        b["planejadoMes"] = m
        b["planejadoPreco"] = b["precoAtual"]

    # ---- montagem final ----
    def rec(b, i):
        return {
            "id": f"b{i:03d}",
            "titulo": b["titulo"],
            "autor": b["autor"],
            "eixo": b["eixo"],
            "tipo": b["tipo"],
            "dif": b["dif"],
            "ext": b["ext"],
            "tags": b["temas"][:5],
            "trilha": TRILHA_LABEL[b["trilha"]] if b["trilha"] else None,
            "origem": b["origem"],
            "status": b["status"],
            "formato": b["formato"],
            "top": b["top"],
            "verificar": b["verificar"],
            "semPt": b["semPt"],
            "dataAquisicao": b.get("dataAquisicao"),
            "valorPago": b.get("valorPago"),
            "dataLeitura": b.get("dataLeitura"),
            "nota": b.get("nota"),
            "precoAtual": b.get("precoAtual"),
            "precoMedia12m": b.get("precoMedia12m"),
            "precoAnterior30d": b.get("precoAnterior30d"),
            "precoMin12m": b.get("precoMin12m"),
            "precoAlvo": b.get("precoAlvo"),
            "historico": b.get("historico"),
            "lojas": b.get("lojas"),
            "matchScore": b.get("matchScore"),
            "motivos": b.get("motivos"),
            "planejadoMes": b.get("planejadoMes"),
            "planejadoPreco": b.get("planejadoPreco"),
        }

    random.shuffle(books)
    records = [rec(b, i) for i, b in enumerate(books, 1)]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT_TYPES.write_text("""// Tipos do dataset da biblioteca (gerado a partir do catálogo mestre)

export type TipoLivro = "F" | "NF" | "poesia" | "HQ" | "antologia";

export interface LojaPreco {
  nome: string;
  preco: number;
  tipo: "novo" | "usado" | "ebook";
}

export interface BookRecord {
  id: string;
  titulo: string;
  autor: string;
  eixo: string;
  tipo: TipoLivro;
  /** dificuldade: 1 = leve · 2 = média · 3 = exigente */
  dif: 1 | 2 | 3;
  /** extensão: 1 = curta · 2 = média · 3 = longa */
  ext: 1 | 2 | 3;
  tags: string[];
  trilha: string | null;
  origem: string[];
  /** estante (possui) | wishlist (desejo) */
  status: "estante" | "wishlist";
  /** fisico | virtual (e-book) | ambos | ebook (desejo em e-book) */
  formato: "fisico" | "virtual" | "ambos" | "ebook";
  top: boolean;
  verificar: boolean;
  semPt: boolean;
  /** mês de aquisição no formato YYYY-MM (null = antes de jun/2025) */
  dataAquisicao: string | null;
  valorPago: number | null;
  /** mês em que terminou de ler (YYYY-MM) */
  dataLeitura: string | null;
  nota: number | null;
  /** melhor preço online atual (somente wishlist) */
  precoAtual: number | null;
  precoMedia12m: number | null;
  precoAnterior30d: number | null;
  precoMin12m: number | null;
  precoAlvo: number | null;
  /** 12 melhores preços mensais (PRICE_MONTHS) */
  historico: number[] | null;
  lojas: LojaPreco[] | null;
  /** score de afinidade/recomendação (somente wishlist) */
  matchScore: number | null;
  motivos: string[] | null;
  planejadoMes: string | null;
  planejadoPreco: number | null;
}
""", encoding="utf-8")

    OUT.write_text(
        "// Arquivo gerado automaticamente por scripts/parse_catalog.py — não editar manualmente.\n"
        'import type { BookRecord } from "./types";\n\n'
        'export const DATA_REF = ' + json.dumps(HOJE, ensure_ascii=False) + ";\n"
        'export const TIMELINE_MONTHS: string[] = ' + json.dumps(TIMELINE_MONTHS) + ";\n"
        'export const PRICE_MONTHS: string[] = ' + json.dumps(PRICE_MONTHS) + ";\n"
        'export const EIXOS: string[] = ' + json.dumps(EIXO_ORDER, ensure_ascii=False) + ";\n"
        'export const BOOKS: BookRecord[] = ' + json.dumps(records, ensure_ascii=False, separators=(",", ":")) + ";\n",
        encoding="utf-8",
    )

    n_estante = sum(1 for r in records if r["status"] == "estante")
    n_virt = sum(1 for r in records if r["status"] == "estante" and r["formato"] in ("virtual", "ambos"))
    n_wish = sum(1 for r in records if r["status"] == "wishlist")
    n_lidos = sum(1 for r in records if r["dataLeitura"])
    invest = sum(r["valorPago"] or 0 for r in records if r["dataAquisicao"])
    print(f"total={len(records)} estante={n_estante} (com virtual={n_virt}) wishlist={n_wish}")
    print(f"lidos={n_lidos} investimento_total=R$ {invest:.2f}")
    print(f"planejados={sum(1 for r in records if r['planejadoMes'])}")
    hist_mes = {}
    for r in records:
        if r["dataAquisicao"]:
            hist_mes[r["dataAquisicao"]] = hist_mes.get(r["dataAquisicao"], 0) + 1
    print("aquisições/mês:", json.dumps(hist_mes, ensure_ascii=False))
    print("amostra:", json.dumps(records[0], ensure_ascii=False, indent=1)[:800])


if __name__ == "__main__":
    main()
