#!/usr/bin/env python3
"""kt38_chrome.py — Kopf-Kapsel, Overlay-Schaufenster und Footer aller KlimaTech38-Seiten.

Redesign 2026-09-12 (Struktur-Blueprint, Achse 1 + 5):
  * Kopf = schwebende Kapsel mit GENAU Wortmarke · „Menü" · Telefon · CTA. Keine Linkleiste.
  * Overlay = ganzseitiges Schaufenster: 4 Bild-Kacheln je Strang + Set-Liste (Preis folgt dem
    Wege-Schalter) + Kontaktzeile. Auf allen Breiten dieselbe Fläche.
  * Footer = 4 Spalten, dunkel, ohne <details>, Set-Index Pflicht.

Jede Seite traegt Sentinels, dieses Modul schreibt den Bereich dazwischen neu:
    <!-- KT38:HEADER:START -->  ...  <!-- KT38:HEADER:END -->
    <!-- KT38:FOOTER:START -->  ...  <!-- KT38:FOOTER:END -->

Aufruf:
    python3 .tools/kt38_chrome.py --write     Kopf/Fuss in alle Seiten schreiben
    python3 .tools/kt38_chrome.py --check     Exit 1, wenn eine Seite abweicht (QA-Gate)
"""
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kt38_katalog as K

SITE = Path(__file__).resolve().parent.parent / "klimatech38"

TEL = "+4953718759972"
TEL_TEXT = "05371 8759972"
WA = "https://wa.me/4953718759972"
MAIL = "info@introtech.de"

# key = Strang (nur noch fuer aria-current im Overlay)
SEITEN = {
    "index.html": "start",
    "klimaanlagen.html": "klima",
    "beratung.html": "klima",
    "montage.html": "klima",
    "wartung.html": "klima",
    "energetische-beratung.html": "energie",
    "shop.html": "shop",
    "shop-split.html": "shop",
    "shop-multisplit.html": "shop",
    "shop-mobil.html": "shop",
    "shop-zubehoer.html": "shop",
    "ratgeber.html": "ratgeber",
    "ratgeber-groesse.html": "ratgeber",
    "ratgeber-kosten.html": "ratgeber",
    "ratgeber-selbsteinbau.html": "ratgeber",
    "ratgeber-pv.html": "ratgeber",
    "faq.html": "ratgeber",
    "kontakt.html": "kontakt",
    "impressum.html": "",
    "datenschutz.html": "",
}


def alle_seiten():
    seiten = dict(SEITEN)
    for p in sorted(SITE.glob("set-*.html")):
        seiten.setdefault(p.name, "shop")
    return seiten


def e(s):
    return html.escape(str(s), quote=True)


# --------------------------------------------------------------------------- Icons (Linien, 2px)
# Das echte InTroTech-Zeichen (Haus + Tropfen) — kein erfundenes App-Icon.
MARK_SVG = '<img class="marke__zeichen" src="assets/brand/mark.png" alt="InTroTech-Zeichen" width="34" height="34">'
ICON_TEL = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>')
ICON_MENU = ('<svg class="icon-menu" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h10"/></svg>'
             '<svg class="icon-x" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>')
ICON_WA = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 11.5a8 8 0 0 1-11.7 7.1L4 20l1.4-4.1A8 8 0 1 1 20 11.5z"/><path d="M9.5 9.5c0 3 2 5 5 5l1-1.5-1.8-.9-.8.8c-1-.5-1.6-1.1-2.1-2.1l.8-.8-.9-1.8z"/></svg>')
ICON_MAIL = ('<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="3"/><path d="m4 7 8 6 8-6"/></svg>')
ICON_CLOCK = ('<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>')
ICON_PIN = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s7-6.2 7-11.5A7 7 0 0 0 5 9.5C5 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>')


