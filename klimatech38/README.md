# KlimaTech38 — Website

Statische Website (HTML/CSS/JS, **kein Build im Deploy**) für **KlimaTech38**, den
Geschäftsbereich der **InTroTech GmbH** (Gifhorn) für **energetische Beratung** sowie **Planung,
Auslegung, Verkauf und Montage von Klimaanlagen**. Gebaut für die Domain **klimatech38.de**.

Die Sparte ist neu — die Marke ist es nicht: Logo, Farben, Ton, Kontakt- und Registerdaten kommen
1:1 vom bestehenden Auftritt der Mutterfirma (`introtech-sanierung/`, Original introtech.de).

---

## Konzept: zwei gleich starke Wege

Der Umbau vom September 2026 folgt zwei vom Kunden benannten Vorbildern:

| Vorbild | Was übernommen wurde |
|---|---|
| **solago.de** | Katalog mit sichtbaren Preisen, Kategorien nach Bauart und Raumgröße, Facettenfilter, Bestseller-Reihe, Ratgeber-Strecke, große FAQ, Mega-Menü und Mega-Footer |
| **klima-mueller.com** | Klassische Anfragestrecke: Preisanker („montiert ab …“), „Lassen Sie sich vom Profi beraten“, Direktkontakt per Telefon/WhatsApp, Rückruf mit Wunsch-Zeitfenster |

Daraus wird **ein** Angebot mit zwei Wegen, die überall nebeneinander stehen:

- **Selbst** — Set aussuchen, in Gifhorn abholen, selbst einbauen (mobil oder Quick-Connect).
- **Machen lassen** — kostenlose Besichtigung, Auslegung, Festpreis-Angebot, Montage, Wartung.

Jede Set-Seite nennt deshalb **zwei Preise**: `Abholung` und `inkl. Montage`.

**Es gibt bewusst keinen Warenkorb und keinen Checkout.** Jede Aktion heißt „anfragen“, nie
„kaufen“. Auf jeder Shop-Seite steht sichtbar, dass online kein Kauf zustande kommt und ein
schriftliches Angebot folgt. Das ist keine Schwäche der Umsetzung, sondern die Vorgabe — und es
hält das Nischen-Tabu ein, keinen Online-Shop anzudeuten, den es nicht gibt.

---

## ⚠️ Die Preise sind Beispielwerte

`META["demo"] = True` in `.tools/kt38_katalog.py`. Solange der Schalter steht:

- an jedem Preis erscheint das Label **„Beispielpreis“**,
- jede Shop-Seite trägt oben ein **Hinweisband**,
- das `Product`-JSON-LD wird **ohne `offers`** gerendert — Demo-Preise dürfen nicht in Googles
  Rich Results landen und dort im Cache stehen bleiben.

**Umschalten, sobald echte Preise vorliegen:** in `.tools/kt38_katalog.py` `META["demo"] = False`
setzen, Preise eintragen, dann `python3 .tools/gen_kt38_shop.py` und
`python3 .tools/kt38_chrome.py --write`. Mehr ist nicht nötig.

### Was rechtlich bewusst *nicht* von solago übernommen wurde
1. **Keine Streichpreise, keine „Ersparnis“.** § 11 PAngV verlangt bei jeder Preisermäßigung den
   niedrigsten Gesamtpreis der letzten 30 Tage. Den gibt es für einen Demo-Katalog nicht. Die
   Felder `streich_cent` / `streichTyp` existieren und sind `None`; `streichTyp` erzwingt später
   eine bewusste Entscheidung (`'uvp'` oder `'vorher30'`).
2. **Kein SEER/SCOP, keine Effizienzklasse.** Sobald echte Geräte mit Modellnamen erscheinen, sind
   Label und Produktdatenblatt nach EnVKV bzw. EU 626/2011 Pflicht. Erfundene Werte wären
   zusätzlich ein Wettbewerbsverstoß.
3. **Keine Countdowns, keine Lagerbestände, keine Bewertungen.**

Preise sind als Gesamtpreise **inkl. 19 % MwSt.** ausgewiesen (§ 3 PAngV), jede Shop-Seite nennt
Abholung und Lieferung (§ 6 PAngV). Da es keinen Bestellbutton gibt, ist die Seite eine
*invitatio ad offerendum* — Fernabsatzpflichten (Widerruf, AGB, Versandseite) greifen nicht.

