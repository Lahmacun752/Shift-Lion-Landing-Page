from pathlib import Path
import json, shutil, html

ROOT = Path(__file__).parent
SRC = ROOT / "src" / "pages"
STATIC = ROOT / "static"
OUT = ROOT / "hosting"
CONFIG = json.loads((ROOT / "site.json").read_text(encoding="utf-8"))


def render_nav(css_class="nav", tag="nav"):
    links = []
    for item in CONFIG["navigation_de"]:
        href = html.escape(item["href"], quote=True)
        label = html.escape(item["label"])
        links.append(f'  <a href="{href}">{label}</a>')
    return f'<{tag} class="{css_class}">\n' + "\n".join(links) + f'\n</{tag}>'


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(STATIC, OUT)

    for source in SRC.rglob("*.html"):
        rel = source.relative_to(SRC)
        target = OUT / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        text = source.read_text(encoding="utf-8")
        text = text.replace("{{NAV_DE}}", render_nav("nav", "nav"))
        text = text.replace("{{NAV_DE_DARK}}", render_nav("nav nav-dark", "div"))
        target.write_text(text, encoding="utf-8")

    # Sitemap from the same config: no manual sitemap maintenance.
    urls = []
    for item in CONFIG["navigation_de"]:
        if item.get("sitemap"):
            urls.append(item["href"])
    urls.extend(CONFIG.get("extra_sitemap", []))

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

    print(f"Build fertig: {OUT}")
    print(f"Seiten in Sitemap: {len(seen)}")

if __name__ == "__main__":
    build()
