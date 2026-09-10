/* ============================================================================
   KlimaTech38 — Seitenlogik
   1) Auslegungs-Konfigurator (shop.html): Räume → Kühllast → passende Bauart
   2) Anfrageformular (kontakt.html): Prüfung + Übernahme der Auslegung
   3) WhatsApp-Button tritt zurück, wenn er etwas verdeckt
   Animation läuft getrennt in assets/motion.js (Persona "mechanical").
   Es werden bewusst KEINE Produktnamen, Preise oder Gerätedaten geführt —
   welches Gerät passt, steht im Angebot des Betriebs.
   ========================================================================== */

/* ---------------------------------------------------------------- 1 · KONFIGURATOR
   Der Rechenweg des Monteurs, offengelegt: Fläche × spezifische Kühllast, dazu die
   drei Zuschläge, die in der Praxis den Unterschied machen. Das Ergebnis filtert
   den Katalog vor (Blueprint: „Rechner filtert vorweg") und lässt sich in die
   Anfrage übernehmen. */
(function () {
  'use strict';
  var konf = document.getElementById('konfigurator');
  if (!konf) { return; }

  /* Spezifische Kühllast in Watt je m² — die Werte stehen sichtbar an den Zeilen
     und in der Fußnote, damit das Ergebnis nachvollziehbar bleibt. */
  var SPEZ = { neubau: 60, bestand: 80, altbau: 100, dach: 130 };
  /* Zuschläge (README/Blueprint): große Süd-/Westverglasung, hoher Raum, Technik. */
  var ZUSCHLAG = { sued: 20, hoch: 1.10, technik: 300 };
  /* Bei Multi-Split laufen selten alle Innengeräte gleichzeitig auf Volllast. */
  var GLEICHZEITIG = 0.85;
  /* Ab hier keine Selbstbedienung mehr, sondern Auslegung vor Ort. */
  var GRENZE_KW = 6;
  var SCHLUESSEL = 'kt38-anfrage';
  var MIN_M2 = 5, MAX_M2 = 80;

  var raeumeBox = document.getElementById('raeume');
  var zaehler = 0;

  function raumZeile(flaeche) {
    zaehler += 1;
    var li = document.createElement('li');
    li.className = 'raum';
    var id = 'r' + zaehler;
    li.innerHTML =
      '<span class="mono raum-nr">Raum ' + zaehler + '</span>' +
      '<div class="raum-f">' +
        '<label class="mono" for="' + id + '-z">Fläche</label>' +
        '<div class="raum-f-in">' +
          '<input type="range" class="r-slider" min="' + MIN_M2 + '" max="' + MAX_M2 + '" step="1" ' +
            'value="' + flaeche + '" aria-labelledby="' + id + '-l" tabindex="-1">' +
          '<span class="raum-f-zahl"><input type="number" id="' + id + '-z" min="' + MIN_M2 + '" max="' + MAX_M2 + '" ' +
            'step="1" value="' + flaeche + '" class="r-flaeche" inputmode="numeric"><b class="mono">m²</b></span>' +
        '</div>' +
      '</div>' +
      '<label class="raum-s"><span class="mono">Situation</span>' +
        '<select class="r-sit">' +
          '<option value="neubau">Neubau / gut gedämmt</option>' +
          '<option value="bestand" selected>Bestand / normal gedämmt</option>' +
          '<option value="altbau">Altbau / wenig gedämmt</option>' +
          '<option value="dach">Dachgeschoss unterm Dach</option>' +
        '</select></label>' +
      '<fieldset class="raum-z"><legend class="mono">Zuschläge</legend>' +
        '<label><input type="checkbox" class="z-sued"><span>Große Süd-/Westfenster</span></label>' +
        '<label><input type="checkbox" class="z-hoch"><span>Raumhöhe über 2,60 m</span></label>' +
        '<label><input type="checkbox" class="z-technik"><span>Technik / offene Küche</span></label>' +
      '</fieldset>' +
      '<span class="raum-kw"><span class="mono">Kühllast</span>' +
        '<b class="mono raum-kw-w">–</b></span>' +
      '<button type="button" class="raum-weg" aria-label="Raum entfernen">entfernen</button>';

    /* Schieber und Zahlenfeld halten sich gegenseitig aktuell. Programmatisches
       Setzen von .value feuert kein input-Event, also entsteht keine Schleife. */
    var slider = li.querySelector('.r-slider');
    var zahl = li.querySelector('.r-flaeche');
    slider.addEventListener('input', function () { zahl.value = slider.value; });
    zahl.addEventListener('input', function () {
      var v = Math.min(MAX_M2, Math.max(MIN_M2, parseInt(zahl.value, 10) || MIN_M2));
      slider.value = v;
    });

    li.querySelector('.raum-weg').addEventListener('click', function () {
      if (raeumeBox.children.length > 1) { li.remove(); nummeriere(); rechne(); }
    });
    return li;
  }

  function nummeriere() {
    Array.prototype.forEach.call(raeumeBox.children, function (li, n) {
      li.querySelector('.raum-nr').textContent = 'Raum ' + (n + 1);
      li.querySelector('.raum-weg').setAttribute('aria-label', 'Raum ' + (n + 1) + ' entfernen');
      li.querySelector('.raum-weg').disabled = raeumeBox.children.length < 2;
    });
    document.getElementById('raum-plus').hidden = raeumeBox.children.length >= 5;
  }

  function kwFuer(li) {
    var m2 = Math.min(MAX_M2, Math.max(MIN_M2, parseInt(li.querySelector('.r-flaeche').value, 10) || 20));
    var spez = SPEZ[li.querySelector('.r-sit').value] || 80;
    if (li.querySelector('.z-sued').checked) { spez += ZUSCHLAG.sued; }
    var w = m2 * spez;
    if (li.querySelector('.z-hoch').checked) { w *= ZUSCHLAG.hoch; }
    if (li.querySelector('.z-technik').checked) { w += ZUSCHLAG.technik; }
    return Math.round(w / 100) / 10;
  }

  function btu(kw) { return Math.round(kw * 3412.142 / 100) * 100; }
  function de(n) { return n.toFixed(1).replace('.', ','); }

  var letzte = null, letzteArt = null, letzteKw = 0;

  /* Die Kältekreis-Linie wird hier zur kW-Skala — dieselbe Haarlinie wie im Kopf
     und im Kontaktband. Bewegt wird nur per transform (Compositor). */
  function zeichneSkala(kw) {
    var zeiger = document.getElementById('k-zeiger');
    var fuell = document.getElementById('k-fuell');
    if (!zeiger || !fuell) { return; }
    var anteil = Math.min(1, kw / 10);
    zeiger.style.transform = 'translateX(' + (anteil * 100).toFixed(2) + '%)';
    fuell.style.transform = 'scaleX(' + anteil.toFixed(4) + ')';
  }

  function passendeSets(bedarfKw, anzahl, art) {
    if (!window.KT38 || !window.KT38.sets) { return []; }
    return window.KT38.sets.filter(function (s) {
      if (art === 'multi') { return s.kategorie === 'multi' && s.innengeraete >= anzahl; }
      if (art === 'mobil') { return s.kategorie === 'mobil'; }
      return s.kategorie === 'split';
    }).filter(function (s) {
      return s.kw >= bedarfKw - 0.35;
    }).sort(function (a, b) { return a.kw - b.kw; }).slice(0, 2);
  }

  function zeichneTreffer(sets) {
    var box = document.getElementById('k-treffer-sets');
    if (!box) { return; }
    if (!sets.length) { box.innerHTML = ''; box.hidden = true; return; }
    var eur = window.KT38 && window.KT38.eur ? window.KT38.eur : function (c) { return (c / 100) + ' €'; };
    var demo = window.KT38 && window.KT38.meta && window.KT38.meta.demo;
    box.innerHTML = '<p class="mono k-treffer-k">Dazu passt</p>' + sets.map(function (s) {
      var p2 = s.preise.montage_cent
        ? '<span class="set-p2">montiert ab ' + eur(s.preise.montage_cent) + '</span>' : '';
      return '<a class="k-set" href="set-' + s.id + '.html">' +
             '<span class="k-set-t"><b>' + s.titel + '</b>' +
             '<span class="mono">' + String(s.kw).replace('.', ',') + ' kW · ' +
             s.flaecheVon + '–' + s.flaecheBis + ' m²</span></span>' +
             '<span class="k-set-p"><b class="preis">' + eur(s.preise.abholung_cent) + '</b>' +
             (demo ? '<span class="preis-demo mono">Beispielpreis</span>' : '') + p2 + '</span></a>';
    }).join('');
    box.hidden = false;
  }

  function rechne() {
    var zeilen = Array.prototype.slice.call(raeumeBox.children);
    var summe = 0;
    zeilen.forEach(function (li) {
      var kw = kwFuer(li);
      summe += kw;
      li.querySelector('.raum-kw-w').textContent = de(kw) + ' kW';
    });
    summe = Math.round(summe * 10) / 10;
    var anzahl = zeilen.length;
    var aussen = anzahl > 1 ? Math.round(summe * GLEICHZEITIG * 10) / 10 : summe;
    var wunsch = (konf.querySelector('input[name="bauart"]:checked') || {}).value || 'egal';
    var massgeblich = anzahl > 1 ? aussen : summe;

    document.getElementById('k-raeume').textContent = anzahl;
    document.getElementById('k-summe').textContent = de(summe);
    document.getElementById('k-btu').textContent = btu(summe).toLocaleString('de-DE');
    document.getElementById('k-aussen').textContent = de(aussen);
    document.getElementById('k-aussen-zeile').hidden = anzahl < 2;
    zeichneSkala(massgeblich);

    /* Bauart aus Raumzahl und Wunsch ableiten — die Raumzahl schlägt den Wunsch,
       weil ein Gerät nun einmal nicht zwei Räume kühlt. */
    var art, satz, hinweis = '';
    if (anzahl > 1) {
      art = 'multi';
      satz = 'Für <b>' + anzahl + ' Räume</b> brauchen Sie eine <b>Multi-Split-Anlage</b>: ein Außengerät '
           + 'ab <b>' + de(aussen) + ' kW</b> und ' + anzahl + ' Innengeräte.';
      if (wunsch === 'mobil') {
        hinweis = 'Ohne Bohren geht das nur mit einem mobilen Gerät je Raum – laut, stromhungrig und '
                + 'in Summe meist teurer als eine feste Anlage.';
      } else if (wunsch === 'split') {
        hinweis = 'Einzelne Split-Anlagen je Raum gehen auch – dann hängen aber mehrere Außengeräte an der Fassade.';
      }
    } else if (wunsch === 'mobil') {
      art = 'mobil';
      satz = 'Ohne Eingriff in die Fassade bleibt das <b>mobile Monoblock-Gerät</b>. Es muss '
           + '<b>' + de(summe) + ' kW</b> abdecken – rechnen Sie beim Kauf mit '
           + 'deutlich mehr Nennleistung, weil der Abluftschlauch Leistung kostet.';
    } else if (wunsch === 'multi') {
      art = 'multi';
      satz = 'Für einen Raum reicht eine <b>Split-Anlage</b>. Multi-Split lohnt sich erst, wenn ein '
           + 'zweiter Raum dazukommt – tragen Sie ihn oben ein, dann rechnen wir mit.';
      art = 'split';
    } else {
      art = 'split';
      satz = 'Eine <b>Split-Anlage mit mindestens ' + de(summe) + ' kW</b> passt zu Ihrem Raum.';
      if (summe <= 1.6) {
        hinweis = 'Bei dieser kleinen Last käme auch ein mobiles Gerät in Frage – die Split-Anlage ist '
                + 'leiser und sparsamer, das mobile Gerät braucht keine Genehmigung.';
      }
    }

    /* Über der Grenze keine Selbstbedienung mehr — das ist eine Auslegungsfrage. */
    var ueberGrenze = massgeblich > GRENZE_KW;
    if (ueberGrenze) {
      satz = 'Ihr Bedarf liegt bei <b>' + de(massgeblich) + ' kW</b> – darüber legen wir nicht mehr '
           + 'nach Faustformel aus, sondern vor Ort. Zu große Anlagen takten und entfeuchten schlecht.';
      hinweis = '';
    }

    document.getElementById('k-satz').innerHTML = satz;
    var hw = document.getElementById('k-treffer');
    hw.textContent = hinweis;
    hw.hidden = !hinweis;

    zeichneTreffer(ueberGrenze ? [] : passendeSets(massgeblich, anzahl, art));

    /* Der Knopf führt in die gefilterte Kategorieseite, nicht mehr nur ins Formular. */
    var weiter = document.getElementById('k-weiter');
    if (weiter) {
      if (ueberGrenze) {
        weiter.hidden = true;
      } else {
        weiter.hidden = false;
        var datei = art === 'multi' ? 'shop-multisplit.html'
                  : art === 'mobil' ? 'shop-mobil.html' : 'shop-split.html';
        var groesste = zeilen.reduce(function (m, li) {
          var v = parseInt(li.querySelector('.r-flaeche').value, 10) || 0;
          return v > m ? v : m;
        }, 0);
        weiter.href = datei + '#flaeche=' + groesste;
        weiter.textContent = 'Passende Sets ansehen';
      }
    }

    var name = { mobil: 'mobiles Monoblock-Gerät', split: 'Split-Anlage', multi: 'Multi-Split-Anlage' }[art];
    letzteArt = art; letzteKw = massgeblich;
    letzte = 'Meine Auslegung über den Konfigurator:\n'
           + '· ' + anzahl + (anzahl === 1 ? ' Raum' : ' Räume') + '\n'
           + '· Kühllast gesamt ' + de(summe) + ' kW (' + btu(summe).toLocaleString('de-DE') + ' BTU/h)'
           + (anzahl > 1 ? ', Außengerät ab ' + de(aussen) + ' kW' : '') + '\n'
           + '· Empfohlene Bauart: ' + name
           + (ueberGrenze ? '\n· Über 6 kW – bitte vor Ort auslegen' : '');
  }

  raeumeBox.appendChild(raumZeile(24));
  nummeriere();
  document.getElementById('raum-plus').addEventListener('click', function () {
    if (raeumeBox.children.length >= 5) { return; }
    raeumeBox.appendChild(raumZeile(18));
    nummeriere(); rechne();
  });
  konf.addEventListener('input', rechne);
  konf.addEventListener('change', rechne);
  konf.addEventListener('submit', function (e) { e.preventDefault(); });

  /* Die Auslegung in die Anfrage übernehmen — über den Sitzungsspeicher,
     weil das Formular auf der Kontaktseite steht. */
  var anfrage = document.getElementById('k-anfrage');
  if (anfrage) {
    anfrage.addEventListener('click', function () {
      try {
        sessionStorage.setItem(SCHLUESSEL, JSON.stringify({
          typ: 'auslegung', quelle: 'konfigurator', kw: letzteKw, bauart: letzteArt,
          text: letzte || ''
        }));
      } catch (e) { /* privater Modus */ }
    });
  }
  rechne();
})();

