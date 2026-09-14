/* ============================================================================
   KlimaTech38 — Seitenlogik (Redesign 2026-09-12)
   1) Overlay-Schaufenster (Menü)          2) Wege-Schalter (Signature, ein Zustand)
   3) Auslegungs-Rechner (Bühne)           4) Katalog-Filter (Kategorieseiten)
   5) Set anfragen → Kontaktformular       6) Produkt-Unterleiste (Set-Seiten)
   7) FAQ-Themenfilter                     8) WhatsApp-Button tritt zurück
   9) Karte lazy laden                    10) Kontaktformular (ohne Backend)
   Animation läuft getrennt in assets/motion.js (Persona "soft").
   Es werden keine Produktnamen, Preise oder Gerätedaten hier gepflegt — alles kommt aus
   assets/produkte.js (generiert aus .tools/kt38_katalog.py).
   ========================================================================== */
(function () {
  'use strict';
  var html = document.documentElement;
  var body = document.body;
  var KT = window.KT38 || { sets: [], meta: {} };
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function store(k, v) { try { if (v === null) { sessionStorage.removeItem(k); } else { sessionStorage.setItem(k, v); } } catch (e) { /* privater Modus */ } }
  function load(k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } }
  function de(n) { return n.toFixed(1).replace('.', ','); }
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }

  /* ---------------------------------------------------------------- 1 · OVERLAY */
  (function () {
    var toggle = $('[data-overlay-toggle]');
    var overlay = $('[data-overlay]');
    if (!toggle || !overlay) { return; }
    var main = $('main');
    var fuss = $('footer');
    var offen = false;
    var FOKUS = 'a[href], button:not([disabled]), input, select, textarea, [tabindex]:not([tabindex="-1"])';

    function setInert(an) {
      [main, fuss].forEach(function (el) { if (el) { if (an) { el.setAttribute('inert', ''); } else { el.removeAttribute('inert'); } } });
    }
    function open() {
      offen = true;
      overlay.classList.add('is-open');
      overlay.setAttribute('aria-hidden', 'false');
      body.classList.add('menu-open', 'is-locked');
      toggle.setAttribute('aria-expanded', 'true');
      toggle.setAttribute('aria-label', 'Menü schließen');
      setInert(true);
      if (window.__lenis) { window.__lenis.stop(); }
      var first = $(FOKUS, overlay);
      if (first) { first.focus({ preventScroll: true }); }
    }
    function close(fokusZurueck) {
      offen = false;
      overlay.classList.remove('is-open');
      overlay.setAttribute('aria-hidden', 'true');
      body.classList.remove('menu-open', 'is-locked');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.setAttribute('aria-label', 'Menü öffnen');
      setInert(false);
      if (window.__lenis) { window.__lenis.start(); }
      if (fokusZurueck !== false) { toggle.focus(); }
    }
    toggle.addEventListener('click', function () { offen ? close() : open(); });
    document.addEventListener('keydown', function (e) {
      if (!offen) { return; }
      if (e.key === 'Escape') { e.preventDefault(); close(); return; }
      if (e.key === 'Tab') {
        var f = $$(FOKUS, overlay).concat([toggle]);
        if (!f.length) { return; }
        var i = f.indexOf(document.activeElement);
        if (e.shiftKey && (i <= 0)) { e.preventDefault(); f[f.length - 1].focus(); }
        else if (!e.shiftKey && i === f.length - 1) { e.preventDefault(); f[0].focus(); }
      }
    });
    overlay.addEventListener('click', function (e) {
      var a = e.target.closest('a[href]');
      if (a && a.getAttribute('href').charAt(0) === '#') { close(false); }
    });
  })();

  /* ---------------------------------------------------------------- 2 · WEGE-SCHALTER */
  (function () {
    var gruppen = $$('[data-weg-schalter]');
    var start = html.getAttribute('data-weg') || 'montage';
    function setze(weg, merken) {
      html.setAttribute('data-weg', weg);
      gruppen.forEach(function (g) {
        $$('[data-weg]', g).forEach(function (b) { b.setAttribute('aria-checked', b.getAttribute('data-weg') === weg ? 'true' : 'false'); });
      });
      if (merken !== false) { store('kt38-weg', weg); }
      var ev; try { ev = new CustomEvent('kt38:weg', { detail: weg }); } catch (e) { ev = document.createEvent('Event'); ev.initEvent('kt38:weg', true, true); }
      document.dispatchEvent(ev);
    }
    setze(start, false);
    gruppen.forEach(function (g) {
      g.addEventListener('click', function (e) {
        var b = e.target.closest('[data-weg]');
        if (b) { setze(b.getAttribute('data-weg')); }
      });
      g.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
          e.preventDefault();
          setze(html.getAttribute('data-weg') === 'montage' ? 'selbst' : 'montage');
          var akt = $('[data-weg][aria-checked="true"]', g); if (akt) { akt.focus(); }
        }
      });
    });
  })();

  /* ---------------------------------------------------------------- 3 · RECHNER */
  (function () {
    var form = $('#rechner-form');
    var box = $('#raeume');
    if (!form || !box) { return; }
    var SPEZ = { neubau: 60, bestand: 80, altbau: 100, dach: 130 };
    var ZUSCHLAG = { sued: 20, hoch: 1.10, technik: 300 };
    var GLEICHZEITIG = 0.85;
    var GRENZE_KW = 6;
    var MIN_M2 = 5, MAX_M2 = 80, MAX_RAEUME = 5;
    var zaehler = 0;
    var ergebnis = { kw: 0, art: 'split', text: '', ueber: false };

    function raumZeile(flaeche, situation, titel) {
      zaehler += 1;
      var id = 'r' + zaehler;
      var li = document.createElement('li');
      li.className = 'raum';
      li.innerHTML =
        '<span class="raum__nr" aria-hidden="true"></span>' +
        '<div class="f f--flaeche"><label for="' + id + '-f">Fläche' + (titel ? ' · ' + titel : '') + '</label>' +
          '<div class="raum__flaeche"><input type="range" id="' + id + '-f" class="r-flaeche" min="' + MIN_M2 + '" max="' + MAX_M2 + '" step="1" value="' + flaeche + '">' +
          '<output for="' + id + '-f" class="r-out">' + flaeche + '<small>m²</small></output></div></div>' +
        '<div class="f f--situation"><label for="' + id + '-s">Raumsituation</label>' +
          '<select id="' + id + '-s" class="r-sit">' +
            '<option value="neubau">Neubau · gut gedämmt</option>' +
            '<option value="bestand">Bestand · normal</option>' +
            '<option value="altbau">Altbau · wenig gedämmt</option>' +
            '<option value="dach">Dachgeschoss</option></select></div>' +
        '<button type="button" class="raum__weg" aria-label="Raum entfernen">entfernen</button>' +
        '<div class="raum__zu" role="group" aria-label="Zuschläge">' +
          '<label><input type="checkbox" class="z-sued">große Süd-/Westfenster</label>' +
          '<label><input type="checkbox" class="z-hoch">über 2,60 m hoch</label>' +
          '<label><input type="checkbox" class="z-technik">Technik / offene Küche</label></div>';
      li.querySelector('.r-sit').value = situation || 'bestand';
      li.querySelector('.raum__weg').addEventListener('click', function () {
        if (box.children.length <= 1) { return; }
        li.remove(); nummeriere(); rechne();
      });
      return li;
    }
    function nummeriere() {
      $$('.raum', box).forEach(function (li, i) {
        li.querySelector('.raum__nr').textContent = (i + 1);
        li.querySelector('.raum__weg').disabled = box.children.length <= 1;
      });
      var plus = $('#raum-hinzu'); if (plus) { plus.hidden = box.children.length >= MAX_RAEUME; }
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

    function passendeSets(bedarfKw, anzahl, art) {
      return KT.sets.filter(function (s) {
        if (art === 'multi') { return s.kategorie === 'multi' && s.innengeraete >= anzahl; }
        if (art === 'mobil') { return s.kategorie === 'mobil'; }
        return s.kategorie === 'split';
      }).filter(function (s) { return s.kw >= bedarfKw - 0.35; })
        .sort(function (a, b) { return a.kw - b.kw; });
    }

    function karteAus(setId) {
      var tpl = $('template[data-set-tpl="' + setId + '"]');
      if (!tpl) { return null; }
      return tpl.content.firstElementChild.cloneNode(true);
    }

    var anzahl = 1;
    function zeichneTreffer(sets, art, satz, ueber) {
      var box2 = $('#treffer');
      if (!box2) { return; }
      box2.className = 'treffer' + (ueber ? ' treffer--grenze' : '');
      if (ueber) {
        box2.innerHTML = '<div class="treffer__b"><span class="chip chip--sky">über 6 kW</span><h4>Das legen wir vor Ort aus.</h4><p class="m2">' + satz + '</p>' +
          '<p class="treffer__cta"><a class="btn btn--hell btn--klein" href="beratung.html">Auslegung anfragen</a><a class="btn btn--rand-hell btn--klein" href="kontakt.html" id="rechner-anfrage">Rückruf mit Auslegung</a></p></div>';
      } else if (!sets.length) {
        box2.innerHTML = '<div class="treffer__b"><h4>Kein Set im Katalog passt genau.</h4><p class="m2">' + satz + '</p>' +
          '<p class="treffer__cta"><a class="btn btn--primary btn--klein" href="beratung.html">Beratung anfragen</a></p></div>';
      } else {
        var s = sets[0];
        var datei = art === 'multi' ? 'shop-multisplit.html' : art === 'mobil' ? 'shop-mobil.html' : 'shop-split.html';
        var weitere = sets.length > 1 ? '<a class="btn btn--rand btn--klein" href="' + datei + '">' + (sets.length - 1) + ' weitere' + (sets.length > 2 ? '' : 's') + ' Set' + (sets.length > 2 ? 's' : '') + '</a>' : '';
        box2.innerHTML = '<div class="treffer__b"><span class="chip">Dazu passt</span><h4>' + s.titel + '</h4><p class="m2">' + satz + '</p>' +
          '<p class="treffer__cta"><a class="btn btn--ink btn--klein" href="set-' + s.id + '.html">Set ansehen</a>' + weitere +
          '<a class="btn btn--rand btn--klein" href="kontakt.html" id="rechner-anfrage">Auslegung anfragen</a></p></div>';
        // Auf der Startseite wird die dritte Karte der Bestseller-Reihe zum Treffer.
        var slot = $('#treffer-karte');
        if (slot) {
          var k = karteAus(s.id);
          if (k) {
            var m2 = $$('.raum .r-flaeche', box).reduce(function (a, i) { return a + (parseInt(i.value, 10) || 0); }, 0);
            var label = anzahl > 1 ? 'Treffer für ' + anzahl + ' Räume' : 'Treffer für ' + m2 + ' m²';
            k.querySelector('.stage').insertAdjacentHTML('beforeend', '<span class="chip chip--best">' + label + '</span>');
            slot.innerHTML = ''; slot.appendChild(k);
          }
        }
      }
      var anfrage = $('#rechner-anfrage');
      if (anfrage) {
        anfrage.addEventListener('click', function () {
          store('kt38-anfrage', JSON.stringify({ typ: 'auslegung', quelle: 'rechner', kw: ergebnis.kw, bauart: ergebnis.art, text: ergebnis.text }));
        });
      }
    }

    function rechne() {
      var zeilen = $$('.raum', box);
      var summe = 0;
      zeilen.forEach(function (li) {
        summe += kwFuer(li);
        li.querySelector('.r-out').innerHTML = li.querySelector('.r-flaeche').value + '<small>m²</small>';
      });
      summe = Math.round(summe * 10) / 10;
      anzahl = zeilen.length;
      var aussen = anzahl > 1 ? Math.round(summe * GLEICHZEITIG * 10) / 10 : summe;
      var wunsch = (form.querySelector('input[name="art"]:checked') || {}).value || 'egal';
      var massgeblich = anzahl > 1 ? aussen : summe;

      $('#erg-kw').textContent = de(massgeblich);
      $('#erg-btu').textContent = btu(massgeblich).toLocaleString('de-DE');

      var art, satz;
      if (anzahl > 1) {
        art = 'multi';
        satz = 'Für ' + anzahl + ' Räume: ein Außengerät ab ' + de(aussen) + ' kW und ' + anzahl + ' Innengeräte.' +
          (wunsch === 'mobil' ? ' Ohne Bohren ginge das nur mit einem mobilen Gerät je Raum – laut, stromhungrig und in Summe meist teurer.' : '') +
          (wunsch === 'split' ? ' Einzelne Split-Anlagen je Raum gehen auch – dann hängen mehrere Außengeräte an der Fassade.' : '');
      } else if (wunsch === 'mobil') {
        art = 'mobil';
        satz = 'Ohne Eingriff in die Fassade bleibt das mobile Gerät. Es muss ' + de(summe) + ' kW abdecken – rechnen Sie mit deutlich mehr Nennleistung, weil der Abluftschlauch Leistung kostet.';
      } else {
        art = 'split';
        satz = 'Eine Split-Anlage mit mindestens ' + de(summe) + ' kW passt zu Ihrem Raum.' +
          (wunsch === 'multi' ? ' Multi-Split lohnt sich erst mit einem zweiten Raum – tragen Sie ihn ein.' : '') +
          (summe <= 1.6 ? ' Bei dieser kleinen Last käme auch ein mobiles Gerät infrage – die Split-Anlage ist leiser und sparsamer.' : '');
      }
      var ueber = massgeblich > GRENZE_KW;
      if (ueber) {
        satz = 'Ihr Bedarf liegt bei ' + de(massgeblich) + ' kW – darüber legen wir nicht nach Faustformel aus, sondern vor Ort. Zu große Anlagen takten und entfeuchten schlecht.';
      }
      var sets = ueber ? [] : passendeSets(massgeblich, anzahl, art);
      ergebnis.kw = massgeblich; ergebnis.art = art; ergebnis.ueber = ueber;
      ergebnis.text = 'Meine Auslegung über den Rechner:\n· ' + anzahl + (anzahl === 1 ? ' Raum' : ' Räume') +
        '\n· Kühllast gesamt ' + de(summe) + ' kW (' + btu(summe).toLocaleString('de-DE') + ' BTU/h)' +
        (anzahl > 1 ? ', Außengerät ab ' + de(aussen) + ' kW' : '') +
        '\n· Empfohlene Bauart: ' + ({ mobil: 'mobiles Monoblock-Gerät', split: 'Split-Anlage', multi: 'Multi-Split-Anlage' }[art]) +
        (ueber ? '\n· Über 6 kW – bitte vor Ort auslegen' : '') +
        (sets.length ? '\n· Passendes Set: ' + sets[0].titel : '');
      zeichneTreffer(sets, art, satz, ueber);
    }

    // Vorwahl aus dem Bento (Klick auf index) oder aus der Sitzung (von Unterseiten).
    function vorwahl(raum) {
      if (!raum || raum.key === 'frei') { return; }
      var erste = $('.raum', box);
      if (!erste) { return; }
      erste.querySelector('.r-sit').value = raum.situation || 'bestand';
      if (raum.flaeche) { erste.querySelector('.r-flaeche').value = raum.flaeche; }
      var lab = erste.querySelector('.f--flaeche label');
      if (lab && raum.titel) { lab.textContent = 'Fläche · ' + raum.titel; }
      rechne();
    }

    box.appendChild(raumZeile(24, 'bestand'));
    nummeriere();
    var plus = $('#raum-hinzu');
    if (plus) {
      plus.addEventListener('click', function () {
        if (box.children.length >= MAX_RAEUME) { return; }
        box.appendChild(raumZeile(18, 'bestand'));
        nummeriere(); rechne();
        var neu = box.lastElementChild.querySelector('.r-flaeche'); if (neu) { neu.focus({ preventScroll: true }); }
      });
    }
    form.addEventListener('input', rechne);
    form.addEventListener('change', rechne);
    form.addEventListener('submit', function (e) { e.preventDefault(); });

    $$('[data-raum]').forEach(function (k) {
      k.addEventListener('click', function () {
        var r = { key: k.getAttribute('data-raum'), situation: k.getAttribute('data-situation'), flaeche: parseInt(k.getAttribute('data-flaeche'), 10) || 0, titel: k.getAttribute('data-titel') };
        store('kt38-raum', JSON.stringify(r));
        vorwahl(r);
      });
    });
    var gemerkt = load('kt38-raum');
    if (gemerkt) { try { vorwahl(JSON.parse(gemerkt)); store('kt38-raum', null); } catch (e) { /* egal */ } }
    rechne();
  })();

  // Bento-Kacheln auf Unterseiten: Raum merken, dann zum Rechner auf der Startseite.
  (function () {
    if ($('#rechner-form')) { return; }
    $$('[data-raum]').forEach(function (k) {
      k.addEventListener('click', function () {
        store('kt38-raum', JSON.stringify({ key: k.getAttribute('data-raum'), situation: k.getAttribute('data-situation'), flaeche: parseInt(k.getAttribute('data-flaeche'), 10) || 0, titel: k.getAttribute('data-titel') }));
      });
    });
  })();

  /* ---------------------------------------------------------------- 4 · KATALOG-FILTER */
  (function () {
    var filter = $('#filter');
    var liste = $('#set-liste');
    if (!filter || !liste) { return; }
    var karten = $$('[data-set]', liste);
    var stand = $('#filter-stand');
    var leer = $('#filter-leer');

    function gewaehlt(name) { return $$('input[name="' + name + '"]:checked', filter).map(function (i) { return i.value.split('-').map(Number); }); }
    function inSpanne(spannen, von, bis) {
      if (!spannen.length) { return true; }
      return spannen.some(function (sp) { return von <= sp[1] && bis >= sp[0]; });
    }
    function filtere() {
      var fl = gewaehlt('flaeche'), pr = gewaehlt('preis');
      var einbau = $$('input[name="einbau"]:checked', filter).map(function (i) { return i.value; });
      var n = 0;
      karten.forEach(function (k) {
        var ok = inSpanne(fl, +k.getAttribute('data-flaeche-von'), +k.getAttribute('data-flaeche-bis')) &&
                 (!pr.length || pr.some(function (sp) { var p = +k.getAttribute('data-preis'); return p >= sp[0] && p <= sp[1]; })) &&
                 (!einbau.length || einbau.indexOf(k.getAttribute('data-einbau')) > -1);
        k.hidden = !ok; if (ok) { n += 1; }
      });
      if (stand) { stand.textContent = n + ' von ' + karten.length + ' Sets'; }
      if (leer) { leer.hidden = n > 0; }
      // Zustand in den Hash, damit der Link teilbar bleibt (#flaeche=32 aus dem Rechner wird gelesen).
      var teile = [];
      $$('input:checked', filter).forEach(function (i) { teile.push(i.name + '=' + i.value); });
      var h = teile.length ? '#' + teile.join('&') : ' ';
      if (history.replaceState) { history.replaceState(null, '', h === ' ' ? location.pathname : h); }
    }
    function lesHash() {
      var h = location.hash.replace('#', '');
      if (!h) { return; }
      h.split('&').forEach(function (t) {
        var kv = t.split('=');
        if (kv[0] === 'flaeche' && /^\d+$/.test(kv[1])) {
          var m2 = +kv[1];
          $$('input[name="flaeche"]', filter).forEach(function (i) { var sp = i.value.split('-').map(Number); if (m2 >= sp[0] && m2 <= sp[1]) { i.checked = true; } });
        } else {
          var inp = $('input[name="' + kv[0] + '"][value="' + kv[1] + '"]', filter); if (inp) { inp.checked = true; }
        }
      });
    }
    filter.addEventListener('change', filtere);
    filter.addEventListener('reset', function () { setTimeout(filtere, 0); });
    lesHash(); filtere();
  })();

  /* ---------------------------------------------------------------- 5 · SET ANFRAGEN → KONTAKT */
  (function () {
    $$('[data-set-anfragen]').forEach(function (a) {
      a.addEventListener('click', function () {
        var id = a.getAttribute('data-set-anfragen');
        var s = KT.sets.filter(function (x) { return x.id === id; })[0];
        if (!s) { return; }
        var weg = html.getAttribute('data-weg');
        var preis = weg === 'montage' && s.preise.montage_cent ? KT.eur(s.preise.montage_cent) + ' inkl. Montage' : KT.eur(s.preise.abholung_cent) + ' zur Abholung';
        store('kt38-anfrage', JSON.stringify({ typ: 'set', quelle: 'set-' + id + '.html', id: id, weg: weg,
          text: 'Ich interessiere mich für: ' + s.titel + ' (' + String(s.kw).replace('.', ',') + ' kW, ' + s.flaecheVon + '–' + s.flaecheBis + ' m²)\n· Weg: ' + (weg === 'montage' ? 'einbauen lassen' : 'selbst einbauen') + '\n· Preis laut Seite: ' + preis + (KT.meta.demo ? ' (Beispielpreis)' : '') }));
      });
    });
  })();

  /* ---------------------------------------------------------------- 6 · PRODUKT-UNTERLEISTE */
  (function () {
    var leiste = $('[data-unterleiste]');
    var kopf = $('.produkt-kopf');
    if (!leiste || !kopf || !('IntersectionObserver' in window)) { return; }
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        var da = !en.isIntersecting && en.boundingClientRect.top < 0;
        leiste.classList.toggle('is-da', da);
        leiste.setAttribute('aria-hidden', da ? 'false' : 'true');
      });
    }, { threshold: 0, rootMargin: '-90px 0px 0px 0px' });
    io.observe(kopf);
  })();

  /* ---------------------------------------------------------------- 7 · FAQ-THEMEN */
  (function () {
    var themen = $('#themen');
    var faq = $('#faq');
    if (!themen || !faq) { return; }
    themen.addEventListener('click', function (e) {
      var b = e.target.closest('button[data-thema]');
      if (!b) { return; }
      var t = b.getAttribute('data-thema');
      $$('button', themen).forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      $$('[data-thema-block]', faq).forEach(function (bl) { bl.hidden = !(t === 'alle' || bl.getAttribute('data-thema-block') === t); });
    });
  })();

  /* ---------------------------------------------------------------- 8 · WHATSAPP-BUTTON TRITT ZURÜCK */
  (function () {
    var fab = $('.wa-fab');
    if (!fab || !('IntersectionObserver' in window)) { return; }
    var ziele = $$('.preis-doppel, .pk__fuss, .abschluss, form.form, .unterleiste, .kontaktkarte, .treffer, .zub__preis, .hero__cta, .hero__fakten, .hero__wahl, .raum, .faq details, .karte-vb__map, .weg, .kanaele');
    if (!ziele.length) { return; }
    var drunter = new Set();
    var fest = false;
    function zeichne() { fab.classList.toggle('is-gedeckt', drunter.size > 0 && !fest); }
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        // Nur der untere rechte Viewport-Bereich zählt – dort sitzt der Knopf.
        var r = en.boundingClientRect;
        var trifft = en.isIntersecting && r.bottom > window.innerHeight - 120 && r.right > window.innerWidth - 140;
        if (trifft) { drunter.add(en.target); } else { drunter.delete(en.target); }
      });
      zeichne();
    }, { threshold: [0, 0.2, 0.5, 1] });
    ziele.forEach(function (z) { io.observe(z); });
    var t;
    window.addEventListener('scroll', function () {
      clearTimeout(t);
      t = setTimeout(function () { ziele.forEach(function (z) { io.unobserve(z); io.observe(z); }); }, 120);
    }, { passive: true });
    fab.addEventListener('focus', function () { fest = true; zeichne(); });
    fab.addEventListener('blur', function () { fest = false; zeichne(); });
  })();

  /* ---------------------------------------------------------------- 9 · KARTE LAZY */
  (function () {
    var m = $('[data-karte]');
    if (!m) { return; }
    function lade() {
      if (m.querySelector('iframe')) { return; }
      var f = document.createElement('iframe');
      f.src = m.getAttribute('data-src');
      f.title = 'Karte: Einzugsgebiet von KlimaTech38 rund um Gifhorn (OpenStreetMap)';
      f.loading = 'lazy';
      f.referrerPolicy = 'no-referrer-when-downgrade';
      m.innerHTML = ''; m.appendChild(f);
    }
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (es) { if (es.some(function (e) { return e.isIntersecting; })) { lade(); io.disconnect(); } }, { rootMargin: '400px 0px' });
      io.observe(m);
    } else { lade(); }
  })();

  /* ---------------------------------------------------------------- 10 · KONTAKTFORMULAR */
  (function () {
    var form = $('#anfrage');
    if (!form) { return; }
    var thema = $('#f-thema'), text = $('#f-text'), bezug = $('#bezug'), bezugText = $('#bezug-text');
    // Der Wege-Schalter waehlt das Thema vor, solange kein konkreter Bezug (Set/Auslegung) das Thema setzt.
    var themaFest = false;
    function themaAusWeg() {
      if (themaFest || !thema) { return; }
      var wunsch = html.getAttribute('data-weg') === 'selbst' ? 'Klimaanlage: Set anfragen' : 'Klimaanlage: Beratung';
      $$('option', thema).forEach(function (o) { if (o.textContent === wunsch) { thema.value = o.textContent; } });
    }
    document.addEventListener('kt38:weg', themaAusWeg);
    themaAusWeg();
    var roh = load('kt38-anfrage');
    if (roh) {
      try {
        var a = JSON.parse(roh);
        if (a && a.text) {
          if (text && !text.value) { text.value = a.text; }
          if (thema) {
            var wunsch = a.typ === 'set' ? 'Klimaanlage: Set anfragen' : 'Klimaanlage: Auslegung';
            $$('option', thema).forEach(function (o) { if (o.textContent === wunsch) { thema.value = o.textContent; } });
            themaFest = true;
          }
          if (bezug && bezugText) {
            bezugText.textContent = a.typ === 'set' ? 'Set ' + (a.id || '') + (a.weg ? ' · ' + (a.weg === 'montage' ? 'einbauen lassen' : 'selbst einbauen') : '') : 'Auslegung aus dem Rechner' + (a.kw ? ' · ' + de(a.kw) + ' kW' : '');
            bezug.hidden = false;
            $('#bezug-weg').addEventListener('click', function () { bezug.hidden = true; if (text) { text.value = ''; } store('kt38-anfrage', null); themaFest = false; themaAusWeg(); });
          }
        }
      } catch (e) { /* egal */ }
    }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var meldung = $('#form-meldung');
      var name = $('#f-name'), tel = $('#f-tel'), ds = $('#f-ds');
      var fehlt = [];
      if (!name.value.trim()) { fehlt.push('Ihren Namen'); }
      if (!tel.value.trim()) { fehlt.push('Ihre Telefonnummer'); }
      if (!ds.checked) { fehlt.push('die Zustimmung zur Datenschutzerklärung'); }
      if (fehlt.length) {
        meldung.textContent = 'Bitte ergänzen Sie ' + fehlt.join(', ') + '.';
        meldung.hidden = false; (fehlt[0].indexOf('Namen') > -1 ? name : fehlt[0].indexOf('Telefon') > -1 ? tel : ds).focus();
        return;
      }
      // Kein Backend in der Vorschau: Hinweis mit Direktkanälen. Vor Live an ein Postfach anbinden (README).
      meldung.innerHTML = 'Vielen Dank – das Formular ist in der Vorschau noch nicht angebunden. Rufen Sie uns an unter <a href="tel:+4953718759972">05371 8759972</a> oder schreiben Sie per <a href="https://wa.me/4953718759972" target="_blank" rel="noopener">WhatsApp</a>.';
      meldung.hidden = false;
      store('kt38-anfrage', null);
    });
  })();
})();
