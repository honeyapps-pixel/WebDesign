#!/usr/bin/env python3
"""InTroTech (introtech-sanierung) — Redesign „High-End" 2026-09-24.

Baut den gemeinsamen Rahmen (Plankopf-Leiste + Lageplan-Footer) in alle 9 Seiten,
schreibt den <main> der Startseite neu und formt die Unterseiten-Köpfe zum „Blattkopf" um.
Idempotent: arbeitet zwischen den Markern <!--ITC:…--> bzw. ersetzt beim ersten Lauf die
alten Header/Hero/Footer-Blöcke. Aufruf: python3 .tools/itc_gen.py
"""
import html, re
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / 'introtech-sanierung'
TEL, TEL_TXT = '+4953718759972', '05371 8759972'
WA = 'https://wa.me/4953718759972'
ABD = 'https://introtech-abdichtung.vercel.app/'

ARROW = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
ARROW_EXT = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M9 7h8v8"/></svg>'
PHONE = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 4h3l2 5-2.5 1.5a11 11 0 0 0 5 5L14 13l5 2v3a2 2 0 0 1-2 2A14 14 0 0 1 3 6a2 2 0 0 1 2-2Z"/></svg>'
PAUSE = '<svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor" aria-hidden="true"><rect x="6" y="5" width="4" height="14"/><rect x="14" y="5" width="4" height="14"/></svg>'
WA_SVG = '<svg viewBox="0 0 32 32" width="30" height="30" fill="currentColor" aria-hidden="true"><path d="M19.11 17.21c-.27-.14-1.6-.79-1.85-.88-.25-.09-.43-.14-.61.14-.18.27-.7.88-.86 1.06-.16.18-.32.2-.59.07-.27-.14-1.14-.42-2.17-1.34-.8-.71-1.34-1.59-1.5-1.86-.16-.27-.02-.42.12-.55.12-.12.27-.32.41-.48.14-.16.18-.27.27-.45.09-.18.05-.34-.02-.48-.07-.14-.61-1.47-.84-2.01-.22-.53-.45-.46-.61-.47h-.52c-.18 0-.48.07-.73.34-.25.27-.96.94-.96 2.29 0 1.35.98 2.65 1.12 2.84.14.18 1.93 2.95 4.68 4.13.65.28 1.16.45 1.56.58.66.21 1.25.18 1.72.11.52-.08 1.6-.65 1.83-1.28.23-.63.23-1.17.16-1.28-.07-.11-.25-.18-.52-.32z"/><path d="M16 3C9.37 3 4 8.37 4 15c0 2.12.55 4.1 1.52 5.83L4 29l8.37-2.2A11.93 11.93 0 0 0 16 27c6.63 0 12-5.37 12-12S22.63 3 16 3zm0 21.6c-1.96 0-3.8-.53-5.38-1.45l-.39-.23-4.97 1.3 1.33-4.84-.25-.4A9.55 9.55 0 0 1 6.4 15c0-5.3 4.3-9.6 9.6-9.6s9.6 4.3 9.6 9.6-4.3 9.6-9.6 9.6z"/></svg>'

