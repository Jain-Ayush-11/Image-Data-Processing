import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"image_processing.settings")

app = Celery("task")

app.config_from_object("django.conf:settings", namespace="CELERY")

# periodic tasks
app.conf.beat_schedule = {
    # NOTE: Currently the time is set very low for testing and output purposes, 
    #       should be increased accordingly
    'process-pending-requests': {
        'task': 'core.tasks.process_pending_requests',
        'schedule': crontab(minute='*/1'),  # Every 1 minutes
    },
    'reconcile-failed-requests': {
        'task': 'core.tasks.reconcile_failed_requests',
        'schedule': crontab(minute='*/10'),  # Every 10 minutes
    },
}

app.autodiscover_tasks()