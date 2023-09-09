##############################
Django REST Framework Cookbook
##############################


Setup the Project for Django REST Framework
###############################################

Install Django REST Framework
*******************************

Modify `requirements.txt` adding `djangorestframework` and `drf-yasg` as dependencies:

.. code-block:: none
   :caption: requirements.txt

   # ...
   djangorestframework
   # ...

We are using `drf-yasg` to generate Swagger interface for our API.

Run `pip` to reflect the changes:

.. code-block:: console

   $ pip install -r requirements.txt

Create Swagger interface for Our API
**************************************

We are using `drf-yasg` as Swagger interface generator so if not already installed, you need to install it:

.. code-block:: console

   $ pip install drf-yasg
   ...

`drf-yasg` is a Django application so you need to register it in the project's `settings.py`:

.. code-block:: python
   :caption: elearn/settings.py
   :emphasize-lines: 5

   # ...
   INSTALLED_APPS = [
      # ...
      # 3rd party apps
      'drf_yasg',
      # Local apps
      # ...
   ]
   # ...

Preview Our API Swagger interface
***********************************

Now you can run a development server:

.. code-block:: console

   $ python elearn/manage.py runserver
   Watching for file changes with StatReloader
   Performing system checks...

   System check identified no issues (0 silenced).
   September 09, 2023 - 17:22:26
   Django version 4.2, using settings 'elearn.settings'
   Starting development server at http://127.0.0.1:8000/
   Quit the server with CTRL-BREAK.

And navigate to http://127.0.0.1:8000/docs/ to see the brand new beautiful Swagger interface for our API.
It has no APIs defined as we haven't created any URLs yet.
