/* Zahnärzte Bischoff — Scroll-Spy · Akkordeon · Impressum */
(function(){
  "use strict";

  /* ---- Header-Hintergrund ab Scroll (eigenständig, ohne Engine) ---- */
  var header = document.querySelector('[data-header]');
  if (header){
    var onScroll = function(){ header.classList.toggle('scrolled', window.scrollY > 40); };
    onScroll(); window.addEventListener('scroll', onScroll, { passive:true });
  }

  /* ---- Scroll-Spy ---- */
  var links = Array.prototype.slice.call(document.querySelectorAll('.spy a'));
  var map = {};
  links.forEach(function(a){ map[a.getAttribute('data-spy')] = a; });
  var sections = links.map(function(a){ return document.getElementById(a.getAttribute('data-spy')); }).filter(Boolean);
  if ('IntersectionObserver' in window && sections.length){
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if (e.isIntersecting){
          links.forEach(function(l){ l.classList.remove('active'); });
          var t = map[e.target.id];
          if (t) t.classList.add('active');
        }
      });
    }, { rootMargin: '-45% 0px -50% 0px', threshold: 0 });
    sections.forEach(function(s){ io.observe(s); });
  }

  /* ---- Akkordeon (single-open, height-animiert) ---- */
  var items = Array.prototype.slice.call(document.querySelectorAll('.acc-item'));
  function close(item){
    var p = item.querySelector('.acc-panel'), b = item.querySelector('.acc-head');
    p.style.height = p.scrollHeight + 'px';
    requestAnimationFrame(function(){ p.style.height = '0px'; });
    item.classList.remove('open'); b.setAttribute('aria-expanded','false');
  }
  function open(item){
    var p = item.querySelector('.acc-panel'), b = item.querySelector('.acc-head');
    p.style.height = p.scrollHeight + 'px';
    item.classList.add('open'); b.setAttribute('aria-expanded','true');
    p.addEventListener('transitionend', function te(){ if(item.classList.contains('open')) p.style.height='auto'; p.removeEventListener('transitionend',te); });
  }
  items.forEach(function(item){
    var b = item.querySelector('.acc-head');
    b.addEventListener('click', function(){
      var isOpen = item.classList.contains('open');
      items.forEach(function(o){ if(o!==item && o.classList.contains('open')) close(o); });
      if (isOpen) close(item); else open(item);
    });
  });

  /* ---- Reveal (still: nur Fade) ---- */
  if ('IntersectionObserver' in window){
    var ro = new IntersectionObserver(function(entries){
      entries.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('in'); ro.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    document.querySelectorAll('[data-reveal]').forEach(function(el){ ro.observe(el); });
  } else {
    document.querySelectorAll('[data-reveal]').forEach(function(el){ el.classList.add('in'); });
  }

  /* ---- Impressum-Overlay ---- */
  var panel = document.querySelector('[data-imprint-panel]');
  document.querySelectorAll('[data-imprint]').forEach(function(btn){
    btn.addEventListener('click', function(){ panel.hidden = !panel.hidden; });
  });
  if (panel){
    panel.addEventListener('click', function(e){ if(e.target === panel) panel.hidden = true; });
    document.addEventListener('keydown', function(e){ if(e.key === 'Escape') panel.hidden = true; });
  }
})();
