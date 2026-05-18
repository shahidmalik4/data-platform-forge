import os
from dotenv import load_dotenv
import time

import dlt
import psycopg2

from data_platform.ingestion.dlt_resources.dlt_customers import customers_resource
from data_platform.ingestion.dlt_resources.dlt_products import products_resource
from data_platform.ingestion.dlt_resources.dlt_orders import orders_resource

load_dotenv(override=False)

SCHEMA = os.getenv("POSTGRES_SCHEMA", "raw")

pipeline = dlt.pipeline(
    pipeline_name="etl_forge_pipeline",
    destination="postgres",
    dataset_name=SCHEMA
)


def get_postgres_conn():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )


def print_load_info(load_info):
    conn = get_postgres_conn()
    cur = conn.cursor()

    print("\nLoad Summary:\n")
    tables_seen = set()

    for package in load_info.load_packages:
        for job in package.jobs.get("completed_jobs", []):
            table = job.job_file_info.table_name

            if table in tables_seen:
                continue

            tables_seen.add(table)

            cur.execute(f'SELECT COUNT(*) FROM "{SCHEMA}"."{table}"')
            count = cur.fetchone()[0]

            print(f"✔ {SCHEMA}.{table}: {count} rows")

    cur.close()
    conn.close()


def run_pipeline():
    # Load base tables first
    for resource_func in [customers_resource, products_resource]:
        load_info = pipeline.run(resource_func())
        print_load_info(load_info)

    # Ensure commit visibility
    print("[INFO] Waiting for data availability...")
    time.sleep(2)

    # Load dependent table
    load_info = pipeline.run(orders_resource())
    print_load_info(load_info)


if __name__ == "__main__":
    run_pipeline()