import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'email_sender_system.settings')

app = Celery('email_sender_system')


app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'resend-email': {
        'task': 'user.tasks.resend_email',
        'schedule': crontab(minute=settings.SCHEDULER_FOR_RETRY_EMAIL),
    },
}

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')