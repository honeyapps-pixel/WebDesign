# Salon Melissa — Demo-Website

Statische Demo-Website (HTML/CSS/JS) für den Friseursalon **Salon Melissa** in Weyhausen.
Per Doppelklick auf `index.html` im Browser lauffähig — keine Installation, kein Server nötig.

## Dateien
- `index.html` — Inhalt & Struktur
- `styles.css` — Gestaltung (hell, editorial, ein Mauve-Akzent)
- `script.js` — Scroll-Animationen, Mobil-Menü, dezente Hero-Parallaxe
- `assets/` — optimierte Bilder
- `desktop.png` / `mobile.png` — Render-Vorschau (1440 / 390 px)

## Design
- **Schriften:** „Marcellus" (Überschriften, elegante Serif) + „Mulish" (Fließtext) — via Google Fonts
- **Palette:** Off-White `#FAF7F4` · Text `#221D1D` · Akzent Mauve `#B06B7A` / `#8F4F5E`
- **Aufbau:** Header · Hero · Salon/Über · Leistungen · Zitat-Band · Galerie · Team · Termin/Kontakt + Karte · Footer
- Voll responsiv inkl. Mobil-Hamburger-Menü; respektiert `prefers-reduced-motion`

## Echte Daten (eingetragen)
- **Name:** Salon Melissa (Friseur)
- **Adresse:** Laischeweg 2, 38554 Weyhausen
- **Telefon:** 05362 71414 (als Anruf-Button `tel:+49536271414`)
- **Karte:** echte OpenStreetMap-Einbettung (kein Key nötig)

## ⚠️ Platzhalter — vor Veröffentlichung ersetzen
1. **Öffnungszeiten** (Di–Fr 09:00–18:00, Sa 08:00–13:00, Mo & So geschlossen) sind
   branchenüblich angenommen — durch die echten Zeiten ersetzen. Stehen in `index.html`
   im Abschnitt „Termin/Kontakt" **und** im Footer.
2. **Team** — die drei Karten („Name folgt") sind Platzhalter ohne echte Personen.
   Echte Namen, Fotos und Schwerpunkte ergänzen (Abschnitt `#team`).
3. **Preise** werden bewusst nicht genannt („Preise nennen wir beim Termin"). Bei Bedarf
   eine Preisliste ergänzen.
4. **Galerie- und Stockfotos** sind Beispielbilder — durch eigene Fotos aus dem Salon
   ersetzen (Ordner `assets/`).
5. **Impressum / Datenschutz** — Footer-Links sind Platzhalter (`#`) und müssen mit
   rechtlich vollständigen Seiten verknüpft werden (Pflicht in Deutschland).
6. **Keine erfundenen Bewertungen/Statistiken** — bewusst weggelassen. Echte Kundenstimmen
   können bei Bedarf ergänzt werden.

## Bildquellen
Beispielbilder von Unsplash (lizenzfrei), lokal optimiert (max ~1200 px, q≈82) und im Ordner
`assets/` gespeichert — nicht gehotlinkt. Vor dem Live-Gang durch eigene Salon-Fotos ersetzen.

## Vorschau neu erzeugen (optional)
```
node shot.mjs
```
erzeugt `desktop.png` und `mobile.png` neu (benötigt das vorinstallierte playwright-core/Chromium).
