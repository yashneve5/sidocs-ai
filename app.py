"""
SiDocs AI – Siemens Press Intelligence Dashboard
Matches Siemens Intranet: white cards, teal-gradient nav, light grey bg
"""

import streamlit as st
import pandas as pd
import os, sys, re, io
from datetime import datetime, date
from pathlib import Path

st.set_page_config(
    page_title="SiDocs AI | Press Intelligence",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"], .stApp {
    font-family: 'Inter', 'Segoe UI', sans-serif !important;
    background-color: #eef2f6 !important;
    color: #1a2332 !important;
}

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stSidebar"] { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── NAV ── */
.si-nav {
    background: linear-gradient(90deg, #002244 0%, #004466 55%, #007788 100%);
    padding: 0 36px;
    height: 58px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky; top: 0; z-index: 999;
    border-bottom: 3px solid #00cccc;
}
.si-nav-logo { font-size: 18px; font-weight: 700; color: #fff; letter-spacing: 3px; }
.si-nav-logo span { color: #00cccc; font-weight: 400; font-size: 15px; letter-spacing: 1px; margin-left: 8px; }
.si-nav-right { display: flex; align-items: center; gap: 12px; }
.si-nav-pill {
    background: transparent;
    border: 1.5px solid #00cccc;
    color: #00cccc;
    font-size: 11px; font-weight: 700;
    padding: 4px 14px; border-radius: 20px; letter-spacing: 1.5px;
}
.si-nav-chip {
    background: rgba(255,255,255,0.1);
    color: #cce8ee;
    font-size: 12px; font-weight: 500;
    padding: 5px 14px; border-radius: 6px;
    border: 1px solid rgba(255,255,255,0.15);
}

/* ── HERO ── */
.si-hero {
    background: linear-gradient(130deg, #002244 0%, #004466 55%, #006688 100%);
    padding: 32px 40px 30px 40px;
    color: #fff;
    border-bottom: 4px solid #00aaaa;
}
.si-hero-eyebrow {
    font-size: 11px; font-weight: 700;
    color: #00cccc; letter-spacing: 2px;
    text-transform: uppercase; margin-bottom: 8px;
}
.si-hero-title { font-size: 26px; font-weight: 700; color: #fff; margin-bottom: 6px; line-height: 1.25; }
.si-hero-title span { color: #00cccc; }
.si-hero-sub { font-size: 13px; color: rgba(255,255,255,0.65); max-width: 600px; line-height: 1.6; margin-bottom: 20px; }
.si-hero-stats { display: flex; gap: 36px; }
.si-hero-stat { border-left: 3px solid #00aaaa; padding-left: 14px; }
.si-hero-stat-val { font-size: 24px; font-weight: 700; color: #00dddd; line-height: 1; }
.si-hero-stat-lbl { font-size: 10px; color: rgba(255,255,255,0.5); font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-top: 3px; }

/* ── BODY ── */
.si-body { background: #eef2f6; padding: 28px 36px 40px 36px; }

/* ── WHITE CARD ── */
.si-card {
    background: #ffffff;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
    border: 1px solid #dde4ec;
    overflow: hidden;
    margin-bottom: 20px;
}
.si-card-head {
    padding: 14px 20px 12px 20px;
    border-bottom: 1px solid #eef2f6;
    display: flex; align-items: center; justify-content: space-between;
    background: #f8fafc;
}
.si-card-title { font-size: 13px; font-weight: 700; color: #002244; letter-spacing: 0.2px; }
.si-card-body { padding: 20px; }

/* ── PILLS ── */
.si-pill-teal { background: #e0f7f7; color: #006666; font-size: 10px; font-weight: 700; padding: 3px 10px; border-radius: 12px; letter-spacing: 0.8px; text-transform: uppercase; }
.si-pill-blue { background: #e0eaf5; color: #002244; font-size: 10px; font-weight: 700; padding: 3px 10px; border-radius: 12px; letter-spacing: 0.8px; text-transform: uppercase; }

/* ── METRIC CARDS (white, visible dates) ── */
.si-metrics { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 20px; }
.si-metric {
    background: #ffffff;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
    border: 1px solid #dde4ec;
    border-top: 4px solid #009999;
    padding: 18px 20px;
}
.si-metric.blue { border-top-color: #002244; }
.si-metric.green { border-top-color: #1a7a4a; }
.si-metric.teal2 { border-top-color: #007799; }
.si-metric-val { font-size: 28px; font-weight: 700; color: #002244; line-height: 1.1; margin-bottom: 4px; }
.si-metric-val.date { font-size: 16px; padding-top: 5px; color: #009999; }
.si-metric-lbl { font-size: 10px; color: #7a8a99; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }

/* ── DATE RANGE BANNER (white, clear) ── */
.si-date-banner {
    background: #ffffff;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
    border: 1px solid #dde4ec;
    border-left: 5px solid #009999;
    padding: 18px 28px;
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 20px;
    flex-wrap: wrap; gap: 16px;
}
.si-date-block-lbl { font-size: 10px; color: #7a8a99; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
.si-date-block-val { font-size: 18px; font-weight: 700; color: #002244; }
.si-date-arrow { font-size: 24px; color: #009999; font-weight: 300; }
.si-date-block-val.accent { color: #009999; }

/* ── CONFIG BOXES ── */
.si-config-box {
    background: #f4f7fb;
    border: 1px solid #dde4ec;
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 14px;
}
.si-config-label { font-size: 10px; color: #7a8a99; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
.si-config-val { font-size: 22px; font-weight: 700; color: #002244; }
.si-config-sub { font-size: 11px; color: #009999; font-weight: 500; }

/* ── TERMINAL ── */
.si-terminal {
    background: #0d1117;
    border-radius: 8px;
    padding: 16px 18px;
    font-family: 'Courier New', monospace;
    font-size: 12px;
    color: #4ade80;
    min-height: 160px;
    max-height: 280px;
    overflow-y: auto;
    line-height: 1.75;
    border: 1px solid #21262d;
}
.t-err { color: #f87171; }
.t-warn { color: #fbbf24; }
.t-info { color: #38bdf8; }
.t-ok { color: #4ade80; }
.t-dim { color: #484f58; }

/* ── TABLE ── */
.si-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.si-table th {
    background: #f4f7fb;
    color: #002244;
    font-size: 10px; font-weight: 700;
    text-transform: uppercase; letter-spacing: 1px;
    padding: 10px 16px; text-align: left;
    border-bottom: 2px solid #dde4ec;
    white-space: nowrap;
}
.si-table td {
    padding: 11px 16px;
    color: #2a3a4a;
    border-bottom: 1px solid #f0f4f8;
    vertical-align: middle;
}
.si-table tr:last-child td { border-bottom: none; }
.si-table tr:hover td { background: #f7fbfb; }
.cat-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 10px; font-weight: 700;
    letter-spacing: 0.3px; white-space: nowrap;
}

/* ── FILTER ROW ── */
.si-filter-row {
    background: #ffffff;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
    border: 1px solid #dde4ec;
    padding: 16px 20px;
    margin-bottom: 20px;
}

/* ── STREAMLIT WIDGET OVERRIDES ── */
.stButton > button {
    background: #009999 !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 11px 24px !important;
    width: 100% !important;
    letter-spacing: 0.3px !important;
}
.stButton > button:hover { background: #007a7a !important; }

.stDownloadButton > button {
    background: #ffffff !important;
    color: #009999 !important;
    border: 2px solid #009999 !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    border-radius: 8px !important;
    padding: 10px 24px !important;
    width: 100% !important;
}
.stDownloadButton > button:hover { background: #f0fafa !important; }

/* Date inputs, selects — white bg with visible text */
div[data-baseweb="select"] > div {
    background: #ffffff !important;
    border: 1.5px solid #c0cdd8 !important;
    border-radius: 8px !important;
    color: #1a2332 !important;
}
div[data-baseweb="select"] * { color: #1a2332 !important; }

.stDateInput > div > div > input {
    background: #ffffff !important;
    border: 1.5px solid #c0cdd8 !important;
    border-radius: 8px !important;
    color: #1a2332 !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    padding: 8px 12px !important;
}
.stTextInput input {
    background: #ffffff !important;
    border: 1.5px solid #c0cdd8 !important;
    border-radius: 8px !important;
    color: #1a2332 !important;
    font-size: 14px !important;
}
.stNumberInput input {
    background: #ffffff !important;
    border: 1.5px solid #c0cdd8 !important;
    border-radius: 8px !important;
    color: #1a2332 !important;
    font-size: 14px !important;
}
.stCheckbox span { color: #1a2332 !important; font-size: 13px !important; }
.stProgress > div > div { background: #009999 !important; }

/* Labels above inputs */
label, .stSelectbox label, .stNumberInput label,
.stDateInput label, .stCheckbox label, .stTextInput label {
    color: #4a6070 !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
    margin-bottom: 4px !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: transparent;
    border-bottom: 2px solid #dde4ec;
    gap: 4px;
    padding: 0 4px;
}
.stTabs [data-baseweb="tab"] {
    color: #7a8a99 !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    padding: 10px 20px !important;
    border-radius: 0 !important;
    border-bottom: 3px solid transparent !important;
    margin-bottom: -2px !important;
    background: transparent !important;
}
.stTabs [aria-selected="true"] {
    color: #002244 !important;
    font-weight: 700 !important;
    border-bottom: 3px solid #009999 !important;
    background: transparent !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: #f4fbfb !important;
    border: 2px dashed #009999 !important;
    border-radius: 10px !important;
}
[data-testid="stFileUploader"] label { color: #009999 !important; text-transform: none !important; font-size: 13px !important; }

/* Expander */
div[data-testid="stExpander"] {
    background: #ffffff;
    border: 1px solid #dde4ec !important;
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# ── Session State ────────────────────────────────────────────
for k, v in [("scraped_articles",[]), ("scraper_log",[])]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── Helpers ──────────────────────────────────────────────────
def parse_d(d):
    if not d: return None
    for fmt in ["%d %B %Y","%B %d, %Y","%d %b %Y","%Y-%m-%d"]:
        try: return datetime.strptime(d.strip(), fmt).date()
        except: pass
    return None

CAT_STYLE = {
    "Digital Industries":   "background:#dbeafe; color:#1e40af;",
    "Smart Infrastructure": "background:#d1fae5; color:#065f46;",
    "Siemens Mobility":     "background:#ede9fe; color:#5b21b6;",
    "Financial Services":   "background:#ffedd5; color:#9a3412;",
    "Siemens AG":           "background:#f1f5f9; color:#334155;",
    "AI & Innovation":      "background:#fce7f3; color:#9d174d;",
    "Sustainability":       "background:#dcfce7; color:#14532d;",
}

# ── NAV ─────────────────────────────────────────────────────
arts = st.session_state.scraped_articles
vd = sorted([d for d in [parse_d(a.get("date","")) for a in arts] if d])
n_arts = len(arts)
n_cats = len(set(a.get("category","") for a in arts)) if arts else 0
date_span = f"{vd[0].strftime('%d %b %Y')}  →  {vd[-1].strftime('%d %b %Y')}" if vd else "No data yet"

st.markdown("""
<div class="si-nav">
    <div class="si-nav-logo">SIEMENS <span>· SiDocs AI</span></div>
    <div class="si-nav-right">
        <span class="si-nav-pill">PRESS INTELLIGENCE</span>
        <span class="si-nav-chip">⊞ Company Hub</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── HERO ─────────────────────────────────────────────────────
st.markdown(f"""
<div class="si-hero">
    <div class="si-hero-eyebrow">Siemens · Internal Platform</div>
    <div class="si-hero-title">Press Release <span>Intelligence</span> Dashboard</div>
    <div class="si-hero-sub">Scrape · Analyse · Filter Siemens press releases by date range — upload PDFs or run the live scraper to get started.</div>
    <div class="si-hero-stats">
        <div class="si-hero-stat">
            <div class="si-hero-stat-val">{n_arts}</div>
            <div class="si-hero-stat-lbl">Articles Loaded</div>
        </div>
        <div class="si-hero-stat">
            <div class="si-hero-stat-val">{n_cats}</div>
            <div class="si-hero-stat-lbl">Categories</div>
        </div>
        <div class="si-hero-stat">
            <div class="si-hero-stat-val" style="font-size:15px; padding-top:4px;">{date_span}</div>
            <div class="si-hero-stat-lbl">Coverage Window</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── BODY + TABS ──────────────────────────────────────────────
st.markdown('<div class="si-body">', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs([
    "  🌐  Live Scraper  ",
    "  📄  PDF Upload & Date Check  ",
    "  📊  Article Explorer  ",
])

# ═══════════════════════════
# TAB 1 — LIVE SCRAPER
# ═══════════════════════════
with tab1:
    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    # Config + Log side by side
    col_left, col_right = st.columns([1, 2], gap="large")

    with col_left:
        st.markdown('<div class="si-card">', unsafe_allow_html=True)
        st.markdown('<div class="si-card-head"><span class="si-card-title">Scraper Settings</span><span class="si-pill-blue">ScraperAPI</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="si-card-body">', unsafe_allow_html=True)

        pages = st.number_input("Pages to Scrape", min_value=1, max_value=20, value=1,
                                help="1 page ≈ 10 articles")
        st.markdown(f"""
        <div class="si-config-box" style="margin-top:12px;">
            <div class="si-config-label">Target</div>
            <div style="font-size:13px; font-weight:600; color:#009999;">press.siemens.com</div>
        </div>
        <div class="si-config-box">
            <div class="si-config-label">Estimated Articles</div>
            <div class="si-config-val">{pages * 10}</div>
            <div class="si-config-sub">from {pages} page(s)</div>
        </div>
        """, unsafe_allow_html=True)

        fetch_full = st.checkbox("Fetch Full Article Body", value=False)
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        run_btn = st.button("▶  Run Scraper", key="run_btn")
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.session_state.scraped_articles:
            df_e = pd.DataFrame(st.session_state.scraped_articles)
            st.download_button(
                "⬇  Export CSV",
                data=df_e.to_csv(index=False).encode(),
                file_name=f"siemens_press_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
            )

        st.markdown('</div></div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="si-card" style="height:100%">', unsafe_allow_html=True)
        st.markdown('<div class="si-card-head"><span class="si-card-title">Scraper Log</span><span class="si-pill-teal">Live Output</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="si-card-body">', unsafe_allow_html=True)

        prog_ph = st.empty()
        log_ph  = st.empty()

        def render_log():
            lines = st.session_state.scraper_log
            html = '<div class="si-terminal">'
            if not lines:
                html += '<div class="t-dim">[--:--:--] SiDocs AI scraper ready.</div>'
                html += '<div class="t-dim">[--:--:--] Press ▶ Run Scraper to begin.</div>'
            for ts, kind, msg in lines:
                html += f'<div class="t-{kind}">[{ts}] {msg}</div>'
            html += '</div>'
            log_ph.markdown(html, unsafe_allow_html=True)

        render_log()
        st.markdown('</div></div>', unsafe_allow_html=True)

    # Run scraper
    if run_btn:
        st.session_state.scraper_log = []
        st.session_state.scraped_articles = []

        def log(msg, kind="ok"):
            ts = datetime.now().strftime("%H:%M:%S")
            st.session_state.scraper_log.append((ts, kind, msg))
            render_log()

        log("Initialising SiDocs AI scraper...", "info")
        log(f"Target: press.siemens.com  |  Pages: {pages}  |  Full fetch: {fetch_full}", "info")
        prog_ph.progress(5)

        try:
            sys.path.insert(0, "/mnt/user-data/uploads")
            from scraper import get_press_releases, scrape_article_content
            from summarizer import detect_category

            log("Connecting via ScraperAPI proxy...", "info")
            articles_raw = get_press_releases(max_pages=pages)
            prog_ph.progress(40)

            if not articles_raw:
                log("No articles returned — check ScraperAPI key in scraper.py", "err")
            else:
                log(f"Fetched {len(articles_raw)} articles successfully", "ok")
                if fetch_full:
                    log("Fetching full article bodies...", "info")
                    for i, a in enumerate(articles_raw):
                        body = scrape_article_content(a["url"])
                        if body: a["body"] = body
                        log(f"[{i+1}/{len(articles_raw)}] {a['title'][:55]}...", "ok")
                        prog_ph.progress(40 + int(40*(i+1)/len(articles_raw)))
                log("Detecting categories...", "info")
                for a in articles_raw:
                    a["category"] = detect_category(a["title"], a["url"], a.get("body",""))
                prog_ph.progress(95)
                st.session_state.scraped_articles = articles_raw
                cats_found = len(set(a["category"] for a in articles_raw))
                log(f"Done — {len(articles_raw)} articles ready across {cats_found} categories", "ok")
                prog_ph.progress(100)
        except ImportError as e:
            log(f"Import error: {e}", "err")
            log("Ensure scraper.py and summarizer.py are in the same folder", "warn")
        except Exception as e:
            log(f"Error: {e}", "err")
        st.rerun()

    # ── Results ──
    if st.session_state.scraped_articles:
        a2 = st.session_state.scraped_articles
        vd2 = sorted([d for d in [parse_d(a.get("date","")) for a in a2] if d])
        mn = vd2[0].strftime("%d %b %Y") if vd2 else "—"
        mx = vd2[-1].strftime("%d %b %Y") if vd2 else "—"
        cats2 = len(set(a.get("category","") for a in a2))

        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

        # Metrics — white cards with dark text
        st.markdown(f"""
        <div class="si-metrics">
            <div class="si-metric">
                <div class="si-metric-val">{len(a2)}</div>
                <div class="si-metric-lbl">Articles Scraped</div>
            </div>
            <div class="si-metric blue">
                <div class="si-metric-val">{cats2}</div>
                <div class="si-metric-lbl">Categories Found</div>
            </div>
            <div class="si-metric teal2">
                <div class="si-metric-val date">{mn}</div>
                <div class="si-metric-lbl">Earliest Date</div>
            </div>
            <div class="si-metric green">
                <div class="si-metric-val date">{mx}</div>
                <div class="si-metric-lbl">Latest Date</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Date range banner
        if vd2:
            span_days = (vd2[-1] - vd2[0]).days
            st.markdown(f"""
            <div class="si-date-banner">
                <div>
                    <div class="si-date-block-lbl">📅 Earliest Article</div>
                    <div class="si-date-block-val">{vd2[0].strftime("%d %B %Y")}</div>
                </div>
                <div class="si-date-arrow">→</div>
                <div>
                    <div class="si-date-block-lbl">📅 Latest Article</div>
                    <div class="si-date-block-val">{vd2[-1].strftime("%d %B %Y")}</div>
                </div>
                <div style="border-left:1px solid #dde4ec; padding-left:24px;">
                    <div class="si-date-block-lbl">Coverage Span</div>
                    <div class="si-date-block-val accent">{span_days} days</div>
                </div>
                <div>
                    <div class="si-date-block-lbl">Dated Articles</div>
                    <div class="si-date-block-val accent">{len(vd2)} / {len(a2)}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Article table
        st.markdown('<div class="si-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="si-card-head"><span class="si-card-title">Scraped Articles</span><span class="si-pill-teal">{len(a2)} Results</span></div>', unsafe_allow_html=True)

        rows = ""
        for i, a in enumerate(a2[:60], 1):
            cat = a.get("category","Siemens AG")
            sty = CAT_STYLE.get(cat, "background:#f1f5f9; color:#334155;")
            rows += f"""<tr>
                <td style="color:#aab; font-weight:600; width:36px;">{i:02d}</td>
                <td style="color:#007799; white-space:nowrap; font-weight:600; width:130px;">{a.get('date','—')}</td>
                <td style="font-weight:500; color:#1a2332;">{a.get('title','')[:90]}</td>
                <td style="width:160px;"><span class="cat-badge" style="{sty}">{cat}</span></td>
            </tr>"""

        st.markdown(f"""
        <div style="overflow-x:auto;">
            <table class="si-table">
                <thead><tr><th>#</th><th>Date</th><th>Title</th><th>Category</th></tr></thead>
                <tbody>{rows}</tbody>
            </table>
        </div>
        {"<div style='padding:12px 16px;font-size:12px;color:#888;'>Showing 60 of "+str(len(a2))+" — see Article Explorer for full view.</div>" if len(a2)>60 else ""}
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════
# TAB 2 — PDF DATE CHECK
# ═══════════════════════════
with tab2:
    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    col_up, col_res = st.columns([1, 1], gap="large")

    with col_up:
        st.markdown('<div class="si-card">', unsafe_allow_html=True)
        st.markdown('<div class="si-card-head"><span class="si-card-title">Upload PDF Report</span><span class="si-pill-teal">Auto-Detect</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="si-card-body">', unsafe_allow_html=True)
        st.markdown("""
        <p style="font-size:13px; color:#4a6070; line-height:1.6; margin-bottom:14px;">
        Drag and drop a generated Siemens Press Intelligence PDF.<br>
        The app will automatically extract all dates, detect the coverage window,
        and verify the article count inside.
        </p>
        """, unsafe_allow_html=True)
        uploaded = st.file_uploader("Drop your PDF here or click to browse", type=["pdf"], label_visibility="visible")
        st.markdown('</div></div>', unsafe_allow_html=True)

        # Also show date range picker for manual filter
        st.markdown('<div class="si-card">', unsafe_allow_html=True)
        st.markdown('<div class="si-card-head"><span class="si-card-title">Manual Date Range Filter</span><span class="si-pill-blue">Optional</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="si-card-body">', unsafe_allow_html=True)
        st.markdown('<p style="font-size:12px;color:#7a8a99;margin-bottom:12px;">Filter scraped articles by selecting a custom date range below.</p>', unsafe_allow_html=True)
        pdf_filter_start = st.date_input("From Date", value=date(2024,1,1), key="pdf_fs")
        pdf_filter_end   = st.date_input("To Date",   value=date.today(),   key="pdf_fe")

        if st.session_state.scraped_articles:
            filtered_for_pdf = [
                a for a in st.session_state.scraped_articles
                if (lambda d: d and pdf_filter_start <= d <= pdf_filter_end)(parse_d(a.get("date","")))
            ]
            st.markdown(f"""
            <div style="background:#f0fafa; border:1px solid #b3e0e0; border-radius:8px;
                        padding:14px 16px; margin-top:12px; color:#004444;">
                <strong style="color:#002244;">{len(filtered_for_pdf)}</strong>
                <span style="font-size:13px;"> articles in this date range</span>
            </div>
            """, unsafe_allow_html=True)
            if filtered_for_pdf:
                df_filtered = pd.DataFrame(filtered_for_pdf)
                st.download_button(
                    "⬇  Export Filtered CSV",
                    data=df_filtered.to_csv(index=False).encode(),
                    file_name=f"filtered_{pdf_filter_start}_{pdf_filter_end}.csv",
                    mime="text/csv",
                )
        st.markdown('</div></div>', unsafe_allow_html=True)

    with col_res:
        if uploaded:
            pdf_bytes = uploaded.read()
            text = ""
            try:
                import pdfplumber
                with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                    for page in pdf.pages[:25]:
                        t = page.extract_text()
                        if t: text += t + "\n"
            except:
                try:
                    import PyPDF2
                    reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
                    for page in reader.pages[:25]:
                        text += (page.extract_text() or "") + "\n"
                except:
                    text = pdf_bytes.decode("latin-1", errors="ignore")

            pats = [
                r'\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b',
                r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',
                r'\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}\b',
                r'\b\d{4}-\d{2}-\d{2}\b',
            ]
            found = []
            for p in pats: found.extend(re.findall(p, text, re.IGNORECASE))

            def try_parse(d):
                for fmt in ["%d %B %Y","%B %d %Y","%B %d, %Y","%d %b %Y","%Y-%m-%d"]:
                    try: return datetime.strptime(d.strip(), fmt).date()
                    except: pass
                return None

            pdates = sorted(set(filter(None, [try_parse(d) for d in found])))
            art_count = len(re.findall(r'^\d{2}\s+', text, re.MULTILINE))

            if pdates:
                mn2, mx2 = min(pdates), max(pdates)
                span2 = (mx2 - mn2).days

                st.markdown('<div class="si-card">', unsafe_allow_html=True)
                st.markdown('<div class="si-card-head"><span class="si-card-title">PDF Analysis Result</span><span class="si-pill-teal">✓ Dates Found</span></div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="si-card-body">
                    <div class="si-date-banner" style="margin-bottom:16px; flex-direction:column; align-items:flex-start; gap:14px;">
                        <div style="display:flex; gap:32px; align-items:center; width:100%;">
                            <div>
                                <div class="si-date-block-lbl">📅 Earliest Date in PDF</div>
                                <div class="si-date-block-val" style="font-size:20px;">{mn2.strftime("%d %B %Y")}</div>
                            </div>
                            <div class="si-date-arrow" style="font-size:28px;">→</div>
                            <div>
                                <div class="si-date-block-lbl">📅 Latest Date in PDF</div>
                                <div class="si-date-block-val" style="font-size:20px;">{mx2.strftime("%d %B %Y")}</div>
                            </div>
                        </div>
                        <div style="display:flex; gap:32px; padding-top:10px; border-top:1px solid #eef2f6; width:100%;">
                            <div>
                                <div class="si-date-block-lbl">Coverage Span</div>
                                <div class="si-date-block-val accent">{span2} days</div>
                            </div>
                            <div>
                                <div class="si-date-block-lbl">Unique Dates</div>
                                <div class="si-date-block-val accent">{len(pdates)}</div>
                            </div>
                            <div>
                                <div class="si-date-block-lbl">Articles Detected</div>
                                <div class="si-date-block-val accent">{art_count if art_count else "—"}</div>
                            </div>
                            <div>
                                <div class="si-date-block-lbl">File Size</div>
                                <div class="si-date-block-val">{round(len(pdf_bytes)/1024)} KB</div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                # All dates table
                st.markdown('<div class="si-card-head" style="margin:0 -1px;"><span class="si-card-title">All Dates Found in PDF</span></div>', unsafe_allow_html=True)
                date_rows = "".join(
                    f'<tr><td style="color:#aab;width:36px;">{i:02d}</td>'
                    f'<td style="font-weight:600;color:#002244;">{d.strftime("%d %B %Y")}</td>'
                    f'<td style="color:#7a8a99;">{d.strftime("%A")}</td>'
                    f'<td style="color:#009999;">{d.strftime("%Y")}</td></tr>'
                    for i,d in enumerate(pdates,1)
                )
                st.markdown(f"""
                <div style="overflow-x:auto; max-height:320px; overflow-y:auto;">
                    <table class="si-table">
                        <thead><tr><th>#</th><th>Date</th><th>Day</th><th>Year</th></tr></thead>
                        <tbody>{date_rows}</tbody>
                    </table>
                </div>
                </div></div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background:#fffbeb; border:1.5px solid #f59e0b; border-radius:10px;
                            padding:20px 24px; color:#78350f;">
                    <strong>⚠ No dates detected</strong><br>
                    <span style="font-size:13px;">The PDF may be image-based (scanned) or use a non-standard date format.</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="si-card" style="padding:60px 40px; text-align:center;">
                <div style="font-size:48px; margin-bottom:14px;">📄</div>
                <div style="font-size:16px; font-weight:700; color:#002244; margin-bottom:6px;">No PDF uploaded yet</div>
                <div style="font-size:13px; color:#7a8a99;">Upload a PDF on the left to see date range analysis here</div>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════
# TAB 3 — ARTICLE EXPLORER
# ═══════════════════════════
with tab3:
    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    all_arts = st.session_state.scraped_articles

    if not all_arts:
        st.markdown("""
        <div class="si-card" style="padding:80px 40px; text-align:center;">
            <div style="font-size:48px; margin-bottom:14px;">🌐</div>
            <div style="font-size:16px; font-weight:700; color:#002244; margin-bottom:8px;">No articles loaded</div>
            <div style="font-size:13px; color:#7a8a99;">Run the Live Scraper in Tab 1 first</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Filter bar
        st.markdown('<div class="si-filter-row">', unsafe_allow_html=True)
        fc1, fc2, fc3, fc4 = st.columns([1,1,1,1])
        with fc1:
            f_start = st.date_input("From Date", value=date(2024,1,1), key="ex_fs")
        with fc2:
            f_end = st.date_input("To Date", value=date.today(), key="ex_fe")
        with fc3:
            cats_opts = ["All"] + sorted(set(a.get("category","") for a in all_arts))
            sel_cat = st.selectbox("Category", cats_opts)
        with fc4:
            srch = st.text_input("Search Title", placeholder="Type keyword...", key="ex_srch")
        st.markdown('</div>', unsafe_allow_html=True)

        # Apply
        filtered = []
        for a in all_arts:
            d = parse_d(a.get("date",""))
            if d and not (f_start <= d <= f_end): continue
            if sel_cat != "All" and a.get("category") != sel_cat: continue
            if srch and srch.lower() not in a.get("title","").lower(): continue
            filtered.append(a)

        # Summary stats
        fvd = sorted([d for d in [parse_d(a.get("date","")) for a in filtered] if d])
        f_mn = fvd[0].strftime("%d %b %Y") if fvd else "—"
        f_mx = fvd[-1].strftime("%d %b %Y") if fvd else "—"

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""<div class="si-metric"><div class="si-metric-val">{len(filtered)}</div><div class="si-metric-lbl">Matching Articles</div></div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class="si-metric teal2"><div class="si-metric-val date">{f_mn}</div><div class="si-metric-lbl">Earliest in Filter</div></div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class="si-metric green"><div class="si-metric-val date">{f_mx}</div><div class="si-metric-lbl">Latest in Filter</div></div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

        if filtered:
            st.markdown('<div class="si-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="si-card-head"><span class="si-card-title">Filtered Results</span><span class="si-pill-teal">{len(filtered)} Articles</span></div>', unsafe_allow_html=True)

            rows = ""
            for i, a in enumerate(filtered, 1):
                cat = a.get("category","Siemens AG")
                sty = CAT_STYLE.get(cat, "background:#f1f5f9; color:#334155;")
                snip = (a.get("body","") or a.get("summary",""))[:90]
                url  = a.get("url","#")
                rows += f"""<tr>
                    <td style="color:#aab;width:36px;">{i:02d}</td>
                    <td style="color:#007799;white-space:nowrap;font-weight:600;width:130px;">{a.get('date','—')}</td>
                    <td>
                        <a href="{url}" target="_blank" style="color:#002244;font-weight:600;text-decoration:none;">{a.get('title','')[:85]}</a>
                        <div style="font-size:11px;color:#9aacbb;margin-top:2px;">{snip}{'...' if len(snip)==90 else ''}</div>
                    </td>
                    <td style="width:165px;"><span class="cat-badge" style="{sty}">{cat}</span></td>
                </tr>"""

            st.markdown(f"""
            <div style="overflow-x:auto;">
                <table class="si-table">
                    <thead><tr><th>#</th><th>Date</th><th>Title</th><th>Category</th></tr></thead>
                    <tbody>{rows}</tbody>
                </table>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            df_f = pd.DataFrame(filtered)
            st.download_button(
                "⬇  Export Filtered Articles (CSV)",
                data=df_f.to_csv(index=False).encode(),
                file_name=f"filtered_{f_start}_{f_end}.csv",
                mime="text/csv",
            )
        else:
            st.markdown("""
            <div class="si-card" style="padding:40px; text-align:center; color:#7a8a99; font-size:14px;">
                No articles match the current filters. Try adjusting the date range or category.
            </div>
            """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
