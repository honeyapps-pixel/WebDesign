#!/usr/bin/env python3
"""kt38_prosa.py — die zwölf Text-Seiten von KlimaTech38 (Leistungen, Ratgeber, FAQ, Kontakt, Recht).

Wird von gen_kt38_shop.py aufgerufen (alle(G) bekommt dessen Bausteine). Die Texte stammen 1:1 aus
dem Erstbau (fachlich geprueft, nichts erfunden); neu ist nur das Skelett lt. Blueprint:
Kapitel-Kopf mit variablem Slot je Leistungsseite, Index-/Artikel-/Fragen-Kopf, Karte-zuerst.
Frage-Headlines der Leistungsseiten stehen in Aussageform (Blueprint Achse 2), Fliesstext unveraendert.
Laengere Artikel- und Rechtstexte liegen als Partials in .tools/kt38_inhalt/.
"""
import html
import json
import re
from pathlib import Path

import kt38_katalog as K
import kt38_chrome as C
import kt38_seite as S

INHALT = Path(__file__).resolve().parent / "kt38_inhalt"
DOMAIN = S.DOMAIN


def e(s):
    return html.escape(str(s), quote=True)


def partial(name):
    return (INHALT / f"{name}.html").read_text(encoding="utf-8")


def service_ld(name, beschreibung, datei, typ="Service"):
    return {"@context": "https://schema.org", "@type": typ, "name": name, "description": beschreibung,
            "url": f"{DOMAIN}/{datei}", "provider": {"@id": f"{DOMAIN}/#business"},
            "areaServed": [{"@type": "City", "name": n} for n in ["Gifhorn", "Wolfsburg", "Braunschweig", "Peine", "Salzgitter", "Helmstedt"]]}


def kapitel_kopf(G, h1, lead, bild, alt, slot, hell=False, chips=None, brot=None, kurz=False):
    kl = "kap" + (" kap--kurz" if kurz else "")
    ch = "".join(G["chip"](c) for c in (chips or []))
    b = ""
    if brot:
        b = '<p class="brot" style="margin-bottom:var(--s2)">' + "".join(
            (f'<a href="{h}">{t}</a><span aria-hidden="true">/</span>' if h else f'<span aria-current="page">{t}</span>') for t, h in brot) + "</p>"
    return f"""<section class="{kl}" aria-labelledby="seite-h">
  <div class="kap__bild"><img src="assets/{bild}" alt="{e(alt)}" width="1400" height="933" fetchpriority="high"></div>
  <div class="kap__innen">
    <div>{b}<h1 id="seite-h">{h1}</h1><p class="kap__lead">{lead}</p></div>
    <div class="kap__slot">{f'<div class="chips">{ch}</div>' if ch else ''}{slot}</div>
  </div>
</section>"""


def punkte(items, icon=False):
    li = []
    for i, (t, d) in enumerate(items):
        nr = f'<span class="punkte__nr">{"" if icon else f"0{i + 1}"}</span>' if not icon else f'<span class="punkte__nr">{icon}</span>'
        li.append(f'<li>{nr}<div><b>{t}</b><p>{d}</p></div></li>')
    return f'<ol class="punkte{" punkte--icon" if icon else ""}">{"".join(li)}</ol>'


def strecke(items, klasse="strecke--5", ids=False):
    def li(i, t, d):
        idattr = f' id="schritt-{i + 1}"' if ids else ""
        return f'<li class="schritt"{idattr} data-reveal style="--d:{i}"><span class="schritt__nr">0{i + 1}</span><h3>{t}</h3><p>{d}</p></li>'
    return '<ol class="strecke ' + klasse + '">' + "".join(li(i, t, d) for i, (t, d) in enumerate(items)) + "</ol>"


def tab(caption, kopf, zeilen, klasse="tab"):
    th = "".join(f'<th scope="col">{c}</th>' for c in kopf)
    body = ""
    for z in zeilen:
        if len(z) == 2 and z[1] is None:
            body += f'<tr><th scope="row">{z[0]}</th></tr>'
            continue
        cells = "".join(f'<td data-l="{e(kopf[i + 1])}">{c}</td>' for i, c in enumerate(z[1:]))
        body += f'<tr><th scope="row">{z[0]}</th>{cells}</tr>'
    cap = f"<caption>{caption}</caption>" if caption else ""
    return f'<table class="{klasse}">{cap}<thead><tr>{th}</tr></thead><tbody>{body}</tbody></table>'


def kanal_wahl():
    return f"""<div class="kanaele">
      <a class="kanal karte" href="tel:{C.TEL}"><span class="kanal__i">{C.ICON_TEL}</span><span><b>{C.TEL_TEXT}</b><small>Mo–Fr 08–18 Uhr · Anruf ist am schnellsten</small></span></a>
      <a class="kanal karte" href="{C.WA}" target="_blank" rel="noopener"><span class="kanal__i">{C.ICON_WA}</span><span><b>WhatsApp</b><small>Fotos vom Raum direkt schicken</small></span></a>
      <a class="kanal karte" href="kontakt.html#anfrage"><span class="kanal__i">{C.ICON_CLOCK}</span><span><b>Beratung anfragen</b><small>Formular mit Rückruf-Zeitfenster</small></span></a>
    </div>"""


# ============================================================================ Leistungsseiten

