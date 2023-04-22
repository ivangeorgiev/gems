Get a List of Foreign Key Constraints for a Table in SQL Server
================================================================

Following SQL Server statement will return a list of `ALTER TABLE` statements which
drop all foreign key constraints for a table.

.. code-block:: sql

   SELECT
      'ALTER TABLE [' +  OBJECT_SCHEMA_NAME(parent_object_id) +
      '].[' + OBJECT_NAME(parent_object_id) +
      '] DROP CONSTRAINT [' + name + ']'
   FROM sys.foreign_keys
   WHERE referenced_object_id = object_id('my-table')

