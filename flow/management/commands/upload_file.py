from django.core.management.base import BaseCommand, CommandError
from flow.models import FileUpload
from flow.utils import upload_file_path, get_filename_ext
import os
import shutil


class Command(BaseCommand):
    help = 'Copy file to web database'

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='+', type=str)

    def handle(self, *args, **options):
        for p in options['path']:
            name, ext = get_filename_ext(p)
            target_path = upload_file_path(None, p)
            if not os.path.exists(target_path):
                self.stdout.write(self.style.ERROR('File "%s" was uploaded already' % name))
            else:

                file_uploaded = FileUpload.objects.filter(filename=name)
                if file_uploaded.exists():
                    self.stdout.write(self.style.ERROR('File "%s" was uploaded already' % name))
                else:
                    try:
                        shutil.copy2(p, target_path)
                    except Exception as e:
                        raise CommandError(e)
                    file_upload_obj = FileUpload()
                    file_upload_obj.filename = name
                    file_upload_obj.file.name = target_path
                    file_upload_obj.save()
            self.stdout.write(self.style.SUCCESS('Success!'))
