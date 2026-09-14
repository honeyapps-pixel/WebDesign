#!/usr/bin/env python3
"""bs_gen.py – Seiten-Generator für die BAUSCHULZ-Demo (bauschulz/).

Erzeugt alle HTML-Seiten aus EINER Content-Quelle (Kopf/Fuß/Kontakt-Kurzform bleiben über alle
Seiten identisch). Inhalte stammen 1:1 von bauschulz.com + dem unfertigen Relaunch-Entwurf des
Kunden (siehe bauschulz/README.md). Nichts erfunden – offene Punkte stehen im README.

Aufruf:  python3 .tools/bs_gen.py
"""
import html
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "bauschulz"
DOMAIN = "https://bauschulz.com"
FACEBOOK = "https://www.facebook.com/BauschulzGmbH/"
GOOGLE = "https://www.google.com/maps/search/?api=1&query=BAUSCHULZ+GmbH+Fehringstra%C3%9Fe+8+38524+Sassenburg"
ROUTE = "https://www.google.com/maps/dir/?api=1&destination=Fehringstra%C3%9Fe+8%2C+38524+Sassenburg"
TEL_ANZ = "0176 31482066"
TEL_INT = "+4917631482066"
WA = "https://wa.me/4917631482066"
MAIL = "info@bauschulz.com"
FIRMA = "BAUSCHULZ GmbH & Co. KG"
ADRESSE = "Fehringstraße 8, 38524 Sassenburg"
JAHR = "2026"

# ----------------------------------------------------------------------------- SVG-Bausteine
GIEBEL = '<svg class="giebel" viewBox="0 0 270 270" aria-hidden="true" focusable="false"><path d="M108 40h54l84 206h-50L135 96 74 246H24z"/></svg>'
I_TEL = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A17 17 0 0 1 3 5a2 2 0 0 1 2-2z"/></svg>'
I_MAIL = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="1.5"/><path d="m4 7 8 6 8-6"/></svg>'
I_PFEIL = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
I_LINKS = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M19 12H5M11 18l-6-6 6-6"/></svg>'
I_RECHTS = I_PFEIL
I_PLUS = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>'
I_X = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>'
I_UHR = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>'
I_FB = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M13.5 22v-8h2.7l.4-3.2h-3.1V8.8c0-.9.3-1.6 1.6-1.6h1.7V4.4c-.3 0-1.3-.1-2.5-.1-2.5 0-4.1 1.5-4.1 4.2v2.3H7.4V14h2.8v8h3.3z"/></svg>'
I_ORT = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-6-5.3-6-11a6 6 0 0 1 12 0c0 5.7-6 11-6 11z"/><circle cx="12" cy="10" r="2.2"/></svg>'
I_WA = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.885-9.886 9.885M20.52 3.449C18.24 1.245 15.24 0 12.045 0 5.463 0 .104 5.359.101 11.945c0 2.096.549 4.14 1.595 5.945L0 24l6.335-1.652a11.96 11.96 0 005.71 1.454h.006c6.585 0 11.946-5.359 11.949-11.945a11.86 11.86 0 00-3.495-8.411z"/></svg>'


def pic(name, alt, *, w, h, sizes="(max-width: 880px) 100vw, 50vw", klein=800, eager=False, klass=""):
    """<picture> mit webp/jpg + kleiner Stufe (falls vorhanden)."""
    base = f"assets/img/{name}"
    hat_klein = (ROOT / "assets/img" / f"{name}-{klein}.jpg").exists()
    if hat_klein:
        ws = f"{base}-{klein}.webp {klein}w, {base}.webp {w}w"
        js = f"{base}-{klein}.jpg {klein}w, {base}.jpg {w}w"
        srcs = f'<source type="image/webp" srcset="{ws}" sizes="{sizes}"><source type="image/jpeg" srcset="{js}" sizes="{sizes}">'
    else:
        srcs = f'<source type="image/webp" srcset="{base}.webp">'
    lazy = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    kl = f' class="{klass}"' if klass else ""
    return f'<picture{kl}>{srcs}<img src="{base}.jpg" alt="{html.escape(alt)}" width="{w}" height="{h}" {lazy}></picture>'


# ----------------------------------------------------------------------------- CONTENT
# Bautagebuch – O-Ton des Betriebs (Relaunch-Entwurf „So kann’s aussehen"), leicht korrekturgelesen.
PHASEN = [
    dict(n=1, t="Planung", sub="Vor dem ersten Spatenstich", img=None,
         p="Vor Baubeginn muss zunächst eine Bauplanung vom Architekten erstellt werden. Diese muss mittels eines Bauantrags im jeweiligen Bauamt genehmigt werden. Um die Planungsphase abzuschließen, muss die Baumaßnahme von einem Statiker berechnet werden."),
    dict(n=2, t="Fundamente ausheben", sub="Schnurgerüst und Minibagger", img="t02-fundamente-ausheben",
         p="Los geht’s. Nach Fertigstellung der Sandplatte wird ein Schnurgerüst aufgestellt. Nun können die Fundamente mit dem Minibagger entlang der Schnüre ausgehoben werden. Nach dem Ausheben werden noch Eisen und der Fundamenterder eingebaut."),
    dict(n=3, t="Fundamente betonieren", sub="Gründung und Frostschürze", img="t03-fundamente-betonieren",
         p="Jetzt kann der Betonmischer kommen. Die Fundamente werden betoniert. Sie dienen neben der stabilen Gründung gleichzeitig als Frostschürze."),
    dict(n=4, t="Bodenplatte einschalen", sub="Entwässerung, Folie, Bewehrung", img="t04-bodenplatte-einschalen",
         p="Bevor wir die Bodenplatte mit Holzbohlen einschalen, bauen wir noch die Entwässerung mit KG-Rohren ein und lassen diese 50 cm aus dem Baukörper herausstehen. Danach Baufolie ausbreiten, um darauf Unter- und Oberbewehrung einzubauen."),
    dict(n=5, t="Bodenplatte betonieren", sub="Betonpumpe und Rüttelpatsche", img="t05-bodenplatte-betonieren",
         p="Am besten bringt der Betonmischer auch eine Betonpumpe mit, um den Beton gleichmäßig und präzise einzubauen. Wenn der Beton eingebaut ist, fahren wir die Fläche mit der Rüttelpatsche ab, um Lufteinschlüsse zu vermeiden."),
    dict(n=6, t="Mauerwerk anlegen", sub="Erdgeschoss · Kimmschicht", img="t06-mauerwerk-anlegen",
         p="Nach ein paar Tagen Ruhe für die Bodenplatte werden Material und Hilfsmittel auf der Platte angeordnet. Bevor wir mit der Kimmschicht beginnen, wird unter allen Wänden die Mauersperrbahn verschweißt. Die Kimmschicht liegt im Mörtelbett und ist die unterste Steinschicht: Sie gleicht alle Unebenheiten des Betons aus und bildet eine plane Oberfläche."),
    dict(n=7, t="Mauerwerk kleben", sub="Erdgeschoss · Kalksandstein im Verband", img="t07-mauerwerk-kleben",
         p="Nun werden die großformatigen Kalksandsteine mit dem Versetzkran im Verband aufeinander geklebt. Bei Türöffnungen wird ein Sturz eingebaut. Fensteröffnungen bleiben meist deckengleich, um Platz für den Rollladenkasten zu haben."),
    dict(n=8, t="Filigrandecke verlegen", sub="Erdgeschoss · stützen, verlegen, armieren", img="t08-filigrandecke-eg",
         p="Bevor die Filigrandecke auf die fertigen Wände kommt, muss die künftige Decke von unten gestützt werden – mit ausreichend Drehsteifen und Dokaträgern. Filigranelemente sind fertig gelieferte, mit Eisen armierte Betonplatten und bilden die erste Deckenschicht. Dann kommen Kabel für die Deckenbeleuchtung hinein, Durchlässe für Wasser- und Abwasserleitungen werden vorbereitet, jede Menge Eisen eingebaut und die Decke außen herum mit Bohlen eingeschalt."),
    dict(n=9, t="Decke betonieren", sub="Erdgeschoss", img="t09-decke-betonieren",
         p="Wenn alle wichtigen Dinge in der Decke liegen, kann betoniert werden. Den frischen Beton fahren wir wieder mit der Rüttelpatsche ab, um eine möglichst gerade Deckenoberfläche zu bekommen."),
    dict(n=10, t="Mauerwerk Obergeschoss", sub="Zweite Runde mit dem Versetzkran", img="t10-mauerwerk-og",
         p="Nach kurzer Ruhephase wird die Decke wieder mit Material und Maschinen bestückt. Die Wand beginnt erneut mit der Kimmschicht, danach kleben wir mit großformatigen Steinen und dem Versetzkran weiter."),
    dict(n=11, t="Filigrandecke Obergeschoss", sub="Zweite Betondecke", img="t11-filigrandecke-og",
         p="Bei diesem Bauvorhaben ist eine zweite Betondecke geplant – gleicher Vorgang wie im Erdgeschoss: Filigranelemente präzise mit dem Turmdrehkran verlegen, mit Holzbohlen ringsum einschalen, ebenso den Luftraum von innen."),
    dict(n=12, t="Decke armieren und betonieren", sub="Obergeschoss · Leitungen, Lüftung, Eisen", img="t12-decke-armieren-og",
         p="Strom-, Wasser- und Abwasserleitungen verlegen, die Rohrleitungen für die Lüftungsanlage installieren: Die blauen Rohre sind Zuluft, die roten Abluft. Dann wird die Decke mit Eisen bewehrt. Jetzt kann der Betonmischer wieder kommen – wir pumpen den Beton hoch, bauen präzise nach Laser ein und ziehen zum Schluss mit der Rüttelpatsche ab."),
    dict(n=13, t="Richtfest", sub="Der Dachstuhl steht", img="t13-richtfest",
         p="Ein paar Tage nach dem Betonieren stellen wir den Dachstuhl auf und verankern ihn in der Decke. Nach getaner Arbeit gibt’s ein Grillerchen mit allen Baubeteiligten, Familie, Freunden und Nachbarn."),
    dict(n=14, t="Dach vorbereiten", sub="Unterspannbahn und Lattung", img="t14-dach-vorbereiten",
         p="Auf den Dachstuhl wird die Unterspannbahn getackert. Anschließend wird das Dach auf das entsprechende Ziegelmaß eingelattet."),
    dict(n=15, t="Dach eindecken", sub="Ortgang zuerst, dann die Fläche", img="t15-dach-eindecken",
         p="Wir fangen mit den Dachrändern – den Ortgangziegeln – an und decken anschließend das gesamte Dach ein. Lüftungsziegel werden zwischendurch an der richtigen Stelle für die Entlüftung eingebaut."),
    dict(n=16, t="Schlüsselfertig", sub="So kann’s aussehen", img="t16-schluesselfertig",
         p="Dach gedeckt, Photovoltaik auf dem Dach, Garten angelegt – fertig. So könnte auch Ihr Bauprojekt aussehen. Machen Sie sich ein eigenes Bild und sprechen Sie uns an."),
]
INDEX_PHASEN = [1, 2, 5, 7, 9, 13, 15, 16]

