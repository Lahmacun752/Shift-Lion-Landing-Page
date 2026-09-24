from pathlib import Path
import json, shutil, html, re
from guide_data import GUIDES
from step9_tools import TOOLS as STEP9_TOOLS, render as render_step9_tool
from trust_pages import PAGES as TRUST_PAGES, render as render_trust_page
from reach_pages import PAGES as REACH_PAGES, render as render_reach_page

ROOT = Path(__file__).parent
SRC = ROOT / "src" / "pages"
STATIC = ROOT / "static"
OUT = ROOT / "hosting"
CONFIG = json.loads((ROOT / "site.json").read_text(encoding="utf-8"))

LEGACY_REDIRECT_PAGES = {"en/fruehschicht-tipps-englisch.html"}

CONTENT_IMAGES = {
    "Shift-Lion-Logo-groß.png": ("Shift-Lion-Logo-320.webp", 320, 171),
    "vorstellungsgrafik1.png": ("vorstellungsgrafik1-640.webp", 640, 1137),
    "tools-bild-deutsch.png": ("tools-bild-deutsch.webp", 1536, 1024),
    "tools-bild-englisch.png": ("tools-bild-englisch.webp", 1536, 1024),
    "kalender.jpg": ("kalender.webp", 1272, 2772),
    "schichtvergleich.png": ("schichtvergleich.webp", 1024, 1536),
    "statistik_neu.png": ("statistik_neu.webp", 941, 1672),
    "lohnrechner.png": ("lohnrechner.webp", 1024, 1536),
    "backup.png": ("backup.webp", 1536, 1024),
    "kalender_englisch.png": ("kalender_englisch.webp", 941, 1672),
    "schichtvergleich_englisch.png": ("schichtvergleich_englisch.webp", 1024, 1536),
    "statistik_englisch.png": ("statistik_englisch.webp", 1024, 1536),
    "lohnrechner_englisch.png": ("lohnrechner_englisch.webp", 1024, 1536),
    "backup_englisch.png": ("backup_englisch.webp", 1086, 1448),
}

TOOL_PAGES = {
    "arbeitszeitrechner.html", "nachtzuschlag-rechner.html",
    "ueberstunden-rechner.html", "stundenlohn-rechner.html",
    "arbeitstage-rechner.html", "feiertagszuschlag-rechner.html",
    "schichten-vergleichen.html", "schichtplaner-online.html",
    "schichtzulagen-rechner.html", "working-time-calculator.html",
    "night-allowance-calculator.html", "overtime-calculator.html",
    "hourly-wage-calculator.html", "workdays-calculator.html",
    "holiday-allowance-calculator.html", "compare-shifts.html",
}

# Metadata is generated during every build, so it cannot drift from the
# published URLs.  The page content remains in the source HTML; this block
# only adds search-engine information to the document head.
SEO_TITLES = {
    "arbeitszeitrechner.html": "Arbeitszeitrechner mit Pause & Überstunden | Shift Lion",
    "arbeitstage-rechner.html": "Arbeitstage-Rechner für Schichtarbeit | Shift Lion",
    "feiertagszuschlag-rechner.html": "Feiertagszuschlag-Rechner bei Nachtschicht | Shift Lion",
    "nachtzuschlag-rechner.html": "Nachtzuschlag-Rechner: Nachtstunden berechnen | Shift Lion",
    "stundenlohn-rechner.html": "Stundenlohn-Rechner: Gehalt umrechnen | Shift Lion",
    "schichten-vergleichen.html": "Schichten vergleichen & gemeinsame freie Tage finden | Shift Lion",
    "schichtplaner-online.html": "Schichtplaner online: Monats- & Jahresplan erstellen | Shift Lion",
    "schichtzulagen-rechner.html": "Schichtzulagen-Rechner 2026: Zuschläge berechnen | Shift Lion",
    "schichtplaner.html": "Schichtplaner-App für den persönlichen Schichtkalender | Shift Lion",
    "dienstplan-app.html": "Dienstplan-App: Arbeitgeberplan persönlich übertragen | Shift Lion",
    "en/working-time-calculator.html": "Working Time Calculator with Breaks & Overtime | Shift Lion",
    "en/workdays-calculator.html": "Workdays Calculator for Shift Work | Shift Lion",
    "en/holiday-allowance-calculator.html": "Holiday Allowance Calculator for Overnight Shifts | Shift Lion",
    "en/night-allowance-calculator.html": "Night Allowance Calculator: Calculate Night Hours | Shift Lion",
    "en/hourly-wage-calculator.html": "Hourly Wage Calculator: Convert Your Salary | Shift Lion",
    "en/compare-shifts.html": "Compare Shifts & Find Shared Days Off | Shift Lion",
    "en/schichtplaner-online.html": "Online Shift Planner: Create a Free Shift Schedule | Shift Lion",
    "en/schichtzulagen-rechner.html": "Shift Allowance Calculator: Calculate Allowances | Shift Lion",
    "en/schichtplaner.html": "Personal Shift Calendar App for Shift Workers | Shift Lion",
    "en/dienstplan-app.html": "Duty Roster App: Transfer Your Employer Schedule | Shift Lion",
}

SEO_DESCRIPTIONS = {
    "index.html": "Shift Lion hilft Schichtarbeitern, Schichtrhythmen zu planen, Dienstpläne zu vergleichen und gemeinsame freie Tage zu finden.",
    "arbeitszeitrechner.html": "Arbeitszeit kostenlos berechnen: Bruttozeit, Pausen, Nettoarbeitszeit und Überstunden für mehrere Schichten – auch über Mitternacht.",
    "arbeitstage-rechner.html": "Berechne Arbeitstage und freie Tage für 5-Tage-Woche, 6-Tage-Woche oder deinen individuellen Schichtrhythmus.",
    "feiertagszuschlag-rechner.html": "Feiertagszuschlag für Tag- und Nachtschichten berechnen – mit Pausen, Schichtzulage und klarer Aufschlüsselung.",
    "nachtzuschlag-rechner.html": "Nachtstunden und Nachtzuschlag inklusive bezahlter oder unbezahlter Pausen kostenlos berechnen.",
    "ueberstunden-rechner.html": "Überstunden kostenlos berechnen und Auszahlung mit Freizeitausgleich vergleichen – inklusive eigener Zuschläge.",
    "stundenlohn-rechner.html": "Monats- oder Jahresgehalt kostenlos in einen vergleichbaren Stundenlohn umrechnen.",
    "schichten-vergleichen.html": "Vergleiche zwei Schichtrhythmen und finde gemeinsame freie Tage direkt im Monatskalender.",
    "schichtplaner-online.html": "Schichtplan kostenlos online erstellen: Rhythmus eingeben, Monats- und Jahresplan anzeigen, als PDF speichern oder direkt ausdrucken.",
    "schichtzulagen-rechner.html": "Schichtzulagen kostenlos berechnen: Grundlohn, Nacht-, Spät-, Sonntags- und Feiertagszuschläge mit eigenen Arbeitszeiten und Prozentsätzen.",
    "schichtplaner.html": "Persönlicher Schichtkalender für Android: Plane eigene Schichtrhythmen, freie Tage, Termine und gemeinsame Zeit in der Shift-Lion-App.",
    "dienstplan-app.html": "Übertrage den fertigen Dienstplan deines Arbeitgebers in deinen persönlichen Kalender und ergänze Urlaub, Termine und freie Tage.",
    "en/index.html": "Shift Lion helps shift workers plan rotations, compare schedules and find shared days off with family and friends.",
    "en/working-time-calculator.html": "Calculate gross time, paid breaks, net working time and overtime for multiple shifts, including overnight work.",
    "en/workdays-calculator.html": "Calculate workdays and days off for a 5-day week, 6-day week or your individual shift rotation.",
    "en/holiday-allowance-calculator.html": "Calculate holiday and shift allowances for day and overnight shifts, including paid or unpaid breaks.",
    "en/night-allowance-calculator.html": "Calculate night hours and night allowance including paid or unpaid breaks.",
    "en/overtime-calculator.html": "Calculate overtime pay and compare it with time off in lieu, including your own allowance rate.",
    "en/hourly-wage-calculator.html": "Convert a monthly or annual salary into a comparable hourly wage for free.",
    "en/compare-shifts.html": "Compare two shift rotations and find shared days off directly in the monthly calendar.",
    "en/schichtplaner-online.html": "Create a free online shift schedule: enter your rotation and generate monthly and yearly plans as a PDF.",
    "en/schichtzulagen-rechner.html": "Calculate night, late, Sunday and holiday allowances from your hourly wage, hours and own rates.",
    "en/schichtplaner.html": "Create a personal shift calendar for rotating schedules, days off, appointments and shared time in the Shift Lion Android app.",
    "en/dienstplan-app.html": "Transfer the duty roster created by your employer into a personal calendar and add leave, appointments and days off.",
}

LANGUAGE_PAIRS = {
    "arbeitszeitrechner.html": "en/working-time-calculator.html",
    "arbeitstage-rechner.html": "en/workdays-calculator.html",
    "feiertagszuschlag-rechner.html": "en/holiday-allowance-calculator.html",
    "nachtzuschlag-rechner.html": "en/night-allowance-calculator.html",
    "ueberstunden-rechner.html": "en/overtime-calculator.html",
    "stundenlohn-rechner.html": "en/hourly-wage-calculator.html",
    "schichten-vergleichen.html": "en/compare-shifts.html",
}

APP_PAGE_NAMES = {
    "index.html", "schichtplaner.html", "dienstplan-app.html",
    "en/index.html", "en/schichtplaner.html", "en/dienstplan-app.html",
}

GUIDE_PAGE_NAMES = {
    "fruehschicht-tipps.html", "spaetschicht-tipps.html", "nachtschicht-tipps.html",
    "schichtarbeit-schlaf.html", "schichtarbeit-fitness.html",
    "schichtarbeit-ernaehrung.html", "schichtarbeit-alltag.html",
    "schichtarbeit-familie.html", "schichtarbeit-beziehung.html",
    "schichtarbeit-stress.html",
}

GUIDE_PUBLISHED = "2026-09-24"
GUIDE_REVIEWED = "2026-09-24"


