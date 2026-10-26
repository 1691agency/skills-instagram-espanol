#!/usr/bin/env python3
"""
humanizar.py - quita de un borrador las huellas de texto hecho por máquina.

Basado en humanize.py de instagram-agent-skill, de Jake Schincariol (licencia
MIT). Traducción y adaptación al español: Juan Sebastian Cruz - 1691 Agency.

Tres pasadas, en este orden:

  1. INVISIBLES   borra o normaliza caracteres que un teclado nunca produce:
                  espacios de ancho cero, uniones de palabras, guiones suaves,
                  marcas BOM, caracteres de etiqueta, espacios de no separación.
                  Sobreviven al copiar y pegar y son la huella más mecánica de
                  un texto generado.
  2. TIPOGRAFÍA   raya -> coma, semirraya -> guion, comillas curvas -> rectas,
                  carácter de puntos suspensivos -> tres puntos, viñeta -> guion.
                  La raya de diálogo al empezar una línea se respeta, y las
                  comillas angulares « » no se tocan: las dos son correctas en
                  español.
  3. LÉXICO       reemplaza la lista de relleno.json con palabras simples,
                  sin importar tildes ni mayúsculas, conservando la mayúscula
                  inicial y sin tocar enlaces.

Las estructuras que delatan ("no es solo X, es Y", tríos, muros de hashtags) se
REPORTAN y nunca se reescriben solas: cambiar la forma de una frase necesita
criterio, y eso le toca a quien escribe, no a una expresión regular.

Uso
  python3 humanizar.py borrador.txt
  python3 humanizar.py borrador.txt --reporte
  python3 humanizar.py borrador.txt -o limpio.txt --reporte
  python3 humanizar.py borrador.txt --json
  cat borrador.txt | python3 humanizar.py - --reporte
"""

import argparse
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "relleno.json")

URL_RE = re.compile(r"https?://\S+|www\.\S+|\S+@\S+\.\S+")
SENT_RE = re.compile(r"[^.!?\n]+[.!?]*")
QUITAR_TILDES = str.maketrans("áéíóúüÁÉÍÓÚÜ", "aeiouuAEIOUU")
VOCALES = {"a": "[aá]", "e": "[eé]", "i": "[ií]", "o": "[oó]", "u": "[uúü]"}


def sin_tildes(texto):
    return texto.translate(QUITAR_TILDES).lower()


def patron(buscar):
    """Expresión que encuentra la frase con o sin tildes y con cualquier espacio."""
    base = sin_tildes(buscar)
    partes = []
    for ch in base:
        if ch in VOCALES:
            partes.append(VOCALES[ch])
        elif ch == " ":
            partes.append(r"\s+")
        else:
            partes.append(re.escape(ch))
    izq = r"\b" if base[:1].isalnum() else ""
    der = r"\b" if base[-1:].isalnum() else ""
    return re.compile(izq + "".join(partes) + der, re.IGNORECASE)


def load_lexicon(path=LEX):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _cp(spec):
    """'U+200B' -> 0x200b;  'U+E0000-U+E007F' -> (inicio, fin)."""
    if "-" in spec:
        a, b = spec.split("-")
        return (int(a[2:], 16), int(b[2:], 16))
    return int(spec[2:], 16)


def protect_urls(text):
    """Cambia los enlaces por marcadores para que ninguna pasada los toque."""
    found = []

    def stash(m):
        found.append(m.group(0))
        return f"\x00URL{len(found) - 1}\x00"

    return URL_RE.sub(stash, text), found


def restore_urls(text, found):
    for i, url in enumerate(found):
        text = text.replace(f"\x00URL{i}\x00", url)
    return text


def pass_invisible(text, lex):
    """Borra o vuelve espacio normal los caracteres invisibles. Devuelve (texto, hallazgos)."""
    hits = []
    for entry in lex["invisibles"]:
        cp = _cp(entry["cp"])
        if isinstance(cp, tuple):
            pattern = "[" + re.escape(chr(cp[0])) + "-" + re.escape(chr(cp[1])) + "]"
        else:
            pattern = re.escape(chr(cp))
        n = len(re.findall(pattern, text))
        if n:
            hits.append({"name": entry["cp"] + " " + entry["name"], "count": n,
                         "action": entry["action"]})
            text = re.sub(pattern, "" if entry["action"] == "borrar" else " ", text)
    # Cualquier otro carácter de formato (categoría Cf) es invisible por definición.
    stray = [c for c in text if unicodedata.category(c) == "Cf"]
    if stray:
        hits.append({"name": "otros caracteres de formato invisibles", "count": len(stray),
                     "action": "borrar"})
        text = "".join(c for c in text if unicodedata.category(c) != "Cf")
    return text, hits


