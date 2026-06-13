# Data Platform Forge

A production-style local data platform built with modern data engineering tools. This project simulates a real-world ELT pipeline — from raw data ingestion through transformation and orchestration — using the same stack used in professional data engineering teams.

---

## Architecture

```
Raw Data
   │
   ▼
[dlt] ──────────── Ingestion (Python-based ELT pipelines)
   │
   ▼
[PostgreSQL] ────── Local Data Warehouse (Docker)
   │
   ▼
[dbt] ──────────── Transformations (Staging → Marts)
   │
   ▼
[Dagster] ─────── Orchestration & Asset Lineage
```

---

## Tech Stack

| Layer           | Tool                          |
|-----------------|-------------------------------|
| Ingestion       | dlt (data load tool)          |
| Warehouse       | PostgreSQL 16 (via Docker)    |
| Transformation  | dbt (dbt-postgres)            |
| Orchestration   | Dagster + dagster-dbt         |
| Dependency Mgmt | uv                            |
| SQL Linting     | SQLFluff                      |
| Testing         | pytest                        |

---

## Project Structure

```
data-platform-forge/
├── .dlt/                        # dlt pipeline configuration
├── dbt/
│   └── dbt_project/             # dbt models (staging, marts)
├── scripts/
│   └── init-warehouse.sql       # PostgreSQL schema initialization
├── src/
│   └── data_platform/
│       └── orchestrator/        # Dagster definitions and assets
├── tests/
│   └── orchestrator/            # pytest test suite
├── docker-compose.yml           # PostgreSQL warehouse container
├── pyproject.toml               # Project dependencies (uv)
├── Makefile                     # Common dev commands
├── .sqlfluff                    # SQL linting config
└── .env                         # Environment variables (not committed)
```

---

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (Python package manager)
- Python 3.10+

### 1. Clone the repository

```bash
git clone https://github.com/shahidmalik4/data-platform-forge.git
cd data-platform-forge
```

### 2. Configure environment variables

Copy the example and fill in your values:

```bash
cp .env.example .env
```

Required variables:

```env
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_db
POSTGRES_PORT=5432
```

### 3. Install dependencies

```bash
make init
```

### 4. Start the PostgreSQL warehouse

```bash
docker compose up -d
```

This spins up a PostgreSQL 16 container and runs `scripts/init-warehouse.sql` to initialize the schema.

### 5. Run the ingestion pipeline

```bash
make run-dlt
```

Loads raw data into the warehouse using dlt pipelines.

### 6. Run dbt transformations

```bash
make dbt-run
```

Transforms raw data through staging and mart layers.

### 7. Run dbt tests

```bash
make dbt-test
```

### 8. Launch the Dagster UI

```bash
make dagster
```

Visit `http://localhost:3000` to view asset lineage, run pipelines, and monitor jobs.

---

## Available Make Commands

| Command        | Description                              |
|----------------|------------------------------------------|
| `make init`    | Install dependencies and sync uv         |
| `make dagster` | Start Dagster dev server                 |
| `make run-dlt` | Run dlt ingestion pipelines              |
| `make dbt-run` | Run dbt models                           |
| `make dbt-test`| Run dbt data quality tests               |
| `make lint`    | Run ruff and black linters               |
| `make format`  | Auto-format code with black              |
| `make clean`   | Remove temp files and dbt artifacts      |

---

## SQL Linting

This project uses [SQLFluff](https://docs.sqlfluff.com/) with the dbt templater to enforce consistent SQL style across all models.

```bash
uv run sqlfluff lint dbt/dbt_project
```

---

## Running Tests

```bash
uv run pytest
```

Tests live in `tests/orchestrator/` and cover Dagster asset definitions.

---

## Author

**Shahid Malik**
[LinkedIn](https://www.linkedin.com/in/shahidmalik4/) · [GitHub](https://github.com/shahidmalik4)
