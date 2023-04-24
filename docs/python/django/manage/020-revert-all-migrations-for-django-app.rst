Revert All Migrations for Django App
==============================================

Doing it the normal way
-----------------------------

If all migrations are consistent, you could Django's migrate command:

.. code-block:: bash

   python manage.py migrate myapp zero

This will revert all applied migrations for application `myapp`.

Doing it brute-force
--------------------------

Sometimes things could be messed-up. Django's `migrate` command fails.

In this case you could fix the database schema manually and than faike the migrations.

Step 1. Manually drop foreign key constraints and tables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

I use following SQL to generate DDL statements to drop all tables for an application:

.. code-block:: sql

   SELECT
      CAST(
      'ALTER TABLE [' +  OBJECT_SCHEMA_NAME(parent_object_id) +
      '].[' + OBJECT_NAME(parent_object_id) +
      '] DROP CONSTRAINT [' + name + '];'
      AS TEXT)
   FROM sys.foreign_keys
   WHERE referenced_object_id IN (
   select object_id(tab.name)
   from sys.tables as tab
   where
      schema_name(tab.schema_id) = 'dbo'
      AND tab.name Like 'TM_%'
   )

   UNION ALL

   select CAST('DROP TABLE ['+ tab.name + '];' AS TEXT)
   from sys.tables as tab
   where
      schema_name(tab.schema_id) = 'dbo'
      AND tab.name Like 'myapp_%'
   ;


Step 2. Fake Django migrations revert
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With following command, I instruct Django to revert all migrations for an application without altering the database schema.
This will just update Django's migration internal data.

.. code-block:: bash

   $ python manage.py migrate myapp zero --fake



