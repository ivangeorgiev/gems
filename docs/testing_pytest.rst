Testing with Pytest
====================

`Pytest`_ is arguably the most popular and widespread testing framework in the Python community. It is also compatible with Python's `unittest`_ and `doctest`_.


Generate XML report with `pytest`_
-----------------------------------

To generate XML report, add the ``--junitxml=<report-path>`` or ``--junit-xml=<report-path>`` option.

Show test function docstring in report
---------------------------------------

.. code-block:: python

   # conftest.py

   import pytest

   @pytest.hookimpl(hookwrapper=True)
   def pytest_runtest_makereport(item, call):
      outcome = yield
      report = outcome.get_result()

      test_fn = item.obj
      docstring = getattr(test_fn, '__doc__')
      if docstring:
         report.nodeid = docstring


   # test_it.py

   def test_ok():
      """This is my very important test."""
      print("ok")

This will produce output similar to:

.. code-block:: console

   $ pytest -v
   test_docstring_in_report.py::test_ok
   ..\..\..\This is my very important test. PASSED                 [100%]

`Pytest`_ built-in fixtures
----------------------------

List of `pytest`_ fixtures could be obtained by running ``pytest -q --fixtures``.

Here are some interesting built-in fixtures:

- ``capsys``
    Enable text capturing of writes to ``sys.stdout`` and ``sys.stderr``.

    Returns an instance of `CaptureFixture`_ to give access to captured ``stdout`` and ``stderr``.

    The captured output is made available via ``capsys.readouterr()`` method
    calls, which return a ``(out, err)`` namedtuple.
    ``out`` and ``err`` will be ``text`` objects.

    Example::

      def test_output(capsys):
         print("hello")
         captured = capsys.readouterr()
         assert captured.out == "hello\n"

- ``capsysbinary``
    Enable bytes capturing of writes to ``sys.stdout`` and ``sys.stderr``.

    The captured output is made available via ``capsysbinary.readouterr()``
    method calls, which return a ``(out, err)`` namedtuple.
    ``out`` and ``err`` will be ``bytes`` objects.

- ``capfd``
    Enable text capturing of writes to file descriptors ``1`` and ``2``.

    The captured output is made available via ``capfd.readouterr()`` method
    calls, which return a ``(out, err)`` namedtuple.
    ``out`` and ``err`` will be ``text`` objects.

- ``capfdbinary``
    Enable bytes capturing of writes to file descriptors ``1`` and ``2``.

    The captured output is made available via ``capfd.readouterr()`` method
    calls, which return a ``(out, err)`` namedtuple.
    ``out`` and ``err`` will be ``byte`` objects.

- ``pytestconfig`` [session scope]
  Session-scoped fixture that returns the `pytest.config.Config`_ object.

  Example::

     def test_foo(pytestconfig):
        if pytestconfig.getoption("verbose") > 0:
             ...
- ``monkeypatch``
    A convenient fixture for monkey-patching.

    The fixture provides these methods to modify objects, dictionaries or
    os.environ::

        monkeypatch.setattr(obj, name, value, raising=True)
        monkeypatch.delattr(obj, name, raising=True)
        monkeypatch.setitem(mapping, name, value)
        monkeypatch.delitem(obj, name, raising=True)
        monkeypatch.setenv(name, value, prepend=False)
        monkeypatch.delenv(name, raising=True)
        monkeypatch.syspath_prepend(path)
        monkeypatch.chdir(path)

    All modifications will be undone after the requesting test function or
    fixture has finished. The ``raising`` parameter determines if a KeyError
    or AttributeError will be raised if the set/deletion operation has no target.
- ``request``
    Special fixture of class `FixtureRequest`_ providing information of the requesting test function.
- ``tmpdir``
    Return a temporary directory path object which is unique to each test
    function invocation, created as a sub directory of the base temporary
    directory.

    The returned object is a `py.path.local`_ path object.

    .. _`py.path.local`: https://py.readthedocs.io/en/latest/path.html

- ``tmp_path``
    Return a temporary directory path object which is unique to each test
    function invocation, created as a sub directory of the base temporary
    directory.

    The returned object is a :class:`pathlib.Path` object.

    .. note::

        In python < 3.6 this is a pathlib2.Path.

`Pytest`_ plugins
-------------------

