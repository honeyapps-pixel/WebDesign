# KlimaTech38 — Website (Redesign 2026-09-12)

Statische Website (HTML/CSS/JS, **kein Build im Deploy**) für **KlimaTech38**, den Geschäftsbereich der
**InTroTech GmbH** (Gifhorn) für **energetische Beratung** sowie **Planung, Auslegung, Verkauf und
Montage von Klimaanlagen**. Zieldomain **klimatech38.de**. Vorschau: https://klimatech38.vercel.app

Die Sparte ist neu — die Marke ist es nicht: Logo, Farben, Ton, Kontakt- und Registerdaten kommen 1:1
vom bestehenden Auftritt der Mutterfirma (`introtech-sanierung/`, Original introtech.de).

---

## Was am 12.09.2026 passiert ist

Der Erstbau (Swiss/Grid-Präzise: Haarlinien, Mono-Labels, Strichzeichnungen statt Fotos, Mega-Menü)
wurde vom Auftraggeber **komplett abgelehnt** — zu karg, zu technisch, „wie ein Datenblatt". Die
beiden vom Kunden benannten Vorbilder (solago.de, klima-mueller.com) sind das Gegenteil: bildgeführt,
Produkt und Preise sichtbar. Deshalb ein **vollständiges Redesign**: neuer Kreativ-Brief
(`assets/art-direction.md`), neues Skelett (`assets/struktur-blueprint.md`), neue `styles.css`,
neues `script.js`, alle 29 Seiten neu generiert. **Unverändert:** Inhalte, Katalogdaten, Preise,
Rechner-Logik, Rechtstexte, URL-Struktur, Formularfelder. Der Erstbau liegt archiviert in
`.tools/kt38_inhalt/_alt_erstbau/`.

## Konzept: zwei Wege, ein Schalter

Jedes Set hat zwei Preise — `Abholung` (selbst einbauen) und `inkl. Montage` (einbauen lassen). Statt
einer eigenen „Zwei Wege"-Sektion trägt die Seite einen **Wege-Schalter** („Selbst einbauen |
Einbauen lassen"), der als *eine* Einstellung überall gilt: Hero, Katalog-Kopf, Kategorien,
Set-Seiten, Overlay-Menü, Kontaktformular (Thema-Vorwahl) und die Ablauf-Strecke auf der Startseite
(5 Schritte je Weg). Zustand in `html[data-weg]`, gemerkt in `sessionStorage` (`kt38-weg`),
Standard „Einbauen lassen" (Conversion-Primärziel Beratung/Montage).

**Es gibt bewusst keinen Warenkorb und keinen Checkout.** Jede Aktion heißt „anfragen", nie „kaufen".
Das ist keine Schwäche, sondern Vorgabe — und hält das Nischen-Tabu ein, keinen Online-Shop
anzudeuten, den es nicht gibt.

## ⚠️ Die Preise sind Beispielwerte

`META["demo"] = True` in `.tools/kt38_katalog.py`. Solange der Schalter steht:

- an jedem Preis erscheint das Label **„Beispielpreis"**, jede preisführende Seite trägt den
  Vorschau-Hinweis, der Footer ebenfalls,
- das `Product`-JSON-LD wird **ohne `offers`** gerendert,
- alle Seiten stehen auf `noindex, nofollow` (+ `robots.txt` Disallow + `X-Robots-Tag` in `vercel.json`).

**Umschalten, sobald echte Preise vorliegen:** `META["demo"] = False`, Preise eintragen, dann
`python3 .tools/gen_kt38_shop.py && python3 .tools/kt38_chrome.py --write`. Mehr ist nicht nötig.

Was rechtlich bewusst *nicht* übernommen wurde: keine Streichpreise/„Ersparnis" (§ 11 PAngV), kein
SEER/SCOP/Effizienzklasse/dB(A) ohne Modell (EnVKV), keine Countdowns, Lagerbestände, Bewertungen.
Preise inkl. 19 % MwSt. (§ 3 PAngV), Abholung/Lieferung genannt (§ 6 PAngV); ohne Bestellbutton ist
die Seite eine *invitatio ad offerendum*.

