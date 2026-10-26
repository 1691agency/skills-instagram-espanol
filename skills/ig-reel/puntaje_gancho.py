#!/usr/bin/env python3
"""
puntaje_gancho.py - califica la primera frase de un Reel en las cinco cosas que
tienen en común los ganchos fuertes, y ordena varios ganchos entre sí.

Basado en hookscore.py de instagram-agent-skill, de Jake Schincariol (licencia
MIT). Traducción y adaptación al español: Juan Sebastian Cruz - 1691 Agency.

Qué es:  cinco reglas simples que se calculan en tu equipo, solo con el texto.
Miden cosas que suelen tener los ganchos que retienen: que se puedan decir en
menos de tres segundos, que tengan algo concreto, que haya algo en juego, que
lo importante vaya al principio y que le hablen a alguien.

Qué NO es:  un predictor de vistas. El autor original lo probó en inglés con
74 ganchos reales: separa bien un gancho real de uno escrito para ser malo,
pero entre los aciertos y los fracasos de un mismo creador acierta casi como
lanzar una moneda. Esta versión en español usa listas de palabras nuevas,
hechas para el español, que NO se han medido contra ganchos reales en español.

Úsalo para lo que sí hace bien: detectar saludos, introducciones, ganchos sin
nada concreto y ganchos que tardan cinco segundos en decirse. No te va a decir
cuál de dos ganchos decentes va a funcionar. Eso lo deciden tu cara, tu edición,
tu audio y a quién se lo muestra Instagram. Confía más en tu gráfica de
retención que en este programa.

Cada revisión da de 0 a 100. Más alto es mejor.

Uso
  python3 puntaje_gancho.py opciones.txt          # un gancho por línea, ordenados
  python3 puntaje_gancho.py --gancho "Perdí 18 millones por una cláusula."
  python3 puntaje_gancho.py opciones.txt --json
  cat opciones.txt | python3 puntaje_gancho.py -
"""

import argparse
import json
import re
import statistics
import sys

# Letras del español (con tildes, ñ y ü), números y los signos que van pegados
# a una cifra hablada. ¿ y ¡ no cuentan como palabra.
WORD_RE = re.compile(r"[^\W_]+(?:[$%'’-][^\W_]+)*%?|\$[\d]+%?", re.UNICODE)
UNIDADES = (r"%|k\b|x\b|mil\b|millones\b|millon\b|millón\b|h\b|horas?\b|min\b|minutos?\b"
            r"|seg\b|segundos?\b|d[ií]as?\b|semanas?\b|mes(?:es)?\b|a[ñn]os?\b"
            r"|pesos\b|d[oó]lares\b|usd\b|cop\b|euros?\b")
NUMBER_RE = re.compile(
    r"\$\s?\d[\d.,]*"                                   # dinero
    r"|\b\d[\d.,]*\s?(?:" + UNIDADES + r")?",           # una cifra, con o sin unidad
    re.IGNORECASE)
MAYUSCULA_RE = re.compile(r"\b[A-ZÁÉÍÓÚÑÜ][a-záéíóúñü]{2,}\b")
HASHTAG_RE = re.compile(r"(?:^|\s)#\w+")
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿]")

QUITAR_TILDES = str.maketrans("áéíóúüÁÉÍÓÚÜ", "aeiouuAEIOUU")


def sin_tildes(texto):
    """Minúsculas y sin tildes, para comparar. La ñ se conserva."""
    return texto.translate(QUITAR_TILDES).lower()


# Los ganchos hablados dicen las cifras en voz alta. "Cero pesos" y "veinte
# millones" son tan concretos como "$0" y "$20.000.000". "Uno", "una" y
# "primero" se dejan fuera a propósito: casi siempre son relleno.
NUMEROS_HABLADOS = {
    "cero", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve",
    "diez", "once", "doce", "trece", "catorce", "quince", "veinte", "treinta",
    "cuarenta", "cincuenta", "sesenta", "setenta", "ochenta", "noventa", "cien",
    "ciento", "cientos", "doscientos", "trescientos", "cuatrocientos", "quinientos",
    "seiscientos", "setecientos", "ochocientos", "novecientos", "mil", "millon",
    "millones", "billon", "docena", "mitad", "doble", "triple",
}
PALABRAS_DINERO = {
    "pesos", "peso", "dolares", "dolar", "euros", "euro", "lucas", "palos",
    "centavos", "porcentaje", "millonario", "millonaria", "ventas", "facturacion",
    "ganancia", "ganancias", "utilidad", "utilidades", "sueldo", "salario",
    "arriendo", "alquiler", "deuda", "deudas", "precio",
}

