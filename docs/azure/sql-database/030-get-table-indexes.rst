Get a List of Table Indexes in SQL Server
================================================================

.. post:: 2023-11-20 09:27:00
   :tags: mssql, sql server, azure sql database
   :category: sql server
   :author: ivan
   :language: en

Following SQL Server statement will return a list of all index names for a table `dbo.sales`.

.. code-block:: sql

    SELECT idx.name
    FROM 
        sys.indexes idx
    JOIN 
        sys.objects obj
        ON idx.object_id = obj.object_id
    WHERE 
        obj.type_desc = 'USER_TABLE'
        AND schema_name(obj.schema_id) = 'dbo'
        AND obj.name = 'sales'
    ;

List only non-clustered indexes
----------------------------------

In case you need only non-clustered index:

.. code-block:: sql

    SELECT idx.name
    FROM 
        sys.indexes idx
    JOIN 
        sys.objects obj
        ON idx.object_id = obj.object_id
    WHERE 
        idx.type_desc = 'NONCLUSTERED'
        AND obj.type_desc = 'USER_TABLE'
        AND schema_name(obj.schema_id) = 'dbo'
        AND obj.name = 'sales'
    ;

List indexes in CSV
----------------------

To make a CSV list of indexes:

.. code-block:: sql

    DECLARE @sql AS VARCHAR(MAX)='';

    SELECT @sql = @sql + idx.name + ','
    FROM 
        sys.indexes idx
    JOIN 
        sys.objects obj
        ON idx.object_id = obj.object_id
    WHERE 
        idx.type_desc = 'NONCLUSTERED'
        AND obj.type_desc = 'USER_TABLE'
        AND schema_name(obj.schema_id) = 'dbo'
        AND obj.name = 'sales'
    ;

    SELECT @sql;