def klimaanlagen(G):
    chip, A = G["chip"], G["ICON_ARROW"]
    datei = "klimaanlagen.html"
    ld = service_ld("Planung, Auslegung und Montage von Klimaanlagen",
                    "Split- und Multi-Split-Klimaanlagen: Beratung, Auslegung, Lieferung, Einbau und Wartung im Raum Gifhorn, Wolfsburg, Braunschweig.", datei)
    t = S.kopf("Klimaanlagen Gifhorn – Planung, Auslegung, Montage | KlimaTech38",
               "Split- und Multi-Split-Klimaanlagen für Gifhorn, Wolfsburg und Braunschweig: Beratung, Auslegung, Lieferung, fachgerechter Einbau und Wartung.",
               datei, ld, og="assets/innengeraet.jpg", og_alt="Wandmontiertes Innengerät einer Split-Klimaanlage")
    slot = (f'<div class="mini-stages">'
            f'<a class="mini-stage" href="shop-split.html">{G["geraet_svg"]("split1", kw=3.5)}<span>Split</span></a>'
            f'<a class="mini-stage" href="shop-multisplit.html">{G["geraet_svg"]("multi3", kw=6.8)}<span>Multi-Split</span></a>'
            f'<a class="mini-stage" href="shop-mobil.html">{G["geraet_svg"]("mono", kw=2.0)}<span>Mobil</span></a></div>'
            f'<p class="btns"><a class="btn btn--primary" href="kontakt.html">Beratung anfragen{A}</a><a class="btn btn--rand" href="index.html#rechner">Kühllast berechnen</a></p>')
    t += kapitel_kopf(G, "Klimaanlagen: geplant, ausgelegt, <em>geliefert, montiert.</em>",
                      "Vom ersten Blick in den Raum bis zur Inbetriebnahme. Wir bestimmen die Kühllast, legen Gerät und Leitungsweg aus, liefern das Gerät und bauen es ein – zwischen Gifhorn, Wolfsburg und Braunschweig.",
                      "innengeraet.jpg", "Wandmontiertes Innengerät einer Split-Klimaanlage in einem hellen Raum", slot)
    vergleich = tab("Split und Multi-Split im Vergleich", ["Merkmal", "Split", "Multi-Split"], [
        ("Aufbau", "1 Außengerät, 1 Innengerät", "1 Außengerät, bis zu 4 Innengeräte"),
        ("Passt für", "einen einzelnen Raum", "mehrere Räume oder Bereiche"),
        ("Temperatur", "eine Zone", "je Raum eigene Einstellung"),
        ("Innengeräte", "ein Modell", "Designs und Leistungsklassen kombinierbar"),
        ("Fassade", "ein Außengerät, diskrete Installation", "ein Außengerät für das ganze Haus"),
    ])
    ablauf = strecke([
        ("Beratung und Raum-Bewertung", "Vor Ort oder digital. Wir sehen uns Raumzuschnitt, Fensterflächen und Ausrichtung, Dämmung, Nutzung und Belegung an. Daraus ergibt sich die Kühllast – und die Frage, ob ein Innengerät reicht oder zwei sinnvoller sind. Für den ersten Eindruck genügen Fotos per WhatsApp."),
        ("Planung und Auslegung", "Leistung in kW, Zahl und Position der Innengeräte, Standort des Außengeräts, Länge und Führung der Kältemittelleitung, Kondensatablauf, Elektroanschluss und Schallabstand zur Nachbargrenze. Ein zu groß gewähltes Gerät taktet und entfeuchtet schlechter – deshalb rechnen wir, statt aufzurunden."),
        ("Auswahl und Lieferung", "Wir wählen das Gerät nach Kühl- und Heizleistung, Schallleistungspegel, Effizienz (SEER/SCOP) und Kältemittel aus und liefern es. Geräte mit R-32 und – wo sinnvoll – Quick-Connect-Anschluss."),
        ("Einbau, Inbetriebnahme, Wartung", "Kernbohrung, Wandhalter, Leitungen verlegen und bördeln, Vakuum ziehen, Dichtheit prüfen, befüllen, in Betrieb nehmen, einweisen. Danach auf Wunsch regelmäßige Wartung: Filter und Wärmetauscher reinigen, Kondensatweg prüfen, Funktion messen."),
        ("Kopplung mit Photovoltaik", "Ist eine PV-Anlage vorhanden oder geplant, stimmen wir Kühlung und Erzeugung aufeinander ab. Die Kühllast ist mittags am höchsten – genau dann liefert die Anlage am meisten."),
    ])
    aussen = punkte([
        ("Abstand zur Grundstücksgrenze", "Für die Geräuschbelastung an der Nachbargrenze gelten Immissionsrichtwerte; nachts sind sie deutlich strenger als tagsüber. Wir prüfen Standort und Schallleistung des Geräts, bevor wir bohren."),
        ("Luftführung", "Das Außengerät braucht freie An- und Abströmung. In einer engen Nische saugt es die eigene Warmluft wieder an und verliert Leistung."),
        ("Leitungslänge", "Je länger die Kältemittelleitung und je größer der Höhenunterschied, desto mehr Leistung geht verloren. Kurze Wege sind kein Schönheitsthema."),
        ("Kondensat", "Ein kühlendes Innengerät entfeuchtet – das Wasser muss sicher abgeführt werden. Fehlt das Gefälle, tropft es irgendwann in die Wand."),
        ("Mietwohnung", "Für Kernbohrung und Außengerät brauchen Sie die Zustimmung der Eigentümerin oder des Eigentümers. Ohne sie bleibt das mobile Monoblock-Gerät die realistische Lösung – <a href=\"shop-mobil.html\">im Katalog</a>."),
    ])
    kaelte = punkte([
        ("Warum R-32", "R-32 hat ein deutlich geringeres Treibhauspotenzial als das früher übliche R-410A und ist ein Einstoff-Kältemittel – es lässt sich sortenrein absaugen und wiederverwenden. Außerdem wird weniger Füllmenge für dieselbe Leistung gebraucht."),
        ("Dichtheitsprüfung", "Regelmäßige Prüfpflichten nach der F-Gase-Verordnung (EU) 2024/573 greifen erst ab einer bestimmten Füllmenge, gerechnet in CO₂-Äquivalent. Eine typische Wohnraum-Splitanlage liegt darunter – für Sie entsteht dadurch keine wiederkehrende Prüfpflicht. Bei größeren Multi-Split- und Gewerbeanlagen sieht das anders aus; wir sagen Ihnen im Angebot, was für Ihre Anlage gilt."),
        ("Brennbarkeit", "R-32 ist schwer entflammbar (Klasse A2L). Daraus ergeben sich Mindest-Raumgrößen je Füllmenge und Regeln für die Aufstellung. Das ist Teil der Auslegung – nicht Ihre Sorge, aber ein Grund, warum wir den Raum sehen wollen."),
        ("Nachfüllen", "Eine dichte Anlage verliert kein Kältemittel. Wenn nachgefüllt werden muss, ist etwas undicht – dann suchen wir das Leck, statt nur aufzufüllen."),
    ])
    wartung = tab("Wartung: was Sie selbst tun und was wir tun", ["Punkt", "Sie selbst", "Wir"], [
        ("Luftfilter", "In der Kühlsaison alle paar Wochen ausklipsen, ausspülen, trocknen lassen", "Zustand prüfen, bei Bedarf tauschen"),
        ("Wärmetauscher", "–", "Innen- und Außeneinheit reinigen; verschmutzte Lamellen kosten spürbar Leistung"),
        ("Kondensat", "Auf Tropfen oder Geruch achten", "Ablauf und Gefälle prüfen, Wanne reinigen"),
        ("Funktion", "–", "Drücke und Temperaturen messen, Dichtheit sichtprüfen, Elektrik kontrollieren"),
    ])
    t += f"""
<section class="sec" aria-label="Die Beratung">
  <div class="wrap">
    <div class="kopf2" data-reveal><h2>Die Beratung <em>kostet nichts.</em></h2>{chip("Erstkontakt bis Angebot")}</div>
    <div class="karten karten--2">
      <div class="karte fk" data-reveal><div class="fk__bild"><img src="assets/wohnraum.jpg" alt="Heller Wohnraum mit hoher Fensterfront" width="1400" height="988" loading="lazy"></div><div class="fk__body">{chip("3 Schritte")}<h3>Erstkontakt, Besichtigung, Angebot</h3>
        <ol class="punkte">
          <li><span class="punkte__nr">01</span><div><b>Erstkontakt</b><p>Anruf, WhatsApp oder Formular. Für den ersten Eindruck reichen Fotos vom Raum und die Quadratmeter – der Rechner gibt Ihnen vorab eine Hausnummer.</p></div></li>
          <li><span class="punkte__nr">02</span><div><b>Vor Ort</b><p>Wir sehen uns den Raum an: Zuschnitt, Fenster, Ausrichtung, Dämmung, Nutzung, mögliche Leitungswege und den Standort für das Außengerät.</p></div></li>
          <li><span class="punkte__nr">03</span><div><b>Angebot</b><p>Danach bekommen Sie ein schriftliches, unverbindliches Angebot mit Gerät, Leistung, Montageumfang und Preis – kein Richtwert, sondern eine Zahl, an der wir uns messen lassen.</p></div></li>
        </ol></div></div>
      <div class="karte fk fk--tint" data-reveal style="--d:1"><div class="fk__bild"><img src="assets/fernbedienung.jpg" alt="Hand mit Fernbedienung vor einem Innengerät" width="1200" height="800" loading="lazy"></div><div class="fk__body">{chip("1 Telefonnummer", "chip--hell")}<h3>Ein Ansprechpartner</h3><p>Angebot, Montage, Inbetriebnahme und Wartung – derselbe Ansprechpartner, dieselbe Telefonnummer.</p><a class="fk__mehr" href="beratung.html">Beratung &amp; Ablauf{A}</a></div></div>
    </div>
  </div>
</section>
<section class="buehne buehne--sec" aria-label="Split oder Multi-Split">
  <div class="wrap">
    <div class="kopf2" data-reveal><h2>Ein Raum oder mehrere: <em>Split oder Multi-Split.</em></h2>{chip("Split · Multi-Split", "chip--hell")}</div>
    <div class="karten karten--2">
      <a class="karte pk" href="shop-split.html" data-reveal><div class="stage">{G["geraet_svg"]("split1", titel="Split-Anlage")}{chip("1 Raum")}</div><div class="pk__body"><h3>Split-Anlage</h3><p class="pk__kurz">Ein Außengerät, ein Innengerät, eine Leitung dazwischen. Die Sets mit Schnellkupplung können Sie selbst anschließen.</p><span class="fk__mehr">Split-Sets ansehen{A}</span></div></a>
      <a class="karte pk" href="shop-multisplit.html" data-reveal style="--d:1"><div class="stage">{G["geraet_svg"]("multi3", titel="Multi-Split-Anlage")}{chip("2–4 Räume")}</div><div class="pk__body"><h3>Multi-Split-Anlage</h3><p class="pk__kurz">Ein Außengerät versorgt bis zu vier Innengeräte, jeder Raum bekommt seine eigene Temperatur.</p><span class="fk__mehr">Multi-Split-Sets ansehen{A}</span></div></a>
    </div>
    <div class="karte" style="margin-top:var(--s3)" data-reveal><div class="karte__body">{vergleich}<p style="margin-top:var(--s3);color:var(--ink-soft)">Beide Bauarten kühlen, entfeuchten und heizen in der Übergangszeit – das spart Heizenergie, solange es draußen nicht zu kalt ist.</p></div></div>
  </div>
</section>
<section class="sec" aria-label="Ablauf">
  <div class="wrap">
    <div class="kopf2" data-reveal><h2>Fünf Leistungen – <em>von der Raum-Bewertung bis zur PV-Kopplung.</em></h2>{chip("Beratung bis PV")}</div>
    {ablauf}
    <p class="demo-hinweis" style="margin-top:var(--s3)">{G["ICON_INFO"]}<span>Wohin das Innengerät kommt, entscheiden wir beim Termin vor Ort: hoch an der Wand, mit freiem Luftweg, nicht direkt über Sitz- oder Schlafplatz. Am Gerät entsteht Kondensat – der Ablauf braucht durchgehendes Gefälle.</span></p>
  </div>
</section>
<section class="sec sec--cool" aria-label="Außengerät, Kältemittel, Wartung">
  <div class="wrap">
    <div class="kopf2" data-reveal><h2>Drei Dinge, die <em>über Jahre zählen.</em></h2></div>
    <div class="karten karten--2">
      <div class="karte fk" data-reveal><div class="fk__bild"><img src="assets/aussengeraet.jpg" alt="Außengerät an einer hellen Fassade" width="1200" height="800" loading="lazy"></div><div class="fk__body">{chip("Standort")}<h3>Der Standort des Außengeräts entscheidet viel.</h3><p>Freie An- und Abströmung, fester Halt, Schwingungsdämpfer – der Standort entscheidet über Wirkungsgrad, Lautstärke und Nachbarschaftsfrieden.</p>{aussen}</div></div>
      <div class="karte fk" data-reveal style="--d:1"><div class="fk__bild"><img src="assets/innengeraet.jpg" alt="Innengerät einer Split-Klimaanlage" width="1000" height="666" loading="lazy"></div><div class="fk__body">{chip("R-32 · GWP 675")}<h3>Das Kältemittel: R-32.</h3><p>Heutige Splitgeräte laufen mit R-32 – das ist relevant für Wartung und Prüfpflichten.</p>{kaelte}</div></div>
      <div class="karte fk fk--breit fk--tint" data-reveal style="--d:2"><div class="fk__body">{chip("1× jährlich", "chip--hell")}<h3>Filter selbst, den Rest einmal im Jahr.</h3>{wartung}<p style="margin-top:var(--s2)">Einmal jährlich reicht bei normaler Wohnnutzung – am besten im Frühjahr, bevor die erste Hitze kommt.</p><a class="fk__mehr" href="wartung.html">Wartung &amp; Service{A}</a></div></div>
    </div>
  </div>
</section>
{G["pv_split"]()}
{G["abschluss"]("Wir sehen uns Ihren Raum an.", "Vor-Ort-Termin oder erst einmal Fotos per WhatsApp – Besichtigung und Angebot sind kostenfrei.", ("Beratung anfragen", "kontakt.html"), (C.TEL_TEXT + " anrufen", "tel:" + C.TEL))}
"""
    return datei, t + S.fuss("voll")