---

## Aufbau — 29 Seiten

```
index.html                  Hero mit Preisanker → Vertrauensleiste → DIE ZWEI WEGE →
                            Rechner → Bestseller + Kategorien → Ablauf 1–5 → Energie →
                            PV-Kopplung → Ratgeber → Nachweise → Kontakt + Karte-Band
shop.html                   Übersicht: Vertrauensleiste, Rechner, 4 Kategorien, Bestseller,
                            Selbsteinbau-Grenzen, Abholung/Lieferung/Montage
shop-split.html             Kategorie: Split-Sets (1 Raum) + Facettenfilter
shop-multisplit.html        Kategorie: Multi-Split (2–4 Räume) + Facettenfilter
shop-mobil.html             Kategorie: mobile Monoblock-Geräte
shop-zubehoer.html          Zubehör als Spec-Zeilenliste mit Preisen
set-*.html            (9)   Set-Seiten: zwei Preise, Lieferumfang, Technikwerte, Zubehör, Ablauf
klimaanlagen.html           Klima-Strang: Beratung, Bauarten, Ablauf, PV, Kältemittel, Wartung
beratung.html         NEU   Der klassische Weg: Vor-Ort-Beratung, Ablauf 1–6, was wir ansehen
montage.html          NEU   Montagetag: Kernbohrung, Halter, Leitung, Vakuumieren, Inbetriebnahme
wartung.html          NEU   Wartung & Service: Umfang je Baugruppe, Intervalle, Störung
energetische-beratung.html  Energie-Strang: Ausweise, Thermografie, Maßnahmen
ratgeber.html         NEU   Übersicht
ratgeber-groesse.html NEU   Welche Leistung braucht mein Raum?
ratgeber-kosten.html  NEU   Was kostet eine Klimaanlage?
ratgeber-selbsteinbau.html NEU  Was darf ich selbst einbauen?
ratgeber-pv.html      NEU   Klimaanlage mit Photovoltaik
faq.html              NEU   14 Fragen mit FAQPage-JSON-LD
kontakt.html                Kanäle + Karte-Band → Anfrage mit Bezugsblock und Rückruf-Zeitfenster
impressum.html · datenschutz.html
```

---

## Werkzeuge — was von Hand gepflegt wird und was nicht

Der alte Zustand hatte die Navigation **siebenmal kopiert**. Bei 29 Seiten geht das nicht mehr.
Deshalb drei Skripte in `.tools/`:

| Skript | Zweck |
|---|---|
| `kt38_katalog.py` | **Einzige Wahrheitsquelle** für Sets, Zubehör, Preise, Demo-Schalter. Hat einen Selbsttest (`python3 .tools/kt38_katalog.py`). |
| `gen_kt38_shop.py` | Rendert daraus `assets/produkte.js`, `index.html`, `shop*.html`, alle `set-*.html` und `sitemap.xml`. `--check` meldet, wenn der Bestand veraltet ist. |
| `kt38_chrome.py` | Setzt Kopf und Fuß über Sentinels in **alle** Seiten. `--write` schreibt, `--check` gibt Exit 1 bei Abweichung. |
| `kt38_seite.py` | Seitenrahmen (head/Skripte) für die handgeschriebenen Prosa-Seiten. |
| `kt38_sweep.mjs` | Breakpoint-Sweep über 11 Breiten — gehört ins QA-Gate. |

**Reihenfolge nach jeder Änderung:**
```bash
python3 .tools/gen_kt38_shop.py        # Katalog + generierte Seiten
python3 .tools/kt38_chrome.py --write  # Kopf/Fuss in alle Seiten
python3 .tools/site_check.py klimatech38
```

Die Sentinels sehen so aus und dürfen **nicht** entfernt werden:
```html
<!-- KT38:HEADER:START --> … <!-- KT38:HEADER:END -->
<!-- KT38:FOOTER:START --> … <!-- KT38:FOOTER:END -->
```

