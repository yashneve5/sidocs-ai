import requests
from bs4 import BeautifulSoup
import re, time, warnings
warnings.filterwarnings("ignore")

BASE_URL   = "https://press.siemens.com"
SEARCH_URL = "https://press.siemens.com/global/en/press-search?f%5B0%5D=content_type:c2_ct_press_release"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age=0",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Referer": "https://press.siemens.com/global/en",
}

SESSION = requests.Session()
SESSION.headers.update(HEADERS)


def fetch_page(url, retries=3):
    for attempt in range(retries):
        try:
            r = SESSION.get(url, verify=False, timeout=45)
            print(f"    [HTTP {r.status_code}] {url[:80]}")
            if r.status_code == 200:
                return r.text
            elif r.status_code == 403:
                print(f"    ⚠️  403 Forbidden — site may be blocking scrapers. Retrying in 5s...")
                time.sleep(5)
            elif r.status_code == 429:
                print(f"    ⚠️  Rate limited. Waiting 10s...")
                time.sleep(10)
            else:
                print(f"    ❌ HTTP {r.status_code}")
                return None
        except requests.exceptions.Timeout:
            print(f"    ⏰ Timeout (attempt {attempt+1}/{retries})")
            time.sleep(3)
        except Exception as e:
            print(f"    ❌ Error: {e}")
            time.sleep(3)
    return None


def parse_listing(html):
    soup  = BeautifulSoup(html, "html.parser")
    seen, articles = set(), []

    # Strategy 1: links containing /pressrelease/
    links = soup.find_all("a", href=lambda x: x and "/pressrelease/" in x)
    print(f"    Strategy 1 (/pressrelease/ links): {len(links)} found")

    # Strategy 2: fallback — any article/h3 links
    if not links:
        links = []
        for h3 in soup.find_all(["h3", "h2"]):
            a = h3.find("a", href=True)
            if a:
                links.append(a)
        print(f"    Strategy 2 (h3/h2 links): {len(links)} found")

    for link in links:
        href = link.get("href", "")
        if href in seen:
            continue
        seen.add(href)

        title = link.get_text(strip=True)
        if not title or len(title) < 10:
            continue

        full_url = BASE_URL + href if href.startswith("/") else href

        # Find date — walk up parent tree
        date_text = ""
        parent = link.find_parent()
        for _ in range(10):
            if parent is None:
                break
            text = parent.get_text(" ", strip=True)
            # Match "12 June 2024" or "June 12, 2024"
            m = re.search(
                r'\b(\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4})\b'
                r'|\b((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4})\b',
                text, re.IGNORECASE
            )
            if m:
                date_text = m.group()
                break
            # Also try time element
            t = parent.find("time")
            if t:
                date_text = t.get("datetime", "") or t.get_text(strip=True)
                break
            parent = parent.find_parent()

        # Snippet from listing
        snippet = ""
        p = link.find_parent("div") or link.find_parent("article")
        if p:
            bullets = p.find_all("li")
            if bullets:
                snippet = " ".join(b.get_text(strip=True) for b in bullets[:3])
            else:
                # Try paragraph text
                paras = p.find_all("p")
                if paras:
                    snippet = " ".join(para.get_text(strip=True) for para in paras[:2])

        articles.append({
            "title":   title,
            "url":     full_url,
            "date":    date_text,
            "body":    snippet,
            "pdf_url": ""
        })

    return articles


def get_press_releases(max_pages=2):
    all_articles = []

    for page_num in range(max_pages):
        url = f"{SEARCH_URL}&sort_by=field_press_releasedate&page={page_num}"
        print(f"\n  📄 Scraping page {page_num+1}/{max_pages}")
        print(f"     URL: {url}")

        html = fetch_page(url)

        if not html:
            print(f"  ❌ Page {page_num+1} failed — no response")
            # Try alternative URL format
            alt_url = f"https://press.siemens.com/global/en/pressreleases?page={page_num}"
            print(f"  🔄 Trying alternative URL: {alt_url}")
            html = fetch_page(alt_url)

        if not html:
            print(f"  ❌ Both URLs failed for page {page_num+1}")
            break

        # Debug: show page structure
        soup_debug = BeautifulSoup(html, "html.parser")
        all_links_with_press = soup_debug.find_all("a", href=lambda x: x and "press" in str(x).lower())
        print(f"     Total 'press' links on page: {len(all_links_with_press)}")

        batch = parse_listing(html)
        print(f"     ✅ Parsed {len(batch)} articles")

        if batch:
            all_articles.extend(batch)
        else:
            # Debug dump — show what the page actually contains
            print("     ⚠️  No articles parsed. Page title:", soup_debug.title.string if soup_debug.title else "N/A")
            # Show first few links
            all_a = soup_debug.find_all("a", href=True)[:10]
            print("     First 10 hrefs on page:")
            for a in all_a:
                print(f"       {a['href'][:80]}")

        time.sleep(2)

    print(f"\n  📊 Total articles collected: {len(all_articles)}")
    return all_articles


def scrape_article_content(url):
    html = fetch_page(url)
    if not html:
        return None
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    content = (
        soup.find("div", class_=lambda x: x and "field--type-text" in str(x)) or
        soup.find("article") or
        soup.find("main")
    )
    body = content.get_text("\n", strip=True) if content else soup.get_text("\n", strip=True)
    return body[:3000]
