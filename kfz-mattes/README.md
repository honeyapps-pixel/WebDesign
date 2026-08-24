# KFZ-Meisterwerkstatt Mattes — Demo-Website

Statische Demo (HTML/CSS/JS) für **KFZ Mattes**, freie Kfz-Meisterwerkstatt in Isenbüttel (Landkreis
Gifhorn), gegründet **1964**. Verkaufs-Demo (`MODE=demo`) — echte Inhalte von der Originalseite
[kfz-mattes.de](https://kfz-mattes.de), Stock-Bilder nur als Lückenfüller.

## Art-Direction
- **Welt:** W8 Vintage-Analog / Heritage-Werkstatt · **Archetyp A** (Editorial-Split) · **Motion** `mechanical`.
- **Signature:** „Werkstatt-Instrument" — Mini-Dial-Sektionsmarker + „seit 1964"-Emaille-Stempel.
  **Hero:** echtes Team-Gruppenfoto (Crew an der Hebebühne, Original-Asset) gestapelt unter der Headline.
- **Marken-Anker (verankert):** Blau **#0F79B3** (aus dem echten Logo gesampelt), Ink #16202B, kühles
  Werkstatt-Papier #ECEEF0. Fonts: Big Shoulders Display (Signage) · Public Sans · Space Mono.
- Details: `assets/art-direction.md`, Skelett: `assets/struktur-blueprint.md`.

## Struktur (Blueprint)
Bottom-Bar-Nav (Anrufen · Route · WhatsApp) + schlanke Topbar · Frage-Headlines + Mini-Dials ·
Preis-Listen mit Dotted-Leader · Reifen-Aushang-Tabelle · Mobilitäts-USP als Split · interaktiver
**Standort-Umschalter** (Liststraße 1 ↔ Am Wendehof 1) · einzeiliger Footer · keine Stock-Galerie.

## Echte Daten (aus Originalseite/Impressum übernommen)
- **KFZ-Werkstatt Mattes**, Inhaber Rudi Mattes, Geschäftsführung Anja Mattes.
- Standorte: **Liststraße 1** & **Am Wendehof 1**, 38550 Isenbüttel.
- Tel **05374 1626** · Fax 05374 1691 · **info@kfz-mattes.de** · Facebook /KfzMattes.
- Öffnungszeiten: Mo–Fr 08:00–17:00 (Mittagspause 12:00–13:00).
- Leistungen, Festpreise (Reifen/Frühjahr-Check) und USP **Mobilitäts-Zentrum** 1:1 von der Originalseite.

## ⚠️ Platzhalter / vor Verkauf zu bestätigen
- **WhatsApp-Link** nutzt die Festnetznummer (`wa.me/4953741626`, WhatsApp Business) — ✅ bestätigt: Festnetz = WA-Nummer.
- **Karten-Marker:** Beide Standorte liegen laut Geocoding praktisch am selben Punkt in Isenbüttel
  (52.4370, 10.5709); exakte Koordinate „Am Wendehof 1" ggf. nachschärfen.
- **Bilder:** Teamfoto, die acht Einzelportraits (`assets/portraits/`), `assets/buero.jpg` und
  `assets/werkstatt.jpg` sind **echte Kundenfotos aus der Lieferung 08/2026** (Fotografin
  **fotosvonaylin**, Credit als `figcaption` am Teamfoto). Von **Rudi Mattes** gibt es kein Foto und
  wird keins geben — seine Team-Karte trägt ein Monogramm. `assets/mobility.jpg` ist Original-Asset
  von kfz-mattes.de; `assets/service.jpg` + `assets/tires.jpg` sind **echte Kundenfotos** (Anhang 01/02,
  07/2026) und bleiben eingebunden — die frühere README-Angabe „Pexels-Stock" war falsch.
  Maßgeblich ist `assets/_attribution.txt`.
- **Referenzen/Arbeitsproben (C2-Pflicht-Inhalt) fehlen** — das Original ist bildarm und zeigt keine
  dokumentierten Arbeiten; nach Verkauf Fotos echter Aufträge nachliefern (Phase 10).
- **Michelle Braschoß** ist laut Originalseite „Bürokauffrau – Angebotserstellung"; ihre Zuordnung als
  Kontakt im Mobilitäts-Block beim Kunden bestätigen (aktuell neutral als „Angebote & Kostenvoranschläge").
- **Rechtsseiten:** `impressum.html` + `datenschutz.html` wurden 1:1 von kfz-mattes.de übernommen und
  auf die Demo-Technik angepasst (OpenStreetMap statt Google Maps; YouTube-/ReCaptcha-/FB-Plugin-Absätze
  entfernt, da nicht eingebunden). Vor Go-Live vom Kunden/Anwalt prüfen lassen.
- **og:image** zeigt auf `https://kfz-mattes.vercel.app/assets/og.jpg` — ✅ beim Deploy angepasst.

## Lokal ansehen
```
open index.html      # oder: python3 -m http.server 8000
```
Eigenständig deploybar (`assets/motion.js` liegt im Ordner). GSAP/Lenis via CDN.
