#!/usr/bin/env python3
"""
detectar.py - cinco revisiones que califican qué tanto parece escrito por
máquina un borrador.

Basado en detect.py de instagram-agent-skill, de Jake Schincariol (licencia
MIT). Traducción y adaptación al español: Juan Sebastian Cruz - 1691 Agency.

Qué es:  cinco reglas simples basadas en las señales que miden los detectores
públicos de texto hecho con IA: variación en el largo de las frases, datos
concretos, vocabulario de relleno, huellas tipográficas y voz. Todo se calcula
en tu equipo, solo con el texto. No se sube nada.

Qué NO es:  GPTZero, Originality, Copyleaks, Winston ni Turnitin. No llama a
esos servicios y no puede prometer lo que ellos digan. Revisa las cosas en las
que todos se fijan, y por eso arreglarlas suele mover también sus números, pero
lo único que se puede afirmar con honestidad es lo que dice esta línea.

Diferencia con el original en inglés: allá la revisión de VOZ cuenta
contracciones ("don't", "it's"), que en español no existen. Aquí se reemplazó
por marcas de habla cotidiana ("o sea", "la verdad", "pues", "ojo"...). Y como
en español casi nunca se dice el pronombre, la persona gramatical cuenta también
los verbos en "nosotros" ("tostamos", "pensábamos"). Son reglas nuevas para el
español y no se han medido contra textos reales.

Cada revisión da un puntaje HUMANO de 0 a 100. Más alto es mejor.

Uso
  python3 detectar.py borrador.txt
  python3 detectar.py borrador.txt --json
  python3 detectar.py antes.txt despues.txt      # compara dos versiones
  cat borrador.txt | python3 detectar.py -
"""

import argparse
import json
import os
import re
import statistics
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "relleno.json")

SENT_RE = re.compile(r"[^.!?\n]+[.!?]*")
WORD_RE = re.compile(r"[^\W\d_]+")
NUMBERS = re.compile(r"\b\d[\d.,]*%?|\$\s?\d")
MAYUSCULA_RE = re.compile(r"\b[A-ZÁÉÍÓÚÑÜ][a-záéíóúñü]{2,}\b")
QUITAR_TILDES = str.maketrans("áéíóúüÁÉÍÓÚÜ", "aeiouuAEIOUU")
VOCALES = {"a": "[aá]", "e": "[eé]", "i": "[ií]", "o": "[oó]", "u": "[uúü]"}

# Marcas de habla cotidiana. Se buscan en minúsculas y sin tildes.
COLOQUIAL = re.compile(
    r"\b(?:pues|o sea|osea|bueno|la verdad|igual|ojo|eso si|en serio|obvio|de verdad|"
    r"ni idea|jaja\w*|uff+|uy|ay|ya|listo|dale|vale|tipo|mejor dicho|de una|ni modo|"
    r"que pena|que bueno|que rico|super|re)\b")
PRONOMBRES = re.compile(
    r"\b(?:yo|me|mi|mis|conmigo|nos|nosotros|nosotras|nuestro|nuestra|nuestros|"
    r"nuestras|tu|tus|te|ti|contigo|usted|ustedes|vos)\b")
# En español casi nunca se dice el pronombre: "tostamos" ya es "nosotros".
# Se cuentan los verbos en primera persona del plural, menos algunos
# sustantivos que terminan igual.
NOSOTROS = re.compile(r"\b\w+(?:amos|emos)\b")
NO_SON_VERBOS = {"amos", "gramos", "kilogramos", "miligramos", "ramos", "tramos",
                 "reclamos", "prestamos", "extremos", "supremos", "remos", "memos"}


def sin_tildes(texto):
    return texto.translate(QUITAR_TILDES).lower()


def patron(buscar):
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


def clamp(n):
    return max(0.0, min(100.0, n))


def scale(value, human, machine):
    """Lleva el valor a 0-100, donde `human` -> 100 y `machine` -> 0."""
    if human == machine:
        return 50.0
    return clamp((value - machine) / (human - machine) * 100)


def sentences(text):
    return [s.strip() for s in SENT_RE.findall(text) if len(s.split()) > 2]


