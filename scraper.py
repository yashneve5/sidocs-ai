"""
scraper.py — Siemens Press Intelligence
Fixed with 3 strategies:
  1. Direct fetch (works when running locally / on Siemens network)
  2. ScraperAPI proxy (works when key is valid + domain is allowed)
  3. RSS/API fallback
"""

import requests
from bs4 import BeautifulSoup
import re, time, warnings
warnings.filterwarnings("ignore")

# ── Config ───────────────────────────────────────────────────
BASE_URL   = "https://press.siemens.com"
SEARCH_URL = "https://press.siemens.com/global/en/press-search?f%5B0%5D=content_type:c2_ct_press_release"

# ✅ Paste your ScraperAPI key here
# Get one FREE at: https://www.scraperapi.com (5000 free requests/month)
SCRAPERAPI_KEY = "13f8d4ab092ded8492675818e44ba486"

HEADERS = {
    "User-Agent":                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept":                    "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language":           "en-US,en;q=0.9",
    "Accept-Encoding":           "gzip, deflate, br",
    "Connection":                "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest":            "document",
    "Sec-Fetch-Mode":            "navigate",
    "Sec-Fetch-Site":            "none",
    "Cache-Control":             "max-age=0",
}


# ── Strategy 1: Direct fetch ──────────────────────────────────
def fetch_direct(url, session=None):
    """Fetch without proxy — works on local machine or Siemens internal network."""
    try:
        caller = session or requests
        r = caller.get(url, headers=HEADERS, verify=False, timeout=30)
        if r.status_code == 200 and len(r.text) > 500:
            return r.text
        print(f"    ⚠ Direct fetch: HTTP {r.status_code}")
        return None
    except Exception as e:
        print(f"    ⚠ Direct fetch error: {e}")
        return None


# ── Strategy 2: ScraperAPI proxy ─────────────────────────────
def fetch_via_scraperapi(url):
    """Route through ScraperAPI — handles JS rendering + bot detection."""
    try:
        # Method A: proxy URL
        proxies = {
            "http":  f"http://scraperapi:{SCRAPERAPI_KEY}@proxy-server.scraperapi.com:8001",
            "https": f"http://scraperapi:{SCRAPERAPI_KEY}@proxy-server.scraperapi.com:8001",
        }
        r = requests.get(url, headers=HEADERS, proxies=proxies, verify=False, timeout=60)
        if r.status_code == 200 and len(r.text) > 500:
            return r.text
        print(f"    ⚠ ScraperAPI proxy: HTTP {r.status_code}")
    except Exception as e:
        print(f"    ⚠ ScraperAPI proxy error: {e}")

    try:
        # Method B: ScraperAPI GET endpoint
        api_url = "https://api.scraperapi.com/"
        params  = {"api_key": SCRAPERAPI_KEY, "url": url, "render": "false"}
        r = requests.get(api_url, params=params, timeout=60)
        if r.status_code == 200 and len(r.text) > 500:
            return r.text
        print(f"    ⚠ ScraperAPI endpoint: HTTP {r.status_code} — {r.text[:100]}")
    except Exception as e:
        print(f"    ⚠ ScraperAPI endpoint error: {e}")

    return None


# ── Strategy 3: RSS feed fallback ────────────────────────────
def fetch_via_rss():
    """
    Pull from Siemens press RSS feeds — no key needed, lightweight XML.
    Returns articles list directly (bypasses HTML parsing).
    """
    rss_urls = [
        "https://press.siemens.com/global/en/pressrelease/rss.xml",
        "https://press.siemens.com/global/en/news/rss.xml",
        "https://www.siemens.com/rss/press-releases/en.rss",
    ]
    articles = []
    for rss in rss_urls:
        try:
            r = requests.get(rss, headers=HEADERS, verify=False, timeout=20)
            if r.status_code != 200:
                continue
            soup = BeautifulSoup(r.text, "xml")
            items = soup.find_all("item")
            if not items:
                items = soup.find_all("entry")
            for item in items:
                title = (item.find("title") or {}).get_text(strip=True) if item.find("title") else ""
                url   = ""
                link  = item.find("link")
                if link:
                    url = link.get_text(strip=True) or link.get("href", "")
                pub  = item.find("pubDate") or item.find("published") or item.find("updated")
                dstr = pub.get_text(strip=True) if pub else ""
                desc = item.find("description") or item.find("summary")
                body = desc.get_text(strip=True)[:500] if desc else ""
                if title and url:
                    articles.append({"title": title, "url": url, "date": dstr, "body": body})
            if articles:
                print(f"    ✅ RSS feed: {len(articles)} articles from {rss}")
                return articles
        except Exception as e:
            print(f"    ⚠ RSS error ({rss}): {e}")
    return []


