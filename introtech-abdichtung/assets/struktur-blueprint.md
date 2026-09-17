# Struktur-Blueprint — InTroTech Bauwerksabdichtung (2026-09-16)

Bau-Vertrag aus Phase 1.6 (`struktur-architekt`). Archetyp C · Welt W4 · Motion mechanical · Signature Diagnose-Schnitt.
Vergleichshorizont: Bauschulz (09-14) · KT38-Redesign (09-12) · KT38-Erstbau (09-10) · DK Fenster (09-05) · MAVA (08-13).
Aktive Sperren (Bauschulz + KT38-Redesign) werden nicht berührt.

## Die 7 Achsen

| Achse | Festlegung | Content-Kopplung |
|---|---|---|
| **1 Nav** | **Minimal** — Kopf: Logo + Sparten-Text links, EIN Outline-Anruf-Button `tel:` rechts (kein Tel-Textlink, kein CTA-Paar). Keine Linkleiste, kein Burger, kein Drawer, in keiner Breite. Kopf **statisch** (scrollt weg). Navigation = **der Schnitt selbst** (Marker → `#stelle-0X`, Legende = Sprungliste) + auf Leistungsseiten die **Schnitt-Leiste im Seitenkopf** (nicht sticky). Einziges Schwebe-Element: `.wa-fab`. | Der Hausbesitzer navigiert über „wo ist es feucht", nicht über Verfahrensnamen. |
| **2 Sektions-Kopf** | **Nummern-Kapitel als Marker-Nummer**: derselbe runde Marker wie im Schnitt (`<use>`), 01–07 gefüllt (= Stelle am Haus), 08–10 als Ring (kein Bauteil). Darunter h2 = Bauteil (600) + Ort-Zeile (300, klein). Kein Eyebrow, kein Lead, keine Frage. | Die Marker sind bereits das Ordnungssystem der Seite. |
| **3 Komponenten** | **Fließtext-Editorial als „Befund-Kapitel"**: Zeichnungs-Band (Schnitt-Ausschnitt an genau dieser Stelle, 1040 × ~240 px, flächig) → Lesespalte 62ch mit Symptom-Foto (float, abwechselnd rechts/links) + gelabeltem Absatz **„Woran Sie es erkennen"** → Link „Was wir an Stelle 0X tun"; **„Was wir tun" steht nur auf der Leistungsseite** (Startseite = Diagnose, Unterseite = Verfahren). **Neben-Bauform: Step-Ablauf** (08: 4 Schritte vertikal ohne Linie; 09: Verbund-Kette 4 Glieder). Leistungsseiten: Verfahren als `dl`. | Ein Gutachten erklärt so: Schnitt, dann Befund. Split-Reihen (DK Fenster, 5×) und Vollbild-Kapitel (7×100 vh gegen C) verworfen. |
| **4 Kontakt** | **Keine Karte — anrufgeführt**: Tel als größtes Element + Zeiten → Formular mit Fieldset „Wo ist es feucht?" (7 Checkboxen mit Marker-Nummern) + Name/Tel/PLZ-Ort/Nachricht → Einzugsgebiet als ausgeschriebene Ortszeile → Anschrift + Route-Link (textuell). KEIN Kanal-Umschalter, kein vorbelegter WA-Text (sonst „interaktiv"). `kontakt.html?stelle=05` darf nur die Checkbox vorwählen. | Betrieb ohne Ladengeschäft: „Wir kommen zu Ihnen". Null Drittanfragen. |
| **5 Footer** | **Einzeilig minimal als „Fundament-Zeile"**: dunkles Band #1E2A36, zwei gestapelte Zeilen ohne Spalten/Claim/`<details>`: A = Stellen-Index 01–07 + Kontakt; B = Logo weiß + Sparte · Anschrift · Tel · Zeiten · introtech.de · Impressum · Datenschutz. Auf allen Seiten identisch. | Minimal-Nav hat keine Linkleiste → der Stellen-Index ist der SEO-Leistungsindex. |
| **6 Galerie** | **Keine Galerie.** Fotos nur funktional (7 kleine Symptom-Fotos in den Kapiteln, auf Leistungsseiten größer), kein Slider, keine Bänder. | Sparte neu, keine eigenen Referenzen — jede Galerie wäre Stock-Hülle. 5. Vergabe, begründet. |
| **7 Spine** | siehe unten | Wasserweg von oben nach unten — die Seite steigt beim Scrollen ins Erdreich. |

