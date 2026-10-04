import re
from app.models import Publication, UserProfile

def lexical_relevance(pub: Publication, profile: UserProfile) -> tuple[float, list[str]]:
    hay = f"{pub.title} {pub.text}".lower()
    hits = [x for x in profile.interests if re.search(rf"(?<!\w){re.escape(x.lower())}(?!\w)", hay)]
    excluded = [x for x in profile.exclusions if x.lower() in hay]
    if excluded: return 0.0, [f"excluded:{x}" for x in excluded]
    if not profile.interests: return 0.5, []
    weighted = sum(profile.priorities.get(x, 1.0) for x in hits)
    denom = sum(profile.priorities.get(x, 1.0) for x in profile.interests) or 1
    return min(1.0, weighted / denom * 2.5), hits
