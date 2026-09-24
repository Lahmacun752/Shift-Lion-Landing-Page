# Mobile-Performance-Prüfung – 24. September 2026

## Umfang

Geprüft wurden die fünf wichtigsten Seitentypen:

- Startseite
- Toolübersicht
- Arbeitszeitrechner
- Nachtzuschlag-Rechner
- Schichten vergleichen

Messwerkzeug: Lighthouse 12.8.2, mobiles Profil mit simulierter Drosselung. Die Ausgangswerte wurden gegen die veröffentlichten Seiten ermittelt. Die Werte nach der Optimierung stammen aus dem lokalen Produktions-Build. Einzelne Zeitwerte schwanken je nach Rechner, Netzwerk und Serverantwort; die Bewertung von Layout-Stabilität und Übertragungsgröße ist hier entscheidend.

## Ergebnisse

| Seite | Performance vorher | Performance danach | LCP danach | CLS vorher | CLS danach | TBT danach |
|---|---:|---:|---:|---:|---:|---:|
| Startseite | 100 | 100 | 1,3 s | 0 | 0 | 0 ms |
| Toolübersicht | 100 | 100 | 1,7 s | 0 | 0 | 0 ms |
| Arbeitszeitrechner | 86 | 100 | 1,5 s | 0,269 | 0,008 | 0 ms |
| Nachtzuschlag-Rechner | 92 | 100 | 1,4 s | 0,185 | 0,007 | 0 ms |
| Schichten vergleichen | 90 | 100 | 1,4 s | 0,208 | 0 | 10 ms |

Alle LCP-Werte liegen deutlich unter dem empfohlenen Grenzwert von 2,5 Sekunden. Alle CLS-Werte liegen nach der Optimierung deutlich unter 0,1. JavaScript blockiert die Seiten praktisch nicht.

## Umgesetzte Verbesserungen

- Das sichtbare Logo wird als passend skalierte WebP-Datei mit 320 × 171 Pixeln ausgeliefert. Die Dateigröße sinkt von rund 19 KB auf rund 6 KB.
- Die große Startseitengrafik wird als WebP-Datei mit 640 × 1137 Pixeln ausgeliefert. Die Dateigröße sinkt von rund 334 KB auf rund 161 KB.
- Rechnerbereiche werden erst sichtbar, nachdem die per JavaScript erzeugten Eingaben, Ergebnisfelder und Kalender aufgebaut sind. Dadurch springen nachfolgende Inhalte nicht mehr sichtbar.
- Eine Sicherheitsfreigabe macht den Inhalt nach drei Sekunden sichtbar, falls ein Skript unerwartet nicht fertig wird.
- Bereits vorhandene Optimierungen wurden bestätigt: Systemschriftarten statt externer Webfonts, WebP-Ausgabe, feste Bildabmessungen, Lazy Loading unterhalb des sichtbaren Bereichs und langfristiges Browser-Caching für statische Dateien.

## Kontrolle nach Veröffentlichung

Nach dem Deployment sollten dieselben fünf URLs erneut gegen die Live-Domain gemessen werden. Die anonyme Google-PageSpeed-API antwortete während dieser Prüfung mit HTTP 429; deshalb wurde Lighthouse lokal mit demselben mobilen Profil verwendet.
