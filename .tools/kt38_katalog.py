#!/usr/bin/env python3
"""kt38_katalog.py — EINZIGE Wahrheitsquelle fuer den KlimaTech38-Katalog.

Aus diesem Modul erzeugt `gen_kt38_shop.py` sowohl `assets/produkte.js` als auch
die statischen Kategorie- und Set-Seiten. Nichts wird an zwei Stellen gepflegt.

WICHTIG — die Regeln, die hier hart eingebaut sind:

  * KEINE Hersteller- oder Modellnamen. Die Sets heissen nach Bauart und Leistung.
    Sobald der Betrieb eine echte Geraeteliste liefert, kommen die Namen hierher.
  * `streich_cent` ist ueberall None. Ein Streichpreis verlangt nach § 11 PAngV den
    niedrigsten Gesamtpreis der letzten 30 Tage — den gibt es fuer einen Demo-Katalog
    nicht. `streichTyp` erzwingt spaeter eine bewusste Entscheidung ('uvp'|'vorher30').
  * `seer` / `scop` / `effizienzklasse`, `kwHeizen` und die Schallwerte sind None. Das sind
    GERAETE-Eigenschaften; sie stehen erst fest, wenn das Modell feststeht. Plausibel geratene
    dB(A)- oder kW-Zahlen waeren fake-praezise Werte ohne Quelle (und bei Schallwerten zusaetzlich
    eine beworbene Geraeteeigenschaft im Sinne des UWG).
    `gwp` bleibt gesetzt: der GWP von R-32 (675) bzw. R-290 (3) ist eine veroeffentlichte
    Eigenschaft des benannten KAELTEMITTELS, keine Aussage ueber ein Geraet. Sobald echte Geraete mit Modellnamen
    erscheinen, sind Effizienzklasse, Label und Produktdatenblatt nach EnVKV bzw.
    EU 626/2011 Pflicht — erfundene Werte waeren zusaetzlich ein Wettbewerbsverstoss.
  * Preise als ganzzahlige CENT. Formatiert wird genau einmal (KT38.eur / eur()).
  * META['demo'] = True  ->  ueberall Demo-Kennzeichnung, Product-JSON-LD OHNE `offers`.
    Auf False schalten, sobald echte Preise vorliegen — das ist der einzige Handgriff.
"""

META = {
    "demo": True,
    "demoWort": "Beispielpreis",
    "stand": "2026-09-10",
    "mwst": 19,
    "preisFuss": (
        "Alle Preise in Euro inkl. 19 % MwSt. Abholung am Zeisigweg 4 in Gifhorn nach "
        "Terminabsprache; Lieferung im Einzugsgebiet nennen wir Ihnen im Angebot. "
        "Die Preise sind unverbindliche Richtwerte – verbindlich wird erst unser "
        "schriftliches Angebot."
    ),
    "demoHinweis": (
        "Die Preise auf diesen Seiten sind <b>Beispielwerte für die Vorschau</b> und noch "
        "nicht die Preise des Betriebs. Verbindlich ist ausschließlich das schriftliche "
        "Angebot."
    ),
    "keinKaufHinweis": (
        "Kein Kaufabschluss online: Sie wählen ein Set und fragen es an – wir melden uns "
        "mit einem schriftlichen, unverbindlichen Angebot."
    ),
}

