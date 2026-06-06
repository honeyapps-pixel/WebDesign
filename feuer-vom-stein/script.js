/* Feuer vom Stein — Interaktion
   Schlank: Scroll-Reveal, Header-Zustand, dezente Hero-Parallaxe, Mobil-Menü. */
(function () {
  'use strict';

  /* ---- Header: fest -> mit Hintergrund beim Scrollen ---- */
  var header = document.getElementById('header');
  var onScrollHeader = function () {
    if (window.scrollY > 40) header.classList.add('scrolled');
    else header.classList.remove('scrolled');
  };
  onScrollHeader();

  /* ---- Scroll-Reveal via IntersectionObserver ---- */
  var reveals = document.querySelectorAll('[data-reveal]');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add('is-visible');
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.14, rootMargin: '0px 0px -8% 0px' });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('is-visible'); });
  }

  /* ---- Dezente Hero-Parallaxe (nur Desktop, respektiert reduced-motion) ---- */
  var prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var parallax = document.querySelector('[data-parallax]');
  var ticking = false;
  function frame() {
    var y = window.scrollY;
    if (parallax && !prefersReduced && window.innerWidth > 980) {
      parallax.style.transform = 'translateY(' + (y * 0.045) + 'px)';
    }
    onScrollHeader();
    ticking = false;
  }
  window.addEventListener('scroll', function () {
    if (!ticking) {
      window.requestAnimationFrame(frame);
      ticking = true;
    }
  }, { passive: true });
  if (prefersReduced && parallax) parallax.style.transform = 'none';

  /* ---- Mobiles Menü ---- */
  var toggle = document.getElementById('navToggle');
  var nav = document.querySelector('.nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? 'Menü schließen' : 'Menü öffnen');
    });
    nav.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        nav.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.setAttribute('aria-label', 'Menü öffnen');
      });
    });
  }
})();
