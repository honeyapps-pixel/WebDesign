/* Ballettschule Franz Wagner — Seiten-Interaktionen */
(function () {
  'use strict';
  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();

  // Aktiver Nav-Punkt (Sidebar + Drawer) nach Sichtbarkeit
  var links = Array.prototype.slice.call(document.querySelectorAll('.side-nav a[href^="#"], .drawer a[href^="#"]'));
  var ids = {};
  links.forEach(function (a) { ids[a.getAttribute('href')] = true; });
  var sections = Object.keys(ids)
    .map(function (h) { return document.querySelector(h); })
    .filter(Boolean);

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