KATEGORIEN = [
    {
        "id": "split",
        "datei": "shop-split.html",
        "titel": "Split-Sets für einen Raum",
        "kurz": "Split-Sets",
        "frage": "Ein Raum soll kühl werden – was brauche ich?",
        "antwort": "Eine Split-Anlage: ein Außengerät, ein Innengerät, eine Leitung dazwischen",
        "lead": (
            "Ein Außengerät, ein Innengerät, dazwischen die Kältemittelleitung. Leiser und "
            "deutlich sparsamer als ein mobiles Gerät – und dieselbe Anlage heizt im Frühjahr "
            "und Herbst. Die Sets mit Schnellkupplung können Sie selbst anschließen, alle "
            "anderen bauen wir ein."
        ),
        "strang": "klima",
    },
    {
        "id": "multi",
        "datei": "shop-multisplit.html",
        "titel": "Multi-Split-Sets für mehrere Räume",
        "kurz": "Multi-Split-Sets",
        "frage": "Mehrere Räume, aber nur ein Gerät an der Fassade – geht das?",
        "antwort": "Ja: ein Außengerät versorgt bis zu vier Innengeräte",
        "lead": (
            "Ein Außengerät versorgt mehrere Innengeräte, jeder Raum bekommt seine eigene "
            "Temperatur. Die Leistung des Außengeräts liegt bewusst unter der Summe der "
            "Innengeräte – es laufen selten alle gleichzeitig auf Volllast. Leitungsführung "
            "und Kondensatablauf planen wir vor Ort."
        ),
        "strang": "klima",
    },
    {
        "id": "mobil",
        "datei": "shop-mobil.html",
        "titel": "Mobile Monoblock-Geräte",
        "kurz": "Mobile Geräte",
        "frage": "Ich darf nicht bohren – was bleibt mir?",
        "antwort": "Ein mobiles Monoblock-Gerät: aufstellen, Schlauch nach draußen, einstecken",
        "lead": (
            "Ein Gerät, ein Abluftschlauch, eine Steckdose. Kein Eingriff in die Fassade, keine "
            "Zustimmung der Eigentümerin nötig – die realistische Lösung für Mietwohnungen. "
            "Dafür lauter als eine Split-Anlage, und über den Schlauch geht Leistung verloren."
        ),
        "strang": "klima",
    },
    {
        "id": "zubehoer",
        "datei": "shop-zubehoer.html",
        "titel": "Zubehör und Montagematerial",
        "kurz": "Zubehör",
        "frage": "Was brauche ich außer dem Gerät noch?",
        "antwort": "Halterung, Leitungsweg, Kondensatablauf – je nach Einbausituation",
        "lead": (
            "Was zusätzlich nötig ist, hängt am Aufstellort. Wenn wir montieren, ist das "
            "Passende im Angebot enthalten – diese Liste ist für alle, die selbst einbauen."
        ),
        "strang": "klima",
    },
]

# --------------------------------------------------------------------------- Sets
# kw            = Kuehlleistung in kW (Nennleistung)
# flaecheVon/Bis= sinnvoller Raumbereich in m2, abgeleitet aus 60-130 W/m2
# schema        = eigene Strichzeichnung (kein Fremdfoto, kein Herstellerlogo)

