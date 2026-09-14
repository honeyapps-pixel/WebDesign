# Kreativ-Brief — KlimaTech38 (Geschäftsbereich der InTroTech GmbH)

Demo-Website für die gekaufte Domain **klimatech38.de**. Neue Sparte des bestehenden Kunden
InTroTech GmbH (Gifhorn): **Energetische Beratung + Planung, Auslegung, Verkauf und Montage
von Klimaanlagen** — plus Self-Service-Shop mit Auslegungs-Rechner.

```
BRAND-ANKER (Mutterfirma InTroTech GmbH — Wiedererkennung ist Pflicht)
  Farben      : Anthrazit #4D4D4D (Wortmarke) · Sky-Blau #A1C8EB (Wassertropfen im Logo)
                → abgeleitet: Aktionsblau #1668AE (5,8:1 auf Weiß), Tiefblau #10303F.
                NEU für diese Sparte: EIN zweites, strang-codiertes Signal
                Energiegrün #1A6E52 — ausschließlich für den Energie-Strang.
  Logo/Name   : echtes InTroTech-Logo (assets/brand/logo.png / logo-white.png / mark.png,
                von introtech.de). Wortmarke der Sparte: "KlimaTech38" — die 38 ist echt:
                Postleitzahlregion 38xxx (Gifhorn · Wolfsburg · Braunschweig), das
                bestehende Einzugsgebiet des Betriebs. Kein erfundener Zusatz.
  Ton/Claim   : sachlich, technisch belegt, ohne Superlative. Original-Ton von introtech.de:
                "Innovation trifft Verantwortung." · "Ihr Weg zu mehr Effizienz und Komfort."
                · "Energiekosten senken, Wert steigern." · "alles aus einer Hand".
  Foto-Anmutung: kühl-neutrale Technik-/Gebäudefotografie, helles Grau/Weiß, kein Warmton-Mix.

NISCHE        : C2 Handwerk & Bau (SHK/Klima) mit C5-Andockung (Verkauf/Shop).
                Conversion primär: Beratungs-/Angebotsanfrage (Anruf > Formular).
                Sekundär: qualifizierte Shop-Anfrage über den Auslegungs-Rechner.
KONZEPT       : "Erst auslegen, dann kühlen." Die Seite denkt wie der Betrieb: nicht Geräte
                zuerst, sondern die Kühllast des Raums. Derselbe Rechenweg, den der Monteur
                bei der Auslegung geht, ist als Rechner öffentlich — er ist nicht Gimmick im
                Shop, sondern das Herz der Seite und der Übergabepunkt zur Beratung.
WELT          : W2 · Swiss / Grid-Präzise — ingenieurhaft, sachlich, Haarlinien-Raster,
                Mono-Beschriftung. Verstärkt den Brand-Anker (technischer Fachbetrieb,
                TÜV-zertifiziert) und trägt Zahlen (kW, BTU, m², SCOP) ohne Dekor.
SIGNATURE     : "Kältekreis-Linie" — eine durchgehende, technisch gezeichnete Haarlinie mit
                Mono-Kürzeln, die im Hero am Außengerät startet und an jedem Sektionsstart
                als Anschlusspunkt (Innengerät-Marker) andockt; im Rechner wird derselbe
                Strich zum Leistungsbalken (kW-Skala). Die Seite mit der durchlaufenden
                Kältemittelleitung.
HERO-MUSTER   : Katalog-Muster 6 „Zentriert-Minimal" — bewusst OHNE den Wort-Wechsel des
                Katalogs: die Persona `mechanical` und die Bandbreite 2 vertragen keinen
                Dauer-Effekt in der Kopfzone. Eintritt per gestaffeltem CSS-Load-Fade,
                darunter ein ruhiges, kontaktes Hero-Bild (kein Full-Bleed, kein Ken-Burns,
                kein Video). Muster 8 (Editorial-Split) wurde bewusst NICHT genommen —
                das war der alte Einheits-Hero.
MOTION        : mechanical  (data-motion="mechanical" am <html>; Vokabular nur up/left/right,
                harte kurze Wege, kein Weich-Fade. prefers-reduced-motion respektiert.)
TYPO-BEGRÜNDUNG: Display "Archivo" (Akzidenz-Grotesk, breite technische Anmutung, trägt
                gesperrte Versalien) + Fließtext "Public Sans" (neutrale, sehr sachliche
                Grotesk — Behörden-/Normtext-Charakter passt zu Energieausweis/Nachweisen)
                + "IBM Plex Mono" für Messwerte, Achsen-Labels und Leitungs-Kürzel.
                Alle drei neu im Register; kein Inter/Roboto/Arial.
FARB-BEGRÜNDUNG: Grund ist Weiß/Kühlgrau (neutraler Hintergrund, wie gefordert). Zwei Signale,
                strang-codiert statt dekorativ: BLAU = Kälte/Klima (Anlagen, Shop, Rechner),
                GRÜN = Energie/Nachhaltigkeit (Beratung, Energieausweis, PV-Kopplung).
                Beide Farben treffen sich nur dort, wo die Stränge sich fachlich treffen
                (PV-gekoppelte Klimaanlage). Sky-Blau #A1C8EB bleibt Tint/Frost-Fläche =
                direkter Logo-Bezug zur Mutterfirma.
BANDBREITE    : 2 (ruhig-technisch — der Betrieb verkauft Nachweise und Montage, nicht Lifestyle)
```