def preis_html(s, klasse="preis"):
    """Beide Wege im Markup — der Schalter (html[data-weg]) zeigt einen. Mobile Geraete haben
       keinen Montagepreis: dann steht bei „Einbauen lassen" der Abholpreis mit Hinweis."""
    demo = f'<span class="preis-demo">{e(K.META["demoWort"])}</span>' if K.META["demo"] else ""
    ab = K.eur(s["preise"]["abholung_cent"])
    mo = K.eur(s["preise"]["montage_cent"]) if s["preise"].get("montage_cent") else None
    selbst = f'<span class="preis__w preis__w--selbst"><b>{e(ab)}</b>{demo}<small>Abholung in Gifhorn</small></span>'
    if mo:
        montage = f'<span class="preis__w preis__w--montage"><b>{e(mo)}</b>{demo}<small>inkl. Montage</small></span>'
    else:
        montage = f'<span class="preis__w preis__w--montage"><b>{e(ab)}</b>{demo}<small>nur zur Abholung – ohne Montage</small></span>'
    return f'<span class="{klasse}">{selbst}{montage}</span>'


def weg_schalter(klasse="", gross=False, id_suffix=""):
    """Der Wege-Schalter (Signature). Ein Zustand fuer die ganze Seite, gespiegelt in html[data-weg]."""
    k = "weg" + (" weg--gross" if gross else "") + (f" {klasse}" if klasse else "")
    return f"""<div class="{k}" role="radiogroup" aria-label="Welcher Weg?" data-weg-schalter>
  <span class="weg__thumb" aria-hidden="true"></span>
  <button type="button" class="weg__opt" role="radio" aria-checked="false" data-weg="selbst">
    <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20h16M6 20V9l6-5 6 5v11"/><path d="M10 20v-6h4v6"/></svg>Selbst einbauen</button>
  <button type="button" class="weg__opt" role="radio" aria-checked="true" data-weg="montage">
    <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14.5 6.5a3.5 3.5 0 0 0 3 5l-8 8a2 2 0 0 1-3-3l8-8"/><path d="m15 3 6 6"/></svg>Einbauen lassen</button>
</div>"""


# --------------------------------------------------------------------------- Kopf + Overlay