def guide_trust_signals(en=False, calculation_guide=False):
    published = "September 24, 2026" if en else "24. September 2026"
    reviewed = "September 24, 2026" if en else "24. September 2026"
    if en:
        links = '<a href="https://www.gesetze-im-internet.de/arbzg/" target="_blank" rel="noopener">German Working Time Act</a>'
        if calculation_guide:
            links += '<a href="https://www.gesetze-im-internet.de/estg/__3b.html" target="_blank" rel="noopener">Income Tax Act § 3b</a>'
        links += '<a href="https://www.baua.de/DE/Themen/Arbeitsgestaltung/Arbeitszeit/Nacht-und-Schichtarbeit" target="_blank" rel="noopener">BAuA: Night and shift work</a>'
        return f'''<section class="guide-trust" aria-label="Article information"><div class="guide-trust-meta"><div><span>Author and publisher</span><strong>Shift Lion editorial team</strong></div><div><span>Published</span><strong><time datetime="{GUIDE_PUBLISHED}">{published}</time></strong></div><div><span>Last reviewed</span><strong><time datetime="{GUIDE_REVIEWED}">{reviewed}</time></strong></div></div><div class="guide-trust-sources"><strong>Official sources</strong>{links}</div><p>This article provides general, non-binding guidance. It does not replace medical, legal, tax or professional advice and cannot assess individual agreements.</p></section>'''
    links = '<a href="https://www.gesetze-im-internet.de/arbzg/" target="_blank" rel="noopener">Arbeitszeitgesetz (ArbZG)</a>'
    if calculation_guide:
        links += '<a href="https://www.gesetze-im-internet.de/estg/__3b.html" target="_blank" rel="noopener">Einkommensteuergesetz § 3b</a>'
    links += '<a href="https://www.baua.de/DE/Themen/Arbeitsgestaltung/Arbeitszeit/Nacht-und-Schichtarbeit" target="_blank" rel="noopener">BAuA: Nacht- und Schichtarbeit</a>'
    return f'''<section class="guide-trust" aria-label="Angaben zum Ratgeber"><div class="guide-trust-meta"><div><span>Autor und Herausgeber</span><strong>Shift Lion Redaktion</strong></div><div><span>Veröffentlicht</span><strong><time datetime="{GUIDE_PUBLISHED}">{published}</time></strong></div><div><span>Zuletzt geprüft</span><strong><time datetime="{GUIDE_REVIEWED}">{reviewed}</time></strong></div></div><div class="guide-trust-sources"><strong>Amtliche Quellen</strong>{links}</div><p>Dieser Ratgeber bietet eine allgemeine, unverbindliche Orientierung. Er ersetzt keine medizinische, rechtliche, steuerliche oder fachliche Beratung und kann individuelle Vereinbarungen nicht prüfen.</p></section>'''


def add_legacy_guide_trust(text, rel):
    if rel.name not in GUIDE_PAGE_NAMES or 'class="guide-trust"' in text:
        return text
    hero_start = text.find('<section class="hero')
    hero_end = text.find('</section>', hero_start)
    if hero_start == -1 or hero_end == -1:
        return text
    hero_end += len('</section>')
    trust = guide_trust_signals(en=bool(rel.parts and rel.parts[0] == "en"))
    text = text[:hero_end] + trust + text[hero_end:]
    return re.sub(r"</head>", '<link rel="stylesheet" href="/guide-trust.css?v=1"></head>', text, count=1, flags=re.I)

TOOL_GUIDES = {
    "arbeitszeitrechner.html": {
        "what": "Der Rechner ermittelt aus Beginn, Ende und Pause die Brutto- und Nettoarbeitszeit mehrerer Schichten. Die Nettozeit wird anschließend mit deiner täglichen Sollzeit verglichen.",
        "example": "06:00 bis 14:00 Uhr sind 8 Stunden brutto. Bei 30 Minuten unbezahlter Pause bleiben 7 Stunden 30 Minuten Nettoarbeitszeit.",
        "formula": "Schichtende − Schichtbeginn − unbezahlte Pause = Nettoarbeitszeit. Nettoarbeitszeit − Sollzeit = Überstunden oder Minusstunden.",
        "limits": "Der Rechner prüft keine tariflichen Arbeitszeitkonten, Rundungsregeln, Bereitschaftszeiten oder gesetzlichen Sonderfälle.",
        "faqs": [("Funktionieren Schichten über Mitternacht?", "Ja. Liegt das Ende vor dem Beginn, behandelt der Rechner das Ende automatisch als Uhrzeit am Folgetag."), ("Wie werden bezahlte Pausen behandelt?", "Mit der Option für bezahlte Pausen bleibt die Pausenzeit in der Nettoarbeitszeit enthalten."), ("Ist das Ergebnis ein offizieller Arbeitszeitnachweis?", "Nein. Es ist eine persönliche Rechenhilfe und ersetzt keinen betrieblichen Arbeitszeitnachweis.")],
        "related": [("Nachtzuschlag berechnen", "/nachtzuschlag-rechner.html"), ("Überstunden vergleichen", "/ueberstunden-rechner.html")],
    },
    "nachtzuschlag-rechner.html": {
        "what": "Der Rechner bestimmt die bezahlten Nachtstunden innerhalb deines gewählten Nachtzeitfensters und berechnet daraus Grundlohn und Nachtzuschlag.",
        "example": "Bei 22:00 bis 06:00 Uhr, 30 Minuten unbezahlter Pause, 20 € Stundenlohn und 25 % Zuschlag entstehen 7:30 bezahlte Nachtstunden, 150 € Grundlohn und 37,50 € Nachtzuschlag.",
        "formula": "Bezahlte Nachtstunden × Stundenlohn × Zuschlagssatz = Nachtzuschlag. Bei einer unbezahlten Pause entfallen Grundlohn und Zuschläge für die Pausenzeit.",
        "limits": "Tarifvertrag, Arbeitsvertrag, steuerliche Behandlung und abweichende betriebliche Nachtzeitfenster werden nur über deine Eingaben, nicht automatisch geprüft.",
        "faqs": [("Kann ich das Nachtzeitfenster ändern?", "Ja. Beginn und Ende der zuschlagsfähigen Nachtzeit lassen sich frei einstellen."), ("Wird eine unbezahlte Pause vom Nachtzuschlag abgezogen?", "Ja. Eine unbezahlte Pause reduziert sowohl die bezahlten Stunden als auch die zuschlagsfähigen Nachtstunden."), ("Kann zusätzlich Sonntagszuschlag berechnet werden?", "Ja. Du kannst Sonntagsarbeit aktivieren und einen eigenen Zuschlagssatz angeben.")],
        "related": [("Feiertagszuschlag berechnen", "/feiertagszuschlag-rechner.html"), ("Arbeitszeit berechnen", "/arbeitszeitrechner.html")],
    },
    "feiertagszuschlag-rechner.html": {
        "what": "Der Rechner teilt eine Schicht in normale, Feiertags- und optional Sonntagsstunden auf. Er zeigt Grundlohn, einzelne Zuschläge und die geschätzte Bruttosumme.",
        "example": "7:30 bezahlte Feiertagsstunden bei 20 € Stundenlohn und 100 % Feiertagszuschlag ergeben 150 € Grundlohn plus 150 € Feiertagszuschlag.",
        "formula": "Feiertagsstunden × Stundenlohn × Feiertagssatz = Feiertagszuschlag. Überschneiden sich Sonntag und Feiertag, gilt die von dir gewählte Kombinationsregel.",
        "limits": "Der Rechner erkennt nicht automatisch, ob ein Datum arbeitsrechtlich als Feiertag gilt. Tarifliche Regeln, Ersatzruhetage, Steuern und regionale Sonderfälle können abweichen.",
        "faqs": [("Wie werden Schichten über Mitternacht aufgeteilt?", "Du wählst, ob die Schicht am Feiertag startet, in den Feiertag führt oder vollständig im Feiertagszeitraum liegt."), ("Was passiert bei einer unbezahlten Pause?", "Die Pause wird vom Grundlohn und von allen aktivierten Zuschlägen abgezogen."), ("Können Sonntag und Feiertag gleichzeitig berücksichtigt werden?", "Ja. Dafür kannst du den höheren Satz, beide Sätze oder einen eigenen kombinierten Satz wählen.")],
        "related": [("Nachtzuschlag berechnen", "/nachtzuschlag-rechner.html"), ("Schichtzulagen berechnen", "/schichtzulagen-rechner.html")],
    },
    "ueberstunden-rechner.html": {
        "what": "Der Rechner vergleicht den Bruttowert deiner Überstunden mit dem möglichen Freizeitausgleich und berücksichtigt einen frei wählbaren Überstundenzuschlag.",
        "example": "20 Überstunden bei 20 € Stundenlohn und 25 % Zuschlag entsprechen 400 € Grundwert plus 100 € Zuschlag, also 500 € brutto.",
        "formula": "Überstunden × Stundenlohn = Grundwert. Grundwert × Zuschlagssatz = Zuschlag. Für Freizeit gilt: Überstunden × Freizeitfaktor.",
        "limits": "Steuern, Sozialabgaben, tarifliche Auszahlungsregeln, Fristen und persönliche Arbeitszeitkonten werden nicht automatisch berücksichtigt.",
        "faqs": [("Was bedeutet der Freizeitfaktor?", "Ein Faktor von 1 entspricht einer freien Stunde je Überstunde; 1,25 macht daraus 1 Stunde und 15 Minuten."), ("Ist die Auszahlung netto oder brutto?", "Der Rechner zeigt einen Bruttowert vor Steuern und Abgaben."), ("Kann ich auch Überstunden ohne Zuschlag berechnen?", "Ja. Setze den Zuschlagssatz einfach auf 0 Prozent.")],
        "related": [("Stundenlohn berechnen", "/stundenlohn-rechner.html"), ("Arbeitszeit berechnen", "/arbeitszeitrechner.html")],
    },
    "stundenlohn-rechner.html": {
        "what": "Der Rechner wandelt Monats- oder Jahresgehalt anhand deiner Wochenarbeitszeit in einen vergleichbaren Brutto-Stundenlohn um.",
        "example": "Bei 3.200 € Monatsgehalt und 40 Wochenstunden rechnet das Tool mit der durchschnittlichen Monatsarbeitszeit und ermittelt daraus den Stundenlohn.",
        "formula": "Wochenstunden × 52 ÷ 12 = durchschnittliche Monatsstunden. Monatsgehalt ÷ Monatsstunden = Brutto-Stundenlohn.",
        "limits": "Sonderzahlungen, unbezahlte Fehlzeiten, Zuschläge, Überstunden, Steuern und Sozialabgaben sind nur enthalten, wenn sie bereits im eingegebenen Bruttogehalt stecken.",
        "faqs": [("Warum wird mit 52 Wochen gerechnet?", "So wird die durchschnittliche Arbeitszeit eines Jahres gleichmäßig auf zwölf Monate verteilt."), ("Kann ich ein Jahresgehalt eingeben?", "Ja. Wähle Jahresgehalt; der Rechner rechnet es für den Vergleich auf einen Monatswert um."), ("Ist das mein Netto-Stundenlohn?", "Nein. Das Ergebnis ist ein rechnerischer Brutto-Stundenlohn.")],
        "related": [("Überstunden vergleichen", "/ueberstunden-rechner.html"), ("Schichtzulagen berechnen", "/schichtzulagen-rechner.html")],
    },
    "arbeitstage-rechner.html": {
        "what": "Der Rechner zählt geplante und effektive Arbeitstage für eine feste Woche oder einen wiederkehrenden Schichtrhythmus. Optional bezieht er Urlaub und gesetzliche Feiertage ein.",
        "example": "Bei einer klassischen 5-Tage-Woche werden Montag bis Freitag gezählt. Aktivierte arbeitsfreie Feiertage und Urlaubstage reduzieren anschließend die effektiven Arbeitstage.",
        "formula": "Geplante Arbeitstage − arbeitsfreie Feiertage − Urlaubstage = effektive Arbeitstage. Überschneidungen werden nicht doppelt abgezogen.",
        "limits": "Kommunale Feiertage, individuelle Dienstplanänderungen, Krankheit und betriebliche Sonderregelungen können von der Berechnung abweichen.",
        "faqs": [("Kann ich einen eigenen Schichtrhythmus eingeben?", "Ja. Du kannst eine beliebige Folge aus Früh-, Spät-, Nacht- und freien Tagen anlegen."), ("Werden Feiertage immer abgezogen?", "Nein. Nur wenn du Feiertage aktivierst und sie in deinem Modell als arbeitsfrei auswählst."), ("Wie wird Urlaub gezählt?", "Urlaub reduziert nur Tage, die laut gewähltem Modell geplante Arbeitstage sind.")],
        "related": [("Schichtplan online erstellen", "/schichtplaner-online.html"), ("Gemeinsame freie Tage finden", "/schichten-vergleichen.html")],
    },
    "schichten-vergleichen.html": {
        "what": "Das Tool legt zwei wiederkehrende Schichtrhythmen über denselben Kalender und zeigt die Tage, an denen beide Personen gleichzeitig frei haben.",
        "example": "Beginnen zwei Acht-Tage-Rhythmen an unterschiedlichen Daten, verschiebt das Tool beide Folgen korrekt und markiert nur echte gemeinsame freie Tage.",
        "formula": "Für jeden Kalendertag wird die Position im jeweiligen Rhythmus berechnet. Ein Treffer entsteht nur, wenn bei beiden Personen an diesem Tag „Frei“ hinterlegt ist.",
        "limits": "Spontane Dienstplanänderungen, Urlaub, Krankheit und Termine werden im Web-Vergleich nicht automatisch berücksichtigt.",
        "faqs": [("Müssen beide Rhythmen gleich lang sein?", "Nein. Beide Personen können unterschiedlich lange Schichtfolgen verwenden."), ("Warum ist das Startdatum wichtig?", "Es legt fest, an welchem Kalendertag Tag 1 des jeweiligen Rhythmus beginnt."), ("Kann ich mehr als zwei Personen vergleichen?", "Der Web-Rechner vergleicht zwei Personen. Weitere Gruppen lassen sich in der Shift-Lion-App verwalten.")],
        "related": [("Arbeitstage berechnen", "/arbeitstage-rechner.html"), ("Schichtplan online erstellen", "/schichtplaner-online.html")],
    },
}

