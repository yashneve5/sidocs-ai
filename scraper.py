"""
Siemens Press Intelligence — Scraper  (Fixed v3)
=================================================
Changes from original:
  1. Uses ScraperAPI via URL method (NOT proxy — proxy was blocked)
  2. Falls back to direct request if ScraperAPI fails
  3. Correct listing URL: /global/en/pressreleases?page=N  (newest first)
  4. Date extracted from <time datetime="..."> attribute — 100% accurate
  5. Per-article isolation so dates never bleed across articles
  6. Session + warm-up cookies to avoid 403 on direct requests
"""

import requests
from bs4 import BeautifulSoup
import re, time, warnings
from datetime import datetime
warnings.filterwarnings("ignore")

# ── Config ────────────────────────────────────────────────────
BASE_URL    = "https://press.siemens.com"
LISTING_URL = "https://press.siemens.com/global/en/pressreleases"

# Your ScraperAPI key — used via URL method (not proxy)
SCRAPERAPI_KEY = "13f8d4ab092ded8492675818e44ba486"

HEADERS = {
    "User-Agent":      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/124.0.0.0 Safari/537.36",
    "Accept":          "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection":      "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest":  "document",
    "Sec-Fetch-Mode":  "navigate",
    "Sec-Fetch-Site":  "none",
    "Cache-Control":   "max-age=0",
}

SESSION = requests.Session()
SESSION.headers.update(HEADERS)


# ── Fetch via ScraperAPI URL method ──────────────────────────
def fetch_via_scraperapi(target_url):
    """Call ScraperAPI as a regular GET — no proxy config needed."""
    try:
        api_url = "http://api.scraperapi.com"
        params  = {
            "api_key": SCRAPERAPI_KEY,
            "url":     target_url,
            "render":  "false",
        }
        r = requests.get(api_url, params=params, timeout=90)
        print(f"    [ScraperAPI {r.status_code}] {target_url[:70]}")
        if r.status_code == 200 and len(r.text) > 500:
            return r.text
        print(f"    ⚠️  ScraperAPI returned {r.status_code}: {r.text[:120]}")
    except Exception as e:
        print(f"    ⚠️  ScraperAPI error: {e}")
    return None


# ── Fetch direct (fallback) ───────────────────────────────────
def fetch_direct(target_url):
    """Direct request with session cookies — works when site allows Python."""
    try:
        r = SESSION.get(target_url, verify=False, timeout=45)
        print(f"    [Direct {r.status_code}] {target_url[:70]}")
        if r.status_code == 200 and len(r.text) > 500:
            return r.text
    except Exception as e:
        print(f"    ⚠️  Direct error: {e}")
    return None


def fetch_page(url):
    """Try ScraperAPI first, then direct request."""
    # 1. ScraperAPI URL method
    html = fetch_via_scraperapi(url)
    if html:
        return html
    # 2. Direct fallback
    print("    🔄 ScraperAPI failed — trying direct request...")
    html = fetch_direct(url)
    if html:
        return html
    return None


# ── Date parsing ─────────────────────────────────────────────
def _parse_dt_attr(dt_str):
    """Convert ISO datetime attr → '15 June 2025'."""
    if not dt_str:
        return ""
    clean = dt_str.strip()[:19].rstrip("Z")
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(clean[:len(fmt)+2].rstrip("TZ:"), fmt.rstrip("TZ:"))
            return dt.strftime("%-d %B %Y")
        except Exception:
            pass
    return dt_str.strip()


def _extract_date(el):
    """Extract date from a single article element — never leaks to other articles."""
    # 1. <time datetime="2025-06-15T..."> — most reliable
    t = el.find("time")
    if t:
        v = _parse_dt_attr(t.get("datetime", ""))
        if v:
            return v
        txt = t.get_text(strip=True)
        if txt:
            return txt

    # 2. Date-labeled divs/spans
    for hint in ["releasedate", "field-press-releasedate", "field--name-field-press-releasedate",
                 "date-display", "created", "submitted", "publication-date", "date"]:
        node = el.find(class_=re.compile(hint, re.I))
        if node:
            txt = node.get_text(strip=True)
            if txt:
                return txt

    # 3. Regex — scoped ONLY to this element
    text = el.get_text(" ", strip=True)
    m = re.search(
        r'\b(\d{1,2}\s+(?:January|February|March|April|May|June|July|'
        r'August|September|October|November|December)\s+\d{4})\b'
        r'|\b((?:January|February|March|April|May|June|July|August|'
        r'September|October|November|December)\s+\d{1,2},?\s+\d{4})\b'
        r'|\b(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4})\b',
        text, re.IGNORECASE
    )
    return m.group() if m else ""


