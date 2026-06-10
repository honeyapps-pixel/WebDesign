# Art-Direction — TK Bewässerungstechnik (Inh. Tobias Koslikow), Gifhorn-Gamsen

MODE=demo · Stack: statisch + GSAP/Lenis · Datum: 2026-06-09

## 1 · Kreativ-Brief

```
BRAND-ANKER
  Farben      : KEINE echte Marke (Neugründung, keine Website, kein Logo) → Farben frei.
                Gewählt: Wasser-Teal #0C637A (EIN Akzent) auf kühlem Hellgrau-Paper #ECEFEE,
                Ink #14211F. Rasen-Grün #6E9F3A NUR funktional im Zonenplan/Legende, NIE als UI-Akzent.
  Logo/Name   : Wortmarke „TK Bewässerungstechnik" + geometrisches Monogramm-Mark
                (Tropfen aus Wurf-Bogen) — selbst gesetzt, im README als ersetzbarer Demo-Schriftzug markiert.
  Ton/Claim   : sachlich, handwerklich-präzise, regional, anpackend. Kein Marketing-Sprech.
                Leit-Claim: „Wasser, genau dorthin. Automatisch."
  Foto-Anmutung: echte Bewässerungs-/Rasenfotos (Pexels-Lückenfüller) — Versenkregner, Wurfbögen,
                Tropfschläuche, gepflegter Rasen; kühl/grün, ein warmer Golden-Hour-Hero als Kontrast.
  → Echte Daten: Waldweg 29, 38518 Gifhorn · 01514 1633842 · 24 h erreichbar · 5,0★ (4×) Google.

KONZEPT       : Ein Garten wird wie ein Ingenieur-Projekt geplant — Zonen, Wurfweiten, Wassermengen.
                Die Seite ZEIGT diese Planung (Zonenplan), statt „grüner Rasen"-Floskeln zu behaupten.
WELT          : W2 · Swiss / Grid-Präzise — trägt „…technik": Vermessung, Raster, Mono-Specs,
                Hairline-Linien. Frisch-hell statt kalt; das Wasser-Teal hält es lebendig.
SIGNATURE     : „Bewässerungs-Zonenplan" — top-down SVG-Schema eines Gartens (Haus, Rasen, Beete)
                mit Regner-Punkten + Wurfbögen (Z1·Z2·Z3) und Mono-Specs (Wurfweite m · l/min · Zonen).
                Wurfbögen fegen mechanisch ein. Zweit-Signature: Mono-Spec-Labels (▦) durchgängig.
MOTION        : mechanical (data-motion="mechanical") — knapp, linear, präzise; nur up/left/right.
                Passt zur Ingenieur-Anmutung; Wurfbögen + Zähler snappen sachlich ein.
TYPO-BEGRÜNDUNG: Geologica (technischer Grotesk-Display, „kartografisch"/engineered) für Headlines +
                Hanken Grotesk (neutral, lesbar) für Fließtext + IBM Plex Mono für Specs/Labels/Zonen.
                Bewusst NICHT Space Grotesk (überstrapaziert), NICHT Inter/Roboto.
FARB-BEGRÜNDUNG: Paper = kühles Hellgrau (Werkstatt-Sauberkeit). Ink = fast-schwarzes Tannen-Slate.
                EIN Akzent = Wasser-Teal (CTA, Links, Aktiv, Wurfbögen). Rasen-Grün rein illustrativ.
BANDBREITE    : 2–3 (ruhig-sachlich, aber mit einem markanten Signature-Modul).
```

## Divergenz-Vorprüfung (gegen die letzten Builds)

Letzte 2 Builds = **Move on Time** (W7 Neo-Modern/Bold-grün · Archetyp D · Display-Grotesk Archivo Black ·
mechanical · Region-Marquee/Steps · Token bold) und **Feengarten** (Mystisch-Botanisch · G+Sidebar ·
Display-Serif Cormorant · soft · Krafttier-Linien · Token soft).

| Achse | TK Bewässerung | vs Move on Time | vs Feengarten |
|---|---|---|---|
| Welt | W2 Swiss/Grid-Präzise | ✓ ≠ W7 | ✓ ≠ Mystisch |
| Archetyp | C-Swiss (links-bündige Spec-/Modul-Grid) | ✓ ≠ D | ✓ ≠ G |
| Font-Klasse | Technical-Grotesk + Mono (Geologica/Hanken/Plex Mono) | ✓ ≠ Archivo Black Display | ✓ ≠ Serif+Sans |
| Motion | mechanical | ✗ = mechanical | ✓ ≠ soft |
| Signature | Zonenplan-Schema + Mono-Specs | ✓ ≠ Marquee/Steps | ✓ ≠ Krafttiere |
| Token-Sprache | Spacing 1.25 · Radius 0 · Container 1300 · Type-Ratio 1.2 · Hairline 1px · flat | ✓ ≠ bold | ✓ ≠ soft |

→ vs Move: **5/6** abweichend (nur Motion gleich; erlaubt, da Welt ≠ → „Welt+Motion nicht beide gleich" erfüllt).
→ vs Feengarten: **6/6** abweichend. **Bestanden.** Markenfarben sind frei (keine Anker-Kollision).

## 3 · Design-Tokens (verbindlich, in :root)

```
--paper #ECEFEE · --panel #F6F8F7 · --ink #14211F · --ink-soft #586460 · --accent #0C637A
--lawn #6E9F3A (NUR Zonenplan) · --line rgba(20,33,31,.14)
--space-ratio 1.25 (eng, Swiss-dicht) · --radius 0 (scharf) · --line-weight 1px (Hairline-Raster)
--shadow none (flach) · --container 1300 (breit) · --type-ratio 1.2 (ruhig, Kontrast über Gewicht/Größe)
Breakpoints aus --container abgeleitet (nicht fix 980/680).
```
Mind. Spacing-Ratio, Radius, Container, Type-Ratio ≠ Move on Time (bold) — erfüllt.

## 4 · 10K-Messlatte
Bespoke Typo: Mono-Specs neben Display-Headlines, große Zonennummern, gesperrte Mono-Labels.
Signature sichtbar: der Zonenplan ist das Herzstück (nicht weglassen). Art-direkte Bilder: kühl-grüner
Grade, Versenkregner-Detail + Wurfbogen als Leitmotiv. Eigene Copy-Stimme: handwerklich, regional,
keine erfundenen Zahlen (nur echte: 24 h, 5,0★/4× Google). Zurückhaltung: flach, viel Hairline-Luft.