def _quitar_rayas(linea):
    """Raya en medio de la frase -> coma. La raya de diálogo al inicio de línea se queda."""
    m = re.match(r"(\s*—)(.*)", linea, re.S)
    if m:
        return m.group(1) + re.sub(r"\s*—\s*", ", ", m.group(2))
    return re.sub(r"\s*—\s*", ", ", linea)


def contar_rayas(text):
    """Rayas que no son de diálogo (las de diálogo empiezan la línea)."""
    return sum(len(re.findall("—", re.sub(r"^\s*—", "", l))) for l in text.split("\n"))


def pass_typographic(text, lex):
    hits = []
    for entry in lex["tipografia"]:
        ch = entry["from"]
        n = contar_rayas(text) if ch == "—" else text.count(ch)
        if not n:
            continue
        hits.append({"name": f"{ch} {entry['name']}", "count": n, "to": entry["to"].strip() or "(espacio)"})
        if ch == "—":
            text = "\n".join(_quitar_rayas(l) for l in text.split("\n"))
        elif ch == "–":
            text = re.sub(r"\s*–\s*(?=\d)", "-", text)      # 5–10  -> 5-10
            text = re.sub(r"\s+–\s+", ", ", text)            # usada como raya
            text = text.replace("–", "-")
        else:
            text = text.replace(ch, entry["to"])
    # Una coma pegada antes de otro signo se ve mal.
    text = re.sub(r",\s*([,.;:!?])", r"\1", text)
    text = re.sub(r",\s*\n", "\n", text)
    return text, hits


def _match_case(src, repl):
    if not repl:
        return repl
    if src.isupper() and len(src) > 1:
        return repl.upper()
    if src[0].isupper():
        return repl[0].upper() + repl[1:]
    return repl