# Palabras que ponen algo en juego. Un gancho sin ninguna es una afirmación;
# con una, es una razón para seguir mirando.
TENSION = {
    "no", "nunca", "jamas", "nadie", "nada", "ni", "error", "errores",
    "equivocado", "equivocada", "equivoque", "perdi", "perdimos", "perder",
    "pierdes", "pierde", "perdiendo", "perdida", "perdidas", "costo", "cuesta",
    "cuestan", "costaron", "quebre", "quiebra", "quebrado", "fracase", "fracaso",
    "fracasar", "falle", "falla", "fallo", "deja", "dejen", "renuncie", "renuncia",
    "despidieron", "despedido", "despedida", "borre", "borra", "elimine", "mato",
    "reemplace", "reemplazo", "reemplaza", "gratis", "pague", "cobre", "cobrar",
    "contrate", "ahorre", "ahorrar", "primero", "primera", "prohibido",
    "ilegal", "peor", "odio", "odie", "desperdicie", "estafa", "mentira",
    "menti", "verdad", "secreto", "oculto", "robaron", "robo", "antes",
    "hasta", "pero", "excepto", "salvo", "sino", "problema", "riesgo",
    "peligro", "cuidado", "arrepiento", "arrepenti", "ojala", "deberia",
    "deberias", "todavia", "aun", "ya", "solo", "sin", "vs", "versus",
    "realmente",
}

# Arranques que gastan el primer segundo sin decir nada. Se comparan con la
# primera palabra o las dos primeras, sin tildes.
ARRANQUES_DEBILES = [
    "hola", "holi", "buenas", "buenos", "bueno", "entonces", "ok", "okey",
    "oye", "oigan", "hey", "chicos", "chicas", "amigos", "amigas", "gente",
    "bienvenidos", "bienvenidas", "hoy", "basicamente", "honestamente",
    "sinceramente", "mira", "miren", "escucha", "escuchen", "eh", "pues",
    "solo", "quiero", "queria", "les quiero", "les traigo", "te traigo",
    "vamos a", "el dia", "uno de", "una de", "has", "sabias", "sabes",
    "alguna vez", "tienes", "eres", "la cosa", "hay", "esto es", "este es",
    "esta es", "si alguna", "ustedes", "en este", "en el", "que tal", "que mas",
]

# Órdenes que se ganan el primer lugar.
IMPERATIVOS = {
    "deja", "roba", "robate", "copia", "borra", "elimina", "prueba", "lee",
    "guarda", "usa", "haz", "arma", "escribe", "manda", "envia", "toma",
    "empieza", "renuncia", "nunca", "siempre", "no", "pon", "revisa", "evita",
    "cambia", "cobra", "sube", "olvida", "aprende",
}

SEGUNDA_PERSONA = re.compile(
    r"\b(?:tu|tus|te|ti|contigo|tuyo|tuya|tuyos|tuyas|usted|ustedes|vos|sabias|"
    r"tienes|eres|estas|haces|vendes|quieres|puedes|necesitas|sabes|vas|cobras|"
    r"trabajas|publicas|subes|sientes|crees|piensas)\b")
SI_SEGUNDA = re.compile(r"\bsi \w{3,}(?:as|es)\b")
PRIMERA_PERSONA = re.compile(
    r"\b(?:yo|me|mi|mis|conmigo|nos|nosotros|nosotras|nuestro|nuestra|nuestros|"
    r"nuestras|perdi|gane|cobre|pague|aprendi|hice|tuve|fui|estuve|cambie|deje|"
    r"borre|vendi|compre|contrate|renuncie|lance|empece|probe|publique|grabe|"
    r"subi|puse|dije|logre|tengo|soy|estoy|hago|vendo|cobro|llevo|pase)\b")

DEALBREAKERS = [
    (re.compile(r"^\s*¡?\s*(?:deja de (?:hacer )?scroll|dejen de (?:hacer )?scroll|"
                r"no (?:hagas|des) scroll|para de (?:hacer )?scroll|deja de deslizar|"
                r"no deslices|stop scrolling|espera,? no (?:te vayas|deslices|pases))"),
     "Empieza con \"deja de hacer scroll\". Pedir atención demuestra que no te la has ganado."),
    (re.compile(r"\b(?:en (?:este|el) (?:video|reel)|en el video de hoy|"
                r"hoy (?:les|te) (?:voy a|vengo a) (?:mostrar|ense[ñn]ar|contar|hablar)|"
                r"(?:les|te) voy a (?:mostrar|ense[ñn]ar|contar)|"
                r"vengo a (?:mostrar|contar|hablar))\b"),
     "Introducción de video. Bórrala y empieza por la recompensa."),
    (re.compile(r"^\s*[¡¿]?\s*(?:hola|holi|buenas|buenos dias|que tal|que mas|"
                r"bienvenid[oa]s|hey|hi|hello)\b"),
     "Saludo. Nadie entró al feed a que lo saludaran."),
]
DEALBREAKERS_ORIGINAL = [
    (HASHTAG_RE,
     "Hashtag en el gancho. Los hashtags van al final del texto, si es que van."),
    (EMOJI_RE,
     "Emoji en el gancho. En texto de pantalla a tamaño de gancho cabe una palabra o un emoji, no las dos."),
]