LEISTUNGEN = [  # (Datei, Kurzname, Anliegen, Stichworte, Bild, Bild-Klasse, Alt)
    ('leckageortung.html', 'Leckageortung & Notdienst', 'Wasser tritt aus, die Ursache ist unklar',
     'Thermografie · Elektroakustik · Tracergas', 'assets/leckageortung.jpg', '', 'Symbolfoto: Rohrverbindung unter einer gedämmten Leitung'),
    ('trocknung.html', 'Trocknung', 'Wand, Estrich oder Dämmung sind nass',
     'Kondensations- & Adsorptionstrocknung · Dämmschicht', 'assets/trocknung.jpg', 'geraet', 'Symbolfoto: zwei Kondensationstrockner'),
    ('sanierung.html', 'Schaden-, Schimmel- & Asbest-Sanierung', 'Schimmel, Asbest oder Folgeschäden',
     'DGUV 201-028 · TRGS 519 · Wiederaufbau', 'assets/sanierung.jpg', '', 'Symbolfoto: Arbeiter mit Atemschutzmaske'),
    (ABD, 'Bauwerksabdichtung', 'Feuchter Keller, nasse Außenwand',
     'Kelleraußen- & Innenabdichtung · Horizontalsperre', 'assets/abdichtung-sockel.jpg', '', 'Symbolfoto: feuchte, abgeplatzte Sockelwand'),
    ('energetische-beratung.html', 'Energetische Beratung & Planung', 'Energieausweis oder Modernisierung',
     'Energieausweis · PV · Wärmepumpe', 'assets/energieberatung.jpg', '', 'Symbolfoto: Baupläne, Wasserwaage und Schutzhelm'),
]
NAV_KURZ = [('leckageortung.html', 'Leckageortung'), ('trocknung.html', 'Trocknung'), ('sanierung.html', 'Sanierung'),
            (ABD, 'Bauwerksabdichtung'), ('energetische-beratung.html', 'Energieberatung')]


def e(s):
    return html.escape(s, quote=True)


def plankopf(aktiv):
    def item(href, txt):
        ext = href.startswith('http')
        cur = ' aria-current="page"' if href == aktiv else ''
        extra = ' target="_blank" rel="noopener"' if ext else ''
        mark = '<svg class="ext" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M9 7h8v8"/></svg>' if ext else ''
        return f'<li><a href="{href}"{cur}{extra}>{e(txt)}{mark}</a></li>'
    lst = ''.join(item(h, t) for h, t in NAV_KURZ)
    unt = ''.join(item(h, t) for h, t in [('ueber-uns.html', 'Über uns'), ('index.html#ablauf', 'Ablauf'), ('index.html#anfrage', 'Anfrage')])
    return f'''<!--ITC:plankopf-->
<a class="skip" href="#inhalt">Zum Inhalt springen</a>
<aside class="plankopf" data-plankopf>
  <div class="plankopf-kopf">
    <a class="plankopf-logo" href="index.html" aria-label="InTroTech GmbH — Startseite"><img src="assets/brand/logo.png" alt="InTroTech GmbH — Leckageortung, Trocknung, Sanierung, Bauwerksabdichtung" width="1400" height="257"></a>
    <a class="plankopf-tel" href="tel:{TEL}" aria-label="24/7 Notruf {TEL_TXT} anrufen">{PHONE}</a>
    <button class="plankopf-menue" type="button" aria-expanded="false" aria-controls="plankopf-panel" data-menue>Menü</button>
  </div>
  <div class="plankopf-panel" id="plankopf-panel">
    <nav class="plankopf-nav" aria-label="Hauptnavigation">
      <p class="plankopf-h">Leistungen</p>
      <ul>{lst}</ul>
      <p class="plankopf-h">Unternehmen</p>
      <ul>{unt}</ul>
    </nav>
    <div class="plankopf-notruf">
      <p class="plankopf-h">24/7 Notruf</p>
      <a class="plankopf-nr" href="tel:{TEL}">{TEL_TXT}</a>
      <a class="wa" href="{WA}" target="_blank" rel="noopener">per WhatsApp schreiben</a>
      <p>Büro Mo–Fr 08–18 Uhr</p>
    </div>
  </div>
</aside>
<!--/ITC:plankopf-->'''


