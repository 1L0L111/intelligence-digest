import json
from pathlib import Path
from app.models import Publication,UserProfile
from app.pipeline import run_pipeline
from app.digest.markdown import render_markdown
from app.digest.docx_export import export_docx
pubs=[Publication(**x) for x in json.loads(Path('data/samples/publications.json').read_text())]
for role,ints in [('security_engineer',['CVE','Microsoft','Kubernetes','ransomware']),('cio',['AI','cloud','regulation','digital transformation'])]:
    profile=UserProfile(role=role,interests=ints); events=run_pipeline(pubs,profile)
    out=Path('artifacts');out.mkdir(exist_ok=True);(out/f'digest_{role}.md').write_text(render_markdown(events,profile),encoding='utf-8');export_docx(events,profile,out/f'digest_{role}.docx')
    print(role,len(events),[e.title for e in events])
