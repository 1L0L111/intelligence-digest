from __future__ import annotations
from collections import defaultdict
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.models import Publication

def cluster_by_topic(publications: list[Publication], threshold: float=.88) -> dict[str,list[Publication]]:
    if not publications:return {}
    docs=[f'{p.title} {p.text[:1200]}' for p in publications]
    X=TfidfVectorizer(ngram_range=(1,2),analyzer='word',min_df=1,max_features=10000).fit_transform(docs)
    sim=cosine_similarity(X); seen=set(); clusters=[]
    for i,p in enumerate(publications):
        if i in seen:continue
        group=[i]; seen.add(i)
        for j in range(i+1,len(publications)):
            if j not in seen and sim[i,j]>=threshold: group.append(j);seen.add(j)
        clusters.append([publications[k] for k in group])
    def label(items):
        text=' '.join(p.title.lower() for p in items)
        rules=[('vulnerabilities',r'cve|уязвим|vulnerab'),('ransomware',r'ransomware|шифроваль'),('attacks',r'атак|campaign|malware|phishing'),('ai',r'\bai\b|llm|нейросет'),('cloud',r'cloud|kubernetes|облач')]
        return next((n for n,pat in rules if re.search(pat,text)), 'other')
    out={}
    for n,items in enumerate(clusters,1):
        base=label(items); key=base if base not in out else f'{base}-{n}'; out[key]=items
    return out
