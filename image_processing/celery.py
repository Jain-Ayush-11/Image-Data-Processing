import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"task.settings")

app = Celery("task")

app.config_from_object("django.conf:settings", namespace="CELERY")

# periodic tasks
app.conf.beat_schedule = {
    'process-pending-requests-every-hour': {
        'task': 'myapp.tasks.process_pending_requests',
        'schedule': crontab(minute=10),  # Every 10 minutes
    },
}

app.autodiscover_tasks()