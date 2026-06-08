# Kreativ-Brief — Tierarztpraxis Bellinato (Wesendorf & Wittingen)

MODE=demo · Branche: veterinary (Kleintiere **und** Pferde) · Region: Wesendorf/Wittingen (Landkreis Gifhorn)
Quelle: tierarzt-wesendorf.de (WebsiteBaker-Seite von 2013/2016, vollständig gecrawlt).

## BRAND-ANKER (zuerst)
- **Farben** : Keine echte Marke vorhanden (alte Textseite, kein Logo). Palette daher frei
  abgeleitet aus der Welt → **EIN Akzent Lehm/Terracotta `#B4582F`**, Neutrale warmes Hafer-Papier
  `#F5EFE6` + Espresso-Tinte `#2E2620` + Taupe `#6B5E50`. Warm-erdig statt klinisch-kühl.
- **Logo/Name** : Kein Logo-Asset → typografische Wortmarke **„Tierarztpraxis Bellinato"**
  (Newsreader-Versalie „B" als feine Linien-Initiale + Wortzug). Kein erfundenes Emblem.
- **Ton/Claim** : warmherzig, persönlich, fachlich fundiert, leicht ländlich-bodenständig.
  Echter O-Ton aus der Originalseite: *„das Tier steht immer im Vordergrund"*,
  *„mit tierisch guten Wünschen für alle Zwei- und Vierbeiner"*.
- **Foto-Anmutung** : Original nur winzige 2015-Innenraum-Schnappschüsse (≤530px, unbrauchbar als
  Hero/Feature) → warme, golden gegradete Stock-Tierfotos als Lückenfüller (Phase 7). Echte
  Praxis-/Team-Fotos erst Phase 10.

## KONZEPT
**„Die Landpraxis für Zwei- und Vierbeiner."** Eine Tierärztin, die Kleintiere **und Pferde**
behandelt — selten und der echte USP. Die Seite erzählt das wie eine warme Reportage über eine
fürsorgliche Praxis auf dem Land, nicht wie eine kühle Klinik-Visitenkarte.

## WELT
**W3-nah · Warm-Natürliche Landpraxis** (erdig, fürsorglich, geerdet) — bewusst **NICHT** Klinisch-Klar
(W4), weil das die Pferde-/Land-Seite verschenken und mit Physio Hübner (klinisch-Salbei) kollidieren
würde. Warmth + Vertrauen statt Hygiene-Kühle. Keywords: `warm natural earthy country veterinary care trust editorial`.

## SIGNATURE
**Der „Zwei-Praxen"-Standort-Umschalter** — ein taktiler Toggle **Wesendorf ⇄ Wittingen**, der
Adresse, Sprechzeiten, Telefon und OpenStreetMap-Karte live umschaltet (löst den echten Pain: zwei
Standorte, unterschiedliche Zeiten). Sekundär: **feine Einlinien-Tier-Marken** (Pferd · Hund · Katze ·
Heimtier) als echte SVG-Marker bei den Tierarten — handgezeichnete Anmutung, konsistente stroke-width.

## MOTION
**`soft`** (langsam, weich, atmend; `power2.out`, ~1.2 s, Vokabular up/mask/wipe; Ken-Burns im Hero).
Bewusst anders als die letzten Builds (Beule = kinetic, InTroTech = editorial). `prefers-reduced-motion`
schaltet statisch.

## TYPO-BEGRÜNDUNG
**Newsreader** (warme, literarische Old-Style-Serif mit echten Kursiven) als Display + **Asap**
(humanistische Grotesk, freundlich, sehr lesbar) für Fließtext/UI. Literarisch-warm = „Reportage über
die Praxis"; humanist-Sans hält es zugänglich (Healthcare-Lesbarkeit). Weder Inter/Roboto/Arial noch
eine im Register schon genutzte Paarung (kein Fraunces/Cormorant/Marcellus/Cinzel/Spectral/Playfair/
Bricolage/Saira). Frische Font-Klasse.

## FARB-BEGRÜNDUNG
Hafer-Papier `#F5EFE6` als warmer Grund (viel Luft), Espresso `#2E2620` als Tinte (warm, nie Schwarz),
**Lehm/Terracotta als EINZIGER Akzent** in drei Helligkeiten DESSELBEN Hue (kein zweiter Akzent):
`--accent #B4582F` (Flächen/Icons/Buttons), `--accent-deep #8C4222` (Akzent-TEXT auf hellem Grund, WCAG-AA),
`--accent-on-dark #E3A983` (aufgehellter Lehm für Lesbarkeit auf Espresso-Bändern, 8.2:1). Kontaktband
dunkel = Espresso. Alle Microlabels über `--ink-faint #736452` (AA 5.0:1). Anti-AI: eine Akzentfarbe.

## BANDBREITE
**2–3** (ruhig-warm, redaktionell; nicht expressiv-schrill — es ist eine Arztpraxis, Vertrauen zählt).

---

## Pflicht-Tokens (Token-Sprache, bewusst ≠ zuletzt gebaut)
| Token | Wahl | ≠ letzter Build? |
|---|---|---|
| Spacing-Ratio | **1.618×** (großzügig, magazinhaft) | Beule eng/bold → ja |
| Radius | **weich 12px** | Beule scharf → ja |
| Line-weight | 1px Haarlinie | — |
| Shadow | weich-diffus, warm, niedrig | Beule hart → ja |
| Container | **breit 1320** | ja |
| Type-Ratio | **1.333** (Quart) | ja |

## Layout-Archetyp
**B — Full-Bleed Editorial / Magazin** (Ken-Burns-Hero, Kapitel-Bänder 01/02/03, Vollbild-Zitatband,
Masonry-Galerie, dunkles Kontaktband). **Im Register noch NIE genutzt** → maximale Struktur-Divergenz.

## Divergenz-Check (gegen letzte 2 Builds — Pflicht ≥3/6)
| Achse | Bellinato (neu) | Beule Indoor Kart | InTroTech | ≠ beide? |
|---|---|---|---|---|
| Welt | Warm-Natürliche Landpraxis | Neo-Modern Bold (dunkel) | Swiss/Technisch | ✅ |
| Archetyp | **B (Magazin)** — neu im Register | D | C/D | ✅ |
| Font-Klasse | Old-Style-Serif (Newsreader) + Humanist-Sans (Asap) | Display-Grotesk condensed | Display-Grotesk + Sans | ✅ |
| Motion | **soft** | kinetic | editorial | ✅ |
| Signature | Standort-Umschalter + Einlinien-Tier-Marken | Startampel/Mono-Rundenzeiten | — | ✅ |
| Token-Sprache | 1.618× · r12 · 1320 · 1.333 · weich | dunkel/scharf/hart | swiss/grau | ✅ |

**6/6 Achsen abweichend** von jedem der letzten zwei Builds (Soll: ≥3/6). Markenfarbe ist hier frei
(keine echte Marke), daher kein Anker-Konflikt.
