from django.contrib import admin
from .models import FileUpload, Meter


class FileUploadAdmin(admin.ModelAdmin):
    list_display = ('filename', 'status', 'date')


admin.site.register(FileUpload, FileUploadAdmin)


class MeterAdmin(admin.ModelAdmin):
    list_display = ('nmi', 'registerid','meterserialnumber', 'currentregisterread', 'updatedatetime', 'uom', 'filename')
    search_fields = ['currentregisterread', 'updatedatetime', 'nmi', 'meterserialnumber']


admin.site.register(Meter, MeterAdmin)