def header(active=""):
    def cur(key):
        return ' aria-current="true"' if active == key else ""

    # Overlay: Set-Liste je Kategorie
    gruppen = []
    for kat in K.KATEGORIEN:
        if kat["id"] == "zubehoer":
            continue
        zeilen = []
        for s in K.sets_der_kategorie(kat["id"]):
            zeilen.append(
                f'<a class="ovs" href="set-{s["id"]}.html">'
                f'<span class="chip">{e(str(s["kw"]).replace(".", ","))} kW</span>'
                f'<b>{e(s["titel"]).replace(" · ", "&nbsp;· ")}</b><small>{s["flaecheVon"]}–{s["flaecheBis"]} m²'
                f'{" · " + str(s["innengeraete"]) + " Räume" if s["innengeraete"] > 1 else ""}</small>'
                f'{preis_html(s)}</a>')
        gruppen.append(f'<p class="overlay__gruppe"><a href="{kat["datei"]}">{e(kat["kurz"])}</a></p>' + "".join(zeilen))

    return f"""<!-- KT38:HEADER:START -->
<header class="kopf" data-header>
  <div class="kopf__kapsel">
    <a class="marke" href="index.html" aria-label="KlimaTech38 – Startseite">{MARK_SVG}<span><b>KlimaTech</b><i>38</i></span></a>
    <button type="button" class="kopf__menu" data-overlay-toggle aria-expanded="false" aria-controls="overlay" aria-label="Menü öffnen">{ICON_MENU}<span>Menü</span></button>
    <a class="kopf__tel" href="tel:{TEL}" aria-label="Anrufen: {TEL_TEXT}">{ICON_TEL}<span>{TEL_TEXT}</span></a>
    <a class="btn btn--primary kopf__cta" href="kontakt.html">Beratung anfragen</a>
  </div>
</header>

<div class="overlay" id="overlay" data-overlay aria-hidden="true" role="dialog" aria-modal="true" aria-label="Menü">
  <div class="overlay__innen">
    <nav class="overlay__kacheln" aria-label="Bereiche">
      <a class="ovk" href="klimaanlagen.html"{cur("klima")}>
        <img src="assets/innengeraet.jpg" alt="Innengerät einer Split-Klimaanlage" width="1000" height="666" loading="lazy">
        <span class="ovk__t"><b>Klimaanlagen</b><span>Beratung · Montage · Wartung</span></span>
      </a>
      <a class="ovk" href="shop.html"{cur("shop")}>
        <img src="assets/hero.jpg" alt="Offener Wohnbereich mit Innengerät einer Klimaanlage" width="1500" height="993" loading="lazy">
        <span class="ovk__t"><b>Sets &amp; Preise</b><span>Split · Multi-Split · mobil · Zubehör</span></span>
      </a>
      <a class="ovk" href="energetische-beratung.html"{cur("energie")}>
        <img src="assets/sonne-vorhang.jpg" alt="Sonnenlicht durch einen Vorhang" width="1400" height="933" loading="lazy">
        <span class="ovk__t"><b>Energieberatung</b><span>Energieausweis · Wärmebrücken · Sanierungsplan</span></span>
      </a>
      <a class="ovk" href="ratgeber.html"{cur("ratgeber")}>
        <img src="assets/fernbedienung.jpg" alt="Hand mit Fernbedienung einer Klimaanlage" width="1200" height="800" loading="lazy">
        <span class="ovk__t"><b>Ratgeber &amp; FAQ</b><span>Größe · Kosten · Selbsteinbau · Photovoltaik</span></span>
      </a>
    </nav>
    <div class="overlay__sets">
      <div class="overlay__sets-kopf"><h2>Alle Sets</h2>{weg_schalter("weg--hell", id_suffix="ov")}</div>
      {"".join(gruppen)}
      <p class="overlay__gruppe"><a href="shop-zubehoer.html">Zubehör</a> · <a href="shop.html">Katalog-Übersicht</a></p>
    </div>
  </div>
  <div class="overlay__fuss">
    <div class="overlay__kontakt">
      <a href="tel:{TEL}">{TEL_TEXT}</a><small>Mo–Fr 08–18 Uhr</small>
      <a href="{WA}" target="_blank" rel="noopener">WhatsApp</a>
      <a href="kontakt.html"{cur("kontakt")}>Kontakt &amp; Rückruf</a>
      <a class="btn btn--primary btn--klein" href="kontakt.html">Beratung anfragen</a>
    </div>
    <div class="overlay__legal"><a href="impressum.html">Impressum</a><a href="datenschutz.html">Datenschutz</a></div>
  </div>
</div>
<!-- KT38:HEADER:END -->"""


# --------------------------------------------------------------------------- Footer

