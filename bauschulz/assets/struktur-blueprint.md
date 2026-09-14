# Struktur-Blueprint — BAUSCHULZ GmbH & Co. KG (Phase 1.6, 2026-09-14)

Bau-Vertrag für das Skelett. Farbe/Welt/Typo/Motion: siehe `art-direction.md` (W3 · Archetyp A + gepinntes
Tagebuch · editorial · Signature „Bautagebuch von oben"). Hier nur: WIE navigiert wird, WIE Sektionen einsteigen,
WOMIT Inhalt dargestellt wird, WIE Kontakt/Footer/Galerie gelöst sind, in WELCHER Reihenfolge.

## Struktur-Blueprint: BAUSCHULZ, Bauunternehmen (C2)   (Archetyp A · Welt W3)

- **Nav-Paradigma:** **Topbar + Drawer als zweizeiliger „Bautafel"-Kopf** — weil die Seite ~19 echte
  Unterseiten (8 Projekte, 3 Leistungen, Tagebuch, Über uns, Kontakt, Recht) hat und SEO-intern verlinkt sein
  muss; Minimal/Scroll-Spy tragen keine Multi-Page-Site, Sidebar/Split-Nav wären Klitzke/Jahn (beide Bau-nah).
  Form (Abgrenzung zu MAVA-Material-Kopf und KT38-Erstbau-Mega-Menü): opak, keine Transparenz/Blur, kein Panel,
  kein Suchlayer. **Zeile 1** (Wortmarke · Tel 0176 31482066 als Textlink · CTA „Anfrage") scrollt weg;
  **Zeile 2** (5 Bereiche als Versalien-Leiste: Leistungen · Bautagebuch · Referenzen · Über uns · Kontakt)
  bleibt sticky, Aktivmarke = Füllbalken unter dem Wort (dasselbe Motiv wie die Phasen-Leiste). Keine Dropdowns —
  die 8 Projekte werden über referenzen.html, die Karten-Marker, die LV-Positionen und den Footer-Index erreicht.
  ≤ 880 px: Burger → **Drawer von links** (bisher immer rechts/Bottom-Sheet), Inhalt: 5 Bereiche · Tel-Zeile ·
  Mo–Fr 08–17; `inert` wenn zu, Esc, Fokusfalle. Plus Pflicht-`.wa-fab` (tritt über Formular/Kontakt zurück).

- **Sektions-Kopf:** **Großes Zitat als Sektionsstart** — weil der Betrieb echte Sätze hat (3 Claims, Tagebuch-
  O-Ton, 6 Google-Rezensionen mit Namen). Form: Zitat-Zeile in Bautafel-Versalien mit 2-px-Latte links + Quellen-
  Zeile („— BAUSCHULZ" / „— Google-Rezension, Name") → darunter die sachliche h2 (SEO-Titel) → **kein Lead**.
  Zuordnung (nur Belegtes): Bautagebuch = „So kann's aussehen." · Leistungen = „vom Einfamilienhaus bis Gewerbe."
  (Hero nimmt dann „Saubere Ausführung. Klare Abläufe. Verlässliche Termine." — oder umgekehrt, nie beide doppelt) ·
  Ablauf & Warum = der jeweils nicht im Hero genutzte Claim · Referenzen = erster echter Satz des Wahrenholz-/
  Sassenburg-Rundgang-Textes · Betrieb = „Familienbetrieb, in dem alle mit anpacken." · Rezensionen = eine echte
  Rezension (voll) · Kontakt = „direkte Kommunikation – schnelle Entscheidungen". **Fehlt ein echter Satz → nur h2,
  nichts erfinden.** Abgrenzung zu Hildebrandt (06-19): kein Ich-Erzähler, keine Handschrift — Claims in Versalien.

- **Komponenten (dominant):** **Timeline** (+ Neben-Bauform **Akkordeon**) — weil der Kern-Content chronologisch
  ist: 16 Bauphasen (Signature), 4 Ablauf-Phasen, 8 Referenzen mit Fertigstellungsjahren 2014→2022. EIN Bauteil
  „Phasen-Leiste mit Füllbalken" trägt alle drei: 16 Phasen (Bautagebuch, gepinnt, vertikal) · 4 Phasen (Ablauf,
  horizontal, ungepinnt) · 8 Jahr-Ticks (Referenz-Chronik auf referenzen.html, vertikal). Neben: **LV-Akkordeon**
  „Leistungsverzeichnis" für Leistungen auf index (Pos. 1–5, Pos. 1 offen geladen, Text im DOM). Weitere Neben-
  Elemente (ändern die Achse nicht): 3 „Warum"-Zeilen mit Giebel-A-Marke · Rezensionen als Zeilenliste · EIN
  Split-Block (Teamfoto | Text) im Betriebs-Band. **Kein Karten-Raster, keine Listen als Träger, kein Split-Wechsel.**

- **Kontakt-Lösung:** **Karte als Spalte — als Referenz-Karte** — weil das Einzugsgebiet aus den Referenzen
  belegt ist (Wolfsburg-Ehmen, Wittingen, Knesebeck, Gifhorn, Sassenburg ×2, Wahrenholz + Sitz Triangel): OSM
  regional, **8 Giebel-A-Marker** (7 Projekte mit bekanntem Ort + Firmensitz; Brücke ohne Ort), Marker = Link zur Projektseite (kein Zustandswechsel →
  nicht „interaktiv"), Legende darunter = 8 Projektnamen. Links: Formular wie Original (Name/E-Mail/Betreff/
  Nachricht) + Direktkanäle (Tel groß · WhatsApp · Mail) + Anschrift + Mo–Fr 08–17. Form-Abgrenzung zur alten
  OSM-Kachel: Spalte volle Sektionshöhe, bis an die rechte Viewport-Kante, 3-px-Radius, 2-px-Ink-Kante, keine
  Pin-Pille. OSM lazy.

- **Footer-Form:** **Mega-Footer mit Claim — als „Bautafel"** — weil die Original-Claim-Zeile „BERATUNG – PLANUNG –
  SCHLÜSSELFERTIGER NEUBAU – ABBRUCH" existiert und die Seite wie ein Bauschild abschließt. Vier Zeilen, **keine
  Spalten, kein `<details>`** (Abgrenzung zu MAVAs 3-Zonen/2-Spalten): (1) Claim-Zeile vollbreit in Versalien →
  (2) Anschrift · Tel · Mail · Zeiten in einer Zeile → (3) Seiten-Index als Zeile, darunter die 8 Projekte als
  Unterzeile (SEO) → (4) Legal (Impressum · Datenschutz · ©).

- **Galerie-Form:** **Horizontaler Streifen** — weil 8 Referenzen mit je 1–10 echten Fotos wie eine Bauakte
  durchgeblättert werden. Auf index: Referenzen-Sektion = Streifen der 8 Projekte, chronologisch sortiert, Kachel
  = 1 Foto + Projekt · Ort · Jahr · Fläche, Jahr-Ticks am unteren Rand, scroll-snap, Pfeiltasten, kein Autoplay.
  Auf Projektseiten: Streifen der Projektfotos mit Zähler „03 / 10"; bei 1–2 Fotos stattdessen ein einzelnes
  Bild-Band (Neben-Element). Renderings (nur Wahrenholz, Fotos 4–8) tragen die Kennzeichnung „Visualisierung".
  Die 16 Tagebuch-Bilder sind KEINE Galerie — sie gehören der Signature.

- **Sektions-Spine (index):**
  Hero(Split, Curtain-Reveal, Tel-CTA) → Bautagebuch(gepinnte Timeline, Auszug) → Leistungen(LV-Akkordeon) →
  Ablauf & Warum(Timeline 4 Phasen + 3 Zeilen) → Referenzen(Streifen chronologisch) → Betrieb(dunkles Band, Teamfoto
  2025 | Text, älteres Foto klein) → Rezensionen(großes Zitat + Zeilenliste 5) → Kontakt(Formular | Referenz-Karte-
  Spalte) → Mega-Footer(Bautafel-Claim) + `.wa-fab`

  Signature auf Pos. 2, Über uns auf Pos. 6 — bewusst nicht das Schema Hero→Über→Leistungen→Galerie→Team→Kontakt.
  **Bautagebuch-Auszug auf index:** 8 Kernphasen (Vorschlag: 01 Planung · 02 Fundamente ausheben · 05 Bodenplatte
  betonieren · 06 Mauerwerk EG · 09 Decke betonieren EG · 13 Richtfest · 15 Dach eindecken · 16 schlüsselfertig);
  die Leiste zeigt trotzdem 01–16, ausgelassene Phasen als dünne Striche; Abschluss-Link „Alle 16 Phasen" →
  bautagebuch.html. Pinning nur hier; Reduced-Motion/≤ 880 px: Bild-Text-Paare gestapelt (lt. AD).

## Kopf-Typen der Unterseiten (nicht DK-Typenblatt, nicht KT38-`kopf-*`/`kap`-Slots)

| Seite | Kopf-Typ | Aufbau danach |
|---|---|---|
| **referenzen.html** | **Chronik-Kopf**: h1 + Jahr-Leiste 2014→2022 (Phasen-Leiste-Motiv, 8 Ticks) | vertikale Chronik-Timeline (Jahr-Tick · Foto · Projekt · Ort · Fläche · Link); Brücke ohne Jahr als „Sonderbau" am Ende → Kontakt-Kurzform |
| **8 Projektseiten** | **Bauschild-Kopf**: 1. Projektfoto als vollbreites Band, darunter Projektdaten-Zeile in Bauschild-Logik (Bauvorhaben · Ort · Fläche · Fertigstellung) mit Giebel-A; h1 = Projektname; fehlende Felder (Brücke) entfallen, nichts erfinden | Foto-Streifen mit Zähler → echter Rundgang-Text (Sassenburg, Wahrenholz; sonst nur Daten) → Chronik-Pfeile „vorheriges/nächstes Projekt" (nach Jahr) → Kontakt-Kurzform |
| **bautagebuch.html** | **kein Kopf-Block** — die Seite beginnt direkt mit Phase 01 im Signature-Layout, h1 „So kann's aussehen." sitzt im ersten Phasen-Panel (umgesetzt: `.tb--ohne-kopf`, h1 + Intro im `li[data-n="1"]`) | alle 16 Phasen gepinnt, Leiste 01–16 → Abschluss-Band „Ihr Haus von oben?" → Kontakt-Kurzform |
| **leistungen.html** | **LV-Kopf**: h1 + Claim-Zeile „BERATUNG – PLANUNG – SCHLÜSSELFERTIGER NEUBAU – ABBRUCH" als Zitat-Start | 5 offene LV-Positionen (Pos. 1 Neubau EFH & MFH · Pos. 2 Gewerbe & Industrie · Pos. 3 Sonderbauten · Pos. 4 Abbruch · Pos. 5 Tief-, Pflaster- & Innenbau lt. Register), je Text + 1 Referenzfoto + Referenz-Links; Pos. 4/5 nur Registerzeile (README: Kundentext fehlt) → Kontakt-Kurzform. Kein mitlaufender Index (MAVA). |
| **3 Leistungsseiten** (neubau · gewerbe-industrie · sonderbauten — nur die mit echtem Text) | **LV-Kopf** mit Positionsnummer im h1-Vorspann | echter Text → zugehörige Referenzen als Streifen (Neubau: Ehmen, Wittingen, Knesebeck, Doppelhaus, EFH, Wahrenholz · Gewerbe: Garagenpark · Sonderbau: Brücke) → Kontakt-Kurzform |
| **ueber-uns.html** | **Teamfoto-Kopf**: Teamfoto 2025 vollbreit als Band, h1 darunter | Editorial-Text (2. Generation, alle packen mit an, eigene Mannschaft, GF Denis Schulz) + älteres Foto vor Bagger als zweites Bild (ohne Jahr) → 3 „Warum"-Zeilen → Kontakt-Kurzform |
| **kontakt.html** | **Formular-zuerst-Kopf**: kein Hero, kein Band; h1 „Anfrage" + Direkt-Zeile (Tel groß · WhatsApp · Mail · Zeiten) | dieselbe Zweispalt-Sektion wie index (Formular | Referenz-Karte-Spalte), nicht vollhöhig |
| **impressum / datenschutz** | schmale Lesespalte, h1 + Text | — |

**Kontakt-Kurzform** (alle Unterseiten außer kontakt.html): dunkles Band mit Tel + WhatsApp + Link „Anfrage" —
keine Karte, kein Formular.

## Divergenz-Nachweis vs. Vergleichshorizont

| Achse | Bauschulz | KT38-Redesign (09-12) | DK Fenster (09-05) | KT38-Erstbau (09-08/10) | MAVA (08-13) |
|---|---|---|---|---|---|
| Nav | Topbar + Drawer (Bautafel, links-Drawer) | Overlay ✓ | Bottom-Bar ✓ | Topbar+Mega ✗ (Bucket) | Topbar+Drawer ✗ |
| Sektions-Kopf | großes Zitat | Kein-Eyebrow+Chip ✓ | eyebrow→h2→lead ✓ | Frage+Mono ✓ | Marginalie ✓ |
| Komponenten | Timeline (+Akkordeon) | Karten-Raster ✓ | Split-Wechsel ✓ | Listen ✓ | Fließtext ✓ |
| Kontakt | Karte als Spalte (Referenz-Karte) | Vollbild-Karte ✓ | interaktiv ✓ | Karte als Band ✓ | keine Karte ✓ |
| Footer | Mega-Footer mit Claim | 4-Spalten ✓ | einzeilig ✓ | Kontaktband ✓ | Mega-Footer ✗ |
| Galerie | horizontaler Streifen | Bento ✓ | Vollbild-Slider ✓ | keine ✓ | keine ✓ |
| **abweichend** | | **6/6** | **6/6** | **5/6** | **4/6** |

- Spine ≠ letzte 3 (KT38-R: Hero→Räume→Rechner→…→VB-Karte→4-Sp · DK: Hero→Sortiment→Fenster→…→Anfrage(Schalter)
  · KT38-E: Hero→Vertrauensband→Wege→Rechner→…→Kontaktband) und ≠ MAVA: **✓** (anderes Set, andere Reihenfolge,
  Signature auf Pos. 2).
- Nav & Kontakt ≠ unmittelbar vorheriger Build (KT38-R: Overlay · Vollbild-Karte): **✓ / ✓**.
- ≥ 4/6 gegen jeden der letzten 2 Builds: **6/6 (KT38-R) · 6/6 (DK) · 5/6 (KT38-E)**; selbst gegen MAVA 4/6.
- Gesperrte Buckets (3 Sperr-Blöcke): keiner belegt — Topbar-Bucket laut Register seit KT38-R wieder frei.
- Kopf-Typen: kein einheitlicher bildloser Typenblatt-Kopf (DK), keine Slot-Karten/Bühnen-Köpfe (KT38-R), keine
  `kopf-*`-Klassen (KT38-E), kein mitlaufender Index (MAVA leistungen).
- Plausibilität: Topbar trägt 19 Seiten · Zitat-Kopf nutzt nur belegte Sätze · Timeline = eine Leiste in drei
  Größen (16/4/8) · Karte zeigt belegte Bauorte · Footer = Original-Claim-Zeile · Streifen = Bauakte.

## Angenommen (nicht aus Quellen)
- Leistungs-Unterseiten nur für die 3 Felder mit echtem Text; Abbruch + Tief-/Pflaster-/Innenbau bleiben Positionen
  auf leistungen.html (README-Platzhalter „Text vom Kunden").
- Auswahl der 8 Kernphasen für den index-Auszug ist ein Vorschlag; Reihenfolge/Nummern der 16 bleiben Original.
- Brücke: keine Projektdaten → Bauschild nur mit „Sonderbau · Brücke", ohne Jahr/Fläche.
- Referenz-Karte: Koordinaten der Bauorte auf Ortsebene (kein Straßenpin an fremden Objekten).

## Register-Struktur-Notiz (für Phase 8, nach QA-BESTANDEN in `kunden-website-register.md` einfügen)

| BAUSCHULZ GmbH & Co. KG | **Topbar + Drawer als zweizeiliger „Bautafel"-Kopf** (Zeile 1 Wortmarke·Tel·CTA scrollt weg, Zeile 2 = 5 Bereiche sticky mit Füllbalken-Aktivmarke; opak, kein Blur/Panel/Suchlayer; ≤ 880 px Drawer von LINKS, `inert`) + `.wa-fab` | **Großes Zitat als Sektionsstart** (echte Claims/O-Ton/Rezensionen in Bautafel-Versalien + Quellen-Zeile → h2, kein Lead) | **Timeline** — EINE Phasen-Leiste mit Füllbalken in 3 Größen: 16 Phasen gepinnt (Signature) · 4 Ablauf-Phasen · 8 Jahr-Ticks Referenz-Chronik (+ LV-Akkordeon Pos. 1–5, Warum-Zeilen, Rezensions-Zeilenliste, 1 Team-Split) | **Karte als Spalte — Referenz-Karte** (OSM regional, 8 Giebel-A-Marker = 7 Bauorte + Sitz, Marker → Projektseite, Legende; neben Original-Formular + Direktkanäle; kantig, keine Pin-Pille) | **Mega-Footer mit Claim als „Bautafel"** (Claim-Zeile vollbreit → Kontakt-Zeile → Seiten-Index + 8-Projekte-Unterzeile → Legal; keine Spalten, kein `<details>`) | **Horizontaler Streifen** (index: 8 Referenzen chronologisch mit Jahr-Ticks; Projektseiten: Fotos mit Zähler; Tagebuch-Bilder = Signature, keine Galerie) | Hero(Split,Curtain)→Bautagebuch(gepinnte Timeline, 8/16 Auszug)→Leistungen(LV-Akkordeon)→Ablauf&Warum(Timeline 4+3 Zeilen)→Referenzen(Streifen)→Betrieb(dunkles Band, Teamfoto)→Rezensionen(Zitat+Zeilenliste)→Kontakt(Formular\|Referenz-Karte-Spalte)→Mega-Footer(Bautafel) · **Kopf-Typen:** Chronik-Kopf (referenzen) · Bauschild-Kopf (8 Projekte) · kein Kopf/Phase 01 (bautagebuch) · LV-Kopf (leistungen + 3 Leistungsseiten) · Teamfoto-Kopf (ueber-uns) · Formular-zuerst (kontakt) · Lesespalte (Recht) |

> **Für die nächsten 2 Builds gesperrt (Stand Bauschulz 2026-09-14):** Topbar + Drawer (jede Ausprägung) ·
> großes Zitat als Sektionsstart · Timeline als dominante Bauform · Karte als Spalte · Mega-Footer mit Claim ·
> horizontaler Streifen · Archetyp A (Split-Hero) · Motion editorial.