**„Empfehlung"** (2 Sets: Split 3,5 kW, Multi Duo) ist unsere Einstiegsempfehlung — **kein
Verkaufsranking**. Die Sparte ist neu, es gibt keine Absatzzahlen, deshalb steht nirgends „Bestseller".

---

## Aufbau — 29 Seiten, 10 Kopf-Typen

```
index.html              Vollbild-Hero (Foto · Wege-Schalter · Preisanker) → Einbausituationen (Bento, 5 Räume
                        + Rechner-Kachel) → Rechner (Bühne) → Zum Einstieg (2 Empfehlungen + „Ihr Treffer")
                        → Alle Sets nach Bauart (4 Kacheln) → Kapitel Montage (je Weg + Strecke 1–5)
                        → Kapitel Energie (+ 3 Karten) → PV (Split) → Wissen (4 Ratgeber + FAQ)
                        → Mit wem (Logo-Band) → Kontakt (Vollbild-Karte) → Footer (4 Spalten)
shop.html               Katalog-Kopf (Schalter + 4 Kacheln) → Rechner → alle 9 Sets je Kategorie → Zubehör
shop-*.html        (4)  Bühnen-Kopf (h1 + Produkt-SVG + Schalter) → Filter → Set-Karten → Nachbarkategorien
set-*.html         (9)  Produkt-Kopf 50/50 (Bühne | h1 · Chips · Schalter · Preis-Doppel) + sticky Unterleiste
                        → Passt für → Lieferumfang | Nicht enthalten → Montage-Karte → Zubehör → Weitere Sets
klimaanlagen/beratung/montage/wartung/energetische-beratung.html
                        Kapitel-Kopf (Vollbild-Foto, helle Waschung, h1 links, Slot-Karte rechts —
                        je Seite ein anderer Slot: Bauform-Kacheln · Schalter + Kanäle · Strecken-Vorschau
                        · Intervall-Chips · Nachweis-Chips) → Karten/Strecken/Kapitel
ratgeber.html           Index-Kopf (h1 + 4 Artikel-Karten)          ratgeber-*.html (4)  Artikel-Kopf + Lesespalte
faq.html                Fragen-Kopf (Themen-Chips filtern 14 Fragen) kontakt.html         Karte-zuerst + Formular
impressum.html · datenschutz.html   Lesespalte
```

## Werkzeuge — nichts wird von Hand gepflegt

| Skript | Zweck |
|---|---|
| `.tools/kt38_katalog.py` | **Einzige Wahrheitsquelle** für Sets, Zubehör, Preise, Demo-Schalter (Selbsttest: `python3 .tools/kt38_katalog.py`). |
| `.tools/gen_kt38_shop.py` | Rendert **alle 29 Seiten**, `assets/produkte.js` und `sitemap.xml`. Enthält Bausteine (Bento, Rechner, Karten, Kapitel, Vollbild-Karte) und die **Produkt-SVGs**. `--check` meldet veralteten Bestand. |
| `.tools/kt38_prosa.py` | Die 12 Text-Seiten (Leistungen, Ratgeber, FAQ, Kontakt, Recht); lange Texte als Partials in `.tools/kt38_inhalt/`. |
| `.tools/kt38_chrome.py` | Kopf-Kapsel, Overlay-Schaufenster, Footer über Sentinels in **alle** Seiten. `--write` / `--check`. |
| `.tools/kt38_seite.py` | Seitenrahmen (`<head>`, Skripte, WhatsApp-FAB). |
| `.tools/shot_kt38_neu.mjs` · `kt38_sweep.mjs` · `kt38_kontrast.mjs` · `kt38_func_neu.mjs` | QA: Screenshots 1440/834/390 · 29 × 11 Breiten · Kontrast-Audit · Funktionstest (Overlay, Schalter, Rechner, Übergabe, Filter, FAQ). Alle laufen gegen `http://localhost:8765/` (`python3 -m http.server 8765` im Site-Ordner — `file://` blockiert die Schriften). |

**Reihenfolge nach jeder Änderung:**
```bash
python3 .tools/gen_kt38_shop.py && python3 .tools/kt38_chrome.py --write && python3 .tools/site_check.py klimatech38
```
Die Sentinels `<!-- KT38:HEADER:START/END -->` und `<!-- KT38:FOOTER:START/END -->` dürfen nicht entfernt werden.

---

