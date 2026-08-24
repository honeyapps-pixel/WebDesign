/* Mobilitäts-Zentrum Mattes — Nav-Toggle + Header-Scrolled übernimmt assets/motion.js.
   Hier nur ein schlanker Fallback, falls die Engine nicht greift. */
(function () {
  'use strict';
  var t = document.querySelector('[data-nav-toggle]');
  var n = document.querySelector('[data-nav]');
  if (t && n && !t.dataset.bound) {
    t.dataset.bound = '1';
    t.addEventListener('click', function () {
      var open = n.classList.toggle('open');
      t.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    n.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { n.classList.remove('open'); t.setAttribute('aria-expanded', 'false'); });
    });
  }
})();

/* Karte erst auf Klick laden — bis dahin kein Kontakt zu OpenStreetMap (DSGVO) */
(function () {
  'use strict';
  document.querySelectorAll('[data-map-consent]').forEach(function (box) {
    var btn = box.querySelector('[data-map-load]');
    if (!btn) return;
    btn.addEventListener('click', function () {
      var f = document.createElement('iframe');
      f.src = box.dataset.mapSrc;
      f.title = box.dataset.mapTitle || 'Karte';
      f.loading = 'lazy';
      f.setAttribute('referrerpolicy', 'no-referrer');
      box.replaceWith(f);
    });
  });
})();
