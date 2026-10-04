# План команды из 5 человек

## 1. Tech Lead / Backend / Integration
**Владелец:** архитектура, API, интеграция, релиз.
- FastAPI contracts, domain models, config.
- LLM provider abstraction.
- Docker/local reproducibility.
- Merge requests, integration branch, release checklist.
**Definition of Done:** `docker compose up` поднимает demo без ручных правок.

## 2. ML / Retrieval Engineer
**Владелец:** качество отбора.
- XLSX → benchmark.
- Embeddings + semantic retrieval.
- Reranker.
- Ranking features: relevance, importance, user-interest, novelty, source trust.
- Precision@K, Recall@K, NDCG.
**DoD:** baseline сравнён с semantic+reranker на benchmark организаторов.

## 3. LLM / Intelligence Engineer
**Владелец:** structured intelligence.
- LLM judge schema.
- Категоризация, entities, importance, reasons.
- Event clustering / dedup.
- Grounded summaries + claim/source verification.
- Prompts и regression fixtures.
**DoD:** summary не содержит неподтверждённых ключевых фактов на golden set.

## 4. Data / Sources Engineer
**Владелец:** репрезентативность данных.
- RSS/API/HTML connectors.
- Нормализация, canonical URL, timestamps, language.
- Источники: vendor advisories, CERT/CVE, отраслевые IT/IB медиа, RU/EN.
- Source trust metadata, retries/cache.
**DoD:** воспроизводимый snapshot >=100 публикаций из разных типов источников.

## 5. Product / Frontend / Demo & Business
**Владелец:** 10/10 business + защита.
- Streamlit/Next UI: profile, funnel, event cards, explainability, feedback.
- Security Engineer ↔ CIO demo.
- Markdown/DOCX export.
- KPI экономии времени, limitations.
- Презентация и 3-минутный demo script.
**DoD:** незнакомый человек проходит demo без объяснений разработчика.

## Общая ответственность
Каждый участник: собственная feature-ветка → MR → review вторым участником. Никаких прямых push в main.
