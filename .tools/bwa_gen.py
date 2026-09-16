#!/usr/bin/env python3
"""bwa_gen.py – Seiten-Generator für die Demo „InTroTech Bauwerksabdichtung" (introtech-abdichtung/).

Erzeugt alle 11 HTML-Seiten + sitemap/robots aus EINER Content-Quelle. Kopf/Fuß/Schnitt-Definition
bleiben über alle Seiten identisch. Firmendaten 1:1 von introtech.de (Mutterfirma); das Leistungs-
Portfolio ist eine Demo-Annahme für die neue Sparte (siehe README, „vor Live bestätigen").

Aufruf:  python3 .tools/bwa_gen.py
"""
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "introtech-abdichtung"
DEMO = True                       # True → noindex/nofollow (Sparten-Name/Domain offen, Leistungen = Annahme)
DOMAIN = "https://introtech-abdichtung.vercel.app"   # Arbeitsstand; echte Sparten-Domain offen
FIRMA = "InTroTech GmbH"
SPARTE = "Bauwerksabdichtung"
TEL_ANZ = "05371 8759972"
TEL_INT = "+4953718759972"
WA = "https://wa.me/4953718759972"
MAIL = "info@introtech.de"
STRASSE = "Zeisigweg 4"
ORT = "38518 Gifhorn"
ZEITEN = "Mo–Fr 08–18 Uhr"
ROUTE = "https://www.openstreetmap.org/search?query=Zeisigweg%204%2C%2038518%20Gifhorn"
GEBIET = ["Gifhorn", "Wolfsburg", "Braunschweig", "Peine", "Salzgitter", "Helmstedt"]
JAHR = "2026"
MUTTER = "https://www.introtech.de"
KT38 = "https://klimatech38.vercel.app"

# ----------------------------------------------------------------------------- Icons (1.5 Strich)
def ico(path, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" '
            f'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{path}</svg>')

I_TEL = ico('<path d="M5 4h3l2 5-2.5 1.5a11 11 0 0 0 5 5L14 13l5 2v3a2 2 0 0 1-2 2A14 14 0 0 1 3 6a2 2 0 0 1 2-2Z"/>')
I_MAIL = ico('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>')
I_ORT = ico('<path d="M12 21s7-6.2 7-11a7 7 0 1 0-14 0c0 4.8 7 11 7 11Z"/><circle cx="12" cy="10" r="2.5"/>')
I_UHR = ico('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>')
I_PFEIL = ico('<path d="M5 12h14M13 6l6 6-6 6"/>', "ico-pfeil")
I_LINKS = ico('<path d="M19 12H5M11 6l-6 6 6 6"/>', "ico-pfeil")
I_RUNTER = ico('<path d="M12 5v14M6 13l6 6 6-6"/>', "ico-pfeil")
I_EXTERN = ico('<path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>')
I_WA = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.885-9.886 9.885M20.52 3.449C18.24 1.245 15.24 0 12.045 0 5.463 0 .104 5.359.101 11.945c0 2.096.549 4.14 1.595 5.945L0 24l6.335-1.652a11.96 11.96 0 005.71 1.454h.006c6.585 0 11.946-5.359 11.949-11.945a11.86 11.86 0 00-3.495-8.411z"/></svg>')
# Verbund-Kette (4 Glieder)
I_LUPE = ico('<circle cx="11" cy="11" r="6"/><path d="m20 20-4.5-4.5M11 8v3l2 1.5"/>')
I_SCHICHT = ico('<path d="M3 9l9-5 9 5-9 5-9-5Z"/><path d="M3 14l9 5 9-5"/>')
I_WIND = ico('<path d="M4 9h10a3 3 0 1 0-3-3M3 14h14a3 3 0 1 1-3 3M5 19h6"/>')
I_HAUS = ico('<path d="M4 11.5 12 5l8 6.5"/><path d="M6 10.5V20h12v-9.5"/><path d="M10 20v-5h4v5"/>')

