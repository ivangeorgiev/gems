Split CSV string into multiple rows in SQL Server (MSSQL)
================================================================

.. post:: 2023-11-20 10:23:00
   :tags: mssql, sql server, azure sql database
   :category: sql server
   :author: ivan
   :language: en

To split a string into multiple rows using a separator, use the the `SPLIT_STRING` table-valued function.
This is very useful in situations where one column is holding a comma serpareted list of values.
Another very common situation is a passing configuration from external tools - e.g. Azure Data Factory
passes a list of tables to be processed.

.. code-block:: sql
    :caption: Split comma-separated value string

    DECLARE @table_names_csv NVARCHAR(400) = 'order,,order_item'

    SELECT value AS table_name
      FROM STRING_SPLIT(@table_names_csv, ',')
     WHERE RTRIM(value) <> '';

The output from above SQL is a set of rows - one row for each non-empty value:

.. code-block::

    order
    order_item


Split CSV string in a column
--------------------------------

To "expand" a table on a column which ontains a CSV string:

.. code-block:: sql
    :caption: Split comma-separated value string in a column

    SELECT product.id00, value as tag
    FROM product
        CROSS APPLY STRING_SPLIT(product.tags, ',');

This technique could be used also for filtering, e.g. products which have given tag assigned:

.. code-block:: sql
    :caption: Filter products with matching tag assigned in CSV column

    SELECT product.id00, value as tag
      FROM product
     WHERE EXISTS (SELECT 1 FROM STRING_SPLIT(tags, ',') WHERE tag = 'sports')

To match multiple tags:

.. code-block:: sql
    :caption: Filter products with matching tags assigned in CSV column

    SELECT product.id00, value as tag
      FROM product
     WHERE EXISTS (SELECT 1 FROM STRING_SPLIT(tags, ',') WHERE tag IN ('sports', 'man'))



Links
---------------

* `STRING_SPLIT table-valued function Documentation <https://learn.microsoft.com/en-us/sql/t-sql/functions/string-split-transact-sql>`__
