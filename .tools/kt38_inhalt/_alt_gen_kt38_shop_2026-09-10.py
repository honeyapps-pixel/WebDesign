#!/usr/bin/env python3
"""gen_kt38_shop.py — erzeugt aus .tools/kt38_katalog.py den kompletten Katalog.

Ausgabe (alles gewoehnliches, statisches HTML — im Deploy laeuft KEIN Build):
    klimatech38/assets/produkte.js      Datenschicht für Rechner und Filter
    klimatech38/shop-*.html             4 Kategorieseiten mit Facettenfilter
    klimatech38/set-*.html              9 Set-Seiten mit Product-JSON-LD
    klimatech38/sitemap.xml             alle Seiten

Warum ein Generator und keine Handarbeit: der alte Zustand hatte die Navigation
7x kopiert. Bei 26 Seiten und einem Katalog, dessen Preise sich aendern, ist das
nicht mehr pflegbar. Kopf und Fuss kommen aus kt38_chrome.py, die Daten aus
kt38_katalog.py — jede Zahl steht genau einmal.

Aufruf:  python3 .tools/gen_kt38_shop.py [--check]
"""
import html
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kt38_katalog as K
import kt38_chrome as C

SITE = Path(__file__).resolve().parent.parent / "klimatech38"
DOMAIN = "https://klimatech38.de"


def e(s):
    return html.escape(str(s), quote=True)


def zahl(n):
    """Deutsche Tausendertrennung — f"{n:,}" liefert englische Kommas."""
    return f"{n:,}".replace(",", ".")


def preis(cent, klasse="preis"):
    """Preis mit Demo-Kennzeichnung. Die Kennzeichnung haengt an META['demo'] —
       eine Stelle, ein Schalter."""
    if cent is None:
        return ""
    txt = f'<b class="{klasse}">{e(K.eur(cent))}</b>'
    if K.META["demo"]:
        txt += f'<span class="preis-demo mono">{e(K.META["demoWort"])}</span>'
    return txt


# --------------------------------------------------------------------- Schemata
# Eigene Strichzeichnungen statt Produktfotos: ein Foto eines fremden Geräts waere
# ein fremdes Lichtbild mit fremdem Herstellerlogo. Die Zeichnung gehoert uns.

def schema_svg(art, klasse="set-schema"):
    if art == "mono":
        inner = ('<rect x="14" y="34" width="34" height="44" rx="2"/>'
                 '<path d="M20 44h22M20 50h22" class="thin"/><circle cx="31" cy="66" r="6"/>'
                 '<path class="leit" d="M48 42c26 0 22-22 44-22"/>'
                 '<rect x="92" y="8" width="26" height="24" rx="1.5"/><path d="M105 8v24" class="thin"/>')
        label = "Schema: mobiles Monoblock-Gerät mit Abluftschlauch durch das Fenster"
    elif art == "split1":
        inner = ('<rect x="8" y="31" width="30" height="26" rx="2"/>'
                 '<circle cx="23" cy="44" r="8"/><circle cx="23" cy="44" r="1.6" class="fill"/>'
                 '<path class="leit" d="M38 44h48"/>'
                 '<rect x="86" y="37" width="36" height="15" rx="1.5"/><path d="M90 49h28" class="thin"/>')
        label = "Schema: ein Außengerät versorgt ein Innengerät"
    else:
        n = int(art[-1])                       # multi2 / multi3 / multi4
        ys = {2: [14, 58], 3: [6, 37, 68], 4: [4, 27, 50, 73]}[n]
        pfade, kaesten = [], []
        for y in ys:
            mitte = y + 6
            pfade.append(f"M62 44V{mitte}h24")
            kaesten.append(f'<rect x="86" y="{y}" width="36" height="12" rx="1.5"/>'
                           f'<path d="M90 {y + 9}h28" class="thin"/>')
        inner = ('<rect x="8" y="31" width="30" height="26" rx="2"/>'
                 '<circle cx="23" cy="44" r="8"/><circle cx="23" cy="44" r="1.6" class="fill"/>'
                 f'<path class="leit" d="M38 44h24{"".join(pfade)}"/>' + "".join(kaesten))
        label = f"Schema: ein Außengerät versorgt {n} Innengeräte"
    return (f'<svg class="{klasse}" viewBox="0 0 132 88" role="img" aria-label="{e(label)}">'
            f'<g class="sch-g">{inner}</g></svg>')


def kw_marke(kw, klasse="kw-marke"):
    """Die kW-Skala der Signature als Produktmarke: dieselbe Haarlinie wie im Kopf und
       im Rechner, gefuellt bis zur Leistung des Sets.

       EINE Skala fuer alle Sets, Vollausschlag 10 kW — identisch mit dem Rechner.
       Ein frueherer Versuch skalierte die mobilen Geraete auf 4 kW, damit 2,0 und 2,6 kW
       weiter auseinanderliegen. Das war falsch: 2,0 kW und 5,0 kW bekamen denselben
       Balken. Eine Datengrafik mit zwei Skalen luegt, auch wenn die Absicht gut war.
       Die genaue Leistung steht ohnehin als Zahl daneben."""
    anteil = min(1.0, kw / 10.0)
    return (f'<p class="{klasse}"><span class="kw-marke-l" aria-hidden="true">'
            f'<span style="transform:scaleX({anteil:.3f})"></span></span>'
            f'<span class="mono">{str(kw).replace(".", ",")} kW'
            f'<span class="kw-marke-voll mono">/ 10 kW</span></span></p>')


# --------------------------------------------------------------------- Bausteine

def set_zeile(s):
    """Tragende Bauform: die Spec-ZEILE (Struktur-Blueprint), kein Kartenraster."""
    k = K.set_by_id(s["id"])
    daten = " ".join([
        f'data-id="{e(s["id"])}"', f'data-kat="{e(s["kategorie"])}"', f'data-kw="{s["kw"]}"',
        f'data-fl-von="{s["flaecheVon"]}"', f'data-fl-bis="{s["flaecheBis"]}"',
        f'data-raeume="{s["innengeraete"]}"',
        f'data-selbst="{1 if s["selbsteinbau"] else 0}"',
        f'data-preis="{s["preise"]["abholung_cent"]}"',
    ])
    montiert = ""
    if s["preise"]["montage_cent"]:
        montiert = (f'<span class="set-p2">montiert ab {e(K.eur(s["preise"]["montage_cent"]))}</span>')
    else:
        montiert = '<span class="set-p2">Selbsteinbau – keine Montage nötig</span>'

    return f"""        <li class="set-zeile" {daten}>
          <div class="set-bild">{schema_svg(s["schema"])}{kw_marke(s["kw"])}</div>
          <div class="set-haupt">
            <p class="mono set-kenn">{e(s["kategorie"].upper())} · {e(str(s["kw"]).replace(".", ","))} kW · {zahl(K.btu(s["kw"]))} BTU/h</p>
            <h3><a href="set-{e(s["id"])}.html">{e(s["titel"])}</a></h3>
            <p class="set-kurz">{e(s["kurz"])}</p>
            {kw_marke(s["kw"])}
          </div>
          <dl class="spec set-spec">
            <div><dt class="mono">Raumgröße</dt><dd>{s["flaecheVon"]}–{s["flaecheBis"]} m²</dd></div>
            <div><dt class="mono">Räume</dt><dd>{s["innengeraete"]}</dd></div>
            <div><dt class="mono">Kältemittel</dt><dd>{e(s["kaeltemittel"])}</dd></div>
            <div><dt class="mono">Selbsteinbau</dt><dd>{"möglich" if s["selbsteinbau"] else "nein – durch uns"}</dd></div>
          </dl>
          <div class="set-preis">
            <p class="mono set-p-k">Abholung</p>
            {preis(s["preise"]["abholung_cent"])}
            {montiert}
          </div>
          <div class="set-akt">
            <a class="btn btn-primary btn-sm" href="set-{e(s["id"])}.html">Set ansehen</a>
          </div>
        </li>"""