def words(text):
    return WORD_RE.findall(text)


def nombres_propios(text):
    out = set()
    for m in MAYUSCULA_RE.finditer(text):
        antes = text[:m.start()].rstrip(" \t\"“'«(")
        if antes and antes[-1] not in ".!?¿¡…\n":
            out.add(m.group(0))
    return out


def check_burstiness(text):
    """La gente varía mucho el largo de sus frases. Las máquinas escriben parejo."""
    lens = [len(s.split()) for s in sentences(text)]
    if len(lens) < 4:
        return 50.0, "muy corto para juzgar"
    mean = statistics.mean(lens)
    cv = statistics.pstdev(lens) / mean if mean else 0
    score = scale(cv, human=0.70, machine=0.22)
    return score, f"variación {cv:.2f} en {len(lens)} frases (ideal 0,55 o más)"


def check_specificity(text):
    """Cifras, nombres y cosas concretas. El relleno es abstracto."""
    w = words(text)
    if len(w) < 25:
        return 50.0, "muy corto para juzgar"
    per100 = 100 / len(w)
    hits = len(NUMBERS.findall(text)) + len(nombres_propios(text))
    density = hits * per100
    score = scale(density, human=6.0, machine=0.5)
    return score, f"{hits} dato(s) concreto(s), {density:.1f} por cada 100 palabras (ideal 4 o más)"


def check_slop(text, lex):
    """Densidad de vocabulario de relleno según la lista."""
    w = words(text)
    if not w:
        return 50.0, "vacío"
    hits, found = 0, []
    # De la más larga a la más corta, tapando lo ya contado, para que
    # "asimismo," y "asimismo" no cuenten dos veces la misma palabra.
    resto = text
    for entry in sorted(lex["palabras"] + lex["frases"], key=lambda e: -len(e["buscar"])):
        pattern = patron(entry["buscar"])
        n = len(pattern.findall(resto))
        if n:
            hits += n
            found.append(entry["buscar"].rstrip(",;:. "))
            resto = pattern.sub(lambda m: "\x00" * len(m.group(0)), resto)
    density = hits * 100 / len(w)
    score = scale(density, human=0.0, machine=4.0)
    detail = f"{hits} términos de relleno, {density:.1f} por cada 100 palabras"
    if found:
        detail += " (" + ", ".join(sorted(found)[:4]) + (", ..." if len(found) > 4 else "") + ")"
    return score, detail


def check_fingerprint(text):
    """Caracteres que el teclado de un celular no produce."""
    invisible = sum(1 for c in text if unicodedata.category(c) == "Cf")
    # La raya de diálogo al empezar una línea es correcta en español: no cuenta.
    em = sum(len(re.findall("—", re.sub(r"^\s*—", "", l))) for l in text.split("\n"))
    curly = sum(text.count(c) for c in "‘’“”")
    ellip = text.count("…")
    nbsp = sum(text.count(c) for c in "\u00a0\u202f\u2009\u2007")
    total = invisible * 4 + em * 2 + curly + ellip + nbsp
    per1k = total * 1000 / max(len(text), 1)
    score = scale(per1k, human=0.0, machine=12.0)
    detail = (f"{invisible} invisibles, {em} rayas, {curly} comillas curvas, "
              f"{ellip} puntos suspensivos en un carácter, {nbsp} espacios duros")
    return score, detail


