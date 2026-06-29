"""
Siemens Press Intelligence — Scraper
=====================================
Fixed version:
  - No ScraperAPI (was blocked on Siemens network)
  - Correct URL:  press.siemens.com/global/en/pressreleases?page=N
  - Accurate date: reads <time datetime="..."> attribute directly
  - Per-article date (not page-level walking which grabbed wrong dates)
  - Session with realistic Chrome headers + cookie warm-up
  - Retry + rate-limit handling
  - Debug mode to diagnose HTML structure if site changes
"""

import requests
from bs4 import BeautifulSoup
import re, time, warnings
from datetime import datetime

warnings.filterwarnings("ignore")

BASE_URL = "https://press.siemens.com"

# ── Correct listing URL (sorted newest first) ──────────────────
# ?page=0 → page 1, ?page=1 → page 2, etc.  (~10 articles per page)
LISTING_URL = "https://press.siemens.com/global/en/pressreleases"

# ── Realistic Chrome 124 headers ───────────────────────────────
HEADERS = {
    "User-Agent":                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                 "AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/124.0.0.0 Safari/537.36",
    "Accept":                    "text/html,application/xhtml+xml,application/xml;"
                                 "q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language":           "en-US,en;q=0.9",
    "Accept-Encoding":           "gzip, deflate, br",
    "Connection":                "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest":            "document",
    "Sec-Fetch-Mode":            "navigate",
    "Sec-Fetch-Site":            "same-origin",
    "Sec-Ch-Ua":                 '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    "Sec-Ch-Ua-Mobile":          "?0",
    "Sec-Ch-Ua-Platform":        '"Windows"',
    "Cache-Control":             "max-age=0",
}

SESSION = requests.Session()
SESSION.headers.update(HEADERS)


# ══════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════

def _warm_up_session():
    """Visit the homepage once to get cookies (avoids bot-detection on first hit)."""
    try:
        SESSION.get(f"{BASE_URL}/global/en", verify=False, timeout=20)
        time.sleep(1)
    except Exception:
        pass


