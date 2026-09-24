(() => {
  const q = id => document.getElementById(id), en = document.documentElement.lang === 'en';
  const M = value => /^\d\d:\d\d$/.test(value || '') ? +value.slice(0, 2) * 60 + +value.slice(3) : NaN;
  const H = value => `${Math.floor(value / 60)}:${String(value % 60).padStart(2, '0')} h`;
  const E = value => new Intl.NumberFormat(en ? 'en-GB' : 'de-DE', {style: 'currency', currency: 'EUR'}).format(value);
  const O = (a, b, c, d) => Math.max(0, Math.min(b, d) - Math.max(a, c));
  const T = en
    ? ['Holiday timing', 'Sunday timing', 'No Sunday allowance', 'Starts on the holiday — until midnight', 'Leads into the holiday — from midnight', 'Whole shift is in the holiday period', 'Starts on Sunday — until midnight', 'Leads into Sunday — from midnight', 'Whole shift is on Sunday', 'Include Sunday allowance', 'Sunday allowance (%)', 'If Sunday and holiday overlap', 'Use the higher rate only', 'Add both rates', 'Use my own combined rate', 'Combined allowance (%)', 'Eligible Sunday hours', 'Sunday & holiday overlap', 'Sunday allowance', 'Combined allowance']
    : ['Feiertagszeit', 'Sonntagszeit', 'Kein Sonntagszuschlag', 'Startet am Feiertag — bis 00:00 Uhr', 'Führt in den Feiertag — ab 00:00 Uhr', 'Gesamte Schicht im Feiertagszeitraum', 'Startet am Sonntag — bis 00:00 Uhr', 'Führt in den Sonntag — ab 00:00 Uhr', 'Gesamte Schicht am Sonntag', 'Sonntagszuschlag einbeziehen', 'Sonntagszuschlag (%)', 'Wenn Sonntag und Feiertag gleichzeitig gelten', 'Nur den höheren Satz verwenden', 'Beide Sätze addieren', 'Eigenen Kombisatz verwenden', 'Kombinierter Zuschlag (%)', 'Sonntagsstunden', 'Sonntag & Feiertag gleichzeitig', 'Sonntagszuschlag', 'Kombinationszuschlag'];
  q('holidayDate')?.closest('.field')?.remove();
  const showError = (message = '') => { q('calculatorError').textContent = message; q('calculatorError').classList.toggle('visible', !!message); };
  const root = document.querySelector('.settings');
  const combination = document.createElement('div');
  combination.className = 'allowance-combination';
  combination.innerHTML = `<label class="toggle-option"><input id="sunOn" type="checkbox"> ${T[9]}</label><div id="sunCfg" hidden><div class="field"><label>${T[10]}</label><input id="sunRate" type="number" value="50" min="0" step=".1"></div><div class="field"><label>${T[11]}</label><select id="rule"><option value="high">${T[12]}</option><option value="add">${T[13]}</option><option value="custom">${T[14]}</option></select></div><div class="field" id="customCfg" hidden><label>${T[15]}</label><input id="customRate" type="number" value="150" min="0" step=".1"></div></div>`;
  q('shiftScope').closest('.field').after(combination);
  q('sunOn').onchange = () => { q('sunCfg').hidden = !q('sunOn').checked; calculate(); };
  q('rule').onchange = () => { q('customCfg').hidden = q('rule').value !== 'custom'; calculate(); };
  document.querySelector('.summary').insertAdjacentHTML('beforeend', `<div class="metric"><span>${T[16]}</span><strong id="sunH">–</strong></div><div class="metric"><span>${T[17]}</span><strong id="bothH">–</strong></div><div class="metric"><span>${T[18]}</span><strong id="sunX">–</strong></div><div class="metric"><span>${T[19]}</span><strong id="bothX">–</strong></div>`);
  const modeFields = () => `<div class="field"><label>${T[0]}</label><select class="hm"><option value="starts">${T[3]}</option><option value="ends">${T[4]}</option><option value="full">${T[5]}</option></select><label>${T[1]}</label><select class="sm"><option value="none">${T[2]}</option><option value="starts">${T[6]}</option><option value="ends">${T[7]}</option><option value="full">${T[8]}</option></select></div>`;
  const list = [{s: q('start'), e: q('end'), p: q('pause')}];
  const firstWrapper = document.createElement('div');
  firstWrapper.innerHTML = modeFields();
  q('pauseType').closest('.field').after(...firstWrapper.children);
  list[0].hm = document.querySelector('.hm'); list[0].sm = document.querySelector('.sm');
  const extra = document.createElement('div'); root.after(extra);
  const add = document.createElement('button'); add.type = 'button'; add.className = 'button secondary'; add.textContent = en ? '＋ Add another holiday shift' : '＋ Weitere Feiertagsschicht hinzufügen'; extra.after(add);
  add.onclick = () => {
    const row = document.createElement('section'); row.className = 'holiday-shift-row';
    row.innerHTML = `<div class="holiday-shift-fields"><div class="field"><label>${en ? 'Shift starts' : 'Schichtbeginn'}</label><input class="s" type="time" value="22:00"></div><div class="field"><label>${en ? 'Shift ends' : 'Schichtende'}</label><input class="e" type="time" value="06:00"></div><div class="field"><label>${en ? 'Break' : 'Pause'} (Min.)</label><input class="p" type="number" value="30" min="0"></div>${modeFields()}</div>`;
    extra.append(row);
    list.push({s: row.querySelector('.s'), e: row.querySelector('.e'), p: row.querySelector('.p'), hm: row.querySelector('.hm'), sm: row.querySelector('.sm')});
    row.querySelectorAll('input,select').forEach(input => input.addEventListener('input', calculate)); calculate();
  };
  const span = (mode, start, end, overnight) => mode === 'none' ? [0, 0] : mode === 'full' ? [start, end] : mode === 'starts' ? (overnight ? [start, 1440] : [start, end]) : mode === 'ends' ? (overnight ? [1440, end] : null) : null;

  function calculate() {
    let paid = 0, holidayHours = 0, sundayHours = 0, bothHours = 0, holidayOnly = 0, sundayOnly = 0;
    const unpaid = q('pauseType').value === 'unpaid';
    for (const shift of list) {
      const start = M(shift.s.value), endValue = M(shift.e.value), pause = +shift.p.value;
      if ([start, endValue, pause].some(value => !Number.isFinite(value) || value < 0) || start === endValue) { showError(en ? 'Please enter valid shift values.' : 'Bitte gültige Schichtwerte eingeben.'); return; }
      const overnight = endValue < start, end = endValue + (overnight ? 1440 : 0), holiday = span(shift.hm.value, start, end, overnight), sunday = q('sunOn').checked ? span(shift.sm.value, start, end, overnight) : [0, 0];
      if (!holiday || !sunday) { showError(en ? 'Choose an earlier end time for a shift leading into Sunday or a holiday.' : 'Für eine in Sonntag oder Feiertag führende Schicht ein früheres Ende wählen.'); return; }
      if (pause > end - start) { showError(en ? 'The break cannot be longer than the shift.' : 'Die Pause darf nicht länger als die Schicht sein.'); return; }
      const deduction = unpaid ? pause : 0;
      const rawHoliday = holiday[1] - holiday[0], rawSunday = sunday[1] - sunday[0], rawBoth = O(...holiday, ...sunday);
      const eligibleHoliday = Math.max(0, rawHoliday - deduction), eligibleSunday = Math.max(0, rawSunday - deduction), eligibleBoth = Math.max(0, rawBoth - deduction);
      paid += end - start - deduction; holidayHours += eligibleHoliday; sundayHours += eligibleSunday; bothHours += eligibleBoth;
      holidayOnly += Math.max(0, eligibleHoliday - eligibleBoth); sundayOnly += Math.max(0, eligibleSunday - eligibleBoth);
    }
    const wage = +q('wage').value, holidayRate = +q('rate').value, sundayRate = q('sunOn').checked ? +q('sunRate').value : 0, customRate = +q('customRate').value, shiftRate = +q('shiftRate').value;
    if ([wage, holidayRate, sundayRate, customRate, shiftRate].some(value => !Number.isFinite(value) || value < 0)) { showError(en ? 'Please enter valid rates.' : 'Bitte gültige Sätze eingeben.'); return; }
    const combinedRate = q('rule').value === 'add' ? holidayRate + sundayRate : q('rule').value === 'custom' ? customRate : Math.max(holidayRate, sundayRate);
    const base = paid / 60 * wage, holidayExtra = holidayOnly / 60 * wage * holidayRate / 100, sundayExtra = sundayOnly / 60 * wage * sundayRate / 100, combinedExtra = bothHours / 60 * wage * combinedRate / 100;
    const shiftExtra = (q('shiftScope').value === 'holiday' ? holidayHours : paid) / 60 * wage * shiftRate / 100;
    q('hours').textContent = H(paid); q('holidayHours').textContent = H(holidayHours); q('sunH').textContent = H(sundayHours); q('bothH').textContent = H(bothHours);
    q('base').textContent = E(base); q('extra').textContent = E(holidayExtra); q('sunX').textContent = E(sundayExtra); q('bothX').textContent = E(combinedExtra); q('shiftExtra').textContent = E(shiftExtra); q('sum').textContent = E(base + holidayExtra + sundayExtra + combinedExtra + shiftExtra);
    q('formula').textContent = en ? `${H(paid)} paid hours · ${H(holidayHours)} holiday hours · ${H(sundayHours)} Sunday hours · ${H(bothHours)} overlap` : `${H(paid)} bezahlte Stunden · ${H(holidayHours)} Feiertagsstunden · ${H(sundayHours)} Sonntagsstunden · ${H(bothHours)} Überschneidung`;
    showError();
  }
  document.querySelectorAll('.calculator input,.calculator select').forEach(input => input.addEventListener(input.type === 'checkbox' ? 'change' : 'input', calculate));
  q('calculate').onclick = calculate;
  calculate();
})();
