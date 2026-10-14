# fetch_news.py
import feedparser
import trafilatura
from datetime import datetime, timedelta
from sources import FEEDS

def fetch_all():
    cutoff = datetime.now() - timedelta(hours=24)
    items = []
    
    for category, urls in FEEDS.items():
        for url in urls:
            try:
                feed = feedparser.parse(url, timeout=15)
                for entry in feed.entries[:25]:
                    pub = getattr(entry, "published_parsed", None)
                    if pub and datetime(*pub[:6]) < cutoff:
                        continue
                    
                    body = ""
                    if entry.link:
                        try:
                            downloaded = trafilatura.fetch_url(entry.link)
                            body = trafilatura.extract(downloaded) or entry.get("summary", "")
                        except Exception:
                            body = entry.get("summary", "")
                    
                    items.append({
                        "title": entry.title,
                        "link": entry.link,
                        "published": str(entry.get("published", "")),
                        "body": body[:3500],
                        "category_feed": category,
                    })
            except Exception as e:
                print(f"  ⚠️ Feed error {url}: {e}")
    
    return items