def beratung(G):
    chip, A = G["chip"], G["ICON_ARROW"]
    datei = "beratung.html"
    ld = service_ld("Beratung und Besichtigung für Klimaanlagen", "Kostenlose Beratung vor Ort: Räume ansehen, Kühllast auslegen, Festpreis-Angebot.", datei)
    t = S.kopf("Beratung & Ablauf – kostenlose Besichtigung | KlimaTech38",
               "Kostenlose Beratung vor Ort für Ihre Klimaanlage: Wir sehen uns die Räume an, legen die Kühllast aus und machen ein Festpreis-Angebot.",
               datei, ld, og="assets/wohnraum.jpg", og_alt="Heller Wohnraum mit hoher Fensterfront")
    ab_montiert = K.eur(K.guenstigster_montagepreis())
    demo = f'<span class="preis-demo">{e(K.META["demoWort"])}</span>' if K.META["demo"] else ""
    slot = f'{C.weg_schalter()}<span class="weg__hint weg__hint--selbst">Auch beim Selbsteinbau: Kernbohrung und Elektroanschluss übernehmen wir auf Wunsch.</span><span class="weg__hint weg__hint--montage">Besichtigung, Auslegung, Festpreis-Angebot, Montage, Wartung.</span>' + kanal_wahl()
    t += kapitel_kopf(G, "Lassen Sie sich <em>die Räume ansehen.</em>",
                      "Wir nennen keine Leistung am Telefon, ohne den Raum gesehen zu haben. Dämmstandard, Fensterfläche, Geschoss und der mögliche Leitungsweg entscheiden über die Anlage – und über den Preis. Besichtigung und Angebot kosten Sie nichts.",
                      "wohnraum.jpg", "Heller Wohnraum mit hoher Fensterfront und Sofa", slot)
    ablauf = strecke([
        ("Anruf oder Anfrage", "Sie sagen uns, welche Räume kühl werden sollen. Fotos per WhatsApp helfen uns, den Termin vorzubereiten."),
        ("Besichtigung vor Ort", "Wir messen die Räume, sehen uns Fenster, Dämmung, Leitungsweg und den möglichen Standort des Außengeräts an."),
        ("Auslegung", "Kühllast je Raum, Gerätegröße, Leitungsführung und Kondensatweg – rechnerisch, nicht nach Gefühl."),
        ("Schriftliches Angebot", "Gerät, Leistung, Montageumfang und Festpreis. Unverbindlich, ohne Frist im Nacken."),
        ("Montage", "Termin nach Absprache. In der Regel ein Tag je Anlage; bei Multi-Split je nach Leitungsweg auch zwei."),
        ("Inbetriebnahme &amp; Einweisung", "Wir fahren die Anlage an, messen die Funktion und zeigen Ihnen Betrieb, Filterreinigung und Heizfunktion."),
    ], "strecke--7")
    vorort = [
        ("Raumgröße und Geschoss", "Grundfläche, Raumhöhe und die Lage im Haus. Unterm Dach liegt die Kühllast gut doppelt so hoch wie im gedämmten Neubau – 130 gegen 60 Watt je Quadratmeter."),
        ("Fenster und Himmelsrichtung", "Große Süd- oder Westverglasung schlägt mit rund 20 Watt je Quadratmeter zusätzlich zu Buche. Außenliegende Beschattung nimmt einen Teil davon wieder weg."),
        ("Standort des Innengeräts", "Hoch an der Wand, mit freiem Luftweg – und nie direkt über dem Sitz- oder Schlafplatz. Zugluft ist ein häufiger Grund, warum eine Anlage später nicht genutzt wird."),
        ("Standort des Außengeräts", "Schallabstand zum Nachbarn, freie Luftführung, Erreichbarkeit für die Wartung. An gedämmten Fassaden setzen wir lieber eine Bodenkonsole als Dübel in die Dämmung."),
        ("Leitungsweg und Kernbohrung", "Wo Kältemittelleitung, Kabel und Kondensatschlauch entlanglaufen und wo gebohrt werden kann, ohne Leitungen zu treffen. Der Bohrkern wird sauber abgedichtet, sonst wird er zur Wärmebrücke."),
        ("Kondensatweg und Strom", "Ob das Kondensat mit Gefälle abfließen kann oder eine Pumpe braucht, und ob die vorhandene Zuleitung reicht oder ein eigener Stromkreis nötig ist."),
    ]
    vk = f'<div class="karte fk__ueber" data-reveal><div class="karte__body"><ol class="punkte punkte--2">' + "".join(f'<li><span class="punkte__nr">0{i + 1}</span><div><b>{t_}</b><p>{d}</p></div></li>' for i, (t_, d) in enumerate(vorort)) + '</ol></div></div>'
    t += f"""
<section class="sec" aria-labelledby="zusagen-h">
  <div class="wrap">
    <h2 class="sr" id="zusagen-h">Drei Zusagen</h2>
    <div class="karten karten--2">
      <div class="karte fk fk--breit fk--tint" data-reveal><div class="fk__body">{chip("Festpreis", "chip--hell")}<h3>Was im Angebot steht, gilt – inklusive Montage.</h3><p class="preis"><span class="preis__w"><b>montiert ab {e(ab_montiert)}</b>{demo}<small>Split-Anlage inkl. Montage – verbindlich im Angebot</small></span></p></div><div class="fk__bild"><img src="assets/raum-schlafzimmer-2.jpg" alt="Schlafzimmer mit Innengerät über dem Bett" width="1200" height="801" loading="lazy"></div></div>
      <div class="karte fk fk--tint" data-reveal style="--d:1"><div class="fk__body">{chip("0 €", "chip--hell")}<h3>Kostenfrei</h3><p>Besichtigung, Auslegung und schriftliches Angebot.</p></div></div>
      <div class="karte fk fk--tint" data-reveal style="--d:2"><div class="fk__body">{chip("1 Telefonnummer", "chip--hell")}<h3>Ein Ansprechpartner</h3><p>Angebot, Montage und Wartung – derselbe Ansprechpartner, dieselbe Telefonnummer.</p></div></div>
    </div>
  </div>
</section>
<section class="sec sec--cool" aria-label="Ablauf">
  <div class="wrap">
    <div class="kopf2" data-reveal><h2>Sechs Schritte <em>vom Anruf bis zur Einweisung.</em></h2>{chip("Anruf bis Einweisung")}</div>
    {ablauf}
  </div>
</section>
<section class="kap kap--kurz kap--ueber" aria-label="Besichtigung">
  <div class="kap__bild"><img src="assets/raum-wohnzimmer.jpg" alt="Helles Wohnzimmer mit Innengerät einer Klimaanlage über dem Fenster" width="1200" height="801" loading="lazy" data-parallax="0.1"></div>
  <div class="kap__innen"><div><h2>Was wir uns <em>vor Ort ansehen.</em></h2></div><div class="kap__slot"><p class="kap__lead">Sechs Punkte, an denen sich später entscheidet, ob die Anlage leise und sparsam läuft.</p></div></div>
</section>
<section class="sec" aria-label="Sechs Punkte">
  <div class="wrap">{vk}</div>
</section>
<section class="sec sec--cool" aria-label="Kontakt aufnehmen">
  <div class="wrap">
    <div class="kopf2" data-reveal><h2>Fotos vorab <em>machen den Termin kürzer.</em></h2></div>
    <div class="split">
      <div class="split__bild" data-reveal="wipe-left"><img src="assets/fernbedienung.jpg" alt="Hand mit Fernbedienung vor einem Innengerät" width="1200" height="800" loading="lazy"></div>
      <div class="split__text" data-reveal><p>Wenn Sie uns vorab Fotos vom Raum, vom Fenster und von der Fassadenseite schicken, können wir den Termin gezielter vorbereiten – und Ihnen oft schon am Telefon sagen, welche Bauart infrage kommt. Anruf ist am schnellsten, Rückruf und WhatsApp gehen auch.</p><p class="btns"><a class="btn btn--primary" href="kontakt.html">Beratung anfragen{A}</a><a class="btn btn--rand" href="index.html#rechner">Erst selbst rechnen</a></p></div>
    </div>
  </div>
</section>
{G["abschluss"]("Sagen Sie uns Ihr Wunsch-Zeitfenster.", "Wir rufen zurück – oder Sie rufen an, das ist am schnellsten.", ("Beratung anfragen", "kontakt.html"), (C.TEL_TEXT + " anrufen", "tel:" + C.TEL))}
"""
    return datei, t + S.fuss("voll")


