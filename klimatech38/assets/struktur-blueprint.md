> ⚠️ **ACHTUNG — dieser Abschnitt beschreibt den Erstbau (Phase 1.6, Sept. 2026) und ist
> in Teilen ÜBERHOLT.** Verbindlich ist der Stand nach den beiden **Nachträgen vom
> 2026-09-10** am Ende der Datei: Nav = Topbar + Mega-Menü (nicht feste Sidebar),
> Footer = Kontaktband (nicht Sidebar-Footer), Divergenz gegen MAVA = **4/6** (nicht 5/6).
> Alles unterhalb bis zum ersten Nachtrag bitte nur als Entstehungs-Dokumentation lesen.

# Struktur-Blueprint — KlimaTech38 (Geschäftsbereich der InTroTech GmbH)
**Phase 1.6 · geplant vom `struktur-architekt` · verbindlich für Bau und QA-Gate (Phase 8)**
Branche: C2 (SHK/Klima) mit C5-Andockung (Shop) · Archetyp C · Welt W2 · Motion mechanical
Signature: Kältekreis-Linie (aus Phase 1.5, nicht verhandelbar)

Strukturprägend ist der Content: **kein einzelner Leistungskatalog, sondern drei Stränge** —
01 Klima (blau) · 02 Energie (grün) · 03 Shop/Selbsteinbau (blau) — plus der Auslegungs-Rechner,
der laut Kreativ-Brief das Herz der Seite ist, nicht Shop-Gimmick.

