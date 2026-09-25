/* BAUSCHULZ – schlichte Seite (v2). Menü, Sparten-Galerie, Karte per Klick. Keine Cookies, kein Speicher. */
(() => {
  'use strict';

  /* Menü (mobil) */
  const kopf = document.querySelector('.kopf');
  const menueKnopf = document.querySelector('.kopf__menue');
  if (kopf && menueKnopf) {
    const zu = () => { kopf.classList.remove('ist-offen'); menueKnopf.setAttribute('aria-expanded', 'false'); };
    menueKnopf.addEventListener('click', () => {
      const offen = kopf.classList.toggle('ist-offen');
      menueKnopf.setAttribute('aria-expanded', String(offen));
    });
    kopf.querySelectorAll('.kopf__nav a').forEach(a => a.addEventListener('click', zu));
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && kopf.classList.contains('ist-offen')) { zu(); menueKnopf.focus(); } });
    document.addEventListener('click', e => { if (!kopf.contains(e.target)) zu(); });
  }

  /* Galerie je Sparte */
  const dlg = document.querySelector('.galerie');
  const datenEl = document.getElementById('galerien');
  if (dlg && datenEl && typeof dlg.showModal === 'function') {
    const daten = JSON.parse(datenEl.textContent);
    const titel = dlg.querySelector('#galerie-titel');
    const zahl = dlg.querySelector('.galerie__zahl');
    const img = dlg.querySelector('.galerie__buehne img');
    const text = dlg.querySelector('figcaption');
    const leiste = dlg.querySelector('.galerie__daumen');
    const GROESSEN = '(max-width: 900px) 100vw, 80vw';
    let aktiv = null, idx = 0, ausloeser = null, lauf = 0;
    img.removeAttribute('loading');
    img.sizes = GROESSEN;

    const zeige = (i) => {
      const b = aktiv.bilder;
      idx = (i + b.length) % b.length;
      const bild = b[idx];
      const nr = ++lauf;
      const srcset = `${bild.klein}.webp 800w, ${bild.gross}.webp ${bild.w}w`;
      /* gleiche Auswahl wie das sichtbare Bild vorladen und dekodieren – kein doppelter Download */
      const neu = new Image();
      neu.sizes = GROESSEN; neu.srcset = srcset; neu.src = bild.gross + '.jpg';
      img.classList.add('ist-leer');
      const setzen = () => {
        if (nr !== lauf) return;
        img.srcset = srcset;
        img.src = bild.gross + '.jpg';
        img.width = bild.w; img.height = bild.h;
        img.alt = bild.text;
        img.classList.remove('ist-leer');
      };
      (neu.decode ? neu.decode() : Promise.resolve()).then(setzen, setzen);
      text.textContent = bild.text;
      zahl.textContent = `Bild ${idx + 1} von ${b.length}`;
      leiste.querySelectorAll('button').forEach((k, j) => k.setAttribute('aria-current', j === idx ? 'true' : 'false'));
      const akt = leiste.children[idx];
      if (akt) akt.scrollIntoView({ block: 'nearest', inline: 'center' });
    };

    const oeffne = (slug, von) => {
      aktiv = daten[slug];
      if (!aktiv) return;
      ausloeser = von || null;
      titel.textContent = aktiv.titel;
      leiste.innerHTML = aktiv.bilder.map((b, j) =>
        `<li><button type="button" aria-label="Bild ${j + 1}: ${b.text.replace(/"/g, '&quot;')}"><picture><source type="image/webp" srcset="${b.daumen}.webp"><img src="${b.daumen}.jpg" alt="" width="400" height="300" loading="lazy"></picture></button></li>`).join('');
      leiste.querySelectorAll('button').forEach((k, j) => k.addEventListener('click', () => zeige(j)));
      dlg.showModal();
      document.documentElement.style.overflow = 'hidden';
      zeige(0);
      dlg.querySelector('.galerie__zu').focus();
      if (location.hash !== '#' + slug) history.replaceState(null, '', '#' + slug);
    };

    const schliesse = () => { if (dlg.open) dlg.close(); };
    dlg.addEventListener('close', () => {
      document.documentElement.style.overflow = '';
      history.replaceState(null, '', location.pathname + location.search);
      if (ausloeser) ausloeser.focus({ preventScroll: true });
    });
    dlg.querySelector('.galerie__zu').addEventListener('click', schliesse);
    dlg.querySelector('.galerie__pfeil--zurueck').addEventListener('click', () => zeige(idx - 1));
    dlg.querySelector('.galerie__pfeil--vor').addEventListener('click', () => zeige(idx + 1));
    dlg.addEventListener('keydown', e => {
      if (e.key === 'ArrowLeft') { e.preventDefault(); zeige(idx - 1); }
      if (e.key === 'ArrowRight') { e.preventDefault(); zeige(idx + 1); }
    });
    /* Wischen auf dem Bild */
    let x0 = null;
    const buehne = dlg.querySelector('.galerie__buehne');
    buehne.addEventListener('pointerdown', e => { x0 = e.clientX; });
    buehne.addEventListener('pointerup', e => {
      if (x0 === null) return;
      const dx = e.clientX - x0; x0 = null;
      if (Math.abs(dx) > 50) zeige(idx + (dx < 0 ? 1 : -1));
    });

    document.querySelectorAll('[data-galerie]').forEach(k => k.addEventListener('click', () => oeffne(k.dataset.galerie, k)));
    /* Menü-Links und direkte Aufrufe (…/#tiefbau) öffnen die Galerie */
    const ausHash = () => {
      const slug = decodeURIComponent(location.hash.slice(1));
      if (daten[slug] && !dlg.open) oeffne(slug, document.querySelector(`[data-galerie="${slug}"]`));
    };
    window.addEventListener('hashchange', ausHash);
    document.querySelectorAll('.kopf__nav a').forEach(a => a.addEventListener('click', e => {
      const slug = a.hash.slice(1);
      if (daten[slug] && a.pathname === location.pathname) { e.preventDefault(); oeffne(slug, document.querySelector(`[data-galerie="${slug}"]`)); }
    }));
    ausHash();
  }

  /* Karte erst nach Klick (keine Drittanfrage vorher) */
  const karte = document.querySelector('.karte');
  const laden = document.querySelector('[data-karte-laden]');
  if (karte && laden) {
    laden.addEventListener('click', () => {
      laden.disabled = true; laden.textContent = 'Karte wird geladen …';
      const css = document.createElement('link'); css.rel = 'stylesheet'; css.href = 'assets/css/leaflet.css'; document.head.appendChild(css);
      const js = document.createElement('script'); js.src = 'assets/js/leaflet.min.js';
      js.onload = () => {
        const lat = +karte.dataset.lat, lon = +karte.dataset.lon;
        const flaeche = karte.querySelector('.karte__leinwand');
        flaeche.hidden = false;
        karte.classList.add('ist-geladen');
        const map = L.map(flaeche, { scrollWheelZoom: false }).setView([lat, lon], 14);
        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19, attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>-Mitwirkende' }).addTo(map);
        const icon = L.divIcon({ className: 'sitz-marker', html: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 22s-7-6.2-7-12a7 7 0 0 1 14 0c0 5.8-7 12-7 12z"/><circle cx="12" cy="10" r="2.6" fill="#fff" stroke="none"/></svg>', iconSize: [40, 40], iconAnchor: [20, 38], popupAnchor: [0, -34] });
        L.marker([lat, lon], { icon, title: 'BAUSCHULZ, Fehringstraße 8' }).addTo(map).bindPopup('<b>BAUSCHULZ</b><br>Fehringstraße 8<br>38524 Sassenburg').openPopup();
        flaeche.focus && flaeche.setAttribute('tabindex', '-1');
      };
      js.onerror = () => { laden.disabled = false; laden.textContent = 'Karte laden'; };
      document.body.appendChild(js);
    });
  }
})();
