#!/usr/bin/env python3
"""gen_kt38_shop.py — erzeugt aus .tools/kt38_katalog.py alle 29 KlimaTech38-Seiten.

Redesign 2026-09-12 (Brief: assets/art-direction.md · Skelett: assets/struktur-blueprint.md).
Ausgabe (statisches HTML, im Deploy laeuft KEIN Build):
    klimatech38/assets/produkte.js      Datenschicht fuer Rechner, Filter, Schalter
    klimatech38/index.html              Vollbild-Hero + Bento + Rechner + Bestseller + ...
    klimatech38/shop.html               Katalog-Kopf + Rechner + alle Sets
    klimatech38/shop-*.html             4 Kategorieseiten (Buehnen-Kopf + Filter)
    klimatech38/set-*.html              9 Set-Seiten (Produkt-Kopf + Unterleiste)
    klimatech38/<prosa>.html            12 Text-Seiten aus kt38_prosa.py
    klimatech38/sitemap.xml

Reihenfolge nach jeder Aenderung:
    python3 .tools/gen_kt38_shop.py && python3 .tools/kt38_chrome.py --write
Aufruf mit --check: Exit 1, wenn der Bestand veraltet ist.
"""
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kt38_katalog as K
import kt38_chrome as C
import kt38_seite as S

SITE = S.SITE
DOMAIN = S.DOMAIN
ORTE = ["Gifhorn", "Wolfsburg", "Braunschweig", "Peine", "Salzgitter", "Helmstedt"]


def e(s):
    return html.escape(str(s), quote=True)


def kw(s):
    return f'{s["kw"]:.1f}'.replace(".", ",") + " kW"


def chip(text, klasse="", icon=""):
    k = "chip" + (f" {klasse}" if klasse else "")
    return f'<span class="{k}">{icon}{text}</span>'


ICON_ARROW = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
ICON_CHECK = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m5 12 4 4L19 7"/></svg>'
ICON_MINUS = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 12h12"/></svg>'
ICON_INFO = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 8h.01M11 12h1v4h1"/></svg>'
ICON_PLUS = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>'
ICON_TOOL = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14.5 6.5a3.5 3.5 0 0 0 3 5l-8 8a2 2 0 0 1-3-3l8-8"/><path d="m15 3 6 6"/></svg>'
ICON_HOME = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20h16M6 20V9l6-5 6 5v11"/><path d="M10 20v-6h4v6"/></svg>'
ICON_SUN = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 3v2M12 19v2M3 12h2M19 12h2M5.6 5.6l1.4 1.4M17 17l1.4 1.4M5.6 18.4 7 17M17 7l1.4-1.4"/></svg>'
ZUB_ICONS = {
    "halter-wand": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 4v16M4 8h12v6H4"/><path d="M8 14l-4 6M14 14l-4 6"/></svg>',
    "halter-boden": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 20h18M6 20v-3M18 20v-3"/><rect x="4" y="9" width="16" height="8" rx="2"/><path d="M7 9V6M17 9V6"/></svg>',
    "kondensatpumpe": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="9" width="12" height="9" rx="2"/><path d="M15 12h3a3 3 0 0 1 3 3v5"/><path d="M9 13.5v.01"/><path d="M6 6l1.5-2 1.5 2a1.5 1.5 0 1 1-3 0z"/></svg>',
    "wanddurchfuehrung": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 4v16M8 4v16"/><circle cx="5.5" cy="12" r="2"/><path d="M8 12h13"/></svg>',
    "leitungskanal": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="8" y="3" width="8" height="18" rx="2"/><path d="M12 3v18M8 9h8M8 15h8"/></svg>',
    "ueberspannung": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="3" width="14" height="18" rx="2"/><path d="M13 7l-3 5h4l-3 5"/></svg>',
    "fensterabdichtung": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="4" y="3" width="16" height="18" rx="2"/><path d="M12 3v18"/><path d="M12 7h2M12 11h2M12 15h2M10 9h2M10 13h2M10 17h2"/></svg>',
}
ICON_BOX = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 8l9-4 9 4-9 4-9-4z"/><path d="M3 8v8l9 4 9-4V8"/><path d="M12 12v8"/></svg>'


# --------------------------------------------------------------------- Produkt-SVG (ausgerendert)
# Eigene Produktdarstellung: kein Fremdfoto, kein Herstellerlogo. Leichte Isometrie (Seitenflaeche),
# Lamellenschlitz, Display-Feld, Radial-Bodenschatten, Breite je kW — 2,5 kW ist sichtbar kleiner als 7,0 kW.

def _breite(kw, lo, hi, kw_lo=2.0, kw_hi=8.4):
    t = max(0.0, min(1.0, (kw - kw_lo) / (kw_hi - kw_lo)))
    return lo + (hi - lo) * t


def _schatten(cx, cy, rx, ry, p):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#{p}-sh)"/>'


def _innen(x, y, w, p, tiefe=10):
    """Wand-Innengeraet: Frontflaeche mit Rundung unten, Ansauggitter oben, Lamelle + Auslassschlitz, Display."""
    h = w * .30
    r, R = 9, h * .38
    front = (f"M{x + r},{y} H{x + w - r} A{r},{r} 0 0 1 {x + w},{y + r} V{y + h - R} "
             f"A{R},{R} 0 0 1 {x + w - R},{y + h} H{x + R} A{R},{R} 0 0 1 {x},{y + h - R} V{y + r} A{r},{r} 0 0 1 {x + r},{y} Z")
    seite = (f"M{x + w},{y + r} L{x + w + tiefe},{y + r - tiefe * .6} V{y + h - R - tiefe * .6} "
             f"A{R},{R} 0 0 1 {x + w + tiefe - R},{y + h - tiefe * .6} L{x + w - R},{y + h} A{R},{R} 0 0 1 {x + w},{y + h - R} Z")
    oben = (f"M{x + r},{y} L{x + r + tiefe},{y - tiefe * .6} H{x + w + tiefe - r} L{x + w},{y} Z")
    gitter = "".join(f'<line x1="{x + 18 + i * 12}" y1="{y + 4}" x2="{x + 18 + i * 12 + tiefe * .7}" y2="{y - tiefe * .6 + 2}" stroke="#C9D5E0" stroke-width="1.2"/>'
                     for i in range(int((w - 36) / 12)))
    lam_h = max(7, h * .17)
    lam_y = y + h - lam_h - h * .16
    return (_schatten(x + w / 2, y + h + 6, w * .5, 7, p) +
            f'<path d="{oben}" fill="#EEF3F7" stroke="rgba(14,42,58,.10)"/>{gitter}'
            f'<path d="{seite}" fill="url(#{p}-side)" stroke="rgba(14,42,58,.12)"/>'
            f'<path d="{front}" fill="url(#{p}-ig)" stroke="rgba(14,42,58,.14)"/>'
            f'<rect x="{x + 12}" y="{y + 7}" width="{w - 24}" height="2.5" rx="1.2" fill="rgba(255,255,255,.95)"/>'
            f'<rect x="{x + 14}" y="{lam_y + lam_h + 2}" width="{w - 28}" height="{max(3, h * .07)}" rx="2" fill="#7F909F"/>'
            f'<rect x="{x + 14}" y="{lam_y}" width="{w - 28}" height="{lam_h}" rx="{lam_h / 2}" fill="url(#{p}-lam)"/>'
            f'<rect x="{x + 22}" y="{lam_y + lam_h * .3}" width="{w - 44}" height="1.4" rx=".7" fill="rgba(255,255,255,.85)"/>'
            f'<rect x="{x + w - 46}" y="{y + h * .42}" width="30" height="{max(8, h * .2)}" rx="3" fill="#DCE5EE"/>'
            f'<circle cx="{x + w - 24}" cy="{y + h * .42 + max(8, h * .2) / 2}" r="2.2" fill="#1668AE"/>')


def _aussen(x, y, w, p, konsole=False):
    """Aussengeraet: Frontgitter mit Ringen und Speichen, Seitenflaeche, Fuesse; optional Wandkonsole."""
    h = w * .72
    cx, cy, r = x + w * .37, y + h * .5, h * .35
    rings = "".join(f'<circle cx="{cx}" cy="{cy}" r="{r * f}" fill="none" stroke="#BFCCD8" stroke-width="1.5"/>' for f in (.82, .62, .42))
    speichen = "".join(f'<line x1="{cx}" y1="{cy}" x2="{cx + r * .95 * __import__("math").cos(a)}" y2="{cy + r * .95 * __import__("math").sin(a)}" stroke="#D3DDE6" stroke-width="1.2"/>'
                       for a in [i * 3.14159 / 6 for i in range(12)])
    slats = "".join(f'<line x1="{sx}" y1="{y + 14}" x2="{sx}" y2="{y + h - 14}" stroke="#D3DDE6" stroke-width="2" stroke-linecap="round"/>'
                    for sx in range(int(x + w * .70), int(x + w - 12), 8))
    tiefe = 12
    seite = f"M{x + w},{y + 10} L{x + w + tiefe},{y + 10 - tiefe * .6} V{y + h - 8 - tiefe * .6} L{x + w},{y + h - 8} Z"
    oben = f"M{x + 10},{y} L{x + 10 + tiefe},{y - tiefe * .6} H{x + w + tiefe - 10} L{x + w - 10},{y} Z"
    kons = ""
    if konsole:
        kons = (f'<path d="M{x + 8},{y + h + 8} L{x - 18},{y + h + 28} M{x + w - 8},{y + h + 8} L{x + w - 34},{y + h + 28}" stroke="#9FB0BF" stroke-width="4" stroke-linecap="round"/>'
                f'<rect x="{x - 4}" y="{y + h + 6}" width="{w + 8}" height="5" rx="2" fill="#9FB0BF"/>')
    return (_schatten(x + w / 2, y + h + 12, w * .52, 8, p) + kons +
            f'<rect x="{x + 10}" y="{y + h}" width="20" height="8" rx="2" fill="#B9C7D3"/><rect x="{x + w - 30}" y="{y + h}" width="20" height="8" rx="2" fill="#B9C7D3"/>'
            f'<path d="{oben}" fill="#EEF3F7" stroke="rgba(14,42,58,.10)"/>'
            f'<path d="{seite}" fill="url(#{p}-side)" stroke="rgba(14,42,58,.12)"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="url(#{p}-ag)" stroke="rgba(14,42,58,.14)"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#E6EDF3" stroke="#BFCCD8" stroke-width="1.5"/>{speichen}{rings}'
            f'<circle cx="{cx}" cy="{cy}" r="{r * .16}" fill="#AAB9C6"/>{slats}'
            f'<rect x="{x + 12}" y="{y + 6}" width="{w - 24}" height="2.5" rx="1.2" fill="rgba(255,255,255,.95)"/>'
            f'<rect x="{x + w * .70}" y="{y + h - 12}" width="{w * .22}" height="5" rx="2" fill="#DCE5EE"/>')


