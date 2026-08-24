/* KFZ Mattes — Standort-Umschalter (2 Filialen Isenbüttel) */
(function () {
  'use strict';

  /* ---- Kontakt: Standort-Umschalter (2 Filialen Isenbüttel) ---- */
  var LOC = {
    list:     { addr: 'Liststraße 1, 38550 Isenbüttel', lat: 52.4369943, lon: 10.5709049 },
    wendehof: { addr: 'Am Wendehof 1, 38550 Isenbüttel', lat: 52.4369304, lon: 10.5708924 }
  };
  var tabs   = Array.prototype.slice.call(document.querySelectorAll('.loc-switch [role="tab"]'));
  var panels = { list: document.getElementById('loc-list'), wendehof: document.getElementById('loc-wendehof') };
  var iframe = document.getElementById('loc-iframe');
  var route  = document.getElementById('route-link');

  function bbox(c) {
    var dx = 0.015, dy = 0.007;
    return (c.lon - dx) + '%2C' + (c.lat - dy) + '%2C' + (c.lon + dx) + '%2C' + (c.lat + dy);
  }
  function select(key) {
    var c = LOC[key]; if (!c) return;
    tabs.forEach(function (t) {
      var on = t.getAttribute('data-loc') === key;
      t.setAttribute('aria-selected', on ? 'true' : 'false');
    });
    Object.keys(panels).forEach(function (k) {
      var on = k === key;
      panels[k].classList.toggle('active', on);
      if (on) { panels[k].removeAttribute('hidden'); } else { panels[k].setAttribute('hidden', ''); }
    });
    if (iframe) {
      iframe.src = 'https://www.openstreetmap.org/export/embed.html?bbox=' + bbox(c) +
        '&layer=mapnik&marker=' + c.lat + '%2C' + c.lon;
    }
    if (route) { route.href = 'https://www.google.com/maps/dir/?api=1&destination=' + encodeURIComponent(c.addr); }
  }
  tabs.forEach(function (t) {
    t.addEventListener('click', function () { select(t.getAttribute('data-loc')); });
    t.addEventListener('keydown', function (e) {
      if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
      e.preventDefault();
      var i = tabs.indexOf(t);
      var nx = e.key === 'ArrowRight' ? (i + 1) % tabs.length : (i - 1 + tabs.length) % tabs.length;
      tabs[nx].focus(); select(tabs[nx].getAttribute('data-loc'));
    });
  });
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
