from celery import Celery
from celery.schedules import crontab

from core.config import settings

celery_app = Celery(
    "dataqguard",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["tasks.rule_executor"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    beat_schedule={
        "check-scheduled-rules": {
            "task": "tasks.rule_executor.check_scheduled_rules",
            "schedule": 60.0,  # Every minute
        },
    }
)
