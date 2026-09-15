"""
Query Archive.org advanced search API for each lemma, fetch text/OCR if available,
and extract candidate Monier-Williams blocks.

Outputs:
  - archive_api_results.json : list of {lemma, identifier, item_url, text_url, candidates}
  - mw_candidates_api.json : same as above (for convenience)

Notes:
  - The Archive advanced search API: https://archive.org/advancedsearch.php
  - This script queries for items matching the lemma and 'Monier Williams' in title/description.
  - Adjust 'rows' or query string for your needs.
"""

import json
import requests
import time
import re
from urllib.parse import quote, urljoin

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; script/1.0)"}
API_BASE = "https://archive.org/advancedsearch.php"

# Lemmas to search (adjust or load from file)
LEMMA_LIST = ["dharma", "atman", "yoga", "karma", "guru", "bhakti", "dhyana", "rta", "loka", "manu"]

def query_archive_api(lemma, rows=5):
    # Search for items that mention Monier Williams and the lemma
    q = f'(title:(Monier Williams) OR description:(Monier Williams) OR creator:(Monier Williams)) AND ({lemma})'
    params = {
        "q": q,
        "fl": "identifier,title,description",
        "rows": rows,
        "output": "json"
    }
    r = requests.get(API_BASE, params=params, headers=HEADERS, timeout=20)
    r.raise_for_status()
    return r.json()

def find_text_download_url(item_identifier):
    # Try common text file patterns via the item metadata JSON
    meta_url = f"https://archive.org/metadata/{item_identifier}"
    r = requests.get(meta_url, headers=HEADERS, timeout=20)
    if r.status_code != 200:
        return None
    meta = r.json()
    files = meta.get("files", [])
    # Prefer files with 'txt' or 'ocr' in name or format
    for f in files:
        name = f.get("name","").lower()
        fmt = (f.get("format") or "").lower()
        if name.endswith(".txt") or "ocr" in name or fmt == "text":
            return urljoin("https://archive.org", f"/download/{item_identifier}/{f.get('name')}")
    # fallback: try /download/<identifier>/<identifier>_djvu.txt or similar
    for f in files:
        name = f.get("name","").lower()
        if name.endswith(".djvu.txt") or name.endswith(".txt"):
            return urljoin("https://archive.org", f"/download/{item_identifier}/{f.get('name')}")
    return None

def fetch_text_from_url(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=30)
        if r.status_code == 200:
            return r.text
    except Exception:
        return None
    return None

def extract_candidate_blocks(text):
    lines = text.splitlines()
    candidates = []
    for i, ln in enumerate(lines):
        # Devanagari headword heuristic
        if re.search(r"[\u0900-\u097F]{2,}", ln):
            block = "\n".join(lines[i:i+8]).strip()
            candidates.append({"type":"devanagari_head","block":block})
            continue
        # ASCII translit headword heuristic (word followed by punctuation)
        if re.match(r"^[A-Za-zāīūṛṝḷṅñṭḍṇśṣḥ\-\']{2,}.*[:\-–—]", ln):
            block = "\n".join(lines[i:i+8]).strip()
            candidates.append({"type":"translit_head","block":block})
    # dedupe
    seen = set()
    uniq = []
    for c in candidates:
        key = c['block'][:140]
        if key not in seen:
            seen.add(key)
            uniq.append(c)
    return uniq

def main():
    results = []
    for lemma in LEMMA_LIST:
        print(f"Searching Archive for lemma: {lemma}")
        try:
            resp = query_archive_api(lemma, rows=5)
            docs = resp.get("response", {}).get("docs", [])
            if not docs:
                print("  No docs found")
                results.append({"lemma": lemma, "items": []})
                continue
            lemma_items = []
            for d in docs:
                identifier = d.get("identifier")
                title = d.get("title")
                item_url = f"https://archive.org/details/{identifier}"
                print(f"  Found item: {identifier} ({title})")
                text_url = find_text_download_url(identifier)
                text = None
                if text_url:
                    print(f"    text_url: {text_url}")
                    text = fetch_text_from_url(text_url)
                else:
                    print("    No direct text file found; will try metadata text fallback")
                    # try metadata 'ocr' or 'text' fields
                    meta_url = f"https://archive.org/metadata/{identifier}"
                    rmeta = requests.get(meta_url, headers=HEADERS, timeout=20)
                    if rmeta.status_code == 200:
                        meta_text = json.dumps(rmeta.json())
                        # attempt to extract any large text-like field
                        if len(meta_text) > 1000:
                            text = meta_text
                candidates = extract_candidate_blocks(text) if text else []
                lemma_items.append({"identifier": identifier, "item_url": item_url, "text_url": text_url, "candidates": candidates})
                time.sleep(0.5)
            results.append({"lemma": lemma, "items": lemma_items})
        except Exception as e:
            print(f"  Error searching {lemma}: {e}")
            results.append({"lemma": lemma, "items": [], "error": str(e)})
        time.sleep(1.0)
    with open("archive_api_results.json", "w", encoding="utf-8") as out:
        json.dump(results, out, ensure_ascii=False, indent=2)
    # also save a compact candidates file
    candidates_only = [{"lemma": r["lemma"], "items": [{"identifier": it["identifier"], "candidates": it["candidates"]} for it in r.get("items",[])]} for r in results]
    with open("mw_candidates_api.json", "w", encoding="utf-8") as out2:
        json.dump(candidates_only, out2, ensure_ascii=False, indent=2)
    print("Saved archive_api_results.json and mw_candidates_api.json")

if __name__ == "__main__":
    main()
