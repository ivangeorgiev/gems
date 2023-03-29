Auomatically Build Sphinx Documentation on Save
=====================================================

Solutions presented here are applicable not for Sphinx documentation authoring,
but in any scenario where you need to execute some command based on changes
you make to files.

Visual Studio Code (VSCode) with File Watcher Extension
--------------------------------------------------------

This solution is for those of us who use Visual Studio Code to as authoring tool.

#. Install the `File Watcher <https://marketplace.visualstudio.com/items?itemName=appulate.filewatcher>`__
   extension for VSCode

#. Update your `.vscode/settings.json`

   .. code-block:: json
      :caption: .vscode/settings.json

      {
         "filewatcher.commands": [
            {
            "match": "docs[/\\\\].*\\.(rst|md)$",
            "isAsync": false,
            "cmd": "${workspaceRoot}\\.venv\\Scripts\\activate.bat & cd ${workspaceRoot}\\docs & make html",
            "event": "onFileChange"
            }
         ]
      }


Python watchdog package
-----------------------------

Install the `watchdog` package:

.. code-block:: bash

   $ pip install watchdog
   $ watchmedo shell-command --patterns "*.rst" --ignore-directories --recursive --command="echo UPDATE: ${watch_src_path} & docs\\make html" --wait --drop --timeout 1

* **watchmedo**: This is the command that launches the `watchdog` package and provides a set of sub-commands that allow you to monitor files for changes.
* **shell-command**: This is the `watchmedo` sub-command that tells the package to execute a shell command when a file change is detected.
* **--patterns "*.rst"**: This option tells `watchdog` to monitor all files in the current directory and its subdirectories that have the .rst file extension. You can modify this pattern to match the specific file types you want to monitor.
* **--ignore-directories**: This option teslls `watchdog` to ignore any directories that match the file pattern. Without this option, `watchdog` would monitor both files and directories that match the pattern.
* **--recursive**: This option tells `watchdog` to monitor the directory and its subdirectories recursively. Without this option, `watchdog` would only monitor the top-level directory.
* **--command="echo ${watch_src_path} & docs\\make html"**: This option specifies the shell command that will be executed when a file change is detected. In this case,  `echo ${watch_src_path}` will
  print the path of the updated file to the console, and the command `docs\make html` will build HTML documentation from files in a `docs` directory.
* **--wait**: This option tells `watchdog` to wait for the current shell command to complete before executing it again. Without this option, watchdog would execute the command repeatedly, which may cause issues if the command takes a long time to complete.
* **--drop**: This option tells `watchdog` to drop events that occur while the current shell command is running. Without this option, `watchdog` would queue events that occur while the command is running and execute them all when the command completes.


See the package documentation at https://python-watchdog.readthedocs.io/en/stable/quickstart.html.

You might also want to check the help for the `shell-command` command.

.. code-block:: bash

   $ whatchmedo shell-command --help
   usage: watchmedo.exe shell-command [-h] [-q | -v] [-c COMMAND] [-p PATTERNS] [-i IGNORE_PATTERNS] [-D]
                                    [-R] [--interval TIMEOUT] [-w] [-W] [--debug-force-polling]
                                    [directories ...]

   Command to execute shell commands in response to file system events.

   positional arguments:
   directories
         Directories to watch.


   options:
   -h, --help
         show this help message and exit

   -q, --quiet
   -v, --verbose
   -c COMMAND, --command COMMAND
         Shell command executed in response to matching events.
         These interpolation variables are available to your command string:

            ${watch_src_path}   - event source path
            ${watch_dest_path}  - event destination path (for moved events)
            ${watch_event_type} - event type
            ${watch_object}     - 'file' or 'directory'

         Note:
            Please ensure you do not use double quotes (") to quote
            your command string. That will force your shell to
            interpolate before the command is processed by this
            command.

         Example:

            --command='echo "${watch_src_path}"'

   -p PATTERNS, --pattern PATTERNS, --patterns PATTERNS
         Matches event paths with these patterns (separated by ;).

   -i IGNORE_PATTERNS, --ignore-pattern IGNORE_PATTERNS, --ignore-patterns IGNORE_PATTERNS
         Ignores event paths with these patterns (separated by ;).

   -D, --ignore-directories
         Ignores events for directories.

   -R, --recursive
         Monitors the directories recursively.

   --interval TIMEOUT, --timeout TIMEOUT
         Use this as the polling interval/blocking timeout.

   -w, --wait
         Wait for process to finish to avoid multiple simultaneous instances.

   -W, --drop
         Ignore events that occur while command is still being executed to avoid multiple simultaneous instances.

   --debug-force-polling
         [debug] Forces polling.



nodemon package from npm
----------------------------

See the `nodemon npm package <https://www.npmjs.com/package/nodemon>`__.

.. code-block:: bash

   $ npm install -g nodemon
   $ nodemon -e rst,md -w docs -x "docs/make html"

Meta
-----

- Created on: 2023-03-29