/* ---------------------------------------------------------------- 2 · ANFRAGE */
(function () {
  'use strict';
  var form = document.getElementById('anfrage');
  if (!form) { return; }

  /* Einen übergebenen Bezug eintragen und danach verwerfen.
     Der Umschlag traegt beides: die Auslegung aus dem Rechner (typ 'auslegung')
     und ein angefragtes Set aus dem Katalog (typ 'set'). */
  var text = document.getElementById('f-text');
  try {
    var roh = sessionStorage.getItem('kt38-anfrage');
    if (roh && text) {
      var paket = null;
      try { paket = JSON.parse(roh); } catch (e2) { paket = { typ: 'auslegung', text: roh }; }
      if (paket && paket.text) {
        text.value = (text.value ? text.value + '\n\n' : '') + paket.text;
      }
      var thema = document.getElementById('f-thema');
      if (thema && paket && paket.typ) {
        Array.prototype.forEach.call(thema.options, function (o) {
          if (o.value === paket.typ) { thema.value = paket.typ; }
        });
      }
      /* Sichtbarer Bezug: der Nutzer soll sehen, was mitgekommen ist — und es
         wieder loswerden können, wenn er doch etwas anderes fragen will. */
      var bezug = document.getElementById('bezug');
      if (bezug && paket) {
        var erste = (paket.text || '').split('\n').filter(function (z) {
          return z.indexOf('·') === 0;
        });
        document.getElementById('bezug-t').textContent =
          erste.length ? erste.join(' · ').replace(/·\s·/g, '·') : (paket.text || '').split('\n')[0];
        bezug.hidden = false;
        var weg = document.getElementById('bezug-weg');
        if (weg) {
          weg.addEventListener('click', function () {
            bezug.hidden = true;
            if (paket.text) { text.value = text.value.replace(paket.text, '').trim(); }
          });
        }
      }
      sessionStorage.removeItem('kt38-anfrage');
    }
  } catch (e) { /* kein sessionStorage verfügbar */ }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var msg = document.getElementById('form-msg');
    var pflicht = [['f-name', 'Bitte tragen Sie Ihren Namen ein.'],
                   ['f-tel',  'Bitte tragen Sie eine Telefonnummer ein — wir rufen zurück.']];
    for (var i = 0; i < pflicht.length; i++) {
      var feld = document.getElementById(pflicht[i][0]);
      if (!feld.value.trim()) {
        msg.className = 'form-msg err'; msg.textContent = pflicht[i][1]; feld.focus(); return;
      }
    }
    if (!document.getElementById('f-ds').checked) {
      msg.className = 'form-msg err';
      msg.textContent = 'Bitte bestätigen Sie die Datenschutzerklärung.';
      document.getElementById('f-ds').focus(); return;
    }
    var zeit = form.querySelector('input[name="zeit"]:checked');
    if (zeit && zeit.value !== 'egal') {
      var wunsch = zeit.value === 'vormittag' ? 'vormittags (08–12 Uhr)' : 'nachmittags (12–18 Uhr)';
      if (text && text.value.indexOf('Rückruf bitte') === -1) {
        text.value = (text.value ? text.value + '\n\n' : '') + 'Rückruf bitte ' + wunsch + '.';
      }
    }
    msg.className = 'form-msg';
    msg.textContent = 'Demo-Hinweis: Dieses Formular ist noch nicht mit einem Postfach verbunden. '
                    + 'Rufen Sie uns bitte unter 05371 8759972 an oder schreiben Sie an info@introtech.de.';
  });
})();