Handgeschrieben (Inhalt frei änderbar, Kopf/Fuß kommen vom Skript):
`klimaanlagen.html` · `energetische-beratung.html` · `beratung.html` · `montage.html` ·
`wartung.html` · `ratgeber*.html` · `faq.html` · `kontakt.html` · `impressum.html` ·
`datenschutz.html`

---

## Design-Direction

- **Welt:** Swiss / Grid-Präzise — Haarlinien-Raster, Mono-Beschriftung, Datenblatt statt Broschüre.
- **Brand-Anker (verankert, nicht erfunden):** Anthrazit `#4D4D4D` und Sky-Blau `#A1C8EB` aus dem
  echten InTroTech-Logo; daraus Aktionsblau `#1668AE` (WCAG-AA) und Tiefblau `#10303F`.
- **Zwei Stränge, farbcodiert:** Blau = Kälte/Klima/Sets, Grün `#1A6E52` = Energie. Sie treffen
  sich nur dort, wo sie sich fachlich treffen: bei der **PV-Kopplung**.
- **Signature „Kältekreis-Linie“ — jetzt waagerecht:** Die Haarlinie unter dem Kopf **ist** die
  Kältemittelleitung; jeder Menüpunkt sitzt als Anschlusspunkt darauf. Sie füllt sich als
  Scroll-Fortschritt, läuft als Sektions-Oberkante durch die Seite, wird im Rechner zur
  **kW-Skala** und im Kontaktband waagerecht durch das Einzugsgebiet.
- **Schriften:** Display **Archivo**, Text **Public Sans**, Messwerte **IBM Plex Mono** — lokal in
  `assets/fonts/`, kein Google-CDN.
- **Motion:** `data-motion="mechanical"`, nur `transform`/`opacity`; `prefers-reduced-motion`
  schaltet alles statisch. Prosa- und Set-Seiten laden GSAP/Lenis bewusst **nicht** (rund 130 KB
  Parse-Arbeit gespart) — `assets/motion.js` hat dafür einen Fallback-Pfad.
- **Der Name:** Die **38** ist die PLZ-Region 38xxx (Gifhorn · Wolfsburg · Braunschweig) und damit
  das echte Einzugsgebiet.

### Skelett (Umbau September 2026)
Die feste linke „Anlagen-Rail“ ist entfallen — sie war für fünf flache Einstiege entworfen, jetzt
sind es fünf Stränge über 29 Seiten. An ihre Stelle tritt ein **sticky Kopf mit Mega-Menü**
(Servicezeile · Wortmarke · 5 Menüpunkte, zwei davon mit Spalten-Panel · Telefon · CTA) und ein
**Mega-Footer**. Mobil: Burger → modales Panel mit `inert`, Fokusfalle und Escape.

---

## Der Auslegungs-Rechner

Faustformel **Fläche × spezifische Kühllast**, offengelegt statt Blackbox:

| Raumsituation | W je m² |
|---|---|
| Neubau / gut gedämmt | 60 |
| Bestand / normal gedämmt | 80 |
| Altbau / wenig gedämmt | 100 |
| Dachgeschoss unterm Dach | 130 |

Zuschläge: große Süd-/Westverglasung **+20 W/m²** · Raumhöhe über 2,60 m **+10 %** ·
Technik/offene Küche **+300 W**. Bei mehreren Räumen wird das Außengerät auf **85 %** der Summe
ausgelegt. Ausgabe in **kW und BTU/h**, dazu die **kW-Skala**; ab **6 kW** keine
Self-Service-Empfehlung mehr, sondern Auslegung vor Ort (der Knopf „Passende Sets ansehen“
verschwindet dann).

Das Ergebnis führt in die **gefilterte Kategorieseite** (`shop-split.html#flaeche=32`) und lässt
sich per `sessionStorage` in das Anfrageformular übernehmen. Auf der Seite steht sichtbar:
**Richtwert nach Faustformel — ersetzt keine Kühllastberechnung nach VDI 2078 bzw.
DIN EN 12831-1.** Kein Formularzwang, `aria-live`, voll tastaturbedienbar.

