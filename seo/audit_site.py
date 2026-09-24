"""Automated technical SEO audit for the generated Shift Lion website."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse


ROOT = Path(__file__).resolve().parents[1]
HOSTING = ROOT / "hosting"
SITE_ORIGIN = "https://shiftlion.app"


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_parts: list[str] = []
        self.in_title = False
        self.h1_count = 0
        self.descriptions: list[str] = []
        self.canonicals: list[str] = []
        self.robots: list[str] = []
        self.links: list[str] = []
        self.json_ld: list[str] = []
        self.in_json_ld = False
        self.json_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): value or "" for key, value in attrs}
        tag = tag.lower()
        if tag == "title":
            self.in_title = True
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "meta" and values.get("name", "").lower() == "description":
            self.descriptions.append(values.get("content", "").strip())
        elif tag == "meta" and values.get("name", "").lower() == "robots":
            self.robots.append(values.get("content", "").lower())
        elif tag == "link" and "canonical" in values.get("rel", "").lower().split():
            self.canonicals.append(values.get("href", "").strip())
        elif tag == "a" and values.get("href"):
            self.links.append(values["href"].strip())
        elif tag == "script" and values.get("type", "").lower() == "application/ld+json":
            self.in_json_ld = True
            self.json_parts = []

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self.in_title = False
        elif tag == "script" and self.in_json_ld:
            self.json_ld.append("".join(self.json_parts).strip())
            self.in_json_ld = False
            self.json_parts = []

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)
        if self.in_json_ld:
            self.json_parts.append(data)

    @property
    def title(self) -> str:
        return " ".join("".join(self.title_parts).split())


def sitemap_urls() -> list[str]:
    root = ET.parse(HOSTING / "sitemap.xml").getroot()
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    return [element.text.strip() for element in root.findall("sm:url/sm:loc", namespace) if element.text]


def url_to_file(url: str) -> Path:
    path = urlparse(url).path
    if path.endswith("/"):
        path += "index.html"
    elif not Path(path).suffix:
        path += "/index.html"
    return HOSTING / path.lstrip("/")


def inspect_page(url: str, sitemap: set[str]) -> tuple[list[str], set[str]]:
    errors: list[str] = []
    internal_targets: set[str] = set()
    source = url_to_file(url)
    if not source.is_file():
        return [f"{url}: Datei fehlt im Hosting-Build"], internal_targets

    parser = PageParser()
    parser.feed(source.read_text(encoding="utf-8"))
    if not parser.title:
        errors.append(f"{url}: Title fehlt")
    if len(parser.descriptions) != 1 or not parser.descriptions[0]:
        errors.append(f"{url}: genau eine Meta-Beschreibung erwartet")
    if len(parser.canonicals) != 1:
        errors.append(f"{url}: genau ein Canonical erwartet")
    elif parser.canonicals[0] != url:
        errors.append(f"{url}: Canonical zeigt auf {parser.canonicals[0]}")
    if parser.h1_count != 1:
        errors.append(f"{url}: {parser.h1_count} H1 statt genau einer")
    if any("noindex" in directive for directive in parser.robots):
        errors.append(f"{url}: Sitemap-URL ist auf noindex gesetzt")
    if not parser.json_ld:
        errors.append(f"{url}: strukturierte Daten fehlen")
    for block_number, block in enumerate(parser.json_ld, start=1):
        try:
            json.loads(block)
        except json.JSONDecodeError as exc:
            errors.append(f"{url}: JSON-LD-Block {block_number} ungültig ({exc.msg})")

    for href in parser.links:
        parsed = urlparse(href)
        if parsed.scheme in {"mailto", "tel", "javascript", "data"}:
            continue
        absolute = urljoin(url, href)
        target = urlparse(absolute)
        if target.netloc != "shiftlion.app":
            continue
        clean = f"{target.scheme or 'https'}://{target.netloc}{target.path}"
        if clean.endswith("/") or Path(target.path).suffix == ".html":
            internal_targets.add(clean)
            if clean not in sitemap and not url_to_file(clean).is_file():
                errors.append(f"{url}: internes Linkziel fehlt ({href})")
    return errors, internal_targets


class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, file_pointer, code, message, headers, new_url):
        return None


def fetch_status(url: str, follow_redirects: bool = True) -> tuple[int, str]:
    request = urllib.request.Request(url, headers={"User-Agent": "ShiftLion-SEO-Audit/1.0"})
    opener = urllib.request.build_opener() if follow_redirects else urllib.request.build_opener(NoRedirectHandler())
    try:
        with opener.open(request, timeout=20) as response:
            return response.status, response.geturl()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.headers.get("Location", "")


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("--live", action="store_true", help="also verify all public URLs")
    args = argument_parser.parse_args()

    urls = sitemap_urls()
    sitemap = set(urls)
    errors: list[str] = []
    linked_targets: set[str] = set()

    if len(urls) != len(sitemap):
        errors.append("Sitemap enthält doppelte URLs")
    for url in urls:
        page_errors, page_targets = inspect_page(url, sitemap)
        errors.extend(page_errors)
        linked_targets.update(page_targets)

    robots = (HOSTING / "robots.txt").read_text(encoding="utf-8")
    if "Disallow: /" in robots:
        errors.append("robots.txt sperrt die gesamte Website")
    if "Sitemap: https://shiftlion.app/sitemap.xml" not in robots:
        errors.append("Sitemap-Verweis fehlt in robots.txt")

    orphaned = sorted(url for url in sitemap if url != f"{SITE_ORIGIN}/" and url not in linked_targets)
    if orphaned:
        errors.extend(f"{url}: kein interner Link gefunden" for url in orphaned)

    live_results: dict[str, int] = {}
    if args.live:
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(fetch_status, url): url for url in urls}
            for future in as_completed(futures):
                url = futures[future]
                try:
                    status, final_url = future.result()
                    live_results[url] = status
                    if status != 200:
                        errors.append(f"{url}: Live-Status {status}")
                    if final_url.rstrip("/") != url.rstrip("/"):
                        errors.append(f"{url}: unerwartete Weiterleitung zu {final_url}")
                except Exception as exc:
                    errors.append(f"{url}: Live-Prüfung fehlgeschlagen ({exc})")

        status, location = fetch_status(
            f"{SITE_ORIGIN}/en/fruehschicht-tipps-englisch.html", follow_redirects=False
        )
        if status != 301 or location != "/en/fruehschicht-tipps.html":
            errors.append(
                "Legacy-Weiterleitung fehlerhaft: "
                f"Status {status}, Ziel {location or '(fehlt)'}"
            )

    structured_pages = 0
    for url in urls:
        parser = PageParser()
        parser.feed(url_to_file(url).read_text(encoding="utf-8"))
        structured_pages += bool(parser.json_ld)

    print(f"Sitemap-URLs: {len(urls)}")
    print(f"Lokale HTML-Seiten geprüft: {len(urls)}")
    print(f"Seiten mit validem JSON-LD: {structured_pages if not errors else 'siehe Fehlerliste'}")
    if args.live:
        print(f"Live-URLs mit HTTP 200: {sum(status == 200 for status in live_results.values())}/{len(urls)}")
        print("Legacy-Weiterleitung: geprüft")
    if errors:
        print(f"Fehler: {len(errors)}")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Ergebnis: keine technischen SEO-Fehler gefunden")
    return 0


if __name__ == "__main__":
    sys.exit(main())