def _mono(x, y, w, h, p):
    vents = "".join(f'<line x1="{x + 16}" y1="{vy}" x2="{x + w - 16}" y2="{vy}" stroke="#D3DDE6" stroke-width="2.2" stroke-linecap="round"/>'
                    for vy in range(int(y + h * .52), int(y + h - 16), 10))
    hx, hy = x + w - 2, y + 30
    d = f"M{hx},{hy} C{hx + 44},{hy} {hx + 36},{hy - 60} {hx + 78},{hy - 74} L{hx + 96},{hy - 82}"
    hose = (f'<path d="{d}" fill="none" stroke="#C4D0DB" stroke-width="14" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="#AEBECC" stroke-width="14" stroke-linecap="round" stroke-dasharray="3 7"/>'
            f'<path d="{d}" fill="none" stroke="rgba(255,255,255,.5)" stroke-width="3" stroke-linecap="round"/>')
    fenster = (f'<rect x="{hx + 76}" y="{hy - 150}" width="78" height="120" rx="6" fill="rgba(255,255,255,.55)" stroke="#C3D0DC" stroke-width="2"/>'
               f'<line x1="{hx + 115}" y1="{hy - 150}" x2="{hx + 115}" y2="{hy - 30}" stroke="#C3D0DC" stroke-width="2"/>')
    tiefe = 12
    seite = f"M{x + w},{y + 18} L{x + w + tiefe},{y + 18 - tiefe * .6} V{y + h - 18 - tiefe * .6} L{x + w},{y + h - 18} Z"
    return (fenster + hose + _schatten(x + w / 2, y + h + 12, w * .6, 8, p) +
            f'<circle cx="{x + 20}" cy="{y + h + 4}" r="8" fill="#AAB9C6"/><circle cx="{x + w - 20}" cy="{y + h + 4}" r="8" fill="#AAB9C6"/>'
            f'<path d="{seite}" fill="url(#{p}-side)" stroke="rgba(14,42,58,.12)"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="url(#{p}-ig)" stroke="rgba(14,42,58,.14)"/>'
            f'<rect x="{x + 16}" y="{y + 14}" width="{w - 32}" height="10" rx="5" fill="#D8E2EC"/>'
            f'<circle cx="{x + w - 26}" cy="{y + 19}" r="2.4" fill="#1668AE"/>'
            f'<rect x="{x + 16}" y="{y + 36}" width="{w - 32}" height="{h * .32}" rx="10" fill="#E6EDF3"/>{vents}')


def _leitung(punkte):
    d = "M" + " L".join(f"{px},{py}" for px, py in punkte)
    return (f'<path d="{d}" fill="none" stroke="#7FB0DE" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="rgba(255,255,255,.7)" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>')


_svg_zaehler = [0]


def geraet_svg(art, klasse="geraet", titel="", kw=3.5):
    _svg_zaehler[0] += 1
    p = f"g{_svg_zaehler[0]}"
    defs = (f'<defs><linearGradient id="{p}-ig" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#E9EEF3"/></linearGradient>'
            f'<linearGradient id="{p}-ag" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FAFCFD"/><stop offset="1" stop-color="#DEE6ED"/></linearGradient>'
            f'<linearGradient id="{p}-side" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#D5DEE7"/><stop offset="1" stop-color="#C3CFDA"/></linearGradient>'
            f'<linearGradient id="{p}-lam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E4EBF1"/><stop offset="1" stop-color="#C9D5DF"/></linearGradient>'
            f'<radialGradient id="{p}-sh" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="rgba(14,42,58,.28)"/><stop offset="1" stop-color="rgba(14,42,58,0)"/></radialGradient></defs>')
    wand = '<line x1="0" y1="34" x2="400" y2="34" stroke="rgba(14,42,58,.08)" stroke-width="1"/>'
    if art == "split1":
        wi = _breite(kw, 150, 240, 2.5, 7.0); wa = _breite(kw, 120, 165, 2.5, 7.0)
        xi, yi = 26, 58; xa, ya = 400 - wa - 22, 290 - wa * .72 - 36
        teile = (wand + _leitung([(xi + wi - 30, yi + wi * .30), (xi + wi - 30, ya + wa * .72 - 24), (xa, ya + wa * .72 - 24)]) +
                 _innen(xi, yi, wi, p) + _aussen(xa, ya, wa, p, konsole=True))
    elif art in ("multi2", "multi3", "multi4"):
        n = int(art[-1]); wa = _breite(kw, 150, 172, 5.2, 8.4)
        xa, ya = 400 - wa - 22, 290 - wa * .72 - 36
        wi = {2: 150, 3: 128, 4: 112}[n]; step = {2: 92, 3: 74, 4: 60}[n]
        trunk = 20 + (n - 1) * 8 + wi + 16
        teile = wand + _leitung([(trunk, 52 + wi * .30), (trunk, ya + wa * .72 - 24), (xa, ya + wa * .72 - 24)])
        for i in range(n):
            xi = 20 + i * 8; yi = 52 + i * step
            teile += _leitung([(xi + wi - 24, yi + wi * .30), (trunk, yi + wi * .30)])
        for i in range(n):
            xi = 20 + i * 8; yi = 52 + i * step
            teile += _innen(xi, yi, wi, p, tiefe=8)
        teile += _aussen(xa, ya, wa, p, konsole=True)
    elif art == "mono":
        w = _breite(kw, 100, 118, 2.0, 2.6)
        teile = _mono(150 - w / 2 + 20, 76, w, 186, p)
    elif art == "zubehoer":
        # Zubehoer im Zusammenhang: Aussengeraet auf Wandkonsole, Leitungskanal, Kondensatpumpe
        teile = (wand + f'<rect x="228" y="40" width="22" height="150" rx="6" fill="#DCE5EE" stroke="rgba(14,42,58,.10)"/>'
                 f'<rect x="234" y="46" width="10" height="138" rx="4" fill="#EEF3F7"/>'
                 + _leitung([(239, 190), (239, 214), (250, 214)]) +
                 f'<rect x="300" y="52" width="60" height="38" rx="8" fill="url(#{p}-ig)" stroke="rgba(14,42,58,.14)"/>'
                 f'<circle cx="352" cy="61" r="2.2" fill="#1668AE"/><path d="M300,71 H278 V140" fill="none" stroke="#7FB0DE" stroke-width="3" stroke-linecap="round"/>'
                 + _aussen(60, 130, 150, p, konsole=True))
    else:
        teile = _innen(60, 100, 280, p)
    role = f' role="img" aria-label="{e(titel)} – schematische Darstellung"' if titel else ' aria-hidden="true"'
    return f'<svg class="{klasse}" viewBox="0 0 400 300"{role}>{defs}{teile}</svg>'


def stage(s, klasse="stage", best=False):
    """Produkt-Buehne: SVG-Geraet auf Verlauf + kW-Chip (+ Bestseller-Chip)."""
    b = chip("Empfehlung", "chip--best") if best else ""
    return f'<div class="{klasse}">{geraet_svg(s["schema"], titel=s["titel"], kw=s["kw"])}{chip(kw(s))}{b}</div>'


# --------------------------------------------------------------------- Bausteine

def preis(s, klasse="preis"):
    return C.preis_html(s, klasse)


def produkt_karte(s, best=False, gross=False, attrs="", voll=False):
    raeume = f'<span><b>{s["innengeraete"]}</b> Räume</span>' if s["innengeraete"] > 1 else '<span><b>1</b> Raum</span>'
    einbau = "selbst möglich" if s["selbsteinbau"] else "durch uns"
    klasse = "karte pk" + (" pk--best" if gross else "") + (" pk--best-3" if (gross and voll) else "")
    return f"""<article class="{klasse}" data-set="{s["id"]}"{attrs}>
  {stage(s, best=best)}
  <div class="pk__body">
    <h3><a href="set-{s["id"]}.html">{e(s["titel"]).replace(" · ", "&nbsp;· ")}</a></h3>
    <p class="pk__kurz">{e(s["kurz"])}</p>
    <p class="pk__meta"><span><b>{s["flaecheVon"]}–{s["flaecheBis"]}</b> m²</span>{raeume}<span>Einbau <b>{einbau}</b></span></p>
    <div class="pk__fuss">{preis(s)}<a class="btn btn--klein btn--ink" href="set-{s["id"]}.html">Set ansehen{ICON_ARROW}</a></div>
  </div>
</article>"""


def demo_zeile():
    if not K.META["demo"]:
        return ""
    return f'<p class="demo-hinweis">{ICON_INFO}<span><b>Vorschau:</b> {K.META["demoHinweis"]}</span></p>'


