# Connys Blumen Atelier — Demo-Website (Neubau)

Statische, voll responsive **Mehrseiten-Website** für **Connys Blumen Atelier** (Floristik,
Weyhausen). Inhalte, Bilder und Rechtstexte sind **1:1 von der bestehenden Website
[connys-blumen-atelier.de](https://www.connys-blumen-atelier.de) übernommen** und in das
Honeyapps-Editorial-System überführt (geteilte Motion-Engine, Hero-Muster „Bild gleitet von links").
Per Doppelklick auf `index.html` lauffähig — kein Server, kein Build nötig.

## Seiten (echte Unterseiten wie das Original)
- `index.html` — Home (Hero, Willkommen, USP, Teaser, Öffnungszeiten)
- `ueber-uns.html` — Über uns + Team (seit 1993)
- `angebot.html` — Angebot (Hochzeits-/Trauerfloristik, festliche Gestecke, offizielle Anlässe)
- `service.html` — Service (Bestellung & Lieferung, Balkon-/Terrassen-/Kübelbepflanzung)
- `galerie.html` — Galerie, **kategorisiert wie das Original** (Hochzeitsdeko, Tischdeko,
  Geschenkartikel, Trauerfloristik, Schnittblumen)
- `kontakt.html` — Kontakt & Anfahrt (Adresse, Telefon, E-Mail, OSM-Karte)
- `impressum.html` — echtes Impressum
- `datenschutz.html` — Datenschutzerklärung (vom Original übernommen)

## Echte Firmendaten (von der Originalseite)
- **Inhaberin:** Cornelia Choritz · **gegründet 1993**
- **Adresse:** Laischeweg 2, 38554 Weyhausen
- **Telefon:** 05362 71746 (`tel:`-Button) · **E-Mail:** connysblumenatelier@t-online.de
- **USt-IdNr:** DE164994496
- **Öffnungszeiten:** Mo–Fr 08:30–18:00, Sa 08:00–13:00, So geschlossen

## Bilder
Alle Galerie-/Hero-/Angebotsbilder sind die **echten Fotos der Originalseite**, lokal in `assets/`
gespeichert und optimiert (max. ~1400 px, JPEG q≈82), benannt nach Kategorie
(`hochzeit-*`, `tisch-*`, `geschenk-*`, `trauer-*`, `schnitt-*`, `angebot-*`, `real-hero.jpg`).
**Logo:** echtes Logo der Originalseite als transparentes PNG (`assets/logo.png`).

## Gestaltung & Technik
- **Ästhetik:** editorial-elegant (Layout-Archetyp G), viel Weißraum, große Fotografie
- **Palette:** Creme `#F7F5EE` · Text tiefes Grün `#25302A` · Akzent Salbei-Grün `#5D7355`
  (passend zum grünen Logo)
- **Schriften:** Playfair Display (Display) + Nunito Sans (Body)
- **Animation:** geteilte GSAP + ScrollTrigger + Lenis-Engine (`assets/motion.js`). Hero & Bilder
  nutzen **`data-reveal="wipe-left/right"`** — das Bild gleitet seitlich herein. Der **rechteckige
  Hero** ist eine **Crossfade-Slideshow** (`data-rotate`) durch mehrere echte Sträuße. Respektiert
  `prefers-reduced-motion` (dann erstes Bild statisch, kein Wechsel).
- **SEO:** JSON-LD `Florist`, Meta/OG je Seite, sprechende Titel.
- **Karte:** echte OpenStreetMap-Einbettung (ohne API-Key).

## Vor Veröffentlichung prüfen / anpassen
- **Datenschutz & Impressum:** vom Original übernommen — vom Betrieb final prüfen lassen,
  insbesondere **Hosting** (Original: IONOS; neue Seite ggf. Vercel) und Funktionen
  (Schriftarten/Karten/Kontaktwege). Hinweis steht auch auf der jeweiligen Seite.
- **Kontaktformular:** Das Original hatte ein Formular; hier läuft Kontakt bewusst über
  Telefon/E-Mail. Bei Bedarf Formular ergänzen (dann Datenschutz anpassen).
- **Öffnungszeiten zu Feiertagen** werden laut Betrieb zeitnah bekannt gegeben.

## Quellmaterial
`_orig/` enthält die heruntergeladenen Original-Seiten, Rohbilder und den Seiten-Generator
(`build_pages.py`) — **nur Arbeitsmaterial, nicht mit deployen.**

## Vorschau erzeugen
`node shot.mjs` rendert `desktop.png`, `tablet.png`, `mobile.png` (Home). Benötigt das lokale
playwright-core + Chromium im übergeordneten `.tools`-Ordner.