def set_kachel(s):
    """Sekundaerbauform, max. 3 nebeneinander: keine Fuellflaeche, kein Schatten,
       kein Hover-Lift. Reihenfolge = Datenreihenfolge."""
    montiert = (f'<span class="set-p2">montiert ab {e(K.eur(s["preise"]["montage_cent"]))}</span>'
                if s["preise"]["montage_cent"] else
                '<span class="set-p2">Selbsteinbau</span>')
    return f"""      <li class="set-kachel">
        <p class="mono set-kenn">{e(s["kategorie"].upper())} · {e(str(s["kw"]).replace(".", ","))} kW</p>
        <div class="set-kachel-bild">{schema_svg(s["schema"])}{kw_marke(s["kw"])}</div>
        <h3><a href="set-{e(s["id"])}.html">{e(s["titel"])}</a></h3>
        <dl class="spec">
          <div><dt class="mono">Raumgröße</dt><dd>{s["flaecheVon"]}–{s["flaecheBis"]} m²</dd></div>
          <div><dt class="mono">Räume</dt><dd>{s["innengeraete"]}</dd></div>
          <div><dt class="mono">Einbau</dt><dd>{"selbst möglich" if s["selbsteinbau"] else "durch uns"}</dd></div>
        </dl>
        <div class="set-preis">
          <p class="mono set-p-k">Abholung</p>
          {preis(s["preise"]["abholung_cent"])}
          {montiert}
        </div>
        <a class="set-mehr" href="set-{e(s["id"])}.html">Set ansehen<span aria-hidden="true">→</span></a>
      </li>"""


def demo_band():
    if not K.META["demo"]:
        return ""
    return f"""<div class="demo-band band">
  <div class="wrap">
    <p class="mono">Hinweis zur Vorschau</p>
    <p>{K.META["demoHinweis"]}</p>
  </div>
</div>"""


def kein_kauf():
    return f"""      <p class="kein-kauf mono">{e(K.META["keinKaufHinweis"])}</p>"""


# --------------------------------------------------------------------- Seitenrahmen

def robots_wert():
    """Solange Beispielpreise stehen, darf die Seite NICHT indexiert werden — sonst
       landen Demo-Preise als Preise des Betriebs in der Suche, und das Canonical
       zeigt dabei auch noch auf die echte Domain. Haengt am selben Schalter."""
    return "noindex, nofollow" if K.META["demo"] else "index, follow, max-image-preview:large"


def head(titel, beschreibung, datei, jsonld=None, og_bild="assets/hero.jpg"):
    demo_attr = ' data-preis-demo' if K.META["demo"] else ""
    ld = ""
    if jsonld:
        ld = ('<script type="application/ld+json">\n'
              + json.dumps(jsonld, ensure_ascii=False, indent=2, sort_keys=False)
              + "\n</script>\n")
    return f"""<!DOCTYPE html>
<html lang="de" data-motion="mechanical"{demo_attr}>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script>document.documentElement.classList.add('anim')</script>
<title>{e(titel)}</title>
<meta name="description" content="{e(beschreibung)}">
<meta name="author" content="InTroTech GmbH">
<meta name="robots" content="{robots_wert()}">
<link rel="canonical" href="{DOMAIN}/{datei}">
<meta name="geo.region" content="DE-NI">
<meta name="geo.placename" content="Gifhorn">
<meta property="og:type" content="website">
<meta property="og:url" content="{DOMAIN}/{datei}">
<meta property="og:site_name" content="KlimaTech38">
<meta property="og:locale" content="de_DE">
<meta property="og:title" content="{e(titel)}">
<meta property="og:description" content="{e(beschreibung)}">
<meta property="og:image" content="{DOMAIN}/{og_bild}">
<meta property="og:image:alt" content="Innengerät einer Split-Klimaanlage in einem hellen Wohnraum">
<meta name="theme-color" content="#10303F">
<link rel="icon" type="image/png" href="assets/brand/mark.png">
<link rel="apple-touch-icon" href="assets/brand/mark.png">
<link rel="stylesheet" href="styles.css">
{ld}</head>
<body>
<a class="skip" href="#inhalt">Zum Inhalt springen</a>

<!-- KT38:HEADER:START -->
<!-- KT38:HEADER:END -->

<main id="inhalt">
"""


WA_FAB = """<a class="wa-fab" href="https://wa.me/4953718759972" target="_blank" rel="noopener" aria-label="Per WhatsApp schreiben">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#fff" d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.885-9.886 9.885M20.52 3.449C18.24 1.245 15.24 0 12.045 0 5.463 0 .104 5.359.101 11.945c0 2.096.549 4.14 1.595 5.945L0 24l6.335-1.652a11.96 11.96 0 005.71 1.454h.006c6.585 0 11.946-5.359 11.949-11.945a11.86 11.86 0 00-3.495-8.411z"/></svg>
  <span class="wa-fab__pulse" aria-hidden="true"></span>
</a>"""


def tail(motion="voll", produkte=True):
    """motion='schlank' laesst GSAP/ScrollTrigger/Lenis weg (rund 130 KB Parse-Arbeit).
       assets/motion.js hat dafuer einen Fallback-Pfad und macht die Reveals sichtbar."""
    js = []
    if motion == "voll":
        js += ['<script src="assets/js/gsap.min.js"></script>',
               '<script src="assets/js/ScrollTrigger.min.js"></script>',
               '<script src="assets/js/lenis.min.js"></script>']
    js.append('<script src="assets/motion.js"></script>')
    if produkte:
        js.append('<script src="assets/produkte.js"></script>')
    js.append('<script src="script.js"></script>')
    return f"""
</main>

<!-- KT38:FOOTER:START -->
<!-- KT38:FOOTER:END -->

{WA_FAB}

{chr(10).join(js)}
</body>
</html>
"""


# --------------------------------------------------------------------- produkte.js

def schreibe_produkte_js():
    daten = {
        "meta": K.META,
        "kategorien": [{k: v for k, v in kat.items() if k != "lead"} for kat in K.KATEGORIEN],
        "sets": [dict(s, btu=K.btu(s["kw"])) for s in K.SETS],
        "zubehoer": K.ZUBEHOER,
    }
    js = f"""/* ============================================================================
   assets/produkte.js — GENERIERT aus .tools/kt38_katalog.py.
   NICHT VON HAND AENDERN: `python3 .tools/gen_kt38_shop.py` ueberschreibt die Datei.
   Preise pflegen: .tools/kt38_katalog.py, dort auch META.demo umschalten.
   ========================================================================== */
window.KT38 = {json.dumps(daten, ensure_ascii=False, indent=2)};

/* Eine Darstellungsregel für Geld — spiegelt kt38_katalog.eur() */
window.KT38.eur = function (cent) {{
  if (cent === null || cent === undefined) {{ return ''; }}
  return (cent / 100).toLocaleString('de-DE', {{
    style: 'currency', currency: 'EUR', minimumFractionDigits: 2
  }});
}};

/* Demo-Kennzeichnung auch für handgeschriebene Seiten, die der Generator nicht kennt */
if (window.KT38.meta.demo) {{ document.documentElement.dataset.preisDemo = '1'; }}
"""
    (SITE / "assets" / "produkte.js").write_text(js, encoding="utf-8")
    return "assets/produkte.js"


# --------------------------------------------------------------------- Kategorieseiten

def facetten_form(kat):
    """Facetten als Checkbox-Gruppen: mehrfachwaehlbar und tastaturbedienbar,
       anders als ein <select>. UND zwischen Gruppen, ODER innerhalb einer Gruppe."""
    if kat["id"] == "zubehoer":
        return ""
    sets = K.sets_der_kategorie(kat["id"])
    zeigt_raeume = kat["id"] == "multi"
    gruppen = []

    gruppen.append(("flaeche", "Raumgröße", [
        ("bis-25", "bis 25 m²"), ("25-40", "25 – 40 m²"),
        ("40-60", "40 – 60 m²"), ("ab-60", "über 60 m²"),
    ]))
    if zeigt_raeume:
        gruppen.append(("raeume", "Räume", [("2", "2 Räume"), ("3", "3 Räume"), ("4", "4 Räume")]))
    if any(s["selbsteinbau"] for s in sets) and not all(s["selbsteinbau"] for s in sets):
        gruppen.append(("selbst", "Einbau", [("1", "Selbsteinbau möglich"), ("0", "Einbau durch uns")]))
    gruppen.append(("preis", "Preisrahmen (Abholung)", [
        ("bis-999", "bis 999 €"), ("1000-1999", "1.000 – 1.999 €"), ("ab-2000", "ab 2.000 €"),
    ]))

    teile = []
    for gid, label, werte in gruppen:
        felder = "".join(
            f'<label><input type="checkbox" data-f="{gid}" value="{v}"><span>{e(t)}</span></label>'
            for v, t in werte)
        teile.append(f'<fieldset class="fac-g"><legend class="mono">{e(label)}</legend>'
                     f'<div class="fac-w">{felder}</div></fieldset>')

    return f"""    <form class="facetten" id="facetten">
      <div class="fac-in">
{chr(10).join("        " + t for t in teile)}
      </div>
      <div class="fac-fuss">
        <p class="mono fac-treffer" id="fac-treffer" aria-live="polite" role="status"></p>
        <button type="button" class="fac-reset" id="fac-reset" hidden>Filter zurücksetzen</button>
      </div>
    </form>"""