# ----------------------------------------------------------------------------- Die 7 Stellen
# Reihenfolge = Wasserweg von oben nach unten (Blueprint). Verfahren/Material = fachüblich, Demo-Annahme.
STELLEN = [
    dict(nr="01", slug="balkon-terrasse-flachdach", name="Balkon, Terrasse &amp; Flachdach", name_kurz="Balkon &amp; Terrasse",
         ort="Anschluss an die Hauswand, Belag und Entwässerung",
         befund="Wasser, das auf Balkon oder Terrasse stehen bleibt, sucht sich den Weg in die Decke darunter und in die Wand dahinter.",
         erkennen="Feuchte Flecken an der Decke unter dem Balkon. Abplatzender Putz oder Farbe an der Unterseite. Lose oder hohl klingende Fliesen, Ausblühungen in den Fugen. Nach Regen eine nasse Stelle innen an der Wand hinter der Terrassentür.",
         tun="Wir prüfen Gefälle, Entwässerung und den Anschluss an die Wand, nehmen den alten Belag ab, soweit nötig, und dichten die Fläche neu ab, mit Flüssigkunststoff oder Bahnen nach DIN 18531 einschließlich der Anschlüsse an Wand, Tür und Ablauf. Darauf kommt ein neuer Belag oder ein begehbarer Aufbau.",
         verfahren=[("Flüssigkunststoff-Abdichtung", "Viele Anschlüsse und Details, kleine bis mittlere Flächen", "PMMA- oder PU-Flüssigkunststoff, vliesarmiert"),
                    ("Bahnenabdichtung", "Größere ebene Flächen, Flachdach", "Bitumen- oder Kunststoffbahnen, mehrlagig"),
                    ("Anschluss- und Detailabdichtung", "Türschwelle, Geländerpfosten, Ablauf, Wandanschluss", "Dichtbänder, Manschetten, Klemmprofile")],
         grenzen="Ist die Betonplatte selbst geschädigt (korrodierte Bewehrung, Abplatzungen), gehört vor die Abdichtung eine Betonsanierung. Das sagen wir Ihnen nach der Besichtigung.",
         foto=("balkon", "Pfütze auf einem Plattenbelag an einer Betonkante", "Stehendes Wasser auf einem Plattenbelag (Symbolfoto)", 1200, 800),
         band="500 197 720 166", band_m="700 190 400 225", verwandt=["02", "04"],
         title="Balkon-, Terrassen- und Flachdachabdichtung Gifhorn",
         desc="Balkon und Terrasse neu abdichten: Anschluss an die Hauswand, Flüssigkunststoff oder Bahnen nach DIN 18531. InTroTech Bauwerksabdichtung, Gifhorn und Umgebung."),
    dict(nr="02", slug="sockelabdichtung", name="Sockel &amp; Spritzwasser", name_kurz="Sockel",
         ort="Die ersten 30 Zentimeter über dem Gelände",
         befund="Der Sockel bekommt Regen, Spritzwasser und im Winter Salz ab. Oft ist er die Stelle, an der die Kellerabdichtung zu früh aufhört.",
         erkennen="Abplatzende Farbe oder Putz knapp über dem Gelände. Eine dunkle, nasse Zone nach Regen, die nur langsam abtrocknet. Grünbelag oder weiße Ausblühungen am Sockel. Innen Feuchte am Fuß der Erdgeschosswand.",
         tun="Wir nehmen den geschädigten Sockelputz ab, führen die Abdichtung der Kellerwand als Sockelabdichtung mindestens 30 Zentimeter über das Gelände, mit mineralischer Dichtungsschlämme oder Bitumendickbeschichtung, und bauen einen wasserabweisenden Sockelputz neu auf. Reicht ein dichter Belag bis an die Wand, empfehlen wir einen Kiesstreifen oder ein Gefälle vom Haus weg.",
         verfahren=[("Sockelabdichtung", "Übergang von der Kellerwand zur Fassade", "Mineralische Dichtungsschlämme oder kunststoffmodifizierte Bitumendickbeschichtung"),
                    ("Sockelputz-Neuaufbau", "Nach der Abdichtung", "Sockel- oder Sanierputz nach WTA, wasserabweisend"),
                    ("Spritzwasserschutz", "Dichter Belag bis an die Wand, Regenspritzer", "Kiesstreifen, Gefälle vom Gebäude weg")],
         grenzen="Endet die Kellerabdichtung unter dem Gelände schon vorher, hilft der Sockel allein nicht. Dann gehört die Kellerwand außen (Stelle 05) dazu; wir prüfen das mit einer Freilegung an einer Stelle.",
         foto=("sockel", "Abplatzende Farbe am Fuß einer verputzten Wand", "Abplatzende Farbe am Wandfuß (Symbolfoto)", 1000, 667),
         band="40 207 720 166", band_m="180 200 400 225", verwandt=["05", "03"],
         title="Sockelabdichtung und Sockelsanierung Gifhorn",
         desc="Sockel abdichten und Sockelputz erneuern: Spritzwasserbereich bis 30 cm über Gelände, Dichtungsschlämme oder Bitumendickbeschichtung. InTroTech, Gifhorn."),
    dict(nr="03", slug="lichtschacht-kellerfenster-rohrdurchfuehrung", name="Lichtschächte, Kellerfenster &amp; Rohrdurchführungen", name_kurz="Lichtschacht &amp; Fenster",
         ort="Jede Öffnung in der Kellerwand",
         befund="Jede Öffnung in der Kellerwand ist eine Fuge: Fenster, Lichtschacht, Hausanschluss. Dort endet die Fläche, und dort kommt Wasser durch.",
         erkennen="Wasser im Lichtschacht nach starkem Regen. Feuchte Laibung oder eine nasse Wand unter dem Kellerfenster. Tropfspuren an Rohren und Kabeldurchführungen. Ausblühungen rund um den Hausanschluss.",
         tun="Wir dichten den Anschluss von Lichtschacht und Kellerfenster an die Wand neu ab, setzen bei Bedarf druckwasserdichte Kellerfenster oder Schachtabdeckungen und verschließen Rohr- und Kabeldurchführungen mit Manschetten oder Ringraumdichtungen und binden sie an die Wandabdichtung an.",
         verfahren=[("Lichtschacht-Anschluss", "Wasser im Schacht, feuchte Laibung", "Dichtbänder, Anschluss an die Wandabdichtung, Schachtabdeckung"),
                    ("Kellerfenster", "Undichte Fuge zwischen Fenster und Wand", "Druckwasserdichte Kellerfenster, Fugenabdichtung"),
                    ("Rohr- und Kabeldurchführungen", "Tropfspuren, Feuchte am Hausanschluss", "Ringraumdichtung, Manschette, Quellmörtel")],
         grenzen="Steht bei jedem Regen Wasser im Lichtschacht, ist oft die Entwässerung des Schachts das Problem und nicht die Wand. Auch das klären wir bei der Besichtigung.",
         foto=("kellerfenster", "Vergittertes Kellerfenster in einer Klinkerwand mit Feuchtespuren an der Fensterbank", "Kellerfenster in der Klinkerwand (Symbolfoto)", 1000, 667),
         band="30 267 720 166", band_m="150 260 400 225", verwandt=["02", "05"],
         title="Lichtschacht & Kellerfenster abdichten Gifhorn",
         desc="Lichtschächte, Kellerfenster und Durchführungen dicht anschließen: Dichtbänder, druckwasserdichte Fenster, Ringraumdichtungen. InTroTech, Gifhorn und Umgebung."),
    dict(nr="04", slug="rissinjektion", name="Risse", name_kurz="Risse",
         ort="In Kellerwand, Bodenplatte oder Decke",
         befund="Ein Riss ist ein offener Weg für Wasser, ob er aus Setzung, Schwinden oder Last entstanden ist. Verpresst wird er wieder dicht und, je nach Ursache, wieder tragfähig.",
         erkennen="Eine feuchte Linie oder Tropfspur entlang eines Risses. Kalkausblühungen, die dem Riss folgen. Wasser, das bei Regen sichtbar aus dem Riss austritt. Risse an Arbeitsfugen von Betonwänden.",
         tun="Wir bohren den Riss im Wechsel an, setzen Packer und verpressen ihn: mit Polyurethanharz, wenn er dicht werden soll und noch Bewegung aufnimmt, mit Epoxidharz, wenn er kraftschlüssig verbunden werden muss, oder mit Acrylatgel bei stark wasserführenden Rissen. Die Rissursache benennen wir Ihnen dabei mit.",
         verfahren=[("Polyurethanharz-Injektion", "Riss soll dicht werden und Bewegung aufnehmen", "Elastisches PU-Harz, Bohrpacker"),
                    ("Epoxidharz-Injektion", "Kraftschlüssiger Verbund, trockene bis leicht feuchte Risse", "Epoxidharz, Klebepacker"),
                    ("Acrylatgel-Injektion", "Stark wasserführende Risse und Fugen", "Acrylatgel, Bohrpacker")],
         grenzen="Bewegt sich ein Riss weiter, etwa durch Setzung, muss die Ursache mit einem Tragwerksplaner geklärt werden, bevor wir kraftschlüssig verpressen. Sonst reißt es daneben wieder auf.",
         foto=("riss", "Riss im Putz mit abplatzender Oberfläche am Fuß einer Wand", "Riss mit abplatzendem Putz (Symbolfoto)", 1200, 800),
         band="440 342 720 166", band_m="640 330 400 225", verwandt=["07", "06"],
         title="Rissinjektion und Rissverpressung Gifhorn",
         desc="Risse in Kellerwand und Bodenplatte verpressen: PU-Harz, Epoxidharz oder Acrylatgel, je nach Riss und Wasser. InTroTech Bauwerksabdichtung, Gifhorn und Umgebung."),
    dict(nr="05", slug="kelleraussenabdichtung", name="Kellerwand außen", name_kurz="Kellerwand außen",
         ort="Die erdberührte Außenseite der Kellerwand",
         befund="Die Außenabdichtung hält das Wasser dort auf, wo es ankommt: an der Außenseite der Kellerwand.",
         erkennen="Großflächig feuchte Kellerwände, besonders nach Regen oder bei hohem Grundwasser. Wasser, das an der Wand herunterläuft. Schimmel oder muffiger Geruch. Alte, spröde Bitumenabdichtung, die beim Aufgraben abblättert.",
         tun="Wir graben die Kellerwand abschnittsweise frei, reinigen und egalisieren den Untergrund und tragen eine neue Abdichtung nach DIN 18533 auf, kunststoffmodifizierte Bitumendickbeschichtung oder Bahnen je nach Wassereinwirkung. Perimeterdämmung und Noppenbahn schützen sie beim Verfüllen. Wo Sickerwasser ansteht, kommt eine Drainage mit Kiesfilter dazu.",
         verfahren=[("Freilegen und Untergrund", "Immer, abschnittsweise und mit gesicherter Baugrube", "Reinigung, Egalisierung, Hohlkehle am Fundament"),
                    ("Bitumendickbeschichtung oder Bahnen", "Bodenfeuchte bis drückendes Wasser (DIN 18533, W1‑E bis W2‑E)", "Kunststoffmodifizierte Bitumendickbeschichtung, Bitumen- oder Kunststoffbahnen"),
                    ("Schutz und Drainage", "Sickerwasser, Hanglage, bindiger Boden", "Perimeterdämmung, Noppenbahn, Drainagerohr im Kiesfilter")],
         grenzen="Ist die Wand nicht zugänglich, etwa wegen Nachbargebäude, Terrasse oder Anbau, arbeiten wir von innen (Stelle 06). Die Innenabdichtung ist ein eigenes Verfahren mit eigenen Regeln.",
         foto=("aussen", "Drainagerohr im Kiesbett in einem ausgehobenen Graben", "Drainagerohr im Kiesbett (Symbolfoto)", 1000, 667),
         band="40 396 720 166", band_m="140 380 400 225", verwandt=["06", "02"],
         title="Kelleraußenabdichtung und Drainage Gifhorn",
         desc="Kellerwand von außen abdichten: Freilegen, Bitumendickbeschichtung oder Bahnen nach DIN 18533, Perimeterdämmung, Drainage. InTroTech, Gifhorn und Umgebung."),
    dict(nr="06", slug="innenabdichtung-horizontalsperre", name="Kellerwand innen &amp; Horizontalsperre", name_kurz="Kellerwand innen",
         ort="Die Innenseite der Kellerwand und der Wandfuß",
         befund="Wenn Aufgraben nicht geht, dichten wir von innen ab und stoppen aufsteigende Feuchte mit einer Sperre im Mauerwerk.",
         erkennen="Ein Feuchtehorizont, der von unten einige Zentimeter bis einen Meter die Wand hochsteigt. Salzausblühungen und abplatzender Putz am Wandfuß. Feuchte Wände, obwohl außen nichts zugänglich oder bereits abgedichtet ist.",
         tun="Bei aufsteigender Feuchte bohren wir die Wand am Fuß in einer Reihe an und injizieren eine Horizontalsperre, die das Kapillarwasser stoppt. Feuchte Wandflächen dichten wir von innen mit mineralischer Dichtungsschlämme und Sanierputz nach WTA ab. Kommt Wasser seitlich durch und außen ist nichts erreichbar, legen wir per Schleierinjektion einen Gelvorhang hinter die Wand.",
         verfahren=[("Horizontalsperre", "Aufsteigende Feuchte im Mauerwerk", "Injektionscreme auf Silan-/Siloxanbasis, Bohrlochreihe nach WTA 4-10"),
                    ("Innenabdichtung", "Außenseite nicht zugänglich", "Mineralische Dichtungsschlämme, Dichtkehle, Sanierputz nach WTA"),
                    ("Schleierinjektion", "Seitlich eindringendes Wasser ohne Zugang von außen", "Acrylatgel, Injektion durch die Wand ins Erdreich")],
         grenzen="Eine Innenabdichtung hält das Wasser aus dem Raum, nicht aus der Wand; die Wand bleibt erdfeucht. Für einen Nutzkeller ist das in Ordnung, bei Wohnräumen sprechen wir vorher über Dämmung und Lüftung.",
         foto=("innen", "Abplatzender Putz und Ausblühungen am Fuß einer Ziegelwand", "Putzabplatzungen am Wandfuß (Symbolfoto)", 1000, 667),
         band="420 417 720 166", band_m="560 380 400 225", verwandt=["05", "07"],
         title="Kellerinnenabdichtung und Horizontalsperre Gifhorn",
         desc="Keller von innen abdichten: Horizontalsperre gegen aufsteigende Feuchte, Dichtungsschlämme, Sanierputz nach WTA, Schleierinjektion. InTroTech, Gifhorn."),
    dict(nr="07", slug="bodenplatte-wand-sohle-fuge", name="Bodenplatte &amp; Wand-Sohle-Fuge", name_kurz="Bodenplatte &amp; Fuge",
         ort="Der Kellerboden und seine Fuge zur Wand",
         befund="Drückendes Wasser kommt von unten: durch die Bodenplatte und durch die Fuge, an der Wand und Sohle aufeinandertreffen.",
         erkennen="Wasser oder feuchte Ränder entlang der Kante zwischen Boden und Wand. Nasse Stellen im Boden nach Regen oder bei hohem Grundwasser. Kalkspuren an Arbeitsfugen. Feuchter Estrich, aufgequollene Bodenbeläge.",
         tun="Wir dichten die Wand-Sohle-Fuge per Injektion oder mit Dichtkehle und Schlämme ab und schließen undichte Arbeitsfugen und Risse in der Bodenplatte durch Verpressen. Bei flächig drückendem Wasser bauen wir eine innenliegende Flächenabdichtung auf der Bodenplatte auf, eine Wanne, die an die Wandabdichtung anschließt.",
         verfahren=[("Fugeninjektion", "Wand-Sohle-Fuge, Arbeitsfugen im Beton", "PU-Harz oder Acrylatgel, Bohrpacker"),
                    ("Dichtkehle und Schlämme", "Nicht drückende Feuchte am Wandfuß", "Dichtmörtel, mineralische Dichtungsschlämme"),
                    ("Innenwanne", "Flächig drückendes Wasser von unten", "Mineralische Dichtungsschlämme im Verbund mit der Wandabdichtung")],
         grenzen="Bei hohem Grundwasser ist eine Innenwanne eine Frage der Statik, weil Auftrieb auf die Bodenplatte wirkt. Das prüfen wir vor der Ausführung.",
         foto=("bodenplatte", "Kalkspuren entlang eines Risses in einer Betonfläche", "Kalkspuren an einem Riss im Beton (Symbolfoto)", 1000, 667),
         band="250 472 720 166", band_m="380 440 460 259", verwandt=["04", "06"],
         title="Bodenplatte und Wand-Sohle-Fuge abdichten Gifhorn",
         desc="Bodenplatte und Wand-Sohle-Fuge gegen drückendes Wasser abdichten: Fugeninjektion, Dichtkehle, Innenwanne. InTroTech Bauwerksabdichtung, Gifhorn und Umgebung."),
]
BY_NR = {s["nr"]: s for s in STELLEN}

