/* BAUSCHULZ — Seitenlogik (läuft nach assets/motion.js).
 * 1 Drawer (von links, inert + Fokusfalle)  2 Bautagebuch (Bühne + Phasen-Leiste)
 * 3 Ablauf-Leiste  4 Streifen (Referenzen/Fotos)  5 Referenz-Karte (Leaflet, lazy)
 * 6 WhatsApp-Button tritt zurück  7 Anfrage-Formular (mailto)
 * Nur transform/opacity werden animiert; prefers-reduced-motion wird überall respektiert. */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------------------------------------------------------------- 1 · DRAWER */
  (function () {
    var drawer = $('[data-drawer]'), toggle = $('[data-drawer-toggle]');
    if (!drawer || !toggle) { return; }
    var panel = $('.drawer__panel', drawer), zuletzt = null;
    function fokusierbar() {
      return $$('a[href], button:not([disabled]), input, textarea, [tabindex]:not([tabindex="-1"])', panel).filter(function (el) { return el.offsetParent !== null; });
    }
    function oeffnen() {
      zuletzt = document.activeElement;
      drawer.removeAttribute('inert');
      drawer.classList.add('is-offen');
      document.body.classList.add('drawer-offen'); document.documentElement.classList.add('drawer-offen');
      toggle.setAttribute('aria-expanded', 'true');
      toggle.setAttribute('aria-label', 'Menü schließen');
      var f = fokusierbar(); if (f.length) { f[0].focus(); }
    }
    function schliessen() {
      drawer.classList.remove('is-offen');
      document.body.classList.remove('drawer-offen'); document.documentElement.classList.remove('drawer-offen');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.setAttribute('aria-label', 'Menü öffnen');
      drawer.setAttribute('inert', '');
      if (zuletzt && zuletzt.focus) { zuletzt.focus(); }
    }
    toggle.addEventListener('click', function () { drawer.classList.contains('is-offen') ? schliessen() : oeffnen(); });
    $$('[data-drawer-close]', drawer).forEach(function (el) { el.addEventListener('click', schliessen); });
    $$('a', panel).forEach(function (a) { a.addEventListener('click', schliessen); });
    document.addEventListener('keydown', function (e) {
      if (!drawer.classList.contains('is-offen')) { return; }
      if (e.key === 'Escape') { e.preventDefault(); schliessen(); return; }
      if (e.key !== 'Tab') { return; }
      var f = fokusierbar(); if (!f.length) { return; }
      var erste = f[0], letzte = f[f.length - 1];
      if (e.shiftKey && document.activeElement === erste) { e.preventDefault(); letzte.focus(); }
      else if (!e.shiftKey && document.activeElement === letzte) { e.preventDefault(); erste.focus(); }
    });
    window.matchMedia('(min-width: 881px)').addEventListener('change', function (m) { if (m.matches && drawer.classList.contains('is-offen')) { schliessen(); } });
  })();

  /* ---------------------------------------------------------------- 2 · BAUTAGEBUCH */
  (function () {
    var sek = $('[data-tagebuch]');
    if (!sek) { return; }
    var phasen = $$('.tb__phase', sek);
    var buehne = $('.tb__buehne', sek);
    var layerA = $('[data-layer="a"]', sek), layerB = $('[data-layer="b"]', sek);
    var plan = $('[data-plan]', sek);
    var fill = $('[data-tb-fill]', sek);
    var num = $('[data-tb-num]', sek), titel = $('[data-tb-titel]', sek);
    var ticks = $$('.tb__leiste li', sek);
    var gesamt = parseInt(sek.getAttribute('data-gesamt'), 10) || 16;
    if (!phasen.length || !buehne || !layerA || !('IntersectionObserver' in window)) { return; }
    var webpOk = (function () { var c = document.createElement('canvas'); return !!(c.getContext && c.getContext('2d')) && c.toDataURL('image/webp').indexOf('data:image/webp') === 0; })();
    var aktiv = layerA, passiv = layerB, aktuelleN = 1, ladeToken = 0;

    function bild(ph) { return webpOk ? (ph.getAttribute('data-webp') || ph.getAttribute('data-img')) : ph.getAttribute('data-img'); }
    function vorladen(i) {
      var n = phasen[i]; if (!n) { return; }
      var src = bild(n); if (!src) { return; }
      var im = new Image(); im.src = src;
    }
    function zeige(ph) {
      var n = parseInt(ph.getAttribute('data-n'), 10);
      if (n === aktuelleN) { return; }
      aktuelleN = n;
      var src = bild(ph);
      if (!src) {
        // Phase ohne Foto (Planung): Bauzeitenplan-Panel
        if (plan) { plan.classList.add('is-on'); }
      } else {
        if (plan) { plan.classList.remove('is-on'); }
        var token = ++ladeToken;
        var ziel = passiv, erledigt = false;
        var fertig = function () {
          if (erledigt || token !== ladeToken) { return; }
          erledigt = true; ziel.onload = null;
          ziel.classList.add('is-on');
          aktiv.classList.remove('is-on');
          var t = aktiv; aktiv = ziel; passiv = t;
        };
        if (ziel.getAttribute('src') === src && ziel.complete) { fertig(); }
        else {
          ziel.onload = fertig;
          ziel.src = src;
          if (ziel.complete && ziel.naturalWidth) { fertig(); }
        }
      }
      if (num) { num.textContent = (n < 10 ? '0' : '') + n; }
      if (titel) { titel.textContent = ph.getAttribute('data-titel') || ''; }
      ticks.forEach(function (li) { li.classList.toggle('is-on', parseInt(li.getAttribute('data-n'), 10) === n); });
      if (fill) { fill.style.setProperty('--p', String(n / gesamt)); }
      var idx = phasen.indexOf(ph);
      vorladen(idx + 1); vorladen(idx + 2);
    }
    // Erste Phase mit Foto vorbereiten, Planung = Panel an
    var erste = phasen[0];
    if (erste && !bild(erste) && plan) { plan.classList.add('is-on'); }
    else if (plan) { plan.classList.remove('is-on'); }
    var io = new IntersectionObserver(function (es) {
      // Die Phase, die die Mitte des Viewports kreuzt, bestimmt die Bühne.
      var kandidat = null;
      es.forEach(function (en) { if (en.isIntersecting) { kandidat = en.target; } });
      if (kandidat) { zeige(kandidat); }
    }, { rootMargin: '-45% 0px -45% 0px', threshold: 0 });
    phasen.forEach(function (ph) { io.observe(ph); });
    // Fallback: beim Laden die erste sichtbare Phase setzen
    var sichtbar = phasen.filter(function (ph) { var r = ph.getBoundingClientRect(); return r.top < window.innerHeight * .55 && r.bottom > window.innerHeight * .45; });
    if (sichtbar.length) { zeige(sichtbar[0]); }
    // Sprungmarken der Leiste: Versatz = Kopf (+ sticky Leiste auf Mobil); motion.js liest data-offset für Lenis,
    // ohne Lenis (Reduced-Motion) springt der eigene Handler. Auf Mobil sind die Balken rein dekorativ (kein Tab-Stopp).
    var links = $$('.tb__leiste a', sek);
    function versatz() {
      var mobil = window.innerWidth <= 880;
      var off = mobil ? ((buehne ? buehne.getBoundingClientRect().height : 60) + 84) : 90;
      links.forEach(function (a) { a.setAttribute('data-offset', String(off)); a.tabIndex = mobil ? -1 : 0; a.setAttribute('aria-hidden', mobil ? 'true' : 'false'); });
    }
    versatz(); window.addEventListener('resize', versatz);
    links.forEach(function (a) {
      a.addEventListener('click', function (e) {
        if (!reduce) { return; }
        var ziel = $(a.getAttribute('href'));
        if (!ziel) { return; }
        e.preventDefault();
        window.scrollTo({ top: ziel.getBoundingClientRect().top + window.scrollY - parseFloat(a.getAttribute('data-offset') || 90), behavior: 'auto' });
      });
    });
  })();

  /* ---------------------------------------------------------------- 3 · ABLAUF-LEISTE */
  (function () {
    var f = $$('[data-ablauf-fill]');
    if (!f.length) { return; }
    if (reduce || !('IntersectionObserver' in window)) { f.forEach(function (x) { x.classList.add('is-voll'); }); return; }
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('is-voll'); io.unobserve(en.target); } });
    }, { threshold: .4 });
    f.forEach(function (x) { io.observe(x); });
  })();

  /* ---------------------------------------------------------------- 4 · STREIFEN */
  $$('[data-strip]').forEach(function (strip) {
    var track = $('[data-strip-track]', strip), prev = $('[data-strip-prev]', strip), next = $('[data-strip-next]', strip), akt = $('[data-strip-akt]', strip);
    if (!track) { return; }
    var items = $$('.strip__item', track);
    function schritt() { var it = items[0]; return it ? it.getBoundingClientRect().width + parseFloat(getComputedStyle(track).columnGap || getComputedStyle(track).gap || 0) : 320; }
    function stand() {
      var max = track.scrollWidth - track.clientWidth - 2;
      if (prev) { prev.disabled = track.scrollLeft <= 2; }
      if (next) { next.disabled = track.scrollLeft >= max; }
      if (akt && items.length) {
        var i = Math.round(track.scrollLeft / schritt());
        i = Math.max(0, Math.min(items.length - 1, i));
        akt.textContent = (i + 1 < 10 ? '0' : '') + (i + 1);
      }
    }
    if (prev) { prev.addEventListener('click', function () { track.scrollBy({ left: -schritt(), behavior: reduce ? 'auto' : 'smooth' }); }); }
    if (next) { next.addEventListener('click', function () { track.scrollBy({ left: schritt(), behavior: reduce ? 'auto' : 'smooth' }); }); }
    var t; track.addEventListener('scroll', function () { clearTimeout(t); t = setTimeout(stand, 60); }, { passive: true });
    window.addEventListener('resize', stand);
    track.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { e.preventDefault(); track.scrollBy({ left: schritt(), behavior: reduce ? 'auto' : 'smooth' }); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); track.scrollBy({ left: -schritt(), behavior: reduce ? 'auto' : 'smooth' }); }
    });
    stand();
  });

  /* ---------------------------------------------------------------- 5 · REFERENZ-KARTE (Leaflet, lazy) */
  (function () {
    var box = $('[data-karte]');
    if (!box) { return; }
    var marker;
    try { marker = JSON.parse(box.getAttribute('data-marker') || '[]'); } catch (e) { marker = []; }
    if (!marker.length) { return; }
    var geladen = false;
    function css(href) { var l = document.createElement('link'); l.rel = 'stylesheet'; l.href = href; document.head.appendChild(l); }
    function js(src, cb) { var s = document.createElement('script'); s.src = src; s.async = true; s.onload = cb; s.onerror = function () { box.classList.add('is-fehler'); }; document.head.appendChild(s); }
    var GIEBEL = '<svg viewBox="0 0 270 270" aria-hidden="true"><path fill="#E88507" stroke="#353534" stroke-width="14" stroke-linejoin="round" d="M108 40h54l84 206h-50L135 96 74 246H24z"/></svg>';
    function baue() {
      if (!window.L) { return; }
      var hinweis = $('.karte__hinweis', box); if (hinweis) { hinweis.remove(); }
      var map = L.map(box, { scrollWheelZoom: false, zoomControl: true, attributionControl: true, tap: false });
      L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 18, attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>-Mitwirkende' }).addTo(map);
      var punkte = [];
      marker.forEach(function (m) {
        var icon = L.divIcon({ className: 'giebel-marker' + (m.sitz ? ' giebel-marker--sitz' : ''), html: GIEBEL, iconSize: [30, 30], iconAnchor: [15, 30], popupAnchor: [0, -28] });
        var mk = L.marker([m.lat, m.lon], { icon: icon, title: m.name, alt: m.name, keyboard: true, zIndexOffset: m.sitz ? 1000 : 0 }).addTo(map);
        var inhalt = '<b>' + m.name + '</b>' + m.ort + (m.sitz ? '' : '<br><a href="referenz-' + m.slug + '.html">Projekt ansehen →</a>');
        mk.bindPopup(inhalt, { closeButton: false, maxWidth: 240 });
        punkte.push([m.lat, m.lon]);
      });
      map.fitBounds(punkte, { padding: [48, 48], maxZoom: 11 });
      var ro; if ('ResizeObserver' in window) { ro = new ResizeObserver(function () { map.invalidateSize(); }); ro.observe(box); }
    }
    function lade() {
      if (geladen) { return; } geladen = true;
      css('https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css');
      js('https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.js', baue);
    }
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (es) { if (es.some(function (e) { return e.isIntersecting; })) { lade(); io.disconnect(); } }, { rootMargin: '500px 0px' });
      io.observe(box);
    } else { lade(); }
  })();

  /* ---------------------------------------------------------------- 6 · WHATSAPP-BUTTON TRITT ZURÜCK */
  (function () {
    var fab = $('.wa-fab');
    if (!fab || !('IntersectionObserver' in window)) { return; }
    // Generisch: jeder Textblock, jedes Bedienelement in main + Footer – der Knopf tritt zurück, sobald er etwas deckt.
    var ziele = $$('main p, main h1, main h2, main h3, main dt, main dd, main li, main label, main figcaption, main blockquote, main .btn, main summary, main input, main textarea, main .chronik-nav a, .tb__stand, .strip__nav, .karte, .karte__legende, .tb__leiste, .fuss__zeile, .fuss__index, .fuss__projekte, .fuss__legal, .drawer__fuss');
    if (!ziele.length) { return; }
    var drunter = new Set(), fest = false, io = null;
    function zeichne() { fab.classList.toggle('is-gedeckt', drunter.size > 0 && !fest); }
    function baue() {
      if (io) { io.disconnect(); drunter.clear(); }
      // Wurzel per negativem rootMargin exakt auf die Knopffläche geschrumpft (56 px + 16 px Rand).
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

  /* ---------------------------------------------------------------- 7 · ANFRAGE-FORMULAR (mailto) */
  (function () {
    var form = $('[data-form]');
    if (!form) { return; }
    var meldung = $('[data-form-meldung]', form);
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = $('#f-name', form), mail = $('#f-mail', form), betreff = $('#f-betreff', form), text = $('#f-text', form);
      var fehlt = [];
      if (!name.value.trim()) { fehlt.push(name); }
      if (!mail.value.trim() || mail.validity.typeMismatch) { fehlt.push(mail); }
      if (fehlt.length) {
        meldung.textContent = 'Bitte geben Sie Ihren Namen und eine gültige E-Mail-Adresse an.';
        meldung.hidden = false; fehlt[0].focus(); return;
      }
      var subj = (betreff.value.trim() || 'Anfrage über bauschulz.com');
      var body = 'Name: ' + name.value.trim() + '\nE-Mail: ' + mail.value.trim() + '\n\n' + (text.value.trim() || '(keine Nachricht)') + '\n';
      var href = 'mailto:info@bauschulz.com?subject=' + encodeURIComponent(subj) + '&body=' + encodeURIComponent(body);
      meldung.innerHTML = 'Ihr E-Mail-Programm öffnet sich mit der vorbereiteten Nachricht. Falls nicht: <a href="' + href + '">hier klicken</a> oder direkt an <a href="mailto:info@bauschulz.com">info@bauschulz.com</a> schreiben.';
      meldung.hidden = false;
      window.location.href = href;
    });
  })();

  /* ---------------------------------------------------------------- 8 · NAV: Abschnitt auf der Startseite markieren */
  (function () {
    var links = $$('.hnav a');
    if (!links.length || !/(^|\/)(index\.html)?$/.test(location.pathname)) { return; }
    var ziele = [['#leistungen', 'leistungen.html'], ['#bautagebuch', 'bautagebuch.html'], ['#referenzen', 'referenzen.html'], ['#betrieb', 'ueber-uns.html'], ['#kontakt', 'kontakt.html']];
    if (!('IntersectionObserver' in window)) { return; }
    var map = {};
    ziele.forEach(function (z) { var el = $(z[0]); if (el) { map[z[0]] = links.filter(function (a) { return a.getAttribute('href') === z[1]; })[0]; } });
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        var a = map['#' + en.target.id]; if (!a) { return; }
        a.classList.toggle('is-aktiv', en.isIntersecting);
      });
    }, { rootMargin: '-40% 0px -50% 0px', threshold: 0 });
    Object.keys(map).forEach(function (k) { var el = $(k); if (el && map[k]) { io.observe(el); } });
  })();
})();