def zubehoer_zeilen():
    zeilen = []
    for z in K.ZUBEHOER:
        passt = ", ".join(K.set_by_id(i)["titel"] for i in z["passendZu"][:3] if K.set_by_id(i))
        if len(z["passendZu"]) > 3:
            passt += " u. a."
        zeilen.append(f"""        <li>
          <span class="reg-a">{e(z["titel"])}</span>
          <span class="reg-b">{e(z["zweck"])}
            <span class="zub-passt mono">Passend zu: {e(passt)}</span></span>
          <span class="reg-c">{preis(z["preis_cent"])}</span>
        </li>""")
    return "\n".join(zeilen)


def kategorieseite(kat):
    sets = K.sets_der_kategorie(kat["id"])
    datei = kat["datei"]

    ld = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": kat["titel"],
        "description": kat["lead"][:180],
        "numberOfItems": len(sets),
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": s["titel"],
             "url": f"{DOMAIN}/set-{s['id']}.html"}
            for i, s in enumerate(sets)
        ],
    }

    t = head(f'{kat["kurz"]} – Preise & Auslegung | KlimaTech38',
             f'{kat["kurz"]} von KlimaTech38 in Gifhorn: Leistung, Raumgröße, Lieferumfang und '
             f'Preis für Abholung oder Montage.',
             datei, ld)

    t += demo_band()

    t += f"""
<section class="kopf-kat">
  <div class="wrap">
    <nav class="brot mono" aria-label="Brotkrumen">
      <a href="index.html">Start</a><span aria-hidden="true">/</span>
      <a href="shop.html">Sets &amp; Preise</a><span aria-hidden="true">/</span>
      <span aria-current="page">{e(kat["kurz"])}</span>
    </nav>
    <h1>{e(kat["frage"])}</h1>
    <p class="mono ans">→ {e(kat["antwort"])}</p>
    <p class="kat-lead">{e(kat["lead"])}</p>
{kein_kauf()}
  </div>
</section>
"""

    if kat["id"] == "zubehoer":
        t += f"""
<section class="sec sec-klima">
  <div class="wrap">
    <header class="sec-head">
      <h2>Was zusätzlich gebraucht wird</h2>
      <p class="mono ans">→ Wenn wir montieren, steht das Passende im Angebot</p>
    </header>
    <ul class="register register-k register-preis">
{zubehoer_zeilen()}
    </ul>
    <p class="preis-fuss mono">{e(K.META["preisFuss"])}</p>
    <p class="abschluss-cta">
      <a class="btn btn-primary" href="tel:+4953718759972">05371 8759972 anrufen</a>
      <a class="btn btn-ghost" href="kontakt.html">Zubehör anfragen</a>
    </p>
  </div>
</section>
"""
    else:
        t += f"""
<section class="sec sec-klima" id="katalog-sec">
  <div class="wrap">
    <header class="sec-head">
      <h2>{e(kat["titel"])}</h2>
      <p class="mono ans">→ {len(sets)} Sets, jeweils mit Preis für Abholung und mit Montage</p>
    </header>
{facetten_form(kat)}
    <ul class="set-liste" id="katalog">
{chr(10).join(set_zeile(s) for s in sets)}
      <li class="set-leer" id="set-leer" hidden>
        <p>Zu dieser Auswahl passt kein Set. Setzen Sie einen Filter zurück – oder rufen Sie an,
          dann legen wir die Anlage direkt für Ihre Räume aus.</p>
        <a class="btn btn-primary btn-sm" href="tel:+4953718759972">05371 8759972</a>
      </li>
    </ul>
    <p class="preis-fuss mono">{e(K.META["preisFuss"])}</p>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <header class="sec-head">
      <h2>Unsicher, welche Leistung passt?</h2>
      <p class="mono ans">→ Der Rechner fragt Ihre Räume ab und filtert diese Liste vor</p>
    </header>
    <p class="hinweis">Die Raumgröße allein reicht nicht: Dämmstandard, Geschoss und die Größe der
      Süd-&nbsp;oder Westfenster verschieben die Kühllast erheblich. Der Auslegungs-Rechner nimmt das
      auf und nennt Ihnen die nötige Leistung in kW.</p>
    <p class="abschluss-cta">
      <a class="btn btn-primary" href="shop.html#rechner">Kühllast berechnen</a>
      <a class="btn btn-ghost" href="beratung.html">Lieber beraten lassen</a>
    </p>
  </div>
</section>
"""

    t += tail(motion="voll", produkte=True)
    return datei, t


# --------------------------------------------------------------------- Set-Seiten

