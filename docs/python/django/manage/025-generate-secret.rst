Generate Secret for Django App
==================================

Start yor python interpreter and execute following script:

.. code-block:: python

    import secrets
    print(secrets.token_urlsafe(32))

Alternatively you can execute the python script inline:

.. code-block:: bash

   python -c "import secrets; print(secrets.token_urlsafe(32))"

