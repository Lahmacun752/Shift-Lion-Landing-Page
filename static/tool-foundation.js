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
    '/schichtzulagen-rechner.html':'/en/schichtzulagen-rechner.html',
    '/monats-schichtlohn-rechner.html':'/en/monthly-shift-pay-calculator.html',
    '/pausenrechner.html':'/en/break-calculator.html',
    '/sonntagszuschlag-rechner.html':'/en/sunday-allowance-calculator.html',
    '/ruhezeit-rechner.html':'/en/rest-period-calculator.html',
    '/urlaubsanspruch-rechner.html':'/en/leave-entitlement-calculator.html'
  };
  const reverse=Object.fromEntries(Object.entries(pairs).map(([de,en])=>[en,de]));
  const path=location.pathname.replace(/\/$/,'')||'/';
  const storageKey=`shiftlion-tool:${path}:inputs:v1`;
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

  const calculator=document.querySelector('.calculator,.calculator-layout,#planner .planner-layout');
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
      actions.append(reset);
    }

    const fields=()=>[...calculator.querySelectorAll('input:not([type="button"]):not([type="submit"]):not([type="hidden"]),select,textarea')];
    const fieldKey=(field,index)=>field.id||field.name||`${field.tagName.toLowerCase()}-${index}`;
    const initialValues=fields().map((field,index)=>({key:fieldKey(field,index),value:field.value,checked:field.checked,type:field.type}));
    const dispatchValue=field=>{field.dispatchEvent(new Event('input',{bubbles:true}));field.dispatchEvent(new Event('change',{bubbles:true}))};
    const applyValues=values=>{
      const byKey=new Map(values.map(value=>[value.key,value]));
      fields().forEach((field,index)=>{
        const saved=byKey.get(fieldKey(field,index));if(!saved)return;
        if(field.type==='checkbox'||field.type==='radio')field.checked=Boolean(saved.checked);else field.value=saved.value;
        dispatchValue(field);
      });
    };
    const calculateResult=()=>{
      const trigger=calculator.querySelector('#calculate,#createPlan,[data-calculate],button.primary,button.primary-btn');
      if(trigger)trigger.click();
    };
    try{
      const saved=JSON.parse(localStorage.getItem(storageKey)||'null');
      if(Array.isArray(saved))applyValues(saved);
    }catch(_error){}
    let saveTimer;
    const saveInputs=()=>{
      clearTimeout(saveTimer);saveTimer=setTimeout(()=>{
        const values=fields().map((field,index)=>({key:fieldKey(field,index),value:field.value,checked:field.checked,type:field.type}));
        try{localStorage.setItem(storageKey,JSON.stringify(values))}catch(_error){}
      },120);
    };
    calculator.addEventListener('input',saveInputs);
    calculator.addEventListener('change',saveInputs);

    const resultText=()=>{
      const title=(document.querySelector('h1')?.textContent||document.title).trim();
      const rows=[...calculator.querySelectorAll('.summary .metric,.results .metric,.result-row,.result-total')].map(row=>{
        const label=row.querySelector('span,.result-label')?.textContent?.trim();
        const value=row.querySelector('strong,.result-value')?.textContent?.trim();
        return label&&value?`${label}: ${value}`:'';
      }).filter(Boolean);
      const note=calculator.querySelector('.calculation-note,#formula')?.textContent?.trim();
      return [title,...rows,note].filter(Boolean).join('\n');
    };
    const copyText=async value=>{
      if(navigator.clipboard&&window.isSecureContext)return navigator.clipboard.writeText(value);
      const area=document.createElement('textarea');area.value=value;area.style.position='fixed';area.style.opacity='0';document.body.append(area);area.select();document.execCommand('copy');area.remove();
    };
    const utilities=document.createElement('section');utilities.className='tool-utilities';utilities.setAttribute('aria-label',isEnglish?'Calculator actions':'Rechner-Aktionen');
    utilities.innerHTML=`<div class="tool-utilities-copy"><strong>${isEnglish?'Quick actions':'Schnellaktionen'}</strong><span>${isEnglish?'Your entries are saved only in this browser.':'Deine Eingaben werden nur in diesem Browser gespeichert.'}</span></div><div class="tool-utility-actions"><button type="button" data-example>${isEnglish?'Load example':'Beispieldaten laden'}</button><button type="button" data-copy>${isEnglish?'Copy result':'Ergebnis kopieren'}</button><button type="button" data-print>${isEnglish?'Save PDF / print':'PDF speichern / drucken'}</button><a href="${toolsHref}">${isEnglish?'Choose another tool':'Weiteres Tool wählen'} →</a></div><span class="tool-utility-status" aria-live="polite"></span>`;
    const firstHeading=calculator.querySelector('h2');
    if(firstHeading)firstHeading.after(utilities);else calculator.prepend(utilities);
    utilities.querySelector('[data-example]').addEventListener('click',()=>{
      const example=initialValues.map(value=>({...value,value:value.type==='date'&&!value.value?new Date().toISOString().slice(0,10):value.value}));
      applyValues(example);saveInputs();calculateResult();utilities.querySelector('.tool-utility-status').textContent=isEnglish?'Example values loaded.':'Beispieldaten wurden geladen.';
    });
    utilities.querySelector('[data-copy]').addEventListener('click',async()=>{
      try{await copyText(resultText());utilities.querySelector('.tool-utility-status').textContent=isEnglish?'Result copied.':'Ergebnis wurde kopiert.'}catch(_error){utilities.querySelector('.tool-utility-status').textContent=isEnglish?'Copying was not available.':'Kopieren war nicht möglich.'}
    });
    utilities.querySelector('[data-print]').addEventListener('click',()=>window.print());

    if(!calculator.querySelector('.tool-method-note')){
      const methodNote=document.createElement('p');methodNote.className='tool-method-note';
      methodNote.innerHTML=isEnglish?'Estimate for guidance only. Your employment contract, collective agreement and applicable law remain authoritative. <a href="/en/methodology.html">See methodology and sources →</a>':'Schätzung zur Orientierung. Maßgeblich bleiben Arbeitsvertrag, Tarifvertrag und anwendbares Recht. <a href="/methodik.html">Methodik und Quellen ansehen →</a>';
      calculator.append(methodNote);
    }

    calculator.querySelectorAll('[data-tool-reset],.tool-reset').forEach(reset=>reset.addEventListener('click',()=>{
      try{localStorage.removeItem(storageKey)}catch(_error){}
      applyValues(initialValues);calculateResult();
    }));
  }

  const main=document.querySelector('main');
  if(main&&!main.querySelector('.app-cta')){
    const cta=document.createElement('section');cta.className='app-cta';cta.innerHTML=`<div><h2>${copy.ctaTitle}</h2><p>${copy.ctaText}</p></div><a href="/download/android/">${copy.download}</a>`;main.append(cta);
  }

  let footer=document.querySelector('footer.footer');
  if(!footer){footer=document.createElement('footer');footer.className='footer';document.body.append(footer)}
  footer.innerHTML=`<a href="${homeHref}">${copy.footerHome}</a><a href="${toolsHref}">${copy.tools}</a><a href="${isEnglish?'/en/for-shift-workers.html':'/fuer-schichtarbeiter.html'}">${isEnglish?'For shift workers':'Für Schichtarbeiter'}</a><a href="${isEnglish?'/en/methodology.html':'/methodik.html'}">${isEnglish?'Methodology':'Methodik'}</a><a href="${isEnglish?'/en/privacy.html':'/datenschutz.html'}">${isEnglish?'Privacy':'Datenschutz'}</a><a href="/download/android/">${copy.download}</a>`;
})();
