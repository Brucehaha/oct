# Start app(python3.4 env)
## run code
1. pip install -r requirements.txt
2. python manage.py makemigrations
3. python manage.py migrate
4. celery -A oct  worker --loglevel=info

## run test
python manage.py test

## upload excel
python manage.py upload_file /path/to/excel.csv

## view uploaded file and search record
python manage.py createsuperuser
login to localhost:800/admin
click Meter table and then try to search data

# Maintainability 
1. management command copy large file to media_root and save file path to FilUpload table
2. celery task 'save_file_to_database' runs and import data to Meter table.
3. 'save_file_to_database' calls 'import_to_database' which is a function to clean
and read and write data by chunk to database for large data set. Chunksize is editable. 
4. Above functions can be used for process the data from rest API.
5. Error message from importing data could be found in FileUpload object message field and debug.log file

6. Assuming that the sequence of data's header is fixed.
7. Assuming that the data file is not only .csv, maybe other excel format. Here I use pandas.read_csv
and pandas.read_excel(could add more)
8. Assuming that the file encoding by default is utf8 or iso-8859-1.