- `pytest-bdd`_ - Implements a subset of the Gherkin language to enable automating project requirements testing and to facilitate behavioral driven development.
- `pytest-cov`_ - Produces coverage reports.
- `pytest-django`_ -  Provides a set of useful tools for testing Django applications and projects.
- `pytest-randomly`_ - Randomly order tests with controlled seed.
- `pytest-reverse`_ - Execute tests in reverse order.
- `pytest-splinter`_ - Provides a set of fixtures to use `splinter`_ for browser testing with `pytest`_
- `pytest-xdist`_ - Adds test execution modes, e.g. multi-CPU and distributed.

Running `doctest`_ test cases
-----------------------------

By default `pytest`_ is looking for ``test_*.txt`` files and if such a file is found, `pytest`_ executes the `doctest`_ tests defined in this file.

`Pytest`_ can also discover and execute `doctest`_ test cases from Python modules. For example if a function has docstring which contains `doctest`_ test cases, `pytest`_ can execute the tests.

.. code-block:: python
   :name: addition-doctest-py
   :caption: addition_doctest.py

   def add(*args):
      """Add one or more numbers and return the result.

      >>> add(3, 2)
      5
      >>> add(5, 4, 3, 2, 3, 4, 5)
      26
      """
      return sum(args)

To execute test cases from modules, specify the ``--doctest-modules`` option to `pytest`_.

.. code-block:: console

   $ pytest --doctest-modules
   ============================== test session starts ==============================
   platform win32 -- Python 3.8.1, pytest-6.1.0, py-1.9.0, pluggy-0.13.1
   rootdir: C:\Sandbox\PoC\python-repl-cmd\src
   plugins: cov-2.8.1, django-4.4.0, flask-0.14.0
   collected 1 item

   addition_doctest.py .                                                      [100%]

   =============================== 1 passed in 0.04s ===============================

For further information refer to the `pytest doctest`_ integration documentation.

Running `unittest`_ test cases
-------------------------------

`Pytest`_ can discover and execute `unittest`_ test cases:

.. code-block:: python
   :name: test-addition-py
   :caption: test_addition.py

   import unittest

   def add(*args):
      return sum(args)

   class TestAddition(unittest.TestCase):
      def test_result_is_sum(self):
         result = add(3, 2)
         self.assertEqual(result, 5)

      def test_add_many(self):
         result = add(5, 4, 3, 2, 3, 4, 5)
         self.assertEqual(result, 26)

Running the tests is as easy as:

.. code-block:: console

   $ pytest
   ============================== test session starts ==============================
   platform win32 -- Python 3.8.1, pytest-6.1.0, py-1.9.0, pluggy-0.13.1
   rootdir: C:\Sandbox\PoC\python-repl-cmd\src
   plugins: cov-2.8.1, django-4.4.0, flask-0.14.0
   collected 2 items

   test_addition.py ..                                                        [100%]

   =============================== 2 passed in 0.06s ===============================

This makes it very easy to migrate from `unittest`_ to `pytest_` or to combine tests that use different frameworks.

.. _doctest: https://docs.python.org/3/library/doctest.html
.. _CaptureFixture: https://docs.pytest.org/en/6.2.x/reference.html#pytest.CaptureFixture
.. _FixtureRequest: https://docs.pytest.org/en/latest/reference.html#pytest.FixtureRequest
.. _pytest: https://docs.pytest.org/en/latest/doctest.html
.. _pytest doctest: https://docs.pytest.org/en/latest/doctest.html
.. _pytest.config.Config: https://docs.pytest.org/en/latest/reference.html#pytest.config.Config
.. _pytest-bdd: https://github.com/pytest-dev/pytest-bdd
.. _pytest-cov: https://github.com/pytest-dev/pytest-cov
.. _pytest_cov documentation: https://pytest-cov.readthedocs.io/en/latest/
.. _pytest-django: https://pytest-django.readthedocs.io/en/latest/
.. _pytest-randomly: https://github.com/pytest-dev/pytest-randomly
.. _pytest-reverse: https://github.com/adamchainz/pytest-reverse
.. _pytest-splinter: https://github.com/pytest-dev/pytest-splinter
.. _pytest-xdist: https://github.com/pytest-dev/pytest-xdist
.. _splinter: https://splinter.readthedocs.io/en/latest/
.. _unittest: https://docs.python.org/3/library/unittest.html

.. _speed up your django tests: https://adamchainz.gumroad.com/l/suydt
