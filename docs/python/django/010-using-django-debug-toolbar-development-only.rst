Development-Only Django Debug Toolbar
================================================

`Django Debug Toolbar <https://django-debug-toolbar.readthedocs.io/en/latest/>`__ is a handy
development tool. It provides tons of useful instruments for developers.

Django Debug Toolbar should be used only in development environments. It should not be even
installed on production environments. This requires to use different setups for production
and development environments.

The technique described is not limited only to Django Debug Toolbar. It could be used to
isolate dependencies and tools which are required only during development.

.. note::
   Django Debug Toolbar is enabled and shown only if Django server is started:

   - in debug mode (`DEBUG=True`)
   - with development-only settings module, e.g. `DJANGO_SETTINGS_MODULE=mdapi.settings_dev`

Step 1. Create requirements-dev.txt file
------------------------------------------

Create a `requirements-dev.txt` file and move into it all development-only dependencies
from `requirements.txt`:

.. code-block::
   :caption: <project-root-dir>/requirements-dev.txt

   -r ./requirements.txt
   django-debug-toolbar
   pytest
   pytest-django

In my `requirements-dev.txt` I have *django-debug-toolbar*, *pytest* and *pytest-django* as
development dependencies. Generic dependencies are also included by using a reference to
`requirements.txt`.

To install development virtual environment you should use `requirements-dev.txt` instead of `requirements.txt`:

.. code-block:: bash

   $ pip install -r requirements-dev.txt


Step 2. Create `settings_dev` module
--------------------------------------

Create `settings_dev.py` in your Django project directory:

.. code-block:: python
   :caption: <project-package-dir>/settings_dev.py

   from .settings import *
   from django.urls import include, path

   globals().setdefault('DEBUG', False)

   if DEBUG:
      MIDDLEWARE += [
         'debug_toolbar.middleware.DebugToolbarMiddleware',
      ]

      INTERNAL_IPS = [
         '127.0.0.1',
      ]

      DEV_URLS = [
         path('__debug__/', include("debug_toolbar.urls")),
      ]

This is configuration file defines settings for development-only dependencies.
All settings from the project's `settings` module are inherited.

Step 3. Add development-only urls
----------------------------------

.. code-block:: python
   :caption: <project-package-dir>/urls.py

   # ..
   from django.conf import settings

   # ...
   if getattr(settings, "DEBUG", False):
      urlpatterns += getattr(settings, "DEV_URLS", [])

Step 4. Start Development Server
----------------------------------

To start development server with development settings, define `DJANGO_SETTINGS_MODULE`
environment variable which points to our development settings module:

.. code-block:: bash

   $ export DJANGO_SETTINGS_MODULE=<project-module>.settings_dev
   $ python manage.py runserver


Start Debug Development Server with Visual Studio Code (VSCode)
----------------------------------------------------------------

With VSCode you could create/update your `launch.json` file to
define proper environment variables. Here is an example I use:

.. code-block:: json
   :caption: .vscode/launch.json

   {
      "version": "0.2.0",
      "configurations": [
         {
               "name": "Python: Django My Code",
               "type": "python",
               "request": "launch",
               "program": "${workspaceFolder}\\manage.py",
               "args": [
                  "runserver"
               ],
               "django": true,
               "justMyCode": true,
               "env": {
                  "DJANGO_SETTINGS_MODULE": "mdapi.settings_dev"
               }
         },
         {
               "name": "Python: Django",
               "type": "python",
               "request": "launch",
               "program": "${workspaceFolder}\\manage.py",
               "args": [
                  "runserver"
               ],
               "django": true,
               "justMyCode": false,
               "env": {
                  "DJANGO_SETTINGS_MODULE": "mdapi.settings_dev"
               }
         }
      ]
   }
