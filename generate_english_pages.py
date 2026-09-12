from pathlib import Path
from html import escape

ROOT = Path(__file__).parent
OUT = ROOT / "src" / "pages" / "en"

pages = {
  "fruehschicht-tipps.html": ("Early Shift Tips", "Start early shifts with less fatigue and more structure.", [
    ("Prepare the evening before", "Lay out clothes, pack your bag and prepare breakfast so the morning needs fewer decisions."),
    ("Protect your bedtime", "Move bedtime forward gradually and reduce bright screens before sleep."),
    ("Use light and movement", "Bright light after waking and a few minutes of movement can help your body become alert."),
    ("Plan caffeine carefully", "Use coffee early in the shift and avoid carrying caffeine into your next sleep window."),
    ("Keep free time realistic", "Do not overload the afternoon after an early shift. Recovery is part of the plan."),
  ]),
  "spaetschicht-tipps.html": ("Late Shift Tips", "Organize late shifts without losing your entire day.", [
    ("Use the morning intentionally", "Complete one important personal task before work instead of waiting for the evening."),
    ("Plan your main meal", "Eat a balanced meal before the shift and keep the late meal lighter."),
    ("Create a wind-down routine", "Reduce light, noise and screen time after work so your body can switch off."),
    ("Coordinate shared time", "Mark mornings and days off clearly so family and friends know when you are available."),
    ("Avoid filling every gap", "Leave space for recovery between errands, work and sleep."),
  ]),
  "nachtschicht-tipps.html": ("Night Shift Tips", "Stay more alert at night and recover better afterwards.", [
    ("Prepare before the first night", "A planned nap and a calm day can make the transition into night work easier."),
    ("Use light deliberately", "Bright light during the first part of the shift supports alertness; reduce morning light on the way home."),
    ("Choose lighter meals", "Heavy meals at night often increase fatigue. Prefer light, filling food and water."),
    ("Stop caffeine early enough", "Avoid caffeine near the end of the shift so it does not interfere with daytime sleep."),
    ("Protect daytime sleep", "Darkness, a cool room, silence and clear agreements at home help you recover."),
    ("Plan the transition back", "After the final night shift, use a deliberate sleep plan instead of leaving the change to chance."),
  ]),
  "schichtarbeit-schlaf.html": ("Sleep and Shift Work", "Build better sleep routines around early, late and night shifts.", [
    ("Darken the room", "Blackout curtains, an eye mask and fewer notifications can improve daytime sleep."),
    ("Keep repeatable routines", "Similar steps before sleep help your body recognize that the workday is over."),
    ("Manage light", "Seek bright light when you need to wake up and reduce it before your planned sleep."),
    ("Time caffeine", "Use caffeine as a tool early in the shift, not as a replacement for recovery."),
    ("Plan sleep with your roster", "Seeing upcoming shifts early makes naps, appointments and recovery easier to coordinate."),
  ]),
  "schichtarbeit-ernaehrung.html": ("Nutrition and Shift Work", "Plan meals that support energy without making sleep harder.", [
    ("Build a reliable base", "Water, protein and regular meals are more sustainable than relying on coffee and snacks."),
    ("Prepare early-shift food", "A small prepared breakfast can be easier than starting the shift completely empty."),
    ("Eat before late shifts", "Have the larger meal earlier and choose something lighter after work."),
    ("Keep night meals light", "Simple, filling meals usually work better at night than heavy food or constant sugar."),
    ("Use meal prep", "Prepared meals reduce vending-machine choices and save time on demanding workdays."),
    ("Connect food and sleep", "Meal timing is part of recovery, especially before daytime sleep after a night shift."),
  ]),
  "schichtarbeit-alltag.html": ("Daily Life with Shift Work", "Create more structure despite changing working hours.", [
    ("Use flexible routines", "Keep a small set of repeatable habits even when the exact time changes."),
    ("Plan before the week begins", "Mark work, appointments and recovery time before additional commitments fill the calendar."),
    ("Manage energy, not only time", "Place demanding tasks where your energy is usually strongest."),
    ("Coordinate family logistics", "Share shifts and free days early to simplify childcare, appointments and events."),
    ("Keep one clear calendar", "A central shift calendar reduces misunderstandings and last-minute planning."),
  ]),
  "schichtarbeit-familie.html": ("Shift Work and Family", "Coordinate family life and find more usable time together.", [
    ("Share the roster early", "Make upcoming shifts visible before appointments and family plans are fixed."),
    ("Find shared days off", "Compare schedules instead of checking every day manually."),
    ("Plan quality time", "Short, protected time together can matter more than waiting for a perfect free weekend."),
    ("Coordinate responsibilities", "Agree who handles school, childcare, errands and recovery periods."),
    ("Keep plans realistic", "Leave buffer for fatigue and unexpected changes in the roster."),
  ]),
  "schichtarbeit-beziehung.html": ("Relationships and Shift Work", "Protect connection and shared time despite different schedules.", [
    ("Make schedules visible", "Knowing each other's shifts reduces misunderstandings about availability."),
    ("Create small rituals", "A shared breakfast, message or walk can keep connection stable across changing shifts."),
    ("Plan time together", "Treat shared free time as a real appointment instead of hoping it appears."),
    ("Respect recovery", "Tiredness after difficult shifts is not rejection. Discuss rest needs clearly."),
    ("Review what works", "Regularly adjust routines when rotations or family responsibilities change."),
  ]),
  "schichtarbeit-fitness.html": ("Fitness and Shift Work", "Train consistently without fighting your recovery.", [
    ("Use a flexible plan", "Choose sessions by energy and shift type rather than fixed weekdays only."),
    ("Keep minimum sessions", "Short workouts maintain consistency when a full session is unrealistic."),
    ("Avoid hard training exhausted", "After demanding nights, recovery may be the better performance decision."),
    ("Prepare food and equipment", "A packed bag and planned meal reduce friction around the session."),
    ("Track the whole rotation", "Judge progress across several weeks, not by one unusual shift week."),
  ]),
  "schichtarbeit-stress.html": ("Stress and Shift Work", "Recognize pressure early and create more control in your schedule.", [
    ("Identify the real stressors", "Separate workload, sleep loss, family logistics and unpredictable changes."),
    ("Protect recovery blocks", "Reserve time after demanding shifts before adding errands or social plans."),
    ("Reduce planning chaos", "One clear calendar removes repeated decisions and forgotten commitments."),
    ("Communicate limits", "Tell family and colleagues when rest or uninterrupted sleep is necessary."),
    ("Seek support when needed", "Persistent exhaustion, anxiety or sleep problems deserve professional support."),
  ]),
}

