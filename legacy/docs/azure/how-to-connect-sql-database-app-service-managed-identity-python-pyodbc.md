---
reference:
  - https://stackoverflow.com/questions/61867652/use-managed-identity-to-authenticate-azure-app-service-to-sql-database
  - https://hedihargam.medium.com/python-sql-database-access-with-managed-identity-from-azure-web-app-functions-14566e5a0f1a
  - https://github.com/AzureAD/azure-activedirectory-library-for-python/wiki/Connect-to-Azure-SQL-Database
---

# Connect to Azure SQL Database from App Service using Python, pyodbc and Managed Identity

## Preparation

### Step 1. Assign Managed Identity to App Service

From Azure Portal, open the App Service and select Settings -> Identity from the left menu. Make sure the system assigned managed identity Status is set to On. If not, update it and save the configuration.

Connect with SSH to verify that Managed Identity has been successfully enabled:

```bash
$ env | grep IDENTITY
IDENTITY_ENDPOINT=http://172.16.0.4:8081/msi/token
IDENTITY_HEADER=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

### Step 2. Create Database Contained User

```sql
CREATE USER <app-name> FROM EXTERNAL PROVIDER;
ALTER ROLE db_datareader ADD MEMBER <app-name>
ALTER ROLE db_datawriter ADD MEMBER <app-name>
ALTER ROLE db_ddladmin ADD MEMBER <app-name>
```

 For more information see: https://docs.microsoft.com/en-us/azure/azure-sql/database/authentication-aad-configure?tabs=azure-powershell#create-contained-database-users-in-your-database-mapped-to-azure-ad-identities

### Step 3. Update SQL Server Firewall Settings

1.  Open your SQL Server in Azure Portal
2. *Select Security -> Firewall and virtual networks* from the left menu
3. Make sure *Allow Azure services and resources to access this server* is set to *Yes*

## Test Database Connection

### Method 1. Using Integrated Managed Identity authentication

Create file `test_python_msi.py`:

```python
import os
import pyodbc

# Configuration
db_azure_server = os.environ['DB_SERVER']
db_server = f'{db_azure_server}.database.windows.net'
db_database = os.environ['DB_DATABASE']

connection_string = f"Driver={{ODBC Driver 17 for SQL Server}};Server={db_server};Database={db_database};Authentication=ActiveDirectoryMsi"

with pyodbc.connect(connection_string) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT getdate()")
        row = cursor.fetchone()
        print(row[0])    
```

Execute the file to test the connectivity:

```bash
$ python test_pyodbc_msi.py
2021-06-13 19:06:10.387000
```



### Method 2. Using Managed Identity Token

Connect to the App Service using SSH and execute following code (see [Query SQL Database from Python using pyodbc and access token](howto-connect-and-query-sql-database-with-token-using-python-and-pyodbc.md)). Place the code in file `test_pyodbc_msi_token.py`

```python
import os
import pyodbc
import requests 
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

    connect_kwargs = add_pyodbc_args_for_access_token(db_token)
    with pyodbc.connect(connection_string, **connect_kwargs) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT getdate()")
            row = cursor.fetchone()
            print(row[0])    
    ```
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
    

identity_endpoint = os.environ["IDENTITY_ENDPOINT"]
identity_header = os.environ["IDENTITY_HEADER"]
resource_uri="https://database.windows.net/"
token_auth_uri = f"{identity_endpoint}?resource={resource_uri}&api-version=2019-08-01"
head_msi = {'X-IDENTITY-HEADER':identity_header}
resp = requests.get(token_auth_uri, headers=head_msi)
access_token = resp.json()['access_token']

# Configuration
db_azure_server = os.environ['DB_SERVER']
db_server = f'{db_azure_server}.database.windows.net'
db_database = os.environ['DB_DATABASE']

connection_string = f"Driver={{ODBC Driver 17 for SQL Server}};Server={db_server};Database={db_database}"

connect_kwargs = add_pyodbc_args_for_access_token(access_token)
with pyodbc.connect(connection_string, **connect_kwargs) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT getdate()")
        row = cursor.fetchone()
        print(row[0])    

```

Test the connectivity by executing the Python script:

```bash
$ python test_pyodbc_msi_token.py
2021-06-13 19:12:54.210000
```











