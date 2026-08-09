import feedparser
from datetime import datetime, timezone

from database import (
    initialize_database,
    topic_exists,
    save_topic
)


RSS_FEEDS = [
    "https://blog.google/technology/ai/rss/",
    "https://huggingface.co/blog/feed.xml",
    "https://www.technologyreview.com/feed/",
]


SECURITY_KEYWORDS = [
    "ai security",
    "artificial intelligence security",
    "cybersecurity",
    "cyber security",
    "vulnerability",
    "exploit",
    "attack",
    "prompt injection",
    "jailbreak",
    "data poisoning",
    "model poisoning",
    "adversarial",
    "malware",
    "privacy",
    "surveillance",
    "deepfake",
    "identity",
    "authentication",
    "authorization",
    "sandbox",
    "agent security",
    "ai safety",
    "model safety",
    "red team",
    "security flaw",
    "security risk",
    "data leak",
    "data breach",
]


def is_security_relevant(title, summary):

    text = (
        title + " " + summary
    ).lower()

    for keyword in SECURITY_KEYWORDS:

        if keyword in text:
            return True

    return False


def discover_topics(agent_id):

    topics = []

    for feed_url in RSS_FEEDS:

        try:

            print(
                f"\nChecking: {feed_url}"
            )

            feed = feedparser.parse(
                feed_url
            )

            print(
                f"Articles available: {len(feed.entries)}"
            )

            for entry in feed.entries[:20]:

                title = entry.get(
                    "title",
                    ""
                ).strip()

                url = entry.get(
                    "link",
                    ""
                ).strip()

                summary = entry.get(
                    "summary",
                    ""
                ).strip()

                if not title or not url:
                    continue

                if not is_security_relevant(
                    title,
                    summary
                ):
                    continue

                if topic_exists(url):
                    continue

                discovered_at = datetime.now(
                    timezone.utc
                ).isoformat()

                save_topic(
                    agent_id,
                    title,
                    url,
                    summary,
                    discovered_at
                )

                topics.append({
                    "title": title,
                    "url": url,
                    "summary": summary,
                    "discovered_at": discovered_at
                })

                print(
                    "\nNEW SECURITY TOPIC:"
                )

                print(title)

        except Exception as error:

            print(
                f"\nError reading {feed_url}: {error}"
            )

    return topics