def footer(active=""):
    sets = "".join(f'<a href="set-{s["id"]}.html">{e(s["titel"].replace("Mobiles Monoblock-Gerät", "Mobil").replace("Multi-Split-Set ", "Multi "))}</a>'
                   for s in K.SETS)
    demo = ""
    if K.META["demo"]:
        demo = '<span>Vorschau mit Beispielpreisen – verbindlich ist das schriftliche Angebot.</span>'
    return f"""<!-- KT38:FOOTER:START -->
<footer class="fuss">
  <div class="wrap">
    <div class="fuss__grid">
      <div class="fuss__spalte fuss__logo">
        <a href="https://www.introtech.de/" rel="noopener" target="_blank"><img src="assets/brand/logo-white.png" alt="InTroTech GmbH" width="380" height="72" loading="lazy"></a>
        <p>KlimaTech38 ist der Geschäftsbereich der InTroTech GmbH für Klimaanlagen und energetische Beratung. Die 38 steht für die Region: Gifhorn, Wolfsburg, Braunschweig, Peine, Salzgitter, Helmstedt.</p>
        <p>dena-Energieberater · TÜV-zertifizierter Fachbetrieb</p>
      </div>
      <div class="fuss__spalte">
        <h3>Sets &amp; Preise</h3>
        <ul>
          <li><a href="shop.html">Katalog-Übersicht</a></li>
          <li><a href="shop-split.html">Split-Sets</a></li>
          <li><a href="shop-multisplit.html">Multi-Split-Sets</a></li>
          <li><a href="shop-mobil.html">Mobile Geräte</a></li>
          <li><a href="shop-zubehoer.html">Zubehör</a></li>
        </ul>
        <h3 style="margin-top:var(--s3)">Alle Sets</h3>
        <div class="fuss__sets">{sets}</div>
      </div>
      <div class="fuss__spalte">
        <h3>Beratung &amp; Wissen</h3>
        <ul>
          <li><a href="klimaanlagen.html">Klimaanlagen</a></li>
          <li><a href="beratung.html">Beratung &amp; Ablauf</a></li>
          <li><a href="montage.html">Montage</a></li>
          <li><a href="wartung.html">Wartung &amp; Service</a></li>
          <li><a href="energetische-beratung.html">Energetische Beratung</a></li>
          <li><a href="ratgeber.html">Ratgeber</a></li>
          <li><a href="faq.html">Häufige Fragen</a></li>
        </ul>
      </div>
      <div class="fuss__spalte">
        <h3>Kontakt</h3>
        <ul>
          <li>InTroTech GmbH<br>Zeisigweg 4 · 38518 Gifhorn</li>
          <li><a href="tel:{TEL}">{TEL_TEXT}</a><br>Mo–Fr 08–18 Uhr</li>
          <li><a href="mailto:{MAIL}">{MAIL}</a></li>
          <li><a href="{WA}" target="_blank" rel="noopener">WhatsApp schreiben</a></li>
          <li><a href="kontakt.html">Rückruf vereinbaren</a></li>
        </ul>
      </div>
    </div>
    <div class="fuss__legal">
      <span>© InTroTech GmbH · Amtsgericht Hildesheim HRB 210481</span>
      {demo}
      <span><a href="impressum.html">Impressum</a> · <a href="datenschutz.html">Datenschutz</a></span>
    </div>
  </div>
</footer>
<!-- KT38:FOOTER:END -->"""


# --------------------------------------------------------------------------- Sync

H_RE = re.compile(r"<!-- KT38:HEADER:START.*?KT38:HEADER:END -->", re.S)
F_RE = re.compile(r"<!-- KT38:FOOTER:START.*?KT38:FOOTER:END -->", re.S)


def sync_datei(pfad, active, schreiben):
    alt = pfad.read_text(encoding="utf-8")
    if not H_RE.search(alt) or not F_RE.search(alt):
        return "ohne Sentinels"
    neu = H_RE.sub(lambda m: header(active), alt)
    neu = F_RE.sub(lambda m: footer(active), neu)
    if neu == alt:
        return "aktuell"
    if schreiben:
        pfad.write_text(neu, encoding="utf-8")
        return "geschrieben"
    return "weicht ab"


def main():
    schreiben = "--write" in sys.argv
    pruefen = "--check" in sys.argv
    if not (schreiben or pruefen):
        print(__doc__)
        return 2
    abweichend = 0
    for name, active in alle_seiten().items():
        p = SITE / name
        if not p.exists():
            continue
        st = sync_datei(p, active, schreiben)
        if st in ("weicht ab", "ohne Sentinels"):
            abweichend += 1
        if schreiben or st != "aktuell":
            print(f"  {st:12} {name}")
    if pruefen:
        print("Kopf/Fuss aktuell." if not abweichend else f"{abweichend} Seite(n) weichen ab.")
        return 1 if abweichend else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