## Design-Direction (Kurzfassung — Details in `assets/art-direction.md`)

- **Welt:** W5 Atmosphärisch in **heller** Ausprägung („Sommerlicht"): großflächige Fotografie, weiche
  kühle Tiefe, Sky-Blau als **Fläche** (Verläufe = kühle Luft), nicht als Haarlinie.
- **Brand-Anker (verankert):** Anthrazit #4D4D4D und Sky-Blau #A1C8EB aus dem echten InTroTech-Logo,
  Aktionsblau #1668AE (AA-Ableitung). **EIN Akzent** — das grüne Energie-Signal des Erstbaus entfällt.
  Tiefblau #0E2A3A nur als Footer-Grund. Echtes Zeichen (Haus + Tropfen) in der Kopf-Kapsel, Logo im
  „Mit wem"-Band und im Footer.
- **Signature:** der **Wege-Schalter** (s. o.).
- **Schriften:** Display **Funnel Display**, Text **Golos Text** — variabel, lokal in `assets/fonts/`,
  kein Google-CDN. Zwei Gewichte in einer Headline (`<em>` = 500/ink-soft) nur dort, wo die Headline
  eine echte Zweiteilung hat. Type-Ratio 1.333 ab 17 px Fließtext, Spacing 1.618, Radius 20 px / pill,
  Schatten weich-kühl, Container 1280 + vollbreite Bühnen.
- **Motion:** `data-motion="soft"` (Reveals up/mask/wipe, Hover-Lift hinter `hover:hover`), Hero als
  CSS-Load-Animation, `prefers-reduced-motion` schaltet alles statisch. Nur `transform`/`opacity`/`clip-path`.
- **Bildwelt:** keine eigenen Fotos (Sparte neu) → Pexels-Platzhalter, **alle auf eine kühle Gradierung
  gezogen** (Messwerte in `assets/_attribution.txt`); Hero-Innengerät ohne Herstellerkennzeichen
  (retuschiert). **Produkte = eigene ausgerenderte SVG-Darstellungen** (Isometrie, Lamelle, Display,
  Bodenschatten, Breite je kW) auf blauer Bühne — kein Fremdfoto mit fremdem Logo. Kein Helm-Stock.

## Skelett (Kurzfassung — Details in `assets/struktur-blueprint.md`)

Nav **Overlay-Fullscreen-Menü** („Schaufenster": Kapsel mit Wortmarke · Menü · Telefon · CTA; Overlay =
4 Bild-Kacheln + Set-Liste mit Preis lt. Schalter) · Sektions-Kopf **große h2 ohne Eyebrow + Kennwert-Chip
(≤ 3 Wörter)**, h2 in Aussageform (Fragen nur in FAQ und Ratgeber-Titeln) · Komponenten **bild-/bühnengeführte
Karten in variierten Größen** + Vollbild-Kapitel · Kontakt **Vollbild-Karte** (OSM lazy) mit
Overlay-Kontaktkarte und 6 Orte-Chips · Footer **4 Spalten, dunkel** mit Set-Index · Galerie **Bento
„Einbausituationen"** (jede Kachel wählt im Rechner die Raumsituation vor).

---

## Der Auslegungs-Rechner

Faustformel **Fläche × spezifische Kühllast**, offengelegt (60 W/m² Neubau · 80 Bestand · 100 Altbau ·
130 Dachgeschoss; Zuschläge Süd-/Westverglasung +20 W/m² · Raumhöhe > 2,60 m +10 % · Technik/offene
Küche +300 W; Multi: Außengerät auf 85 % der Summe). Ausgabe kW + BTU/h; ab **6 kW** keine
Self-Service-Empfehlung, sondern „Auslegung vor Ort". Der Treffer erscheint als Produktkarte (aus
`<template>`-Karten geklont) und auf der Startseite zusätzlich als dritte Karte der Einstiegsreihe.
Bento-Kacheln (`data-raum`) und `sessionStorage` (`kt38-raum`) belegen die erste Raumzeile vor.
Sichtbarer Hinweis: **Richtwert nach Faustformel — ersetzt keine Kühllastberechnung nach VDI 2078 bzw.
DIN EN 12831-1.** `aria-live`, tastaturbedienbar, kein Formularzwang.

