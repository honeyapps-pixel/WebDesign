# Kreativ-Brief — KlimaTech38 · Redesign 2026-09-12

**Anlass:** Der Erstbau (Swiss/Grid-Präzise, Haarlinien, Mono-Labels, Strichzeichnungen statt Fotos)
wurde vom Auftraggeber komplett abgelehnt: zu karg, zu technisch, zu textlastig — „sieht aus wie ein
Datenblatt, nicht wie ein Betrieb, bei dem man eine Klimaanlage kauft". Die beiden vom Kunden
benannten Vorbilder (solago.de, klima-mueller.com) sind das Gegenteil: **bildgeführt, atmosphärisch,
Produkt sichtbar, Preise sichtbar**. Dieser Brief ersetzt den vom 2026-09-08 vollständig
(archiviert in `.tools/kt38_inhalt/_alt_erstbau/`). Inhalte, Katalog, Rechner-Logik, Rechtstexte und URL-Struktur bleiben.

```
BRAND-ANKER (verankert, nicht verhandelbar)
  Farben      : Anthrazit #4D4D4D und Sky-Blau #A1C8EB aus dem echten InTroTech-Logo.
                Neu ist nur die ANWENDUNG: Sky-Blau wird von der Haarlinie zur FLÄCHE — großflächige
                kühle Verläufe (Sky → Weiß = „kühle Luft"), tonige Bühnen hinter Produkten, Chips.
                Aktion/Links: Aktionsblau #1668AE (AA-konforme Ableitung, wie bisher).
                Ink/Text: #24282D (Anthrazit vertieft). Tiefblau #0E2A3A nur als Footer-Grund.
                → EIN Akzent (Blau). Das grüne Energie-Signal des Erstbaus ENTFÄLLT — Energie
                  unterscheidet sich über die Bildwelt (Sonnenlicht, Dach, Ausweis), nicht über Farbe.
  Logo/Name   : Wortmarke „KlimaTech38" (Sparte) + echtes InTroTech-Logo im Footer/„Mit wem".
  Ton/Claim   : sachlich-freundlich, erklärend, keine Superlative; Grundsatz der Mutterfirma
                „Innovation trifft Verantwortung". Texte des Erstbaus bleiben (fachlich geprüft).
  Foto-Anmutung: helle, sonnige Innenräume mit sichtbarem Innengerät; kühle Weiß-/Blautöne;
                Außengerät vor weißer Wand/blauem Himmel. Alle Bilder auf EINE kühle Gradierung.

NISCHE        : C2 Handwerk (SHK/Klima) + C5-Andockung (Katalog mit sichtbaren Preisen, KEIN Shop).
                Conversion primär: Beratungsanfrage (Anruf/WhatsApp/Formular); sekundär: Set anfragen.
KONZEPT       : „Sommer, geplant." — Die Seite fühlt sich an wie der Moment, in dem man an einem
                heißen Tag einen gekühlten Raum betritt: hell, ruhig, klar. Zwei Wege (selbst
                einbauen / einbauen lassen) stehen als ein SCHALTER auf jeder Seite nebeneinander.
WELT          : W5 Atmosphärisch — in HELLER Ausprägung („Sommerlicht"): kinoreife, großflächige
                Fotografie und weiche Tiefe wie im Boutique-Dunkel-Katalog, aber auf hellem Grund,
                weil das Produkt (kühle Luft, Licht) hell ist und Sky-Blau eine helle Markenfarbe.
                Bewusste Abweichung vom Katalog-Default „dunkler Grund" (zählt als Divergenz).
SIGNATURE     : **Der Wege-Schalter** — ein Segment-Schalter „Selbst einbauen | Einbauen lassen",
                der im Hero sitzt, in jeder Produktkarte den Preis umschaltet (Abholung ↔ inkl.
                Montage), auf jeder Set-Seite die passende Preisspalte hervorhebt und im Anfrage-
                formular das Thema vorwählt (sessionStorage `kt38-weg`). „Die Seite mit dem Schalter."
                (Ein ursprünglich geplantes Luftstrom-Motiv im Hero wurde im QA als Deko gestrichen.)
MOTION        : soft (→ data-motion="soft"): Reveals up/mask/wipe, sanfte Skalierung der Bühnen,
                Hover-Lift der Karten hinter (hover:hover). Keine mechanischen Linien, kein Ticker.
TYPO-BEGRÜNDUNG: Display **Funnel Display** (geometrisch, leicht kondensiert, technisch-freundlich —
                trägt große Zahlen wie „3,5 kW" und Preise ohne Mono-Anmutung) + Text **Golos Text**
                (robuste Grotesk, sehr gut lesbar bei 17 px, nicht KI-üblich). Beide variabel, lokal
                in assets/fonts/. Typo-Entscheidungen: Headlines mischen zwei Gewichte in EINER Zeile
                (600 + 500/ink-soft, nur bei echter Zweiteilung), Kennwert-Chips in Gemischtschreibung
                (.01em), Preise/Telefon in tabular-nums, Lesespalte ≤ 62ch, clamp()-Kette mit Ratio 1.333.
FARB-BEGRÜNDUNG: Grund Weiß #FFFFFF + „Kühl-Grau" #F3F6F9; Bühnen (Produkt-Stages, Rechner) als
                Verlauf Sky #A1C8EB → #E8F1F9; CTA Aktionsblau #1668AE; Text Ink #24282D;
                Footer Tiefblau #0E2A3A mit InTroTech-Logo weiß. Grün gibt es nicht mehr.
BANDBREITE    : 3 (markant durch Bild und Fläche, ruhig in Typo und Bewegung).
```

