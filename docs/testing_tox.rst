Using Tox
==========

Getting started with Tox
--------------------------

We are using the sample project from the `Crafting Test Drieven Software with Python <https://github.com/PacktPublishing/Crafting-Test-Driven-Software-with-Python/tree/main/Chapter09>`__ book.

Step 1. Install tox
~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

   $ pip install tox
   .............

Step 2: Create tox.ini
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create ``tox.ini`` file at the project root directory.

.. code-block:: ini

   # FILE: tox.ini
   [tox]
   setupdir = ./src

   [testenv]
   deps =
      flaky == 3.7.0
      pytest
      pytest-bdd == 3.4.0
      pytest-cov
      pytest-benchmark == 3.2.3
   commands =
      pytest --cov=contacts {posargs}

1. The ``setupdir`` option instructs `tox`_ which directory to use to build and install the package from. This is the directory where ``setup.py`` or ``pyproject.toml`` is located. Current directory is used as default.
2. The ``testenv`` section defines default settings for `tox`_ environment.
3. The ``deps`` option instructs `tox`_ to install listed dependencies to the environment. In our example, `tox`_ will install ``flaky``, ``pytest``, ``pytest-bdd`` version 3.4.0, ``pytest-cov`` and ``pytest-benchmark``.
4. The ``commands`` option instructs `tox_` which commands to execute after the environment is created, acitvated and the project package is installed into it. By default no commands are executed.
5. ``{posargs}`` tells `tox`_ to include the command line argiments found after the ``--`` command line, e.g. ``tox -- m load`` will execute only test cases makred as ``load``.

Step 3: Run tox
~~~~~~~~~~~~~~~~

.. code-block:: console
   :linenos:

   $ tox
   GLOB sdist-make: C:\Sandbox\projects\statuspage\tox\practice\src\setup.py
   python recreate: C:\Sandbox\projects\statuspage\tox\practice\.tox\python
   python installdeps: flaky == 3.7.0, pytest, pytest-bdd == 3.4.0, pytest-cov, pytest-benchmark
   python inst: C:\Sandbox\projects\statuspage\tox\practice\.tox\.tmp\package\1\contacts-0.0.0.zip
   python installed: atomicwrites==1.4.0,attrs==21.2.0,colorama==0.4.4,contacts @ file:///C:/Sandbox/projects/statuspage/tox/practice/.tox/.tmp/package/1/contacts-0.0.0.zip,coverage==6.2,flaky==3.7.0,glob2==0.7,iniconfig==1.1.1,Mako==1.1.6,MarkupSafe==2.0.1,packaging==21.3,parse==1.19.0,parse-type==0.5.2,pluggy==1.0.0,py==1.11.0,py-cpuinfo==8.0.0,pyparsing==3.0.6,pytest==6.2.5,pytest-bdd==3.4.0,pytest-benchmark==3.4.1,pytest-cov==3.0.0,six==1.16.0,toml==0.10.2,tomli==2.0.0
   python run-test-pre: PYTHONHASHSEED='176'
   python run-test: commands[0] | pytest --cov=contacts
   ================================ test session starts =================================
   platform win32 -- Python 3.10.0, pytest-6.2.5, py-1.11.0, pluggy-1.0.0
   cachedir: .tox\python\.pytest_cache
   benchmark: 3.4.1 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
   rootdir: C:\Sandbox\projects\statuspage\tox\practice
   plugins: flaky-3.7.0, bdd-3.4.0, benchmark-3.4.1, cov-3.0.0
   collected 26 items

   tests\acceptance\test_delete_contact.py .                                       [  3%]
   tests\acceptance\test_list_contacts.py ..                                       [ 11%]
   benchmarks\test_persistence.py .                                                [ 15%]
   tests\acceptance\test_adding.py ..                                              [ 23%]
   tests\functional\test_basic.py ...                                              [ 34%]
   tests\functional\test_main.py .                                                 [ 38%]
   tests\unit\test_adding.py ......                                                [ 61%]
   tests\unit\test_application.py .......                                          [ 88%]
   tests\unit\test_flaky.py .                                                      [ 92%]
   tests\unit\test_persistence.py ..                                               [100%]

   ---------- coverage: platform win32, python 3.10.0-final-0 -----------
   Name                                                 Stmts   Miss  Cover
   ------------------------------------------------------------------------
   .tox\python\Lib\site-packages\contacts\__init__.py      51      0   100%
   .tox\python\Lib\site-packages\contacts\__main__.py       0      0   100%
   ------------------------------------------------------------------------
   TOTAL                                                   51      0   100%



   ----------------------------------------------------- benchmark: 1 tests ----------------------------------------------------
   Name (time in us)          Min         Max      Mean    StdDev    Median      IQR  Outliers  OPS (Kops/s)  Rounds  Iterations
   -----------------------------------------------------------------------------------------------------------------------------
   test_loading          335.3000  9,861.9000  449.3980  604.9698  385.9000  75.8000
   1;19        2.2252     249           1
   -----------------------------------------------------------------------------------------------------------------------------

   Legend:
   Outliers: 1 Standard Deviation from Mean; 1.5 IQR (InterQuartile Range) from 1st Quartile and 3rd Quartile.
   OPS: Operations Per Second, computed as 1 / Mean
   ===Flaky Test Report===

   test_appender passed 1 out of the required 1 times. Success!

   ===End Flaky Test Report===
   ================================= 26 passed in 1.66s =================================
   ______________________________________ summary _______________________________________
   python: commands succeeded
   congratulations :)

1. Line #2 - `tox`_ is building the project package.
2. Line #3 - `tox`_ creates Python virtual enviornment.
3. Line #4 - `tox`_ installs depenencies, listed in ``tox.ini``.
4. Line #8 - `tox`_ runs commands, isted in ``tox.ini``.
5. Lines #9 - #53 are output from the command execution
6. Lines from line #54 are summary report from `tox`_ execution.


Manage multiple environments
-----------------------------

.. code-block:: ini
   :emphasize-lines: 4, 14-

   # FILE: tox.ini
   [tox]
   setupdir = ./src
   envlist = py39, py310

   [testenv]
   deps =
       pytest
       pytest-bdd == 3.4.0
       pytest-cov == 2.10.1
   commands =
       pytest --cov=contacts --benchmark-skip {posargs}

   [testenv:py36]
   deps =
       pytest == 4.6.11
       pytest-bdd == 3.4.0
       pytest-cov == 2.10.1
       flaky == 3.7.0
       pytest-benchmark == 3.2.3
       pytest-cov == 2.10.1
   commands =
       pytest --cov=contacts --benchmark-skip {posargs}

1. The ``envlist`` option tells `tox`_ which environments to build and execute.
2. The ``testenv`` section defines default environment settings.
3. The ``testenv:py36`` section defines settings for the Python 3.6 environment.


Using Travis with Tox
----------------------

.. code-block:: ini
   :emphasize-lines: 6

   # FILE: tox.ini
   [tox]
   setupdir = ./src

   [testenv]
   usedevelop = true
   deps =
      flaky == 3.7.0
      pytest
      pytest-bdd == 3.4.0
      pytest-cov
      pytest-benchmark == 3.2.3
   commands =
      pytest --cov=contacts {posargs}

1. Add the ``usedevelop`` option to instruct `tox`_ to not build and isntall source distribution, but to use develop setup instead (``-e`` option of pip).

Modify `travis.yml`:

.. code-block:: yaml

   script:
      - "tox"

   install:
      - "pip install travis-tox"


Further reading
---------------

- `Tox documentation`_

.. _tox: https://tox.wiki/en/stable/
.. _tox documentation: tox_
