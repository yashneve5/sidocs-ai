"""
Siemens Press Intelligence Report Generator
============================================
Usage:
    python main.py                   # 1 page (~10 articles)
    python main.py --pages 3         # ~30 articles
    python main.py --pages 5 --full  # full content + AI summaries
"""

import argparse
from scraper    import get_press_releases, scrape_article_content
from summarizer import get_ai_summary, detect_category
from save_pdf   import save_to_pdf

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pages", type=int, default=1, help="Pages to scrape (default 1 = ~10 articles)")
    parser.add_argument("--full",  action="store_true",  help="Fetch full article text before summarizing")
    args = parser.parse_args()

    print("=" * 60)
    print("  Siemens Press Intelligence Report")
    print("=" * 60)
    print(f"  Pages   : {args.pages}  (~{args.pages * 10} articles)")
    print(f"  Full    : {args.full}")
    print("=" * 60)

    # ── Step 1: Scrape listing pages ──────────────────────
    print("\n🔍 Step 1: Scraping press release list...")
    articles = get_press_releases(max_pages=args.pages)

    if not articles:
        print("❌ No articles found. Check SCRAPERAPI_KEY in scraper.py")
        return

    print(f"\n✅ Collected {len(articles)} articles")

    # ── Step 2: Optionally fetch full body ────────────────
    if args.full:
        print(f"\n📰 Step 2: Fetching full article content...")
        for i, a in enumerate(articles, 1):
            print(f"  [{i}/{len(articles)}] {a['title'][:60]}...")
            body = scrape_article_content(a["url"])
            if body:
                a["body"] = body
    else:
        print("\n⏭️  Step 2: Skipping full fetch (add --full to enable)")

    # ── Step 3: Detect category + AI summary ─────────────
    print(f"\n🤖 Step 3: Generating AI summaries...")
    for i, a in enumerate(articles, 1):
        print(f"  [{i}/{len(articles)}] Summarising: {a['title'][:55]}...")
        a["category"] = detect_category(a["title"], a["url"], a.get("body", ""))
        a["summary"]  = get_ai_summary(
            title    = a["title"],
            body     = a.get("body", ""),
            date     = a.get("date", ""),
            category = a["category"],
        )

    # ── Step 4: Save PDF ──────────────────────────────────
    print(f"\n💾 Step 4: Building PDF report...")
    out = save_to_pdf(articles, "output/siemens_press_report.pdf")

    print("\n" + "=" * 60)
    print(f"  ✅ Done!  →  {out}")
    print("=" * 60)

if __name__ == "__main__":
    main()
