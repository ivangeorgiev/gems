---
reference:
  - https://www.linkedin.com/pulse/using-azure-ad-service-principals-connect-sql-from-python-andrade/
---

# Query SQL Database from Python using pyodbc and access token

pyodbc is an open source Python module that makes accessing ODBC databases simple. It implements the Python's [DB API 2.0](https://www.python.org/dev/peps/pep-0249) specification

If you want to learn more about pyodbc, check the [pypi page](https://pypi.org/project/pyodbc/) or the [pyodbc wiki](https://github.com/mkleehammer/pyodbc/wiki).

Connecting to a database using username and password is very convenient and easy. There are situations where we have a restriction to use token from Active Directory or Azure Active Directory.

Here is a Python function which you can be used to connect to a SQL Database using access token. I have created and tested it with personal users and service principals in Azure, using Azure Active Directory.

# Make it work

How to use Azure Active Directory with the ODBC driver is explained in [this article](https://docs.microsoft.com/en-us/sql/connect/odbc/using-azure-active-directory?view=sql-server-ver15). Based on it, I was able to connect to SQL Database using access token and pyodbc.

To configure the database connection I used environment variables:

```python
import osdb_azure_server = os.environ['DB_SERVER']
db_server = f'{db_azure_server}.database.windows.net'
db_database = os.environ['DB_DATABASE']
db_token = os.environ['DB_TOKEN']
```

Using the token and a few lines of code, I managed to connect and query the Azure SQL Database:

```python
import struct
import pyodbcSQL_COPT_SS_ACCESS_TOKEN = 1256
exptoken = b'';
for i in bytes(db_token, "UTF-8"):
    exptoken += bytes({i});
    exptoken += bytes(1);
tokenstruct = struct.pack("=i", len(exptoken)) + exptoken;conn = pyodbc.connect(connection_string, attrs_before = { SQL_COPT_SS_ACCESS_TOKEN:tokenstruct })
with conn.cursor() as cursor:
    cursor.execute("SELECT getdate()")
    row = cursor.fetchone()
    print(row[0])
```

The output from above example :

```
2021-04-23 08:45:50.153000
```

# Reuse it

To make above code more reusable I wrapped it into a function. The function is adding the `attrs_before` keyword attribute to be used in a `pyodbc.connect` call. This approach follows the best software design practices and provides high flexibility and maintainability of the client code.

```python
import structdef add_pyodbc_args_for_access_token(token:str, kwargs:dict=None):
   kwargs = kwargs or {}
    if (token):
        SQL_COPT_SS_ACCESS_TOKEN = 1256
        exptoken = b'';
        for i in bytes(token, "UTF-8"):
            exptoken += bytes({i});
            exptoken += bytes(1);
        tokenstruct = struct.pack("=i", len(exptoken)) + exptoken;
        kwargs['attrs_before'] = { SQL_COPT_SS_ACCESS_TOKEN:tokenstruct }
    return kwargs
```

# Full Code

Here is the function code with docstring documentation, which includes function, arguments and return result description along with example how to use it.

```python
import struct
def add_pyodbc_args_for_access_token(token:str, kwargs:dict=None):
    """
    Add pyodbc.connect arguments for SQL Server connection with token.
    
    Based on https://docs.microsoft.com/en-us/sql/connect/odbc/using-azure-active-directory?view=sql-server-ver15
    
    Parameters
    ----------
    token : str
        Access token.
    kwargs: dict
        Optional kwargs. If not provided, a new dictionary will be created.
        
    Returns
    -------
    dict
        Dictionary of pyodbc.connect keyword arguments.
Example:
    --------
    
    ```python
    import os
    import pyodbc
    
    # Configuration
    db_azure_server = os.environ['DB_SERVER']
    db_server = f'{db_azure_server}.database.windows.net'
    db_database = os.environ['DB_DATABASE']
    db_token = os.environ['DB_TOKEN']
    
    connection_string = f"Driver={{ODBC Driver 17 for SQL Server}};Server={db_server};Database={db_database}"
    connect_kwargs = add_pyodbc_args_for_access_token(db_token)
    with pyodbc.connect(connection_string, **connect_kwargs) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT getdate()")
            row = cursor.fetchone()
            print(row[0])
    """
    kwargs = kwargs or {}
    if (token):
        SQL_COPT_SS_ACCESS_TOKEN = 1256
        exptoken = b'';
        for i in bytes(token, "UTF-8"):
            exptoken += bytes({i});
            exptoken += bytes(1);
        tokenstruct = struct.pack("=i", len(exptoken)) + exptoken;
        kwargs['attrs_before'] = { SQL_COPT_SS_ACCESS_TOKEN:tokenstruct}
    return kwargs
```



# Further Reading

* [Connect to Azure SQL Database form Azure App Service using Python, Pyodbc and Managed Identity](how-to-connect-sql-database-app-service-managed-identity-python-pyodbc.md)