def kein_kauf():
    return f'<p class="demo-hinweis">{ICON_INFO}<span>{e(K.META["keinKaufHinweis"])}</span></p>'


def abschluss(titel, text, cta1, cta2=None):
    b2 = f'<a class="btn btn--rand-hell" href="{cta2[1]}">{cta2[0]}</a>' if cta2 else ""
    return f"""<section class="sec sec--eng">
  <div class="wrap">
    <div class="abschluss" data-reveal>
      <div><h2>{titel}</h2><p>{text}</p></div>
      <p class="btns"><a class="btn btn--hell" href="{cta1[1]}">{cta1[0]}</a>{b2}</p>
    </div>
  </div>
</section>"""


def kontakt_vollbild(als_h1=False, titel="Wir sehen uns <em>Ihre Räume an.</em>"):
    """Vollbild-Karte (Achse 4): OSM traegt die Sektion, Kontakt-Karte als Overlay, lazy geladen."""
    h = "h1" if als_h1 else "h2"
    orte = "".join(chip(o, "chip--rand") for o in ORTE)
    bbox = "10.15%2C52.08%2C10.95%2C52.62"
    kl = "karte-vb karte-vb--kopf" if als_h1 else "karte-vb"
    return f"""<section class="{kl}" id="kontakt" aria-labelledby="kontakt-h">
  <div class="karte-vb__map" data-karte data-src="https://www.openstreetmap.org/export/embed.html?bbox={bbox}&amp;layer=mapnik&amp;marker=52.481%2C10.547">
    <p class="karte-vb__laden">Karte wird geladen …</p>
  </div>
  <div class="karte-vb__innen">
    <div class="kontaktkarte" data-reveal>
      <{h} id="kontakt-h">{titel}</{h}>
      <div class="kanaele">
        <a class="kanal" href="tel:{C.TEL}"><span class="kanal__i">{C.ICON_TEL}</span><span><b>{C.TEL_TEXT}</b><small>Mo–Fr 08–18 Uhr · Anruf ist am schnellsten</small></span></a>
        <a class="kanal" href="{C.WA}" target="_blank" rel="noopener"><span class="kanal__i">{C.ICON_WA}</span><span><b>WhatsApp</b><small>Fotos vom Raum direkt schicken</small></span></a>
        <a class="kanal" href="mailto:{C.MAIL}"><span class="kanal__i">{C.ICON_MAIL}</span><span><b>{C.MAIL}</b><small>Zeisigweg 4 · 38518 Gifhorn</small></span></a>
      </div>
      <div class="chips" aria-label="Einzugsgebiet">{orte}</div>
      <p class="btns"><a class="btn btn--primary" href="{'#anfrage' if als_h1 else 'kontakt.html#anfrage'}">Beratung anfragen{ICON_ARROW}</a></p>
      <p class="kontaktkarte__fuss">Rückruf mit Wunsch-Zeitfenster über das Formular. Karte: <a href="https://www.openstreetmap.org/?mlat=52.481&amp;mlon=10.547#map=10/52.481/10.547" target="_blank" rel="noopener">OpenStreetMap</a> © Mitwirkende, ODbL.</p>
    </div>
  </div>
</section>"""


RAEUME = [
    # (Schluessel, Titel, Bild, typ. Flaeche, kW-Spanne, Situation im Rechner, Kachelklasse)
    # bento__k--chip-r: Chip auf die geraeteabgewandte Seite, damit das Innengeraet frei bleibt.
    ("wohnzimmer", "Wohnzimmer", "raum-wohnzimmer.jpg", "25–40 m²", "2,0–3,5 kW", "bestand", "bento__k--2x"),
    ("schlafzimmer", "Schlafzimmer", "raum-schlafzimmer.jpg", "14–20 m²", "bis 2,5 kW", "bestand", "bento__k--chip-r"),
    ("dachgeschoss", "Dachgeschoss", "raum-dachgeschoss.jpg", "20–35 m²", "2,5–5,0 kW", "dach", "bento__k--hoch bento__k--chip-r"),
    ("kinderzimmer", "Kinderzimmer", "raum-kinderzimmer.jpg", "12–18 m²", "bis 2,5 kW", "bestand", "bento__k--chip-r"),
    ("arbeitszimmer", "Arbeitszimmer", "raum-arbeitszimmer.jpg", "12–20 m²", "bis 2,5 kW", "bestand", ""),
]


def bento(ziel="#rechner"):
    k = []
    for key, titel, bild, m2, kws, sit, kl in RAEUME:
        flaeche = re.match(r"(\d+)", m2).group(1)
        k.append(f"""<a class="bento__k {kl}" href="{ziel}" data-raum="{key}" data-situation="{sit}" data-flaeche="{int(flaeche) + 5}" data-titel="{e(titel)}">
      <img src="assets/{bild}" alt="{e(titel)} mit Innengerät einer Split-Klimaanlage – Einbausituation" width="1200" height="800" loading="lazy">
      {chip({"bestand": "80 W/m²", "dach": "130 W/m²"}[sit])}
      <span class="bento__t"><b>{e(titel)}</b><span>typisch {m2} · {kws}</span></span>
    </a>""")
    k.append(f"""<a class="bento__k bento__k--text" href="{ziel}" data-raum="frei" data-titel="Anderer Raum">
      <span class="pfeil" aria-hidden="true">{ICON_ARROW}</span>
      <b>Anderer Raum, andere Fläche.</b><span>Fläche eintragen, Dämmstandard wählen – der Rechner nennt die Kühllast in kW und die passenden Sets.</span>
    </a>""")
    return f"""<section class="sec" id="situationen" aria-labelledby="raeume-h">
  <div class="wrap">
    <div class="kopf2" data-reveal>
      <h2 id="raeume-h">Der Raum bestimmt <em>die Leistung.</em></h2>
      {chip("Richtwerte nach Faustformel")}
    </div>
    <div class="bento" data-reveal>{"".join(k)}</div>
  </div>
</section>"""


def rechner(als_kopf=False):
    """Rechner als Buehne: Eingabe-Karte links, Ergebnis-Produktkarte rechts. Logik in script.js."""
    h = "h1" if als_kopf else "h2"
    # Alle 9 Produktkarten als <template>: der Rechner klont den Treffer, statt SVG in JS nachzubauen.
    tpls = "".join(f'<template data-set-tpl="{s["id"]}">{produkt_karte(s, best=s["empfehlung"])}</template>' for s in K.SETS)
    return f"""<section class="buehne buehne--sec" id="rechner" aria-labelledby="rechner-h">
  <div class="wrap">
    <div class="kopf2" data-reveal>
      <{h} id="rechner-h">Kühllast berechnen: <em>Fläche, Dämmung, Zuschläge.</em></{h}>
      {chip("kW und BTU/h")}
    </div>
    <div class="rechner" id="konfigurator" data-reveal>
      <form class="karte rechner__eingabe" id="rechner-form" novalidate>
        <h3>Räume eintragen</h3>
        <ol id="raeume" class="raeume"></ol>
        <p><button type="button" class="rechner__hinzu" id="raum-hinzu">{ICON_PLUS}Raum hinzufügen</button></p>
        <div class="rechner__zeile">
          <div class="rechner__wunsch" role="radiogroup" aria-label="Bauart">
            <label><input type="radio" name="art" value="egal" checked>Bauart egal</label>
            <label><input type="radio" name="art" value="mobil">Ohne Bohren</label>
            <label><input type="radio" name="art" value="split">Split</label>
            <label><input type="radio" name="art" value="multi">Mehrere Räume</label>
          </div>
        </div>
      </form>
      <aside class="rechner__ergebnis" aria-live="polite">
        <div class="karte ergebnis">
          <div class="ergebnis__werte">
            <div class="wert"><small>Kühllast gesamt</small><b><span id="erg-kw">–</span><i>kW</i></b></div>
            <div class="wert"><small>entspricht</small><b><span id="erg-btu">–</span><i>BTU/h</i></b></div>
          </div>
          <div class="treffer" id="treffer"></div>
        </div>
      </aside>
    </div>
    <p class="rechenweg"><b>Rechenweg:</b> Fläche × spezifische Kühllast (60 W/m² Neubau · 80 Bestand · 100 Altbau · 130 Dachgeschoss). Zuschläge: große Süd-/Westverglasung +20 W/m² · Raumhöhe über 2,60 m +10 % · Technik oder offene Küche +300 W. Bei mehreren Räumen wird das Außengerät auf 85 % der Summe ausgelegt. Richtwert nach Faustformel – ersetzt keine Kühllastberechnung nach VDI 2078 bzw. DIN EN 12831-1. Ab 6 kW legen wir vor Ort aus.</p>
    {tpls}
  </div>
</section>"""


def bestseller_reihe():
    best = [s for s in K.SETS if s["empfehlung"]]
    karten = "".join(produkt_karte(s, best=True) for s in best)
    treffer_leer = K.set_by_id("split-25")
    return f"""<section class="sec" id="einstieg" aria-labelledby="best-h">
  <div class="wrap">
    <div class="kopf2" data-reveal>
      <h2 id="best-h">Zum Einstieg: zwei Empfehlungen <em>und Ihr Treffer.</em></h2>
      {chip("Preis lt. Schalter")}
    </div>
    <div class="produkte" data-reveal>
      {karten}
      <div id="treffer-karte" class="pk-slot" data-leer="{treffer_leer["id"]}">{produkt_karte(treffer_leer)}</div>
    </div>
    <div style="margin-top:var(--s3)">{demo_zeile()}</div>
  </div>
</section>"""