SETS = [
    {
        "id": "split-25",
        "kategorie": "split",
        "titel": "Split-Set 2,5 kW",
        "bauform": "Wand-Innengerät",
        "kurz": "Der kleine Standard – Schlaf-, Kinder- oder Arbeitszimmer.",
        "kw": 2.5, "kwHeizen": None,
        "flaecheVon": 18, "flaecheBis": 30,
        "innengeraete": 1,
        "kaeltemittel": "R-32", "gwp": 675,
        "schallInnen_dbA": None, "schallAussen_dbA": None,
        "seer": None, "scop": None, "effizienzklasse": None,
        "selbsteinbau": True,
        "anschlussart": "Quick-Connect, Leitung ab Werk befüllt",
        "lieferumfang": [
            "Außengerät und Wand-Innengerät",
            "Vorgefüllte Kältemittelleitung 3 m mit Schnellkupplung",
            "Wandhalterung für das Außengerät",
            "Fernbedienung und Montageanleitung",
        ],
        "nichtEnthalten": [
            "Kernbohrung durch die Außenwand",
            "Elektroanschluss im Verteiler",
            "Kondensatpumpe, falls kein Gefälle möglich",
        ],
        "preise": {"abholung_cent": 74900, "montage_cent": 169000,
                   "streich_cent": None, "streichTyp": None},
        "montageUmfang": "bis 3 m Leitungsweg, eine Kernbohrung, Inbetriebnahme und Einweisung",
        "schema": "split1",
        "zubehoer": ["halter-wand", "kondensatpumpe", "wanddurchfuehrung"],
        "empfehlung": False,
        "hinweis": None,
    },
    {
        "id": "split-35",
        "kategorie": "split",
        "titel": "Split-Set 3,5 kW",
        "bauform": "Wand-Innengerät",
        "kurz": "Die gängige Größe fürs Wohnzimmer im Bestand.",
        "kw": 3.5, "kwHeizen": None,
        "flaecheVon": 25, "flaecheBis": 42,
        "innengeraete": 1,
        "kaeltemittel": "R-32", "gwp": 675,
        "schallInnen_dbA": None, "schallAussen_dbA": None,
        "seer": None, "scop": None, "effizienzklasse": None,
        "selbsteinbau": True,
        "anschlussart": "Quick-Connect, Leitung ab Werk befüllt",
        "lieferumfang": [
            "Außengerät und Wand-Innengerät",
            "Vorgefüllte Kältemittelleitung 5 m mit Schnellkupplung",
            "Wandhalterung für das Außengerät",
            "Fernbedienung und Montageanleitung",
        ],
        "nichtEnthalten": [
            "Kernbohrung durch die Außenwand",
            "Elektroanschluss im Verteiler",
            "Kondensatpumpe, falls kein Gefälle möglich",
        ],
        "preise": {"abholung_cent": 89900, "montage_cent": 189000,
                   "streich_cent": None, "streichTyp": None},
        "montageUmfang": "bis 5 m Leitungsweg, eine Kernbohrung, Inbetriebnahme und Einweisung",
        "schema": "split1",
        "zubehoer": ["halter-wand", "kondensatpumpe", "wanddurchfuehrung", "ueberspannung"],
        "empfehlung": True,
        "hinweis": None,
    },
    {
        "id": "split-50",
        "kategorie": "split",
        "titel": "Split-Set 5,0 kW",
        "bauform": "Wand-Innengerät",
        "kurz": "Großer Wohnraum, offene Küche oder Dachgeschoss.",
        "kw": 5.0, "kwHeizen": None,
        "flaecheVon": 38, "flaecheBis": 60,
        "innengeraete": 1,
        "kaeltemittel": "R-32", "gwp": 675,
        "schallInnen_dbA": None, "schallAussen_dbA": None,
        "seer": None, "scop": None, "effizienzklasse": None,
        "selbsteinbau": False,
        "anschlussart": "offener Kältekreis – muss vakuumiert werden",
        "lieferumfang": [
            "Außengerät und Wand-Innengerät",
            "Kältemittelleitung nach Maß",
            "Wand- oder Bodenkonsole für das Außengerät",
            "Fernbedienung",
        ],
        "nichtEnthalten": [
            "Kernbohrung durch die Außenwand",
            "Elektroanschluss im Verteiler",
        ],
        "preise": {"abholung_cent": 119900, "montage_cent": 229000,
                   "streich_cent": None, "streichTyp": None},
        "montageUmfang": "bis 5 m Leitungsweg, eine Kernbohrung, Vakuumieren, Inbetriebnahme",
        "schema": "split1",
        "zubehoer": ["halter-boden", "kondensatpumpe", "wanddurchfuehrung", "ueberspannung"],
        "empfehlung": False,
        "hinweis": "Ab dieser Größe bauen wir ein – der Kältekreis wird geöffnet und vakuumiert.",
    },
    {
        "id": "split-70",
        "kategorie": "split",
        "titel": "Split-Set 7,0 kW",
        "bauform": "Wand-Innengerät",
        "kurz": "Ladenlokal, Praxis, große Dachwohnung.",
        "kw": 7.0, "kwHeizen": None,
        "flaecheVon": 55, "flaecheBis": 85,
        "innengeraete": 1,
        "kaeltemittel": "R-32", "gwp": 675,
        "schallInnen_dbA": None, "schallAussen_dbA": None,
        "seer": None, "scop": None, "effizienzklasse": None,
        "selbsteinbau": False,
        "anschlussart": "offener Kältekreis – muss vakuumiert werden",
        "lieferumfang": [
            "Außengerät und Wand-Innengerät",
            "Kältemittelleitung nach Maß",
            "Boden- oder Wandkonsole mit Schwingungsdämpfern",
            "Fernbedienung",
        ],
        "nichtEnthalten": [
            "Kernbohrung durch die Außenwand",
            "Fester Elektroanschluss im Verteiler",
        ],
        "preise": {"abholung_cent": 154900, "montage_cent": 279000,
                   "streich_cent": None, "streichTyp": None},
        "montageUmfang": "bis 7 m Leitungsweg, eine Kernbohrung, Vakuumieren, Inbetriebnahme",
        "schema": "split1",
        "zubehoer": ["halter-boden", "kondensatpumpe", "wanddurchfuehrung", "ueberspannung"],
        "empfehlung": False,
        "hinweis": "Ab 6 kW legen wir die Anlage grundsätzlich vor Ort aus, nicht nach Faustformel.",
    },
    {
        "id": "multi-duo",
        "kategorie": "multi",
        "titel": "Multi-Split-Set Duo · 2 Räume",
        "bauform": "1 Außengerät, 2 Wand-Innengeräte",
        "kurz": "Schlafzimmer und Wohnzimmer – ein Gerät an der Fassade.",
        "kw": 5.2, "kwHeizen": None,
        "flaecheVon": 35, "flaecheBis": 65,
        "innengeraete": 2,
        "kaeltemittel": "R-32", "gwp": 675,
        "schallInnen_dbA": None, "schallAussen_dbA": None,
        "seer": None, "scop": None, "effizienzklasse": None,
        "selbsteinbau": False,
        "anschlussart": "offener Kältekreis – muss vakuumiert werden",
        "lieferumfang": [
            "Ein Außengerät 5,2 kW",
            "Zwei Wand-Innengeräte (2,0 und 3,5 kW)",
            "Kältemittelleitungen nach Maß",
            "Boden- oder Wandkonsole",
        ],
        "nichtEnthalten": [
            "Kernbohrungen",
            "Fester Elektroanschluss im Verteiler",
            "Leitungskanäle in Sichtbereichen",
        ],
        "preise": {"abholung_cent": 219000, "montage_cent": 389000,
                   "streich_cent": None, "streichTyp": None},
        "montageUmfang": "zwei Innengeräte, bis 12 m Leitung gesamt, zwei Kernbohrungen, Inbetriebnahme",
        "schema": "multi2",
        "zubehoer": ["halter-boden", "kondensatpumpe", "leitungskanal", "ueberspannung"],
        "empfehlung": True,
        "hinweis": None,
    },
    {
        "id": "multi-trio",
        "kategorie": "multi",
        "titel": "Multi-Split-Set Trio · 3 Räume",
        "bauform": "1 Außengerät, 3 Wand-Innengeräte",
        "kurz": "Wohnung mit Schlaf-, Kinder- und Wohnzimmer.",
        "kw": 6.8, "kwHeizen": None,
        "flaecheVon": 50, "flaecheBis": 90,
        "innengeraete": 3,
        "kaeltemittel": "R-32", "gwp": 675,
        "schallInnen_dbA": None, "schallAussen_dbA": None,
        "seer": None, "scop": None, "effizienzklasse": None,
        "selbsteinbau": False,
        "anschlussart": "offener Kältekreis – muss vakuumiert werden",
        "lieferumfang": [
            "Ein Außengerät 6,8 kW",
            "Drei Wand-Innengeräte (2× 2,0 und 1× 3,5 kW)",
            "Kältemittelleitungen nach Maß",
            "Boden- oder Wandkonsole mit Schwingungsdämpfern",
        ],
        "nichtEnthalten": [
            "Kernbohrungen",
            "Fester Elektroanschluss im Verteiler",
            "Leitungskanäle in Sichtbereichen",
        ],
        "preise": {"abholung_cent": 299000, "montage_cent": 519000,
                   "streich_cent": None, "streichTyp": None},
        "montageUmfang": "drei Innengeräte, bis 18 m Leitung gesamt, drei Kernbohrungen, Inbetriebnahme",
        "schema": "multi3",
        "zubehoer": ["halter-boden", "kondensatpumpe", "leitungskanal", "ueberspannung"],
        "empfehlung": False,
        "hinweis": None,
    },
    {
        "id": "multi-quattro",
        "kategorie": "multi",
        "titel": "Multi-Split-Set Quattro · 4 Räume",
        "bauform": "1 Außengerät, 4 Wand-Innengeräte",
        "kurz": "Einfamilienhaus oder Büroetage.",
        "kw": 8.4, "kwHeizen": None,
        "flaecheVon": 65, "flaecheBis": 115,
        "innengeraete": 4,
        "kaeltemittel": "R-32", "gwp": 675,
        "schallInnen_dbA": None, "schallAussen_dbA": None,
        "seer": None, "scop": None, "effizienzklasse": None,
        "selbsteinbau": False,
        "anschlussart": "offener Kältekreis – muss vakuumiert werden",
        "lieferumfang": [
            "Ein Außengerät 8,4 kW",
            "Vier Wand-Innengeräte (3× 2,0 und 1× 3,5 kW)",
            "Kältemittelleitungen nach Maß",
            "Bodenkonsole mit Schwingungsdämpfern",
        ],
        "nichtEnthalten": [
            "Kernbohrungen",
            "Fester Elektroanschluss im Verteiler",
            "Leitungskanäle in Sichtbereichen",
        ],
        "preise": {"abholung_cent": 379000, "montage_cent": 649000,
                   "streich_cent": None, "streichTyp": None},
        "montageUmfang": "vier Innengeräte, bis 25 m Leitung gesamt, vier Kernbohrungen, Inbetriebnahme",
        "schema": "multi4",
        "zubehoer": ["halter-boden", "kondensatpumpe", "leitungskanal", "ueberspannung"],
        "empfehlung": False,
        "hinweis": "Ab vier Innengeräten sehen wir uns die Leitungswege immer vorher an.",
    },
    {
        "id": "mobil-20",
        "kategorie": "mobil",
        "titel": "Mobiles Monoblock-Gerät 2,0 kW",
        "bauform": "Monoblock, fahrbar",
        "kurz": "Ohne Bohren, ohne Genehmigung – für Miete und Übergangslösungen.",
        "kw": 2.0, "kwHeizen": None,
        "flaecheVon": 12, "flaecheBis": 20,
        "innengeraete": 1,
        "kaeltemittel": "R-290", "gwp": 3,
        "schallInnen_dbA": None, "schallAussen_dbA": None,
        "seer": None, "scop": None, "effizienzklasse": None,
        "selbsteinbau": True,
        "anschlussart": "geschlossenes Gerät, nur einstecken",
        "lieferumfang": [
            "Monoblock-Gerät auf Rollen",
            "Abluftschlauch 1,5 m",
            "Fensterabdichtung zum Einklemmen",
            "Fernbedienung",
        ],
        "nichtEnthalten": [
            "Feste Fensterdurchführung",
        ],
        "preise": {"abholung_cent": 39900, "montage_cent": None,
                   "streich_cent": None, "streichTyp": None},
        "montageUmfang": None,
        "schema": "mono",
        "zubehoer": ["fensterabdichtung"],
        "empfehlung": False,
        "hinweis": "Rechnen Sie mit deutlich weniger Fläche, als die Nennleistung vermuten lässt – "
                   "über den Abluftschlauch geht Leistung verloren.",
    },
    {
        "id": "mobil-26",
        "kategorie": "mobil",
        "titel": "Mobiles Monoblock-Gerät 2,6 kW",
        "bauform": "Monoblock, fahrbar",
        "kurz": "Die größere mobile Variante, leiser geregelt.",
        "kw": 2.6, "kwHeizen": None,
        "flaecheVon": 16, "flaecheBis": 26,
        "innengeraete": 1,
        "kaeltemittel": "R-290", "gwp": 3,
        "schallInnen_dbA": None, "schallAussen_dbA": None,
        "seer": None, "scop": None, "effizienzklasse": None,
        "selbsteinbau": True,
        "anschlussart": "geschlossenes Gerät, nur einstecken",
        "lieferumfang": [
            "Monoblock-Gerät auf Rollen",
            "Abluftschlauch 1,5 m",
            "Fensterabdichtung zum Einklemmen",
            "Fernbedienung",
        ],
        "nichtEnthalten": [
            "Feste Fensterdurchführung",
        ],
        "preise": {"abholung_cent": 54900, "montage_cent": None,
                   "streich_cent": None, "streichTyp": None},
        "montageUmfang": None,
        "schema": "mono",
        "zubehoer": ["fensterabdichtung"],
        "empfehlung": False,
        "hinweis": None,
    },
]

