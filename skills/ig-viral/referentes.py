#!/usr/bin/env python3
"""
referentes.py - ordena los reels que recogiste según cuánto superaron a su
propia cuenta, nombra la fórmula de gancho de cada uno y escribe el archivo de
referentes.

Basado en swipe.py de instagram-agent-skill, de Jake Schincariol (licencia
MIT). Traducción y adaptación al español: Juan Sebastian Cruz - 1691 Agency.

La idea de este programa es una sola corrección: las vistas solas no son
evidencia. Una cuenta de 2.000.000 de seguidores con 400.000 vistas tuvo un día
tranquilo. Una cuenta de 4.000 seguidores con 400.000 vistas encontró algo.
Esto ordena por cuántas veces superó lo normal de su propia cuenta, que es la
única versión de "se hizo viral" que te dice algo que puedas copiar.

La entrada es un archivo separado por tabulaciones que vas llenando mientras
miras, un reel por fila, con una primera línea que nombra las columnas (en
español o en inglés):

    cuenta    seguidores   mediana   vistas    gancho
    @alguien  48000        11000     412000    nadie te dice que tus primeros 30 fracasan

`mediana` son las vistas normales recientes de esa cuenta y es la mejor base.
Si solo tienes `seguidores`, deja la mediana vacía y el programa lo avisa.
`gancho` es la primera frase del reel, dicha o en pantalla, en sus palabras.
Las cifras pueden ir como 412000, 412.000, 412,000, 412k, 412 mil o 1,2M.

Uso
  python3 referentes.py recogidos.tsv
  python3 referentes.py recogidos.tsv --salida referentes.md
  python3 referentes.py recogidos.tsv --json
"""

import argparse
import json
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORD_RE = re.compile(r"[^\W_]+(?:[$%'’-][^\W_]+)*%?|\$[\d]+%?", re.UNICODE)
QUITAR_TILDES = str.maketrans("áéíóúüÁÉÍÓÚÜ", "aeiouuAEIOUU")


def sin_tildes(texto):
    return texto.translate(QUITAR_TILDES).lower()


def buscar(nombre):
    """Busca un archivo en esta carpeta y, si no está, en la carpeta de ig-reel."""
    for carpeta in (HERE, os.path.join(HERE, "..", "ig-reel")):
        ruta = os.path.join(carpeta, nombre)
        if os.path.exists(ruta):
            return ruta, carpeta
    return None, None


GANCHOS, _ = buscar("ganchos.json")
_, CARPETA_PUNTAJE = buscar("puntaje_gancho.py")
try:                                              # opcional: calificar también los ganchos
    if CARPETA_PUNTAJE:
        sys.path.insert(0, CARPETA_PUNTAJE)
    from puntaje_gancho import run as score_hook  # noqa: E402
except Exception:
    score_hook = None

COLUMNAS = {
    "cuenta": "account", "account": "account",
    "seguidores": "followers", "followers": "followers",
    "mediana": "median", "median": "median",
    "vistas": "views", "reproducciones": "views", "views": "views",
    "gancho": "hook", "hook": "hook",
}


def load_formulas(path):
    try:
        d = json.load(open(path, encoding="utf-8"))
    except Exception:
        return None
    by_id = {h["id"]: h for h in d["hooks"]}
    order = d.get("classify_order") or sorted(by_id)
    return [(by_id[i]["id"], by_id[i]["name"],
             re.compile(by_id[i]["match"], re.IGNORECASE)) for i in order if i in by_id]


def classify(hook, formulas):
    if not formulas:
        return None, "sin clasificar"
    low = sin_tildes(hook)
    for fid, name, pattern in formulas:
        if pattern.search(low):
            return fid, name
    return None, "sin clasificar"


def numero(texto):
    """412000, 412.000, 412,000, 412k, 412 mil, 1,2M, 1.2 millones -> entero."""
    s = sin_tildes(texto or "").replace(" ", "")
    if not s:
        return None
    m = re.match(r"^([\d.,]+)(k|mil|m|mm|millones|millon)?$", s)
    if not m:
        digits = re.sub(r"[^\d]", "", s)
        return int(digits) if digits else None
    num, suf = m.groups()
    if not suf:
        digits = re.sub(r"[^\d]", "", num)
        return int(digits) if digits else None
    mult = 1000 if suf in ("k", "mil") else 1_000_000
    num = num.replace(",", ".")
    if num.count(".") > 1:
        num = num.replace(".", "", num.count(".") - 1)
    try:
        return int(round(float(num) * mult))
    except ValueError:
        return None


def read_rows(path):
    raw = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
    lines = [l for l in raw.splitlines() if l.strip() and not l.lstrip().startswith("#")]
    if not lines:
        return []
    head = [COLUMNAS.get(sin_tildes(c.strip()), sin_tildes(c.strip())) for c in lines[0].split("\t")]
    if "views" in head and "hook" in head:
        cols, body = head, lines[1:]
    else:
        cols, body = ["account", "followers", "views", "hook"], lines
    rows = []
    for line in body:
        cells = line.split("\t")
        if len(cells) < len(cols):
            cells += [""] * (len(cols) - len(cells))
        r = dict(zip(cols, [c.strip() for c in cells]))
        r["views"] = numero(r.get("views", "")) or 0
        for k in ("followers", "median"):
            r[k] = numero(r.get(k, ""))
        if r["views"] and r.get("hook"):
            rows.append(r)
    return rows


def miles(n):
    return f"{n:,}".replace(",", ".")


