from __future__ import absolute_import, unicode_literals
from celery.schedules import crontab
from celery.task import periodic_task
from .utils import import_to_database
from .models import FileUpload
import logging


logger = logging.getLogger(__name__)


@periodic_task(run_every=crontab(minute="*/1"))
def save_file_to_database():
    file = FileUpload.objects.filter(status=FileUpload.NONE)
    try:
        import_to_database(file.file.name)
    except Exception as e:
        logger.error(e)