EN_TOOL_GUIDES = {
    "working-time-calculator.html": ("The calculator uses shift start, end and break times to show gross time, net working time and the difference from your target hours.", "A 06:00–14:00 shift is 8 hours gross. After a 30-minute unpaid break, 7 hours 30 minutes remain.", "Shift end − shift start − unpaid break = net working time. Net time − target time = overtime balance.", "It does not verify collective agreements, rounding rules, on-call time or every legal exception.", [("Does it support overnight shifts?", "Yes. An end time before the start is treated as the following day."), ("How are paid breaks handled?", "When paid breaks are enabled, the break remains part of net working time."), ("Is this an official time record?", "No. It is a personal calculation aid, not an employer time record.")], [("Calculate night allowance", "/en/night-allowance-calculator.html"), ("Compare overtime", "/en/overtime-calculator.html")]),
    "night-allowance-calculator.html": ("The calculator finds paid hours inside your chosen night period and estimates base pay and night allowance.", "For 22:00–06:00, a 30-minute unpaid break, €20 hourly pay and 25%, the result is 7:30 paid night hours, €150 base pay and €37.50 allowance.", "Paid night hours × hourly wage × allowance rate = night allowance. An unpaid break removes base pay and all allowances for that time.", "Contractual night periods, tax treatment and collective-agreement rules are not checked automatically.", [("Can I change the night period?", "Yes. The eligible start and end times are adjustable."), ("Does an unpaid break reduce night allowance?", "Yes. It reduces paid time and eligible night hours."), ("Can Sunday allowance be included?", "Yes. Enable Sunday work and enter your own percentage.")], [("Calculate holiday allowance", "/en/holiday-allowance-calculator.html"), ("Calculate working time", "/en/working-time-calculator.html")]),
    "holiday-allowance-calculator.html": ("The calculator separates regular, holiday and optional Sunday hours and estimates base pay, allowances and gross total.", "7:30 paid holiday hours at €20 and a 100% holiday rate produce €150 base pay plus €150 holiday allowance.", "Holiday hours × hourly wage × holiday rate = holiday allowance. For Sunday overlaps, your selected combination rule is used.", "The tool does not determine whether a date legally qualifies as a holiday or verify regional, contractual and tax rules.", [("How are overnight shifts divided?", "Choose whether the shift starts on, leads into or falls fully within the holiday."), ("What happens with an unpaid break?", "It is deducted from base pay and every enabled allowance."), ("Can Sunday and holiday overlap?", "Yes. Choose the higher rate, add both rates or use a custom combined rate.")], [("Calculate night allowance", "/en/night-allowance-calculator.html"), ("Calculate shift allowances", "/en/schichtzulagen-rechner.html")]),
    "overtime-calculator.html": ("The calculator compares the gross value of overtime with time off and includes an adjustable overtime premium.", "20 overtime hours at €20 and a 25% premium equal €400 base value plus €100 premium, or €500 gross.", "Overtime × hourly wage = base value. Base value × premium rate = premium. Time off = overtime × time-off factor.", "Taxes, social contributions, contractual deadlines and individual time-account rules are not included.", [("What is the time-off factor?", "A factor of 1 gives one free hour per overtime hour; 1.25 gives 1 hour 15 minutes."), ("Is the payout net or gross?", "The calculator shows a gross amount before deductions."), ("Can I calculate without a premium?", "Yes. Set the premium to 0%." )], [("Calculate hourly wage", "/en/hourly-wage-calculator.html"), ("Calculate working time", "/en/working-time-calculator.html")]),
    "hourly-wage-calculator.html": ("The calculator converts monthly or annual gross salary into a comparable hourly wage using weekly working hours.", "For a €3,200 monthly salary and 40 weekly hours, the tool first determines average monthly hours and then the hourly wage.", "Weekly hours × 52 ÷ 12 = average monthly hours. Monthly salary ÷ monthly hours = gross hourly wage.", "Bonuses, unpaid absences, allowances, overtime, taxes and contributions are not added separately.", [("Why use 52 weeks?", "It spreads the average annual working time evenly across twelve months."), ("Can I enter annual salary?", "Yes. The calculator converts it to a monthly comparison value."), ("Is this my net hourly wage?", "No. It is a calculated gross hourly wage.")], [("Compare overtime", "/en/overtime-calculator.html"), ("Calculate shift allowances", "/en/schichtzulagen-rechner.html")]),
    "workdays-calculator.html": ("The calculator counts planned and effective workdays for fixed weeks or repeating shift rotations, optionally including leave and public holidays.", "For a five-day week, Monday to Friday are counted first. Selected days off for holidays and leave then reduce effective workdays.", "Planned workdays − holidays off − leave days = effective workdays. Overlaps are not deducted twice.", "Local holidays, sickness, roster changes and company-specific rules may differ.", [("Can I enter my own rotation?", "Yes. Build any repeating sequence of early, late, night and off days."), ("Are holidays always deducted?", "No. Only when enabled and selected as days off."), ("How is leave counted?", "Leave reduces only days that were planned workdays in the selected model.")], [("Create an online shift plan", "/en/schichtplaner-online.html"), ("Find shared days off", "/en/compare-shifts.html")]),
    "compare-shifts.html": ("The tool overlays two repeating shift rotations and identifies dates when both people are off.", "Two eight-day rotations can begin on different dates; the tool aligns both sequences and marks only genuine shared days off.", "For each date, the tool calculates the position in each rotation. A match occurs only when both positions are set to “Off”.", "Last-minute roster changes, leave, sickness and appointments are not included automatically.", [("Must both rotations have the same length?", "No. Each person can use a different rotation length."), ("Why does the start date matter?", "It defines the calendar date on which day 1 of each rotation begins."), ("Can I compare more than two people?", "The web tool compares two people; the Shift Lion app supports additional groups.")], [("Calculate workdays", "/en/workdays-calculator.html"), ("Create an online shift plan", "/en/schichtplaner-online.html")]),
}

for english_name, values in EN_TOOL_GUIDES.items():
    TOOL_GUIDES[f"en/{english_name}"] = dict(zip(("what", "example", "formula", "limits", "faqs", "related"), values))

