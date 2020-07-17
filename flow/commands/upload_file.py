from django.core.management.base import BaseCommand, CommandError
from flow.models import FileUpload
class Command(BaseCommand):
    help = 'Copy file to web database'

    def add_arguments(self, parser):
        parser.add_argument('file_path', nargs='+', type=str)

    def handle(self, *args, **options):
        for file in options['file_path']:

            pass

            self.stdout.write(self.style.SUCCESS('Successfully'))
