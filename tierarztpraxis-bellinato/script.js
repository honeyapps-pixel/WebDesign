/* Tierarztpraxis Bellinato — Seiten-Interaktionen
   (Animationen kommen aus assets/motion.js — data-motion="soft") */
(function () {
  'use strict';

  /* ---- Jahr im Footer ---- */
  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();

  /* ---- Signature: Standort-Umschalter Wesendorf ⇄ Wittingen ---- */
  var sw = document.querySelector('.loc-switch');
  if (sw) {
    var buttons = Array.prototype.slice.call(sw.querySelectorAll('button[data-loc]'));
    var states = document.querySelectorAll('.loc-state');
    var maps = document.querySelectorAll('[data-map]');

    function activate(loc, focus) {
      sw.setAttribute('data-active', loc);
      buttons.forEach(function (b) {
        var sel = b.dataset.loc === loc;
        b.setAttribute('aria-selected', sel ? 'true' : 'false');
        b.tabIndex = sel ? 0 : -1;
        if (sel && focus) b.focus();
      });
      states.forEach(function (s) {
        var on = s.dataset.state === loc;
        s.classList.toggle('on', on);
        s.hidden = !on;
        if (on) { s.classList.remove('fade-swap'); void s.offsetWidth; s.classList.add('fade-swap'); }
      });
      maps.forEach(function (m) {
        m.style.display = m.dataset.map === loc ? 'block' : 'none';
      });
    }

    buttons.forEach(function (b, i) {
      b.addEventListener('click', function () { activate(b.dataset.loc); });
      b.addEventListener('keydown', function (e) {
        var dir = e.key === 'ArrowRight' || e.key === 'ArrowDown' ? 1
                : e.key === 'ArrowLeft' || e.key === 'ArrowUp' ? -1 : 0;
        if (!dir) return;
        e.preventDefault();
        var next = buttons[(i + dir + buttons.length) % buttons.length];
        activate(next.dataset.loc, true);
      });
    });
  }

  /* ---- Aktiver Nav-Punkt nach Sichtbarkeit ---- */
  var navLinks = Array.prototype.slice.call(document.querySelectorAll('.nav a[href^="#"]'));
  var sections = navLinks
    .map(function (a) { return document.querySelector(a.getAttribute('href')); })
    .filter(Boolean);

  if ('IntersectionObserver' in window && sections.length) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          var id = '#' + e.target.id;
          navLinks.forEach(function (a) {
            a.classList.toggle('active', a.getAttribute('href') === id);
          });
        }
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    sections.forEach(function (s) { spy.observe(s); });
  }

  /* ---- Mobil-Menü nach Klick schließen (motion.js öffnet/schließt) ---- */
  var nav = document.querySelector('[data-nav]');
  var toggle = document.querySelector('[data-nav-toggle]');
  if (nav && toggle) {
    nav.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        if (nav.classList.contains('open')) {
          nav.classList.remove('open');
          toggle.setAttribute('aria-expanded', 'false');
        }
      });
    });
  }
})();
