# Shift Lion – Testplan für die Rechner

Stand: 14. September 2026. Dieser Plan ist die gemeinsame Prüfbasis vor und nach jeder Rechner-Änderung. Jede Zeile wird in Deutsch und Englisch sowie auf Desktop und Mobilgerät geprüft.

## Gemeinsame Prüfregeln

- Leere Pflichtfelder, negative Werte und ungültige Zeiträume zeigen eine verständliche Fehlermeldung. Es bleibt kein altes Ergebnis sichtbar.
- Ein Ergebnis wird bei jeder Eingabe sofort aktualisiert und beim Button erneut korrekt berechnet.
- `22:00` bis `06:00` bedeutet eine Schicht über Mitternacht. Gleiche Start- und Endzeit darf nicht unbemerkt zu einem falschen Wert führen.
- Kopieren übernimmt die sichtbaren Werte. Zurücksetzen stellt nachvollziehbare Standardwerte wieder her.
- Die Ergebniswerte, Farben und Beschriftungen bleiben bei schmaler Mobilansicht lesbar.

## Arbeitstage-Rechner

| Fall | Eingabe | Erwartung |
| --- | --- | --- |
| 5-Tage-Woche | 01.–30.09.2026, Mo–Fr | 22 geplante Arbeitstage |
| 6-Tage-Woche | 01.–30.09.2026, Mo–Sa | 26 geplante Arbeitstage |
| Individueller Rhythmus | E,E,L,L,N,N,O,O ab 01.09.2026 | Arbeit und frei folgen exakt dem gewählten Rhythmus |
| Feiertag frei | Arbeitstag am Feiertag, Option „an Feiertagen frei“ | Feiertag wird separat gezählt und von effektiven Arbeitstagen abgezogen |
| Feiertag im Rhythmus | Arbeitstag am Feiertag, Option „nach Rhythmus arbeiten“ | Feiertag bleibt Arbeitstag, wird aber im Kalender markiert |
| Urlaub + Feiertag | Urlaubszeitraum enthält Feiertag | kein doppelter Abzug |
| Ungültiges Datum | Ende vor Beginn | Fehlermeldung, keine alten Kennzahlen |
| Sachsen | Buß- und Bettag | Mittwoch vor dem 23. November |

## Arbeitszeit-Rechner

| Fall | Eingabe | Erwartung |
| --- | --- | --- |
| Tagschicht | 06:00–14:00, 30 Min. Pause | 8:00 h brutto, 7:30 h netto |
| Nachtschicht | 22:00–06:00, 30 Min. Pause | 8:00 h brutto, 7:30 h netto |
| Pause zu lang | 06:00–08:00, 180 Min. Pause | Fehlermeldung statt stiller Korrektur |
| Mindestpause | 06:00–14:00, 15 Min. Pause | klare Pausenwarnung |
| Entfernen | mittlere Schicht entfernen | Tagesnummern und Summe bleiben korrekt |

## Zuschlagsrechner

| Rechner | Fall | Erwartung |
| --- | --- | --- |
| Nachtzuschlag | 22:00–06:00, Nachtfenster 23:00–06:00 | 7:00 Nachtstunden vor Berücksichtigung einer Pause |
| Feiertagszuschlag | 06:00–14:00, 30 Min., 20 €/h, 100 % | 7:30 bezahlte Stunden, 150 € Grundlohn, 150 € Feiertagszuschlag, 300 € Gesamt brutto |
| Feiertag + Schichtzulage | derselbe Fall, 10 % Schichtzulage | Zuschläge separat und Gesamt nachvollziehbar ausgewiesen |
| Über Mitternacht | 22:00–06:00 | Datum und zuschlagsfähige Stunden sind nachvollziehbar getrennt |
| Ungültig | fehlende Zeit oder negative Pause | Fehlermeldung, kein scheinbar gültiges Ergebnis |

## Lohn- und Überstunden-Rechner

| Rechner | Fall | Erwartung |
| --- | --- | --- |
| Stundenlohn | 3.000 €/Monat, 40 Std./Woche, 52 Wochen | Jahresgehalt 36.000 €, Stundenlohn 36.000 ÷ 2.080 = 17,31 € |
| Stundenlohn | 0 Wochenstunden | Fehlermeldung, kein extrem hoher Stundenlohn |
| Überstunden | 10 Std., 20 €/h, 25 % | 200 € Grundvergütung, 50 € Zuschlag, 250 € Auszahlung |
| Freizeitausgleich | 10 Std., Faktor 1,25, 7,5-Std.-Tag | 12,5 Std. und ca. 1,67 freie Arbeitstage |

## Online-Schichtplaner und Schichtvergleich

| Fall | Erwartung |
| --- | --- |
| Rhythmus verlängern | „+ Tag“ fügt sichtbar einen Schichttag hinzu und berechnet neu |
| Einzelner Kalendertag | manuelle Änderung bleibt sichtbar, ohne den Grundrhythmus zu zerstören |
| Zwei gleiche freie Tage | gemeinsamer freier Tag wird im Kalender und in der Ergebniszahl gezeigt |
| Keine Überschneidung | klare Meldung statt leerer Ergebnisfläche |

## Abnahme vor Veröffentlichung

- Deutsche und englische Seite haben dieselben Funktionen und dieselbe Reihenfolge.
- Jede Toolkarte und jeder Button führt zur richtigen Seite.
- Mobil: Navigation, Eingaben, Ergebnis, Kopieren und Zurücksetzen funktionieren.
- Browser-Konsole zeigt keine Fehler.
- Nach `python .\\build.py` stimmen die erzeugten Dateien im Ordner `hosting` mit dem Quellstand überein.
