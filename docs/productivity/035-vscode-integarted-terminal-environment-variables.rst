Environment Variables in VSCode Integrated Terminal
=========================================================



#. Open Settings (`Ctrl`+`,`)
#. Find `@id:terminal.integrated.env.windows`
#. Select which config you would like to change - User's or Worspace (recommended)
#. For the setting `Terminal › Integrated › Env: Windows`, click the `Edit settings.json` link
#. Define your environment variables here:

   .. code-block:: json

      {
         ".....": "....",
         "terminal.integrated.env.windows": {
            "ME": "IVAN"
         }
      }

