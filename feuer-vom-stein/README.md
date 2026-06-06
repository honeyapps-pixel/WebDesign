# Feuer vom Stein — Demo-Website

Statische Demo-Website (Deutsch) für das Restaurant **Feuer vom Stein**, Grill & Restaurant in Wittingen.
Per Doppelklick auf `index.html` im Browser lauffähig (Google Fonts werden via `<link>` geladen — Internetverbindung dafür nötig).

## Dateien
- `index.html` — Seitenstruktur und Inhalte
- `styles.css` — Design (dunkel, warm, rustikal-modern)
- `script.js` — Scroll-Reveals, Sticky-Header, dezente Hero-Parallaxe, Mobil-Menü
- `assets/` — optimierte Bilder
- `desktop.png` / `mobile.png` — Render-Kontrollscreenshots (1440 / 390 px)
- `shot.mjs` — Hilfsskript zum Erzeugen der Screenshots (kann entfernt werden)

## Design
- **Palette:** Hintergrund Espresso/Anthrazit `#17120F`, Text warmes Creme `#EFE7DA`, EIN Akzent Glut/Kupfer-Orange `#C8662F`
- **Schriften (Google Fonts):** Display „Fraunces“ (Serif), Fließtext „Hanken Grotesk“
- **Effekte:** dezente IntersectionObserver-Reveals (gestaffelt), leichte Hero-Parallaxe; `prefers-reduced-motion` wird respektiert
- Voll responsiv inkl. funktionierendem Hamburger-Menü

## Echte Daten (bereits eingepflegt)
- **Name:** Feuer vom Stein
- **Adresse:** Junkerstraße 6, 29378 Wittingen
- **Telefon:** 05831 251068 (als Anruf-Buttons `tel:+495831251068` mehrfach eingebunden)
- **Karte:** echte OpenStreetMap-Einbettung (iframe, ohne API-Key) mit Marker auf Wittingen

## WICHTIG — Platzhalter vor Veröffentlichung ersetzen
Folgende Inhalte sind **branchenübliche Platzhalter**, da nicht bekannt. Vor dem Live-Gang durch echte Angaben ersetzen:

1. **Öffnungszeiten** (Header-Kontakt & Footer): aktuell beispielhaft
   `Mo Ruhetag · Di–Fr 17:30–22:00 · Sa 17:00–22:30 · So 11:30–21:00` — durch die tatsächlichen Zeiten ersetzen.
2. **Speisekarte (Abschnitt „Speisekarte“):** die Gerichte sind als **Beispielauszug** gekennzeichnet; **keine Preise** angegeben. Durch die echte Karte ersetzen. Hinweistext „Beispielgerichte als Auszug. Preise und vollständige Karte vor Ort.“ ggf. anpassen/entfernen.
3. **Bilder (`assets/`):** Stock-Fotos als Platzhalter. In der Galerie steht ein sichtbarer Hinweis. Durch eigene Fotos vom Restaurant, von den Gerichten und vom Interieur ersetzen.
4. **Zitat im dunklen Banner („Ein gutes Stück Fleisch …“):** generisches Stimmungs-Zitat, kein echtes Zitat einer namentlichen Person. Bei Bedarf anpassen.
5. **Impressum & Datenschutz** (Footer-Links): aktuell Platzhalter `#`. Vor Veröffentlichung mit den rechtlich erforderlichen Seiten verlinken (Pflicht in Deutschland).
6. **E-Mail:** keine bekannt, daher bewusst nicht aufgeführt. Bei Bedarf in Kontakt/Footer ergänzen.

## Bildquellen
Bilder stammen von Unsplash (frei nutzbar), wurden lokal optimiert (max. ~1000–1500 px, JPEG ~80 %) und liegen unter `assets/`. Es wird nicht hotgelinkt. Motive: gegrilltes Fleisch/Steaks, Spareribs, Grillteller, gedeckter Tisch, rustikales Interieur.

## Hinweis
Footer enthält den Vermerk „Entwurf — Demo-Vorschau“. Vor Übergabe an den Kunden entfernen oder anpassen.