# ── Master fetch with auto-fallback ──────────────────────────
_session = None

def fetch_page(url):
    """
    Try direct → ScraperAPI → return None.
    Maintains a session for cookie handling.
    """
    global _session
    if _session is None:
        _session = requests.Session()
        # Warm up session with homepage
        try:
            _session.get(BASE_URL, headers=HEADERS, verify=False, timeout=15)
        except Exception:
            pass

    # 1. Direct fetch
    html = fetch_direct(url, session=_session)
    if html:
        return html

    # 2. ScraperAPI
    print("    ↩ Direct failed — trying ScraperAPI...")
    html = fetch_via_scraperapi(url)
    if html:
        return html

    print("    ❌ All fetch strategies failed for:", url)
    return None


# ── Parse listing page ───────────────────────────────────────
def parse_listing(html):
    soup  = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a", href=lambda x: x and "/pressrelease/" in x)
    seen, articles = set(), []

    for link in links:
        href = link.get("href", "")
        if href in seen:
            continue
        seen.add(href)

        title = link.get_text(strip=True)
        if not title or len(title) < 10:
            continue

        full_url = BASE_URL + href if href.startswith("/") else href

        # ── Find nearest date ──
        date_text = ""
        parent = link.find_parent()
        for _ in range(8):
            if parent is None:
                break
            m = re.search(r"\d{1,2}\s+\w+\s+\d{4}", parent.get_text(" ", strip=True))
            if m:
                date_text = m.group()
                break
            parent = parent.find_parent()

        # ── Bullet snippet ──
        snippet = ""
        container = link.find_parent("div") or link.find_parent("article")
        if container:
            bullets = container.find_all("li")
            if bullets:
                snippet = " ".join(b.get_text(strip=True) for b in bullets[:3])

        articles.append({"title": title, "url": full_url, "date": date_text, "body": snippet})

    return articles


# ── Main entry point ─────────────────────────────────────────
def get_press_releases(max_pages=1):
    """
    Scrape up to max_pages of Siemens press releases.
    Auto-falls back to RSS if HTML scraping fails.
    """
    all_articles = []

    for page_num in range(max_pages):
        url = f"{SEARCH_URL}&sort_by=field_press_releasedate&page={page_num}"
        print(f"  📄 Page {page_num + 1}/{max_pages}")
        print(f"     URL: {url}")

        html = fetch_page(url)

        if not html:
            # Last resort: RSS feed
            print("  ↩ HTML scraping failed — trying RSS feed fallback...")
            rss_articles = fetch_via_rss()
            if rss_articles:
                all_articles.extend(rss_articles)
                print(f"  ✅ RSS fallback: {len(rss_articles)} articles loaded")
            else:
                print("  ❌ All methods failed.")
                print("  ─────────────────────────────────────────")
                print("  FIX OPTIONS:")
                print("  1. Run app on your LOCAL machine (not cloud)")
                print("  2. Get a new ScraperAPI key → scraperapi.com")
                print("  3. Check ScraperAPI dashboard for usage limits")
                print("  4. Your Siemens network may block outbound proxies")
                print("  ─────────────────────────────────────────")
            break

        batch = parse_listing(html)
        print(f"     Found {len(batch)} articles")

        if not batch and page_num == 0:
            # Page fetched but no articles parsed — try RSS
            print("  ↩ Page fetched but no articles found — trying RSS fallback...")
            rss_articles = fetch_via_rss()
            if rss_articles:
                all_articles.extend(rss_articles)
                print(f"  ✅ RSS fallback: {len(rss_articles)} articles")
                break

        all_articles.extend(batch)
        if page_num < max_pages - 1:
            time.sleep(2)

    return all_articles


# ── Scrape full article body ──────────────────────────────────
def scrape_article_content(url):
    html = fetch_page(url)
    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    content = (
        soup.find("div", class_=lambda x: x and "field--type-text" in str(x))
        or soup.find("article")
        or soup.find("main")
    )

    body = content.get_text("\n", strip=True) if content else soup.get_text("\n", strip=True)
    return body[:3000]


# ── Quick test when run directly ─────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("  SiDocs AI — Scraper Diagnostics")
    print("=" * 55)
    articles = get_press_releases(max_pages=1)
    print(f"\nResult: {len(articles)} articles")
    for a in articles[:3]:
        print(f"  • [{a.get('date','?')}] {a.get('title','')[:70]}")
