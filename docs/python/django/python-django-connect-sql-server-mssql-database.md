# Connect Django to Microsoft SQL Server (MSSQL) Database

We need to connect Django to a Microsoft SQL Server. In addition, we have some more requirements to the way we implement the connectivity:

* Connect Django to Microsoft SQL Server and Azure SQL Database
* Keep database tables organized into a single database schema
* Be able to easily configure the database settings
* Be able to change the database engine (e.g. locally work with SQLite, on production work with Azure SQL Database)

We are going to use `mssql-django` package which is a fork of `django-mssql-backend`. It uses internally the `pyodbc` package.

## Setup Database Connectivity

Install the `mssql-django` package:

```bash
$ pip install mssql-django
...
```

Update your `settings.py` for your Django project. Here is an example. For further details, refer to the `mssql-django` package [documentation](https://github.com/microsoft/mssql-django):

```python
DATABASES = {
    'default': {
        # String. It must be "mssql".
        'ENGINE': 'mssql',
        
        # String. Database name. Required.
        'NAME': 'mydb',
        
        # String. Database user name in "user" format. If not given then MS Integrated Security will be used.
        'USER': 'user@myserver',
        
        # String. Database user password.
        'PASSWORD': 'password',
        
         # String. SQL Server instance in "server\instance" format.
        'HOST': 'myserver.database.windows.net',
        
        # String. Server instance port. An empty string means the default port.
        'PORT': '',

        # Dictionary. Additional database settings.
        'OPTIONS': {
            # String. ODBC Driver to use ("ODBC Driver 17 for SQL Server", 
            # "SQL Server Native Client 11.0", "FreeTDS" etc). 
            # Default is "ODBC Driver 17 for SQL Server".
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    },
}

```



## Setup the Database Schema for Django Application

Django maintains database tables in the default schema. There is no way to specify which schema to use for storing the tables. Best solution is to define the default schema for the application database user (technical user).

We would like that all application tables are stored inside single schema, called `myapp`. We need to make sure that:

1. `myapp` schema exists in the target database
2. application user owns the `myapp` schema (recommended)
3. the default schema for our application user is set to `myapp`

Here are some SQL statements that could be used to achieve this:

```sql
IF NOT EXISTS (SELECT 1 FROM information_schema.schemata WHERE schema_name = 'myapp' )
BEGIN
   EXEC('CREATE SCHEMA [myapp] AUTHORIZATION [user@myserver);
END

EXEC('ALTER USER [user@myserver] WITH DEFAULT_SCHEMA = [myapp]');

```



## Configure the Database using Environment Variables

For flexible, easy configuration, we are using the [`django-environ`  package](https://django-environ.readthedocs.io/en/latest/).

```bash
$ pip install django-environ
```



Modify Django `settings.py` file:

```python
import environ

# environ maps mssql engine to django's default mssql engine
environ.Env.DB_SCHEMES['mssql'] = 'mssql'
env = environ.Env(DEBUG=(bool,False))

# Use SQLite database if DATABASE_URL environment variable is not set 
DEFULT_DATABASE_URL = f'sqlite:///{urllib.parse.quote(str(BASE_DIR / "db.sqlite3"))}'

DATABASE_URL = os.environ.get('DATABASE_URL', DEFULT_DATABASE_URL)
os.environ['DJANGO_DATABASE_URL'] =  DATABASE_URL.format(**os.environ)

DATABASES = {
    'default': env.db('DJANGO_DATABASE_URL', default=DEFULT_DATABASE_URL)
}
```

Here is an example for environment variable definitions for Windows:

```bash
SET "DATABASE_URL=mssql://user@myserver:password@ddos01-d-01-sqlsrv.database.windows.net:/mydb?driver=ODBC Driver 17 for SQL Server"
```

Database URL is processed as standard Python template string, against the environment variables dictionary. This allows that we could build connection string, referring other environment variables:

```bash
SET "DATABASE_USER=user@myserver"
SET "DATABASE_PWD=password"
SET "DATABASE_URL=mssql://{DATABASE_USER}:{DATABASE_PWD}@ddos01-d-01-sqlsrv.database.windows.net:/mydb?driver=ODBC Driver 17 for SQL Server"
```

One scenario where this could be used is - Azure WebApp. You could define database username and database password as application settings, [referred from Key Vault](https://docs.microsoft.com/en-us/azure/app-service/app-service-key-vault-references).

## Summary

To achieve flexible, usable connectivity from Django to SQL Server:

- Use `mssql-django` and `django-environ`  packages.
- Configure default schema for the technical database user.
- Use environment variable(s) to define the database connectivity.

