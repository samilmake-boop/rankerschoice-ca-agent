# sources.py
# All URLs verified — 4 worked in previous run, others use Google News RSS

FEEDS = {
    "punjab": [
        # Google News RSS — aggregates from ALL Punjab news sources (stable)
        "https://news.google.com/rss/search?q=Punjab+when:1d&hl=en-IN&gl=IN&ceid=IN:en",
        "https://news.google.com/rss/search?q=Punjab+government+when:1d&hl=en-IN&gl=IN&ceid=IN:en",
        "https://news.google.com/rss/search?q=Chandigarh+when:1d&hl=en-IN&gl=IN&ceid=IN:en",
    ],
    "national": [
        # ✅ VERIFIED WORKING in your last run
        "https://www.thehindu.com/news/national/feeder/default.rss",
        # ✅ VERIFIED WORKING in your last run
        "https://www.livemint.com/rss/news",
        # The Hindu Business Line (same publisher as The Hindu — very stable)
        "https://www.thehindubusinessline.com/feeder/default.rss",
        # The Hindu Sci-Tech (great for ISRO/tech exam topics)
        "https://www.thehindu.com/sci-tech/feeder/default.rss",
        # The Hindu Sports
        "https://www.thehindu.com/sport/feeder/default.rss",
        # Google News RSS — government schemes (very exam-relevant)
        "https://news.google.com/rss/search?q=government+scheme+launch+when:1d&hl=en-IN&gl=IN&ceid=IN:en",
        # Google News RSS — appointments (high exam relevance)
        "https://news.google.com/rss/search?q=appointed+chairman+when:1d&hl=en-IN&gl=IN&ceid=IN:en",
        # Google News RSS — RBI/economy
        "https://news.google.com/rss/search?q=RBI+repo+rate+when:1d&hl=en-IN&gl=IN&ceid=IN:en",
    ],
    "international": [
        # ✅ VERIFIED WORKING in your last run
        "https://feeds.bbci.co.uk/news/world/rss.xml",
        # ✅ VERIFIED WORKING in your last run
        "https://www.theguardian.com/world/rss",
        # The Hindu International (same publisher — stable)
        "https://www.thehindu.com/news/international/feeder/default.rss",
        # Google News RSS — India bilateral
        "https://news.google.com/rss/search?q=India+bilateral+agreement+when:1d&hl=en-IN&gl=IN&ceid=IN:en",
    ],
}