def clamp(n):
    return max(0.0, min(100.0, n))


def words(text):
    # "$18.000.000" es una sola palabra cuando se dice, así que aquí también.
    return WORD_RE.findall(re.sub(r"(?<=\d)[.,](?=\d)", "", text))


def nombres_propios(text):
    """Palabras con mayúscula que no están al empezar una oración."""
    out = []
    for m in MAYUSCULA_RE.finditer(text):
        antes = text[:m.start()].rstrip(" \t\"“'«(")
        if not antes or antes[-1] in ".!?¿¡…\n":
            continue
        out.append(m.group(0))
    return out


def es_numero_hablado(w):
    return w in NUMEROS_HABLADOS or w.startswith(("veinti", "dieci"))


def check_length(text):
    """El gancho tiene que llegar antes de que se mueva el dedo. Unos dos segundos."""
    w = words(text)
    n = len(w)
    secs = n / 2.75                      # ~165 palabras por minuto, hablado
    chars = len(text.strip())
    if 5 <= n <= 13:
        score = 100.0
    elif n < 5:
        score = clamp(100 - (5 - n) * 20)
    else:
        score = clamp(100 - (n - 13) * 11)
    if chars > 70:                       # dos líneas de texto grande en pantalla
        score -= 12
    return clamp(score), f"{n} palabras, {chars} caracteres, ~{secs:.1f} s hablado (ideal 5-13 palabras)"


def check_specificity(text):
    """Una cosa concreta le gana a tres abstractas."""
    nums = [n.strip() for n in NUMBER_RE.findall(text) if n.strip()]
    propios = sorted(set(nombres_propios(text)))
    low = [sin_tildes(w) for w in words(text)]
    hablados = [w for w in low if es_numero_hablado(w) or w in PALABRAS_DINERO]
    hits = len(nums) + len(propios) + len(hablados)
    score = 15.0 if hits == 0 else clamp(45 + hits * 30)
    found = ", ".join(nums[:2] + propios[:2] + hablados[:2])
    return score, (f"{hits} dato(s) concreto(s)" + (f": {found}" if found else
                   " - sin cifra, sin nombre, nada comprobable"))


def check_stakes(text):
    """Tensión, costo, negación. Algo que quien mira podría perder."""
    w = [sin_tildes(x) for x in words(text)]
    marcas = sorted(set(x for x in w if x in TENSION))
    if re.search(r"\$\s?\d", text):
        marcas.append("un precio")
    n = len(marcas)
    score = {0: 20.0, 1: 70.0}.get(n, 100.0)
    detail = f"{n} marca(s) de tensión" + (f": {', '.join(marcas[:4])}" if marcas else
                                           " - en esta frase no hay nada en juego")
    return clamp(score), detail


def check_frontload(text):
    """La palabra interesante no puede estar en la posición nueve."""
    w = words(text)
    if not w:
        return 0.0, "vacío"
    low = [sin_tildes(x) for x in w]
    opener = " ".join(low[:2])
    penalty = 0
    hit_opener = None
    for weak in ARRANQUES_DEBILES:
        if opener == weak or opener.startswith(weak + " ") or low[0] == weak:
            penalty, hit_opener = 30, weak
            break
    propios = set(nombres_propios(text))
    payload = None
    for i, token in enumerate(low):
        if (token in TENSION or es_numero_hablado(token) or token in PALABRAS_DINERO
                or NUMBER_RE.match(w[i]) or w[i] in propios):
            payload = i
            break
    if payload is None:
        base = 30.0
        where = "no hay ninguna palabra de peso en la frase"
    elif payload <= 3:
        base = 100.0
        where = f"lo importante está en la palabra {payload + 1}"
    elif payload <= 6:
        base = 70.0
        where = f"lo importante está en la palabra {payload + 1}, podría ir antes"
    else:
        base = 40.0
        where = f"lo importante está en la palabra {payload + 1}, demasiado tarde"
    detail = where + (f"; arranque débil \"{hit_opener}\"" if hit_opener else "")
    return clamp(base - penalty), detail


