import requests
from bs4 import BeautifulSoup
import re, time, warnings
import streamlit as st

warnings.filterwarnings("ignore")

# ── Configuration ────────────────────────────────────────────
BASE_URL   = "https://press.siemens.com"
SEARCH_URL = "https://press.siemens.com/global/en/press-search?f%5B0%5D=content_type:c2_ct_press_release"

HEADERS = {
    "User-Agent":      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept":          "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

# ── ScraperAPI Key ───────────────────────────────────────────
# Option 1: Loaded from Streamlit secrets (recommended for deployment)
#   → Create .streamlit/secrets.toml and add:
#     SCRAPERAPI_KEY = "your_key_here"
#
# Option 2: Hardcoded fallback (for local testing only)
#   → Replace the string below with your actual key

try:
    SCRAPERAPI_KEY = st.secrets["SCRAPERAPI_KEY"]
except Exception:
    SCRAPERAPI_KEY = "d8bb1b231a688b238276eb5f10c48f6f"  # ← Replace with your key


# ── Proxy ────────────────────────────────────────────────────
def get_proxies():
    return {
        "http":  f"http://scraperapi:{SCRAPERAPI_KEY}@proxy-server.scraperapi.com:8001",
        "https": f"http://scraperapi:{SCRAPERAPI_KEY}@proxy-server.scraperapi.com:8001",
    }


# ── Fetch a single page ──────────────────────────────────────
def fetch_page(url):
    try:
        r = requests.get(
            url,
            headers=HEADERS,
            proxies=get_proxies(),
            verify=False,
            timeout=60,
        )
        if r.status_code == 200:
            return r.text
        print(f"  ⚠️  HTTP {r.status_code} for {url}")
        return None
    except Exception as e:
        print(f"  ❌ Fetch error: {e}")
        return None


# ── Parse listing page → article list ───────────────────────
def parse_listing(html):
    soup   = BeautifulSoup(html, "html.parser")
    links  = soup.find_all("a", href=lambda x: x and "/pressrelease/" in x)
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
        parent    = link.find_parent()
        for _ in range(8):
            if parent is None:
                break
            m = re.search(r"\d{1,2}\s+\w+\s+\d{4}", parent.get_text(" ", strip=True))
            if m:
                date_text = m.group()
                break
            parent = parent.find_parent()

        # ── Bullet summary from listing ──
        snippet = ""
        container = link.find_parent("div") or link.find_parent("article")
        if container:
            bullets = container.find_all("li")
            if bullets:
                snippet = " ".join(b.get_text(strip=True) for b in bullets[:3])

        articles.append({
            "title": title,
            "url":   full_url,
            "date":  date_text,
            "body":  snippet,
        })

    return articles


# ── Scrape multiple listing pages ────────────────────────────
def get_press_releases(max_pages=2):
    all_articles = []

    for page_num in range(max_pages):
        url = f"{SEARCH_URL}&sort_by=field_press_releasedate&page={page_num}"
        print(f"  📄 Page {page_num + 1}/{max_pages} → {url}")

        html = fetch_page(url)
        if not html:
            print("  ❌ Failed — check your ScraperAPI key")
            break

        batch = parse_listing(html)
        print(f"     Found {len(batch)} articles")
        all_articles.extend(batch)
        time.sleep(2)

    return all_articles


# ── Scrape full article body ─────────────────────────────────
def scrape_article_content(url):
    html = fetch_page(url)
    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")

    # Remove non-content tags
    for tag in soup.find_all(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    # Find main content block
    content = (
        soup.find("div", class_=lambda x: x and "field--type-text" in str(x))
        or soup.find("article")
        or soup.find("main")
    )

    body = content.get_text("\n", strip=True) if content else soup.get_text("\n", strip=True)
    return body[:3000]
