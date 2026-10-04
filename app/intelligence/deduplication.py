from difflib import SequenceMatcher
from app.models import Publication

def deduplicate(publications: list[Publication], threshold: float = .88) -> list[Publication]:
    kept: list[Publication] = []
    for p in publications:
        if not any(SequenceMatcher(None, p.title.lower(), q.title.lower()).ratio() >= threshold for q in kept):
            kept.append(p)
    return kept