def lageplan():
    # Nur der Sitz wird markiert — die Orte des Einzugsgebiets beschriftet die OSM-Karte selbst.
    return f'''<!--ITC:lageplan-->
<footer class="lageplan" aria-label="Kontakt und Einzugsgebiet">
  <div class="lageplan-karte">
    <div class="lageplan-buehne">
      <img src="assets/media/lageplan.webp" alt="Karte der Region: Sitz in Gifhorn, Einzugsgebiet Wolfsburg, Braunschweig, Peine, Salzgitter und Helmstedt" width="1427" height="1143" loading="lazy">
      <span class="ort ort--sitz" style="left:43.57%;top:16.53%" aria-hidden="true"><span>InTroTech · Zeisigweg 4</span></span>
    </div>
    <p class="lageplan-osm">Karte © <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap-Mitwirkende</a></p>
  </div>
  <div class="schriftfeld">
    <div class="sf-logo voll"><img src="assets/brand/logo.png" alt="InTroTech GmbH" width="1400" height="257" loading="lazy"></div>
    <div><span class="sf-h">24/7 Notruf</span><a class="sf-nr" href="tel:{TEL}">{TEL_TXT}</a></div>
    <div><span class="sf-h">Büro</span>Mo–Fr 08–18 Uhr</div>
    <div><span class="sf-h">Anschrift</span>Zeisigweg 4<br>38518 Gifhorn<br><a href="https://www.openstreetmap.org/?mlat=52.481&amp;mlon=10.547#map=15/52.481/10.547" target="_blank" rel="noopener">Route <svg class="ext" viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M9 7h8v8"/></svg></a></div>
    <div><span class="sf-h">Schreiben</span><a href="mailto:info@introtech.de">info@introtech.de</a><br><a href="{WA}" target="_blank" rel="noopener">WhatsApp</a></div>
    <div class="voll"><span class="sf-h">Einzugsgebiet</span>Gifhorn · Wolfsburg · Braunschweig · Peine · Salzgitter · Helmstedt und Umgebung</div>
    <div class="sf-recht voll"><span>© <span id="year">2026</span> InTroTech GmbH · TÜV-zertifizierter Fachbetrieb</span><a href="impressum.html">Impressum</a><a href="datenschutz.html">Datenschutz</a><a href="agb.html">AGB</a></div>
  </div>
</footer>
<!--/ITC:lageplan-->'''


def kopf(leitsatz, h2, id_=None):
    return f'<header class="kopf" data-reveal><p class="leitsatz">{leitsatz}</p><h2{f" id={chr(34)}{id_}{chr(34)}" if id_ else ""}>{h2}</h2></header>'


