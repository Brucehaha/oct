from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .utils import import_to_database
from .models import FileUpload
import logging

logger = logging.getLogger(__name__)




@shared_task
def add(a, b):
    print(a*b)


@shared_task(bind=True)
def save_file_to_database(self, file_pk):
    files = FileUpload.objects.filter(pk=file_pk)
    if files.exists():
        file = files.first()
        # make status to pending avoiding celery task process the same task
        file.status = FileUpload.PENDING
        file.task_id = self.request.id
        file.save()
        try:
            import_to_database(file)
            file.status = FileUpload.SUCCESS
            file.save()
        except UnicodeError as e:
            try:
                # could add more encoding type
                import_to_database(file, encoding='iso-8859-1')
                file.status = FileUpload.SUCCESS
                file.save()
            except:
                file.status = FileUpload.ERROR
                file.message = e
                file.save()
                logger.error(e)
        except Exception as e:
            file.message = e
            file.save()
            logger.error(e)

