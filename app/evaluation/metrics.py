from __future__ import annotations
import math


def precision_at_k(ranked_ids: list[str], relevant_ids: set[str], k: int) -> float:
    if k <= 0: return 0.0
    top = ranked_ids[:k]
    return sum(x in relevant_ids for x in top) / k


def recall_at_k(ranked_ids: list[str], relevant_ids: set[str], k: int) -> float:
    if not relevant_ids: return 0.0
    return sum(x in relevant_ids for x in ranked_ids[:k]) / len(relevant_ids)


def ndcg_at_k(ranked_ids: list[str], relevance: dict[str, float], k: int) -> float:
    gains = [relevance.get(x, 0.0) for x in ranked_ids[:k]]
    dcg = sum((2**g - 1) / math.log2(i + 2) for i, g in enumerate(gains))
    ideal = sorted(relevance.values(), reverse=True)[:k]
    idcg = sum((2**g - 1) / math.log2(i + 2) for i, g in enumerate(ideal))
    return dcg / idcg if idcg else 0.0


def duplicate_reduction_rate(before: int, after: int) -> float:
    return 0.0 if before <= 0 else max(0.0, 1 - after / before)
