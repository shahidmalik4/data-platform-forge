from dagster import AssetSelection, define_asset_job
from dagster_dbt import build_dbt_asset_selection

from .dlt_assets import (
    ingestion_customers,
    ingestion_products,
    ingestion_orders,
)

from .dbt_assets import dbt_models


# ingestion selection
ingestion_selection = AssetSelection.assets(
    ingestion_customers,
    ingestion_products,
    ingestion_orders,
)


# dbt selection (unchanged)
dbt_selection = build_dbt_asset_selection(
    [dbt_models],
    dbt_select="tag:daily or fqn:*",
).required_multi_asset_neighbors()


# final pipeline job
data_pipeline_job = define_asset_job(
    name="data_pipeline_job",
    selection=ingestion_selection | dbt_selection,
)