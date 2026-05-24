import os

from celery import Celery
from celery.signals import setup_logging
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("electronics_store")
app.conf.broker_connection_retry_on_startup = True
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@setup_logging.connect
def setup_celery_logging(*args, **kwargs) -> None:
    pass
