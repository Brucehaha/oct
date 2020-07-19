from .models import Meter
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


def read_file(filenamme):
    """
    Add other read method e.g. read.fwf with fixed formated data
    :param filenamme: file path to proccess
    :return: np.read_csv or np.read_excel
    """
    filename, ext = get_filename_ext(filenamme)
    if ext == "csv":
        return filename, pd.read_csv
    else:
        return filename, pd.read_excel


def import_to_database(filename, chunksize=3, usecols=[1, 3, 6, 13, 14, 19]):
    readfile = read_file(filename)
    objs =list
    try:
        df = readfile(
            filename,
            skiprows=1,
            chunksize=chunksize,
            usecols=usecols,
            names=['nmi', 'registerid', 'meterserialnumber', 'CurrentRegisterRead', 'CurrentRegisterReadDateTime', 'uom'],
            dtype='string', )

        for chunk in df:
            for index, row in chunk.iterrows():
                if not isinstance(row[0], pd._libs.missing.NAType):
                    meter = Meter
                    meter.file.name = filename
                    meter.filename = filename
                    objs = objs.append(meter)
            Meter.objects.bulk_create(objs)
    except Exception as e:
        logger.error(e)