TOOL_GUIDES.update({
    "schichtplaner-online.html": {
        "what": "Der Online-Schichtplaner überträgt einen wiederkehrenden Rhythmus ab deinem Startdatum in einen Monats- oder Jahreskalender.",
        "example": "Ein Rhythmus aus zwei Früh-, zwei Spät-, zwei Nacht- und zwei freien Tagen wird fortlaufend wiederholt und für jeden Kalendertag eingezeichnet.",
        "formula": "Kalendertage seit dem Startdatum modulo Rhythmuslänge bestimmen, welcher Rhythmustag an einem Datum gilt.",
        "limits": "Kurzfristige Dienständerungen, Urlaub, Krankheit und betriebliche Besonderheiten müssen außerhalb des automatisch wiederholten Grundrhythmus berücksichtigt werden.",
        "faqs": [("Bleiben meine Eingaben gespeichert?", "Der Web-Planer arbeitet direkt im Browser. Für eine dauerhafte persönliche Planung ist die Shift-Lion-App vorgesehen."), ("Kann ich den Jahresplan drucken?", "Ja. Der erzeugte Jahresplan kann gedruckt oder als PDF gespeichert werden."), ("Kann der Plan über Mitternacht reichende Schichten darstellen?", "Der Kalender markiert den jeweiligen Schichttag. Konkrete Beginn- und Endzeiten werden in diesem Rhythmusplaner nicht berechnet.")],
        "related": [("Arbeitstage berechnen", "/arbeitstage-rechner.html"), ("Schichten vergleichen", "/schichten-vergleichen.html")],
    },
    "schichtzulagen-rechner.html": {
        "what": "Der Rechner kombiniert Grundlohn mit frei eingegebenen Nacht-, Spät-, Sonn-, Feiertags- und weiteren Zulagen.",
        "example": "40 Nachtstunden bei 20 € Stundenlohn und 25 % Nachtzuschlag ergeben zusätzlich zum Grundlohn einen Nachtzuschlag von 200 €.",
        "formula": "Gesamtstunden × Stundenlohn = Grundlohn. Je Zuschlagsart gilt: Zuschlagsstunden × Stundenlohn × Prozentsatz.",
        "limits": "Der Rechner liefert eine Brutto-Schätzung. Steuerfreiheit, Sozialabgaben, Tarifvorrang und Regeln für sich überschneidende Zuschläge werden nicht rechtlich bewertet.",
        "faqs": [("Kann ich eigene Zuschlagssätze verwenden?", "Ja. Alle Prozentsätze und eine zusätzliche Pauschale können individuell angepasst werden."), ("Werden Zuschläge automatisch steuerfrei behandelt?", "Nein. Der Rechner zeigt Bruttowerte und trifft keine steuerliche Einordnung."), ("Dürfen Zuschlagsstunden mehrfach eingetragen werden?", "Mathematisch ja. Ob Zuschläge kombiniert werden dürfen, richtet sich nach deinen geltenden Regelungen.")],
        "related": [("Nachtzuschlag berechnen", "/nachtzuschlag-rechner.html"), ("Feiertagszuschlag berechnen", "/feiertagszuschlag-rechner.html")],
    },
    "en/schichtplaner-online.html": {
        "what": "The online shift planner places a repeating rotation into a monthly or yearly calendar from your selected start date.",
        "example": "A rotation of two early, two late, two night and two off days repeats continuously across the calendar.",
        "formula": "Calendar days since the start date modulo rotation length determine which rotation day applies to each date.",
        "limits": "Short-notice roster changes, leave, sickness and company-specific exceptions are outside the automatically repeated base rotation.",
        "faqs": [("Are my entries stored permanently?", "The web planner works in your browser. The Shift Lion app is intended for ongoing personal planning."), ("Can I print the yearly plan?", "Yes. The generated plan can be printed or saved as a PDF."), ("Does it calculate exact overnight hours?", "It marks the shift assigned to each date; exact start and end times are not calculated here.")],
        "related": [("Calculate workdays", "/en/workdays-calculator.html"), ("Compare rotations", "/en/compare-shifts.html")],
    },
    "en/schichtzulagen-rechner.html": {
        "what": "The calculator combines base pay with editable night, late, Sunday, holiday and additional allowances.",
        "example": "40 night hours at €20 and a 25% night rate add a €200 night allowance to base pay.",
        "formula": "Total hours × hourly wage = base pay. For each allowance: eligible hours × hourly wage × percentage.",
        "limits": "This is a gross estimate. Tax exemptions, social contributions, collective agreements and overlap rules are not assessed legally.",
        "faqs": [("Can I use my own allowance rates?", "Yes. Every percentage and the optional fixed allowance can be adjusted."), ("Are allowances treated as tax-free?", "No. The calculator shows gross values and does not make a tax classification."), ("Can allowance hours overlap?", "The calculation permits it, but whether rates may be combined depends on your applicable rules.")],
        "related": [("Calculate night allowance", "/en/night-allowance-calculator.html"), ("Calculate holiday allowance", "/en/holiday-allowance-calculator.html")],
    },
})

TOOL_ARTICLE_LINKS = {
    "arbeitszeitrechner.html": ("Arbeitszeit mit Pause erklärt", "/arbeitszeit-mit-pause-berechnen.html"),
    "nachtzuschlag-rechner.html": ("Ratgeber zum Nachtzuschlag", "/nachtzuschlag-berechnen.html"),
    "feiertagszuschlag-rechner.html": ("Feiertagszuschlag bei Nachtschicht", "/feiertagszuschlag-nachtschicht.html"),
    "ueberstunden-rechner.html": ("Auszahlung oder Freizeitausgleich?", "/ueberstunden-auszahlen-oder-freizeit.html"),
    "stundenlohn-rechner.html": ("Stundenlohn aus Gehalt erklärt", "/stundenlohn-aus-gehalt-berechnen.html"),
    "arbeitstage-rechner.html": ("Arbeitstage und Schichtrhythmus", "/arbeitstage-schichtrhythmus-berechnen.html"),
    "schichten-vergleichen.html": ("Gemeinsame freie Tage planen", "/gemeinsame-freie-tage-schichtplan.html"),
    "schichtplaner-online.html": ("Online-Schichtplan richtig erstellen", "/schichtplan-online-erstellen.html"),
    "schichtzulagen-rechner.html": ("Schichtzulagen verständlich erklärt", "/schichtzulagen-berechnen.html"),
    "en/working-time-calculator.html": ("Guide to working time and breaks", "/en/calculate-working-time-with-break.html"),
    "en/night-allowance-calculator.html": ("Night allowance guide", "/en/calculate-night-shift-allowance.html"),
    "en/holiday-allowance-calculator.html": ("Holiday allowance on night shifts", "/en/holiday-allowance-night-shift.html"),
    "en/overtime-calculator.html": ("Overtime pay or time off?", "/en/overtime-pay-or-time-off.html"),
    "en/hourly-wage-calculator.html": ("Hourly wage from salary guide", "/en/calculate-hourly-wage-from-salary.html"),
    "en/workdays-calculator.html": ("Workdays and shift rotations", "/en/calculate-workdays-shift-rotation.html"),
    "en/compare-shifts.html": ("Plan shared days off", "/en/find-shared-days-off-shift-plan.html"),
    "en/schichtplaner-online.html": ("Create an online shift plan", "/en/create-shift-plan-online.html"),
    "en/schichtzulagen-rechner.html": ("Shift allowances explained", "/en/calculate-shift-allowances.html"),
}

TOOL_APP_BENEFITS = {
    "arbeitszeitrechner.html": "Arbeitszeiten, Pausen und Überstunden dauerhaft im Schichtkalender behalten",
    "nachtzuschlag-rechner.html": "Nachtschichten und die anschließende Erholungszeit gemeinsam planen",
    "feiertagszuschlag-rechner.html": "Feiertagsschichten direkt im persönlichen Kalender erkennen",
    "ueberstunden-rechner.html": "Überstunden und freie Tage im gesamten Schichtrhythmus einordnen",
    "stundenlohn-rechner.html": "Schichten und deine voraussichtliche Vergütung zusammen überblicken",
    "arbeitstage-rechner.html": "Arbeitstage, Urlaub und freie Tage langfristig planen",
    "schichten-vergleichen.html": "Mehrere Schichtgruppen vergleichen und gemeinsame freie Tage finden",
    "schichtplaner-online.html": "Deinen Schichtplan unterwegs pflegen und private Termine ergänzen",
    "schichtzulagen-rechner.html": "Schichtplan und voraussichtliche Zuschläge zusammen verfolgen",
    "en/working-time-calculator.html": "Keep working hours, breaks and overtime together in your shift calendar",
    "en/night-allowance-calculator.html": "Plan night shifts and the recovery time that follows them",
    "en/holiday-allowance-calculator.html": "See holiday shifts directly in your personal calendar",
    "en/overtime-calculator.html": "Put overtime and days off into the context of your full rotation",
    "en/hourly-wage-calculator.html": "Track shifts and expected pay in one place",
    "en/workdays-calculator.html": "Plan workdays, leave and days off well ahead",
    "en/compare-shifts.html": "Compare several shift groups and find shared days off",
    "en/schichtplaner-online.html": "Maintain your shift plan on the go and add personal appointments",
    "en/schichtzulagen-rechner.html": "Track your shift plan and expected allowances together",
}


def public_path(rel):
    path = rel.as_posix()
    if path == "index.html":
        return "/"
    if path == "en/index.html":
        return "/en/"
    if path == "tools/index.html":
        return "/tools/"
    if path == "en/tools/index.html":
        return "/en/tools/"
    return "/" + path


def add_seo_metadata(text, rel):
    key = rel.as_posix()
    url = CONFIG["site_url"].rstrip("/") + public_path(rel)
    title = SEO_TITLES.get(key)
    if title:
        text = re.sub(r"<title>.*?</title>", f"<title>{html.escape(title)}</title>", text, count=1, flags=re.I | re.S)
    tags = []
    description = SEO_DESCRIPTIONS.get(key)
    if description:
        text = re.sub(r'<meta\s+name=["\']description["\'][^>]*>', '', text, flags=re.I)
        tags.append(f'<meta name="description" content="{html.escape(description, quote=True)}">')
    text = re.sub(r'<link\s+rel=["\']canonical["\'][^>]*>', '', text, flags=re.I)
    tags.append(f'<link rel="canonical" href="{html.escape(url, quote=True)}">')
    pair = LANGUAGE_PAIRS.get(key)
    if not pair:
        pair = next((de for de, en in LANGUAGE_PAIRS.items() if en == key), None)
    if not pair:
        candidate = key[3:] if key.startswith("en/") else "en/" + key
        if (SRC / candidate).exists():
            pair = candidate
    if pair:
        text = re.sub(r'<link\s+rel=["\']alternate["\'][^>]*hreflang=[^>]*>', '', text, flags=re.I)
        language = "en" if key.startswith("en/") else "de"
        other_language = "de" if language == "en" else "en"
        other_url = CONFIG["site_url"].rstrip("/") + "/" + pair
        tags.append(f'<link rel="alternate" hreflang="{language}" href="{html.escape(url, quote=True)}">')
        tags.append(f'<link rel="alternate" hreflang="{other_language}" href="{html.escape(other_url, quote=True)}">')
    if tags:
        text = re.sub(r"</head>", "".join(tags) + "</head>", text, count=1, flags=re.I)
    return text


