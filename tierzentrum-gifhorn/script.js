/* Tierzentrum Gifhorn — Site-Script (Reveals/Header/Hero: _engine kinetic-Persona) */
(function () {
  var yr = document.getElementById('yr');
  if (yr) yr.textContent = new Date().getFullYear();

  // Overlay-Menü
  var overlay = document.querySelector('[data-overlay]');
  var openBtn = document.querySelector('[data-menu-open]');
  var closeBtn = document.querySelector('[data-menu-close]');
  function setMenu(open) {
    overlay.classList.toggle('open', open);
    overlay.setAttribute('aria-hidden', open ? 'false' : 'true');
    if (openBtn) openBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    document.body.style.overflow = open ? 'hidden' : '';
  }
  if (overlay && openBtn) {
    openBtn.addEventListener('click', function () { setMenu(true); });
    if (closeBtn) closeBtn.addEventListener('click', function () { setMenu(false); });
    overlay.querySelectorAll('.overlay__nav a').forEach(function (a) {
      a.addEventListener('click', function () { setMenu(false); });
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });
  }

  // Vorher/Nachher-Slider
  document.querySelectorAll('.ba').forEach(function (ba) {
    var range = ba.querySelector('[data-ba-range]');
    if (!range) return;
    function upd() { ba.style.setProperty('--w', range.value + '%'); }
    range.addEventListener('input', upd); upd();
  });

  // Interaktiver Kontakt-Picker
  var tabs = document.querySelectorAll('.picker__tab');
  var panels = document.querySelectorAll('.picker__panel');
  tabs.forEach(function (tab) {
    tab.addEventListener('click', function () {
      var area = tab.getAttribute('data-area');
      tabs.forEach(function (t) { t.classList.toggle('is-active', t === tab); t.setAttribute('aria-selected', t === tab ? 'true' : 'false'); });
      panels.forEach(function (p) { p.classList.toggle('is-active', p.getAttribute('data-panel') === area); });
    });
  });
})();
