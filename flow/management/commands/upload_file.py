from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from flow.models import FileUpload
from flow.tasks import save_file_to_database
from flow.utils import upload_file_path, get_filename_ext
import os
import shutil


class Command(BaseCommand):
    """
    copy large file directly to media_root, and store the absolute url to
    FileUpload project. After, celery task read csv file to Meter table
    """

    help = 'Copy file to web database'

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='+', type=str)

    def handle(self, *args, **options):
        for p in options['path']:
            name, ext = get_filename_ext(p)
            relative_path = upload_file_path(None, p)
            target_path = os.path.join(os.path.join(settings.MEDIA_ROOT,upload_file_path(None, p)))
            direname = os.path.dirname(target_path)
            try:
                os.makedirs(direname+'/')
            except FileExistsError:
                pass
            file_uploaded = FileUpload.objects.filter(filename=name)
            if file_uploaded.exists():
                self.stdout.write(self.style.ERROR('File "%s" was uploaded already' % name))
            else:
                try:
                    # copy file to media root
                    shutil.copy2(p, target_path)
                except Exception as e:
                    raise CommandError(e)
                # save absolute url to FileUpload object
                file_upload_obj = FileUpload()
                file_upload_obj.filename = name
                file_upload_obj.file.name = target_path
                file_upload_obj.save()
                # write csv to databases
                save_file_to_database.delay(file_upload_obj.pk)

                self.stdout.write(self.style.SUCCESS('Success!'))

