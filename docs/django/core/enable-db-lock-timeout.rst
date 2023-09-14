Enable Database Lock Timeout in Django 
##############################################################

.. post:: 2023-09-14 13:25:00
   :tags: django,sql database,core
   :category: django
   :author: ivan
   :language: en

By default clients requesting database lock should wait until the lock is released. This might take forever.
In locking contention situations it might be useful to instrument your database to timeout when lock is not 
being released for given amount of time, e.g. 5 seconds.

.. literalinclude:: assets/db_lock_timeout_middleware.py
   :caption: db_lock_timeout_middleware.py
   :linenos:

You can download the source from :download:`here <assets/db_lock_timeout_middleware.py>`.