## Anfrage-Übergabe statt Warenkorb
Ein `sessionStorage`-Schlüssel `kt38-anfrage` trägt einen JSON-Umschlag
(`{typ, quelle, id, variante, text}`). Ihn schreiben der Rechner (`typ:'auslegung'`) und jede
Set-Seite (`typ:'set'`); gelesen wird er einmalig auf `kontakt.html`, wo er das Thema vorwählt,
die Nachricht füllt und einen sichtbaren, entfernbaren **Bezugsblock** zeigt. In der
Datenschutzerklärung ist das beschrieben.

---

## Echte Daten (verifiziert, aus introtech.de)
InTroTech GmbH · Zeisigweg 4 · 38518 Gifhorn · Tel. **05371 8759972** · info@introtech.de ·
WhatsApp `wa.me/4953718759972` · Mo–Fr 08–18 Uhr · Geschäftsführung Johann Warkentin,
Jonathan Mangold, Adrian Mangold · Amtsgericht Hildesheim **HRB 210481** · USt-IdNr.
**DE460142356** · **dena-Energieberater**, geprüft über **TÜV Rheinland**, TÜV-zertifizierter
Fachbetrieb · Einzugsgebiet Gifhorn, Wolfsburg, Braunschweig, Peine, Salzgitter, Helmstedt.

## ⚠️ Vor Live-Schaltung klären
1. **Echte Geräteliste und Preise** → `META["demo"] = False`. Bis dahin sind alle Preise als
   Beispielwerte gekennzeichnet. Gebraucht werden: Modellbezeichnung, Leistungsdaten, SEER/SCOP
   und Effizienzklasse (EnVKV-Pflicht), Lieferumfang, Verfügbarkeit, Montagepauschalen.
2. **BAFA / Meisterbetrieb / Innung / Kälteschein bewusst NICHT behauptet.** Belegt sind über
   introtech.de nur **dena** und **TÜV Rheinland**. Sobald der Betrieb weitere Nachweise
   bestätigt (BAFA-Energieeffizienz-Expertenliste, Kälte-Klima-Meister, Sachkundenachweis nach
   EU-VO 517/2014), ergänze ich sie im Block „Mit wem haben Sie es zu tun?“.
3. **Keine Referenzen/Projektfotos**, weil die Sparte neu ist. Sobald die ersten Anlagen stehen:
   eigene Fotos statt der Pexels-Platzhalter (`assets/_attribution.txt`) — besonders das Hero.
   **Produktbilder sind bewusst eigene Strichzeichnungen**, kein Stock: ein Foto eines fremden
   Geräts wäre ein fremdes Lichtbild mit fremdem Herstellerlogo.
4. **Kontaktformular ohne Backend** (Submit zeigt einen Hinweis) → an ein Postfach anbinden.
5. **Datenschutzerklärung:** Hosting-Dienstleister und Auftragsverarbeitungsvertrag müssen unter
   „Server-Logfiles“ ergänzt werden (im Text als Hinweis markiert).
6. **Karten-Ausschnitt** zeigt das Einzugsgebiet, nicht die Hausnummer; Koordinaten `52.481/10.547`
   sind auf Gifhorn gerundet — exakte Adresskoordinaten vor Live setzen.
7. **Verhältnis zur Mutterseite** klären: bleibt introtech.de eigenständig und klimatech38.de
   verlinkt nur hin (aktueller Stand), oder soll gegenseitig verlinkt werden?
8. Keine erfundenen Stats, Bewertungen oder Gründungsjahre verwendet.

---

## Technik
- Statisch, kein Build im Deploy. Animation: `assets/motion.js` (Persona `mechanical`).
- **Keine externen Requests außer der OpenStreetMap-Karte:** GSAP, ScrollTrigger und Lenis liegen
  lokal in `assets/js/`, Schriften in `assets/fonts/`. Die Karte lädt verzögert und ist in der
  Datenschutzerklärung beschrieben.
