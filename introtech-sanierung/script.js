/* InTroTech — seiteneigene Extras. Scroll-Reveals kommen aus assets/motion.js
   (geteilte Engine, ohne Lenis: die Leiste ist sticky). */
(function () {
  'use strict';

  var ruhig = window.matchMedia('(prefers-reduced-motion: reduce)');
  var sparen = navigator.connection && navigator.connection.saveData;

  // Aktuelles Jahr im Schriftfeld
  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();

  // ---- Plankopf: unter 1100 px Kopfleiste mit Menü-Panel von oben ----
  var leiste = document.querySelector('[data-plankopf]');
  var menue = document.querySelector('[data-menue]');
  var panel = document.getElementById('plankopf-panel');
  var schmal = window.matchMedia('(max-width: 1099px)');
  if (leiste && menue && panel) {
    var setze = function (offen) {
      leiste.classList.toggle('offen', offen);
      menue.setAttribute('aria-expanded', offen ? 'true' : 'false');
      menue.textContent = offen ? 'Schließen' : 'Menü';
      if (schmal.matches) {
        if (offen) panel.removeAttribute('inert'); else panel.setAttribute('inert', '');
      } else {
        panel.removeAttribute('inert');
      }
    };
    setze(false);
    menue.addEventListener('click', function () {
      var offen = !leiste.classList.contains('offen');
      setze(offen);
      if (offen) { var erster = panel.querySelector('a'); if (erster) erster.focus(); }
    });
    panel.addEventListener('click', function (ev) { if (ev.target.closest('a')) setze(false); });
    document.addEventListener('keydown', function (ev) {
      if (!leiste.classList.contains('offen')) return;
      if (ev.key === 'Escape') { setze(false); menue.focus(); return; }
      if (ev.key === 'Tab') {  // Fokusfalle im offenen Panel (inkl. Menü-Knopf)
        var ziele = [menue].concat([].slice.call(panel.querySelectorAll('a,button')));
        var a = ziele[0], z = ziele[ziele.length - 1];
        if (ev.shiftKey && document.activeElement === a) { ev.preventDefault(); z.focus(); }
        else if (!ev.shiftKey && document.activeElement === z) { ev.preventDefault(); a.focus(); }
      }
    });
    (schmal.addEventListener ? schmal.addEventListener.bind(schmal, 'change') : schmal.addListener.bind(schmal))(function () { setze(false); });
  }

  // ---- Einstieg: ein Raum, drei Stadien (Trocknung → Sanierung → fertig) ----
  // Ruhige Überblendung; sichtbar nur „Symbolbilder" + Pause-Knopf. Bei reduzierter
  // Bewegung oder Datensparmodus bleibt Bild 1 stehen, Bild 2/3 werden nicht geladen.
  var film = document.querySelector('[data-stadien]');
  if (film) {
    var bilder = [].slice.call(film.querySelectorAll('.stadium'));
    var pause = film.querySelector('[data-stadien-pause]');
    var TAKT = 5200, aktiv = 0, timer = null, angehalten = false, imBild = true, geladen = false;
    var darf = function () { return !ruhig.matches && !sparen; };
    var lade = function () {
      if (geladen) return; geladen = true;
      bilder.forEach(function (f) { var i = f.querySelector('img[data-src]'); if (i) { i.src = i.getAttribute('data-src'); i.removeAttribute('data-src'); } });
    };
    var zeige = function (i) {
      aktiv = (i + bilder.length) % bilder.length;
      bilder.forEach(function (b, k) { b.classList.toggle('ist-aktiv', k === aktiv); });
    };
    var stopp = function () { clearInterval(timer); timer = null; };
    var start = function () {
      stopp();
      if (pause) pause.hidden = !darf();
      if (!darf() || angehalten || !imBild || document.hidden) return;
      lade();
      timer = setInterval(function () { zeige(aktiv + 1); }, TAKT);
    };
    if (pause) {
      pause.addEventListener('click', function () {
        angehalten = !angehalten;
        pause.setAttribute('aria-label', angehalten ? 'Bildwechsel fortsetzen' : 'Bildwechsel anhalten');
        pause.innerHTML = angehalten
          ? '<svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor" aria-hidden="true"><path d="M7 5l12 7-12 7z"/></svg>'
          : '<svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor" aria-hidden="true"><rect x="6" y="5" width="4" height="14"/><rect x="14" y="5" width="4" height="14"/></svg>';
        start();
      });
    }
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (e) { imBild = e[0].isIntersecting; start(); }).observe(film);
    }
    document.addEventListener('visibilitychange', start);
    if (ruhig.addEventListener) ruhig.addEventListener('change', start);
    if (document.readyState === 'complete') start(); else window.addEventListener('load', start);
  }

  // ---- WhatsApp-Button tritt zurück, solange Einstieg/Blattkopf, Formular, Anfrage-Zeile
  // oder Schriftfeld sichtbar sind — dort gibt es WhatsApp bzw. Absenden schon.
  var fab = document.querySelector('.wa-float');
  var ziele = document.querySelectorAll('.titel-text, .kontakt-form, .kurzanfrage, .schriftfeld, .blattkopf');
  if (fab && ziele.length && 'IntersectionObserver' in window) {
    var sichtbar = new Set();
    var io = new IntersectionObserver(function (eintraege) {
      eintraege.forEach(function (en) { en.isIntersecting ? sichtbar.add(en.target) : sichtbar.delete(en.target); });
      fab.classList.toggle('zurueck', sichtbar.size > 0);
    });
    ziele.forEach(function (z) { io.observe(z); });
  }

  // ---- Conversion-Tracking-Hooks (für Google Ads / GA4) ----
  // Feuert NUR, wenn ein Google-Tag (gtag) geladen ist. Ohne gesetzte IDs passiert
  // nichts — so wird ohne Einwilligung/Setup kein Tracking ausgelöst (DSGVO).
  function track(action, label) {
    if (typeof window.gtag !== 'function') return;
    window.gtag('event', action, { event_category: 'kontakt', event_label: label });
  }
  document.querySelectorAll('a[href^="tel:"]').forEach(function (a) {
    a.addEventListener('click', function () { track('anruf', 'telefon'); });
  });
  document.querySelectorAll('a[href*="wa.me"]').forEach(function (a) {
    a.addEventListener('click', function () { track('whatsapp', 'whatsapp'); });
  });

  // Kontaktformular (Demo, kein Backend) — höflicher Hinweis statt stillem Nichts.
  var form = document.getElementById('kontaktForm');
  var note = document.getElementById('formNote');
  if (form && note) {
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      track('formular_absenden', 'kontaktformular');
      note.hidden = false;
      note.textContent = 'Danke! Dies ist eine Demo-Seite — bitte melden Sie sich direkt unter 05371 8759972 oder info@introtech.de. Im Notfall jederzeit telefonisch.';
    });
  }
})();
