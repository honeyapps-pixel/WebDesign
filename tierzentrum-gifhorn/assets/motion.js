/* Honeyapps Motion-Engine — geteilte Scroll-/Hero-Animationsschicht.
 * Lädt NACH den CDNs für GSAP, ScrollTrigger und Lenis (siehe _engine/README.md).
 * Hebt das Niveau jeder Seite, ohne sie zu homogenisieren: die KONKRETEN Effekte
 * werden pro Element per data-Attribut gewählt — UND der CHARAKTER der Bewegung
 * (Easing, Tempo, Distanz, Trigger, Stagger, erlaubtes Vokabular) pro Seite per
 * Motion-Persönlichkeit. So fühlt sich nicht jede Seite gleich an.
 *
 * Motion-Persönlichkeit per Attribut am <html>:
 *   <html data-motion="still | editorial | mechanical | kinetic | soft">
 *   FEHLT das Attribut → "editorial" (= bisheriges Verhalten, bit-genau).
 *   "still" = bewusst (fast) keine Scroll-Animation; Inhalte sofort sichtbar (Premium-Zurückhaltung).
 *
 * Steuerung per Markup (unverändert):
 *   [data-reveal]                 → Einblendung beim Scrollen (Default: fade-up)
 *   [data-reveal="left|right|scale|mask"]  → Variante
 *   [data-reveal="wipe-left|wipe-right"]   → Bild gleitet seitlich herein (Clip-Wipe + Drift)
 *   [data-reveal] style="--d:2"   → Stagger-Verzögerung (×Persona-Stagger)
 *   [data-reveal] style="--rx:140"→ Slide-Distanz px für left/right; --ry für up
 *   [data-parallax="0.2"]         → Scroll-Parallaxe (Faktor; +runter/−hoch)
 *   [data-hero-stagger] > *       → gestaffelter Hero-Entrance beim Laden
 *   [data-rotate="4.5"] > img     → Crossfade-Slideshow durch die Kindbilder (Sek.; CSS s. README)
 *   [data-hero-kenburns] img      → langsamer Ken-Burns-Zoom
 *   [data-tilt]                   → dezenter Maus-Tilt (Tiefe), Desktop only (nur bei Personas mit tilt)
 *   [data-count="1985"]          → Hochzählen (nur ECHTE Zahlen verwenden!)
 *
 * Vokabular-Gate: Nutzt eine Persona ein Reveal nicht (z. B. "mechanical" kein "wipe"),
 * fällt das Element sauber auf "up" zurück (inkl. Entfernen des Pre-Hide-Clips).
 */
