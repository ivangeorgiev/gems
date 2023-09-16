Register Django Model in Admin
########################################################################

.. post:: 2023-09-11 15:30:00
   :tags: django,orm,database diagram,erd,er diagram
   :category: django
   :author: ivan
   :language: en

There are multiple methods to register a model in Django admin. I will show you
how to register a single model (one by one for multiple), all the models in an
application and all the models in the project.

Register Specific Model(s) in Application's `admin.py`
*********************************************************

You can register one or more models in the application's `admin.py` module using the
`admin.site.register()` method:

.. code-block:: python
   :caption: courses/admin.py

   from django.contrib import admin
   from .models import Subject, Course, Module, Content

   admin.site.register(Subject)
   admin.site.register(Course)
   admin.site.register(Module)
   admin.site.register(Content)


Register All Application Models
**********************************

You can register all the models in the application's `admin.py` module using the
`admin.site.register()` method enumerating the models:

.. code-block:: python
   :caption: courses/admin.py

   from django.contrib import admin
   from django.apps import apps

   app_models = apps.get_app_config('courses').get_models()

   for model in app_models:
      try:
         admin.site.register(model)
      except admin.sites.AlreadyRegistered:
         pass


Register All Models from Django Project
****************************************

This code needs to be placed in the project's package under `admin` module:

.. code-block:: python
   :caption: elearn/admin.py

   from django.contrib import admin
   from django.apps import apps

   all_models = apps.get_models()

   for model in all_models:
      try:
         admin.site.register(model)
      except admin.sites.AlreadyRegistered:
         pass

For this code to work, you need to register your project package as Django application:

.. code-block:: python
   :caption: elearn/settings.py


   INSTALLED_APPS = [
      # ...
      # 3rd party apps
      # ...
      # Local apps
      'elearn'
      'courses',
   ]

Of course you can add this code in any application from your project, but is considered smelly practice.
It introduces implicit dependency from this particular application to all Django applications. When working
with such code, for example, it might be very difficult to find out where exactly this registration takes
place.
