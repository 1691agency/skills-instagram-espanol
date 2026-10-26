#!/usr/bin/env python3
"""
tiempos.py - convierte el guion de un Reel en una hoja de tiempos antes de grabar.

Basado en beats.py de instagram-agent-skill, de Jake Schincariol (licencia
MIT). Traducción y adaptación al español: Juan Sebastian Cruz - 1691 Agency.

Calcula cuánto se demora cada línea en decirse, las va sumando en tiempos y
marca las cuatro cosas que matan un Reel en la edición: un gancho que pasa de
tres segundos, una parte tan larga que la gente se va, varias líneas seguidas
sin nada concreto y una duración que no coincide con lo que dijiste que ibas a
hacer.

Los tiempos son un cálculo a partir del número de palabras y una velocidad en
palabras por minuto. Sirven para planear la edición, no reemplazan grabar.
Ajusta tu propia velocidad con --ppm después de cronometrarte leyendo un guion
en voz alta: la mayoría de la gente está entre 150 y 200, y aquí se usa 165.

Uso
  python3 tiempos.py guion.txt
  python3 tiempos.py guion.txt --objetivo 30
  python3 tiempos.py guion.txt --ppm 185 --objetivo 45
  python3 tiempos.py guion.txt --json
  cat guion.txt | python3 tiempos.py -
"""

import argparse
import json
import re
import sys

WORD_RE = re.compile(r"[^\W_]+(?:[$%'’-][^\W_]+)*%?|\$[\d]+%?", re.UNICODE)
SENT_RE = re.compile(r"[^.!?]+[.!?]*")
NUMERO_RE = re.compile(r"\$\s?\d|\b\d[\d.,]*\b")
MAYUSCULA_RE = re.compile(r"\b[A-ZÁÉÍÓÚÑÜ][a-záéíóúñü]{2,}\b")
QUITAR_TILDES = str.maketrans("áéíóúüÁÉÍÓÚÜ", "aeiouuAEIOUU")

NUMEROS_HABLADOS = {
    "cero", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve",
    "diez", "once", "doce", "trece", "catorce", "quince", "veinte", "treinta",
    "cuarenta", "cincuenta", "sesenta", "setenta", "ochenta", "noventa", "cien",
    "ciento", "cientos", "quinientos", "mil", "millon", "millones", "docena",
    "mitad", "doble", "triple", "pesos", "dolares", "lucas", "palos",
}

PALABRAS_VACIAS = {
    "el", "la", "los", "las", "un", "una", "unos", "unas", "y", "o", "u", "e",
    "pero", "si", "de", "del", "a", "al", "en", "con", "por", "para", "que",
    "este", "esta", "esto", "estos", "estas", "ese", "esa", "eso", "es", "son",
    "era", "fue", "ser", "te", "tu", "tus", "yo", "mi", "mis", "me", "nos",
    "lo", "le", "les", "se", "su", "sus", "no", "ni", "ya", "mas", "muy",
    "como", "cuando", "donde", "porque", "hay", "tiene", "hace", "uno", "todo",
    "todos", "sin", "sobre", "hasta", "desde", "asi", "solo", "tan", "aqui",
    "ahi", "ahora", "hoy", "voy", "vas", "va",
}

HOOK_WINDOW = 3.0        # segundos. Después de esto, el dedo ya decidió.
MAX_BEAT = 4.0           # segundos en una sola idea sin cambio en pantalla.
ABSTRACT_RUN = 3         # partes seguidas sin nada comprobable.


def sin_tildes(texto):
    return texto.translate(QUITAR_TILDES).lower()


def words(text):
    # "$18.000.000" es una sola palabra cuando se dice, así que aquí también.
    return WORD_RE.findall(re.sub(r"(?<=\d)[.,](?=\d)", "", text))


def concretos(text):
    """Cifras, nombres propios y números dichos con palabras."""
    n = len(NUMERO_RE.findall(text))
    for m in MAYUSCULA_RE.finditer(text):
        antes = text[:m.start()].rstrip(" \t\"“'«(")
        if antes and antes[-1] not in ".!?¿¡…\n":
            n += 1
    n += sum(1 for w in words(text) if sin_tildes(w) in NUMEROS_HABLADOS
             or sin_tildes(w).startswith(("veinti", "dieci")))
    return n


def pretty(token):
    """Vuelve a poner el separador de miles para mostrarlo."""
    return re.sub(r"(\d)(?=(\d{3})+$)", r"\1.", token)


def tc(seconds):
    m, s = divmod(seconds, 60)
    return f"{int(m)}:{s:04.1f}"


def split_beats(raw, wps):
    """Una línea es una parte, salvo que la línea sea demasiado larga."""
    beats = []
    for line in [l.strip() for l in raw.splitlines()]:
        if not line:
            continue
        if len(words(line)) / wps <= MAX_BEAT * 1.5:
            beats.append(line)
            continue
        # Párrafo largo: se corta en los finales de oración para que los
        # tiempos signifiquen algo.
        parts = [p.strip() for p in SENT_RE.findall(line) if p.strip()]
        buf = ""
        for part in parts:
            candidate = (buf + " " + part).strip()
            if buf and len(words(candidate)) / wps > MAX_BEAT:
                beats.append(buf)
                buf = part
            else:
                buf = candidate
        if buf:
            beats.append(buf)
    return beats


