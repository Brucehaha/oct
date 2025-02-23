from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oct.settings')

app = Celery('oct')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# #comment back below code if you need a beat task
# app.conf.beat_schedule = {
#     # Executes every Monday morning at 7:30 a.m.
#     'every-20-second': {
#         'task': 'flow.tasks.save_file_to_database',
#         'schedule': 59,
#     },
# }
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
