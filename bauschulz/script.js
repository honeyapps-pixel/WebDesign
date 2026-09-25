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

  /* Alte Sprungadressen der Startseite (…/#tiefbau) führen auf die Sparten-Seiten */
  const SPARTEN = ['hochbau', 'tiefbau', 'garten-landschaftsbau'];
  if (document.querySelector('.sparten') && SPARTEN.includes(location.hash.slice(1))) {
    location.replace(location.hash.slice(1) + '.html');
  }

  /* Großansicht auf den Sparten-Seiten: Bild anklicken → groß, Pfeile/Tastatur/Wischen zum Durchklicken */
  const dlg = document.querySelector('.galerie');
  const datenEl = document.getElementById('galerie-daten');
  if (dlg && datenEl && typeof dlg.showModal === 'function') {
    const bilder = JSON.parse(datenEl.textContent).bilder;
    const zahl = dlg.querySelector('.galerie__zahl');
    const img = dlg.querySelector('.galerie__buehne img');
    const text = dlg.querySelector('figcaption');
    const GROESSEN = '(max-width: 900px) 100vw, 80vw';
    let idx = 0, ausloeser = null, lauf = 0;
    img.removeAttribute('loading');
    img.sizes = GROESSEN;

    const zeige = (i) => {
      idx = (i + bilder.length) % bilder.length;
      const bild = bilder[idx];
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
      zahl.textContent = `Bild ${idx + 1} von ${bilder.length}`;
    };

    const oeffne = (i, von) => {
      ausloeser = von || null;
      dlg.showModal();
      document.documentElement.style.overflow = 'hidden';
      zeige(i);
      dlg.querySelector('.galerie__zu').focus();
    };
    const schliesse = () => { if (dlg.open) dlg.close(); };
    dlg.addEventListener('close', () => {
      document.documentElement.style.overflow = '';
      /* Fokus auf das Vorschaubild des zuletzt gezeigten Bildes */
      const ziel = document.querySelector(`[data-bild="${idx}"]`) || ausloeser;
      if (ziel) { ziel.focus({ preventScroll: true }); ziel.scrollIntoView({ block: 'nearest' }); }
    });
    dlg.querySelector('.galerie__zu').addEventListener('click', schliesse);
    dlg.querySelector('.galerie__pfeil--zurueck').addEventListener('click', () => zeige(idx - 1));
    dlg.querySelector('.galerie__pfeil--vor').addEventListener('click', () => zeige(idx + 1));
    dlg.addEventListener('keydown', e => {
      if (e.key === 'ArrowLeft') { e.preventDefault(); zeige(idx - 1); }
      if (e.key === 'ArrowRight') { e.preventDefault(); zeige(idx + 1); }
    });
    /* Wischen auf dem Bild */
    let x0 = null, gewischt = false;
    const buehne = dlg.querySelector('.galerie__buehne');
    const rahmen = dlg.querySelector('.galerie__rahmen');
    buehne.addEventListener('pointerdown', e => { x0 = e.clientX; gewischt = false; });
    img.addEventListener('dragstart', e => e.preventDefault());
    buehne.addEventListener('pointercancel', () => { x0 = null; });
    buehne.addEventListener('pointerup', e => {
      if (x0 === null) return;
      const dx = e.clientX - x0; x0 = null;
      if (Math.abs(dx) > 50) { gewischt = true; zeige(idx + (dx < 0 ? 1 : -1)); }
    });
    /* Klick auf die dunkle Fläche neben dem Bild schließt (nicht nach einem Wischen) */
    dlg.addEventListener('click', e => {
      if (gewischt) { gewischt = false; return; }
      if (e.target === dlg || e.target === buehne || e.target === rahmen) schliesse();
    });

    document.querySelectorAll('[data-bild]').forEach(k => k.addEventListener('click', e => {
      e.preventDefault();
      oeffne(Number(k.dataset.bild), k);
    }));
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
