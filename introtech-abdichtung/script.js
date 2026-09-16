/* InTroTech Bauwerksabdichtung — Seitenlogik (ohne Abhängigkeiten).
   1 Diagnose-Schnitt: Hover/Fokus/Tap hebt die Stelle hervor, Mobil-Zuschnitt des Schnitts
   2 WhatsApp-FAB tritt zurück, sobald er etwas verdeckt (Hausregel, IntersectionObserver)
   3 Anfrageformular: mailto-Zusammenbau + Vorwahl der Stelle über ?stelle=NN */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------------------------------------------------------------- 1 · Diagnose-Schnitt */
  (function () {
    var svg = $('[data-schnitt="hero"]');
    var marker = svg ? $$('.mk', svg) : [];
    var VOLL = '0 160 1200 460', MOBIL = '300 195 720 425';
    function zuschnitt() {
      var mobil = window.innerWidth <= 700;
      var soll = mobil ? MOBIL : VOLL;
      if (svg && svg.getAttribute('viewBox') !== soll) { svg.setAttribute('viewBox', soll); }
      // Zeichnungs-Bänder: eigener Mobil-Zuschnitt (16:9) statt blindem Slice
      $$('.band[data-vb-mobil]').forEach(function (b) {
        var vb = mobil ? b.getAttribute('data-vb-mobil') : b.getAttribute('data-vb');
        if (b.getAttribute('viewBox') !== vb) { b.setAttribute('viewBox', vb); }
      });
    }
    zuschnitt();
    var t; window.addEventListener('resize', function () { clearTimeout(t); t = setTimeout(zuschnitt, 120); });

    if (!svg) { return; }
    function aktiv(nr) {
      if (nr) { svg.setAttribute('data-active', nr); } else { svg.removeAttribute('data-active'); }
      marker.forEach(function (m) { m.classList.toggle('is-aktiv', m.getAttribute('data-stelle') === nr); });
    }
    marker.forEach(function (m) {
      var nr = m.getAttribute('data-stelle');
      m.addEventListener('mouseenter', function () { aktiv(nr); });
      m.addEventListener('mouseleave', function () { aktiv(null); });
      m.addEventListener('focus', function () { aktiv(nr); });
      m.addEventListener('blur', function () { aktiv(null); });
      // Tastatur: Enter/Space folgt dem Sprunglink (SVG-<a> reagiert nicht überall auf Space)
      m.addEventListener('keydown', function (e) {
        if (e.key === ' ') { e.preventDefault(); location.hash = m.getAttribute('href'); }
      });
    });
    // Legende spiegelt in den Schnitt: Hover auf einen Legenden-Eintrag hebt die Stelle hervor
    $$('.legende__liste a').forEach(function (a) {
      var nr = (a.getAttribute('href') || '').replace('#stelle-', '');
      a.addEventListener('mouseenter', function () { aktiv(nr); });
      a.addEventListener('mouseleave', function () { aktiv(null); });
      a.addEventListener('focus', function () { aktiv(nr); });
      a.addEventListener('blur', function () { aktiv(null); });
    });
  })();

  /* ---------------------------------------------------------------- 2 · WhatsApp-FAB tritt zurück */
  (function () {
    var fab = $('.wa-fab');
    if (!fab || !('IntersectionObserver' in window)) { return; }
    var ziele = $$('main p, main h1, main h2, main h3, main dt, main dd, main li, main label, main figcaption, main .btn, main input, main textarea, main button, main .anruf__tel, main .weiter, main .leiste__nav, main .leiste, #schnitt .mk, .fuss__zeile');
    if (!ziele.length) { return; }
    var drunter = new Set(), fest = false, io = null;
    function zeichne() { fab.classList.toggle('is-gedeckt', drunter.size > 0 && !fest); }
    function baue() {
      if (io) { io.disconnect(); drunter.clear(); }
      var w = window.innerWidth, h = window.innerHeight;
      var rm = '-' + Math.max(0, h - 96) + 'px -8px -8px -' + Math.max(0, w - 88) + 'px';
      io = new IntersectionObserver(function (es) {
        es.forEach(function (en) { if (en.isIntersecting) { drunter.add(en.target); } else { drunter.delete(en.target); } });
        zeichne();
      }, { rootMargin: rm, threshold: 0 });
      ziele.forEach(function (z) { io.observe(z); });
    }
    baue();
    var t; window.addEventListener('resize', function () { clearTimeout(t); t = setTimeout(baue, 150); });
    fab.addEventListener('focus', function () { fest = true; zeichne(); });
    fab.addEventListener('blur', function () { fest = false; zeichne(); });
  })();

  /* ---------------------------------------------------------------- 3 · Anfrageformular */
  (function () {
    var form = $('[data-form]');
    if (!form) { return; }
    // Vorwahl der Stelle aus der URL (kontakt.html?stelle=05) – nur die Checkbox, kein Kanalwechsel
    var m = /[?&]stelle=(\d\d)/.exec(location.search);
    if (m) {
      var box = $('input[name="stelle"][value^="' + m[1] + ' "]', form);
      if (box) { box.checked = true; }
    }
    var meldung = $('[data-form-meldung]', form);
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = $('#f-name', form), tel = $('#f-tel', form), ort = $('#f-ort', form), text = $('#f-text', form);
      var fehlt = [];
      if (!name.value.trim()) { fehlt.push(name); }
      if (!tel.value.trim()) { fehlt.push(tel); }
      if (fehlt.length) {
        meldung.textContent = 'Bitte geben Sie Ihren Namen und eine Telefonnummer für den Rückruf an.';
        meldung.hidden = false; fehlt[0].focus(); return;
      }
      meldung.hidden = true;
      var stellen = $$('input[name="stelle"]:checked', form).map(function (i) { return i.value; });
      var subj = 'Besichtigung Bauwerksabdichtung' + (stellen.length ? ' – Stelle ' + stellen.map(function (s) { return s.slice(0, 2); }).join(', ') : '');
      var body = 'Name: ' + name.value.trim() + '\nTelefon: ' + tel.value.trim() + '\nPLZ/Ort: ' + (ort.value.trim() || '–') +
        '\nWo ist es feucht: ' + (stellen.length ? stellen.join('; ') : 'nicht angegeben') +
        '\n\nBeobachtung:\n' + (text.value.trim() || '(keine Angabe)') + '\n';
      location.href = 'mailto:' + form.getAttribute('action').replace('mailto:', '') + '?subject=' + encodeURIComponent(subj) + '&body=' + encodeURIComponent(body);
    });
  })();
})();