def check_voice(text, lex):
    """Habla cotidiana, persona gramatical y las formas que las máquinas usan por defecto."""
    w = words(text)
    if len(w) < 25:
        return 50.0, "muy corto para juzgar"
    low = sin_tildes(text)
    per100 = 100 / len(w)
    coloquial = len(COLOQUIAL.findall(low)) * per100
    nosotros = [x for x in NOSOTROS.findall(low) if x not in NO_SON_VERBOS]
    person = (len(PRONOMBRES.findall(low)) + len(nosotros)) * per100
    tells = 0
    names = []
    for s in lex["estructuras"]:
        try:
            n = len(re.compile(s["regex"], re.MULTILINE).findall(text))
        except re.error:
            continue
        if n:
            tells += n
            names.append(s["id"])
    bullets = [len(b.split()) for b in re.findall(r"(?m)^\s*[-*•]\s+(.+)$", text)]
    uniform = (len(bullets) >= 3 and statistics.pstdev(bullets) < 1.6)
    score = (scale(coloquial, human=2.0, machine=0.0) * 0.35
             + scale(person, human=6.0, machine=1.0) * 0.35
             + clamp(100 - tells * 22) * 0.30)
    if uniform:
        score -= 12
        names.append("vinetas-parejas")
    detail = (f"{coloquial:.1f} marcas de habla cotidiana, {person:.1f} marcas de primera o "
              f"segunda persona por cada 100 palabras, {tells} estructura(s) que delatan")
    if names:
        detail += " [" + ", ".join(names[:4]) + "]"
    return clamp(score), detail


CHECKS = ["VARIACIÓN", "CONCRECIÓN", "RELLENO", "HUELLAS", "VOZ"]


def run(text, lex):
    results = {}
    results["VARIACIÓN"] = check_burstiness(text)
    results["CONCRECIÓN"] = check_specificity(text)
    results["RELLENO"] = check_slop(text, lex)
    results["HUELLAS"] = check_fingerprint(text)
    results["VOZ"] = check_voice(text, lex)
    scores = [results[c][0] for c in CHECKS]
    # La revisión más débil arrastra el resultado: a un detector le basta una señal.
    overall = statistics.mean(scores) * 0.6 + min(scores) * 0.4
    verdict = "PASA" if overall >= 70 and min(scores) >= 55 else (
        "REVISAR" if overall >= 50 else "MARCADO")
    return results, overall, verdict


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render(results, overall, verdict, label=None, out=sys.stdout):
    title = "PANEL DE DETECCIÓN" + (f"  -  {label}" if label else "")
    print("\n" + title, file=out)
    print("=" * max(len(title), 62), file=out)
    for name in CHECKS:
        score, detail = results[name]
        print(f"  {name:<13} {bar(score)} {score:5.1f}", file=out)
        print(f"  {'':<13} {detail}", file=out)
    print("-" * 62, file=out)
    print(f"  {'HUMANO':<13} {bar(overall)} {overall:5.1f}   {verdict}", file=out)
    if verdict != "PASA":
        weakest = min(CHECKS, key=lambda c: results[c][0])
        print(f"\n  Señal más débil: {weakest}. Arregla esa primero.", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Califica qué tanto parece escrito por máquina un borrador.")
    ap.add_argument("input", nargs="?", default="-", help="archivo, o - para leer de la entrada")
    ap.add_argument("compare", nargs="?", help="segundo archivo, para ver el antes y el después")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--lista", "--lexicon", dest="lista", default=LEX, help="ruta de relleno.json")
    args = ap.parse_args()

    lex = json.load(open(args.lista, encoding="utf-8"))
    read = lambda p: sys.stdin.read() if p == "-" else open(p, encoding="utf-8").read()

    targets = [(args.input, read(args.input))]
    if args.compare:
        targets.append((args.compare, read(args.compare)))

    payload = []
    for name, text in targets:
        results, overall, verdict = run(text, lex)
        payload.append({
            "source": name,
            "checks": {k: {"score": round(v[0], 1), "detail": v[1]} for k, v in results.items()},
            "human_score": round(overall, 1),
            "verdict": verdict,
        })

    if args.json:
        print(json.dumps(payload if args.compare else payload[0], indent=2, ensure_ascii=False))
        return

    for (name, text), p in zip(targets, payload):
        results, overall, verdict = run(text, lex)
        render(results, overall, verdict, label=os.path.basename(name) if args.compare else None)
    if args.compare:
        a, b = payload
        delta = b["human_score"] - a["human_score"]
        print(f"  {a['human_score']:.1f} {a['verdict']}  ->  "
              f"{b['human_score']:.1f} {b['verdict']}   ({delta:+.1f})\n")

    sys.exit(0 if payload[-1]["verdict"] == "PASA" else 1)


if __name__ == "__main__":
    main()
