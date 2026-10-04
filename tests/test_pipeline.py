import json
from pathlib import Path
from app.models import Publication, UserProfile
from app.pipeline import run_pipeline

def pubs():
    return [Publication(**x) for x in json.loads(Path("data/samples/publications.json").read_text())]
def test_personalization_changes_digest():
    sec=run_pipeline(pubs(),UserProfile(role="security_engineer",interests=["CVE","Microsoft","Kubernetes","ransomware"]))
    cio=run_pipeline(pubs(),UserProfile(role="cio",interests=["AI","cloud","regulation","digital transformation"]))
    assert sec and cio
    assert {e.title for e in sec} != {e.title for e in cio}
def test_sources_are_preserved():
    events=run_pipeline(pubs(),UserProfile(interests=["CVE","Microsoft"]))
    assert all(e.sources for e in events)