def montage(G):
    chip, A = G["chip"], G["ICON_ARROW"]
    datei = "montage.html"
    ld = service_ld("Montage von Klimaanlagen", "Einbau von Split- und Multi-Split-Klimaanlagen: Kernbohrung, Halter, Leitungsweg, Vakuumieren, Inbetriebnahme, Einweisung.", datei)
    t = S.kopf("Montage von Klimaanlagen – so läuft der Einbau | KlimaTech38",
               "Wie wir eine Klimaanlage einbauen: Kernbohrung, Halter, Leitungsweg, Kondensat, Vakuumieren, Inbetriebnahme und Einweisung. KlimaTech38, Gifhorn.",
               datei, ld, og="assets/aussengeraet.jpg", og_alt="Außengerät einer Klimaanlage an einer weißen Fassade")
    schritte = ["Einmessen", "Kernbohrung", "Halter", "Leitungen", "Vakuumieren", "Elektrik", "Inbetriebnahme"]
    slot = '<nav class="vorschau-strecke" aria-label="Zu den sieben Schritten">' + "".join(f'<a href="#schritt-{i + 1}"><i>0{i + 1}</i>{s}</a>' for i, s in enumerate(schritte)) + "</nav>"
    t += kapitel_kopf(G, "Der Montagetag: <em>sieben Schritte, ein Arbeitstag.</em>",
                      "In der Regel ein Arbeitstag je Anlage – bei Multi-Split auch zwei. Eine Klimaanlage einzubauen heißt nicht, ein Gerät an die Wand zu schrauben. Der größere Teil der Arbeit liegt im Leitungsweg, in der Kernbohrung und darin, dass der Kältekreis am Ende dicht und trocken ist.",
                      "aussengeraet.jpg", "Außengerät einer Split-Klimaanlage an einer weißen Fassade unter blauem Himmel", slot)
    strecke7 = strecke([
        ("Abdecken und einmessen", "Boden und Möbel abdecken, Position des Innengeräts anzeichnen. Hoch an der Wand, freier Luftweg, nicht über dem Sitzplatz."),
        ("Kernbohrung", "Meist 60 bis 80 mm, mit leichtem Gefälle nach außen, damit Kondensat abläuft. Vorher prüfen wir, wo Leitungen in der Wand liegen."),
        ("Halter setzen", "Innen die Montageplatte, außen Wandkonsole oder Bodenkonsole mit Schwingungsdämpfern. An gedämmten Fassaden bevorzugen wir den Boden."),
        ("Leitungen verlegen", "Kältemittelleitung, Steuerkabel und Kondensatschlauch gemeinsam durch die Bohrung, außen im Kanal oder verdeckt geführt."),
        ("Vakuumieren", "Der Kältekreis wird evakuiert, bis Luft und Feuchtigkeit heraus sind, und auf Dichtheit geprüft. Bei Quick-Connect-Sets entfällt das – die Leitung ist ab Werk befüllt."),
        ("Elektrisch anschließen", "Über Stecker oder fest im Verteiler, je nach Gerät und Leistung. Der feste Anschluss gehört in Fachhände."),
        ("Inbetriebnahme", "Anlage anfahren, Drücke und Temperaturen messen, Kondensatablauf prüfen, Bohrkern abdichten, aufräumen – dann die Einweisung."),
    ], "strecke--7", ids=True)
    worauf = [
        ("Der Bohrkern", "Er geht durch die Dämmebene. Wird er nicht sauber abgedichtet, entsteht genau dort eine Wärmebrücke – und im Winter kondensiert Feuchtigkeit im Mauerwerk. Wir setzen eine Dichtmanschette und schäumen nicht einfach zu."),
        ("Das Gefälle des Kondensatschlauchs", "Kondensat läuft nur mit durchgehendem Gefälle ab. Wo das baulich nicht geht, kommt eine Kondensatpumpe – lieber gleich als nach dem ersten Wasserfleck."),
        ("Der Schallabstand des Außengeräts", "Das Außengerät ist das, was Nachbarn hören. Wir wählen den Standort mit Blick auf Abstand, Reflexionsflächen und Nachtbetrieb – und entkoppeln es von der Wand."),
        ("Dichtheit des Kältekreises", "R-32 ist ein fluoriertes Treibhausgas. Arbeiten am offenen Kältekreis setzen einen Sachkundenachweis nach der F-Gase-Verordnung (EU) 2024/573 voraus – deshalb gehört dieser Schritt zur Montage und nicht zum Selbsteinbau."),
    ]
    wk_chips = ["60–80 mm Bohrkern", "durchgehendes Gefälle", "Nachtwerte gelten", "F-Gase-VO 2024/573"]
    wk_bild = {0: ("daemmung.jpg", "Dämmarbeiten an einer Fassade – der Bohrkern geht durch die Dämmebene", 1200, 800),
               2: ("energieausweis.jpg", "Wohnhäuser dicht beieinander – der Schallabstand zum Nachbarn zählt", 1200, 800)}
    wk = ""
    for i, (t_, d) in enumerate(worauf):
        if i in wk_bild:
            b_, a_, w_, h_ = wk_bild[i]
            wk += f'<div class="karte fk fk--breit" data-reveal style="--d:{i}"><div class="fk__bild"><img src="assets/{b_}" alt="{a_}" width="{w_}" height="{h_}" loading="lazy"></div><div class="fk__body">{chip(wk_chips[i])}<h3>{t_}</h3><p>{d}</p></div></div>'
        else:
            wk += f'<div class="karte fk" data-reveal style="--d:{i}"><div class="fk__body">{chip(wk_chips[i])}<h3>{t_}</h3><p>{d}</p></div></div>'
    t += f"""
<section class="sec" aria-label="Die Arbeitsschritte">
  <div class="wrap">
    <div class="kopf2" data-reveal><h2>Die sieben Schritte <em>in dieser Reihenfolge.</em></h2>{chip("1 Arbeitstag")}</div>
    {strecke7}
  </div>
</section>
<section class="sec sec--cool" aria-label="Worauf es ankommt">
  <div class="wrap">
    <div class="kopf2" data-reveal><h2>Vier Punkte, an denen <em>später Ärger entsteht.</em></h2>{chip("4 Prüfpunkte")}</div>
    <div class="karten">{wk}</div>
  </div>
</section>
<section class="sec" aria-label="Montagepreis">
  <div class="wrap">
    <div class="kopf2" data-reveal><h2>Was im Montagepreis <em>enthalten ist.</em></h2>{chip("Standardumfang")}</div>
    <div class="karte" data-reveal><div class="karte__body set-liste">
      <div><h3>Enthalten</h3><ul><li>{G["ICON_CHECK"]}<span>Anfahrt im Einzugsgebiet, eine Kernbohrung, Halter, Leitungsweg im angegebenen Umfang, Vakuumieren, Inbetriebnahme, Einweisung, Entsorgung des Verpackungsmaterials.</span></li><li>{G["ICON_CHECK"]}<span><b>Vorher klar:</b> Was nötig ist, sehen wir bei der Besichtigung – der Festpreis im Angebot enthält es dann bereits.</span></li></ul></div>
      <div><h3>Kommt einzeln dazu</h3><ul><li class="nein">{G["ICON_PLUS"]}<span>Zusätzliche Leitungsmeter, weitere Kernbohrungen, Kondensatpumpe, Leitungskanäle in Sichtbereichen, fester Elektroanschluss im Verteiler, Gerüst oder Hebebühne.</span></li><li class="nein">{G["ICON_MINUS"]}<span><b>Nicht enthalten:</b> Bauliche Änderungen, Malerarbeiten, Elektroinstallation über den Anschluss hinaus.</span></li></ul></div>
    </div></div>
  </div>
</section>
{G["abschluss"]("Die Besichtigung ist kostenfrei.", "Wir sehen uns Räume, Leitungsweg und Fassade an – der Festpreis steht im Angebot.", ("Beratung anfragen", "kontakt.html"), ("Sets & Preise ansehen", "shop.html"))}
"""
    return datei, t + S.fuss("voll")


def wartung(G):
    chip, A = G["chip"], G["ICON_ARROW"]
    datei = "wartung.html"
    ld = service_ld("Wartung von Klimaanlagen", "Wartung und Service für Klimaanlagen: Filter, Wärmetauscher, Kondensatweg, Kältekreis, Elektrik. Dichtheitsprüfung nach der F-Gase-Verordnung (EU) 2024/573.", datei)
    t = S.kopf("Wartung & Service für Klimaanlagen | KlimaTech38",
               "Wartung von Klimaanlagen in Gifhorn, Wolfsburg und Braunschweig: Intervalle, Umfang, Dichtheitsprüfung nach F-Gase-Verordnung, Störungsdienst.",
               datei, ld, og="assets/innengeraet.jpg", og_alt="Innengerät einer Split-Klimaanlage")
    slot = (f'<dl class="zaehler"><div><dt>Wohnbereich</dt><dd>1×<small>jährlich</small></dd></div><div><dt>Dauerbetrieb</dt><dd>2×<small>jährlich</small></dd></div><div><dt>Dichtheitsprüfung</dt><dd>2024/573<small>F-Gase-VO (EU), je Füllmenge</small></dd></div></dl>'
            f'<p class="btns"><a class="btn btn--primary" href="tel:{C.TEL}">{C.ICON_TEL}{C.TEL_TEXT}</a><a class="btn btn--rand" href="kontakt.html">Beratung anfragen</a></p>')
    t += kapitel_kopf(G, "Wartung: damit die Anlage <em>leise und sparsam bleibt.</em>",
                      "Eine Klimaanlage saugt die Raumluft an und kühlt sie über einen Wärmetauscher ab. Was in der Luft war, bleibt im Filter und auf den Lamellen. Verschmutzte Wärmetauscher kosten Leistung und Strom, ein zugesetzter Kondensatweg führt zu Wasserflecken – und Ablagerungen in einem dauerfeuchten Bauteil sind hygienisch kein guter Ort.",
                      "innengeraet.jpg", "Wandmontiertes Innengerät einer Split-Klimaanlage aus der Nähe", slot)
    umfang = tab("Wartungsumfang je Baugruppe", ["Baugruppe", "Was passiert", "Warum"], [
        ("Luftfilter", "Ausbauen, reinigen oder tauschen", "Ein zugesetzter Filter kostet spürbar Luftmenge und damit Leistung"),
        ("Wärmetauscher innen", "Lamellen reinigen, Gebläserad prüfen", "Staub auf den Lamellen wirkt wie eine Dämmschicht"),
        ("Kondensatwanne und -weg", "Reinigen, Ablauf und Gefälle prüfen, ggf. Pumpe testen", "Der häufigste Grund für Wasserflecken unter dem Innengerät"),
        ("Außengerät", "Verflüssiger reinigen, Laub entfernen, Befestigung prüfen", "Ein verschmutzter Verflüssiger treibt den Verdichterdruck hoch"),
        ("Kältekreis", "Drücke und Temperaturen messen, Sichtprüfung auf Leckagen", "Kältemittelverlust senkt die Leistung, lange bevor die Anlage ausfällt"),
        ("Elektrik", "Klemmen nachziehen, Stromaufnahme messen", "Lose Klemmen sind eine typische Ausfall- und Brandursache"),
    ])
    t += f"""
<section class="sec" aria-label="Intervalle">
  <div class="wrap">
    <div class="kopf2" data-reveal><h2>Einmal jährlich reicht im Wohnbereich&nbsp;– <em>zwei Dinge kommen dazu.</em></h2></div>
    <div class="karten">
      <div class="karte fk fk--tint" data-reveal><div class="fk__body">{chip("1× jährlich", "chip--hell")}<h3>Wohnung und Einfamilienhaus</h3><p>Einmal im Jahr, am besten im Frühjahr vor der ersten Hitze. Den Luftfilter können Sie zwischendurch selbst reinigen – wir zeigen es Ihnen bei der Einweisung.</p></div></div>
      <div class="karte fk fk--tint" data-reveal style="--d:1"><div class="fk__body">{chip("2× jährlich", "chip--hell")}<h3>Dauerbetrieb</h3><p>Anlagen, die rund um die Uhr laufen – Serverraum, Technikraum, Laden mit Kühlbedarf –, brauchen zweimal jährlich Wartung.</p></div></div>
      <div class="karte fk fk--tint" data-reveal style="--d:2"><div class="fk__body">{chip("je nach Füllmenge", "chip--hell")}<h3>Dichtheitsprüfung</h3><p>Für Anlagen ab einer bestimmten Kältemittelfüllmenge schreibt die F-Gase-Verordnung (EU) 2024/573 wiederkehrende Dichtheitsprüfungen vor. Ob Ihre Anlage darunter fällt, hängt an Füllmenge und Kältemittel – wir sagen es Ihnen anhand des Typenschilds.</p></div></div>
      <div class="karte fk fk--voll fk--deep" data-reveal style="--d:3"><div class="fk__body">{chip("Garantie", "chip--sky")}<h3>Herstellergarantie</h3><p>Viele Hersteller verlängern die Garantie nur bei nachgewiesener, regelmäßiger Wartung. Was für Ihr Gerät gilt, steht in den Garantiebedingungen des Herstellers – wir dokumentieren jede Wartung schriftlich.</p></div></div>
    </div>
  </div>
</section>
<section class="sec sec--cool" aria-label="Was wir bei der Wartung machen">
  <div class="wrap">
    <div class="kopf2" data-reveal><h2>Innengerät, Außengerät, Kältekreis, Elektrik&nbsp;– <em>in dieser Reihenfolge.</em></h2></div>
    <div class="karte" data-reveal><div class="karte__body">{umfang}</div></div>
  </div>
</section>
<section class="sec" aria-label="Störung">
  <div class="wrap">
    <div class="split">
      <div class="split__bild" data-reveal="wipe-left"><img src="assets/raum-schlafzimmer.jpg" alt="Schlafzimmer mit Innengerät einer Klimaanlage" width="1200" height="801" loading="lazy"></div>
      <div class="split__text" data-reveal>
        <h2>Wenn die Anlage <em>nicht mehr kühlt.</em></h2>
        <p>Nicht jede Störung ist ein Defekt. Ein zugesetzter Filter, eine falsch eingestellte Betriebsart oder ein blockiertes Außengerät erklären die meisten Fälle von „kühlt nicht mehr richtig“. Bleibt die Leistung danach zu gering, messen wir den Kältekreis – Kältemittelverlust zeigt sich in Drücken und Temperaturen, lange bevor die Anlage ganz ausfällt.</p>
        <p>Wir warten und reparieren auch Anlagen, die nicht von uns eingebaut wurden. Sagen Sie uns am Telefon Hersteller, Typ und ungefähres Baujahr vom Typenschild, dann bringen wir das Passende gleich mit.</p>
        <p class="btns"><a class="btn btn--primary" href="tel:{C.TEL}">{C.ICON_TEL}{C.TEL_TEXT}</a></p>
      </div>
    </div>
  </div>
</section>
{G["abschluss"]("Hersteller, Typ und Baujahr genügen.", "Nennen Sie uns die Angaben vom Typenschild – wir bringen das Passende mit.", ("Beratung anfragen", "kontakt.html"), (C.TEL_TEXT + " anrufen", "tel:" + C.TEL))}
"""
    return datei, t + S.fuss("voll")


