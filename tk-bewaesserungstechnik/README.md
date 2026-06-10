# TK Bewässerungstechnik — Demo-Website

Verkaufs-Demo (MODE=demo) für **TK Bewässerungstechnik**, Inhaber **Tobias Koslikow**, Gifhorn-Gamsen.
Automatische Gartenbewässerung: Planung, Versenkregner, Tropfbewässerung, Steuerung, Brunnen, Wartung.

Statische Seite (HTML/CSS/JS) + GSAP/ScrollTrigger/Lenis (Honeyapps Motion-Engine). Kein Build-Schritt.

## Echte Daten (aus dem Google-Unternehmensprofil)
- **Name:** TK Bewässerungstechnik · **Inhaber:** Tobias Koslikow
- **Adresse:** Waldweg 29, 38518 Gifhorn (Ortsteil Gamsen)
- **Telefon / WhatsApp:** 01514 1633842  (`tel:+4915141633842`, `wa.me/4915141633842`)
- **Öffnungszeiten:** rund um die Uhr erreichbar (Google: „Open 24 hours")
- **Bewertung:** 5,0 ★ bei 4 Google-Bewertungen
- **Keine bestehende Website, kein Logo** (Neugründung).

## Platzhalter / vor Verkauf bzw. Go-Live klären (Phase 10)
- **Logo:** aktuell gesetzte Wortmarke „TK Bewässerungstechnik" + geometrisches Tropfen-Mark (SVG im
  Header). Durch echtes Logo ersetzen, sobald vorhanden.
- **Technische Richtwerte** (Wurfweite 4–12 m, ≈ 18 l/min je Zone, Tropfer 2–8 l/h, 2–6 Zonen) sind
  branchenübliche Beispielwerte — vom Inhaber bestätigen/anpassen.
- **Zonenplan** (`#plan`) ist ein **beispielhaftes** Schema, kein realer Garten — so im Untertitel markiert.
- **Bilder:** Stock-Lückenfüller von Pexels (siehe `IMAGE-CREDITS.txt`). Nach Verkauf durch echte
  Projektfotos von Tobias Koslikow ersetzen (Versenkregner, verlegte Leitungen, fertige Gärten).
- **Impressum:** USt-IdNr./Steuernummer fehlt noch (im Footer-Impressum als „wird ergänzt" markiert).
- **E-Mail:** keine bekannt — Kontakt läuft bewusst über Telefon/WhatsApp (Mobil-/Vor-Ort-Betrieb).
- **Google-Profil-Link:** für „5,0 ★"-Beleg den echten Google-Maps-Link hinterlegen, sobald bekannt.

## Struktur & Art-Direction
- **Welt:** W2 Swiss/Grid-Präzise · **Motion:** `mechanical` · **Archetyp:** C-Swiss (links-bündige Spec-Grid).
- **Signature:** „Bewässerungs-Zonenplan" (animiertes SVG-Schema, Spine-Position 2) + durchgängige Mono-Spec-Labels.
- **Skelett (Blueprint, `assets/struktur-blueprint.md`):** Nav = Scroll-Spy-Indikator · Sektions-Kopf = kein
  Eyebrow + Mono-Label · Komponenten = Spec-Listen · Kontakt = keine Karte (Adresse + Route + WhatsApp +
  Service-Gebiet) · Footer = einzeilig minimal · Galerie = große Bild-Bänder.
- **Tokens:** Paper #ECEFEE · Ink #14211F · Akzent Wasser-Teal #0C637A (Rasen-Grün #6E9F3A nur im Zonenplan) ·
  Radius 0 · Hairline 1px · Container 1300 · flach. Fonts: Geologica + Hanken Grotesk + IBM Plex Mono.
- Details: `assets/art-direction.md`, `assets/struktur-blueprint.md`.

## Dateien
```
index.html · styles.css · script.js   (Scroll-Spy, Zonenplan-Animation)
assets/ → hero/spray/head/install/lawn.jpg · motion.js · art-direction.md · struktur-blueprint.md
IMAGE-CREDITS.txt
```

## Lokal ansehen
`open index.html` (Safari/Chrome). `prefers-reduced-motion` wird respektiert; ohne JS/CDNs bleibt die
Seite voll lesbar (Failsafe macht Reveal-Elemente sichtbar).

---
Demo von **Honeyapps GbR**. Deploy/Repo/Versand erst nach ausdrücklicher Freigabe.
