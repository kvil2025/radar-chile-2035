.PHONY: help install seed pipeline test run-api run-web docker-up docker-down

PYTHON = .venv/bin/python
PYTEST = .venv/bin/pytest
NPM = npm

help:
	@echo "RADAR CHILE 2035 — Command Automation"
	@echo "  make install     : Install Python and Node dependencies"
	@echo "  make seed        : Initialize database tables and master seed data"
	@echo "  make pipeline    : Execute full ingestion, scoring, and regime pipeline"
	@echo "  make test        : Run pytest unit, integration, and data quality test suite"
	@echo "  make run-api     : Start FastAPI backend server on :8000"
	@echo "  make run-web     : Start Vite React frontend on :3000"
	@echo "  make docker-up   : Run all services in Docker Compose (TimescaleDB, API, Web)"
	@echo "  make docker-down : Stop Docker Compose containers"

install:
	$(PYTHON) -m pip install -r requirements.txt
	$(NPM) --prefix apps/web install

seed:
	$(PYTHON) scripts/seed_data.py

pipeline:
	$(PYTHON) scripts/run_pipeline.py

test:
	$(PYTEST) -v

run-api:
	$(PYTHON) -m uvicorn apps.api.src.main:app --host 0.0.0.0 --port 8000 --reload

run-web:
	$(NPM) --prefix apps/web run dev

docker-up:
	docker-compose up -d --build

docker-down:
	docker-compose down
