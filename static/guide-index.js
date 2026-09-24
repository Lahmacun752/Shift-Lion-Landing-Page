(() => {
  const search = document.querySelector('#guideSearch');
  const buttons = [...document.querySelectorAll('[data-filter]')];
  const cards = [...document.querySelectorAll('.guide-card-grid article')];
  const count = document.querySelector('#guideResultCount');
  const empty = document.querySelector('.guide-empty');
  if (!search || !cards.length) return;

  const english = document.documentElement.lang === 'en';
  let category = 'all';
  const update = () => {
    const query = search.value.trim().toLocaleLowerCase(document.documentElement.lang);
    let visible = 0;
    cards.forEach(card => {
      const categoryMatches = category === 'all' || card.dataset.category === category;
      const searchMatches = !query || (card.dataset.search || '').includes(query);
      card.hidden = !(categoryMatches && searchMatches);
      if (!card.hidden) visible += 1;
    });
    count.textContent = english
      ? `${visible} ${visible === 1 ? 'guide' : 'guides'} shown`
      : `${visible} ${visible === 1 ? 'Ratgeber' : 'Ratgeber'} angezeigt`;
    empty.hidden = visible !== 0;
  };

  search.addEventListener('input', update);
  buttons.forEach(button => button.addEventListener('click', () => {
    category = button.dataset.filter;
    buttons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    update();
  }));
  update();
})();
