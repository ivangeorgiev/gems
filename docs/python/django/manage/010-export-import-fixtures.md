# Import and export data fixtures in Django


## Export database table as fixture

You could export a single model into a JSON file:

```bash
$ python src/manage.py -Xutf8 dumpdata <application>.<model> -o path/to/file.json
```

Example:
```bash
$ python src/manage.py dumpdata auth.users -o .dev/fixtures/users.json
```

## Delete all the records in a table

To delete all the records in a table (model):
1. Start a Django shell

```bash
$ python src/manage.py
```

2. Delete the records using the Django model

```python
from auth import users

users.objects.all().delete()
exit()
```

## Load a fixture into a database table

To load the fixture data into the database table:

```
$ python src/manage.py -Xutf8 loaddata path/to/file.json
```

Example:
```bash
$ python src/manage.py -Xutf8 loaddata .dev/fixtures/users.json
```
