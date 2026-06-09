/* DAVID Partyservice — Seiten-Interaktionen */
(function () {
  'use strict';
  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();

  /* Buffet-Strecke: Pfeil-Steuerung (Signature E) */
  var track = document.querySelector('[data-strecke-track]');
  if (track) {
    function step() {
      var card = track.querySelector('.buffet');
      var gap = parseFloat(getComputedStyle(track).columnGap || getComputedStyle(track).gap || 24) || 24;
      return card ? card.getBoundingClientRect().width + gap : 380;
    }
    document.querySelectorAll('[data-strecke]').forEach(function (b) {
      b.addEventListener('click', function () {
        track.scrollBy({ left: step() * parseInt(b.dataset.strecke, 10), behavior: 'smooth' });
      });
    });
  }

  /* Aktiver Nav-Punkt */
  var links = Array.prototype.slice.call(document.querySelectorAll('.nav a[href^="#"]'));
  var sections = links.map(function (a) { return document.querySelector(a.getAttribute('href')); }).filter(Boolean);
  if ('IntersectionObserver' in window && sections.length) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          var id = '#' + e.target.id;
          links.forEach(function (a) { a.classList.toggle('active', a.getAttribute('href') === id); });
        }
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    sections.forEach(function (s) { spy.observe(s); });
  }
})();
