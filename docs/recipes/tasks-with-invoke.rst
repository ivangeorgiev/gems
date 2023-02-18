Tasks with invoke
=======================

You need first to install the ``invoke`` package:

.. code-block:: console

   $ pip install invoke
   ..........

Let's define a simple task ``greet`` which will greet the user by name. Name is optional (`invoke_tasks_basic.py <https://gist.github.com/ivangeorgiev/574eb3198b011a107ee018326d0ff6de#file-invoke_tasks_basic-py>`__):

.. raw:: html

   <script src="https://gist.github.com/ivangeorgiev/574eb3198b011a107ee018326d0ff6de.js?file=invoke_tasks_basic.py"></script>

Place the task definitions into ``tasks.py`` module.

Tasks are plain Python functions, decorated with the ``invoke.task`` decorator. First argument to the function is always ``invoke`` context (``invoke.context.Context`` instance).

Defining the ``name`` task parameter tells ``invoke`` to define ``--name`` option and also ``-n`` shortcut option.

Let's try our tasks:

.. code-block:: console

   $ invoke greet
   Hi there!

   $ invoke greet -n Ivan
   Hello Ivan!

   $ invoke greet --name Ivan
   Hello Ivan!

``invoke`` provides also help out of the box. The docstring for the function implementing the task is used:

.. code-block:: console

   $ invoke greet --help
   Usage: inv[oke] [--core-opts] greet [--options] [other tasks here ...]

   Docstring:
   Greet user.

   Options:
   -n STRING, --name=STRING

   $ invoke greet --help
   Usage: inv[oke] [--core-opts] greet [--options] [other tasks here ...]

   Docstring:
   Greet user.

   Options:
   -n STRING, --name=STRING

To list available tasks, use the ``--list`` (``-l``) option:

.. code-block:: console

   $ invoke --list
   Available tasks:

     greet   Greet user.

To see all available options, just execute ``invoke`` or ``invoke --help``:

.. code-block:: console

   $ invoke
   Usage: inv[oke] [--core-opts] task1 [--task1-opts] ... taskN [--taskN-opts]

   Core options:

   --complete                         Print tab-completion candidates for given parse remainder.
   --hide=STRING                      Set default value of run()'s 'hide' kwarg.
   --no-dedupe                        Disable task deduplication.
   --print-completion-script=STRING   Print the tab-completion script for your preferred shell (bash|zsh|fish).
   --prompt-for-sudo-password         Prompt user at start of session for the sudo.password config value.
   --write-pyc                        Enable creation of .pyc files.
   -c STRING, --collection=STRING     Specify collection name to load.
   -d, --debug                        Enable debug output.
   -D INT, --list-depth=INT           When listing tasks, only show the first INT levels.
   -e, --echo                         Echo executed commands before running.
   -f STRING, --config=STRING         Runtime configuration file to use.
   -F STRING, --list-format=STRING    Change the display format used when listing tasks. Should be one of: flat
                                       (default), nested, json.
   -h [STRING], --help[=STRING]       Show core or per-task help and exit.
   -l [STRING], --list[=STRING]       List available tasks, optionally limited to a namespace.
   -p, --pty                          Use a pty when executing shell commands.
   -r STRING, --search-root=STRING    Change root directory used for finding task modules.
   -R, --dry                          Echo commands instead of running.
   -T INT, --command-timeout=INT      Specify a global command execution timeout, in seconds.
   -V, --version                      Show version and exit.
   -w, --warn-only                    Warn, instead of failing, when shell commands fail.

Documenting options
--------------------

To provide documentation for the task options, pass ``help`` argument to the ``@task`` decorator (`infoke_tasks_documenting.py <https://gist.github.com/ivangeorgiev/574eb3198b011a107ee018326d0ff6de#file-invoke_tasks_documenting-py>`__):

.. code-block:: python

   @invoke.task(help={
      "name": "Name of the person to greet."
   })

Running shell commands
-------------------------

To execute shell commands, use the ``run`` method of the ``ctx`` context argument:

.. code-block:: python

   import invoke
   import io

   @invoke.task
   def ls(ctx):
      ctx.run("dir")

The output of the command is passed to the standard ouptut (the terminal) of the script:

.. code-block:: console

   $ invoke ls
    Volume in drive C is OS
    Volume Serial Number is B89A-B1F9

    Directory of C:\Sandbox\PoC\python-repl-cmd\src\pacan

   12/24/2021  01:55 PM    <DIR>          .
   12/24/2021  01:55 PM    <DIR>          ..
   12/23/2021  06:54 PM             1,189 basic_shell.py
   12/24/2021  01:55 PM               372 tasks.py
   12/22/2021  09:47 PM             1,613 __init__.py
   12/22/2021  09:17 PM                52 __main__.py
   12/22/2021  09:47 PM    <DIR>          __pycache__
                  4 File(s)          3,226 bytes
                  3 Dir(s)  23,473,487,872 bytes free

Hiding shell command output
----------------------------

The default behaviour when running a shell command using the context's ``.run()`` method is to pass the standard output and standard error of the shell command to the script's ``stdout`` and ``stderr``. You can hide the standard otuput of the standard error by passing the ``hide`` parameter:

   - ``out`` or ``stdout`` hide only the standard output of the command
   - ``err`` or ``stderr`` hide only the sttandard error of the command
   - ``both`` or ``True`` hide both standard error and standard output of the command.

Capturing the shell command output
-----------------------------------

You can capture the shell command output by passing a file-like object as ``out_stream`` or ``err_stream`` arguments. ``invoke`` already captures the standard input and output of the command. You can access it as string from the result object's ``stdout`` and ``stderr`` attributes.

In the following example the ``ls`` command captures the output of Windows's ``dir`` command to extract and print only the filenames:

.. raw:: html

   <script src="https://gist.github.com/ivangeorgiev/574eb3198b011a107ee018326d0ff6de.js?file=invoke_capture.py"></script>

And the output:

.. code-block:: console

   $ invoke ls
   .
   ..
   basic_shell.py
   tasks.py
   __init__.py
   __main__.py
   __pycache__


Further information
--------------------

Invoke provides a lot more features than what we saw. Refer to the `invoke's documentation <https://docs.pyinvoke.org/en/stable/index.html>`__ for further details.
