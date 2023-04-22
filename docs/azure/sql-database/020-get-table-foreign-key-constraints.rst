Get a List of Foreign Key Constraints in SQL Server
========================================================

.. code-block:: sql

   SELECT
      'ALTER TABLE [' +  OBJECT_SCHEMA_NAME(parent_object_id) +
      '].[' + OBJECT_NAME(parent_object_id) +
      '] DROP CONSTRAINT [' + name + ']'
   FROM sys.foreign_keys
   WHERE referenced_object_id = object_id('my-table')

