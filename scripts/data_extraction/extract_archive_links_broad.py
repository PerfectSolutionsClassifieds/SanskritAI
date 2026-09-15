"""
Broader extractor for saved Archive.org search HTML files.

- Scans saved *_page.html files for any occurrence of '/details/' (href, data-attr, JS).
- Produces archive_links_broad.json with {filename, lemma, item_url_candidates}.
- Use when saved search pages may not include standard <a href="/details/..."> links.
"""

import glob
import json
import re
from urllib.parse import urljoin

def extract_lemma_from_filename(fn):
    m = re.match(r"([a-zA-Z0-9_\-]+)_page\.html", fn)
    return m.group(1) if m else fn

def find_details_urls(html):
    # Find all /details/<identifier> occurrences in the HTML (hrefs, JS, data attributes)
    found = set()
    for m in re.finditer(r'(/details/[A-Za-z0-9_\-]+)', html):
        found.add(m.group(1))
    # Also look for full URLs
    for m in re.finditer(r'(https?://archive\.org/details/[A-Za-z0-9_\-]+)', html):
        found.add(m.group(1))
    # Normalize to absolute URLs
    urls = []
    for u in sorted(found):
        if u.startswith("http"):
            urls.append(u)
        else:
            urls.append(urljoin("https://archive.org", u))
    return urls

def main():
    files = sorted(glob.glob("*_page.html"))
    results = []
    for fn in files:
        try:
            with open(fn, "rb") as f:
                raw = f.read()
            try:
                html = raw.decode("utf-8")
            except:
                html = raw.decode("latin-1", errors="ignore")
            lemma = extract_lemma_from_filename(fn)
            urls = find_details_urls(html)
            results.append({"filename": fn, "lemma": lemma, "item_url_candidates": urls})
            print(f"{fn}: found {len(urls)} candidate(s)")
        except Exception as e:
            print(f"Error {fn}: {e}")
    with open("archive_links_broad.json", "w", encoding="utf-8") as out:
        json.dump(results, out, ensure_ascii=False, indent=2)
    print("Saved archive_links_broad.json")

if __name__ == "__main__":
    main()
