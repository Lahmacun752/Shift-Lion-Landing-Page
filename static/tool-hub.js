(() => {
  const isEnglish=document.documentElement.lang==='en';
  const suggestion=document.querySelector('.cta');
  if(suggestion){
    const promo=document.createElement('section');
    promo.className='app-promo';
    promo.innerHTML=isEnglish
      ? '<div><span class="app-label">Shift Lion App</span><h2>Your shift plan, always with you.</h2><p>Plan shifts, compare schedules and keep your free time in view—even when you are on the go.</p></div><a class="app-download" href="/download/android/">Download Shift Lion</a>'
      : '<div><span class="app-label">Shift Lion App</span><h2>Dein Schichtplan gehört in deine Tasche.</h2><p>Plane Schichten, vergleiche Dienstpläne und behalte deine freie Zeit auch unterwegs im Blick.</p></div><a class="app-download" href="/download/android/">Shift Lion herunterladen</a>';
    suggestion.insertAdjacentElement('afterend',promo);
    const style=document.createElement('style');
    style.textContent='.app-promo{width:min(1180px,calc(100% - 48px));margin:-42px auto 70px;padding:34px 42px;display:flex;align-items:center;justify-content:space-between;gap:32px;background:linear-gradient(135deg,#fff7df,#fff);border:1px solid #ead28c;border-radius:22px;box-shadow:0 12px 35px rgba(15,23,42,.08)}.app-label{display:block;color:#9b6d00;font-size:12px;font-weight:900;letter-spacing:.11em;text-transform:uppercase}.app-promo h2{margin:7px 0 8px;font-size:clamp(27px,3vw,40px);letter-spacing:-.03em}.app-promo p{margin:0;max-width:690px;color:#667085;line-height:1.6}.app-download{flex:0 0 auto;background:#f2be37;color:#111318;text-decoration:none;font-weight:900;padding:15px 20px;border-radius:11px;text-align:center}@media(max-width:900px){.app-promo{width:min(100% - 28px,680px);margin-top:-44px;padding:28px;align-items:stretch;flex-direction:column}.app-download{width:100%}}';
    document.head.appendChild(style);
  }
  const workingTimeCard=[...document.querySelectorAll('.tool-card')].find(card=>card.querySelector('h3')?.textContent===(isEnglish?'Working Time Calculator':'Arbeitszeitrechner'));
  if(workingTimeCard){
    workingTimeCard.classList.remove('coming');
    workingTimeCard.querySelector('.badge').textContent=isEnglish?'Available':'Verfügbar';
    const oldAction=workingTimeCard.querySelector('.card-action');
    const action=document.createElement('a');
    action.className='card-action';
    action.href=isEnglish?'/en/working-time-calculator.html':'/arbeitszeitrechner.html';
    action.textContent=isEnglish?'Open calculator →':'Zum Rechner →';
    oldAction.replaceWith(action);
  }
  const nightCard=[...document.querySelectorAll('.tool-card')].find(card=>card.querySelector('h3')?.textContent===(isEnglish?'Night Allowance Calculator':'Nachtzuschlag-Rechner'));
  if(nightCard){
    nightCard.classList.remove('coming');
    nightCard.querySelector('.badge').textContent=isEnglish?'Available':'Verfügbar';
    const oldAction=nightCard.querySelector('.card-action'),action=document.createElement('a');
    action.className='card-action';action.href=isEnglish?'/en/night-allowance-calculator.html':'/nachtzuschlag-rechner.html';action.textContent=isEnglish?'Open calculator →':'Zum Rechner →';oldAction.replaceWith(action);
  }
  const overtimeCard=[...document.querySelectorAll('.tool-card')].find(card=>card.querySelector('h3')?.textContent===(isEnglish?'Overtime Calculator':'Überstunden-Rechner'));
  if(overtimeCard){overtimeCard.classList.remove('coming');overtimeCard.querySelector('.badge').textContent=isEnglish?'Available':'Verfügbar';const old=overtimeCard.querySelector('.card-action'),a=document.createElement('a');a.className='card-action';a.href=isEnglish?'/en/overtime-calculator.html':'/ueberstunden-rechner.html';a.textContent=isEnglish?'Open calculator →':'Zum Rechner →';old.replaceWith(a)}
  const wageCard=[...document.querySelectorAll('.tool-card')].find(card=>card.querySelector('h3')?.textContent===(isEnglish?'Hourly Wage Calculator':'Stundenlohn-Rechner'));
  if(wageCard){wageCard.classList.remove('coming');wageCard.querySelector('.badge').textContent=isEnglish?'Available':'Verfügbar';const old=wageCard.querySelector('.card-action'),a=document.createElement('a');a.className='card-action';a.href=isEnglish?'/en/hourly-wage-calculator.html':'/stundenlohn-rechner.html';a.textContent=isEnglish?'Open calculator →':'Zum Rechner →';old.replaceWith(a)}
  const grid=document.querySelector('.tool-grid');
  if(grid){
    const holiday=document.createElement('article');holiday.className='tool-card coming';holiday.dataset.category='lohn';
    holiday.innerHTML=isEnglish
      ? '<div class="card-top"><div class="icon">🎉</div><span class="badge">Coming soon</span></div><h3>Holiday Allowance Calculator</h3><p>Calculate holiday hours, base pay and your individual holiday allowance.</p><div class="tags"><span>Public holidays</span><span>Pay</span><span>Custom rate</span></div><span class="card-action">Planned</span>'
      : '<div class="card-top"><div class="icon">🎉</div><span class="badge">Demnächst</span></div><h3>Feiertagszuschlag-Rechner</h3><p>Berechne Feiertagsstunden, Grundlohn und deinen individuellen Feiertagszuschlag.</p><div class="tags"><span>Feiertage</span><span>Lohn</span><span>Eigener Satz</span></div><span class="card-action">Geplant</span>';
    grid.appendChild(holiday);
  }
  const totalStat=document.querySelectorAll('.hero-stat strong')[0];
  if(totalStat)totalStat.textContent=String(document.querySelectorAll('.tool-card').length);
  const availableCount=document.querySelectorAll('.tool-card:not(.coming)').length;
  const availableStat=document.querySelectorAll('.hero-stat strong')[1];
  if(availableStat)availableStat.textContent=String(availableCount);
  const search=document.querySelector('#toolSearch'),buttons=[...document.querySelectorAll('.filter')],cards=[...document.querySelectorAll('.tool-card')],count=document.querySelector('#resultCount'),empty=document.querySelector('.empty');
  cards.filter(card=>!card.classList.contains('coming')).forEach(card=>{
    const link=card.querySelector('a.card-action');
    if(!link)return;
    card.classList.add('clickable');
    card.tabIndex=0;
    card.setAttribute('role','link');
    card.setAttribute('aria-label',`${card.querySelector('h3')?.textContent}: ${link.textContent}`);
    card.addEventListener('click',event=>{if(!event.target.closest('a'))location.href=link.href});
    card.addEventListener('keydown',event=>{if(event.key==='Enter'||event.key===' '){event.preventDefault();location.href=link.href}});
  });
  let category='all';
  const update=()=>{const query=(search.value||'').trim().toLowerCase();let shown=0;cards.forEach(card=>{const matchesCategory=category==='all'||card.dataset.category===category;const matchesText=!query||card.textContent.toLowerCase().includes(query);card.hidden=!(matchesCategory&&matchesText);if(!card.hidden)shown+=1});count.textContent=count.dataset.template.replace('{count}',shown).replace('{total}',cards.length);empty.classList.toggle('visible',shown===0)};
  search.addEventListener('input',update);buttons.forEach(button=>button.addEventListener('click',()=>{buttons.forEach(item=>item.classList.remove('active'));button.classList.add('active');category=button.dataset.category;update()}));update();
  const toggle=document.querySelector('.menu-toggle'),menu=document.querySelector('.mobile-menu');toggle?.addEventListener('click',()=>{const open=toggle.getAttribute('aria-expanded')==='true';toggle.setAttribute('aria-expanded',String(!open));menu.hidden=open});
})();
