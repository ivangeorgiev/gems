Setup a New Django Project
###########################


Create and Activate Virtual Environment
*****************************************

.. code-block:: console

   $ python -m venv .venv
   $ source .venv/Scripts/activate

Install Django and Dependencies
********************************

Create a `requirements.txt` file. At this moment we put inside only `django` as the only
requirement for the project:

.. code-block:: none
   :emphasize-lines: 1

   django

Install Django as defined in `requirements.txt`:

.. code-block:: console

   $ pip install -r requirements.txt
   ...

Create Django Project
************************

To create a new Django project:

.. code-block:: console

   $ django-admin startproject elearn

At this time you can already preview the project by running a development server:

.. code-block:: console

   $ python elear/manage.py migrate    # Apply all pending database migrations
   Operations to perform:
     Apply all migrations: admin, auth, contenttypes, sessions
   Running migrations:
     Applying contenttypes.0001_initial... OK
     Applying auth.0001_initial... OK
     Applying admin.0001_initial... OK
     Applying admin.0002_logentry_remove_auto_add... OK
     Applying admin.0003_logentry_add_action_flag_choices... OK
     Applying contenttypes.0002_remove_content_type_name... OK
     Applying auth.0002_alter_permission_name_max_length... OK
     Applying auth.0003_alter_user_email_max_length... OK
     Applying auth.0004_alter_user_username_opts... OK
     Applying auth.0005_alter_user_last_login_null... OK
     Applying auth.0006_require_contenttypes_0002... OK
     Applying auth.0007_alter_validators_add_error_messages... OK
     Applying auth.0008_alter_user_username_max_length... OK
     Applying auth.0009_alter_user_last_name_max_length... OK
     Applying auth.0010_alter_group_name_max_length... OK
     Applying auth.0011_update_proxy_permissions... OK
     Applying auth.0012_alter_user_first_name_max_length... OK
     Applying sessions.0001_initial... OK

   $ python elearn/manage.py runserver # Start a development server

   Watching for file changes with StatReloader
   Performing system checks...

   System check identified no issues (0 silenced).
   September 09, 2023 - 16:57:28
   Django version 4.2.5, using settings 'elearn.settings'
   Starting development server at http://127.0.0.1:8000/
   Quit the server with CTRL-BREAK.

You can open the browser and navigate to `<http://127.0.0.1:8000/>`__ to see the default Django project page.

Start a New Django Application
********************************

To start a new Django application, use the Django command line inteface `django-admin`:

.. code-block:: console

   $ cd elearn
   $ django-admin startapp courses

The new application needs to be registered in the project's `settings.py`:

.. code-block:: python
   :caption: elearn/settings.py
   :linenos:
   :emphasize-lines: 4-6

   # ...
   INSTALLED_APPS = [
      # ...
      # 3rd party apps
      # Local apps
      "courses",
   ]
   # ...

We append the `courses` project in the `INSTALLED_APPS` list. The `3rd party apps` and `Local apps` commented lines we keep
to visually organize registered applications in three categories:

- Django core applications
- 3rd party applications, e.g. Swagger API interface generator
- Local applications which are part of our local Django project

