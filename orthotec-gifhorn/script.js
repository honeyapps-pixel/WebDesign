/* ORTHOTEC Gifhorn — Site-Script (Motion: _engine still-Persona) */
(function () {
  var yr = document.getElementById('yr');
  if (yr) yr.textContent = new Date().getFullYear();
  // Akkordeon: pro Gruppe nur eines offen
  document.querySelectorAll('[data-acc]').forEach(function (group) {
    var items = group.querySelectorAll('details');
    items.forEach(function (d) {
      d.addEventListener('toggle', function () {
        if (d.open) items.forEach(function (o) { if (o !== d) o.open = false; });
      });
    });
  });
})();