def startseite_main():
    reg = []
    for href, name, anl, stw, img, cls, alt in LEISTUNGEN:
        ext = href.startswith('http')
        extra = ' target="_blank" rel="noopener"' if ext else ''
        reg.append(f'''<li><a href="{href}"{extra}>
          <span class="anliegen">{e(anl)}</span>
          <h3>{e(name)}</h3>
          <span class="stichworte">{e(stw)}</span>
          <span class="pfeil">{ARROW_EXT if ext else ARROW}</span>
        </a></li>''')
    reg = '\n        '.join(reg)
    return f'''<!--ITC:main-->
<main id="inhalt">

<section class="titelblatt" aria-labelledby="titel">
  <div class="titel-text">
    <h1 class="titel" id="titel">Damit Ihr Gebäude nicht nur trocken wird, <em>sondern auch bleibt.</em></h1>
    <p class="titel-lead">Wir sind Ihr TÜV-zertifizierter Fachbetrieb für Leckageortung, Trocknung, Sanierung und Bauwerksabdichtung in Gifhorn, Wolfsburg, Braunschweig und der Region. Die Abwicklung mit Ihrer Versicherung übernehmen wir.</p>
    <div class="titel-notruf notruf">
      <span class="label">24/7 Notruf</span>
      <a class="titel-nr" href="tel:{TEL}">{TEL_TXT}</a>
      <a class="titel-wa" href="{WA}" target="_blank" rel="noopener">oder per WhatsApp schreiben</a>
    </div>
    <a class="textlink titel-link" href="#anfrage">Schaden melden {ARROW}</a>
  </div>
  <div class="bildfolge" data-stadien aria-roledescription="Bildfolge" aria-label="Ein Raum nach dem Wasserschaden: Trocknung, Sanierung, fertig (Symbolbilder)">
    <figure class="stadium ist-aktiv"><img src="assets/media/stadium-1-trocknung.webp" width="1600" height="1600" alt="Heller Wohnraum während der technischen Trocknung: Kondenstrockner mit Kondensatschlauch in den Eimer, Ventilator, Folienwand vor der Tür" fetchpriority="high"></figure>
    <figure class="stadium"><img src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==" data-src="assets/media/stadium-2-sanierung.webp" width="1600" height="1600" alt="Derselbe Raum bei der Sanierung: neu verputzter Wandsockel, Eimer mit Glättkelle"></figure>
    <figure class="stadium"><img src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==" data-src="assets/media/stadium-3-fertig.webp" width="1600" height="1600" alt="Derselbe Raum fertig saniert: durchgehendes Parkett, frisch gestrichene Wände, Sessel am Fenster"></figure>
    <span class="bildfolge-kennung">Symbolbilder</span>
    <button class="bildfolge-pause" type="button" data-stadien-pause aria-label="Bildwechsel anhalten">{PAUSE}</button>
  </div>
</section>

<section class="abschnitt" id="leistungen" aria-labelledby="h-leistungen">
  <div class="inhalt">
    {kopf("Von der Schadensanalyse über Sofortmaßnahmen und technische Trocknung bis zur vollständigen Sanierung Ihrer Räume.", "Leistungen", "h-leistungen")}
    <ul class="register" data-reveal>
        {reg}
    </ul>
  </div>
</section>

<section class="abschnitt abschnitt--papier" id="unternehmen" aria-labelledby="h-unternehmen">
  <div class="inhalt">
    {kopf("Innovation trifft Verantwortung. <span class='leise'>Gebäude schützen, Werte erhalten und Lebensqualität sichern.</span>", "Über InTroTech", "h-unternehmen")}
    <div class="unternehmen-raster">
      <div class="fliesstext" data-reveal>
        <p>Wir verbinden Ingenieurwissen mit moderner Messtechnik zur präzisen Feuchtigkeitsanalyse. Leckageortung, Trocknung und fachgerechte Sanierung erledigen wir mit zerstörungsarmen Verfahren.</p>
        <p>Ein Wasserschaden bringt genug Stress mit sich. Wir nehmen ihn Ihnen ab: mit professionellem Fachpersonal aus Ihrer Region, moderner Technik und einem klaren Ablauf, der ohne Schnittstellenprobleme funktioniert.</p>
        <a class="textlink" href="ueber-uns.html">Mehr über uns {ARROW}</a>
      </div>
      <dl class="datenblatt" data-reveal>
        <div><dt>Geschäftsführung</dt><dd>Johann Warkentin · Jonathan Mangold · Adrian Mangold</dd></div>
        <div><dt>Zertifiziert</dt><dd><ul>
          <li>Sachkundenachweis Leckageortung in Innenräumen (TRA) – TÜV Rheinland</li>
          <li>Fachkraft für Wasserschadenbeseitigung – TÜV Rheinland</li>
          <li>Sachkundenachweis gemäß Anlage 4C TRGS 519 – Asbest Akademie Ahaus</li>
          <li>Energieberater Wohn- und Nichtwohngebäude (dena-Anerkennung) – TÜV Rheinland</li>
        </ul></dd></div>
        <div><dt>Versicherung</dt><dd>Schadensdokumentation und Kommunikation mit Ihrem Versicherer</dd></div>
        <div><dt>Sitz</dt><dd>Zeisigweg 4, 38518 Gifhorn</dd></div>
      </dl>
    </div>
  </div>
</section>

<section class="abschnitt" id="ablauf" aria-labelledby="h-ablauf">
  <div class="inhalt">
    {kopf("In nur 4 Schritten wird Ihnen geholfen.", "Ablauf", "h-ablauf")}
    <ol class="ablauf-raster" data-reveal>
      <li><span class="schritt-nr">1</span><h3>Kontaktaufnahme</h3><p>Rufen Sie uns einfach an unter <a href="tel:{TEL}">{TEL_TXT}</a> oder schreiben Sie uns eine E-Mail. Schildern Sie kurz Ihr Anliegen – wir melden uns schnell zurück und vereinbaren einen Termin.</p></li>
      <li><span class="schritt-nr">2</span><h3>Sofortmaßnahmen und Beratung vor Ort</h3><p>Ob feuchte Wände, Schimmel oder ein Rohrbruch – wir kommen zu Ihnen, ordnen die Situation ein und handeln direkt vor Ort.</p></li>
      <li><span class="schritt-nr">3</span><h3>Maßnahme und nachhaltige Sanierung</h3><p>Nach der Soforthilfe folgt die Sanierung: fachgerecht, effizient und nachhaltig – mit modernen Verfahren und langjähriger Erfahrung.</p></li>
      <li><span class="schritt-nr">4</span><h3>Versicherungsservice</h3><p>Von der Schadensdokumentation bis zur Kommunikation mit dem Versicherer: Wir übernehmen das für Sie, damit Sie sich um nichts kümmern müssen.</p></li>
    </ol>
    <p class="ablauf-fuss">Ein Ansprechpartner, klare Abläufe, keine Schnittstellenprobleme.</p>
  </div>
</section>

<section class="abschnitt abschnitt--papier" id="anfrage" aria-labelledby="h-anfrage">
  <div class="inhalt">
    {kopf("Jeder Schaden ist anders. <span class='leise'>Wir nehmen uns Zeit für Ihr Anliegen und beraten Sie kompetent und individuell.</span>", "Anfrage &amp; Notruf", "h-anfrage")}
    <div class="anfrage-raster">
      <div data-reveal>
        <span class="label">24/7 Notruf</span>
        <a class="anfrage-nr" href="tel:{TEL}">{TEL_TXT}</a>
        <p class="anfrage-meta"><a href="{WA}" target="_blank" rel="noopener">per WhatsApp schreiben</a> · Büro Mo–Fr 08–18 Uhr</p>
      </div>
      <form class="formular kontakt-form" id="kontaktForm" novalidate data-reveal>
        <div class="feld"><label for="f-name">Name</label><input type="text" id="f-name" name="name" autocomplete="name" placeholder="Ihr Name"></div>
        <div class="zeile">
          <div class="feld"><label for="f-tel">Telefon</label><input type="tel" id="f-tel" name="tel" autocomplete="tel" placeholder="Für den Rückruf"></div>
          <div class="feld"><label for="f-ort">Ort</label><input type="text" id="f-ort" name="ort" placeholder="z. B. Gifhorn"></div>
        </div>
        <div class="feld"><label for="f-msg">Was ist passiert?</label><textarea id="f-msg" name="nachricht" rows="4" placeholder="Kurz zum Schaden: Art, Raum, seit wann …"></textarea></div>
        <button type="submit" class="senden">Nachricht senden {ARROW}</button>
        <p class="form-note" id="formNote" hidden></p>
      </form>
    </div>
  </div>
</section>

</main>
<!--/ITC:main-->'''


