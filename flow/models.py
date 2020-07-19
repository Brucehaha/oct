from django.db import models
from .utils import upload_file_path


class FileUpload(models.Model):
    """
    store the file upload by management command or by rest api
    'file' file path
    'filename' is unique by assumption
    'status' indicate if the file upload has been import to database
    'message' store some message e.g. error message,  after importing to Meter model
    'task_id' storing the task id from celery function if later you want to import large file to Meter model which is
    also use for check the importing progress with celery.
    """
    SUCCESS, ERROR, PENDING, NONE = 1, 0, 2, 3
    STATUS_CHOICE = (
        (SUCCESS, 'success'),
        (ERROR, 'error'),
        (PENDING, 'pendding'),

    )

    file = models.FileField(upload_to=upload_file_path, blank=False, null=False, verbose_name='CSV/Excel File')
    filename = models.CharField(max_length=50, unique=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICE, default=NONE)
    message = models.CharField(max_length=200, null=True)
    task_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.filename


class Meter(models.Model):
    """store the data imported from FileUpload
        ● NMI
        ● Meter serial number
        ● The reading value
        ● When the reading happened
        ● The filename of the flow file
    """
    nmi = models.CharField(max_length=10, blank=True, null=True)
    registerid = models.CharField(max_length=10, blank=True, null=True)
    meterserialnumber = models.CharField(max_length=12, blank=True, null=True)
    currentregisterread = models.CharField(max_length=15, blank=True, null=True)
    updatedatetime = models.CharField(max_length=16,blank=True, null=True)
    uom = models.CharField(max_length=5,blank=True, null=True)
    filename = models.ForeignKey(FileUpload,blank=True, null=True, on_delete=models.SET_NULL)



