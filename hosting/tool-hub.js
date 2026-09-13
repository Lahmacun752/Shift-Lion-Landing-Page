(()=>{
  const search=document.querySelector('#toolSearch');
  const clearSearch=document.querySelector('#clearSearch');
  const resetFilters=document.querySelector('#resetFilters');
  const buttons=[...document.querySelectorAll('.filter')];
  const cards=[...document.querySelectorAll('.tool-card')];
  const count=document.querySelector('#resultCount');
  const empty=document.querySelector('.empty');
  let category='all';

  const normalize=value=>(value||'').toLocaleLowerCase(document.documentElement.lang||'de').normalize('NFD').replace(/[\u0300-\u036f]/g,'');
  const update=()=>{
    const query=normalize(search?.value.trim());
    let shown=0;
    cards.forEach(card=>{
      const categories=(card.dataset.category||'').split(/\s+/);
      const searchable=normalize(`${card.textContent} ${card.dataset.search||''}`);
      const visible=(category==='all'||categories.includes(category))&&(!query||searchable.includes(query));
      card.hidden=!visible;
      if(visible)shown+=1;
    });
    if(count)count.textContent=count.dataset.template.replace('{count}',shown).replace('{total}',cards.length);
    empty?.classList.toggle('visible',shown===0);
    if(clearSearch)clearSearch.hidden=!search?.value;
  };
  const chooseCategory=next=>{
    category=next;
    buttons.forEach(button=>{
      const active=button.dataset.category===category;
      button.classList.toggle('active',active);
      button.setAttribute('aria-pressed',String(active));
    });
    update();
  };
  const reset=()=>{
    if(search)search.value='';
    chooseCategory('all');
    search?.focus();
  };

  search?.addEventListener('input',update);
  clearSearch?.addEventListener('click',()=>{if(search)search.value='';update();search?.focus()});
  resetFilters?.addEventListener('click',reset);
  buttons.forEach(button=>button.addEventListener('click',()=>chooseCategory(button.dataset.category)));

  const toggle=document.querySelector('.menu-toggle');
  const menu=document.querySelector('.mobile-menu');
  const closeMenu=()=>{if(menu)menu.hidden=true;toggle?.setAttribute('aria-expanded','false')};
  toggle?.addEventListener('click',event=>{event.stopPropagation();const open=menu?.hidden??true;if(menu)menu.hidden=!open;toggle.setAttribute('aria-expanded',String(open))});
  menu?.addEventListener('click',event=>{if(event.target.closest('a'))closeMenu()});
  document.addEventListener('click',event=>{if(!event.target.closest('.topbar'))closeMenu()});
  document.addEventListener('keydown',event=>{if(event.key==='Escape')closeMenu()});
  update();
})();