def pass_lexical(text, lex):
    """Reemplaza palabras y frases de relleno. Las más largas primero, para que ganen las frases."""
    hits = []
    entries = sorted(lex["frases"] + lex["palabras"],
                     key=lambda e: len(e["buscar"]), reverse=True)
    for entry in entries:
        pattern = patron(entry["buscar"])
        found = pattern.findall(text)
        if not found:
            continue
        hits.append({"find": entry["buscar"], "replace": entry["reemplazo"] or "(borrada)",
                     "count": len(found), "family": entry["familia"]})
        text = pattern.sub(lambda m: _match_case(m.group(0), entry["reemplazo"]), text)
    # Limpieza después de borrar. Borrar una frase entera deja signos sueltos
    # ("sistema. ." o una línea que ahora empieza con coma), y eso se ve peor
    # que el relleno.
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"(?m)^[ \t]*(?:[,.;:]+[ \t]*)+", "", text)
    text = re.sub(r"(?m)^[ \t](?=\S)", "", text)       # un espacio que dejó un borrado.
                                                      # Las sangrías más hondas son a propósito.
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    text = re.sub(r",\s*([,.;:!?])", r"\1", text)      # una raya que se volvió coma
                                                      # y luego se borró lo que seguía
    text = re.sub(r"([¿¡])\s*,\s*", r"\1", text)       # "¿, hoy..." -> "¿hoy..."
    text = text.replace("...", "\x00ELL\x00")          # protege los puntos suspensivos reales
    text = re.sub(r"\.\s*\.+", ".", text)
    text = re.sub(r"([!?])\s*\.", r"\1", text)
    text = text.replace("\x00ELL\x00", "...")
    text = re.sub(r"(?m)^[ \t]+$", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Una raya que se volvió coma, seguida de un conector, deja dos frases
    # pegadas ("es importante, además, es prueba"). Se vuelve punto seguido.
    text = re.sub(r",\s*(además|también|así que|aun así|al final|básicamente)\s*,\s*",
                  lambda m: ". " + m.group(1)[0].upper() + m.group(1)[1:] + ", ", text)
    return text, hits


def scan_structures(text, lex):
    flags = []
    for s in lex["estructuras"]:
        try:
            pattern = re.compile(s["regex"], re.MULTILINE)
        except re.error:
            continue
        found = pattern.findall(text)
        if found:
            flags.append({"name": s["name"], "count": len(found), "fix": s["fix"]})
    # Que todas las frases midan lo mismo también es una estructura.
    lens = [len(s.split()) for s in SENT_RE.findall(text) if len(s.split()) > 2]
    if len(lens) >= 4:
        mean = sum(lens) / len(lens)
        var = sum((n - mean) ** 2 for n in lens) / len(lens)
        cv = (var ** 0.5) / mean if mean else 0
        if cv < 0.35:
            flags.append({
                "name": f"Frases del mismo largo (variación {cv:.2f})",
                "count": len(lens),
                "fix": "Parte una frase en dos. Deja que otra se alargue. Las máquinas escriben parejo.",
            })
    return flags


INICIO = r"[¿¡\"“«(]*"


def restore_capitals(original, text):
    """Borrar el arranque de una frase deja la siguiente palabra en minúscula.

    Solo se arregla si quien escribe usa mayúscula al empezar sus frases: escribir
    todo en minúscula a propósito es un estilo, no una huella, y gritarle encima
    sería justo lo que este programa existe para evitar.
    """
    starts = re.findall(r"(?:^|[.!?]\s+|\n)\s*" + INICIO + r"([^\W\d_])", original)
    if not starts or sum(1 for c in starts if c.isupper()) * 2 < len(starts):
        return text
    return re.sub(r"(?:^|(?<=[.!?] )(?<!\.\. )|(?<=[.!?]\n)|(?<=\n))(\s*" + INICIO + r")([a-záéíóúñü])",
                  lambda m: m.group(1) + m.group(2).upper(), text)


def humanize(text, lex):
    raw_for_case = text
    text, urls = protect_urls(text)
    text, inv = pass_invisible(text, lex)
    text, typo = pass_typographic(text, lex)
    text, lexi = pass_lexical(text, lex)
    text = restore_capitals(raw_for_case, text)
    text = restore_urls(text, urls)
    return text.strip() + "\n", {
        "invisible": inv,
        "typographic": typo,
        "lexical": lexi,
        "structures": scan_structures(text, lex),
    }


def render_report(report, out=sys.stderr):
    def head(title):
        print(f"\n{title}\n" + "-" * len(title), file=out)

    total = sum(h["count"] for h in report["invisible"]) \
        + sum(h["count"] for h in report["typographic"]) \
        + sum(h["count"] for h in report["lexical"])

    head("REPORTE DE HUMANIZACIÓN")
    print(f"{total} huellas de máquina quitadas, "
          f"{len(report['structures'])} estructura(s) marcada(s) para reescribir", file=out)

    if report["invisible"]:
        head("1. CARACTERES INVISIBLES")
        for h in report["invisible"]:
            print(f"  {h['count']:>3}x  {h['name']}  -> {h['action']}", file=out)
    if report["typographic"]:
        head("2. TIPOGRAFÍA")
        for h in report["typographic"]:
            print(f"  {h['count']:>3}x  {h['name']}  -> {h['to']}", file=out)
    if report["lexical"]:
        head("3. PALABRAS DE RELLENO")
        for h in report["lexical"]:
            print(f"  {h['count']:>3}x  {h['find']}  -> {h['replace']}   [{h['family']}]", file=out)
    if report["structures"]:
        head("4. ESTRUCTURAS QUE DELATAN  (no se arreglan solas: reescríbelas tú)")
        for h in report["structures"]:
            print(f"  {h['count']:>3}x  {h['name']}\n        {h['fix']}", file=out)
    if not any(report.values()):
        head("LIMPIO")
        print("  No hay nada que quitar.", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Quita de un borrador las huellas de texto hecho por máquina.")
    ap.add_argument("input", nargs="?", default="-", help="archivo, o - para leer de la entrada")
    ap.add_argument("-o", "--out", "--salida", dest="out", help="guarda el texto limpio aquí")
    ap.add_argument("--reporte", "--report", dest="reporte", action="store_true",
                    help="muestra qué cambió")
    ap.add_argument("--json", action="store_true", help="devuelve {text, report} en JSON")
    ap.add_argument("--lista", "--lexicon", dest="lista", default=LEX, help="ruta de relleno.json")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    lex = load_lexicon(args.lista)
    clean, report = humanize(raw, lex)

    if args.json:
        print(json.dumps({"text": clean, "report": report}, indent=2, ensure_ascii=False))
        return
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(clean)
        print(f"guardado en {args.out}", file=sys.stderr)
    else:
        sys.stdout.write(clean)
    if args.reporte:
        render_report(report)


if __name__ == "__main__":
    main()
