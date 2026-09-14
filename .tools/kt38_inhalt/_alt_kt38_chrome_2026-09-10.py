#!/usr/bin/env python3
"""kt38_chrome.py — Kopf und Fuss aller KlimaTech38-Seiten, an EINER Stelle.

Bisher war die "Anlagen-Rail" in jede der 7 Seiten kopiert; eine Navigationsaenderung
bedeutete 7 Edits. Bei ~26 Seiten ist das nicht mehr haltbar. Jede Seite traegt deshalb
Sentinels, und dieses Modul schreibt den Bereich dazwischen neu:

    <!-- KT38:HEADER:START -->  ...  <!-- KT38:HEADER:END -->
    <!-- KT38:FOOTER:START -->  ...  <!-- KT38:FOOTER:END -->

Aufruf:
    python3 .tools/kt38_chrome.py --write     Kopf/Fuss in alle Seiten schreiben
    python3 .tools/kt38_chrome.py --check     Exit 1, wenn eine Seite abweicht (QA-Gate)

Der aktive Menuepunkt kommt aus SEITEN; {{ACTIVE}} wird pro Seite ersetzt.
"""
import re
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "klimatech38"

TEL = "+4953718759972"
TEL_TEXT = "05371 8759972"
WA = "https://wa.me/4953718759972"

# --------------------------------------------------------------------------- Seiten
# key = Wert für {{ACTIVE}} (welcher Hauptmenuepunkt markiert wird)
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
    """SEITEN plus die vom Generator erzeugten Set-Seiten (set-*.html), die alle
       unter dem Menuepunkt 'Sets & Preise' haengen."""
    seiten = dict(SEITEN)
    for p in sorted(SITE.glob("set-*.html")):
        seiten.setdefault(p.name, "shop")
    return seiten

MARK_SVG = (
    '<svg class="unit" viewBox="0 0 44 30" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.2">'
    '<rect x=".6" y=".6" width="42.8" height="28.8" rx="1.5"/>'
    '<circle cx="15" cy="15" r="8.6"/><circle cx="15" cy="15" r="1.6" fill="currentColor" stroke="none"/>'
    '<path d="M15 6.4A8.6 8.6 0 0 1 22.6 11M15 23.6A8.6 8.6 0 0 1 7.4 19"/>'
    '<path d="M29 7h10M29 11h10M29 15h10M29 19h10M29 23h10" stroke-width=".9"/></svg>'
)

TEL_SVG = (
    '<svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="1.6" '
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<path d="M5 4h3l2 5-2.5 1.5a11 11 0 0 0 5 5L14 13l5 2v3a2 2 0 0 1-2 2A14 14 0 0 1 3 6a2 2 0 0 1 2-2Z"/></svg>'
)


def _mega_klima():
    return """      <div class="mega" id="mega-klima" data-strang="klima" hidden>
        <div class="wrap mega-in">
          <div class="mega-sp">
            <p class="mono mega-k">Der Weg zur Anlage</p>
            <ul class="mega-l">
              <li><a href="klimaanlagen.html"><b>Klimaanlagen im Überblick</b><span>Bauarten, Ablauf, Kältemittel, Wartung</span></a></li>
              <li><a href="beratung.html"><b>Beratung &amp; Ablauf</b><span>Kostenlose Besichtigung, Angebot, Termin</span></a></li>
              <li><a href="montage.html"><b>Montage</b><span>Kernbohrung, Leitungsweg, Inbetriebnahme</span></a></li>
              <li><a href="wartung.html"><b>Wartung &amp; Service</b><span>Intervalle, Umfang, Störungsdienst</span></a></li>
            </ul>
          </div>
          <div class="mega-sp">
            <p class="mono mega-k">Häufig gefragt</p>
            <ul class="mega-l">
              <li><a href="ratgeber-groesse.html"><b>Welche Leistung brauche ich?</b><span>Kühllast statt Bauchgefühl</span></a></li>
              <li><a href="ratgeber-kosten.html"><b>Was kostet eine Klimaanlage?</b><span>Set, Montage und Betrieb getrennt</span></a></li>
              <li><a href="ratgeber-selbsteinbau.html"><b>Was darf ich selbst einbauen?</b><span>EU-VO 517/2014 und Quick-Connect</span></a></li>
              <li><a href="ratgeber-pv.html"><b>Klimaanlage mit Photovoltaik</b><span>Kühlen, wenn der Strom ohnehin da ist</span></a></li>
            </ul>
          </div>
          <div class="mega-sp mega-akt">
            <p class="mono mega-k">Direkt</p>
            <p class="mega-satz">Besichtigung und Angebot sind kostenfrei. Wir sehen uns die Räume an,
              bevor wir eine Leistung nennen.</p>
            <a class="btn btn-primary btn-sm" href="beratung.html">Beratung anfragen</a>
            <a class="mega-tel mono" href="tel:{tel}">{telsvg}{teltext}</a>
          </div>
        </div>
      </div>""".format(tel=TEL, telsvg=TEL_SVG, teltext=TEL_TEXT)


