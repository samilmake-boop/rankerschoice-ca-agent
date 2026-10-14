# agent.py
import os
import sys
import time
from datetime import datetime
from fetch_news import fetch_all
from exam_filter import filter_article
from human_writer import write_human_style
from publish_wp import publish
from telegram_alert import alert

def run():
    start = time.time()
    print(f"[{datetime.now()}] 🚀 RankersChoice Daily CA Agent starting...")
    
    print(f"[{datetime.now()}] 📰 Fetching RSS feeds...")
    all_news = fetch_all()
    print(f"  → Got {len(all_news)} raw articles\n")
    
    if not all_news:
        alert("⚠️ No news fetched today — check RSS feeds.")
        return
    
    approved = []
    for i, article in enumerate(all_news, 1):
        title_short = article["title"][:60]
        print(f"[{i}/{len(all_news)}] 🔍 Filtering: {title_short}...")
        
        try:
            relevant, data = filter_article(article)
        except Exception as e:
            print(f"  ⚠️ Error: {e}")
            continue
        
        if relevant:
            score = data.get("exam_score", "?")
            category = data.get("category", "National")
            print(f"  ✓ PASS (score: {score}, cat: {category}) — writing human-style...")
            
            try:
                summary = write_human_style(data, article["title"])
                approved.append({
                    "title": article["title"],
                    "link": article["link"],
                    "category": category,
                    "summary": summary,
                    "exam_score": score,
                })
                print(f"  ✍️ Written ({len(summary)} chars)\n")
            except Exception as e:
                print(f"  ⚠️ Write error: {e}\n")
                continue
        else:
            print(f"  ✗ SKIP\n")
    
    duration_min = round((time.time() - start) / 60, 1)
    print(f"\n📊 Summary:")
    print(f"  • Fetched: {len(all_news)}")
    print(f"  • Approved: {len(approved)}")
    print(f"  • Time: {duration_min} min")
    
    if not approved:
        alert(f"⚠️ No exam-relevant news approved today.\nFetched: {len(all_news)}, Time: {duration_min} min")
        return
    
    date_str = datetime.now().strftime("%d %B %Y")
    print(f"\n📤 Publishing to WordPress...")
    
    try:
        result = publish(approved, date_str)
        post_url = result.get("link", "pending")
        print(f"  ✅ Published! Post ID: {result.get('id')}")
        print(f"  🔗 URL: {post_url}")
        
        alert(
            f"✅ *Daily Current Affairs for {date_str} published!*\n\n"
            f"• Fetched: {len(all_news)} articles\n"
            f"• Approved for exams: {len(approved)}\n"
            f"• Processing time: {duration_min} min\n"
            f"• Post ID: {result.get('id')}\n"
            f"• URL: {post_url}"
        )
    except Exception as e:
        alert(f"❌ Publishing failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run()