def _parse_datetime_attr(dt_str):
    """
    Parse ISO datetime attribute → 'DD Month YYYY' string.
    Handles:  2025-06-15T00:00:00Z  /  2025-06-15  /  2025-06-15T12:30:00+02:00
    """
    if not dt_str:
        return ""
    dt_str = dt_str.strip()
    for fmt in ("%Y-%m-%dT%H:%M:%SZ",
                "%Y-%m-%dT%H:%M:%S+00:00",
                "%Y-%m-%dT%H:%M:%S%z",
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%d"):
        try:
            dt = datetime.strptime(dt_str[:19].rstrip("Z"), fmt.rstrip("Z").replace("%z",""))
            return dt.strftime("%-d %B %Y")          # "15 June 2025"
        except Exception:
            pass
    # Last resort: already human-readable
    if re.search(r'[A-Za-z]', dt_str):
        return dt_str
    return dt_str


def _extract_date_from_element(el):
    """
    Look for a date INSIDE a single article element only.
    Priority: <time datetime=...>  →  visible text patterns
    """
    # 1. <time datetime="...">  ← most reliable on Drupal sites
    time_tag = el.find("time")
    if time_tag:
        dt_attr = time_tag.get("datetime", "")
        if dt_attr:
            parsed = _parse_datetime_attr(dt_attr)
            if parsed:
                return parsed
        # Fallback: visible text of <time> element
        txt = time_tag.get_text(strip=True)
        if txt:
            return txt

    # 2. Date-class divs / spans
    for cls_hint in ["date", "releasedate", "press-date", "field--name-field-press-releasedate",
                     "field-press-releasedate", "created", "submitted", "publication"]:
        node = el.find(class_=re.compile(cls_hint, re.I))
        if node:
            txt = node.get_text(strip=True)
            if txt:
                return txt

    # 3. Regex on the element text — only within THIS element (tight scope)
    text = el.get_text(" ", strip=True)
    # "15 June 2025" or "June 15, 2025" or "15 Jun 2025"
    m = re.search(
        r'\b(\d{1,2}\s+(?:January|February|March|April|May|June|July|'
        r'August|September|October|November|December)\s+\d{4})\b'
        r'|\b((?:January|February|March|April|May|June|July|'
        r'August|September|October|November|December)\s+\d{1,2},?\s+\d{4})\b'
        r'|\b(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4})\b',
        text, re.IGNORECASE
    )
    if m:
        return m.group()

    return ""


def fetch_page(url, retries=3):
    for attempt in range(1, retries + 1):
        try:
            r = SESSION.get(url, verify=False, timeout=45)
            print(f"    [HTTP {r.status_code}] {url}")
            if r.status_code == 200:
                return r.text
            elif r.status_code in (403, 429):
                wait = 8 * attempt
                print(f"    ⚠️  {r.status_code} — waiting {wait}s before retry {attempt}/{retries}")
                time.sleep(wait)
            else:
                print(f"    ❌ HTTP {r.status_code} — skipping")
                return None
        except requests.exceptions.Timeout:
            print(f"    ⏰ Timeout (attempt {attempt}/{retries}) — retrying...")
            time.sleep(4)
        except Exception as e:
            print(f"    ❌ {type(e).__name__}: {e}")
            time.sleep(3)
    return None


# ══════════════════════════════════════════════════════════════
# CORE PARSERS
# ══════════════════════════════════════════════════════════════

def parse_listing(html, debug=False):
    """
    Parse one listing page → list of article dicts.
    Tries multiple selector strategies to handle site HTML variations.
    """
    soup = BeautifulSoup(html, "html.parser")
    articles = []
    seen_urls = set()

    if debug:
        print(f"    [DEBUG] Page title: {soup.title.string if soup.title else 'N/A'}")

    # ── Strategy A: Drupal article nodes (most reliable) ─────
    # Drupal renders each press release as <article class="node--type-...">
    article_nodes = soup.find_all("article")
    if debug:
        print(f"    [DEBUG] <article> tags found: {len(article_nodes)}")

    for art in article_nodes:
        # Title link
        title_tag = (
            art.find("h3") or art.find("h2") or art.find("h4")
        )
        link_tag = title_tag.find("a") if title_tag else art.find("a", href=True)
        if not link_tag:
            continue

        href  = link_tag.get("href", "")
        title = link_tag.get_text(strip=True)
        if not title or len(title) < 8 or href in seen_urls:
            continue
        seen_urls.add(href)

        full_url = BASE_URL + href if href.startswith("/") else href
        date     = _extract_date_from_element(art)

        # Snippet / teaser text
        teaser = ""
        for cls in ["field--name-body", "field--name-field-teaser",
                    "views-field-body", "teaser", "summary"]:
            node = art.find(class_=re.compile(cls, re.I))
            if node:
                teaser = node.get_text(strip=True)
                break

        articles.append({
            "title":   title,
            "url":     full_url,
            "date":    date,
            "body":    teaser,
            "pdf_url": ""
        })

    # ── Strategy B: /pressrelease/ links if no articles found ─
    if not articles:
        if debug:
            print("    [DEBUG] Strategy A found nothing — trying /pressrelease/ links")
        links = soup.find_all("a", href=lambda x: x and "/pressrelease/" in str(x))
        if debug:
            print(f"    [DEBUG] /pressrelease/ links: {len(links)}")

        for link in links:
            href  = link.get("href", "")
            title = link.get_text(strip=True)
            if not title or len(title) < 8 or href in seen_urls:
                continue
            seen_urls.add(href)

            full_url = BASE_URL + href if href.startswith("/") else href

            # Climb to nearest container for date
            container = (
                link.find_parent("article") or
                link.find_parent("li") or
                link.find_parent("div", class_=re.compile(r'views-row|item|result', re.I))
            )
            date = _extract_date_from_element(container) if container else ""

            articles.append({
                "title":   title,
                "url":     full_url,
                "date":    date,
                "body":    "",
                "pdf_url": ""
            })

    # ── Strategy C: h3/h2 links as last resort ────────────────
    if not articles:
        if debug:
            print("    [DEBUG] Strategy B found nothing — trying h3/h2 headings")
        for heading in soup.find_all(["h2", "h3"]):
            a = heading.find("a", href=True)
            if not a:
                continue
            href  = a.get("href", "")
            title = a.get_text(strip=True)
            if not title or len(title) < 8 or href in seen_urls:
                continue
            seen_urls.add(href)
            full_url = BASE_URL + href if href.startswith("/") else href
            container = heading.find_parent("li") or heading.find_parent("div")
            date = _extract_date_from_element(container) if container else ""
            articles.append({
                "title":   title,
                "url":     full_url,
                "date":    date,
                "body":    "",
                "pdf_url": ""
            })

    if debug and not articles:
        print("    [DEBUG] All strategies failed. First 500 chars of HTML:")
        print(html[:500])

    return articles


# ══════════════════════════════════════════════════════════════
# PUBLIC API
# ══════════════════════════════════════════════════════════════

def get_press_releases(max_pages=2, debug=False):
    """
    Scrape Siemens press releases — newest first.

    Args:
        max_pages: Number of listing pages to scrape (~10 articles each).
        debug:     Print detailed HTML diagnostics if True.

    Returns:
        List of dicts: title, url, date, body, pdf_url
    """
    print(f"\n  🌐 Target: {LISTING_URL}")
    print(f"  📄 Pages to scrape: {max_pages}  (~{max_pages * 10} articles)\n")

    _warm_up_session()
    all_articles = []

    for page_num in range(max_pages):
        # Page 0 = first page (no ?page= param needed, but adding it is harmless)
        if page_num == 0:
            url = LISTING_URL
        else:
            url = f"{LISTING_URL}?page={page_num}"

        print(f"  ── Page {page_num + 1}/{max_pages} ──")
        html = fetch_page(url)

        if not html:
            print(f"  ❌ Page {page_num + 1} failed — stopping early")
            break

        batch = parse_listing(html, debug=debug)
        print(f"     ✅ Found {len(batch)} articles on this page")

        if batch:
            # Print first 3 to verify correctness
            for a in batch[:3]:
                print(f"        • [{a['date'] or 'no date'}] {a['title'][:65]}")

        all_articles.extend(batch)

        if page_num < max_pages - 1:
            time.sleep(2)   # polite delay between pages

    # Deduplicate by URL (safety net)
    seen, unique = set(), []
    for a in all_articles:
        if a["url"] not in seen:
            seen.add(a["url"])
            unique.append(a)

    print(f"\n  📊 Total unique articles: {len(unique)}")
    return unique


def scrape_article_content(url):
    """Fetch and return the main body text of a single press release."""
    html = fetch_page(url)
    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    # Drupal field selectors — try most specific first
    content = (
        soup.find("div", class_=re.compile(r"field--name-body|field--type-text-with-summary", re.I)) or
        soup.find("div", class_=re.compile(r"field--name-field-teaser", re.I)) or
        soup.find("article") or
        soup.find("main")
    )

    if content:
        body = content.get_text("\n", strip=True)
    else:
        body = soup.get_text("\n", strip=True)

    # Clean up excessive whitespace
    body = re.sub(r'\n{3,}', '\n\n', body)
    return body[:3000]
