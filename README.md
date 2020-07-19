# Start app(python3.4 env)
## run code
1. pip install -r requirements.txt
2. python manage.py makemigrations
3. python manage.py migrate
4. celery -A oct  worker --loglevel=info

# run test
python manage.py test

# upload excel
python manage.py upload_file /path/to/excel.csv

# view uploaded file and search record
python manage.py createsuperuser
login to localhost:800/admin
click Meter table and then try to search data