def setseite(s):
    datei = f"set-{s['id']}.html"
    kat = next(k for k in K.KATEGORIEN if k["id"] == s["kategorie"])

    # Product-JSON-LD OHNE `offers`, solange die Preise Demo sind: sonst landen
    # Beispielpreise in den Rich Results und bleiben dort im Cache stehen.
    ld = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": s["titel"],
        "description": s["kurz"],
        "category": kat["titel"],
        "additionalProperty": [
            {"@type": "PropertyValue", "name": "Kühlleistung", "value": f'{s["kw"]} kW'},
            {"@type": "PropertyValue", "name": "Raumgröße",
             "value": f'{s["flaecheVon"]}–{s["flaecheBis"]} m²'},
            {"@type": "PropertyValue", "name": "Innengeräte", "value": s["innengeraete"]},
            {"@type": "PropertyValue", "name": "Kältemittel", "value": s["kaeltemittel"]},
        ],
        "brand": {"@type": "Brand", "name": "KlimaTech38"},
        "seller": {"@id": f"{DOMAIN}/#business"},
    }
    if not K.META["demo"]:
        ld["offers"] = {
            "@type": "Offer", "priceCurrency": "EUR",
            "price": f'{s["preise"]["abholung_cent"] / 100:.2f}',
            "availability": "https://schema.org/InStock",
            "seller": {"@id": f"{DOMAIN}/#business"},
        }

    brot = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Start", "item": f"{DOMAIN}/"},
            {"@type": "ListItem", "position": 2, "name": "Sets & Preise", "item": f"{DOMAIN}/shop.html"},
            {"@type": "ListItem", "position": 3, "name": kat["kurz"], "item": f"{DOMAIN}/{kat['datei']}"},
            {"@type": "ListItem", "position": 4, "name": s["titel"], "item": f"{DOMAIN}/{datei}"},
        ],
    }

    t = head(f'{s["titel"]} – Preis & Daten | KlimaTech38',
             f'{s["titel"]}: {s["kw"]} kW für {s["flaecheVon"]}–{s["flaecheBis"]} m². '
             f'Lieferumfang, Kältemittel {s["kaeltemittel"]}, Preis für Abholung oder mit Montage. '
             f'KlimaTech38, Gifhorn.',
             datei, [ld, brot])

    t += demo_band()

    lieferung = "".join(f"<li>{e(x)}</li>" for x in s["lieferumfang"])
    nicht = "".join(f"<li>{e(x)}</li>" for x in s["nichtEnthalten"])

    montage_block = ""
    if s["preise"]["montage_cent"]:
        montage_block = f"""        <div class="pv-wahl">
          <p class="mono pv-k">Mit Montage durch uns</p>
          {preis(s["preise"]["montage_cent"], "preis preis-gross")}
          <p class="pv-satz">Enthält {e(s["montageUmfang"])}.</p>
          <button class="btn btn-primary" type="button" data-anfrage="{e(s["id"])}" data-variante="montage">
            Mit Montage anfragen</button>
        </div>"""
    else:
        montage_block = f"""        <div class="pv-wahl pv-wahl-aus">
          <p class="mono pv-k">Mit Montage</p>
          <p class="pv-satz">Ein mobiles Gerät wird nicht montiert – Sie stellen es auf, führen den
            Abluftschlauch nach draußen und stecken es ein.</p>
        </div>"""

    hinweis = f'\n    <p class="set-hinweis">{e(s["hinweis"])}</p>' if s["hinweis"] else ""

    zub = [K.zubehoer_by_id(z) for z in s["zubehoer"]]
    zub_zeilen = "".join(
        f'<li><span class="reg-a">{e(z["titel"])}</span>'
        f'<span class="reg-b">{e(z["zweck"])}</span>'
        f'<span class="reg-c">{preis(z["preis_cent"])}</span></li>'
        for z in zub if z)

    t += f"""
<section class="kopf-set">
  <div class="wrap">
    <nav class="brot mono" aria-label="Brotkrumen">
      <a href="index.html">Start</a><span aria-hidden="true">/</span>
      <a href="shop.html">Sets &amp; Preise</a><span aria-hidden="true">/</span>
      <a href="{e(kat["datei"])}">{e(kat["kurz"])}</a><span aria-hidden="true">/</span>
      <span aria-current="page">{e(s["titel"])}</span>
    </nav>

    <div class="set-kopf">
      <div class="set-kopf-bild">{schema_svg(s["schema"], "set-schema set-schema-gross")}{kw_marke(s["kw"], "kw-marke kw-marke-gross")}</div>
      <div class="set-kopf-txt">
        <h1>{e(s["titel"])}</h1>
        <p class="mono ans">→ {e(s["bauform"])} · {e(str(s["kw"]).replace(".", ","))} kW · {zahl(K.btu(s["kw"]))} BTU/h</p>
        <p class="set-lead">{e(s["kurz"])} Ausgelegt für Räume von
          <b>{s["flaecheVon"]} bis {s["flaecheBis"]} m²</b>.</p>{hinweis}
      </div>
    </div>
  </div>
</section>

<section class="sec sec-klima" id="preis">
  <div class="wrap">
    <header class="sec-head">
      <h2>Was kostet dieses Set?</h2>
      <p class="mono ans">→ Zwei Wege: selbst abholen und einbauen – oder einbauen lassen</p>
    </header>

    <div class="preis-wahl">
      <div class="pv-wahl">
        <p class="mono pv-k">Abholung in Gifhorn</p>
        {preis(s["preise"]["abholung_cent"], "preis preis-gross")}
        <p class="pv-satz">{"Anschluss über Schnellkupplung – der Kältekreis bleibt geschlossen, Sie dürfen das selbst machen." if s["selbsteinbau"] else "Nur als Material – den Anschluss übernehmen wir, der Kältekreis muss vakuumiert werden."}</p>
        <button class="btn btn-ghost" type="button" data-anfrage="{e(s["id"])}" data-variante="abholung">
          Zur Abholung anfragen</button>
      </div>
{montage_block}
    </div>
{kein_kauf()}
    <p class="preis-fuss mono">{e(K.META["preisFuss"])}</p>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <header class="sec-head">
      <h2>Was steckt drin?</h2>
      <p class="mono ans">→ Lieferumfang und die harten Werte</p>
    </header>

    <div class="set-detail">
      <div class="set-detail-sp">
        <p class="mono sd-k">Im Set enthalten</p>
        <ul class="sd-liste">{lieferung}</ul>
        <p class="mono sd-k sd-k2">Nicht enthalten</p>
        <ul class="sd-liste sd-liste-aus">{nicht}</ul>
      </div>
      <div class="set-detail-sp">
        <p class="mono sd-k">Technische Werte</p>
        <table class="tab">
          <tbody>
            <tr><th scope="row">Kühlleistung</th><td data-l="Kühlleistung">{e(str(s["kw"]).replace(".", ","))} kW · {zahl(K.btu(s["kw"]))} BTU/h</td></tr>
            {"<tr><th scope='row'>Heizleistung</th><td data-l='Heizleistung'>" + str(s["kwHeizen"]).replace(".", ",") + " kW</td></tr>" if s["kwHeizen"] else ""}
            <tr><th scope="row">Raumgröße</th><td data-l="Raumgröße">{s["flaecheVon"]}–{s["flaecheBis"]} m²</td></tr>
            <tr><th scope="row">Innengeräte</th><td data-l="Innengeräte">{s["innengeraete"]}</td></tr>
            <tr><th scope="row">Kältemittel</th><td data-l="Kältemittel">{e(s["kaeltemittel"])} (GWP {s["gwp"]})</td></tr>
            {"<tr><th scope='row'>Schalldruck innen</th><td data-l='Schalldruck innen'>" + str(s["schallInnen_dbA"]) + " dB(A)</td></tr>" if s["schallInnen_dbA"] else ""}
            {"<tr><th scope='row'>Schalldruck außen</th><td data-l='Schalldruck außen'>" + str(s["schallAussen_dbA"]) + " dB(A)</td></tr>" if s["schallAussen_dbA"] else ""}
            <tr><th scope="row">Anschluss</th><td data-l="Anschluss">{e(s["anschlussart"])}</td></tr>
          </tbody>
        </table>
        <p class="sd-fuss mono">Heizleistung, Schalldruck, Effizienzklasse, SEER und SCOP nennen wir,
          sobald das konkrete Gerät feststeht – sie gehören zum Modell, nicht zur Bauart. Die hier genannten
          Leistungswerte beschreiben die Auslegung, nicht ein bestimmtes Fabrikat; der GWP ist eine
          Eigenschaft des Kältemittels.</p>
      </div>
    </div>
  </div>
</section>

{"" if not zub_zeilen else f'''<section class="sec">
  <div class="wrap">
    <header class="sec-head">
      <h2>Was brauchen Sie eventuell dazu?</h2>
      <p class="mono ans">→ Hängt am Aufstellort – wir sagen Ihnen vorher, was nötig ist</p>
    </header>
    <ul class="register register-k register-preis">{zub_zeilen}</ul>
  </div>
</section>'''}

<section class="sec sec-klima">
  <div class="wrap">
    <header class="sec-head">
      <h2>Wie geht es weiter?</h2>
      <p class="mono ans">→ Sie fragen an, wir melden uns mit einem schriftlichen Angebot</p>
    </header>
    <ol class="steps">
      <li><span class="mono">01</span><b>Anfragen</b><span>Set anfragen oder anrufen – mit Raumgröße, Geschoss und Baujahr.</span></li>
      <li><span class="mono">02</span><b>Besichtigen</b><span>Wir sehen uns die Räume an: Leitungsweg, Außengerät-Standort, Kondensat. Kostenfrei.</span></li>
      <li><span class="mono">03</span><b>Angebot</b><span>Schriftlich und unverbindlich, mit Gerät, Leistung, Montageumfang und Festpreis.</span></li>
      <li><span class="mono">04</span><b>Einbau</b><span>Termin nach Absprache, Inbetriebnahme und Einweisung am selben Tag.</span></li>
    </ol>
    <p class="abschluss-cta">
      <a class="btn btn-primary" href="tel:+4953718759972">05371 8759972 anrufen</a>
      <a class="btn btn-ghost" href="{e(kat["datei"])}">Andere {e(kat["kurz"])}</a>
    </p>
  </div>
</section>
"""

    t += tail(motion="schlank", produkte=True)
    return datei, t



# --------------------------------------------------------------------- Shop-Uebersicht

