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
  const search=document.querySelector('#toolSearch'),buttons=[...document.querySelectorAll('.filter')],cards=[...document.querySelectorAll('.tool-card')],count=document.querySelector('#resultCount'),empty=document.querySelector('.empty');
  let category='all';
  const update=()=>{const query=(search.value||'').trim().toLowerCase();let shown=0;cards.forEach(card=>{const matchesCategory=category==='all'||card.dataset.category===category;const matchesText=!query||card.textContent.toLowerCase().includes(query);card.hidden=!(matchesCategory&&matchesText);if(!card.hidden)shown+=1});count.textContent=count.dataset.template.replace('{count}',shown).replace('{total}',cards.length);empty.classList.toggle('visible',shown===0)};
  search.addEventListener('input',update);buttons.forEach(button=>button.addEventListener('click',()=>{buttons.forEach(item=>item.classList.remove('active'));button.classList.add('active');category=button.dataset.category;update()}));update();
  const toggle=document.querySelector('.menu-toggle'),menu=document.querySelector('.mobile-menu');toggle?.addEventListener('click',()=>{const open=toggle.getAttribute('aria-expanded')==='true';toggle.setAttribute('aria-expanded',String(!open));menu.hidden=open});
})();
