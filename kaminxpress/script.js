/* KaminXpress — Overlay-Menü · Slider · Video · Impressum */
(function(){
  "use strict";

  /* ---- Overlay-Fullscreen-Menü ---- */
  var overlay = document.getElementById('overlay');
  var open = document.getElementById('menuOpen');
  var close = document.getElementById('menuClose');
  function setMenu(o){
    if(o){ overlay.hidden=false; requestAnimationFrame(function(){ overlay.classList.add('open'); });
      document.body.style.overflow='hidden'; open.setAttribute('aria-expanded','true'); }
    else { overlay.classList.remove('open'); open.setAttribute('aria-expanded','false');
      document.body.style.overflow=''; setTimeout(function(){ overlay.hidden=true; },400); }
  }
  open.addEventListener('click', function(){ setMenu(true); });
  close.addEventListener('click', function(){ setMenu(false); });
  overlay.querySelectorAll('a').forEach(function(a){ a.addEventListener('click', function(){ setMenu(false); }); });
  document.addEventListener('keydown', function(e){ if(e.key==='Escape' && !overlay.hidden) setMenu(false); });

  /* ---- Ausstellung-Slider ---- */
  var slides = document.getElementById('slides');
  if (slides){
    var items = slides.children, n = items.length, i = 0;
    var dotsBox = document.getElementById('dots');
    for (var d=0; d<n; d++){
      var dot = document.createElement('button');
      dot.setAttribute('aria-label','Bild '+(d+1));
      (function(idx){ dot.addEventListener('click', function(){ go(idx); }); })(d);
      dotsBox.appendChild(dot);
    }
    var dots = dotsBox.children;
    function go(idx){
      i = (idx+n)%n;
      slides.style.transform = 'translateX(-'+(i*100)+'%)';
      slides.style.transition = 'transform .6s cubic-bezier(.4,.1,.2,1)';
      for (var k=0;k<n;k++) dots[k].classList.toggle('on', k===i);
    }
    document.querySelector('.s-next').addEventListener('click', function(){ go(i+1); });
    document.querySelector('.s-prev').addEventListener('click', function(){ go(i-1); });
    go(0);
    var auto = null;
    function play(){ if(window.matchMedia('(prefers-reduced-motion:reduce)').matches) return; auto = setInterval(function(){ go(i+1); }, 5200); }
    function stop(){ if(auto){ clearInterval(auto); auto=null; } }
    var sl = document.querySelector('.slider');
    sl.addEventListener('mouseenter', stop); sl.addEventListener('mouseleave', play);
    play();
  }

  /* ---- Video: bei Reduced-Motion pausieren, Poster zeigen ---- */
  var vid = document.getElementById('heroVid');
  if (vid && window.matchMedia('(prefers-reduced-motion:reduce)').matches){
    vid.removeAttribute('autoplay'); vid.pause();
  }

  /* ---- Impressum ---- */
  var panel = document.querySelector('[data-imprint-panel]');
  document.querySelectorAll('[data-imprint]').forEach(function(btn){ btn.addEventListener('click', function(){ panel.hidden = !panel.hidden; }); });
  if (panel){
    panel.addEventListener('click', function(e){ if(e.target===panel) panel.hidden=true; });
    document.addEventListener('keydown', function(e){ if(e.key==='Escape') panel.hidden=true; });
  }
})();
