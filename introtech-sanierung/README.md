# InTroTech GmbH — Demo-Website

Statische Website (HTML/CSS/JS) für die **InTroTech GmbH** in Gifhorn — TÜV-zertifizierter
Fachbetrieb für **Leckageortung, Trocknung und Sanierung** mit 24/7-Notdienst.
Komplett neu gebaut auf Basis der bestehenden Seite [introtech.de](https://www.introtech.de),
**brand-treu** (echtes Logo + Logo-Farben) und mit allen Inhalten inkl. Unterseiten.

## Design-Direction — aus der echten Marke abgeleitet
Die Palette stammt **direkt aus dem echten Logo** (nicht erfunden):
- **Wortmarke Anthrazit** `#404040` → Text/Überschriften (`#383838` / `#262626`).
- **Wassertropfen Sky-Blau** `#A1C8EB` → Akzent-Tints; daraus abgeleitetes „Aktionsblau"
  `#2E72B8` (Buttons/Links, WCAG-AA auf Weiß) und tiefes Stahlblau `#1B3A57` (Kontakt-Band).
- **Logo-Neutrale** Grau `#6E7173` / Linien `#E2E5E9` auf hellem Grund.
- Hell, ruhig, seriös; Stahlblau #1B3A57 nur im Kontakt-Band.

**Echtes Logo eingebaut (aktuelle Fassung „… | Bauwerksabdichtung“, 2026-09-24 von introtech.de freigestellt; alte Fassung in `.tools/_archiv/introtech-sanierung_logo_alt/`):** `assets/brand/logo.png` (Header), `logo-white.png` (dunkler Footer),
`mark.png` (Favicon / Icon = Gebäude + Tropfen). Heruntergeladen von introtech.de.

**Schriften (Google Fonts):** Display **Source Sans 3** (humanistisch wie die Logo-Wortmarke), Fließtext **IBM Plex Sans**.

**Icons:** echte SVG-Linien-Icons; WhatsApp im offiziellen Glyph.

## Aufbau (editorial, kein Card-Template)
Header (Notruf + WhatsApp) · Hero · Mission „Innovation trifft Verantwortung" (Ansatz/Idee/Vision) ·
Leistungen als wechselseitige Bild-Text-Reihen (4 Leistungen mit Detailtiefe) · Ablauf (seit 2026-09-24: 4 Original-Schritte,
„alles aus einer Hand") · Über uns (inkl. Geschäftsführung) · Einzugsgebiet · Kontakt (Notdienst,
WhatsApp, Formular, OSM-Karte) · Footer. Plus **impressum.html** (echte Registerdaten).

## Inhalte 1:1 von introtech.de übernommen (inkl. Unterseiten)
- **Mission:** „Innovation trifft Verantwortung." · „Gebäude schützen, Werte erhalten und
  Lebensqualität sichern." · Ansatz / Idee / Vision.
- **Leistungen:** Leckageortung & Notdienst · Trocknung (Wasserschäden & Neubauten) ·
  Schaden-, Schimmel- & Asbest-Sanierung (Schimmelsanierung nach **BG BAU DGUV 201-028**,
  Personenschutz **P3/A3**, Unterdruckhaltung & Freimessung; Asbest nach **TRGS 519**;
  Inventarreinigung; Wiederaufbau inkl. Versicherungsabwicklung) · Energetische Beratung &
  Planung (Energieausweis; PV/Wärmepumpe/Klima; 6 Punkte energetische Sanierung).
- **WhatsApp** übernommen (Original nutzt den Wix-„Start Chat Button"): Header-Icon, Hero-Button,
  Kontaktzeile und Floating-Button → `https://wa.me/4953718759972`.
- **Echte Kontakt-/Registerdaten:** Zeisigweg 4, 38518 Gifhorn · Tel/Notdienst 05371 8759972 ·
  info@introtech.de · Mo–Fr 08–18 Uhr · GF Johann Warkentin, Jonathan & Adrian Mangold ·
  Amtsgericht Hildesheim HRB 210481 · USt-IdNr DE460142356 · TÜV-zertifiziert.
- **Einzugsgebiet:** Gifhorn, Wolfsburg, Braunschweig, Peine, Salzgitter, Helmstedt und Umgebung.

## Redesign „High-End" (2026-09-24)
Verlauf am selben Tag: Notruf-Tafel (dunkel) → heller Einstieg mit Video-Loop → Bildfolge mit
Stadien-Leiste — alles vom Nutzer abgelehnt („muss viel edler und hochwertiger aussehen, moderne
High-End-Website, benutze unser System"). Daraufhin volle Pipeline: Kreativ-Brief
(`assets/art-direction.md`), Struktur-Blueprint vom `struktur-architekt` (`assets/struktur-blueprint.md`).

- **Leitidee „Planblatt":** links die feste Leiste (Plankopf: Logo, Leistungen, Unternehmen, 24/7 Notruf
  als Textlink), rechts das Blatt, unten der **Lageplan** (statische, lokal gespeicherte OSM-Karte mit Sitz
  und Einzugsgebiet, 0 iframes) mit weißem **Schriftfeld** als Footer — auf allen 9 Seiten gleich.
- **Titelblatt:** h1 = Original-Satz in Source Serif 4 Light („… *sondern auch bleibt.*"), rechts randlos die
  **Bildfolge „ein Raum, drei Stadien"** (Trocknung → Sanierung → fertig, ruhige Überblendung, nur
  „Symbolbilder" + Pause-Knopf sichtbar; bei Reduced Motion/Save-Data bleibt Bild 1 stehen).
- **Leistungen als Haarlinien-Register** (Anliegen · Leistung · Stichworte · Foto · Pfeil), Unternehmen mit
  Datenblatt (Geschäftsführung, Zertifikate wörtlich von introtech.de/über-uns), Ablauf 4 Original-Schritte,
  Anfrage (große Notrufnummer | Haarlinien-Formular). Sektionsköpfe = Original-Leitsätze.
- **Schrift lokal:** Source Serif 4 + Source Sans 3 (`assets/fonts/`, `assets/fonts.css`); GSAP lokal
  (`assets/js/`), kein Lenis, keine Google-/CDN-Anfragen mehr.
- **Unterseiten:** „Blattkopf" (Titelzeile · h1 Serif · Lead + „Schaden melden" | Foto randlos), Innenteile
  im Haarlinien-Stil, dunkles CTA-Band ersetzt durch Anfrage-Zeile.
- **Generator:** `.tools/itc_gen.py` (Leiste, Lageplan, Startseite, Blattköpfe; idempotent über `<!--ITC:…-->`).
- Vorstände archiviert: `.tools/_archiv/introtech-sanierung_vor-highend-2026-09-24/`,
  Juli-Zwischenstand `.tools/_archiv/introtech-sanierung_juli2026_unveroeffentlicht/`, Video `_raw/alt-video/`.

**Offen:** Bauwerksabdichtung verlinkt vorerst auf die Sparten-Demo `introtech-abdichtung.vercel.app`
(Domain/Name der Sparte offen). **Referenzen/Einsatzbeispiele** (Schadensfall, Ort, Verfahren,
Vorher/Nachher) und echte Einsatzfotos beim Kunden anfragen: das würde die Seite am stärksten aufwerten.
Ablauf: die 4 Schritte von introtech.de („In nur 4 Schritten wird Ihnen geholfen“) 1:1 übernommen.
Schriften, GSAP und Karte sind lokal (0 Drittanfragen außer den Links auf OSM/WhatsApp);
Datenschutzerklärung vor Livegang auf den echten Hoster (Vercel) anpassen.

## ⚠️ Platzhalter / vor Live-Schaltung klären
- **Bilder:** Stockfotos (Pexels, lizenzfrei; Quellen in `assets/_attribution.txt`) → durch echte
  Fotos von InTroTech ersetzen (Team, Fahrzeuge, Einsätze, Geräte).
- **Karten-Pin:** OSM-Embed grob auf Gifhorn — exakte Koordinaten Zeisigweg 4 final setzen.
- **Kontaktformular:** Demo ohne Backend (Submit zeigt Hinweis) → an Endpoint anbinden.
- **Rechtsseiten vollständig übernommen:** `impressum.html` (echte Registerdaten),
  `agb.html` (komplette AGB inkl. Widerrufsbelehrung, 14 Abschnitte) und `datenschutz.html`
  (vollständige Datenschutzerklärung) — Texte 1:1 von introtech.de übernommen, im Footer verlinkt.
  - ⚠️ Die **Datenschutzerklärung** ist die ursprüngliche (Wix-basierte) Fassung. Sie beschreibt
    teils Wix-Gegebenheiten (Speicherorte USA/Irland/… , „Registrierung", Drittanbieter-Login) und
    deckt die NEUEN Bausteine dieser Seite (Google Fonts, OpenStreetMap-Embed, WhatsApp, geplantes
    Google-Ads/Analytics-Tracking) noch nicht ab. **Vor Live durch den Betrieb / einen Generator
    (z. B. eRecht24) aktualisieren lassen.** Offensichtlicher Fremd-Firmenname im Original
    („TJA Photovoltaik") wurde zu „InTroTech GmbH" korrigiert.
- Keine erfundenen Stats/Bewertungen verwendet.

## Technik
- Statisch, kein Build. Animation: geteilte Motion-Engine `assets/motion.js`
  (GSAP + ScrollTrigger + Lenis via CDN), per `data-`Attributen gesteuert.
- `prefers-reduced-motion` respektiert; nur `transform/opacity/clip-path` animiert.
- Responsiv (Desktop/Tablet/Mobil) inkl. Mobil-Menü (Escape schließt, Body-Scroll-Lock).
- WCAG-AA-Kontraste; Fokuszustände sichtbar; Bilder lokal & optimiert.

## SEO
Eingebaut für gutes (lokales) Ranking:
- **Meta:** sprechender `<title>`, Description, `canonical`, `robots` (index), `author`, **Geo-Meta** (Gifhorn).
- **Open Graph + Twitter Card** (Titel/Description/Bild) für hübsche Vorschauen beim Teilen.
- **Strukturierte Daten (JSON-LD):** `HomeAndConstructionBusiness` mit Adresse, Geo, Telefon,
  Öffnungszeiten, **Einzugsgebiet** (areaServed), Leistungskatalog, USt-ID, Geschäftsführung,
  Instagram (`sameAs`). → Grundlage für Rich Results & Google-Maps/Local-Pack.
- **`robots.txt` + `sitemap.xml`** im Root.
- Saubere Semantik (genau **eine** H1, sinnvolle H2/H3), Alt-Texte, schnelle, kleine Assets.

> **Domain:** `canonical`, `og:url`, `og:image`, `sitemap.xml`, `robots.txt` und das JSON-LD nutzen
> `https://www.introtech.de/`. Bei Deploy auf eine andere Domain (z. B. Vercel-Preview) diese URLs
> anpassen. Nach Live-Schaltung: Seite in der **Google Search Console** verifizieren, Sitemap
> einreichen; **Google-Unternehmensprofil** (Maps) pflegen — das wirkt für lokale Suche am stärksten.

## Google Ads (vorbereitet, noch nicht aktiv)
Die Seite ist eine taugliche Landingpage (klare Headline, mehrere Conversion-Wege: Anruf, WhatsApp,
Formular). **Conversion-Hooks** sind in `script.js` angelegt (`track()`): sie feuern bei Klick auf
Telefon-/WhatsApp-Links und beim Formular-Absenden — **aber nur, wenn ein Google-Tag geladen ist.**
Ohne gesetzte IDs passiert nichts (kein Tracking ohne Setup/Einwilligung).

**Zum Aktivieren brauche ich von dir / sind nötig:**
1. **Google-Ads-Konto** → Conversion-ID + -Label (Format `AW-XXXXXXXXX/XXXXXXXX`); optional **GA4**-Mess-ID (`G-XXXXXXX`).
2. **DSGVO-Einwilligung zwingend:** Consent-Banner (Cookie-Consent) mit **Google Consent Mode v2**
   — Google-Tag erst nach Zustimmung laden/aktivieren. Ohne Consent-Lösung darf in DE kein
   Ads-/Analytics-Tag laufen.
3. Dann: Google-Tag (gtag.js) im `<head>` einbinden und in `script.js` (`track()`) die Conversion-
   Labels eintragen (Beispielzeile ist bereits als Kommentar vorhanden).
- **Call-Tracking:** Telefon-Conversions laufen über die `tel:`-Klicks (bereits verkabelt);
  alternativ Google-Forwarding-Nummer einsetzen.

## Dateien
```
index.html · impressum.html · datenschutz.html · agb.html · styles.css · script.js · README.md
robots.txt · sitemap.xml
assets/  hero.jpg leckageortung.jpg trocknung.jpg sanierung.jpg energieberatung.jpg team.jpg
         motion.js  _attribution.txt
assets/brand/  logo.png  logo-white.png  mark.png
```
Eigenständig deploybar (Vercel: Ordner als statische Site).
