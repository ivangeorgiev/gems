
Setup the Project for Django REST Framework
###############################################

.. post:: 2023-09-09 15:00:00
   :tags: django,django rest framework, drf
   :category: django
   :author: ivan
   :language: en

   Install Django REST Framework and implement Swagger interface for the API.


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

We need also to do a litle work to define a view for our Swagger interface and register it
the `/docs/` url for it.

.. code-block:: python
   :caption: elearn/views.py
   :linenos:
   :emphasize-lines: 1-16

   from drf_yasg.views import get_schema_view
   from drf_yasg import openapi
   from rest_framework import permissions

   schema_view = get_schema_view(
      openapi.Info(
         title="BEL",
         default_version='v1',
         description="Brith E-Learning (BEL) API",
         terms_of_service="https://www.bel.local/bel/terms/",
         contact=openapi.Contact(email="contact@bel.local"),
         license=openapi.License(name="BSD License"),
      ),
      public=True,
      permission_classes=(permissions.AllowAny,),
   )

.. code-block:: python
   :caption: elearn/urls.py
   :linenos:
   :emphasize-lines: 3,7

   from django.contrib import admin
   from django.urls import path
   from .views import schema_view


   urlpatterns = [
      path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
      path('admin/', admin.site.urls),
   ]


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
