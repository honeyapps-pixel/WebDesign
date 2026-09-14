# Struktur-Blueprint — KlimaTech38 · Redesign 2026-09-12
**Phase 1.6 · geplant vom `struktur-architekt` · verbindlich für Bau und QA-Gate (Phase 8)**
Ersetzt `.tools/kt38_inhalt/_alt_erstbau/struktur-blueprint-2026-09-10.md` vollständig. Das alte Blueprint ist der **Gegenpol**:
alles darin gilt als „wie zuletzt" und wird auf keiner Achse wiederholt.

Branche: C2 (SHK/Klima) + C5-Andockung (Katalog mit sichtbaren Preisen, KEIN Warenkorb — alles heißt „anfragen")
Archetyp **B/Showcase** · Welt W5 hell „Sommerlicht" · Motion **soft**
Signature (Phase 1.5, nicht verhandelbar): **Wege-Schalter** „Selbst einbauen | Einbauen lassen" (sessionStorage `kt38-weg`)
Kein Batch — Einzelbuild. Vergleichshorizont: **KT38-Erstbau** (letzter) · **DK Fenster** (vorletzter) · **MAVA** (3.).

Strukturprägend ist der Content, nicht der Wunsch nach Andersartigkeit:
- **Katalog:** 9 Sets in 4 Kategorien (Split 2,5/3,5/5,0/7,0 kW · Multi Duo/Trio/Quattro · mobil 2,0/2,6 kW · 7 Zubehör-Positionen),
  je Set **zwei Preise** (Abholung / inkl. Montage), im Katalog markierte Bestseller: **genau 2** (Split 3,5 kW · Multi Duo).
  Wahrheitsquelle `.tools/kt38_katalog.py`.
- **Auslegungs-Rechner:** Räume (bis 5) → Kühllast kW/BTU → passendes Set, 6-kW-Grenze → Multi-Split / Auslegung vor Ort.
- **Ablauf:** 5 Auftragsschritte (Anfrage → Besichtigung → Angebot → Montage → Einweisung) auf index; 7 Arbeitsschritte auf montage.html.
- **Energie:** aus den vorhandenen h2 ableitbar: Energieausweis · Wärmeverlust-Aufnahme · Sanierungsplan; PV-Kopplung als Brücke.
- **Wissen:** 4 Ratgeber (Fragetitel) + 14 FAQ.
- **Kontakt:** ein Standort (Zeisigweg 4, Gifhorn), 6 Einzugsorte, Rückruf-Zeitfenster im Formular.
- **Nachweise:** nur dena-Energieberater + TÜV Rheinland; InTroTech-Logo als Mutterfirma.
- **Bilder:** keine eigenen Referenzfotos (Sparte neu) → Bilder sind **Einbausituationen** (5 Räume mit Innengerät, Pexels),
  nie Referenzen; Produkte als eigene SVG-Darstellung auf Bühne + kW-Chip.

---

## Die 7 Achsen

### 1. Nav-Paradigma — **Overlay-Fullscreen-Menü („Schaufenster")**, auf allen Breiten identisch
- **Kopf** = schwebende Kapsel, vom Rand abgesetzt, transparent über dem Hero → deckend nach Scroll. Inhalt **genau**:
  Wortmarke · „Menü"-Taste · Telefon · CTA-Pill. **Kein weiterer Link im Kopf**, keine Servicezeile, keine Linie unter dem Kopf.
  Unter 720 px: Wortmarke · Menü · Telefon-Icon (CTA wandert ins Overlay).
- **Overlay** = ganzseitiges Schaufenster mit 3 Zonen:
  (a) **4 Bild-Kacheln je Strang** — Klimaanlagen (Beratung · Montage · Wartung) · Sets & Preise (shop + 4 Kategorien) ·
  Energieberatung · Ratgeber & FAQ; (b) **Set-Liste** — 9 Sets: Titel · kW · Preis lt. Schalter, der **Wege-Schalter sitzt auch
  im Overlay**; (c) Kontaktzeile (Telefon · WhatsApp · Zeiten) + Legal-Links.
  Technik: `inert` auf dem Seiteninhalt, Fokusfalle, Esc, Scroll-Lock, `aria-expanded` auf der Taste. **Kein Drawer-Fallback**
  auf irgendeiner Breite — das Overlay ist überall dieselbe Fläche.
- **Weil:** 29 Seiten mit 4 Kategorien + 9 Sets brauchen eine Übersicht **mit Bild** (Vorbilder des Kunden sind bildgeführt),
  und der Topbar-Bucket ist gesperrt (MAVA + Erstbau in Folge). Feste Sidebar (war der abgelehnte Erstbau-Ursprung und kollidiert
  mit vollbreiten Bühnen), Minimal/Scroll-Spy (tragen 29 Seiten nicht) und Split-Screen-Nav (nur im Hero) scheiden aus.
- **Detail, kein Paradigma:** die 9 Set-Seiten bekommen eine sticky **Produkt-Unterleiste** (Titel · Preis lt. Schalter ·
  „Set anfragen"), die **oben unter der Kapsel andockt**, sobald der Produkt-Kopf ausgescrollt ist. Nie unten (Bottom-Bar ist
  gesperrt), nie mit Site-Links, nur auf Set-Seiten.

### 2. Sektions-Kopf — **Kein Eyebrow: große h2 mit zwei Gewichten in EINER Zeile + optionaler Kennwert-Chip**
- h2 mischt zwei Gewichte in einer Zeile (Typo lt. Brief). **Kein** Eyebrow, **keine** Antwortzeile, **kein** Lead unter der h2
  (Leads nur unter der h1 im Seitenkopf).
- **Kennwert-Chip** = Pill mit ≤ 3 Wörtern aus dem Content — „ab 749 €", „2–4 Räume", „1 Arbeitstag", „dena-zertifiziert" —
  rechts neben der h2 (ab 900 px) oder darunter (mobil). Nicht Mono, nie ein Satz, nie eine Erklärung.
- **h2 in Aussageform.** Fragen bleiben nur dort, wo die Frage der Inhalt IST: FAQ-Einträge (`<summary>`) und
  Ratgeber-Artikeltitel. → Einzige Textberührung des Redesigns: die Frage-h2 der Leistungsseiten („Split oder Multi-Split?",
  „Wie oft muss gewartet werden?") werden in Aussageform gesetzt — gleiche Aussage, keine neuen Fakten, Fließtext 1:1.
  Grund: „Frage-Headline" ist im Register gesperrt.
- **Weil:** Die harten Werte des Katalogs (kW, Preis, Räume, Dauer) gehören AN die Headline — als Chip, nicht als Mono-Zeile
  darunter (Erstbau) und nicht als Versalien-Strich darüber (DK).

### 3. Komponenten — dominant **Karten-Raster** in der Ausprägung *bild-/bühnengeführte Karten in variierten Größen*
- **Karte** = Foto (Situation) ODER Produkt-Bühne (SVG-Gerät auf Verlauf) + Titel + Kennwert-Chip + Preis lt. Schalter.
  Größen 2:1 / 1:1 / 1:2, Bento-artig gesetzt. Radius/Schatten/Hover-Lift lt. Brief-Tokens.
- **Neben-Bauform: Vollbild-Kapitel** — Montage- und Energie-Kapitel auf index; Kapitel-Kopf der 5 Leistungsseiten.
- **Unter-Elemente** (keine eigenen Achsenwerte): horizontale **Step-Strecke** (Ablauf 1–5 auf index, 1–7 auf montage) innerhalb
  des Montage-Kapitels · **Akkordeon** nur auf faq.html (14 Fragen, contentbedingt) · Listen nur *innerhalb* einer Set-Karte
  (Lieferumfang / Nicht enthalten) · **ein** Split-Block für die PV-Kopplung (kein Wechsel-Rhythmus).
- **Regeln gegen das alte 3-Karten-Default:** nie drei gleich große, textbasierte Karten als alleiniges Muster einer Sektion;
  jede Karten-Sektion hat ≥ 2 Kachelgrößen oder trägt Bild/Bühne; keine Karte ohne Bild, Bühne oder Kennwert.
- **Weil:** Produkt und Situation müssen **sichtbar** sein (Kundenanmutung solago/klima-mueller); ein Katalog wird über
  Kacheln verglichen. Spec-Zeilen/Tabellen sind gesperrt.

### 4. Kontakt — **Vollbild-Karte**
- OSM-Karte im regionalen Zoom (Gifhorn – Wolfsburg – Braunschweig – Peine – Salzgitter – Helmstedt) trägt die **ganze
  Sektion**: ≥ 72 vh Desktop / ≥ 60 vh mobil. Darüber eine **Kontakt-Karte als Overlay**: Telefon · WhatsApp · Mail · Zeiten ·
  **6 Einzugsorte als Chips** · „Rückruf vereinbaren" → kontakt.html.
- Eigene Sektion, klar vom Footer getrennt (der Footer ist ein eigener dunkler Block — kein Karte-als-Footer-Hintergrund).
  Karte lazy geladen; `prefers-reduced-data`-Fallback als statisches Kartenbild optional.
- Auf **kontakt.html** ist die Vollbild-Karte der Seiteneinstieg (h1 im Overlay); das Formular mit Rückruf-Zeitfenster und
  Thema-/Set-Vorwahl (sessionStorage) folgt als eigene Sektion.
- **Weil:** Ein Einzugsgebiet aus 6 Orten braucht die Fläche einer Karte, nicht einen Streifen (Band gesperrt); ein Standort
  braucht keinen Umschalter (interaktiv gesperrt); ein Katalogbetrieb ohne Ladenlokal-Fokus braucht keine Kachel neben dem Formular.

### 5. Footer — **mehrspaltig (4 Spalten), dunkler Block, Menü-Bucket „3-Spalten", ohne `<details>`**
- Spalte 1: **InTroTech-Logo** (weiße Fassung lt. Brief) + Sparten-Erklärung als 2–3 Zeilen in **Textgröße** — kein Display-Satz.
- Spalte 2: **Set-Index** (4 Kategorien, darunter die 9 Sets). Spalte 3: Beratung & Wissen (5 Leistungsseiten · Ratgeber · FAQ).
  Spalte 4: Kontakt kurz (Anschrift · Telefon · Zeiten) in Textgröße — **keine** große Tel-CTA.
- Legal-Zeile darunter: Impressum · Datenschutz · Demo-Hinweis. Mobil: Spalten gestapelt, Set-Index als Chip-Zeile.
- Größtes Textelement im Footer = Spaltenüberschriften (verhindert Mega-Footer-Lesart); größte Aktion = Textlinks
  (verhindert Kontaktband-Lesart).
- **Weil:** 29 Seiten brauchen einen Index-Fuß; Kontaktband (Erstbau), einzeilig (DK) und Mega-Footer (MAVA) sind im
  Horizont; Sidebar-Footer ohne Sidebar ist unplausibel.

### 6. Galerie — **Bento-Grid „Einbausituationen"**
- 5 Kacheln in 3 Größen: Wohnzimmer (groß, 2:1) · Schlafzimmer · Kinderzimmer · Arbeitszimmer · Dachgeschoss (1:2 hoch).
  Bildquelle: die vorhandenen `assets/raum-*.jpg` (Pexels, Attribution in `assets/_attribution.txt`).
- Jede Kachel: Foto mit Innengerät + Raumtyp + typische Fläche + **kW-Spanne** (abgeleitet aus Rechner-Regel/Katalog-Raumbereich,
  **kein Preis** auf der Kachel) — und **verlinkt in den Rechner mit vorgewählter Raumsituation**:
  auf index Scroll zur Rechner-Bühne direkt darunter + Vorwahl; von Unterseiten `index.html#rechner` + Vorwahl per
  URL-Parameter oder sessionStorage (`kt38-raum`). Dachgeschoss setzt zusätzlich die Raumsituation „Dachgeschoss".
- Captions sagen „Einbausituation", **nie** „Referenz", „Kundenprojekt", „unsere Montage".
- **Weil:** Die Räume SIND die Eingabe des Rechners — die Galerie hat eine Funktion (Einstieg in die Auslegung). „Keine Galerie"
  ist nach 4 Vergaben gesperrt, und hier gibt es erstmals einen echten Grund FÜR eine.

### 7. Sektions-Spine (index)
```
Hero(Vollbild-Foto · Wege-Schalter · Preisanker · Luftstrom-Motiv)
→ Einbausituationen(Bento 5 Räume — „Welcher Raum?")
→ Rechner(Bühne: Eingabe-Karte | Ergebnis-Produktkarte; vorbelegt aus Bento; 6-kW-Grenze)
→ Bestseller(Karten-Reihe 3: die 2 Katalog-Bestseller [Split 3,5 · Multi Duo] + 1 „Ihr Treffer"-Karte = Rechner-Ergebnis;
             Leerzustand: Split 2,5 kW als „Kleinster Standard"; Preis folgt Schalter)
→ Kategorien-Bühne(4 Bild-Kacheln → shop-split · shop-multisplit · shop-mobil · shop-zubehoer)
→ Montage-Kapitel(Vollbild-Foto + Ablauf-Strecke 1–5 horizontal → montage.html)
→ Energie-Kapitel(Vollbild Sonne/Vorhang + 3 Leistungs-Karten: Ausweis · Wärmeverlust-Aufnahme · Sanierungsplan → energetische-beratung.html)
→ PV-Kopplung(EIN Split-Block Bild | Text → ratgeber-pv.html)
→ Wissen(Karten-Reihe: 4 Ratgeber-Karten mit Bild + 1 breite FAQ-Karte mit 3 Beispielfragen → faq.html)
→ Mit wem(Logo-Band: InTroTech-Logo + „Geschäftsbereich der InTroTech GmbH" + 2 Nachweise dena / TÜV Rheinland)
→ Kontakt(Vollbild-Karte + Overlay)
→ Footer(4-spaltig)   [+ .wa-fab]
```
**Abweichung vom Brief-Vorschlag** (dort Kategorien Pos. 2 · Bestseller 3 · Rechner 4 · Bento 5): Bento → Rechner → Treffer-Karte
sind **ein Trichter** (Kachel wählt Raum, Rechner direkt darunter rechnet vorbelegt, Ergebnis erscheint als dritte Karte der
Bestseller-Reihe) und stehen deshalb hintereinander auf Pos. 2–4. Die Kategorien-Bühne ist danach der „alle Sets"-Ausgang.
Preise bleiben ab dem ersten Viewport sichtbar (Preisanker im Hero). Der Rechner rückt von Pos. 4 (Erstbau) auf Pos. 3.
**Set-Änderungen gegenüber dem Erstbau:** − Vertrauensband · − eigene „Zwei Wege"-Sektion (der Schalter ersetzt sie) ·
+ Einbausituationen · + Kategorien als eigene Bühne · Ratgeber + FAQ zusammengelegt · Nachweise als Logo-Band statt Zeilenliste.

---

## Unterseiten — je Seitenfamilie ein eigener Kopf (keine Familie nutzt den Kopf einer anderen)
| Familie | Seiten | Einstiegstyp | Trägerbauform darunter |
|---|---|---|---|
| Start | index.html | **Vollbild-Hero** mit Wege-Schalter + Preisanker | Spine oben |
| Katalog-Übersicht | shop.html | **Katalog-Kopf**: h1 + großer Wege-Schalter + **4 Kategorie-Bildkacheln bilden den Kopf** (der Rechner ist hier NICHT mehr Kopf) | Rechner (Bühne) → alle 9 Sets als Karten, je Kategorie gruppiert (h2 + Chip) → Zubehör (kompakte Karten) → 2 Karten „Grenzen des Selbsteinbaus" / „Abholung · Lieferung · Montage" |
| Kategorie | shop-split · shop-multisplit · shop-mobil · shop-zubehoer | **Bühnen-Kopf**: vollbreite Bühne, links h1 + Raumbereich-Chip (z. B. „1 Raum · 18–70 m²"), rechts große Produkt-SVG der Kategorie; Schalter im Kopf | Set-Karten der Kategorie (Bestseller 2:1, übrige 1:1) → 2 Nachbarkategorie-Kacheln → Anfrage-CTA. Zubehör: Karten mit Einzelpreis + „passt zu"-Links |
| Set | 9 × set-*.html | **Produkt-Kopf** (50/50): links Produkt-SVG auf Bühne + kW-Chip, rechts h1 + Kurztext + **Preis-Doppel** (Abholung \| inkl. Montage — der Schalter hebt eine Spalte hervor) + „Set anfragen"; darunter dockt die sticky Produkt-Unterleiste **oben** an | „Passt für" (Raum-Chips + Fläche) → eine Karte mit 2 Spalten Lieferumfang \| Nicht enthalten → Montageumfang-Karte (bei Schalter „Einbauen lassen" hervorgehoben) → passendes Zubehör (Karten) → Nachbar-Sets (Karten-Reihe) → Anfrage-CTA (übergibt Set + Weg per sessionStorage) |
| Leistungsseite | beratung · montage · wartung · klimaanlagen · energetische-beratung | **Kapitel-Kopf**: Vollbild-Foto, h1 unten links + Kennwert-Chip + **variabler Kopf-Slot je Seite** — montage: Strecken-Vorschau 1–7 · wartung: Intervall-Chips (1× Wohnbereich · 2× Dauerbetrieb · Dichtheit) · energetische-beratung: Nachweis-Chips (dena · TÜV) · beratung: Kontaktwahl (Tel · WhatsApp · Formular) · klimaanlagen: Bauform-Chips (Split · Multi-Split · mobil) | montage: Step-Strecke 1–7 → Karte „Im Montagepreis enthalten" · wartung: 3 Intervall-Karten → Ablauf-Karte → Störungs-Karte · energetische-beratung: 3 Leistungs-Karten → je Thema ein Vollbild-Kapitel (Ausweis / Wärmeverlust / Plan) → Nachweis-Band · beratung: Ablauf-Strecke 1–5 → Vor-Ort-Karte → Kontaktwahl · klimaanlagen: 2 Bühnen-Karten Split \| Multi-Split → Themen-Karten (Außengerät · Kältemittel · Wartung) → PV-Split-Block |
| Ratgeber-Index | ratgeber.html | **Index-Kopf**: h1 + die 4 Artikel-Karten (Bild · Fragetitel · Lesezeit) sind selbst der Kopf | breite FAQ-Karte → Set-Hinweis-Karte |
| Ratgeber-Artikel | 4 × ratgeber-*.html | **Artikel-Kopf**: Bild-Band ~40 vh + h1 (Frage = Inhalt) + Lesezeit-Chip | Lesespalte ≤ 62ch, Zwischen-h2 in Aussageform → Karte „Passende Sets" → Nachbar-Artikel (2 Karten) |
| FAQ | faq.html | **Fragen-Kopf**: h1 + 4 Themen-Chips (Einbau · Betrieb · Kosten · Recht) filtern die 14 Fragen — jede Frage genau ein Thema, Zuordnung im Bau | Akkordeon (`<details>`), nach Thema gruppiert → Kontakt-Karte |
| Kontakt | kontakt.html | **Karte-zuerst**: Vollbild-Karte mit Overlay-Kontaktkarte, h1 darin | Formular (Rückruf-Zeitfenster · Thema/Set vorbelegt) \| Zeiten & Kanäle als Split → Einzugsorte-Chips |
| Recht | impressum · datenschutz | schmale Lesespalte, kein Bild, h1 + Stand | — |

**10 Kopf-Typen** (Hero · Katalog · Bühne · Produkt · Kapitel mit 5 Slots · Index · Artikel · Fragen · Karte-zuerst · Recht).
Die Erstbau-Klassen `.kopf-*` (rechner · kat · set · art · index · frage · ablauf · intervall · nachweis · schema · beratung)
werden **nicht wiederverwendet** — weder als Name noch als Form.

---

## Wege-Schalter — strukturelle Einbauorte (Signature aus Phase 1.5)
Hero (index) · Katalog-Kopf (shop) · Bühnen-Kopf (4 Kategorien) · Produkt-Kopf + Unterleiste (9 Sets) · Overlay-Set-Liste ·
Kontaktformular (Thema). Ein Zustand (`kt38-weg`), alle Preise in Karten, Listen und Unterleiste folgen ihm. **Standard =
„Einbauen lassen"** (Conversion-Primärziel Beratung/Montage; Vorbild klima-mueller „montiert ab") — Annahme, siehe unten.
Der Schalter ist eine Steuerung, **keine** Sektion: es gibt keine „Zwei Wege"-Sektion mehr.

## Rechner — Bauform (Logik unverändert)
Bühne (vollbreiter Verlauf lt. Brief) mit **Eingabe-Karte** links (Räume bis 5: Fläche + Raumsituation + Süd-Verglasung, Bauart-Wunsch)
und **Ergebnis-Produktkarte** rechts (SVG-Gerät + kW-Chip + Set-Titel + Preis lt. Schalter + „Set ansehen"/„anfragen").
Über 6 kW: Ergebniskarte zeigt Multi-Split-Empfehlung + „Auslegung vor Ort". Kein Datenblatt-Panel, kein Modal, kein Wizard.
Weiter gültig: Gleichzeitigkeitsfaktor offengelegt, kein Formularzwang, `aria-live="polite"`, feste Ergebnisposition,
Tastaturbedienung, Disclaimer „Richtwert nach Faustformel". **Verboten bleibt:** Preisberechnung, Ersparnis-/Amortisationsrechnung,
Förderhöhen, Verfügbarkeits-/Countdown-Anzeigen.

---

## Divergenz-Nachweis vs. Vergleichshorizont
| Achse | **Redesign** | KT38-Erstbau (letzter) | DK Fenster (vorletzter) | MAVA (3.) |
|---|---|---|---|---|
| Nav | Overlay-Fullscreen-Menü (Schaufenster) | Topbar + Mega-Menü ✓ | Bottom-Bar ✓ | Topbar + Drawer ✓ |
| Sektions-Kopf | Kein Eyebrow: große h2 (2 Gewichte) + Kennwert-Chip | Frage-Headline + Mono-Antwortzeile ✓ | eyebrow→h2→lead ✓ | Randständige Marginalie ✓ |
| Komponenten | Karten-Raster (bühnengeführt, variierte Größen) + Vollbild-Kapitel | Listen/Tabellen ✓ | Split-Bild-Text-Wechsel ✓ | Fließtext-Editorial ✓ |
| Kontakt | Vollbild-Karte + Overlay | Karte als Band ✓ | interaktiv (Anfrage-Schalter) ✓ | keine Karte / formulargeführt ✓ |
| Footer | mehrspaltig 4 Sp. (3-Spalten-Bucket, ohne `<details>`) | Footer als Kontaktband ✓ | einzeilig minimal ✓ | Mega-Footer mit Claim ✓ |
| Galerie | Bento-Grid (Einbausituationen) | keine ✓ | Vollbild-Slider ✓ | keine ✓ |
| **abweichend** | — | **6/6** | **6/6** | **6/6** |

- **Spine ≠ letzte 3:** ✓ — Erstbau: anderes Sektions-Set (− Vertrauensband, − Wege-Sektion, + Bento, + Kategorien-Bühne,
  Wissen zusammengelegt), andere Reihenfolge (Bento/Rechner/Bestseller/Kategorien statt Wege/Rechner/Bestseller+Kategorien),
  jede Sektion in anderer Bauform. DK Fenster (Sortiment-Zeilenliste → Split-Reihen → Slider → Referenzen → Ablauf → Betrieb → Anfrage)
  und MAVA (Editorial-Split → Bild-Register → Wort-Trias → Erstgespräch-Band) teilen weder Set noch Reihenfolge.
- **Nav ≠ unmittelbar vorheriger (Erstbau Topbar+Mega):** ✓ · **Kontakt ≠ unmittelbar vorheriger (Karte als Band):** ✓
- **≥ 4/6 gegen jeden der letzten 2:** 6/6 gegen Erstbau, 6/6 gegen DK Fenster (und 6/6 gegen MAVA).
- **Sperrliste Stand DK eingehalten:** Bottom-Bar/Sheet ✗ (Unterleiste dockt oben, nur Set-Seiten) · eyebrow→h2→lead ✗ ·
  Split-Bild-Text-Wechsel ✗ (PV = ein Einzelblock, kein Wechsel) · Vollbild-Slider ✗ · einzeilig-minimaler Footer ✗ ·
  Typenblatt-Einheitskopf ✗ (10 Kopf-Typen) · Kontakt interaktiv ✗.
- **Sperrliste Stand KT38-Erstbau eingehalten:** Topbar jeder Ausprägung ✗ · Footer als Kontaktband ✗ · Frage-Headline + Mono-Antwort ✗ ·
  Listen/Tabellen dominant ✗ · Karte als Band ✗ · keine Galerie ✗ (Bento mit Funktion) · Motion mechanical ✗ (soft).
- **Archetyp B** teilt sich das Redesign mit DK Fenster — erlaubt (gleicher Archetyp, anderes Skelett auf allen 7 Achsen).
- **Paarungs-Check** (Kopf + Footer + Galerie): „Kein-Eyebrow + 3-Spalten-Bucket + Bento" existiert im Register nicht
  (Schlaf-T-Raum: Marginalie + 3-Sp + Bento · Oberflächentechnik: Kein-Eyebrow + Mega-Footer + Bento).
- **Abgrenzung zur Mutterseite `introtech-sanierung/`:** deren Skelett (Topbar+Drawer · eyebrow→h2→lead · Karten-Raster 3-gleich ·
  FAQ-Akkordeon · 3-Spalten+`<details>`) wird nicht übernommen; Karten-Raster hier nur in der bühnengeführten, größenvariierten Form.

---

## Bau-Auflagen (was NICHT / was ZWINGEND gebaut wird)
1. **Kopf:** genau ein Nav-Trigger („Menü"); keine Linkleiste in irgendeiner Breite; kein Drawer, keine Bottom-Bar, keine Servicezeile,
   keine Haarlinie als Kältekreis. Overlay auf allen Breiten identisch (`inert` + Fokusfalle + Esc + Scroll-Lock).
2. **Sektions-Kopf:** kein `eyebrow`-Element, keine Mono-Antwortzeile, kein Lead unter h2; Chip ≤ 3 Wörter, Pill, nicht Mono;
   h2 mit zwei Gewichten in einer Zeile; h2 in Aussageform außer FAQ-`<summary>` und Ratgeber-h1.
3. **Katalog:** keine Spec-Zeilen (`.set-zeile`), keine Vergleichs-/Ausweis-/Wartungstabellen als tragende Bauform; Tabellen/Listen
   höchstens innerhalb einer Karte. Alle 9 Sets als Karten mit Produkt-SVG auf Bühne + kW-Chip + Preis lt. Schalter; jede Karten-Sektion
   mit ≥ 2 Kachelgrößen oder Bild/Bühne.
4. **Kontakt:** keine gerundete OSM-Kachel mit Pin-Pille, kein Band, keine Karte als Spalte, kein Footer-Hintergrund, kein Umschalter;
   Karte ≥ 72 vh / ≥ 60 vh, Overlay-Kontaktkarte mit 6 Orte-Chips; Karte lazy.
5. **Footer:** ≥ 3 Spalten, dunkler Block, keine `<details>`, keine große Tel-CTA, kein Display-Claim, nicht einzeilig; Set-Index Pflicht.
6. **Galerie:** Bento mit genau den 5 Raumkacheln, 3 Größen; keine Masonry, kein Slider, keine Lightbox, keine Bild-Bänder als Trenner;
   Kacheln funktional (Rechner-Vorwahl nachweisbar); Caption „Einbausituation", nie „Referenz".
7. **Spine index** exakt in der deklarierten Reihenfolge (12 Blöcke, feste `id`s); kein Vertrauensband, keine „Zwei Wege"-Sektion.
8. **Wege-Schalter** an allen sechs Einbauorten, ein Zustand, Preise folgen überall; Standard „Einbauen lassen".
9. **Keine erfundenen Fakten:** Nachweise nur dena + TÜV Rheinland; „Bestseller" nur für die 2 im Katalog markierten Sets; keine
   Kundenstimmen, Projektzahlen, Sterne, „seit"-Angaben; Preise nur aus `kt38_katalog.py`; Demo-Kennzeichnung über `META["demo"]`.
10. **Rechner** nur in der Bauform „Bühne mit Eingabe-Karte + Ergebnis-Produktkarte" (Logik/Verbote s. o.).
11. **Unterseiten:** 10 Kopf-Typen, keine Familie mit dem Kopf einer anderen; Leistungsseiten mit 5 verschiedenen Kopf-Slots;
    `.kopf-*`-Klassen des Erstbaus nicht wiederverwenden.
12. **Pflicht `.wa-fab`** (rund, Dauerpuls, Referenz `kfz-mattes/`) — tritt vor Preis-Doppel, Formular und Unterleiste zurück
    (IntersectionObserver, Memory `wa-fab-tritt-zurueck`).
13. Overlay-Öffnen, Karten-Hover, Bühnen-Skalierung nur `transform`/`opacity`/`clip-path`, `prefers-reduced-motion` respektiert
    (Motion-Persona lt. Brief, nicht Teil dieser Achse).

---

## Prüfauftrag für den `struktur-divergenz-reviewer` (Phase 8)
1. **Nav:** In 5 Testbreiten (360 · 768 · 1024 · 1280 · 1600) enthält der Kopf außer Wortmarke, „Menü", Telefon, CTA keinen Link;
   das Overlay ist in allen Breiten dieselbe Fläche (kein Drawer-Variante), enthält 4 Bild-Kacheln + Set-Liste mit Preisen + Schalter.
2. **Unterleiste:** nur auf `set-*.html`, dockt oben an, enthält keine Site-Links — auf keiner anderen Seite eine fixe Leiste.
3. **Sektions-Kopf:** kein Element mit Strich+Versalien über einer h2; h2 zeigt zwei Gewichte; Chips ≤ 3 Wörter, nicht Mono;
   auf index/shop/Kategorie/Set keine h2 mit „?"; keine Antwortzeile unter h2; kein `<p>`-Lead direkt nach einer h2.
4. **Komponenten:** ≥ 50 % der inhaltstragenden Sektionen auf index und shop werden von Bild-/Bühnen-Karten getragen; keine Sektion
   mit drei gleich großen textbasierten Karten; kein `.set-zeile`-Äquivalent; Tabellen nur innerhalb von Karten.
5. **Kontakt:** Sektion mit Karte ≥ 72 vh Desktop, Overlay-Karte darüber, 6 Orte-Chips; getrennt vom Footer (eigenes `<section>`, Footer
   ohne Karte dahinter).
6. **Footer:** ≥ 3 Spalten, Set-Index vorhanden, kein `<details>`, größtes Text-Element = Spaltenüberschrift, keine Tel-CTA-Pille.
7. **Bento:** 5 Kacheln, 3 Größen; Klick auf „Dachgeschoss" setzt im Rechner die Raumsituation „Dachgeschoss" (Vorwahl nachweisbar);
   Captions ohne „Referenz".
8. **Spine:** `section`-Reihenfolge auf index = deklarierte 12 Blöcke; Rechner auf Pos. 3; kein Vertrauensband, keine Wege-Sektion.
9. **Kopf-Typen:** 10 verschiedene Seitenkopf-Bausteine nachweisbar (Klassen benennen); Leistungsseiten mit 5 unterschiedlichen Slots;
   keine `.kopf-*`-Klasse des Erstbaus.
10. **Schalter:** Umschalten im Hero ändert Preise in Bestseller-Reihe, Overlay-Set-Liste und (nach Navigation) auf Set-Seiten; Kontaktformular
    zeigt das vorgewählte Thema.
11. **Gegenpol-Check:** nichts aus `.tools/kt38_inhalt/_alt_erstbau/struktur-blueprint-2026-09-10.md` ist zurückgekehrt (Mega-Menü, Mono-Antwortzeile, Spec-Zeilen,
    Karte-Band, Kontaktband-Footer, Strichzeichnungen, grüner Energie-Strang, Kältekreis-Linie).
12. Divergenz-Rechnung gegen Erstbau / DK Fenster / MAVA nachrechnen (Soll: 6/6 · 6/6 · 6/6; Spine ≠ alle 3; Nav & Kontakt ≠ Erstbau).

---

## Register-Struktur-Notiz (für Phase 8.5, nach BESTANDEN eintragen)
| KlimaTech38 (InTroTech) — Redesign 2026-09-12 | **Overlay-Fullscreen-Menü** („Schaufenster": Kapsel-Kopf mit Wortmarke · Menü · Tel · CTA; Overlay = 4 Bild-Kacheln je Strang + Set-Liste mit Preis lt. Schalter + Kontaktzeile, auf allen Breiten identisch; Set-Seiten mit oben andockender Produkt-Unterleiste) | **Kein-Eyebrow**: große h2 mit 2 Gewichten in einer Zeile + Kennwert-Chip (≤ 3 Wörter, Pill), h2 in Aussageform | **Karten-Raster, bühnengeführt in variierten Größen** (Foto-Situation oder Produkt-SVG auf Bühne + kW-Chip + Preis lt. Schalter) + Vollbild-Kapitel (Montage, Energie, Leistungs-Köpfe); Step-Strecke und FAQ-Akkordeon nur als Unter-Elemente | **Vollbild-Karte** (Einzugsgebiet regional, ≥ 72 vh) + Overlay-Kontaktkarte mit 6 Orte-Chips; kontakt.html steigt über die Karte ein | **mehrspaltig 4 Sp., dunkler Block** (InTroTech-Logo + Sparten-Erklärung · Set-Index · Beratung & Wissen · Kontakt kurz · Legal-Zeile), ohne `<details>`, kein Claim, keine Tel-CTA | **Bento-Grid „Einbausituationen"** (5 Räume, 3 Größen, jede Kachel = Rechner-Vorwahl) | Hero(VB-Foto+Schalter+Preisanker)→Räume(Bento)→Rechner(Bühne)→Bestseller(2+Treffer)→Kategorien(4 Bild-Kacheln)→Montage(VB-Kapitel+Strecke 1–5)→Energie(VB-Kapitel+3 Karten)→PV(1 Split-Block)→Wissen(4 Ratgeber+FAQ-Karte)→Mit wem(Logo-Band)→Kontakt(VB-Karte)→Footer(4-Sp) · **10 Kopf-Typen** über 29 Seiten (Hero · Katalog · Bühne · Produkt · Kapitel[5 Slots] · Index · Artikel · Fragen · Karte-zuerst · Recht) |

**Nach diesem Build für die nächsten 2 Builds zu sperren (Vorschlag für Phase 8.5):** Overlay-Fullscreen-Menü · Kein-Eyebrow + Chip ·
Karten-Raster (auch bühnengeführt) · Vollbild-Karte · mehrspaltiger Footer (3-Spalten-Bucket) · Bento-Grid · Motion soft.

---

## Annahmen (bitte im Bau bestätigen oder korrigieren)
1. Schalter-Standard „Einbauen lassen" (Conversion-Primärziel Beratung/Montage). Alternative „Selbst einbauen" ändert nur den Startzustand.
2. Frage-h2 der Leistungsseiten werden in Aussageform gesetzt (Fließtext 1:1) — nötig, weil „Frage-Headline" gesperrt ist.
3. Bento nutzt die vorhandenen `assets/raum-*.jpg`; Energie-Kapitel `sonne-vorhang.jpg`, PV-Block `pv-dach.jpg`.
4. Die 3 Energie-Leistungen sind aus den vorhandenen h2 der Seite abgeleitet (Ausweis · Wärmeverlust-Aufnahme · Sanierungsplan) — keine neuen Leistungen.
5. Bestseller-Reihe = 2 markierte Sets + 1 Treffer-Karte (der Katalog markiert nur 2 Bestseller; ein drittes „Bestseller" wäre erfunden).
6. Bento → Rechner → Bestseller-Reihenfolge weicht bewusst vom Brief-Vorschlag ab (Trichter-Logik, s. Achse 7).
