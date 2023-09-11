Setup Django for Testing with `pytest`
##################################################

.. post:: 2023-09-10 13:00:00
   :tags: django,testing,django rest framework
   :category: django
   :author: ivan
   :language: en

   Test Driven Development is a popular software development practice which helps in creating
   better software. The practice that I prefer is a little bit relaxed practice that I call
   Test Assisted Development as sometimes tests are not written before the production code (but
   let's leave this discussion for another place and time).
   Django projects also need to be thoroughly tested. Let's configure our Django project for
   testing with `pytest` before even creating
   the first Django application.

.. contents:: Table of Contents
   :local:
   :depth: 3

Overview
************

There are multiple approaches and frameworks for testing Django projects. We are going to
use `pytest` as test framework and `pytest_django` package.

Tests are stored in `elearn/tests` directory and follow the package structure of the
project being tested.

Test file name should start with `test_` in order to be discoverble by `pytest`. One can
decide on different naming convention and modify the test configuration.

Install `pytest`
*****************

.. code-block:: none
   :caption: requirements.txt

   # ...
   pytest
   pytest-django
   # ....

.. code-block:: console

   $ pip install -U requirements.txt
   ...

Configure Django for Tests
**********************************

Normally all tests should be executed against the same configuration that is being used
to run the project in production. However there might be additional settings, e.g.
fake Django applications or test management API application etc. that need to be specified
only during testing.

To make things simple and straightforward I like defining separate `settings` modules for
three types of environments:

- `settings.py` -- the default configuration, used in production
- `settings_local.py`-- the local development configuration
- `settings_test.py` -- the configurtion used when running tests

Here is what the test configuration looks like:

.. code-block:: python
   :caption: elearn/settings_test.py

   from .settings import *

At this moment it is just an empty shell that imports all the configuration settings from
the default project configuration. We will start adding settings while developing the project.

Configure `pytest`
******************************

There are many ways to configure `pytest`. Here are just some of the options:

- Use `pytest.ini <https://docs.pytest.org/en/stable/reference/customize.html#pytest-ini>`__.
- Use `pyproject.toml <https://docs.pytest.org/en/stable/reference/customize.html#pyproject-toml>`__.
- Use `setup.cfg`

All methods use the same configuration settings, just are different in where the configuration settings are
stored and slightly different on the syntax.

We are using `setup.cfg` to configure `pytest` as it is well supported by Visual Studio Code (VSCode):

.. code-block:: ini
   :caption: setup.cfg
   :linenos:

   [tool:pytest]
   addopts = --rootdir elearn -s -vv --import-mode importlib
   testpaths =
      elearn/tests
   DJANGO_SETTINGS_MODULE = elearn.settings_test

Here is the same configuration, but using `pyproject.toml`:

.. code-block:: ini
   :caption: pyproject.toml
   :linenos:

   [tool.pytest.ini_options]
   addopts = "--rootdir elearn -s --import-mode importlib"
   testpaths = [
      "elearn/tests",
   ]
   DJANGO_SETTINGS_MODULE = "elearn.settings_test"

Setup test directories
***************************

- Create `elearn/tests` directory
- Add empty `__init__.py` file into it

.. code-block:: console

   $ mkdir elearn/tests
   $ touch elear/tests/__init__.py

Our First Test Case
*********************

Let's create our first test case which confirms our project is up and running,
configured correctly and is serving Swagger interface.

We will put our test file in `elearn` test sub-package. So let's first create
an empty test `elearn` sub-package:

.. code-block:: console

   $ mkdir elearn/tests/elearn
   $ touch elearn/tests/elearn/__init__.py

Now we can create a simple test file:

.. code-block::
   :caption: elearn/tests/elearn/test_hello_elearn.py

   def test_hello_elearn(client):
      response = client.get("/docs/")
      assert response.status_code == 200

Run all the tests:

.. code-block:: console

   $ pytest
   ========================= test session starts =========================
   platform win32 -- Python 3.10.2, pytest-7.4.2, pluggy-0.13.1
   django: settings: elearn.settings_test (from ini)
   rootdir: D:\Sandbox\repos\django-elearn
   configfile: pyproject.toml
   testpaths: elearn/tests
   plugins: anyio-3.6.2, cov-4.0.0, django-4.5.2
   collected 1 item

   elearn/tests/elearn/test_hello.py::test_hello_elearn PASSED

   ========================== 1 passed in 0.53s ==========================

The test case uses a Django test client, provided as `pytest` fixture by the `pytest-djang`
extension. The test case makes a `GET` request to the Swagger documentation page (`/docs/`)
and asserts that the response was a success response.