ABLAUF = [
    ("Befund vor Ort", "Wir sehen uns die feuchte Stelle an, messen die Feuchte im Bauteil und suchen die Ursache des Schadens. Ist die Herkunft unklar, übernimmt die Leckageortung der InTroTech GmbH."),
    ("Abdichtungskonzept", "Sie bekommen ein schriftliches Konzept: welche Stelle, welches Verfahren, nach welchem Regelwerk (DIN 18531, DIN 18533 oder WTA), und ein Angebot dazu."),
    ("Ausführung", "Wir führen die Arbeiten abschnittsweise aus, mit gesicherter Baugrube und Schutz für Haus und Garten. Sie wissen jeden Tag, was als Nächstes passiert."),
    ("Abnahme und Dokumentation", "Sie erhalten eine Dokumentation der ausgeführten Abdichtung mit Fotos der verdeckten Schichten. Das ist wichtig für Versicherung, Verkauf und die nächste Sanierung."),
]

KETTE = [
    (I_LUPE, "Leckageortung", "Ursache zerstörungsarm finden.", MUTTER + "/", False),
    (I_SCHICHT, "Abdichtung", "Den Weg des Wassers schließen.", "index.html#schnitt", True),
    (I_WIND, "Trocknung", "Bauteile und Räume kontrolliert trocknen.", MUTTER + "/", False),
    (I_HAUS, "Sanierung", "Schäden beheben, Räume wieder nutzbar machen.", MUTTER + "/", False),
]

# ----------------------------------------------------------------------------- Der Diagnose-Schnitt (SVG)
# Koordinaten: 1 Einheit ≈ 1 cm. Gelände y=300, Kellerdecke y=280–300, Wände x=400–436 / 784–820,
# Keller y=300–540, Bodenplatte y=540–565, Grundwasser ab y≈545. Zonen 01–07 werden über CSS-Variablen
# --z01…--z07 sichtbar (Hover im Hero, fest in den Zeichnungs-Bändern).
MARKER = {  # nr: (x, y, label, anchor, label_x)
    "01": (836, 264, "Balkon &amp; Terrasse", "end", 778),
    "02": (418, 286, "Sockel", "start", 446),
    "03": (370, 340, "Lichtschacht &amp; Kellerfenster", "end", 344),
    "04": (802, 424, "Risse", "end", 778),
    "05": (418, 470, "Kellerwand außen", "start", 446),
    "06": (760, 505, "Kellerwand innen", "end", 736),
    "07": (610, 556, "Bodenplatte &amp; Fuge", "start", 636),
}


def pfeil_h(x1, x2, y, cls="wz"):
    """Horizontaler Wasserpfeil (Sky-Blau), Spitze am Ende."""
    d = 1 if x2 > x1 else -1
    return (f'<path class="{cls}" d="M{x1} {y}H{x2 - 6 * d}"/>'
            f'<path class="{cls}" d="M{x2 - 12 * d} {y - 6}L{x2} {y}L{x2 - 12 * d} {y + 6}"/>')


def pfeil_v(x, y1, y2, cls="wz"):
    d = 1 if y2 > y1 else -1
    return (f'<path class="{cls}" d="M{x} {y1}V{y2 - 6 * d}"/>'
            f'<path class="{cls}" d="M{x - 6} {y2 - 12 * d}L{x} {y2}L{x + 6} {y2 - 12 * d}"/>')


