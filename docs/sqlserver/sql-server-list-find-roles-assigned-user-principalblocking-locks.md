---
created: 2020-09-12 06:00:00
tags: sql server, mssql, roles, users
---

# List or find roles assigned to a principal / user in SQL Server (MSSQL) Database

## Problem

You use SQL Server. You to know which roles were granted to which users (database principals).

## Solution

To find all the role assignments to users in SQL Server database, you can use the following query.

```sql
SELECT r.name role_principal_name, 
       m.name AS member_principal_name
  FROM sys.database_role_members rm 
  JOIN sys.database_principals r 
       ON rm.role_principal_id = r.principal_id
  JOIN sys.database_principals m 
       ON rm.member_principal_id = m.principal_id
 WHERE r.type = 'R';
```

You can also limit the list of roles to only the roles, assigned to a particular user or principal by adding a filtering condition to the WHERE clause.

```sql
DECLARE @PrincipalName VARCHAR(128) = 'principal-name-here'
SELECT r.name role_principal_name, 
       m.name AS member_principal_name
  FROM sys.database_role_members rm 
  JOIN sys.database_principals r 
       ON rm.role_principal_id = r.principal_id
  JOIN sys.database_principals m 
       ON rm.member_principal_id = m.principal_id
 WHERE r.type = 'R'
       AND m.name = @PrincipalName;
```

You can find this solution also as GitHub gist [list-principal-roles.sql](https://gist.github.com/ivangeorgiev/8db4631372cc8a9e8981f51860524143#file-list-principal-roles-sql).