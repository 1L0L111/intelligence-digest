import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import streamlit as st

from app.digest.docx_export import export_docx
from app.digest.markdown import render_markdown
from app.models import Publication, UserProfile
from app.pipeline import run_pipeline

ROOT = Path(__file__).resolve().parents[1]
st.set_page_config(page_title="Intelligence Digest", page_icon="◈", layout="wide")

ROLE_LABELS = {"security_engineer": "ИБ / ИТ специалист", "cio": "Руководитель"}
CATEGORY_LABELS = {
    "vulnerabilities": "Уязвимости",
    "ransomware": "Ransomware",
    "attacks": "Атаки",
    "ai": "ИИ и регулирование",
    "cloud": "Облако и трансформация",
    "other": "Прочее",
}
DEFAULTS = {
    "security_engineer": ["CVE", "Microsoft", "Kubernetes", "ransomware"],
    "cio": ["AI", "cloud", "regulation", "digital transformation"],
}
OPTIONS = ["CVE", "Microsoft", "Kubernetes", "ransomware", "SCADA", "energy", "AI", "cloud", "regulation", "digital transformation"]

st.markdown("""
<style>
.block-container {max-width: 1280px; padding-top: 2.2rem;}
[data-testid="stMetricValue"] {font-size: 2.1rem;}
.small-muted {color:#8b949e;font-size:.9rem}
.topic-badge {display:inline-block;padding:.25rem .65rem;border:1px solid #444;border-radius:999px;font-size:.82rem;margin-bottom:.4rem}
.score-high {font-weight:700}
</style>
""", unsafe_allow_html=True)

with open(ROOT / "data/samples/publications.json", encoding="utf-8") as f:
    publications = [Publication(**x) for x in json.load(f)]

st.sidebar.markdown("### Персонализация")
role = st.sidebar.radio("Аудитория", list(ROLE_LABELS), format_func=ROLE_LABELS.get)
if st.session_state.get("last_role") != role:
    st.session_state["interests"] = DEFAULTS[role]
    st.session_state["last_role"] = role
interests = st.sidebar.multiselect("Интересы", OPTIONS, key="interests")
limit = st.sidebar.slider("Размер дайджеста", 3, 10, 6)
st.sidebar.caption("Подборка пересчитывается при смене роли или интересов — без перезапуска приложения.")

profile = UserProfile(role=role, interests=interests)
events = run_pipeline(publications, profile, limit)
selected_publications = sum(len(e.publication_ids) for e in events)
compression = 1 - len(events) / max(len(publications), 1)

st.title("◈ Intelligence Digest")
st.caption("Персональный ИТ/ИБ-дайджест: от публикаций к объяснимым событиям и решениям")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Публикаций на входе", len(publications))
m2.metric("Релевантных", selected_publications)
m3.metric("Событий", len(events))
m4.metric("Сжатие потока", f"{compression:.0%}")

if not events:
    st.warning("По выбранным интересам релевантных материалов не найдено. Добавьте интерес или смените аудиторию.")
else:
    groups = {}
    for event in events:
        base = event.category.split("-")[0]
        groups.setdefault(base, []).append(event)

    for category, category_events in groups.items():
        st.markdown(f"### {CATEGORY_LABELS.get(category, 'Другие события')}")
        for event in category_events:
            with st.container(border=True):
                left, right = st.columns([5, 1])
                left.subheader(event.title)
                right.metric("Релевантность", f"{event.score:.0%}")
                st.write(event.summary)
                st.markdown(f"**Почему важно:** {event.why_it_matters}")
                if event.reasons:
                    st.caption("Сигналы отбора: " + " · ".join(event.reasons))

                details = event.details or {}
                detail_bits = []
                if details.get("cve"):
                    detail_bits.append("CVE: " + ", ".join(details["cve"]))
                if details.get("cvss") is not None:
                    detail_bits.append(f"CVSS: {details['cvss']}")
                if details.get("exploit_available"):
                    detail_bits.append("Есть упоминание exploit/PoC")
                if details.get("tags"):
                    detail_bits.append("Бизнес-сигналы: " + ", ".join(details["tags"]))
                if detail_bits:
                    st.info(" • ".join(detail_bits))

                with st.expander(f"Источники ({len(event.sources)})"):
                    for idx, source in enumerate(event.sources, 1):
                        st.markdown(f"{idx}. {source}")

st.divider()
st.markdown("### Экспорт готового дайджеста")
st.caption("Результат можно передать в корпоративный портал, почту или документооборот.")
md = render_markdown(events, profile)
c1, c2 = st.columns(2)
c1.download_button("↓ Скачать Markdown", md, "digest.md", "text/markdown", use_container_width=True)
with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
    docx_path = export_docx(events, profile, tmp.name)
    docx_data = Path(docx_path).read_bytes()
c2.download_button("↓ Скачать DOCX", docx_data, "digest.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
