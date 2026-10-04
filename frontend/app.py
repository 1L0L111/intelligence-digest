import io,json,sys,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import streamlit as st
from app.models import Publication,UserProfile
from app.pipeline import run_pipeline
from app.digest.markdown import render_markdown
from app.digest.docx_export import export_docx
st.set_page_config(page_title='Intelligence Digest',page_icon='◈',layout='wide')
st.title('◈ Intelligence Digest'); st.caption('Explainable event-centric IT / InfoSec intelligence for energy enterprises')
with open(Path(__file__).parents[1]/'data/samples/publications.json',encoding='utf-8') as f: pubs=[Publication(**x) for x in json.load(f)]
role=st.sidebar.radio('Аудитория',['security_engineer','cio'],format_func=lambda x:'ИБ / ИТ специалист' if x=='security_engineer' else 'Руководитель')
opts=['CVE','Microsoft','Kubernetes','ransomware','SCADA','energy','AI','cloud','regulation','digital transformation']
defaults=['CVE','Microsoft','Kubernetes','ransomware'] if role=='security_engineer' else ['AI','cloud','regulation','digital transformation']
interests=st.sidebar.multiselect('Интересы',opts,defaults); limit=st.sidebar.slider('Размер дайджеста',3,10,6)
profile=UserProfile(role=role,interests=interests); events=run_pipeline(pubs,profile,limit)
a,b,c,d=st.columns(4);a.metric('Вход',len(pubs));b.metric('Отобрано',sum(len(e.publication_ids) for e in events));c.metric('Событий',len(events));d.metric('Сжатие',f'{(1-len(events)/max(len(pubs),1)):.0%}')
for e in events:
    with st.container(border=True):
        left,right=st.columns([5,1]); left.subheader(e.title); right.metric('Score',f'{e.score:.0%}')
        st.write(e.summary); st.caption('Почему важно: '+e.why_it_matters)
        if e.details: st.json(e.details,expanded=False)
        st.caption('Сигналы: '+(', '.join(e.reasons) or 'semantic relevance'))
        with st.expander(f'Источники ({len(e.sources)})'):
            for s in e.sources: st.write(s)
md=render_markdown(events,profile); st.divider(); c1,c2=st.columns(2)
c1.download_button('↓ Markdown',md,'digest.md','text/markdown',use_container_width=True)
with tempfile.NamedTemporaryFile(suffix='.docx',delete=False) as tmp: p=export_docx(events,profile,tmp.name); data=Path(p).read_bytes()
c2.download_button('↓ DOCX',data,'digest.docx','application/vnd.openxmlformats-officedocument.wordprocessingml.document',use_container_width=True)
