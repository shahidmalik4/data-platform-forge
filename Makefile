# ========================================
# Data Platform Makefile
# ========================================

# Directories
TRANSFORMATIONS_DIR = data-platform/transformations/dbt_project
ORCHESTRATOR_DIR   = data-platform/orchestrator
DLT_PIPELINE_DIR   = data-platform/ingestion/pipeline

# Commands
UV = uv run
DBT = $(UV) dbt --project-dir $(TRANSFORMATIONS_DIR)
DAGSTER = $(UV) dagster
PYTHON = $(UV) python

# ========================================
# Default
# ========================================
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make dagster      - Run Dagster dev server"
	@echo "  make run-dlt      - Run DLT pipelines"
	@echo "  make dbt-run      - Run dbt models"
	@echo "  make dbt-test     - Run dbt tests"
	@echo "  make clean        - Clean temp files and artifacts"
	@echo "  make lint         - Run Python linters (ruff/black)"
	@echo "  make init         - Install dependencies and sync uv"

# ========================================
# Project setup
# ========================================
.PHONY: init
init:
	$(UV) sync
	@echo "Dependencies installed and environment synced!"

# ========================================
# Dagster
# ========================================
.PHONY: dagster
dagster:
	cd $(ORCHESTRATOR_DIR) && $(DAGSTER) dev

# ========================================
# DLT pipelines
# ========================================
.PHONY: run-dlt
run-dlt:
	$(PYTHON) $(DLT_PIPELINE_DIR)/run_dlt_pipeline.py

# ========================================
# dbt
# ========================================
.PHONY: dbt-run
dbt-run:
	$(DBT) run

.PHONY: dbt-test
dbt-test:
	$(DBT) test

# ========================================
# Lint & format
# ========================================
.PHONY: lint
lint:
	$(UV) ruff check data-platform
	$(UV) black --check data-platform

.PHONY: format
format:
	$(UV) black data-platform

# ========================================
# Clean
# ========================================
.PHONY: clean
clean:
	rm -rf data-platform/__pycache__
	rm -rf data-platform/orchestrator/__pycache__
	rm -rf data-platform/ingestion/__pycache__
	rm -rf data-platform/transformations/dbt_project/target
	@echo "Cleaned temporary files and artifacts."