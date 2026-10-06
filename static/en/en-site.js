(() => {
  const hero = document.querySelector('.hero');
  if (!hero) return;
  let top = hero.querySelector('.topbar');
  const logo = hero.querySelector('.brand-logo');
  if (!top) {
    top = document.createElement('div');
    top.className = 'topbar';
    hero.insertBefore(top, hero.firstChild);
    if (logo) top.appendChild(logo);
  }
  hero.querySelectorAll('.nav').forEach((nav) => nav.remove());
  document.querySelector('.language-switch')?.remove();
  const links = '<a href="/en/#features">Features</a><a href="/en/compare-shifts.html">Compare Shifts</a><a href="/en/tools/">Tools</a><a href="/download/android/" class="nav-download">Download App</a>';
  const mobileLinks = '<a href="/en/">Home</a><a href="/en/tools/">Free Tools</a><a href="/">Deutsch</a><a href="/download/android/" class="mobile-download">Download App</a>';
  top.insertAdjacentHTML('beforeend', `<nav class="desktop-nav">${links}</nav><div class="language-switch" aria-label="Choose language"><a href="/" lang="de">DE</a><a class="active" href="/en/" lang="en" aria-current="page">EN</a></div><button class="menu-toggle" aria-expanded="false" aria-controls="mobileMenu">☰ Menu</button><nav class="mobile-menu" id="mobileMenu" hidden>${mobileLinks}</nav>`);

  if (location.pathname === '/en/' || location.pathname === '/en/index.html') {
    const preview = document.querySelector('.preview-card');
    const tool = document.getElementById('tool');
    const lookInside = [...document.querySelectorAll('h2')].find(heading => heading.textContent.includes('A look inside Shift Lion'))?.closest('.section');
    lookInside?.insertAdjacentHTML('beforebegin', '<section class="section"><div class="panel"><h2 class="section-title">Tips for your shift-work life</h2><p class="section-copy">Discover practical guides for sleep, health, relationships and everyday life around rotating shifts.</p><details class="page-directory" open><summary><span class="directory-open">Discover more shift-work tips</span><span class="directory-close">Collapse the page overview</span></summary><nav class="nav nav-dark"><a href="/en/">🏠 Home</a><a href="/en/schichtplaner.html">📅 Shift Planner App</a><a href="/en/dienstplan-app.html">📋 Duty Roster App</a><a href="/en/fruehschicht-tipps.html">🌅 Early Shift Tips</a><a href="/en/spaetschicht-tipps.html">🌆 Late Shift Tips</a><a href="/en/nachtschicht-tipps.html">🌙 Night Shift Tips</a><a href="/en/schichtarbeit-schlaf.html">😴 Shift Work & Sleep</a><a href="/en/schichtarbeit-fitness.html">💪 Shift Work & Fitness</a><a href="/en/schichtarbeit-ernaehrung.html">🍎 Shift Work & Nutrition</a><a href="/en/schichtarbeit-alltag.html">📌 Shift Work & Daily Life</a><a href="/en/schichtarbeit-familie.html">👪 Shift Work & Family</a><a href="/en/schichtarbeit-beziehung.html">❤️ Shift Work & Relationships</a><a href="/en/schichtarbeit-stress.html">🧠 Shift Work & Stress</a><a href="/en/schichtplaner-online.html">🗓️ Online Shift Planner</a><a href="/en/tools/">🧰 Free Tools</a></nav></details></div></section>');
    if (window.matchMedia('(max-width: 860px)').matches) {
      document.querySelectorAll('.page-directory').forEach(directory => directory.removeAttribute('open'));
    }
    if (preview && tool) tool.insertAdjacentElement('afterend', preview);
  }

  document.querySelector('.cta')?.insertAdjacentHTML('afterend', '<footer class="site-footer"><div class="footer-grid"><div><img src="../Shift-Lion-Logo-groß.png" alt="Shift Lion"><p>Your personal shift planner for more clarity, better planning and more shared time.</p></div><div class="footer-col"><strong>Shift Lion</strong><a href="/en/">Home</a><a href="/en/schichtplaner.html">Shift Planner</a><a href="/en/dienstplan-app.html">Duty Roster App</a><a href="/en/schichtplaner-online.html">Online Planner</a><a href="/en/schichtzulagen-rechner.html">Allowance Calculator</a></div><div class="footer-col"><strong>Guides</strong><a href="/en/fruehschicht-tipps.html">Early Shift</a><a href="/en/spaetschicht-tipps.html">Late Shift</a><a href="/en/nachtschicht-tipps.html">Night Shift</a><a href="/en/schichtarbeit-alltag.html">Shift Work Life</a><a href="/kontakt.html">Contact</a></div></div><div class="footer-bottom">© 2026 Shift Lion. All rights reserved.</div></footer>');
  const button = document.querySelector('.menu-toggle');
  const menu = document.getElementById('mobileMenu');
  button?.addEventListener('click', () => {
    const open = button.getAttribute('aria-expanded') === 'true';
    button.setAttribute('aria-expanded', String(!open));
    menu.hidden = open;
  });
})();
