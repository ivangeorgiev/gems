Setting Up Fake Django Application for Testing with Pytest
##############################################################

.. post:: 2023-09-30 12:00:00
   :tags: django,testing,testdrive,pytest,core
   :category: django
   :author: ivan
   :language: en

Sometimes we need to test our code in a context of a Django application. Usually this code implements
generic components, e.g. custom Django fields. We could always test our components in the context of our Django
application, but this breaks the requirement for test isolation. To overcome this problem we could create a
Django application which is intended for testing the specific components.

Create The Application
****************************************

.. code-block:: console

   $ cd tests
   $ django-admin startapp fake_app


Modify the Application name
****************************************

Because `django-admin` doesn't support applications in sub-packages, we need to change the name, assigned to our application in the application config:

.. code-block:: python
   :caption: tests/fake_app/apps.py
   :linenos:
   :emphasize-lines: 5

   from django.apps import AppConfig

   class FakeAppConfig(AppConfig):
      default_auto_field = 'django.db.models.BigAutoField'
      name = 'tests.fake_app'


Register the Application in Django Settings
**********************************************

To isolate the test harness from production code, we register the fake application only in the Django settings module
used for testing:

.. code-block:: python
   :caption: iris/settings_test.py
   :linenos:
   :emphasize-lines: 3-5

   from .settings import *

   INSTALLED_APPS.extend([
      "tests.fake_app",
   ])


Create Migrations
************************************

Do not forget that when creating migrations you need to specify the testing Django settings module:

.. code-block:: console

   $ DJANGO_SETTINGS_MODULE=iris.settings_test python iris/manage.py makemigrations


