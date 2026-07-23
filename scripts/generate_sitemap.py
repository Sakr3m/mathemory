#!/usr/bin/env python3
"""
Rigenera sitemap.xml scansionando tutti i file .html nella cartella principale
del sito. Va eseguito dalla cartella radice della repo.

- index.html ottiene sempre priorità 1.0 e cambio settimanale (è la home).
- Tutte le altre pagine .html ottengono priorità 0.8 e cambio mensile.
- L'ordine: index.html per primo, poi le altre in ordine alfabetico.

Pensato per essere lanciato in automatico a ogni pubblicazione tramite una
GitHub Action (vedi .github/workflows/update-sitemap.yml), così non serve
ricordarsi di aggiornare la sitemap a mano ogni volta che si aggiunge una
pagina nuova.
"""
import os
import sys

BASE_URL = "https://sakr3m.github.io/Mathemory"

def find_html_pages(root_dir):
    pages = []
    for name in sorted(os.listdir(root_dir)):
        if not name.endswith(".html") or not os.path.isfile(os.path.join(root_dir, name)):
            continue
        # file di verifica di Google Search Console (es. googleXXXXXXXX.html):
        # non sono pagine vere del sito, non vanno nella sitemap
        if name.startswith("google") and name != "index.html":
            continue
        pages.append(name)
    # index.html sempre per primo, se presente
    if "index.html" in pages:
        pages.remove("index.html")
        pages.insert(0, "index.html")
    return pages

def build_sitemap(pages):
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for page in pages:
        is_home = (page == "index.html")
        loc = f"{BASE_URL}/" if is_home else f"{BASE_URL}/{page}"
        changefreq = "weekly" if is_home else "monthly"
        priority = "1.0" if is_home else "0.8"
        lines.append("  <url>")
        lines.append(f"    <loc>{loc}</loc>")
        lines.append(f"    <changefreq>{changefreq}</changefreq>")
        lines.append(f"    <priority>{priority}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"

def main():
    root_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    pages = find_html_pages(root_dir)
    sitemap = build_sitemap(pages)
    out_path = os.path.join(root_dir, "sitemap.xml")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(sitemap)
    print(f"sitemap.xml scritta con {len(pages)} pagine: {', '.join(pages)}")

if __name__ == "__main__":
    main()