/* ---------------------------------------------------------------- 3 · WHATSAPP-BUTTON
   Der Button steht fix unten rechts. In einspaltigen Layouts wandert früher oder
   später jedes vollbreite Element darunter — Preise, Formularfelder, sogar der
   Anruf-Knopf. Statt jeden Container mit Schutzabstand zu versehen, nimmt sich der
   Button selbst zurück, sobald etwas Wichtiges unter ihm liegt. Er bleibt sichtbar
   und anklickbar und kommt bei Hover/Fokus sofort zurück.
   Gemessen mit einem IntersectionObserver, dessen Wurzel per negativem rootMargin
   exakt auf die Button-Fläche geschrumpft ist — echte Flächenprüfung. */
(function () {
  'use strict';
  var fab = document.querySelector('.wa-fab');
  if (!fab || !window.IntersectionObserver) { return; }

  var WICHTIG = 'a[href],button,input,select,textarea,label,summary,details,' +
                '.kw-marks,.skala-marks,.b-a,.preis,.set-p2,.set-preis,.preis-demo,' +
                '.raum-kw,.konfig-werte,dd,th,caption';
  var SEITE = 56, RAND = 16;
  var beobachter = null, drunter = new Set(), festgehalten = false;

  function zeichne() { fab.classList.toggle('is-gedeckt', drunter.size > 0 && !festgehalten); }

  function aufbauen() {
    if (beobachter) { beobachter.disconnect(); }
    drunter.clear();
    var oben  = -(innerHeight - RAND - SEITE);
    var links = -(innerWidth  - RAND - SEITE);
    beobachter = new IntersectionObserver(function (eintraege) {
      eintraege.forEach(function (e) {
        if (e.isIntersecting) { drunter.add(e.target); } else { drunter.delete(e.target); }
      });
      zeichne();
    }, { rootMargin: oben + 'px ' + (-RAND) + 'px ' + (-RAND) + 'px ' + links + 'px', threshold: 0 });
    Array.prototype.forEach.call(document.querySelectorAll(WICHTIG), function (el) {
      if (!fab.contains(el)) { beobachter.observe(el); }
    });
  }

  var t;
  addEventListener('resize', function () { clearTimeout(t); t = setTimeout(aufbauen, 150); });
  fab.addEventListener('mouseenter', function () { festgehalten = true; zeichne(); });
  fab.addEventListener('mouseleave', function () { festgehalten = false; zeichne(); });
  fab.addEventListener('focus',      function () { festgehalten = true; zeichne(); });
  fab.addEventListener('blur',       function () { festgehalten = false; zeichne(); });
  aufbauen();
})();