def energetische_beratung(G):
    chip, A = G["chip"], G["ICON_ARROW"]
    datei = "energetische-beratung.html"
    ld = service_ld("Energetische Beratung und Energieausweis",
                    "Energieausweis für Wohn- und Nichtwohngebäude, Thermografie, Maßnahmenplanung, Planung von PV, Wärmepumpe und Klimaanlage. dena-Energieberater, Gifhorn.", datei)
    t = S.kopf("Energieausweis & Energieberatung Gifhorn – KlimaTech38",
               "Energieausweis für Wohn- und Nichtwohngebäude, energetische Bewertung und Planung von PV, Wärmepumpe und Klimaanlage. dena-Energieberater, Gifhorn.",
               datei, ld, og="assets/sonne-vorhang.jpg", og_alt="Sonnenlicht durch einen weißen Vorhang")
    slot = f'<p class="btns"><a class="btn btn--primary" href="kontakt.html">Beratung anfragen</a><a class="btn btn--rand" href="tel:{C.TEL}">{C.ICON_TEL}{C.TEL_TEXT}</a></p>'
    t += kapitel_kopf(G, "Energetische Beratung <em>und Planung.</em>",
                      "Wir erstellen die energetische Bewertung Ihrer Immobilie und den gesetzlich vorgeschriebenen Energieausweis – für Wohngebäude ebenso wie für Büro, Praxis, Laden, Werkstatt und Halle. Anlass: Verkauf, Vermietung, Verpachtung, Sanierung.",
                      "sonne-vorhang.jpg", "Sonnenlicht fällt durch einen weißen Vorhang auf den Boden", slot, hell=True,
                      chips=["dena-Energieberater", "TÜV-zertifizierter Fachbetrieb"])
    ausweis = tab("Welcher Ausweis?", ["Ausweisart", "Grundlage", "Typisch für"], [
        ("Verbrauchsausweis", "Abrechnungen der letzten drei Jahre", "Gebäude, für die eine lückenlose Verbrauchsreihe vorliegt"),
        ("Bedarfsausweis", "Aufnahme von Hülle und Anlagentechnik am Gebäude", "ältere, kleine Wohngebäude und Fälle ohne belastbare Verbrauchsdaten"),
    ])
    arten = punkte([
        ("Geometrische Wärmebrücken", "Außenecken, Gebäudekanten, Erker: außen mehr Fläche zum Abkühlen als innen zum Nachheizen."),
        ("Konstruktive Wärmebrücken", "Auskragende Balkonplatten, Deckenauflager, Rollladenkästen, Fensteranschlüsse, durchgehende Stürze – Bauteile, die die Dämmebene durchstoßen."),
        ("Materialbedingte Wärmebrücken", "Stahlbeton oder Metall in einer sonst gedämmten Fläche: das Material leitet Wärme um ein Vielfaches besser als die Dämmung daneben."),
    ])
    aufnahme = tab("", ["Schritt", "Was passiert", "Worauf es ankommt"], [
        ("Zeitpunkt", "Aufnahme in der Heizperiode, möglichst früh am Morgen", "Mindestens rund 15 °C Unterschied zwischen innen und außen, keine Sonne auf der Fassade"),
        ("Aufnahme", "Thermogramme von außen und – wo es zählt – von innen", "Innen zeigt sich das Schimmelrisiko; außen zeigt sich der Wärmeverlust"),
        ("Auswertung", "Bilder mit Temperaturskala, Fundstellen beschrieben und eingeordnet", "Ein rotes Bild allein ist kein Befund – es zählt, was baulich dahintersteckt"),
        ("Ergebnis", "Ein Bericht, der die Fundstellen benennt, bewertet und in den Maßnahmenplan einsortiert", "Nicht nur bunte Bilder"),
    ])
    stell = [
        ("Dämmung von Dach, Fassade und Kellerdecke", "Vermeidung von Wärmeverlusten und deutliche Reduzierung der Heizkosten."),
        ("Fenster- und Türentausch", "Moderne Wärmeschutzverglasung für optimale Isolierung."),
        ("Optimierung der Heizungsanlage", "Austausch alter Systeme gegen effiziente Wärmepumpen oder Hybridlösungen."),
        ("Lüftungssysteme mit Wärmerückgewinnung", "Für ein gesundes Raumklima und zusätzliche Energieeinsparung."),
        ("Integration erneuerbarer Energien", "Photovoltaik, Solarthermie und Speicherlösungen für maximale Unabhängigkeit."),
        ("Modernisierung der Warmwasserbereitung", "Effiziente Systeme für weniger Energieverbrauch."),
    ]
    sk = f'<div class="karte fk__ueber" data-reveal><div class="karte__body"><ol class="punkte punkte--2">' + "".join(f'<li><span class="punkte__nr">0{i + 1}</span><div><b>{t_}</b><p>{d}</p></div></li>' for i, (t_, d) in enumerate(stell)) + '</ol></div></div>'
    plan = strecke([
        ("Aufnahme am Gebäude", "Baujahr, Bauteilaufbauten, Fenster, Heizung, Warmwasser, Lüftung, bisherige Modernisierungen. Wo vorhanden, nehmen wir Pläne und Abrechnungen dazu."),
        ("Bewertung", "Daraus entsteht das energetische Bild des Gebäudes: Wo geht Wärme verloren, welche Bauteile sind die größten Posten, wo droht Feuchte. Hier kommen die Thermogramme dazu."),
        ("Maßnahmen ableiten", "Für jede sinnvolle Maßnahme: erwartete Wirkung, bauliche Voraussetzungen und die Abhängigkeiten. Manche Reihenfolgen sind zwingend – eine Wärmepumpe vor der Dämmung ist meist die teure Variante."),
        ("Priorisieren", "Was zuerst, was später, was zusammen. Wir sagen auch, welche Maßnahme sich in Ihrem Fall nicht lohnt – das gehört zur Beratung dazu."),
        ("Umsetzung begleiten", "Auf Wunsch begleiten wir die Ausführung und prüfen nach: dieselbe Kamera, dieselben Stellen, vorher und nachher."),
    ])
    t += f"""
<section class="sec" aria-labelledby="leist-h">
  <div class="wrap">
    <h2 class="sr" id="leist-h">Drei Leistungen</h2>
    <div class="karten">
      <a class="karte fk" href="#ausweis" data-reveal><div class="fk__bild"><img src="assets/energieausweis.jpg" alt="Wohnhäuser mit Sattel- und Solardächern" width="1200" height="800" loading="lazy"></div><div class="fk__body"><h3>Energieausweis</h3><p>Verbrauchs- oder Bedarfsausweis für Wohn- und Nichtwohngebäude.</p><span class="fk__mehr">Welcher Ausweis?{A}</span></div></a>
      <a class="karte fk" href="#waerme" data-reveal style="--d:1"><div class="fk__bild"><img src="assets/daemmung.jpg" alt="Dämmarbeiten an einer Fassade" width="1200" height="800" loading="lazy"></div><div class="fk__body"><h3>Wärmebrücken finden</h3><p>Die Wärmebildkamera zeigt, wo das Gebäude Wärme verliert – und wo Schimmel beginnt.</p><span class="fk__mehr">Wie die Aufnahme abläuft{A}</span></div></a>
      <a class="karte fk" href="#plan" data-reveal style="--d:2"><div class="fk__bild"><img src="assets/pv-dach.jpg" alt="Haus mit Photovoltaikanlage" width="1400" height="916" loading="lazy"></div><div class="fk__body"><h3>Sanierungsplan</h3><p>Sechs Stellschrauben, in der Reihenfolge, die sich rechnet – bis zur Technik, die sich aus der Bewertung ergibt.</p><span class="fk__mehr">Wie daraus ein Plan wird{A}</span></div></a>
    </div>
  </div>
</section>
<section class="kap kap--kurz kap--ueber" id="ausweis" aria-labelledby="ausweis-h">
  <div class="kap__bild"><img src="assets/energieausweis.jpg" alt="Wohnhäuser mit Sattel- und Solardächern" width="1200" height="800" loading="lazy" data-parallax="0.1"></div>
  <div class="kap__innen"><div><h2 id="ausweis-h">Welchen Ausweis <em>Ihr Gebäude braucht.</em></h2></div><div class="kap__slot"><p class="kap__lead">Verbrauchsausweis oder Bedarfsausweis – das Gebäude entscheidet, nicht der Preis.</p><div class="chips">{chip("Verkauf")}{chip("Vermietung")}{chip("Verpachtung")}{chip("Sanierung")}</div></div></div>
</section>
<section class="sec" aria-label="Ausweisarten">
  <div class="wrap">
    <div class="karte fk__ueber" data-reveal><div class="karte__body">{ausweis}
      <p style="margin-top:var(--s3);color:var(--ink-soft)">Welche Art in Ihrem Fall zulässig oder vorgeschrieben ist, klären wir vorab am Telefon – dafür reichen meist Baujahr, Wohnfläche, Zahl der Wohneinheiten und der Anlass. Angaben im Ausweis müssen bereits in der Immobilienanzeige stehen, deshalb sollte er früh vorliegen.</p>
      <p style="color:var(--ink-soft)"><b>Was wir dafür brauchen:</b> Baujahr und Wohnfläche, Angaben zu Heizung und Warmwasser, durchgeführte Modernisierungen (Fenster, Dämmung, Heizungstausch) und – beim Verbrauchsausweis – die Abrechnungen der letzten drei Jahre.</p></div></div>
  </div>
</section>
<section class="kap kap--kurz kap--ueber" id="waerme" aria-labelledby="waerme-h">
  <div class="kap__bild"><img src="assets/daemmung.jpg" alt="Dämmarbeiten an einer Gebäudefassade mit Gerüst" width="1200" height="800" loading="lazy" data-parallax="0.1"></div>
  <div class="kap__innen"><div><h2 id="waerme-h">Wo Ihr Gebäude <em>Wärme verliert.</em></h2></div><div class="kap__slot"><p class="kap__lead">Wärmebrücken sieht man nicht – die Wärmebildkamera schon. Eine Wärmebrücke ist eine Stelle, an der Wärme schneller nach außen wandert als in der Fläche daneben. Zwei Folgen: Sie heizen für draußen, und die Innenoberfläche wird dort kälter. Fällt sie unter den Taupunkt, schlägt sich Feuchte nieder – und genau dort beginnt Schimmel. Wir kommen aus der Schadensanierung; diese Ecken kennen wir von der anderen Seite.</p></div></div>
</section>
<section class="sec" aria-label="Wärmebrücken">
  <div class="wrap">
    <div class="karten karten--2 karten--oben fk__ueber">
      <div class="karte fk" data-reveal><div class="fk__body">{chip("3 Arten")}<h3>Die drei Arten, die wir suchen</h3>{arten}</div></div>
      <div class="karte fk" data-reveal style="--d:1"><div class="fk__body">{chip("≥ 15 °C Differenz")}<h3>Wie die Aufnahme abläuft</h3>{aufnahme}<p class="demo-hinweis" style="margin-top:var(--s2)">{G["ICON_INFO"]}<span>Die Aufnahme braucht Kälte draußen. Wenn Sie im Sommer fragen, planen wir den Termin für die nächste Heizperiode ein und ziehen die Bauteilaufnahme vor.</span></p></div></div>
    </div>
  </div>
</section>
<section class="kap kap--kurz kap--ueber" id="plan" aria-labelledby="plan-h">
  <div class="kap__bild"><img src="assets/pv-dach.jpg" alt="Haus mit Photovoltaikanlage auf dem Dach" width="1400" height="916" loading="lazy" data-parallax="0.1"></div>
  <div class="kap__innen"><div><h2 id="plan-h">Sechs Stellschrauben&nbsp;– <em>welche sich lohnt, zeigt die Bewertung.</em></h2></div><div class="kap__slot"><p class="kap__lead">Die Dämmebene ist die größte Stellschraube – und die, an der Wärmebrücken entstehen, wenn Anschlüsse und Durchdringungen nicht sauber geplant sind.</p></div></div>
</section>
<section class="sec" aria-label="Stellschrauben">
  <div class="wrap">
    {sk}
    <p class="demo-hinweis" style="margin-top:var(--s3)">{G["ICON_INFO"]}<span>Unser Ziel: nachhaltige Lösungen, die gesetzliche Anforderungen erfüllen, Ihre Energiekosten senken und den Wert Ihrer Immobilie steigern.</span></p>
  </div>
</section>
<section class="sec sec--cool" aria-label="Wie daraus ein Plan wird">
  <div class="wrap">
    <div class="kopf2" data-reveal><h2>Nicht alles auf einmal – <em>sondern in der Reihenfolge, die sich rechnet.</em></h2></div>
    {plan}
  </div>
</section>
<section class="sec" aria-label="Technik nach der Bewertung">
  <div class="wrap">
    <div class="kopf2" data-reveal><h2>Wir planen die Technik, <em>die sich aus der Analyse ergibt.</em></h2>{chip("Nicht umgekehrt")}</div>
    <div class="karten">
      <div class="karte fk" data-reveal><div class="fk__bild"><img src="assets/pv-dach.jpg" alt="Photovoltaikanlage auf einem Hausdach" width="1400" height="916" loading="lazy"></div><div class="fk__body"><h3>Photovoltaik</h3><p>Auslegung nach Dachfläche, Ausrichtung und tatsächlichem Verbrauchsprofil – inklusive der Frage, ob ein Speicher sich rechnet.</p></div></div>
      <div class="karte fk" data-reveal style="--d:1"><div class="fk__bild"><img src="assets/daemmung.jpg" alt="Dämmarbeiten an einer Fassade" width="1200" height="800" loading="lazy"></div><div class="fk__body"><h3>Wärmepumpe</h3><p>Sinnvoll erst, wenn Hülle und Heizflächen dazu passen. Genau das prüft die energetische Bewertung vorher.</p></div></div>
      <a class="karte fk" href="klimaanlagen.html" data-reveal style="--d:2"><div class="fk__bild"><img src="assets/innengeraet.jpg" alt="Innengerät einer Split-Klimaanlage" width="1000" height="666" loading="lazy"></div><div class="fk__body"><h3>Klimaanlage</h3><p>Kühlung als Teil der Energiebilanz gedacht, nicht als Einzelgerät.</p><span class="fk__mehr">Zu den Klimaanlagen{A}</span></div></a>
    </div>
  </div>
</section>
{G["mitwem"]()}
{G["abschluss"]("Baujahr, Fläche und Anlass reichen für den Anfang.", "Ein Anruf genügt – oder Sie schreiben uns kurz.", ("Beratung anfragen", "kontakt.html"), (C.TEL_TEXT + " anrufen", "tel:" + C.TEL))}
"""
    return datei, t + S.fuss("voll")


