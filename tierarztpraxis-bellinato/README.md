# Tierarztpraxis Bellinato — Wesendorf & Wittingen (Demo)

Statische Demo-Website (HTML/CSS/JS) für die **Tierarztpraxis Nerina Bellinato** —
Kleintiere und Pferde, zwei Standorte (Wesendorf & Wittingen, Landkreis Gifhorn).
Modernisierung der veralteten Originalseite `tierarzt-wesendorf.de` (WebsiteBaker, Stand 2013/2016).

**MODE:** `demo` (Verkaufs-Demo) · **Stack:** statisch + GSAP/ScrollTrigger + Lenis (`assets/motion.js`)
**Art-Direction:** siehe `assets/art-direction.md` (Welt: Warm-Natürliche Landpraxis · Archetyp B Magazin ·
Motion `soft` · Signature: Standort-Umschalter + Einlinien-Tier-Marken).

## Dateien
- `index.html` · `styles.css` · `script.js` (Standort-Umschalter, aktive Nav, A11y-Tabs)
- `assets/motion.js` (Honeyapps-Motion-Engine, `data-motion="soft"`)
- `assets/*.jpg` (Bilder), `assets/_orig/` (Original-Screenshots 2015, nur Referenz)
- `assets/art-direction.md` (Kreativ-Brief), `assets/BILDNACHWEIS.txt` (Pexels-Attribution)

## Echte, übernommene Inhalte (von der Originalseite)
- **Praxis & Inhaberin:** Nerina Bellinato, prakt. Tierärztin (TiHo Hannover, seit 01/2012 Inhaberin Wesendorf,
  seit 2014 Zweitpraxis Wittingen; Schwerpunkte Zahn/Chirurgie/Kolik). Bio 1:1 aus der Team-Seite.
- **Leistungen:** Digitales Röntgen, Ultraschall, EKG, Zahnbehandlungen, Chirurgie, Inhalationsnarkose,
  Labordiagnostik, Haut/Allergien/biologische Therapie, Impfungen, Ernährungsberatung, Heimtiere, Pferde.
- **Zwei Standorte (echte Daten):**
  - Wesendorf — Celler Straße 1, 29392 Wesendorf · **Tel. 05376 976907** · Fax 05376 976908
  - Wittingen — Knesebecker Straße 1, 29378 Wittingen · **Tel. 05831 9936973**
  - E-Mail: info@tierarztpraxis-wesendorf.de
  - Sprechzeiten je Standort 1:1 übernommen (im Umschalter hinterlegt).
- **Preise/GOT:** 1,2-facher GOT-Satz im Normalfall, Kostenvoranschläge möglich (aus Originaltext).
- **Impressum:** Tierärztekammer Niedersachsen, Verantwortliche Nerina Bellinato (Footer-`<details>`).
- **JSON-LD** `VeterinaryCare` mit beiden Standorten + Geokoordinaten.

## ⚠️ PLATZHALTER — vor finaler Auslieferung ersetzen (Phase 10, nach Verkauf)
- **Bilder = Stock-Lückenfüller (Pexels).** Die Originalseite hatte nur winzige 2015-Innenraum-Schnappschüsse
  (≤530 px), daher warme Stock-Tierfotos. Quellen: `assets/BILDNACHWEIS.txt`.
- **Hero-Foto** zeigt aktuell einen (männlichen) Stock-Tierarzt — die Inhaberin ist **Nerina Bellinato (w)**.
  → durch ein echtes Foto der Praxis/Inhaberin ersetzen.
- **Team:** Die Original-Team-Seite (2016) nannte zusätzlich Assistenz-/Azubi-Namen (Stand veraltet).
  Bewusst NICHT übernommen außer der Inhaberin. Vor Veröffentlichung aktuelles Team einpflegen.
- **E-Mail/Telefon** anhand aktueller Praxisangaben final bestätigen.

## QA (Phase 8 — 3-Agenten-Panel)
`anti-ai-reviewer` · `ui-layout-reviewer` · `web-design-reviewer` — Fix-Loop bis alle BESTANDEN.
Screenshots: `.tools/shots-bellinato/`. Re-Screenshot: `node .tools/shot_bellinato.mjs`.

## Lokal ansehen
`open index.html` (Safari/Chrome). Eigenständig deploybar (alle Pfade relativ, Engine in `assets/`).