ZUBEHOER = [
    {
        "id": "halter-wand",
        "titel": "Wandkonsole für das Außengerät",
        "zweck": "Verzinkte Konsole mit Schwingungsdämpfern. Hält das Außengerät frei von der "
                 "Wand, damit Schall nicht ins Mauerwerk geht.",
        "preis_cent": 8900,
        "passendZu": ["split-25", "split-35"],
    },
    {
        "id": "halter-boden",
        "titel": "Bodenkonsole mit Dämpfern",
        "zweck": "Für Aufstellung auf Terrasse oder Flachdach. Erspart die Fassadenbefestigung – "
                 "wichtig bei gedämmten Außenwänden.",
        "preis_cent": 12900,
        "passendZu": ["split-50", "split-70", "multi-duo", "multi-trio", "multi-quattro"],
    },
    {
        "id": "kondensatpumpe",
        "titel": "Kondensatpumpe",
        "zweck": "Nötig, wenn das Kondensat nicht mit Gefälle abfließen kann – der häufigste "
                 "Grund, warum eine Anlage nachträglich tropft.",
        "preis_cent": 14900,
        "passendZu": ["split-25", "split-35", "split-50", "split-70",
                      "multi-duo", "multi-trio", "multi-quattro"],
    },
    {
        "id": "wanddurchfuehrung",
        "titel": "Wanddurchführung mit Dichtmanschette",
        "zweck": "Sauber abgedichteter Bohrkern durch die Dämmebene. Ohne sie wird die Bohrung "
                 "zur Wärmebrücke.",
        "preis_cent": 4900,
        "passendZu": ["split-25", "split-35", "split-50", "split-70"],
    },
    {
        "id": "leitungskanal",
        "titel": "Leitungskanal, 2 m",
        "zweck": "Deckt Kältemittelleitung, Kabel und Kondensatschlauch an der Fassade ab. "
                 "In Sichtbereichen die Alternative zum offenen Leitungsstrang.",
        "preis_cent": 5900,
        "passendZu": ["multi-duo", "multi-trio", "multi-quattro"],
    },
    {
        "id": "ueberspannung",
        "titel": "Überspannungsschutz für die Zuleitung",
        "zweck": "Schützt die Elektronik des Außengeräts. Wird bei festem Anschluss im Verteiler "
                 "gesetzt – gehört in Fachhände.",
        "preis_cent": 7900,
        "passendZu": ["split-35", "split-50", "split-70",
                      "multi-duo", "multi-trio", "multi-quattro"],
    },
    {
        "id": "fensterabdichtung",
        "titel": "Fensterabdichtung mit Reißverschluss",
        "zweck": "Ersetzt die mitgelieferte Klemmleiste. Ohne dichtes Fenster zieht das mobile "
                 "Gerät die warme Luft direkt wieder herein.",
        "preis_cent": 3900,
        "passendZu": ["mobil-20", "mobil-26"],
    },
]


