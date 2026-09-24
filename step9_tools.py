import html


TOOLS = {
    "monats-schichtlohn-rechner.html": ("monthly-pay", "Monats-Schichtlohnrechner", "Berechne Grundlohn und Zuschläge für Früh-, Spät-, Nacht-, Sonn- und Feiertagsschichten.", "en/monthly-shift-pay-calculator.html"),
    "pausenrechner.html": ("break", "Pausenrechner nach Arbeitszeit", "Ermittle die gesetzliche Mindestpause nach der eingegebenen Arbeitszeit.", "en/break-calculator.html"),
    "sonntagszuschlag-rechner.html": ("sunday", "Sonntagszuschlag-Rechner", "Berechne Grundlohn, individuellen Sonntagszuschlag und Bruttosumme.", "en/sunday-allowance-calculator.html"),
    "ruhezeit-rechner.html": ("rest", "Ruhezeitrechner zwischen Schichten", "Prüfe den zeitlichen Abstand zwischen zwei Schichten und vergleiche ihn mit elf Stunden.", "en/rest-period-calculator.html"),
    "urlaubsanspruch-rechner.html": ("leave", "Urlaubsanspruch-Rechner", "Rechne einen Jahresurlaubsanspruch auf Teilzeit- oder Schichtarbeitstage um.", "en/leave-entitlement-calculator.html"),
    "en/monthly-shift-pay-calculator.html": ("monthly-pay", "Monthly Shift Pay Calculator", "Estimate base pay and allowances for early, late, night, Sunday and holiday shifts.", "monats-schichtlohn-rechner.html"),
    "en/break-calculator.html": ("break", "Break Calculator by Working Time", "Estimate the statutory minimum break under the German Working Time Act.", "pausenrechner.html"),
    "en/sunday-allowance-calculator.html": ("sunday", "Sunday Allowance Calculator", "Calculate base pay, your individual Sunday allowance and gross total.", "sonntagszuschlag-rechner.html"),
    "en/rest-period-calculator.html": ("rest", "Rest Period Calculator Between Shifts", "Check the time between two shifts against the general eleven-hour rule in Germany.", "ruhezeit-rechner.html"),
    "en/leave-entitlement-calculator.html": ("leave", "Leave Entitlement Calculator", "Convert annual leave to your part-time or shift-work schedule.", "urlaubsanspruch-rechner.html"),
}


def field(identifier, label, value, kind="number", step="0.25", minimum="0"):
    attrs = f'type="{kind}" value="{value}"'
    if kind == "number":
        attrs += f' min="{minimum}" step="{step}"'
    return f'<div class="field"><label for="{identifier}">{html.escape(label)}</label><input id="{identifier}" {attrs}></div>'


def form(kind, en):
    if kind == "monthly-pay":
        labels = (("wage", "Hourly wage (€)", "20", ".01"), ("early", "Early-shift hours", "80", ".25"), ("late", "Late-shift hours", "40", ".25"), ("lateRate", "Late allowance (%)", "10", ".1"), ("night", "Night hours", "40", ".25"), ("nightRate", "Night allowance (%)", "25", ".1"), ("sunday", "Sunday hours", "8", ".25"), ("sundayRate", "Sunday allowance (%)", "50", ".1"), ("holiday", "Holiday hours", "0", ".25"), ("holidayRate", "Holiday allowance (%)", "100", ".1")) if en else (("wage", "Stundenlohn (€)", "20", ".01"), ("early", "Frühschichtstunden", "80", ".25"), ("late", "Spätschichtstunden", "40", ".25"), ("lateRate", "Spätzuschlag (%)", "10", ".1"), ("night", "Nachtstunden", "40", ".25"), ("nightRate", "Nachtzuschlag (%)", "25", ".1"), ("sunday", "Sonntagsstunden", "8", ".25"), ("sundayRate", "Sonntagszuschlag (%)", "50", ".1"), ("holiday", "Feiertagsstunden", "0", ".25"), ("holidayRate", "Feiertagszuschlag (%)", "100", ".1"))
        return "".join(field(*item) for item in labels)
    if kind == "break":
        return field("hours", "Working time excluding breaks (hours)" if en else "Arbeitszeit ohne Pausen (Stunden)", "8", "0.25")
    if kind == "sunday":
        labels = (("hours", "Sunday hours", "8", ".25"), ("wage", "Hourly wage (€)", "20", ".01"), ("rate", "Sunday allowance (%)", "50", ".1")) if en else (("hours", "Sonntagsstunden", "8", ".25"), ("wage", "Stundenlohn (€)", "20", ".01"), ("rate", "Sonntagszuschlag (%)", "50", ".1"))
        return "".join(field(*item) for item in labels)
    if kind == "rest":
        return field("shiftEnd", "Previous shift ends" if en else "Vorherige Schicht endet", "2026-09-22T22:00", "datetime-local") + field("nextStart", "Next shift starts" if en else "Nächste Schicht beginnt", "2026-09-23T09:00", "datetime-local")
    labels = (("fullLeave", "Annual leave at reference schedule", "30", "0.5"), ("referenceDays", "Reference workdays per week", "5", "0.5"), ("actualDays", "Your workdays per week", "3", "0.5"), ("months", "Full months employed this year", "12", "1")) if en else (("fullLeave", "Jahresurlaub im Referenzmodell", "30", "0.5"), ("referenceDays", "Arbeitstage pro Woche im Referenzmodell", "5", "0.5"), ("actualDays", "Deine Arbeitstage pro Woche", "3", "0.5"), ("months", "Volle Beschäftigungsmonate im Jahr", "12", "1"))
    return "".join(field(*item) for item in labels)