## Sektions-Spine (index.html)
```
Hero(h1 + Ortszeile + Tel · vollbreiter Diagnose-Schnitt · Legende 01–07 als Sprungliste)
→ 01 Balkon, Terrasse & Flachdach(Befund-Kapitel)
→ 02 Sockel & Spritzwasser(Befund-Kapitel)
→ 03 Lichtschächte, Kellerfenster & Rohrdurchführungen(Befund-Kapitel)
→ 04 Risse(Befund-Kapitel)
→ 05 Kellerwand außen(Befund-Kapitel)
→ 06 Kellerwand innen & Horizontalsperre(Befund-Kapitel)
→ 07 Bodenplatte & Wand-Sohle-Fuge(Befund-Kapitel)
→ 08 Warum schnelles Handeln(Intro + 3 Risiken der Originalseite als Punkte-Liste)
→ 09 Vier Schritte(Steps 4 vertikal ohne Linie, Wortlaut Originalseite)
→ 10 Ihre Vorteile(4 Punkte der Originalseite + Verbund-Kette; nachgetragen 2026-09-17 nach Abgleich mit introtech.de/bauwerksabdichtung)
→ 11 Kontakt & Einzugsgebiet(keine Karte, anrufgeführt + Original-CTA-Text + Bauteil-Formular + Ortszeile)
→ Fundament-Footer(einzeilig, 2 Zeilen) + .wa-fab
```
Mobil ≤ 640: Schnitt bleibt vollbreit quer, Marker-Hitbox ≥ 44 px, Legende darunter = primäre Sprungliste.

## Divergenz-Nachweis
- Spine ≠ letzte 3 ✓ (auch ≠ Schwester introtech-sanierung: Topbar+Drawer · eyebrow · OSM-iframe · 3-Sp-Footer).
- Nav & Kontakt ≠ Bauschulz (Topbar+Drawer / Karte als Spalte) ✓.
- Diskrete Achsen: vs. Bauschulz 6/6 · vs. KT38-Redesign 6/6 · vs. KT38-Erstbau 5/6 · vs. DK Fenster 5/6.
- Bewusst notierte Wiederholungen: einzeilig minimal (6. Vergabe, einziges freies Menü), keine Galerie (5., begründet).

## Unterseiten — 4 Kopf-Typen (kein Einheits-Typenblatt)
| Kopf-Typ | Seiten | Aufbau |
|---|---|---|
| `hero` | index | h1 (300/600-Zweiteilung) + Ortszeile + Tel → vollbreiter Schnitt → Legende |
| `stellen-kopf` | 7 Leistungsseiten | Schnitt-Leiste (ganzer Schnitt klein, aktive Stelle gefüllt, übrige gedimmt aber klickbar; Textlinks ← vor / zurück → · „Alle Stellen" → `index.html#schnitt`; nicht sticky) → Marker + h1 + Befund-Satz + Tel-Link |
| `anruf-kopf` | kontakt | h1 + Tel als größtes Element + Zeiten → Formular (Fieldset vorwählbar per `?stelle=`) → Ortszeile → Anschrift |
| `lese` | impressum, datenschutz | Lesespalte 62ch, nur h1 |

Körper Leistungsseite: `stellen-kopf` → Befund & Ursache (Zeichnungs-Band groß + gerahmtes Symptom-Foto) → Verfahren als `dl` (Verfahren · wann · Material) → „Wann das nicht reicht" (Grenz-Absatz) → Verwandte Stellen (2–3 Nachbar-Marker) → Kontakt-Abschluss in der Lesespalte (Tel groß + „Besichtigung anfragen — Stelle 0X vorgemerkt") → Fundament-Footer.