## Die 7 Achsen
1. **Nav-Paradigma — feste Sidebar („Anlagen-Rail")** + Mobil-Strang-Segmentleiste.
   Die Rail-Linie IST die Kältekreis-Linie; jeder der 5 Einstiege ist ein Anschlusspunkt
   (Innengerät-Marker), strang-farbcodiert. Aktivmarke = gefüllter Punkt. CTA am Rail-Fuß.
   Kein Burger, kein Drawer, kein Overlay, keine Bottom-Bar — nichts klappt zu.
   < 1080 px: sticky zweizeilige Strang-Leiste (5 Mono-Segmente + CTA-Zeile).
   Rail ist Rand, nicht Layout-Hälfte → Archetyp C (zentrierte Spalte, 1180) bleibt intakt.
2. **Sektions-Kopf — Frage-Headline** (h2 = echte Kundenfrage) + einzeilige **Mono-Antwortzeile**
   mit dem harten Wert. Kein Eyebrow, kein Lead-Absatz, keine Nummern-Kapitel.
3. **Komponenten — dominant Listen/Tabellen** (Spec-Zeilen), Neben-Bauform **Step-Ablauf**:
   Maßnahmen-Register (6, grün) · Ausweis-Tabelle · Split/Multi-Split-Vergleichstabelle (blau) ·
   Shop-Spec-Zeilen (Set │ Leistung │ Raumgröße │ Preis │ Aktion) · Steps 1–5 · Nachweis-Zeilenliste.
   **Kein Karten-Raster** als tragende Bauform, auch nicht für die Shop-Sets.
4. **Kontakt — Karte als Band.** Kontaktdaten zentriert darüber; darunter schmaler Vollbreite-Streifen,
   in dem die Kältekreis-Linie horizontal weiterläuft und die 6 echten Einzugsorte als Mono-Marker trägt.
   Keine OSM-Kachel mit Pin-Pille, keine Karte als Spalte, kein Standort-Umschalter.
5. **Footer — Sidebar-Footer** (Rail-Fuß). Mobil: gestapelter Rail-Block am Seitenende
   (linke Haarlinie), nicht 3-spaltig, nicht einzeilig-minimal.
6. **Galerie — keine.** Neue Sparte ohne eigene Referenzfotos; Galerie wäre Stock-Deko oder
   implizite Referenz-Lüge. Bilder nur funktional: Hero · Gerätefoto in der Spec-Zeile ·
   Strichzeichnung Split/Multi-Split. Keine Masonry, kein Slider, keine Bildbänder als Trenner.
7. **Sektions-Spine (index)** — *überarbeitet 2026-09-08 nach Kundenfeedback („drei Themenbereiche")*
```
Hero(zentriert) + Bereichs-Dreiklang(3 Haarlinien-Zeilen, strang-farbcodiert, je ein Einstieg)
→ Auslegung(Rechner-Panel, Pos. 2) → 01 Klima(Vergleichstabelle + Steps 1–5)
→ 02 Energie(Ausweis-Tabelle + Maßnahmen-Register 6) → PV-Kopplung(Strang-Kreuzung)
→ 03 Shop(Teaser: 3 Spec-Zeilen + Verweis in den Shop, kein zweiter Warenkorb)
→ Nachweise & Betrieb(Zeilenliste) → Kontakt(zentriert) + Karte-Band → Sidebar-Footer  [+ .wa-fab]
```
Der Dreiklang sitzt im Hero-Block (vor dem Hero-Bild), damit die drei Bereiche ohne Scrollen
sichtbar sind und der Rechner trotzdem auf Position 2 bleibt.

## Unterseiten — je EIGENER Einstiegstyp (kein gemeinsamer Kopf-Baustein)
| Seite | Einstieg | Trägerbauform |
|---|---|---|
| `index.html` | Hero zentriert + Rechner an Position 2 | Spine oben |
| `energetische-beratung.html` | **Nachweis-Kopf** (Datenzeile Ausweisart │ Gebäudeart │ Anlass, bildlos, grün) | Maßnahmen-Register + dena/TÜV-Zeile |
| `klimaanlagen.html` | **Schema-Kopf** (Strichzeichnung Split ↔ Multi-Split, blau) | Vergleichstabelle → Steps 1–5 in Tiefe |
| `shop.html` | **Konfigurator steht ganz oben**, ersetzt den Kopfblock | Katalog nach Leistung (7 Sets) + Zubehör + Selbsteinbau + Lieferung |
| `kontakt.html` | **Kontaktzeile + Karte-Band sofort**, kein Kopfblock | Terminanfrage-Formular |
| Rechtsseiten | schmale Lesespalte | — |

## Der Shop (überarbeitet 2026-09-08) — Vorbild Solago, Form nach unserem Blueprint
Referenz des Kunden: **solago.de** (Balkonkraftwerk-Komplettsets). Übernommen wird das **Modell**,
nicht die Optik: Produkte sind **Sets, gegliedert nach Leistung**; ein **Rechner filtert vorweg**;
Zubehör ist eine eigene Kategorie; Selbsteinbau wird mit Anleitungen und klaren Grenzen gestützt.
- **Konfigurator als Kopf:** mehrere Räume erfassbar (bis 5), je Raum Fläche + Raumsituation,
  dazu ein Bauart-Wunsch. Ausgabe: kW je Raum, Gesamt-Kühllast, bei mehreren Räumen die nötige
  Außengerät-Leistung (Gleichzeitigkeitsfaktor 0,85, offengelegt). Filtert den Katalog.
- **Katalog als Spec-Zeilen** (NICHT als Karten-Raster — Blueprint-Auflage 3 gilt weiter):
  4 Sets für einen Raum (mobil 2,6 · Split 2,5 / 3,5 / 5,0 kW), 3 Multi-Split-Sets (2/3/4 Räume),
  4 Zubehör-Positionen. Jedes Set trägt eine **eigene Strichzeichnung** statt eines Fotos.
- **Warenkorb** nur hier (nicht doppelt auf der Startseite); Übergabe an das Anfrageformular
  auf `kontakt.html` über `sessionStorage` — in der Datenschutzerklärung benannt.
- Ergänzt: Grenzen des Selbsteinbaus, Abholung/Lieferung/Montage, Wartung.

## Der Rechner — ehrliche Bauform (verbindlich)
Datenblatt-Panel im Raster (1px-Rahmen, radius 3px). Kein Karten-Look, kein Modal, kein Wizard.
- Eingabe 1: Raumfläche m² — Zahlenfeld UND Slider synchronisiert (5–80 m²).
- Eingabe 2: Raumsituation — Segmente (Neubau/gut gedämmt · Altbau · Dachgeschoss) + Süd-Verglasung.
- Ausgabe: kW + BTU als Mono-Großwert; **der Ergebnisbalken IST die Kältekreis-Linie** (kW-Skala);
  Zuordnung zu genau EINEM Muster-Set; oberhalb des Bereichs „→ Multi-Split, Auslegung vor Ort".
- Rechenregel offengelegt (W/m² je Situation als Mono-Fußzeile) — nachvollziehbar statt Blackbox.
- Ergebnis ohne Formularzwang (keine Lead-Wall), `aria-live="polite"`, feste Ergebnisposition,
  volle Tastaturbedienung. Disclaimer: „Richtwert nach Faustformel — verbindliche Auslegung vor Ort."
- **Verboten:** Preisberechnung, Amortisations-/Ersparnisrechnung, „spart bis zu X %", Förderhöhen,
  Verfügbarkeits-/Countdown-Anzeigen.

## Divergenz-Nachweis

> **Überholt** — gültig ist der Divergenz-Nachweis im Nachtrag 2026-09-10 (MAVA 4/6).
| Achse | KlimaTech38 | DK Fenster (letzter) | MAVA (vorletzter) | Ackermann (3.) |
|---|---|---|---|---|
| Nav | feste Sidebar (Anlagen-Rail) + Mobil-Strangleiste | Bottom-Bar + Sheet ✔ | Topbar + Drawer ✔ | Scroll-Spy ✔ |
| Sektions-Kopf | Frage-Headline + Mono-Antwortzeile | eyebrow→h2→lead ✔ | Marginalie ✔ | kein-Eyebrow + Chip ✔ |
| Komponenten | Listen/Tabellen (Spec-Zeilen) | Split-Bild-Text-Wechsel ✔ | Fließtext-Editorial ✔ | Akkordeon + Strecke ✔ |
| Kontakt | Karte als Band (Einzugsgebiet) | interaktiv ✔ | keine Karte ✔ | Karte als Footer-Hintergrund ✔ |
| Footer | Sidebar-Footer | einzeilig minimal ✔ | Mega-Footer ✔ | Kontaktband ✔ |
| Galerie | keine Galerie | Vollbild-Slider ✔ | keine Galerie ✗ | Bild-Bänder ✔ |
| **abweichend** | — | **6/6** | **5/6** | **6/6** |
Spine ≠ letzte 3 ✓ · Nav ≠ unmittelbar vorheriger ✓ · Kontakt ≠ unmittelbar vorheriger ✓.
Sperrliste (Stand DK) eingehalten: Bottom-Bar/Sheet ✗ · eyebrow→h2→lead ✗ · Split-Bild-Text ✗ ·
Vollbild-Slider ✗ · einzeilig-minimaler Footer ✗ · Typenblatt-Einheitskopf ✗ · Kontakt interaktiv ✗.
Abgrenzung zur Mutterseite `introtech-sanierung/`: deren Skelett (Topbar+Drawer · eyebrow→h2→lead ·
Karten-Raster · Tag-Wolke · FAQ-Akkordeon · 3-Spalten-Footer) wird NICHT übernommen — nur Logo,
Farbanker, Tonfall, Kontaktdaten und die belegten Nachweise.

## Bau-Auflagen (was NICHT gebaut werden darf)
1. Keine Topbar mit Linkleiste + Burger-Drawer, keine Overlay-Nav, keine Bottom-Bar.
2. Kein `eyebrow`-Element, kein Lead-Absatz unter der Sektions-Headline.
3. Kein 3-/4-Karten-Raster als tragende Bauform; Shop-Sets sind Spec-Zeilen ohne Schatten.
4. Keine gerundete OSM-Kachel mit Pin-Pille, keine Karte als Spalte/Footer-Hintergrund.
5. Kein 3-Spalten-Footer mit `<details>`, kein einzeiliger, kein Mega-Footer.
6. Keine Galerie in irgendeiner Form, keine Vollbreiten-Bildbänder als Trenner, keine Lightbox.
7. Keine erfundenen Nachweise: NUR dena-Energieberater und TÜV Rheinland / TÜV-zertifizierter
   Fachbetrieb. BAFA, Meisterbetrieb, Innung, ISO, Gründungsjahr, Projektzahlen, Kundenstimmen,
   Sterne: verboten.
8. Keine Preis-Versprechen außerhalb der drei Muster-Sets; Set-Preise als Richtpreise (Demo)
   kennzeichnen und im README als Platzhalter markieren.
9. Kein zweites Nummernsystem: Ziffern nur in den 5 Prozess-Schritten und in Messwerten.
10. Farbdisziplin: Grün nur Energie-Strang, Blau nur Klima/Shop/Rechner; Treffpunkt nur im
    PV-Kopplungs-Block. Keine dritte Signalfarbe, kein Verlauf, kein Neon.
11. Motion `mechanical`, nur transform/opacity/clip-path, `prefers-reduced-motion` respektiert.
12. Pflicht: runder schwebender WhatsApp-Button `.wa-fab` mit Dauerpuls (Referenz `kfz-mattes/`).
13. Unterseiten teilen keinen gemeinsamen Kopf-Baustein.

---

## Nachtrag 2026-09-10 · Shop-Ausbau (Kundenentscheidung)

Der Kunde hat den Auftrag massiv erweitert: der Katalog bekommt sichtbare Preise nach dem Vorbild
**solago.de**, die Anfragestrecke das Muster von **klima-mueller.com**. Aus 7 Seiten wurden 29.
Damit halten drei Bau-Auflagen des ursprünglichen Blueprints nicht mehr — das steht hier offen,
statt es stillschweigend zu unterlaufen.

| Auflage | Status | Begründung | Kompensation |
|---|---|---|---|
| **1 · Kein Burger, kein Drawer, feste Rail** | **aufgehoben** | Die Rail war für 5 flache Einstiege entworfen. Jetzt sind es 5 Stränge über 29 Seiten mit 4 Shop-Kategorien und 9 Set-Seiten — das trägt eine vertikale Liste nicht. | Sticky Kopf mit **Mega-Menü in Spalten** (kein Drawer auf Desktop). Die Signature wandert mit: die Haarlinie unter dem Kopf **ist** die Kältekreis-Leitung, jeder Menüpunkt ein Anschlusspunkt. Mobil ein modales Panel mit `inert` + Fokusfalle. |
| **3 · Kein Karten-Raster als tragende Bauform** | **präzisiert, nicht aufgehoben** | Ein Katalog braucht eine vergleichbare Darstellung. | Tragend bleibt die **Spec-Zeile** (`.set-zeile`): Schema · Titel · Spec-`dl` · zwei Preise · Aktion, durch Haarlinien getrennt. Die **Kachel** (`.set-kachel`) ist Sekundärbauform, **nur** für die Bestseller-Reihe, **max. 3**, und hart begrenzt: kein Schatten, kein Radius über 3 px, **kein Hover-Lift** (nur die Haarlinie reagiert), `aspect-ratio` auf dem Schema-Slot, damit die Kacheln auf einer Grundlinie enden, Text-CTA statt gefülltem Button. |
| **5 · Kein Mega-Footer** | **gilt weiter — eingehalten** | Ein zwischenzeitlich gebauter Mega-Footer deckte sich mit MAVA und riss die Struktur-Divergenz unter die Schwelle; er wurde zurückgebaut. | **Footer als Kontaktband** (Achsenwert gewechselt): große Telefon-CTA + Zeiten + Direktkanäle · Anschrift + Parent-Logo · Gebiets-Band · **einzeiliger Seiten-Index** als Mono-Haarlinienzeile (Energie-Einträge mit grünem Strang-Punkt) · Legal-Zeile. Kein Spaltenraster, kein Claim-Block. |
| **8 · Richtpreise statt Preisliste** | **erweitert** | Kundenentscheidung. | **Zwei** Preise je Set (Abholung / inkl. Montage) — das ist die Brücke zwischen beiden Vorbildern. Demo-Kennzeichnung über **einen** Schalter `META["demo"]`. |
| **6 · Keine Galerie** | **gilt weiter** | Die Sparte ist neu, es gibt keine eigenen Referenzfotos. | Produktbilder sind **eigene Strichzeichnungen** (5 Varianten), kein Stock mit fremdem Herstellerlogo. |

### Divergenz-Nachweis (Stand nach Runde 2, im Panel bestätigt)
Gegen **DK Fenster**: 6/6 Achsen abweichend. Gegen **MAVA Marketing**: **4/6** — gefordert ≥ 4,
also die Untergrenze, nicht Komfort.

- **Abweichend:** Sektions-Kopf (Frage + Mono-Antwort vs. randständige Marginalie) · Komponenten
  (Spec-Zeilen und Tabellen vs. Fließtext-Editorial) · Kontakt (Karte als Band vs. formulargeführt
  ohne Karte) · **Footer (Kontaktband vs. Mega-Footer mit Claim)**.
- **Kollidierend:** **Nav** — `struktur-varianz.md` kennt keinen Wert „Mega-Menü"; nach der Regel
  „Achse nach Form, nicht nach Detail" fällt es in denselben Bucket wie MAVAs Topbar + Drawer.
  Und **Galerie** — beide „keine".

**Für den nächsten Build hart vorgemerkt:** Der Nav-Bucket „Topbar" ist aufgebraucht (MAVA und
KlimaTech38 in Folge) — der nächste Betrieb muss zwingend aus einem anderen Bucket greifen.
„Keine Galerie" ist die 4. Vergabe und nur noch mit echtem inhaltlichem Grund zulässig.
Motion `mechanical` ist ebenfalls gesperrt (2. Vergabe in 4 Builds).

### Neue Achse 7 (Sektions-Spine, Startseite)
Hero mit Preisanker → Vertrauensleiste → **die zwei Wege** (der Kern des Auftrags) → Rechner →
Bestseller + Kategorien → Ablauf 1–5 → Energie → PV-Kopplung (dunkles Band) → Ratgeber →
Nachweise → Kontakt + Karte-Band → Kontaktband-Footer.


---

## Nachtrag 2, 2026-09-10 · nach Runde 1 des QA-Panels

Das Panel hat den ersten Nachtrag in zwei Punkten kassiert. Beides ist umgebaut, nicht wegdiskutiert.

**Achse 5 zurückgedreht.** „Mega-Footer" war derselbe Achsenwert wie bei MAVA; zusammen mit
„Topbar" und „keine Galerie" waren drei Achsen identisch (3/6, gefordert ≥ 4). Der Fuß ist jetzt
ein **Kontaktband** (siehe Tabelle oben) — Achse gewechselt, ohne Nav oder Galerie anzutasten:
das Mega-Menü ist die inhaltlich richtige Informationsarchitektur für fünf Stränge über 29 Seiten,
und eine Galerie gäbe es nur als Stock-Deko, weil die Sparte keine eigenen Referenzfotos hat.

**Auflage 13 eingelöst.** `.kopf-kat` trug neun inhaltlich fremde Seitentypen. Jetzt gilt er nur
noch für die vier Katalog-Kategorien. Eigene Kopf-Bausteine haben bekommen:

| Seite | Kopfform |
|---|---|
| `shop.html` | `.kopf-rechner` — der Konfigurator **ist** der Einstieg und trägt die `h1` (so war es ursprünglich deklariert) |
| `montage.html` | `.kopf-ablauf` — nummerierte 7-Punkt-Ablauf-Leiste |
| `wartung.html` | `.kopf-intervall` — Intervall-Datenliste neben der Headline |
| `ratgeber.html` · `faq.html` | `.kopf-index` · `.kopf-frage` — schlanke Typo-Köpfe, die Liste darunter trägt die Seite |

Damit stehen **elf** unterschiedliche Einstiegstypen: Hero · Nachweis-Kopf · Schema-Kopf ·
Beratungs-Split · Kontaktzeile mit sofortigem Karte-Band · Set-Kopf · Artikel-Kopf ·
Katalog-Kopf · Rechner-Kopf · Ablauf-Kopf · Intervall-Kopf.

**index ↔ shop entkoppelt.** Die Bestseller-Kachelreihe steht nur noch auf der Startseite;
`shop.html` steigt über den Rechner ein. `.set-kachel` erscheint damit in genau einer Reihe.

### Auflage 2 — präzisiert (im Panel geprüft und getragen)
Die Auflage lautet neu: **kein Lead-Absatz unter der SEKTIONS-Headline (`h2`); im Seitenkopf unter
der `h1` ist er zulässig.** Der ursprüngliche Wortlaut („kein Lead-Absatz") war zu absolut — das
war ein Formulierungs-, kein Baufehler.

Gemessen über alle 29 Seiten: **81 von 81** inhaltstragenden `h2` werden direkt von der
Mono-Antwortzeile gefolgt, **0 Leads unter einer Sektions-Headline**. Die verbliebenen Leads
(`.kat-lead` · `.set-lead` · `.art-lead` · `.ber-lead`) sitzen im **Seitenkopf hinter der
Antwortzeile** und tragen dort die Orientierung, die eine Katalog- oder Produktseite braucht
(Raumbereich, Einbauweg, Abgrenzung). Auf `montage`, `wartung`, `ratgeber`, `faq` und `shop` sind
sie entfernt, weil dort der Kopf-Baustein selbst die Information trägt.