def add_social_metadata(text, rel):
    """Keep Open Graph and Twitter previews aligned with page SEO metadata."""
    if re.search(r'<meta\s+name=["\']robots["\'][^>]*noindex', text, re.I):
        return text
    head = text.split("</head>", 1)[0]
    title_match = re.search(r"<title\b[^>]*>(.*?)</title>", head, re.I | re.S)
    description_match = re.search(
        r'<meta\s+name=["\']description["\'][^>]*content=["\']([^"\']*)',
        head,
        re.I,
    )
    canonical_match = re.search(
        r'<link\s+rel=["\']canonical["\'][^>]*href=["\']([^"\']+)',
        head,
        re.I,
    )
    if not (title_match and description_match and canonical_match):
        return text

    title = plain_text(title_match.group(1))
    description = html.unescape(description_match.group(1)).strip()
    url = html.unescape(canonical_match.group(1)).strip()
    english = rel.as_posix().startswith("en/")
    image_path = "/tools-bild-englisch.png" if english else "/tools-bild-deutsch.png"
    image_url = CONFIG["site_url"].rstrip("/") + image_path
    locale = "en_US" if english else "de_DE"

    social_names = (
        "og:title", "og:description", "og:url", "og:image", "og:type", "og:site_name", "og:locale",
        "twitter:card", "twitter:title", "twitter:description", "twitter:image",
    )
    for name in social_names:
        text = re.sub(
            rf'<meta\s+(?:property|name)=["\']{re.escape(name)}["\'][^>]*>',
            "",
            text,
            flags=re.I,
        )
    text = re.sub(r"^[ \t]+$", "", text, flags=re.M)
    tags = (
        f'<meta property="og:type" content="website">'
        f'<meta property="og:site_name" content="Shift Lion">'
        f'<meta property="og:locale" content="{locale}">'
        f'<meta property="og:title" content="{html.escape(title, quote=True)}">'
        f'<meta property="og:description" content="{html.escape(description, quote=True)}">'
        f'<meta property="og:url" content="{html.escape(url, quote=True)}">'
        f'<meta property="og:image" content="{html.escape(image_url, quote=True)}">'
        f'<meta name="twitter:card" content="summary_large_image">'
        f'<meta name="twitter:title" content="{html.escape(title, quote=True)}">'
        f'<meta name="twitter:description" content="{html.escape(description, quote=True)}">'
        f'<meta name="twitter:image" content="{html.escape(image_url, quote=True)}">'
    )
    return re.sub(r"</head>", tags + "</head>", text, count=1, flags=re.I)


def integrate_contact_page(text, rel):
    """Route footer contact links through the central contact page."""
    if rel.as_posix() == "kontakt.html":
        return text
    english = rel.as_posix().startswith("en/")
    label = "Contact" if english else "Kontakt"

    def update_footer(match):
        footer = match.group(0)
        footer = re.sub(
            r'<a\b([^>]*?)href=["\']mailto:[^"\']+["\']([^>]*)>.*?</a>',
            rf'<a\1href="/kontakt.html"\2>{label}</a>',
            footer,
            flags=re.I | re.S,
        )
        if re.search(r'href=["\']/kontakt\.html["\']', footer, re.I):
            return footer
        link = f'<a href="/kontakt.html">{label}</a>'
        if re.search(r"<small\b", footer, re.I):
            return re.sub(r"<small\b", link + "<small", footer, count=1, flags=re.I)
        return re.sub(r"</footer>", link + "</footer>", footer, count=1, flags=re.I)

    return re.sub(r"<footer\b.*?</footer>", update_footer, text, flags=re.I | re.S)


def plain_text(value):
    value = re.sub(r"<[^>]+>", " ", value)
    return html.unescape(re.sub(r"\s+", " ", value)).strip()


def optimize_content_images(text):
    def optimize(match):
        tag = match.group(0)
        def add_attributes(value, attributes):
            return re.sub(r'\s*/?>$', f' {attributes}>', value)
        source = re.search(r'src=["\']([^"\']+)["\']', tag, re.I)
        if not source:
            return tag
        filename = source.group(1).rsplit("/", 1)[-1]
        image = CONTENT_IMAGES.get(filename)
        if not image:
            return tag
        replacement, width, height = image
        new_source = source.group(1)[:-len(filename)] + replacement
        tag = tag[:source.start(1)] + new_source + tag[source.end(1):]
        if not re.search(r'\swidth=["\']', tag, re.I):
            tag = add_attributes(tag, f'width="{width}" height="{height}"')
        if not re.search(r'\sdecoding=["\']', tag, re.I):
            tag = add_attributes(tag, 'decoding="async"')
        if not re.search(r'\sloading=["\']', tag, re.I):
            if filename.startswith("tools-bild-") or filename == "Shift-Lion-Logo-groß.png":
                tag = add_attributes(tag, 'loading="eager" fetchpriority="high"')
            else:
                tag = add_attributes(tag, 'loading="lazy"')
        return tag
    return re.sub(r'<img\b[^>]*>', optimize, text, flags=re.I)


def remove_unpublished_legal_links(text):
    """Do not expose links to the intentionally unpublished legal-notice drafts."""
    return re.sub(
        r'<a\s+[^>]*href=["\'](?:/impressum\.html|/en/legal-notice\.html)["\'][^>]*>.*?</a>',
        '',
        text,
        flags=re.I | re.S,
    )


def add_accessibility_foundation(text):
    """Add a consistent keyboard entry point without changing page layouts."""
    if '<link rel="stylesheet" href="/accessibility.css?v=1">' not in text:
        text = re.sub(
            r"</head>",
            '<link rel="stylesheet" href="/accessibility.css?v=1"></head>',
            text,
            count=1,
            flags=re.I,
        )
    main_match = re.search(r"<main\b[^>]*>", text, re.I)
    if not main_match:
        return text
    main_tag = main_match.group(0)
    if re.search(r"\sid=[\"']", main_tag, re.I):
        main_id = re.search(r"\sid=[\"']([^\"']+)", main_tag, re.I).group(1)
    else:
        main_id = "main-content"
        updated_main = re.sub(r">$", ' id="main-content">', main_tag)
        text = text[:main_match.start()] + updated_main + text[main_match.end():]
    if "class=\"skip-link\"" not in text:
        language_match = re.search(r"<html[^>]+lang=[\"']([^\"']+)", text, re.I)
        english = bool(language_match and language_match.group(1).lower().startswith("en"))
        label = "Skip to main content" if english else "Zum Hauptinhalt springen"
        text = re.sub(
            r"(<body\b[^>]*>)",
            rf'\1<a class="skip-link" href="#{html.escape(main_id, quote=True)}">{label}</a>',
            text,
            count=1,
            flags=re.I,
        )
    return text


def validate_internal_links():
    """Stop the build when a visible internal page link has no target."""
    broken = []
    anchor_pattern = re.compile(r'<a\b[^>]*\shref=["\']([^"\']+)["\']', re.I)
    for source in OUT.rglob("*.html"):
        page = source.read_text(encoding="utf-8")
        for href in anchor_pattern.findall(page):
            if not href.startswith("/") or href.startswith("//"):
                continue
            path = href.split("#", 1)[0].split("?", 1)[0]
            if not path:
                continue
            relative = path.lstrip("/")
            target = OUT / relative
            if path.endswith("/") or not Path(relative).suffix:
                target = target / "index.html"
            if not target.exists():
                broken.append(f"{source.relative_to(OUT)} -> {href}")
    if broken:
        preview = "\n".join(sorted(set(broken))[:25])
        raise RuntimeError(f"Fehlende interne Linkziele:\n{preview}")


def validate_seo_foundation():
    """Verify indexable pages have one clear search result and one main heading."""
    errors = []
    canonical_pages = {}
    sitemap = (OUT / "sitemap.xml").read_text(encoding="utf-8")
    sitemap_urls = set(re.findall(r"<loc>(.*?)</loc>", sitemap, re.I))
    for source in OUT.rglob("*.html"):
        relative = source.relative_to(OUT).as_posix()
        if relative.startswith("google"):
            continue
        page = source.read_text(encoding="utf-8")
        if re.search(r'<meta\s+name=["\']robots["\'][^>]*noindex', page, re.I):
            continue
        head = page.split("</head>", 1)[0]
        titles = re.findall(r"<title\b[^>]*>(.*?)</title>", head, re.I | re.S)
        descriptions = re.findall(r'<meta\s+name=["\']description["\'][^>]*>', head, re.I)
        canonicals = re.findall(r'<link\s+rel=["\']canonical["\'][^>]*href=["\']([^"\']+)', head, re.I)
        social_fields = (
            "og:title", "og:description", "og:url", "og:image",
            "twitter:card", "twitter:title", "twitter:description", "twitter:image",
        )
        visible = re.sub(r"<(script|style)\b.*?</\1>", "", page, flags=re.I | re.S)
        headings = re.findall(r"<h1\b", visible, re.I)
        if len(titles) != 1:
            errors.append(f"{relative}: {len(titles)} Title")
        if len(descriptions) != 1:
            errors.append(f"{relative}: {len(descriptions)} Meta-Descriptions")
        if len(canonicals) != 1:
            errors.append(f"{relative}: {len(canonicals)} Canonicals")
        for field in social_fields:
            count = len(re.findall(
                rf'<meta\s+(?:property|name)=["\']{re.escape(field)}["\'][^>]*>',
                head,
                re.I,
            ))
            if count != 1:
                errors.append(f"{relative}: {count} {field}")
        social_images = re.findall(
            r'<meta\s+(?:property|name)=["\'](?:og:image|twitter:image)["\'][^>]*content=["\']([^"\']+)',
            head,
            re.I,
        )
        if any(not image.startswith("https://shiftlion.app/") for image in social_images):
            errors.append(f"{relative}: Social-Bild ist nicht absolut")
        if len(headings) != 1:
            errors.append(f"{relative}: {len(headings)} sichtbare H1")
        if len(canonicals) == 1:
            canonical = canonicals[0]
            if canonical in canonical_pages:
                errors.append(f"{relative}: Canonical doppelt mit {canonical_pages[canonical]}")
            canonical_pages[canonical] = relative
            if canonical not in sitemap_urls:
                errors.append(f"{relative}: Canonical fehlt in Sitemap ({canonical})")
    if errors:
        raise RuntimeError("SEO-Grundprüfung fehlgeschlagen:\n" + "\n".join(errors[:30]))


def page_label(text, rel):
    heading = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.I | re.S)
    if heading:
        return plain_text(heading.group(1))
    title = re.search(r"<title>(.*?)</title>", text, re.I | re.S)
    if title:
        return re.split(r"\s+[|–-]\s+Shift Lion", plain_text(title.group(1)), maxsplit=1)[0]
    return rel.stem.replace("-", " ").title()