def _mega_shop():
    return """      <div class="mega" id="mega-shop" data-strang="klima" hidden>
        <div class="wrap mega-in">
          <div class="mega-sp">
            <p class="mono mega-k">Nach Bauart</p>
            <ul class="mega-l">
              <li><a href="shop.html"><b>Alle Sets ansehen</b><span>Übersicht, Rechner und Vergleich</span></a></li>
              <li><a href="shop-split.html"><b>Split-Sets</b><span>Ein Raum · 2,5 bis 7,0 kW</span></a></li>
              <li><a href="shop-multisplit.html"><b>Multi-Split-Sets</b><span>2 bis 4 Räume · ein Außengerät</span></a></li>
              <li><a href="shop-mobil.html"><b>Mobile Geräte</b><span>Ohne Bohren, für Mietwohnungen</span></a></li>
              <li><a href="shop-zubehoer.html"><b>Zubehör</b><span>Halter, Kondensat, Durchführung</span></a></li>
            </ul>
          </div>
          <div class="mega-sp">
            <p class="mono mega-k">Nach Raumgröße</p>
            <ul class="mega-l">
              <li><a href="shop-split.html#flaeche=20"><b>bis 25 m²</b><span>Schlaf-&nbsp;und Arbeitszimmer</span></a></li>
              <li><a href="shop-split.html#flaeche=32"><b>25 bis 40 m²</b><span>Wohnzimmer im Bestand</span></a></li>
              <li><a href="shop-split.html#flaeche=50"><b>40 bis 60 m²</b><span>Offener Wohnraum, Dachgeschoss</span></a></li>
              <li><a href="shop-multisplit.html"><b>Mehrere Räume</b><span>Multi-Split statt Einzelgeräte</span></a></li>
            </ul>
          </div>
          <div class="mega-sp mega-akt">
            <p class="mono mega-k">Erst rechnen</p>
            <p class="mega-satz">Der Auslegungs-Rechner fragt Ihre Räume ab und filtert den Katalog
              auf die Sets, die wirklich passen.</p>
            <a class="btn btn-primary btn-sm" href="shop.html#rechner">Kühllast berechnen</a>
            <p class="mono mega-fuss">Kein Kaufabschluss online – Sie erhalten ein Angebot.</p>
          </div>
        </div>
      </div>"""


