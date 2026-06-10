/* TK Bewässerungstechnik — Seiten-Logik:
   Scroll-Spy-Aktivzustand · animierter Zonenplan (Signature) · Footer-Jahr.
   Läuft NACH assets/motion.js (nutzt window.gsap/ScrollTrigger + Lenis, falls vorhanden). */
(function () {
  'use strict';

  /* ---------- Footer-Jahr ---------- */
  var y = document.querySelector('[data-year]');
  if (y) { try { y.textContent = new Date().getFullYear(); } catch (e) {} }

  /* ---------- Scroll-Spy: aktiven Abschnitt markieren ---------- */
  var links = Array.prototype.slice.call(document.querySelectorAll('.spy-link[data-spy]'));
  if (links.length && 'IntersectionObserver' in window) {
    var map = {};
    links.forEach(function (a) {
      var id = a.getAttribute('href').slice(1);
      var sec = document.getElementById(id);
      if (sec) map[id] = a;
    });
    var current = null;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          if (current) current.classList.remove('active');
          var a = map[en.target.id];
          if (a) { a.classList.add('active'); current = a; }
        }
      });
    }, { rootMargin: '-45% 0px -50% 0px', threshold: 0 });
    Object.keys(map).forEach(function (id) { io.observe(document.getElementById(id)); });
  }

  /* ---------- Zonenplan-Signature: Wurfbögen fegen ein (mechanical) ---------- */
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var still = document.documentElement.getAttribute('data-motion') === 'still';
  var svg = document.querySelector('.zoneplan');
  var gsapOK = typeof window.gsap !== 'undefined' && typeof window.ScrollTrigger !== 'undefined';

  if (svg && gsapOK && !reduce && !still) {
    try {
      var fans = svg.querySelectorAll('.zp-fan');
      var heads = svg.querySelectorAll('.zp-heads circle');
      var anno = svg.querySelectorAll('.zp-valve,.zp-leader,.zp-t,.zp-tag,.zp-drip,.zp-emitters circle,.zp-scale path,.zp-north path');

      // Startzustände nur jetzt setzen (sonst bleibt der Plan sichtbar)
      gsap.set(fans, { strokeDasharray: 1, strokeDashoffset: 1, fillOpacity: 0 });
      gsap.set(heads, { attr: { r: 0 } });
      gsap.set(anno, { opacity: 0 });

      ScrollTrigger.create({
        trigger: svg,
        start: 'top 78%',
        once: true,
        onEnter: function () {
          var tl = gsap.timeline();
          tl.to(fans, { strokeDashoffset: 0, fillOpacity: 0.085, duration: 0.65, ease: 'power1.inOut', stagger: 0.12 })
            .to(heads, { attr: { r: 5.5 }, duration: 0.3, ease: 'power1.out', stagger: 0.05 }, 0.25)
            .to(anno, { opacity: 1, duration: 0.45, ease: 'power1.out', stagger: 0.012 }, 0.55);
        }
      });
    } catch (e) {
      // Failsafe: Plan voll sichtbar lassen
      var f = svg.querySelectorAll('.zp-fan,.zp-heads circle,.zp-valve,.zp-leader,.zp-t,.zp-tag,.zp-drip,.zp-emitters circle,.zp-scale path,.zp-north path');
      Array.prototype.forEach.call(f, function (el) { el.style.opacity = 1; });
    }
  }
})();
