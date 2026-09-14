#!/usr/bin/env python3
"""kt38_seite.py — Seitenrahmen fuer die handgeschriebenen KlimaTech38-Seiten.

Kopf und Fuss setzt kt38_chrome.py ueber die Sentinels ein; hier steht nur das,
was pro Seite verschieden ist: <head>, WhatsApp-FAB und die Skriptzeilen.
"""
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "klimatech38"
DOMAIN = "https://klimatech38.de"

WA_FAB = """<a class="wa-fab" href="https://wa.me/4953718759972" target="_blank" rel="noopener" aria-label="Per WhatsApp schreiben">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#fff" d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.885-9.886 9.885M20.52 3.449C18.24 1.245 15.24 0 12.045 0 5.463 0 .104 5.359.101 11.945c0 2.096.549 4.14 1.595 5.945L0 24l6.335-1.652a11.96 11.96 0 005.71 1.454h.006c6.585 0 11.946-5.359 11.949-11.945a11.86 11.86 0 00-3.495-8.411z"/></svg>
  <span class="wa-fab__pulse" aria-hidden="true"></span>
</a>"""


def kopf(titel, desc, datei, ld="", og="assets/hero.jpg",
         og_alt="Innengerät einer Split-Klimaanlage in einem hellen Wohnraum"):
    import kt38_katalog as _K
    demo_attr = ' data-preis-demo' if _K.META["demo"] else ""
    robots = "noindex, nofollow" if _K.META["demo"] else "index, follow, max-image-preview:large"
    if ld:
        ld = '<script type="application/ld+json">\n' + ld + "\n</script>\n"
    return f"""<!DOCTYPE html>
<html lang="de" data-motion="mechanical"{demo_attr}>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script>document.documentElement.classList.add('anim')</script>
<title>{titel}</title>
<meta name="description" content="{desc}">
<meta name="author" content="InTroTech GmbH">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{DOMAIN}/{datei}">
<meta name="geo.region" content="DE-NI">
<meta name="geo.placename" content="Gifhorn">
<meta property="og:type" content="website">
<meta property="og:url" content="{DOMAIN}/{datei}">
<meta property="og:site_name" content="KlimaTech38">
<meta property="og:locale" content="de_DE">
<meta property="og:title" content="{titel}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{DOMAIN}/{og}">
<meta property="og:image:alt" content="{og_alt}">
<meta name="theme-color" content="#10303F">
<link rel="icon" type="image/png" href="assets/brand/mark.png">
<link rel="apple-touch-icon" href="assets/brand/mark.png">
<link rel="stylesheet" href="styles.css">
{ld}</head>
<body>
<a class="skip" href="#inhalt">Zum Inhalt springen</a>

<!-- KT38:HEADER:START -->
<!-- KT38:HEADER:END -->

<main id="inhalt">
"""


def fuss(motion="voll", produkte=False):
    """motion='schlank' spart GSAP/ScrollTrigger/Lenis (rund 130 KB Parse-Arbeit).
       assets/motion.js macht die Reveals dann ueber seinen Fallback-Pfad sichtbar."""
    js = []
    if motion == "voll":
        js += ['<script src="assets/js/gsap.min.js"></script>',
               '<script src="assets/js/ScrollTrigger.min.js"></script>',
               '<script src="assets/js/lenis.min.js"></script>']
    js.append('<script src="assets/motion.js"></script>')
    if produkte:
        js.append('<script src="assets/produkte.js"></script>')
    js.append('<script src="script.js"></script>')
    return f"""
</main>

<!-- KT38:FOOTER:START -->
<!-- KT38:FOOTER:END -->

{WA_FAB}

{chr(10).join(js)}
</body>
</html>
"""


def schreibe(datei, inhalt):
    (SITE / datei).write_text(inhalt, encoding="utf-8")
    return datei