/* ---------------------------------------------------------------- 4 · KOPF
   Mega-Menü (Desktop) und Panel (Mobil). Bewusst OHNE die generische
   initMobileMenu() aus assets/motion.js: die kennt weder `inert` noch eine
   Fokusfalle noch Escape. Die Engine bleibt unangetastet, die Logik steht hier.

   Auszeichnung: <nav> mit Links und Disclosure-Buttons — KEIN role="menu",
   das erzwingt Desktop-App-Pfeiltastensemantik, die hier falsch wäre. */
(function () {
  'use strict';
  var kopf = document.querySelector('.kopf');
  if (!kopf) { return; }

  var FOKUSSIERBAR = 'a[href],button:not([disabled]),input,select,textarea,[tabindex]:not([tabindex="-1"])';
  var feinzeiger = window.matchMedia('(hover:hover) and (pointer:fine)');

  /* ---------- Mega-Panels ---------- */
  var trigger = Array.prototype.slice.call(kopf.querySelectorAll('.hn-a[aria-controls]'));

  function panelVon(btn) { return document.getElementById(btn.getAttribute('aria-controls')); }

  function schliesse(btn, fokusZurueck) {
    var p = panelVon(btn);
    if (!p || p.hidden) { return; }
    p.hidden = true;
    btn.setAttribute('aria-expanded', 'false');
    var nochOffen = trigger.some(function (b) { return b.getAttribute('aria-expanded') === 'true'; });
    if (!nochOffen) { scrimAn(false); }
    if (fokusZurueck) { btn.focus(); }
  }

  function schliesseAlle(ausser) {
    trigger.forEach(function (b) { if (b !== ausser) { schliesse(b, false); } });
    if (!ausser) { scrimAn(false); }
  }

  /* Ein Scrim liegt unter dem offenen Panel: sonst schneidet die Panelkante
     mitten durch den Inhalt darunter. */
  var scrim = null;
  function scrimAn(an) {
    if (an && !scrim) {
      scrim = document.createElement('div');
      scrim.className = 'mega-scrim';
      document.body.appendChild(scrim);
    }
    document.documentElement.classList.toggle('mega-offen', !!an);
  }

  function oeffne(btn) {
    var p = panelVon(btn);
    if (!p) { return; }
    schliesseAlle(btn);
    p.hidden = false;
    btn.setAttribute('aria-expanded', 'true');
    scrimAn(true);
  }

  trigger.forEach(function (btn) {
    var p = panelVon(btn);
    if (!p) { return; }
    var li = btn.closest('.hn-i');
    var auf = null, zu = null;

    btn.addEventListener('click', function () {
      if (btn.getAttribute('aria-expanded') === 'true') { schliesse(btn, false); } else { oeffne(btn); }
    });

    /* Pfeil-ab springt aus dem geöffneten Auslöser in den ersten Link */
    btn.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        oeffne(btn);
        var erst = p.querySelector(FOKUSSIERBAR);
        if (erst) { erst.focus(); }
      }
    });

    /* Heraus-Tabben schließt — relatedTarget sagt, wohin der Fokus geht */
    li.addEventListener('focusout', function (e) {
      if (!e.relatedTarget || !li.contains(e.relatedTarget)) { schliesse(btn, false); }
    });

    /* Hover nur mit feinem Zeiger, mit Öffnungs-Absicht und Schließ-Karenz.
       aria-expanded läuft mit, damit optischer und semantischer Zustand nie auseinanderdriften. */
    if (feinzeiger.matches) {
      li.addEventListener('mouseenter', function () {
        clearTimeout(zu);
        auf = setTimeout(function () { oeffne(btn); }, 120);
      });
      li.addEventListener('mouseleave', function () {
        clearTimeout(auf);
        zu = setTimeout(function () { schliesse(btn, false); }, 220);
      });
    }
  });

  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') { return; }
    trigger.forEach(function (b) {
      if (b.getAttribute('aria-expanded') === 'true') { schliesse(b, true); }
    });
  });

  document.addEventListener('click', function (e) {
    if (!kopf.contains(e.target)) { schliesseAlle(null); }
  });

  /* ---------- Mobil-Panel (modal) ---------- */
  var burger = kopf.querySelector('.kopf-burger');
  var panel = document.getElementById('kopf-panel');

  if (burger && panel) {
    var zuBtn = panel.querySelector('.kopf-panel-zu');
    var wurzel = document.documentElement;

    function drumherum(anAus) {
      ['main', 'footer', '.wa-fab'].forEach(function (sel) {
        var el = document.querySelector(sel);
        if (!el) { return; }
        if (anAus) { el.setAttribute('inert', ''); } else { el.removeAttribute('inert'); }
      });
      var k = document.querySelector('.kopf-in');
      if (k) { if (anAus) { k.setAttribute('inert', ''); } else { k.removeAttribute('inert'); } }
    }

    function panelAuf() {
      schliesseAlle(null);
      panel.hidden = false;
      wurzel.classList.add('panel-offen');
      burger.setAttribute('aria-expanded', 'true');
      drumherum(true);
      /* Lenis scrollt sonst die Seite hinter dem Panel weiter */
      if (window.__lenis && window.__lenis.stop) { window.__lenis.stop(); }
      if (zuBtn) { zuBtn.focus(); }
    }

    function panelZu(fokusZurueck) {
      if (panel.hidden) { return; }
      panel.hidden = true;
      wurzel.classList.remove('panel-offen');
      burger.setAttribute('aria-expanded', 'false');
      drumherum(false);
      if (window.__lenis && window.__lenis.start) { window.__lenis.start(); }
      if (fokusZurueck) { burger.focus(); }
    }

    burger.addEventListener('click', function () {
      if (panel.hidden) { panelAuf(); } else { panelZu(true); }
    });
    if (zuBtn) { zuBtn.addEventListener('click', function () { panelZu(true); }); }

    panel.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { e.preventDefault(); panelZu(true); return; }
      if (e.key !== 'Tab') { return; }
      /* Fokusfalle: das Panel ist modal, der Fokus darf es nicht verlassen */
      var f = Array.prototype.filter.call(panel.querySelectorAll(FOKUSSIERBAR), function (el) {
        return el.offsetParent !== null;
      });
      if (!f.length) { return; }
      var erst = f[0], letzt = f[f.length - 1];
      if (e.shiftKey && document.activeElement === erst) { e.preventDefault(); letzt.focus(); }
      else if (!e.shiftKey && document.activeElement === letzt) { e.preventDefault(); erst.focus(); }
    });

    /* Ein Klick auf einen Link im Panel führt weg — Zustand vorher aufräumen */
    panel.addEventListener('click', function (e) {
      if (e.target.closest('a[href]')) { panelZu(false); }
    });

    /* Wird das Fenster breit genug für das Mega-Menü, muss das Panel weg */
    window.addEventListener('resize', function () {
      if (window.innerWidth >= 1180 && !panel.hidden) { panelZu(false); }
    });
  }

  /* ---------- Die Kältekreis-Linie füllt sich als Scroll-Fortschritt ----------
     Nur transform, kein width — das wäre Layout-Arbeit in jedem Frame. */
  var fort = document.getElementById('kopf-fort');
  if (fort && !window.matchMedia('(prefers-reduced-motion:reduce)').matches) {
    var offen = false;
    function zeichneFort() {
      offen = false;
      var doc = document.documentElement;
      var max = doc.scrollHeight - window.innerHeight;
      var p = max > 0 ? Math.min(1, Math.max(0, window.scrollY / max)) : 0;
      fort.style.transform = 'scaleX(' + p.toFixed(4) + ')';
    }
    window.addEventListener('scroll', function () {
      if (offen) { return; }
      offen = true;
      requestAnimationFrame(zeichneFort);
    }, { passive: true });
    zeichneFort();
  }
})();

