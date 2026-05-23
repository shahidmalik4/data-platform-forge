# ============================================================
# Data Platform Makefile
# ============================================================

# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------

DBT_DIR = dbt/dbt_project
DBT = uv run dbt --project-dir $(DBT_DIR)
SRC_DIR         = src
TESTS_DIR       = tests
SCRIPTS_DIR     = scripts
DAGSTER_HOME   ?= $(CURDIR)/.dagster_home

# ------------------------------------------------------------
# Commands
# ------------------------------------------------------------

UV      = uv run
DBT     = $(UV) dbt --project-dir $(DBT_DIR)
DAGSTER = DAGSTER_HOME=$(DAGSTER_HOME) $(UV) dagster
PYTHON  = $(UV) python
RUFF    = $(UV) ruff
BLACK   = $(UV) black

# ============================================================
# Help  (default target)
# ============================================================

.PHONY: help
help:
	@echo ""
	@echo "  Data Platform — available commands"
	@echo ""
	@echo "  Setup"
	@echo "    make init            Install dependencies and create runtime dirs"
	@echo ""
	@echo "  Infrastructure"
	@echo "    make docker-up       Start Postgres container"
	@echo "    make docker-down     Stop and remove containers"
	@echo "    make docker-reset    Destroy volumes and restart fresh"
	@echo ""
	@echo "  Orchestration"
	@echo "    make dagster         Launch Dagster dev UI"
	@echo ""
	@echo "  Ingestion"
	@echo "    make ingest          Run dlt ingestion pipeline"
	@echo ""
	@echo "  Transformation"
	@echo "    make dbt-run         Run all dbt models"
	@echo "    make dbt-run-full    Run all dbt models (--full-refresh)"
	@echo "    make dbt-test        Run dbt tests"
	@echo "    make dbt-compile     Compile dbt project (validate SQL)"
	@echo "    make dbt-docs        Generate and serve dbt docs"
	@echo ""
	@echo "  Testing"
	@echo "    make test            Run pytest suite"
	@echo ""
	@echo "  Code quality"
	@echo "    make lint            Check code style (ruff + black)"
	@echo "    make format          Auto-format code (ruff + black)"
	@echo "    make sql-lint        Lint SQL with sqlfluff"
	@echo "    make sql-fix         Auto-fix SQL with sqlfluff"
	@echo ""
	@echo "  Housekeeping"
	@echo "    make clean           Remove build artifacts and caches"
	@echo ""

# ============================================================
# Setup
# ============================================================

.PHONY: init
init:
	uv sync
	mkdir -p $(DAGSTER_HOME)
	@echo "✓ Dependencies installed"
	@echo "✓ DAGSTER_HOME created at $(DAGSTER_HOME)"

# ============================================================
# Infrastructure
# ============================================================

.PHONY: docker-up
docker-up:
	docker compose up -d
	@echo "✓ Postgres running"

.PHONY: docker-down
docker-down:
	docker compose down

.PHONY: docker-reset
docker-reset:
	docker compose down -v
	docker compose up -d
	@echo "✓ Warehouse reset — volumes wiped and recreated"

# ============================================================
# Orchestration
# ============================================================

.PHONY: dagster
dagster:
	$(DAGSTER) dev

# ============================================================
# Ingestion
# ============================================================

.PHONY: ingest
ingest:
	$(PYTHON) -m src.data_platform.ingestion.pipeline.run_dlt_pipeline

# ============================================================
# Transformation
# ============================================================

.PHONY: dbt-run
dbt-run:
	$(DBT) run

.PHONY: dbt-run-full
dbt-run-full:
	$(DBT) run --full-refresh

.PHONY: dbt-test
dbt-test:
	$(DBT) test

.PHONY: dbt-compile
dbt-compile:
	$(DBT) compile

.PHONY: dbt-docs
dbt-docs:
	$(DBT) docs generate
	$(DBT) docs serve

# ============================================================
# Testing
# ============================================================

.PHONY: test
test:
	$(UV) pytest $(TESTS_DIR) -v

# ============================================================
# Code quality
# ============================================================

.PHONY: lint
lint:
	$(RUFF) check $(SRC_DIR)
	$(BLACK) --check $(SRC_DIR)

.PHONY: format
format:
	$(RUFF) check --fix $(SRC_DIR)
	$(BLACK) $(SRC_DIR)

.PHONY: sql-lint
sql-lint:
	$(UV) sqlfluff lint $(DBT_DIR)

.PHONY: sql-fix
sql-fix:
	$(UV) sqlfluff fix $(DBT_DIR)

.PHONY: all
all:
	make ingest
	make dbt-run
	make dbt-test
	make sql-lint
	make lint

# ============================================================
# Housekeeping
# ============================================================

.PHONY: clean
clean:
	find $(SRC_DIR) -type d -name "__pycache__" -exec rm -rf {} +
	find $(TESTS_DIR) -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf $(DBT_DIR)/target
	rm -rf $(DBT_DIR)/logs
	rm -rf $(DBT_DIR)/dbt_packages
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	@echo "✓ Cleaned build artifacts and caches"
