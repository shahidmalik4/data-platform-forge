from dagster import asset, AssetExecutionContext

from data_platform.ingestion.pipeline.run_dlt_pipeline import run_pipeline


@asset(
    key="ingestion_asset",
    group_name="ingestion",
    compute_kind="dlt",
)
def ingestion_asset(context: AssetExecutionContext):
    context.log.info("Starting dlt ingestion pipeline...")

    result = run_pipeline()

    context.log.info("dlt ingestion pipeline completed.")

    return result