/* ============================================================================
   assets/produkte.js — GENERIERT aus .tools/kt38_katalog.py.
   NICHT VON HAND AENDERN: `python3 .tools/gen_kt38_shop.py` ueberschreibt die Datei.
   Preise pflegen: .tools/kt38_katalog.py, dort auch META.demo umschalten.
   ========================================================================== */
window.KT38 = {
  "meta": {
    "demo": true,
    "demoWort": "Beispielpreis",
    "stand": "2026-09-10",
    "mwst": 19,
    "preisFuss": "Alle Preise in Euro inkl. 19 % MwSt. Abholung am Zeisigweg 4 in Gifhorn nach Terminabsprache; Lieferung im Einzugsgebiet nennen wir Ihnen im Angebot. Die Preise sind unverbindliche Richtwerte – verbindlich wird erst unser schriftliches Angebot.",
    "demoHinweis": "Die Preise auf diesen Seiten sind <b>Beispielwerte für die Vorschau</b> und noch nicht die Preise des Betriebs. Verbindlich ist ausschließlich das schriftliche Angebot.",
    "keinKaufHinweis": "Kein Kaufabschluss online: Sie wählen ein Set und fragen es an – wir melden uns mit einem schriftlichen, unverbindlichen Angebot."
  },
  "kategorien": [
    {
      "id": "split",
      "datei": "shop-split.html",
      "titel": "Split-Sets für einen Raum",
      "kurz": "Split-Sets",
      "frage": "Ein Raum soll kühl werden – was brauche ich?",
      "antwort": "Eine Split-Anlage: ein Außengerät, ein Innengerät, eine Leitung dazwischen",
      "strang": "klima"
    },
    {
      "id": "multi",
      "datei": "shop-multisplit.html",
      "titel": "Multi-Split-Sets für mehrere Räume",
      "kurz": "Multi-Split-Sets",
      "frage": "Mehrere Räume, aber nur ein Gerät an der Fassade – geht das?",
      "antwort": "Ja: ein Außengerät versorgt bis zu vier Innengeräte",
      "strang": "klima"
    },
    {
      "id": "mobil",
      "datei": "shop-mobil.html",
      "titel": "Mobile Monoblock-Geräte",
      "kurz": "Mobile Geräte",
      "frage": "Ich darf nicht bohren – was bleibt mir?",
      "antwort": "Ein mobiles Monoblock-Gerät: aufstellen, Schlauch nach draußen, einstecken",
      "strang": "klima"
    },
    {
      "id": "zubehoer",
      "datei": "shop-zubehoer.html",
      "titel": "Zubehör und Montagematerial",
      "kurz": "Zubehör",
      "frage": "Was brauche ich außer dem Gerät noch?",
      "antwort": "Halterung, Leitungsweg, Kondensatablauf – je nach Einbausituation",
      "strang": "klima"
    }
  ],
  "sets": [
    {
      "id": "split-25",
      "kategorie": "split",
      "titel": "Split-Set 2,5 kW",
      "bauform": "Wand-Innengerät",
      "kurz": "Der kleine Standard – Schlaf-, Kinder- oder Arbeitszimmer.",
      "kw": 2.5,
      "kwHeizen": null,
      "flaecheVon": 18,
      "flaecheBis": 30,
      "innengeraete": 1,
      "kaeltemittel": "R-32",
      "gwp": 675,
      "schallInnen_dbA": null,
      "schallAussen_dbA": null,
      "seer": null,
      "scop": null,
      "effizienzklasse": null,
      "selbsteinbau": true,
      "anschlussart": "Quick-Connect, Leitung ab Werk befüllt",
      "lieferumfang": [
        "Außengerät und Wand-Innengerät",
        "Vorgefüllte Kältemittelleitung 3 m mit Schnellkupplung",
        "Wandhalterung für das Außengerät",
        "Fernbedienung und Montageanleitung"
      ],
      "nichtEnthalten": [
        "Kernbohrung durch die Außenwand",
        "Elektroanschluss im Verteiler",
        "Kondensatpumpe, falls kein Gefälle möglich"
      ],
      "preise": {
        "abholung_cent": 74900,
        "montage_cent": 169000,
        "streich_cent": null,
        "streichTyp": null
      },
      "montageUmfang": "bis 3 m Leitungsweg, eine Kernbohrung, Inbetriebnahme und Einweisung",
      "schema": "split1",
      "zubehoer": [
        "halter-wand",
        "kondensatpumpe",
        "wanddurchfuehrung"
      ],
      "bestseller": false,
      "hinweis": null,
      "btu": 8500
    },
    {
      "id": "split-35",
      "kategorie": "split",
      "titel": "Split-Set 3,5 kW",
      "bauform": "Wand-Innengerät",
      "kurz": "Die häufigste Größe – Wohnzimmer im Bestand.",
      "kw": 3.5,
      "kwHeizen": null,
      "flaecheVon": 25,
      "flaecheBis": 42,
      "innengeraete": 1,
      "kaeltemittel": "R-32",
      "gwp": 675,
      "schallInnen_dbA": null,
      "schallAussen_dbA": null,
      "seer": null,
      "scop": null,
      "effizienzklasse": null,
      "selbsteinbau": true,
      "anschlussart": "Quick-Connect, Leitung ab Werk befüllt",
      "lieferumfang": [
        "Außengerät und Wand-Innengerät",
        "Vorgefüllte Kältemittelleitung 5 m mit Schnellkupplung",
        "Wandhalterung für das Außengerät",
        "Fernbedienung und Montageanleitung"
      ],
      "nichtEnthalten": [
        "Kernbohrung durch die Außenwand",
        "Elektroanschluss im Verteiler",
        "Kondensatpumpe, falls kein Gefälle möglich"
      ],
      "preise": {
        "abholung_cent": 89900,
        "montage_cent": 189000,
        "streich_cent": null,
        "streichTyp": null
      },
      "montageUmfang": "bis 5 m Leitungsweg, eine Kernbohrung, Inbetriebnahme und Einweisung",
      "schema": "split1",
      "zubehoer": [
        "halter-wand",
        "kondensatpumpe",
        "wanddurchfuehrung",
        "ueberspannung"
      ],
      "bestseller": true,
      "hinweis": null,
      "btu": 11900
    },
    {
      "id": "split-50",
      "kategorie": "split",
      "titel": "Split-Set 5,0 kW",
      "bauform": "Wand-Innengerät",
      "kurz": "Großer Wohnraum, offene Küche oder Dachgeschoss.",
      "kw": 5.0,
      "kwHeizen": null,
      "flaecheVon": 38,
      "flaecheBis": 60,
      "innengeraete": 1,
      "kaeltemittel": "R-32",
      "gwp": 675,
      "schallInnen_dbA": null,
      "schallAussen_dbA": null,
      "seer": null,
      "scop": null,
      "effizienzklasse": null,
      "selbsteinbau": false,
      "anschlussart": "offener Kältekreis – muss vakuumiert werden",
      "lieferumfang": [
        "Außengerät und Wand-Innengerät",
        "Kältemittelleitung nach Maß",
        "Wand- oder Bodenkonsole für das Außengerät",
        "Fernbedienung"
      ],
      "nichtEnthalten": [
        "Kernbohrung durch die Außenwand",
        "Elektroanschluss im Verteiler"
      ],
      "preise": {
        "abholung_cent": 119900,
        "montage_cent": 229000,
        "streich_cent": null,
        "streichTyp": null
      },
      "montageUmfang": "bis 5 m Leitungsweg, eine Kernbohrung, Vakuumieren, Inbetriebnahme",
      "schema": "split1",
      "zubehoer": [
        "halter-boden",
        "kondensatpumpe",
        "wanddurchfuehrung",
        "ueberspannung"
      ],
      "bestseller": false,
      "hinweis": "Ab dieser Größe bauen wir ein – der Kältekreis wird geöffnet und vakuumiert.",
      "btu": 17100
    },
    {
      "id": "split-70",
      "kategorie": "split",
      "titel": "Split-Set 7,0 kW",
      "bauform": "Wand-Innengerät",
      "kurz": "Ladenlokal, Praxis, große Dachwohnung.",
      "kw": 7.0,
      "kwHeizen": null,
      "flaecheVon": 55,
      "flaecheBis": 85,
      "innengeraete": 1,
      "kaeltemittel": "R-32",
      "gwp": 675,
      "schallInnen_dbA": null,
      "schallAussen_dbA": null,
      "seer": null,
      "scop": null,
      "effizienzklasse": null,
      "selbsteinbau": false,
      "anschlussart": "offener Kältekreis – muss vakuumiert werden",
      "lieferumfang": [
        "Außengerät und Wand-Innengerät",
        "Kältemittelleitung nach Maß",
        "Boden- oder Wandkonsole mit Schwingungsdämpfern",
        "Fernbedienung"
      ],
      "nichtEnthalten": [
        "Kernbohrung durch die Außenwand",
        "Fester Elektroanschluss im Verteiler"
      ],
      "preise": {
        "abholung_cent": 154900,
        "montage_cent": 279000,
        "streich_cent": null,
        "streichTyp": null
      },
      "montageUmfang": "bis 7 m Leitungsweg, eine Kernbohrung, Vakuumieren, Inbetriebnahme",
      "schema": "split1",
      "zubehoer": [
        "halter-boden",
        "kondensatpumpe",
        "wanddurchfuehrung",
        "ueberspannung"
      ],
      "bestseller": false,
      "hinweis": "Ab 6 kW legen wir die Anlage grundsätzlich vor Ort aus, nicht nach Faustformel.",
      "btu": 23900
    },
    {
      "id": "multi-duo",
      "kategorie": "multi",
      "titel": "Multi-Split-Set Duo · 2 Räume",
      "bauform": "1 Außengerät, 2 Wand-Innengeräte",
      "kurz": "Schlafzimmer und Wohnzimmer – ein Gerät an der Fassade.",
      "kw": 5.2,
      "kwHeizen": null,
      "flaecheVon": 35,
      "flaecheBis": 65,
      "innengeraete": 2,
      "kaeltemittel": "R-32",
      "gwp": 675,
      "schallInnen_dbA": null,
      "schallAussen_dbA": null,
      "seer": null,
      "scop": null,
      "effizienzklasse": null,
      "selbsteinbau": false,
      "anschlussart": "offener Kältekreis – muss vakuumiert werden",
      "lieferumfang": [
        "Ein Außengerät 5,2 kW",
        "Zwei Wand-Innengeräte (2,0 und 3,5 kW)",
        "Kältemittelleitungen nach Maß",
        "Boden- oder Wandkonsole"
      ],
      "nichtEnthalten": [
        "Kernbohrungen",
        "Fester Elektroanschluss im Verteiler",
        "Leitungskanäle in Sichtbereichen"
      ],
      "preise": {
        "abholung_cent": 219000,
        "montage_cent": 389000,
        "streich_cent": null,
        "streichTyp": null
      },
      "montageUmfang": "zwei Innengeräte, bis 12 m Leitung gesamt, zwei Kernbohrungen, Inbetriebnahme",
      "schema": "multi2",
      "zubehoer": [
        "halter-boden",
        "kondensatpumpe",
        "leitungskanal",
        "ueberspannung"
      ],
      "bestseller": true,
      "hinweis": null,
      "btu": 17700
    },
    {
      "id": "multi-trio",
      "kategorie": "multi",
      "titel": "Multi-Split-Set Trio · 3 Räume",
      "bauform": "1 Außengerät, 3 Wand-Innengeräte",
      "kurz": "Wohnung mit Schlaf-, Kinder- und Wohnzimmer.",
      "kw": 6.8,
      "kwHeizen": null,
      "flaecheVon": 50,
      "flaecheBis": 90,
      "innengeraete": 3,
      "kaeltemittel": "R-32",
      "gwp": 675,
      "schallInnen_dbA": null,
      "schallAussen_dbA": null,
      "seer": null,
      "scop": null,
      "effizienzklasse": null,
      "selbsteinbau": false,
      "anschlussart": "offener Kältekreis – muss vakuumiert werden",
      "lieferumfang": [
        "Ein Außengerät 6,8 kW",
        "Drei Wand-Innengeräte (2× 2,0 und 1× 3,5 kW)",
        "Kältemittelleitungen nach Maß",
        "Boden- oder Wandkonsole mit Schwingungsdämpfern"
      ],
      "nichtEnthalten": [
        "Kernbohrungen",
        "Fester Elektroanschluss im Verteiler",
        "Leitungskanäle in Sichtbereichen"
      ],
      "preise": {
        "abholung_cent": 299000,
        "montage_cent": 519000,
        "streich_cent": null,
        "streichTyp": null
      },
      "montageUmfang": "drei Innengeräte, bis 18 m Leitung gesamt, drei Kernbohrungen, Inbetriebnahme",
      "schema": "multi3",
      "zubehoer": [
        "halter-boden",
        "kondensatpumpe",
        "leitungskanal",
        "ueberspannung"
      ],
      "bestseller": false,
      "hinweis": null,
      "btu": 23200
    },
    {
      "id": "multi-quattro",
      "kategorie": "multi",
      "titel": "Multi-Split-Set Quattro · 4 Räume",
      "bauform": "1 Außengerät, 4 Wand-Innengeräte",
      "kurz": "Einfamilienhaus oder Büroetage.",
      "kw": 8.4,
      "kwHeizen": null,
      "flaecheVon": 65,
      "flaecheBis": 115,
      "innengeraete": 4,
      "kaeltemittel": "R-32",
      "gwp": 675,
      "schallInnen_dbA": null,
      "schallAussen_dbA": null,
      "seer": null,
      "scop": null,
      "effizienzklasse": null,
      "selbsteinbau": false,
      "anschlussart": "offener Kältekreis – muss vakuumiert werden",
      "lieferumfang": [
        "Ein Außengerät 8,4 kW",
        "Vier Wand-Innengeräte (3× 2,0 und 1× 3,5 kW)",
        "Kältemittelleitungen nach Maß",
        "Bodenkonsole mit Schwingungsdämpfern"
      ],
      "nichtEnthalten": [
        "Kernbohrungen",
        "Fester Elektroanschluss im Verteiler",
        "Leitungskanäle in Sichtbereichen"
      ],
      "preise": {
        "abholung_cent": 379000,
        "montage_cent": 649000,
        "streich_cent": null,
        "streichTyp": null
      },
      "montageUmfang": "vier Innengeräte, bis 25 m Leitung gesamt, vier Kernbohrungen, Inbetriebnahme",
      "schema": "multi4",
      "zubehoer": [
        "halter-boden",
        "kondensatpumpe",
        "leitungskanal",
        "ueberspannung"
      ],
      "bestseller": false,
      "hinweis": "Ab vier Innengeräten sehen wir uns die Leitungswege immer vorher an.",
      "btu": 28700
    },
    {
      "id": "mobil-20",
      "kategorie": "mobil",
      "titel": "Mobiles Monoblock-Gerät 2,0 kW",
      "bauform": "Monoblock, fahrbar",
      "kurz": "Ohne Bohren, ohne Genehmigung – für Miete und Übergangslösungen.",
      "kw": 2.0,
      "kwHeizen": null,
      "flaecheVon": 12,
      "flaecheBis": 20,
      "innengeraete": 1,
      "kaeltemittel": "R-290",
      "gwp": 3,
      "schallInnen_dbA": null,
      "schallAussen_dbA": null,
      "seer": null,
      "scop": null,
      "effizienzklasse": null,
      "selbsteinbau": true,
      "anschlussart": "geschlossenes Gerät, nur einstecken",
      "lieferumfang": [
        "Monoblock-Gerät auf Rollen",
        "Abluftschlauch 1,5 m",
        "Fensterabdichtung zum Einklemmen",
        "Fernbedienung"
      ],
      "nichtEnthalten": [
        "Feste Fensterdurchführung"
      ],
      "preise": {
        "abholung_cent": 39900,
        "montage_cent": null,
        "streich_cent": null,
        "streichTyp": null
      },
      "montageUmfang": null,
      "schema": "mono",
      "zubehoer": [
        "fensterabdichtung"
      ],
      "bestseller": false,
      "hinweis": "Rechnen Sie mit deutlich weniger Fläche, als die Nennleistung vermuten lässt – über den Abluftschlauch geht Leistung verloren.",
      "btu": 6800
    },
    {
      "id": "mobil-26",
      "kategorie": "mobil",
      "titel": "Mobiles Monoblock-Gerät 2,6 kW",
      "bauform": "Monoblock, fahrbar",
      "kurz": "Die größere mobile Variante, leiser geregelt.",
      "kw": 2.6,
      "kwHeizen": null,
      "flaecheVon": 16,
      "flaecheBis": 26,
      "innengeraete": 1,
      "kaeltemittel": "R-290",
      "gwp": 3,
      "schallInnen_dbA": null,
      "schallAussen_dbA": null,
      "seer": null,
      "scop": null,
      "effizienzklasse": null,
      "selbsteinbau": true,
      "anschlussart": "geschlossenes Gerät, nur einstecken",
      "lieferumfang": [
        "Monoblock-Gerät auf Rollen",
        "Abluftschlauch 1,5 m",
        "Fensterabdichtung zum Einklemmen",
        "Fernbedienung"
      ],
      "nichtEnthalten": [
        "Feste Fensterdurchführung"
      ],
      "preise": {
        "abholung_cent": 54900,
        "montage_cent": null,
        "streich_cent": null,
        "streichTyp": null
      },
      "montageUmfang": null,
      "schema": "mono",
      "zubehoer": [
        "fensterabdichtung"
      ],
      "bestseller": false,
      "hinweis": null,
      "btu": 8900
    }
  ],
  "zubehoer": [
    {
      "id": "halter-wand",
      "titel": "Wandkonsole für das Außengerät",
      "zweck": "Verzinkte Konsole mit Schwingungsdämpfern. Hält das Außengerät frei von der Wand, damit Schall nicht ins Mauerwerk geht.",
      "preis_cent": 8900,
      "passendZu": [
        "split-25",
        "split-35"
      ]
    },
    {
      "id": "halter-boden",
      "titel": "Bodenkonsole mit Dämpfern",
      "zweck": "Für Aufstellung auf Terrasse oder Flachdach. Erspart die Fassadenbefestigung – wichtig bei gedämmten Außenwänden.",
      "preis_cent": 12900,
      "passendZu": [
        "split-50",
        "split-70",
        "multi-duo",
        "multi-trio",
        "multi-quattro"
      ]
    },
    {
      "id": "kondensatpumpe",
      "titel": "Kondensatpumpe",
      "zweck": "Nötig, wenn das Kondensat nicht mit Gefälle abfließen kann – der häufigste Grund, warum eine Anlage nachträglich tropft.",
      "preis_cent": 14900,
      "passendZu": [
        "split-25",
        "split-35",
        "split-50",
        "split-70",
        "multi-duo",
        "multi-trio",
        "multi-quattro"
      ]
    },
    {
      "id": "wanddurchfuehrung",
      "titel": "Wanddurchführung mit Dichtmanschette",
      "zweck": "Sauber abgedichteter Bohrkern durch die Dämmebene. Ohne sie wird die Bohrung zur Wärmebrücke.",
      "preis_cent": 4900,
      "passendZu": [
        "split-25",
        "split-35",
        "split-50",
        "split-70"
      ]
    },
    {
      "id": "leitungskanal",
      "titel": "Leitungskanal, 2 m",
      "zweck": "Deckt Kältemittelleitung, Kabel und Kondensatschlauch an der Fassade ab. In Sichtbereichen die Alternative zum offenen Leitungsstrang.",
      "preis_cent": 5900,
      "passendZu": [
        "multi-duo",
        "multi-trio",
        "multi-quattro"
      ]
    },
    {
      "id": "ueberspannung",
      "titel": "Überspannungsschutz für die Zuleitung",
      "zweck": "Schützt die Elektronik des Außengeräts. Wird bei festem Anschluss im Verteiler gesetzt – gehört in Fachhände.",
      "preis_cent": 7900,
      "passendZu": [
        "split-35",
        "split-50",
        "split-70",
        "multi-duo",
        "multi-trio",
        "multi-quattro"
      ]
    },
    {
      "id": "fensterabdichtung",
      "titel": "Fensterabdichtung mit Reißverschluss",
      "zweck": "Ersetzt die mitgelieferte Klemmleiste. Ohne dichtes Fenster zieht das mobile Gerät die warme Luft direkt wieder herein.",
      "preis_cent": 3900,
      "passendZu": [
        "mobil-20",
        "mobil-26"
      ]
    }
  ]
};

/* Eine Darstellungsregel für Geld — spiegelt kt38_katalog.eur() */
window.KT38.eur = function (cent) {
  if (cent === null || cent === undefined) { return ''; }
  return (cent / 100).toLocaleString('de-DE', {
    style: 'currency', currency: 'EUR', minimumFractionDigits: 2
  });
};

/* Demo-Kennzeichnung auch für handgeschriebene Seiten, die der Generator nicht kennt */
if (window.KT38.meta.demo) { document.documentElement.dataset.preisDemo = '1'; }
