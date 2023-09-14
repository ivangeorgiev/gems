Log Django SQL Queries to Terminal
##############################################################

.. post:: 2023-09-14 12:00:00
   :tags: django,database,core
   :category: django
   :author: ivan
   :language: en

Sometimes you might need to be able to log Django SQL queries. You might want to 
print them to the terminal or send them to a remote logging system. In this example
I show you how to create Django middleware which logs the SQL queries executed by HTTP
session to the terminal.

.. literalinclude:: assets/db_sql_terminal_logging_middleware.py
   :caption: db_sql_terminal_logging_middleware.py
   :linenos:

You can download the source from :download:`here <assets/db_sql_terminal_logging_middleware.py>`.
