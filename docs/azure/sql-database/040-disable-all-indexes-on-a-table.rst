Disable all non-clustered indexes for a table in SQL Server
================================================================

.. post:: 2023-11-20 09:39:00
   :tags: mssql, sql server, azure sql database
   :category: sql server
   :author: ivan
   :language: en

Building on :doc:`/azure/sql-database/030-get-table-indexes` here is a SQL script which allows you to
disable all non-clustered indexes for a table in SQL server. In the following example, use build a 
DDL statement which disables all non-clustered indexes for a table:

.. code-block:: sql
    :caption: Disable all non-clustered indexes on MSSQL table using generated DDL statement

    DECLARE @sql AS VARCHAR(MAX)='';

    -- Generate a string with DDL statement.
    -- Each statement in the string disables on index on the target table.
    -- DDLs are separated by semicolon and CRLF.
    SELECT @sql = @sql + 
        'ALTER INDEX ' + idx.name + ' ON  [dbo].[' + obj.name + '] DISABLE;' +CHAR(13)+CHAR(10)
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

    EXEC(@sql);

Use cursor to disable all non-clustered indexes for a table in MSSQL
-----------------------------------------------------------------------

If you prefer, you could execute individual `ALTER INDEX` statements using a cursor:

.. code-block:: sql
    :caption: Disable all non-clustered indexes on MSSQL table using cursor

    DECLARE @stmt NVARCHAR(2000)
    DECLARE @stmnts CURSOR

    -- For each index, generate ALTER INDEX DDL statement
    SET @stmnts = CURSOR FOR
        SELECT 'ALTER INDEX ' + idx.name + ' ON  [dbo].[' + obj.name + '] DISABLE;'
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

    -- Iterate over generated DDL statements and execute each one of them
    OPEN @stmnts
    FETCH NEXT
    FROM @stmnts INTO @stmt
    WHILE @@FETCH_STATUS = 0
    BEGIN
        EXEC (@stmt)
        FETCH NEXT
        FROM @stmnts INTO @stmt
    END

    CLOSE @stmnts
    DEALLOCATE @stmnts

Enable all non-clustered indexes for a table in MSSQL
------------------------------------------------------

If you need the opposite - enable all non-clustered indexes on a MSSQL table, change the `DISABLE` keyword 
in above `ALTER INDEX` statements to `REBUILD`:


.. code-block:: sql
    :caption: Enable all non-clustered indexes on MSSQL table

    DECLARE @sql AS VARCHAR(MAX)='';

    SELECT @sql = @sql + 
        'ALTER INDEX ' + idx.name + ' ON  [dbo].[' + obj.name + '] REBUILD;' +CHAR(13)+CHAR(10)
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

    EXEC(@sql);
