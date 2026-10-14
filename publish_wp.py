# publish_wp.py
import os
import requests

WP_URL = "https://ranekrschoice.com/wp-json/wp/v2"
WP_USER = os.environ["WP_USER"]
WP_PASS = os.environ["WP_APP_PASSWORD"]
WP_CATEGORY_ID = int(os.environ.get("WP_CA_CATEGORY_ID", "0"))


def build_html(items):
    """Build exam-style HTML grouped by category."""
    cats = ["Punjab", "National", "International", "Appointment", "Scheme",
            "Award", "Sports", "Economy", "SciTech", "Obituary", "Index", "Defence"]

    html = '<div class="daily-ca">\n'
    for cat in cats:
        cat_items = [i for i in items if i["category"].lower() == cat.lower()]
        if not cat_items:
            continue
        html += f'<h2>{cat} Affairs</h2>\n'
        for item in cat_items:
            html += f"""<div class="ca-item">
<h3>{item['title']}</h3>
<p>{item['summary']}</p>
<p><small>Source: <a href="{item['link']}" target="_blank" rel="noopener">{item['link']}</a></small></p>
</div>
<hr>
"""
    html += '</div>\n<p><em>Auto-curated by RankersChoice AI Agent for competitive exam aspirants.</em></p>'
    return html


def publish(items, date_str):
    """Create a DRAFT post — you publish manually after review."""
    title = f"Daily Current Affairs — {date_str}"
    html = build_html(items)

    payload = {
        "title": title,
        "content": html,
        "status": "draft",  # ← KEY CHANGE: draft instead of publish
        "categories": [WP_CATEGORY_ID] if WP_CATEGORY_ID else [],
    }

    r = requests.post(
        f"{WP_URL}/posts",
        json=payload,
        auth=(WP_USER, WP_PASS),
        timeout=30,
    )
    r.raise_for_status()
    return r.json()
