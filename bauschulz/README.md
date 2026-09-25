# BAUSCHULZ GmbH & Co. KG – Website v2 „schlicht" (Honeyapps)

**Betrieb:** BAUSCHULZ GmbH & Co. KG (Komplementärin: BAUSCHULZ Verwaltungs GmbH) · Geschäftsführer Denis Schulz
**Adresse:** Fehringstraße 8, 38524 Sassenburg (Ortsteil Triangel) · **Telefon:** 0176 31482066 · **E-Mail:** info@bauschulz.com
**Status:** `MODE=individualisierung` – Redesign nach Kundenwunsch vom 2026-09-25, **LIVE seit 2026-09-25** auf https://bauschulz.vercel.app (Repo `10b791e`).
Vorige Demo (v1, 19 Seiten, „Bautagebuch von oben", live seit 2026-09-14): `_archiv/bauschulz-v1-demo-2026-09-14/`.

Bauen: `python3 .tools/bs2_bilder.py` (Bildexport, nur bei neuen Fotos) → `python3 .tools/bs2_gen.py` (HTML, Sitemap,
`vercel.json`) → `python3 .tools/site_check.py bauschulz`. Vorschau: `cd bauschulz && python3 -m http.server 8791`.
Screenshots: `node .tools/bs2_shots.mjs`. HTML nie direkt bearbeiten – Inhalte stehen in `.tools/bs2_gen.py`.

## Kundenwunsch (2026-09-25)
Kunde war mit v1 nicht zufrieden. Vorgabe: **ganz schlicht, klassisch, wie https://www.fuender.de**.
1. Beim Öffnen ein großes Bild (Hallenfassade mit Schriftzug, aus dem neuen Fotoshooting).
2. Darunter die **drei Sparten nebeneinander als Bild**: Hochbau · Tiefbau · Garten- und Landschaftsbau. Klick → kleine Galerie mit Bildauswahl.
3. Weiter unten **Team**, dann **Standort**.
4. **WhatsApp-Button** unten rechts. Farben schlicht.

Umsetzung: eine Startseite + Impressum + Datenschutz + 404. Galerie = Dialog mit großem Bild, Pfeilen (auch Tastatur/Wischen),
Bildunterschrift und Daumenleiste. Menüpunkte „Hochbau/Tiefbau/Garten- & Landschaftsbau" öffnen die jeweilige Galerie;
`bauschulz.com/#tiefbau` öffnet sie direkt. Alte v1-Adressen (`referenzen.html`, `kontakt.html` …) leitet `vercel.json` auf die Startseite um.

## Herkunft der Inhalte (nichts erfunden)
| Inhalt | Quelle |
|---|---|
| Logo, Farben Anthrazit #353534 / Orange #E88507 | bauschulz.com (Logo), wie v1 |
| Hero-, Team-, Porträt- und Hallenfotos | **Fotoshooting Thomas Koschel (Fotografiker), 09.09.2025**, vom Kunden geliefert (Ordner „BAUSCHULZ", 18 Fotos; Originale in `_raw/bauschulz-fotoshooting-2025/`). Hero = Foto 14, Team = Foto 5, Porträts = 1, 8, 13, 2, 3, Standort = 18. Fotograf im Impressum genannt |
| Sparten Hochbau/Tiefbau/GaLaBau | Kundenangabe 2026-09-25 |
| Galeriebilder | Projektfotos aus v1 (bauschulz.com-Portfolio + Relaunch-Entwurf bauschulz2.hawker-group.de), Zuordnung in `.tools/bs2_gen.py` → `SPARTEN` |
| „Bauunternehmen in 2. Generation", „Saubere Ausführung, klare Abläufe, verlässliche Termine" | Relaunch-Entwurf des Kunden (wie v1) |
| Kurztexte unter den Sparten | Hochbau: Leistungstext des Kunden (EFH/MFH/Gewerbe); Tiefbau/GaLaBau: beschreiben nur, was die Fotos zeigen, bzw. Registergegenstand „Pflaster- und Gartenarbeiten" (HRA 202485) |
| Bürozeiten Mo–Fr 08–17 Uhr | Google-Eintrag / 11880 / hanse-immobilien (übereinstimmend, wie v1) |
| Impressum | bauschulz.com, wörtlich (aus v1 übernommen) + Fotografen-Nennung |
| Datenschutz | v1-Fassung (Hosting Vercel, keine Cookies, Karte per Klick), Kontaktformular-Passagen entfernt |

## ⚠️ Offene Punkte für den Kunden
| Punkt | To-do |
|---|---|
| **Team-Namen** | Namen + Funktion der 5 Personen (Porträts in Reihenfolge des Gruppenfotos). Eintrag in `TEAM` → erscheint automatisch als Bildunterschrift |
| **Garten- und Landschaftsbau: Fotos** | Es gibt noch keine eigenen GaLaBau-Projektfotos. Aktuell: Pflaster-/Außenanlagen-Fotos aus Wohnbau-Projekten (Knesebeck, Ehmen, Wahrenholz, Wittingen) – **bestätigen lassen, dass die Außenanlagen von Bauschulz sind**, besser echte GaLaBau-Fotos anfordern |
| **Tiefbau: Fotos/Text** | Brücke + Fundamente + Maschinenfoto. Weitere Tiefbau-Projekte (Kanal, Erdarbeiten, Hofflächen?) und ein Satz des Kunden je Sparte wären gut |
| **Samstag** | Quellen widersprüchlich → nur Mo–Fr genannt |
| **WhatsApp** | angenommen für die Mobilnummer – bestätigen |
| **Hosting** | Datenschutz nennt Vercel. Bei Umzug zu All-Inkl Abschnitt 2 tauschen. Domain-Umzug: A-Record → 76.76.21.21, `www` CNAME → cname.vercel-dns.com, MX/SPF unverändert lassen |

## Bewusst weggelassen (Kundenwunsch „ganz schlicht“ – jederzeit reaktivierbar aus v1)
- **Ablauf der Zusammenarbeit** (Erstgespräch & Bedarf → Angebot & Zeitplan → Ausführung & Abstimmung → Abnahme, Kundentext aus dem Relaunch-Entwurf)
- **6 Google-Rezensionen** mit Namen (aus dem Relaunch-Entwurf) – beim Kunden fragen, ob eine als Zitat rein soll
- **Leistungs- und Referenz-Unterseiten** (v1: 19 Seiten) – bringen bei Google mehr Sichtbarkeit; alte Adressen leiten per 301 auf die Startseite
- **Bautagebuch** (16 Drohnen-Bauphasen) – 3 Bilder davon stecken in der Hochbau-Galerie, 2 in Tiefbau
- **Porträtreihe** (5 Einzelfotos aus dem Shooting) – liegt fertig in `assets/img/team-p1…p5`, erscheint automatisch, sobald in `TEAM` Namen stehen

## Cookies & Datenschutz
Keine Cookies, kein Storage, keine Drittanfrage vor Nutzeraktion: Schriften und Leaflet liegen lokal, OSM-Kacheln erst nach
„Karte laden" (Klick = Einwilligung). WhatsApp/Route/Facebook sind reine Links. → **Kein Cookie-Banner nötig.**

## QA (Stand 2026-09-25)
- `site_check.py`: 0 FAIL · 0 WARN (4 Seiten). `impeccable detect`: nur bekannte Fehlalarme (cramped-padding bei Vollbreite-Sektionen, clipped-overflow an Kachel/Karte, flat-type auf Rechtsseiten).
- Cookie-Messung (Playwright, alle Seiten gescrollt, Galerie geöffnet): vor „Karte laden" nur eigene Domain, 0 Cookies, 0 Set-Cookie, 0 Storage; danach zusätzlich nur tile.openstreetmap.org.
- Kein Overflow bei 320–2560 px; Galerie per Maus, Tastatur (Pfeile/Esc, Fokus zurück), Wischen; Menü mobil (Esc/außen/Link).
- 4-Agenten-Panel: struktur-divergenz (R2) · web-design (R2) · anti-ai (R2, alle 26 Bildunterschriften gegen das Foto geprüft) · ui-layout (R3 + Nachmessung 320 px) – bestanden.
