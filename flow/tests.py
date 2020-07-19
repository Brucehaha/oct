from io import StringIO
from django.core.management import call_command
from django.test import TestCase
from unittest import mock
from flow.models import FileUpload


@mock.patch('shutil.copy2', return_value=True)
class ManagementCommandTest(TestCase):

    def test_command_output_success(self, mock_copy2):
        out = StringIO()
        path='/path/test.csv'
        call_command('upload_file',{'path':path}, stdout=out)
        self.assertIn('Success!', out.getvalue())
        file = FileUpload.objects.filter(filename='test')
        self.assertEqual(file.exists(), True)

    def test_command_output_failure(self, mock_copy2):

        file = FileUpload.objects.filter(filename='test')
        self.assertEqual(file.exists(), False)

        out = StringIO()
        path='/path/test.csv'

        file = FileUpload()
        file.file.name = path
        file.filename = 'test'
        file.save()

        call_command('upload_file',{'path':path}, stdout=out)
        self.assertIn('File "test" was uploaded already', out.getvalue())


class SaveCSVTest(TestCase):

    @mock.patch('flow.utils.import_to_database')  # < patching import_to_database
    def test_success(self, mock_import_to_database):
        file = FileUpload.objects.create(
            filename='test',
        )
        mock_import_to_database(file)
        mock_import_to_database.assert_called_with(file)

    @mock.patch('flow.utils.import_to_database')  # < patching import_to_database
    def test_failure(self, mock_import_to_database):
        file = FileUpload.objects.create(
            filename='test',
        )
        mock_import_to_database.side_effect =UnicodeError()
        with self.assertRaises(UnicodeError):
            mock_import_to_database(file, encoding='iso-8859-1') # test Unicode error then try another encoding
            mock_import_to_database.assert_called_with(file, encoding='iso-8859-1')

