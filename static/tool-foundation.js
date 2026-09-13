(()=>{
  const isEnglish=(document.documentElement.lang||'de').toLowerCase().startsWith('en');
  const copy=isEnglish?{
    home:'Home',tools:'All tools',language:'DE',download:'Download app',menu:'☰ Menu',
    reset:'Reset calculator',error:'Please check the highlighted entry.',
    ctaTitle:'Keep your complete shift plan with you.',
    ctaText:'Plan rotations, compare schedules and keep your days off in view with Shift Lion.',
    footerHome:'Home'
  }:{
    home:'Startseite',tools:'Alle Tools',language:'EN',download:'App herunterladen',menu:'☰ Menü',
    reset:'Rechner zurücksetzen',error:'Bitte prüfe die markierte Eingabe.',
    ctaTitle:'Dein kompletter Schichtplan für unterwegs.',
    ctaText:'Plane Rhythmen, vergleiche Schichten und behalte deine freien Tage mit Shift Lion im Blick.',
    footerHome:'Startseite'
  };

  const pairs={
    '/arbeitszeitrechner.html':'/en/working-time-calculator.html',
    '/nachtzuschlag-rechner.html':'/en/night-allowance-calculator.html',
    '/ueberstunden-rechner.html':'/en/overtime-calculator.html',
    '/stundenlohn-rechner.html':'/en/hourly-wage-calculator.html',
    '/arbeitstage-rechner.html':'/en/workdays-calculator.html',
    '/feiertagszuschlag-rechner.html':'/en/holiday-allowance-calculator.html',
    '/schichten-vergleichen.html':'/en/compare-shifts.html',
    '/schichtplaner-online.html':'/en/schichtplaner-online.html',
    '/schichtzulagen-rechner.html':'/en/schichtzulagen-rechner.html'
  };
  const reverse=Object.fromEntries(Object.entries(pairs).map(([de,en])=>[en,de]));
  const path=location.pathname.replace(/\/$/,'')||'/';
  const languageHref=isEnglish?(reverse[path]||'/'):(pairs[path]||'/en/');
  const homeHref=isEnglish?'/en/':'/';
  const toolsHref=isEnglish?'/en/tools/':'/tools/';

  document.body.classList.add('tool-page');
  document.querySelectorAll('.logo').forEach(logo=>{if(!logo.alt)logo.alt='Shift Lion'});

  const topbar=document.querySelector('.topbar');
  if(topbar){
    let desktop=topbar.querySelector('.desktop-nav');
    if(!desktop){desktop=document.createElement('nav');desktop.className='desktop-nav';topbar.append(desktop)}
    desktop.setAttribute('aria-label',isEnglish?'Main navigation':'Hauptnavigation');
    desktop.innerHTML=`<a href="${homeHref}">${copy.home}</a><a href="${toolsHref}">${copy.tools}</a><a href="${languageHref}" hreflang="${isEnglish?'de':'en'}">${copy.language}</a><a class="download" href="/download/android/">${copy.download}</a>`;

    let toggle=topbar.querySelector('.menu-toggle');
    if(!toggle){toggle=document.createElement('button');toggle.className='menu-toggle';topbar.append(toggle)}
    toggle.type='button';toggle.textContent=copy.menu;toggle.id='toolMenuToggle';toggle.setAttribute('aria-controls','toolMobileMenu');toggle.setAttribute('aria-expanded','false');toggle.removeAttribute('onclick');

    let mobile=topbar.querySelector('.mobile-menu');
    if(!mobile){mobile=document.createElement('nav');mobile.className='mobile-menu';topbar.append(mobile)}
    mobile.id='toolMobileMenu';mobile.hidden=true;mobile.setAttribute('aria-label',isEnglish?'Mobile navigation':'Mobile Navigation');mobile.removeAttribute('style');
    mobile.innerHTML=`<a href="${homeHref}">${copy.home}</a><a href="${toolsHref}">${copy.tools}</a><a href="${languageHref}" hreflang="${isEnglish?'de':'en'}">${isEnglish?'Deutsch':'English'}</a><a class="mobile-download" href="/download/android/">${copy.download}</a>`;
    const closeMenu=()=>{mobile.hidden=true;toggle.setAttribute('aria-expanded','false')};
    toggle.addEventListener('click',event=>{event.stopPropagation();const open=mobile.hidden;mobile.hidden=!open;toggle.setAttribute('aria-expanded',String(open))});
    mobile.addEventListener('click',event=>{if(event.target.closest('a'))closeMenu()});
    document.addEventListener('click',event=>{if(!topbar.contains(event.target))closeMenu()});
    document.addEventListener('keydown',event=>{if(event.key==='Escape')closeMenu()});
  }

  const calculator=document.querySelector('.calculator');
  if(calculator){
    const liveAreas=calculator.querySelectorAll('.summary,[class*="result-summary"],.results');
    liveAreas.forEach(area=>area.setAttribute('aria-live','polite'));
    let feedback=calculator.querySelector('.tool-feedback');
    if(!feedback){feedback=document.createElement('p');feedback.className='tool-feedback';feedback.setAttribute('role','alert');calculator.append(feedback)}
    const clearError=input=>{input.removeAttribute('aria-invalid');if(!calculator.querySelector('[aria-invalid="true"]'))feedback.classList.remove('visible')};
    calculator.addEventListener('input',event=>{
      const input=event.target.closest('input,select');
      if(!input)return;
      if(!input.checkValidity()){
        input.setAttribute('aria-invalid','true');feedback.textContent=copy.error;feedback.classList.add('visible');
        event.stopImmediatePropagation();
      }else clearError(input);
    },true);
    calculator.addEventListener('click',event=>{
      const trigger=event.target.closest('#calculate,[data-calculate],button.primary');
      if(!trigger||trigger.matches('[type="reset"]'))return;
      const invalid=[...calculator.querySelectorAll('input,select')].find(input=>!input.checkValidity());
      if(invalid){event.preventDefault();event.stopImmediatePropagation();invalid.setAttribute('aria-invalid','true');feedback.textContent=copy.error;feedback.classList.add('visible');invalid.focus()}
      else{feedback.classList.remove('visible')}
    },true);

    const hasReset=calculator.querySelector('#resetCalculator,[type="reset"],[data-tool-reset]')||[...calculator.querySelectorAll('button')].some(button=>/zurücksetzen|reset/i.test(button.textContent));
    const calculate=calculator.querySelector('#calculate');
    if(calculate&&!hasReset){
      let actions=calculate.closest('.actions,.foundation-actions');
      if(!actions){actions=document.createElement('div');actions.className='foundation-actions';calculate.before(actions);actions.append(calculate)}
      const reset=document.createElement('button');reset.type='button';reset.className='button secondary tool-reset';reset.dataset.toolReset='';reset.textContent=copy.reset;
      reset.addEventListener('click',()=>location.reload());actions.append(reset);
    }
  }

  const main=document.querySelector('main');
  if(main&&!main.querySelector('.app-cta')){
    const cta=document.createElement('section');cta.className='app-cta';cta.innerHTML=`<div><h2>${copy.ctaTitle}</h2><p>${copy.ctaText}</p></div><a href="/download/android/">${copy.download}</a>`;main.append(cta);
  }

  let footer=document.querySelector('footer.footer');
  if(!footer){footer=document.createElement('footer');footer.className='footer';document.body.append(footer)}
  footer.innerHTML=`<a href="${homeHref}">${copy.footerHome}</a><a href="${toolsHref}">${copy.tools}</a><a href="/download/android/">${copy.download}</a>`;
})();
