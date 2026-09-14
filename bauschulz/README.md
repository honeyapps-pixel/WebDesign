# BAUSCHULZ GmbH & Co. KG — Demo-Website (Honeyapps)

**Betrieb:** BAUSCHULZ GmbH & Co. KG (Komplementärin: BAUSCHULZ Verwaltungs GmbH) · Geschäftsführer Denis Schulz
**Adresse:** Fehringstraße 8, 38524 Sassenburg (Ortsteil Triangel), Landkreis Gifhorn
**Telefon:** 0176 31482066 (mobil) · **E-Mail:** info@bauschulz.com
**Original-Website:** https://bauschulz.com (WordPress, Theme „Roof", Stand 2021/22)
**Zweiter Fundort:** https://bauschulz2.hawker-group.de — unfertiger Relaunch-Entwurf eines anderen Anbieters
(Elementor, viele Template-Reste), aber mit echten Kundentexten und neuen Fotos (2024/25).
**Status:** `MODE=demo` — Verkaufs-Demo, **LIVE: https://bauschulz.vercel.app** (deployed 2026-09-14, Repo `honeyapps-pixel/WebDesign`); kein Angebot versendet. Kundenauftrag (Demo zuerst).

Bauen: `python3 .tools/bs_gen.py` erzeugt alle 19 HTML-Seiten aus einer Content-Quelle (Kopf/Fuß/Kontakt-Kurzform
identisch). Danach `python3 .tools/site_check.py bauschulz`. Vorschau: `cd bauschulz && python3 -m http.server 8790`.

---

## Herkunft der Inhalte (nichts erfunden)

