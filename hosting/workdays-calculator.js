(()=>{
  const q=id=>document.getElementById(id);
  const en=document.documentElement.lang==='en';
  const DAY=86400000;
  const text=en?{
    early:'Early',late:'Late',night:'Night',off:'Off',work:'Work',day:'Day',
    invalid:'The end date must not be before the start date.',
    missing:'Please complete all required dates.',
    tooLong:'Please choose a period of no more than ten years.',
    minCycle:'Your rotation needs at least one day.', vacationInvalid:'Leave cannot end before it starts.', holiday:'Holiday', vacation:'Leave',
    weekdays:['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],
    monthLocale:'en-GB'
  }:{
    early:'Früh',late:'Spät',night:'Nacht',off:'Frei',work:'Arbeit',day:'Tag',
    invalid:'Das Enddatum darf nicht vor dem Startdatum liegen.',
    missing:'Bitte fülle alle benötigten Datumsfelder aus.',
    tooLong:'Bitte wähle einen Zeitraum von höchstens zehn Jahren.',
    minCycle:'Dein Rhythmus benötigt mindestens einen Tag.', vacationInvalid:'Das Urlaubsende darf nicht vor dem Urlaubsbeginn liegen.', holiday:'Feiertag', vacation:'Urlaub',
    weekdays:['Mo','Di','Mi','Do','Fr','Sa','So'],
    monthLocale:'de-DE'
  };
  const labels={E:text.early,L:text.late,N:text.night,O:text.off};
  let rotation=['E','E','L','L','N','N','O','O'];
  let calendarYear=0;
  let calendarMonth=0;

  const pad=value=>String(value).padStart(2,'0');
  const formatDate=(year,month,day)=>`${year}-${pad(month+1)}-${pad(day)}`;
  const parseDate=value=>{
    const match=/^(\d{4})-(\d{2})-(\d{2})$/.exec(value||'');
    return match?Date.UTC(Number(match[1]),Number(match[2])-1,Number(match[3])):NaN;
  };
  const monthKey=(year,month)=>year*12+month;
  const positiveModulo=(value,divisor)=>((value%divisor)+divisor)%divisor;
  const easterSunday=year=>{
    const a=year%19,b=Math.floor(year/100),c=year%100,d=Math.floor(b/4),e=b%4,f=Math.floor((b+8)/25),g=Math.floor((b-f+1)/3),h=(19*a+b-d-g+15)%30,i=Math.floor(c/4),k=c%4,l=(32+2*e+2*i-h-k)%7,m=Math.floor((a+11*h+22*l)/451),month=Math.floor((h+l-7*m+114)/31)-1,day=(h+l-7*m+114)%31+1;
    return Date.UTC(year,month,day);
  };
  const nationwideHolidaySet=(from,to)=>{
    const dates=new Set();
    for(let year=new Date(from).getUTCFullYear();year<=new Date(to).getUTCFullYear();year++){
      [Date.UTC(year,0,1),Date.UTC(year,4,1),Date.UTC(year,9,3),Date.UTC(year,11,25),Date.UTC(year,11,26)].forEach(date=>dates.add(date));
      const easter=easterSunday(year);[-2,1,39,50].forEach(offset=>dates.add(easter+offset*DAY));
    }
    return dates;
  };
  const regionalHolidaySet=(from,to,state)=>{
    const dates=new Set();
    const add=(year,month,day)=>dates.add(Date.UTC(year,month,day));
    const addEaster=(year,offset)=>dates.add(easterSunday(year)+offset*DAY);
    for(let year=new Date(from).getUTCFullYear();year<=new Date(to).getUTCFullYear();year++){
      if(['BW','BY','ST'].includes(state))add(year,0,6);
      if(['BW','BY','HE','NW','RP','SL'].includes(state))addEaster(year,60);
      if(['BW','BY','NW','RP','SL'].includes(state))add(year,10,1);
      if(['BE','MV'].includes(state))add(year,2,8);
      if(['BE','BB','HB','HH','MV','NI','SH','SN','ST','TH'].includes(state))add(year,9,31);
      if(state==='SN'){
        const nov23=Date.UTC(year,10,23);
        dates.add(nov23-((new Date(nov23).getUTCDay()+3)%7)*DAY);
      }
      if(state==='TH')add(year,8,20);
    }
    return dates;
  };
  const shiftFor=time=>{
    if(q('model').value!=='custom')return q('weekdays').querySelector(`input[data-day="${new Date(time).getUTCDay()}"]`)?.checked?'W':'O';
    const reference=parseDate(q('reference').value);
    const index=positiveModulo(Math.round((time-reference)/DAY),rotation.length);
    return rotation[index];
  };
  const setError=message=>{
    const error=q('workdaysError');
    error.textContent=message||'';
    error.classList.toggle('visible',Boolean(message));
  };
  const setWeekdays=days=>{
    q('weekdays').querySelectorAll('input[data-day]').forEach(input=>{input.checked=days.includes(Number(input.dataset.day))});
  };
  const renderRotation=()=>{
    const container=q('sequence');
    container.innerHTML='';
    rotation.forEach((shift,index)=>{
      const field=document.createElement('label');
      field.className=`cycle-day cycle-${shift.toLowerCase()}`;
      const label=document.createElement('span');
      label.textContent=`${text.day} ${index+1}`;
      const select=document.createElement('select');
      select.setAttribute('aria-label',`${text.day} ${index+1}`);
      Object.entries(labels).forEach(([value,name])=>{
        const option=document.createElement('option');option.value=value;option.textContent=name;option.selected=value===shift;select.append(option);
      });
      select.addEventListener('change',()=>{rotation[index]=select.value;field.className=`cycle-day cycle-${select.value.toLowerCase()}`;calculate()});
      field.append(label,select);container.append(field);
    });
    q('removeCycleDay').disabled=rotation.length<=1;
    q('addCycleDay').disabled=rotation.length>=31;
  };
  const updateModel=resetWeekdays=>{
    const custom=q('model').value==='custom';
    q('weekdayEditor').hidden=custom;
    q('referenceField').hidden=!custom;
    q('cycleEditor').hidden=!custom;
    if(resetWeekdays&&!custom)setWeekdays(q('model').value==='6'?[1,2,3,4,5,6]:[1,2,3,4,5]);
    calculate();
  };
  const renderCalendar=(start,end,holidays,vacationStart,vacationEnd)=>{
    const firstMonth=monthKey(new Date(start).getUTCFullYear(),new Date(start).getUTCMonth());
    const lastMonth=monthKey(new Date(end).getUTCFullYear(),new Date(end).getUTCMonth());
    let current=monthKey(calendarYear,calendarMonth);
    if(current<firstMonth||current>lastMonth){calendarYear=new Date(start).getUTCFullYear();calendarMonth=new Date(start).getUTCMonth();current=firstMonth}
    const title=new Intl.DateTimeFormat(text.monthLocale,{month:'long',year:'numeric',timeZone:'UTC'}).format(new Date(Date.UTC(calendarYear,calendarMonth,1)));
    q('calendarTitle').textContent=title;
    q('prevMonth').disabled=current<=firstMonth;
    q('nextMonth').disabled=current>=lastMonth;
    const grid=q('workdaysCalendar');
    grid.innerHTML='';
    const offset=(new Date(Date.UTC(calendarYear,calendarMonth,1)).getUTCDay()+6)%7;
    for(let i=0;i<offset;i++){const blank=document.createElement('span');blank.className='calendar-day blank';blank.setAttribute('aria-hidden','true');grid.append(blank)}
    const totalDays=new Date(Date.UTC(calendarYear,calendarMonth+1,0)).getUTCDate();
    for(let day=1;day<=totalDays;day++){
      const time=Date.UTC(calendarYear,calendarMonth,day);
      const cell=document.createElement('div');
      cell.className='calendar-day';
      if(time<start||time>end){cell.classList.add('outside');cell.innerHTML=`<strong>${day}</strong>`}
      else{
        const shift=shiftFor(time);
        const free=shift==='O';
        const holiday=holidays.has(time);
        const vacation=!free&&Number.isFinite(vacationStart)&&time>=vacationStart&&time<=vacationEnd;
        cell.classList.add(free?'free':'work',`shift-${shift.toLowerCase()}`);
        if(holiday)cell.classList.add('holiday');
        if(vacation)cell.classList.add('vacation');
        const name=vacation?text.vacation:holiday?text.holiday:shift==='W'?text.work:labels[shift];
        cell.innerHTML=`<strong>${day}</strong><small>${name}</small>`;
        cell.setAttribute('aria-label',`${formatDate(calendarYear,calendarMonth,day)}: ${name}`);
      }
      grid.append(cell);
    }
  };
  function calculate(){
    const start=parseDate(q('start').value);
    const end=parseDate(q('end').value);
    const custom=q('model').value==='custom';
    const reference=parseDate(q('reference').value);
    const vacationStart=parseDate(q('vacationStart').value);
    const vacationEnd=parseDate(q('vacationEnd').value);
    if(!Number.isFinite(start)||!Number.isFinite(end)||(custom&&!Number.isFinite(reference))){setError(text.missing);return}
    if(end<start){setError(text.invalid);return}
    if((Number.isFinite(vacationStart)||Number.isFinite(vacationEnd))&&(!Number.isFinite(vacationStart)||!Number.isFinite(vacationEnd))){setError(text.missing);return}
    if(Number.isFinite(vacationStart)&&vacationEnd<vacationStart){setError(text.vacationInvalid);return}
    const days=Math.round((end-start)/DAY)+1;
    if(days>3660){setError(text.tooLong);return}
    if(custom&&!rotation.length){setError(text.minCycle);return}
    setError('');
    const holidays=q('nationwideHolidays').checked?nationwideHolidaySet(start,end):new Set();
    if(q('nationwideHolidays').checked)regionalHolidaySet(start,end,q('state').value).forEach(date=>holidays.add(date));
    let work=0;
    let free=0;
    let holidayDays=0;
    let vacationDays=0;
    for(let time=start;time<=end;time+=DAY){
      const isWork=shiftFor(time)!=='O';
      if(!isWork){free+=1;continue}
      work+=1;
      if(holidays.has(time)){holidayDays+=1;continue}
      if(Number.isFinite(vacationStart)&&time>=vacationStart&&time<=vacationEnd)vacationDays+=1;
    }
    const effectiveWork=work-holidayDays-vacationDays;
    q('total').textContent=String(days);
    q('work').textContent=String(work);
    q('holidays').textContent=String(holidayDays);
    q('vacation').textContent=String(vacationDays);
    q('effectiveWork').textContent=String(effectiveWork);
    q('free').textContent=String(free);
    renderCalendar(start,end,holidays,vacationStart,vacationEnd);
  }

  const now=new Date();
  const monthEnd=new Date(now.getFullYear(),now.getMonth()+1,0);
  q('start').value=formatDate(now.getFullYear(),now.getMonth(),1);
  q('end').value=formatDate(monthEnd.getFullYear(),monthEnd.getMonth(),monthEnd.getDate());
  q('reference').value=q('start').value;
  calendarYear=now.getFullYear();
  calendarMonth=now.getMonth();
  q('model').addEventListener('change',()=>updateModel(true));
  q('weekdays').querySelectorAll('input').forEach(input=>input.addEventListener('change',calculate));
  ['start','end','reference','vacationStart','vacationEnd'].forEach(id=>q(id).addEventListener('change',()=>{if(id==='start'){const start=parseDate(q('start').value);if(Number.isFinite(start)){calendarYear=new Date(start).getUTCFullYear();calendarMonth=new Date(start).getUTCMonth()}}calculate()}));
  q('nationwideHolidays').addEventListener('change',calculate);
  q('state').addEventListener('change',calculate);
  q('addCycleDay').addEventListener('click',()=>{if(rotation.length<31){rotation.push('O');renderRotation();calculate()}});
  q('removeCycleDay').addEventListener('click',()=>{if(rotation.length>1){rotation.pop();renderRotation();calculate()}});
  q('calculate').addEventListener('click',calculate);
  q('prevMonth').addEventListener('click',()=>{calendarMonth-=1;if(calendarMonth<0){calendarMonth=11;calendarYear-=1}calculate()});
  q('nextMonth').addEventListener('click',()=>{calendarMonth+=1;if(calendarMonth>11){calendarMonth=0;calendarYear+=1}calculate()});
  renderRotation();
  setWeekdays([1,2,3,4,5]);
  updateModel(false);
})();