def _mega_energie():
    return """      <div class="mega" id="mega-energie" data-strang="energie" hidden>
        <div class="wrap mega-in">
          <div class="mega-sp">
            <p class="mono mega-k">Gebäude bewerten</p>
            <ul class="mega-l">
              <li><a href="energetische-beratung.html"><b>Energetische Beratung</b><span>Überblick, Ablauf, was wir aufnehmen</span></a></li>
              <li><a href="energetische-beratung.html#ausweis"><b>Energieausweis</b><span>Wohn-&nbsp;und Nichtwohngebäude, dena-Energieberater</span></a></li>
              <li><a href="energetische-beratung.html#thermografie"><b>Wärmebrücken &amp; Thermografie</b><span>Messen statt vermuten</span></a></li>
              <li><a href="energetische-beratung.html#massnahmen"><b>Maßnahmenplan</b><span>Priorisiert nach Wirkung und Aufwand</span></a></li>
            </ul>
          </div>
          <div class="mega-sp">
            <p class="mono mega-k">Treffpunkt</p>
            <ul class="mega-l">
              <li><a href="ratgeber-pv.html"><b>Klimaanlage mit Photovoltaik</b><span>Gekühlt wird, wenn die Sonne scheint</span></a></li>
              <li><a href="ratgeber-kosten.html"><b>Was kostet der Betrieb?</b><span>Strom, Wartung und die Rolle der Gebäudehülle</span></a></li>
            </ul>
          </div>
          <div class="mega-sp mega-akt">
            <p class="mono mega-k">Zuerst die Hülle</p>
            <p class="mega-satz">Jede Kilowattstunde, die nicht durch ein ungedämmtes Dach
              hereinkommt, muss auch nicht weggekühlt werden. Deshalb sehen wir uns die
              Gebäudehülle an, bevor wir Kühlleistung planen.</p>
            <a class="btn btn-primary btn-energie btn-sm" href="energetische-beratung.html">Energetische Beratung</a>
          </div>
        </div>
      </div>"""


def header(active=""):
    def cur(key):
        return ' aria-current="page"' if key and key == active else ""

    def on(key):
        return " is-on" if key and key == active else ""

    return f"""<!-- KT38:HEADER:START (erzeugt von .tools/kt38_chrome.py) -->
<header class="kopf" data-header>
  <div class="kopf-service band">
    <div class="wrap kopf-service-in">
      <p class="mono">KlimaTech38 · ein Geschäftsbereich der InTroTech GmbH, Gifhorn</p>
      <ul class="mono kopf-service-r">
        <li>Mo–Fr 08–18 Uhr</li>
        <li><span class="kopf-lang">Besichtigung &amp; </span>Angebot kostenfrei</li>
        <li>Gifhorn · Wolfsburg · Braunschweig</li>
      </ul>
    </div>
  </div>

  <div class="wrap kopf-in">
    <a class="kopf-mark{on('start')}" href="index.html" aria-label="KlimaTech38 – Startseite"{cur('start')}>
      {MARK_SVG}<span class="kopf-name">KlimaTech<b>38</b></span>
    </a>

    <nav class="kopf-nav" aria-label="Hauptnavigation">
      <ul class="hn">
        <li class="hn-i">
          <button class="hn-a{on('klima')}" type="button" aria-expanded="false" aria-controls="mega-klima">
            Klimaanlagen<i aria-hidden="true"></i></button>
{_mega_klima()}
        </li>
        <li class="hn-i">
          <button class="hn-a{on('shop')}" type="button" aria-expanded="false" aria-controls="mega-shop">
            Sets &amp; Preise<i aria-hidden="true"></i></button>
{_mega_shop()}
        </li>
        <li class="hn-i">
          <button class="hn-a s-energie{on('energie')}" type="button" aria-expanded="false" aria-controls="mega-energie">
            Energieberatung<i aria-hidden="true"></i></button>
{_mega_energie()}
        </li>
        <li class="hn-i"><a class="hn-a{on('ratgeber')}" href="ratgeber.html"{cur('ratgeber')}>Ratgeber<i aria-hidden="true"></i></a></li>
        <li class="hn-i"><a class="hn-a{on('kontakt')}" href="kontakt.html"{cur('kontakt')}>Kontakt<i aria-hidden="true"></i></a></li>
      </ul>
    </nav>

    <div class="kopf-akt">
      <a class="kopf-tel" href="tel:{TEL}" aria-label="{TEL_TEXT} anrufen">{TEL_SVG}<span>{TEL_TEXT}</span></a>
      <a class="kopf-cta" href="beratung.html">Beratung anfragen</a>
      <button class="kopf-burger" type="button" aria-expanded="false" aria-controls="kopf-panel" aria-label="Menü öffnen">
        <span class="kopf-burger-l" aria-hidden="true"></span><span>Menü</span>
      </button>
    </div>
  </div>
  <div class="kopf-linie" aria-hidden="true"><span class="kopf-fort" id="kopf-fort"></span></div>
</header>

<div class="kopf-panel" id="kopf-panel" role="dialog" aria-modal="true" aria-label="Menü und Kontakt" hidden>
  <div class="kopf-panel-in">
    <div class="kopf-panel-kopf">
      <span class="mono">Menü</span>
      <button class="kopf-panel-zu" type="button">Schließen</button>
    </div>
    <nav aria-label="Menü">
      <ul class="pn">
        <li><a href="index.html"{cur('start')}>Start</a></li>
        <li class="pn-g"><span class="mono">Klimaanlagen</span>
          <ul>
            <li><a href="klimaanlagen.html">Überblick</a></li>
            <li><a href="beratung.html">Beratung &amp; Ablauf</a></li>
            <li class="fi-k"><a href="montage.html">Montage</a></li>
            <li><a href="wartung.html">Wartung &amp; Service</a></li>
          </ul>
        </li>
        <li class="pn-g"><span class="mono">Sets &amp; Preise</span>
          <ul>
            <li><a href="shop.html">Übersicht &amp; Rechner</a></li>
            <li><a href="shop-split.html">Split-Sets</a></li>
            <li><a href="shop-multisplit.html">Multi-Split-Sets</a></li>
            <li><a href="shop-mobil.html">Mobile Geräte</a></li>
            <li class="fi-k"><a href="shop-zubehoer.html">Zubehör</a></li>
          </ul>
        </li>
        <li class="pn-g"><span class="mono">Energie</span>
          <ul>
            <li><a href="energetische-beratung.html">Energetische Beratung</a></li>
            <li><a href="ratgeber-pv.html">Klimaanlage mit Photovoltaik</a></li>
          </ul>
        </li>
        <li class="pn-g"><span class="mono">Wissen</span>
          <ul>
            <li><a href="ratgeber.html">Ratgeber</a></li>
            <li><a href="faq.html">Häufige Fragen</a></li>
          </ul>
        </li>
        <li><a href="kontakt.html"{cur('kontakt')}>Kontakt</a></li>
      </ul>
    </nav>
    <div class="kopf-panel-akt">
      <a class="btn btn-primary" href="tel:{TEL}">{TEL_TEXT} anrufen</a>
      <a class="btn btn-ghost" href="{WA}" target="_blank" rel="noopener">WhatsApp schreiben</a>
      <p class="mono">Mo–Fr 08–18 Uhr · Zeisigweg 4 · 38518 Gifhorn</p>
    </div>
  </div>
</div>
<!-- KT38:HEADER:END -->"""


