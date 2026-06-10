/* Katenhusen Hofladen — Site-Script (Reveals/Header/Parallax: _engine soft-Persona) */
(function () {
  var yr = document.getElementById('yr');
  if (yr) yr.textContent = new Date().getFullYear();

  // Drawer
  var drawer = document.querySelector('[data-nav]');
  var toggle = document.querySelector('[data-nav-toggle]');
  if (drawer && toggle) {
    drawer.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { drawer.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); });
    });
    toggle.addEventListener('click', function () {
      var open = drawer.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Frische-Uhr: täglich 7:30–19:00
  var box = document.querySelector('[data-clock]');
  var label = document.querySelector('[data-clock-label]');
  if (box && label) {
    var now = new Date();
    var mins = now.getHours() * 60 + now.getMinutes();
    var open = mins >= 450 && mins < 1140; // 7:30 .. 19:00
    box.classList.add(open ? 'is-open' : 'is-closed');
    label.textContent = open ? 'Jetzt geöffnet' : 'Gerade geschlossen';
  }
})();