def add_tool_guide(text, rel):
    key = rel.as_posix()
    guide = TOOL_GUIDES.get(key)
    if not guide or 'class="tool-guide"' in text:
        return text
    is_english = key.startswith("en/")
    labels = ({
        "title": "Understand the result",
        "what": "What does this tool calculate?",
        "example": "Example",
        "formula": "How it is calculated",
        "limits": "What is not included?",
        "faq": "Frequently asked questions",
        "related": "Useful next steps",
        "app": "Plan your complete rotation in the Shift Lion app",
    } if is_english else {
        "title": "Ergebnis richtig verstehen",
        "what": "Was berechnet dieses Tool?",
        "example": "Kurzes Beispiel",
        "formula": "So wird gerechnet",
        "limits": "Was berücksichtigt der Rechner nicht?",
        "faq": "Häufige Fragen",
        "related": "Passende nächste Schritte",
        "app": "Kompletten Schichtrhythmus in der Shift-Lion-App planen",
    })
    faq = "".join(
        f"<details><summary>{html.escape(question)}</summary><p>{html.escape(answer)}</p></details>"
        for question, answer in guide["faqs"]
    )
    related_pairs = list(guide["related"])
    article_link = TOOL_ARTICLE_LINKS.get(key)
    if article_link:
        related_pairs.insert(0, article_link)
    related = "".join(
        f'<a href="{html.escape(href, quote=True)}">{html.escape(label)} →</a>'
        for label, href in related_pairs
    )
    section = (
        '<section class="tool-guide" aria-labelledby="toolGuideTitle">'
        f'<div class="tool-guide-head"><span>{"RECHENHILFE" if not is_english else "CALCULATION GUIDE"}</span>'
        f'<h2 id="toolGuideTitle">{labels["title"]}</h2></div>'
        '<div class="tool-guide-grid">'
        f'<article><h3>{labels["what"]}</h3><p>{html.escape(guide["what"])}</p></article>'
        f'<article class="tool-example"><h3>{labels["example"]}</h3><p>{html.escape(guide["example"])}</p></article>'
        f'<article><h3>{labels["formula"]}</h3><p>{html.escape(guide["formula"])}</p></article>'
        f'<article><h3>{labels["limits"]}</h3><p>{html.escape(guide["limits"])}</p></article>'
        '</div>'
        f'<div class="tool-guide-faq"><h3>{labels["faq"]}</h3>{faq}</div>'
        f'<div class="tool-guide-links"><div><strong>{labels["related"]}</strong>{related}</div>'
        f'<a class="tool-guide-app" href="/download/android/">{html.escape(TOOL_APP_BENEFITS.get(key, labels["app"]))} →</a></div>'
        '</section>'
    )
    app_cta = re.search(r'<section class="app-cta"', text, re.I)
    if app_cta:
        return text[:app_cta.start()] + section + text[app_cta.start():]
    page_cta = re.search(r'<section class="cta"', text, re.I)
    if page_cta:
        return text[:page_cta.start()] + section + text[page_cta.start():]
    main_end = text.lower().rfind("</main>")
    return text[:main_end] + section + text[main_end:] if main_end != -1 else text


def add_tool_article_link(text, rel):
    key = rel.as_posix()
    article = TOOL_ARTICLE_LINKS.get(key)
    if not article or 'class="tool-article-link"' in text:
        return text
    label, href = article
    english = key.startswith("en/")
    section = (
        '<section class="tool-article-link" aria-label="'
        + ("Detailed calculation guide" if english else "Ausführlicher Rechenratgeber")
        + '"><div><strong>'
        + ("Want the full calculation explained?" if english else "Du möchtest die Berechnung genau verstehen?")
        + '</strong><span>'
        + ("The guide explains the formula, an example and important limitations." if english else "Im Ratgeber findest du Formel, Beispiel und wichtige Einschränkungen.")
        + '</span></div><a href="'
        + html.escape(href, quote=True) + '">' + html.escape(label) + ' →</a></section>'
    )
    text = re.sub(r"</head>", '<link rel="stylesheet" href="/tool-article-link.css?v=1"></head>', text, count=1, flags=re.I)
    app_cta = re.search(r'<section class="app-cta"', text, re.I)
    if app_cta:
        return text[:app_cta.start()] + section + text[app_cta.start():]
    page_cta = re.search(r'<section class="cta"', text, re.I)
    if page_cta:
        return text[:page_cta.start()] + section + text[page_cta.start():]
    main_end = text.lower().rfind("</main>")
    return text[:main_end] + section + text[main_end:] if main_end != -1 else text


def add_guide_navigation(text, rel):
    if rel.as_posix().startswith("en/"):
        addition = '<a href="/en/guides/">Guides</a>'
        anchors = ('<a href="/en/tools/">All Tools</a>', '<a href="/en/tools/">Tools</a>')
    else:
        addition = '<a href="/ratgeber/">Ratgeber</a>'
        anchors = ('<a href="/tools/">Alle Tools</a>', '<a href="/tools/">Tools</a>')
    for anchor in anchors:
        text = re.sub(re.escape(anchor) + rf'(?!\s*{re.escape(addition)})', anchor + addition, text)
    return text


PLANNER_POSITIONING = {
    "schichtplaner.html": (
        "Persönlicher Schichtkalender in der App",
        "Hier planst du deinen eigenen Schichtrhythmus, private Termine, Urlaub und gemeinsame freie Zeit dauerhaft auf dem Smartphone.",
        (("Arbeitgeber-Dienstplan persönlich übertragen", "/dienstplan-app.html", "Wenn dein Betrieb den Plan vorgibt und du ihn in deinen Alltag übernehmen möchtest."), ("Kostenlosen Grundrhythmus im Browser erstellen", "/schichtplaner-online.html", "Wenn du ohne Installation schnell einen Monats- oder Jahresplan brauchst.")),
    ),
    "dienstplan-app.html": (
        "Den fertigen Arbeitgeberplan persönlich übernehmen",
        "Diese Seite zeigt, wie du einen bereits erstellten betrieblichen Dienstplan in deinen persönlichen Kalender überträgst und um Urlaub oder Termine ergänzt.",
        (("Eigenen Schichtrhythmus in der App planen", "/schichtplaner.html", "Wenn du deinen persönlichen Rhythmus und gemeinsame freie Tage langfristig organisieren möchtest."), ("Grundplan kostenlos im Browser erzeugen", "/schichtplaner-online.html", "Wenn du zunächst nur eine wiederkehrende Folge als Monats- oder Jahresplan ausgeben willst.")),
    ),
    "schichtplaner-online.html": (
        "Kostenloser Grundplan direkt im Browser",
        "Der Online-Planer wiederholt deinen festen Schichtrhythmus und erzeugt ohne Konto einen Monats- oder Jahresplan zum Drucken. Einzelne Termine werden hier bewusst nicht verwaltet.",
        (("Persönlichen Schichtkalender dauerhaft nutzen", "/schichtplaner.html", "Für einzelne Änderungen, Urlaub, Termine und die mobile Nutzung."), ("Arbeitgeber-Dienstplan in den Alltag übertragen", "/dienstplan-app.html", "Für einen bereits vorgegebenen betrieblichen Plan.")),
    ),
    "en/schichtplaner.html": (
        "Your personal shift calendar in the app",
        "Plan your own rotation, private appointments, leave and shared days off permanently on your phone.",
        (("Transfer an employer duty roster", "/en/dienstplan-app.html", "For a schedule that has already been created by your workplace."), ("Create a free base rotation in your browser", "/en/schichtplaner-online.html", "For a quick monthly or yearly plan without installing the app.")),
    ),
    "en/dienstplan-app.html": (
        "Bring your employer roster into your personal calendar",
        "Transfer a duty roster that your workplace has already created, then add leave, appointments and personal plans.",
        (("Plan your own rotation in the app", "/en/schichtplaner.html", "For a long-term personal shift calendar and shared days off."), ("Generate a free base plan in your browser", "/en/schichtplaner-online.html", "For a repeating monthly or yearly schedule without an account.")),
    ),
    "en/schichtplaner-online.html": (
        "A free base schedule directly in your browser",
        "The online planner repeats a fixed rotation and creates a printable monthly or yearly plan without an account. It deliberately does not manage individual appointments.",
        (("Use a permanent personal shift calendar", "/en/schichtplaner.html", "For individual changes, leave, appointments and mobile planning."), ("Transfer an employer duty roster", "/en/dienstplan-app.html", "For a schedule that has already been set by your workplace.")),
    ),
}

PLANNER_CONTENT_REPLACEMENTS = {
    "en/dienstplan-app.html": (
        ("Manage early, late and night duties, vacation, appointments and days off on your phone.", "Transfer the duty roster created by your employer to your phone, then add leave, appointments and days off."),
        ("<h2>Why this matters</h2><p>Changing shifts affect sleep, energy, appointments and time with other people. A clear plan makes the next step easier to see.</p>", "<h2>From workplace roster to personal overview</h2><p>Your employer assigns the duties. Shift Lion gives you a private copy that is easier to combine with leave, appointments and everyday plans.</p>"),
        ("<h2>Practical tips</h2>", "<h2>Keep the assigned duties useful in everyday life</h2>"),
        ("<h3>Custom duties</h3><p>Create your own duty names, colors, working times and repeating sequences.</p>", "<h3>Copy assigned duties</h3><p>Transfer early, late, night and custom duties with their times and colours.</p>"),
        ("<h2>Plan around your real rotation</h2><p>Shift Lion helps you keep shifts, days off and appointments in one place and compare schedules with the people who matter.</p>", "<h2>Personal calendar, not staff scheduling software</h2><p>Shift Lion does not create a company-wide roster or assign employees. It helps one shift worker organise a roster that has already been set.</p>"),
        ("<h3>Do these tips work for rotating schedules?</h3><p>Yes. Adapt them to your shift sequence, personal health and recovery needs.</p>", "<h3>Does Shift Lion create the employer roster?</h3><p>No. Your workplace remains responsible for staff scheduling; the app is for your personal overview.</p>"),
    ),
}


