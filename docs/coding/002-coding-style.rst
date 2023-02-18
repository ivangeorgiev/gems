===============
Coding Style
===============


Pre-commit
===============

Getting started
----------------

To get started with ``pre-commit``, follow these steps:

1. **Install pre-commit.** To do so, follow `the pre-commit installation instructions <https://pre-commit.com/#install>`_.

    .. code-block:: console

        $ pip install pre-commit

    Create a ``.pre-commit-config.yaml`` configuration file. To get started use sample config:

    .. code-block:: console

        $ pre-commit sample-config > .pre-commit-config.yaml

    Here is another ``.pre-commit-config.yaml`` to start with. Based on Django ``.pre-commit-conifg.yaml``.

    .. code-block:: yaml

        # See https://pre-commit.com for more information
        # See https://pre-commit.com/hooks.html for more hooks
        repos:
        - repo: https://github.com/pre-commit/pre-commit-hooks
        rev: v3.2.0
        hooks:
            - id: trailing-whitespace
            - id: end-of-file-fixer
            - id: check-yaml
            - id: check-added-large-files
        - repo: https://github.com/PyCQA/isort
        rev: 5.9.3
        hooks:
            - id: isort
        - repo: https://github.com/PyCQA/flake8
        rev: 4.0.1
        hooks:
            - id: flake8
              additional_dependencies: ['flake8-quotes', 'flake8-todos', 'flake8-docstrings']
              # args:
              #   - --show-source  # Instruct flake8 to show sorce along with error. Specify in setup.cfg
        - repo: https://github.com/pre-commit/mirrors-eslint
        rev: v7.32.0
        hooks:
            - id: eslint


2. Install the git hook scripts

    * run ``pre-commit install`` to setup the git hook script:

      .. code-block:: console

          $ pre-commit install
            pre-commit installed at .git\hooks\pre-commit

      Now ``pre-commit`` will run automatically on ``git commit``.

3. (Optional) Run pre-commit against all files:

   .. code-block:: console

       $ pre-commit run --all-files
       Trim Trailing Whitespace.......................................Passed
       Fix End of Files...............................................Passed
       Check Yaml.....................................................Passed
       Check for added large files....................................Passed
       Trim Trailing Whitespace.......................................Passed
       Fix End of Files...............................................Passed
       Check Yaml.....................................................Passed
       Check for added large files....................................Passed

   If you do not specify the ``--all-files`` option, ``pre-commit`` will run only against staged files.

Tips and tricks
----------------

Execute pytest with each commit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can use local repository to define in-place hook.

.. code-block:: yaml

   # FILE: .pre-commit-config.yaml
   repos:
      - repo: local
        hooks:
          - id: pytest
            name: execute pytest
            language: python
            entry: pytest
            pass_filenames: false
            stages: [commit]
            additional_dependencies: ['pytest']


Validate commit message
~~~~~~~~~~~~~~~~~~~~~~~~

To make this work, you also need to install ``pre-commit`` as ``commit-msg`` hook.

.. code-block:: console

   $ pre-commit install -t commit-msg
   pre-commit installed at .git\hooks\commit-msg

You can use local repository and ``pygrep`` language to validate commit message against regular expression.

Following hook will fail commit if message doesn't comply to Executable Book's project `commit message rules <https://executablebooks.org/en/latest/contributing.html#commit-messages>`_. The emoji part is skipped.

.. code-block:: yaml

   # FILE: .pre-commit-config.yaml
   repos:
      - repo: local
        hooks:
          - id: commit-message
            name: check for commit message
            language: pygrep
            entry: '\A(BREAKING|NEW|IMPROVE|FIX|DOCS|MAINTAIN|TEST|RELEASE|UPGRADE|REFACTOR|DEPRECATE|MERGE|OTHER): .{1,72}(\n|\Z)'
            args: [--negate, --multiline]
            stages: [commit-msg]


Editorconfig
===============

`EditorConfig <https://editorconfig.org/>`_ project consists of a file format for defining coding styles and a collection of text editor plugins that enable editors to read the file format and adhere to defined styles. EditorConfig files are easily readable and they work nicely with version control systems.

