# Struktur-Blueprint: TK Bewässerungstechnik, Gartenbewässerung (Gifhorn-Gamsen)
Archetyp C-Swiss · Welt W2 Swiss/Grid-Präzise · Motion mechanical · MODE=demo
Bau-Vertrag (Phase 1.6 → bauender Skill). Nur Skelett — Farbe/Font/Welt/Token aus assets/art-direction.md.

## Achsen-Festlegung (je genau ein Wert, an echten Content gekoppelt)

- **Nav-Paradigma:** Scroll-Spy ohne sichtbare Nav (Strich-/Punkt-Indikator am rechten Rand, mitwandernd;
  oben links nur Wortmarke „TK Bewässerungstechnik", oben rechts EIN Solid-CTA „Anrufen 01514 1633842").
  Mobil: schmale fixe Bottom-Aktion NUR Anrufen·WhatsApp — KEINE volle Bottom-Bar (Move-Kollision vermeiden).
- **Sektions-Kopf:** Kein-Eyebrow / große h2 — jede Sektion startet mit gesperrter Display-h2, daneben ein
  Mono-Spec-Label (▦ Zweit-Signature, z. B. „▦ ZONE / WURFWEITE / l-min"). Kein Strich-Versalien-Eyebrow.
- **Komponenten (dominant):** Listen / Tabellen — Leistungen als links-bündige Spec-Liste mit Mono-Werten
  je Zeile, Hairline-Leader statt Karten-Schatten. (+ Neben-Bauform: kompakte 4-Zeilen-Prozessleiste 1→2→3→4 —
  bewusst klein, damit „Step-Ablauf" NICHT die dominante Achse wird.)
- **Kontakt-Lösung:** Keine Karte — Adresse Waldweg 29 + großer Route-Link (extern) + Anrufen + WhatsApp +
  Service-Gebiet als Mono-Ortsliste. Statt Karten-Kachel ein Hairline-Raster-Feld mit Eckdaten.
- **Footer-Form:** Einzeilig minimal — Wortmarke · Tel/WhatsApp · Waldweg 29 · Impressum-Link in einer Zeile.
- **Galerie-Form:** Große Bild-Bänder als Sektions-Trenner — vorhandene Fotos als einzelne Vollbreite-Bänder
  mit je einem Mono-Caption-Label; kein Masonry/Streifen/Bento/Slider.
- **Sektions-Spine:**
  `Hero(C-Swiss, Text-links + Bild rechts) → Zonenplan(SVG-Signature, Pos.2) → Leistungen(Spec-Liste) →
   Bild-Band → Ablauf(4-Schritt-Leiste) → Bild-Band → Wartung & 24h(Liste) → Vertrauen(Hairline-Raster) →
   Kontakt(keine Karte) → Footer(minimal)`
  Zonenplan bewusst auf Pos. 2 (prominentester Platz) — rahmt die Seite als „geplantes Projekt".

## Divergenz-Nachweis
- Spine ≠ letzte 3 (Move/Feengarten/Schlaf): ✓ (Signature-Modul Pos.2, Listen statt Karten, Bild-Bänder).
- Nav & Kontakt ≠ unmittelbar vorher (Move = Bottom-Bar / Vollbild-Karte): ✓ beide abweichend.
- ≥4/6 diskrete Achsen abweichend: **6/6** vs Move · **6/6** vs Feengarten · **6/6** vs Schlaf-T-Raum.

## Bau-Hinweise (verbindlich)
- Zonenplan-Signature = Pflicht-Modul auf Spine-Pos. 2 (nicht weglassen/verschieben).
- Mono-Spec-Labels (▦) als Sektions-Kopf-Begleiter durchgängig (ersetzen den Eyebrow).
- Step-Ablauf klein halten (Neben-Bauform); dominante Bauform = Liste/Tabelle.
- Nur echte Daten (24 h · 5,0★/4× Google · inhabergeführt · Waldweg 29) — keine erfundenen Stats/Stimmen.
- prefers-reduced-motion respektieren; mechanical = nur transform/opacity/clip-path, up/left/right.

## Register-Struktur-Notiz (für Phase 8 / Register)
| Betrieb | Nav | Sektions-Kopf | Komponenten | Kontakt | Footer | Galerie | Spine-Kürzel |
|---|---|---|---|---|---|---|---|
| TK Bewässerungstechnik | Scroll-Spy (Strich-Indikator) | kein-Eyebrow + Mono-Spec-Label | Listen/Tabellen (+kompakte Steps) | keine Karte (Adresse+Route+WhatsApp+Gebiet) | einzeilig minimal | große Bild-Bänder | Hero→Zonenplan(Sig)→Leistungen(Liste)→Bild-Band→Ablauf(Steps)→Bild-Band→Wartung/24h(Liste)→Vertrauen(Raster)→Kontakt(keine Karte)→Footer(minimal) |