def footer(active=""):
    """Footer als KONTAKTBAND (Struktur-Achse 5, geaendert 2026-09-10).

    Der Mega-Footer deckte sich mit MAVA Marketing und riss die Struktur-Divergenz
    unter die Schwelle. Der Fuss ist jetzt eine Kontaktzone: grosse Telefon-CTA,
    Anschrift, Zeiten, Einzugsgebiet. Die Zweitnavigation fuer 29 Seiten steht
    darunter als EINE dichte Haarlinienzeile im Idiom der Seite, nicht als Raster.
    """
    return f"""<!-- KT38:FOOTER:START (erzeugt von .tools/kt38_chrome.py) -->
<footer class="fuss">
  <div class="fuss-band">
    <div class="wrap fuss-band-in">
      <div class="fuss-ruf">
        <p class="mono fuss-ruf-k">Rufen Sie an – das geht am schnellsten</p>
        <a class="fuss-tel" href="tel:{TEL}">{TEL_SVG}{TEL_TEXT}</a>
        <p class="fuss-zeit">Mo–Fr 08–18 Uhr · Besichtigung und Angebot kostenfrei</p>
        <p class="fuss-kanal">
          <a href="{WA}" target="_blank" rel="noopener">WhatsApp schreiben</a>
          <a href="mailto:info@introtech.de">info@introtech.de</a>
          <a href="kontakt.html">Rückruf vereinbaren</a>
        </p>
      </div>
      <div class="fuss-ort">
        <p class="mono fuss-ruf-k">Wo wir sind</p>
        <p class="fuss-adr">InTroTech GmbH<br>Zeisigweg 4<br>38518 Gifhorn</p>
        <a class="fuss-parent" href="https://www.introtech.de/" target="_blank" rel="noopener">
          <span class="mono">Ein Geschäftsbereich der</span>
          <img src="assets/brand/logo-white.png" width="1319" height="254" alt="InTroTech GmbH">
        </a>
      </div>
    </div>
  </div>

  <div class="fuss-gebiet band">
    <div class="wrap">
      <p class="mono"><span>Wir arbeiten in</span>
        Gifhorn · Wolfsburg · Braunschweig · Peine · Salzgitter · Helmstedt</p>
    </div>
  </div>

  <nav class="fuss-index band" aria-label="Alle Seiten">
    <div class="wrap">
      <ul class="mono">
        <li><a href="index.html">Start</a></li>
        <li class="fi-k"><a href="klimaanlagen.html">Klimaanlagen</a></li>
        <li class="fi-k"><a href="beratung.html">Beratung</a></li>
        <li><a href="montage.html">Montage</a></li>
        <li class="fi-k"><a href="wartung.html">Wartung</a></li>
        <li class="fi-k"><a href="shop.html">Sets &amp; Preise</a></li>
        <li class="fi-k"><a href="shop-split.html">Split</a></li>
        <li class="fi-k"><a href="shop-multisplit.html">Multi-Split</a></li>
        <li class="fi-k"><a href="shop-mobil.html">Mobil</a></li>
        <li><a href="shop-zubehoer.html">Zubehör</a></li>
        <li class="fi-e"><a href="energetische-beratung.html">Energetische Beratung</a></li>
        <li class="fi-e"><a href="ratgeber-pv.html">Klimaanlage &amp; Photovoltaik</a></li>
        <li><a href="ratgeber.html">Ratgeber</a></li>
        <li><a href="faq.html">Häufige Fragen</a></li>
        <li><a href="kontakt.html">Kontakt</a></li>
      </ul>
    </div>
  </nav>

  <div class="fuss-legal band">
    <div class="wrap fuss-legal-in">
      <p class="mono">dena-Energieberater · TÜV-zertifizierter Fachbetrieb (TÜV Rheinland)</p>
      <ul class="mono">
        <li><a href="impressum.html">Impressum</a></li>
        <li><a href="datenschutz.html">Datenschutz</a></li>
        <li><a href="https://www.introtech.de/" target="_blank" rel="noopener">introtech.de</a></li>
      </ul>
    </div>
  </div>
</footer>
<!-- KT38:FOOTER:END -->"""


