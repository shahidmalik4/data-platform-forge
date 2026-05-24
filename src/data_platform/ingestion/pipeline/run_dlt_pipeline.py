import os
from dotenv import load_dotenv

import dlt
import psycopg2

from data_platform.ingestion.dlt_resources.dlt_customers import customers_resource
from data_platform.ingestion.dlt_resources.dlt_products import products_resource
from data_platform.ingestion.dlt_resources.dlt_orders import orders_resource
from data_platform.ingestion.generators.generate_orders import run_order_generation


load_dotenv(override=False)

SCHEMA = os.getenv("POSTGRES_SCHEMA", "raw")

pipeline = dlt.pipeline(
    pipeline_name="etl_forge_pipeline",
    destination="postgres",
    dataset_name=SCHEMA,
)


def get_postgres_conn():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )


def print_load_info(load_info):
    conn = get_postgres_conn()
    cur = conn.cursor()

    print("\nLoad Summary:\n")
    tables_seen = set()

    for package in load_info.load_packages:
        jobs = package.jobs or {}

        all_jobs = (
            jobs.get("completed_jobs", [])
            + jobs.get("failed_jobs", [])
            + jobs.get("started_jobs", [])
        )

        for job in all_jobs:
            table = job.job_file_info.table_name

            if table in tables_seen:
                continue

            tables_seen.add(table)

            cur.execute(f'SELECT COUNT(*) FROM "{SCHEMA}"."{table}"')
            count = cur.fetchone()[0]

            print(f"{SCHEMA}.{table}: {count} rows")

    cur.close()
    conn.close()


# FUNCTIONS PER DAGSTER ASSET
def run_customers_pipeline():
    load_info = pipeline.run(customers_resource())
    print_load_info(load_info)
    return load_info


def run_products_pipeline():
    print("[DEBUG] running products pipeline")

    load_info = pipeline.run(products_resource())

    if not load_info:
        raise RuntimeError("DLT returned empty load_info for products")

    print_load_info(load_info)
    return load_info


def run_orders_pipeline():
    print("[DEBUG] running orders pipeline")

    orders = run_order_generation()

    load_info = pipeline.run(orders_resource(orders))

    if not load_info:
        raise RuntimeError("orders pipeline returned None")

    print_load_info(load_info)
    return load_info


# Local debugging entrypoint
if __name__ == "__main__":
    print("Running full ingestion locally...")
    print("\nLoad Summary:\n")

    run_customers_pipeline()
    run_products_pipeline()

    import time
    time.sleep(2)

    run_orders_pipeline()

    print("\nIngestion Done")