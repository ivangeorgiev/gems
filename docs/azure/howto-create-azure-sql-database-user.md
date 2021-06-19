---
reference:
  - https://azure.microsoft.com/en-us/blog/adding-users-to-your-sql-azure-database/
  - https://www.sqlnethub.com/blog/creating-azure-sql-database-logins-and-users/
  - https://docs.microsoft.com/en-us/azure/azure-sql/database/authentication-aad-configure?tabs=azure-powershell
---

# How to database logins and users for Azure SQL Database

This quick tip, talks about creating Azure SQL Database logins and users after you have performed an initial setup of your Azure SQL Database server and defined the admin user. I will also show how database user can be removed and how to keep track on assigned roles.

## Create Database contained users

### Step 1. Create database login

```sql
CREATE LOGIN <login-name> WITH password='<password>';
```

You must be connected to the master database on SQL Azure with the administrative login (which you get from the SQL Azure portal) to execute the CREATE LOGIN command. Connect to your Azure SQL Database server as an admin via SQL Server Management Studio or Azure Data Studio.

### Step 2. Create database user

```sql
CREATE USER <user-name> FROM LOGIN <login-name>;
```

Users are created per database and are associated with logins. You must be connected to the database in where you want to create the user. In most cases, this is not the master database. 

Consider specifying default schema for the user:

```sql
-- add database user for login testLogin1
CREATE USER [<user-name>]
  FROM LOGIN [<login-name>]
  WITH DEFAULT_SCHEMA=dbo;
```



### Step 3. Grant database permissions

```sql
EXEC sp_addrolemember 'db_datareader', '<user-name>';
```

You could grant permissions also using `ALTER ROLE`:

```sql
ALTER ROLE db_owner ADD MEMBER [<user-name>];
```

For more information on available roles and assigned permissions, check [Database-Level Roles](https://docs.microsoft.com/en-us/sql/relational-databases/security/authentication-access/database-level-roles?view=sql-server-ver15) page.

Commonly used roles are:

* `db_datareader` - Members of the **db_datareader** fixed database role can read all data from all user tables and views. User objects can exist in any schema except *sys* and *INFORMATION_SCHEMA*.
* `db_datawriter` - Members of the **db_datawriter** fixed database role can add, delete, or change data in all user tables.
* `db_ddladmin` - Members of the **db_ddladmin** fixed database role can run any Data Definition Language (DDL) command in a database.
* `db_owner` - Members of the **db_owner** fixed database role can perform all configuration and maintenance activities on the database, and can also drop the database in SQL Server. This role should be used with extreme caution.

## Create contained users mapped to Azure AD identities

Here is an example of creating database contained users mapped to Azure AD identity:

```sql
CREATE USER [bob@contoso.com] FROM EXTERNAL PROVIDER;
CREATE USER [alice@fabrikam.onmicrosoft.com] FROM EXTERNAL PROVIDER;
```

To create a contained database user representing an application that connects using an Azure AD token:

```sql
CREATE USER [appName] FROM EXTERNAL PROVIDER;
```

As next step you need to grant database permissions to the user.

Earlier I have published a post on [how to connect and query Azure SQL database using AD token using Python and pyodbc](howto-connect-and-query-sql-database-with-token-using-python-and-pyodbc.md) and [how to use Managed Identity in Azure to connect to Azure SQL Database using Python and pyodbc](how-to-connect-sql-database-app-service-managed-identity-python-pyodbc.md).

## Remove database user

Here is an example of removing a database user:

```sql
DROP USER [appName]
```



## List roles assigned to a user

To list the roles assigned to a user in a database, you need to be in the database.

```sql
SELECT r.name role_principal_name, m.name AS member_principal_name
FROM sys.database_role_members rm 
JOIN sys.database_principals r 
    ON rm.role_principal_id = r.principal_id

JOIN sys.database_principals m 

    ON rm.member_principal_id = m.principal_id
WHERE m.name = '<user-name>'
```

To list roles assigned to all users, remove the filter predicate.

```sql
SELECT r.name role_principal_name, m.name AS member_principal_name
FROM sys.database_role_members rm 
JOIN sys.database_principals r 
    ON rm.role_principal_id = r.principal_id

JOIN sys.database_principals m 

    ON rm.member_principal_id = m.principal_id
ORDER BY m.name, r.name;
```