def analyse(rows, formulas):
    used_median = any(r.get("median") for r in rows)
    for r in rows:
        base = r.get("median") or r.get("followers") or 0
        r["baseline"] = base
        r["outlier"] = round(r["views"] / base, 2) if base else None
        r["formula_id"], r["formula"] = classify(r["hook"], formulas)
        r["words"] = len(WORD_RE.findall(r["hook"]))
        if score_hook:
            _, overall, verdict, _ = score_hook(r["hook"])
            r["hook_score"], r["hook_verdict"] = round(overall, 1), verdict
        else:
            r["hook_score"], r["hook_verdict"] = None, None
    ranked = sorted(rows, key=lambda r: -(r["outlier"] or 0))
    third = max(1, len(ranked) // 3)
    top, bottom = ranked[:third], ranked[-third:]

    def med(items, key):
        vals = [i[key] for i in items if i.get(key) is not None]
        return round(statistics.median(vals), 1) if vals else None

    counts = {}
    for r in top:
        counts[r["formula"]] = counts.get(r["formula"], 0) + 1
    return {
        "baseline": "mediana de la cuenta" if used_median else "número de seguidores",
        "n": len(ranked),
        "accounts": len({r.get("account", "") for r in ranked}),
        "reels": ranked,
        "top_formulas": sorted(counts.items(), key=lambda kv: -kv[1]),
        "top_hook_score": med(top, "hook_score"),
        "bottom_hook_score": med(bottom, "hook_score"),
        "top_words": med(top, "words"),
        "bottom_words": med(bottom, "words"),
        "unclassified": sum(1 for r in ranked if r["formula"] == "sin clasificar"),
    }


def render(a, out=sys.stdout):
    head = (f"REFERENTES  ·  {a['n']} reels  ·  {a['accounts']} cuentas  ·  "
            f"base: {a['baseline']}")
    print("\n" + head, file=out)
    print("=" * max(len(head), 78), file=out)
    for r in a["reels"]:
        mult = f"{r['outlier']:.1f}x" if r["outlier"] else "   ?"
        score = f"{r['hook_score']:.0f}" if r["hook_score"] is not None else " -"
        fid = f"#{r['formula_id']:<2}" if r["formula_id"] else "-  "
        print(f"  {mult:>7}  gancho {score:>3}  {fid} {r['formula'][:24]:<24} "
              f"{r.get('account', '')[:16]:<16} {miles(r['views']):>11}", file=out)
        print(f"           \"{r['hook'][:96]}\"", file=out)
    print("-" * max(len(head), 78), file=out)
    print("LO QUE ESTÁ FUNCIONANDO EN ESTE GRUPO", file=out)
    if a["top_formulas"]:
        print("  tercio superior:          "
              + ", ".join(f"{n} x{c}" for n, c in a["top_formulas"][:4]), file=out)
    if a["top_hook_score"] is not None:
        print(f"  puntaje medio del gancho: arriba {a['top_hook_score']:.0f}  "
              f"vs abajo {a['bottom_hook_score']:.0f}", file=out)
    print(f"  largo medio del gancho:   arriba {a['top_words']} palabras  "
          f"vs abajo {a['bottom_words']} palabras", file=out)
    print(f"  sin clasificar:           {a['unclassified']} de {a['n']}. Léelos a mano: ahí "
          "se esconde una fórmula que todavía no tienes.", file=out)
    print("\n  Un grupo recogido a mano es evidencia, no prueba. Doce reels no muestran nada;\n"
          "  cuarenta en seis cuentas muestran algo. Recoge más antes de creerlo.\n", file=out)


def to_markdown(a):
    lines = ["# Referentes", "",
             f"{a['n']} reels de {a['accounts']} cuentas. "
             f"Ordenados por cuántas veces superaron la {a['baseline']}.", ""]
    for r in a["reels"]:
        mult = f"{r['outlier']:.1f}x" if r["outlier"] else "?"
        lines += [f"## {mult}  {r['formula']}  ({r.get('account', '')})",
                  f"- vistas: {miles(r['views'])}  base: {miles(r['baseline'])}",
                  f"- puntaje del gancho: {r['hook_score']}  palabras: {r['words']}",
                  f"- gancho: \"{r['hook']}\"", ""]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Ordena reels recogidos por cuántas veces superaron a su cuenta.")
    ap.add_argument("input", nargs="?", default="-", help="archivo TSV, o - para leer de la entrada")
    ap.add_argument("--ganchos", "--hooks", dest="ganchos", default=GANCHOS,
                    help="ruta de ganchos.json")
    ap.add_argument("--salida", "--out", dest="salida", help="guarda también el archivo de referentes en markdown")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rows = read_rows(args.input)
    if not rows:
        print("no hay filas útiles. Hace falta un archivo separado por tabulaciones con al "
              "menos vistas y gancho.", file=sys.stderr)
        sys.exit(2)
    formulas = load_formulas(args.ganchos) if args.ganchos else None
    a = analyse(rows, formulas)
    if not formulas:
        print("aviso: no se encontró ganchos.json, las fórmulas no tienen nombre. Usa --ganchos.",
              file=sys.stderr)
    if score_hook is None:
        print("aviso: no se pudo cargar puntaje_gancho.py, se omiten los puntajes.", file=sys.stderr)

    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    if args.salida:
        path = os.path.expanduser(args.salida)
        carpeta = os.path.dirname(path)
        if carpeta:
            os.makedirs(carpeta, exist_ok=True)
        open(path, "w", encoding="utf-8").write(to_markdown(a))
        print(f"guardado en {path}", file=sys.stderr)


if __name__ == "__main__":
    main()