# Referenzen – Daten 1:1 von bauschulz.com (Projekt · Ort · Fläche · Fertigstellung), chronologisch.
PROJEKTE = [
    dict(slug="seniorenwohnanlage-wittingen", name="Seniorenwohnanlage Wittingen", kurz="Seniorenwohnanlage", ort="Wittingen", jahr="2014",
         flaeche="1.400 m²", flaeche_art="Wohn- und Nutzfläche", art="Mehrfamilienhaus · barrierefrei", lat=52.7289, lon=10.7357,
         bilder=[("p-wittingen-1", 1600, 1066, "Seniorenwohnanlage Wittingen: dreigeschossiger Neubau mit Balkonen und Grünanlage"),
                 ("p-wittingen-2", 1200, 800, "Seniorenwohnanlage Wittingen: Balkone mit Metallgeländern an der Gartenseite"),
                 ("p-wittingen-3", 1200, 800, "Seniorenwohnanlage Wittingen: Ansicht von der Straße mit Zufahrt"),
                 ("p-wittingen-4", 1200, 800, "Seniorenwohnanlage Wittingen: Giebelseite mit Balkonen und Straßenlaterne"),
                 ("p-wittingen-5", 900, 1349, "Seniorenwohnanlage Wittingen: Seitenansicht mit Balkonen zur Zufahrt"),
                 ("p-wittingen-6", 900, 1349, "Seniorenwohnanlage Wittingen: Hauseingang mit Vordach und gepflastertem Vorplatz")],
         punkte=["1 Gebäude mit 21 Wohneinheiten, barrierefrei", "Fahrstuhl, behindertengerecht", "Alle Wohnungen mit Balkon, Terrasse und Kellerraum", "Notfalltreppenhaus", "12 Einstellplätze und ein behindertengerechter Parkplatz", "Dreifachverglasung, elektrische Rollos", "Solarunterstützung der Brennwertheizung, Fußbodenheizung", "Photovoltaik mit 29,9 kWp", "Videogegensprechanlage mit Display"],
         text=None, leistung="neubau"),
    dict(slug="einfamilienhaus-sassenburg", name="Einfamilienhaus Sassenburg", kurz="Einfamilienhaus", ort="Sassenburg", jahr="2016",
         flaeche="180 m²", flaeche_art="Wohnfläche", art="Einfamilienhaus · schlüsselfertig", lat=52.5220, lon=10.6466,
         bilder=[("p-efh-sassenburg-1", 1600, 1051, "Einfamilienhaus Sassenburg: Bungalow mit Klinker-Garage und weißer Putzfassade")],
         punkte=None, leistung="neubau",
         text=["Sie betreten das Haus mittig über eine schicke Hauseingangstür mit Seitenglas und stehen im offenen Eingangsbereich.",
               "Weiter gelangen Sie geradeaus in den Wohnbereich mit gemütlicher Sitzgruppe. Daneben ist der Essbereich mit viel Platz für einen großen Esstisch. Die Küche ist offen und parallel zum Esstisch in Form einer Insel angelegt, die Elektrogeräte sind in der Wand dahinter eingelassen. Der Wohn-, Koch- und Essbereich ist ein heller Raum mit großen bodentiefen Fenstern und einem Hebe-Schiebeelement. Ein weiteres Highlight ist die Deckenhöhe von 4,60 m. Vom Kochbereich kommt man in den Hauswirtschaftsraum, der genügend Stauraum für Lebensmittel, Wäsche etc. bietet – hier können Waschmaschine und Trockner stehen.",
               "Vom Hauswirtschaftsraum gibt es einen Zugang in den Garten und in die Garage. Die Garage bietet Platz für mindestens ein Auto plus Motorrad, Werkbänke und Regale. Von der Garage aus gelangen Sie in den Hausanschlussraum, in dem sich die Heizungsanlage, der Sicherungskasten und alle Hausanschlüsse befinden. Das Garagentor ist 5 m breit.",
               "Vom Eingangsbereich gehen Sie weiter in einen kleinen Flur, von dem aus Gästezimmer bzw. Büro und Gästebad erreichbar sind. Das Gästezimmer ist mit einem großen Eckfenster sehr gut ausgeleuchtet. Das innenliegende Gäste-WC ist mit einer ebenerdigen Dusche ausgestattet; über die Lichtkuppel an der Decke gibt es trotzdem genügend Tageslicht und die Möglichkeit zu lüften.",
               "Vom Wohnbereich gelangen Sie in einen weiteren Flur. Er trennt den Privatbereich – zwei Kinderzimmer, Kinderbad und Elternbereich – vom Wohnbereich. Die Kinderzimmer sind geräumig und ebenfalls mit großen bodentiefen Fenstern ausgestattet. Das Kinderbad verfügt neben Waschbecken und Toilette über eine bodentiefe Dusche. Der Elternbereich ist in Ankleide und großen Schlafbereich aufgeteilt, dazu ein Bad mit Dusche und Badewanne.",
               "Die Gartenanlage ums Haus wurde liebevoll gestaltet. Machen Sie sich ein eigenes Bild vor Ort bei einem Besichtigungstermin."],
         ausstattung="Der gesamte Wohnbereich ist mit Echtholzparkett ausgestattet. Die Bäder sind mit großformatigen Fliesen hergerichtet, jedes im eigenen Stil. Alle Wände im Haus sind weiß gestrichen, die Innentüren weiß und stumpf einschlagend. Heizung: Gastherme mit Solarunterstützung, Fußbodenheizung im gesamten Haus inklusive Garage. Smart Home: Die Hauselektrik ist über ein Bussystem jederzeit umprogrammierbar und zusätzlich per Smartphone steuerbar. Ein Staubsaugersystem ist im Haus installiert. In den Bädern sind ausschließlich hochwertige Keramikobjekte, Armaturen und Möbel verbaut. Die Küche ist Bestandteil des Hauses und wird mit allen Geräten angeboten. Das Grundstück wird von einem Kamerasystem überwacht."),
    dict(slug="sozialer-wohnungsbau-knesebeck", name="Sozialer Wohnungsbau Knesebeck", kurz="Sozialer Wohnungsbau", ort="Knesebeck", jahr="2017",
         flaeche="885 m²", flaeche_art="Wohnfläche", art="Mehrfamilienhaus · 10 Einheiten", lat=52.6789, lon=10.7026,
         bilder=[("p-knesebeck-1", 1600, 1066, "Sozialer Wohnungsbau Knesebeck: Mehrfamilienhaus mit Satteldach und Photovoltaik von der Straße"),
                 ("p-knesebeck-2", 1200, 800, "Sozialer Wohnungsbau Knesebeck: Straßenecke mit zweifarbiger Putzfassade unter Bäumen"),
                 ("p-knesebeck-3", 1200, 800, "Sozialer Wohnungsbau Knesebeck: Giebelseite mit weißer Putzfassade und Satteldach"),
                 ("p-knesebeck-4", 1200, 800, "Sozialer Wohnungsbau Knesebeck: Holz-Sichtschutz und gepflasterter Gartenweg an der Gebäudeseite"),
                 ("p-knesebeck-5", 1200, 800, "Sozialer Wohnungsbau Knesebeck: Rückseite mit Photovoltaik auf dem Dach"),
                 ("p-knesebeck-6", 900, 1349, "Sozialer Wohnungsbau Knesebeck: zweifarbige Fassade mit Fenstern zur Straße"),
                 ("p-knesebeck-7", 900, 1349, "Sozialer Wohnungsbau Knesebeck: Fassadendetail mit Fallrohr und gepflastertem Weg")],
         punkte=["1 Gebäude mit 10 Einheiten auf drei Etagen", "Pflegeleichte Zweizimmer-Wohneinheiten mit Vinylboden, Badezimmer gefliest", "Großzügiges Treppenhaus", "Videogegensprechanlage", "Photovoltaikanlage mit 29,9 kWp"],
         text=None, leistung="neubau"),
    dict(slug="garagenpark-sassenburg", name="Garagenpark Sassenburg", kurz="Garagenpark", ort="Sassenburg", jahr="2018",
         flaeche="980 m²", flaeche_art="Nutzfläche", art="Gewerbe · 28 Garagen", lat=52.5150, lon=10.6300,
         bilder=[("p-garagenpark-1", 1600, 1066, "Garagenpark Sassenburg: Garagenzeile mit anthrazitfarbenen Sektionaltoren"),
                 ("p-garagenpark-2", 1200, 799, "Garagenpark Sassenburg: gepflasterte Fahrgasse zwischen zwei Garagenzeilen"),
                 ("p-garagenpark-3", 1200, 799, "Garagenpark Sassenburg: Sektionaltore in Reihe"),
                 ("p-garagenpark-4", 1200, 799, "Garagenpark Sassenburg: Schlüsselschalter neben Sektionaltor Nr. 5"),
                 ("p-garagenpark-5", 1200, 799, "Garagenpark Sassenburg: Garagenzeile mit Zufahrt"),
                 ("p-garagenpark-6", 900, 1350, "Garagenpark Sassenburg: zwei Garagen mit Sektionaltoren und Wandleuchte")],
         punkte=["28 Garagen mit je 35 m²", "3 × 3 Meter Sektionaltor", "Jede Garage mit separater Unterverteilung, LED-Beleuchtung, 6 × 230-Volt-Steckdose und 1 × 32-Ampere-Starkstromanschluss", "Gesamtes Gelände beleuchtet und videoüberwacht"],
         text=None, leistung="gewerbe-industrie"),
    dict(slug="doppelhaus-gifhorn", name="Doppelhaus Gifhorn", kurz="Doppelhaus", ort="Gifhorn", jahr="2020",
         flaeche="380 m²", flaeche_art="Wohnfläche", art="Doppelhaus · 2 Wohneinheiten", lat=52.4874, lon=10.5463,
         bilder=[("p-doppelhaus-1", 1600, 1200, "Doppelhaus Gifhorn: weißer Putz im Obergeschoss, grauer Klinker im Erdgeschoss, Außengerät der Luftwärmepumpe an der Seitenwand")],
         punkte=["Zwei Wohneinheiten mit jeweils ca. 190 m², je drei Schlafzimmer und ein Ankleideraum", "Großzügiger Wohn-Essbereich", "Fußbodenheizung", "Luftwärmepumpe", "Videogegensprechanlage", "Bodentiefe Duschen", "Massive Betontreppe, gefliest"],
         text=None, leistung="neubau"),
    dict(slug="wohnanlage-wolfsburg-ehmen", name="Wohnanlage Wolfsburg-Ehmen", kurz="Wohnanlage · 14 Einheiten", ort="Wolfsburg-Ehmen", jahr="2020",
         flaeche="1.000 m²", flaeche_art="Wohnfläche", art="Wohnanlage · 3 Gebäude", lat=52.3991, lon=10.6992,
         bilder=[("p-ehmen-1", 1024, 768, "Wohnanlage Wolfsburg-Ehmen: zwei der drei Gebäude mit weißer Putzfassade und Glasbalkonen an der gepflasterten Zufahrt"),
                 ("p-ehmen-2", 1024, 768, "Wohnanlage Wolfsburg-Ehmen: Zufahrt zwischen den Gebäuden, Dachterrasse mit Glasgeländer"),
                 ("p-ehmen-3", 768, 1024, "Wohnanlage Wolfsburg-Ehmen: Gebäude mit Penthouse und umlaufender Dachterrasse von der Zufahrt"),
                 ("p-ehmen-4", 768, 1024, "Wohnanlage Wolfsburg-Ehmen: Bad mit großformatigen grauen Fliesen und bodentiefer Dusche"),
                 ("p-ehmen-5", 768, 1024, "Wohnanlage Wolfsburg-Ehmen: Wohn-Essbereich mit offener Küche und Boden in Holzoptik")],
         punkte=["3 Gebäude: 2 × 5 Einheiten auf drei Etagen mit Penthousewohnung und 1 × 4 Einheiten auf zwei Etagen mit großer, umlaufender 360°-Dachterrasse", "Funktionale, aber offene Raumaufteilung", "Dreifachverglasung", "Luftwärmepumpe, Fußbodenheizung", "Videogegensprechanlage mit 7″-Display", "Digitale Hausklingelanlage mit Kamera", "Großformatige Wand- und Bodenfliesen", "Gehobene Sanitärausstattung von Grohe mit ebenerdigen Duschen und eingelassenen Badewannen"],
         text=None, leistung="neubau"),
    dict(slug="seniorenwohnanlage-wahrenholz", name="Seniorenwohnanlage Wahrenholz", kurz="Seniorenwohnanlage", ort="Wahrenholz", jahr="2022",
         flaeche="1.350 m²", flaeche_art="Wohn- und Nutzfläche", art="Wohnanlage · 20 Einheiten · barrierefrei", lat=52.6125, lon=10.6008,
         bilder=[("p-wahrenholz-1", 1600, 900, "Seniorenwohnanlage Wahrenholz: Drohnenaufnahme des fertigen Gebäudes mit roter Klinkerfassade und Satteldach"),
                 ("p-wahrenholz-2", 1200, 675, "Seniorenwohnanlage Wahrenholz: Drohnenaufnahme von der Gartenseite mit Balkonen in Holzoptik"),
                 ("p-wahrenholz-3", 1200, 675, "Seniorenwohnanlage Wahrenholz: Rohbau mit Filigrandecken und Gerüst aus der Luft"),
                 ("p-wahrenholz-4", 1200, 672, "Seniorenwohnanlage Wahrenholz: Straßenansicht mit Satteldach und Gauben"),
                 ("p-wahrenholz-5", 1200, 673, "Seniorenwohnanlage Wahrenholz: Gesamtanlage aus der Vogelperspektive"),
                 ("p-wahrenholz-6", 1200, 672, "Seniorenwohnanlage Wahrenholz: Gartenseite mit Balkonen in Holzoptik"),
                 ("p-wahrenholz-7", 1200, 674, "Seniorenwohnanlage Wahrenholz: Anlage mit Außenanlagen aus der Vogelperspektive"),
                 ("p-wahrenholz-8", 1200, 674, "Seniorenwohnanlage Wahrenholz: Wohnraum mit offener Küche")],
         punkte=None, leistung="neubau",
         text=["Nach unserem Entwurf fügt sich das Seniorenheim Wahrenholz durch den klassischen Baustil mit Satteldach und roter Backsteinfassade wunderbar in die unmittelbare Nachbarschaft und Umgebung ein. Durch das Flachdach am Anfang und Ende des Hauses und die freihängenden Balkone in Holzoptik gewinnt die Architektur dennoch an Moderne. Die weiße WDVS-Fassade der Gauben und des großzügigen Eingangsbereichs bringt ein wenig Kontrast hinein und lockert das Gesamtbild auf.",
               "Die Wohnanlage verfügt über 20 einzelne Wohneinheiten mit einer Gesamtwohnfläche inklusive Nutzflächen von 1.352,04 m². Das gesamte Haus ist barrierefrei. Vom Erdgeschoss erreichen Sie jedes Stockwerk über das großzügige, helle Treppenhaus direkt am Hauseingang, das mit Granitfliesen bzw. -stufen belegt ist. Alternativ kommt man über den zentral gelegenen, behindertengerechten Fahrstuhl gleich hinter dem Treppenhaus in jede Etage.",
               "Acht Wohnungen sind nach DIN behindertengerecht geplant und weisen genügend Platz auf, um mit einem Rollstuhl zu passieren und diesen abzustellen. Außerdem sind alle Wohneinheiten so geplant, dass Pflege- und Servicekräfte möglichst kurze Wege in den Wohnungen haben. Die Wohnungen sind am Treppenhaus und Fahrstuhl vorbei über einen kurzen, leisen Flur mit Teppichboden erreichbar, der farblich auf die Wandfarbe abgestimmt ist.",
               "Alle Wohneinheiten haben zwei Zimmer und 47 bis 67 m² Wohnfläche. Dazu hat jede Wohnung eine eigene Terrasse, einen Balkon oder eine Dachterrasse direkt angeschlossen. In jedem Wohnbereich kann eine Küche installiert werden; jede Wohneinheit weist die geforderten 6 m² Abstellraumfläche nach. Über die Videogegensprechanlage mit Display in jeder Wohnung kann man mit seinem Besuch kommunizieren und die Tür öffnen.",
               "Gestalterisch sind die Wohnungen in schlichten Pastelltönen gestrichen und farblich auf den Vinylboden (0,55 mm Nutzschicht) abgestimmt. Es wurde darauf geachtet, dass möglichst viele WC-Räume an der Außenfassade liegen und ein Fenster zum Lüften haben; unvermeidbar innenliegende WCs sind mit einer Abluftanlage ausgestattet. Die Bäder sind zur Hälfte gefliest, zur Hälfte gestrichen und farblich aufeinander abgestimmt. In den bodentiefen, 1 × 1 m großen Duschbereichen ist genügend Platz, um Sitzmöglichkeiten zu installieren oder im Rollstuhl vom Pflegeservice gewaschen zu werden.",
               "Allgemein lädt diese Wohnanlage ältere Menschen dazu ein, ihren Lebensabend möglichst lange selbstständig in eigener, gemütlicher Atmosphäre zu verbringen – und dennoch die Vorteile zu genießen, wenn eines Tages doch fremde Hilfe beansprucht wird. Raumaufteilung und farbliche Gestaltung der gesamten Anlage sollen nicht an ein Krankenhaus erinnern, sondern an Eigenheim und angenehme Nachbarschaft mit Wohlfühlcharakter."],
         visual_ab=4),
    dict(slug="bruecke", name="Brücke", kurz="Brücke", ort=None, jahr=None, flaeche=None, flaeche_art=None, art="Brückenbauwerk über einen Graben", band_pos="50% 68%", lat=None, lon=None,
         bilder=[("p-bruecke-1", 1600, 900, "Brückenbauwerk: Überbau frisch betoniert, noch in der Schalung – aus der Luft"),
                 ("p-bruecke-2", 1200, 675, "Brückenbauwerk: Bestandsbrücke vor dem Umbau"),
                 ("p-bruecke-3", 1200, 675, "Brückenbauwerk: alte Brücke mit Geländer über dem Graben"),
                 ("p-bruecke-4", 1200, 675, "Brückenbauwerk: Bestand nach Abbruch des Belags"),
                 ("p-bruecke-5", 1200, 675, "Brückenbauwerk: neuer Überbau mit Bewehrung"),
                 ("p-bruecke-6", 1200, 675, "Brückenbauwerk: Widerlager und Schalung"),
                 ("p-bruecke-7", 1200, 675, "Brückenbauwerk: Schalung mit Holzträgern von oben"),
                 ("p-bruecke-8", 1200, 675, "Brückenbauwerk: Bestand von der Uferseite"),
                 ("p-bruecke-9", 1200, 900, "Brückenbauwerk: fertige Betonbrücke über den Graben")],
         punkte=None, leistung="sonderbauten",
         text=["Ein Brückenbauwerk über einen Graben – mit der Drohne begleitet vom Bestand über Schalung und Bewehrung bis zum fertigen Betonüberbau. Eines der „kniffligen Projekte“, die wir als Sonderbau gern übernehmen."]),
]
PROJEKT_MAP = {p["slug"]: p for p in PROJEKTE}
SITZ = dict(lat=52.5078, lon=10.5955)

