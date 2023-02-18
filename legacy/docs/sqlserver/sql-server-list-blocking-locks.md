---
created: 2020-09-12 06:00:00
tags: sql server, mssql, locks
---

# List blocking locks in SQL Server (MSSQL) Database

## Problem

You use SQL Server and you need to know which sessions are blocked and for what reason.

## Solution

Use the following query to get a list of blocked sessions.

```sql
SELECT p.cmd,
       p.*
  FROM sys.sysprocesses p
 WHERE blocked > 0
```

You can find this solution also as GitHub gist [list-blocking-locks.sql](https://gist.github.com/ivangeorgiev/8db4631372cc8a9e8981f51860524143#file-list-blocking-locks-sql).

