"""
Download Archive.org item text (if available) and attempt to extract candidate Monier-Williams
headword blocks into a simple JSON structure.

Usage:
  1. Ensure archive_links.json exists (created by extract_archive_links.py).
  2. Install dependencies: pip install requests beautifulsoup4 regex
  3. Run: python archive_to_mw_json.py
  4. Output: mw_candidates.json (array of candidate text blocks per lemma)

Notes:
  - Archive items vary: some provide 'See other formats' -> 'Text' or 'OCR' links.
  - This script tries to find a text/plain or /download/ text link and falls back to the item page.
  - The extraction heuristics are intentionally conservative; tune regexes for your edition.
"""

import json
import requests
from bs4 import BeautifulSoup
import re
import time
from urllib.parse import urljoin

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; script/1.0)"}
TIMEOUT = 20

def load_links():
    with open("archive_links.json", "r", encoding="utf-8") as f:
        return json.load(f)

def fetch_url(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        r.raise_for_status()
        return r
    except Exception as e:
        print(f"Fetch error {url}: {e}")
        return None

def find_text_download(item_url):
    """
    Given an Archive.org item page URL, try to find a direct text/OCR download link.
    """
    r = fetch_url(item_url)
    if not r:
        return None
    soup = BeautifulSoup(r.text, "html.parser")
    # Look for links to /download/<identifier>/<file>
    for a in soup.select("a[href]"):
        href = a['href']
        if re.search(r"/download/.*\.txt$", href) or re.search(r"/download/.*\.txt\?", href):
            return urljoin(item_url, href)
    # Look for 'See other formats' links with text/plain or 'Text' label
    for a in soup.select("a[href]"):
        txt = (a.get_text() or "").lower()
        if "text" in txt or "plain text" in txt:
            return urljoin(item_url, a['href'])
    # Try common pattern: item_url + "/download"
    if item_url.endswith("/"):
        candidate = item_url + "download"
    else:
        candidate = item_url + "/download"
    return candidate

def extract_candidate_blocks(text):
    """
    Heuristic extraction of candidate MW blocks:
    - Look for lines that start with a Devanagari headword or a transliteration followed by punctuation.
    - Return list of short blocks (headword + following 2-6 lines).
    """
    # Normalize line endings
    lines = text.splitlines()
    candidates = []
    for i, ln in enumerate(lines):
        # Heuristic 1: Devanagari headword line (contains Devanagari range)
        if re.search(r"[\u0900-\u097F]{2,}", ln):
            block = "\n".join(lines[i:i+6]).strip()
            candidates.append({"type": "devanagari_head", "block": block})
            continue
        # Heuristic 2: ASCII transliteration headword followed by punctuation or dash
        if re.match(r"^[A-Za-zāīūṛṝḷṅñṭḍṇśṣḥ\-\']{2,}\b.*[:\-–—]", ln):
            block = "\n".join(lines[i:i+6]).strip()
            candidates.append({"type": "translit_head", "block": block})
    # Deduplicate similar blocks
    seen = set()
    uniq = []
    for c in candidates:
        key = c['block'][:120]
        if key not in seen:
            seen.add(key)
            uniq.append(c)
    return uniq

def main():
    links = load_links()
    all_results = []
    for entry in links:
        lemma = entry.get("lemma")
        item_url = entry.get("item_url")
        if not item_url:
            print(f"No item_url for {lemma}, skipping")
            continue
        print(f"Processing {lemma} -> {item_url}")
        text_link = find_text_download(item_url)
        print(f"  text_link candidate: {text_link}")
        # Try to fetch text_link
        r = fetch_url(text_link) if text_link else None
        text = None
        if r and r.status_code == 200 and 'text' in (r.headers.get("content-type","").lower() or ""):
            text = r.text
        else:
            # fallback: try item_url/text or item_url/ocr or item_url/download
            fallback_urls = [item_url + "/text", item_url + "/ocr", item_url + "/download"]
            for fu in fallback_urls:
                rr = fetch_url(fu)
                if rr and rr.status_code == 200 and 'text' in (rr.headers.get("content-type","").lower() or ""):
                    text = rr.text
                    break
        if not text:
            # As last resort, use the item page HTML and extract visible text
            r_item = fetch_url(item_url)
            if r_item:
                soup = BeautifulSoup(r_item.text, "html.parser")
                text = soup.get_text("\n", strip=True)
        if not text:
            print(f"  No text found for {lemma}")
            continue
        # Extract candidate blocks
        candidates = extract_candidate_blocks(text)
        print(f"  Found {len(candidates)} candidate blocks")
        all_results.append({"lemma": lemma, "item_url": item_url, "text_link": text_link, "candidates": candidates})
        # polite pause
        time.sleep(1.0)
    with open("mw_candidates.json", "w", encoding="utf-8") as out:
        json.dump(all_results, out, ensure_ascii=False, indent=2)
    print("Saved mw_candidates.json")

if __name__ == "__main__":
    main()