LEISTUNGEN = [
    dict(slug="neubau", pos="01", name="Neubau Einfamilien- und Mehrfamilienhäuser", kurz="Neubau EFH & MFH",
         text=["Durch unsere langjährige Erfahrung in der 2. Generation sind wir Ihr kompetenter Ansprechpartner – von Einfamilien- und Mehrfamilienhäusern bis zu großen Renditeobjekten.",
               "Beratung, Planung und schlüsselfertiger Neubau: Wie ein Einfamilienhaus bei uns entsteht, zeigt das Bautagebuch Phase für Phase – von oben."],
         refs=["einfamilienhaus-sassenburg", "doppelhaus-gifhorn", "wohnanlage-wolfsburg-ehmen", "seniorenwohnanlage-wahrenholz", "seniorenwohnanlage-wittingen", "sozialer-wohnungsbau-knesebeck"],
         bild=("p-wahrenholz-1", 1600, 900, "Seniorenwohnanlage Wahrenholz aus der Luft"), seite=True),
    dict(slug="gewerbe-industrie", pos="02", name="Gewerbe und Industrie", kurz="Gewerbe & Industrie",
         text=["Zu unserem facettenreichen Repertoire gehören ebenfalls Bauten für Gewerbe und Industrie."],
         refs=["garagenpark-sassenburg"],
         bild=("p-garagenpark-1", 1600, 1066, "Garagenpark Sassenburg mit 28 Garagen"), seite=True),
    dict(slug="sonderbauten", pos="03", name="Sonderbauten", kurz="Sonderbauten",
         text=["Sie haben ein spezielles Bauanliegen? Wir sind die Antwort! Gerne kümmern wir uns um Ihre Sonderbauten. Erfolgreich realisiert haben wir bereits Parkplätze, Brücken und andere knifflige Projekte."],
         refs=["bruecke"],
         bild=("p-bruecke-9", 1200, 900, "Fertige Betonbrücke über den Graben"), seite=True),
    dict(slug="abbruch", pos="04", name="Abbruch", kurz="Abbruch",
         text=["Wo ein Neubau ansteht, übernehmen wir auch den Abbruch des Bestands – wie beim Brückenbauwerk: vom alten Bauwerk bis zum neuen Überbau."],
         refs=[], bild=("p-bruecke-4", 1200, 675, "Abbruch des alten Brückenbelags"), seite=False),
    dict(slug="hoch-tiefbau", pos="05", name="Hoch- und Tiefbau, Trocken- und Innenbau, Pflaster- und Gartenarbeiten", kurz="Hoch- & Tiefbau, Innenbau, Pflaster",
         text=["Fundamente, Bodenplatte, Mauerwerk und Decken – wie im Bautagebuch zu sehen –, dazu Trockenbau, Pflaster- und Außenanlagen."],
         refs=[], bild=("t05-bodenplatte-betonieren", 1400, 788, "Frisch betonierte Bodenplatte von oben"), seite=False),
]
LEISTUNG_MAP = {l["slug"]: l for l in LEISTUNGEN}

REZENSIONEN = [
    ("Toller Bauprozess mit Bauschulz: Unser Hausbau inklusive Abriss dauerte nur 8 Monate. Die Firma war flexibel bei Änderungswünschen und die Baustelle stets ordentlich. Besonders beeindruckt sind wir von der handgeschliffenen Betontreppe. Bis jetzt keinerlei Probleme mit der Qualität. Sehr zufrieden mit Bauschulz!", "Talabaa"),
    ("Toller Bau mit der Firma in Gifhorn! Alles lief reibungslos, Termine wurden eingehalten, und spontane Änderungen waren kein Problem. Die Zusammenarbeit war freundschaftlich und auch Jahre später stehen sie für Fragen bereit. Würde jederzeit wieder mit ihnen bauen!", "Markus Pioch"),
    ("Wir arbeiten seit 2017 mit der Fa. Schulz-Bau zusammen und sind mehr als zufrieden. Sehr zuverlässig, kompetent und stets schnell verfügbar, wenn mal was „brennt“. Kann ich nur weiterempfehlen!", "Martin Schölkmann"),
    ("Top Leistung von BauSchulz! Trotz Corona lief der Bau reibungslos in 5–6 Monaten. Änderungswünsche wurden problemlos umgesetzt. Ich empfehle sie gerne weiter!", "Micha Egal"),
    ("Super professionell und kompetent. Sehr schnelle und präzise Arbeit. Bei Fragen und Anliegen immer zur Stelle.", "Viktoria Ostanin"),
    ("Junger, frischer Betrieb mit geballter Kompetenz und angenehmem Auftritt. Hier ist man in besten Händen.", "Sebastian Kasten"),
]

NAV = [("leistungen.html", "Leistungen"), ("bautagebuch.html", "Bautagebuch"), ("referenzen.html", "Referenzen"), ("ueber-uns.html", "Über uns"), ("kontakt.html", "Kontakt")]


# ----------------------------------------------------------------------------- CHROME
def kopf(aktiv):
    def a(href, label, extra=""):
        cur = ' aria-current="page"' if href == aktiv else ""
        return f'<a href="{href}"{cur}{extra}>{label}</a>'
    hnav = "".join(f"<li>{a(h, l)}</li>" for h, l in NAV)
    dnav = "".join(a(h, l) for h, l in NAV)
    return f'''<header class="kopf">
  <div class="kopf__z1">
    <a class="marke" href="index.html" aria-label="BAUSCHULZ – zur Startseite"><img src="assets/brand/logo.png" alt="BAUSCHULZ" width="630" height="155"></a>
    <div class="kopf__kontakt">
      <a class="kopf__tel" href="tel:{TEL_INT}" aria-label="Anrufen: {TEL_ANZ}">{I_TEL}<span>{TEL_ANZ}</span></a>
      <a class="btn btn--solid" href="kontakt.html">Anfrage</a>
      <button class="burger" type="button" data-drawer-toggle aria-controls="drawer" aria-expanded="false" aria-label="Menü öffnen"><span></span></button>
    </div>
  </div>
</header>
<div class="navbar" data-navbar>
  <nav class="navbar__i" aria-label="Hauptnavigation">
    <ul class="hnav">{hnav}</ul>
    <a class="navbar__tel" href="tel:{TEL_INT}">{I_TEL}{TEL_ANZ}</a>
  </nav>
</div>
<div class="drawer" id="drawer" data-drawer inert>
  <div class="drawer__hg" data-drawer-close></div>
  <div class="drawer__panel" role="dialog" aria-modal="true" aria-label="Menü">
    <div class="drawer__kopf"><img src="assets/brand/logo-hell.png" alt="BAUSCHULZ" width="630" height="155"><button class="drawer__zu" type="button" data-drawer-close aria-label="Menü schließen">{I_X}</button></div>
    <nav class="drawer__nav" aria-label="Menü">{dnav}</nav>
    <div class="drawer__fuss">
      <a class="btn btn--solid" href="tel:{TEL_INT}">{I_TEL}{TEL_ANZ}</a>
      <a class="btn btn--hell" href="kontakt.html">Anfrage</a>
      <small>Mo–Fr 08:00–17:00 Uhr · {ADRESSE}</small>
    </div>
  </div>
</div>
'''


def fuss():
    idx = "".join(f'<a href="{h}">{l}</a>' for h, l in NAV)
    proj = "".join(f'<a href="referenz-{p["slug"]}.html">{html.escape(p["name"])}</a>' for p in PROJEKTE)
    return f'''<footer class="fuss">
  <div class="wrap">
    <p class="fuss__claim"><span>Beratung</span><span class="claim__t">{GIEBEL}Planung</span><span class="claim__t">{GIEBEL}Schlüsselfertiger Neubau</span><span class="claim__t">{GIEBEL}Abbruch</span></p>
    <p class="fuss__zeile"><b>{FIRMA}</b><span>{ADRESSE}</span><a href="tel:{TEL_INT}">{TEL_ANZ}</a><a href="mailto:{MAIL}">{MAIL}</a><span>Mo–Fr 08:00–17:00 Uhr</span><a href="{ROUTE}" target="_blank" rel="noopener">Route planen</a><a class="fuss__social" href="{FACEBOOK}" target="_blank" rel="noopener">{I_FB}Facebook</a></p>
    <nav class="fuss__index" aria-label="Seitenübersicht"><a href="index.html">Start</a>{idx}</nav>
    <nav class="fuss__projekte" aria-label="Referenzprojekte">{proj}</nav>
    <p class="fuss__legal"><a href="impressum.html">Impressum</a><a href="datenschutz.html">Datenschutz</a><span>© {JAHR} {FIRMA}</span><a class="fuss__marke" href="index.html"><img src="assets/brand/logo-hell.png" alt="BAUSCHULZ – zur Startseite" width="630" height="155" loading="lazy"></a></p>
  </div>
</footer>
<a class="wa-fab" href="{WA}" target="_blank" rel="noopener" aria-label="Per WhatsApp schreiben">{I_WA}<span class="wa-fab__pulse" aria-hidden="true"></span></a>
'''


def kurz(text="Ihr Bauvorhaben – <em>sprechen wir darüber.</em>"):
    return f'''<section class="kurz sek--eng" aria-label="Kontakt">
  <div class="wrap kurz__i">
    <p class="kurz__t">{text}</p>
    <div class="kurz__cta">
      <a class="btn btn--solid" href="tel:{TEL_INT}">{I_TEL}{TEL_ANZ}</a>
      <a class="btn btn--wa" href="{WA}" target="_blank" rel="noopener">{I_WA}WhatsApp</a>
      <a class="btn btn--hell" href="kontakt.html">Anfrage</a>
    </div>
  </div>
</section>
'''


