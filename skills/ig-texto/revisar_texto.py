#!/usr/bin/env python3
"""
revisar_texto.py - revisa el texto (caption) de una publicación de Instagram y
te muestra exactamente lo que se ve en el feed antes del "... más".

Basado en caption.py de instagram-agent-skill, de Jake Schincariol (licencia
MIT). Traducción y adaptación al español: Juan Sebastian Cruz - 1691 Agency.

Instagram muestra unos 125 caracteres del texto en el feed y esconde el resto
detrás de un toque. Casi todos los textos que fallan, fallan ahí: el gancho está
en la tercera frase, la primera línea es un saludo o todo arranca con un
hashtag. Esto imprime la parte visible en un recuadro, para que la leas como la
lee un desconocido que va bajando, y luego revisa las cosas que vale la pena
revisar.

El corte de 125 caracteres es aproximado. El número real cambia según el
teléfono, el tamaño de letra y dónde caen tus saltos de línea; por eso conviene
dejar margen en vez de ajustar el texto para que termine justo en 125. Cámbialo
con --corte si quieres probar uno más estricto.

Uso
  python3 revisar_texto.py texto.txt
  python3 revisar_texto.py texto.txt --palabras-clave "café de especialidad,barista en Ibagué"
  python3 revisar_texto.py texto.txt --json
  cat texto.txt | python3 revisar_texto.py -
"""

import argparse
import json
import re
import sys
import textwrap

LIMIT = 2200             # Límite fijo de Instagram para el texto.
TRUNCATE = 125           # Más o menos donde el feed corta en "... más".
HASHTAG_LIMIT = 5        # Tope de Instagram por publicación o reel desde
                         # diciembre de 2025, antes era 30. Instagram dijo que
                         # usar menos hashtags (hasta 5) y más específicos
                         # funciona mejor que muchos genéricos.

HASHTAG_RE = re.compile(r"(?:^|\s)(#\w+)")
MENTION_RE = re.compile(r"(?:^|\s)(@[\w.]+)")
LINK_RE = re.compile(
    r"https?://\S+|\bwww\.\S+"
    r"|\b[\w-]+\.(?:com|co|io|net|org|ai|app|me|la|mx|es|ar|cl|pe|ec|uy|ly|shop|store|link)"
    r"(?:\.[a-z]{2})?\b(?:/\S*)?",
    re.IGNORECASE)
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿←-⇿️]")
NUMERO_RE = re.compile(r"\$\s?\d|\b\d[\d.,]*\b")
MAYUSCULA_RE = re.compile(r"\b[A-ZÁÉÍÓÚÑÜ][a-záéíóúñü]{2,}\b")
SALUDO_RE = re.compile(r"\s*[¡¿]?\s*(?:hola|holi|buenas|buenos dias|que tal|que mas|"
                       r"bienvenid[oa]s|hey|hi|hello)\b")
QUITAR_TILDES = str.maketrans("áéíóúüÁÉÍÓÚÜ", "aeiouuAEIOUU")


def sin_tildes(texto):
    return texto.translate(QUITAR_TILDES).lower()


# Cada llamado a la acción se busca en el texto en minúsculas y sin tildes,
# salvo el de "comenta PALABRA", que necesita ver las mayúsculas.
ASK_KEYWORD = re.compile(
    r"(?i:\b(?:comenta(?:me|nos)?|escribe|escribeme|escríbeme|déjame|dejame)\b)\s+"
    r"(?:(?i:la palabra|aqu[ií] abajo|abajo)\s+)?[\"“'«]?[A-ZÁÉÍÓÚÑ0-9]{3,}\b")
ASKS = [
    (re.compile(r"\b(?:escribeme|escribenos|mandame|envia(?:me|nos)|hablame|contactame|"
                r"contactanos)\b[^.!?\n]{0,25}\b(?:dm|md|mensaje|privado|interno|inbox|"
                r"whatsapp|wasap)\b|\b(?:por|al) (?:dm|md|interno|privado|inbox)\b"),
     "mensaje directo"),
    (re.compile(r"\bguarda(?:lo|la|los|las|te)?\b|\bguardalo\b"), "guardar"),
    (re.compile(r"\bcomparte(?:lo|la|los|las)?\b|\benvia(?:selo|sela|lo|la)? a\b|"
                r"\bmanda(?:selo|sela)\b|\bmandale (?:esto|este)\b"), "compartir"),
    (re.compile(r"\bsigue(?:me|nos)\b|\bdale (?:a )?seguir\b|\bsigue la cuenta\b"), "seguir"),
    (re.compile(r"\b(?:link|enlace|link de compra) (?:en|de) (?:la|mi|nuestra) "
                r"(?:bio|biografia|perfil)\b|\ben (?:la|mi|nuestra) bio\b|\blink in bio\b"),
     "link en la bio"),
    (re.compile(r"\bdesliza\b|\bpasa (?:a la|al) (?:siguiente|derecha|izquierda)\b|\bswipe\b"),
     "deslizar"),
    (re.compile(r"\bcuentame\b|\bcuentanos\b|\bque (?:harias|opinas|prefieres|piensas)\b|"
                r"\bcual (?:prefieres|eliges|te gusta)\b"), "responder una pregunta"),
    # Solo cuenta como orden al empezar una frase ("Reserva tu mesa"), para no
    # confundirla con el sustantivo ("tu reserva", "mi agenda").
    (re.compile(r"(?:^|[.!¡?\n]\s*|\by\s)(?:pide(?:la|lo|los|las)?|haz tu pedido|reserva|"
                r"agenda|cotiza|llama(?:nos)?|visita(?:nos)?|ven a|compra(?:lo|la)?)\b", re.MULTILINE),
     "pedido, reserva o visita"),
]