# ============================================================================ Ratgeber

ARTIKEL = {
    "ratgeber-groesse": ("Welche Leistung braucht mein Raum? – Ratgeber | KlimaTech38",
                         "Wie viel kW braucht eine Klimaanlage? Faustformel nach Fläche und Dämmstandard, Zuschläge für Fenster, Raumhöhe und Technik.",
                         "Welche Leistung braucht mein Raum?", "hero.jpg", "4 Min.", ["split-25", "split-35", "split-50"]),
    "ratgeber-kosten": ("Was kostet eine Klimaanlage? – Ratgeber | KlimaTech38",
                        "Was eine Klimaanlage kostet: Gerätepreis, Montage und Stromkosten getrennt gerechnet, mit den Punkten, die den Preis im Angebot wirklich verschieben.",
                        "Was kostet eine Klimaanlage?", "buero.jpg", "4 Min.", ["mobil-20", "split-35", "multi-duo"]),
    "ratgeber-selbsteinbau": ("Was darf ich selbst einbauen? – Ratgeber | KlimaTech38",
                              "Klimaanlage selbst einbauen: Was bei Quick-Connect-Sets erlaubt ist und wo der Sachkundenachweis nach der F-Gase-Verordnung (EU) 2024/573 greift.",
                              "Was darf ich selbst einbauen?", "raum-schlafzimmer-2.jpg", "3 Min.", ["mobil-20", "split-25", "split-35"]),
    "ratgeber-pv": ("Klimaanlage mit Photovoltaik koppeln – Ratgeber | KlimaTech38",
                    "Klimaanlage und Photovoltaik: Warum Kühlbedarf und Solarertrag zeitlich zusammenfallen und was das für den Eigenverbrauch bedeutet.",
                    "Klimaanlage und Photovoltaik – passt das zusammen?", "pv-dach.jpg", "3 Min.", ["split-35", "multi-duo", "multi-trio"]),
}