KOPFBILD = {  # Unterseiten-Köpfe: eine Bildwelt (Stadien-Raum) statt Katalog-/Fremdteam-Fotos
    'trocknung.html': ('assets/media/kopf-trocknung.webp', 'Heller Raum während der technischen Trocknung: Kondenstrockner mit Kondensatschlauch im Eimer, Ventilator', 'Symbolbild'),
    'sanierung.html': ('assets/media/kopf-sanierung.webp', 'Derselbe Raum bei der Sanierung: neu verputzter Wandsockel, Abdeckvlies auf dem Boden', 'Symbolbild'),
    'ueber-uns.html': ('assets/media/kopf-fertig.webp', 'Fertig sanierter, heller Wohnraum mit Parkett und Sessel am Fenster', 'Symbolbild'),
}


def blattkopf(sec, datei):
    """Liest h1/Claim/Lead/Bild aus dem alten Hero ODER dem bereits erzeugten Blattkopf."""
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', sec, re.S).group(1)
    claim = re.search(r'<p class="(?:sp-claim|blattkopf-claim)">(.*?)</p>', sec, re.S)
    lead = re.search(r'<p class="hero-lead">(.*?)</p>', sec, re.S) or re.search(r'<p class="blattkopf-lead">(.*?)</p>', sec, re.S) or re.search(r'<div class="blattkopf-unten">\s*<div><p>(.*?)</p>', sec, re.S)
    img = re.search(r'<img src="([^"]+)" alt="([^"]*)"', sec)
    cur = re.search(r'<span class="cur">(.*?)</span>', sec) or re.search(r'<div class="titelzeile"><span>(.*?)</span>', sec)
    cur = cur.group(1)
    geraet = False
    if datei in KOPFBILD:
        src, alt, kennung = KOPFBILD[datei]
    else:
        src, alt, kennung = img.group(1), img.group(2), 'Symbolfoto'
    claim_html = f'<p class="blattkopf-claim">{claim.group(1)}</p>' if claim and datei != 'ueber-uns.html' else ''
    zelle1 = cur if datei != 'ueber-uns.html' else 'Unternehmen'
    return f'''<!--ITC:blattkopf-->
<section class="blattkopf inhalt" aria-labelledby="seitentitel">
  <div class="titelzeile"><span>{zelle1}</span><span>Gifhorn &amp; Region</span><a href="tel:{TEL}">24/7 Notruf {TEL_TXT}</a></div>
  <div class="blattkopf-raster">
    <div class="blattkopf-text">
      <h1 id="seitentitel">{h1}</h1>
      {claim_html}
      <p class="blattkopf-lead">{lead.group(1)}</p>
      <a class="textlink" href="index.html#anfrage">Schaden melden {ARROW}</a>
    </div>
    <figure class="blattkopf-bild"><img src="{src}" alt="{alt}" width="1500" height="1000" fetchpriority="high"><figcaption>{kennung}</figcaption></figure>
  </div>
</section>
<!--/ITC:blattkopf-->'''