# --------------------------------------------------------------------------- Sync

H_RE = re.compile(r"<!-- KT38:HEADER:START.*?KT38:HEADER:END -->", re.S)
F_RE = re.compile(r"<!-- KT38:FOOTER:START.*?KT38:FOOTER:END -->", re.S)


def sync_datei(pfad, active, schreiben):
    txt = pfad.read_text(encoding="utf-8")
    neu = txt
    fehlend = []

    if H_RE.search(neu):
        neu = H_RE.sub(lambda m: header(active), neu, count=1)
    else:
        fehlend.append("HEADER-Sentinel")

    if F_RE.search(neu):
        neu = F_RE.sub(lambda m: footer(active), neu, count=1)
    else:
        fehlend.append("FOOTER-Sentinel")

    if fehlend:
        return "fehlend", fehlend
    if neu == txt:
        return "gleich", []
    if schreiben:
        pfad.write_text(neu, encoding="utf-8")
        return "geschrieben", []
    return "abweichend", []


def main():
    schreiben = "--write" in sys.argv
    pruefen = "--check" in sys.argv
    if not schreiben and not pruefen:
        print(__doc__)
        return 2

    problem = 0
    for datei, active in sorted(alle_seiten().items()):
        p = SITE / datei
        if not p.exists():
            print(f"  – {datei}: (noch nicht vorhanden)")
            continue
        stand, fehlend = sync_datei(p, active, schreiben)
        if stand == "fehlend":
            print(f"  ! {datei}: {', '.join(fehlend)}")
            problem = 1
        elif stand == "abweichend":
            print(f"  ! {datei}: weicht vom Modul ab")
            problem = 1
        elif stand == "geschrieben":
            print(f"  ✎ {datei}")
    if pruefen and not problem:
        print("Kopf und Fuss auf allen Seiten identisch.")
    return problem


if __name__ == "__main__":
    sys.exit(main())