- Kein Cookie, kein Tracking. `sessionStorage` nur für die Anfrage-Übergabe (siehe oben).
- **WCAG-AA-Kontraste, nachgemessen** — auf hellem Grund 4,9–14,7:1; auf dem dunklen
  `--klima-deep` über die drei Tokens `--on-deep-1/-2/-3` (12,5 / 7,6 / 5,5:1, alle klar blau getönt statt neutralgrau). Die Nachweiszeile
  (dena · TÜV Rheinland) trägt bewusst die zweitstärkste Stufe. Sichtbare Fokuszustände; jede
  Hover-Reaktion auf Karten-Ebene hat einen `:focus-within`-Zwilling **außerhalb** der
  `@media (hover:hover)`-Blöcke, damit Tastaturnutzer auf Touch-Geräten nichts verlieren.
  Mega-Menü und Mobil-Panel voll tastaturbedienbar (Enter/ArrowDown/Escape/Tab-Falle, geprüft mit
  `.tools/kt38_tastatur.mjs`).
- ⚠️ **`scroll-behavior:smooth` darf nicht gesetzt sein** — es kämpft mit Lenis, bremst das
  Scrollen aus und die `data-reveal`-Elemente bleiben unsichtbar.
- ⚠️ **`[hidden]{display:none!important}`** steht bewusst ganz oben in `styles.css`. Ohne diese
  Regel schlagen `display:grid` / `inline-flex` das `hidden`-Attribut — Filter, 6-kW-Grenze und
  Mega-Panel hätten stumm nicht funktioniert.

## Qualitätssicherung (Stand 2026-09-10, nach Runde 2 des QA-Panels)

Deterministisch — alle grün:
- `python3 .tools/site_check.py klimatech38` → **0 FAIL / 0 WARN** über 29 Seiten
- `node .tools/shot_kt38.mjs` → Screenshots 1440/834/390, keine Konsolenfehler
- `node .tools/kt38_tastatur.mjs` → Tastaturpfad Kopf → Mega → Panel (Enter/ArrowDown/
  Escape/Fokusfalle/Fokusrückgabe) ohne Befund
- `node .tools/kt38_sweep.mjs` → **29 Seiten × 11 Breiten (320–1920 px)**, kein Overflow,
  keine JS-Fehler. Dieser Sweep hat einen Fehler gefunden, den der 3-Breiten-Test übersah:
  bei exakt 1080 px erschien das Mega-Menü, obwohl der Kopf erst ab ~1180 px passt — die
  Servicezeile lief 70 px über. Behoben (Breakpoint auf 1180 px, Servicezeile darf umbrechen).
- `python3 .tools/kt38_chrome.py --check` · `python3 .tools/gen_kt38_shop.py --check` → aktuell
- **Motion-Gate**: nur `transform`/`opacity`, `out`-Easing, jede Hover-Bewegung hinter
  `@media (hover:hover) and (pointer:fine)`; `prefers-reduced-motion` und „ohne JS" geprüft —
  0 unsichtbare Reveal-Elemente

`npx impeccable detect .` (v4.1.0) → **86 Treffer aus zwei Regeln**, beide nachgemessen und als
False Positive bewertet:

**`cramped-padding` (77)** auf den
vollbreiten Farbbändern. **Nachgemessen und als False Positive bewertet** (vom
`anti-ai-reviewer` bestätigt): bei 1280 px haben die Bänder 50 px Abstand links/rechts und
7–16 px oben/unten, bei 390 px 18 px horizontal. Die Regel greift auf das Muster „vollbreites
Band + zentrierter `.wrap`" und erkennt den Innenabstand des Wrappers nicht.

**`wide-tracking` (9)** — 0,16 em auf `.mega-k` (Spaltenköpfe im Mega-Menü), dem Label des
Vorschau-Bands und der Filter-Legende. Das sind **Versalien-Labels von 14 bis 22 Zeichen**, nicht
Fließtext — genau das Mono-Label-Vokabular, das die Swiss-Welt dieser Seite trägt und das in
`assets/art-direction.md` als Typo-Entscheidung deklariert ist. Die Regel zählt jede Zeichenkette
über etwa 12 Zeichen als Fließtext. Echte Sätze in Versalien wurden entfernt (165 Treffer in
Runde 1); was bleibt, sind Labels.
*Hinweis:* Unter älteren impeccable-Versionen erscheinen zusätzlich `flat-type-hierarchy`
(der Detektor löst `clamp()` nicht auf — real ist die H1-zu-Body-Ratio ≈ 3,6:1, nicht 1,7:1)
und `numbered-section-markers` (bewusste Struktur-Achse). Beides ebenfalls False Positives.