def jsonld_breadcrumb(datei, titel, aktiv):
    import json
    items = [{"@type": "ListItem", "position": 1, "name": "Start", "item": f"{DOMAIN}/"}]
    eltern = dict(NAV)
    if aktiv and aktiv != datei and aktiv in eltern:
        items.append({"@type": "ListItem", "position": 2, "name": eltern[aktiv], "item": f"{DOMAIN}/{aktiv}"})
    items.append({"@type": "ListItem", "position": len(items) + 1, "name": titel.split(" | ")[0].split(" – Referenz")[0], "item": f"{DOMAIN}/{datei}"})
    return json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}, ensure_ascii=False)


def seite(*, datei, titel, beschreibung, aktiv, body, jsonld=None, og_bild="assets/og.jpg", og_typ="website", head_extra=""):
    url = f"{DOMAIN}/" if datei == "index.html" else f"{DOMAIN}/{datei}"
    if datei != "index.html":
        bc = jsonld_breadcrumb(datei, titel, aktiv)
        jsonld = (jsonld + "</script><script type=\"application/ld+json\">" + bc) if jsonld else bc
    og_dims = '\n<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">' if og_bild == "assets/og.jpg" else ""
    ld = f'<script type="application/ld+json">{jsonld}</script>' if jsonld else ""
    return f'''<!DOCTYPE html>
<html lang="de" data-motion="editorial">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(titel)}</title>
<meta name="description" content="{html.escape(beschreibung)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow">
<meta name="theme-color" content="#353534">
<meta name="geo.region" content="DE-NI"><meta name="geo.placename" content="Sassenburg">
<meta name="geo.position" content="{SITZ['lat']};{SITZ['lon']}"><meta name="ICBM" content="{SITZ['lat']}, {SITZ['lon']}">
<meta property="og:type" content="{og_typ}">
<meta property="og:locale" content="de_DE">
<meta property="og:site_name" content="BAUSCHULZ">
<meta property="og:title" content="{html.escape(titel)}">
<meta property="og:description" content="{html.escape(beschreibung)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMAIN}/{og_bild}">{og_dims}
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="preload" href="assets/fonts/sofia-sans-xcond-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/sofia-sans-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="styles.css">
<script>document.documentElement.classList.add('anim')</script>
{head_extra}{ld}
</head>
<body>
<a class="skip" href="#inhalt">Zum Inhalt springen</a>
{kopf(aktiv)}
<main id="inhalt">
{body}
</main>
{fuss()}
<script src="assets/js/gsap.min.js"></script>
<script src="assets/js/ScrollTrigger.min.js"></script>
<script src="assets/motion.js"></script>
<script src="script.js"></script>
</body>
</html>
'''


# ----------------------------------------------------------------------------- BAUSTEINE
def zitat_kopf(zitat, quelle, h2, *, lang=False, hell=False, breit=False, mitte=False, klein=False):
    kl = "zk" + (" zk--hell" if hell else "") + (" zk--breit" if breit else "") + (" zk--mitte" if mitte else "") + (" zk--klein" if klein else "")
    pk = ' class="zk__zitat--lang"' if lang else ""
    fu = "" if klein else f"<footer>– {quelle}</footer>"
    return f'<div class="{kl}"><blockquote class="zk__zitat"><p{pk}>„{zitat}“</p>{fu}</blockquote><h2 class="zk__h2">{h2}</h2></div>'


def phase_li(ph, *, inline_img=True, tag="h3", h1_intro=None):
    n = f"{ph['n']:02d}"
    img_attr = ""
    inline = ""
    if ph["img"]:
        b = f"assets/img/{ph['img']}"
        img_attr = f' data-img="{b}.jpg" data-webp="{b}.webp"'
        if inline_img:
            inline = pic(ph["img"], f"Bauphase {n} – {ph['t']}: Drohnenaufnahme der Baustelle von oben", w=1400, h=788, sizes="100vw", klass="tb__inline")
    else:
        inline = '<div class="tb__plan tb__plan--inline tb__inline">' + plan_liste() + "</div>"
    if h1_intro:
        kopf = f'<h1>So kann’s aussehen.<small>Bautagebuch · Phase {n} {html.escape(ph["t"])} – {html.escape(ph["sub"])}</small></h1><p class="tb__intro">{h1_intro}</p>'
    else:
        kopf = f'<{tag}>{html.escape(ph["t"])}<small>{html.escape(ph["sub"])}</small></{tag}>'
    return f'<li class="tb__phase" id="phase-{n}" data-n="{ph["n"]}" data-titel="{html.escape(ph["t"])}"{img_attr}><span class="tb__num" aria-hidden="true">{n}</span>{kopf}<p>{html.escape(ph["p"])}</p>{inline}</li>'


def plan_liste():
    items = "".join(f'<li><b>{p["n"]:02d}</b>{html.escape(p["t"])}</li>' for p in PHASEN)
    return f'<p class="tb__plan__t"><small>Bauzeitenplan · Einfamilienhaus</small>16 Phasen bis schlüsselfertig</p><ol>{items}</ol>'


def tagebuch(phasen_nummern, *, voll=False, intro=None, h1=False):
    aktive = [p for p in PHASEN if p["n"] in phasen_nummern]
    leiste = "".join(
        (f'<li data-n="{p["n"]}" class="{"is-on" if p["n"] == 1 else ""}"><a href="#phase-{p["n"]:02d}" aria-label="Phase {p["n"]:02d}: {html.escape(p["t"])}">{p["n"]:02d}</a></li>' if p["n"] in phasen_nummern
         else f'<li data-n="{p["n"]}" class="tb__tick--leer" aria-hidden="true"><span>{p["n"]:02d}</span></li>')
        for p in PHASEN)
    erste = next(p for p in aktive if p["img"])
    stage = (f'<div class="tb__stage" aria-hidden="true">'
             f'<img class="tb__img is-on" data-layer="a" src="assets/img/{erste["img"]}.jpg" alt="" aria-hidden="true" width="1400" height="788" loading="lazy" decoding="async">'
             f'<img class="tb__img" data-layer="b" src="assets/img/{erste["img"]}.jpg" alt="" aria-hidden="true" width="1400" height="788" loading="lazy" decoding="async">'
             f'<div class="tb__plan is-on" data-plan>{plan_liste()}</div></div>')
    phasen = "".join(phase_li(p, tag="h2" if h1 else "h3", h1_intro=(intro if (h1 and p["n"] == 1) else None)) for p in aktive)
    mehr = "" if voll else f'<div class="tb__mehr"><a class="btn btn--line" href="bautagebuch.html">Alle 16 Phasen ansehen {I_PFEIL}</a><span class="label">8 von 16 Phasen als Auszug</span></div>'
    intro_html = ""
    kl = "tb sek" + (" tb--voll" if voll else "")
    kopf_html = "" if h1 else zitat_kopf("So kann’s aussehen.", "BAUSCHULZ", "Bautagebuch: Ein Einfamilienhaus in 16 Phasen – dokumentiert mit der Drohne, senkrecht von oben.")
    return f'''<section class="{kl}{' tb--ohne-kopf' if h1 else ''}" id="bautagebuch" data-tagebuch data-gesamt="{len(PHASEN)}">
  {f'<div class="wrap">{kopf_html}</div>' if kopf_html else ''}
  <div class="wrap tb__grid">
    <div class="tb__buehne">
      <nav class="tb__nav" aria-label="Bauphasen"><ol class="tb__leiste"><span class="tb__fill" data-tb-fill aria-hidden="true"></span>{leiste}</ol></nav>
      {stage}
      <div class="tb__stand" aria-hidden="true"><b data-tb-num>01</b><span data-tb-titel>Planung</span></div>
    </div>
    <ol class="tb__phasen">{phasen}</ol>
  </div>
  {f'<div class="wrap">{mehr}</div>' if mehr else ''}
</section>'''


def lv_akkordeon():
    out = []
    for i, l in enumerate(LEISTUNGEN):
        text = "".join(f"<p>{html.escape(t)}</p>" for t in l["text"])
        links = ""
        if l["refs"]:
            links = '<div class="lv__links">' + "".join(
                f'<a href="referenz-{r}.html">{I_PFEIL}{html.escape(PROJEKT_MAP[r]["name"])}</a>' for r in l["refs"]) + "</div>"
        elif l["slug"] == "abbruch":
            links = f'<div class="lv__links"><a href="referenz-bruecke.html">{I_PFEIL}Brücke: vom Bestand zum Neubau</a></div>'
        else:
            links = f'<div class="lv__links"><a href="bautagebuch.html">{I_PFEIL}Bautagebuch: Fundament bis Dach</a></div>'
        mehr = f'<a class="btn btn--line" href="{l["slug"]}.html" style="margin-top:var(--s3)">Mehr zu {html.escape(l["kurz"])}</a>' if l["seite"] else ""
        b = l["bild"]
        bild = f'<figure class="lv__bild">{pic(b[0], b[3], w=b[1], h=b[2], sizes="(max-width: 760px) 100vw, 40vw")}<figcaption>{html.escape(b[3])}</figcaption></figure>'
        out.append(f'''<details{' open' if i == 0 else ''}>
  <summary><span class="lv__pos">Pos. {l["pos"]}</span><span>{html.escape(l["name"])}</span><span class="lv__zu" aria-hidden="true">{I_PLUS}</span></summary>
  <div class="lv__body"><div><div class="lv__text">{text}{links}{mehr}</div>{bild}</div></div>
</details>''')
    return '<div class="lv" data-lv>' + "".join(out) + "</div>"


def ablauf_block(mit_absatz=True):
    schritte = [("01", "Erstgespräch &amp;&nbsp;Bedarf"), ("02", "Angebot &amp;&nbsp;Zeitplan"), ("03", "Ausführung &amp;&nbsp;Abstimmung"), ("04", "Abnahme")]
    ab = "".join(f'<li><span class="ablauf__n">{n}</span><b>{t}</b></li>' for n, t in schritte)
    warum = "".join(f'<li>{GIEBEL}{w}</li>' for w in ["feste Abläufe statt Chaos auf der Baustelle", "saubere Ausführung nach Fachregeln", "direkte Kommunikation – schnelle Entscheidungen"])
    return f'''<div class="ablauf-grid">
  <div>
    {zitat_kopf("Jedes Projekt ist für uns einmalig und individuell.", "BAUSCHULZ", "So läuft ein Projekt bei uns ab – vier Phasen, die jedes Bauvorhaben durchläuft.", klein=True)}
    <ol class="ablauf" data-ablauf><span class="ablauf__fill" data-ablauf-fill></span>{ab}</ol>
  </div>
  <div>
    <p class="label">Warum BauSchulz</p>
    <ul class="warum">{warum}</ul>
    {'<p class="lese" style="margin-top:var(--s4);color:var(--ink-soft)">Bauen in Tradition und Moderne: ein Familienbetrieb in 2.&nbsp;Generation, der seine Projekte oft mit eigener Mannschaft umsetzt.</p>' if mit_absatz else ''}
  </div>
</div>'''


def referenz_karte(p, *, klass="strip__item"):
    b = p["bilder"][0]
    jahr = p["jahr"] or "Sonderbau"
    daten = " · ".join(x for x in [p["ort"], p["flaeche"]] if x)
    tag = '<span class="rk__tag">Visualisierung</span>' if p.get("visual") else ""
    return (f'<li class="{klass}"><a class="rk" href="referenz-{p["slug"]}.html">'
            f'<span class="rk__jahr">{jahr}</span>'
            f'<div class="rk__bild">{pic(b[0], b[3], w=b[1], h=b[2], sizes="(max-width: 880px) 80vw, 33vw")}</div>'
            f'<div class="rk__txt"><b>{html.escape(p["name"])}</b><span>{html.escape(daten) if daten else html.escape(p["art"])}</span>{tag}</div></a></li>')


def referenz_strip(projekte, *, kopf_html="", mit_nav=True):
    items = "".join(referenz_karte(p) for p in projekte)
    nav = (f'<div class="strip__nav"><button type="button" data-strip-prev aria-label="Vorherige Referenz">{I_LINKS}</button>'
           f'<button type="button" data-strip-next aria-label="Nächste Referenz">{I_RECHTS}</button></div>') if mit_nav else ""
    return f'''<div class="strip" data-strip>
  <div class="strip__kopf">{kopf_html}{nav}</div>
  <ul class="strip__track" data-strip-track>{items}</ul>
</div>'''


def foto_strip(p):
    figs = []
    for i, (name, w, h, alt) in enumerate(p["bilder"]):
        if i == 0:
            continue  # Foto 1 trägt bereits das Bauschild-Band
        vis = " (Visualisierung)" if (p.get("visual") or (p.get("visual_ab") and i + 1 >= p["visual_ab"])) else ""
        figs.append(f'<li class="strip__item"><figure><div class="rk__bild">{pic(name, alt, w=w, h=h, sizes="(max-width: 880px) 90vw, 60vw")}</div><figcaption>{html.escape(alt)}{vis}</figcaption></figure></li>')
    n = len(p["bilder"]) - 1
    return f'''<div class="strip strip--fotos" data-strip>
  <div class="strip__kopf"><p class="strip__zaehler"><b data-strip-akt>01</b> / {n:02d}</p><div class="strip__nav"><button type="button" data-strip-prev aria-label="Vorheriges Foto">{I_LINKS}</button><button type="button" data-strip-next aria-label="Nächstes Foto">{I_RECHTS}</button></div></div>
  <ul class="strip__track" data-strip-track>{"".join(figs)}</ul>
</div>'''