def kategorien_buehne():
    kacheln = f"""<a class="kat" href="shop-split.html">
        <img src="assets/innengeraet.jpg" alt="Wandmontiertes Innengerät einer Split-Klimaanlage" width="1000" height="666" loading="lazy">
        {chip("4 Sets")}
        <span class="kat__t"><b>Split-Sets</b><span>Ein Raum · 2,5 bis 7,0 kW · Quick-Connect selbst einbaubar</span></span>
      </a>
      <a class="kat" href="shop-multisplit.html">
        <img src="assets/gewerbe.jpg" alt="Büroraum mit Innengerät einer Klimaanlage" width="1200" height="801" loading="lazy">
        {chip("3 Sets")}
        <span class="kat__t"><b>Multi-Split-Sets</b><span>Zwei bis vier Räume · ein Außengerät an der Fassade</span></span>
      </a>
      <a class="kat kat--buehne" href="shop-mobil.html">
        {geraet_svg("mono", kw=2.0)}
        {chip("2 Geräte")}
        <span class="kat__t"><b>Mobile Geräte</b><span>Ohne Bohren, ohne Genehmigung · aufstellen und einstecken</span></span>
      </a>
      <a class="kat kat--buehne" href="shop-zubehoer.html">
        {geraet_svg("zubehoer")}
        {chip(f"{len(K.ZUBEHOER)} Positionen")}
        <span class="kat__t"><b>Zubehör</b><span>Konsolen, Kondensatpumpe, Wanddurchführung, Leitungskanal</span></span>
      </a>"""
    return f"""<section class="sec sec--cool" id="kategorien" aria-labelledby="kat-h">
  <div class="wrap">
    <div class="kopf2" data-reveal>
      <h2 id="kat-h">Alle Sets nach Bauart.</h2>
      {chip("Abholung · Montage")}
    </div>
    <div class="kats" data-reveal>{kacheln}</div>
  </div>
</section>"""


def montage_kapitel():
    montage = [
        ("Anruf oder Anfrage", "Anruf, WhatsApp oder Formular – mit Raumgröße, Geschoss und Baujahr."),
        ("Besichtigung", "Wir sehen uns Räume, Fenster, Leitungsweg und Fassade an."),
        ("Auslegung", "Kühllast je Raum, Gerätegröße, Leitungsführung und Kondensatweg – rechnerisch, nicht nach Gefühl."),
        ("Angebot", "Schriftlich, unverbindlich, mit Festpreis und klarem Montageumfang."),
        ("Montage", "Termin nach Absprache, in der Regel ein Arbeitstag je Anlage."),
        ("Einweisung", "Inbetriebnahme, Messung, Übergabe – und auf Wunsch die Wartung danach."),
    ]
    selbst = [
        ("Set wählen", "Mobil oder Quick-Connect – der Rechner nennt die Leistung, der Katalog das Set."),
        ("Anfragen", "Set anfragen, schriftliches Angebot bekommen, Abholtermin abstimmen."),
        ("Abholen", "Am Zeisigweg 4 in Gifhorn. Wer möchte, lässt sich das Set erklären."),
        ("Selbst einbauen", "Quick-Connect: Halter setzen, Leitung kuppeln – der Kältekreis bleibt geschlossen. Mobil: aufstellen, einstecken."),
        ("Bei Fragen anrufen", "Kernbohrung oder Elektroanschluss übernehmen wir auf Wunsch auch beim Selbsteinbau."),
    ]
    def strecke(items, kl):
        return f'<ol class="strecke strecke--5 strecke--{len(items)} {kl}">' + "".join(
            f'<li class="schritt" data-reveal style="--d:{i}"><span class="schritt__nr">0{i + 1}</span><h3>{t}</h3><p>{d}</p></li>'
            for i, (t, d) in enumerate(items)) + "</ol>"
    return f"""<section class="kap kap--ueber" id="montage" aria-labelledby="montage-h">
  <div class="kap__bild"><img src="assets/aussengeraet.jpg" alt="Außengerät einer Split-Klimaanlage an einer weißen Fassade unter blauem Himmel" width="1200" height="800" loading="lazy" data-parallax="0.12"></div>
  <div class="kap__innen">
    <div>
      <h2 id="montage-h"><span class="nur-montage">Einbauen lassen: <em>in der Regel ein Arbeitstag.</em></span><span class="nur-selbst">Selbst einbauen: <em>abholen, anschließen, einstecken.</em></span></h2>
    </div>
    <div class="kap__slot">
      <p class="kap__lead nur-montage">Kernbohrung, Halter, Leitungsweg, Vakuumieren, Inbetriebnahme, Einweisung – und ein Festpreis, der im Angebot steht, bevor wir bohren.</p>
      <p class="kap__lead nur-selbst">Mobile Geräte und Quick-Connect-Sets dürfen Sie selbst anschließen – der Kältekreis bleibt geschlossen. Wo die Grenze liegt, steht im Ratgeber.</p>
      <div class="chips">{chip("Festpreis inkl. Montage")}{chip("Ein Ansprechpartner")}</div>
      <p class="btns"><a class="btn btn--hell nur-montage" href="montage.html">Was am Montagetag passiert{ICON_ARROW}</a><a class="btn btn--hell nur-selbst" href="ratgeber-selbsteinbau.html">Was darf ich selbst einbauen?{ICON_ARROW}</a></p>
    </div>
  </div>
</section>
<section class="sec sec--cool" id="ablauf" aria-label="Ablauf Schritt für Schritt">
  <div class="wrap fk__ueber">{strecke(montage, "nur-montage")}{strecke(selbst, "nur-selbst")}</div>
</section>"""


def energie_kapitel():
    karten = f"""<a class="karte fk" href="energetische-beratung.html#ausweis" data-reveal style="--d:0">
      <div class="fk__bild"><img src="assets/energieausweis.jpg" alt="Wohnhäuser mit Sattel- und Solardächern" width="1200" height="800" loading="lazy"></div>
      <div class="fk__body"><h3>Energieausweis</h3><p>Verbrauchs- oder Bedarfsausweis für Wohn- und Nichtwohngebäude – ausgestellt von einem dena-Energieberater.</p><span class="fk__mehr">Mehr dazu{ICON_ARROW}</span></div>
    </a>
    <a class="karte fk" href="energetische-beratung.html#waerme" data-reveal style="--d:1">
      <div class="fk__bild"><img src="assets/daemmung.jpg" alt="Dämmarbeiten an einer Gebäudefassade" width="1200" height="800" loading="lazy"></div>
      <div class="fk__body"><h3>Wärmebrücken finden</h3><p>Per Thermografie sichtbar machen, wo Wärme aus- und im Sommer eintritt. Der Unterschied zwischen Vermuten und Messen.</p><span class="fk__mehr">Mehr dazu{ICON_ARROW}</span></div>
    </a>
    <a class="karte fk fk--tint" href="energetische-beratung.html#plan" data-reveal style="--d:2">
      <div class="fk__body">{chip("Sanierungsplan", "chip--hell")}<h3>Maßnahmen ableiten</h3><p>Priorisiert nach Wirkung und Aufwand – damit klar ist, was zuerst gemacht werden sollte und was warten kann.</p>
      <ul class="fk__liste"><li>Dämmung von Dach, Fassade, Kellerdecke</li><li>Fenster, Heizung, Lüftung</li><li>Photovoltaik und Warmwasser</li></ul><span class="fk__mehr">Zur energetischen Beratung{ICON_ARROW}</span></div>
    </a>"""
    return f"""<section class="kap kap--ueber" id="energie" aria-labelledby="energie-h">
  <div class="kap__bild"><img src="assets/sonne-vorhang.jpg" alt="Sonnenlicht fällt durch einen weißen Vorhang auf den Boden" width="1400" height="933" loading="lazy" data-parallax="0.1"></div>
  <div class="kap__innen">
    <div><h2 id="energie-h">Wenn das Haus <em>schon warm hereinlässt.</em></h2></div>
    <div class="kap__slot"><p class="kap__lead">Eine Klimaanlage arbeitet gegen die Gebäudehülle an. Deshalb sehen wir uns zuerst an, wo die Wärme überhaupt hereinkommt – und ob eine Maßnahme an der Hülle nicht mehr bringt als mehr Kilowatt.</p><div class="chips">{chip("dena-Energieberater")}{chip("TÜV-zertifizierter Fachbetrieb")}</div></div>
  </div>
</section>
<section class="sec sec--eng" id="energie-leistungen" aria-label="Energetische Leistungen">
  <div class="wrap"><div class="karten fk__ueber">{karten}</div></div>
</section>"""


def pv_split():
    return f"""<section class="sec" id="pv" aria-labelledby="pv-h">
  <div class="wrap">
    <div class="split split--r">
      <div class="split__bild" data-reveal="wipe-right"><img src="assets/pv-dach-2.jpg" alt="Ziegeldach mit Photovoltaikmodulen" width="1400" height="933" loading="lazy"></div>
      <div class="split__text" data-reveal>
        <h2>Kühlen mit dem <em>eigenen Strom.</em></h2>
        <p>Es gibt wenige Verbraucher, deren Bedarf so genau zur Erzeugung passt: Gekühlt wird, wenn die Sonne scheint. Wer eine Photovoltaikanlage hat, betreibt die Klimaanlage weitgehend mit eigenem Strom – ohne sein Verhalten zu ändern.</p>
        <p>Ist noch keine Anlage da, planen wir die Klimaanlage so, dass eine spätere dazupasst – und rechnen in der energetischen Beratung durch, ob sich PV für Ihr Dach lohnt.</p>
        <p class="btns"><a class="btn btn--rand" href="ratgeber-pv.html">Ausführlich nachlesen{ICON_ARROW}</a></p>
      </div>
    </div>
  </div>
</section>"""


