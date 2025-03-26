from dagster import ScheduleDefinition
from .jobs import twitter_etl_job

twitter_etl_schedule = ScheduleDefinition(
    job=twitter_etl_job,
    cron_schedule="0 0 5 * *", # every 5th of the month at midnight
)