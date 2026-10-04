# Architecture

`Sources → Normalize → Cheap filter → Embedding retrieval → Rerank → LLM Judge → Event clustering → Grounded composer → Markdown/DOCX`

Design rules:
1. LLM is replaceable, not the architecture.
2. Every digest item keeps source URLs.
3. Expensive inference only after retrieval.
4. Event is the output unit; articles are evidence.
5. Offline evaluation is a first-class subsystem.
6. Demo has deterministic offline fallback.
