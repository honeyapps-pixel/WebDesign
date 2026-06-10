/* Oberflächentechnik Südheide — Site-Script (Reveals/Header/Count/Parallax: _engine editorial) */
(function () {
  var yr = document.getElementById('yr');
  if (yr) yr.textContent = new Date().getFullYear();
  var rail = document.querySelector('[data-nav]');
  var toggle = document.querySelector('[data-nav-toggle]');
  if (rail && toggle) {
    toggle.addEventListener('click', function () {
      var open = rail.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    rail.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { rail.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); });
    });
  }
})();
