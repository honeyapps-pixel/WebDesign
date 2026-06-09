/* Feengarten — Failsafe: falls die Motion-Engine nicht lädt, alles sichtbar schalten */
(function(){
  "use strict";
  window.addEventListener('load', function(){
    setTimeout(function(){
      if (!window.__motionReady){
        document.documentElement.classList.remove('anim');
        document.querySelectorAll('[data-reveal]').forEach(function(el){ el.style.opacity=1; el.style.transform='none'; el.style.clipPath='none'; });
      }
    }, 600);
  });
})();
