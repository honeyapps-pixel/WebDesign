// Header scroll effect
const header = document.getElementById('header');
window.addEventListener('scroll', () => {
  header.classList.toggle('scrolled', window.scrollY > 60);
});

// Mobile nav toggle
const burger = document.getElementById('burger');
const mobileNav = document.getElementById('mobileNav');
burger.addEventListener('click', () => {
  mobileNav.classList.toggle('open');
});

// Close mobile nav on link click
document.querySelectorAll('.nav__mobile-link').forEach(link => {
  link.addEventListener('click', () => mobileNav.classList.remove('open'));
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const target = document.querySelector(a.getAttribute('href'));
    if (!target) return;
    e.preventDefault();
    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
});

// Contact form
const form = document.getElementById('kontaktForm');
const success = document.getElementById('formSuccess');

form.addEventListener('submit', e => {
  e.preventDefault();
  const btn = form.querySelector('button[type="submit"]');
  btn.textContent = 'Wird gesendet …';
  btn.disabled = true;
  setTimeout(() => {
    form.reset();
    btn.textContent = 'Anfrage absenden →';
    btn.disabled = false;
    success.classList.add('show');
    setTimeout(() => success.classList.remove('show'), 5000);
  }, 1200);
});

// Scroll reveal
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.leistung__card, .prozess__step, .warum__card').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(20px)';
  el.style.transition = 'opacity .5s ease, transform .5s ease';
  observer.observe(el);
});
