from app.evaluation.golden_dataset import GOLDEN_EXAMPLES, TECHNICAL_OUTPUT_FIELDS
from app.evaluation.metrics import precision_at_k, recall_at_k, ndcg_at_k
from app.intelligence.organizer_rules import organizer_importance, infer_category
from app.models import Publication


def test_organizer_dataset_is_fully_normalized():
    assert len(GOLDEN_EXAMPLES) == 21
    assert sum(x.audience == "technical" for x in GOLDEN_EXAMPLES) == 10
    assert sum(x.audience == "executive" for x in GOLDEN_EXAMPLES) == 11
    assert len(TECHNICAL_OUTPUT_FIELDS["Уязвимость"]) == 10


def test_metrics():
    ranked=["a","x","b"]
    assert precision_at_k(ranked,{"a","b"},2) == .5
    assert recall_at_k(ranked,{"a","b"},3) == 1
    assert 0 < ndcg_at_k(ranked,{"a":3,"b":2},3) <= 1


def test_organizer_rules_boost_energy_and_exploit():
    p=Publication(id="x", title="Критическая уязвимость CVE-2026-12345 в SCADA РФ", url="https://example.org", source="test", text="Публичный exploit PoC для энергетики")
    importance, reasons=organizer_importance(p)
    assert infer_category(p) == "Уязвимость"
    assert importance >= .9
    assert "есть exploit/PoC" in reasons