KURZANFRAGE = f'''<!--ITC:kurzanfrage-->
<section class="kurzanfrage" aria-label="Anfrage">
  <div class="inhalt">
    <p>Jeder Schaden ist anders.</p>
    <a class="kurz-nr" href="tel:{TEL}">24/7 Notruf {TEL_TXT}</a>
    <a class="textlink" href="index.html#anfrage">Anfrage schreiben {ARROW}</a>
  </div>
</section>
<!--/ITC:kurzanfrage-->'''

WA_FAB = f'<!--ITC:fab--><a href="{WA}" class="wa-float" target="_blank" rel="noopener" aria-label="Per WhatsApp schreiben">{WA_SVG}</a><!--/ITC:fab-->'
SCRIPTS = '''<!--ITC:scripts-->
<script src="assets/js/gsap.min.js"></script>
<script src="assets/js/ScrollTrigger.min.js"></script>
<script src="assets/motion.js"></script>
<script src="script.js"></script>
<!--/ITC:scripts-->'''
HEADLINKS = '<!--ITC:fonts--><link rel="preload" href="assets/fonts/SourceSerif4-normal-latin.woff2" as="font" type="font/woff2" crossorigin>\n<link rel="stylesheet" href="assets/fonts.css"><!--/ITC:fonts-->'


def ersetze_block(s, name, neu, fallback_pattern=None):
    m = re.search(rf'<!--ITC:{name}-->.*?<!--/ITC:{name}-->', s, re.S)
    if m:
        return s[:m.start()] + neu + s[m.end():]
    if fallback_pattern:
        m = re.search(fallback_pattern, s, re.S)
        if m:
            return s[:m.start()] + neu + s[m.end():]
    raise SystemExit(f'Block {name} nicht gefunden')