def page_html(filename, title, lead, items):
    cards = "".join(f'<div class="feature"><h3>{escape(h)}</h3><p>{escape(p)}</p></div>' for h,p in items)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} | Shift Lion</title><meta name="description" content="{escape(lead)}"><link rel="canonical" href="https://shiftlion.app/en/{filename}"><link rel="alternate" hreflang="de" href="https://shiftlion.app/{filename}"><link rel="alternate" hreflang="en" href="https://shiftlion.app/en/{filename}"><link rel="icon" href="../favicon.png"><link rel="stylesheet" href="page.css"><link rel="stylesheet" href="en-site.css"></head><body><main class="app"><section class="hero"><img src="../Shift-Lion-Logo-groß.png" alt="Shift Lion" class="brand-logo"><h1>{escape(title)}</h1><p class="lead">{escape(lead)}</p><a class="btn" href="/download/android/">Download Shift Lion</a></section><section class="section"><div class="panel"><h2>Why this matters</h2><p>Changing shifts affect sleep, energy, appointments and time with other people. A clear plan makes the next step easier to see.</p></div><div class="panel"><h2>Practical tips</h2><div class="feature-grid">{cards}</div></div><div class="panel"><h2>Plan around your real rotation</h2><p>Shift Lion helps you keep shifts, days off and appointments in one place and compare schedules with the people who matter.</p></div><div class="panel"><h2>Frequently asked questions</h2><h3>Do these tips work for rotating schedules?</h3><p>Yes. Adapt them to your shift sequence, personal health and recovery needs.</p><h3>Can planning reduce shift-work stress?</h3><p>A clear overview cannot remove every burden, but it can reduce uncertainty and last-minute conflicts.</p></div></section><section class="cta"><h2>Bring more clarity to your shift life.</h2><p>Plan work, recovery and shared time with Shift Lion.</p><a class="btn" href="/download/android/">Download Shift Lion</a></section></main><script src="en-site.js?v=3"></script></body></html>'''

OUT.mkdir(parents=True, exist_ok=True)
for filename, (title, lead, items) in pages.items():
    (OUT / filename).write_text(page_html(filename, title, lead, items), encoding="utf-8")

dienstplan = page_html("dienstplan-app.html", "Duty Roster App for Shift Workers", "Manage early, late and night duties, vacation, appointments and days off on your phone.", [
  ("Custom duties", "Create your own duty names, colors, working times and repeating sequences."),
  ("Monthly overview", "See duties, vacation and free days across your personal calendar."),
  ("Compare rosters", "Find overlaps with partners, friends or colleagues."),
  ("Statistics", "Review working hours and shift distribution over time."),
  ("Local planning", "Use your personal roster without mandatory registration."),
])
(OUT / "dienstplan-app.html").write_text(dienstplan, encoding="utf-8")

# Preserve the German tools and enhance them with an English text layer so all calculations remain identical.
for source_name in ("schichtplaner-online.html", "schichtzulagen-rechner.html"):
    text = (ROOT / "src" / "pages" / source_name).read_text(encoding="utf-8")
    text = text.replace('<html lang="de">', '<html lang="en">')
    text = text.replace('https://shiftlion.app/' + source_name, 'https://shiftlion.app/en/' + source_name)
    text = text.replace('href="/"', 'href="/en/"')
    text = text.replace('href="/schichtplaner.html"', 'href="/en/schichtplaner.html"')
    text = text.replace('href="/dienstplan-app.html"', 'href="/en/dienstplan-app.html"')
    text = text.replace('href="/schichtplaner-online.html"', 'href="/en/schichtplaner-online.html"')
    text = text.replace('href="/schichtzulagen-rechner.html"', 'href="/en/schichtzulagen-rechner.html"')
    text = text.replace('Flexibel', 'Flexible').replace('Hauptnavigation', 'Main navigation')
    if source_name == "schichtplaner-online.html":
        text = text.replace('<title>Schichtplaner Online – Kostenlos Schichtplan erstellen | Shift Lion</title>', '<title>Online Shift Planner – Create a Free Shift Schedule | Shift Lion</title>')
        text = text.replace('content="Schichtplaner Online', 'content="Online Shift Planner')
    else:
        text = text.replace('<title>Schichtzulagen Rechner', '<title>Shift Allowance Calculator')
        text = text.replace('content="Schichtzulagen Rechner', 'content="Shift Allowance Calculator')
    head, closing = text.rsplit('</body>', 1)
    text = head + '<script src="en-tools.js?v=9"></script></body>' + closing
    (OUT / source_name).write_text(text, encoding="utf-8")

print(f"Generated {len(pages) + 3} English pages")
