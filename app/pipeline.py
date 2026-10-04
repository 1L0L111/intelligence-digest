from uuid import uuid4
from app.models import Publication, UserProfile, DigestEvent
from app.retrieval.relevance import lexical_relevance
from app.retrieval.semantic import semantic_scores
from app.intelligence.deduplication import deduplicate
from app.intelligence.clustering import cluster_by_topic
from app.intelligence.scoring import final_score
from app.intelligence.organizer_rules import organizer_importance
from app.intelligence.extraction import technical_card, executive_tags

def run_pipeline(publications: list[Publication], profile: UserProfile, limit: int = 10) -> list[DigestEvent]:
    pubs=deduplicate(publications); sem=semantic_scores(pubs,profile); ranked=[]
    for p in pubs:
        lex,hits=lexical_relevance(p,profile); rel=max(lex,sem.get(p.id,0)*.85)
        if rel < .08: continue
        importance,org=organizer_importance(p); hits=list(dict.fromkeys(hits+org))
        score=final_score(relevance=rel,importance=importance,user_interest=max(lex,rel*.8),novelty=.7,source_trust=.8)
        if score>=.38: ranked.append((p,score,hits))
    ranked.sort(key=lambda x:x[1],reverse=True); selected=ranked[:max(limit*3,limit)]
    clusters=cluster_by_topic([x[0] for x in selected]); meta={p.id:(s,h) for p,s,h in selected}; events=[]
    for topic,items in clusters.items():
        score=max(meta[p.id][0] for p in items); reasons=sorted(set(sum((meta[p.id][1] for p in items),[])))
        lead=max(items,key=lambda p:meta[p.id][0]); cards=[technical_card(p) for p in items]
        tags=sorted(set(t for p in items for t in executive_tags(p)))
        detail=cards[0] if profile.role!='cio' else {'tags':tags}
        summary=(lead.text[:520].strip() or lead.title)
        why=('; '.join(tags[:4]) if tags else f'Соответствует интересам роли {profile.role}')
        events.append(DigestEvent(id=str(uuid4()),title=lead.title,category=topic,summary=summary,why_it_matters=why,
            score=score,publication_ids=[p.id for p in items],sources=[p.url for p in items],reasons=reasons,details=detail))
    return sorted(events,key=lambda x:x.score,reverse=True)[:limit]
