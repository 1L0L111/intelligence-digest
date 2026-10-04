from app.evaluation.golden_dataset import GOLDEN_EXAMPLES
from app.intelligence.extraction import executive_tags
from app.models import Publication

def main():
    execs=[x for x in GOLDEN_EXAMPLES if x.audience=='executive']; tp=pred=gold=0
    for i,x in enumerate(execs):
        # Benchmark is intentionally title-only: conservative lower-bound for tagger quality.
        p=Publication(id=str(i),title=x.title,url=x.url,source='golden',text='')
        got=set(executive_tags(p)); want=set(x.tags); tp+=len(got&want);pred+=len(got);gold+=len(want)
    precision=tp/pred if pred else 0; recall=tp/gold if gold else 0; f1=2*precision*recall/(precision+recall) if precision+recall else 0
    print(f'Golden examples: {len(GOLDEN_EXAMPLES)} (technical=10, executive=11)')
    print(f'Executive tagger title-only lower bound: precision={precision:.3f} recall={recall:.3f} f1={f1:.3f}')
    print('Pipeline tests and organizer-aligned rules are the primary reproducible offline evaluation in semifinal package.')
if __name__=='__main__':main()
