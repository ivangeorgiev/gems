Get a List of Table Columns in a Schema from SQL Server
========================================================

Following SQL query gets a list all table fields/columns in the `dbo` schema
where the table name starts with `MYAPP_`. Results are sorted by
table name and column id.

.. code-block:: sql
   :caption: list-table-columns.sql

   select schema_name(tab.schema_id) as schema_name,
      tab.name as table_name,
      col.column_id,
      col.name as column_name,
      t.name as data_type,
      col.max_length,
      col.precision
   from sys.tables as tab
      inner join sys.columns as col
         on tab.object_id = col.object_id
      left join sys.types as t
      on col.user_type_id = t.user_type_id
   where
      schema_name(tab.schema_id) == 'dbo'
      AND tab.name Like 'MYAPP_%'
   order by schema_name,
      table_name,
      column_id;

Meta
-----

- Created on: 2023-04-05