def ratgeber_index(G):
    chip, A = G["chip"], G["ICON_ARROW"]
    datei = "ratgeber.html"
    ld = {"@context": "https://schema.org", "@type": "ItemList", "name": "Ratgeber Klimaanlagen",
          "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": t, "url": f"{DOMAIN}/{d}"} for i, (d, t, *_r) in enumerate(G["RATGEBER"])]}
    t = S.kopf("Ratgeber Klimaanlagen – Größe, Kosten, Selbsteinbau | KlimaTech38",
               "Ratgeber von KlimaTech38: Welche Leistung Ihr Raum braucht, was eine Klimaanlage kostet und was Sie selbst einbauen dürfen.", datei, ld)
    karten = "".join(f"""<a class="karte fk" href="{d}" data-reveal style="--d:{i}">
      <div class="fk__bild"><img src="assets/{b}" alt="{G["alt"](b)}" width="1200" height="800" loading="lazy"></div>
      <div class="fk__body">{chip("Lesezeit " + lesezeit_von(partial(d.replace(".html", ""))), "chip--rand")}<h3>{e(t_)}</h3><p>{e(k)}</p><span class="fk__mehr">Lesen{A}</span></div>
    </a>""" for i, (d, t_, k, b, z) in enumerate(G["RATGEBER"]))
    t += f"""
<section class="index-kopf" aria-labelledby="seite-h">
  <div class="wrap">
    <h1 id="seite-h">Vier Fragen, die <em>vor jedem Angebot kommen.</em></h1>
    <h2 class="sr">Die vier Ratgeber</h2>
    <p class="index-kopf__lead">Wir erklären lieber vorher, wovon die Entscheidung abhängt, als hinterher, warum das Angebot so aussieht. Alles hier ist allgemeine Fachkunde – die Zahlen für Ihre Räume kommen aus der Besichtigung.</p>
    <div class="karten karten--4">{karten}</div>
  </div>
</section>
<section class="sec sec--cool" aria-label="Häufige Fragen">
  <div class="wrap">
    <div class="karten karten--2">
      <a class="karte fk fk--breit fk--tint" href="faq.html" data-reveal><div class="fk__body">{chip("14 Antworten")}<h3>Häufige Fragen</h3><p>Die häufigsten stehen gesammelt in den FAQ – Einbaudauer, Lautstärke, Wartung, Kältemittel, Vermieter, Förderung.</p><span class="fk__mehr">Zu den häufigen Fragen{A}</span></div><div class="fk__bild"><img src="assets/raum-schlafzimmer.jpg" alt="Schlafzimmer mit Innengerät einer Klimaanlage" width="1200" height="801" loading="lazy"></div></a>
    </div>
  </div>
</section>
{G["abschluss"]("Lieber direkt fragen.", "Anruf ist am schnellsten – Fotos vom Raum gehen per WhatsApp.", ("Beratung anfragen", "kontakt.html"), (C.TEL_TEXT + " anrufen", "tel:" + C.TEL))}
"""
    return datei, t + S.fuss("voll")


def lesezeit_von(text):
    """Lesezeit aus der Wortzahl (200 Woerter/Minute) statt hartkodiert."""
    woerter = len(re.sub(r"<[^>]+>", " ", text).split())
    return f"{max(1, round(woerter / 200))} Min."


def ratgeber_artikel(G, key):
    chip, A = G["chip"], G["ICON_ARROW"]
    titel, desc, h1, bild, _lz, sets = ARTIKEL[key]
    lesezeit = lesezeit_von(partial(key))
    datei = f"{key}.html"
    ld = [{"@context": "https://schema.org", "@type": "Article", "headline": h1, "description": desc,
           "image": f"{DOMAIN}/assets/{bild}", "author": {"@type": "Organization", "name": "KlimaTech38 – InTroTech GmbH"},
           "publisher": {"@id": f"{DOMAIN}/#business"}, "datePublished": "2026-09-10", "dateModified": K.META["stand"],
           "mainEntityOfPage": f"{DOMAIN}/{datei}"},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "Start", "item": f"{DOMAIN}/"},
              {"@type": "ListItem", "position": 2, "name": "Ratgeber", "item": f"{DOMAIN}/ratgeber.html"},
              {"@type": "ListItem", "position": 3, "name": h1, "item": f"{DOMAIN}/{datei}"}]}]
    t = S.kopf(titel, desc, datei, ld, og=f"assets/{bild}", og_alt=h1)
    body = partial(key)
    body = body.replace('class="tab"', 'class="tab"').replace('<caption class="mono">', "<caption>")
    body = body.replace('<p class="kein-kauf mono">', '<p class="kein-kauf">')
    body = re.sub(r'<h2>(.*?)</h2>', lambda m: f'<h2>{m.group(1)}</h2>', body)
    passend = "".join(G["produkt_karte"](K.set_by_id(s), best=K.set_by_id(s)["empfehlung"]) for s in sets)
    andere = [(k, v) for k, v in ARTIKEL.items() if k != key][:2]
    nachbar = "".join(f'<a class="karte fk" href="{k}.html" data-reveal style="--d:{i}"><div class="fk__bild"><img src="assets/{v[3]}" alt="{G["alt"](v[3])}" width="1200" height="800" loading="lazy"></div><div class="fk__body">{chip("Lesezeit " + lesezeit_von(partial(k)), "chip--rand")}<h3>{e(v[2])}</h3><span class="fk__mehr">Lesen{A}</span></div></a>' for i, (k, v) in enumerate(andere))
    t += f"""
<section class="artikel-kopf">
  <img src="assets/{bild}" alt="{G["alt"](bild)}" width="1400" height="933" fetchpriority="high">
  <div class="artikel-kopf__innen">
    <p class="brot"><a href="index.html">Start</a><span aria-hidden="true">/</span><a href="ratgeber.html">Ratgeber</a></p>
    <h1>{e(h1)}</h1>
    <div class="chips">{chip("Lesezeit " + lesezeit, "chip--hell")}</div>
  </div>
</section>
<section class="sec">
  <article class="artikel">{body}</article>
</section>
<section class="sec sec--cool" aria-label="Passende Sets">
  <div class="wrap">
    <div class="kopf2" data-reveal><h2>Passende Sets.</h2>{C.weg_schalter()}</div>
    <div class="produkte">{passend}</div>
  </div>
</section>
<section class="sec" aria-label="Weitere Ratgeber">
  <div class="wrap">
    <div class="kopf2" data-reveal><h2>Weitere Ratgeber.</h2><a class="btn btn--rand btn--klein" href="ratgeber.html">Alle Ratgeber{A}</a></div>
    <div class="karten karten--2">{nachbar}</div>
  </div>
</section>
{G["abschluss"]("Die Zahlen für Ihre Räume kommen aus der Besichtigung.", "Kostenfrei, mit schriftlichem Angebot.", ("Beratung anfragen", "kontakt.html"), ("Kühllast berechnen", "index.html#rechner"))}
"""
    return datei, t + S.fuss("voll")


# ============================================================================ FAQ

FAQ = [
    ("einbau", "Wie lange dauert der Einbau?", "Für eine Split-Anlage in der Regel ein Arbeitstag. Bei Multi-Split-Anlagen mit mehreren Innengeräten und längeren Leitungswegen können es zwei werden. Den genauen Rahmen nennen wir im Angebot."),
    ("kosten", "Was kostet die Besichtigung?", "Nichts. Besichtigung, Auslegung und das schriftliche Angebot sind kostenfrei und unverbindlich."),
    ("betrieb", "Kann eine Klimaanlage auch heizen?", "Ja. Jede Split-Anlage ist technisch eine Luft-Luft-Wärmepumpe und kann heizen. Im Frühjahr und Herbst ersetzt sie damit oft die Heizung; als alleinige Heizung im tiefen Winter ist sie nicht ausgelegt."),
    ("betrieb", "Wie laut ist so eine Anlage?", "Das Innengerät liegt im Wohnbereich typischerweise bei etwa 21 bis 27 dB(A) in der niedrigsten Stufe – leiser als ein Kühlschrank. Das Außengerät ist lauter; dessen Standort und Schallabstand legen wir bei der Besichtigung fest, mit Blick auf die Nachbarschaft."),
    ("recht", "Brauche ich die Zustimmung des Vermieters?", "Für eine Kernbohrung und ein Außengerät an der Fassade ja – es ist ein Eingriff in die Bausubstanz. Holen Sie sie schriftlich ein, bevor Sie sich für ein Set entscheiden. Ohne Zustimmung bleibt das mobile Gerät."),
    ("einbau", "Darf ich eine Klimaanlage selbst einbauen?", "Mobile Geräte und vorgefüllte Quick-Connect-Sets ja. Sobald ein Kältekreis geöffnet, evakuiert oder befüllt wird, greift die F-Gase-Verordnung (EU) 2024/573 und verlangt einen Sachkundenachweis."),
    ("betrieb", "Wie oft muss die Anlage gewartet werden?", "Im Wohnbereich einmal jährlich, am besten im Frühjahr. Anlagen im Dauerbetrieb zweimal. Für Anlagen ab einer bestimmten Kältemittelfüllmenge kommen wiederkehrende Dichtheitsprüfungen dazu."),
    ("betrieb", "Welches Kältemittel wird verwendet?", "In aktuellen Split-Anlagen überwiegend R-32 mit einem GWP von 675 – deutlich niedriger als das früher übliche R-410A. Mobile Monoblock-Geräte arbeiten häufig mit R-290 (Propan, GWP 3)."),
    ("betrieb", "Tropft die Anlage?", "Sie erzeugt Kondensat, das über einen Schlauch mit Gefälle abläuft. Wo kein Gefälle möglich ist, kommt eine Kondensatpumpe. Wasserflecken unter dem Innengerät haben fast immer mit dem Kondensatweg zu tun, nicht mit dem Gerät."),
    ("einbau", "Kühlt eine Anlage auch mehrere Räume?", "Ein einzelnes Innengerät kühlt einen Raum. Für mehrere Räume gibt es Multi-Split: ein Außengerät versorgt bis zu vier Innengeräte, jeder Raum bekommt seine eigene Temperatur."),
    ("einbau", "Was passiert mit meinem alten Gerät?", "Wir nehmen es zurück und führen es der fachgerechten Entsorgung zu. Kältemittel wird dabei abgesaugt und nicht in die Atmosphäre abgelassen."),
    ("betrieb", "Arbeiten Sie auch an Anlagen, die nicht von Ihnen sind?", "Ja, wir warten und reparieren auch Fremdanlagen. Nennen Sie uns Hersteller, Typ und ungefähres Baujahr vom Typenschild, dann bringen wir das Passende mit."),
    ("recht", "In welchem Gebiet arbeiten Sie?", "Gifhorn, Wolfsburg, Braunschweig, Peine, Salzgitter, Helmstedt und Umgebung – die PLZ-Region 38, daher der Name."),
    ("kosten", "Gibt es Förderung für eine Klimaanlage?", "Für reine Kühlung in der Regel nicht. Anders sieht es bei Maßnahmen an der Gebäudehülle und bei Heizungstechnik aus. Was für Ihr Gebäude infrage kommt, klären wir in der energetischen Beratung – verbindlich ist immer der aktuelle Stand des jeweiligen Programms."),
]
THEMEN = [("einbau", "Einbau"), ("betrieb", "Betrieb"), ("kosten", "Kosten"), ("recht", "Recht & Region")]


