from io import StringIO
from django.core.management import call_command
from unittest import mock, TestCase
from flow.models import FileUpload


@mock.patch('os.path.exists', return_value=True)
@mock.patch('shutil.copy2', return_value=True)
class ManagementCommandTest(TestCase):

    def test_command_output_success(self, mock_exists, mock_copy2):
        out = StringIO()
        path='/path/test.csv'
        call_command('upload_file',{'path':path}, stdout=out)
        existed = FileUpload.objects.filter(filename='test').exists()
        self.assertIn('Success!', out.getvalue())
        self.assertEqual(existed, True)

    def test_command_output_failure(self, mock_exists, mock_copy2):
        out = StringIO()
        path='/path/test.csv'
        call_command('upload_file', {'path':path}, stdout=out)
        self.assertIn('File "test" was uploaded already', out.getvalue())