RATGEBER = [
    ("ratgeber-groesse.html", "Welche Leistung braucht mein Raum?", "Faustformel, Zuschläge und warum zu groß genauso falsch ist wie zu klein.", "hero.jpg", "4 Min."),
    ("ratgeber-kosten.html", "Was kostet eine Klimaanlage?", "Set, Montage und Strom getrennt – und was den Montagepreis bewegt.", "buero.jpg", "4 Min."),
    ("ratgeber-selbsteinbau.html", "Was darf ich selbst einbauen?", "Quick-Connect ja, offener Kältekreis nein – und was in der Miete gilt.", "raum-schlafzimmer-2.jpg", "3 Min."),
    ("ratgeber-pv.html", "Klimaanlage und Photovoltaik – passt das?", "Kühlbedarf und Solarertrag fallen zeitlich zusammen – der seltene Glücksfall.", "pv-dach.jpg", "3 Min."),
]
BILD_ALT = {
    "hero.jpg": "Offener Wohn- und Küchenbereich mit Innengerät einer Klimaanlage",
    "hero-wohnzimmer.jpg": "Helles Wohnzimmer mit Innengerät über dem Fenster",
    "buero.jpg": "Büro mit weißem Schreibtisch und Innengerät an der Wand",
    "gewerbe.jpg": "Büroetage mit Innengerät einer Klimaanlage",
    "raum-schlafzimmer-2.jpg": "Schlafzimmer mit Innengerät über dem Bett",
    "raum-schlafzimmer.jpg": "Schlafzimmer mit Innengerät einer Klimaanlage",
    "raum-wohnzimmer.jpg": "Wohnzimmer mit Innengerät über dem Fenster",
    "raum-kinderzimmer.jpg": "Kinderzimmer mit Innengerät einer Klimaanlage",
    "raum-arbeitszimmer.jpg": "Arbeitszimmer mit Regal, Schreibtisch und Innengerät",
    "raum-dachgeschoss.jpg": "Dachgeschoss mit Dachfenstern und Innengerät",
    "pv-dach.jpg": "Haus mit Photovoltaikanlage auf dem Dach unter blauem Himmel",
    "pv-dach-2.jpg": "Ziegeldach mit Photovoltaikmodulen",
    "wohnraum.jpg": "Heller Wohnraum mit hoher Fensterfront",
    "innengeraet.jpg": "Wandmontiertes Innengerät einer Split-Klimaanlage",
    "aussengeraet.jpg": "Außengerät an einer weißen Fassade",
    "fernbedienung.jpg": "Hand mit Fernbedienung vor einem Innengerät",
    "sonne-vorhang.jpg": "Sonnenlicht durch einen weißen Vorhang",
    "daemmung.jpg": "Dämmarbeiten an einer Fassade mit Gerüst",
    "energieausweis.jpg": "Wohnhäuser mit Sattel- und Solardächern",
}


def alt(bild):
    return e(BILD_ALT.get(bild, ""))


def wissen():
    import kt38_prosa as P
    karten = "".join(f"""<a class="karte fk" href="{d}" data-reveal style="--d:{i}">
      <div class="fk__bild"><img src="assets/{b}" alt="{alt(b)}" width="1200" height="800" loading="lazy"></div>
      <div class="fk__body">{chip("Lesezeit " + P.lesezeit_von(P.partial(d.replace(".html", ""))), "chip--rand")}<h3>{e(t)}</h3><p>{e(k)}</p><span class="fk__mehr">Lesen{ICON_ARROW}</span></div>
    </a>""" for i, (d, t, k, b, z) in enumerate(RATGEBER))
    faq = f"""<a class="karte fk fk--breit fk--tint" href="faq.html" data-reveal style="--d:4">
      <div class="fk__body">
        {chip("14 Antworten")}
        <h3>Häufige Fragen</h3>
        <ul class="fk__liste"><li>Wie lange dauert der Einbau?</li><li>Wie laut ist so eine Anlage?</li><li>Brauche ich die Zustimmung des Vermieters?</li></ul>
        <span class="fk__mehr">Alle Fragen{ICON_ARROW}</span>
      </div>
      <div class="fk__bild"><img src="assets/wohnraum.jpg" alt="Heller Wohnraum mit hoher Fensterfront" width="1400" height="988" loading="lazy"></div>
    </a>"""
    return f"""<section class="sec sec--cool" id="wissen" aria-labelledby="wissen-h">
  <div class="wrap">
    <div class="kopf2" data-reveal>
      <h2 id="wissen-h">Was Sie vor dem Angebot <em>wissen sollten.</em></h2>
      {chip("Ohne Anruf nachlesbar")}
    </div>
    <div class="karten karten--4">{karten}{faq}</div>
  </div>
</section>"""


def mitwem():
    return f"""<section class="sec sec--eng" id="mitwem" aria-labelledby="mitwem-h">
  <div class="wrap">
    <div class="band" data-reveal>
      <div class="band__logo"><img src="assets/brand/logo.png" alt="InTroTech GmbH – Leckageortung, Trocknung, Sanierung, Energetische Beratung" width="1320" height="262" loading="lazy"></div>
      <div>
        <h2 id="mitwem-h" style="font-size:var(--fs-4);margin-bottom:.5rem">KlimaTech38 ist ein Geschäftsbereich <em>der InTroTech GmbH, Gifhorn.</em></h2>
        <p>Wir kommen aus der Schadensanierung: Leckageortung, Trocknung, Schimmel- und Asbestsanierung. Wer täglich sieht, was Feuchte und Wärme in einem Gebäude anrichten, plant eine Klimaanlage anders – mit Blick auf Kondensat, Dämmung und die Energiebilanz des ganzen Hauses. Geschäftsführung: Johann Warkentin, Jonathan Mangold, Adrian Mangold.</p>
      </div>
      <div class="chips">{chip("dena-Energieberater", "chip--deep")}{chip("TÜV-zertifizierter Fachbetrieb", "chip--deep")}</div>
    </div>
  </div>
</section>"""


# --------------------------------------------------------------------- produkte.js

def schreibe_produkte_js():
    daten = {
        "meta": K.META,
        "kategorien": [{k: v for k, v in kat.items() if k != "lead"} for kat in K.KATEGORIEN],
        "sets": [dict(s, btu=K.btu(s["kw"])) for s in K.SETS],
        "zubehoer": K.ZUBEHOER,
        "raeume": [{"key": r[0], "titel": r[1], "situation": r[5]} for r in RAEUME],
    }
    js = f"""/* ============================================================================
   assets/produkte.js — GENERIERT aus .tools/kt38_katalog.py.
   NICHT VON HAND AENDERN: `python3 .tools/gen_kt38_shop.py` ueberschreibt die Datei.
   ========================================================================== */
window.KT38 = {json.dumps(daten, ensure_ascii=False, indent=2)};
window.KT38.eur = function (cent) {{
  if (cent === null || cent === undefined) {{ return ''; }}
  return (cent / 100).toLocaleString('de-DE', {{ style: 'currency', currency: 'EUR', minimumFractionDigits: 2 }});
}};
if (window.KT38.meta.demo) {{ document.documentElement.dataset.preisDemo = '1'; }}
"""
    (SITE / "assets" / "produkte.js").write_text(js, encoding="utf-8")
    return "assets/produkte.js"


# --------------------------------------------------------------------- Startseite

def business_ld():
    return {
        "@context": "https://schema.org", "@type": "HVACBusiness",
        "@id": f"{DOMAIN}/#business",
        "name": "KlimaTech38", "legalName": "InTroTech GmbH",
        "description": "Energetische Beratung, Planung, Auslegung, Verkauf und Montage von Klimaanlagen sowie "
                       "Energieausweise für Wohn- und Nichtwohngebäude in Gifhorn, Wolfsburg und Braunschweig.",
        "url": f"{DOMAIN}/", "logo": f"{DOMAIN}/assets/brand/logo.png",
        "image": f"{DOMAIN}/assets/hero-wohnzimmer.jpg",
        "telephone": "+49 5371 8759972", "email": "info@introtech.de", "vatID": "DE460142356",
        "parentOrganization": {"@type": "Organization", "name": "InTroTech GmbH", "url": "https://www.introtech.de/"},
        "address": {"@type": "PostalAddress", "streetAddress": "Zeisigweg 4", "postalCode": "38518",
                    "addressLocality": "Gifhorn", "addressRegion": "Niedersachsen", "addressCountry": "DE"},
        "geo": {"@type": "GeoCoordinates", "latitude": 52.481, "longitude": 10.547},
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
                                       "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                                       "opens": "08:00", "closes": "18:00"}],
        "areaServed": [{"@type": "City", "name": n} for n in ORTE],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Leistungen KlimaTech38",
                            "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": n}} for n in [
                                "Energieausweis für Wohn- und Nichtwohngebäude",
                                "Energetische Beratung und Planung",
                                "Planung und Auslegung von Klimaanlagen",
                                "Lieferung und Montage von Split- und Multi-Split-Klimaanlagen",
                                "Wartung von Klimaanlagen",
                                "Kopplung von Klimaanlage und Photovoltaik"]]},
    }