### Runde 1 des Panels: alle vier Agenten DURCHGEFALLEN — was behoben wurde

**Fakten und Recht** (`anti-ai-reviewer`)
- Die Startseite führte Demo-Preise **ohne Kennzeichnung** — als einzige preisführende Seite
  ohne Hinweisband. Jetzt Band + Label am Hero-Anker; `data-preis-demo` wird serverseitig
  gesetzt (vorher war das CSS-Sicherheitsnetz toter Code), und die €-Beträge sind aus
  `description`/`og:description` verschwunden, solange `META["demo"]` gilt.
- `montage.html` behauptete den Sachkundenachweis per Schlussfolgerung („deshalb bauen wir …
  selbst ein") — umformuliert.
- „kein Weiterreichen an Subunternehmer" und „Montage vom eigenen Betrieb" widersprachen der
  eigenen AGB der Muttergesellschaft — ersetzt durch „Beratung, Montage und Wartung aus einer Hand".
- Floskeln „Rundum-Sorglos-Paket" und „Ihr Weg zu mehr Effizienz und Komfort" gestrichen;
  „kaufen"/„bestellen" aus zwei Sätzen entfernt.
- **Fremdes Herstellerlogo im Hero** (Schriftzug + Technologie-Badge auf der Gerätefront) —
  retuschiert, dokumentiert in `assets/_attribution.txt`.
- Englische Em-Dashes in vier Ratgeber-Seiten → Halbgeviertstrich; ae/oe/ue-Transliteration in
  Meta/OG/JSON-LD → echte Umlaute (Regel „echte Umlaute").
- Mobil-Burger war ein leerer Kasten (`>span{display:none}` traf auch das Icon) und hatte
  keinen zugänglichen Namen.

**Layout** (`ui-layout-reviewer`)
- `.steps` (Ablauf, 14 Seiten): CSS zielte auf `h3`/`p`, das Markup hat
  `span`/`b`/`span` — das dritte Kind fiel in eine implizite Zeile, die Schrittnummer verlor
  ihre Strangfarbe. Neu geschrieben: drei Spuren, Nummer wieder blau bzw. grün.
- `.raum` (Rechner): fünf Spuren bei sechs Kindern — „entfernen" kippte in Zeile 2, die
  Zuschläge in eine 80-px-Spalte. Jetzt sechs benannte Grid-Flächen.
- `.raum label{display:block}` schlug `.raum-z label{display:flex}` → Kästchen klebten am Text.
- `.nw-logo` hatte **keine einzige Regel** → das Logo lief auf 971 × 187 px.
- kW-Skala: die Achslinie lief durch die Beschriftung „ab hier vor Ort".
- `.set-zeile` unter 1080 px: Preis sprang unter die Schema-Spalte, weg vom Knopf.
- Die zwei Wege: CTAs 25 px versetzt. Kartenfuß 106 px neben der Inhaltsachse.
- **WhatsApp-Button** lag auf Preisen, FAQ-Zeilen und der Hero-CTA: die Kollisionsliste kannte
  weder `summary` noch `.preis`; im gedeckten Zustand tritt er jetzt zusätzlich per `transform`
  aus der Aktionsspalte.
- Touch-Ziele im Kopf auf 44 × 44 px.

**Design** (`web-design-reviewer`)
- Die Signature war zwei verschiedene Linien: Kopf `--line-strong`, Sektionskante `--line` —
  jetzt ein Wert. Der Anschlusspunkt verschwand unter 640 px komplett — bleibt jetzt.
- `assets/daemmung.jpg` war das einzige warme, 40 % dunklere Bild — und ausgerechnet das des
  Energie-Strangs. Neu graduiert (R/G/B 108/101/98 → 141/140/144, kühl wie die übrigen).
- **Energie-Strang untergewichtet** (3,8:1): Energieberatung war ein nackter Link neben zwei
  Klima-Mega-Panels, der Footer führte die Codierung gar nicht mehr, und `ratgeber-pv.html` —
  die eine Kreuzung beider Stränge — war neutral gebaut. Jetzt: eigenes `mega-energie`-Panel
  (1 von 3), grüne Strang-Punkte im Fuß-Index, PV-Seite mit zweifarbiger Kreuzungslinie.
- Vier Split-Sets teilten eine byte-identische Zeichnung. Die **kW-Skala der Signature** ist
  jetzt Produktmarke in Katalogzeile, Kachel und Set-Kopf — sie unterscheidet die Sets in genau
  dem Merkmal, in dem sie sich unterscheiden.

**Struktur** (`struktur-divergenz-reviewer`)
- Nav, Footer und „keine Galerie" kollidierten mit einem früheren Build (3/6, gefordert ≥ 4).
  Der **Mega-Footer ist einem Kontaktband gewichen** (große Telefon-CTA, Ort, Gebiets-Band,
  einzeiliger Seiten-Index) → Achse gewechselt.
- Blueprint-Auflage 13 („Unterseiten teilen keinen Kopf-Baustein") war verletzt: `.kopf-kat`
  trug neun fremde Seitentypen. `montage` bekam eine nummerierte Ablauf-Leiste, `wartung` eine
  Intervall-Datenliste, `ratgeber` und `faq` je einen eigenen Typo-Kopf; `.kopf-kat` gilt jetzt
  nur noch für die vier Katalog-Kategorien.
- `shop.html` steigt wie deklariert **mit dem Rechner** ein (h1); Vertrauensband und
  Bestseller-Reihe dort entfernt, damit index und shop nicht über drei Blöcke synchron laufen.

### Runde 2: was die zweite Prüfung noch fand

**Struktur — BESTANDEN.** Der Footer-Umbau hat die Achsen-Kollision geräumt (4/6 gegen den
Vergleichs-Build statt 3/6); Auflage 13 und die Rechner-Kopflösung auf `shop.html` sind umgesetzt.
Auflage 2 wurde präzisiert statt umgangen: **kein Lead unter der Sektions-Headline** (81 von 81
`h2` folgen direkt der Mono-Antwortzeile); im Seitenkopf unter der `h1` bleibt er zulässig.

**Anti-KI — weitere Funde, alle behoben:**
- **`&amp;` war doppelt escapt**: 15 Seiten trugen `&amp;amp;` im `<title>` und in jeder
  Share-Karte — der Generator escapte einen bereits escapten String ein zweites Mal.
- **Erfundene Gerätewerte.** Heizleistung und Schalldruck (dB(A)) waren je Set plausibel gesetzt
  und standen ungekennzeichnet als Datenblatt-Fakten, während dieselbe Fußnote SEER/SCOP
  zurückhielt. Beide sind jetzt `None` und die Zeilen entfallen. **`gwp` bleibt** — der GWP von
  R-32 (675) bzw. R-290 (3) ist eine veröffentlichte Eigenschaft des benannten *Kältemittels*,
  keine Aussage über ein Gerät.
- Der **Sachkundenachweis** wurde immer noch implizit behauptet („diesen Teil übernehmen wir
  deshalb"). Jetzt über die Zuordnung der Arbeit formuliert: „deshalb gehört dieser Schritt zur
  Montage und nicht zum Selbsteinbau."
- Badge „Ein Betrieb" (dieselbe Behauptung wie das gestrichene „eigener Betrieb") → „Ein
  Ansprechpartner". „Marken-Klimageräte, keine Restposten" → sachlich ersetzt.
- „Rückmeldung in der Regel am selben Werktag" war nirgends belegt → entfernt.
- Restliche Transliterationen in JSON-LD und Quelltext-Kommentaren.

**Breakpoint-Sweep** (neues Werkzeug): bei exakt 1080 px erschien das Mega-Menü, obwohl der Kopf
erst ab ~1180 px passt — die Servicezeile lief auf **allen 29 Seiten** 70 px über. Der
3-Breiten-Test hatte das nicht gesehen. Breakpoint auf 1180 px, Servicezeile darf umbrechen.

### Runde 2, zweite Schleife — was noch fiel

Zwei meiner Runde-1-Fixes hatten **Regressionen** erzeugt; beide sind zurückgenommen:
- Ich hatte `.steps h3` / `.steps p` als toten Code gelöscht — sie waren **nicht tot**:
  `energetische-beratung.html` und `klimaanlagen.html` benutzten die `h3`/`p`-Variante mit **zwei**
  Kindern. Ergebnis waren bis zu 86 px Text über Text. Jetzt nutzen alle 14 Seiten **ein** Markup
  (`span.mono` · `b` · `span`).
- `.art{margin-inline:0}` sollte Lesespalte und H1 auf eine Achse bringen, hat aber die
  `.wrap`-Zentrierung abgeschaltet — die Lesespalte klebte auf fünf Seiten bei `x=0`. Richtig ist:
  Wrap behält die Container-Achse, die Lesebreite geht an die Kinder
  (`.art>*{max-width:min(70ch,42rem)}` — `ch` löst in dieser Schrift auf 12 px auf, 70ch wären
  857 px Zeilenlänge gewesen).

Weiter behoben: `.abschluss-cta` saß auf **24 Seiten** mit 0 px auf der Vorgängerkante (Haarlinie
und Knopfrahmen verschmolzen) · `.tab` klebte am Absatz · `.kanal` deklarierte `align-items`
zweimal in derselben Regel, das spätere gewann · die kW-Skala brach rechts aus dem Panel · der
Rechner-Wert war der einzige ohne Mono-Label und saß dadurch auf der Spaltenkopf-Achse · der
Sektions-Marker klebte zwischen 641 und 900 px am Bildschirmrand · Anker-Sprünge landeten 18 px
unter dem Kopf, weil `--kopf-h` die Servicezeile nicht mitzählte · die Mega-Panels hatten keinen
Scrim · im Fuß waren die Touch-Ziele 15 px und die 76-px-Magic-Number war zurück.

Aus dem Design-Review: **zwei harte WCAG-AA-Verstöße** auf dem dunklen Grund (4,31:1 und 3,67:1 —
ausgerechnet auf der Nachweiszeile dena/TÜV). Behoben über drei Tokens `--on-deep-1/-2/-3`
(12,5 / 7,6 / 5,5:1), die zugleich neun kaum unterscheidbare Blaugrau ersetzen. Dazu: der
Strang-Schlüssel auf `ratgeber-pv.html` zeigte die Farben der **dunklen** Fläche und damit weder
`--klima` noch `--energie` · 12 Sperrungswerte auf 7 Tokens reduziert · `daemmung.jpg` und
`aussengeraet.jpg` in die kühle Bildfamilie gezogen · die kW-Marke der mobilen Geräte auf 4 kW
Vollausschlag skaliert (auf der 10-kW-Skala lagen 2,0 und 2,6 kW nur 3 px auseinander).

## SEO
Eigene Unterseite je Leistung und je Set, sprechende Titel/Descriptions, `canonical`, Open Graph,
Geo-Meta, **JSON-LD** (`HVACBusiness` · je Unterseite `Service` · `ItemList` je Kategorie ·
`Product` + `BreadcrumbList` je Set · `FAQPage` · `Article` je Ratgeber · `ContactPage`),
`robots.txt`, generierte `sitemap.xml`, genau eine H1 je Seite, Alt-Texte, lokale Keywords.

## Dateien
```
index.html  shop.html  shop-{split,multisplit,mobil,zubehoer}.html  set-*.html (9)
klimaanlagen.html  beratung.html  montage.html  wartung.html  energetische-beratung.html
ratgeber.html  ratgeber-*.html (4)  faq.html  kontakt.html  impressum.html  datenschutz.html
styles.css  script.js  robots.txt  sitemap.xml  README.md
assets/  hero.jpg  wohnraum.jpg  innengeraet.jpg  aussengeraet.jpg  daemmung.jpg
         energieausweis.jpg  motion.js  produkte.js (generiert)
         art-direction.md  struktur-blueprint.md  _attribution.txt
assets/brand/  logo.png  logo-white.png  mark.png     (echtes InTroTech-Logo)
assets/fonts/  Archivo · Public Sans · IBM Plex Mono  (lokal, latin)
assets/js/     gsap.min.js  ScrollTrigger.min.js  lenis.min.js
```
Eigenständig deploybar (Vercel: Ordner als statische Site).