def rechner(als_kopf=False):
    """Der Auslegungs-Rechner. Auf shop.html ist er der Einstieg (h1, eigener
       Kopftyp), auf der Startseite eine Sektion im Fluss (h2)."""
    if als_kopf:
        rahmen_auf = ('<section class="kopf-rechner" id="rechner">\n  <div class="wrap">\n'
                      '    <h1>Welche Leistung brauchen Ihre Räume?</h1>\n'
                      '    <p class="mono ans">→ Fläche eintragen, Zuschläge ankreuzen, '
                      'Kühllast in kW ablesen</p>\n')
    else:
        rahmen_auf = ('<section class="sec sec-klima" id="rechner">\n  <div class="wrap">\n'
                      '    <header class="sec-head">\n'
                      '      <h2>Welche Leistung brauchen Ihre Räume?</h2>\n'
                      '      <p class="mono ans">→ Fläche eintragen, Zuschläge ankreuzen, '
                      'Kühllast in kW ablesen</p>\n    </header>\n')
    return rahmen_auf + """

    <form class="konfig" id="konfigurator">
      <div class="konfig-kopf">
        <span class="mono">Welche Räume sollen gekühlt werden?</span>
        <button type="button" id="raum-plus" class="btn btn-ghost btn-sm">+ Raum hinzufügen</button>
      </div>
      <ul class="raeume" id="raeume"></ul>

      <div class="konfig-art">
        <span class="mono konfig-art-t" id="bauart-label">Wunsch</span>
        <div class="art-w" role="radiogroup" aria-labelledby="bauart-label">
          <label><input type="radio" name="bauart" value="egal" checked><span>Ist mir egal<b class="mono">wir empfehlen</b></span></label>
          <label><input type="radio" name="bauart" value="mobil"><span>Ohne Bohren<b class="mono">mobiles Gerät</b></span></label>
          <label><input type="radio" name="bauart" value="split"><span>Fest eingebaut<b class="mono">Split</b></span></label>
          <label><input type="radio" name="bauart" value="multi"><span>Mehrere Räume<b class="mono">Multi-Split</b></span></label>
        </div>
      </div>

      <output class="konfig-out" id="konfig-out" aria-live="polite">
        <ul class="konfig-werte mono">
          <li><span>Räume</span><b id="k-raeume">1</b></li>
          <li><span>Kühllast gesamt</span><b><span id="k-summe">1,9</span> kW</b></li>
          <li><span>entspricht</span><b><span id="k-btu">6.600</span> BTU/h</b></li>
          <li id="k-aussen-zeile" hidden><span>Außengerät ab</span><b><span id="k-aussen">0</span> kW</b></li>
        </ul>

        <!-- Die Kältekreis-Linie als kW-Skala: dieselbe Haarlinie wie im Kopf. -->
        <div class="kw-skala" aria-hidden="true">
          <div class="kw-linie"><span class="kw-fuell" id="k-fuell"></span></div>
          <div class="kw-zeiger" id="k-zeiger"></div>
          <ul class="kw-marks mono">
            <li style="left:20%"><i></i>2</li>
            <li style="left:35%"><i></i>3,5</li>
            <li style="left:50%"><i></i>5</li>
            <li style="left:60%"><i></i>6</li>
            <li style="left:70%"><i></i>7</li>
            <li style="left:100%"><i></i>10 kW</li>
          </ul>
          <div class="kw-grenze"></div>
        </div>

        <p class="konfig-satz" id="k-satz"></p>
        <p class="konfig-treffer mono" id="k-treffer"></p>
        <div class="k-treffer-sets" id="k-treffer-sets" hidden></div>
        <p class="konfig-akt">
          <a class="btn btn-primary btn-sm" id="k-weiter" href="shop-split.html">Passende Sets ansehen</a>
          <a class="btn btn-ghost btn-sm" href="kontakt.html" id="k-anfrage">Auslegung anfragen</a>
        </p>
      </output>

      <p class="mono konfig-fuss">
        Rechenweg: Fläche × spezifische Kühllast (60 W/m² Neubau · 80 Bestand · 100 Altbau ·
        130 Dachgeschoss). Zuschläge: große Süd-/Westverglasung +20 W/m² · Raumhöhe über 2,60 m
        +10 % · Technik oder offene Küche +300 W. Bei mehreren Räumen wird das Außengerät auf 85 %
        der Summe ausgelegt – es laufen selten alle Innengeräte gleichzeitig auf Volllast.
        Richtwert nach Faustformel; er ersetzt keine Kühllastberechnung nach VDI 2078 bzw.
        DIN EN 12831-1. Die verbindliche Auslegung machen wir vor Ort.
      </p>
    </form>
  </div>
</section>
"""


def shopseite():
    datei = "shop.html"
    bestseller = [s for s in K.SETS if s["bestseller"]][:3]
    if len(bestseller) < 3:
        rest = [s for s in K.SETS if not s["bestseller"] and s["kategorie"] != "mobil"]
        bestseller = (bestseller + rest)[:3]

    ab_montiert = K.eur(K.guenstigster_montagepreis())
    ab_abholung = K.eur(K.guenstigster_abholpreis())

    ld = {
        "@context": "https://schema.org", "@type": "CollectionPage",
        "name": "Klimaanlagen-Sets und Preise",
        "description": "Komplettsets für ein oder mehrere Räume, Auslegungs-Rechner und "
                       "Zubehör von KlimaTech38 in Gifhorn.",
        "isPartOf": {"@id": f"{DOMAIN}/#business"},
    }

    beschr = ("Klimaanlagen-Sets von KlimaTech38, Gifhorn: Split, Multi-Split und mobile Geräte "
              "zum Selbsteinbau oder mit Montage. Mit Auslegungs-Rechner für die Kühllast.")
    if not K.META["demo"]:
        beschr = (f"Klimaanlagen-Sets von KlimaTech38, Gifhorn: Split, Multi-Split und mobile Geräte "
                  f"ab {ab_abholung} zur Abholung, montiert ab {ab_montiert}. Mit Auslegungs-Rechner.")
    t = head("Klimaanlagen-Sets & Preise – Rechner | KlimaTech38", beschr,
             datei, ld)

    t += demo_band()

    kat_zeilen = []
    for kat in K.KATEGORIEN:
        anzahl = len(K.sets_der_kategorie(kat["id"]))
        wieviel = f"{anzahl} Sets" if kat["id"] != "zubehoer" else f"{len(K.ZUBEHOER)} Positionen"
        kat_zeilen.append(f"""        <li>
          <a href="{e(kat["datei"])}">
            <span class="kz-bild">{schema_svg("split1" if kat["id"] == "split" else "multi3" if kat["id"] == "multi" else "mono" if kat["id"] == "mobil" else "split1", "set-schema")}</span>
            <span class="kz-txt"><b>{e(kat["kurz"])}</b><span>{e(kat["antwort"])}</span></span>
            <span class="mono kz-n">{wieviel}</span>
          </a>
        </li>""")

    t += f"""
{rechner(als_kopf=True)}
<section class="sec">
  <div class="wrap">
    <header class="sec-head">
      <h2>Wo wollen Sie einsteigen?</h2>
      <p class="mono ans">→ Nach Bauart – die Raumzahl entscheidet, nicht der Geschmack</p>
    </header>
    <ul class="kat-zeilen">
{chr(10).join(kat_zeilen)}
    </ul>
  </div>
</section>


<section class="sec" id="selbsteinbau">
  <div class="wrap">
    <header class="sec-head">
      <h2>Was darf ich selbst einbauen?</h2>
      <p class="mono ans">→ Vorgefüllte Quick-Connect-Sets ja – offene Kältekreise nein</p>
    </header>
    <ul class="register register-k">
      <li><span class="reg-a">Mobiles Monoblock-Gerät</span>
        <span class="reg-b">Vollständig selbst. Aufstellen, Abluftschlauch nach draußen führen, einstecken.
          Wichtig: Der Schlauch muss möglichst kurz und das Fenster abgedichtet sein, sonst zieht das
          Gerät die warme Luft direkt wieder herein.</span></li>
      <li><span class="reg-a">Quick-Connect-Split-Set</span>
        <span class="reg-b">Selbst möglich. Die Leitung ist ab Werk befüllt und wird über Schnellkupplungen
          verbunden – der Kältekreis bleibt dabei geschlossen, es muss nicht vakuumiert und nicht
          nachgefüllt werden.</span></li>
      <li><span class="reg-a">Klassische Split-&nbsp;und Multi-Split-Anlage</span>
        <span class="reg-b">Nicht selbst. Sobald ein Kältekreis geöffnet, evakuiert oder befüllt wird, ist
          das Arbeit an fluorierten Treibhausgasen – dafür ist ein Sachkundenachweis nach der
          EU-Verordnung 517/2014 vorgeschrieben.</span></li>
      <li><span class="reg-a">Elektroanschluss</span>
        <span class="reg-b">Ein Gerät mit Stecker dürfen Sie einstecken. Ein fester Anschluss im Verteiler
          gehört in Fachhände.</span></li>
      <li><span class="reg-a">Kernbohrung</span>
        <span class="reg-b">Technisch machbar, praktisch heikel: In der Wand liegen Leitungen, und Bohrkerne
          durch die Dämmebene wollen sauber abgedichtet sein. Wir übernehmen das auf Wunsch auch dann,
          wenn Sie den Rest selbst machen.</span></li>
      <li><span class="reg-a">Mietwohnung</span>
        <span class="reg-b">Für Kernbohrung und Außengerät brauchen Sie die Zustimmung der Eigentümerin oder
          des Eigentümers. Ohne sie bleibt das mobile Gerät die realistische Lösung.</span></li>
    </ul>
    <p class="abschluss-cta">
      <a class="btn btn-ghost" href="ratgeber-selbsteinbau.html">Ausführlich nachlesen</a>
    </p>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <header class="sec-head">
      <h2>Abholen, liefern lassen oder montieren lassen?</h2>
      <p class="mono ans">→ Alles drei – der Preis auf jeder Set-Seite sagt, was enthalten ist</p>
    </header>
    <ul class="nachweise">
      <li><span class="mono nw-k">Abholung</span><span class="nw-v">Zeisigweg 4, 38518 Gifhorn – nach Terminabsprache, Mo–Fr 08–18 Uhr.</span></li>
      <li><span class="mono nw-k">Lieferung</span><span class="nw-v">Im Einzugsgebiet Gifhorn, Wolfsburg, Braunschweig, Peine, Salzgitter, Helmstedt. Kosten nennen wir im Angebot.</span></li>
      <li><span class="mono nw-k">Mit Montage</span><span class="nw-v">Kernbohrung, Halter, Leitung, Inbetriebnahme und Einweisung. <a href="montage.html">So läuft der Einbau ab</a>.</span></li>
      <li><span class="mono nw-k">Danach</span><span class="nw-v">Auf Wunsch <a href="wartung.html">Wartung</a>: Filter und Wärmetauscher reinigen, Kondensatweg prüfen, Funktion messen.</span></li>
    </ul>
    <p class="abschluss-cta">
      <a class="btn btn-primary" href="tel:+4953718759972">05371 8759972 anrufen</a>
      <a class="btn btn-ghost" href="beratung.html">Beratung vor Ort</a>
    </p>
  </div>
</section>
"""
    t += tail(motion="voll", produkte=True)
    return datei, t