| Übernommen | Quelle |
|---|---|
| **Logo** (Wortmarke, „A" = orangefarbener Giebel) + Icon | bauschulz.com (`Logo_Bauschulz-2022_web-01.png`, `cropped-Logo_Bauschulz-A-Icon`) → `assets/brand/` (helle Fassung für Dunkelflächen abgeleitet) |
| **Markenfarben** | 1:1 aus dem Logo gesampelt: Anthrazit **#353534**, Orange **#E88507** (WordPress-Theme-Color war #f18b0d). Orange läuft **nie als Text auf hellem Grund** (2,4:1) — nur als Fläche (CTA mit dunkler Schrift), Linie/Latte, Giebel-Marker, Füllbalken, Hero-Unterstrich; auf dunklem Grund als Text (5,8:1) |
| **Claim-Zeile** „Beratung – Planung – Schlüsselfertiger Neubau – Abbruch" | bauschulz.com, Startseite |
| **Hero-/Sektions-Claims** „vom Einfamilienhaus bis Gewerbe.", „Saubere Ausführung. Klare Abläufe. Verlässliche Termine.", „Bauunternehmen in 2. Generation", „bauen in Tradition & Moderne" | Relaunch-Entwurf, wörtlich (als Zitate geführt) |
| „ein Familienbetrieb, in dem alle mit anpacken", „oft mit eigener Mannschaft" | Firmenbeschreibung in Branchenverzeichnissen/Suchergebnis-Snippet (Bauunternehmen im Hochbau in zweiter Generation … Familienbetrieb, in dem alle mit anpacken … oft mit eigener Mannschaft) — **nicht als Zitat geführt**, als Aussage übernommen; Wortlaut vom Kunden bestätigen lassen |
| **Leistungen** (Neubau EFH/MFH · Gewerbe & Industrie · Sonderbauten) mit Text | Relaunch-Entwurf, wörtlich |
| **Pos. 05** „Hoch- und Tiefbau, Trocken- und Innenbau, Pflaster- und Gartenarbeiten" | Unternehmensgegenstand lt. Handelsregister (HRA 202485) |
| **„Warum BauSchulz"** (3 Punkte) + **Ablauf** (Erstgespräch & Bedarf → Angebot & Zeitplan → Ausführung & Abstimmung → Abnahme) + „Jedes Projekt ist für uns einmalig und individuell." | Relaunch-Entwurf, wörtlich |
| **Bautagebuch** (16 Phasen, O-Ton + 15 Drohnen-Senkrechtaufnahmen) | Relaunch-Entwurf, Seite „So kanns aussehen" — Texte leicht korrekturgelesen (Rechtschreibung, keine inhaltliche Änderung); Phase „Schlüsselfertig" beschreibt nur, was das Foto zeigt. Bild↔Phase nach Bildinhalt zugeordnet (im Entwurf zwei Bilder doppelt) |
| **8 Referenzen** mit Projekt · Ort · Fläche · Fertigstellung + Beschreibungen/Stichpunkten + **alle Fotos** | bauschulz.com `/portfolio/…` (7 Projekte) + Relaunch-Entwurf (Brücke, Drohnenfotos Wahrenholz). „Senjorenwohnanlage" → „Seniorenwohnanlage", „Balken" → „Balkon" (Tippfehler im Original) |
| **Teamfotos** | Relaunch-Entwurf (`DSC00316.jpg`, 2025, 5 Personen vor der Halle) + bauschulz.com (`DSC07344.jpg`, 3 Personen vor Bagger/Radlader) |
| **Google-Rezensionen** (6, mit Namen) | Relaunch-Entwurf, Abschnitt „Erfahrungsberichte" — Wortlaut/Namen wie dort |
| **Impressum** | bauschulz.com `/impressum/`, wörtlich (HRB 207363 / HRA 202485, USt DE341873217, StNr 19/201/05082) |
| **Datenschutz** | Relaunch-Entwurf (Hosting All-Inkl), ergänzt um OSM-Karte, Leaflet via cdnjs, mailto-Formular, WhatsApp |
| **Öffnungszeiten Mo–Fr 08–17** | Google-Eintrag / 11880 / hanse-immobilien (alle drei stimmen überein) |

**Kein Stock-Bild.** Alle 60 Motive stammen vom Betrieb (Fotos, Drohnenaufnahmen, Renderings). Renderings gibt es
nur bei Wahrenholz (Fotos 4–8; Fotos 1–3 sind Drohnenaufnahmen) — auf der Seite als **„Visualisierung"** gekennzeichnet.
Die Ehmen-Bilder sind echte Fotos (WhatsApp-Uploads des Betriebs). Alle Bildunterschriften beschreiben nur, was im Bild zu sehen ist.

## Design-Entscheidungen (kurz)
- Kreativ-Brief: `assets/art-direction.md` · Struktur-Blueprint: `assets/struktur-blueprint.md`.
- **Signature „Bautagebuch von oben":** gepinnte Drohnenbühne mit Phasen-Leiste 01–16 (Startseite: 8 von 16 als
  Auszug, `bautagebuch.html`: alle 16). Mobil ≤ 880 px: Bild-Text-Paare gestapelt, darüber eine sticky Phasen-Leiste (16 Balken + Füllbalken + „Phase 07 Mauerwerk kleben"); Reduced-Motion: keine Überblendungen, alles sichtbar.
- Schriften **Sofia Sans Extra Condensed / Condensed / Sofia Sans** lokal in `assets/fonts/` (OFL), kein Google-CDN.
- GSAP/ScrollTrigger/Lenis + `assets/motion.js` lokal (`data-motion="editorial"`). Einzige Fremd-Origins:
  **tile.openstreetmap.org** (Karte) und **cdnjs.cloudflare.com** (Leaflet 1.9.4, lazy erst beim Scrollen zur Karte).
- **Referenz-Karte** (Kontakt): 8 Giebel-Marker = Firmensitz + 7 Bauorte auf Ortsebene (Nominatim; Brücke ohne bekannten Ort), Marker → Projektseite.
- **Formular** ohne Backend: öffnet das E-Mail-Programm mit vorbereiteter Nachricht (`mailto:`). Vor Live an ein
  Postfach/Formular-Dienst anbinden — oder so lassen (DSGVO-schlank).

## ⚠️ Offene Punkte (vor Verkauf/Deploy mit dem Kunden klären)

| Punkt | Status | To-do |
|---|---|---|
| **Adresse** | ✅ Fehringstraße 8 (Impressum + Register) | Die alte Startseite zeigt noch „Alte Mühle 1" und Template-Platzhalter („(1001) 888 123 4567", „144 FF Designer Street") — im Gespräch erwähnen |
| **Samstag** | ⚠️ widersprüchlich (09–12 vs. 10–15 in Verzeichnissen) | bestätigen; solange nur Mo–Fr genannt (auch im JSON-LD) |
| **„2. Generation" / „über 30 Jahre" / „25 Jahre"** | ⚠️ | „2. Generation" steht im Kundenentwurf → übernommen. Jahreszahlen („25 Jahre", „seit 1983", Zähler 0/0/0) waren Template-Reste → **bewusst nicht** übernommen. Gründungsjahr erfragen |
| **Pos. 04 Abbruch / Pos. 05 Tief-/Innenbau/Pflaster** | ⚠️ nur ein Satz | Kundentext fehlt; Pos. 04 stützt sich auf die Claim-Zeile („Abbruch"), eine Google-Rezension („inklusive Abriss") und die Brücken-Fotos; Pos. 05 auf den Registergegenstand. Text + Fotos anfordern |
| **Brücke (Sonderbau)** | ⚠️ ohne Daten | Ort, Jahr, Auftraggeber, Bauart erfragen; Text beschreibt nur, was die Drohnenfotos zeigen |
| **Rezensionen** | ⚠️ aus dem Entwurf | Link „Alle Rezensionen bei Google ansehen" zeigt auf eine Google-Maps-Suche nach dem Betrieb — durch den direkten Profil-Link (Google-Unternehmensprofil → „Rezensionen teilen") ersetzen; Sterne/Anzahl bewusst nicht genannt |
| **Facebook** | ✅ facebook.com/BauschulzGmbH (existiert; im Footer + JSON-LD) | Instagram/LinkedIn/Xing-Icons im Entwurf hatten keine echten Links → weggelassen |
| **WhatsApp** | ⚠️ angenommen (Mobilnummer 0176) | bestätigen, ob WhatsApp genutzt wird; sonst FAB entfernen |
| **Team** | ⚠️ ohne Namen | Namen/Funktionen der 5 Personen auf dem Teamfoto erfragen (Entwurf hatte nur Template-Namen „John Smith") |
| **Bautagebuch-Objekt** | ℹ️ | Ort/Jahr des dokumentierten Einfamilienhauses erfragen (könnte als Referenz verlinkt werden) |
| **Datenschutz/Impressum** | ⚠️ Entwurf | juristisch prüfen lassen (Hosting-Angabe All-Inkl stammt aus dem Kundenentwurf — prüfen, ob es beim Deploy so bleibt) |
| **Hoster-Wechsel** | ℹ️ | Demo ist statisch (Vercel-fähig); Live-Betrieb bei bauschulz.com erfordert DNS-Umstellung |

**Nichts erfunden:** kein Gründungsjahr, keine Mitarbeiterzahl, keine Projektanzahl, keine Zertifikate,
keine Garantien, keine Preise, keine Zeitversprechen (die „8 Monate"/„5–6 Monate" stehen nur als Zitat in Rezensionen).

## QA (Stand 2026-09-14)
- `site_check.py`: 0 FAIL · 0 WARN (19 Seiten). `impeccable detect`: nur bekannte Struktur-/Marken-FPs
  (cramped-padding bei Vollbreite-Sektionen mit `.wrap`, all-caps auf Labels/Zitat-Headlines, cream-palette = W3-Grund,
  tight-leading = Display-Typo, numbered-section-markers = Struktur-Achse, clipped-overflow = `overflow-x:clip`).
- Sweep 19 Seiten × 15 Breiten (320–1920): kein Overflow, keine JS-Fehler (`.tools/bs_sweep.mjs`).
- Funktionstest (`.tools/bs_func.mjs`): Wheel-Scroll mit Lenis → 0 versteckte Reveals · Drawer (inert/Esc/Fokus/Scroll-Lock) ·
  Reduced-Motion (Curtain/Puls/Fill aus, alles sichtbar) · Tab-Reihenfolge inkl. Skip-Link · Akkordeon · Formular (mailto).
- Motion-Gate (`motion-standards.md`): nur transform/opacity/clip-path, Eintritte `ease-out`, Hover hinter `hover:hover`,
  Reduced-Motion überall; einziger Dauerläufer = WhatsApp-Puls (Hausregel).
- 4-Agenten-Panel: **struktur-divergenz BESTANDEN** (R1+R2, 6/6 Achsen vs. KT38-Redesign und DK) · **web-design BESTANDEN** (R4,
  Fokusring ≥ 6,98:1, Hero 2-zeilig ab 1100 px, CTA im Fold bis 1366×700) · **anti-ai** nach 5 Runden (Copy-Dopplungen, Quellen-
  Sprache, Bildunterschriften gegen jedes Foto geprüft; alle Befunde umgesetzt) · **ui-layout** nach 5 Runden (Ablauf/Bauschild-
  Breakpoints, Plan-Panel, Sprungmarken-Offset, FAB-Rücktritt generisch, Drawer-Scroll-Lock). Details im Register-Eintrag.
- OG-Bild `assets/og.jpg` 1200×630 (Drohnenfoto + Wortmarke); Projektseiten nutzen ihr Titelfoto. JSON-LD: GeneralContractor
  (index, kontakt) + BreadcrumbList (alle Unterseiten).