def startseite():
    datei = "index.html"
    ab_montiert = K.eur(K.guenstigster_montagepreis())
    ab_abholung = K.eur(K.guenstigster_abholpreis())
    demo = f'<span class="preis-demo">{e(K.META["demoWort"])}</span>' if K.META["demo"] else ""
    beschr = ("Klimaanlagen für Gifhorn, Wolfsburg und Braunschweig: Sets zum Selbsteinbau oder mit Montage, "
              "kostenlose Beratung vor Ort. Dazu Energieausweise.")
    if not K.META["demo"]:
        beschr = (f"Klimaanlagen aus Gifhorn: Sets ab {ab_abholung} zur Abholung, montiert ab {ab_montiert}. "
                  f"Kostenlose Beratung vor Ort, Auslegung, Montage und Wartung.")
    t = S.kopf("Klimaanlagen Gifhorn – Sets, Montage & Energieberatung | KlimaTech38", beschr, datei, business_ld())

    t += f"""
<section class="hero" id="hero" aria-labelledby="hero-h">
  <div class="hero__bild"><img src="assets/hero-wohnzimmer.jpg" alt="Helles Wohnzimmer mit hellblauem Sofa, über dem Fenster das Innengerät einer Split-Klimaanlage" width="1800" height="1201" fetchpriority="high"></div>
  <div class="hero__innen">
    <div class="hero__panel">
      <h1 id="hero-h">Erst auslegen. <em>Dann kühlen.</em></h1>
      <p class="hero__lead">Klimaanlagen für Wohnung, Haus und Gewerbe zwischen Gifhorn, Wolfsburg und Braunschweig – als Komplettset zum Selbsteinbau oder von uns ausgelegt und montiert. Dazu Energieausweise und energetische Beratung.</p>
      <div class="hero__wahl">
        {C.weg_schalter(gross=True)}
        <span class="weg__hint weg__hint--selbst">Set aussuchen, in Gifhorn abholen, selbst einbauen – mobil oder Quick-Connect.</span>
        <span class="weg__hint weg__hint--montage">Besichtigung, Auslegung, Festpreis-Angebot, Montage, Wartung.</span>
        <div class="hero__anker">
          <span class="preis"><span class="preis__w preis__w--selbst"><b>ab {e(ab_abholung)}</b>{demo}<small>Komplettset zur Abholung</small></span><span class="preis__w preis__w--montage"><b>ab {e(ab_montiert)}</b>{demo}<small>Split-Anlage inkl. Montage</small></span></span>
        </div>
      </div>
      <p class="hero__cta"><a class="btn btn--primary btn--gross" href="kontakt.html">Beratung anfragen</a><a class="btn btn--hell" href="shop.html">Sets &amp; Preise{ICON_ARROW}</a></p>
      <p class="hero__fakten"><i>Gifhorn · Wolfsburg · Braunschweig</i>&nbsp;<span aria-hidden="true">–</span> <i>Besichtigung und Angebot kostenfrei</i>&nbsp;<span aria-hidden="true">–</span> <i>dena-Energieberater · TÜV-zertifizierter Fachbetrieb</i></p>
    </div>
  </div>
</section>
{bento()}
{rechner()}
{bestseller_reihe()}
{kategorien_buehne()}
{montage_kapitel()}
{energie_kapitel()}
{pv_split()}
{wissen()}
{mitwem()}
{kontakt_vollbild()}
"""
    t += S.fuss("voll")
    return datei, t


# --------------------------------------------------------------------- Shop-Uebersicht

def shopseite():
    datei = "shop.html"
    ld = {"@context": "https://schema.org", "@type": "CollectionPage",
          "name": "Klimaanlagen-Sets und Preise",
          "description": "Komplettsets für ein oder mehrere Räume, Auslegungs-Rechner und Zubehör von KlimaTech38 in Gifhorn.",
          "isPartOf": {"@id": f"{DOMAIN}/#business"}}
    t = S.kopf("Klimaanlagen-Sets & Preise – Split, Multi-Split, mobil | KlimaTech38",
               "Klimaanlagen-Sets von KlimaTech38, Gifhorn: Split, Multi-Split und mobile Geräte zum Selbsteinbau "
               "oder mit Montage. Mit Auslegungs-Rechner für die Kühllast.", datei, ld)
    gruppen = []
    for kat in K.KATEGORIEN:
        if kat["id"] == "zubehoer":
            continue
        sets = K.sets_der_kategorie(kat["id"])
        karten = mit_rest("".join(produkt_karte(s, best=s["empfehlung"], gross=s["empfehlung"], voll=(len(sets) == 4)) for s in bestseller_zuerst(sets)), sets, len(sets) == 4)
        spanne = f'{min(s["flaecheVon"] for s in sets)}–{max(s["flaecheBis"] for s in sets)} m²'
        raster = "produkte" if len(sets) == 4 else "produkte produkte--2"
        gruppen.append(f"""<div class="gruppe" id="{kat["id"]}">
      <div class="kopf2" data-reveal><h2>{e(kat["kurz"])} <em>· {len(sets)} Sets</em></h2>{chip(spanne)}</div>
      <div class="{raster}">{karten}</div>
    </div>""")
    zub = "".join(zubehoer_karte(z) for z in K.ZUBEHOER)
    t += f"""
<section class="katalog-kopf" aria-labelledby="shop-h">
  <div class="wrap">
    <div class="katalog-kopf__oben">
      <div>
        <h1 id="shop-h">Sets &amp; Preise. <em>Für beide Wege.</em></h1>
        <p class="katalog-kopf__lead">Jedes Set hat zwei Preise: zur Abholung in Gifhorn – oder von uns ausgelegt und eingebaut. Der Schalter zeigt den Preis Ihres Weges.</p>
      </div>
      <div>{C.weg_schalter(gross=True)}</div>
    </div>
    <div class="kats" data-reveal>
      <a class="kat" href="#split"><img src="assets/innengeraet.jpg" alt="Innengerät einer Split-Klimaanlage" width="1000" height="666" loading="lazy">{chip("4 Sets")}<span class="kat__t"><b>Split-Sets</b><span>Ein Raum</span></span></a>
      <a class="kat" href="#multi"><img src="assets/gewerbe.jpg" alt="Büroetage mit Innengerät einer Klimaanlage" width="1200" height="800" loading="lazy">{chip("3 Sets")}<span class="kat__t"><b>Multi-Split</b><span>2–4 Räume</span></span></a>
      <a class="kat kat--buehne" href="#mobil">{geraet_svg("mono", kw=2.0)}{chip("2 Geräte")}<span class="kat__t"><b>Mobile Geräte</b><span>Ohne Bohren</span></span></a>
      <a class="kat kat--buehne" href="#zubehoer">{geraet_svg("zubehoer")}{chip(f"{len(K.ZUBEHOER)} Positionen")}<span class="kat__t"><b>Zubehör</b><span>Konsolen, Pumpe, Kanal</span></span></a>
    </div>
    <div style="margin-top:var(--s3)">{demo_zeile()}</div>
  </div>
</section>
{rechner()}
<section class="sec" aria-label="Alle Sets">
  <div class="wrap">
    {"".join(gruppen)}
    <div class="gruppe" id="zubehoer">
      <div class="kopf2" data-reveal><h2>Zubehör und Montagematerial.</h2>{chip(f"{len(K.ZUBEHOER)} Positionen")}</div>
      <div class="karten karten--2">{zub}</div>
    </div>
    <div class="karten karten--2" style="margin-top:var(--s5)">
      <div class="karte fk fk--deep" data-reveal>
        <div class="fk__body">{chip("Selbsteinbau", "chip--sky")}<h3>Wo die Grenze liegt</h3>
        <p>Mobile Geräte und vorgefüllte Quick-Connect-Sets dürfen Sie selbst anschließen – der Kältekreis bleibt geschlossen. Sobald ein Kältekreis geöffnet, evakuiert oder befüllt wird, greift die F-Gase-Verordnung (EU) 2024/573 und verlangt einen Sachkundenachweis. Deshalb bauen wir ab 5,0 kW und bei jeder Multi-Split-Anlage ein.</p>
        <a class="fk__mehr" href="ratgeber-selbsteinbau.html">Was darf ich selbst einbauen?{ICON_ARROW}</a></div>
      </div>
      <div class="karte fk" data-reveal style="--d:1">
        <div class="fk__body">{chip("Abholung · Lieferung · Montage")}<h3>So kommt das Set zu Ihnen</h3>
        <p>{e(K.META["preisFuss"])}</p>
        <p>{e(K.META["keinKaufHinweis"])}</p></div>
      </div>
    </div>
  </div>
</section>
{abschluss("Unsicher, welches Set passt: wir legen aus.", "Besichtigung, Auslegung und Angebot sind kostenfrei – wir sagen Ihnen auch, wenn ein kleineres Set reicht.", ("Beratung anfragen", "kontakt.html"), ("Selbsteinbau-Ratgeber", "ratgeber-selbsteinbau.html"))}
"""
    t += S.fuss("voll")
    return datei, t


def mit_rest(karten_html, sets, voll):
    """Bei 2 Spalten (Tablet) darf keine Karte allein in der letzten Reihe stehen: die letzte
       Karte bekommt dann `pk--rest` (Querformat, volle Breite). Empfehlung zaehlt 2 Zellen (span 2)
       bzw. 0 Rest-Zellen, wenn sie vollbreit (`voll`) steht."""
    zellen = 0
    for s in sets:
        zellen += 0 if (s["empfehlung"] and voll) else (2 if s["empfehlung"] else 1)
    if zellen % 2 == 1:
        i = karten_html.rfind('<article class="karte pk')
        karten_html = karten_html[:i] + karten_html[i:].replace('class="karte pk', 'class="karte pk pk--rest', 1)
    return karten_html


def bestseller_zuerst(sets):
    """Die Empfehlung traegt die grosse Karte (span 2) — im Raster steht sie deshalb vorn."""
    return sorted(sets, key=lambda s: (not s["empfehlung"], s["kw"]))


def zubehoer_karte(z, mit_passt=True):
    demo = f'<small>{e(K.META["demoWort"])}</small>' if K.META["demo"] else "<small>inkl. MwSt.</small>"
    passt = ""
    if mit_passt:
        links = "".join(f'<a href="set-{sid}.html">{e(K.set_by_id(sid)["titel"].replace("Mobiles Monoblock-Gerät", "Mobil").replace("Multi-Split-Set ", "Multi "))}</a>' for sid in z["passendZu"])
        passt = f'<p class="zub__passt"><span>passt zu</span>{links}</p>'
    return f"""<article class="karte zub" data-reveal>
  <span class="zub__i">{ZUB_ICONS.get(z["id"], ICON_BOX)}</span>
  <div><h3>{e(z["titel"])}</h3><p>{e(z["zweck"])}</p></div>
  <p class="zub__preis">{e(K.eur(z["preis_cent"]))}{demo}</p>
  {passt}
</article>"""


