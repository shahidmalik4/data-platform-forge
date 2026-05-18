from dagster import AssetSelection, define_asset_job
from dagster_dbt import build_dbt_asset_selection

from .dlt_assets import ingestion_asset
from .dbt_assets import dbt_models


# Select all dbt models + their dependencies (sources, upstream assets)
dbt_selection = build_dbt_asset_selection(
    [dbt_models],
    dbt_select="tag:daily or fqn:*",
).required_multi_asset_neighbors()


# Select single ingestion asset
ingestion_selection = AssetSelection.assets(ingestion_asset)


# Final job: ingestion → dbt
data_pipeline_job = define_asset_job(
    name="data_pipeline_job",
    selection=ingestion_selection | dbt_selection,
)