# Art-Direction — KFZ-Meisterwerkstatt Mattes (Isenbüttel)

## 1 · Kreativ-Brief

```
BRAND-ANKER (zuerst, Pflicht)
  Farben      : Marken-Blau #0F79B3 (Emaille-/Schild-Blau, aus Logo gesampelt) · Ink #16202B (blau-schwarz, kein reines Schwarz) · Stahl/Chrom-Neutrale · kühles Werkstatt-/Beton-Papier #ECEEF0 (siehe §3)
  Logo/Name   : echtes Logo assets/brand/logo.jpg — Maskottchen-Mechaniker + bold 3D-Wortmarke „MATTES" + Band „KFZ-MEISTERWERKSTATT". Schreibweise: KFZ Mattes / KFZ-Meisterwerkstatt Mattes
  Ton/Claim   : bodenständig, direkt, vertrauensvoll, „Hand-drauf"-Handwerk. Echte Claims:
                „Sie haben ein Problem mit Ihrem Auto? Wir lösen es." · „Ihre Zufriedenheit ist unser Erfolg."
                „Erfahrung seit 1964" · „Sie fragen, wir antworten." (— Rudi Mattes)
  Foto-Anmutung: Originalseite ist bildarm (Logo + Teamfoto + Konzeptbild „Autofahren trotz Behinderung" + Porträts).
                → echte Fotos zuerst (Team-Hero, Konzeptbild, Michelle-Porträt); Werkstatt/Reifen als Stock-Lückenfüller (Pexels), einheitlich kühl-neutral gegradet (saturate .82/grayscale .1 — Angleich an Original-Fotos).
  → Marke existiert: Farben verankert, NICHT divergent.

KONZEPT       : Die Werkstatt als Präzisions-Instrument — eine Heritage-Meisterwerkstatt seit 1964, erzählt wie eine analoge Instrumententafel: ablesbar, ehrlich, geeicht. 60 Jahre Erfahrung als Gütesiegel, kein Marketing-Lack.
WELT          : W8 · Vintage-Analog / Heritage-Werkstatt — trägt „seit 1964" + Maskottchen-Logo + Emaille-Schild-Blau; divergiert hart von W7 (Oberflächentechnik) & W6 (Tierzentrum) und von den Kfz-Nachbarn WFT/Hoyer.
SIGNATURE     : „Werkstatt-Instrument" als wiederkehrendes Motiv — Mini-Dial-Sektionsmarker (gezeichnete Tacho-Dials) + großer „seit 1964"-Emaille-Stempel. HERO trägt das ECHTE Team-Gruppenfoto (Crew an der Hebebühne, Original-Asset) als Vertrauensanker. [Update auf Kundenwunsch 2026-06-11: ursprünglicher Hero-Gauge/Tacho durch das echte Teamfoto ersetzt, Instrument-Motiv lebt in den Mini-Dials + Stempel weiter.]
MOTION        : mechanical (Nadel-Sweep, präzise up/left/right-Reveals, tool-haft) → data-motion="mechanical" am <html>. Divergiert von editorial (Oberflächentechnik) & kinetic (Tierzentrum).
TYPO-BEGRÜNDUNG: Big Shoulders Display (industrielle US-Signage/Werkstatt-Schild, kondensiert, bold — Echo der fetten „MATTES"-Wortmarke) + Public Sans (neutraler, sehr legibler Humanist-Grotesk fürs Lesen) + Space Mono (technische Spec-/Gauge-Labels, Service-Codes, 01/02-Marker, Retro-Typewriter-Note). Font-Klasse „Industrial-Signage-Display + Humanist-Grotesk + Mono" ≠ Display-Grotesk (Syne/Bricolage der letzten 2).
FARB-BEGRÜNDUNG: Grund = warmes Werkstatt-Papier (#F3F0EA), Text = blau-schwarzer Ink, EIN Akzent = Marken-Blau #0F79B3 (Schilder, Linien, Gauge, CTA). Stahl/Chrom nur als Neutral-Mittelton (Logo-3D-Echo). Kein zweiter Farbakzent.
BANDBREITE    : 3–4 (selbstbewusst-handwerklich, aber geerdet — nicht schrill)
```

## Divergenz-Nachweis (gegen letzte 2 Builds + Kfz-Nachbarn)
| Achse | KFZ Mattes | Oberflächentechnik (zuletzt) | Tierzentrum (vorletzt) | WFT (Kfz) | Hoyer (blau) |
|---|---|---|---|---|---|
| Welt | **W8 Vintage/Heritage** | W7 Neo-Bold | W6 Verspielt | Neo-Industrial | W2 Swiss |
| Archetyp | **A Editorial-Split + Instrument** | B/D Sidebar | E/D Vollbild-Kapitel | D Bold | D Split |
| Font-Klasse | **Signage-Display+Grotesk+Mono** | Display-Grotesk (Syne) | Display-Grotesk (Bricolage) | Oswald | Space Grotesk |
| Motion | **mechanical** | editorial | kinetic | mechanical | mechanical |
| Signature | **Analog-Gauge + 1964-Stempel** | RAL-Farbwand | Pfoten/V-N-Slider | Lack-Farbnummer | Kabelbaum-SVG |
| Token-Sprache | **1.25 eng · r3 · 1320 · 1.333** | Sidebar-breit | full-bleed | — | — |
→ 5–6 von 6 Achsen abweichend von jedem der letzten 2. Brand-Blau verankert (nicht gezählt). Motion = mechanical wie WFT/Hoyer, aber Welt/Archetyp/Font/Signature/Farbe klar anders → kein Kfz-Twin.

## 3 · Design-Tokens (in :root)
- `--space` Ratio **1.25 (eng)** — dichter, instrumententafel-haft
- `--radius` **3px** (Schild-Platte, fast scharf)
- `--line-weight` **1px** Haarlinie (Instrument-Bezel/Grid) + **2px** Heritage-Rahmen
- `--shadow` überwiegend flach / Kante `0 1px 0`; **hart-versetzt** nur am „1964"-Stempel (Echo der 3D-Logo-Extrusion)
- `--container` **1320 (breit, board-haft)**
- `--type-ratio` **1.333** (starke Hierarchie für Signage-Headlines + Gründungsjahr)
- Brand: `--accent #0F79B3` · `--ink #16202B` · `--paper #ECEEF0` (kühles Werkstatt-/Beton-Papier, bewusst kein warmes Cream → klärt impeccable `cream-palette`) · `--steel #8A929B` · `--line` blau-grau

## Charakter / USP-Hebel
- **Seit 1964** (60+ Jahre) — Heritage groß spielen (Emaille-Stempel, Jahreszahl).
- **Mobilitäts-Zentrum** (behindertengerechter Fahrzeugumbau, „Autofahren trotz Behinderung!") — echtes Alleinstellungsmerkmal, eigene starke Sektion mit dem echten Original-Konzeptbild.
- **Freie Werkstatt aller Marken** · TÜV-Abnahme im Haus (TÜV Nord) · 2 Standorte Isenbüttel.
- Bodenständige, direkte Copy-Stimme (Original-Claims 1:1).