def karte_html():
    marker = [dict(slug="sitz", name="BAUSCHULZ – Firmensitz", ort="Fehringstraße 8, Sassenburg", lat=SITZ["lat"], lon=SITZ["lon"], sitz=True)]
    for p in PROJEKTE:
        if p["lat"]:
            marker.append(dict(slug=p["slug"], name=p["name"], ort=f'{p["ort"]} · {p["jahr"]}', lat=p["lat"], lon=p["lon"], sitz=False))
    import json
    data = html.escape(json.dumps(marker, ensure_ascii=False), quote=True)
    leg = "".join(
        (f'<li class="is-sitz">{GIEBEL}<span>Firmensitz Sassenburg</span> <a href="{ROUTE}" target="_blank" rel="noopener">Route planen</a></li>' if m["sitz"] else
         f'<li>{GIEBEL}<a href="referenz-{m["slug"]}.html">{html.escape(m["name"])}</a></li>') for m in marker)
    return f'''<div class="kontakt__karte">
  <div class="karte" data-karte data-marker="{data}">
    <p class="karte__hinweis">Referenz-Karte: Wo wir gebaut haben.<br><a href="https://www.openstreetmap.org/?mlat={SITZ['lat']}&amp;mlon={SITZ['lon']}#map=11/{SITZ['lat']}/{SITZ['lon']}" target="_blank" rel="noopener">Karte auf OpenStreetMap öffnen</a></p>
  </div>
  <ol class="karte__legende" aria-label="Bauorte">{leg}</ol>
</div>'''


def kontakt_block(*, mit_zitat=True, kurz=False, mit_kanaelen=True):
    kanaele = (f'''<div class="kanaele">
        <a class="kanal" href="tel:{TEL_INT}"><span class="kanal__i">{I_TEL}</span><span><b>{TEL_ANZ}</b><small>Mo–Fr 08:00–17:00 Uhr</small></span></a>
        <a class="kanal" href="{WA}" target="_blank" rel="noopener"><span class="kanal__i"><svg class="fill" viewBox="0 0 24 24" aria-hidden="true">{I_WA[I_WA.index('>')+1:-6]}</svg></span><span><b>WhatsApp</b><small>Kurze Frage, Foto vom Grundstück – einfach schreiben</small></span></a>
        <a class="kanal" href="mailto:{MAIL}"><span class="kanal__i">{I_MAIL}</span><span><b>{MAIL}</b><small>{ADRESSE}</small></span></a>
      </div>''') if mit_kanaelen else ""
    zk = zitat_kopf("direkte Kommunikation – schnelle Entscheidungen", "BAUSCHULZ", "Anfrage: Erzählen Sie uns von Ihrem Bauvorhaben – wir melden uns.", klein=True) if mit_zitat else ""
    return f'''<section class="kontakt{' kontakt--kurz' if kurz else ''}" id="kontakt">
  <div class="kontakt__grid">
    <div class="kontakt__form">
      {zk}
      {kanaele}
      <form class="form" id="anfrage" action="mailto:{MAIL}" method="post" enctype="text/plain" novalidate data-form>
        <div class="form__reihe">
          <div class="feld"><label for="f-name">Ihr Name</label><input id="f-name" name="name" type="text" autocomplete="name" required></div>
          <div class="feld"><label for="f-mail">Ihre E-Mail-Adresse</label><input id="f-mail" name="email" type="email" autocomplete="email" required></div>
        </div>
        <div class="feld"><label for="f-betreff">Betreff</label><input id="f-betreff" name="betreff" type="text" placeholder="z. B. Einfamilienhaus in Gifhorn"></div>
        <div class="feld"><label for="f-text">Ihre Nachricht (optional)</label><textarea id="f-text" name="nachricht"></textarea></div>
        <p class="form__meldung" data-form-meldung hidden></p>
        <div class="form__fuss"><button class="btn btn--solid" type="submit">Anfrage senden {I_PFEIL}</button><small>Mit dem Absenden öffnet sich Ihr E-Mail-Programm mit der vorbereiteten Nachricht an {MAIL}.</small></div>
      </form>
    </div>
    {karte_html()}
  </div>
</section>'''


# ----------------------------------------------------------------------------- SEITEN
def jsonld_org():
    import json
    d = {"@context": "https://schema.org", "@type": "GeneralContractor", "@id": f"{DOMAIN}/#betrieb",
         "name": FIRMA, "alternateName": "Bauschulz", "url": f"{DOMAIN}/", "telephone": TEL_INT, "email": MAIL,
         "image": f"{DOMAIN}/assets/img/team-2025.jpg", "logo": f"{DOMAIN}/assets/brand/logo.png",
         "description": "Bauunternehmen in 2. Generation aus Sassenburg bei Gifhorn: Beratung, Planung, schlüsselfertiger Neubau und Abbruch – vom Einfamilienhaus bis Gewerbe.",
         "address": {"@type": "PostalAddress", "streetAddress": "Fehringstraße 8", "postalCode": "38524", "addressLocality": "Sassenburg", "addressRegion": "Niedersachsen", "addressCountry": "DE"},
         "geo": {"@type": "GeoCoordinates", "latitude": SITZ["lat"], "longitude": SITZ["lon"]},
         "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:00", "closes": "17:00"}],
         "vatID": "DE341873217", "sameAs": ["https://www.facebook.com/BauschulzGmbH/"],
         "areaServed": [{"@type": "City", "name": n} for n in ["Sassenburg", "Gifhorn", "Wolfsburg", "Wittingen", "Knesebeck", "Wahrenholz"]],
         "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Leistungen", "itemListElement": [
             {"@type": "Offer", "itemOffered": {"@type": "Service", "name": l["name"], "url": f"{DOMAIN}/{l['slug']}.html" if l["seite"] else f"{DOMAIN}/leistungen.html"}} for l in LEISTUNGEN]}}
    return json.dumps(d, ensure_ascii=False)


def seite_index():
    hero = f'''<section class="hero">
  <div class="wrap hero__grid">
    <div class="hero__copy" data-hero-stagger>
      <p class="hero__ort">Bauunternehmen in Sassenburg bei Gifhorn</p>
      <h1 class="h1">Vom Einfamilienhaus bis <em>Gewerbe.</em></h1>
      <p class="hero__lead">Beratung, Planung, schlüsselfertiger Neubau und Abbruch – ein Familienbetrieb in 2.&nbsp;Generation, der seine Projekte oft mit eigener Mannschaft umsetzt.</p>
      <div class="hero__cta"><a class="btn btn--solid btn--gross" href="tel:{TEL_INT}">{I_TEL}{TEL_ANZ}</a><a class="btn btn--line btn--gross" href="#bautagebuch">Bautagebuch ansehen</a></div>
    </div>
    <figure class="hero__media">
      <div class="hero__frame">{pic("hero-haus-oben", "Fertiges Einfamilienhaus aus der Drohnenperspektive: graues Ziegeldach mit Photovoltaik, Terrasse und Garten", w=1152, h=1440, sizes="(max-width: 880px) 100vw, 46vw", eager=True)}</div>
      <figcaption>{GIEBEL}<b>Phase 16 / 16</b><span>Einfamilienhaus, schlüsselfertig – Drohnenaufnahme aus dem Bautagebuch</span></figcaption>
    </figure>
  </div>
</section>'''
    tb = tagebuch(INDEX_PHASEN)
    leist = f'''<section class="sek" id="leistungen">
  <div class="wrap">
    {zitat_kopf("Saubere Ausführung. Klare Abläufe. Verlässliche Termine.", "BAUSCHULZ", "Leistungsverzeichnis: Was wir bauen – vom Einfamilienhaus über Gewerbe bis zum Sonderbau.", klein=True)}
    {lv_akkordeon()}
  </div>
</section>'''
    ablauf = f'<section class="sek" id="ablauf" style="padding-top:0"><div class="wrap">{ablauf_block(mit_absatz=False)}</div></section>'
    refs = f'''<section class="sek" id="referenzen" style="background:var(--paper-2);border-top:1px solid var(--line);border-bottom:1px solid var(--line)">
  {referenz_strip(PROJEKTE, kopf_html=zitat_kopf("Machen Sie sich ein eigenes Bild vor Ort.", "BAUSCHULZ", "Referenzen: Sieben Bauvorhaben aus dem Landkreis Gifhorn und Wolfsburg – und ein Brückenbauwerk. Chronologisch von 2014 bis heute.", klein=True))}
  <div class="strip__fuss"><a class="btn btn--line" href="referenzen.html">Alle Referenzen mit Projektdaten {I_PFEIL}</a></div>
</section>'''
    betrieb = f'''<section class="betrieb sek" id="betrieb">
  <div class="wrap betrieb__grid">
    <figure class="betrieb__bild" data-reveal="wipe-left">{pic("team-2025", "Das Bauschulz-Team: fünf Personen in schwarzen Firmenshirts vor der Halle mit BAUSCHULZ-Schriftzug", w=1800, h=1199, sizes="(max-width: 880px) 100vw, 55vw", klein=900)}<figcaption>Das Team vor der Halle in Sassenburg</figcaption></figure>
    <div class="betrieb__copy" data-reveal="up">
      {zitat_kopf("Bauen in Tradition &amp; Moderne.", "BAUSCHULZ", "Bauunternehmen in 2.&nbsp;Generation – ein Familienbetrieb aus Sassenburg, in dem alle mit anpacken.", hell=True)}
      <p>Bauschulz baut im Hochbau. Geführt wird der Betrieb von <b>Denis Schulz</b>; zu Hause ist das Unternehmen in Sassenburg im Landkreis&nbsp;Gifhorn.</p>
      <p>Unsere Projekte setzen wir oft mit eigener Mannschaft um – vom Fundament bis zum Dach.</p>
      <a class="btn btn--hell" href="ueber-uns.html">Über uns {I_PFEIL}</a>
      <figure class="betrieb__klein">{pic("team-maschinen", "Drei Mitarbeiter vor Radlader und Bagger auf dem Betriebsgelände", w=1600, h=1066, sizes="150px")}<figcaption>Vor Radlader und Bagger auf dem Betriebsgelände</figcaption></figure>
    </div>
  </div>
</section>'''
    r0 = REZENSIONEN[0]
    rest = "".join(f'<li data-reveal style="--d:{i}"><p>„{html.escape(t)}“</p><footer>{GIEBEL}{html.escape(n)} · Google</footer></li>' for i, (t, n) in enumerate(REZENSIONEN[1:5]))
    rez = f'''<section class="sek" id="stimmen">
  <div class="wrap">
    {zitat_kopf(html.escape(r0[0]), f"Google-Rezension, {r0[1]}", "Was Bauherren über Bauschulz sagen – Rezensionen von Google.", lang=True, breit=True)}
    <ul class="rez">{rest}</ul>
    <p class="rez__hinweis"><a href="{GOOGLE}" target="_blank" rel="noopener">Alle Rezensionen bei Google ansehen {I_PFEIL}</a></p>
  </div>
</section>'''
    body = hero + tb + leist + ablauf + refs + betrieb + rez + kontakt_block()
    return seite(datei="index.html", titel="Bauschulz – Bauunternehmen Sassenburg bei Gifhorn",
                 beschreibung="Beratung, Planung, schlüsselfertiger Neubau und Abbruch – vom Einfamilienhaus bis Gewerbe. Familienbetrieb in 2. Generation aus Sassenburg. 0176 31482066.",
                 aktiv="index.html", body=body, jsonld=jsonld_org(), og_bild="assets/og.jpg")


def seite_bautagebuch():
    intro = "Dies könnte Ihre Baustelle sein! Wir haben ein Einfamilienhaus mit Drohnenaufnahmen dokumentiert, um Ihnen die verschiedenen Bauphasen zu zeigen – vom Ausheben der Fundamente bis zum fertigen Dach. So könnte auch Ihr Bauprojekt aussehen."
    body = tagebuch([p["n"] for p in PHASEN], voll=True, intro=intro, h1=True)
    body += f'''<section class="sek">
  <div class="wrap">
    <figure class="bildband" data-reveal="mask">{pic("band-unterspannbahn", "Dach beim Eindecken, senkrecht von oben: oben bereits Dachsteine, rechts unten noch weiße Unterspannbahn mit Lattung", w=1800, h=1012, sizes="100vw", klein=900)}<figcaption>Phase 15 – Dach beim Eindecken: Dachsteine oben, Unterspannbahn und Lattung noch unten rechts</figcaption></figure>
  </div>
</section>'''
    body += kurz("Ihr Haus <em>von oben?</em>")
    return seite(datei="bautagebuch.html", titel="Bautagebuch: Ein Einfamilienhaus in 16 Bauphasen von oben | Bauschulz",
                 beschreibung="Von den Fundamenten bis zum gedeckten Dach: der Neubau eines Einfamilienhauses in 16 Phasen – mit Drohnenaufnahmen dokumentiert und von Bauschulz erklärt.",
                 aktiv="bautagebuch.html", body=body, og_bild="assets/img/t13-richtfest.jpg")


