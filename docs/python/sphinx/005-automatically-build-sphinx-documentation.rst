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


nodemon package from npm
----------------------------

See the `nodemon npm package <https://www.npmjs.com/package/nodemon>`__.

.. code-block:: bash

   $ npm install -g nodemon
   $ nodemon -e rst,md -w docs -x "docs/make html"

Meta
-----

- Created on: 2023-03-29