RELLENO_TAGS = {
    "#viral", "#fyp", "#parati", "#paratii", "#foryou", "#foryoupage", "#explore",
    "#explorepage", "#explorar", "#tendencia", "#tendencias", "#trending",
    "#instagood", "#love", "#amor", "#follow", "#seguidores", "#like4like",
    "#likes", "#megusta", "#reels", "#reelsinstagram", "#viralreels",
    "#instadaily", "#photooftheday", "#picoftheday", "#fotodeldia", "#insta",
    "#instagram",
}


def visible_window(text, cut):
    """Lo que muestra el feed. Instagram corta a mitad de palabra, así que esto también."""
    flat = text.strip()
    return flat if len(flat) <= cut else flat[:cut]


def concretos(text):
    found = NUMERO_RE.findall(text)
    for m in MAYUSCULA_RE.finditer(text):
        antes = text[:m.start()].rstrip(" \t\"“'«(")
        if antes and antes[-1] not in ".!?¿¡…\n":
            found.append(m.group(0))
    return found


def render_box(window, truncated, out=sys.stdout, width=52):
    print("\n  LO QUE MUESTRA EL FEED", file=out)
    print("  +" + "-" * (width + 2) + "+", file=out)
    lines = []
    for raw in window.rstrip().split("\n"):
        lines.extend(textwrap.wrap(raw, width) or [""])
    for line in lines[:8]:
        print(f"  | {line:<{width}} |", file=out)
    tail = "... más" if truncated else "(se ve completo)"
    print("  +" + "-" * (width + 2 - len(tail) - 2) + f" {tail} " + "+", file=out)