## Anfrage-Übergabe statt Warenkorb
`sessionStorage`-Schlüssel `kt38-anfrage` (`{typ, quelle, id, weg, kw, text}`), geschrieben vom Rechner
(`typ:'auslegung'`) und jeder Set-Seite (`typ:'set'`, inkl. gewähltem Weg), gelesen einmalig auf
`kontakt.html`: Thema vorwählen, Nachricht füllen, sichtbarer, entfernbarer Bezugsblock. Ohne Bezug
wählt der Wege-Schalter das Thema vor (selbst → „Set anfragen", montage → „Beratung"). Beschrieben in
der Datenschutzerklärung.

---

## Echte Daten (verifiziert, aus introtech.de)
InTroTech GmbH · Zeisigweg 4 · 38518 Gifhorn · Tel. **05371 8759972** · info@introtech.de ·
WhatsApp `wa.me/4953718759972` · Mo–Fr 08–18 Uhr · Geschäftsführung Johann Warkentin, Jonathan
Mangold, Adrian Mangold · Amtsgericht Hildesheim **HRB 210481** · USt-IdNr. **DE460142356** ·
**dena-Energieberater**, **TÜV-zertifizierter Fachbetrieb** (einheitliche Formel auf allen Seiten) ·
Einzugsgebiet Gifhorn, Wolfsburg, Braunschweig, Peine, Salzgitter, Helmstedt.

## ⚠️ Vor Live-Schaltung klären
1. **Echte Geräteliste und Preise** → `META["demo"] = False`. Gebraucht: Modellbezeichnung, kW,
   SEER/SCOP + Effizienzklasse (EnVKV-Pflicht), Lieferumfang, Verfügbarkeit, Montagepauschalen.
2. **BAFA / Meisterbetrieb / Innung / Kälteschein bewusst NICHT behauptet.** Belegt sind nur dena und
   TÜV Rheinland. Weitere Nachweise erst nach Bestätigung des Betriebs ergänzen.
3. **Keine Referenzen/Projektfotos**, weil die Sparte neu ist. Sobald die ersten Anlagen stehen: eigene
   Fotos statt der Pexels-Platzhalter (`assets/_attribution.txt`) — besonders Hero und Bento.
4. **Kontaktformular ohne Backend** (Submit zeigt einen Hinweis mit Telefon/WhatsApp) → an ein Postfach anbinden.
5. **Datenschutzerklärung:** Hosting-Dienstleister und AV-Vertrag unter „Server-Logfiles" ergänzen.
6. **Karte:** zeigt das Einzugsgebiet; Koordinaten `52.481/10.547` sind auf Gifhorn gerundet.
7. **Verhältnis zur Mutterseite** klären (gegenseitige Verlinkung?).
8. Keine erfundenen Stats, Bewertungen, Gründungsjahre oder Verkaufsränge.
9. **Rechtslage Selbsteinbau prüfen lassen:** Die Seite zitiert die **F-Gase-Verordnung (EU) 2024/573** (löst
   seit 11.03.2024 die VO 517/2014 ab). Nach Art. 11 Abs. 5 dürfen nicht hermetisch geschlossene Geräte an
   Endkunden nur abgegeben werden, wenn die Installation durch ein zertifiziertes Unternehmen nachgewiesen wird.
   Ob die Quick-Connect-Sets als hermetisch geschlossen gelten und die Aussage „selbst einbaubar" so stehen
   bleiben darf, muss der Betrieb (bzw. sein Lieferant) bestätigen — sonst Hero-Schalter, FAQ und Ratgeber anpassen.
10. **Service-Zusagen bestätigen lassen** (stehen nicht auf introtech.de, die Sparte ist neu): Besichtigung,
   Auslegung und Angebot kostenfrei · Festpreis inkl. Montage · „in der Regel ein Arbeitstag" · Rücknahme von
   Altgeräten · Wartung/Reparatur von Fremdanlagen · Rückruf-Zeitfenster · **Abholung am Zeisigweg 4** und
   damit der ganze Weg „Selbst einbauen" (Vertriebsannahme aus den Vorbildern). Jede Zusage, die der Betrieb
   nicht halten will, muss vor Livegang raus.