## Design-Tokens (Phase 2 — bewusst anders als beim letzten Build DK Fenster)
| Token | Wert | Begründung |
|---|---|---|
| Spacing-Ratio | **1.25×** (eng, technisch) | DK: 1.618× — Rhythmus enger, datenblattartig |
| `--radius` | **3px** | DK: 0 — minimal weicher, aber nicht "freundlich" |
| `--line-weight` | **1px** Haarlinie | sichtbares Raster ist Teil der Welt W2 |
| `--shadow` | **Kante** `0 1px 0` (keine weichen Schatten) | DK: weich-diffus |
| `--container` | **1180px** | DK: breit — schmaler, ruhiger Satzspiegel |
| `--type-ratio` | **1.25** | DK: 1.333–1.5 — flachere Hierarchie, mehr Sachlichkeit |
| Archetyp | **C · Zentriert-Minimal** | DK: B · MAVA: D |

## Divergenz-Vorprüfung (6 Oberflächen-Achsen)
| Achse | KlimaTech38 | vs. DK Fenster (letzter) | vs. MAVA (vorletzter) |
|---|---|---|---|
| Welt | W2 Swiss/Grid | W5 Boutique-Dunkel ✔ | W1 Editorial ✔ |
| Archetyp | C Zentriert-Minimal | B ✔ | D ✔ |
| Font-Klasse | Grotesk + Grotesk + Mono (3 Familien) | Serif-Display + Neo-Grotesk ✔ | Ein-Familien-Geometric ✔ |
| Motion | mechanical | still ✔ | editorial ✔ |
| Signature | Kältekreis-Linie | DIN-Öffnungssymbole ✔ | MAVA-Diagonale ✔ |
| Token-Sprache | 1.25× / 3px / Kante / 1180 / 1.25 | ✔ | ✔ |
→ **6 von 6** abweichend (gefordert: ≥ 3). Markenfarbe bleibt verankert (InTroTech-Blau).

---

## Nachtrag 2026-09-10 · Signature jetzt waagerecht

Mit dem Wegfall der Anlagen-Rail verliert die Kältekreis-Linie ihre vertikale Lesart. Sie ist
deshalb um 90° gedreht und dabei eher stärker geworden, weil sie jetzt auf **jeder** Seite an
derselben Stelle liegt:

1. **Kopf:** Die Haarlinie an der Unterkante des Kopfes ist die Kältemittelleitung. Jeder
   Menüpunkt trägt einen Anschlusspunkt (9 px, `--paper` gefüllt, `--line-strong` umrandet), der
   bei der aktiven Seite in `--klima` bzw. `--energie` gefüllt ist.
2. **Scroll-Fortschritt:** Dieselbe Linie füllt sich beim Scrollen in `--klima` (`scaleX`, nur
   Compositor). Kein zweites Element, keine zweite Metapher.
3. **Sektionen:** `.sec` trägt die Linie als Oberkante weiter, `.sec-head` dockt mit einem Punkt an.
4. **Rechner:** Dort wird die Linie zur **kW-Skala** — Teilstriche bei 2 / 3,5 / 5 / 6 / 7 / 10 kW,
   gefüllter Abschnitt bis zum Bedarf, ab 6 kW als Haarlinien-Schraffur (Grenze, nicht Warnung).
   Das war im ursprünglichen Brief versprochen und ist erst jetzt gebaut.
5. **Kontaktband:** waagerecht durch das Einzugsgebiet (unverändert).
6. **Mega-Panel:** das offene Panel ist ein Abzweig — 2 px Oberkante in der Strangfarbe.

Alles andere am Brief bleibt: Welt W2 (Swiss/Grid-Präzise), Archivo + Public Sans + IBM Plex Mono,
Motion `mechanical`, Brand-Anker Anthrazit/Sky-Blau, Strang-Codierung Blau = Klima / Grün = Energie
mit dem einen Treffpunkt bei der PV-Kopplung.