def analyse(text, cut=TRUNCATE, keywords=None):
    text = text.rstrip()
    stripped = text.strip()
    low = sin_tildes(stripped)
    chars = len(stripped)
    lines = [l for l in stripped.split("\n")]
    first_line = lines[0].strip() if lines else ""
    tags = HASHTAG_RE.findall(stripped)
    mentions = MENTION_RE.findall(stripped)
    links = LINK_RE.findall(MENTION_RE.sub(" ", stripped))   # @cuenta.co no es un enlace
    emoji = EMOJI_RE.findall(stripped)
    window = visible_window(stripped, cut)
    truncated = chars > cut
    asks = (["comentar una palabra"] if ASK_KEYWORD.search(stripped) else [])
    asks += [name for pattern, name in ASKS if pattern.search(low)]
    filler = [t for t in tags if t.lower() in RELLENO_TAGS]
    keywords = [k.strip() for k in (keywords or []) if k.strip()]

    checks = []

    def add(name, status, detail):
        checks.append({"check": name, "status": status, "detail": detail})

    add("LONGITUD", "FALLA" if chars > LIMIT else "BIEN",
        f"{chars} / {LIMIT} caracteres" + (f", {chars - LIMIT} por encima del límite"
                                           if chars > LIMIT else ""))

    if not first_line:
        add("PRIMERA LÍNEA", "FALLA", "el texto empieza con una línea en blanco")
    elif first_line.startswith("#") or first_line.startswith("@"):
        add("PRIMERA LÍNEA", "FALLA",
            "empieza con un hashtag o una mención, en el único lugar que merece una frase")
    elif SALUDO_RE.match(sin_tildes(first_line)):
        add("PRIMERA LÍNEA", "OJO",
            "empieza con un saludo. Nadie entró al feed a que lo saludaran: abre con la idea")
    elif EMOJI_RE.match(first_line):
        add("PRIMERA LÍNEA", "OJO",
            "empieza con un emoji. El primer carácter vale más como palabra")
    elif len(first_line) > cut:
        add("PRIMERA LÍNEA", "OJO",
            f"{len(first_line)} caracteres, así que se corta en {cut} a mitad de idea. "
            "Está bien si el corte deja suspenso, mal si corta una frase a medias")
    else:
        add("PRIMERA LÍNEA", "BIEN", f"{len(first_line)} caracteres, se ve completa")

    datos = concretos(window)
    add("GANCHO CONCRETO", "BIEN" if datos else "OJO",
        f"{len(datos)} cifra(s) o nombre(s) en la parte visible"
        + ("" if datos else " - nada comprobable antes del toque"))

    if len(tags) > HASHTAG_LIMIT:
        add("HASHTAGS", "FALLA", f"{len(tags)} hashtags, más del tope de {HASHTAG_LIMIT} de Instagram. "
                                 "Los que pasan del quinto no cuentan y el bloque se ve viejo")
    elif len(tags) == HASHTAG_LIMIT and filler:
        add("HASHTAGS", "OJO", f"{len(tags)} hashtags, en el tope, y "
                               f"{len(filler)} genéricos. Usa los cinco en temas")
    elif filler:
        add("HASHTAGS", "OJO", f"{len(tags)} hashtags, {len(filler)} genéricos "
                               f"({', '.join(filler[:3])}). Esos no describen nada")
    else:
        add("HASHTAGS", "BIEN", f"{len(tags)} hashtag(s)" + (f": {' '.join(tags)}" if tags else ""))

    if not tags:
        add("UBICACIÓN TAGS", "BIEN", "no hay hashtags que ubicar")
    elif any(re.search(r"(?:^|\s)" + re.escape(t) + r"\b", window) for t in tags):
        add("UBICACIÓN TAGS", "OJO", "hay un hashtag dentro de la parte visible, "
                                     "gastando espacio del feed en una etiqueta")
    else:
        add("UBICACIÓN TAGS", "BIEN", "los hashtags quedan debajo del corte")

    add("ENLACES", "OJO" if links else "BIEN",
        f"{len(links)} enlace(s) en el texto, y en el texto no se puede hacer clic. "
        f"Pásalo a la bio o al mensaje directo" if links else "no hay enlaces muertos en el texto")

    if len(asks) == 1:
        add("UNA ACCIÓN", "BIEN", f"un solo llamado a la acción: {asks[0]}")
    elif not asks:
        add("UNA ACCIÓN", "OJO", "no hay llamado a la acción. Decide para qué es esta publicación")
    else:
        add("UNA ACCIÓN", "OJO", f"{len(asks)} pedidos ({', '.join(asks)}). "
                                 "Dos pedidos valen lo mismo que ninguno")

    density = len(emoji) * 100 / max(chars, 1)
    add("EMOJIS", "OJO" if density > 4 else "BIEN",
        f"{len(emoji)} emoji(s), {density:.1f} por cada 100 caracteres"
        + (" - se ve como decoración" if density > 4 else ""))

    if keywords:
        found = [k for k in keywords if sin_tildes(k) in low]
        missing = [k for k in keywords if sin_tildes(k) not in low]
        in_window = [k for k in found if sin_tildes(k) in sin_tildes(window)]
        status = "BIEN" if not missing else ("OJO" if found else "FALLA")
        add("BÚSQUEDA", status,
            f"{len(found)}/{len(keywords)} presentes"
            + (f", {len(in_window)} en la parte visible" if found else "")
            + (f". Faltan: {', '.join(missing)}" if missing else ""))

    fails = sum(1 for c in checks if c["status"] == "FALLA")
    warns = sum(1 for c in checks if c["status"] == "OJO")
    verdict = "CORREGIR" if fails else ("REVISAR" if warns else "LISTO")

    return {
        "characters": chars, "limit": LIMIT, "truncate_at": cut,
        "visible": window, "truncated": truncated,
        "first_line_chars": len(first_line),
        "hashtags": tags, "mentions": mentions, "links": links,
        "emoji": len(emoji), "asks": asks,
        "checks": checks, "verdict": verdict,
    }


def render(a, out=sys.stdout):
    head = (f"REVISIÓN DEL TEXTO  ·  {a['characters']} / {a['limit']} caracteres  ·  "
            f"{len(a['hashtags'])} hashtags  ·  {len(a['asks'])} pedido(s)")
    print("\n" + head, file=out)
    print("=" * max(len(head), 62), file=out)
    render_box(a["visible"], a["truncated"], out=out)
    print("", file=out)
    for c in a["checks"]:
        print(f"  {c['status']:<5} {c['check']:<16} {c['detail']}", file=out)
    print("-" * max(len(head), 62), file=out)
    print(f"  RESULTADO  {a['verdict']}\n", file=out)


def main():
    ap = argparse.ArgumentParser(description="Revisa el texto de una publicación de Instagram.")
    ap.add_argument("input", nargs="?", default="-", help="archivo del texto, o - para leer de la entrada")
    ap.add_argument("--corte", "--truncate", dest="corte", type=int, default=TRUNCATE,
                    help=f"caracteres visibles antes de '... más' ({TRUNCATE} por defecto)")
    ap.add_argument("--palabras-clave", "--keywords", dest="palabras", default="",
                    help="términos separados por coma con los que quieres que te encuentren")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    a = analyse(raw, cut=args.corte, keywords=args.palabras.split(","))
    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    sys.exit(0 if a["verdict"] == "LISTO" else 1)


if __name__ == "__main__":
    main()
