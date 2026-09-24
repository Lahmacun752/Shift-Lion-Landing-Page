(() => {
  const q = id => document.getElementById(id), en = document.documentElement.lang === 'en';
  const M = value => /^\d\d:\d\d$/.test(value || '') ? +value.slice(0, 2) * 60 + +value.slice(3) : NaN;
  const H = value => `${Math.floor(value / 60)}:${String(value % 60).padStart(2, '0')} h`;
  const E = value => new Intl.NumberFormat(en ? 'en-GB' : 'de-DE', {style: 'currency', currency: 'EUR'}).format(value);
  const O = (a, b, c, d) => Math.max(0, Math.min(b, d) - Math.max(a, c));
  const text = en
    ? ['Include Sunday allowance', 'Sunday timing', 'No Sunday allowance', 'Starts on Sunday — until midnight', 'Leads into Sunday — from midnight', 'Whole shift is on Sunday', 'Sunday allowance (%)', 'Eligible Sunday hours', 'Sunday allowance']
    : ['Sonntagszuschlag einbeziehen', 'Sonntagszeit', 'Kein Sonntagszuschlag', 'Startet am Sonntag — bis 00:00 Uhr', 'Führt in den Sonntag — ab 00:00 Uhr', 'Gesamte Schicht am Sonntag', 'Sonntagszuschlag (%)', 'Zuschlagsfähige Sonntagsstunden', 'Sonntagszuschlag'];
  const sunday = document.createElement('div');
  sunday.className = 'sunday-settings';
  sunday.innerHTML = `<label class="toggle-option"><input id="sunOn" type="checkbox"> ${text[0]}</label><div id="sunCfg" hidden><div class="field"><label>${text[1]}</label><select id="sunMode"><option value="none">${text[2]}</option><option value="starts">${text[3]}</option><option value="ends">${text[4]}</option><option value="full">${text[5]}</option></select></div><div class="field"><label>${text[6]}</label><input id="sunRate" type="number" value="50" min="0" step=".1"></div></div>`;
  q('rate').closest('.field').after(sunday);
  q('sunOn').onchange = () => { q('sunCfg').hidden = !q('sunOn').checked; calculate(); };
  document.querySelector('.summary').insertAdjacentHTML('beforeend', `<div class="metric"><span>${text[7]}</span><strong id="sunHours">–</strong></div><div class="metric"><span>${text[8]}</span><strong id="sunExtra">–</strong></div>`);
  const error = message => { q('calculatorError').textContent = message || ''; q('calculatorError').classList.toggle('visible', !!message); };

  function calculate() {
    const start = M(q('start').value), endValue = M(q('end').value), nightStart = M(q('nightStart').value), nightEnd = M(q('nightEnd').value);
    const pause = +q('pause').value, wage = +q('wage').value, rate = +q('rate').value, sundayRate = q('sunOn').checked ? +q('sunRate').value : 0;
    if ([start, endValue, nightStart, nightEnd, pause, wage, rate, sundayRate].some(value => !Number.isFinite(value) || value < 0) || start === endValue) { error(en ? 'Please enter valid values.' : 'Bitte gültige Werte eingeben.'); return; }
    const end = endValue + (endValue < start ? 1440 : 0), duration = end - start;
    if (pause > duration) { error(en ? 'The break cannot be longer than the shift.' : 'Die Pause darf nicht länger als die Schicht sein.'); return; }
    let rawNight = 0;
    for (let day = -1; day <= 1; day++) rawNight += O(start, end, nightStart + day * 1440, nightEnd + day * 1440 + (nightEnd <= nightStart ? 1440 : 0));
    rawNight = Math.min(duration, rawNight);
    const mode = q('sunMode').value;
    const rawSunday = !q('sunOn').checked || mode === 'none' ? 0 : mode === 'full' ? duration : mode === 'starts' ? (endValue < start ? 1440 - start : duration) : (endValue < start ? end - 1440 : -1);
    if (rawSunday < 0) { error(en ? 'For a shift leading into Sunday, choose an earlier end time.' : 'Für eine in den Sonntag führende Schicht ein früheres Ende wählen.'); return; }
    const deducted = q('pauseType').value === 'unpaid' ? pause : 0;
    const paid = duration - deducted, night = Math.max(0, rawNight - deducted), sundayHours = Math.max(0, rawSunday - deducted);
    const base = paid / 60 * wage, nightExtra = night / 60 * wage * rate / 100, sundayExtra = sundayHours / 60 * wage * sundayRate / 100;
    q('total').textContent = H(duration); q('paid').textContent = H(paid); q('night').textContent = H(night); q('sunHours').textContent = H(sundayHours);
    q('base').textContent = E(base); q('extra').textContent = E(nightExtra); q('sunExtra').textContent = E(sundayExtra); q('sum').textContent = E(base + nightExtra + sundayExtra);
    q('formula').textContent = en ? `${H(paid)} paid hours · ${H(night)} night hours · ${H(sundayHours)} Sunday hours` : `${H(paid)} bezahlte Stunden · ${H(night)} Nachtstunden · ${H(sundayHours)} Sonntagsstunden`;
    error();
  }
  document.querySelectorAll('.calculator input,.calculator select').forEach(input => input.addEventListener(input.type === 'checkbox' ? 'change' : 'input', calculate));
  q('calculate').onclick = calculate;
  calculate();
})();