def schnitt_def():
    z = []
    # Zone 01 – Balkon/Terrasse: Regen auf die Platte, Wasser läuft zum Wandanschluss; Abdichtung über die Platte + hochgezogen
    z.append('<g class="zn zn-01">' + pfeil_v(866, 236, 280) + pfeil_v(912, 236, 280)
             + '<path class="wz" d="M980 277H828V297"/><path class="wz" d="M822 291l6 8 6-8"/>'
             + '<path class="ab" d="M1000 284H822V270"/><text class="lb" x="910" y="226" text-anchor="middle">Regen · Wandanschluss</text></g>')
    # Zone 02 – Sockel: Spritzwasser vom Gelände an die Wand; Abdichtung bis 30 cm über Gelände
    z.append('<g class="zn zn-02"><path class="wz" d="M316 298q30-30 76-16"/><path class="wz" d="M380 276l12 6-9 9"/>'
             '<path class="wz" d="M300 298q22-14 46-8"/>'
             '<path class="ab" d="M398 302V266"/><text class="lb" x="392" y="256" text-anchor="end">30 cm über Gelände</text></g>')
    # Zone 03 – Lichtschacht/Kellerfenster: Regen in den Schacht, Pfütze, Wasser über die Fensterfuge nach innen
    z.append('<g class="zn zn-03">' + pfeil_v(374, 300, 384)
             + '<rect class="wf" x="348" y="392" width="52" height="8"/>' + pfeil_h(392, 446, 395)
             + '<path class="ab" d="M398 300V400"/><rect class="ab ab--fein" x="398" y="338" width="40" height="54"/>'
             '<text class="lb" x="330" y="318" text-anchor="end">Schacht-Anschluss</text></g>')
    # Zone 04 – Riss in der rechten Kellerwand: Wasser von außen durch den Riss; Riss verpresst (Packer)
    riss = "M796 380l8 18-6 14 9 20-5 16 8 22"
    z.append('<g class="zn zn-04">' + pfeil_h(872, 826, 420)
             + f'<path class="ab ab--riss" d="{riss}"/>'
             + '<circle class="pk" cx="802" cy="392" r="4"/><circle class="pk" cx="804" cy="428" r="4"/><circle class="pk" cx="806" cy="462" r="4"/>'
             + '<text class="lb" x="836" y="456">Riss verpresst</text></g>')
    # Zone 05 – Kellerwand außen: Sickerwasser aus dem Erdreich; Abdichtung außen bis zum Fundament, Drainage
    z.append('<g class="zn zn-05">' + pfeil_h(300, 392, 436) + pfeil_h(300, 392, 478) + pfeil_h(300, 392, 518)
             + '<path class="ab" d="M398 300V568H386"/><circle class="dr" cx="372" cy="551" r="9"/>'
             + '<text class="lb" x="386" y="414" text-anchor="end">Abdichtung außen · Drainage</text></g>')
    # Zone 06 – Kellerwand innen: aufsteigende Feuchte im Wandfuß, Horizontalsperre stoppt sie; Innenabdichtung; Schleier außen
    z.append('<g class="zn zn-06"><rect class="wf" x="784" y="526" width="36" height="14"/>'
             + pfeil_v(802, 540, 528) + pfeil_v(794, 540, 528, "wz wz--fein") + pfeil_v(810, 540, 528, "wz wz--fein")
             + '<path class="ab ab--sperre" d="M782 522H822"/><path class="ab" d="M786 300V540"/>'
             + '<path class="ab ab--schleier" d="M830 400q-8 40 0 80t0 60"/>'
             + '<text class="lb" x="760" y="470" text-anchor="end">Horizontalsperre</text></g>')
    # Zone 07 – Bodenplatte: drückendes Wasser von unten; Innenwanne + Dichtkehle + Fugeninjektion
    z.append('<g class="zn zn-07">' + pfeil_v(520, 598, 572, 'wz wz--gw') + pfeil_v(610, 598, 572, 'wz wz--gw') + pfeil_v(700, 598, 572, 'wz wz--gw')
             + pfeil_h(408, 432, 552, "wz wz--fein wz--gw") + pfeil_h(812, 788, 552, "wz wz--fein wz--gw")
             + '<path class="ab" d="M436 542H784"/><path class="ab ab--fill" d="M436 542v-14l14 14z"/><path class="ab ab--fill" d="M784 542v-14l-14 14z"/>'
             + '<circle class="pk" cx="436" cy="542" r="4"/><circle class="pk" cx="784" cy="542" r="4"/>'
             + '<text class="lb" x="610" y="620" text-anchor="middle">drückendes Wasser</text></g>')
    zonen = "".join(z)

    return f'''<svg class="defs" width="0" height="0" aria-hidden="true" focusable="false"><defs>
<linearGradient id="g-himmel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="var(--sky-top)"/><stop offset="1" stop-color="var(--sky-bot)"/></linearGradient>
<linearGradient id="g-wasser" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="var(--gw-top)"/><stop offset="1" stop-color="var(--gw-bot)"/></linearGradient>
<pattern id="p-erde" width="16" height="16" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><path d="M0 0v16" class="sd__hatch"/></pattern>
<g id="schnitt-def" class="sd">
  <rect class="sd__himmel" x="-200" y="0" width="1600" height="300"/>
  <path class="sd__erde" d="M-200 300H400V680H-200Z"/><path class="sd__erde" d="M820 300H1400V680H820Z"/><rect class="sd__erde" x="400" y="565" width="420" height="115"/>
  <path class="sd__erde-hatch" d="M-200 300H400V680H-200Z"/><path class="sd__erde-hatch" d="M820 300H1400V680H820Z"/><rect class="sd__erde-hatch" x="400" y="565" width="420" height="115"/>
  <path class="sd__gw" d="M-200 548q40-6 80 0t80 0 80 0 80 0 80 0 80 0 80 0 80 0 80 0 80 0 80 0 80 0 80 0 80 0 80 0 80 0 80 0 80 0 80 0 80 0V680H-200Z"/>
  <rect class="sd__kies" x="390" y="565" width="440" height="16"/>
  <rect class="sd__raum" x="436" y="112" width="348" height="168"/>
  <rect class="sd__raum" x="436" y="300" width="348" height="240"/>
  <rect class="sd__wand" x="400" y="112" width="36" height="428"/>
  <rect class="sd__wand" x="784" y="112" width="36" height="428"/>
  <rect class="sd__wand" x="400" y="280" width="420" height="20"/>
  <rect class="sd__platte" x="400" y="540" width="420" height="25"/>
  <rect class="sd__oeffnung" x="398" y="180" width="40" height="70"/><path class="sd__rahmen" d="M418 180v70"/>
  <rect class="sd__oeffnung" x="782" y="180" width="40" height="100"/><path class="sd__rahmen" d="M802 180v100"/>
  <rect class="sd__platte" x="820" y="286" width="180" height="14"/><rect class="sd__kies" x="820" y="300" width="180" height="26"/>
  <rect class="sd__wand" x="340" y="300" width="60" height="100"/><rect class="sd__schacht" x="348" y="300" width="52" height="92"/>
  <path class="sd__gitter" d="M348 300h52M352 300v6M360 300v6M368 300v6M376 300v6M384 300v6M392 300v6"/>
  <rect class="sd__oeffnung" x="398" y="340" width="40" height="50"/><path class="sd__rahmen" d="M418 340v50"/>
  <path class="sd__linie" pathLength="1" d="M-200 300H340M400 300V100M820 100V286H1000V300H1400"/>
  <path class="sd__linie sd__linie--2" pathLength="1" d="M436 112V280H784V112M436 300V540H784V300M400 540H820V565H400ZM340 300V400H400"/>
  <text class="sd__t" x="610" y="230" text-anchor="middle">Erdgeschoss</text>
  <text class="sd__t" x="610" y="332" text-anchor="middle">Keller</text>
  <text class="sd__t" x="200" y="452" text-anchor="middle">Erdreich</text>
  <text class="sd__t sd__t--gw" x="200" y="600" text-anchor="middle">Grundwasser</text>
  <text class="sd__t sd__t--terrasse" x="985" y="278" text-anchor="middle">Terrasse</text>
  {zonen}
</g>
<g id="mk-form"><circle class="mk__k" r="15"/></g>
</defs></svg>'''


