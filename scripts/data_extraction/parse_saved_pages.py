import glob
import json
from bs4 import BeautifulSoup

def extract_from_archive_search(html):
    soup = BeautifulSoup(html, "html.parser")
    # Try to find first result link (common Archive patterns)
    a = soup.select_one("a[href*='/details/'], a.result-title, a[itemprop='url']")
    link = a.get("href") if a else None
    # snippet: first paragraph or meta description
    p = soup.select_one("p")
    snippet = p.get_text(strip=True) if p else ""
    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    return {"title": title, "first_link": link, "snippet": snippet}

def extract_from_generic_html(html):
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.string.strip() if soup.title and soup.title.string else None
    main = soup.find(id="content") or soup.find("main") or soup.find("body")
    text = main.get_text(separator="\n", strip=True) if main else soup.get_text(separator="\n", strip=True)
    snippet = text[:800]
    return {"title": title, "snippet": snippet}

def parse_file(path):
    with open(path, "rb") as f:
        raw = f.read()
    try:
        html = raw.decode("utf-8")
    except:
        try:
            html = raw.decode("latin-1")
        except:
            html = raw.decode("utf-8", errors="ignore")
    lower = html.lower()
    if "archive.org" in lower or "archive" in path.lower():
        return extract_from_archive_search(html)
    else:
        return extract_from_generic_html(html)

def main():
    files = glob.glob("*_page.html") + glob.glob("*.htm") + glob.glob("*.html")
    results = []
    for fn in files:
        try:
            info = parse_file(fn)
            results.append({
                "filename": fn,
                "title": info.get("title"),
                "first_link": info.get("first_link"),
                "snippet": info.get("snippet")
            })
            print(f"Parsed {fn}: title={info.get('title')!r}")
        except Exception as e:
            print(f"Error parsing {fn}: {e}")
    with open("parsed_pages.json", "w", encoding="utf-8") as out:
        json.dump(results, out, ensure_ascii=False, indent=2)
    print(f"Saved {len(results)} records to parsed_pages.json")

if __name__ == "__main__":
    main()
