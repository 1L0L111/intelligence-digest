WEIGHTS = {"relevance": .35, "importance": .25, "user_interest": .20, "novelty": .10, "source_trust": .10}
def final_score(*, relevance: float, importance: float, user_interest: float, novelty: float, source_trust: float) -> float:
    values = locals()
    return round(sum(WEIGHTS[k] * values[k] for k in WEIGHTS), 4)