# --------------------------------------------------------------------------- Hilfen

def btu(kw):
    """kW -> BTU/h, auf 100 gerundet. Nie speichern, immer ableiten."""
    return int(round(kw * 3412.142 / 100.0) * 100)


def eur(cent):
    """Cent -> '1.899,00 €'. Eine Darstellungsregel fuer Python und JS."""
    if cent is None:
        return None
    s = f"{cent // 100:,}".replace(",", ".")
    return f"{s},{cent % 100:02d} €"


def set_by_id(sid):
    for s in SETS:
        if s["id"] == sid:
            return s
    return None


def zubehoer_by_id(zid):
    for z in ZUBEHOER:
        if z["id"] == zid:
            return z
    return None


def sets_der_kategorie(kid):
    return [s for s in SETS if s["kategorie"] == kid]


def guenstigster_montagepreis():
    """Fuer den Preisanker auf der Startseite ('montiert ab ...')."""
    werte = [s["preise"]["montage_cent"] for s in SETS if s["preise"].get("montage_cent")]
    return min(werte) if werte else None


def guenstigster_abholpreis():
    werte = [s["preise"]["abholung_cent"] for s in SETS if s["preise"].get("abholung_cent")]
    return min(werte) if werte else None


def pruefe():
    """Selbsttest — laeuft im Generator und im QA-Gate."""
    fehler = []
    ids = [s["id"] for s in SETS]
    if len(ids) != len(set(ids)):
        fehler.append("doppelte Set-IDs")
    katids = {k["id"] for k in KATEGORIEN}
    for s in SETS:
        if s["kategorie"] not in katids:
            fehler.append(f"{s['id']}: unbekannte Kategorie {s['kategorie']}")
        if s["flaecheVon"] >= s["flaecheBis"]:
            fehler.append(f"{s['id']}: flaecheVon >= flaecheBis")
        if s["preise"]["streich_cent"] is not None and not s["preise"]["streichTyp"]:
            fehler.append(f"{s['id']}: Streichpreis ohne streichTyp — § 11 PAngV verlangt eine Grundlage")
        if META["demo"] and s["preise"]["streich_cent"] is not None:
            fehler.append(f"{s['id']}: Streichpreis im Demo-Katalog ist unzulaessig")
        if s["seer"] is not None and not s.get("modell"):
            fehler.append(f"{s['id']}: SEER ohne Modellbezug — EnVKV verlangt Label und Datenblatt")
        for zid in s["zubehoer"]:
            if not zubehoer_by_id(zid):
                fehler.append(f"{s['id']}: unbekanntes Zubehoer {zid}")
    return fehler


if __name__ == "__main__":
    probleme = pruefe()
    print(f"{len(SETS)} Sets, {len(ZUBEHOER)} Zubehoerteile, {len(KATEGORIEN)} Kategorien")
    print(f"guenstigster Montagepreis: {eur(guenstigster_montagepreis())}")
    print(f"guenstigster Abholpreis:   {eur(guenstigster_abholpreis())}")
    if probleme:
        print("PROBLEME:")
        for p in probleme:
            print("  -", p)
    else:
        print("Selbsttest ohne Befund.")
