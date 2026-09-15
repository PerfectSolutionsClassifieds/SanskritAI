"""
Extract first Archive.org item links from saved Archive search pages.

Usage:
  1. Place your saved search HTML files (e.g., dharma_page.html) in the same folder.
  2. Run: python extract_archive_links.py
  3. Output: archive_links.json with {filename, lemma, item_url}
"""

import glob
import json
from bs4 import BeautifulSoup
import re

def find_archive_item(html):
    soup = BeautifulSoup(html, "html.parser")
    # Prefer links that contain /details/
    a = soup.select_one("a[href*='/details/']")
    if a:
        href = a.get("href")
        # Make absolute if needed
        if href.startswith("/"):
            href = "https://archive.org" + href
        return href
    # fallback: any link with /details/ in text
    for a in soup.find_all("a", href=True):
        if "/details/" in a['href']:
            href = a['href']
            if href.startswith("/"):
                href = "https://archive.org" + href
            return href
    return None

def extract_lemma_from_filename(fn):
    # Expect pattern like <lemma>_page.html
    m = re.match(r"([a-zA-Z0-9_\-]+)_page\.html", fn)
    return m.group(1) if m else fn

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
            item = find_archive_item(html)
            lemma = extract_lemma_from_filename(fn)
            results.append({"filename": fn, "lemma": lemma, "item_url": item})
            print(f"{fn} -> {item}")
        except Exception as e:
            print(f"Error parsing {fn}: {e}")
    with open("archive_links.json", "w", encoding="utf-8") as out:
        json.dump(results, out, ensure_ascii=False, indent=2)
    print("Saved archive_links.json")

if __name__ == "__main__":
    main()