def faq(G):
    chip, A = G["chip"], G["ICON_ARROW"]
    datei = "faq.html"
    ld = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for _, q, a in FAQ]}
    t = S.kopf("Häufige Fragen zu Klimaanlagen | KlimaTech38",
               "Antworten zu Klimaanlagen: Einbaudauer, Lautstärke, Wartung, Kältemittel, Selbsteinbau und Mietwohnung. KlimaTech38, Gifhorn.", datei, ld)
    plus = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>'
    gruppen = ""
    for key, name in THEMEN:
        items = "".join(f'<details data-thema="{k}"><summary><span>{e(q)}</span>{plus}</summary><p>{e(a)}</p></details>' for k, q, a in FAQ if k == key)
        gruppen += f'<div class="faq__block" data-thema-block="{key}"><h2 class="faq__gruppe">{name}</h2>{items}</div>'
    themen = '<button type="button" aria-pressed="true" data-thema="alle">Alle 14</button>' + "".join(
        f'<button type="button" aria-pressed="false" data-thema="{k}">{n} ({sum(1 for x in FAQ if x[0] == k)})</button>' for k, n in THEMEN)
    t += f"""
<section class="fragen-kopf" aria-labelledby="seite-h">
  <div class="wrap">
    <h1 id="seite-h">Häufige Fragen.</h1>
    <p class="fragen-kopf__lead">14 Antworten – wenn Ihre Frage fehlt, rufen Sie an.</p>
    <div class="themen" id="themen" role="group" aria-label="Nach Thema filtern">{themen}</div>
  </div>
</section>
<section class="sec sec--eng sec--cool" aria-label="Fragen und Antworten">
  <div class="wrap"><div class="faq" id="faq">{gruppen}</div></div>
</section>
{G["abschluss"]("Ihre Frage ist nicht dabei.", "Anruf ist am schnellsten – oder Sie schreiben uns.", ("Beratung anfragen", "kontakt.html"), (C.TEL_TEXT + " anrufen", "tel:" + C.TEL))}
"""
    return datei, t + S.fuss("voll")


# ============================================================================ Kontakt

def kontakt(G):
    chip, A = G["chip"], G["ICON_ARROW"]
    datei = "kontakt.html"
    ld = {"@context": "https://schema.org", "@type": "ContactPage", "name": "Kontakt KlimaTech38", "url": f"{DOMAIN}/{datei}",
          "mainEntity": {"@id": f"{DOMAIN}/#business"}}
    t = S.kopf("Kontakt – KlimaTech38, InTroTech GmbH Gifhorn",
               "KlimaTech38, InTroTech GmbH: Zeisigweg 4, 38518 Gifhorn. Telefon 05371 8759972, Mo–Fr 8–18 Uhr. Terminanfrage für Klimaanlage und Energieausweis.", datei, ld)
    themen = ["Klimaanlage: Beratung", "Klimaanlage: Auslegung", "Klimaanlage: Set anfragen", "Klimaanlage: Wartung",
              "Energieausweis Wohnhaus", "Energieausweis Gewerbe", "Energetische Beratung"]
    opts = "".join(f'<option>{e(x)}</option>' for x in themen)
    t += G["kontakt_vollbild"](als_h1=True, titel="Kontakt. <em>Anruf, WhatsApp oder Rückruf.</em>")
    t += f"""
<section class="sec" aria-labelledby="form-h">
  <div class="wrap">
    <div class="form-split">
      <form class="karte form" id="anfrage" novalidate style="padding:var(--s4)">
        <div><h2 id="form-h">Sagen Sie uns, <em>was wir uns ansehen sollen.</em></h2><p style="color:var(--ink-mute);font-size:var(--fs-1);margin-top:.4rem">Pflichtfelder sind nur Name und Telefonnummer.</p></div>
        <div class="bezug" id="bezug" hidden><div><small>Ihr Bezug</small><b id="bezug-text"></b></div><button type="button" id="bezug-weg">Entfernen</button></div>
        <div class="f--2">
          <p class="f"><label for="f-name">Name *</label><input id="f-name" name="name" type="text" autocomplete="name" required></p>
          <p class="f"><label for="f-tel">Telefon *</label><input id="f-tel" name="telefon" type="tel" autocomplete="tel" required></p>
        </div>
        <div class="f--2">
          <p class="f"><label for="f-mail">E-Mail</label><input id="f-mail" name="email" type="email" autocomplete="email"></p>
          <p class="f"><label for="f-ort">Ort</label><input id="f-ort" name="ort" type="text" autocomplete="address-level2" placeholder="z. B. Gifhorn"></p>
        </div>
        <div class="f"><span class="f__label">Welcher Weg?</span>{C.weg_schalter()}</div>
        <p class="f"><label for="f-thema">Worum geht es?</label><select id="f-thema" name="thema">{opts}</select></p>
        <fieldset class="zeitfenster"><legend>Wann sollen wir zurückrufen?</legend>
          <div class="zeitfenster__opt">
            <label><input type="radio" name="zeit" value="egal" checked><b>Egal</b><small>Mo–Fr 08–18 Uhr</small></label>
            <label><input type="radio" name="zeit" value="vormittags"><b>Vormittags</b><small>08–12 Uhr</small></label>
            <label><input type="radio" name="zeit" value="nachmittags"><b>Nachmittags</b><small>12–18 Uhr</small></label>
          </div>
        </fieldset>
        <p class="f"><label for="f-text">Nachricht</label><textarea id="f-text" name="nachricht" placeholder="Welche Räume, wie groß, welches Geschoss – und was Sie sich vorstellen."></textarea></p>
        <p class="f-check"><input id="f-ds" type="checkbox" required><label for="f-ds">Ich habe die <a href="datenschutz.html">Datenschutzerklärung</a> gelesen und bin mit der Verarbeitung meiner Angaben zur Bearbeitung der Anfrage einverstanden.</label></p>
        <p class="btns"><button type="submit" class="btn btn--primary btn--gross">Anfrage senden{A}</button></p>
        <p class="form__meldung" id="form-meldung" hidden></p>
      </form>
      <aside class="karte karte--cool seite-karte" data-reveal>
        <h3>Wen Sie erreichen</h3>
        <p style="color:var(--ink-soft)">KlimaTech38 ist der Geschäftsbereich Klima und Energie der InTroTech GmbH.</p>
        <ul class="daten">
          <li><b>Anschrift</b><span>InTroTech GmbH · Zeisigweg 4 · 38518 Gifhorn</span></li>
          <li><b>Telefon</b><span><a href="tel:{C.TEL}">{C.TEL_TEXT}</a> · Mo–Fr 08–18 Uhr</span></li>
          <li><b>E-Mail</b><span><a href="mailto:{C.MAIL}">{C.MAIL}</a></span></li>
          <li><b>WhatsApp</b><span><a href="{C.WA}" target="_blank" rel="noopener">Fotos vom Raum direkt schicken</a></span></li>
          <li><b>Geschäftsführung</b><span>Johann Warkentin, Jonathan Mangold, Adrian Mangold</span></li>
          <li><b>Einzugsgebiet</b><span>Gifhorn, Wolfsburg, Braunschweig, Peine, Salzgitter, Helmstedt und Umgebung</span></li>
        </ul>
        <div class="chips">{chip("dena-Energieberater")}{chip("TÜV-zertifizierter Fachbetrieb")}</div>
        <p class="demo-hinweis">{G["ICON_INFO"]}<span>Abholung von Sets am Zeisigweg 4 nach Terminabsprache. Besichtigung und Angebot sind kostenfrei.</span></p>
      </aside>
    </div>
  </div>
</section>
"""
    return datei, t + S.fuss("schlank")


# ============================================================================ Recht

def recht(G, key):
    titel = {"impressum": "Impressum – KlimaTech38 / InTroTech GmbH", "datenschutz": "Datenschutzerklärung – KlimaTech38 / InTroTech GmbH"}[key]
    desc = {"impressum": "Impressum der InTroTech GmbH, Zeisigweg 4, 38518 Gifhorn – Anbieter von KlimaTech38.",
            "datenschutz": "Datenschutzerklärung für klimatech38.de – Verantwortlicher, Server-Logfiles, Kontaktformular, Karte, Ihre Rechte."}[key]
    body = partial(key)
    body = body.replace('<p class="mono lese-sub">', '<p class="lese-sub">').replace('class="mono"', "")
    t = S.kopf(titel, desc, f"{key}.html")
    t += body
    return f"{key}.html", t + S.fuss("schlank", produkte=True)


def alle(G):
    out = [klimaanlagen(G), beratung(G), montage(G), wartung(G), energetische_beratung(G), ratgeber_index(G)]
    out += [ratgeber_artikel(G, k) for k in ARTIKEL]
    out += [faq(G), kontakt(G), recht(G, "impressum"), recht(G, "datenschutz")]
    return out