def marker_svg(nr, href, aktiv=None, leiste=False):
    """Marker im Hero (aktiv=None) oder in der Schnitt-Leiste (aktiv = Nummer der Seite)."""
    x, y, label, anchor, lx = MARKER[nr]
    s = BY_NR[nr]
    cls = "mk mk-" + nr
    if aktiv is not None:
        cls += " mk--aktiv" if aktiv == nr else " mk--dim"
    title = f"{nr} {html.unescape(s['name'])}"
    cur = ' aria-current="page"' if aktiv == nr else ""
    return (f'<a class="{cls}" href="{href}" data-stelle="{nr}" style="--i:{int(nr) - 1}"{cur} aria-label="{html.escape(title)}">'
            f'<circle class="mk__hit" cx="{x}" cy="{y}" r="36"/>'
            f'<circle class="mk__k" cx="{x}" cy="{y}" r="15"/>'
            f'<text class="mk__n" x="{x}" y="{y}" text-anchor="middle" dominant-baseline="central">{nr}</text>'
            + ("" if leiste else f'<text class="mk__l" x="{lx}" y="{y}" text-anchor="{anchor}" dominant-baseline="central">{label}</text>')
            + '</a>')


def schnitt_hero():
    marks = "".join(marker_svg(s["nr"], f'#stelle-{s["nr"]}') for s in STELLEN)
    legende = "".join(
        f'<li><a href="#stelle-{s["nr"]}"><span class="mk-nr" aria-hidden="true">{s["nr"]}</span>'
        f'<span class="legende__name">{s["name"]}</span><span class="legende__ort">{s["ort"]}</span></a></li>' for s in STELLEN)
    return f'''<figure class="schnitt" id="schnitt">
  <svg class="schnitt__svg schnitt__svg--hero" viewBox="0 160 1200 460" role="img" aria-label="Schnitt durch ein Haus mit Keller: sieben Stellen, an denen Wasser eindringen kann" data-schnitt="hero" style="--zlbl:hidden">
    <use href="#schnitt-def"/>
    {marks}
  </svg>
  <figcaption class="wrap legende">
    <p class="legende__hinweis">Wählen Sie die Stelle, an der es bei Ihnen feucht ist. Jede Nummer führt zum passenden Kapitel.</p>
    <ol class="legende__liste">{legende}</ol>
  </figcaption>
</figure>'''


def schnitt_leiste(aktiv):
    marks = "".join(marker_svg(s["nr"], f'{s["slug"]}.html', aktiv=aktiv, leiste=True) for s in STELLEN)
    return (f'<svg class="schnitt__svg schnitt__svg--leiste" viewBox="300 220 720 400" role="img" '
            f'aria-label="Schnitt durch das Haus, Stelle {aktiv} hervorgehoben" style="--z{aktiv}:1;--zlbl:hidden;--lblv:hidden"><use href="#schnitt-def"/>{marks}</svg>')


def band(nr, klein=False):
    s = BY_NR[nr]
    cls = "band band--klein" if klein else "band"
    return (f'<svg class="{cls}" viewBox="{s["band"]}" data-vb="{s["band"]}" data-vb-mobil="{s["band_m"]}" preserveAspectRatio="xMidYMid slice" aria-hidden="true" '
            f'focusable="false" style="--z{nr}:1;--lblv:hidden"><use href="#schnitt-def"/></svg>')


def mk_nr(nr, ring=False):
    return f'<span class="mk-nr{" mk-nr--ring" if ring else ""}" aria-hidden="true">{nr}</span>'


# ----------------------------------------------------------------------------- Bilder
def pic(name, alt, w, h, *, sizes="(max-width: 700px) 92vw, 420px", klass="", eager=False):
    base = f"assets/img/{name}"
    srcs = (f'<source type="image/webp" srcset="{base}-640.webp 640w, {base}.webp {w}w" sizes="{sizes}">'
            f'<source type="image/jpeg" srcset="{base}-640.jpg 640w, {base}.jpg {w}w" sizes="{sizes}">')
    lazy = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    kl = f' class="{klass}"' if klass else ""
    return f'<picture{kl}>{srcs}<img src="{base}.jpg" alt="{html.escape(alt)}" width="{w}" height="{h}" {lazy}></picture>'


# ----------------------------------------------------------------------------- Rahmen
def kopf():
    return f'''<header class="kopf">
  <div class="wrap kopf__zeile">
    <a class="marke" href="index.html" aria-label="{FIRMA} {SPARTE} – Startseite">
      <img class="marke__logo" src="assets/brand/logo.png" alt="InTroTech" width="1319" height="247">
      <span class="marke__sparte">{SPARTE}</span>
    </a>
    <a class="btn btn--line kopf__cta" href="tel:{TEL_INT}">{I_TEL}<span>{TEL_ANZ}</span></a>
  </div>
</header>'''


def fuss():
    index = "".join(f'<a href="{s["slug"]}.html"><span class="fuss__nr">{s["nr"]}</span> {s["name_kurz"]}</a>' for s in STELLEN)
    return f'''<footer class="fundament">
  <div class="wrap">
    <nav class="fuss__zeile fuss__index" aria-label="Alle Stellen am Haus">{index}<a href="kontakt.html">Kontakt</a></nav>
    <div class="fuss__zeile fuss__firma">
      <a class="fuss__marke" href="index.html"><img src="assets/brand/logo-white.png" alt="InTroTech" width="1319" height="247"><span>{SPARTE}</span></a>
      <span>{STRASSE}, {ORT}</span>
      <a href="tel:{TEL_INT}">{TEL_ANZ}</a>
      <span>{ZEITEN}</span>
      <a href="{MUTTER}/" rel="noopener">introtech.de</a>
      <a href="impressum.html">Impressum</a>
      <a href="datenschutz.html">Datenschutz</a>
    </div>
  </div>
</footer>
<a class="wa-fab" href="{WA}" target="_blank" rel="noopener" aria-label="WhatsApp: Nachricht an {FIRMA} schreiben"><span class="wa-fab__pulse" aria-hidden="true"></span>{I_WA}</a>'''


def seite(*, datei, title, desc, body, jsonld="", og_type="website", body_cls=""):
    robots = "noindex, nofollow" if DEMO else "index, follow"
    url = f"{DOMAIN}/{'' if datei == 'index.html' else datei}"
    ld = f'<script type="application/ld+json">{jsonld}</script>' if jsonld else ""
    bc = f' class="{body_cls}"' if body_cls else ""
    return f'''<!DOCTYPE html>
<html lang="de" data-motion="mechanical">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{FIRMA} · {SPARTE}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMAIN}/assets/og.png">
<meta property="og:locale" content="de_DE">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#ffffff">
<link rel="icon" href="assets/brand/mark.png" type="image/png">
<link rel="apple-touch-icon" href="assets/brand/mark.png">
<link rel="preload" href="assets/fonts/FiraSans-300-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/FiraSans-400-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/fonts/_fontface.css">
<link rel="stylesheet" href="styles.css">
<script>document.documentElement.classList.add('anim')</script>
{ld}
</head>
<body{bc}>
<a class="skip" href="#inhalt">Zum Inhalt springen</a>
{schnitt_def()}
{kopf()}
<main id="inhalt">
{body}
</main>
{fuss()}
<script src="assets/js/gsap.min.js" defer></script>
<script src="assets/js/ScrollTrigger.min.js" defer></script>
<script src="assets/motion.js" defer></script>
<script src="script.js" defer></script>
</body>
</html>
'''


# ----------------------------------------------------------------------------- Seiten
def kap_kopf(nr, h, ort, ring=False, tag="h2"):
    return (f'<header class="kap__kopf">{mk_nr(nr, ring)}'
            f'<{tag} id="k{nr}" class="kap__h">{h}</{tag}><p class="kap__ort">{ort}</p></header>')


