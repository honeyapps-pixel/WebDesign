# Struktur-Blueprint InTroTech — Redesign „High-End" (2026-09-24, struktur-architekt)

Leitidee: **Planblatt eines Architekturbüros** — links der Plankopf (Leiste), rechts der Inhalt,
am Ende der Lageplan mit Schriftfeld. Archetyp F (feste Leiste) in redaktioneller Lesart.

| Achse | Wert |
|---|---|
| Nav | feste Sidebar „Plankopf" (Logo · Leistungen · Unternehmen · 24/7 Notruf als Textlink unten); < 1100 px Kopfleiste (Logo · Tel · „Menü") + Panel von oben, `inert` + Esc + Fokusfalle. Kein Lenis. |
| Sektions-Kopf | Original-Leitsatz groß in Serife 300 → Haarlinie → kleine h2 (Sans 600). 0× Eyebrow, 0× Lead unter h2. |
| Komponenten | Haarlinien-Register (Leistungen, 5 Zeilen) + Step-Ablauf 4 horizontal + Datenblatt-`dl` |
| Kontakt | Karte als Footer-Hintergrund: statischer heller OSM-Lageplan (lokal), Sitz + 6 Orte, 0 iframes |
| Footer | Footer als Kontaktband: Lageplan + weißes Schriftfeld-Zellraster, auf allen 9 Seiten gleich |
| Galerie | keine (nur Symbolbilder; Bildfolge = Einstiegs-Signature) |
| Spine | Titelblatt (h1 Serife + randlose Bildfolge + Notruf-Textzeile) → Leistungen (Register) → Unternehmen (Leitsatz + Datenblatt) → Ablauf (4 horizontal) → Anfrage (Notruf-Typo \| Haarlinien-Formular) → Lageplan-Footer |

Unterseiten: „Blattkopf" (Haarlinien-Titelzeile 3 Zellen → h1 Serife 300 → Lead + „Schaden melden →" | Foto randlos 3:2),
Innensektionen h2 Serife ohne Eyebrow, `sp-cta-band` → Anfrage-Kurzzeile. Rechtsseiten: schmale Lesespalte.
Bildfolge: 3 Stadien, Überblendung, sichtbar nur „Symbolbilder" + ein Pause-Knopf (WCAG 2.2.2), keine Leiste/Punkte.

**Umsetzungs-Abweichungen (nach Review):** Titelblatt als h1 | Bildfolge nebeneinander (5fr/6fr, Bild randlos
oben/rechts), damit das Bild im ersten Viewport steht; ab 1100 px trägt die Leiste den Notruf, im Titelblatt
steht dann nur „Schaden melden →" (unter 1100 px der Notruf-Block). Register ohne Vorschaubilder (typografisch).
Anfrage: Notruf-Typo + eine Meta-Zeile | Formular (Kanal-Liste gestrichen, steht im Schriftfeld).
