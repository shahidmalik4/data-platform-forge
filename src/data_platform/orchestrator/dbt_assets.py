from pathlib import Path

from dagster import AssetExecutionContext
from dagster_dbt import DbtCliResource, DbtProject, DagsterDbtTranslator, DagsterDbtTranslatorSettings, dbt_assets

BASE_DIR = Path(__file__).resolve().parent
while not (BASE_DIR / "pyproject.toml").exists():
    if BASE_DIR == BASE_DIR.parent:
        raise RuntimeError("Could not find project root")
    BASE_DIR = BASE_DIR.parent

DBT_PROJECT_DIR = BASE_DIR / "dbt" / "dbt_project"

dbt_project = DbtProject(
    project_dir=DBT_PROJECT_DIR,
    packaged_project_dir=DBT_PROJECT_DIR,
)
dbt_project.prepare_if_dev()

dbt_resource = DbtCliResource(
    project_dir=dbt_project,
    profiles_dir=DBT_PROJECT_DIR,
)

# Allow multiple dbt sources to share the same upstream Dagster asset key
# This is correct because all 4 tables are produced by a single ingestion_asset
translator = DagsterDbtTranslator(
    settings=DagsterDbtTranslatorSettings(
        enable_duplicate_source_asset_keys=True,
    )
)


@dbt_assets(
    manifest=dbt_project.manifest_path,
    dagster_dbt_translator=translator,
)
def dbt_models(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()