/* Hoyer Kabelfertigung — Site-Script (Reveals/Header/Counter: _engine motion.js) */
(function () {
  // Jahr im Footer
  var yr = document.getElementById('yr');
  if (yr) yr.textContent = new Date().getFullYear();

  // Drawer: schließt beim Klick auf einen Link, ARIA synchron halten
  var drawer = document.querySelector('[data-nav]');
  var toggle = document.querySelector('[data-nav-toggle]');
  if (drawer) {
    drawer.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        drawer.classList.remove('open');
        if (toggle) toggle.setAttribute('aria-expanded', 'false');
      });
    });
  }
  if (toggle && drawer) {
    toggle.addEventListener('click', function () {
      var open = drawer.classList.contains('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }
})();
