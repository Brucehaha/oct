from django.db import transaction
import os
import random
from datetime import date
import pandas as pd
import logging

logger = logging.getLogger(__name__)


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
    # could use uuid4
    file_rand = random.randint(1, 1000000000)
    name, ext = get_filename_ext(filename)

    foldername = date.today().strftime('%Y%b%d')
    file_path = 'csv/%s/' % foldername
    filename = '{name}_{file_rand}{ext}'.format(
        foldername=foldername,
        name=name,
        file_rand=file_rand,
        ext=ext
    )
    full_filename = file_path + filename
    return full_filename


def read_file(filenamme):
    """
    Add other read method e.g. read.fwf with fixed formated data
    :param filenamme: file path to proccess
    :return: np.read_csv or np.read_excel
    """
    _, ext = get_filename_ext(filenamme)
    if ext == ".csv":
        return  pd.read_csv
    else:
        return  pd.read_excel


def import_to_database(file, chunksize=3, usecols=[1, 3, 6, 13, 14, 19], encoding='utf8'):
    """

    :param filename: file path
    :param chunksize: lazy read large file by chunk
    :param usecols: columns used for importing to database
    :param encoding: encoding type, could change if has encoding error
    :return:
    """
    from .models import Meter, FileUpload

    readfile = read_file(file.file.name)

    try:
        # roll back if any error
        with transaction.atomic():
            df = readfile(
                file.file.name,
                skiprows=1,
                chunksize=chunksize,
                usecols=usecols,
                names=['nmi', 'registerid', 'meterserialnumber', 'CurrentRegisterRead', 'CurrentRegisterReadDateTime', 'uom'],
                dtype='string',
                encoding=encoding
            )
            for chunk in df:
                objs = []
                for index, row in chunk.iterrows():
                    if not isinstance(row[0], pd._libs.missing.NAType):
                        objs.append(Meter(
                            nmi=row[0],
                            registerid=row[1],
                            meterserialnumber=row[2],
                            currentregisterread=row[3],
                            updatedatetime=row[4],
                            uom=row[5],
                            filename=file
                        ))
                Meter.objects.bulk_create(objs)
    except UnicodeDecodeError as e:
        file.message = e
        file.status = FileUpload.ERROR
        file.save()
        raise UnicodeDecodeError(e)
    except Exception as e:
        file.message = e
        file.status = FileUpload.ERROR
        file.save()
        logger.error(e)

