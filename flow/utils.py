from uuid import uuid4
import os
import random
from datetime import date


def get_filename_ext(filename):
    base_name = os.path.basename(filename)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_file_path(instance, filename):
    """

    :param instance:
    :param filename:
    :param unique: True if allow file upload only one time
    :return:
    """

    file_rand = random.randint(1, 1000000000)
    name, ext = get_filename_ext(filename)
    foldername = date.today().strftime('%Y%b%d')
    full_filename = 'csv/{foldername}/{name}_{file_rand}.{ext}'.format(
        foldername=foldername,
        name=name,
        file_rand=file_rand,
        ext=ext
    )
    return full_filename

