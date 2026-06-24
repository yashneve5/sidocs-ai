import requests
import streamlit as st

# ✅ Option A: Paste your Anthropic API key here
# Get it free at: https://console.anthropic.com
ANTHROPIC_API_KEY = st.secrets.get("ANTHROPIC_API_KEY", "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")


def get_ai_summary(title, body, date, category):
    """Generate a 3-sentence manager-level summary using Claude API"""

    if not body or len(body.strip()) < 30:
        prompt = f"""You are summarizing a Siemens press release for a senior manager report.
Title: {title}
Date: {date}
Category: {category}
The full article content was not available. Based on the title alone, write a professional
2-3 sentence summary. Keep it concise, factual and business-focused."""
    else:
        prompt = f"""You are summarizing a Siemens press release for a senior manager report.
Title: {title}
Date: {date}
Category: {category}
Article Content: {body[:2000]}
Write a professional 3-sentence summary covering:
1. What was announced
2. Key business impact or benefit
3. Strategic significance for Siemens
Keep it concise and suitable for a C-level executive reader."""

    # Check if API key is set
    if ANTHROPIC_API_KEY == "your_anthropic_api_key_here":
        return _fallback_summary(title, body)

    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01",
                "x-api-key": ANTHROPIC_API_KEY,
            },
            json={
                "model": "claude-sonnet-4-6",
                "max_tokens": 1000,
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=30
        )
        data = response.json()
        if "content" in data and data["content"]:
            return data["content"][0]["text"].strip()
        return _fallback_summary(title, body)
    except Exception as e:
        print(f"  ⚠️  AI summary failed: {e}")
        return _fallback_summary(title, body)


def _fallback_summary(title, body):
    """Generate a basic summary from title + body when no API key set"""
    if body and len(body.strip()) > 50:
        # Take first 2 clean sentences from body
        sentences = [s.strip() for s in body.replace("\n", " ").split(".") if len(s.strip()) > 20]
        if sentences:
            return ". ".join(sentences[:2]) + "."
    return f"This press release covers: {title}. Please refer to the full article for complete details."


def detect_category(title, url, body=""):
    """Detect business category from title/url/body"""
    text = (title + " " + url + " " + body).lower()

    categories = {
        "AI & Innovation":       ["eigen", "artificial intelligence", "machine learning", "digital twin", "innovation", " ai "],
        "Sustainability":        ["sustainable", "carbon", "green", "renewable", "climate", "net zero", "lithium"],
        "Siemens Mobility":      ["mobility", "rail", "train", "transport", "metro", "rolling stock"],
        "Smart Infrastructure":  ["infrastructure", "building", "energy", "grid", "power", "electrical"],
        "Financial Services":    ["financial", "finance", "investment", "leasing", "fund"],
        "Digital Industries":    ["digital", "automation", "plc", "simatic", "software", "manufacturing", "factory", "supply chain"],
        "Siemens AG":            ["annual", "revenue", "profit", "quarter", "fiscal", "agm", "shareholder", "spin-off"],
    }

    for cat, keywords in categories.items():
        if any(k in text for k in keywords):
            return cat

    return "Siemens AG"