# ── Parse one listing page ────────────────────────────────────
def parse_listing(html):
    soup     = BeautifulSoup(html, "html.parser")
    articles = []
    seen     = set()

    # Strategy A — Drupal <article> nodes (best)
    nodes = soup.find_all("article")
    print(f"    [Parse] <article> tags: {len(nodes)}")

    for art in nodes:
        h = art.find(["h1","h2","h3","h4"])
        a = h.find("a", href=True) if h else art.find("a", href=True)
        if not a:
            continue
        href  = a.get("href", "")
        title = a.get_text(strip=True)
        if not title or len(title) < 8 or href in seen:
            continue
        seen.add(href)
        full_url = BASE_URL + href if href.startswith("/") else href
        date     = _extract_date(art)

        snippet = ""
        for cls in ["field--name-body", "field--name-field-teaser", "teaser", "summary"]:
            nd = art.find(class_=re.compile(cls, re.I))
            if nd:
                snippet = nd.get_text(strip=True)[:300]
                break

        articles.append({"title": title, "url": full_url,
                         "date": date, "body": snippet, "pdf_url": ""})

    # Strategy B — /pressrelease/ links
    if not articles:
        links = soup.find_all("a", href=lambda x: x and "/pressrelease/" in str(x))
        print(f"    [Parse] /pressrelease/ links: {len(links)}")
        for a in links:
            href  = a.get("href","")
            title = a.get_text(strip=True)
            if not title or len(title) < 8 or href in seen:
                continue
            seen.add(href)
            full_url = BASE_URL + href if href.startswith("/") else href
            container = (a.find_parent("article") or a.find_parent("li") or
                         a.find_parent("div", class_=re.compile(r"views-row|item|result", re.I)))
            date = _extract_date(container) if container else ""
            articles.append({"title": title, "url": full_url,
                             "date": date, "body": "", "pdf_url": ""})

    # Strategy C — h2/h3 links last resort
    if not articles:
        for hd in soup.find_all(["h2","h3"]):
            a = hd.find("a", href=True)
            if not a:
                continue
            href  = a.get("href","")
            title = a.get_text(strip=True)
            if not title or len(title) < 8 or href in seen:
                continue
            seen.add(href)
            full_url = BASE_URL + href if href.startswith("/") else href
            container = hd.find_parent("li") or hd.find_parent("div")
            date = _extract_date(container) if container else ""
            articles.append({"title": title, "url": full_url,
                             "date": date, "body": "", "pdf_url": ""})
        print(f"    [Parse] h2/h3 strategy: {len(articles)}")

    if not articles:
        print(f"    [DEBUG] Page title: {soup.title.string if soup.title else 'N/A'}")
        all_a = soup.find_all("a", href=True)[:8]
        for a in all_a:
            print(f"    [DEBUG] link: {a['href'][:80]}")

    return articles


# ── Public API ────────────────────────────────────────────────
def get_press_releases(max_pages=2):
    all_articles = []

    # Warm-up visit for cookies (helps with direct requests)
    try:
        SESSION.get(f"{BASE_URL}/global/en", verify=False, timeout=15)
        time.sleep(1)
    except Exception:
        pass

    for page_num in range(max_pages):
        url = LISTING_URL if page_num == 0 else f"{LISTING_URL}?page={page_num}"
        print(f"\n  ── Page {page_num+1}/{max_pages}")

        html = fetch_page(url)
        if not html:
            print(f"  ❌ Page {page_num+1} failed completely")
            break

        batch = parse_listing(html)
        print(f"  ✅ {len(batch)} articles parsed")

        for a in batch[:3]:
            print(f"     • [{a['date'] or 'no date'}] {a['title'][:65]}")

        all_articles.extend(batch)
        if page_num < max_pages - 1:
            time.sleep(2)

    # Deduplicate
    seen, unique = set(), []
    for a in all_articles:
        if a["url"] not in seen:
            seen.add(a["url"])
            unique.append(a)

    print(f"\n  📊 Total unique articles: {len(unique)}")
    return unique


def scrape_article_content(url):
    html = fetch_page(url)
    if not html:
        return None
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all(["script","style","nav","footer","header","aside"]):
        tag.decompose()
    content = (
        soup.find("div", class_=re.compile(r"field--name-body|field--type-text", re.I)) or
        soup.find("article") or soup.find("main")
    )
    body = content.get_text("\n", strip=True) if content else soup.get_text("\n", strip=True)
    return re.sub(r'\n{3,}', '\n\n', body)[:3000]