def add_planner_positioning(text, rel):
    item = PLANNER_POSITIONING.get(rel.as_posix())
    if not item or 'class="planner-positioning"' in text:
        return text
    for old, new in PLANNER_CONTENT_REPLACEMENTS.get(rel.as_posix(), ()):
        text = text.replace(old, new)
    title, description, choices = item
    english = rel.as_posix().startswith("en/")
    cards = "".join(
        f'<a href="{html.escape(href, quote=True)}">{html.escape(label)} →<span>{html.escape(note)}</span></a>'
        for label, href, note in choices
    )
    section = (
        '<section class="planner-positioning" aria-labelledby="plannerChoiceTitle">'
        f'<span>{"Choose the right planner" if english else "Den passenden Planer wählen"}</span>'
        f'<h2 id="plannerChoiceTitle">{html.escape(title)}</h2><p>{html.escape(description)}</p>'
        f'<div class="planner-choice-grid">{cards}</div></section>'
    )
    text = re.sub(r"</head>", '<link rel="stylesheet" href="/planner-positioning.css?v=1"></head>', text, count=1, flags=re.I)
    cta = re.search(r'<section class="cta"', text, re.I)
    if cta:
        return text[:cta.start()] + section + text[cta.start():]
    main_end = text.lower().rfind("</main>")
    return text[:main_end] + section + text[main_end:] if main_end != -1 else text


def add_structured_data(text, rel):
    key = rel.as_posix()
    site_url = CONFIG["site_url"].rstrip("/")
    url = site_url + public_path(rel)
    is_english = key.startswith("en/")
    graph = []
    is_legacy_guide = rel.name in GUIDE_PAGE_NAMES

    if is_legacy_guide:
        headline_match = re.search(r"<h1\b[^>]*>(.*?)</h1>", text, re.I | re.S)
        description_match = re.search(
            r'<meta\s+name=["\']description["\'][^>]*content=["\']([^"\']+)',
            text,
            re.I,
        )
        headline = plain_text(headline_match.group(1)) if headline_match else page_label(text, rel)
        description = html.unescape(description_match.group(1)) if description_match else ""
        graph.append({
            "@type": "Article",
            "@id": f"{url}#article",
            "headline": headline,
            "description": description,
            "inLanguage": "en" if is_english else "de",
            "mainEntityOfPage": {"@type": "WebPage", "@id": url},
            "author": {"@type": "Organization", "name": "Shift Lion Redaktion"},
            "publisher": {"@type": "Organization", "name": "Shift Lion Redaktion", "url": f"{site_url}/"},
            "datePublished": GUIDE_PUBLISHED,
            "dateModified": GUIDE_REVIEWED,
        })

    if key in {"index.html", "en/index.html"}:
        graph.append({
            "@type": "Organization",
            "@id": f"{site_url}/#organization",
            "name": "Shift Lion",
            "url": f"{site_url}/",
            "logo": {
                "@type": "ImageObject",
                "url": f"{site_url}/Shift-Lion-Logo-gro%C3%9F.png",
            },
            "sameAs": [
                "https://play.google.com/store/apps/details?id=com.masterinpocket.shiftmaestro"
            ],
        })

    if key in APP_PAGE_NAMES:
        graph.append({
            "@type": "SoftwareApplication",
            "@id": f"{site_url}/#android-app",
            "name": "Shift Lion",
            "url": url,
            "description": (
                "Shift planner for rotating shifts, shared days off, appointments and working-time overview."
                if is_english else
                "Schichtplaner für Wechselschichten, gemeinsame freie Tage, Termine und Arbeitszeitübersicht."
            ),
            "applicationCategory": "ProductivityApplication",
            "operatingSystem": "Android",
            "downloadUrl": "https://play.google.com/store/apps/details?id=com.masterinpocket.shiftmaestro",
            "image": f"{site_url}/kalender.jpg",
            "publisher": {"@id": f"{site_url}/#organization"},
            "offers": {
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "EUR",
            },
        })

    if key not in {"index.html", "en/index.html"}:
        current_label = page_label(text, rel)
        items = [{
            "@type": "ListItem",
            "position": 1,
            "name": "Home" if is_english else "Startseite",
            "item": f"{site_url}/en/" if is_english else f"{site_url}/",
        }]
        is_tool = rel.name in TOOL_PAGES or rel.parent.name == "tools"
        if is_legacy_guide:
            items.append({
                "@type": "ListItem",
                "position": 2,
                "name": "Guides" if is_english else "Ratgeber",
                "item": f"{site_url}/en/guides/" if is_english else f"{site_url}/ratgeber/",
            })
        if is_tool:
            items.append({
                "@type": "ListItem",
                "position": 2,
                "name": "All Tools" if is_english else "Alle Tools",
                "item": f"{site_url}/en/tools/" if is_english else f"{site_url}/tools/",
            })
        items.append({
            "@type": "ListItem",
            "position": len(items) + 1,
            "name": current_label,
            "item": url,
        })
        graph.append({"@type": "BreadcrumbList", "itemListElement": items})

    questions = []
    faq_pattern = re.compile(
        r"<details[^>]*>\s*<summary[^>]*>(.*?)</summary>\s*<p[^>]*>(.*?)</p>\s*</details>",
        re.I | re.S,
    )
    for question, answer in faq_pattern.findall(text):
        question_text, answer_text = plain_text(question), plain_text(answer)
        if question_text and answer_text:
            questions.append({
                "@type": "Question",
                "name": question_text,
                "acceptedAnswer": {"@type": "Answer", "text": answer_text},
            })
    if questions and '"@type": "FAQPage"' not in text:
        graph.append({"@type": "FAQPage", "mainEntity": questions})

    if not graph:
        return text
    payload = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    payload = payload.replace("</", "<\\/")
    script = f'<script type="application/ld+json">{payload}</script>'
    return re.sub(r"</head>", script + "</head>", text, count=1, flags=re.I)


def render_nav(css_class="nav", tag="nav"):
    links = []
    for item in CONFIG["navigation_de"]:
        href = html.escape(item["href"], quote=True)
        label = html.escape(item["label"])
        links.append(f'  <a href="{href}">{label}</a>')
    return f'<{tag} class="{css_class}">\n' + "\n".join(links) + f'\n</{tag}>'


def render_guide(relative, guide):
    en = guide["lang"] == "en"
    site = CONFIG["site_url"].rstrip("/")
    url = site + "/" + relative
    pair_url = site + "/" + guide["pair"]
    sections = []
    for heading, points in guide["sections"]:
        items = "".join(f"<li>{html.escape(point)}</li>" for point in points)
        sections.append(f'<section class="guide-section"><h2>{html.escape(heading)}</h2><ul>{items}</ul></section>')
    faq_html = "".join(
        f"<details><summary>{html.escape(question)}</summary><p>{html.escape(answer)}</p></details>"
        for question, answer in guide["faqs"]
    )
    related_html = "".join(
        f'<a href="{html.escape(href, quote=True)}">{html.escape(label)} →</a>'
        for label, href in guide["related"]
    )
    faq_data = [{
        "@type": "Question", "name": question,
        "acceptedAnswer": {"@type": "Answer", "text": answer},
    } for question, answer in guide["faqs"]]
    data = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Article", "@id": f"{url}#article", "headline": guide["h1"], "description": guide["description"], "inLanguage": guide["lang"], "mainEntityOfPage": {"@type": "WebPage", "@id": url}, "author": {"@type": "Organization", "name": "Shift Lion Redaktion"}, "publisher": {"@type": "Organization", "name": "Shift Lion Redaktion", "url": f"{site}/"}, "datePublished": GUIDE_PUBLISHED, "dateModified": GUIDE_REVIEWED},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home" if en else "Startseite", "item": f"{site}/en/" if en else f"{site}/"},
                {"@type": "ListItem", "position": 2, "name": "Guides" if en else "Ratgeber", "item": f"{site}/en/guides/" if en else f"{site}/ratgeber/"},
                {"@type": "ListItem", "position": 3, "name": guide["h1"], "item": url},
            ]},
            {"@type": "FAQPage", "mainEntity": faq_data},
        ],
    }
    json_ld = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    nav = (
        '<a href="/en/">Home</a><a href="/en/tools/">Tools</a><a href="/en/guides/">Guides</a><a href="/' + guide["pair"] + '">DE</a>'
        if en else
        '<a href="/">Startseite</a><a href="/tools/">Tools</a><a href="/ratgeber/">Ratgeber</a><a href="/' + guide["pair"] + '">EN</a>'
    )
    tool_label, tool_href = guide["tool"]
    return f'''<!doctype html><html lang="{guide["lang"]}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(guide["title"])}</title><meta name="description" content="{html.escape(guide["description"], quote=True)}">
<link rel="canonical" href="{url}"><link rel="alternate" hreflang="{guide["lang"]}" href="{url}"><link rel="alternate" hreflang="{"de" if en else "en"}" href="{pair_url}"><link rel="icon" href="/favicon.png"><link rel="stylesheet" href="/guide.css?v=1"><link rel="stylesheet" href="/guide-trust.css?v=1">
<script type="application/ld+json">{json_ld}</script></head><body>
<header class="guide-hero"><nav><a class="guide-logo" href="/{'en/' if en else ''}"><img src="/Shift-Lion-Logo-groß.png" alt="Shift Lion"></a><div>{nav}<a class="nav-cta" href="/download/android/">{"Download app" if en else "App herunterladen"}</a></div></nav><div class="hero-copy"><span>{html.escape(guide["eyebrow"])}</span><h1>{html.escape(guide["h1"])}</h1><p>{html.escape(guide["intro"])}</p><a class="primary" href="{html.escape(tool_href, quote=True)}">{html.escape(tool_label)} →</a></div></header>
<main>{guide_trust_signals(en=en, calculation_guide=True)}<div class="article-grid"><article>{''.join(sections)}</article><aside><strong>{"Calculate it now" if en else "Direkt ausrechnen"}</strong><p>{"Use the free calculator with your own values." if en else "Nutze den kostenlosen Rechner mit deinen eigenen Werten."}</p><a href="{html.escape(tool_href, quote=True)}">{html.escape(tool_label)} →</a></aside></div>
<section class="guide-faq"><span>{"FAQ" if en else "HÄUFIGE FRAGEN"}</span><h2>{"Questions about this topic" if en else "Fragen zu diesem Thema"}</h2>{faq_html}</section>
<section class="guide-next"><div><h2>{"Continue with Shift Lion" if en else "Mit Shift Lion weiterplanen"}</h2><p>{"Use another calculator or keep your complete rotation in the app." if en else "Nutze den passenden Rechner oder plane deinen vollständigen Rhythmus in der App."}</p><div class="related">{related_html}</div></div><a class="primary" href="/download/android/">{"Download Shift Lion" if en else "Shift Lion herunterladen"}</a></section></main>
<footer><a href="/{'en/' if en else ''}">{"Home" if en else "Startseite"}</a><a href="/{'en/' if en else ''}tools/">{"All tools" if en else "Alle Tools"}</a><a href="/{'en/guides/' if en else 'ratgeber/'}">{"Guides" if en else "Ratgeber"}</a><a href="/{'en/methodology.html' if en else 'methodik.html'}">{"Methodology" if en else "Methodik"}</a><a href="/download/android/">{"Download app" if en else "App herunterladen"}</a></footer></body></html>'''


