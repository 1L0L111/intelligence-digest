.PHONY: install test api ui demo benchmark lint
install:
	python -m pip install -e '.[dev]'
test:
	pytest -q
api:
	uvicorn app.api.main:app --reload --host 0.0.0.0 --port 8000
ui:
	streamlit run frontend/app.py
demo:
	python scripts/demo.py
benchmark:
	python scripts/benchmark.py
lint:
	ruff check app tests scripts
