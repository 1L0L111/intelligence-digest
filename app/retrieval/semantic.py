from __future__ import annotations
from functools import lru_cache
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.models import Publication, UserProfile

def semantic_scores(publications: list[Publication], profile: UserProfile) -> dict[str,float]:
    if not publications: return {}
    query=' '.join(profile.interests) or profile.role
    docs=[f'{p.title}. {p.text}' for p in publications]
    # Deterministic offline semantic-ish fallback; no model download required for jury demo.
    vec=TfidfVectorizer(ngram_range=(1,2), analyzer='word', min_df=1, max_features=12000, lowercase=True)
    X=vec.fit_transform([query]+docs)
    scores=cosine_similarity(X[0:1],X[1:]).ravel()
    return {p.id: float(s) for p,s in zip(publications,scores)}