def index_body():
    kapitel = []
    for s in STELLEN:
        nr = s["nr"]
        f = s["foto"]
        kapitel.append(f'''<section class="kap kap--stelle" id="stelle-{nr}" aria-labelledby="k{nr}">
  <div class="wrap"><div class="kap__band" data-reveal="up">{band(nr)}</div></div>
  <div class="wrap lese">
    {kap_kopf(nr, s["name"], s["ort"])}
    <div class="kap__text" data-reveal="up">
      <figure class="kap__foto">{pic(f[0], f[1], f[3], f[4])}<figcaption>{f[2]}</figcaption></figure>
      <h3 class="lab">Woran Sie es erkennen</h3>
      <p>{s["erkennen"]}</p>
      <p class="kap__weiter"><a class="weiter" href="{s["slug"]}.html">Was wir an Stelle <span class="nowrap">{nr} tun{I_PFEIL}</span></a></p>
    </div>
  </div>
</section>''')
    kapitel_html = "\n".join(kapitel)

    ablauf = "".join(f'<li><span class="ablauf__n" aria-hidden="true">{i + 1}</span><h3>{t}</h3><p>{p}</p></li>'
                     for i, (t, p) in enumerate(ABLAUF))
    kette = "".join(
        f'<li class="kette__glied{" kette__glied--hier" if hier else ""}">'
        f'{"<span class=&quot;kette__hier&quot;>Diese Seite</span>" if hier else ""}'
        f'{"<a class=&quot;kette__knoten&quot; href=&quot;" + href + "&quot;" + (" rel=&quot;noopener&quot;" if href.startswith("http") else "") + ">" if not hier else "<span class=&quot;kette__knoten&quot;>"}'
        f'{ic}<strong>{t}</strong><small>{p}</small>{"</a>" if not hier else "</span>"}</li>'
        for i, (ic, t, p, href, hier) in enumerate(KETTE)).replace("&quot;", '"')
    orte = " · ".join(GEBIET)
    stellen_opts = "".join(f'<label class="chk"><input type="checkbox" name="stelle" value="{s["nr"]} {html.unescape(s["name"])}">'
                           f'<span class="mk-nr mk-nr--klein" aria-hidden="true">{s["nr"]}</span><span>{s["name"]}</span></label>' for s in STELLEN)

    hero = f'''<section class="hero" aria-labelledby="h1">
  <div class="wrap hero__kopf">
    <h1 id="h1" class="hero__h1"><span class="hero__frage">Wo kommt das Wasser her?</span> <span class="hero__antwort">Wir finden die Stelle&nbsp;– und dichten sie ab.</span></h1>
    <p class="hero__lead">Bauwerksabdichtung für Keller, Sockel, Balkon und Bodenplatte. Ein Geschäftsbereich der {FIRMA}, Gifhorn.</p>
    <div class="hero__aktion">
      <a class="btn btn--gross" href="tel:{TEL_INT}">{I_TEL}<span>{TEL_ANZ}</span></a>
      <a class="hero__runter" href="#schnitt">Stelle am Haus wählen{I_RUNTER}</a>
    </div>
    <p class="hero__orte">{orte} und Umgebung</p>
  </div>
  {schnitt_hero()}
</section>'''

    rest = f'''<section class="kap kap--ablauf" id="ablauf" aria-labelledby="k08">
  <div class="wrap lese">
    {kap_kopf("08", "So läuft es ab", "Von der Besichtigung bis zur Dokumentation", ring=True)}
    <ol class="ablauf" data-reveal="up">{ablauf}</ol>
  </div>
</section>
<section class="kap kap--verbund" id="aus-einer-hand" aria-labelledby="k09">
  <div class="wrap lese">
    {kap_kopf("09", "Aus einer Hand", f"Ein Geschäftsbereich der {FIRMA}", ring=True)}
    <div class="verbund" data-reveal="up">
    <p>Die Bauwerksabdichtung ist ein Geschäftsbereich der {FIRMA}, TÜV-zertifizierter Fachbetrieb für Leckageortung, Trocknung und Sanierung in Gifhorn. Für Sie heißt das: Die Ursache wird gefunden und abgestellt, der Schaden getrocknet und saniert. Sie haben dabei einen Ansprechpartner. Geschäftsführer sind Johann Warkentin, Jonathan Mangold und Adrian Mangold.</p>
    <ol class="kette">{kette}</ol>
    <p class="verbund__mehr">Für Klimaanlagen und energetische Beratung gibt es die Sparte <a href="{KT38}" rel="noopener">KlimaTech38{I_EXTERN}</a>. Alles über die Mutterfirma: <a href="{MUTTER}/" rel="noopener">introtech.de{I_EXTERN}</a></p>
    </div>
  </div>
</section>
<section class="kap kap--kontakt" id="kontakt" aria-labelledby="k10">
  <div class="wrap lese">
    {kap_kopf("10", "Besichtigung anfragen", "Wir kommen zu Ihnen: Gifhorn und Umgebung", ring=True)}
    <div class="anruf" data-reveal="up">
      <a class="anruf__tel" href="tel:{TEL_INT}">{TEL_ANZ}</a>
      <p class="anruf__zeiten">{I_UHR}<span>{ZEITEN} · oder per <a href="{WA}" rel="noopener">WhatsApp</a> und <a href="mailto:{MAIL}">E-Mail</a></span></p>
    </div>
    {formular(stellen_opts)}
    <p class="gebiet"><strong>Einzugsgebiet:</strong> {orte} und Umgebung.</p>
    <p class="anschrift">{I_ORT}<span>{FIRMA} · {STRASSE} · {ORT} · <a href="{ROUTE}" rel="noopener">Route planen{I_EXTERN}</a></span></p>
  </div>
</section>'''
    return hero + "\n" + kapitel_html + "\n" + rest


def formular(stellen_opts, vorwahl=None):
    return f'''<form class="form" id="formular" data-form action="mailto:{MAIL}" method="post" enctype="text/plain">
      <fieldset class="form__stellen"><legend>Wo ist es feucht? <small>(Mehrfachauswahl möglich)</small></legend>{stellen_opts}</fieldset>
      <div class="form__felder">
        <label>Name<input type="text" id="f-name" name="name" autocomplete="name" required></label>
        <label>Telefon für den Rückruf<input type="tel" id="f-tel" name="telefon" autocomplete="tel" required></label>
        <label>PLZ / Ort<input type="text" id="f-ort" name="ort" autocomplete="postal-code"></label>
        <label class="form__breit">Was haben Sie beobachtet?<textarea id="f-text" name="nachricht" rows="4" placeholder="Seit wann, wo genau, nach Regen oder immer?"></textarea></label>
      </div>
      <p class="form__hinweis" data-form-meldung hidden></p>
      <div class="form__senden"><button class="btn" type="submit"><span>Anfrage senden</span>{I_PFEIL}</button><small>Pflichtangaben: Name und Telefon. Ihre Angaben nutzen wir nur für den Rückruf (<a href="datenschutz.html">Datenschutz</a>).</small></div>
    </form>'''