## Struktur-Tokens (Phase 2, verbindlich)
| Token | Wert | Abweichung zum Erstbau / zu DK Fenster / MAVA |
|---|---|---|
| Spacing-Ratio | **1.618×** | Erstbau 1.25–1.5× |
| `--radius` | **20 px** Karten / **pill** Buttons / 12 px Chips | Erstbau 0 · DK 0–2 px · MAVA 0 |
| `--line-weight` | 1 px, nur innerhalb von Karten | Erstbau: Haarlinien als Skelett |
| `--shadow` | **weich-diffus, kühl getönt** (2 Lagen, rgba(14,42,58,.10/.06)) | Erstbau none · DK weich (dunkel) |
| `--container` | **1280** + vollbreite Bühnen (Hero, Kapitel, Karte) | Erstbau 1180 zentriert |
| `--type-ratio` | **1.333** | Erstbau 1.2 |

## Divergenz-Vorprüfung (gegen Register: DK Fenster 2026-09-05 · KlimaTech38-Erstbau 2026-09-08)
| Achse | DK Fenster | KT38-Erstbau | **Redesign** |
|---|---|---|---|
| Welt | W5 dunkel | W2 Swiss | W5 **hell** (Abweichung dokumentiert) |
| Archetyp | B Full-Bleed | C zentriert | **B/Showcase** (Vollbild-Hero + Produkt-Bühnen + Bento) |
| Font-Klasse | Serif-Display + Neo-Grotesk | Grotesk + Grotesk + Mono | **Geometric-Display + Grotesk-Text** |
| Motion | still | mechanical | **soft** |
| Signature | DIN-Öffnungssymbole | Kältekreis-Linie | **Wege-Schalter** |
| Token-Sprache | 1.618 / 0–2 / weich / breit / 1.5 | 1.25 / 0 / none / 1180 / 1.2 | 1.618 / **20+pill** / weich-kühl / **1280+Bühnen** / **1.333** |
→ gegen KT38-Erstbau 6/6, gegen DK Fenster ≥ 4/6 (Welt strittig, Archetyp nah — Font, Motion,
Signature, Token klar anders). Gegen MAVA (W1 · D · Ein-Familien-Sans · editorial · Diagonale): 6/6.

## Bildwelt (Phase 7, umgesetzt)
Original-Betrieb hat keine eigenen Klima-Fotos (Sparte neu) → Pexels als Lückenfüller, alle auf
kühle Gradierung; Nachweise in `assets/_attribution.txt`. Hero: `hero-wohnzimmer.jpg` (helles
Wohnzimmer, Innengerät sichtbar — ab 641 px; ≤ 900 px tragen Kapitel-Köpfe eine flächige Waschung, dort ist
das Foto Stimmung, nicht Produktnachweis). Einbausituationen (Bento): Wohnzimmer · Schlafzimmer · Kinderzimmer
· Arbeitszimmer · Dachgeschoss. Energie: `sonne-vorhang.jpg`, `daemmung.jpg`, `energieausweis.jpg`,
`pv-dach.jpg`. Produkte: **keine Fremdfotos mit Herstellerlogo** — die Sets tragen eine eigene,
weich schattierte SVG-Produktdarstellung auf blauer Bühne + kW-Chip (kein Strich-Schema mehr).
