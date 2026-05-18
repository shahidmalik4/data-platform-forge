from dagster import ScheduleDefinition
from .jobs import data_pipeline_job

daily_schedule = ScheduleDefinition(
    job=data_pipeline_job,
    cron_schedule="0 2 * * *",
)