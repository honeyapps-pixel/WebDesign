# Connys Blumen Atelier — Demo-Website

Statische, voll responsive Demo-Website für **Connys Blumen Atelier** (Floristik, Weyhausen).
Per Doppelklick auf `index.html` im Browser lauffähig — kein Server, kein Build nötig.

## Dateien
- `index.html` — Seitenstruktur und Inhalte
- `styles.css` — Gestaltung (Palette, Layout, Responsive, Animationen)
- `script.js` — Scroll-Reveals, Header-Zustand, dezente Hero-Parallaxe, Mobil-Menü
- `assets/` — optimierte Bilder (lokal, nicht hotgelinkt)
- `desktop.png` / `mobile.png` — Vorschau-Screenshots (1440 px / 390 px)

## Gestaltung
- **Ästhetik:** soft, botanisch, organisch, hell & elegant — viel Weißraum, dezente Effekte
- **Palette:** Creme `#F7F5EE` · Text tiefes Grün `#25302A` · EIN Akzent Salbei-Grün `#5D7355`
- **Schriften (Google Fonts):** Display „Playfair Display", Fließtext „Nunito Sans"
- **Icons:** eigene SVG-Linien-Icons (einheitliche stroke-width), keine Emojis
- **Animation:** IntersectionObserver-Reveals (gestaffelt), dezente Hero-Parallaxe; respektiert `prefers-reduced-motion`
- **Karte:** echte OpenStreetMap-Einbettung (iframe, ohne API-Key)

## Sektionen
Header · Hero (Anruf-CTA) · Atelier/Über · Leistungen (Sträuße & Gestecke, Hochzeits-,
Trauerfloristik, Pflanzen & Deko, Blumen-Abo, Abholung & Lieferung) · Galerie · Feature-Band ·
Öffnungszeiten · Kontakt + OSM-Karte · Footer.

## Echte Firmendaten (verwendet)
- **Name:** Connys Blumen Atelier
- **Adresse:** Laischeweg 2, 38554 Weyhausen
- **Telefon:** 05362 71746 (als `tel:`-Anruf-Button eingebunden)

## Platzhalter — VOR Veröffentlichung anpassen
- **Öffnungszeiten:** branchenübliche Beispielzeiten (Mo–Fr 09:00–18:00, Sa 09:00–13:00,
  So geschlossen). Im Abschnitt „Öffnungszeiten" und im Footer hinterlegt, mit Hinweistext markiert.
  → Echte Zeiten eintragen.
- **Galeriebilder:** Beispiel-Stockfotos (siehe Bildquellen). Durch Fotos echter Arbeiten ersetzen.
- **Hero-/Atelier-/Feature-Bild:** ebenfalls Stockfotos — bei Bedarf durch eigene Aufnahmen
  (Atelier, Conny bei der Arbeit) ersetzen.
- **Impressum / Datenschutz:** Footer-Links sind Platzhalter (`#`) — rechtlich erforderliche
  Seiten ergänzen.
- **Keine E-Mail / Website bekannt:** Kontakt läuft bewusst über Telefon/Anruf-Button.
- **Keine erfundenen Bewertungen/Testimonials** und keine erfundenen Statistiken verwendet.

## Bildquellen
Alle Bilder lokal in `assets/` gespeichert und optimiert (max. ~1200 px, JPEG q≈82, progressiv).
Quelle: Unsplash (kostenlose Lizenz). Motive: Blumensträuße, florale Arrangements, Rosen,
Tulpen, Callas, Lilie sowie ein Blumenladen (europäischer Kontext). Vor Live-Gang idealerweise
durch eigene Fotos ersetzen.

## Vorschau erzeugen
`node shot.mjs` rendert `desktop.png` und `mobile.png` (benötigt das lokale playwright-core +
Chromium im übergeordneten `.tools`-Ordner).
