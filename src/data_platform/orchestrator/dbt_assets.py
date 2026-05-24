from pathlib import Path
from dagster_dbt import DagsterDbtTranslator, DagsterDbtTranslatorSettings

from dagster import AssetExecutionContext
from dagster_dbt import (
    DbtCliResource,
    DbtProject,
    DagsterDbtTranslator,
    DagsterDbtTranslatorSettings,
    dbt_assets,
)

# ----------------------------
# Resolve project root
# ----------------------------
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

# ----------------------------
# Custom translator (GROUPING LOGIC)
# ----------------------------
class GroupedDbtTranslator(DagsterDbtTranslator):

    def get_asset_spec(self, *args, **kwargs):

        dbt_resource_props = args[0]

        spec = super().get_asset_spec(*args, **kwargs)

        # ✅ SAFE extraction (handles multiple Dagster versions)
        fqn = (
            dbt_resource_props.get("fqn")
            or dbt_resource_props.get("path")
            or []
        )

        group = "default"

        if len(fqn) > 1:

            if fqn[1] == "staging":
                group = "staging"

            elif fqn[1] == "intermediate":
                group = "intermediate"

            elif fqn[1] == "marts":
                group = "marts"

            elif fqn[1] == "analytics":
                group = "analytics"

        return spec.replace_attributes(group_name=group)


# ----------------------------
# Translator instance
# ----------------------------
translator = GroupedDbtTranslator(
    settings=DagsterDbtTranslatorSettings(
        enable_duplicate_source_asset_keys=True,
    )
)

# ----------------------------
# dbt assets
# ----------------------------
@dbt_assets(
    manifest=dbt_project.manifest_path,
    dagster_dbt_translator=translator,
)
def dbt_models(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()