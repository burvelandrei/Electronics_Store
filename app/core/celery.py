import os

from celery import Celery
from celery.schedules import crontab
from celery.signals import setup_logging
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("electronics_store")
app.conf.broker_connection_retry_on_startup = True
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


app.conf.beat_schedule = {
    "restock-zero-items": {
        "task": "stores.tasks.restock_zero_items",
        "schedule": crontab(hour=9, minute=0),
    },
    "process-hourly-sales": {
        "task": "stores.tasks.process_hourly_sales",
        "schedule": crontab(minute=0),
    },
    "reset-daily-revenue": {
        "task": "stores.tasks.reset_daily_revenue",
        "schedule": crontab(hour=21, minute=15),
    },
}


@setup_logging.connect
def setup_celery_logging(*args, **kwargs) -> None:
    pass
