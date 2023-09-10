Debug Django Project with Visual Studio Code (VSCode)
##############################################################

.. post:: 2023-09-09 13:30:00
   :tags: django,debugging,vscode
   :category: django
   :author: ivan
   :language: en

   In order to debug Django project, we need to first create a Visual Studio Code (VSCode) run
   configuration.


Method 1: Create Run Configuration
************************************

# From the VSCode menu select :menuselection:`Run --> Add Configuration...`
# Select `Python` as debugger
# Select `Django` as Debug configuration
# Configure the path to your project's `manage.py`, e.g. `${workspaceFolder}\elearn\manage.py`

VS Code creates a new Run Configuration for your Django project and opens the `lanuch.json` file.
You can close it.


Method 2: Create `launch.json` File
*************************************

In the `.vscode` directory create or update `launch.json` to include run configuration for your Django app:

.. code-block:: json
   :linenos:
   :caption: .vscode/launch.json

   {
      // Use IntelliSense to learn about possible attributes.
      // Hover to view descriptions of existing attributes.
      // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
      "version": "0.2.0",
      "configurations": [
         {
               "name": "Python: Django",
               "type": "python",
               "request": "launch",
               "program": "${workspaceFolder}\\elearn\\manage.py",
               "args": [
                  "runserver"
               ],
               "django": true,
               "justMyCode": true
         }
      ]
   }

Running Django Development Server in Debug Mode
***************************************************

Open the `Run and Debug` sidebar (:kbd:`Ctrl-Shift-d`). Press the green arrow button to start debugging (or press :kbd:`F5`).

Happy debugging!


.. list-table:: Debug Shortcuts
   :header-rows: 1

   * - Shortcut
     - Action
   * - :kbd:`F6`
     - Pause
   * - :kbd:`F5`
     - Start/Continue
   * - :kbd:`F9`
     - Toggle Breakpoint
   * - :kbd:`F10`
     - Step Over
   * - :kbd:`F11`
     - Step Into
   * - :kbd:`Shift-F11`
     - Step Out
   * - :kbd:`Ctrl-Shift-F5`
     - Restart
   * - :kbd:`Shift-F5`
     - Stop
