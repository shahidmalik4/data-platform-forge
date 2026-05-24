from dagster import asset, AssetExecutionContext, Output

from data_platform.ingestion.pipeline.run_dlt_pipeline import (
    run_customers_pipeline,
    run_products_pipeline,
    run_orders_pipeline,
)


# Customers
@asset(
    key="ingestion_customers",
    group_name="ingestion",
    compute_kind="dlt",
)
def ingestion_customers(context: AssetExecutionContext):
    context.log.info("Starting customers ingestion pipeline...")
    result = run_customers_pipeline()
    context.log.info("Customers ingestion completed.")
    return result


# Products
@asset(
    key="ingestion_products",
    group_name="ingestion",
    compute_kind="dlt",
)
def ingestion_products(context: AssetExecutionContext):
    context.log.info("Starting products ingestion pipeline...")
    result = run_products_pipeline()
    context.log.info("Products ingestion completed.")
    return result


# Orders / Order Items
@asset(
    key="ingestion_orders",
    group_name="ingestion",
    compute_kind="dlt",
    deps=["ingestion_customers", "ingestion_products"],
)
def ingestion_orders(context):
    context.log.info("Starting orders pipeline...")

    load_info = run_orders_pipeline()

    return load_info