def check_address(text):
    """Le habla a una persona, o flota en el aire."""
    low = sin_tildes(text)
    w = [sin_tildes(x) for x in words(text)]
    if SEGUNDA_PERSONA.search(low) or SI_SEGUNDA.search(low):
        return 100.0, "le habla a quien mira"
    if w and w[0] in IMPERATIVOS:
        return 90.0, f"empieza con una orden (\"{w[0]}\")"
    if PRIMERA_PERSONA.search(low):
        return 70.0, "primera persona, sin hablarle a nadie"
    return 35.0, "tercera persona, no hay nadie en la sala"


CHECKS = ["LONGITUD", "CONCRECIÓN", "TENSIÓN", "ARRANQUE", "DESTINATARIO"]


def run(text):
    results = {
        "LONGITUD": check_length(text),
        "CONCRECIÓN": check_specificity(text),
        "TENSIÓN": check_stakes(text),
        "ARRANQUE": check_frontload(text),
        "DESTINATARIO": check_address(text),
    }
    low = sin_tildes(text)
    flags = [msg for pattern, msg in DEALBREAKERS if pattern.search(low)]
    flags += [msg for pattern, msg in DEALBREAKERS_ORIGINAL if pattern.search(text)]
    scores = [results[c][0] for c in CHECKS]
    # La propiedad más débil limita el gancho: basta con una mala para que el
    # dedo siga bajando.
    overall = statistics.mean(scores) * 0.6 + min(scores) * 0.4 - len(flags) * 15
    overall = clamp(overall)
    verdict = "FUERTE" if overall >= 70 and min(scores) >= 55 and not flags else (
        "ACEPTABLE" if overall >= 50 else "DÉBIL")
    return results, overall, verdict, flags


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render_one(text, results, overall, verdict, flags, out=sys.stdout):
    print("\nPUNTAJE DEL GANCHO", file=out)
    print("=" * 62, file=out)
    print(f"  \"{text.strip()}\"\n", file=out)
    for name in CHECKS:
        score, detail = results[name]
        print(f"  {name:<13} {bar(score)} {score:5.1f}", file=out)
        print(f"  {'':<13} {detail}", file=out)
    print("-" * 62, file=out)
    print(f"  {'TOTAL':<13} {bar(overall)} {overall:5.1f}   {verdict}", file=out)
    for f in flags:
        print(f"\n  DESCARTE  {f}", file=out)
    if verdict != "FUERTE":
        weakest = min(CHECKS, key=lambda c: results[c][0])
        print(f"\n  Lo más débil: {weakest}. Arregla eso y vuelve a correrlo.", file=out)
    print("", file=out)


def render_table(rows, out=sys.stdout):
    print("\nRANKING DE GANCHOS\n" + "=" * 78, file=out)
    for i, r in enumerate(rows, 1):
        mark = "->" if i == 1 else "  "
        hook = r["hook"] if len(r["hook"]) <= 60 else r["hook"][:57] + "..."
        print(f"{mark} {r['score']:5.1f} {r['verdict']:<9} {hook}", file=out)
        print(f"        lo más débil: {r['weakest']} ({r['checks'][r['weakest']]['score']:.0f})", file=out)
        for f in r["flags"]:
            print(f"        descarte: {f}", file=out)
    print("\nGraba el primero. Si el primero tiene menos de 50, ninguno de estos es el gancho.\n",
          file=out)


def main():
    ap = argparse.ArgumentParser(description="Califica el gancho de un Reel en cinco propiedades.")
    ap.add_argument("input", nargs="?", default="-", help="archivo con un gancho por línea, o -")
    ap.add_argument("--gancho", "--hook", dest="gancho", help="califica un solo gancho escrito aquí")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.gancho:
        lines = [args.gancho]
    else:
        raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
        lines = [l.strip() for l in raw.splitlines() if l.strip()]
    if not lines:
        print("no hay nada que calificar", file=sys.stderr)
        sys.exit(2)

    payload = []
    for line in lines:
        results, overall, verdict, flags = run(line)
        payload.append({
            "hook": line,
            "checks": {k: {"score": round(v[0], 1), "detail": v[1]} for k, v in results.items()},
            "weakest": min(CHECKS, key=lambda c: results[c][0]),
            "flags": flags,
            "score": round(overall, 1),
            "verdict": verdict,
        })

    if args.json:
        print(json.dumps(payload if len(payload) > 1 else payload[0], indent=2, ensure_ascii=False))
        return

    if len(payload) == 1:
        results, overall, verdict, flags = run(lines[0])
        render_one(lines[0], results, overall, verdict, flags)
    else:
        render_table(sorted(payload, key=lambda r: -r["score"]))

    sys.exit(0 if max(p["score"] for p in payload) >= 70 else 1)


if __name__ == "__main__":
    main()
