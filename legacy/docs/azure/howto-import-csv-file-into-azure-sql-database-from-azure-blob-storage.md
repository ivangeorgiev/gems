---
reference:
  - https://docs.microsoft.com/en-us/azure/azure-sql/load-from-csv-with-bcp
  - bcp samples.city in "C:\mydata\city.csv" -F 2 -S contoso-sqlsrv.database.windows.net -d contoso-sqldb -U baobab -P contoso564-Pwd -q -c -t  ,
---

# Import CSV file from Azure Blob Storage into Azure SQL Database using T-SQL

## Scenario

We have a storage account named `contoso-sa` which contains container `dim-data`. File `city.csv` is stored in the `data` container.

We are going to import the `city.csv` file into a table `city` from `samples` database schema.

Here is a sample from the `city.csv` file:

```
name,population
Abilene,115930
Akron,217074
Albany,93994
Albuquerque,448607
Alexandria,128283
Allentown,106632
Amarillo,173627
Anaheim,328014
Anchorage,260283
Ann Arbor,114024
```

## Preparation

First you need to create SAS token that will be used to access the Blob Storage from SQL Database. SAS token needs to provide at least read permission on the object that should be loaded (`srt=o&sp=r`).

You also need make sure that SQL Server firewall is configured to enable access to the server from all networks.

Your database needs to also master encryption key created. For example, you could use the following SQL:

```sql
CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'YourStrongPassword1';
```

## Import CSV file using T-SQL

### Step 1: Create target schema and target table

```sql
CREATE SCHEMA [samples];

CREATE TABLE [samples].[city](
	[name] [text] NOT NULL,
	[population] [int] NOT NULL
)
GO
```



### Step 2: Created database credential

The database credential is used to access the blob storage:

```sql
CREATE DATABASE SCOPED CREDENTIAL MyAzureBlobStorageCredential
 WITH IDENTITY = 'SHARED ACCESS SIGNATURE',
 SECRET = 'sv=....';
```

Make sure that leading `?` is not included in the SAS token.

### Step 3: Create external data source

To access files in the blob container, you create external data source:

```sql
CREATE EXTERNAL DATA SOURCE MyAzureBlobStorage
WITH ( TYPE = BLOB_STORAGE,
          LOCATION = 'https://contoso-sa.blob.core.windows.net/dim-data'
          , CREDENTIAL= MyAzureBlobStorageCredential --> CREDENTIAL is not required if a blob is configured for public (anonymous) access!
);
```



### Step 4: Use `BULK INSERT` to import the CSV file

Let's import the `city.csv` file into the `samples.city` table. Target table must exist.

```sql
BULK INSERT samples.city
FROM 'city.csv'
WITH (DATA_SOURCE = 'MyAzureBlobStorage',
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',  --CSV field delimiter
    ROWTERMINATOR = '\n'   --Use to shift the control to next row
);
```

You can verify the result:

```sql
SELECT * FROM samples.city;
```

Here is a sample output created using [mssql-cli](https://docs.microsoft.com/en-us/sql/tools/mssql-cli?view=sql-server-ver15):

```
contoso-sqldb> SELECT * FROM samples.city;
Time: 1.309s (a second)
+-------------------------+--------------+
| name                    | population   |
|-------------------------+--------------|
| Abilene                 | 115930       |
| Akron                   | 217074       |
| Albany                  | 93994        |
| Albuquerque             | 448607       |
| Alexandria              | 128283       |
| Allentown               | 106632       |
| Amarillo                | 173627       |
| Anaheim                 | 328014       |
| Anchorage               | 260283       |
| Ann Arbor               | 114024       |
+-------------------------+--------------+
(10 rows affected)
contoso-sqldb>
```



## Further reading

* [Use BULK INSERT or OPENROWSET(BULK...) to import data to SQL Server](https://docs.microsoft.com/en-us/sql/relational-databases/import-export/import-bulk-data-by-using-bulk-insert-or-openrowset-bulk-sql-server?view=sql-server-ver15)