def seite_leistungen():
    pos = []
    for l in LEISTUNGEN:
        text = "".join(f"<p>{html.escape(t)}</p>" for t in l["text"])
        links = ""
        if l["refs"]:
            links = '<div class="lv__links">' + "".join(f'<a href="referenz-{r}.html">{I_PFEIL}{html.escape(PROJEKT_MAP[r]["name"])}</a>' for r in l["refs"]) + "</div>"
        elif l["slug"] == "abbruch":
            links = f'<div class="lv__links"><a href="referenz-bruecke.html">{I_PFEIL}Brücke: vom Bestand zum Neubau</a></div>'
        else:
            links = f'<div class="lv__links"><a href="bautagebuch.html">{I_PFEIL}Bautagebuch: Fundament bis Dach</a></div>'
        titel = f'<a href="{l["slug"]}.html">{html.escape(l["name"])}</a>' if l["seite"] else html.escape(l["name"])
        b = l["bild"]
        pos.append(f'''<div class="lv-offen__pos" id="{l["slug"]}">
  <span class="lv__pos">Pos. {l["pos"]}</span>
  <div><h2>{titel}</h2>
    <div class="lv-offen__body"><div class="lv__text">{text}{links}</div><figure class="lv__bild">{pic(b[0], b[3], w=b[1], h=b[2], sizes="(max-width: 760px) 100vw, 40vw")}<figcaption>{html.escape(b[3])}</figcaption></figure></div>
  </div>
</div>''')
    body = f'''<section class="lv-kopf">
  <div class="wrap">
    <p class="lv-kopf__claim lv-kopf__claim--oben"><span>Beratung</span><span class="claim__t">{GIEBEL}Planung</span><span class="claim__t">{GIEBEL}Schlüsselfertiger Neubau</span><span class="claim__t">{GIEBEL}Abbruch</span></p>
    <h1>Was wir bauen.</h1>
  </div>
</section>
<section class="sek" style="padding-top:0"><div class="wrap"><div class="lv-offen">{"".join(pos)}</div></div></section>
<section class="sek" style="padding-top:0"><div class="wrap">{ablauf_block()}</div></section>
{kurz()}'''
    return seite(datei="leistungen.html", titel="Leistungen: Neubau, Gewerbe, Sonderbau, Abbruch | Bauschulz",
                 beschreibung="Leistungsverzeichnis: Neubau von Einfamilien- und Mehrfamilienhäusern, Gewerbe und Industrie, Sonderbauten, Abbruch, Hoch- und Tiefbau, Innenbau, Pflaster.",
                 aktiv="leistungen.html", body=body)


def seite_leistung(l):
    refs = [PROJEKT_MAP[r] for r in l["refs"]]
    text = "".join(f"<p>{html.escape(t)}</p>" for t in l["text"])
    strip = referenz_strip(refs, kopf_html=f'<p class="label">Referenzen zu Pos. {l["pos"]}</p>', mit_nav=len(refs) > 2) if refs else ""
    extra = ""
    if l["slug"] == "neubau":
        teaser = []
        for p in PHASEN:
            if p["n"] not in (2, 7, 13, 15):
                continue
            alt = "Bauphase %02d: %s" % (p["n"], p["t"])
            teaser.append('<li class="strip__item"><a class="rk" href="bautagebuch.html#bautagebuch"><span class="rk__jahr">Phase %02d</span><div class="rk__bild">%s</div><div class="rk__txt"><b>%s</b></div></a></li>'
                          % (p["n"], pic(p["img"], alt, w=1400, h=788, sizes="(max-width: 700px) 100vw, 25vw"), html.escape(p["t"])))
        extra = f'''<section class="sek" style="padding-top:0">
  <div class="wrap">{zitat_kopf("So kann’s aussehen.", "BAUSCHULZ", "Wie ein Einfamilienhaus bei uns entsteht – das Bautagebuch zeigt alle 16 Phasen von oben.")}</div>
  <div class="strip" data-strip><div class="strip__kopf"><p class="label">Vier von 16 Phasen</p><div class="strip__nav"><button type="button" data-strip-prev aria-label="Vorherige Phase">{I_LINKS}</button><button type="button" data-strip-next aria-label="Nächste Phase">{I_RECHTS}</button></div></div><ul class="strip__track" data-strip-track>{"".join(teaser)}</ul></div>
  <div class="wrap" style="margin-top:var(--s4)"><a class="btn btn--line" href="bautagebuch.html">Zum Bautagebuch {I_PFEIL}</a></div>
</section>'''
    b = l["bild"]
    body = f'''<section class="lv-kopf">
  <div class="wrap">
    <h1><small class="lv-kopf__pos">Leistungsverzeichnis · Pos. {l["pos"]}</small>{html.escape(l["name"])}</h1>
    <div class="lv-offen__body"><div class="lv__text lv__text--gross">{text}</div><figure class="lv__bild">{pic(b[0], b[3], w=b[1], h=b[2], sizes="(max-width: 760px) 100vw, 40vw", eager=True)}<figcaption>{html.escape(b[3])}</figcaption></figure></div>
    <p class="lv-kopf__claim"><span>Beratung</span><span class="claim__t">{GIEBEL}Planung</span><span class="claim__t">{GIEBEL}Schlüsselfertiger Neubau</span><span class="claim__t">{GIEBEL}Abbruch</span></p>
  </div>
</section>
<section class="sek" style="padding-top:0">{strip}</section>
{extra}
{kurz()}'''
    titel = {"neubau": "Neubau Einfamilien- & Mehrfamilienhäuser Gifhorn/Wolfsburg | Bauschulz",
             "gewerbe-industrie": "Gewerbe- & Industriebau Landkreis Gifhorn | Bauschulz",
             "sonderbauten": "Sonderbauten: Brücken, Parkplätze & knifflige Projekte | Bauschulz"}[l["slug"]]
    beschr = {"neubau": "Schlüsselfertiger Neubau von Einfamilien- und Mehrfamilienhäusern bis zum Renditeobjekt – Bauschulz, Bauunternehmen in 2. Generation aus Sassenburg bei Gifhorn.",
              "gewerbe-industrie": "Bauten für Gewerbe und Industrie von Bauschulz aus Sassenburg – zum Beispiel der Garagenpark mit 28 Garagen. Beratung, Planung, Ausführung.",
              "sonderbauten": "Sonderbauten von Bauschulz: Parkplätze, Brücken und andere knifflige Projekte – Bauunternehmen aus Sassenburg im Landkreis Gifhorn."}[l["slug"]]
    return seite(datei=f'{l["slug"]}.html', titel=titel, beschreibung=beschr, aktiv="leistungen.html", body=body, og_bild=f"assets/img/{b[0]}.jpg")


def seite_referenzen():
    eintraege = []
    for p in PROJEKTE:
        b = p["bilder"][0]
        jahr = p["jahr"] or "Sonder&shy;bau"
        daten = "".join(f"<span><b>{html.escape(v)}</b> {k}</span>" for k, v in [("", p["ort"] or ""), (p["flaeche_art"] or "", p["flaeche"] or "")] if v)
        if p["text"]:
            satz = re.split(r"(?<=[a-zäöüß])\. ", p["text"][0])[0].rstrip(".") + "."
        else:
            satz = (p["punkte"][0].rstrip(".") + ".") if p["punkte"] else ""
        tag = '<span class="rk__tag">Visualisierungen</span>' if p.get("visual") else ""
        daten_html = f'<p class="chronik__daten">{daten}{tag}</p>' if (daten or tag) else ""
        eintraege.append(f'''<li class="chronik__eintrag" id="{p["slug"]}">
  <div><p class="chronik__jahr">{jahr}<small>{html.escape(p["art"])}</small></p><figure class="chronik__bild" data-reveal="mask">{pic(b[0], b[3], w=b[1], h=b[2], sizes="(max-width: 760px) 100vw, 45vw")}</figure></div>
  <div class="chronik__txt" data-reveal="up"><h2><a href="referenz-{p["slug"]}.html">{html.escape(p["name"])}</a></h2>{daten_html}<p>{html.escape(satz)}</p><a class="btn btn--line" href="referenz-{p["slug"]}.html">Projekt ansehen {I_PFEIL}</a></div>
</li>''')
    jahre = "".join(f'<a href="#{p["slug"]}">{p["jahr"] or "Sonderbau"}</a>' for p in PROJEKTE)
    body = f'''<section class="chronik-kopf">
  <div class="wrap">
    <h1 class="h1">Gebaut. 2014 bis heute.</h1>
    <nav class="jahrleiste" aria-label="Nach Jahr springen">{jahre}</nav>
  </div>
</section>
<section class="sek" style="padding-top:var(--s5)"><div class="wrap"><ol class="chronik">{"".join(eintraege)}</ol></div></section>
{kurz()}'''
    return seite(datei="referenzen.html", titel="Referenzen 2014 bis heute | Bauschulz Sassenburg",
                 beschreibung="Acht Referenzen von Bauschulz: Seniorenwohnanlagen Wittingen und Wahrenholz, Wohnungsbau Knesebeck, Doppelhaus Gifhorn, Wohnanlage Ehmen, Garagenpark, Brücke.",
                 aktiv="referenzen.html", body=body, og_bild="assets/img/p-wahrenholz-1.jpg")


def seite_projekt(i, p):
    prev_p = PROJEKTE[i - 1] if i > 0 else None
    next_p = PROJEKTE[i + 1] if i + 1 < len(PROJEKTE) else None
    b = p["bilder"][0]
    daten = []
    daten.append(("Bauvorhaben", html.escape(p["art"]), ""))
    if p["slug"] == "bruecke":
        daten.append(("Leistung", "Sonderbau · Pos.&nbsp;03", ""))
    if p["ort"]:
        daten.append(("Ort", html.escape(p["ort"]), ""))
    if p["flaeche"]:
        daten.append((p["flaeche_art"], p["flaeche"], ""))
    if p["jahr"]:
        daten.append(("Fertigstellung", p["jahr"], ""))
    dl = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v, _ in daten)
    if p["punkte"]:
        text = "<ul>" + "".join(f"<li>{html.escape(x)}</li>" for x in p["punkte"]) + "</ul>"
    else:
        text = "".join(f"<p>{html.escape(t)}</p>" for t in p["text"])
    if p.get("ausstattung"):
        text += f'<h2>Ausstattung</h2><p>{html.escape(p["ausstattung"])}</p>'
    hinweis = ""
    if p.get("visual"):
        hinweis = f'<p class="projekt__hinweis">{GIEBEL}Die Abbildungen sind Visualisierungen des Bauvorhabens.</p>'
    elif p.get("visual_ab"):
        hinweis = f'<p class="projekt__hinweis">{GIEBEL}Titelfoto und die ersten beiden Fotos der Reihe sind Drohnenaufnahmen, alle weiteren Visualisierungen aus der Planung – in den Bildunterschriften gekennzeichnet.</p>'
    if len(p["bilder"]) > 1:
        fotos = foto_strip(p)
    else:
        fotos = ""
    nav = '<nav class="chronik-nav" aria-label="Weitere Projekte">'
    nav += (f'<a href="referenz-{prev_p["slug"]}.html"><small>← Vorheriges Projekt · {prev_p["jahr"] or "Sonderbau"}</small><b>{html.escape(prev_p["name"])}</b></a>' if prev_p else '<a href="referenzen.html"><small>← Alle Referenzen</small><b>Chronik 2014 bis heute</b></a>')
    nav += (f'<a href="referenz-{next_p["slug"]}.html"><small>Nächstes Projekt · {next_p["jahr"] or "Sonderbau"} →</small><b>{html.escape(next_p["name"])}</b></a>' if next_p else '<a href="referenzen.html"><small>Alle Referenzen →</small><b>Chronik 2014 bis heute</b></a>')
    nav += "</nav>"
    leist = LEISTUNG_MAP[p["leistung"]]
    band_pos = f' style="--band-pos:{p["band_pos"]}"' if p.get("band_pos") else ""
    body = f'''<div class="band"{band_pos}>{pic(b[0], b[3], w=b[1], h=b[2], sizes="100vw", eager=True)}</div>
<section class="bauschild">
  <div class="wrap bauschild__i">
    <img class="bauschild__a" src="assets/brand/icon-a.png" alt="" aria-hidden="true" width="270" height="270">
    <h1><small>Referenz · Pos. {leist["pos"]} {html.escape(leist["kurz"])}</small>{html.escape(p["name"])}</h1>
    <dl class="bauschild__daten">{dl}</dl>
  </div>
</section>
<section class="sek">
  {fotos}
  <div class="wrap" style="margin-top:var(--s6)">
    <div class="projekt__text lese">
      <p class="label">Projektbeschreibung</p>
      {text}
      {hinweis}
    </div>
  </div>
</section>
<section class="sek" style="padding-top:0"><div class="wrap">{nav}</div></section>
{kurz()}'''
    titel = f'{p["name"]} – Referenz | Bauschulz'
    beschr = (f'{p["name"]}: {p["art"]}' + (f', {p["ort"]}' if p["ort"] else "") + (f', fertig {p["jahr"]}' if p["jahr"] else "") + (f', {p["flaeche"]}' if p["flaeche"] else "") + " – Referenz von Bauschulz, Bauunternehmen aus Sassenburg.")
    return seite(datei=f'referenz-{p["slug"]}.html', titel=titel, beschreibung=beschr, aktiv="referenzen.html", body=body, og_bild=f"assets/img/{b[0]}.jpg", og_typ="article")