def verarbeite(datei):
    p = SITE / datei
    s = p.read_text(encoding='utf-8')
    s = re.sub(r'<html lang="de"[^>]*>', '<html lang="de" data-motion="editorial">', s, count=1)
    # Kopf: Google Fonts raus, lokale Schriften rein
    s = re.sub(r'<link rel="preconnect" href="https://fonts\.(googleapis|gstatic)\.com"[^>]*>\n?', '', s)
    s = re.sub(r'<link href="https://fonts\.googleapis\.com[^>]*>\n?', '', s)
    if '<!--ITC:fonts-->' not in s:
        s = s.replace('<link rel="stylesheet" href="styles.css">', HEADLINKS + '\n<link rel="stylesheet" href="styles.css">', 1)
    # Rahmen öffnen: alter Header → Plankopf in .seite
    aktiv = datei if datei != 'index.html' else ''
    if '<!--ITC:plankopf-->' in s:
        s = ersetze_block(s, 'plankopf', plankopf(aktiv))
    else:
        s = re.sub(r'<header class="site-header[^"]*" data-header>.*?</header>',
                   lambda m: '<div class="seite">\n' + plankopf(aktiv) + '\n<div class="blatt">', s, count=1, flags=re.S)
    # Main
    if datei == 'index.html':
        s = ersetze_block(s, 'main', startseite_main(), r'<main>.*?</main>')
    elif datei not in ('impressum.html', 'datenschutz.html', 'agb.html'):
        if '<!--ITC:blattkopf-->' not in s:
            s = re.sub(r'<section class="hero">.*?</section>', lambda m: blattkopf(m.group(0), datei), s, count=1, flags=re.S)
            s = s.replace('<main>', '<main id="inhalt">', 1)
        else:
            m = re.search(r'<!--ITC:blattkopf-->.*?<!--/ITC:blattkopf-->', s, re.S)
            s = s[:m.start()] + blattkopf(m.group(0), datei) + s[m.end():]
        if '<!--ITC:kurzanfrage-->' in s:
            s = ersetze_block(s, 'kurzanfrage', KURZANFRAGE)
        else:
            s = re.sub(r'<section class="sp-cta-band">.*?</section>', lambda m: KURZANFRAGE, s, count=1, flags=re.S)
    else:
        s = s.replace('<main class="legal">', '<main class="legal" id="inhalt">', 1)
    # Footer → Lageplan, Rahmen schließen
    if '<!--ITC:lageplan-->' in s:
        s = ersetze_block(s, 'lageplan', lageplan())
    else:
        s = re.sub(r'<footer class="site-footer">.*?</footer>', lambda m: lageplan() + '\n</div>\n</div>', s, count=1, flags=re.S)
    # WhatsApp-Button + Skripte
    if '<!--ITC:fab-->' in s:
        s = ersetze_block(s, 'fab', WA_FAB)
    else:
        s = re.sub(r'(<!-- Floating WhatsApp -->\s*)?<a href="https://wa\.me/[^"]+" class="wa-float".*?</a>', lambda m: WA_FAB, s, count=1, flags=re.S)
    if '<!--ITC:scripts-->' in s:
        s = ersetze_block(s, 'scripts', SCRIPTS)
    else:
        s = re.sub(r'<script src="https://cdnjs[^<]*</script>\s*<script src="https://cdnjs[^<]*</script>\s*<script src="https://cdn\.jsdelivr[^<]*</script>\s*(<script src="assets/premium-media\.js"></script>\s*)?<script src="assets/motion\.js"></script>\s*<script src="script\.js"></script>',
                   lambda m: SCRIPTS, s, count=1, flags=re.S)
    p.write_text(s, encoding='utf-8')
    rest = [k for k in ('site-header', 'site-footer', 'fonts.googleapis', 'cdnjs', 'jsdelivr', 'sp-cta-band', 'class="hero"') if k in s]
    print(f'{datei:28s} ok' + (f'  ⚠ Reste: {rest}' if rest else ''))


if __name__ == '__main__':
    for d in ['index.html', 'leckageortung.html', 'trocknung.html', 'sanierung.html', 'energetische-beratung.html',
              'ueber-uns.html', 'impressum.html', 'datenschutz.html', 'agb.html']:
        verarbeite(d)
