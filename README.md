This is a DRF project using python 3.11

Run the tests using:

```python manage.py test```

Run the linter:
```ruff .```

By default it uses sqlite, so before running one needs to run migrations and import data, alternatively it can load data on startup from a csv file to a temporary db
To set the csv file use the environment variable as below:
```USE_CSV=titanic.csv python manage.py runserver```

The server exposes the DRF browsable API at: http://127.0.0.1:8000/api/

The passenger list at http://127.0.0.1:8000/api/passenger/
One passenger at http://127.0.0.1:8000/api/passenger/ID_GOES_HERE
One may also filter the fields returned using the fields GET PARAMETER:

http://127.0.0.1:8000/api/passenger/1?fields=Age
http://127.0.0.1:8000/api/passenger/1?fields=Age&fields=Survived

To access the fares price histogram as a png file:
http://127.0.0.1:8000/api/fare-histogram/

openapi schema generated using:
```python manage.py spectacular --color --file schema.yml```
it may be accessed at 127.0.0.1:8000/schema

swagger UI at: http://127.0.0.1:8000/schema/swagger-ui/