def seite_ueber():
    warum = "".join(f'<li>{GIEBEL}{w}</li>' for w in ["feste Abläufe statt Chaos auf der Baustelle", "saubere Ausführung nach Fachregeln", "direkte Kommunikation – schnelle Entscheidungen"])
    body = f'''<div class="band band--kurz">{pic("team-2025", "Das Bauschulz-Team vor der Firmenhalle mit BAUSCHULZ-Schriftzug", w=1800, h=1199, sizes="100vw", klein=900, eager=True)}</div>
<section class="sek team-kopf">
  <div class="wrap ueber__grid">
    <div>
      <h1>Bauunternehmen in 2.&nbsp;Generation.</h1>
      <div class="lese" style="margin-top:var(--s4)">
        <p class="lese__auftakt">Bauen in Tradition und Moderne – ein Familienbetrieb aus Sassenburg, in dem alle mit anpacken.</p>
        <p>Bauschulz baut im Hochbau – Einfamilien- und Mehrfamilienhäuser, Gewerbe, Sonderbauten. Geschäftsführer ist <b>Denis Schulz</b>. Unsere Projekte setzen wir oft mit eigener Mannschaft um – vom Fundament über Mauerwerk und Decken bis zum Dach.</p>
      </div>
      <dl class="fakten">
        <div><dt>Betrieb</dt><dd>{FIRMA}</dd></div>
        <div><dt>Geschäftsführer</dt><dd>Denis Schulz</dd></div>
        <div><dt>Sitz</dt><dd>{ADRESSE} (Ortsteil Triangel), Landkreis Gifhorn</dd></div>
        <div><dt>Tätigkeit</dt><dd>Hoch- und Tiefbau, Trocken- und Innenbau, Pflaster- und Gartenarbeiten</dd></div>
        <div><dt>Handelsregister</dt><dd>Amtsgericht Hildesheim, HRA 202485</dd></div>
      </dl>
    </div>
    <div>
      <figure class="ueber__bild" data-reveal="mask">{pic("team-maschinen", "Drei Mitarbeiter von Bauschulz vor Radlader und Bagger", w=1600, h=1066, sizes="(max-width: 880px) 100vw, 45vw")}<figcaption>Vor Radlader und Bagger auf dem Betriebsgelände</figcaption></figure>
      <p class="label" style="margin-top:var(--s5)">Warum BauSchulz</p>
      <ul class="warum" style="margin-top:var(--s2)">{warum}</ul>
    </div>
  </div>
</section>
{kurz("Lernen Sie uns kennen – <em>am besten auf der Baustelle.</em>")}'''
    return seite(datei="ueber-uns.html", titel="Über uns: Familienbetrieb in 2. Generation | Bauschulz Sassenburg",
                 beschreibung="Bauschulz ist ein Bauunternehmen im Hochbau in zweiter Generation aus Sassenburg bei Gifhorn – Geschäftsführer Denis Schulz, eigene Mannschaft.",
                 aktiv="ueber-uns.html", body=body)


def seite_kontakt():
    body = f'''<section class="kontakt-kopf">
  <div class="wrap">
    <h1>Anfrage.</h1>
    <div class="direkt">
      <a href="tel:{TEL_INT}">{I_TEL}{TEL_ANZ}</a>
      <a href="{WA}" target="_blank" rel="noopener"><svg class="fill" viewBox="0 0 24 24" aria-hidden="true">{I_WA[I_WA.index('>')+1:-6]}</svg>WhatsApp</a>
      <a href="mailto:{MAIL}">{I_MAIL}{MAIL}</a>
      <span>Mo–Fr 08:00–17:00 Uhr · {ADRESSE}</span>
    </div>
  </div>
</section>
{kontakt_block(mit_zitat=False, kurz=True, mit_kanaelen=False)}'''
    return seite(datei="kontakt.html", jsonld=jsonld_org(), titel="Kontakt & Anfrage | Bauschulz, Fehringstraße 8, Sassenburg",
                 beschreibung="Kontakt zu Bauschulz: 0176 31482066, info@bauschulz.com, Fehringstraße 8, 38524 Sassenburg – Anfrage per Telefon, WhatsApp oder Formular.",
                 aktiv="kontakt.html", body=body)


def seite_impressum():
    body = f'''<section class="recht"><div class="wrap">
  <h1>Impressum</h1>
  <h2>Angaben gemäß § 5 TMG</h2>
  <p><b>BAUSCHULZ Verwaltungs GmbH</b></p>
  <address>Fehringstraße 8<br>38524 Sassenburg</address>
  <p>Amtsgericht Hildesheim, HRB 207363<br>Geschäftsführer: Denis Schulz</p>
  <p style="margin-top:var(--s4)"><b>BAUSCHULZ GmbH &amp; Co. KG</b></p>
  <address>Fehringstraße 8<br>38524 Sassenburg</address>
  <p>Amtsgericht Hildesheim, HRA 202485</p>
  <h2>Kontakt</h2>
  <p>Telefon: <a href="tel:{TEL_INT}">0176 31482066</a><br>E-Mail: <a href="mailto:{MAIL}">{MAIL}</a></p>
  <h2>Umsatzsteuer-Identifikationsnummer</h2>
  <p>Umsatzsteuer-Identifikationsnummer gemäß § 27 a Umsatzsteuergesetz: DE341873217<br>Steuer-Nr.: 19/201/05082</p>
  <h2>Berufsbezeichnung</h2>
  <p>Bauunternehmen</p>
  <h2>Haftungsausschluss</h2>
  <h3>1. Inhalt des Onlineangebotes</h3>
  <p>Der Autor übernimmt keinerlei Gewähr für die Aktualität, Korrektheit, Vollständigkeit oder Qualität der bereitgestellten Informationen. Haftungsansprüche gegen den Autor, welche sich auf Schäden materieller oder ideeller Art beziehen, die durch die Nutzung oder Nichtnutzung der dargebotenen Informationen bzw. durch die Nutzung fehlerhafter und unvollständiger Informationen verursacht wurden, sind grundsätzlich ausgeschlossen, sofern seitens des Autors kein nachweislich vorsätzliches oder grob fahrlässiges Verschulden vorliegt. Alle Angebote sind freibleibend und unverbindlich. Der Autor behält es sich ausdrücklich vor, Teile der Seiten oder das gesamte Angebot ohne gesonderte Ankündigung zu verändern, zu ergänzen, zu löschen oder die Veröffentlichung zeitweise oder endgültig einzustellen.</p>
  <h3>2. Verweise und Links</h3>
  <p>Bei direkten oder indirekten Verweisen auf fremde Webseiten (Hyperlinks), die außerhalb des Verantwortungsbereiches des Autors liegen, würde eine Haftungsverpflichtung ausschließlich in dem Fall in Kraft treten, in dem der Autor von den Inhalten Kenntnis hat und es ihm technisch möglich und zumutbar wäre, die Nutzung im Falle rechtswidriger Inhalte zu verhindern. Der Autor erklärt hiermit ausdrücklich, dass zum Zeitpunkt der Linksetzung keine illegalen Inhalte auf den zu verlinkenden Seiten erkennbar waren. Auf die aktuelle und zukünftige Gestaltung, die Inhalte oder die Urheberschaft der verlinkten/verknüpften Seiten hat der Autor keinerlei Einfluss. Deshalb distanziert er sich hiermit ausdrücklich von allen Inhalten aller verlinkten/verknüpften Seiten, die nach der Linksetzung verändert wurden. Diese Feststellung gilt für alle innerhalb des eigenen Internetangebotes gesetzten Links und Verweise sowie für Fremdeinträge in vom Autor eingerichteten Gästebüchern, Diskussionsforen, Linkverzeichnissen, Mailinglisten und in allen anderen Formen von Datenbanken, auf deren Inhalt externe Schreibzugriffe möglich sind. Für illegale, fehlerhafte oder unvollständige Inhalte und insbesondere für Schäden, die aus der Nutzung oder Nichtnutzung solcherart dargebotener Informationen entstehen, haftet allein der Anbieter der Seite, auf welche verwiesen wurde, nicht derjenige, der über Links auf die jeweilige Veröffentlichung lediglich verweist.</p>
  <h3>3. Urheber- und Kennzeichenrecht</h3>
  <p>Der Autor ist bestrebt, in allen Publikationen die Urheberrechte der verwendeten Grafiken, Tondokumente, Videosequenzen und Texte zu beachten, von ihm selbst erstellte Grafiken, Tondokumente, Videosequenzen und Texte zu nutzen oder auf lizenzfreie Grafiken, Tondokumente, Videosequenzen und Texte zurückzugreifen. Alle innerhalb des Internetangebotes genannten und ggf. durch Dritte geschützten Marken- und Warenzeichen unterliegen uneingeschränkt den Bestimmungen des jeweils gültigen Kennzeichenrechts und den Besitzrechten der jeweiligen eingetragenen Eigentümer. Allein aufgrund der bloßen Nennung ist nicht der Schluss zu ziehen, dass Markenzeichen nicht durch Rechte Dritter geschützt sind! Das Copyright für veröffentlichte, vom Autor selbst erstellte Objekte bleibt allein beim Autor der Seiten. Eine Vervielfältigung oder Verwendung solcher Grafiken, Tondokumente, Videosequenzen und Texte in anderen elektronischen oder gedruckten Publikationen ist ohne ausdrückliche Zustimmung des Autors nicht gestattet.</p>
  <h3>4. Datenschutz</h3>
  <p>Sofern innerhalb des Internetangebotes die Möglichkeit zur Eingabe persönlicher oder geschäftlicher Daten (E-Mail-Adressen, Namen, Anschriften) besteht, so erfolgt die Preisgabe dieser Daten seitens des Nutzers auf ausdrücklich freiwilliger Basis. Die Inanspruchnahme und Bezahlung aller angebotenen Dienste ist – soweit technisch möglich und zumutbar – auch ohne Angabe solcher Daten bzw. unter Angabe anonymisierter Daten oder eines Pseudonyms gestattet. Die Nutzung der im Rahmen des Impressums oder vergleichbarer Angaben veröffentlichten Kontaktdaten wie Postanschriften, Telefon- und Faxnummern sowie E-Mail-Adressen durch Dritte zur Übersendung von nicht ausdrücklich angeforderten Informationen ist nicht gestattet. Rechtliche Schritte gegen die Versender von sogenannten Spam-Mails bei Verstößen gegen dieses Verbot sind ausdrücklich vorbehalten.</p>
  <h3>5. Rechtswirksamkeit dieses Haftungsausschlusses</h3>
  <p>Dieser Haftungsausschluss ist als Teil des Internetangebotes zu betrachten, von dem aus auf diese Seite verwiesen wurde. Sofern Teile oder einzelne Formulierungen dieses Textes der geltenden Rechtslage nicht, nicht mehr oder nicht vollständig entsprechen sollten, bleiben die übrigen Teile des Dokumentes in ihrem Inhalt und ihrer Gültigkeit davon unberührt.</p>
  <h2>Bildnachweis</h2>
  <p>Alle Fotos, Drohnenaufnahmen und Visualisierungen: BAUSCHULZ GmbH &amp; Co. KG. Kartendaten: © <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a>-Mitwirkende.</p>
</div></section>'''
    return seite(datei="impressum.html", titel="Impressum | BAUSCHULZ GmbH & Co. KG", beschreibung="Impressum der BAUSCHULZ GmbH & Co. KG, Fehringstraße 8, 38524 Sassenburg – Angaben gemäß § 5 TMG.", aktiv="", body=body)


