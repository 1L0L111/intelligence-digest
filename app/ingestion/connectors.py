from __future__ import annotations
from datetime import datetime
from hashlib import sha1
import feedparser, httpx, trafilatura
from app.models import Publication

def _id(url: str) -> str: return sha1(url.encode()).hexdigest()[:16]

def fetch_rss(url: str, limit: int = 30) -> list[Publication]:
    feed = feedparser.parse(url)
    out=[]
    for e in feed.entries[:limit]:
        link=e.get('link',''); title=e.get('title','').strip()
        if not link or not title: continue
        text=e.get('summary','') or e.get('description','') or ''
        out.append(Publication(id=_id(link), title=title, url=link, source=feed.feed.get('title',url), text=trafilatura.extract(text) or text))
    return out

def fetch_article(url: str, source: str | None = None) -> Publication:
    r=httpx.get(url, timeout=15, follow_redirects=True, headers={'User-Agent':'IntelligenceDigest/1.0'})
    r.raise_for_status(); text=trafilatura.extract(r.text, include_links=False) or ''
    title=(trafilatura.extract_metadata(r.text).title if trafilatura.extract_metadata(r.text) else None) or url
    return Publication(id=_id(url), title=title, url=url, source=source or r.url.host, text=text)