# --------------------------------------------------------------------- Kategorieseiten

KAT_KOPF = {
    "split": ("1 Raum · 18–85 m²", "split1", "Ein Raum <em>soll kühl werden.</em>"),
    "multi": ("2–4 Räume · 35–115 m²", "multi3", "Mehrere Räume, <em>ein Gerät an der Fassade.</em>"),
    "mobil": ("Ohne Bohren · 12–26 m²", "mono", "Aufstellen, Schlauch nach draußen, <em>einstecken.</em>"),
    "zubehoer": ("7 Positionen", "zubehoer", "Was außer dem Gerät <em>noch nötig ist.</em>"),
}


def filter_leiste(kat, sets):
    if kat["id"] == "zubehoer":
        return ""
    flaechen = [("bis 20 m²", "0-20"), ("20–40 m²", "20-40"), ("40–70 m²", "40-70"), ("über 70 m²", "70-999")]
    fl = "".join(f'<label><input type="checkbox" name="flaeche" value="{v}">{t}</label>' for t, v in flaechen)
    einbau = ('<label><input type="checkbox" name="einbau" value="selbst">selbst möglich</label>'
              '<label><input type="checkbox" name="einbau" value="montage">nur mit Montage</label>')
    preise = "".join(f'<label><input type="checkbox" name="preis" value="{v}">{t}</label>'
                     for t, v in [("bis 1.000 €", "0-100000"), ("1.000–2.500 €", "100000-250000"), ("über 2.500 €", "250000-99999999")])
    return f"""<form class="filter" id="filter" aria-label="Sets filtern">
      <fieldset><div class="filter__gruppe"><legend>Raumgröße</legend>{fl}</div></fieldset>
      <fieldset><div class="filter__gruppe"><legend>Einbau</legend>{einbau}</div></fieldset>
      <fieldset><div class="filter__gruppe"><legend>Preis (Abholung)</legend>{preise}</div></fieldset>
      <span class="filter__stand" id="filter-stand" aria-live="polite">{len(sets)} von {len(sets)} Sets</span>
      <button type="reset" class="filter__reset">Zurücksetzen</button>
    </form>"""


def kategorieseite(kat):
    sets = K.sets_der_kategorie(kat["id"])
    datei = kat["datei"]
    ld = {"@context": "https://schema.org", "@type": "ItemList", "name": kat["titel"],
          "description": kat["lead"][:180], "numberOfItems": len(sets),
          "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": s["titel"], "url": f"{DOMAIN}/set-{s['id']}.html"}
                              for i, s in enumerate(sets)]}
    if kat["id"] == "zubehoer":
        ld = {"@context": "https://schema.org", "@type": "ItemList", "name": kat["titel"], "numberOfItems": len(K.ZUBEHOER),
              "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": z["titel"]} for i, z in enumerate(K.ZUBEHOER)]}
    t = S.kopf(f'{kat["kurz"]} – Preise & Auslegung | KlimaTech38',
               f'{kat["kurz"]} von KlimaTech38 in Gifhorn: Leistung, Raumgröße, Lieferumfang und Preis für Abholung oder Montage.',
               datei, ld)
    spanne, schema, h1 = KAT_KOPF[kat["id"]]
    t += f"""
<section class="buehne buehnen-kopf" aria-labelledby="kat-h">
  <div class="buehnen-kopf__innen">
    <div>
      <p class="brot"><a href="index.html">Start</a><span aria-hidden="true">/</span><a href="shop.html">Sets &amp; Preise</a><span aria-hidden="true">/</span><span aria-current="page">{e(kat["kurz"])}</span></p>
      <h1 id="kat-h">{h1}</h1>
      <p class="buehnen-kopf__lead">{e(kat["lead"])}</p>
      <div class="chips" style="margin-bottom:var(--s3)">{chip(spanne, "chip--hell")}</div>
      {C.weg_schalter() if kat["id"] != "zubehoer" else ""}
    </div>
    <div class="buehnen-kopf__geraet">{geraet_svg(schema, titel=kat["kurz"])}</div>
  </div>
</section>
<section class="sec" aria-labelledby="liste-h">
  <div class="wrap">
    <h2 class="sr" id="liste-h">{"Zubehör – alle Positionen" if kat["id"] == "zubehoer" else "Alle " + e(kat["kurz"])}</h2>
    {demo_zeile()}
    <div style="height:var(--s3)"></div>
"""
    if kat["id"] == "zubehoer":
        t += f'<div class="karten karten--2">{"".join(zubehoer_karte(z) for z in K.ZUBEHOER)}</div>'
        t += f'<p style="margin-top:var(--s4)" class="demo-hinweis">{ICON_INFO}<span>Wenn wir montieren, ist das passende Zubehör im Angebot enthalten – diese Liste ist für alle, die selbst einbauen.</span></p>'
    else:
        t += filter_leiste(kat, sets)
        karten = "".join(
            produkt_karte(s, best=s["empfehlung"], gross=s["empfehlung"], voll=(len(sets) == 4),
                          attrs=f' data-flaeche-von="{s["flaecheVon"]}" data-flaeche-bis="{s["flaecheBis"]}" '
                                f'data-einbau="{"selbst" if s["selbsteinbau"] else "montage"}" data-preis="{s["preise"]["abholung_cent"]}"')
            for s in bestseller_zuerst(sets))
        raster = "produkte" if len(sets) == 4 else "produkte produkte--2"
        karten = mit_rest(karten, sets, len(sets) == 4)
        t += f'<div class="{raster}" id="set-liste">{karten}</div><p class="leer" id="filter-leer" hidden>Kein Set passt zu dieser Auswahl – setzen Sie einen Filter zurück oder <a href="beratung.html">fragen Sie uns</a>.</p>'
    # Nachbarkategorien
    andere = [k for k in K.KATEGORIEN if k["id"] != kat["id"]][:2]
    KAT_SUB = {"split": "Ein Raum · 2,5 bis 7,0 kW · Quick-Connect selbst einbaubar", "multi": "Zwei bis vier Räume · ein Außengerät an der Fassade",
               "mobil": "Ohne Bohren, ohne Genehmigung · aufstellen und einstecken", "zubehoer": "Konsolen, Kondensatpumpe, Wanddurchführung, Leitungskanal"}
    nachbar = "".join(f'<a class="kat" href="{k["datei"]}"><img src="assets/{ {"split": "innengeraet.jpg", "multi": "gewerbe.jpg", "mobil": "fernbedienung.jpg", "zubehoer": "aussengeraet.jpg"}[k["id"]]}" alt="{e(k["kurz"])}" width="1000" height="666" loading="lazy"><span class="kat__t"><b>{e(k["kurz"])}</b><span>{KAT_SUB[k["id"]]}</span></span></a>' for k in andere)
    t += f"""
    <div class="kopf2" style="margin-top:var(--s5)" data-reveal><h2>Andere Bauarten.</h2></div>
    <div class="kats kats--2" data-reveal>{nachbar}</div>
  </div>
</section>
{abschluss("Das passende Set ergibt sich aus dem Raum.", "Der Rechner gibt einen Richtwert – die verbindliche Auslegung machen wir vor Ort, kostenfrei.", ("Beratung anfragen", "kontakt.html"), ("Kühllast berechnen", "index.html#rechner"))}
"""
    t += S.fuss("voll")
    return datei, t


# --------------------------------------------------------------------- Set-Seiten

