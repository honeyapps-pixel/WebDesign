// Mobile nav
const burger = document.getElementById('burger');
const mobileNav = document.getElementById('mobileNav');
if (burger && mobileNav) {
  burger.addEventListener('click', () => {
    mobileNav.classList.toggle('open');
    burger.setAttribute('aria-expanded', mobileNav.classList.contains('open'));
  });
  document.querySelectorAll('.nav__mobile a').forEach(link => {
    link.addEventListener('click', () => mobileNav.classList.remove('open'));
  });
}

// Active nav link
const currentPage = window.location.pathname.split('/').pop() || 'index.html';
document.querySelectorAll('.nav__list a').forEach(a => {
  const href = a.getAttribute('href');
  if (href === currentPage || (currentPage === '' && href === 'index.html')) {
    a.classList.add('active');
  }
});

// Contact form
const form = document.getElementById('kontaktForm');
if (form) {
  form.addEventListener('submit', e => {
    e.preventDefault();
    let valid = true;
    form.querySelectorAll('[required]').forEach(field => {
      const err = field.closest('.form__group')?.querySelector('.form__error-msg');
      if (!field.value.trim()) {
        valid = false;
        field.style.borderColor = 'var(--color-emergency)';
        if (err) err.classList.add('show');
      } else {
        field.style.borderColor = '';
        if (err) err.classList.remove('show');
      }
    });
    if (!valid) return;

    const btn = form.querySelector('button[type="submit"]');
    btn.disabled = true;
    btn.textContent = 'Wird gesendet …';

    setTimeout(() => {
      form.reset();
      btn.disabled = false;
      btn.textContent = 'Anfrage senden';
      document.getElementById('formSuccess')?.classList.add('show');
    }, 1400);
  });
}

// Scroll reveal
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.card, .step, .leistung-detail').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(16px)';
  el.style.transition = 'opacity .45s ease, transform .45s ease';
  observer.observe(el);
});