## Technik
- Statisch, kein Build. Animation: `assets/motion.js` (Persona `soft`), GSAP/ScrollTrigger/Lenis lokal in
  `assets/js/`. Keine externen Requests außer der OpenStreetMap-Karte (lazy, in der Datenschutzerklärung beschrieben).
- Kein Cookie, kein Tracking. `sessionStorage` nur für Weg, Raum-Vorwahl und Anfrage-Übergabe.
- Kontraste nachgemessen (`.tools/kt38_kontrast.mjs`): alle Token-Paare ≥ 4,5:1; weißer Text nur auf
  Bildkacheln mit dunklem Verlauf. Sichtbare Fokuszustände, Hover auf allen Interaktiven, Touch-Ziele ≥ 44 px.
- Overlay: `inert` auf Inhalt/Footer, Fokusfalle, Esc, Scroll-Lock (Lenis pausiert).
- ⚠️ **`scroll-behavior:smooth` darf nicht gesetzt sein** (kämpft mit Lenis). ⚠️ **`[hidden]{display:none!important}`**
  steht bewusst ganz oben in `styles.css`.

## Qualitätssicherung (Stand 2026-09-12)
Deterministisch: `site_check.py` 0 FAIL / 0 WARN · Sweep 29 Seiten × 11 Breiten ohne Overflow/JS-Fehler ·
Kontrast-Audit · Funktionstest · Motion-Gate (nur transform/opacity/clip-path, Hover gegatet, Reduced-Motion).
`impeccable detect`: verbleibende Treffer sind False Positives (weißer Text auf Bildkacheln mit Verlauf,
kühl getönte Schatten-Tokens, bewusste Ablauf-Nummern, vollbreite Sektionen mit zentriertem `.wrap`).
4-Agenten-Panel (anti-ai · ui-layout · web-design · struktur-divergenz): Runde 1 mit Befunden, alle
umgesetzt — u. a. „Bestseller" → „Empfehlung", Button-Glow und Hero-Deko-Linien entfernt, Hero-Gerät
retuschiert, Bildwelt kühl gradiert und Motive getauscht (Kinderzimmer, Arbeitszimmer, Helm-Stock),
Produkt-SVGs ausgerendert und je kW skaliert, alle Kapitel-Köpfe hell, Frage-h2 in Aussageform, ein
CTA-Label („Beratung anfragen" → Formular), Hover auf allen Interaktiven, Kapsel ohne Blur, Grundlinien
der Karten, Rechner-Select, Touch-Ziele. Ergebnis der Runde 2 siehe Register-Eintrag.

## SEO
Eigene Unterseite je Leistung und je Set, Titel/Descriptions, `canonical`, Open Graph, Geo-Meta, JSON-LD
(`HVACBusiness` · `Service` · `ItemList` · `Product` + `BreadcrumbList` · `FAQPage` · `Article` ·
`ContactPage`), `robots.txt`, `sitemap.xml`, genau eine H1 je Seite, Alt-Texte, lokale Keywords.

## Dateien
```
index.html  shop.html  shop-{split,multisplit,mobil,zubehoer}.html  set-*.html (9)
klimaanlagen.html  beratung.html  montage.html  wartung.html  energetische-beratung.html
ratgeber.html  ratgeber-*.html (4)  faq.html  kontakt.html  impressum.html  datenschutz.html
styles.css  script.js  robots.txt  sitemap.xml  vercel.json  README.md  UEBERGABE.md
assets/  hero-wohnzimmer.jpg  hero.jpg  raum-*.jpg (6)  buero.jpg  gewerbe.jpg  innengeraet.jpg
         aussengeraet.jpg  fernbedienung.jpg  wohnraum.jpg  sonne-vorhang.jpg  daemmung.jpg
         energieausweis.jpg  pv-dach.jpg  pv-dach-2.jpg  motion.js  produkte.js (generiert)
         art-direction.md  struktur-blueprint.md  _attribution.txt
assets/brand/  logo.png  logo-white.png  mark.png     (echtes InTroTech-Logo)
assets/fonts/  FunnelDisplay-500-700  GolosText-400-600  (variabel, latin, lokal)
assets/js/     gsap.min.js  ScrollTrigger.min.js  lenis.min.js
```
Eigenständig deploybar (Vercel: Ordner als statische Site).