def render_guide_index(language):
    en = language == "en"
    site = CONFIG["site_url"].rstrip("/")
    relative = "en/guides/" if en else "ratgeber/"
    url = site + "/" + relative

    def category_for(path):
        slug = path.lower()
        if any(term in slug for term in ("nacht", "night", "feiertag", "holiday", "stundenlohn", "hourly-wage", "schichtzulagen", "shift-allowances")):
            return "pay"
        if any(term in slug for term in ("schichtplan", "shift-plan", "shared-days", "gemeinsame-freie")):
            return "planning"
        return "time"

    cards = "".join(
        f'<article data-category="{category_for(path)}" data-search="{html.escape((guide["h1"] + " " + guide["description"] + " " + guide["eyebrow"]).lower(), quote=True)}"><span>{html.escape(guide["eyebrow"])}</span><h2>{html.escape(guide["h1"])}</h2><p>{html.escape(guide["description"])}</p><a href="/{html.escape(path, quote=True)}">{"Read guide" if en else "Ratgeber lesen"} →</a></article>'
        for path, guide in GUIDES.items() if guide["lang"] == language
    )
    data = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "name": "Shift Lion Guides" if en else "Shift Lion Ratgeber", "url": url},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home" if en else "Startseite", "item": f"{site}/en/" if en else f"{site}/"},
            {"@type": "ListItem", "position": 2, "name": "Guides" if en else "Ratgeber", "item": url},
        ]},
    ]}
    other = f"{site}/ratgeber/" if en else f"{site}/en/guides/"
    json_ld = json.dumps(data, ensure_ascii=False)
    controls = f'''<section class="guide-controls" aria-label="{'Filter guides' if en else 'Ratgeber filtern'}"><label for="guideSearch">{'Search guides' if en else 'Ratgeber durchsuchen'}<input id="guideSearch" type="search" placeholder="{'Search by topic or term' if en else 'Thema oder Begriff eingeben'}" autocomplete="off"></label><div class="guide-filters" role="group" aria-label="{'Categories' if en else 'Kategorien'}"><button type="button" data-filter="all" aria-pressed="true">{'All guides' if en else 'Alle Ratgeber'}</button><button type="button" data-filter="time" aria-pressed="false">{'Working time' if en else 'Arbeitszeit'}</button><button type="button" data-filter="pay" aria-pressed="false">{'Pay & allowances' if en else 'Lohn & Zuschläge'}</button><button type="button" data-filter="planning" aria-pressed="false">{'Shift planning' if en else 'Schichtplanung'}</button></div><p id="guideResultCount" class="guide-result-count" aria-live="polite"></p></section>'''
    return f'''<!doctype html><html lang="{language}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{"Shift Work Guides and Calculations | Shift Lion" if en else "Ratgeber für Schichtarbeit und Berechnungen | Shift Lion"}</title><meta name="description" content="{"Practical guides for working time, allowances, overtime and shift planning with examples and free calculators." if en else "Praktische Ratgeber zu Arbeitszeit, Zuschlägen, Überstunden und Schichtplanung mit Beispielen und kostenlosen Rechnern."}"><link rel="canonical" href="{url}"><link rel="alternate" hreflang="{language}" href="{url}"><link rel="alternate" hreflang="{"de" if en else "en"}" href="{other}"><link rel="icon" href="/favicon.png"><link rel="stylesheet" href="/guide.css?v=1"><script type="application/ld+json">{json_ld}</script></head><body><header class="guide-hero guide-index-hero"><nav><a class="guide-logo" href="/{'en/' if en else ''}"><img src="/Shift-Lion-Logo-groß.png" alt="Shift Lion"></a><div><a href="/{'en/' if en else ''}">{"Home" if en else "Startseite"}</a><a href="/{'en/' if en else ''}tools/">Tools</a><a href="/{'ratgeber/' if en else 'en/guides/'}">{"DE" if en else "EN"}</a><a class="nav-cta" href="/download/android/">{"Download app" if en else "App herunterladen"}</a></div></nav><div class="hero-copy"><span>{"SHIFT WORK KNOWLEDGE" if en else "WISSEN FÜR SCHICHTARBEIT"}</span><h1>{"Guides for calculations and shift planning" if en else "Ratgeber für Berechnungen und Schichtplanung"}</h1><p>{"Clear explanations, practical examples and the matching free calculator for every topic." if en else "Verständliche Erklärungen, konkrete Beispiele und zu jedem Thema der passende kostenlose Rechner."}</p></div></header><main>{controls}<section class="guide-card-grid">{cards}</section><p class="guide-empty" hidden>{"No matching guide found." if en else "Kein passender Ratgeber gefunden."}</p></main><footer><a href="/{'en/' if en else ''}">{"Home" if en else "Startseite"}</a><a href="/{'en/' if en else ''}tools/">{"All tools" if en else "Alle Tools"}</a><a href="/kontakt.html">{"Contact" if en else "Kontakt"}</a><a href="/download/android/">{"Download app" if en else "App herunterladen"}</a></footer><script src="/guide-index.js?v=1"></script></body></html>'''


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(STATIC, OUT)

    for source in SRC.rglob("*.html"):
        rel = source.relative_to(SRC)
        if rel.as_posix() in LEGACY_REDIRECT_PAGES:
            continue
        target = OUT / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        text = source.read_text(encoding="utf-8")
        text = text.replace("{{NAV_DE}}", render_nav("nav", "nav"))
        text = text.replace("{{NAV_DE_DARK}}", render_nav("nav nav-dark", "div"))
        text = add_guide_navigation(text, rel)
        text = add_legacy_guide_trust(text, rel)
        text = add_seo_metadata(text, rel)
        text = add_tool_article_link(text, rel)
        text = add_planner_positioning(text, rel)
        text = add_structured_data(text, rel)
        text = optimize_content_images(text)
        text = remove_unpublished_legal_links(text)
        text = re.sub(r'/workdays-calculator\.js(?:\?v=\d+)?"', '/workdays-calculator.js?v=9"', text)
        text = re.sub(r'/calculator-tools\.css(?:\?v=\d+)?"', '/calculator-tools.css?v=6"', text)
        text = re.sub(r'/tool-hub\.js(?:\?v=\d+)?"', '/tool-hub.js?v=10"', text)
        if source.name in TOOL_PAGES or (
            source.name in {"schichtplaner-online.html", "schichtzulagen-rechner.html"}
            and rel.parts and rel.parts[0] == "en"
        ):
            text = re.sub(
                r"</head>",
                '<link rel="stylesheet" href="/tool-foundation.css?v=8">'
                '<style>html.tool-preparing main{visibility:hidden}</style>'
                '<script>document.documentElement.classList.add("tool-preparing");setTimeout(()=>document.documentElement.classList.remove("tool-preparing"),3000)</script>'
                '</head>',
                text,
                count=1,
                flags=re.I,
            )
            # Some tools contain printable HTML inside JavaScript template
            # strings. Inject at the real page end, never at an inner </body>.
            body_end = text.lower().rfind("</body>")
            if body_end != -1:
                text = (
                    text[:body_end]
                    + '<script src="/tool-foundation.js?v=12"></script>'
                    + text[body_end:]
                )
        target.write_text(text, encoding="utf-8")

    # Keep the English homepage visually identical to the German homepage.
    german_home = (SRC / "index.html").read_text(encoding="utf-8")
    style_match = re.search(r"<style>(.*?)</style>", german_home, re.S)
    if style_match:
        (OUT / "en" / "homepage-structure.css").write_text(style_match.group(1), encoding="utf-8")

    for relative, guide in GUIDES.items():
        target = OUT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render_guide(relative, guide), encoding="utf-8")

    for relative, language in (("ratgeber/index.html", "de"), ("en/guides/index.html", "en")):
        target = OUT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        index_html = render_guide_index(language).replace(
            "</head>", '<link rel="stylesheet" href="/guide-index.css?v=2"></head>'
        )
        target.write_text(index_html, encoding="utf-8")

    for relative, item in STEP9_TOOLS.items():
        target = OUT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render_step9_tool(relative, item).replace("/tool-foundation.css?v=3", "/tool-foundation.css?v=8").replace("/tool-foundation.js?v=4", "/tool-foundation.js?v=12"), encoding="utf-8")

    published_trust_pages = [relative for relative in TRUST_PAGES if relative not in {"impressum.html", "en/legal-notice.html"}]
    for relative in published_trust_pages:
        target = OUT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render_trust_page(relative), encoding="utf-8")

    for relative in REACH_PAGES:
        target = OUT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render_reach_page(relative), encoding="utf-8")

    # Apply shared metadata and accessibility after every source and generated
    # page has been written, so generated guides and tools stay consistent too.
    for target in OUT.rglob("*.html"):
        page = target.read_text(encoding="utf-8")
        page = add_social_metadata(page, target.relative_to(OUT))
        page = integrate_contact_page(page, target.relative_to(OUT))
        page = add_accessibility_foundation(page)
        target.write_text(page, encoding="utf-8")

    # Sitemap from the same config: no manual sitemap maintenance.
    urls = []
    for item in CONFIG["navigation_de"]:
        if item.get("sitemap"):
            urls.append(item["href"])
    urls.extend(CONFIG.get("extra_sitemap", []))
    urls.extend("/" + relative for relative in GUIDES)
    urls.extend(["/ratgeber/", "/en/guides/"])
    urls.extend("/" + relative for relative in STEP9_TOOLS)
    urls.extend("/" + relative for relative in published_trust_pages)
    urls.extend("/" + relative for relative in REACH_PAGES)

    base = CONFIG["site_url"].rstrip("/")
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    seen = set()
    for path in urls:
        if path in seen:
            continue
        seen.add(path)
        url = base + (path if path.startswith("/") else "/" + path)
        if path == "/":
            url = base + "/"
        lines += ["", "  <url>", f"    <loc>{html.escape(url)}</loc>", "  </url>"]
    lines += ["", "</urlset>", ""]
    (OUT / "sitemap.xml").write_text("\n".join(lines), encoding="utf-8")

    validate_internal_links()
    validate_seo_foundation()

    print(f"Build fertig: {OUT}")
    print(f"Seiten in Sitemap: {len(seen)}")

if __name__ == "__main__":
    build()
