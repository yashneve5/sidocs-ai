"""
SiDocs AI – Siemens Press Intelligence
Exact Siemens.com design: #000028 bg, white text, #00ffbf teal CTA
+ PDF Merge functionality (Live Scraper + Article Explorer)
+ Fixed calendar popup colors comprehensively
"""

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import sys, re, io
from datetime import datetime, date

st.set_page_config(
    page_title="SiDocs AI | Siemens Press Intelligence",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', sans-serif !important;
    background-color: #000028 !important;
    color: #ffffff !important;
    -webkit-font-smoothing: antialiased;
}
#MainMenu, footer, header { visibility: hidden !important; }
[data-testid="stSidebar"] { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stAppViewContainer"] > div { padding: 0 !important; }

/* ── NAV ── */
.nav {
    background: #000028;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    padding: 0 56px; height: 68px;
    display: flex; align-items: center; justify-content: space-between;
    position: sticky; top: 0; z-index: 1000;
}
.nav-logo { font-size: 22px; font-weight: 900; color: #fff; letter-spacing: 3px; }
.nav-links { display: flex; gap: 32px; }
.nav-link { font-size: 13px; color: rgba(255,255,255,0.55); cursor: pointer; }
.nav-link:hover { color: #fff; }
.nav-right { display: flex; align-items: center; gap: 20px; }
.nav-sep { width: 1px; height: 18px; background: rgba(255,255,255,0.12); }
.nav-txt { font-size: 13px; color: rgba(255,255,255,0.5); }
.nav-tag { font-size: 11px; font-weight: 700; letter-spacing: 1.5px; color: #00ffbf; border: 1.5px solid rgba(0,255,191,0.35); padding: 5px 14px; }

/* ── HERO ── */
.hero {
    background: #000028;
    padding: 72px 56px 62px 56px;
    position: relative; overflow: hidden;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}
.hero::before { content:''; position:absolute; top:-100px; right:-80px; width:550px; height:550px; background:radial-gradient(ellipse, rgba(0,155,130,0.12) 0%, transparent 65%); pointer-events:none; }
.hero-eyebrow { font-size: 11px; font-weight: 700; letter-spacing: 2.5px; text-transform: uppercase; color: #00ccaa; margin-bottom: 18px; }
.hero-title { font-size: 48px; font-weight: 800; color: #fff; line-height: 1.1; margin-bottom: 20px; max-width: 700px; letter-spacing: -0.5px; }
.hero-title em { color: #00ffbf; font-style: normal; }
.hero-sub { font-size: 16px; color: rgba(255,255,255,0.5); line-height: 1.8; max-width: 540px; font-weight: 300; margin-bottom: 8px; }
.hero-stats { display: flex; gap: 52px; margin-top: 46px; padding-top: 38px; border-top: 1px solid rgba(255,255,255,0.07); }
.hs-val { font-size: 38px; font-weight: 900; color: #00ffbf; line-height: 1; letter-spacing: -1px; }
.hs-val.sm { font-size: 19px; font-weight: 700; color: #ffffff; padding-top: 9px; line-height: 1.3; letter-spacing: 0; }
.hs-lbl { font-size: 10px; font-weight: 700; color: rgba(255,255,255,0.3); text-transform: uppercase; letter-spacing: 1.8px; margin-top: 7px; }

/* ── PAGE BODY ── */
.page { background: #000028; padding: 40px 56px 80px 56px; }

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: #000028 !important;
    border-bottom: 1px solid rgba(255,255,255,0.08) !important;
    gap: 0 !important; padding: 0 56px !important; margin: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: rgba(255,255,255,0.42) !important;
    font-size: 14px !important; font-weight: 500 !important;
    padding: 16px 28px !important;
    border: none !important; border-bottom: 3px solid transparent !important;
    margin-bottom: -1px !important; letter-spacing: 0.1px !important;
}
.stTabs [aria-selected="true"] {
    color: #ffffff !important; font-weight: 700 !important;
    border-bottom: 3px solid #00ffbf !important;
}
.stTabs [data-baseweb="tab-panel"] { background: transparent !important; padding: 0 !important; }
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }

/* ── CARDS ── */
.card { background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.09); margin-bottom: 20px; overflow: hidden; }
.card-hd { padding: 15px 22px; border-bottom: 1px solid rgba(255,255,255,0.07); background: rgba(255,255,255,0.025); display: flex; align-items: center; justify-content: space-between; }
.card-title { font-size: 14px; font-weight: 700; color: #fff; }
.card-body { padding: 26px 22px; }

/* ── BADGES ── */
.bg-teal { background: rgba(0,255,191,0.1); color: #00ffbf; border: 1px solid rgba(0,255,191,0.25); font-size: 10px; font-weight: 700; padding: 3px 11px; letter-spacing: 1.2px; text-transform: uppercase; }
.bg-grey { background: rgba(255,255,255,0.06); color: rgba(255,255,255,0.42); border: 1px solid rgba(255,255,255,0.1); font-size: 10px; font-weight: 700; padding: 3px 11px; letter-spacing: 1.2px; text-transform: uppercase; }
.bg-purple { background: rgba(168,85,247,0.14); color: #d8b4fe; border: 1px solid rgba(168,85,247,0.3); font-size: 10px; font-weight: 700; padding: 3px 11px; letter-spacing: 1.2px; text-transform: uppercase; }

/* ── KPI GRID ── */
.kpi-row { display: grid; grid-template-columns: repeat(4,1fr); gap: 14px; margin: 26px 0; }
.kpi { background: rgba(255,255,255,0.035); border: 1px solid rgba(255,255,255,0.08); border-top: 3px solid #00ffbf; padding: 22px 20px 18px; }
.kpi.b { border-top-color: #0099dd; }
.kpi.g { border-top-color: #00cc88; }
.kpi.w { border-top-color: rgba(255,255,255,0.22); }
.kpi-val { font-size: 34px; font-weight: 900; color: #00ffbf; line-height: 1; margin-bottom: 7px; letter-spacing: -1px; }
.kpi-val.dt { font-size: 15px; font-weight: 700; color: #fff; line-height: 1.4; padding-top: 8px; letter-spacing: 0; }
.kpi-lbl { font-size: 10px; font-weight: 700; color: rgba(255,255,255,0.3); text-transform: uppercase; letter-spacing: 1.5px; }

/* ── DATE BANNER ── */
.dbanner { background: rgba(0,255,191,0.05); border: 1px solid rgba(0,255,191,0.15); border-left: 4px solid #00ffbf; padding: 22px 28px; display: flex; align-items: center; gap: 36px; flex-wrap: wrap; margin-bottom: 22px; }
.db-lbl { font-size: 10px; font-weight: 700; color: rgba(255,255,255,0.3); text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 5px; }
.db-val { font-size: 19px; font-weight: 700; color: #ffffff; }
.db-val.teal { color: #00ffbf; }
.db-arrow { font-size: 22px; color: rgba(0,255,191,0.55); flex-shrink: 0; }

/* ── SECTION LABEL ── */
.sec { font-size: 10px; font-weight: 700; color: rgba(255,255,255,0.26); text-transform: uppercase; letter-spacing: 2px; margin: 32px 0 14px; display: flex; align-items: center; gap: 12px; }
.sec::after { content:''; flex:1; height:1px; background:rgba(255,255,255,0.06); }

/* ── TERMINAL ── */
.term { background: #00001c; border: 1px solid rgba(0,255,191,0.1); padding: 18px 20px; font-family: 'Courier New', monospace; font-size: 12.5px; line-height: 1.9; min-height: 200px; max-height: 300px; overflow-y: auto; color: #00ffbf; }
.t-ok   { color: #00ffbf; }
.t-info { color: #60c8e8; }
.t-warn { color: #ffd166; }
.t-err  { color: #ff6b6b; }
.t-dim  { color: rgba(255,255,255,0.18); }

/* ── TABLE ── */
.tbl { width: 100%; border-collapse: collapse; }
.tbl th { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; color: rgba(255,255,255,0.5); padding: 11px 16px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.08); background: rgba(255,255,255,0.02); }
.tbl td { padding: 13px 16px; font-size: 13px; color: rgba(255,255,255,0.85); border-bottom: 1px solid rgba(255,255,255,0.045); vertical-align: middle; }
.tbl tr:last-child td { border-bottom: none; }
.tbl tr:hover td { background: rgba(0,255,191,0.04); }

/* ── CFG BOX ── */
.cfg-grid { display: grid; grid-template-columns:1fr 1fr; gap:10px; margin-top:18px; }
.cfg-box { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); padding: 14px 16px; }
.cfg-lbl { font-size: 9px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.3px; color: rgba(255,255,255,0.28); margin-bottom: 5px; }
.cfg-val { font-size: 22px; font-weight: 800; color: #00ffbf; }
.cfg-val.sm { font-size: 12px; font-weight: 600; }

/* ── FILTER BAR ── */
.fbar { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); padding: 22px 22px 24px; margin-bottom: 22px; }
.fbar-title { font-size: 10px; font-weight: 700; color: rgba(255,255,255,0.28); text-transform: uppercase; letter-spacing: 1.8px; margin-bottom: 16px; }

/* ── INFO / WARN / EMPTY ── */
.ibox { background: rgba(0,255,191,0.05); border: 1px solid rgba(0,255,191,0.14); border-left: 3px solid #00ffbf; padding: 18px 20px; margin: 14px 0; display: flex; align-items: center; gap: 16px; }
.ibox-num { font-size: 34px; font-weight: 900; color: #00ffbf; line-height: 1; }
.ibox-txt { font-size: 13px; color: rgba(255,255,255,0.45); line-height: 1.5; }
.ibox-txt strong { color: #fff; display: block; font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 2px; }
.wbox { background: rgba(255,107,107,0.06); border: 1px solid rgba(255,107,107,0.18); border-left: 3px solid #ff6b6b; padding: 18px 20px; }
.wbox-t { font-size: 14px; font-weight: 700; color: #ff6b6b; margin-bottom: 6px; }
.wbox-b { font-size: 13px; color: rgba(255,255,255,0.42); line-height: 1.6; }
.empty { display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 360px; text-align: center; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); padding: 60px 40px; }
.empty-i { font-size: 52px; opacity: 0.15; margin-bottom: 18px; }
.empty-t { font-size: 20px; font-weight: 800; color: #fff; margin-bottom: 10px; }
.empty-s { font-size: 14px; color: rgba(255,255,255,0.28); line-height: 1.7; max-width: 300px; }

/* ── PDF MERGE BANNER ── */
.merge-box {
    background: rgba(168,85,247,0.06);
    border: 1px solid rgba(168,85,247,0.2);
    border-left: 4px solid #a855f7;
    padding: 20px 24px; margin-bottom: 18px;
    display: flex; align-items: center; justify-content: space-between; gap: 20px; flex-wrap: wrap;
}
.merge-txt { font-size: 13px; color: rgba(255,255,255,0.6); line-height: 1.6; }
.merge-txt strong { color: #d8b4fe; display: block; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }

/* ════════════════════════════════════
   STREAMLIT WIDGETS — ALL DARK
════════════════════════════════════ */

/* Buttons */
.stButton > button {
    background: #00ffbf !important; color: #000028 !important;
    font-weight: 700 !important; font-size: 14px !important;
    border: none !important; border-radius: 0 !important;
    padding: 14px 28px !important; width: 100% !important;
    letter-spacing: 0.3px !important;
}
.stButton > button:hover { background: #00e0aa !important; }

/* Secondary / merge buttons (use type="secondary") */
.stButton > button[kind="secondary"] {
    background: #a855f7 !important; color: #ffffff !important;
}
.stButton > button[kind="secondary"]:hover { background: #9333ea !important; }

.stDownloadButton > button {
    background: transparent !important; color: #00ffbf !important;
    border: 1.5px solid rgba(0,255,191,0.4) !important;
    font-weight: 700 !important; font-size: 13px !important;
    border-radius: 0 !important; padding: 13px 24px !important; width: 100% !important;
}

/* Labels — ALL inputs */
label,
div[data-testid="stWidgetLabel"] p,
div[data-testid="stWidgetLabel"] label,
.stSelectbox label, .stNumberInput label,
.stDateInput label, .stTextInput label, .stCheckbox label {
    color: rgba(255,255,255,0.38) !important;
    font-size: 10px !important; font-weight: 700 !important;
    text-transform: uppercase !important; letter-spacing: 1.2px !important;
}

/* Number input — dark with WHITE text */
.stNumberInput [data-baseweb="input"] {
    background: rgba(255,255,255,0.07) !important;
    border: 1.5px solid rgba(255,255,255,0.18) !important;
    border-radius: 0 !important;
}
.stNumberInput input {
    background: transparent !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    font-size: 18px !important; font-weight: 700 !important;
    caret-color: #00ffbf !important;
}
.stNumberInput button {
    background: rgba(255,255,255,0.08) !important;
    border-color: rgba(255,255,255,0.15) !important;
    color: #ffffff !important;
}
.stNumberInput button svg { fill: #ffffff !important; }

/* Select — dark */
div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.07) !important;
    border: 1.5px solid rgba(255,255,255,0.18) !important;
    border-radius: 0 !important; min-height: 46px !important;
}
div[data-baseweb="select"] span,
div[data-baseweb="select"] input {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    font-size: 14px !important;
}
div[data-baseweb="select"] svg { fill: rgba(255,255,255,0.4) !important; }
div[data-baseweb="menu"] { background: #00052e !important; border: 1px solid rgba(0,255,191,0.15) !important; }
div[data-baseweb="option"] { background: transparent !important; color: rgba(255,255,255,0.8) !important; font-size: 14px !important; padding: 11px 16px !important; }
div[data-baseweb="option"]:hover { background: rgba(0,255,191,0.08) !important; color: #ffffff !important; }
ul[role="listbox"] { background: #00052e !important; }
ul[role="listbox"] li { background: #00052e !important; color: #ffffff !important; }
ul[role="listbox"] li:hover { background: rgba(0,255,191,0.1) !important; }

/* ── DATE INPUT — comprehensive dark fix ── */
.stDateInput [data-baseweb="input"] {
    background: rgba(255,255,255,0.07) !important;
    border: 1.5px solid rgba(255,255,255,0.18) !important;
    border-radius: 0 !important;
}
.stDateInput input {
    background: transparent !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    font-size: 14px !important; font-weight: 600 !important;
    caret-color: #00ffbf !important;
}

/* ── CALENDAR POPUP — force dark on ALL nested layers ── */
div[data-baseweb="popover"],
div[data-baseweb="popover"] > div,
div[data-baseweb="popover"] div[role="presentation"] {
    background: #00052e !important;
}
[data-baseweb="calendar"],
[data-baseweb="calendar"] > div,
[data-baseweb="calendar"] div {
    background-color: #00052e !important;
}
[data-baseweb="calendar"] {
    border: 1px solid rgba(0,255,191,0.25) !important;
    box-shadow: 0 8px 30px rgba(0,0,0,0.6) !important;
}
/* Calendar header (month/year + arrows) */
[data-baseweb="calendar-header"],
[data-baseweb="calendar"] [class*="Header"] {
    background-color: #00052e !important;
    color: #ffffff !important;
}
/* All text inside calendar */
[data-baseweb="calendar"] *,
[data-baseweb="calendar"] div[role="gridcell"] *,
[data-baseweb="calendar"] button * {
    color: #ffffff !important;
}
/* Day cells */
[data-baseweb="calendar"] [role="gridcell"] {
    background-color: transparent !important;
}
[data-baseweb="calendar"] [role="gridcell"] div {
    background-color: transparent !important;
    color: #ffffff !important;
}
/* Today / selected day backgrounds */
[data-baseweb="calendar"] [aria-selected="true"] div,
[data-baseweb="calendar"] [aria-selected="true"] {
    background-color: #00ffbf !important;
    color: #000028 !important;
    border-radius: 0 !important;
}
[data-baseweb="calendar"] [aria-roledescription="button"]:hover div {
    background-color: rgba(0,255,191,0.18) !important;
}
/* Month/Year dropdown selects inside calendar */
[data-baseweb="calendar"] [data-baseweb="select"] > div {
    background: rgba(255,255,255,0.08) !important;
    border-color: rgba(255,255,255,0.2) !important;
}
/* Prev/Next month arrow buttons */
[data-baseweb="calendar"] button[aria-label*="month"],
[data-baseweb="calendar"] button[aria-label*="Month"] {
    background: transparent !important;
    color: #ffffff !important;
}
[data-baseweb="calendar"] button[aria-label*="month"] svg,
[data-baseweb="calendar"] button[aria-label*="Month"] svg {
    fill: #ffffff !important;
}
/* Weekday header row (Su Mo Tu...) */
[data-baseweb="calendar"] [class*="WeekdayHeader"] {
    color: rgba(255,255,255,0.45) !important;
    background-color: #00052e !important;
}

/* Text input — dark */
.stTextInput [data-baseweb="input"] {
    background: rgba(255,255,255,0.07) !important;
    border: 1.5px solid rgba(255,255,255,0.18) !important;
    border-radius: 0 !important;
}
.stTextInput input {
    background: transparent !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    font-size: 14px !important;
    caret-color: #00ffbf !important;
}
.stTextInput input::placeholder { color: rgba(255,255,255,0.22) !important; }

/* Checkbox */
.stCheckbox > label { text-transform: none !important; font-size: 13px !important; font-weight: 400 !important; letter-spacing: 0 !important; color: rgba(255,255,255,0.65) !important; }

/* File uploader */
[data-testid="stFileUploader"] { background: rgba(0,255,191,0.03) !important; border: 2px dashed rgba(0,255,191,0.22) !important; border-radius: 0 !important; }
[data-testid="stFileUploaderDropzone"] { background: transparent !important; padding: 20px !important; }
[data-testid="stFileUploaderDropzoneInstructions"] * { color: rgba(255,255,255,0.48) !important; }
[data-testid="stFileUploader"] button { background: rgba(255,255,255,0.07) !important; color: rgba(255,255,255,0.75) !important; border: 1px solid rgba(255,255,255,0.15) !important; border-radius: 0 !important; }
[data-testid="stFileUploader"] small { color: rgba(255,255,255,0.22) !important; }
[data-testid="stFileUploader"] label { color: rgba(255,255,255,0.5) !important; font-size: 14px !important; font-weight: 400 !important; text-transform: none !important; letter-spacing: 0 !important; }
[data-testid="stFileUploader"] p { color: rgba(255,255,255,0.45) !important; }

/* Progress */
.stProgress > div > div { background: #00ffbf !important; }
[data-testid="stProgress"] > div { background: rgba(255,255,255,0.07) !important; border-radius: 0 !important; }

/* Spinner */
.stSpinner > div { border-top-color: #00ffbf !important; }
.stSpinner p { color: rgba(255,255,255,0.6) !important; }

/* Column padding */
[data-testid="column"] { padding: 0 8px !important; }
[data-testid="column"]:first-child { padding-left: 0 !important; }
[data-testid="column"]:last-child  { padding-right: 0 !important; }

/* Alerts (success/error/warning/info) */
.stAlert { border-radius: 0 !important; background: rgba(255,255,255,0.05) !important; }
.stAlert p { color: #ffffff !important; }
</style>
""", unsafe_allow_html=True)

# ── Session & helpers ────────────────────────────────────────
for k, v in [("scraped_articles", []), ("scraper_log", []), ("merged_pdf_bytes", None), ("merged_pdf_name", "")]:
    if k not in st.session_state:
        st.session_state[k] = v

def parse_d(d):
    if not d: return None
    for fmt in ["%d %B %Y", "%B %d, %Y", "%d %b %Y", "%Y-%m-%d"]:
        try: return datetime.strptime(str(d).strip(), fmt).date()
        except: pass
    return None

CAT = {
    "Digital Industries":   "background:rgba(59,130,246,0.18);color:#93c5fd;border:1px solid rgba(59,130,246,0.3);",
    "Smart Infrastructure": "background:rgba(16,185,129,0.18);color:#6ee7b7;border:1px solid rgba(16,185,129,0.3);",
    "Siemens Mobility":     "background:rgba(139,92,246,0.18);color:#c4b5fd;border:1px solid rgba(139,92,246,0.3);",
    "Financial Services":   "background:rgba(245,158,11,0.18);color:#fcd34d;border:1px solid rgba(245,158,11,0.3);",
    "Siemens AG":           "background:rgba(255,255,255,0.07);color:rgba(255,255,255,0.6);border:1px solid rgba(255,255,255,0.12);",
    "AI & Innovation":      "background:rgba(236,72,153,0.18);color:#f9a8d4;border:1px solid rgba(236,72,153,0.3);",
    "Sustainability":       "background:rgba(0,255,191,0.12);color:#00ffbf;border:1px solid rgba(0,255,191,0.25);",
}
DEF = "background:rgba(255,255,255,0.07);color:rgba(255,255,255,0.6);border:1px solid rgba(255,255,255,0.12);"

def pdf_btn(url):
    if url:
        return f'<a href="{url}" target="_blank" style="display:inline-block;padding:4px 10px;background:rgba(0,255,191,0.12);color:#00ffbf;border:1px solid rgba(0,255,191,0.3);font-size:10px;font-weight:700;text-decoration:none;letter-spacing:0.5px;white-space:nowrap;">⬇ PDF</a>'
    return '<span style="font-size:11px;color:rgba(255,255,255,0.18);">—</span>'


# ── PDF Merge helper ────────────────────────────────────────
def merge_article_pdfs(article_list, progress_callback=None):
    """
    Downloads each article's pdf_url and merges them into a single PDF.
    Returns (merged_bytes, success_count, fail_count, fail_titles).
    """
    import requests as _req
    from pypdf import PdfReader, PdfWriter
    import warnings as _w; _w.filterwarnings("ignore")

    writer = PdfWriter()
    success, fail = 0, 0
    fail_titles = []

    pdf_articles = [a for a in article_list if a.get("pdf_url")]
    total = len(pdf_articles)

    for i, a in enumerate(pdf_articles):
        try:
            r = _req.get(a["pdf_url"], headers={"User-Agent": "Mozilla/5.0"},
                         verify=False, timeout=30)
            if r.status_code == 200 and r.content[:4] == b"%PDF":
                reader = PdfReader(io.BytesIO(r.content))
                for page in reader.pages:
                    writer.add_page(page)
                success += 1
            else:
                fail += 1
                fail_titles.append(a.get("title", "Unknown")[:50])
        except Exception:
            fail += 1
            fail_titles.append(a.get("title", "Unknown")[:50])

        if progress_callback:
            progress_callback(i + 1, total)

    if success == 0:
        return None, success, fail, fail_titles

    out = io.BytesIO()
    writer.write(out)
    out.seek(0)
    return out.getvalue(), success, fail, fail_titles


arts  = st.session_state.scraped_articles
vd    = sorted([d for d in [parse_d(a.get("date", "")) for a in arts] if d])
n_a   = len(arts)
n_c   = len(set(a.get("category", "") for a in arts)) if arts else 0
dspan = f"{vd[0].strftime('%d %b %Y')}  →  {vd[-1].strftime('%d %b %Y')}" if vd else "No data yet"

# ══ NAV ══════════════════════════════════════════════════════
st.markdown(f"""
<div class="nav">
    <div class="nav-logo">SIEMENS</div>
    <div class="nav-links">
        <span class="nav-link">Products &amp; services</span>
        <span class="nav-link">Solutions</span>
        <span class="nav-link">Industries</span>
        <span class="nav-link">Topics &amp; insights</span>
    </div>
    <div class="nav-right">
        <span class="nav-txt">🌐 India | EN</span>
        <span class="nav-txt">Support ▾</span>
        <div class="nav-sep"></div>
        <span class="nav-tag">SiDocs AI</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ══ HERO ══════════════════════════════════════════════════════
st.markdown(f"""
<div class="hero">
    <div class="hero-eyebrow">Siemens · Internal Platform · Press Intelligence</div>
    <div class="hero-title">Building the intelligence layer<br>for <em>Siemens Press</em></div>
    <div class="hero-sub">Scrape, analyse and explore Siemens global press releases by date range.
    Upload PDFs for instant analysis — or run the live scraper to surface the latest news across all business units.</div>
    <div class="hero-stats">
        <div><div class="hs-val">{n_a}</div><div class="hs-lbl">Articles Loaded</div></div>
        <div><div class="hs-val">{n_c}</div><div class="hs-lbl">Categories</div></div>
        <div><div class="hs-val sm">{dspan}</div><div class="hs-lbl">Coverage Window</div></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ══ TABS ══════════════════════════════════════════════════════
tab1, tab2, tab3 = st.tabs([
    "  🌐  Live Scraper  ",
    "  📄  PDF Upload & Date Check  ",
    "  📊  Article Explorer  ",
])

# ══════════════════════════════════════════════════════════════
# TAB 1 — LIVE SCRAPER
# ══════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="page">', unsafe_allow_html=True)

    col_cfg, col_log = st.columns([5, 7], gap="large")

    with col_cfg:
        st.markdown('<div class="card" style="margin-left:14px;">', unsafe_allow_html=True)
        st.markdown('<div class="card-hd"><span class="card-title">⚙ Scraper Configuration</span><span class="bg-teal">ScraperAPI</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="card-body">', unsafe_allow_html=True)

        article_options = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        articles_to_scrape = st.selectbox(
            "Articles to Scrape",
            options=article_options,
            index=0,
            format_func=lambda x: f"{x} articles  (~{x // 10} page{'s' if x // 10 > 1 else ''})",
        )
        pages = articles_to_scrape // 10

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        fetch_full  = st.checkbox("Fetch Full Article Body", value=False)
        scrape_pdfs = st.checkbox("Scrape Article PDFs", value=True,
                                  help="Find and collect PDF download links from each article page")

        st.markdown(f"""
        <div class="cfg-grid">
            <div class="cfg-box">
                <div class="cfg-lbl">Target Domain</div>
                <div class="cfg-val sm" style="color:#00ffbf;font-size:12px;font-weight:700;">press.siemens.com</div>
            </div>
            <div class="cfg-box">
                <div class="cfg-lbl">Est. Articles</div>
                <div class="cfg-val">{articles_to_scrape}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)
        run_btn = st.button("▶  Run Scraper", type="primary")
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        if st.session_state.scraped_articles:
            df_e = pd.DataFrame(st.session_state.scraped_articles)
            st.download_button(
                "⬇  Export All Articles (CSV)",
                data=df_e.to_csv(index=False).encode(),
                file_name=f"siemens_press_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
            )
            all_pdfs = [a for a in st.session_state.scraped_articles if a.get("pdf_url")]
            if all_pdfs:
                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                pdf_csv = "Title,PDF URL\n" + "\n".join(
                    f'"{a.get("title","")[:60]}",{a.get("pdf_url","")}' for a in all_pdfs
                )
                st.download_button(
                    f"⬇  Export PDF Links ({len(all_pdfs)} PDFs)",
                    data=pdf_csv.encode(),
                    file_name=f"siemens_pdf_links_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                )

        st.markdown('</div></div>', unsafe_allow_html=True)

    with col_log:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-hd"><span class="card-title">⬛ Scraper Log</span><span class="bg-teal">Live Output</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="card-body">', unsafe_allow_html=True)
        prog_ph = st.empty()
        log_ph  = st.empty()

        def render_log():
            lines = st.session_state.scraper_log
            h = '<div class="term">'
            if not lines:
                h += '<div class="t-dim">[--:--:--] SiDocs AI Scraper — Ready.</div>'
                h += '<div class="t-dim">[--:--:--] Configure settings on the left, then press ▶ Run Scraper.</div>'
                h += '<div class="t-dim">[--:--:--] Live output will stream here...</div>'
            for ts, k, m in lines:
                h += f'<div class="t-{k}">[{ts}] {m}</div>'
            h += '</div>'
            log_ph.markdown(h, unsafe_allow_html=True)

        render_log()
        st.markdown('</div></div>', unsafe_allow_html=True)

    # ── Run scraper ──────────────────────────────────────────
    if run_btn:
        st.session_state.scraper_log = []
        st.session_state.scraped_articles = []
        st.session_state.merged_pdf_bytes = None

        def log(m, k="ok"):
            st.session_state.scraper_log.append((datetime.now().strftime("%H:%M:%S"), k, m))
            render_log()

        log("Initialising SiDocs AI scraper...", "info")
        log(f"Target: press.siemens.com  |  Pages: {pages}  |  Full fetch: {fetch_full}  |  PDF scrape: {scrape_pdfs}", "info")
        prog_ph.progress(5)

        try:
            sys.path.insert(0, "/mnt/user-data/uploads")
            from scraper import get_press_releases, scrape_article_content
            from summarizer import detect_category

            log("Connecting via ScraperAPI proxy...", "info")
            raw = get_press_releases(max_pages=pages)
            prog_ph.progress(40)

            if not raw:
                log("No articles returned — verify ScraperAPI key in scraper.py", "err")
            else:
                log(f"Fetched {len(raw)} articles successfully", "ok")

                if fetch_full:
                    log("Fetching full article bodies...", "info")
                    for i, a in enumerate(raw):
                        b = scrape_article_content(a["url"])
                        if b: a["body"] = b
                        log(f"  [{i+1}/{len(raw)}] {a['title'][:52]}...", "ok")
                        prog_ph.progress(40 + int(20 * (i + 1) / len(raw)))

                if scrape_pdfs:
                    log("Scraping PDF links from article pages...", "info")
                    import requests as _req
                    from bs4 import BeautifulSoup as _BS
                    import warnings as _w; _w.filterwarnings("ignore")

                    def _get_pdf_link(url):
                        try:
                            r = _req.get(url, headers={"User-Agent": "Mozilla/5.0"},
                                         verify=False, timeout=20)
                            soup = _BS(r.text, "html.parser")
                            for tag in soup.find_all("a", href=True):
                                href = tag["href"]
                                txt  = tag.get_text(strip=True).lower()
                                if href.lower().endswith(".pdf") or "pdf" in txt:
                                    if href.startswith("http"):
                                        return href
                                    if href.startswith("/"):
                                        return "https://press.siemens.com" + href
                        except Exception:
                            pass
                        return None

                    for i, a in enumerate(raw):
                        pdf_url = _get_pdf_link(a["url"])
                        a["pdf_url"] = pdf_url or ""
                        status = "PDF found" if pdf_url else "No PDF"
                        kind   = "ok" if pdf_url else "dim"
                        log(f"  [{i+1}/{len(raw)}] {status}: {a['title'][:45]}...", kind)
                        prog_ph.progress(60 + int(30 * (i + 1) / len(raw)))

                    n_pdfs = sum(1 for a in raw if a.get("pdf_url"))
                    log(f"PDF scraping complete — {n_pdfs}/{len(raw)} PDFs found", "ok")

                log("Detecting categories...", "info")
                for a in raw:
                    a["category"] = detect_category(a["title"], a["url"], a.get("body", ""))

                prog_ph.progress(95)
                st.session_state.scraped_articles = raw
                n_cats_f = len(set(a["category"] for a in raw))
                log(f"Complete — {len(raw)} articles across {n_cats_f} categories", "ok")
                prog_ph.progress(100)

        except ImportError as e:
            log(f"Import error: {e}", "err")
            log("Ensure scraper.py and summarizer.py are in the same folder as app.py", "warn")
        except Exception as e:
            log(f"Unexpected error: {e}", "err")

        st.rerun()

    # ── Results ──────────────────────────────────────────────
    if st.session_state.scraped_articles:
        a2  = st.session_state.scraped_articles
        vd2 = sorted([d for d in [parse_d(a.get("date", "")) for a in a2] if d])
        mn  = vd2[0].strftime("%d %b %Y")  if vd2 else "—"
        mx  = vd2[-1].strftime("%d %b %Y") if vd2 else "—"
        c2  = len(set(a.get("category", "") for a in a2))

        st.markdown('<div class="sec">Results Overview</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="kpi-row">
            <div class="kpi"><div class="kpi-val">{len(a2)}</div><div class="kpi-lbl">Articles Scraped</div></div>
            <div class="kpi b"><div class="kpi-val">{c2}</div><div class="kpi-lbl">Categories Found</div></div>
            <div class="kpi w"><div class="kpi-val dt">{mn}</div><div class="kpi-lbl">Earliest Article</div></div>
            <div class="kpi g"><div class="kpi-val dt">{mx}</div><div class="kpi-lbl">Latest Article</div></div>
        </div>
        """, unsafe_allow_html=True)

        if vd2:
            s = (vd2[-1] - vd2[0]).days
            st.markdown(f"""
            <div class="dbanner">
                <div><div class="db-lbl">📅 Earliest Article Date</div><div class="db-val">{vd2[0].strftime("%d %B %Y")}</div></div>
                <div class="db-arrow">→</div>
                <div><div class="db-lbl">📅 Latest Article Date</div><div class="db-val">{vd2[-1].strftime("%d %B %Y")}</div></div>
                <div><div class="db-lbl">Coverage Span</div><div class="db-val teal">{s} days</div></div>
                <div><div class="db-lbl">Dated Articles</div><div class="db-val teal">{len(vd2)} / {len(a2)}</div></div>
            </div>
            """, unsafe_allow_html=True)

        # ── PDF Merge section ──────────────────────────────
        all_pdfs = [a for a in a2 if a.get("pdf_url")]
        if all_pdfs:
            st.markdown('<div class="sec">Merge PDFs</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="merge-box">
                <div class="merge-txt">
                    <strong>📎 {len(all_pdfs)} Article PDFs Available</strong>
                    Combine all scraped article PDFs into a single document for offline reading or sharing.
                </div>
            </div>
            """, unsafe_allow_html=True)

            col_m1, col_m2 = st.columns([1, 2], gap="medium")
            with col_m1:
                merge_btn = st.button(f"🔗  Merge All {len(all_pdfs)} PDFs into One", key="merge_all_btn", type="secondary")

            if merge_btn:
                merge_status = st.empty()
                merge_prog   = st.progress(0)

                def _cb(done, total):
                    merge_prog.progress(done / total)
                    merge_status.markdown(
                        f'<div style="font-size:12px;color:rgba(255,255,255,0.5);">Merging {done}/{total} PDFs...</div>',
                        unsafe_allow_html=True
                    )

                merged_bytes, ok_count, fail_count, fail_titles = merge_article_pdfs(a2, progress_callback=_cb)
                merge_prog.empty()
                merge_status.empty()

                if merged_bytes:
                    st.session_state.merged_pdf_bytes = merged_bytes
                    st.session_state.merged_pdf_name = f"siemens_articles_merged_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
                    st.success(f"✅ Merged {ok_count} PDFs successfully" + (f" — {fail_count} failed to download" if fail_count else ""))
                else:
                    st.error("❌ Could not merge any PDFs — all downloads failed.")
                st.rerun()

            if st.session_state.merged_pdf_bytes:
                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                st.download_button(
                    f"⬇  Download Merged PDF ({round(len(st.session_state.merged_pdf_bytes)/1024)} KB)",
                    data=st.session_state.merged_pdf_bytes,
                    file_name=st.session_state.merged_pdf_name,
                    mime="application/pdf",
                )

        st.markdown('<div class="sec">Article List</div>', unsafe_allow_html=True)

        if all_pdfs:
            st.markdown(f'<div style="padding:14px 20px;background:rgba(0,255,191,0.06);border:1px solid rgba(0,255,191,0.2);border-left:4px solid #00ffbf;font-size:13px;color:rgba(255,255,255,0.7);margin-bottom:14px;"><b style="color:#00ffbf;">{len(all_pdfs)} PDFs found</b> — Download links available per article in the table below.</div>', unsafe_allow_html=True)

        rows = ""
        for i, a in enumerate(a2[:80], 1):
            cat = a.get("category", "Siemens AG")
            sty = CAT.get(cat, DEF)
            title = a.get("title", "")[:85]
            url   = a.get("url", "#")
            rows += f"""<tr>
                <td style="color:rgba(255,255,255,0.22);font-size:11px;width:36px;">{i:02d}</td>
                <td style="color:#00ffbf;font-weight:600;white-space:nowrap;width:124px;">{a.get('date','—')}</td>
                <td><a href="{url}" target="_blank" style="color:#ffffff;font-weight:500;font-size:13px;text-decoration:none;">{title}</a></td>
                <td style="width:155px;"><span style="display:inline-block;font-size:10px;font-weight:700;padding:3px 10px;white-space:nowrap;{sty}">{cat}</span></td>
                <td style="width:72px;text-align:center;">{pdf_btn(a.get('pdf_url',''))}</td>
            </tr>"""

        tbl_html = f"""<!DOCTYPE html><html><head><style>
        *{{box-sizing:border-box;margin:0;padding:0;}}
        body{{background:#000028;font-family:'Segoe UI',sans-serif;}}
        .wrap{{border:1px solid rgba(255,255,255,0.09);background:rgba(255,255,255,0.04);overflow:hidden;}}
        .hd{{padding:14px 20px;border-bottom:1px solid rgba(255,255,255,0.07);background:rgba(255,255,255,0.025);display:flex;align-items:center;justify-content:space-between;}}
        .hd-title{{font-size:14px;font-weight:700;color:#fff;}}
        .badge{{background:rgba(0,255,191,0.1);color:#00ffbf;border:1px solid rgba(0,255,191,0.25);font-size:10px;font-weight:700;padding:3px 11px;letter-spacing:1.2px;text-transform:uppercase;}}
        table{{width:100%;border-collapse:collapse;}}
        th{{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;color:rgba(255,255,255,0.5);padding:11px 16px;text-align:left;border-bottom:1px solid rgba(255,255,255,0.08);background:rgba(255,255,255,0.02);}}
        td{{padding:12px 16px;font-size:13px;color:rgba(255,255,255,0.85);border-bottom:1px solid rgba(255,255,255,0.045);vertical-align:middle;}}
        tr:last-child td{{border-bottom:none;}}
        tr:hover td{{background:rgba(0,255,191,0.04);}}
        </style></head><body>
        <div class="wrap">
          <div class="hd"><span class="hd-title">Scraped Articles</span><span class="badge">{len(a2)} Results</span></div>
          <div style="overflow-x:auto;">
            <table>
              <thead><tr><th>#</th><th>Date</th><th>Title</th><th>Category</th><th>PDF</th></tr></thead>
              <tbody>{rows}</tbody>
            </table>
          </div>
        </div>
        </body></html>"""

        components.html(tbl_html, height=min(80 + len(a2[:80]) * 54, 680), scrolling=True)

        if len(a2) > 80:
            st.markdown(f'<div style="font-size:12px;color:rgba(255,255,255,0.22);margin-top:8px;">Showing 80 of {len(a2)} — see Article Explorer tab for full view.</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# TAB 2 — PDF DATE CHECK
# ══════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="page">', unsafe_allow_html=True)
    col_l, col_r = st.columns([1, 1], gap="large")

    with col_l:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-hd"><span class="card-title">📄 Upload PDF Report</span><span class="bg-teal">Auto-Detect</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="card-body">', unsafe_allow_html=True)
        st.markdown('<p style="font-size:14px;color:rgba(255,255,255,0.45);line-height:1.8;margin-bottom:20px;">Drag and drop a Siemens Press Intelligence PDF. The app automatically extracts all dates, detects the full coverage window, and verifies article count.</p>', unsafe_allow_html=True)
        uploaded = st.file_uploader("Drop your PDF here or click to browse", type=["pdf"], label_visibility="visible")
        st.markdown('</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-hd"><span class="card-title">📅 Date Range Filter</span><span class="bg-grey">Optional</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="card-body">', unsafe_allow_html=True)
        st.markdown('<p style="font-size:13px;color:rgba(255,255,255,0.36);line-height:1.7;margin-bottom:20px;">Select a date range to filter articles loaded from the Live Scraper.</p>', unsafe_allow_html=True)

        dc1, dc2 = st.columns(2, gap="medium")
        with dc1: pdf_fs = st.date_input("From Date", value=date(2024, 1, 1), key="pdf_fs")
        with dc2: pdf_fe = st.date_input("To Date",   value=date.today(),     key="pdf_fe")

        if st.session_state.scraped_articles:
            filt = [a for a in st.session_state.scraped_articles
                    if (lambda d: d and pdf_fs <= d <= pdf_fe)(parse_d(a.get("date", "")))]
            fvd = sorted([d for d in [parse_d(a.get("date", "")) for a in filt] if d])
            span_txt = f"{fvd[0].strftime('%d %b %Y')} → {fvd[-1].strftime('%d %b %Y')}" if fvd else "—"
            st.markdown(f"""
            <div class="ibox" style="margin-top:16px;">
                <div class="ibox-num">{len(filt)}</div>
                <div class="ibox-txt"><strong>Articles in Range</strong>{span_txt}</div>
            </div>
            """, unsafe_allow_html=True)
            if filt:
                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                st.download_button("⬇  Export Filtered CSV",
                    data=pd.DataFrame(filt).to_csv(index=False).encode(),
                    file_name=f"filtered_{pdf_fs}_{pdf_fe}.csv", mime="text/csv")
        else:
            st.markdown('<div style="margin-top:14px;padding:14px 18px;background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);font-size:12px;color:rgba(255,255,255,0.22);">Run the Live Scraper first to enable date filtering.</div>', unsafe_allow_html=True)

        st.markdown('</div></div>', unsafe_allow_html=True)

    with col_r:
        if uploaded:
            pdf_bytes = uploaded.read()
            text = ""
            try:
                import pdfplumber
                with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                    for page in pdf.pages[:25]:
                        t = page.extract_text()
                        if t: text += t + "\n"
            except Exception:
                try:
                    import PyPDF2
                    reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
                    for page in reader.pages[:25]:
                        text += (page.extract_text() or "") + "\n"
                except Exception:
                    text = pdf_bytes.decode("latin-1", errors="ignore")

            pats = [
                r'\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b',
                r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',
                r'\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}\b',
                r'\b\d{4}-\d{2}-\d{2}\b',
            ]
            found = []
            for p in pats:
                found.extend(re.findall(p, text, re.IGNORECASE))

            def tp(d):
                for fmt in ["%d %B %Y", "%B %d %Y", "%B %d, %Y", "%d %b %Y", "%Y-%m-%d"]:
                    try: return datetime.strptime(d.strip(), fmt).date()
                    except: pass
                return None

            pdates    = sorted(set(filter(None, [tp(d) for d in found])))
            art_count = len(re.findall(r'^\d{2}\s+', text, re.MULTILINE))

            if pdates:
                mn2, mx2 = min(pdates), max(pdates)
                s2 = (mx2 - mn2).days
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('<div class="card-hd"><span class="card-title">✅ PDF Analysis Result</span><span class="bg-teal">Dates Detected</span></div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="card-body">
                    <div class="dbanner" style="flex-direction:column;align-items:flex-start;gap:20px;margin-bottom:22px;">
                        <div style="display:flex;gap:18px;align-items:center;width:100%;">
                            <div><div class="db-lbl">📅 Earliest Date</div><div class="db-val" style="font-size:21px;">{mn2.strftime("%d %B %Y")}</div></div>
                            <div class="db-arrow" style="font-size:26px;">→</div>
                            <div><div class="db-lbl">📅 Latest Date</div><div class="db-val" style="font-size:21px;">{mx2.strftime("%d %B %Y")}</div></div>
                        </div>
                        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:14px;width:100%;padding-top:14px;border-top:1px solid rgba(255,255,255,0.07);">
                            <div><div class="db-lbl">Span</div><div class="db-val teal">{s2} days</div></div>
                            <div><div class="db-lbl">Unique Dates</div><div class="db-val teal">{len(pdates)}</div></div>
                            <div><div class="db-lbl">Articles Est.</div><div class="db-val teal">{art_count if art_count else '—'}</div></div>
                            <div><div class="db-lbl">File Size</div><div class="db-val">{round(len(pdf_bytes)/1024)} KB</div></div>
                        </div>
                    </div>
                    <div class="sec" style="margin-top:0;margin-bottom:12px;">All Dates Found in PDF</div>
                """, unsafe_allow_html=True)

                date_rows = "".join(
                    f'<tr>'
                    f'<td style="color:rgba(255,255,255,0.22);font-size:11px;width:36px;">{i:02d}</td>'
                    f'<td style="font-weight:700;color:#ffffff;font-size:14px;">{d.strftime("%d %B %Y")}</td>'
                    f'<td style="color:rgba(255,255,255,0.38);">{d.strftime("%A")}</td>'
                    f'<td style="color:#00ffbf;font-weight:700;">{d.strftime("%Y")}</td>'
                    f'</tr>'
                    for i, d in enumerate(pdates, 1)
                )
                st.markdown(
                    f'<div style="overflow-y:auto;max-height:300px;">'
                    f'<table class="tbl"><thead><tr><th>#</th><th>Full Date</th><th>Day</th><th>Year</th></tr></thead>'
                    f'<tbody>{date_rows}</tbody></table></div></div></div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown('<div class="wbox"><div class="wbox-t">⚠ No Dates Detected</div><div class="wbox-b">This PDF may be image-based (scanned) or uses a non-standard date format. Try OCR processing first.</div></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="empty"><div class="empty-i">📄</div><div class="empty-t">No PDF Uploaded Yet</div><div class="empty-s">Upload a Siemens Press Intelligence PDF on the left to see date range analysis and article count here.</div></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# TAB 3 — ARTICLE EXPLORER
# ══════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="page">', unsafe_allow_html=True)
    all_arts = st.session_state.scraped_articles

    if not all_arts:
        st.markdown('<div class="empty"><div class="empty-i">🌐</div><div class="empty-t">No Articles Loaded</div><div class="empty-s">Run the Live Scraper in Tab 1 first to populate this explorer.</div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="fbar">', unsafe_allow_html=True)
        st.markdown('<div class="fbar-title">🔍 Filter & Search Articles</div>', unsafe_allow_html=True)

        fc1, fc2, fc3, fc4 = st.columns([1, 1, 1, 1], gap="medium")
        with fc1: f_s = st.date_input("From Date", value=date(2024, 1, 1), key="ex_fs")
        with fc2: f_e = st.date_input("To Date",   value=date.today(),     key="ex_fe")
        with fc3:
            c_opts = ["All Categories"] + sorted(set(a.get("category", "") for a in all_arts))
            sel_c  = st.selectbox("Category", c_opts)
        with fc4:
            srch = st.text_input("Search Title", placeholder="e.g. digital twin...", key="srch")

        st.markdown('</div>', unsafe_allow_html=True)

        filtered = [
            a for a in all_arts
            if (lambda d: not d or (f_s <= d <= f_e))(parse_d(a.get("date", "")))
            and (sel_c in ["All Categories", "All"] or a.get("category") == sel_c)
            and (not srch or srch.lower() in a.get("title", "").lower())
        ]

        fvd3 = sorted([d for d in [parse_d(a.get("date", "")) for a in filtered] if d])
        f_mn = fvd3[0].strftime("%d %b %Y")  if fvd3 else "—"
        f_mx = fvd3[-1].strftime("%d %b %Y") if fvd3 else "—"

        c1, c2, c3 = st.columns(3, gap="medium")
        with c1: st.markdown(f'<div class="kpi"><div class="kpi-val">{len(filtered)}</div><div class="kpi-lbl">Matching Articles</div></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="kpi w"><div class="kpi-val dt">{f_mn}</div><div class="kpi-lbl">Earliest in Filter</div></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="kpi g"><div class="kpi-val dt">{f_mx}</div><div class="kpi-lbl">Latest in Filter</div></div>', unsafe_allow_html=True)

        # ── PDF Merge by date range ──────────────────────
        filtered_pdfs = [a for a in filtered if a.get("pdf_url")]
        if filtered_pdfs:
            st.markdown('<div class="sec">Merge Filtered PDFs</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="merge-box">
                <div class="merge-txt">
                    <strong>📎 {len(filtered_pdfs)} PDFs in selected range</strong>
                    {f_mn} → {f_mx}{' · ' + sel_c if sel_c not in ['All Categories','All'] else ''}
                </div>
            </div>
            """, unsafe_allow_html=True)

            merge_filt_btn = st.button(
                f"🔗  Merge {len(filtered_pdfs)} Filtered PDFs into One",
                key="merge_filtered_btn", type="secondary"
            )

            if merge_filt_btn:
                mf_status = st.empty()
                mf_prog   = st.progress(0)

                def _cb2(done, total):
                    mf_prog.progress(done / total)
                    mf_status.markdown(
                        f'<div style="font-size:12px;color:rgba(255,255,255,0.5);">Merging {done}/{total} PDFs...</div>',
                        unsafe_allow_html=True
                    )

                merged_bytes2, ok2, fail2, fail_titles2 = merge_article_pdfs(filtered, progress_callback=_cb2)
                mf_prog.empty()
                mf_status.empty()

                if merged_bytes2:
                    st.session_state.merged_pdf_bytes = merged_bytes2
                    st.session_state.merged_pdf_name = f"siemens_filtered_{f_s}_{f_e}.pdf"
                    st.success(f"✅ Merged {ok2} PDFs successfully" + (f" — {fail2} failed" if fail2 else ""))
                else:
                    st.error("❌ Could not merge any PDFs — all downloads failed.")
                st.rerun()

            if st.session_state.merged_pdf_bytes:
                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                st.download_button(
                    f"⬇  Download Merged PDF ({round(len(st.session_state.merged_pdf_bytes)/1024)} KB)",
                    data=st.session_state.merged_pdf_bytes,
                    file_name=st.session_state.merged_pdf_name,
                    mime="application/pdf",
                    key="dl_merged_explorer"
                )

        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

        if filtered:
            st.markdown('<div class="sec">Filtered Results</div>', unsafe_allow_html=True)

            rows = ""
            for i, a in enumerate(filtered, 1):
                cat  = a.get("category", "Siemens AG")
                sty  = CAT.get(cat, DEF)
                snip = (a.get("body", "") or a.get("summary", ""))[:88]
                snip_html = f'<div style="font-size:11px;color:rgba(255,255,255,0.35);margin-top:3px;">{snip}{"..." if len(snip)==88 else ""}</div>' if snip else ""
                rows += f"""<tr>
                    <td style="color:rgba(255,255,255,0.2);font-size:11px;width:36px;">{i:02d}</td>
                    <td style="color:#00ffbf;font-weight:600;white-space:nowrap;width:124px;">{a.get('date','—')}</td>
                    <td>
                        <a href="{a.get('url','#')}" target="_blank" style="color:#fff;font-weight:600;font-size:13px;text-decoration:none;">{a.get('title','')[:88]}</a>
                        {snip_html}
                    </td>
                    <td style="width:155px;"><span style="display:inline-block;font-size:10px;font-weight:700;padding:3px 10px;white-space:nowrap;{sty}">{cat}</span></td>
                    <td style="width:72px;text-align:center;">{pdf_btn(a.get('pdf_url',''))}</td>
                </tr>"""

            tbl_html2 = f"""<!DOCTYPE html><html><head><style>
            *{{box-sizing:border-box;margin:0;padding:0;}}
            body{{background:#000028;font-family:'Segoe UI',sans-serif;}}
            .wrap{{border:1px solid rgba(255,255,255,0.09);background:rgba(255,255,255,0.04);overflow:hidden;}}
            .hd{{padding:14px 20px;border-bottom:1px solid rgba(255,255,255,0.07);background:rgba(255,255,255,0.025);display:flex;align-items:center;justify-content:space-between;}}
            .hd-title{{font-size:14px;font-weight:700;color:#fff;}}
            .badge{{background:rgba(0,255,191,0.1);color:#00ffbf;border:1px solid rgba(0,255,191,0.25);font-size:10px;font-weight:700;padding:3px 11px;letter-spacing:1.2px;text-transform:uppercase;}}
            table{{width:100%;border-collapse:collapse;}}
            th{{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;color:rgba(255,255,255,0.5);padding:11px 16px;text-align:left;border-bottom:1px solid rgba(255,255,255,0.08);background:rgba(255,255,255,0.02);}}
            td{{padding:13px 16px;font-size:13px;color:rgba(255,255,255,0.85);border-bottom:1px solid rgba(255,255,255,0.045);vertical-align:middle;}}
            tr:last-child td{{border-bottom:none;}}
            tr:hover td{{background:rgba(0,255,191,0.04);}}
            </style></head><body>
            <div class="wrap">
              <div class="hd"><span class="hd-title">Articles</span><span class="badge">{len(filtered)} Results</span></div>
              <div style="overflow-x:auto;">
                <table>
                  <thead><tr><th>#</th><th>Date</th><th>Title</th><th>Category</th><th>PDF</th></tr></thead>
                  <tbody>{rows}</tbody>
                </table>
              </div>
            </div>
            </body></html>"""

            components.html(tbl_html2, height=min(80 + len(filtered) * 58, 700), scrolling=True)

            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            st.download_button(
                "⬇  Export Filtered Articles (CSV)",
                data=pd.DataFrame(filtered).to_csv(index=False).encode(),
                file_name=f"filtered_{f_s}_{f_e}.csv",
                mime="text/csv",
            )
        else:
            st.markdown('<div style="padding:60px;text-align:center;background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);"><div style="font-size:14px;color:rgba(255,255,255,0.26);">No articles match the current filters.<br>Try adjusting the date range, category or search term.</div></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