def result_rows(kind, en):
    labels = {
        "monthly-pay": (("hoursResult", "Total hours" if en else "Stunden gesamt"), ("baseResult", "Base pay" if en else "Grundlohn"), ("allowanceResult", "Allowances" if en else "Zuschläge"), ("totalResult", "Gross total" if en else "Gesamt brutto")),
        "break": (("breakResult", "Minimum break" if en else "Mindestpause"), ("splitResult", "Possible split" if en else "Mögliche Aufteilung"), ("netResult", "Attendance incl. break" if en else "Anwesenheit inkl. Pause")),
        "sunday": (("baseResult", "Base pay" if en else "Grundlohn"), ("allowanceResult", "Sunday allowance" if en else "Sonntagszuschlag"), ("totalResult", "Gross total" if en else "Gesamt brutto")),
        "rest": (("restResult", "Rest period" if en else "Ruhezeit"), ("differenceResult", "Compared with 11 hours" if en else "Vergleich mit 11 Stunden"), ("statusResult", "Assessment" if en else "Einordnung")),
        "leave": (("annualResult", "Converted annual leave" if en else "Umgerechneter Jahresurlaub"), ("partialResult", "For entered months" if en else "Für eingegebene Monate"), ("weeksResult", "Equivalent weeks off" if en else "Entspricht freien Wochen")),
    }[kind]
    return "".join(f'<div class="metric{" metric-highlight" if index == len(labels)-1 else ""}"><span>{label}</span><strong id="{identifier}">–</strong></div>' for index, (identifier, label) in enumerate(labels))


def render(path, item):
    kind, title, description, pair = item
    en = path.startswith("en/")
    lang = "en" if en else "de"
    home = "/en/" if en else "/"
    tools = "/en/tools/" if en else "/tools/"
    calculate = "Calculate result" if en else "Ergebnis berechnen"
    source = "German Working Time Act, sections 4 and 5" if en else "Arbeitszeitgesetz § 4 und § 5"
    source_url = "https://www.gesetze-im-internet.de/arbzg/BJNR117100994.html"
    legal = "This calculator provides general guidance for Germany. Collective agreements, employment contracts, sector rules and individual circumstances may differ." if en else "Der Rechner bietet eine allgemeine Orientierung für Deutschland. Tarifvertrag, Arbeitsvertrag, Branchenregeln und der Einzelfall können abweichen."
    if kind == "leave":
        source = "German Federal Leave Act, sections 3 and 5" if en else "Bundesurlaubsgesetz § 3 und § 5"
        source_url = "https://www.gesetze-im-internet.de/burlg/"
    return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)} | Shift Lion</title><meta name="description" content="{html.escape(description, quote=True)}"><link rel="canonical" href="https://shiftlion.app/{path}"><link rel="alternate" hreflang="{lang}" href="https://shiftlion.app/{path}"><link rel="alternate" hreflang="{'de' if en else 'en'}" href="https://shiftlion.app/{pair}"><link rel="icon" href="/favicon.png"><link rel="stylesheet" href="/calculator-tools.css?v=6"><link rel="stylesheet" href="/new-calculators.css?v=1"><link rel="stylesheet" href="/tool-foundation.css?v=3"></head><body data-calculator="{kind}"><header class="hero"><div class="topbar"><a href="{home}"><img class="logo" src="/Shift-Lion-Logo-groß.png" alt="Shift Lion"></a></div><div class="eyebrow">{"Free shift-work calculator" if en else "Kostenloser Rechner für Schichtarbeit"}</div><h1>{html.escape(title)}</h1><p>{html.escape(description)}</p></header><main class="layout"><section class="calculator"><h2>{"Enter your details" if en else "Deine Angaben"}</h2><div class="settings">{form(kind, en)}</div><p class="calculator-error" id="newCalculatorError" role="alert"></p><button id="calculate" class="button primary" type="button">{calculate}</button><div class="summary">{result_rows(kind, en)}</div><p id="formula" class="calculation-note" aria-live="polite"></p><p class="hint">{html.escape(legal)} <a href="{source_url}" target="_blank" rel="noopener">{html.escape(source)} ↗</a></p></section><section class="info-card"><h2>{"How the result is calculated" if en else "So wird das Ergebnis berechnet"}</h2><p>{html.escape(description)} {"Enter your actual contractual rates where applicable." if en else "Trage bei Zuschlägen deine tatsächlich vereinbarten Sätze ein."}</p></section><section class="app-cta"><div><h2>{"Keep the complete month in view." if en else "Den ganzen Monat im Blick behalten."}</h2><p>{"Plan shifts, days off and appointments together in Shift Lion." if en else "Plane Schichten, freie Tage und Termine gemeinsam mit Shift Lion."}</p></div><a href="/download/android/">{"Download Shift Lion" if en else "Shift Lion herunterladen"}</a></section></main><script src="/new-calculators.js?v=1"></script><script src="/tool-foundation.js?v=4"></script></body></html>'''