Slugs: `balkon-terrasse-flachdach.html` · `sockelabdichtung.html` · `lichtschacht-kellerfenster-rohrdurchfuehrung.html` · `rissinjektion.html` · `kelleraussenabdichtung.html` · `innenabdichtung-horizontalsperre.html` · `bodenplatte-wand-sohle-fuge.html`.

## Hinweise an den Bau
- Regelwerk: DIN 18533 (erdberührt: 02, 03 außen, 05, 07) · DIN 18531 (01 Balkon/Terrasse/Flachdach) · WTA 4-6 / 4-10 (06, teils 04). Im Ablauf „nach geltendem Regelwerk (DIN 18531/18533, WTA)"; README: bestätigen lassen.
- TÜV-Zertifizierung nur als Text der Mutterfirma in 09 (belegt: introtech.de), kein Siegel-Bild.
- Motion: Zeichnungs-Band zeichnet sich (stroke/clip-path), Text kommt `up`.
- `.wa-fab` wie KT38 (gleiche Firma), Rücktritt über Tel-Links/Formular.

## Register-Struktur-Notiz (nach QA eintragen)
| InTroTech Bauwerksabdichtung (2026-09-16) | **Minimal** (Logo+Sparte · Tel-Textlink · 1 CTA; Kopf statisch, kein Burger/Drawer in keiner Breite; Navigation = Diagnose-Schnitt mit Marker-Sprüngen + Legende, Leistungsseiten mit nicht-klebender Schnitt-Leiste im Kopf) + `.wa-fab` | **Nummern-Kapitel als Marker-Nummer** (Schnitt-Marker per `<use>`: 01–07 gefüllt = Stelle am Haus, 08–10 Ring; h2 = Bauteil + Ort-Zeile; 0× eyebrow, 0× lead) | **Fließtext-Editorial „Befund-Kapitel"** (Zeichnungs-Band = Schnitt-Ausschnitt 1040 → Lesespalte 62ch mit Absätzen „Erkennen"/„Tun" → 1 kleines gerahmtes Symptom-Foto) (+ Step-Ablauf 4 vertikal ohne Linie, Verbund-Kette 4 Glieder, `dl`-Verfahrenslisten auf Leistungsseiten) | **keine Karte — anrufgeführt** (Tel groß + Zeiten → Formular mit Bauteil-Fieldset 01–07 → Einzugsgebiet als Ortszeile → Anschrift/Route-Link; kein Kanal-Umschalter) | **einzeilig minimal „Fundament-Zeile"** (dunkles Erdreich-Band, 2 gestapelte Zeilen: Stellen-Index 01–07 / Logo·Anschrift·Tel·Legal; keine Spalten, kein Claim, kein `<details>`) | **keine Galerie** (Sparte neu, keine Referenzen; 7 Symptom-Fotos nur funktional in den Kapiteln, als Symbolfoto beschriftet) | Hero(h1+vollbreiter Schnitt+Legende)→01–07 Stellen(Befund-Kapitel, oben→unten)→08 Ablauf(Steps)→09 Aus einer Hand(Kette)→10 Kontakt&Einzugsgebiet(keine Karte)→Fundament-Footer · **4 Kopf-Typen** über 11 Seiten: `hero` · `stellen-kopf` (7×) · `anruf-kopf` · `lese` |

> **Für die nächsten 2 Builds sperren (Stand Abdichtung):** Minimal-Nav · Nummern-Kapitel · Fließtext-Editorial · keine Karte (5. Vergabe) · einzeilig minimaler Footer (6. Vergabe — Bucket hart zu) · keine Galerie (5. Vergabe) · Archetyp C · Motion mechanical (3. Vergabe) · Welt W4.
