# Shift Lion Landing Page – strukturierte Version

Diese Version trennt **Quellseiten** und **generierte Firebase-Dateien**.

## Ordner

- `src/pages/` – HTML-Seiten, die du bearbeitest
- `site.json` – zentrale Navigation + Sitemap-Konfiguration
- `static/` – Bilder, robots.txt, Download-Weiterleitung usw.
- `hosting/` – wird automatisch erzeugt; nicht von Hand pflegen
- `build.py` – baut die Website
- `deploy.ps1` – baut und deployed zu Firebase

## Neue SEO-Seite hinzufügen

1. Neue HTML-Datei in `src/pages/` anlegen.
2. An der Stelle der langen Navigation nur `{{NAV_DE}}` verwenden.
3. **Einmal** in `site.json` unter `navigation_de` ergänzen, z. B.:

```json
{
  "href": "/schichtkalender.html",
  "label": "🗓️ Schichtkalender",
  "sitemap": true
}
```

4. Ausführen:

```powershell
.\deploy.ps1
```

Damit werden automatisch:
- alle Navigationen aktualisiert,
- `sitemap.xml` neu erzeugt,
- der `hosting/`-Ordner gebaut,
- Firebase deployed.

## Nur lokal bauen

```powershell
python .\build.py
```

## Wichtig

`hosting/` ist Build-Ausgabe. Die Master-Dateien liegen in `src/pages/`, `static/` und `site.json`.
GitHub sollte diese Master-Dateien enthalten.