/* ---------------------------------------------------------------- 5 · KATALOG-FILTER
   Facetten ohne Framework. UND zwischen den Gruppen, ODER innerhalb einer Gruppe.
   Geschaltet wird ueber `hidden`, nicht ueber eine Klasse: so verschwindet die Zeile
   auch aus dem A11y-Baum und aus der Browser-Suche. Es wird nicht umsortiert und
   nicht animiert — sonst wirkt die Trefferzahl traege und das Layout springt. */
(function () {
  'use strict';
  var liste = document.getElementById('katalog');
  var form = document.getElementById('facetten');
  if (!liste || !form) { return; }

  var zeilen = Array.prototype.slice.call(liste.querySelectorAll('.set-zeile'));
  var leer = document.getElementById('set-leer');
  var treffer = document.getElementById('fac-treffer');
  var reset = document.getElementById('fac-reset');
  var kaesten = Array.prototype.slice.call(form.querySelectorAll('input[data-f]'));
  var flaecheDirekt = null;   // numerischer Deep-Link, z. B. #flaeche=32

  function inSpanne(li, wert) {
    var von = parseInt(li.dataset.flVon, 10), bis = parseInt(li.dataset.flBis, 10);
    return wert >= von && wert <= bis;
  }

  function passtFlaeche(li, werte) {
    return werte.some(function (w) {
      var von = parseInt(li.dataset.flVon, 10), bis = parseInt(li.dataset.flBis, 10);
      if (w === 'bis-25') { return von <= 25; }
      if (w === '25-40') { return bis >= 25 && von <= 40; }
      if (w === '40-60') { return bis >= 40 && von <= 60; }
      if (w === 'ab-60') { return bis >= 60; }
      return true;
    });
  }

  function passtPreis(li, werte) {
    var p = parseInt(li.dataset.preis, 10);
    return werte.some(function (w) {
      if (w === 'bis-999') { return p < 100000; }
      if (w === '1000-1999') { return p >= 100000 && p < 200000; }
      if (w === 'ab-2000') { return p >= 200000; }
      return true;
    });
  }

  function gewaehlt() {
    var g = {};
    kaesten.forEach(function (k) {
      if (!k.checked) { return; }
      (g[k.dataset.f] = g[k.dataset.f] || []).push(k.value);
    });
    return g;
  }

  function filtere() {
    var g = gewaehlt();
    var sichtbar = 0;

    zeilen.forEach(function (li) {
      var ok = true;
      if (flaecheDirekt !== null && !inSpanne(li, flaecheDirekt)) { ok = false; }
      if (ok && g.flaeche && !passtFlaeche(li, g.flaeche)) { ok = false; }
      if (ok && g.raeume && g.raeume.indexOf(li.dataset.raeume) === -1) { ok = false; }
      if (ok && g.selbst && g.selbst.indexOf(li.dataset.selbst) === -1) { ok = false; }
      if (ok && g.preis && !passtPreis(li, g.preis)) { ok = false; }
      li.hidden = !ok;
      if (ok) { sichtbar += 1; }
    });

    if (leer) { leer.hidden = sichtbar > 0; }
    var aktiv = Object.keys(g).length > 0 || flaecheDirekt !== null;
    if (reset) { reset.hidden = !aktiv; }
    if (treffer) {
      treffer.textContent = aktiv
        ? sichtbar + ' von ' + zeilen.length + (zeilen.length === 1 ? ' Set' : ' Sets')
        : zeilen.length + (zeilen.length === 1 ? ' Set' : ' Sets');
    }
    schreibeHash(g);
  }

  function schreibeHash(g) {
    var teile = [];
    ['flaeche', 'raeume', 'selbst', 'preis'].forEach(function (k) {
      if (g[k]) { teile.push(k + '=' + g[k].join(',')); }
    });
    if (flaecheDirekt !== null) { teile.push('flaeche=' + flaecheDirekt); }
    var neu = teile.length ? '#' + teile.join('&') : window.location.pathname;
    /* replaceState statt pushState: sonst laeuft der Zurueck-Button durch jeden Klick */
    try { history.replaceState(null, '', neu); } catch (e) { /* file:// */ }
  }

  function lesHash() {
    flaecheDirekt = null;
    kaesten.forEach(function (k) { k.checked = false; });
    var h = window.location.hash.replace(/^#/, '');
    if (!h) { return; }
    h.split('&').forEach(function (paar) {
      var t = paar.split('=');
      if (t.length !== 2) { return; }
      var feld = t[0], werte = decodeURIComponent(t[1]).split(',');
      if (feld === 'flaeche' && werte.length === 1 && /^\d+$/.test(werte[0])) {
        flaecheDirekt = parseInt(werte[0], 10);
        return;
      }
      kaesten.forEach(function (k) {
        if (k.dataset.f === feld && werte.indexOf(k.value) > -1) { k.checked = true; }
      });
    });
  }

  form.addEventListener('change', function () { flaecheDirekt = null; filtere(); });
  form.addEventListener('submit', function (e) { e.preventDefault(); });
  if (reset) {
    reset.addEventListener('click', function () {
      kaesten.forEach(function (k) { k.checked = false; });
      flaecheDirekt = null;
      filtere();
    });
  }
  window.addEventListener('hashchange', function () { lesHash(); filtere(); });

  lesHash();
  filtere();
})();

/* ---------------------------------------------------------------- 6 · SET ANFRAGEN
   Kein Warenkorb: ein Set wird ANGEFRAGT. Der Umschlag im Sitzungsspeicher ist
   derselbe wie beim Rechner (Block 1) — ein Schluessel, ein Konsument (Block 2). */
(function () {
  'use strict';
  var knoepfe = document.querySelectorAll('[data-anfrage]');
  if (!knoepfe.length) { return; }

  Array.prototype.forEach.call(knoepfe, function (b) {
    b.addEventListener('click', function () {
      var id = b.dataset.anfrage;
      var variante = b.dataset.variante === 'montage' ? 'inklusive Montage' : 'zur Abholung';
      var s = null;
      if (window.KT38 && window.KT38.sets) {
        for (var i = 0; i < window.KT38.sets.length; i++) {
          if (window.KT38.sets[i].id === id) { s = window.KT38.sets[i]; break; }
        }
      }
      var text = 'Meine Anfrage zu einem Set:\n';
      if (s) {
        var cent = b.dataset.variante === 'montage' ? s.preise.montage_cent : s.preise.abholung_cent;
        text += '· ' + s.titel + ' (' + id + ')\n'
              + '· Variante: ' + variante + '\n'
              + '· Leistung: ' + String(s.kw).replace('.', ',') + ' kW für '
              + s.flaecheVon + '–' + s.flaecheBis + ' m²\n';
        if (cent && window.KT38.meta.demo) {
          text += '· Angezeigter Beispielpreis: ' + window.KT38.eur(cent)
                + ' (bitte verbindlich angeben)\n';
        } else if (cent) {
          text += '· Angezeigter Preis: ' + window.KT38.eur(cent) + '\n';
        }
      } else {
        text += '· Set-Kennung: ' + id + '\n· Variante: ' + variante + '\n';
      }

      try {
        sessionStorage.setItem('kt38-anfrage', JSON.stringify({
          typ: 'set', quelle: 'set-seite', id: id,
          variante: b.dataset.variante, text: text
        }));
      } catch (e) { /* privater Modus — dann traegt der Nutzer es selbst ein */ }
      window.location.href = 'kontakt.html#anfrage';
    });
  });
})();