# --------------------------------------------------------------------- Startseite

def startseite():
    datei = "index.html"
    bestseller = [s for s in K.SETS if s["bestseller"]][:3]
    if len(bestseller) < 3:
        rest = [s for s in K.SETS if not s["bestseller"] and s["kategorie"] != "mobil"]
        bestseller = (bestseller + rest)[:3]
    ab_montiert = K.eur(K.guenstigster_montagepreis())
    ab_abholung = K.eur(K.guenstigster_abholpreis())

    ld = {
        "@context": "https://schema.org", "@type": "HVACBusiness",
        "@id": f"{DOMAIN}/#business",
        "name": "KlimaTech38", "legalName": "InTroTech GmbH",
        "description": "Energetische Beratung, Planung, Auslegung, Verkauf und Montage von "
                       "Klimaanlagen sowie Energieausweise für Wohn-&nbsp;und Nichtwohngebäude in "
                       "Gifhorn, Wolfsburg und Braunschweig.",
        "url": f"{DOMAIN}/", "logo": f"{DOMAIN}/assets/brand/logo.png",
        "image": f"{DOMAIN}/assets/hero.jpg",
        "telephone": "+49 5371 8759972", "email": "info@introtech.de", "vatID": "DE460142356",
        "parentOrganization": {"@type": "Organization", "name": "InTroTech GmbH",
                               "url": "https://www.introtech.de/"},
        "address": {"@type": "PostalAddress", "streetAddress": "Zeisigweg 4", "postalCode": "38518",
                    "addressLocality": "Gifhorn", "addressRegion": "Niedersachsen", "addressCountry": "DE"},
        "geo": {"@type": "GeoCoordinates", "latitude": 52.481, "longitude": 10.547},
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "opens": "08:00", "closes": "18:00"}],
        "areaServed": [{"@type": "City", "name": n} for n in
                       ["Gifhorn", "Wolfsburg", "Braunschweig", "Peine", "Salzgitter", "Helmstedt"]],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Leistungen KlimaTech38",
            "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": n}} for n in [
                "Energieausweis für Wohn-&nbsp;und Nichtwohngebäude",
                "Energetische Beratung und Planung",
                "Planung und Auslegung von Klimaanlagen",
                "Lieferung und Montage von Split-&nbsp;und Multi-Split-Klimaanlagen",
                "Wartung von Klimaanlagen",
                "Kopplung von Klimaanlage und Photovoltaik"]]},
    }

    beschr = ("Klimaanlagen aus Gifhorn: Komplettsets zum Selbsteinbau oder mit Montage. "
              " Kostenlose Beratung vor Ort, Auslegung, Montage und Wartung. "
              "Dazu Energieausweise.")
    if not K.META["demo"]:
        beschr = (f"Klimaanlagen aus Gifhorn: Sets ab {ab_abholung} zur Abholung, montiert ab "
                  f"{ab_montiert}. Kostenlose Beratung vor Ort, Auslegung, Montage und Wartung.")
    t = head("Klimaanlagen & Energieausweis Gifhorn – KlimaTech38", beschr,
             datei, ld)

    t += demo_band()

    kat_zeilen = []
    for kat in K.KATEGORIEN:
        anzahl = len(K.sets_der_kategorie(kat["id"]))
        wieviel = f"{anzahl} Sets" if kat["id"] != "zubehoer" else f"{len(K.ZUBEHOER)} Positionen"
        art = {"split": "split1", "multi": "multi3", "mobil": "mono"}.get(kat["id"], "split1")
        kat_zeilen.append(f"""        <li>
          <a href="{e(kat["datei"])}">
            <span class="kz-bild">{schema_svg(art, "set-schema")}</span>
            <span class="kz-txt"><b>{e(kat["kurz"])}</b><span>{e(kat["antwort"])}</span></span>
            <span class="mono kz-n">{wieviel}</span>
          </a>
        </li>""")

    t += f"""
<section class="hero" id="start">
  <div class="wrap hero-in">
    <h1>Erst auslegen.<br>Dann kühlen.</h1>
    <p class="hero-sub">Klimaanlagen für Wohnung, Haus und Gewerbe – geplant, ausgelegt, geliefert
      und montiert. Dazu Energieausweise und energetische Planung für Wohn-&nbsp;und Nichtwohngebäude.
      Aus Gifhorn, im gesamten 38er-Raum.</p>
    <p class="hero-anker">
      <span class="mono">Komplettset ab {e(ab_abholung)} zur Abholung</span>
      <span class="mono">montiert ab {e(ab_montiert)}</span>
      {'<span class="mono hero-anker-demo">Beispielpreise – verbindlich ist das Angebot</span>' if K.META["demo"] else ''}
    </p>
    <div class="hero-btns">
      <a class="btn btn-primary" href="beratung.html">Kostenlose Beratung anfragen</a>
      <a class="btn btn-ghost" href="shop.html">Sets &amp; Preise ansehen</a>
    </div>
    <a class="hero-quiet mono" href="#rechner">↓ Erst die Kühllast Ihrer Räume berechnen</a>
  </div>
  <figure class="hero-fig wrap" data-reveal>
    <img src="assets/hero.jpg" width="1500" height="993" fetchpriority="high"
         alt="Split-Innengerät an der Wand eines hellen, offenen Wohn-&nbsp;und Küchenbereichs">
    <figcaption class="mono">Das Innengerät sitzt hoch an der Wand und nie direkt über dem Sitzplatz –
      Position, Leitungsweg und Schallabstand legen wir vor Ort fest.</figcaption>
  </figure>
</section>

<section class="vertrauen band">
  <div class="wrap">
    <ul class="mono">
      <li><i aria-hidden="true"></i>dena-Energieberater</li>
      <li><i aria-hidden="true"></i>TÜV-zertifizierter Fachbetrieb</li>
      <li><i aria-hidden="true"></i>Besichtigung &amp; Angebot kostenfrei</li>
      <li><i aria-hidden="true"></i>Auslegung nach Kühllast, nicht nach Faustregel</li>
      <li><i aria-hidden="true"></i>Gifhorn · Wolfsburg · Braunschweig</li>
    </ul>
  </div>
</section>

<!-- Der Kern des Auftrags: zwei gleich starke Wege, nicht ein Weg mit Nebenausgang. -->
<section class="sec" id="wege">
  <div class="wrap">
    <header class="sec-head">
      <h2>Selbst einbauen oder einbauen lassen?</h2>
      <p class="mono ans">→ Beides geht – auf jeder Set-Seite steht der Preis für beide Wege</p>
    </header>
    <div class="wege">
      <article class="weg">
        <p class="mono weg-k">Weg 1 · Selbst</p>
        <h3>Set aussuchen, abholen, einbauen</h3>
        <p>Mobile Geräte und vorgefüllte Quick-Connect-Sets dürfen Sie selbst anschließen – der
          Kältekreis bleibt dabei geschlossen. Sie wählen im Katalog, holen bei uns in Gifhorn ab
          und bauen ein. Wo Sie die Grenze überschreiten würden, sagen wir es Ihnen vorher.</p>
        <ul class="weg-l">
          <li>Preise je Set sichtbar</li>
          <li>Auslegungs-Rechner statt Bauchgefühl</li>
          <li>Kernbohrung auf Wunsch trotzdem von uns</li>
        </ul>
        <a class="btn btn-ghost" href="shop.html">Zu den Sets &amp; Preisen</a>
      </article>
      <article class="weg weg-2">
        <p class="mono weg-k">Weg 2 · Machen lassen</p>
        <h3>Wir kommen, legen aus und montieren</h3>
        <p>Wir sehen uns die Räume an, rechnen die Kühllast, planen Leitungsweg und Standort des
          Außengeräts und machen ein schriftliches Festpreis-Angebot. Besichtigung und Angebot
          kosten nichts – auch wenn Sie sich dagegen entscheiden.</p>
        <ul class="weg-l">
          <li>Besichtigung und Angebot kostenfrei</li>
          <li>Festpreis inklusive Montage</li>
          <li>Inbetriebnahme, Einweisung, Wartung</li>
        </ul>
        <a class="btn btn-primary" href="beratung.html">Beratung anfragen</a>
      </article>
    </div>
  </div>
</section>
{rechner(als_kopf=False)}
<section class="sec">
  <div class="wrap">
    <header class="sec-head">
      <h2>Womit fangen die meisten an?</h2>
      <p class="mono ans">→ Drei Sets decken die häufigsten Wohnsituationen im 38er-Raum ab</p>
    </header>
    <ul class="set-kacheln">
{chr(10).join(set_kachel(s) for s in bestseller)}
    </ul>
    <ul class="kat-zeilen kat-zeilen-kurz">
{chr(10).join(kat_zeilen)}
    </ul>
    <p class="preis-fuss mono">{e(K.META["preisFuss"])}</p>
  </div>
</section>

<section class="sec sec-klima" id="ablauf">
  <div class="wrap">
    <header class="sec-head">
      <h2>Wie läuft das ab, wenn wir montieren?</h2>
      <p class="mono ans">→ Fünf Schritte, in der Regel innerhalb weniger Wochen</p>
    </header>
    <ol class="steps">
      <li><span class="mono">01</span><b>Anfrage</b><span>Anruf, WhatsApp oder Formular – mit Raumgröße, Geschoss und Baujahr.</span></li>
      <li><span class="mono">02</span><b>Besichtigung</b><span>Wir sehen uns Räume, Fenster, Leitungsweg und Fassade an. Kostenfrei.</span></li>
      <li><span class="mono">03</span><b>Angebot</b><span>Schriftlich, unverbindlich, mit Festpreis und klarem Montageumfang.</span></li>
      <li><span class="mono">04</span><b>Montage</b><span>Termin nach Absprache, in der Regel ein Arbeitstag je Anlage.</span></li>
      <li><span class="mono">05</span><b>Einweisung</b><span>Inbetriebnahme, Messung, Übergabe – und auf Wunsch die Wartung danach.</span></li>
    </ol>
    <p class="abschluss-cta">
      <a class="btn btn-ghost" href="montage.html">Was am Montagetag passiert</a>
      <a class="btn btn-ghost" href="wartung.html">Wartung &amp; Service</a>
    </p>
  </div>
</section>

<section class="sec sec-energie" id="energie">
  <div class="wrap">
    <header class="sec-head">
      <h2>Und wenn das Haus schon warm hereinlässt?</h2>
      <p class="mono ans">→ Dann kühlen Sie gegen die Gebäudehülle an – das rechnet sich nie</p>
    </header>
    <p class="hinweis">Eine Klimaanlage arbeitet gegen die Gebäudehülle an. Ist das Dach ungedämmt
      oder die Südverglasung unbeschattet, wächst die Kühllast schneller, als jedes größere Gerät sie
      wegnehmen kann. Deshalb sehen wir uns zuerst an, wo die Wärme überhaupt hereinkommt – und ob
      eine Maßnahme an der Hülle nicht mehr bringt als mehr Kilowatt.</p>
    <ul class="register register-e">
      <li><span class="reg-a">Energieausweis</span>
        <span class="reg-b">Für Wohn-&nbsp;und Nichtwohngebäude, als Verbrauchs-&nbsp;oder Bedarfsausweis –
          ausgestellt von einem dena-Energieberater.</span></li>
      <li><span class="reg-a">Wärmebrücken finden</span>
        <span class="reg-b">Per Thermografie sichtbar machen, wo Wärme aus-&nbsp;und im Sommer eintritt.
          Das ist der Unterschied zwischen Vermuten und Messen.</span></li>
      <li><span class="reg-a">Maßnahmen ableiten</span>
        <span class="reg-b">Priorisiert nach Wirkung und Aufwand – damit klar ist, was zuerst
          gemacht werden sollte und was warten kann.</span></li>
    </ul>
    <p class="abschluss-cta">
      <a class="btn btn-primary btn-energie" href="energetische-beratung.html">Energetische Beratung</a>
    </p>
  </div>
</section>

<section class="sec kreuzung" id="pv">
  <div class="wrap kreuzung-in">
    <header class="sec-head">
      <h2>Kühlen mit dem eigenen Strom?</h2>
      <p class="mono ans">→ Der eine Punkt, an dem sich beide Stränge treffen</p>
    </header>
    <p class="kreuzung-p">Es gibt wenige Verbraucher, deren Bedarf so genau zur Erzeugung passt:
      Gekühlt wird, wenn die Sonne scheint. Wer eine Photovoltaikanlage hat, betreibt die
      Klimaanlage weitgehend mit eigenem Strom – ohne sein Verhalten zu ändern.</p>
    <p class="kreuzung-legende mono">
      <span class="lg lg-k">Klima</span><span class="lg lg-e">Energie</span>
      <a href="ratgeber-pv.html">Ausführlich nachlesen</a>
    </p>
  </div>
</section>

<section class="sec" id="wissen">
  <div class="wrap">
    <header class="sec-head">
      <h2>Was Sie vor dem Angebot wissen sollten</h2>
      <p class="mono ans">→ Vier Ratgeber und die häufigsten Fragen – ohne Anruf</p>
    </header>
    <ul class="rg-liste">
      <li><a href="ratgeber-groesse.html"><span class="rg-txt"><b>Welche Leistung braucht mein Raum?</b><span>Faustformel, Zuschläge und warum zu groß genauso falsch ist wie zu klein.</span></span><span class="rg-pfeil" aria-hidden="true">→</span></a></li>
      <li><a href="ratgeber-kosten.html"><span class="rg-txt"><b>Was kostet eine Klimaanlage?</b><span>Set, Montage und Strom getrennt – und was den Montagepreis bewegt.</span></span><span class="rg-pfeil" aria-hidden="true">→</span></a></li>
      <li><a href="ratgeber-selbsteinbau.html"><span class="rg-txt"><b>Was darf ich selbst einbauen?</b><span>Quick-Connect ja, offener Kältekreis nein – und was in der Miete gilt.</span></span><span class="rg-pfeil" aria-hidden="true">→</span></a></li>
      <li><a href="faq.html"><span class="rg-txt"><b>Häufige Fragen</b><span>Einbaudauer, Lautstärke, Wartung, Kältemittel, Vermieter, Förderung.</span></span><span class="rg-pfeil" aria-hidden="true">→</span></a></li>
    </ul>
  </div>
</section>

<section class="sec" id="betrieb">
  <div class="wrap">
    <header class="sec-head">
      <h2>Mit wem haben Sie es zu tun?</h2>
      <p class="mono ans">→ InTroTech GmbH, Gifhorn – KlimaTech38 ist ihr Geschäftsbereich für Klima und Energie</p>
    </header>
    <ul class="nachweise">
      <li><span class="mono nw-k">Qualifikation</span><span class="nw-v"><b>dena-Energieberater</b> – Energieausweise für Wohn-&nbsp;und Nichtwohngebäude</span></li>
      <li><span class="mono nw-k">Prüfung</span><span class="nw-v"><b>TÜV Rheinland</b> – TÜV-zertifizierter Fachbetrieb</span></li>
      <li><span class="mono nw-k">Betrieb</span><span class="nw-v">
        <img class="nw-logo" src="assets/brand/logo.png" width="1319" height="254" alt="InTroTech GmbH">
        Geschäftsführung Johann Warkentin, Jonathan Mangold, Adrian Mangold</span></li>
      <li><span class="mono nw-k">Register</span><span class="nw-v">Amtsgericht Hildesheim HRB 210481 · USt-IdNr. DE460142356</span></li>
      <li><span class="mono nw-k">Grundsatz</span><span class="nw-v">Innovation trifft Verantwortung – Gebäude schützen, Werte erhalten, Lebensqualität sichern.</span></li>
    </ul>
    <p class="betrieb-p">Wir kommen aus der Schadensanierung: Leckageortung, Trocknung, Schimmel-&nbsp;und       Asbestsanierung. Wer täglich sieht, was Feuchte und Wärme in einem Gebäude anrichten, plant eine
      Klimaanlage anders – mit Blick auf Kondensat, Dämmung und die Energiebilanz des ganzen Hauses.
      <a href="https://www.introtech.de/" target="_blank" rel="noopener">introtech.de</a></p>
  </div>
</section>

<section class="sec kontakt" id="kontakt">
  <div class="wrap kontakt-in">
    <header class="sec-head sec-head-c">
      <h2>Sollen wir uns Ihre Räume ansehen?</h2>
      <p class="mono ans">→ Anruf, WhatsApp oder Formular – Besichtigung und Angebot sind kostenfrei</p>
    </header>
    <div class="kanaele">
      <a class="kanal" href="tel:+4953718759972">
        <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 4h3l2 5-2.5 1.5a11 11 0 0 0 5 5L14 13l5 2v3a2 2 0 0 1-2 2A14 14 0 0 1 3 6a2 2 0 0 1 2-2Z"/></svg>
        <span><b>05371 8759972</b><span class="mono">Mo–Fr 08–18 Uhr</span></span>
      </a>
      <a class="kanal" href="https://wa.me/4953718759972" target="_blank" rel="noopener">
        <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 21l1.7-5A8 8 0 1 1 8 19.3L3 21Z"/><path d="M8.5 9.5c0 3 2 5 5 5 .8 0 1.3-.6 1.3-1.1l-1.6-.8-.8.8a4 4 0 0 1-1.8-1.8l.8-.8-.8-1.6c-.5 0-1.1.5-1.1 1.3Z"/></svg>
        <span><b>WhatsApp</b><span class="mono">Fotos vom Raum direkt schicken</span></span>
      </a>
      <a class="kanal" href="mailto:info@introtech.de">
        <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>
        <span><b>info@introtech.de</b><span class="mono">Zeisigweg 4 · 38518 Gifhorn</span></span>
      </a>
    </div>
    <p class="abschluss-cta">
      <a class="btn btn-primary" href="tel:+4953718759972">05371 8759972 anrufen</a>
      <a class="btn btn-ghost" href="kontakt.html">Anfrage schreiben</a>
    </p>
  </div>

  <div class="karte-band">
    <div class="gebiet">
      <div class="gebiet-linie" aria-hidden="true"></div>
      <ul class="mono">
        <li><i></i>Gifhorn</li><li><i></i>Wolfsburg</li><li><i></i>Braunschweig</li>
        <li><i></i>Peine</li><li><i></i>Salzgitter</li><li><i></i>Helmstedt</li>
      </ul>
    </div>
    <iframe class="karte" title="Karte des Einzugsgebiets zwischen Gifhorn, Wolfsburg und Braunschweig"
      loading="lazy" referrerpolicy="no-referrer-when-downgrade"
      src="https://www.openstreetmap.org/export/embed.html?bbox=10.20%2C52.28%2C10.95%2C52.68&amp;layer=mapnik&amp;marker=52.481%2C10.547"></iframe>
    <p class="karte-fuss mono">
      <a href="https://www.openstreetmap.org/?mlat=52.481&amp;mlon=10.547#map=12/52.481/10.547" target="_blank" rel="noopener">Größere Karte öffnen</a>
      <span>Kartendaten © OpenStreetMap-Mitwirkende</span>
    </p>
  </div>
</section>
"""
    t += tail(motion="voll", produkte=True)
    return datei, t