def stelle_body(s):
    nr = s["nr"]
    i = int(nr) - 1
    prev = STELLEN[i - 1] if i > 0 else None
    nxt = STELLEN[i + 1] if i < len(STELLEN) - 1 else None
    f = s["foto"]
    verf = "".join(f'<div class="verf__zeile"><dt>{v}</dt><dd><span class="lab">Wann</span>{w}</dd><dd><span class="lab">Material</span>{m}</dd></div>'
                   for v, w, m in s["verfahren"])
    verwandt = "".join(f'<li><a href="{BY_NR[n]["slug"]}.html">{mk_nr(n)}<span>{BY_NR[n]["name"]}</span><small>{BY_NR[n]["ort"]}</small>{I_PFEIL}</a></li>'
                       for n in s["verwandt"])
    nachbarn = ""
    LEISTE_KURZ = {"01": "Balkon &amp; Terrasse", "02": "Sockel", "03": "Lichtschacht", "04": "Risse", "05": "Kellerwand außen", "06": "Kellerwand innen", "07": "Bodenplatte"}
    if prev:
        nachbarn += f'<a class="leiste__nachbar" href="{prev["slug"]}.html">{I_LINKS}<span>{prev["nr"]} {LEISTE_KURZ[prev["nr"]]}</span></a>'
    nachbarn += f'<a class="leiste__alle" href="index.html#schnitt">Alle Stellen</a>'
    if nxt:
        nachbarn += f'<a class="leiste__nachbar" href="{nxt["slug"]}.html"><span>{nxt["nr"]} {LEISTE_KURZ[nxt["nr"]]}</span>{I_PFEIL}</a>'
    return f'''<section class="stk" aria-labelledby="h1">
  <div class="wrap stk__grid">
    <div class="stk__text">
      <p class="stk__pfad"><a href="index.html">Bauwerksabdichtung</a> <span aria-hidden="true">/</span> Stelle {nr}</p>
      {mk_nr(nr)}
      <h1 id="h1" class="stk__h1">{s["name"]}</h1>
      <p class="stk__ort">{s["ort"]}</p>
      <p class="stk__befund">{s["befund"]}</p>
      <a class="btn" href="tel:{TEL_INT}">{I_TEL}<span>{TEL_ANZ}</span></a>
    </div>
    <nav class="leiste" aria-label="Weitere Stellen am Haus">
      {schnitt_leiste(nr)}
      <div class="leiste__nav">{nachbarn}</div>
    </nav>
  </div>
</section>
<article class="stelle">
  <div class="wrap"><div class="kap__band kap__band--gross" data-reveal="up">{band(nr)}</div></div>
  <div class="wrap lese">
    <div data-reveal="up">
    <h2 class="kap__h2">Befund und Ursache</h2>
    <h3 class="lab">Woran Sie es erkennen</h3>
    <p>{s["erkennen"]}</p>
    <figure class="stelle__foto">{pic(f[0], f[1], f[3], f[4], sizes="(max-width: 1100px) 92vw, 1040px")}<figcaption>{f[2]}</figcaption></figure>
    <h3 class="lab">Was wir tun</h3>
    <p>{s["tun"]}</p>
    </div>
    <div data-reveal="up">
    <h2 class="kap__h2">Verfahren</h2>
    <dl class="verf">{verf}</dl>
    </div>
    <div data-reveal="up">
    <h2 class="kap__h2">Wann das nicht reicht</h2>
    <p>{s["grenzen"]}</p>
    </div>
    <div data-reveal="up">
    <h2 class="kap__h2">Verwandte Stellen</h2>
    <ul class="verwandt">{verwandt}</ul>
    </div>

    <aside class="abschluss" data-reveal="up" aria-labelledby="abschluss-h">
      <h2 id="abschluss-h">Feucht an dieser Stelle?</h2>
      <a class="anruf__tel" href="tel:{TEL_INT}">{TEL_ANZ}</a>
      <p>{ZEITEN} · Wir sehen es uns vor Ort an und sagen Ihnen, was zu tun ist.</p>
      <a class="btn" href="kontakt.html?stelle={nr}"><span>Besichtigung anfragen, Stelle&nbsp;{nr} vorgemerkt</span>{I_PFEIL}</a>
    </aside>
  </div>
</article>'''


def kontakt_body():
    stellen_opts = "".join(f'<label class="chk"><input type="checkbox" name="stelle" value="{s["nr"]} {html.unescape(s["name"])}">'
                           f'<span class="mk-nr mk-nr--klein" aria-hidden="true">{s["nr"]}</span><span>{s["name"]}</span></label>' for s in STELLEN)
    orte = " · ".join(GEBIET)
    return f'''<section class="ak" aria-labelledby="h1">
  <div class="wrap lese">
    <p class="stk__pfad"><a href="index.html">Bauwerksabdichtung</a> <span aria-hidden="true">/</span> Kontakt</p>
    <h1 id="h1" class="ak__h1">Besichtigung anfragen</h1>
    <div class="anruf anruf--gross">
      <a class="anruf__tel" href="tel:{TEL_INT}">{TEL_ANZ}</a>
      <p class="anruf__zeiten">{I_UHR}<span>{ZEITEN} · oder per <a href="{WA}" rel="noopener">WhatsApp</a> und <a href="mailto:{MAIL}">E-Mail</a></span></p>
    </div>
    <p class="ak__text">Ein Anruf reicht: Sie beschreiben, wo es feucht ist, wir kommen vorbei, messen und sagen Ihnen, welche Stelle betroffen ist und was dort zu tun ist. Wenn Sie lieber schreiben, nutzen Sie das Formular. Wir rufen zurück.</p>
    {formular(stellen_opts)}
    <p class="gebiet"><strong>Einzugsgebiet:</strong> {orte} und Umgebung.</p>
    <p class="anschrift">{I_ORT}<span>{FIRMA} · {STRASSE} · {ORT} · <a href="{ROUTE}" rel="noopener">Route planen{I_EXTERN}</a></span></p>
  </div>
</section>'''


def impressum_body():
    return f'''<article class="lese lese--recht wrap">
  <h1>Impressum</h1>
  <p class="recht__stand">Angaben gemäß § 5 DDG (Digitale-Dienste-Gesetz)</p>
  <h2>Anbieter</h2>
  <p>{FIRMA}<br>{STRASSE}<br>{ORT}<br>Deutschland</p>
  <p><strong>{SPARTE}</strong> ist ein Geschäftsbereich der {FIRMA} und keine eigene Rechtspersönlichkeit.</p>
  <h2>Vertreten durch</h2>
  <p>Geschäftsführer: Johann Warkentin, Jonathan Mangold, Adrian Mangold</p>
  <h2>Kontakt</h2>
  <p>Telefon: <a href="tel:{TEL_INT}">{TEL_ANZ}</a><br>E-Mail: <a href="mailto:{MAIL}">{MAIL}</a></p>
  <h2>Registereintrag</h2>
  <p>Eintragung im Handelsregister<br>Registergericht: Amtsgericht Hildesheim<br>Registernummer: HRB 210481</p>
  <h2>Umsatzsteuer-Identifikationsnummer</h2>
  <p>USt-IdNr. gemäß § 27a Umsatzsteuergesetz: DE460142356</p>
  <h2>Verantwortlich für den Inhalt nach § 18 Abs. 2 MStV</h2>
  <p>Die Geschäftsführung, Anschrift wie oben.</p>
  <h2>Verbraucherstreitbeilegung</h2>
  <p>Beschwerden nehmen wir per E-Mail an die oben genannte Adresse entgegen. Wir sind nicht bereit und nicht verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p>
  <h2>Bildnachweis</h2>
  <p>Die Fotos auf dieser Seite sind Symbolfotos von Pexels (lizenzfrei). Die Schnittzeichnungen sind schematische eigene Darstellungen, keine Ausführungspläne.</p>
  <p><a class="weiter" href="index.html">{I_LINKS}Zurück zur Startseite</a></p>
</article>'''


