Setup PostgreSQL Sandbox with Docker
=======================================

In this recipe we will use Docker and Docker compose to setup a PostgreSQL sandbox. The sandbox will run following services:

- PostgreSQL database server
- Pgadmin

Although we call it sandbox, the environment preserves the data and configuration between sessions. You can start and stop the environment without loosing configuration and data.

Define the environment
----------------------------------------------------------

To define our environment, we need to describe it to Docker compose. Create a ``docker-compose.yml`` file with the following environment definition:

.. code-block:: yaml
   :caption: docker-compose.yml

    version: '3.8'

    services:
    pgdb:
        image: postgres
        restart: always
        environment:
            - POSTGRES_USER=postgres
            - POSTGRES_PASSWORD=postgres
        ports:
            - '5432:5432'
        volumes: 
            - pgdb:/var/lib/postgresql/data

    pgadmin:
        container_name: pgadmin4_container
        image: dpage/pgadmin4
        restart: always
        environment:
        PGADMIN_DEFAULT_EMAIL: admin@admin.com
        PGADMIN_DEFAULT_PASSWORD: postgres
        ports:
            - "5050:80"
        volumes:
            - pgadmin:/var/lib/pgadmin
    
    volumes:
        pgdb:
            driver: local
        pgadmin:
            driver: local

Start the environment
-----------------------

.. code-block:: console

    $ docker compose up

To open ``pgadmin``, navigate the web browser to `http://localhost:5050 <http://localhost:5050>`__.
To login ``pagadmin``:

- Admin email: ``admin@admin.com``
- Admin password: ``postgres``

If this is the first time you login to ``pgadmin``, you need to create a database server. Use following settings:

- General

  - Name: ``my-db``

- Connection

  - Host name/address: ``pgdb``
  - Username: ``postgres``
  - Password: ``postgres``
 

Shutdown the environment
-------------------------

.. code-block:: console

    $ docker compose down


Further reading
----------------

- `pgadmin 4 container <https://www.pgadmin.org/download/pgadmin-4-container/>`__
- `pgadmin container mapped files and directories <https://www.pgadmin.org/docs/pgadmin4/latest/container_deployment.html#mapped-files-and-directories>`__


.. https://geshan.com.np/blog/2021/12/docker-postgres/
.. https://towardsdatascience.com/how-to-run-postgresql-and-pgadmin-using-docker-3a6a8ae918b5