def setseite(s):
    datei = f"set-{s['id']}.html"
    kat = next(k for k in K.KATEGORIEN if k["id"] == s["kategorie"])
    ld = {"@context": "https://schema.org", "@type": "Product", "name": s["titel"], "description": s["kurz"],
          "category": kat["titel"],
          "additionalProperty": [
              {"@type": "PropertyValue", "name": "Kühlleistung", "value": f'{s["kw"]} kW'},
              {"@type": "PropertyValue", "name": "Raumgröße", "value": f'{s["flaecheVon"]}–{s["flaecheBis"]} m²'},
              {"@type": "PropertyValue", "name": "Innengeräte", "value": s["innengeraete"]},
              {"@type": "PropertyValue", "name": "Kältemittel", "value": s["kaeltemittel"]}],
          "brand": {"@type": "Brand", "name": "KlimaTech38"}, "seller": {"@id": f"{DOMAIN}/#business"}}
    if not K.META["demo"]:
        ld["offers"] = {"@type": "Offer", "priceCurrency": "EUR", "price": f'{s["preise"]["abholung_cent"] / 100:.2f}',
                        "availability": "https://schema.org/InStock", "seller": {"@id": f"{DOMAIN}/#business"}}
    brot = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Start", "item": f"{DOMAIN}/"},
        {"@type": "ListItem", "position": 2, "name": "Sets & Preise", "item": f"{DOMAIN}/shop.html"},
        {"@type": "ListItem", "position": 3, "name": kat["kurz"], "item": f"{DOMAIN}/{kat['datei']}"},
        {"@type": "ListItem", "position": 4, "name": s["titel"], "item": f"{DOMAIN}/{datei}"}]}
    t = S.kopf(f'{s["titel"]} – Preis & Daten | KlimaTech38',
               f'{s["titel"]}: {s["kw"]} kW für {s["flaecheVon"]}–{s["flaecheBis"]} m². Lieferumfang, Kältemittel '
               f'{s["kaeltemittel"]}, Preis für Abholung oder mit Montage. KlimaTech38, Gifhorn.',
               datei, json.dumps([ld, brot], ensure_ascii=False, indent=2))
    demo = f'<span class="preis-demo">{e(K.META["demoWort"])}</span>' if K.META["demo"] else ""
    ab = K.eur(s["preise"]["abholung_cent"])
    mo = K.eur(s["preise"]["montage_cent"]) if s["preise"].get("montage_cent") else None
    pd_montage = (f'<div class="pd pd--montage"><small>Einbauen lassen</small><b>{e(mo)}</b>{demo}<span>inkl. Montage: {e(s["montageUmfang"])}</span></div>'
                  if mo else
                  f'<div class="pd pd--montage pd--leer"><small>Einbauen lassen</small><b>–</b><span>Ein mobiles Gerät braucht keine Montage: aufstellen, Schlauch nach draußen, einstecken.</span></div>')
    raeume = f'{s["innengeraete"]} Räume' if s["innengeraete"] > 1 else "1 Raum"
    meta = "".join(chip(x, "chip--rand") for x in [kw(s), f'{s["flaecheVon"]}–{s["flaecheBis"]} m²', raeume, s["kaeltemittel"] + f' (GWP {s["gwp"]})', s["bauform"]])
    lief = "".join(f'<li>{ICON_CHECK}<span>{e(x)}</span></li>' for x in s["lieferumfang"])
    nicht = "".join(f'<li class="nein">{ICON_MINUS}<span>{e(x)}</span></li>' for x in s["nichtEnthalten"])
    hinweis = f'<p class="hinweis-karte" style="margin-top:var(--s3)">{ICON_INFO}<span>{e(s["hinweis"])}</span></p>' if s["hinweis"] else ""
    zub = "".join(zubehoer_karte(K.zubehoer_by_id(z), mit_passt=False) for z in s["zubehoer"])
    nachbarn = [x for x in K.SETS if x["id"] != s["id"] and x["kategorie"] == s["kategorie"]]
    if len(nachbarn) < 2:
        nachbarn += [x for x in K.SETS if x["id"] != s["id"] and x not in nachbarn and x["kategorie"] != "mobil"][:3 - len(nachbarn)]
    nachbar_karten = "".join(produkt_karte(x, best=x["empfehlung"]) for x in nachbarn[:3])
    passt = "".join(chip(r[1], "chip--rand") for r in RAEUME if _passt(s, r))
    montage_text = (f"Bei „Einbauen lassen“ ist enthalten: {e(s['montageUmfang'])}. Zusätzliche Leitungsmeter, weitere Kernbohrungen, Kondensatpumpe oder Leitungskanäle in Sichtbereichen stehen einzeln im Angebot."
                    if mo else "Dieses Gerät wird nicht montiert. Wir beraten Sie zur Aufstellung und zur Fensterabdichtung – der größte Hebel für die tatsächliche Kühlleistung.")
    t += f"""
<section class="produkt-kopf" aria-labelledby="set-h">
  <div class="wrap">
    <div class="produkt-kopf__innen">
      <div data-reveal="mask">{stage(s, best=s["empfehlung"])}</div>
      <div>
        <p class="brot"><a href="index.html">Start</a><span aria-hidden="true">/</span><a href="shop.html">Sets &amp; Preise</a><span aria-hidden="true">/</span><a href="{kat["datei"]}">{e(kat["kurz"])}</a></p>
        <h1 id="set-h">{e(s["titel"])}</h1>
        <p class="produkt-kopf__kurz">{e(s["kurz"])}</p>
        <div class="produkt-kopf__meta">{meta}</div>
        {C.weg_schalter()}
        <div class="preis-doppel">
          <div class="pd pd--selbst"><small>Selbst einbauen</small><b>{e(ab)}</b>{demo}<span>Abholung am Zeisigweg 4, Gifhorn · {e(s["anschlussart"])}</span></div>
          {pd_montage}
        </div>
        <p class="btns"><a class="btn btn--primary btn--gross" href="kontakt.html" data-set-anfragen="{s["id"]}">Set anfragen{ICON_ARROW}</a><a class="btn btn--rand" href="tel:{C.TEL}">{C.TEL_TEXT}</a></p>
        <div>{demo_zeile()}</div>
      </div>
    </div>
  </div>
</section>
<div class="unterleiste" data-unterleiste aria-hidden="true">
  <div class="unterleiste__innen"><span class="unterleiste__t">{e(s["titel"])}</span>{preis(s)}<a class="btn btn--klein btn--primary" href="kontakt.html" data-set-anfragen="{s["id"]}">Set anfragen</a></div>
</div>
<section class="sec sec--cool" aria-label="Details zum Set">
  <div class="wrap">
    <div class="kopf2" data-reveal><h2>Passt für diese Räume.</h2>{chip(f'{s["flaecheVon"]}–{s["flaecheBis"]} m²')}</div>
    <div class="chips" data-reveal>{passt}</div>
    {hinweis}
    <div class="karte" style="margin-top:var(--s4)" data-reveal>
      <div class="karte__body set-liste">
        <div><h3>Im Set enthalten</h3><ul>{lief}</ul></div>
        <div><h3>Nicht enthalten</h3><ul>{nicht}</ul></div>
      </div>
    </div>
    <div class="montage-karte" style="margin-top:var(--s3)" data-reveal>
      <span class="montage-karte__i">{ICON_TOOL}</span>
      <div><h3 style="margin-bottom:.4rem">Montage</h3><p>{montage_text}</p></div>
    </div>
  </div>
</section>
<section class="sec" aria-label="Passendes Zubehör">
  <div class="wrap">
    <div class="kopf2" data-reveal><h2>Passendes Zubehör.</h2>{chip("Im Montagepreis")}</div>
    <div class="karten karten--2">{zub}</div>
  </div>
</section>
<section class="sec sec--cool" aria-label="Weitere Sets">
  <div class="wrap">
    <div class="kopf2" data-reveal><h2>Weitere Sets.</h2><a class="btn btn--rand btn--klein" href="{kat["datei"]}">Alle {e(kat["kurz"])}{ICON_ARROW}</a></div>
    <div class="produkte">{nachbar_karten}</div>
    <div style="margin-top:var(--s3)">{kein_kauf()}</div>
  </div>
</section>
{abschluss("Ob das Set passt, prüfen wir vor Ort.", "Fragen Sie es an – wir prüfen Leitungsweg, Standort und Kühllast und melden uns mit einem schriftlichen Angebot.", ("Set anfragen", "kontakt.html"), ("Beratung vor Ort", "beratung.html"))}
"""
    t += S.fuss("voll")
    return datei, t


def _passt(s, r):
    m2 = re.match(r"(\d+)–(\d+)", r[3])
    lo, hi = int(m2.group(1)), int(m2.group(2))
    if r[0] == "dachgeschoss":
        return s["kategorie"] != "mobil" and s["flaecheVon"] <= hi * 1.6 and s["flaecheBis"] >= lo * 1.6
    if s["innengeraete"] > 1:
        return r[0] in ("wohnzimmer",)
    return s["flaecheVon"] <= hi and s["flaecheBis"] >= lo


# --------------------------------------------------------------------- Sitemap

def sitemap():
    seiten = list(C.SEITEN.keys()) + [f"set-{s['id']}.html" for s in K.SETS]
    prio = {"index.html": "1.0", "shop.html": "0.9", "beratung.html": "0.9", "klimaanlagen.html": "0.9",
            "energetische-beratung.html": "0.9", "kontakt.html": "0.8"}
    eintraege = []
    for p in sorted(set(seiten)):
        loc = f"{DOMAIN}/" if p == "index.html" else f"{DOMAIN}/{p}"
        pr = prio.get(p, "0.6" if p.startswith(("impressum", "datenschutz")) else "0.7")
        eintraege.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{K.META['stand']}</lastmod>\n    <priority>{pr}</priority>\n  </url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(eintraege) + "\n</urlset>\n")


# --------------------------------------------------------------------- Lauf

def main():
    probleme = K.pruefe()
    if probleme:
        print("Katalog-Selbsttest schlaegt fehl:")
        for p in probleme:
            print("  -", p)
        return 1
    import kt38_prosa as P

    nur_pruefen = "--check" in sys.argv
    geschrieben = []

    def ohne_chrome(s):
        s = re.sub(r"(<!-- KT38:HEADER:START).*?(KT38:HEADER:END -->)", r"\1\2", s, flags=re.S)
        s = re.sub(r"(<!-- KT38:FOOTER:START).*?(KT38:FOOTER:END -->)", r"\1\2", s, flags=re.S)
        return re.sub(r'id="g\d+-|url\(#g\d+-|#g\d+-', "#g-", s)

    def schreibe(name, inhalt):
        ziel = SITE / name
        if nur_pruefen:
            if not ziel.exists() or ohne_chrome(ziel.read_text(encoding="utf-8")) != ohne_chrome(inhalt):
                print(f"  ! {name} weicht ab")
                return False
            return True
        ziel.write_text(inhalt, encoding="utf-8")
        geschrieben.append(name)
        return True

    ok = True
    if not nur_pruefen:
        geschrieben.append(schreibe_produkte_js())
    ok &= schreibe(*startseite())
    ok &= schreibe(*shopseite())
    for kat in K.KATEGORIEN:
        ok &= schreibe(*kategorieseite(kat))
    for s in K.SETS:
        ok &= schreibe(*setseite(s))
    for name, inhalt in P.alle(globals()):
        ok &= schreibe(name, inhalt)
    ok &= schreibe("sitemap.xml", sitemap())

    if nur_pruefen:
        print("Bestand aktuell." if ok else "Bestand veraltet — Generator laufen lassen.")
        return 0 if ok else 1
    print(f"{len(geschrieben)} Dateien geschrieben.")
    print("Jetzt Kopf/Fuss einsetzen:  python3 .tools/kt38_chrome.py --write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