# --------------------------------------------------------------------- Sitemap

def sitemap():
    """Wird erzeugt, aber solange META["demo"] gilt nicht in robots.txt beworben —
       eine Sitemap aus lauter noindex-URLs ist ein Widerspruch."""
    seiten = list(C.SEITEN.keys()) + [f"set-{s['id']}.html" for s in K.SETS]
    prio = {"index.html": "1.0", "shop.html": "0.9", "beratung.html": "0.9",
            "klimaanlagen.html": "0.9", "energetische-beratung.html": "0.9", "kontakt.html": "0.8"}
    eintraege = []
    for p in sorted(set(seiten)):
        if not (SITE / p).exists() and p not in C.SEITEN:
            continue
        loc = f"{DOMAIN}/" if p == "index.html" else f"{DOMAIN}/{p}"
        pr = prio.get(p, "0.6" if p.startswith(("impressum", "datenschutz")) else "0.7")
        eintraege.append(f"  <url>\n    <loc>{loc}</loc>\n"
                         f"    <lastmod>{K.META['stand']}</lastmod>\n"
                         f"    <priority>{pr}</priority>\n  </url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(eintraege) + "\n</urlset>\n")


# --------------------------------------------------------------------- Lauf

def main():
    probleme = K.pruefe()
    if probleme:
        print("Katalog-Selbsttest schlaegt fehl:")
        for p in probleme:
            print("  -", p)
        return 1

    nur_pruefen = "--check" in sys.argv
    geschrieben = []

    def ohne_chrome(s):
        """Kopf und Fuss setzt kt38_chrome.py NACH dem Generator ein. Für den
           Vergleich wird der Sentinel-Inhalt auf beiden Seiten entfernt."""
        import re as _re
        s = _re.sub(r"(<!-- KT38:HEADER:START).*?(KT38:HEADER:END -->)", r"\1\2", s, flags=_re.S)
        return _re.sub(r"(<!-- KT38:FOOTER:START).*?(KT38:FOOTER:END -->)", r"\1\2", s, flags=_re.S)

    def schreibe(name, inhalt):
        ziel = SITE / name
        if nur_pruefen:
            if not ziel.exists() or ohne_chrome(ziel.read_text(encoding="utf-8")) != ohne_chrome(inhalt):
                print(f"  ! {name} weicht ab")
                return False
            return True
        ziel.write_text(inhalt, encoding="utf-8")
        geschrieben.append(name)
        return True

    ok = True
    if not nur_pruefen:
        geschrieben.append(schreibe_produkte_js())

    ok &= schreibe(*startseite())
    ok &= schreibe(*shopseite())
    for kat in K.KATEGORIEN:
        ok &= schreibe(*kategorieseite(kat))
    for s in K.SETS:
        ok &= schreibe(*setseite(s))
    ok &= schreibe("sitemap.xml", sitemap())

    if nur_pruefen:
        print("Katalog aktuell." if ok else "Katalog veraltet — Generator laufen lassen.")
        return 0 if ok else 1

    print(f"{len(geschrieben)} Dateien geschrieben:")
    for g in geschrieben:
        print("  ✎", g)
    print("\nJetzt Kopf/Fuss einsetzen:  python3 .tools/kt38_chrome.py --write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
