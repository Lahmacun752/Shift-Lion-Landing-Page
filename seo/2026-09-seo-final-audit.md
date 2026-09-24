# Technische SEO-Abschlussprüfung – 24. September 2026

## Ergebnis

Die automatische Prüfung wurde über alle 83 URLs der Sitemap ausgeführt.

- 83 von 83 lokalen Seiten vorhanden
- 83 von 83 Live-URLs mit HTTP-Status 200
- genau ein Title pro indexierbarer Seite
- genau eine Meta-Beschreibung pro indexierbarer Seite
- genau ein passender Canonical pro indexierbarer Seite
- genau eine sichtbare H1 pro indexierbarer Seite
- gültiges JSON-LD auf allen 83 Seiten
- keine `noindex`-Anweisung auf Sitemap-Seiten
- keine fehlenden internen Seitenziele
- keine verwaisten Sitemap-Seiten
- Sitemap korrekt in `robots.txt` angegeben
- alte englische Frühschicht-URL leitet mit HTTP 301 auf die aktuelle URL weiter

## Behobene Lücken

Der erste Prüflauf fand 13 Seiten ohne strukturierte Daten. Betroffen waren:

- die fünf neueren Rechner in deutscher und englischer Sprache
- die Kontaktseite
- die deutsche und englische Zielgruppenseite für Schichtarbeiter

Die Build-Pipeline ergänzt nun auch für dynamisch generierte Seiten passende Breadcrumb-Daten. Dadurch erhalten neue Seiten die technische Grundlage künftig automatisch und müssen nicht einzeln nachgepflegt werden.

## Wiederholbare Prüfung

Lokaler Produktions-Build:

```powershell
python build.py
python seo\audit_site.py
```

Zusätzliche Kontrolle aller öffentlichen URLs und Weiterleitungen:

```powershell
python seo\audit_site.py --live
```

Das Skript beendet sich mit einem Fehlercode, sobald eine der geprüften SEO-Bedingungen verletzt wird. Es kann deshalb auch vor jedem späteren Deployment oder in einer automatisierten GitHub-Prüfung ausgeführt werden.
