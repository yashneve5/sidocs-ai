"""
SiDocs AI – Siemens Press Intelligence
Exact Siemens.com design: #000028 bg, white text, #00ffbf teal CTA
Full professional layout with perfect padding and visibility
"""

import streamlit as st
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

/* ══════════════════════════════════════════
   GLOBAL RESET — Siemens.com dark base
══════════════════════════════════════════ */
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

/* ══════════════════════════════════════════
   TOP NAV — exact Siemens.com style
══════════════════════════════════════════ */
.nav {
    background: #000028;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    padding: 0 60px;
    height: 70px;
    display: flex; align-items: center; justify-content: space-between;
    position: sticky; top: 0; z-index: 1000;
}
.nav-logo {
    font-size: 24px; font-weight: 900;
    color: #ffffff; letter-spacing: 3px;
    text-transform: uppercase;
}
.nav-links { display: flex; gap: 36px; align-items: center; }
.nav-link {
    font-size: 14px; font-weight: 400;
    color: rgba(255,255,255,0.65);
    border-bottom: 2px solid transparent;
    padding-bottom: 2px; cursor: pointer;
    transition: color 0.2s;
}
.nav-link:hover { color: #ffffff; }
.nav-right { display: flex; align-items: center; gap: 24px; }
.nav-right-txt { font-size: 13px; color: rgba(255,255,255,0.55); }
.nav-sep { width: 1px; height: 20px; background: rgba(255,255,255,0.12); }
.nav-login-btn {
    font-size: 13px; font-weight: 600; color: #ffffff;
    border: 1.5px solid rgba(255,255,255,0.3);
    padding: 7px 18px; cursor: pointer;
    transition: border-color 0.2s;
}
.nav-login-btn:hover { border-color: #00ffbf; color: #00ffbf; }

/* ══════════════════════════════════════════
   SUB-NAV (secondary menu strip)
══════════════════════════════════════════ */
.subnav {
    background: #000028;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    padding: 0 60px;
    display: flex; gap: 0; align-items: center;
}
.subnav-item {
    font-size: 13px; font-weight: 500; color: rgba(255,255,255,0.5);
    padding: 14px 20px; cursor: pointer;
    border-bottom: 2px solid transparent;
    transition: all 0.2s;
}
.subnav-item:hover { color: #ffffff; border-bottom-color: rgba(0,255,191,0.5); }
.subnav-item.active { color: #ffffff; border-bottom-color: #00ffbf; font-weight: 600; }

/* ══════════════════════════════════════════
   HERO — full-width Siemens.com hero section
══════════════════════════════════════════ */
.hero {
    background: #000028;
    padding: 80px 60px 70px 60px;
    position: relative; overflow: hidden;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    min-height: 380px;
    display: flex; flex-direction: column; justify-content: center;
}
.hero::before {
    content: '';
    position: absolute; top: -120px; right: -100px;
    width: 600px; height: 600px;
    background: radial-gradient(ellipse, rgba(0,160,140,0.13) 0%, transparent 65%);
    pointer-events: none;
}
.hero::after {
    content: '';
    position: absolute; bottom: -100px; left: 45%;
    width: 500px; height: 500px;
    background: radial-gradient(ellipse, rgba(0,40,120,0.1) 0%, transparent 65%);
    pointer-events: none;
}
.hero-kicker {
    font-size: 11px; font-weight: 700; letter-spacing: 3px;
    text-transform: uppercase; color: #00ccaa;
    margin-bottom: 20px;
}
.hero-title {
    font-size: 52px; font-weight: 800; color: #ffffff;
    line-height: 1.1; margin-bottom: 22px;
    max-width: 720px; letter-spacing: -0.5px;
}
.hero-title em { color: #00ffbf; font-style: normal; }
.hero-body {
    font-size: 17px; color: rgba(255,255,255,0.55);
    line-height: 1.8; max-width: 560px;
    font-weight: 300; margin-bottom: 44px;
}
.hero-cta {
    display: inline-block;
    background: #00ffbf; color: #000028;
    font-size: 15px; font-weight: 700;
    padding: 15px 36px; cursor: pointer;
    letter-spacing: 0.4px;
    border: none; outline: none;
    text-decoration: none;
}
.hero-cta:hover { background: #00e6aa; }
.hero-stats {
    display: flex; gap: 60px;
    margin-top: 60px; padding-top: 40px;
    border-top: 1px solid rgba(255,255,255,0.07);
}
.hs-val {
    font-size: 40px; font-weight: 900; color: #00ffbf;
    line-height: 1; letter-spacing: -1px;
}
.hs-val.md { font-size: 20px; font-weight: 700; padding-top: 8px; color: #ffffff; }
.hs-label {
    font-size: 10px; font-weight: 700; color: rgba(255,255,255,0.32);
    text-transform: uppercase; letter-spacing: 1.8px; margin-top: 7px;
}

/* ══════════════════════════════════════════
   CONTENT AREA
══════════════════════════════════════════ */
.content { background: #000028; padding: 44px 60px 80px 60px; }

/* ══════════════════════════════════════════
   TABS — Siemens.com tab style
══════════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid rgba(255,255,255,0.08) !important;
    gap: 0 !important; padding: 0 !important;
    margin: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: rgba(255,255,255,0.45) !important;
    font-weight: 500 !important; font-size: 14px !important;
    padding: 16px 32px !important;
    border: none !important;
    border-bottom: 3px solid transparent !important;
    margin-bottom: -1px !important;
    letter-spacing: 0.1px !important;
    transition: all 0.2s !important;
}
.stTabs [data-baseweb="tab"]:hover { color: rgba(255,255,255,0.8) !important; }
.stTabs [aria-selected="true"] {
    color: #ffffff !important; font-weight: 700 !important;
    border-bottom: 3px solid #00ffbf !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: transparent !important; padding: 0 !important;
}
.stTabs [data-baseweb="tab-highlight"] { background: transparent !important; }

/* ══════════════════════════════════════════
   CARDS
══════════════════════════════════════════ */
.card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.09);
    margin-bottom: 24px; overflow: hidden;
}
.card-header {
    padding: 16px 24px 15px 24px;
    border-bottom: 1px solid rgba(255,255,255,0.07);
    background: rgba(255,255,255,0.025);
    display: flex; align-items: center; justify-content: space-between;
}
.card-title {
    font-size: 14px; font-weight: 700; color: #ffffff;
    letter-spacing: 0.1px;
}
.card-body { padding: 28px 24px; }

/* ══════════════════════════════════════════
   BADGES
══════════════════════════════════════════ */
.badge-green {
    display: inline-block;
    background: rgba(0,255,191,0.1); color: #00ffbf;
    border: 1px solid rgba(0,255,191,0.25);
    font-size: 10px; font-weight: 700;
    padding: 3px 12px; letter-spacing: 1.2px;
    text-transform: uppercase;
}
.badge-grey {
    display: inline-block;
    background: rgba(255,255,255,0.06); color: rgba(255,255,255,0.45);
    border: 1px solid rgba(255,255,255,0.1);
    font-size: 10px; font-weight: 700;
    padding: 3px 12px; letter-spacing: 1.2px;
    text-transform: uppercase;
}

/* ══════════════════════════════════════════
   KPI METRIC CARDS
══════════════════════════════════════════ */
.kpi-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 16px; margin: 28px 0; }
.kpi {
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.08);
    border-top: 3px solid #00ffbf;
    padding: 24px 22px 20px 22px;
}
.kpi.b  { border-top-color: #0099dd; }
.kpi.g  { border-top-color: #00cc88; }
.kpi.w  { border-top-color: rgba(255,255,255,0.22); }
.kpi-val {
    font-size: 36px; font-weight: 900; color: #00ffbf;
    line-height: 1; margin-bottom: 8px; letter-spacing: -1px;
}
.kpi-val.dt { font-size: 16px; font-weight: 700; color: #ffffff; line-height: 1.4; padding-top: 7px; letter-spacing: 0; }
.kpi-label {
    font-size: 10px; font-weight: 700; color: rgba(255,255,255,0.32);
    text-transform: uppercase; letter-spacing: 1.5px;
}

/* ══════════════════════════════════════════
   DATE RANGE BANNER
══════════════════════════════════════════ */
.date-banner {
    background: rgba(0,255,191,0.05);
    border: 1px solid rgba(0,255,191,0.16);
    border-left: 4px solid #00ffbf;
    padding: 24px 32px;
    display: flex; align-items: center; gap: 40px;
    flex-wrap: wrap; margin: 0 0 24px 0;
}
.db-block {}
.db-label { font-size: 10px; font-weight: 700; color: rgba(255,255,255,0.32); text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 6px; }
.db-value { font-size: 20px; font-weight: 700; color: #ffffff; }
.db-value.teal { color: #00ffbf; }
.db-arrow { font-size: 24px; color: rgba(0,255,191,0.6); flex-shrink: 0; }

/* ══════════════════════════════════════════
   SECTION DIVIDER LABEL
══════════════════════════════════════════ */
.sec-label {
    font-size: 10px; font-weight: 700; color: rgba(255,255,255,0.28);
    text-transform: uppercase; letter-spacing: 2px;
    margin: 36px 0 14px 0;
    display: flex; align-items: center; gap: 14px;
}
.sec-label::after { content:''; flex:1; height:1px; background:rgba(255,255,255,0.06); }

/* ══════════════════════════════════════════
   TERMINAL LOG
══════════════════════════════════════════ */
.terminal {
    background: #00001c;
    border: 1px solid rgba(0,255,191,0.1);
    padding: 20px 22px;
    font-family: 'Courier New', monospace;
    font-size: 12.5px; line-height: 1.9;
    min-height: 200px; max-height: 320px; overflow-y: auto;
    color: #00ffbf;
}
.t-ok   { color: #00ffbf; }
.t-info { color: #60c8e8; }
.t-warn { color: #ffd166; }
.t-err  { color: #ff6b6b; }
.t-dim  { color: rgba(255,255,255,0.18); }

/* ══════════════════════════════════════════
   DATA TABLE
══════════════════════════════════════════ */
.si-table { width: 100%; border-collapse: collapse; }
.si-table th {
    font-size: 10px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 1.5px; color: rgba(255,255,255,0.6);
    padding: 12px 18px; text-align: left;
    border-bottom: 1px solid rgba(255,255,255,0.07);
    background: rgba(255,255,255,0.02);
}
.si-table td {
    padding: 14px 18px; font-size: 13px;
    color: #ffffff;
    border-bottom: 1px solid rgba(255,255,255,0.045);
    vertical-align: middle;
}
.si-table tr:last-child td { border-bottom: none; }
.si-table tr:hover td { background: rgba(0,255,191,0.04); }
.td-num  { color: rgba(255,255,255,0.2) !important; font-size: 11px !important; width: 40px !important; }
.td-date { color: #00ffbf !important; font-weight: 600 !important; white-space: nowrap !important; width: 130px !important; }
.td-title { font-weight: 500 !important; color: #ffffff !important; }
.td-snip  { font-size: 11px !important; color: rgba(255,255,255,0.55) !important; margin-top: 3px !important; }
.cat-tag {
    display: inline-block; font-size: 10px; font-weight: 700;
    padding: 3px 10px; letter-spacing: 0.4px;
    white-space: nowrap;
}

/* ══════════════════════════════════════════
   SMALL INFO BOXES
══════════════════════════════════════════ */
.info-box {
    background: rgba(0,255,191,0.05);
    border: 1px solid rgba(0,255,191,0.14);
    border-left: 3px solid #00ffbf;
    padding: 18px 22px; margin: 14px 0;
    display: flex; align-items: center; gap: 16px;
}
.info-box-num { font-size: 36px; font-weight: 900; color: #00ffbf; line-height: 1; }
.info-box-txt { font-size: 13px; color: rgba(255,255,255,0.5); line-height: 1.5; }
.info-box-txt strong { color: #ffffff; display: block; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 2px; }

.warn-box {
    background: rgba(255,107,107,0.06);
    border: 1px solid rgba(255,107,107,0.18);
    border-left: 3px solid #ff6b6b;
    padding: 18px 22px;
}
.warn-box-title { font-size: 14px; font-weight: 700; color: #ff6b6b; margin-bottom: 6px; }
.warn-box-body  { font-size: 13px; color: rgba(255,255,255,0.45); line-height: 1.6; }

.empty-state {
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    min-height: 380px; text-align: center;
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    padding: 60px 40px;
}
.empty-icon { font-size: 56px; opacity: 0.18; margin-bottom: 20px; }
.empty-title { font-size: 20px; font-weight: 800; color: #ffffff; margin-bottom: 10px; }
.empty-sub   { font-size: 14px; color: rgba(255,255,255,0.3); line-height: 1.7; max-width: 320px; }

/* ══════════════════════════════════════════
   CFG MINI BOXES
══════════════════════════════════════════ */
.cfg-grid { display: grid; grid-template-columns:1fr 1fr; gap:10px; margin-top:16px; }
.cfg-box {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    padding: 14px 16px;
}
.cfg-label { font-size: 9px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.3px; color: rgba(255,255,255,0.3); margin-bottom: 5px; }
.cfg-val   { font-size: 22px; font-weight: 800; color: #00ffbf; line-height: 1; }
.cfg-val.sm { font-size: 12px; font-weight: 600; color: #00ffbf; }

/* ══════════════════════════════════════════
   FILTER BAR
══════════════════════════════════════════ */
.filter-bar {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 22px 24px 24px 24px; margin-bottom: 24px;
}
.filter-title { font-size: 10px; font-weight: 700; color: rgba(255,255,255,0.3); text-transform: uppercase; letter-spacing: 1.8px; margin-bottom: 18px; }

/* ══════════════════════════════════════════
   STREAMLIT WIDGETS — ALL DARK
══════════════════════════════════════════ */

/* Buttons */
.stButton > button {
    background: #00ffbf !important; color: #000028 !important;
    font-weight: 700 !important; font-size: 14px !important;
    border: none !important; border-radius: 0 !important;
    padding: 14px 32px !important; width: 100% !important;
    letter-spacing: 0.4px !important; cursor: pointer !important;
    transition: background 0.15s !important;
}
.stButton > button:hover { background: #00e0aa !important; }
.stButton > button:focus { box-shadow: none !important; outline: 2px solid rgba(0,255,191,0.4) !important; }

.stDownloadButton > button {
    background: transparent !important; color: #00ffbf !important;
    border: 1.5px solid rgba(0,255,191,0.45) !important;
    font-weight: 700 !important; font-size: 13px !important;
    border-radius: 0 !important;
    padding: 13px 28px !important; width: 100% !important;
}
.stDownloadButton > button:hover { background: rgba(0,255,191,0.07) !important; }

/* All labels */
label,
.stSelectbox label,
.stNumberInput label,
.stDateInput label,
.stCheckbox label,
.stTextInput label {
    color: rgba(255,255,255,0.38) !important;
    font-size: 10px !important; font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 1.3px !important;
    margin-bottom: 7px !important;
    display: block !important;
}

/* Date inputs */
.stDateInput > div { width: 100% !important; }
.stDateInput input, input[type="date"] {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.16) !important;
    border-radius: 0 !important;
    color: #ffffff !important;
    font-size: 15px !important; font-weight: 600 !important;
    padding: 13px 16px !important;
    width: 100% !important;
    outline: none !important;
    -webkit-text-fill-color: #ffffff !important;
}
.stDateInput input:focus, input[type="date"]:focus {
    border-color: rgba(0,255,191,0.5) !important;
    background: rgba(255,255,255,0.09) !important;
}
/* Kill the white calendar popup */
[data-baseweb="popover"] { background: #000a38 !important; }
[data-baseweb="calendar"] { background: #000a38 !important; border: 1px solid rgba(0,255,191,0.18) !important; }
[data-baseweb="calendar"] * { color: #ffffff !important; }
[data-baseweb="calendar"] button { background: transparent !important; color: #ffffff !important; border: none !important; }
[data-baseweb="calendar"] [aria-selected="true"] { background: #00ffbf !important; color: #000028 !important; }
[data-baseweb="calendar"] [data-testid="day"]:hover { background: rgba(0,255,191,0.15) !important; }

/* Number input */
.stNumberInput input {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.16) !important;
    border-radius: 0 !important;
    color: #ffffff !important;
    font-size: 16px !important; font-weight: 700 !important;
    padding: 13px 16px !important;
    -webkit-text-fill-color: #ffffff !important;
}
.stNumberInput input:focus { border-color: rgba(0,255,191,0.5) !important; }
.stNumberInput [data-testid="stNumberInputStepUp"],
.stNumberInput [data-testid="stNumberInputStepDown"] {
    background: rgba(255,255,255,0.07) !important;
    border-color: rgba(255,255,255,0.16) !important;
    color: #ffffff !important;
}

/* Text input */
.stTextInput input {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.16) !important;
    border-radius: 0 !important;
    color: #ffffff !important;
    font-size: 14px !important;
    padding: 13px 16px !important;
    -webkit-text-fill-color: #ffffff !important;
}
.stTextInput input::placeholder { color: rgba(255,255,255,0.22) !important; }
.stTextInput input:focus { border-color: rgba(0,255,191,0.5) !important; }

/* Select dropdown */
div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.16) !important;
    border-radius: 0 !important;
    color: #ffffff !important;
    padding: 6px 2px !important;
    min-height: 48px !important;
}
div[data-baseweb="select"] span,
div[data-baseweb="select"] input { color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; }
div[data-baseweb="select"] svg { fill: rgba(255,255,255,0.45) !important; }
div[data-baseweb="select"] > div:focus-within { border-color: rgba(0,255,191,0.45) !important; }
div[data-baseweb="menu"] { background: #000a38 !important; border: 1px solid rgba(0,255,191,0.15) !important; }
div[data-baseweb="option"] { background: transparent !important; color: rgba(255,255,255,0.8) !important; font-size: 14px !important; padding: 12px 16px !important; }
div[data-baseweb="option"]:hover { background: rgba(0,255,191,0.08) !important; color: #ffffff !important; }

/* Checkbox */
.stCheckbox { margin-top: 6px !important; }
.stCheckbox > label { text-transform: none !important; font-size: 13px !important; font-weight: 400 !important; letter-spacing: 0 !important; color: rgba(255,255,255,0.65) !important; }
.stCheckbox [data-baseweb="checkbox"] > div { background: rgba(255,255,255,0.08) !important; border-color: rgba(255,255,255,0.2) !important; border-radius: 0 !important; }
.stCheckbox input:checked + div { background: #00ffbf !important; border-color: #00ffbf !important; }

/* File uploader */
[data-testid="stFileUploader"] {
    background: rgba(0,255,191,0.03) !important;
    border: 2px dashed rgba(0,255,191,0.25) !important;
    border-radius: 0 !important;
}
[data-testid="stFileUploaderDropzone"] { background: transparent !important; padding: 24px !important; }
[data-testid="stFileUploaderDropzoneInstructions"] { color: rgba(255,255,255,0.5) !important; }
[data-testid="stFileUploaderDropzoneInstructions"] * { color: rgba(255,255,255,0.5) !important; }
[data-testid="stFileUploader"] button {
    background: rgba(255,255,255,0.07) !important;
    color: rgba(255,255,255,0.75) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 0 !important; font-size: 13px !important;
}
[data-testid="stFileUploader"] small { color: rgba(255,255,255,0.25) !important; }
[data-testid="stFileUploader"] label { color: rgba(255,255,255,0.55) !important; font-size: 14px !important; font-weight: 400 !important; text-transform: none !important; letter-spacing: 0 !important; }
[data-testid="stFileUploader"] p { color: rgba(255,255,255,0.45) !important; }

/* Progress */
.stProgress > div > div { background: #00ffbf !important; }
[data-testid="stProgress"] > div { background: rgba(255,255,255,0.07) !important; border-radius: 0 !important; }

/* Expander */
details { background: rgba(255,255,255,0.025) !important; border: 1px solid rgba(255,255,255,0.07) !important; padding: 0 !important; }
summary { color: rgba(255,255,255,0.75) !important; padding: 14px 18px !important; font-size: 13px !important; font-weight: 600 !important; }

/* Alert/info boxes */
.stAlert { border-radius: 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Session ──────────────────────────────────────────────────
for k, v in [("scraped_articles",[]), ("scraper_log",[])]:
    if k not in st.session_state: st.session_state[k] = v

def parse_d(d):
    if not d: return None
    for fmt in ["%d %B %Y","%B %d, %Y","%d %b %Y","%Y-%m-%d"]:
        try: return datetime.strptime(str(d).strip(), fmt).date()
        except: pass
    return None

CAT = {
    "Digital Industries":   "background:rgba(59,130,246,0.18);color:#93c5fd;border:1px solid rgba(59,130,246,0.28);",
    "Smart Infrastructure": "background:rgba(16,185,129,0.18);color:#6ee7b7;border:1px solid rgba(16,185,129,0.28);",
    "Siemens Mobility":     "background:rgba(139,92,246,0.18);color:#c4b5fd;border:1px solid rgba(139,92,246,0.28);",
    "Financial Services":   "background:rgba(245,158,11,0.18);color:#fcd34d;border:1px solid rgba(245,158,11,0.28);",
    "Siemens AG":           "background:rgba(255,255,255,0.07);color:rgba(255,255,255,0.6);border:1px solid rgba(255,255,255,0.12);",
    "AI & Innovation":      "background:rgba(236,72,153,0.18);color:#f9a8d4;border:1px solid rgba(236,72,153,0.28);",
    "Sustainability":       "background:rgba(0,255,191,0.12);color:#00ffbf;border:1px solid rgba(0,255,191,0.25);",
}
DEF_CAT = "background:rgba(255,255,255,0.07);color:rgba(255,255,255,0.6);border:1px solid rgba(255,255,255,0.12);"

arts  = st.session_state.scraped_articles
vd    = sorted([d for d in [parse_d(a.get("date","")) for a in arts] if d])
n_a   = len(arts)
n_c   = len(set(a.get("category","") for a in arts)) if arts else 0
dspan = f"{vd[0].strftime('%d %b %Y')}  →  {vd[-1].strftime('%d %b %Y')}" if vd else "No data yet"

# ══════════════════════════════════════════
# TOP NAV
# ══════════════════════════════════════════
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
        <span class="nav-right-txt">🌐 India | EN</span>
        <span class="nav-right-txt">Support ▾</span>
        <div class="nav-sep"></div>
        <span class="nav-login-btn">SiDocs AI</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# HERO
# ══════════════════════════════════════════
st.markdown(f"""
<div class="hero">
    <div class="hero-kicker">Siemens · Internal Platform · Press Intelligence</div>
    <div class="hero-title">
        Building the intelligence layer<br>for <em>Siemens Press</em>
    </div>
    <div class="hero-body">
        Scrape, analyse and explore Siemens global press releases by date range.
        Upload PDFs for instant date analysis — or run the live scraper to surface
        the latest news across all business units.
    </div>
    <a class="hero-cta">Get started ↓</a>
    <div class="hero-stats">
        <div>
            <div class="hs-val">{n_a}</div>
            <div class="hs-label">Articles Loaded</div>
        </div>
        <div>
            <div class="hs-val">{n_c}</div>
            <div class="hs-label">Categories</div>
        </div>
        <div>
            <div class="hs-val md">{dspan}</div>
            <div class="hs-label">Coverage Window</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# TABS
# ══════════════════════════════════════════
st.markdown('<div style="background:#000028; padding: 0 60px; border-bottom:1px solid rgba(255,255,255,0.06);">', unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs([
    "  🌐  Live Scraper  ",
    "  📄  PDF Upload & Date Check  ",
    "  📊  Article Explorer  ",
])
st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════
# TAB 1 — LIVE SCRAPER
# ══════════════════════════════════════════
with tab1:
    st.markdown('<div class="content">', unsafe_allow_html=True)

    col_cfg, col_log = st.columns([1, 2], gap="large")

    with col_cfg:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header"><span class="card-title">⚙ Scraper Configuration</span><span class="badge-green">ScraperAPI</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="card-body">', unsafe_allow_html=True)

        pages = st.number_input("Pages to Scrape", min_value=1, max_value=20, value=1,
                                help="Each page retrieves approximately 10 articles.")
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        fetch_full = st.checkbox("Fetch Full Article Body", value=False)

        st.markdown(f"""
        <div class="cfg-grid">
            <div class="cfg-box">
                <div class="cfg-label">Target Domain</div>
                <div class="cfg-val sm">press.siemens.com</div>
            </div>
            <div class="cfg-box">
                <div class="cfg-label">Est. Articles</div>
                <div class="cfg-val">{pages * 10}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        run_btn = st.button("▶  Run Scraper")
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        if st.session_state.scraped_articles:
            df_e = pd.DataFrame(st.session_state.scraped_articles)
            st.download_button("⬇  Export All Articles (CSV)",
                data=df_e.to_csv(index=False).encode(),
                file_name=f"siemens_press_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv")

        st.markdown('</div></div>', unsafe_allow_html=True)

    with col_log:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header"><span class="card-title">⬛ Scraper Log</span><span class="badge-green">Live Output</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="card-body">', unsafe_allow_html=True)
        prog_ph = st.empty()
        log_ph  = st.empty()

        def render_log():
            lines = st.session_state.scraper_log
            h = '<div class="terminal">'
            if not lines:
                h += '<div class="t-dim">[--:--:--] SiDocs AI Scraper — Ready.</div>'
                h += '<div class="t-dim">[--:--:--] Configure settings on the left, then press ▶ Run Scraper.</div>'
                h += '<div class="t-dim">[--:--:--] Output will stream here in real time...</div>'
            for ts, k, m in lines:
                h += f'<div class="t-{k}">[{ts}] {m}</div>'
            h += '</div>'
            log_ph.markdown(h, unsafe_allow_html=True)
        render_log()
        st.markdown('</div></div>', unsafe_allow_html=True)

    # Run
    if run_btn:
        st.session_state.scraper_log = []
        st.session_state.scraped_articles = []
        def log(m, k="ok"):
            st.session_state.scraper_log.append((datetime.now().strftime("%H:%M:%S"), k, m))
            render_log()
        log("Initialising SiDocs AI scraper...", "info")
        log(f"Target: press.siemens.com  |  Pages: {pages}  |  Full fetch: {fetch_full}", "info")
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
                    for i, a in enumerate(raw):
                        b = scrape_article_content(a["url"])
                        if b: a["body"] = b
                        log(f"  [{i+1}/{len(raw)}] {a['title'][:55]}...", "ok")
                        prog_ph.progress(40 + int(40*(i+1)/len(raw)))
                log("Detecting categories...", "info")
                for a in raw:
                    a["category"] = detect_category(a["title"], a["url"], a.get("body",""))
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

    # Results
    if st.session_state.scraped_articles:
        a2  = st.session_state.scraped_articles
        vd2 = sorted([d for d in [parse_d(a.get("date","")) for a in a2] if d])
        mn  = vd2[0].strftime("%d %b %Y")  if vd2 else "—"
        mx  = vd2[-1].strftime("%d %b %Y") if vd2 else "—"
        c2  = len(set(a.get("category","") for a in a2))

        st.markdown('<div class="sec-label">Results Overview</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="kpi-grid">
            <div class="kpi">
                <div class="kpi-val">{len(a2)}</div>
                <div class="kpi-label">Articles Scraped</div>
            </div>
            <div class="kpi b">
                <div class="kpi-val">{c2}</div>
                <div class="kpi-label">Categories Found</div>
            </div>
            <div class="kpi w">
                <div class="kpi-val dt">{mn}</div>
                <div class="kpi-label">Earliest Article</div>
            </div>
            <div class="kpi g">
                <div class="kpi-val dt">{mx}</div>
                <div class="kpi-label">Latest Article</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if vd2:
            s = (vd2[-1]-vd2[0]).days
            st.markdown(f"""
            <div class="date-banner">
                <div class="db-block">
                    <div class="db-label">📅 Earliest Article Date</div>
                    <div class="db-value">{vd2[0].strftime("%d %B %Y")}</div>
                </div>
                <div class="db-arrow">→</div>
                <div class="db-block">
                    <div class="db-label">📅 Latest Article Date</div>
                    <div class="db-value">{vd2[-1].strftime("%d %B %Y")}</div>
                </div>
                <div class="db-block">
                    <div class="db-label">Coverage Span</div>
                    <div class="db-value teal">{s} days</div>
                </div>
                <div class="db-block">
                    <div class="db-label">Articles with Dates</div>
                    <div class="db-value teal">{len(vd2)} / {len(a2)}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="sec-label">Article List</div>', unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f'<div class="card-header"><span class="card-title">Scraped Articles</span><span class="badge-green">{len(a2)} Results</span></div>', unsafe_allow_html=True)
        rows = ""
        for i, a in enumerate(a2[:60], 1):
            cat = a.get("category","Siemens AG")
            sty = CAT.get(cat, DEF_CAT)
            rows += f"""<tr>
                <td class="td-num">{i:02d}</td>
                <td class="td-date">{a.get('date','—')}</td>
                <td class="td-title">{a.get('title','')[:90]}</td>
                <td style="width:165px;"><span class="cat-tag" style="{sty}">{cat}</span></td>
            </tr>"""
        st.markdown(f'<div style="overflow-x:auto;"><table class="si-table"><thead><tr><th>#</th><th>Date</th><th>Title</th><th>Category</th></tr></thead><tbody>{rows}</tbody></table></div>', unsafe_allow_html=True)
        if len(a2) > 60:
            st.markdown(f'<div style="padding:12px 18px;font-size:12px;color:rgba(255,255,255,0.22);">Showing 60 of {len(a2)} articles — switch to Article Explorer for full view.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════
# TAB 2 — PDF DATE CHECK
# ══════════════════════════════════════════
with tab2:
    st.markdown('<div class="content">', unsafe_allow_html=True)

    col_l2, col_r2 = st.columns([1, 1], gap="large")

    with col_l2:
        # ── Upload ──
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header"><span class="card-title">📄 Upload PDF Report</span><span class="badge-green">Auto-Detect</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="card-body">', unsafe_allow_html=True)
        st.markdown('<p style="font-size:14px;color:rgba(255,255,255,0.45);line-height:1.8;margin-bottom:20px;">Drag and drop a Siemens Press Intelligence PDF below. The app will automatically extract all dates, detect the full coverage window, and verify article count.</p>', unsafe_allow_html=True)
        uploaded = st.file_uploader("Drop your PDF here or click to browse", type=["pdf"], label_visibility="visible")
        st.markdown('</div></div>', unsafe_allow_html=True)

        # ── Date range filter ──
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header"><span class="card-title">📅 Date Range Filter</span><span class="badge-grey">Optional</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="card-body">', unsafe_allow_html=True)
        st.markdown('<p style="font-size:13px;color:rgba(255,255,255,0.38);line-height:1.7;margin-bottom:20px;">Select a custom date range to filter articles that were loaded from the Live Scraper.</p>', unsafe_allow_html=True)
        dc1, dc2 = st.columns(2, gap="medium")
        with dc1: pdf_fs = st.date_input("From Date", value=date(2024,1,1), key="pdf_fs")
        with dc2: pdf_fe = st.date_input("To Date",   value=date.today(),   key="pdf_fe")

        if st.session_state.scraped_articles:
            filt = [a for a in st.session_state.scraped_articles
                    if (lambda d: d and pdf_fs<=d<=pdf_fe)(parse_d(a.get("date","")))]
            fvd = sorted([d for d in [parse_d(a.get("date","")) for a in filt] if d])
            span_txt = f"{fvd[0].strftime('%d %b %Y')} → {fvd[-1].strftime('%d %b %Y')}" if fvd else "—"
            st.markdown(f"""
            <div class="info-box" style="margin-top:16px;">
                <div class="info-box-num">{len(filt)}</div>
                <div class="info-box-txt">
                    <strong>Articles in Range</strong>
                    {span_txt}
                </div>
            </div>
            """, unsafe_allow_html=True)
            if filt:
                st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
                st.download_button("⬇  Export Filtered CSV",
                    data=pd.DataFrame(filt).to_csv(index=False).encode(),
                    file_name=f"filtered_{pdf_fs}_{pdf_fe}.csv", mime="text/csv")
        else:
            st.markdown('<div style="margin-top:16px;padding:16px 20px;background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);"><span style="font-size:12px;color:rgba(255,255,255,0.22);">Run the Live Scraper first to enable date filtering.</span></div>', unsafe_allow_html=True)

        st.markdown('</div></div>', unsafe_allow_html=True)

    with col_r2:
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

            def tp(d):
                for fmt in ["%d %B %Y","%B %d %Y","%B %d, %Y","%d %b %Y","%Y-%m-%d"]:
                    try: return datetime.strptime(d.strip(), fmt).date()
                    except: pass
                return None

            pdates    = sorted(set(filter(None,[tp(d) for d in found])))
            art_count = len(re.findall(r'^\d{2}\s+', text, re.MULTILINE))

            if pdates:
                mn2, mx2 = min(pdates), max(pdates)
                s2 = (mx2-mn2).days
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('<div class="card-header"><span class="card-title">✅ PDF Analysis Result</span><span class="badge-green">Dates Detected</span></div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="card-body">
                    <div class="date-banner" style="flex-direction:column;align-items:flex-start;gap:20px;margin-bottom:24px;">
                        <div style="display:flex;gap:20px;align-items:center;width:100%;">
                            <div class="db-block">
                                <div class="db-label">📅 Earliest Date in PDF</div>
                                <div class="db-value" style="font-size:22px;">{mn2.strftime("%d %B %Y")}</div>
                            </div>
                            <div class="db-arrow" style="font-size:28px; margin: 0 6px;">→</div>
                            <div class="db-block">
                                <div class="db-label">📅 Latest Date in PDF</div>
                                <div class="db-value" style="font-size:22px;">{mx2.strftime("%d %B %Y")}</div>
                            </div>
                        </div>
                        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px;width:100%;
                                    padding-top:16px;border-top:1px solid rgba(255,255,255,0.07);">
                            <div>
                                <div class="db-label">Span</div>
                                <div class="db-value teal">{s2} days</div>
                            </div>
                            <div>
                                <div class="db-label">Unique Dates</div>
                                <div class="db-value teal">{len(pdates)}</div>
                            </div>
                            <div>
                                <div class="db-label">Articles Est.</div>
                                <div class="db-value teal">{art_count if art_count else '—'}</div>
                            </div>
                            <div>
                                <div class="db-label">File Size</div>
                                <div class="db-value">{round(len(pdf_bytes)/1024)} KB</div>
                            </div>
                        </div>
                    </div>
                    <div class="sec-label" style="margin-top:0; margin-bottom:12px;">All Dates Detected</div>
                """, unsafe_allow_html=True)
                date_rows = "".join(
                    f'<tr>'
                    f'<td class="td-num">{i:02d}</td>'
                    f'<td style="font-weight:700;color:#ffffff;font-size:14px;">{d.strftime("%d %B %Y")}</td>'
                    f'<td style="color:rgba(255,255,255,0.35);font-size:13px;">{d.strftime("%A")}</td>'
                    f'<td style="color:#00ffbf;font-weight:700;font-size:13px;">{d.strftime("%Y")}</td>'
                    f'</tr>'
                    for i,d in enumerate(pdates,1)
                )
                st.markdown(f'<div style="overflow-y:auto;max-height:320px;"><table class="si-table"><thead><tr><th>#</th><th>Full Date</th><th>Day of Week</th><th>Year</th></tr></thead><tbody>{date_rows}</tbody></table></div></div></div>', unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="warn-box" style="margin-top:0;">
                    <div class="warn-box-title">⚠ No Dates Detected</div>
                    <div class="warn-box-body">
                        This PDF may be image-based (scanned) and requires OCR processing,
                        or it uses a non-standard date format not recognised by the parser.
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-icon">📄</div>
                <div class="empty-title">No PDF Uploaded Yet</div>
                <div class="empty-sub">Upload a Siemens Press Intelligence PDF on the left to see full date range analysis and article count here.</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════
# TAB 3 — ARTICLE EXPLORER
# ══════════════════════════════════════════
with tab3:
    st.markdown('<div class="content">', unsafe_allow_html=True)
    all_arts = st.session_state.scraped_articles

    if not all_arts:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">🌐</div>
            <div class="empty-title">No Articles Loaded</div>
            <div class="empty-sub">Run the Live Scraper in Tab 1 first to populate this explorer with articles.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="filter-bar">', unsafe_allow_html=True)
        st.markdown('<div class="filter-title">🔍 Filter & Search Articles</div>', unsafe_allow_html=True)
        fc1, fc2, fc3, fc4 = st.columns([1,1,1,1], gap="medium")
        with fc1: f_s = st.date_input("From Date", value=date(2024,1,1), key="ex_fs")
        with fc2: f_e = st.date_input("To Date",   value=date.today(),   key="ex_fe")
        with fc3:
            c_opts = ["All Categories"] + sorted(set(a.get("category","") for a in all_arts))
            sel_c  = st.selectbox("Category", c_opts)
        with fc4: srch = st.text_input("Search Title", placeholder="e.g. digital twin...", key="srch")
        st.markdown('</div>', unsafe_allow_html=True)

        filtered = [
            a for a in all_arts
            if (lambda d: not d or (f_s<=d<=f_e))(parse_d(a.get("date","")))
            and (sel_c in ["All Categories","All"] or a.get("category")==sel_c)
            and (not srch or srch.lower() in a.get("title","").lower())
        ]
        fvd3 = sorted([d for d in [parse_d(a.get("date","")) for a in filtered] if d])
        f_mn3 = fvd3[0].strftime("%d %b %Y")  if fvd3 else "—"
        f_mx3 = fvd3[-1].strftime("%d %b %Y") if fvd3 else "—"

        c1, c2, c3 = st.columns(3, gap="medium")
        with c1: st.markdown(f'<div class="kpi"><div class="kpi-val">{len(filtered)}</div><div class="kpi-label">Matching Articles</div></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="kpi w"><div class="kpi-val dt">{f_mn3}</div><div class="kpi-label">Earliest in Filter</div></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="kpi g"><div class="kpi-val dt">{f_mx3}</div><div class="kpi-label">Latest in Filter</div></div>', unsafe_allow_html=True)

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

        if filtered:
            st.markdown('<div class="sec-label">Filtered Results</div>', unsafe_allow_html=True)
            rows = ""
            for i, a in enumerate(filtered, 1):
                cat  = a.get("category","Siemens AG")
                sty  = CAT.get(cat, DEF_CAT)
                snip = (a.get("body","") or a.get("summary",""))[:90]
                url  = a.get("url","#")
                snip_html = f'<div style="font-size:11px;color:rgba(255,255,255,0.55);margin-top:3px;">{snip}{"..." if len(snip)==90 else ""}</div>' if snip else ""
                rows += f"""<tr>
                    <td style="padding:14px 18px;font-size:11px;color:rgba(255,255,255,0.3);width:40px;border-bottom:1px solid rgba(255,255,255,0.045);">{i:02d}</td>
                    <td style="padding:14px 18px;font-size:13px;color:#00ffbf;font-weight:600;white-space:nowrap;width:130px;border-bottom:1px solid rgba(255,255,255,0.045);">{a.get('date','&#8212;')}</td>
                    <td style="padding:14px 18px;font-size:13px;color:#ffffff;border-bottom:1px solid rgba(255,255,255,0.045);">
                        <a href="{url}" target="_blank" style="color:#ffffff;font-weight:600;font-size:13px;text-decoration:none;line-height:1.4;">{a.get('title','')[:88]}</a>
                        {snip_html}
                    </td>
                    <td style="padding:14px 18px;width:165px;border-bottom:1px solid rgba(255,255,255,0.045);"><span style="display:inline-block;font-size:10px;font-weight:700;padding:3px 10px;letter-spacing:0.4px;white-space:nowrap;{sty}">{cat}</span></td>
                </tr>"""

            table_html = f"""<!DOCTYPE html>
<html><head><style>
body {{ margin:0; padding:0; background:#000028; font-family:'Segoe UI',sans-serif; }}
table {{ width:100%; border-collapse:collapse; background:#000028; }}
thead tr {{ background:rgba(255,255,255,0.02); }}
th {{ font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:1.5px;
      color:rgba(255,255,255,0.6); padding:12px 18px; text-align:left;
      border-bottom:1px solid rgba(255,255,255,0.1); }}
tr:hover td {{ background:rgba(0,255,191,0.04); }}
.header-bar {{ padding:16px 24px; border-bottom:1px solid rgba(255,255,255,0.07);
               background:rgba(255,255,255,0.025); display:flex; align-items:center;
               justify-content:space-between; }}
.card-title {{ font-size:14px; font-weight:700; color:#ffffff; }}
.badge {{ display:inline-block; background:rgba(0,255,191,0.1); color:#00ffbf;
          border:1px solid rgba(0,255,191,0.25); font-size:10px; font-weight:700;
          padding:3px 12px; letter-spacing:1.2px; text-transform:uppercase; }}
.wrap {{ border:1px solid rgba(255,255,255,0.09); background:rgba(255,255,255,0.04); overflow:hidden; }}
</style></head>
<body>
<div class="wrap">
  <div class="header-bar">
    <span class="card-title">Articles</span>
    <span class="badge">{len(filtered)} Results</span>
  </div>
  <div style="overflow-x:auto;">
    <table>
      <thead><tr><th>#</th><th>Date</th><th>Title</th><th>Category</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
  </div>
</div>
</body></html>"""

            import streamlit.components.v1 as components
            components.html(table_html, height=min(90 + len(filtered) * 62, 700), scrolling=True)

            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            st.download_button("⬇  Export Filtered Articles (CSV)",
                data=pd.DataFrame(filtered).to_csv(index=False).encode(),
                file_name=f"filtered_{f_s}_{f_e}.csv", mime="text/csv")
        else:
            st.markdown('<div style="padding:60px;text-align:center;background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);"><div style="font-size:14px;color:rgba(255,255,255,0.28);">No articles match the current filters.<br>Try adjusting the date range, category or search term.</div></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)