def analyse(raw, wpm=165, target=None):
    wps = wpm / 60.0
    beats = split_beats(raw, wps)
    if not beats:
        return None

    rows, clock = [], 0.0
    for i, text in enumerate(beats):
        n = len(words(text))
        dur = n / wps
        rows.append({
            "n": i + 1,
            "start": round(clock, 2),
            "dur": round(dur, 2),
            "words": n,
            "text": text,
            "concrete": concretos(text),
            "label": "",
            "flags": [],
        })
        clock += dur
    total = clock

    # Marca las posiciones sobre las que de verdad se construye un Reel.
    for r in rows:
        if r["n"] == 1 or r["start"] + r["dur"] <= HOOK_WINDOW:
            r["label"] = "GANCHO"
    rows[-1]["label"] = "CIERRE" if rows[-1]["label"] != "GANCHO" else "GANCHO/CIERRE"
    half = total / 2
    for r in rows:
        if not r["label"] and r["start"] <= half < r["start"] + r["dur"]:
            r["label"] = "MITAD"

    notes = []
    if rows[0]["dur"] > HOOK_WINDOW:
        rows[0]["flags"].append(f"el gancho dura {rows[0]['dur']:.1f} s, pasa de los {HOOK_WINDOW:.0f} s")
        notes.append(f"La parte 1 se demora {rows[0]['dur']:.1f} s en decirse. Déjala en "
                     f"{int(HOOK_WINDOW * wps)} palabras o menos, o el gancho llega después "
                     "de que la persona ya decidió.")
    if rows[0]["concrete"] == 0:
        notes.append("La parte 1 no tiene ni una cifra ni un nombre. Los ganchos sin algo "
                     "comprobable son los que se pasan de largo.")

    for r in rows:
        if r["dur"] > MAX_BEAT:
            r["flags"].append(f"{r['dur']:.1f} s en una sola parte")
    long_beats = [r["n"] for r in rows if r["dur"] > MAX_BEAT]
    if long_beats:
        notes.append(f"La(s) parte(s) {', '.join(map(str, long_beats))} pasan de {MAX_BEAT:.0f} s. "
                     "Divide la línea o cambia lo que se ve en pantalla en la mitad. "
                     "Un plano quieto es donde la gente se va.")

    run, start = 0, None
    for r in rows:
        if r["concrete"] == 0:
            run += 1
            start = start if start is not None else r["n"]
            if run == ABSTRACT_RUN:
                notes.append(f"Las partes {start}-{r['n']} no tienen nada concreto. "
                             "Pon una cifra, un nombre o un precio en alguna.")
        else:
            run, start = 0, None

    # ¿La última línea te devuelve a la primera?
    def claves(texto):
        return {sin_tildes(w): w for w in words(texto) if sin_tildes(w) not in PALABRAS_VACIAS}
    first, last = claves(rows[0]["text"]), claves(rows[-1]["text"])
    loop = sorted(pretty(first[k]) for k in set(first) & set(last))
    if loop:
        notes.append(f"Hay bucle: la última parte repite \"{', '.join(loop[:3])}\" del gancho. "
                     "Las segundas vistas son alcance gratis.")
    else:
        notes.append("No hay bucle. La última parte no comparte ninguna palabra con el gancho, "
                     "así que el video termina plano. Repetir una palabra de la parte 1 es la "
                     "segunda vista más barata que vas a conseguir.")

    if target:
        delta = total - target
        if abs(delta) <= target * 0.1:
            notes.append(f"La duración está en el objetivo ({total:.1f} s frente a {target:g} s).")
        elif delta > 0:
            notes.append(f"{delta:.1f} s por encima del objetivo. Corta unas {int(delta * wps)} palabras.")
        else:
            notes.append(f"{-delta:.1f} s por debajo del objetivo. Agrega {int(-delta * wps)} palabras "
                         "o grábalo más corto. Más corto casi siempre es mejor.")

    return {
        "wpm": wpm, "target": target,
        "total_seconds": round(total, 2),
        "total_words": sum(r["words"] for r in rows),
        "beats": rows,
        "notes": notes,
    }


def render(a, out=sys.stdout):
    head = (f"HOJA DE TIEMPOS  ·  {a['total_words']} palabras  ·  ~{a['total_seconds']:.1f} s "
            f"a {a['wpm']:g} ppm" + (f"  ·  objetivo {a['target']:g} s" if a["target"] else ""))
    print("\n" + head, file=out)
    print("=" * max(len(head), 72), file=out)
    for r in a["beats"]:
        label = f"{r['label']:<14}" if r["label"] else " " * 14
        print(f"  {tc(r['start'])}  {r['dur']:4.1f}s  {label}{r['text']}", file=out)
        for f in r["flags"]:
            print(f"  {'':>6}  {'':>5}  {'':<14}^ {f}", file=out)
    print("-" * max(len(head), 72), file=out)
    for n in a["notes"]:
        print(f"  - {n}", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Convierte el guion de un Reel en una hoja de tiempos.")
    ap.add_argument("input", nargs="?", default="-", help="archivo del guion, o - para leer de la entrada")
    ap.add_argument("--ppm", "--wpm", dest="ppm", type=float, default=165,
                    help="velocidad al hablar en palabras por minuto (165 por defecto)")
    ap.add_argument("--objetivo", "--target", dest="objetivo", type=float,
                    help="duración objetivo en segundos")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    a = analyse(raw, wpm=args.ppm, target=args.objetivo)
    if not a:
        print("el guion está vacío", file=sys.stderr)
        sys.exit(2)
    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    sys.exit(0)


if __name__ == "__main__":
    main()
