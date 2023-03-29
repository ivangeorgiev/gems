Dockerized Testing with Pytest
================================

This setup is based on the *Unit Testing in Python* Linkedin course.

Docker configuration
----------------------

.. code-block:: docker
   :caption: Dockerfile

   FROM python:3.7.6-buster

   RUN mkdir /pytest_project/
   COPY ./test-requirements.txt /pytest_project/
   COPY ./setup.py ./setup.py

   RUN pip install --upgrade pip
   RUN pip install -e .
   RUN pip3 install -r /pytest_project/test-requirements.txt

   WORKDIR /pytest_project/

   CMD "pytest"
   ENV PYTHONDONTWRITEBYTECODE=true

.. code-block:: yaml
   :caption: docker-compose.yaml

   version: '3.1'
   services:
   test:
      build: .
      volumes:
         - .:/pytest_project
      stdin_open: true
      tty: true


Python configuration
----------------------------

.. code-block:: python
   :caption: setup.py

   from setuptools import setup, find_packages
   import os

   long_description = '''
   This project is an example of a pytest
   project featuring assertions,
   exceptions, parametrization,
   fixtures and factory fixtures.
   '''

   version = "1.0.0"

   requirements = [
   ]

   if __name__ == '__main__':
      setup(
         name='python_unit_testing_in_docker',
         version=version,
         description='Pytest Configuration Example',
         long_description=long_description,
         author="jomeke",
         packages=find_packages(
               exclude=[
                  'tests',
               ],
               include=[
                  'scripts',
                  'utils'
               ],
         ),
         license='MIT',
         install_requires=requirements,
         classifiers=[
            'Development Status :: 1 - Planning',
            'Framework :: Pytest',
            'Intended Audience :: Developers',
            'Intended Audience :: Education',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Topic :: Software Development',
            'Topic :: Software Development :: Libraries',
            'Topic :: Software Development :: Libraries :: Python Modules'
         ],
      )


.. code-block:: cfg
   :caption: setup.cfg

   [metadata]
   description-file = README.md


.. code-block:: ini
   :caption: pytest.ini

   [pytest]
   python_paths = scripts
   testpaths = tests
   addopts = --pep8 --flakes --verbose --durations=10 --color=yes
      --cov=scripts
   pep8maxlinelength=100
   markers =
      pep8: pep8 style check
      flakes: pyflakes style check


.. code-block::
   :caption: test-requirements.txt

   coverage==4.5.2
   pytest==5.2.0
   pytest-cov==2.6.1
   pytest-flakes==2.0.0
   pytest-pep8
   pytest-pythonpath
   docker

Usage
-------

**Build docker image**

.. code-block:: bash

   $ docker-compose build

**Run test container**

This will run the container and open a bash shell inside the container.

.. code-block:: bash

   $ docker-compose run test sh

**Inside container**

*Run entire test suite*

.. code-block:: bash

   $ pytest

*Run tests from files that match a keyword*

.. code-block:: bash

   $ pytest -k <keyword-to-match-filename>

*Run tests while printing all variables and verbose output*

.. code-block:: bash

   $ pytest -vvl

*Exit the shell and the test container*

.. code-block:: bash

   $ exit

Discussion
------------

Pytest settings could be moved from `pytest.ini` to `setup.cfg`. See `Pytest Configuration <https://docs.pytest.org/en/7.1.x/reference/customize.html#setup-cfg>`_.

.. code-block:: cfg
   :caption: setup.cfg

   [tool:pytest]
   python_paths = scripts
   testpaths = tests
   addopts = --pep8 --flakes --verbose --durations=10 --color=yes
      --cov=scripts
   pep8maxlinelength=100
   markers =
      pep8: pep8 style check
      flakes: pyflakes style check


See Also
---------

* `pytest-cov` package `documentation <https://pytest-cov.readthedocs.io/en/latest/>`__
* `pytest-flakes` on `pypi <https://pypi.org/project/pytest-flakes/>`__
* `pytest-pep8` package on `pypi <https://pypi.org/project/pytest-pep8/>`__
* `pytest-pythonpath` package on `pypi <https://pypi.org/project/pytest-pythonpath/>`__
   * `pytest import mechanisms <https://docs.pytest.org/en/7.1.x/explanation/pythonpath.html>`__
* `docker` package on `pypi <https://pypi.org/project/docker/>`__ or `documentation <https://docker-py.readthedocs.io/en/stable/>`__

Meta
-----

- Created on: 2023-03-29