Here is sample ``.editorconfig`` file, based on Django's ``.editorconfig``, to start with.

.. code-block:: ini

    # https://editorconfig.org/

    root = true

    [*]
    indent_style = space
    indent_size = 4
    insert_final_newline = true
    trim_trailing_whitespace = true
    end_of_line = lf
    charset = utf-8

    # Docstrings and comments use max_line_length = 79
    [*.py]
    max_line_length = 119

    # Use 2 spaces for the HTML files
    [*.html]
    indent_size = 2

    # The JSON files contain newlines inconsistently
    [*.json]
    indent_size = 2
    insert_final_newline = ignore

    [**/admin/js/vendor/**]
    indent_style = ignore
    indent_size = ignore

    # Minified JavaScript files shouldn't be changed
    [**.min.js]
    indent_style = ignore
    insert_final_newline = ignore

    # Makefiles always use tabs for indentation
    [Makefile]
    indent_style = tab

    # Batch files use tabs for indentation
    [*.bat]
    indent_style = tab

    [docs/**.txt]
    max_line_length = 79

    [*.yml]
    indent_size = 2

    [*.rst]
    indent_size = 3


Plugins (see `EditorConfig plugins download <https://editorconfig.org/#download>`_ for full list):

- `EditorConfig for VS Code <https://marketplace.visualstudio.com/items?itemName=EditorConfig.EditorConfig>`_


Flake8
===============

Flake8 combines pyflakes_ and pep8_ (pep8_ was renamed and is now pycodestyle_ to avoid confusion) into a single command.

Add ``Flake8`` config into your ``tox.ini`` or ``setup.cfg``:

.. code-block:: ini

    [flake8]
    exclude = build,.git,.tox,./tests/.env,**/migrations/*
    ignore = W504,W601
    max-line-length = 119
    show-source = true
    inline-quotes = single
    docstring-quotes = double

`In-line ignoring errors <https://flake8.pycqa.org/en/latest/user/violations.html#in-line-ignoring-errors>`_:

.. code-block:: python

    example = lambda: 'example'  # noqa: E731,E123

Further Flake8_ reading:

- `Flake8 documentation`_
- `Flake8 rules`_


.. _Flake8: https://flake8.pycqa.org/en/latest/index.html
.. _Flake8 documentation: Flake8_
.. _Flake8 rules: https://www.flake8rules.com/
.. _pep8: https://pep8.readthedocs.io/
.. _pycodestyle: https://pycodestyle.pycqa.org/
.. _pycodestyle source: https://github.com/PyCQA/pycodestyle
.. _pyflakes: https://pypi.org/project/pyflakes/

Document autoformat
====================

Frequently used Python document autoformatters are:

- ``autopep8`` - autopep8_
- ``black`` - black_
- ``yapf`` - `Yet another Python formatter`_

VS Code Python autoformatting
-------------------------------

Python extension for VS Code comes with autoformatting feature. You can format active document:

- Keyboard shortcut :kbd:`Alt` + :kbd:`Shift` + :kbd:`F`
- Command palette: :kbd:`Ctrl` + :kbd:`Shift` + :kbd:`P` > ``>Format document``

To select or change the formatting tool used:

1. Open settings using either method:

   - File > Preferences > Settings
   - Command palette :kbd:`Ctrl` + :kbd:`Shift` + :kbd:`P` > ``>Preferences: Open Settings``
   - :kbd:`Ctrl` + :kbd:`,`

2. Navigate to ``Extensions`` > ``Python``
3. Scroll to the *Formatting:* **Provider**
4. Select the formatter to be used, e.g. ``yapf``

There are also provider-specific settings which could be used to customize the formatting behavior.

.. _autopep8: https://pypi.org/project/autopep8/
.. _black: https://black.readthedocs.io/en/stable/
.. _Yet another Python formatter: yapf_
.. _yapf: https://github.com/google/yapf


Further reading
=================

- `Django coding style <https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/>`_
- `Executable book Coding Style <https://executablebooks.org/en/latest/contributing.html#coding-style>`_
- `Linters and formatters <https://books.agiliq.com/projects/essential-python-tools/en/latest/linters.html>`_