def datenschutz_body():
    return f'''<article class="lese lese--recht wrap">
  <h1>Datenschutzerklärung</h1>
  <p class="recht__stand">Stand: September {JAHR}</p>
  <h2>1 · Verantwortlicher</h2>
  <p>{FIRMA}, {STRASSE}, {ORT}, Deutschland · Telefon <a href="tel:{TEL_INT}">{TEL_ANZ}</a> · E-Mail <a href="mailto:{MAIL}">{MAIL}</a>. Vertreten durch die Geschäftsführung (Johann Warkentin, Jonathan Mangold, Adrian Mangold). {SPARTE} ist ein Geschäftsbereich der {FIRMA}.</p>
  <h2>2 · Grundsätzliches</h2>
  <p>Wir verarbeiten personenbezogene Daten nur, soweit das für den Betrieb dieser Website und die Bearbeitung Ihrer Anfragen erforderlich ist. Diese Website setzt <strong>keine Cookies</strong>, bindet <strong>kein Tracking</strong>, <strong>keine Werbenetzwerke</strong> und <strong>keine Kartendienste</strong> ein. Schriften und Skripte liegen auf unserem eigenen Webspace – beim Aufruf der Seite werden dafür keine Daten an Dritte übertragen.</p>
  <h2>3 · Hosting und Server-Logfiles</h2>
  <p>Diese Website wird bei Vercel Inc., 440 N Barranca Ave #4133, Covina, CA 91723, USA, gehostet und über deren Netzwerk auch aus Europa ausgeliefert. Beim Aufruf übermittelt Ihr Browser technisch notwendige Daten, die in Logfiles gespeichert werden: IP-Adresse, Datum und Uhrzeit, aufgerufene Datei, übertragene Datenmenge, Referrer und Browserkennung. Diese Daten dienen dem sicheren und stabilen Betrieb der Seite; Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO. Mit Vercel besteht ein Auftragsverarbeitungsvertrag mit EU-Standardvertragsklauseln. Die Logfiles werden nach kurzer Zeit gelöscht.</p>
  <h2>4 · Kontaktaufnahme und Anfrageformular</h2>
  <p>Wenn Sie uns über das Formular, per E-Mail, Telefon oder WhatsApp kontaktieren, verarbeiten wir Ihre Angaben zur Bearbeitung der Anfrage und für den Fall von Anschlussfragen. Das Formular öffnet eine E-Mail in Ihrem eigenen E-Mail-Programm; es werden keine Daten auf unserem Server gespeichert. Pflichtangaben sind Name und Telefonnummer, damit wir zurückrufen können; alle weiteren Angaben sind freiwillig. Rechtsgrundlage ist Art. 6 Abs. 1 lit. b DSGVO (vorvertragliche Maßnahmen). Wir löschen die Daten, sobald sie für den Zweck nicht mehr erforderlich sind und keine gesetzlichen Aufbewahrungsfristen entgegenstehen.</p>
  <h2>5 · Externe Links, WhatsApp und Routenplanung</h2>
  <p>Die WhatsApp-Schaltfläche, der Link „Route planen“ (OpenStreetMap) und die Links zu introtech.de und KlimaTech38 sind einfache Links. Erst wenn Sie darauf klicken, öffnet sich der jeweilige Dienst und es entsteht eine Verbindung zu dessen Anbieter (bei WhatsApp: WhatsApp Ireland Limited). Dort gelten zusätzlich die Datenschutzbestimmungen des Anbieters. Wenn Sie das vermeiden möchten, erreichen Sie uns ebenso per Telefon oder E-Mail.</p>
  <h2>6 · Ihre Rechte</h2>
  <p>Sie haben das Recht auf Auskunft (Art. 15 DSGVO), Berichtigung (Art. 16), Löschung (Art. 17), Einschränkung der Verarbeitung (Art. 18), Datenübertragbarkeit (Art. 20) und Widerspruch gegen Verarbeitungen auf Grundlage berechtigter Interessen (Art. 21). Wenden Sie sich dafür an die oben genannten Kontaktdaten. Sie können sich außerdem bei einer Aufsichtsbehörde beschweren; zuständig ist für uns die Landesbeauftragte für den Datenschutz Niedersachsen, Prinzenstraße 5, 30159 Hannover.</p>
  <h2>7 · Verschlüsselung</h2>
  <p>Diese Website wird über HTTPS ausgeliefert. Die Übertragung zwischen Ihrem Browser und dem Server ist damit verschlüsselt.</p>
  <p><a class="weiter" href="index.html">{I_LINKS}Zurück zur Startseite</a></p>
</article>'''


def jsonld_index():
    leistungen = ", ".join('{"@type":"Offer","itemOffered":{"@type":"Service","name":"%s","url":"%s/%s.html"}}'
                           % (html.unescape(s["name"]).replace('"', ''), DOMAIN, s["slug"]) for s in STELLEN)
    orte = ",".join(f'{{"@type":"City","name":"{o}"}}' for o in GEBIET)
    return ('{"@context":"https://schema.org","@type":"HomeAndConstructionBusiness",'
            f'"name":"{FIRMA} – {SPARTE}","url":"{DOMAIN}/","image":"{DOMAIN}/assets/og.png","logo":"{DOMAIN}/assets/brand/logo.png",'
            f'"telephone":"{TEL_INT}","email":"{MAIL}",'
            f'"address":{{"@type":"PostalAddress","streetAddress":"{STRASSE}","postalCode":"38518","addressLocality":"Gifhorn","addressCountry":"DE"}},'
            '"openingHoursSpecification":{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"08:00","closes":"18:00"},'
            f'"areaServed":[{orte}],'
            f'"parentOrganization":{{"@type":"Organization","name":"{FIRMA}","url":"{MUTTER}/","vatID":"DE460142356"}},'
            f'"hasOfferCatalog":{{"@type":"OfferCatalog","name":"Bauwerksabdichtung","itemListElement":[{leistungen}]}},'
            f'"sameAs":["{MUTTER}/"]}}')


def jsonld_stelle(s):
    return ('{"@context":"https://schema.org","@type":"Service",'
            f'"name":"{html.unescape(s["name"])}","serviceType":"Bauwerksabdichtung","url":"{DOMAIN}/{s["slug"]}.html",'
            f'"description":"{s["desc"]}",'
            f'"provider":{{"@type":"HomeAndConstructionBusiness","name":"{FIRMA} – {SPARTE}","telephone":"{TEL_INT}","url":"{DOMAIN}/"}},'
            f'"areaServed":[{",".join(chr(34) + o + chr(34) for o in GEBIET)}]}}')


def main():
    seiten = {}
    seiten["index.html"] = seite(
        datei="index.html",
        title="Bauwerksabdichtung Gifhorn – Keller & Sockel abdichten | InTroTech",
        desc="Sieben Stellen, an denen ein Haus undicht wird – und was wir dort tun: Kellerabdichtung, Horizontalsperre, Rissinjektion, Balkon, Bodenplatte. InTroTech, Gifhorn.",
        body=index_body(), jsonld=jsonld_index(), body_cls="ist-start")
    for s in STELLEN:
        seiten[f'{s["slug"]}.html'] = seite(datei=f'{s["slug"]}.html', title=s["title"] + " | InTroTech", desc=s["desc"],
                                            body=stelle_body(s), jsonld=jsonld_stelle(s))
    seiten["kontakt.html"] = seite(
        datei="kontakt.html", title="Besichtigung anfragen – Bauwerksabdichtung Gifhorn | InTroTech",
        desc="Feuchter Keller, nasser Sockel, Wasser am Balkon? Rufen Sie an: 05371 8759972, Mo–Fr 08–18 Uhr. Wir kommen nach Gifhorn, Wolfsburg, Braunschweig und Umgebung.",
        body=kontakt_body())
    seiten["impressum.html"] = seite(datei="impressum.html", title="Impressum – InTroTech Bauwerksabdichtung",
                                     desc="Impressum der InTroTech GmbH, Zeisigweg 4, 38518 Gifhorn – Anbieterkennzeichnung für die Sparte Bauwerksabdichtung.",
                                     body=impressum_body())
    seiten["datenschutz.html"] = seite(datei="datenschutz.html", title="Datenschutzerklärung – InTroTech Bauwerksabdichtung",
                                       desc="Datenschutzerklärung der InTroTech GmbH für die Website der Sparte Bauwerksabdichtung: keine Cookies, kein Tracking, Hosting, Kontaktformular, Ihre Rechte.",
                                       body=datenschutz_body())
    for name, inhalt in seiten.items():
        (ROOT / name).write_text(inhalt, encoding="utf-8")
    # sitemap + robots
    urls = "".join(f'<url><loc>{DOMAIN}/{"" if n == "index.html" else n}</loc><changefreq>monthly</changefreq><priority>{"1.0" if n == "index.html" else ("0.8" if n.endswith(".html") and n not in ("impressum.html", "datenschutz.html") else "0.3")}</priority></url>'
                   for n in seiten)
    (ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n', encoding="utf-8")
    robots = ("User-agent: *\nDisallow: /\n" if DEMO else "User-agent: *\nAllow: /\n") + f"Sitemap: {DOMAIN}/sitemap.xml\n"
    (ROOT / "robots.txt").write_text(robots, encoding="utf-8")
    print(f"{len(seiten)} Seiten geschrieben nach {ROOT}")


if __name__ == "__main__":
    main()
