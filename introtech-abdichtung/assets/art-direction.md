# Kreativ-Brief — InTroTech Bauwerksabdichtung (Demo, 2026-09-16)

**Anlass:** Dritte Seite der InTroTech-Familie (nach `introtech-sanierung/` und `klimatech38/`) für die
neue Sparte **Bauwerksabdichtung**. Die Sparte ist neu — Name/Domain sind noch offen (Arbeitsstand:
„InTroTech Bauwerksabdichtung", analog zur Sparten-Logik von KlimaTech38). Die Marke ist nicht neu:
Logo, Farben, Ton, Kontakt- und Registerdaten kommen 1:1 von introtech.de.

**Lehre aus KlimaTech38 (2026-09-12):** Der Auftraggeber hat den kargen Haarlinien-/Datenblatt-Look
abgelehnt. Diese Seite ist deshalb **hell, ruhig und großzügig (W4)**, aber **flächig illustriert und
fotografisch gestützt** — keine Strichzeichnungen als Skelett, keine Mono-Labels, kein Hairline-Raster.

```
BRAND-ANKER (verankert, nicht verhandelbar)
  Farben      : Anthrazit #4D4D4D + Sky-Blau #A1C8EB aus dem echten InTroTech-Logo (Haus + Tropfen).
                Aktion/Links: Aktionsblau #1668AE (AA-Ableitung, identisch zu KlimaTech38 → Familie).
                Ink/Text: #2B2F33. Grund: Weiß #FFFFFF + Kühl-Grau #F5F7F9.
                NEU ist die ANWENDUNG: das Aktionsblau IST in jeder Zeichnung die Abdichtungsschicht
                (die eine dicke blaue Linie am Bauteil), Sky-Blau ist das Wasser (Grundwasser, Sicker-
                wasser, Spritzwasser). Farbe ist also Bedeutung, nicht Dekoration. EIN Akzent.
  Logo/Name   : echtes InTroTech-Logo (assets/brand/logo.png, ohne Tagline-Zeile) + Sparten-Zusatz
                „Bauwerksabdichtung" als gesetzter Text. Kein erfundener Markenname.
  Ton/Claim   : sachlich, erklärend, ohne Superlative — „Innovation trifft Verantwortung",
                „Gebäude schützen, Werte erhalten" (introtech.de). Kunde wird geduzt? Nein: Sie.
  Foto-Anmutung: Original hat keine Abdichtungs-Fotos → Pexels-Lückenfüller, alle auf EINE kühle,
                neutrale Gradierung (Grau/Blau, kein Warmstich); Baustelle/Bauteil statt Helm-Model.

NISCHE        : C2 Handwerk & Bau (Sanierung) · Conversion primär: Besichtigung anfragen
                (Anruf 05371 8759972 > Formular); kein „24/7" auf dieser Seite (Notdienst gehört zur
                Leckageortung der Mutterfirma, wird dort verlinkt, hier nicht behauptet).
KONZEPT       : „Wo kommt das Wasser her?" — Die Seite denkt wie der Kunde, nicht wie der Katalog:
                Der Hausbesitzer kennt keine Verfahrensnamen, aber er weiß, WO es feucht ist. Ein
                Schnitt durchs Haus zeigt die sieben Stellen, an denen Wasser eindringt — jede Stelle
                führt zum passenden Verfahren. Das Logo (Haus + Tropfen) wird zum Prinzip der Seite.
WELT          : W4 Klinisch-Klar, Lesart „Trockenraum": hell, sehr viel Luft, kühles Neutral, EIN
                gedämpfter Akzent, ruhige Linien-Icons. Begründung: Abdichtung verkauft Ruhe und
                Trockenheit — die Seite fühlt sich an wie ein trockener, aufgeräumter Keller.
                Illustrationen sind FLÄCHIG getönt (Erdreich, Wasser, Wand als Flächen), nicht Hairline.
SIGNATURE     : **Der Diagnose-Schnitt** — ein flächig illustrierter Hausschnitt (Erdgeschoss-Ausschnitt → Sockel →
                Kellerwand → Bodenplatte → Grundwasser; im Hero ohne Dach, damit alle Marker im Fold liegen) mit sieben nummerierten Stellen ①–⑦. Hover/
                Fokus hebt die Stelle hervor (Wasserweg in Sky-Blau, Abdichtung in Aktionsblau), Klick
                springt zum Kapitel; die Nummern des Schnitts SIND die Kapitelnummern der Seite; auf
                jeder Leistungsseite steht derselbe Schnitt klein mit der aktiven Stelle. „Die Seite,
                auf der man aufs Haus klickt, wo es feucht ist."
MOTION        : mechanical (→ data-motion="mechanical"): knapp, linear, kurze Wege; Reveals nur
                up/left/right (Zeile kommt von der Seite ihres Bildes); Schnitt: Wasser-/Abdichtungs-
                pfade zeichnen sich beim Laden (stroke-dashoffset, power2.out), Marker ticken nach-
                einander ein. Kein Lenis (nativ scrollen). Hover-Bewegung nur hinter hover:hover.
TYPO-BEGRÜNDUNG: EINE Familie, Gewichtskontrast als Idee — **Fira Sans** (Spiekermann; humanistisch,
                technisch-deutsch, echte Tabellenziffern): Display 300 (leicht, groß, ruhig — „Plan-
                Beschriftung"), Text 400, Labels 600 Versalien gesperrt (.08em), Kapitelnummern 300
                tabular. Neu im Register. Entscheidungen: h1/h2 mischen 300 + 600 in EINER Zeile
                (nur bei echter Zweiteilung), Lesespalte ≤ 62ch, clamp()-Kette Ratio 1.2, Ziffern
                tabular-nums für Telefon/Nummern/Maße.
FARB-BEGRÜNDUNG: Grund Weiß + Kühl-Grau im Wechsel; Zeichnungs-Bühnen Sky #A1C8EB→#EAF2F9 (Wasser
                unten, Himmel oben); Erdreich als kühles Grau #D5DAE0 mit feiner Schraffur; Wand
                #EEF1F4; Abdichtung = Aktionsblau #1668AE (auch CTA); Text Ink #2B2F33; dunkler
                Fundament-Footer #1E2A36 (Erdreich unter der Bodenplatte).
BANDBREITE    : 2 (ruhig, seriös — der Schnitt trägt die Aufmerksamkeit, alles andere tritt zurück).
```

## Struktur-Tokens (Phase 2, verbindlich)
| Token | Wert | Bauschulz (letzter Build) | KT38-Redesign |
|---|---|---|---|
| Spacing-Ratio | **1.618×** | 1.5× | 1.618× |
| `--radius` | **6 px** (Buttons/Karten/Bild), Marker rund | 3 px | 20 px + pill |
| `--line-weight` | **1 px** (Trennlinien), Zeichnung 1.5–2 px flächig | 2 px | 1 px in Karten |
| `--shadow` | **none** (flach; Tiefe nur über Flächenton) | Kante 0 2px 0 | weich-kühl 2 Lagen |
| `--container` | **1040** schmal (Lesespalte 62ch) + vollbreiter Schnitt | 1160 | 1280 + Bühnen |
| `--type-ratio` | **1.2** ruhig (h1 per eigener clamp-Kurve groß) | 1.25 | 1.333 |

## Divergenz-Vorprüfung (gegen Register: Bauschulz 2026-09-14 · KT38-Redesign 2026-09-12 · KT38-Erstbau 2026-09-10)
| Achse | Bauschulz | KT38-Redesign | KT38-Erstbau | **Abdichtung** |
|---|---|---|---|---|
| Welt | W3 Warm-Handwerklich | W5 hell | W2 Swiss | **W4 Klinisch-Klar** |
| Archetyp | A Split + gepinnte Bühne | B/Showcase | C zentriert | **C Zentriert-Minimal, Plan-Lesart** (schmale Spalte, vollbreiter Schnitt) |
| Font-Klasse | Condensed-Signage-Superfamilie | Geometric-Display + Grotesk | Grotesk + Grotesk + Mono | **Ein-Familien Humanist-Sans, Gewichtskontrast 300/600** |
| Motion | editorial | soft | mechanical | **mechanical** |
| Signature | Bautagebuch von oben | Wege-Schalter | Kältekreis-Linie | **Diagnose-Schnitt** |
| Token-Sprache | 1.5 / 3 / Kante / 1160 / 1.25 | 1.618 / 20+pill / weich / 1280 / 1.333 | 1.25 / 0 / none / 1180 / 1.2 | **1.618 / 6 / none / 1040 / 1.2** |
→ gegen Bauschulz 6/6, gegen KT38-Redesign 5/6 (Spacing gleich), gegen KT38-Erstbau 4/6 (Archetyp C
und Motion mechanical wiederholen sich — beide liegen 3 Builds zurück; Welt/Font/Signature/Token anders).

## Bildwelt (Phase 7)
Sparte neu, keine eigenen Fotos → Pexels als Lückenfüller, kühl-neutral gradiert, Nachweise in
`assets/_attribution.txt`. Motive: Baugrube am Bestandshaus (Kelleraußenabdichtung), Drainagerohr im
Kiesbett, Riss mit abplatzendem Putz, feuchter Sockel innen, Bodenplatte/Bewehrung, Lichtschacht/
Kellerfenster, Balkon/Terrasse. Keine Helm-Stock-Models, keine fremden Herstellerkennzeichen (retuschieren).
Der Schnitt und alle Bauteil-Details sind eigene SVG-Illustrationen (flächig, aus `.tools/bwa_gen.py`).

## QA-Runde 1 (2026-09-16) — was sich geändert hat
Kopf auf Logo + EIN Anruf-Button (Minimal wörtlich, eine Conversion-Intention) · Hero-viewBox ohne Dach (Signature im Fold) ·
Startseiten-Kapitel auf Diagnose („Erkennen“) gekürzt, „Tun“ nur auf der Leistungsseite · Verbund-Kette als durchlaufende Leitung
statt vier Kacheln · Verfahren als flächige Zebra-Zeilen statt Haarlinien · Zonen-Beschriftungen nur in den Bändern, Marker-Namen
nur im Hero · drei Symbolfotos/Captions getauscht (kein Mittelmeer-Fenster, kein Neubau-Betonieren) · Copy ohne Antithesen-Punchlines.
