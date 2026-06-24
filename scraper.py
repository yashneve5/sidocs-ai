import requests
import streamlit as st
from bs4 import BeautifulSoup
import re, time, warnings
warnings.filterwarnings("ignore")

BASE_URL   = "https://press.siemens.com"
SEARCH_URL = "https://press.siemens.com/global/en/press-search?f%5B0%5D=content_type:c2_ct_press_release"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

# ✅ Paste your ScraperAPI key here
SCRAPERAPI_KEY = st.secrets.get("SCRAPERAPI_KEY", "13f8d4ab092ded8492675818e44ba486")

def get_proxies():
    return {
        "http":  f"http://scraperapi:{SCRAPERAPI_KEY}@proxy-server.scraperapi.com:8001",
        "https": f"http://scraperapi:{SCRAPERAPI_KEY}@proxy-server.scraperapi.com:8001",
    }

def fetch_page(url):
    try:
        r = requests.get(url, headers=HEADERS, proxies=get_proxies(), verify=False, timeout=60)
        return r.text if r.status_code == 200 else None
    except Exception as e:
        print(f"  ❌ Fetch error: {e}")
        return None

def parse_listing(html):
    soup  = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a", href=lambda x: x and "/pressrelease/" in x)
    seen, articles = set(), []

    for link in links:
        href = link.get("href", "")
        if href in seen: continue
        seen.add(href)

        title = link.get_text(strip=True)
        if not title or len(title) < 10: continue

        full_url = BASE_URL + href if href.startswith("/") else href

        # Find date
        date_text = ""
        parent = link.find_parent()
        for _ in range(8):
            if parent is None: break
            m = re.search(r'\d{1,2}\s+\w+\s+\d{4}', parent.get_text(" ", strip=True))
            if m:
                date_text = m.group()
                break
            parent = parent.find_parent()

        # Bullet summary from listing
        snippet = ""
        p = link.find_parent("div") or link.find_parent("article")
        if p:
            bullets = p.find_all("li")
            if bullets:
                snippet = " ".join(b.get_text(strip=True) for b in bullets[:3])

        articles.append({"title": title, "url": full_url, "date": date_text, "body": snippet})

    return articles

def get_press_releases(max_pages=2):
    all_articles = []
    for page_num in range(max_pages):
        url = f"{SEARCH_URL}&sort_by=field_press_releasedate&page={page_num}"
        print(f"  📄 Page {page_num+1}/{max_pages} → {url}")
        html = fetch_page(url)
        if not html:
            print("  ❌ Failed — check your ScraperAPI key")
            break
        batch = parse_listing(html)
        print(f"     Found {len(batch)} articles")
        all_articles.extend(batch)
        time.sleep(2)
    return all_articles

def scrape_article_content(url):
    html = fetch_page(url)
    if not html: return None
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all(["script","style","nav","footer","header"]):
        tag.decompose()
    content = (
        soup.find("div", class_=lambda x: x and "field--type-text" in str(x)) or
        soup.find("article") or soup.find("main")
    )
    body = content.get_text("\n", strip=True) if content else soup.get_text("\n", strip=True)
    return body[:3000]
