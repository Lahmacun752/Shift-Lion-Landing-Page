import html
import json


PAGES = {
    "methodik.html": "de",
    "en/methodology.html": "en",
    "datenschutz.html": "de",
    "en/privacy.html": "en",
    "impressum.html": "de",
    "en/legal-notice.html": "en",
}


SOURCES = [
    ("Arbeitszeitgesetz (ArbZG)", "Arbeitszeit, Ruhepausen, Ruhezeit sowie Sonn- und Feiertagsruhe", "https://www.gesetze-im-internet.de/arbzg/"),
    ("Einkommensteuergesetz § 3b", "Steuerliche Grenzen für tatsächlich geleistete Sonn-, Feiertags- und Nachtarbeit", "https://www.gesetze-im-internet.de/estg/__3b.html"),
    ("Entgeltfortzahlungsgesetz § 2", "Entgeltzahlung, wenn Arbeit wegen eines Feiertags ausfällt", "https://www.gesetze-im-internet.de/entgfg/__2.html"),
    ("Bundesurlaubsgesetz", "Gesetzlicher Mindesturlaub und Teilurlaub", "https://www.gesetze-im-internet.de/burlg/"),
    ("Bundesarbeitsgericht 5 AZR 431/16", "Einordnung von Sonn- und Feiertagszuschlägen", "https://www.bundesarbeitsgericht.de/entscheidung/5-azr-431-16/"),
]


