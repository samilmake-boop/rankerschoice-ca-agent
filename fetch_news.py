# fetch_news.py
import feedparser
import trafilatura
import requests
from datetime import datetime, timedelta, timezone
from sources import FEEDS

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0 Safari/537.36"
}


def fetch_all():
    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
    items = []

    print(f"\n=== RSS FEED REPORT ===")
    print(f"Cutoff time (UTC): {cutoff.isoformat()}")
    print(f"Total feeds configured: {sum(len(v) for v in FEEDS.values())}\n")

    for category, urls in FEEDS.items():
        print(f"\n--- Category: {category.upper()} ({len(urls)} feeds) ---")
        for url in urls:
            try:
                # Use requests with timeout, then feedparser for parsing
                response = requests.get(url, headers=HEADERS, timeout=20)
                if response.status_code != 200:
                    print(f"  ❌ {url}")
                    print(f"     HTTP Status: {response.status_code}")
                    continue

                feed = feedparser.parse(response.content)
                feed_title = getattr(feed.feed, "title", "Unknown")
                n_entries = len(feed.entries)

                if n_entries == 0:
                    print(f"  ❌ {url}")
                    print(f"     Feed: {feed_title}, Entries: 0")
                    if feed.bozo:
                        print(f"     Parse error: {feed.bozo_exception}")
                    continue

                print(f"  ✅ {url}")
                print(f"     Feed: {feed_title}, Entries: {n_entries}")

                added = 0
                for entry in feed.entries[:25]:
                    # Date filter (only skip if date is old AND parseable)
                    pub = getattr(entry, "published_parsed", None)
                    if pub:
                        try:
                            pub_dt = datetime(*pub[:6], tzinfo=timezone.utc)
                            if pub_dt < cutoff:
                                continue
                        except Exception:
                            pass  # If date parsing fails, include it anyway

                    # Extract article body
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
                    added += 1

                print(f"     Added: {added} recent articles")

            except requests.exceptions.Timeout:
                print(f"  ⚠️ Timeout (20s): {url}")
            except requests.exceptions.RequestException as e:
                print(f"  ⚠️ Request failed: {url}")
                print(f"     {e}")
            except Exception as e:
                print(f"  ⚠️ Exception: {url}")
                print(f"     {e}")

    print(f"\n=== SUMMARY ===")
    print(f"Total articles collected: {len(items)}\n")
    return items
