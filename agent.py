# agent.py
import os
import sys
import time
from datetime import datetime
from fetch_news import fetch_all
from exam_filter import filter_article
from human_writer import write_human_style
from publish_wp import publish


def log(message):
    """Print with timestamp — replaces Telegram alerts."""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")


def run():
    start = time.time()
    log("🚀 RankersChoice Daily CA Agent starting...")
    
    log("📰 Fetching RSS feeds...")
    all_news = fetch_all()
    log(f"  → Got {len(all_news)} raw articles\n")
    
    if not all_news:
        log("⚠️ No news fetched today — check RSS feeds.")
        return
    
    approved = []
    for i, article in enumerate(all_news, 1):
        title_short = article["title"][:60]
        log(f"[{i}/{len(all_news)}] 🔍 Filtering: {title_short}...")
        
        try:
            relevant, data = filter_article(article)
        except Exception as e:
            log(f"  ⚠️ Filter error: {e}")
            continue
        
        if relevant:
            score = data.get("exam_score", "?")
            category = data.get("category", "National")
            log(f"  ✓ PASS (score: {score}, cat: {category}) — writing human-style...")
            
            try:
                summary = write_human_style(data, article["title"])
                approved.append({
                    "title": article["title"],
                    "link": article["link"],
                    "category": category,
                    "summary": summary,
                    "exam_score": score,
                })
                log(f"  ✍️ Written ({len(summary)} chars)\n")
            except Exception as e:
                log(f"  ⚠️ Write error: {e}\n")
                continue
        else:
            log(f"  ✗ SKIP\n")
    
    duration_min = round((time.time() - start) / 60, 1)
    log(f"\n📊 Summary:")
    log(f"  • Fetched: {len(all_news)}")
    log(f"  • Approved: {len(approved)}")
    log(f"  • Time: {duration_min} min")
    
    if not approved:
        log("⚠️ No exam-relevant news approved today.")
        return
    
    date_str = datetime.now().strftime("%d %B %Y")
    log(f"\n📤 Publishing to WordPress...")
    
    try:
        result = publish(approved, date_str)
        post_url = result.get("link", "pending")
        log(f"  ✅ Published! Post ID: {result.get('id')}")
        log(f"  🔗 URL: {post_url}")
        log(f"\n🎉 SUCCESS! Daily Current Affairs for {date_str} is live on ranekrschoice.com")
    except Exception as e:
        log(f"❌ Publishing failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run()