(function () {
  'use strict';

  /* ---------- Motion-Persönlichkeiten ---------- */
  var EASE = {
    expoOut: function (t) { return Math.min(1, 1.001 - Math.pow(2, -10 * t)); }, // Lenis editorial/kinetic
    quartOut: function (t) { return 1 - Math.pow(1 - t, 4); },                   // Lenis soft
    quadOut: function (t) { return 1 - Math.pow(1 - t, 2); }                     // Lenis mechanical
  };
  var PERSONAS = {
    // editorial = exaktes bisheriges Verhalten (Default & Fallback). NICHT verändern.
    editorial: {
      lenis: { duration: 1.1, easing: EASE.expoOut },
      ease: 'power3.out', dur: { base: 0.9, mask: 1.0, wipe: 1.1 },
      dist: { y: 40, x: 48, scale: 0.92 }, start: 'top 86%', staggerStep: 0.08,
      vocab: ['up', 'left', 'right', 'scale', 'mask', 'wipe-left', 'wipe-right'],
      hero: { y: 28, dur: 0.9, ease: 'power3.out', stagger: 0.12, delay: 0.15 },
      kenburns: { from: 1.12, dur: 6, ease: 'power1.out' },
      counter: { dur: 1.6, ease: 'power2.out' }, tilt: true
    },
    still: { static: true, vocab: ['up'] }, // (fast) keine Bewegung — alles sofort sichtbar
    mechanical: {
      lenis: { duration: 0.7, easing: EASE.quadOut },
      ease: 'power1.inOut', dur: { base: 0.5, mask: 0.5, wipe: 0.5 },
      dist: { y: 24, x: 24, scale: 0.96 }, start: 'top 90%', staggerStep: 0.04,
      vocab: ['up', 'left', 'right'],
      hero: { y: 18, dur: 0.5, ease: 'power1.inOut', stagger: 0.05, delay: 0.1 },
      kenburns: { from: 1.06, dur: 5, ease: 'none' },
      counter: { dur: 1.0, ease: 'power1.out' }, tilt: false
    },
    kinetic: {
      lenis: { duration: 1.0, easing: EASE.expoOut },
      ease: 'back.out(1.6)', dur: { base: 0.7, mask: 0.7, wipe: 0.8 },
      dist: { y: 56, x: 64, scale: 0.88 }, start: 'top 82%', staggerStep: 0.06,
      vocab: ['up', 'left', 'right', 'scale'],
      hero: { y: 36, dur: 0.7, ease: 'back.out(1.6)', stagger: 0.08, delay: 0.12 },
      kenburns: { from: 1.14, dur: 6, ease: 'power1.out' },
      counter: { dur: 1.4, ease: 'power2.out' }, tilt: true
    },
    soft: {
      lenis: { duration: 1.4, easing: EASE.quartOut },
      ease: 'power2.out', dur: { base: 1.2, mask: 1.2, wipe: 1.3 },
      dist: { y: 28, x: 36, scale: 0.94 }, start: 'top 80%', staggerStep: 0.10,
      vocab: ['up', 'mask', 'wipe-left', 'wipe-right'],
      hero: { y: 24, dur: 1.2, ease: 'power2.out', stagger: 0.14, delay: 0.2 },
      kenburns: { from: 1.12, dur: 7, ease: 'power1.out' },
      counter: { dur: 1.8, ease: 'power2.out' }, tilt: false
    }
  };
  var persona = PERSONAS[document.documentElement.getAttribute('data-motion')] || PERSONAS.editorial;

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hasGSAP = typeof window.gsap !== 'undefined';
  var hasST = hasGSAP && typeof window.ScrollTrigger !== 'undefined';
  if (hasST) gsap.registerPlugin(ScrollTrigger);

  // "off" = keine Effekte: Reduced-Motion ODER bewusst stille Persona.
  var off = reduce || persona.static === true;

  /* ---------- Smooth Scroll (Lenis) ---------- */
  var lenis = null;
  if (!off && persona.lenis && typeof window.Lenis !== 'undefined') {
    lenis = new Lenis({ duration: persona.lenis.duration, easing: persona.lenis.easing, smoothWheel: true });
    if (hasST) {
      lenis.on('scroll', ScrollTrigger.update);
      gsap.ticker.add(function (time) { lenis.raf(time * 1000); });
      gsap.ticker.lagSmoothing(0);
    } else {
      function raf(t) { lenis.raf(t); requestAnimationFrame(raf); }
      requestAnimationFrame(raf);
    }
    // interne Anker-Links sanft scrollen
    document.querySelectorAll('a[href^="#"]').forEach(function (a) {
      a.addEventListener('click', function (e) {
        var id = a.getAttribute('href');
        if (id.length > 1 && document.querySelector(id)) { e.preventDefault(); lenis.scrollTo(id, { offset: -70 }); }
      });
    });
  }

  // Macht alle Reveal-Elemente sichtbar und nimmt die anim-Sperre weg (Failsafe).
  function revealAll() {
    document.documentElement.classList.remove('anim');
    document.querySelectorAll('[data-reveal]').forEach(function (el) {
      el.style.opacity = 1; el.style.transform = 'none'; el.style.clipPath = 'none';
    });
  }
  window.__motionReady = true; // Signal an den Inline-Failsafe: Engine läuft

  /* ---------- Reduced-Motion / stille Persona / fehlende Libs: alles sichtbar, keine Effekte ---------- */
  if (off || !hasGSAP || !hasST) {
    revealAll();
    initHeaderState();
    initMobileMenu();
    return;
  }
  // Ab hier Effekte — bei jedem Fehler nichts verschlucken, sondern sichtbar schalten.
  try {

  /* ---------- Reveal-Varianten beim Scrollen ---------- */
  var FROM = {
    up:    { y: persona.dist.y, opacity: 0 },
    left:  { x: -persona.dist.x, opacity: 0 },
    right: { x: persona.dist.x, opacity: 0 },
    scale: { scale: persona.dist.scale, opacity: 0 },
    mask:  { yPercent: 0, opacity: 1, clipPath: 'inset(0 0 100% 0)' },
    // Cinematischer Seiteneintritt: Bild „gleitet" + Clip-Wipe öffnet von der Kante.
    'wipe-left':  { xPercent: -6, opacity: 1, clipPath: 'inset(0 0 0 100%)' }, // öffnet links→rechts
    'wipe-right': { xPercent:  6, opacity: 1, clipPath: 'inset(0 100% 0 0)' }  // öffnet rechts→links
  };
  var CLIPPED = { mask: 1, 'wipe-left': 1, 'wipe-right': 1 };
  document.querySelectorAll('[data-reveal]').forEach(function (el) {
    var kind = el.getAttribute('data-reveal') || 'up';
    // Vokabular-Gate: nicht erlaubte Variante → "up". Pre-Hide-Clip entfernen, falls vorhanden.
    if (persona.vocab.indexOf(kind) < 0) {
      if (CLIPPED[kind]) el.style.clipPath = 'none';
      kind = 'up';
    }
    var cs = getComputedStyle(el);
    var d  = parseFloat(cs.getPropertyValue('--d')) || 0;
    var rx = parseFloat(cs.getPropertyValue('--rx')); // optionale Slide-Distanz (px)
    var ry = parseFloat(cs.getPropertyValue('--ry'));
    var from = Object.assign({}, FROM[kind] || FROM.up); // klonen, damit --rx/--ry nicht global wirken
    if (kind === 'left'  && !isNaN(rx)) from.x = -rx;
    if (kind === 'right' && !isNaN(rx)) from.x =  rx;
    if (kind === 'up'    && !isNaN(ry)) from.y =  ry;
    var delay = d * persona.staggerStep;
    var to;
    if (kind === 'mask')
      to = { clipPath: 'inset(0 0 0% 0)', duration: persona.dur.mask, ease: persona.ease, delay: delay };
    else if (kind === 'wipe-left' || kind === 'wipe-right')
      to = { xPercent: 0, clipPath: 'inset(0 0 0 0%)', duration: persona.dur.wipe, ease: persona.ease, delay: delay };
    else
      to = { x: 0, y: 0, scale: 1, opacity: 1, duration: persona.dur.base, ease: persona.ease, delay: delay };
    gsap.fromTo(el, from, Object.assign(to, {
      scrollTrigger: { trigger: el, start: persona.start, toggleActions: 'play none none none' }
    }));
  });

  /* ---------- Scroll-Parallaxe (mehrschichtige Tiefe) ---------- */
  document.querySelectorAll('[data-parallax]').forEach(function (el) {
    var f = parseFloat(el.getAttribute('data-parallax')) || 0.15;
    gsap.to(el, {
      yPercent: f * 100,
      ease: 'none',
      scrollTrigger: { trigger: el.closest('section') || el, start: 'top bottom', end: 'bottom top', scrub: true }
    });
  });

  /* ---------- Ken-Burns-Zoom (Hero-Bild) ---------- */
  document.querySelectorAll('[data-hero-kenburns] img, img[data-hero-kenburns]').forEach(function (img) {
    gsap.fromTo(img, { scale: persona.kenburns.from }, { scale: 1, duration: persona.kenburns.dur, ease: persona.kenburns.ease });
  });

  /* ---------- Hero-Entrance (gestaffelt beim Laden) ---------- */
  document.querySelectorAll('[data-hero-stagger]').forEach(function (wrap) {
    var kids = wrap.querySelectorAll(':scope > *');
    gsap.fromTo(kids, { y: persona.hero.y, opacity: 0 }, { y: 0, opacity: 1, duration: persona.hero.dur, ease: persona.hero.ease, stagger: persona.hero.stagger, delay: persona.hero.delay });
  });

  /* ---------- Bild-Rotator (Crossfade durch mehrere Bilder) ---------- */
  document.querySelectorAll('[data-rotate]').forEach(function (box) {
    var items = box.querySelectorAll(':scope > img, :scope > .rot-item');
    if (items.length < 2) return;
    var iv = (parseFloat(box.getAttribute('data-rotate')) || 4.5) * 1000;
    box.classList.add('js-rot');          // schaltet CSS-Crossfade-Modus ein
    var i = 0; items[0].classList.add('on');
    setInterval(function () {
      items[i].classList.remove('on');
      i = (i + 1) % items.length;
      items[i].classList.add('on');
    }, iv);
  });

  /* ---------- Dezenter Maus-Tilt (Tiefe), nur Desktop & nur bei Personas mit tilt ---------- */
  if (persona.tilt && window.innerWidth > 980) {
    document.querySelectorAll('[data-tilt]').forEach(function (el) {
      var qx = gsap.quickTo(el, 'rotationY', { duration: 0.6, ease: 'power3' });
      var qy = gsap.quickTo(el, 'rotationX', { duration: 0.6, ease: 'power3' });
      el.style.transformPerspective = '900px';
      el.addEventListener('mousemove', function (e) {
        var r = el.getBoundingClientRect();
        qx(((e.clientX - r.left) / r.width - 0.5) * 10);
        qy(((e.clientY - r.top) / r.height - 0.5) * -10);
      });
      el.addEventListener('mouseleave', function () { qx(0); qy(0); });
    });
  }

  /* ---------- Echte Zähler (NUR mit echten Zahlen einsetzen) ---------- */
  document.querySelectorAll('[data-count]').forEach(function (el) {
    var end = parseFloat(el.getAttribute('data-count')) || 0;
    var obj = { v: 0 };
    gsap.to(obj, {
      v: end, duration: persona.counter.dur, ease: persona.counter.ease,
      scrollTrigger: { trigger: el, start: 'top 90%' },
      onUpdate: function () { el.textContent = Math.round(obj.v).toLocaleString('de-DE'); }
    });
  });

  } catch (e) { revealAll(); }

  initHeaderState();
  initMobileMenu();

  /* ---------- Header: Hintergrund ab Scroll ---------- */
  function initHeaderState() {
    var header = document.querySelector('[data-header]') || document.querySelector('header');
    if (!header) return;
    function upd() { header.classList.toggle('scrolled', window.scrollY > 40); }
    upd(); window.addEventListener('scroll', upd, { passive: true });
  }

  /* ---------- Mobiles Menü ---------- */
  function initMobileMenu() {
    var t = document.querySelector('[data-nav-toggle]'); var n = document.querySelector('[data-nav]');
    if (!t || !n) return;
    t.addEventListener('click', function () {
      var open = n.classList.toggle('open');
      t.setAttribute('aria-expanded', open ? 'true' : 'false');
      t.setAttribute('aria-label', open ? 'Menü schließen' : 'Menü öffnen');
    });
    n.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', function () { n.classList.remove('open'); t.setAttribute('aria-expanded', 'false'); t.setAttribute('aria-label', 'Menü öffnen'); }); });
  }
})();
