import requests
from urllib.parse import quote
import time
import json

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; script/1.0)"}
TIMEOUT = 15

LEMMA_LIST = ["dharma", "atman", "yoga", "karma", "guru", "bhakti", "dhyana", "rta", "loka", "manu"]

ENDPOINTS = [
    "https://www.sanskrit-lexicon.uni-koeln.de/scans/MWScan/2014/web/webtc/index.php?lemma={lemma}",
    "https://www.sanskrit-lexicon.uni-koeln.de/scans/",
    "https://en.wikisource.org/wiki/A_Sanskrit-English_Dictionary_(M-W)#{lemma}",
    "https://archive.org/search.php?query=Monier+Williams+{lemma}"
]

def try_url(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
        return r.status_code, r.headers.get("content-type",""), r.text[:1000]
    except Exception as e:
        return None, None, f"ERROR: {e}"

def probe_lemma(lemma):
    results = []
    for pattern in ENDPOINTS:
        url = pattern.format(lemma=quote(lemma))
        status, ctype, snippet = try_url(url)
        results.append({"url": url, "status": status, "content_type": ctype, "snippet_preview": snippet})
        if status == 200 and snippet and len(snippet) > 200:
            break
        time.sleep(0.5)
    return results

def main():
    all_results = {}
    for lemma in LEMMA_LIST:
        res = probe_lemma(lemma)
        all_results[lemma] = res
        print(f"\n=== {lemma} ===")
        for r in res:
            preview = r['snippet_preview'].replace("\n"," ")[:200]
            print(f"{r['url']}  status={r['status']}  preview={preview!r}")
        ok = next((r for r in res if r['status']==200 and len(r['snippet_preview'])>200), None)
        if ok:
            fname = f"{lemma}_page.html"
            print(f"Saving successful page to {fname}")
            rr = requests.get(ok['url'], headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
            open(fname, "wb").write(rr.content)
    with open("probe_results.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    print("\nSaved probe_results.json")

if __name__ == "__main__":
    main()
