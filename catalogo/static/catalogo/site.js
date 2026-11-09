(() => {
  'use strict';
  const root = document.documentElement;
  root.classList.add('js');
  const themeButton = document.querySelector('.theme-toggle');
  const preference = matchMedia('(prefers-color-scheme: dark)');
  function storedTheme() { try { return localStorage.getItem('parfums-theme'); } catch (_) { return null; } }
  function setTheme(theme) {
    root.dataset.theme = theme;
    const label = theme === 'dark' ? 'Activar modo claro' : 'Activar modo oscuro';
    themeButton.setAttribute('aria-label', label);
    themeButton.title = label;
    themeButton.querySelector('.theme-label').textContent = label;
    document.getElementById('browser-theme').content = theme === 'dark' ? '#131619' : '#ffffff';
  }
  themeButton.hidden = false;
  setTheme(root.dataset.theme);
  themeButton.addEventListener('click', () => {
    const theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    setTheme(theme);
    try { localStorage.setItem('parfums-theme', theme); } catch (_) {}
  });
  preference.addEventListener('change', (event) => { if (!['light', 'dark'].includes(storedTheme())) setTheme(event.matches ? 'dark' : 'light'); });
  window.addEventListener('storage', (event) => { if (event.key === 'parfums-theme') setTheme(['light', 'dark'].includes(event.newValue) ? event.newValue : preference.matches ? 'dark' : 'light'); });
  const menu = document.querySelector('.main-nav');
  const menuButton = document.querySelector('.menu-toggle');
  menuButton.hidden = false;
  function closeMenu() { menu.classList.remove('is-open'); menuButton.setAttribute('aria-expanded', 'false'); menuButton.setAttribute('aria-label', 'Abrir menú'); menuButton.querySelector('use').setAttribute('href', '#i-menu'); }
  menuButton.addEventListener('click', () => {
    const open = menuButton.getAttribute('aria-expanded') !== 'true';
    menu.classList.toggle('is-open', open);
    menuButton.setAttribute('aria-expanded', String(open));
    menuButton.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
    menuButton.querySelector('use').setAttribute('href', open ? '#i-close' : '#i-menu');
  });
  document.addEventListener('keydown', (event) => { if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') { closeMenu(); menuButton.focus(); } });
  matchMedia('(min-width: 761px)').addEventListener('change', closeMenu);
  document.querySelectorAll('form[method="post"]').forEach(form => form.addEventListener('submit', () => {
    const submit = form.querySelector('button[type="submit"]');
    if (submit) { submit.disabled = true; submit.textContent = 'Enviando…'; }
  }));
  window.addEventListener('pageshow', () => document.querySelectorAll('form[method="post"] button[type="submit"]').forEach(button => {
    if (button.dataset.originalHtml) button.innerHTML = button.dataset.originalHtml;
    button.disabled = false;
  }));
  document.querySelectorAll('form[method="post"] button[type="submit"]').forEach(button => { button.dataset.originalHtml = button.innerHTML; });
})();