def shell(title, description, body, en=False):
    lang = "en" if en else "de"
    home = "/en/" if en else "/"
    tools = "/en/tools/" if en else "/tools/"
    method = "/en/methodology.html" if en else "/methodik.html"
    privacy = "/en/privacy.html" if en else "/datenschutz.html"
    contact = "mailto:masterinpocket@gmail.com"
    lowered = title.lower()
    if "method" in lowered or "calculate" in lowered or "rechnen" in lowered:
        slug = "en/methodology.html" if en else "methodik.html"
    elif "privacy" in lowered or "datenschutz" in lowered:
        slug = "en/privacy.html" if en else "datenschutz.html"
    else:
        slug = "en/legal-notice.html" if en else "impressum.html"
    page_url = f"https://shiftlion.app/{slug}"
    structured_data = json.dumps({"@context": "https://schema.org", "@graph": [{"@type": "WebPage", "name": title, "description": description, "url": page_url, "inLanguage": lang}, {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home" if en else "Startseite", "item": f"https://shiftlion.app{home}"}, {"@type": "ListItem", "position": 2, "name": title, "item": page_url}]}]}, ensure_ascii=False).replace("</", "<\\/")
    return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)} | Shift Lion</title><meta name="description" content="{html.escape(description, quote=True)}"><link rel="icon" href="/favicon.png"><link rel="canonical" href="{page_url}"><link rel="stylesheet" href="/trust.css?v=2"><script type="application/ld+json">{structured_data}</script></head><body><header><nav><a class="logo" href="{home}"><img src="/Shift-Lion-Logo-groß.png" alt="Shift Lion" width="852" height="456"></a><div><a href="{home}">{'Home' if en else 'Startseite'}</a><a href="{tools}">{'Tools' if en else 'Rechner'}</a><a href="{method}">{'Methodology' if en else 'Methodik'}</a></div></nav><div class="hero-copy"><span>{'TRANSPARENCY' if en else 'TRANSPARENZ'}</span><h1>{html.escape(title)}</h1><p>{html.escape(description)}</p></div></header><main>{body}</main><footer><a href="{method}">{'Methodology' if en else 'So rechnen die Tools'}</a><a href="{privacy}">{'Privacy' if en else 'Datenschutz'}</a><a href="{contact}">{'Contact' if en else 'Kontakt'}</a><small>© 2026 Shift Lion · Master in Pocket</small></footer></body></html>'''


def methodology(en=False):
    source_cards = "".join(f'<article><h3>{html.escape(name)}</h3><p>{html.escape(purpose)}</p><a href="{url}" target="_blank" rel="noopener">{'Open official source' if en else 'Amtliche Quelle öffnen'} ↗</a></article>' for name, purpose, url in SOURCES)
    if en:
        body = f'''<section><h2>What the calculators do</h2><p>Shift Lion calculators turn the values you enter into transparent estimates. Time differences are calculated in minutes; pay figures use the entered hourly wage, eligible hours and allowance rate. Results are rounded only for display.</p><div class="principles"><article><strong>Inputs</strong><p>You control times, rates, work models and assumptions.</p></article><article><strong>Calculation</strong><p>The formula is shown on the calculator or its explanatory section.</p></article><article><strong>Result</strong><p>Pay values are gross estimates unless the page explicitly says otherwise.</p></article></div></section><section><h2>Core formulas at a glance</h2><div class="formula-table"><div><strong>Working time</strong><span>End − start − unpaid break</span></div><div><strong>Allowance</strong><span>Eligible hours × hourly wage × rate</span></div><div><strong>Overtime pay</strong><span>Overtime hours × hourly wage × (1 + premium)</span></div><div><strong>Workdays</strong><span>Planned workdays − holidays off − leave days</span></div></div><p class="note">Paid breaks remain in base pay and eligible allowances. Unpaid breaks are deducted from both wherever the calculator offers this selection.</p></section><section><h2>What is not automatically assessed</h2><p>The tools do not determine which collective agreement, employment contract, works agreement, state holiday law or exception applies to you. They do not provide legal, tax or financial advice. Your contract, applicable collective agreement, payslip and current law remain authoritative.</p></section><section><h2>How content is reviewed</h2><ol class="review-steps"><li>Formulas and visible examples are compared.</li><li>Legal references link to official primary sources.</li><li>Calculator edge cases such as overnight shifts and unpaid breaks are tested.</li><li>Material rule or calculator changes trigger a new content review.</li></ol></section><section><h2>Sources</h2><div class="source-grid">{source_cards}</div><p class="note">Last content review: 23 September 2026. Links lead to primary German legal sources.</p></section><section><h2>Built for shift workers</h2><p>Shift Lion grew from the practical problem that ordinary calendars rarely understand rotating early, late and night shifts. The website combines quick calculations with the app’s longer-term shift planning. The aim is clarity—not false precision.</p><a class="primary" href="/en/tools/">Open all calculators →</a></section>'''
        return shell("How the Shift Lion tools calculate", "Formulas, assumptions, limits and official sources behind the Shift Lion calculators.", body, True)
    body = f'''<section><h2>Was die Rechner tun</h2><p>Die Shift-Lion-Rechner wandeln deine Eingaben in nachvollziehbare Schätzungen um. Zeitdifferenzen werden minutengenau verarbeitet; Lohnwerte verwenden den eingetragenen Stundenlohn, die anrechenbaren Stunden und den gewählten Zuschlagssatz. Gerundet wird grundsätzlich erst für die Anzeige.</p><div class="principles"><article><strong>Eingaben</strong><p>Du bestimmst Uhrzeiten, Sätze, Arbeitsmodelle und Annahmen.</p></article><article><strong>Rechenweg</strong><p>Die Formel steht direkt am Rechner oder im erklärenden Abschnitt.</p></article><article><strong>Ergebnis</strong><p>Geldbeträge sind Brutto-Schätzungen, sofern nicht ausdrücklich anders angegeben.</p></article></div></section><section><h2>Die wichtigsten Formeln im Überblick</h2><div class="formula-table"><div><strong>Arbeitszeit</strong><span>Ende − Beginn − unbezahlte Pause</span></div><div><strong>Zuschlag</strong><span>Zuschlagsstunden × Stundenlohn × Zuschlagssatz</span></div><div><strong>Überstundenlohn</strong><span>Überstunden × Stundenlohn × (1 + Zuschlag)</span></div><div><strong>Arbeitstage</strong><span>Geplante Arbeitstage − freie Feiertage − Urlaubstage</span></div></div><p class="note">Bezahlte Pausen bleiben im Grundlohn und in den anrechenbaren Zuschlägen enthalten. Unbezahlte Pausen werden bei entsprechender Auswahl von beidem abgezogen.</p></section><section><h2>Was nicht automatisch geprüft wird</h2><p>Die Tools entscheiden nicht, welcher Tarifvertrag, Arbeitsvertrag, welche Betriebsvereinbarung, welches Landesfeiertagsrecht oder welche Ausnahme auf dich zutrifft. Sie ersetzen keine Rechts-, Steuer- oder Finanzberatung. Maßgeblich bleiben dein Vertrag, anwendbare Tarifregeln, deine Lohnabrechnung und das aktuelle Recht.</p></section><section><h2>So prüfen wir die Inhalte</h2><ol class="review-steps"><li>Formeln und sichtbare Rechenbeispiele werden miteinander abgeglichen.</li><li>Rechtliche Hinweise verlinken auf amtliche Primärquellen.</li><li>Sonderfälle wie Nachtschichten über Mitternacht und unbezahlte Pausen werden getestet.</li><li>Wesentliche Regel- oder Rechneränderungen lösen eine erneute Inhaltsprüfung aus.</li></ol></section><section><h2>Verwendete Quellen</h2><div class="source-grid">{source_cards}</div><p class="note">Letzte inhaltliche Prüfung: 23. September 2026. Die Links führen zu amtlichen deutschen Rechtsquellen.</p></section><section><h2>Entwickelt für Schichtarbeiter</h2><p>Shift Lion entstand aus dem praktischen Problem, dass gewöhnliche Kalender wechselnde Früh-, Spät- und Nachtschichten kaum verstehen. Die Website verbindet schnelle Berechnungen mit der langfristigen Schichtplanung der App. Das Ziel ist Klarheit – nicht vorgetäuschte Genauigkeit.</p><a class="primary" href="/tools/">Alle Rechner öffnen →</a></section>'''
    return shell("So rechnen die Shift-Lion-Tools", "Formeln, Annahmen, Grenzen und amtliche Quellen hinter den Shift-Lion-Rechnern.", body)


def privacy(en=False):
    if en:
        body = '''<section><h2>Local calculator data</h2><p>Values entered into the web calculators are processed in your browser. Step 8 may store calculator inputs locally in your browser so they remain available after a reload. You can remove them through your browser’s site-data controls.</p></section><section><h2>No analytics or advertising scripts</h2><p>The current website does not embed analytics, advertising or behavioural tracking scripts. The website is delivered through Firebase Hosting; technically necessary connection data may be processed by the hosting provider.</p></section><section><h2>App data</h2><p>The current Shift Lion app can be used without an account. Shift, appointment, working-time, wage and settings data is stored locally on the device and is not automatically transmitted to the provider.</p></section><section><h2>Contact</h2><p>If you email us, we process the information you provide to answer your request. Contact: <a href="mailto:masterinpocket@gmail.com">masterinpocket@gmail.com</a>.</p><p>Version: 22 September 2026.</p></section>'''
        return shell("Privacy policy", "How the Shift Lion website and app handle locally entered data.", body, True)
    body = '''<section><h2>Lokale Rechnerdaten</h2><p>Eingaben in die Web-Rechner werden in deinem Browser verarbeitet. Seit Schritt 8 können Rechnerwerte lokal im Browser gespeichert werden, damit sie nach einem Neuladen erhalten bleiben. Du kannst sie über die Website-Daten deines Browsers löschen.</p></section><section><h2>Keine Analyse- oder Werbeskripte</h2><p>Die aktuelle Website bindet keine Analyse-, Werbe- oder verhaltensbezogenen Tracking-Skripte ein. Die Bereitstellung erfolgt über Firebase Hosting; dabei können technisch notwendige Verbindungsdaten durch den Hostinganbieter verarbeitet werden.</p></section><section><h2>Daten in der App</h2><p>Die aktuelle Shift-Lion-App kann ohne Benutzerkonto verwendet werden. Schicht-, Termin-, Arbeitszeit-, Lohn- und Einstellungsdaten werden lokal auf dem Gerät gespeichert und nicht automatisch an den Anbieter übertragen.</p></section><section><h2>Kontakt</h2><p>Wenn du uns per E-Mail kontaktierst, verarbeiten wir deine freiwilligen Angaben zur Beantwortung der Anfrage. Kontakt: <a href="mailto:masterinpocket@gmail.com">masterinpocket@gmail.com</a>.</p><p>Stand: 22. September 2026.</p></section>'''
    return shell("Datenschutzerklärung", "So verarbeitet die Shift-Lion-Website lokal eingegebene Daten.", body)


def legal(en=False):
    if en:
        body = '''<section><h2>Provider</h2><p><strong>Master in Pocket</strong><br>Contact: <a href="mailto:masterinpocket@gmail.com">masterinpocket@gmail.com</a></p><div class="warning"><strong>Required before publication:</strong> The provider’s legal name and serviceable postal address are not available in the project data and must be supplied to complete this legal notice.</div></section><section><h2>Editorial responsibility</h2><p>Master in Pocket, address to be added before publication.</p></section>'''
        return shell("Legal notice", "Provider and contact details for the Shift Lion website.", body, True)
    body = '''<section><h2>Anbieter</h2><p><strong>Master in Pocket</strong><br>Kontakt: <a href="mailto:masterinpocket@gmail.com">masterinpocket@gmail.com</a></p><div class="warning"><strong>Vor Veröffentlichung erforderlich:</strong> Der bürgerliche Name beziehungsweise die vollständige Firmierung und eine ladungsfähige Anschrift sind in den Projektdaten nicht vorhanden und müssen für ein vollständiges Impressum ergänzt werden.</div></section><section><h2>Redaktionell verantwortlich</h2><p>Master in Pocket, Anschrift vor Veröffentlichung ergänzen.</p></section>'''
    return shell("Impressum", "Anbieter- und Kontaktangaben der Shift-Lion-Website.", body)


def render(path):
    en = PAGES[path] == "en"
    if "method" in path:
        return methodology(en)
    if "privacy" in path or "datenschutz" in path:
        return privacy(en)
    return legal(en)
