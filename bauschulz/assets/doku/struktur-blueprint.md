# Struktur-Blueprint – BAUSCHULZ v2 (Kundenvorgabe, 2026-09-25)

Skelett vom Kunden vorgegeben (Referenz fuender.de) – kein struktur-architekt-Entwurf, Divergenz-Regel tritt zurück.

| Achse | Festlegung |
|---|---|
| Nav-Paradigma | dunkle Kopfleiste, Logo links, Textlinks rechts + Telefon-Knopf; mobil Menü-Knopf → Liste unter der Leiste |
| Sektions-Kopf | schlichte H2, keine Eyebrows/Nummern |
| Komponenten | Hero mit Textbox · Infoleiste 4 Spalten · 3 Bildkacheln mit Beschriftungsleiste · Galerie-Dialog mit Daumenleiste |
| Kontakt | Abschnitt „Standort & Kontakt": Adresse/Zeiten/Telefon/E-Mail/WhatsApp + Projektorte + Karte per Klick (OSM, Platzhalter = graue Fläche) |
| Footer | eine dunkle Zeile: Logo · © · Impressum · Datenschutz · Facebook |
| Galerie | pro Sparte eigene Seite: Bildraster (Auswahl) → Großansicht-Dialog mit Pfeilen, Zähler, Bildunterschrift (seit 2026-09-25 nachmittags) |
| Spine | Kopf → Hero → Infoleiste → Sparten (3) → Team (Gruppenfoto; Porträtreihe erst mit Namen) → Standort & Kontakt → Fuß; Unterseiten nur Impressum/Datenschutz |

## Änderung 2026-09-25 nachmittags (Kundenfeedback Johann Warkentin)
„Wenn man auf die Sparten klickt, kommen sofort Bilder" → je Sparte eine **eigene Seite**: Kopfbild mit Text (Box wie Startseite) →
Bilder klein im Raster (4/3/2 Spalten) → Klick = Großansicht (Dialog, Pfeile/Tastatur/Wischen) → Infoleiste → Fuß.
Kopfleiste bleibt auf allen Seiten; aktive Sparte = orange Unterstreichung (mobil: orange Kante links), `aria-current="page"`.
Startseite: Kacheln verlinken auf `hochbau.html` · `tiefbau.html` · `garten-landschaftsbau.html`; alte `/#tiefbau`-Adressen leiten per JS weiter.
