# Mobilitäts-Zentrum Mattes — Behindertengerechter Fahrzeugumbau

Statische Website (HTML/CSS/JS) für den behindertengerechten Fahrzeugumbau der KFZ-Meisterwerkstatt
Mattes in Isenbüttel. **Schwester-Seite zu `kfz-mattes/` — bewusst im gleichen Marken-Stil**
(Familien-Wiedererkennung, Kundenwunsch), aber mit eigenem Skelett.

## Design (Familien-Stil = kfz-mattes)
- Marken-Blau **#0F79B3**, kühles Werkstatt-Papier, scharfe 3px-Kanten, **Mini-Dial-Sektionsmarker**,
  **Emaille-Stempel**, `data-motion="mechanical"`. Fonts **Big Shoulders Display + Public Sans + Space Mono**.
- `styles.css`/`script.js` = Kopie von kfz-mattes + eigener CSS-Block. Brief: `assets/art-direction.md`.
- **Eigenes Skelett** (kein Klon): Split-Hero (Fahr-Motiv), bildgeführte Leistungs-Reihen, Team-Streifen,
  2 statische Standort-Karten, kein Bottom-Bar.

## Seiten (7)
- `index.html` — Hero · Philosophie · Leistungen (4 Reihen + „Mehr erfahren") · Führerschein · Finanzierung
  · Team · **Schwester-Betrieb (Verweis auf die KFZ-Meisterwerkstatt)** · Kontakt (2 Standorte + Karte)
  · Partner-Logo-Strip.
- `fahrhilfen.html` — **kompletter Fahrhilfen-Katalog**: Handbediengeräte (Veigel Basic/Classic II/Compact II/
  Tetra/Joystick), Lenkhilfen (Drehknopf/Dreizack/Lenkradgabel), Links-/Fußgas/Pedale/Hebel,
  Fahrschul-Doppelbedienung, Einstieg/Sitze/Verladung, Spiegel — mit allen Originaltexten.
- `multifunktionsdrehknopf.html` — SmartSteer Classic & Premium (5/8).
- `partner.html` — 6 Partner-Logos (Veigel, AMF-Bruns, Bever, AlphaDynamik, Rausch, Autolift).
- `bildergalerie.html` — 35 echte Fotos (Werkstatt, Team, Umbauten, Maskottchen Amy).
- `impressum.html` · `datenschutz.html` (beide `noindex,follow`, daher nicht in der Sitemap).

**Auf Kundenwunsch entfernt (2026-07):** Scooter-Unterseite sowie die Partner Mobilis, WETAC und KIVI.
Der Scooter-Block auf `index.html` bleibt als Leistungshinweis ohne Unterseite — laut
Anweisungs-Screenshot `Scooter_Homepage.jpg` bewusst OHNE Modellliste: Überschrift „Scooter",
ein Satz (6–15 km/h), ein Punkt „verschiedene Modelle". Keine M-Modellnamen einbauen.

## Verlinkung der beiden Mattes-Seiten (Angebotsleistung)
Gegenseitig, in beide Richtungen — Stand 2026-07-17:
- **MZM → KFZ:** Schwester-Block vor dem Kontakt (`.sister-sec`, Bild `assets/kfz-werkstatt.jpg` =
  Kopie von `kfz-mattes/assets/service.jpg`) · Inline-Link im Philosophie-Text · Footer **aller 7 Seiten**.
- **KFZ → MZM:** Mobilitäts-Block auf der Startseite (Badge + Banner + Button) · Footer **aller 3 Seiten**.

Die Leistungen im Schwester-Block (Inspektion, TÜV Nord, Klimaservice, Reifen) sind von der KFZ-Seite
übernommen — nicht erfunden. Beim Ändern dort bitte hier nachziehen.

## Bilder
**Alle Original-Bilder übernommen** (Quelle: behindertengerechter-fahrzeugumbau.de), optimiert in
`assets/produkte` · `assets/scooter` · `assets/partner` · `assets/team` + Logo/Hero.
Kein Stock verwendet. Rohbestand-Archiv unter `_orig/` (nicht deployen, via `.vercelignore`).

**Kunden-Anhang (Ordner „MZM", 2026-07): alle 20 Fotos eingebaut**, Zuordnung laut den mitgelieferten
Anweisungs-Screenshots (`01. Handbedienung`, `04. Fahrschule`, `05. Einstieg, Sitze`, `06. Detaillösungen`)
geprüft und bestätigt — Foto 001–003 = Veigel eClassic III, 004–008 = Fahrschul-Umrüstung,
009–011 = Sitze/Verladung, 012–018 = Detaillösungen, 019 = Caddy-Heckausschnitt, 020 = Scooter S700.
**Nachlieferung 2026-07-17:** 2 Fotos **Veigel MyCommand** (Multifunktionsdrehknopf, 8 Tasten) →
`veigel-mycommand.jpg` + `veigel-mycommand-nah.jpg` — ersetzen die doppelten SmartSteer-Premium-8-Karten
auf der Drehknopf-Seite und das falsche „Command Veigel"-Bild (Mercedes-Interieur) in Fahrhilfen 02.

**Foto-Credit:** Teambild (`assets/team.jpg`), Einzelportraits (`assets/portraits/*.jpg`) sowie
`buero.jpg` / `werkstatt.jpg` stammen aus der Kunden-Lieferung 08/2026 (WeTransfer „Fotos Homepage"),
Fotografin **fotosvonaylin** — Credit steht als `figcaption` am Teamfoto und muss dort bleiben.
(Vorher: © Michael Uhmeyer / KURT Media, ersetzt am 2026-08-18.) Von **Rudi Mattes** existiert kein
Foto und wird keins geben (Kundenauskunft) — seine Team-Karte trägt ein Monogramm statt eines Bildes.

## Echte Daten — vom Kunden bestätigt
Inhaber Rudi Mattes · GF Anja Mattes · Team Rudi, Anja, Michelle Braschoß, Vitali, Marcel, Carine Klein,
**Levin und Jamie** (die letzten beiden von Michelle nachgereicht, nicht auf dem Teamfoto — bestätigt).
Liststraße 1 & Am Wendehof 1, 38550 Isenbüttel · Tel 05374 1626 · Fax 05374 1691 · info@kfz-mattes.de.
Werkstatt Mo–Fr 08–17 Uhr (Mittag 12–13); **Mobilitäts-Zentrum Mo–Fr 09–16 Uhr; Firmenadresse Am Wendehof 1,
Eingang über die KFZ Werkstatt Mattes, Liststraße 1 — Route zeigt bewusst zur Liststraße**
(Kundenvorgabe 2026-07-17). Steuer-Nr 19/126/05615 · Amtsgericht Hildesheim HRA 100145 ·
**USt-IdNr DE115210472** (vom Kunden bestätigt).
**„Seit 2010 · Mobilitäts-Zentrum"** im Hero ist Kundenvorgabe (Anweisungs-Screenshot
`Startseite_Homepage.jpg`: „Eigen/Verlade-Entwicklung" rot durchgestrichen → „Seit 2010"; Jahr bestätigt).

## ⚠️ Offen / vor Go-Live
- **Impressum unvollständig:** zuständige **Handwerkskammer** + **gesetzliche Berufsbezeichnung**
  (+ Staat der Verleihung) + Verweis auf die Handwerksordnung fehlen (§ 5 DDG). Angaben stehen bei
  Michelle aus.
- WhatsApp nutzt die Festnetznummer (bei Mattes bestätigt: Festnetz = WA).
- og:image = Logo-Banner; für Social ein 1200×630-Bild nachlegen.
- Rechtsseiten (Impressum/Datenschutz) anwaltlich prüfen lassen.
- Scooter-Modellfotos sind Hersteller-Beispielbilder (wie im Original); Prospekt auf Anfrage.
- 2 weitere Partner-Logos vom Kunden angekündigt.
- Motto-Bild (`hero-freiheit.jpg`) liegt nur in 315×200 vor — Original beim Kunden anfragen.

## Datenschutz (Stand Juli 2026)
Keine Cookies, kein Tracking, keine Formulare. Fonts und GSAP/Lenis liegen **lokal** in `assets/`.
Die OSM-Karte lädt **erst nach Klick** (Zwei-Klick-Lösung). Gemessen: **0 externe Requests** beim Seitenaufruf.

## Lokal ansehen
```
open index.html   # oder: python3 -m http.server 8000
```
Eigenständig deploybar (`assets/motion.js` + GSAP/Lenis liegen lokal in `assets/js/`).
`_orig/` und `*.md` werden beim Deploy via `.vercelignore` ausgeschlossen.
