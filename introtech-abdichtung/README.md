# InTroTech Bauwerksabdichtung — Demo-Website (2026-09-16)

Statische Website (HTML/CSS/JS, kein Build) für die **neue Sparte Bauwerksabdichtung der InTroTech GmbH**
(Gifhorn) — dritte Seite der Familie nach `introtech-sanierung/` und `klimatech38/`. Modus **Demo**: die Marke
ist echt (Logo, Farben, Kontakt- und Registerdaten 1:1 von introtech.de), das Leistungs-Portfolio ist eine
fachübliche **Demo-Annahme**, die der Betrieb bestätigen muss (siehe „Vor Live klären").

## Konzept: „Wo kommt das Wasser her?"
Der Hausbesitzer kennt keine Verfahrensnamen, aber er weiß, **wo** es feucht ist. Deshalb navigiert die Seite
über einen **Diagnose-Schnitt**: ein flächig illustrierter Hausschnitt (Terrasse → Sockel → Kellerwand →
Bodenplatte → Grundwasser) mit sieben nummerierten Stellen. Hover/Fokus zeigt den Wasserweg (Sky-Blau) und
die Abdichtung (Aktionsblau), Klick springt zum Kapitel. Die Nummern des Schnitts **sind** die Kapitelnummern;
jede Leistungsseite trägt denselben Schnitt klein mit der aktiven Stelle. Das Logo (Haus + Tropfen) wird so zum
Prinzip der Seite.

Kreativ-Brief: `assets/art-direction.md` · Struktur-Blueprint: `assets/struktur-blueprint.md`.

## Aufbau — 11 Seiten, 4 Kopf-Typen
```
index.html                                   Hero (h1 + vollbreiter Schnitt + Legende)
                                             → 01–07 Stellen als Befund-Kapitel (Zeichnungs-Band · Erkennen · Symbolfoto · Link)
                                             → 08 Ablauf · 09 Aus einer Hand (Verbund-Kette) · 10 Kontakt & Einzugsgebiet
balkon-terrasse-flachdach.html           01  Stellen-Kopf (Schnitt-Leiste) → Befund → Verfahren (dl) → Grenzen → Verwandte → Abschluss
sockelabdichtung.html                    02
lichtschacht-kellerfenster-rohrdurchfuehrung.html 03
rissinjektion.html                       04
kelleraussenabdichtung.html              05
innenabdichtung-horizontalsperre.html    06
bodenplatte-wand-sohle-fuge.html         07
kontakt.html                                 Anruf zuerst → Formular mit Stellen-Auswahl (?stelle=NN wählt vor) → Gebiet → Anschrift
impressum.html · datenschutz.html            Lesespalte
```
Navigation bewusst **minimal** (Logo + Sparte · ein Anruf-Button), keine Linkleiste, kein Burger: der Schnitt, die
Legende, die Schnitt-Leiste der Leistungsseiten und der Stellen-Index im Footer erschließen alle Seiten.
Die Startseiten-Kapitel zeigen nur „Woran Sie es erkennen“ (Diagnose); „Was wir tun“ steht auf der Leistungsseite.
Kontakt ohne Karte („Wir kommen zu Ihnen") — Adresse, Route-Link, Einzugsgebiet ausgeschrieben.

## Werkzeuge — nichts von Hand pflegen
```
python3 .tools/bwa_gen.py            # alle 11 Seiten + sitemap.xml + robots.txt aus EINER Quelle (Texte, Stellen, SVG-Schnitt)
python3 .tools/site_check.py introtech-abdichtung
cd introtech-abdichtung && python3 -m http.server 8793      # Fonts laden nicht über file://
node .tools/shot_bwa.mjs [seiten] [breiten] [--fold]        # Screenshots · shot_bwa_el.mjs <seite> <breite> <selectoren>
node .tools/bwa_sweep.mjs            # 11 Seiten × 17 Breiten: Overflow + JS-Fehler
node .tools/bwa_func.mjs             # Funktionstest: Hover-Zonen, Tastatur, ?stelle=, FAB-Rücktritt, Fremd-Hosts, Reduced Motion
```
`DEMO = True` in `bwa_gen.py` → `noindex, nofollow` + `robots.txt` Disallow (Sparten-Name/Domain offen).
Vor dem echten Livegang `DEMO = False`, `DOMAIN` setzen, neu generieren.

## Design (aus der Marke abgeleitet)
- **Brand-Anker:** Anthrazit #4D4D4D + Sky-Blau #A1C8EB aus dem echten InTroTech-Logo → Aktionsblau #1668AE
  (identisch zu KlimaTech38). Farbe ist Bedeutung: Aktionsblau = Abdichtungsschicht, Sky-Blau = Wasser.
- **Welt W4 Klinisch-Klar** („Trockenraum"): hell, viel Luft, ruhig. Archetyp C (schmale Lesespalte 62ch,
  vollbreiter Schnitt). Motion `mechanical` (kurz, knapp; Schnitt zeichnet sich beim Laden; kein Lenis).
- **Schrift:** Fira Sans 300/400/500/600, lokal in `assets/fonts/` (SIL OFL) — eine Familie, Gewichtskontrast als Idee.
- **Tokens:** Spacing 1.618 · Radius 6 px · Linie 1 px · kein Schatten · Container 1040 · Type-Ratio 1.2.
- Icons: eigene SVG-Linien-Icons (1.5 px). Keine Emojis, keine Fake-Zahlen, keine Testimonials.

## Bilder
Sieben **Symbolfotos** (Pexels, lizenzfrei, Nachweise `assets/_attribution.txt`), alle auf eine kühl-neutrale
Gradierung gezogen und **als Symbolfoto beschriftet** — die Sparte hat noch keine eigenen Referenzfotos.
Schnitt und Detail-Bänder sind eigene SVG-Illustrationen (in `bwa_gen.py`, eine Definition, per `<use>` und
CSS-Variablen `--z01…--z07` je Stelle geschaltet). `assets/og.png` (1200×630) für Social-Vorschauen.

## Cookies & Datenschutz beim Livegang
Gemessen (`bwa_func.mjs`): **0 Cookies, 0 localStorage/sessionStorage, keine Fremd-Hosts** — Fonts, GSAP und
Motion-Engine liegen lokal, keine Karte, kein Tracking. WhatsApp/Route/introtech.de sind reine Links (öffnen
erst bei Klick). → **Kein Cookie-Banner nötig.** Datenschutzerklärung nennt Vercel als Host; bei anderem
Hoster Abschnitt 3 anpassen. Formular ist `mailto:` (öffnet das Mailprogramm, speichert nichts serverseitig).

## ⚠️ Vor Live klären (Demo-Annahmen, nicht erfinden)
1. **Sparten-Name und Domain** — Arbeitsstand „InTroTech Bauwerksabdichtung"; bei eigenem Namen (analog
   KlimaTech38) `SPARTE`/`DOMAIN` in `bwa_gen.py` setzen, ggf. Wortmarke ergänzen.
2. **Leistungs-Portfolio bestätigen:** Welche der 7 Stellen/Verfahren bietet der Betrieb wirklich an
   (Kelleraußenabdichtung mit Aufgraben? Injektionen? Balkon/Flachdach?). Nicht angebotene Stellen aus `STELLEN` entfernen.
3. **Regelwerk-Verweise prüfen:** DIN 18531 (Balkon/Terrasse/Dach), DIN 18533 (erdberührt), WTA 4-6/4-10
   (Innenabdichtung/Injektion) — Formulierungen mit dem Betrieb abstimmen.
4. **Service-Zusagen im Ablauf:** schriftliches Konzept, Dokumentation mit Fotos der verdeckten Schichten,
   Übergabe an die Leckageortung — bestätigen lassen.
5. **Referenzen/Arbeitsproben** (C2-Pflicht): sobald erste Projekte vorliegen, echte Fotos statt Symbolfotos
   (Phase 10 Individualisierung); dann auch Vorher/Nachher je Stelle möglich.
6. **Formular-Postfach:** `mailto:info@introtech.de` — oder Formular-Endpoint anbinden.
7. **KlimaTech38-Link** zeigt auf die Vorschau (klimatech38.vercel.app) → nach Domain-Umstellung auf klimatech38.de.
8. Öffnungszeiten Mo–Fr 08–18 von introtech.de übernommen — für die Sparte bestätigen.
9. **Versicherungsabwicklung:** introtech.de nennt sie für die Sanierung („inklusive“). Ob sie auch für Abdichtungs-
   aufträge gilt, ist offen — bis dahin steht hier nur „Dokumentation, wichtig für die Versicherung“.

## QA (2026-09-16)
`site_check.py` 0 FAIL / 0 WARN · `impeccable detect` nur `numbered-section-markers` (unsere Struktur-Achse),
`cramped-padding` (Sektion mit innenliegendem `.wrap`, bekannter Fehlalarm) und `flat-type-hierarchy` auf
Rechts-/Kontaktseite (statische Analyse ohne `clamp()`) · Sweep 11 × 17 Breiten ohne Overflow/JS-Fehler ·
Funktionstest bestanden (Hover/Fokus/Tastatur, `?stelle=`, FAB-Rücktritt, Reduced Motion, 0 Cookies/0 Fremd-Hosts) ·
**4-Agenten-Panel 4/4 BESTANDEN**: struktur-divergenz (Runde 2) · anti-ai (Runde 2) · web-design (Runde 5) ·
ui-layout (Runde 5). Alle Befunde der Zwischenrunden sind umgesetzt (siehe `assets/art-direction.md`, „QA-Runde 1“);
Kern-Lehren: `<use>`-Instanzen nur über CSS-Variablen steuern und Kaskaden-Reihenfolge prüfen, SVG-Marker
nicht als Gruppe skalieren (unsichtbares Label verschiebt den Ursprung), kein `inline-flex` auf Textlinks mit
gemischten Knoten, Pexels-Motive gegen Land/Kontext prüfen.
