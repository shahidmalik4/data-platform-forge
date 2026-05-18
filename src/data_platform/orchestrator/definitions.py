from dagster import Definitions

from .dlt_assets import ingestion_asset
from .dbt_assets import dbt_models, dbt_resource
from .jobs import data_pipeline_job
from .schedules import daily_schedule

defs = Definitions(
    assets=[
        # dlt assets
        ingestion_asset,

        # dbt assets
        dbt_models,
    ],
    jobs=[
        data_pipeline_job,
    ],
    schedules=[
        daily_schedule,
    ],
    resources={
        "dbt": dbt_resource,
    },
)