def seite_datenschutz():
    body = f'''<section class="recht"><div class="wrap">
  <h1>Datenschutz&shy;erklärung</h1>
  <h2>1. Datenschutz auf einen Blick</h2>
  <h3>Allgemeine Hinweise</h3>
  <p>Die folgenden Hinweise geben einen einfachen Überblick darüber, was mit Ihren personenbezogenen Daten passiert, wenn Sie diese Website besuchen. Personenbezogene Daten sind alle Daten, mit denen Sie persönlich identifiziert werden können. Ausführliche Informationen zum Thema Datenschutz entnehmen Sie unserer unter diesem Text aufgeführten Datenschutzerklärung.</p>
  <h3>Datenerfassung auf dieser Website</h3>
  <p><b>Wer ist verantwortlich für die Datenerfassung auf dieser Website?</b><br>Die Datenverarbeitung auf dieser Website erfolgt durch den Websitebetreiber. Dessen Kontaktdaten können Sie dem Abschnitt „Hinweis zur verantwortlichen Stelle“ in dieser Datenschutzerklärung entnehmen.</p>
  <p><b>Wie erfassen wir Ihre Daten?</b><br>Ihre Daten werden zum einen dadurch erhoben, dass Sie uns diese mitteilen. Hierbei kann es sich z. B. um Daten handeln, die Sie in ein Kontaktformular eingeben. Andere Daten werden automatisch oder nach Ihrer Einwilligung beim Besuch der Website durch unsere IT-Systeme erfasst. Das sind vor allem technische Daten (z. B. Internetbrowser, Betriebssystem oder Uhrzeit des Seitenaufrufs). Die Erfassung dieser Daten erfolgt automatisch, sobald Sie diese Website betreten.</p>
  <p><b>Wofür nutzen wir Ihre Daten?</b><br>Ein Teil der Daten wird erhoben, um eine fehlerfreie Bereitstellung der Website zu gewährleisten. Andere Daten können zur Analyse Ihres Nutzerverhaltens verwendet werden.</p>
  <p><b>Welche Rechte haben Sie bezüglich Ihrer Daten?</b><br>Sie haben jederzeit das Recht, unentgeltlich Auskunft über Herkunft, Empfänger und Zweck Ihrer gespeicherten personenbezogenen Daten zu erhalten. Sie haben außerdem ein Recht, die Berichtigung oder Löschung dieser Daten zu verlangen. Wenn Sie eine Einwilligung zur Datenverarbeitung erteilt haben, können Sie diese Einwilligung jederzeit für die Zukunft widerrufen. Außerdem haben Sie das Recht, unter bestimmten Umständen die Einschränkung der Verarbeitung Ihrer personenbezogenen Daten zu verlangen. Des Weiteren steht Ihnen ein Beschwerderecht bei der zuständigen Aufsichtsbehörde zu. Hierzu sowie zu weiteren Fragen zum Thema Datenschutz können Sie sich jederzeit an uns wenden.</p>
  <h2>2. Hosting</h2>
  <p>Wir hosten die Inhalte unserer Website bei folgendem Anbieter:</p>
  <h3>All-Inkl</h3>
  <p>Anbieter ist die ALL-INKL.COM – Neue Medien Münnich, Inh. René Münnich, Hauptstraße 68, 02742 Friedersdorf (nachfolgend All-Inkl). Details entnehmen Sie der Datenschutzerklärung von All-Inkl: <a href="https://all-inkl.com/datenschutzinformationen/" target="_blank" rel="noopener">https://all-inkl.com/datenschutzinformationen/</a>.</p>
  <p>Die Verwendung von All-Inkl erfolgt auf Grundlage von Art. 6 Abs. 1 lit. f DSGVO. Wir haben ein berechtigtes Interesse an einer möglichst zuverlässigen Darstellung unserer Website. Sofern eine entsprechende Einwilligung abgefragt wurde, erfolgt die Verarbeitung ausschließlich auf Grundlage von Art. 6 Abs. 1 lit. a DSGVO und § 25 Abs. 1 TTDSG, soweit die Einwilligung die Speicherung von Cookies oder den Zugriff auf Informationen im Endgerät des Nutzers (z. B. Device-Fingerprinting) im Sinne des TTDSG umfasst. Die Einwilligung ist jederzeit widerrufbar.</p>
  <p><b>Auftragsverarbeitung</b><br>Wir haben einen Vertrag über Auftragsverarbeitung (AVV) zur Nutzung des oben genannten Dienstes geschlossen. Hierbei handelt es sich um einen datenschutzrechtlich vorgeschriebenen Vertrag, der gewährleistet, dass dieser die personenbezogenen Daten unserer Websitebesucher nur nach unseren Weisungen und unter Einhaltung der DSGVO verarbeitet.</p>
  <h2>3. Allgemeine Hinweise und Pflichtinformationen</h2>
  <h3>Datenschutz</h3>
  <p>Die Betreiber dieser Seiten nehmen den Schutz Ihrer persönlichen Daten sehr ernst. Wir behandeln Ihre personenbezogenen Daten vertraulich und entsprechend den gesetzlichen Datenschutzvorschriften sowie dieser Datenschutzerklärung. Wenn Sie diese Website benutzen, werden verschiedene personenbezogene Daten erhoben. Personenbezogene Daten sind Daten, mit denen Sie persönlich identifiziert werden können. Die vorliegende Datenschutzerklärung erläutert, welche Daten wir erheben und wofür wir sie nutzen. Sie erläutert auch, wie und zu welchem Zweck das geschieht. Wir weisen darauf hin, dass die Datenübertragung im Internet (z. B. bei der Kommunikation per E-Mail) Sicherheitslücken aufweisen kann. Ein lückenloser Schutz der Daten vor dem Zugriff durch Dritte ist nicht möglich.</p>
  <h3>Hinweis zur verantwortlichen Stelle</h3>
  <p>Die verantwortliche Stelle für die Datenverarbeitung auf dieser Website ist:</p>
  <address>BAUSCHULZ GmbH &amp; Co. KG<br>Fehringstraße 8<br>38524 Sassenburg<br>Telefon: <a href="tel:{TEL_INT}">0176 31482066</a><br>E-Mail: <a href="mailto:{MAIL}">{MAIL}</a></address>
  <p>Verantwortliche Stelle ist die natürliche oder juristische Person, die allein oder gemeinsam mit anderen über die Zwecke und Mittel der Verarbeitung von personenbezogenen Daten (z. B. Namen, E-Mail-Adressen o. Ä.) entscheidet.</p>
  <h3>Speicherdauer</h3>
  <p>Soweit innerhalb dieser Datenschutzerklärung keine speziellere Speicherdauer genannt wurde, verbleiben Ihre personenbezogenen Daten bei uns, bis der Zweck für die Datenverarbeitung entfällt. Wenn Sie ein berechtigtes Löschersuchen geltend machen oder eine Einwilligung zur Datenverarbeitung widerrufen, werden Ihre Daten gelöscht, sofern wir keine anderen rechtlich zulässigen Gründe für die Speicherung Ihrer personenbezogenen Daten haben (z. B. steuer- oder handelsrechtliche Aufbewahrungsfristen); im letztgenannten Fall erfolgt die Löschung nach Fortfall dieser Gründe.</p>
  <h3>Widerruf Ihrer Einwilligung zur Datenverarbeitung</h3>
  <p>Viele Datenverarbeitungsvorgänge sind nur mit Ihrer ausdrücklichen Einwilligung möglich. Sie können eine bereits erteilte Einwilligung jederzeit widerrufen. Die Rechtmäßigkeit der bis zum Widerruf erfolgten Datenverarbeitung bleibt vom Widerruf unberührt.</p>
  <h3>Beschwerderecht bei der zuständigen Aufsichtsbehörde</h3>
  <p>Im Falle von Verstößen gegen die DSGVO steht den Betroffenen ein Beschwerderecht bei einer Aufsichtsbehörde zu, insbesondere in dem Mitgliedstaat ihres gewöhnlichen Aufenthalts, ihres Arbeitsplatzes oder des Orts des mutmaßlichen Verstoßes. Das Beschwerderecht besteht unbeschadet anderweitiger verwaltungsrechtlicher oder gerichtlicher Rechtsbehelfe.</p>
  <h3>Recht auf Datenübertragbarkeit</h3>
  <p>Sie haben das Recht, Daten, die wir auf Grundlage Ihrer Einwilligung oder in Erfüllung eines Vertrags automatisiert verarbeiten, an sich oder an einen Dritten in einem gängigen, maschinenlesbaren Format aushändigen zu lassen. Sofern Sie die direkte Übertragung der Daten an einen anderen Verantwortlichen verlangen, erfolgt dies nur, soweit es technisch machbar ist.</p>
  <h3>Auskunft, Berichtigung und Löschung</h3>
  <p>Sie haben im Rahmen der geltenden gesetzlichen Bestimmungen jederzeit das Recht auf unentgeltliche Auskunft über Ihre gespeicherten personenbezogenen Daten, deren Herkunft und Empfänger und den Zweck der Datenverarbeitung und ggf. ein Recht auf Berichtigung oder Löschung dieser Daten. Hierzu sowie zu weiteren Fragen zum Thema personenbezogene Daten können Sie sich jederzeit an uns wenden.</p>
  <h3>SSL- bzw. TLS-Verschlüsselung</h3>
  <p>Diese Seite nutzt aus Sicherheitsgründen und zum Schutz der Übertragung vertraulicher Inhalte, wie zum Beispiel Anfragen, die Sie an uns als Seitenbetreiber senden, eine SSL- bzw. TLS-Verschlüsselung. Eine verschlüsselte Verbindung erkennen Sie daran, dass die Adresszeile des Browsers von „http://“ auf „https://“ wechselt und an dem Schloss-Symbol in Ihrer Browserzeile.</p>
  <h2>4. Datenerfassung auf dieser Website</h2>
  <h3>Server-Log-Dateien</h3>
  <p>Der Provider der Seiten erhebt und speichert automatisch Informationen in so genannten Server-Log-Dateien, die Ihr Browser automatisch an uns übermittelt. Dies sind: Browsertyp und Browserversion, verwendetes Betriebssystem, Referrer URL, Hostname des zugreifenden Rechners, Uhrzeit der Serveranfrage und IP-Adresse. Eine Zusammenführung dieser Daten mit anderen Datenquellen wird nicht vorgenommen. Die Erfassung dieser Daten erfolgt auf Grundlage von Art. 6 Abs. 1 lit. f DSGVO. Der Websitebetreiber hat ein berechtigtes Interesse an der technisch fehlerfreien Darstellung und der Optimierung seiner Website – hierzu müssen die Server-Log-Dateien erfasst werden.</p>
  <h3>Kontaktformular und Anfrage per E-Mail, Telefon oder WhatsApp</h3>
  <p>Wenn Sie uns per Kontaktformular, E-Mail, Telefon oder WhatsApp kontaktieren, wird Ihre Anfrage inklusive aller daraus hervorgehenden personenbezogenen Daten (Name, Anfrage) zum Zwecke der Bearbeitung Ihres Anliegens bei uns gespeichert und verarbeitet. Diese Daten geben wir nicht ohne Ihre Einwilligung weiter. Die Verarbeitung dieser Daten erfolgt auf Grundlage von Art. 6 Abs. 1 lit. b DSGVO, sofern Ihre Anfrage mit der Erfüllung eines Vertrags zusammenhängt oder zur Durchführung vorvertraglicher Maßnahmen erforderlich ist. In allen übrigen Fällen beruht die Verarbeitung auf unserem berechtigten Interesse an der effektiven Bearbeitung der an uns gerichteten Anfragen (Art. 6 Abs. 1 lit. f DSGVO) oder auf Ihrer Einwilligung (Art. 6 Abs. 1 lit. a DSGVO), sofern diese abgefragt wurde. Das Kontaktformular dieser Website öffnet Ihr E-Mail-Programm mit einer vorbereiteten Nachricht; es werden keine Formulardaten auf unserem Server gespeichert. Bei der Nutzung von WhatsApp gelten zusätzlich die Datenschutzbestimmungen der WhatsApp Ireland Ltd.</p>
  <h2>5. Kartendarstellung (OpenStreetMap)</h2>
  <p>Auf der Kontaktseite binden wir eine Karte des Dienstes OpenStreetMap ein, bereitgestellt von der OpenStreetMap Foundation, St John's Innovation Centre, Cowley Road, Cambridge, CB4 0WS, Großbritannien. Die Karte wird erst geladen, wenn der Kartenbereich in Ihrem Browserfenster sichtbar wird. Dabei wird Ihre IP-Adresse an die Server der OpenStreetMap Foundation übertragen. Die Nutzung erfolgt im Interesse einer ansprechenden Darstellung unserer Bauorte und einer leichten Auffindbarkeit unseres Betriebs (Art. 6 Abs. 1 lit. f DSGVO). Weitere Informationen: <a href="https://wiki.osmfoundation.org/wiki/Privacy_Policy" target="_blank" rel="noopener">wiki.osmfoundation.org/wiki/Privacy_Policy</a>.</p>
  <h2>6. Schriften und Skripte</h2>
  <p>Schriften und Skripte dieser Website werden lokal von unserem Server geladen; es findet keine Verbindung zu Google Fonts oder anderen Schriftdiensten statt. Die Kartenbibliothek Leaflet wird beim Laden der Karte von cdnjs.cloudflare.com (Cloudflare, Inc.) bezogen; dabei wird Ihre IP-Adresse an Cloudflare übermittelt.</p>
  <p class="hinweis">Diese Datenschutzerklärung basiert auf dem Entwurf des Betriebs und wurde um die tatsächlich auf dieser Website eingesetzten Dienste ergänzt. Vor Veröffentlichung juristisch prüfen lassen.</p>
</div></section>'''
    return seite(datei="datenschutz.html", titel="Datenschutzerklärung | BAUSCHULZ GmbH & Co. KG", beschreibung="Datenschutzerklärung der BAUSCHULZ GmbH & Co. KG, Fehringstraße 8, 38524 Sassenburg – Hosting, Kontakt, Karte.", aktiv="", body=body)


# ----------------------------------------------------------------------------- BUILD
def main():
    seiten = {
        "index.html": seite_index(),
        "bautagebuch.html": seite_bautagebuch(),
        "leistungen.html": seite_leistungen(),
        "referenzen.html": seite_referenzen(),
        "ueber-uns.html": seite_ueber(),
        "kontakt.html": seite_kontakt(),
        "impressum.html": seite_impressum(),
        "datenschutz.html": seite_datenschutz(),
    }
    for l in LEISTUNGEN:
        if l["seite"]:
            seiten[f'{l["slug"]}.html'] = seite_leistung(l)
    for i, p in enumerate(PROJEKTE):
        seiten[f'referenz-{p["slug"]}.html'] = seite_projekt(i, p)
    for name, inhalt in seiten.items():
        (ROOT / name).write_text(inhalt, encoding="utf-8")
    # Sitemap + robots
    urls = "".join(f"<url><loc>{DOMAIN}/{'' if n == 'index.html' else n}</loc><changefreq>monthly</changefreq><priority>{'1.0' if n == 'index.html' else '0.7'}</priority></url>" for n in seiten if n not in ("impressum.html", "datenschutz.html"))
    (ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n', encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n", encoding="utf-8")
    print(f"{len(seiten)} Seiten geschrieben nach {ROOT}")


if __name__ == "__main__":
    main()
