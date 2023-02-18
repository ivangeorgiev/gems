==========================
Documentation with Sphinx
==========================

Start a Sphinx project
=======================

1. Create virtual environment
2. Install Sphinx
3. Setup documentation project
4. Build documentation

1. Create virtual environment
-------------------------------

This step is optional. You can use Python installed on your system directly.
However it is good practice to keep your project isolated from other projects.
This could be achieved with Python virtual environment.

.. code-block:: console

    $ py -3.10 -m venv .venv310

Above command will create a directory ``.venv310`` with local "copy" of
Python 3.10 - a virtual environment. To use the virtual environment you need to
activate it.

To activate Python virtual environment in bash:

.. code-block:: console

    $ source .venv310/Scripts/activate
    (.venv310)
    $

To activate Python virtual environment in PowerShell:

.. code-block:: console

    PS> .\.venv310\Scripts\Activate.ps1
    (.venv310) PS>

To activate Python virtual environment in Windows Command Prompt:

.. code-block:: bat

    C:\myproj> .venv310\Scripts\activate.bat
    (.venv310) C:\myproj>

Virtual environment is active only for the console session it has been activated for.
All packages you install are installed into the virtual environment and do not
have any impact on the global Python environment.

2. Install Sphinx
--------------------

You can use ``pip`` to install ``sphinx`` package directly. I personally prefer
to use ``requirements.txt`` file:

.. code-block:: ini

    # FILE: -- requirements.txt
    sphinx
    sphinx-rtd-theme

Than run ``pip`` to install required packages:

.. code-block:: console

    $ pip install --upgrade -r requirements.txt
    ...


3. Setup Sphinx project
---------------------------

Document sources need to be stored in a directory. Common approach is
to use ``docs`` directory under the project root to keep the documentation sources
and artifacts. To initialize the directory as Sphinx project, the
``sphinx-quickstart`` is used:

.. code-block:: console

    $ mkdir docs
    $ cd docs
    $ sphinx-quickstart

Modify the ``index.rst`` file created by ``sphinx-quickstart`` - delete last section:

.. code-block:: rst

    Indices and tables
    ==================

    * :ref:`genindex`
    * :ref:`modindex`
    * :ref:`search`

Optionally update the ``conf.py`` file to change the default theme:

Replace

.. code-block:: python

    html_theme = 'alabaster'

with

.. code-block:: python

    html_theme = 'sphinx_rtd_theme'

    RTD_NEW_THEME = True

    html_theme_options = {
        'display_version': False,
    }

    html_show_sphinx = False

If you want to experiment with other themes, you can look at:

- `Sphinx Theme Gallery <https://sphinx-themes.org/>`_.
- `Sphinx Tehemes <https://www.writethedocs.org/guide/tools/sphinx-themes/>`_ from Write the docs
- `<https://sphinxthemes.com/>`_

4. Build documentation
-------------------------

To build the documentation from the ``docs`` directory you execute the ``make`` script.
``make`` script supports various output formats. To build documentation in HTML format:

.. code-block:: console

    $ make html
    Running Sphinx v4.3.1
    loading pickled environment... done
    ...................................
    dumping object inventory... done
    build succeeded.

    The HTML pages are in _build\html.

You can build other formats, e.g.

- ``epub``
- ``latex``
- ``text``
- ``gettext``
- ``singlehtml``
- ``dirhtml``

For more information on Sphinx build refer to the `documentation <https://www.sphinx-doc.org/en/master/man/sphinx-build.html>`_.

Hosting on Read the Docs
===========================

Add build requirements
--------------------------

If you need to install additional build-time dependencies, e.g. for a custom theme, you
can create a ``.readthedocs.yaml`` file and place it at the root of your project:

.. code-block:: yaml

    version: 2

    python:
      install:
        - requirements: requirements.txt

If necessary, you coul have more than one ``requirements.txt`` file and specify Python version to be used:

.. code-block:: yaml

    version: 2

    python:
      version: "3.7"
      install:
        - requirements: docs/requirements.txt
        - requirements: requirements.txt

For more information refer to `Configuration File V2 <https://docs.readthedocs.io/en/stable/config-file/v2.html>`_
documentation.


Further reading
=====================

- `typo3 rest cheatsheet`_
- Write the Docs's list of `Tools for documentation writing`_
- `Box drawing characters <https://en.wikipedia.org/wiki/Box-drawing_character>`__
- `Unicode Character Code Charts <https://unicode.org/charts/>`__
- `reStructuredText Primer <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`__ at Sphinx

.. _typo3 rest cheatsheet: https://docs.typo3.org/m/typo3/docs-how-to-document/main/en-us/WritingReST/CheatSheet.html
.. _Tools for documentation writing: https://www.writethedocs.org/guide/tools/
