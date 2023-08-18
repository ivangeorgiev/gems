Log SQL for Django's Database Queries 
======================================

.. code-block:: python

    import logging
    l = logging.getLogger('django.db.backends')
    l.setLevel(logging.DEBUG)
    l.addHandler(logging.StreamHandler())

