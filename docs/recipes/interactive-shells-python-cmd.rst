Interactive shell with Python Cmd
==========================================

We are using Python's core module ``cmd``.

Basic shell
------------

Let's start with a "Hello world!" example.

Our interactive shell provides two commands:

- ``greet`` - print a greeting.
- ``bye`` - finish the interactive shell session.

.. raw:: html

   <script src="https://gist.github.com/ivangeorgiev/8cba5b37bdd83c63c31353fcc0516ac5.js?file=basic_shell.py"></script>

To create a shell, start with creating a subclass to the ``Cmd`` class from the ``cmd`` module.

.. code-block:: python

   import cmd

   class BasicShell(cmd.Cmd):
      pass

   if __name__ == "__main__":
      BasicShell().cmdloop()

This is it! We already have an interactive shell. Well, it is not providing much functionality. It has only one command: ``help`` (and ``?`` as shortcut to ``help``). To exit the shell, you need to use :kbd:`Ctrl` + :kbd:`C`.

We can run the shell:

.. code-block:: console

   $ python basic_shell.py
   (Cmd) help

   Documented commands (type help <topic>):
   ========================================
   help

   (Cmd) Traceback (most recent call last):
   File "c:\Sandbox\PoC\python-repl-cmd\src\pacan\basic_shell.py", line 31, in <module>
      BasicShell().cmdloop()
   File "C:\Users\ivang\AppData\Local\Programs\Python\Python310\lib\cmd.py", line 126, in cmdloop
      line = input(self.prompt)
   KeyboardInterrupt
   ^C

To add command, we implement a method, named as ``do_<command-name>``. For example to add a ``bye`` command that exits the shell, we need to create a ``do_bye`` method:

.. code-block:: python

   def do_bye(self, argline:str) -> bool:
      return True

Command method takes two arguments:

- ``self`` - reference to the class instance.
- ``argline`` - string containing the command arguments. This is the user input after the command. For example if user input is ``"great Ivan"``, the ``do_great`` method will receive ``Ivan`` as command argument.

Command method **return value** is evaluated to boolean to decide if the shell session should be terminated. If result evaluates to ``True``, session is terminated. Otherwise, a prompt is shown and the shell awaits next user command.

Change the prompt
------------------

The default prompt is `(cmd)`. To change it, assign corresponding value to the ``prompt`` attribute:

.. code-block:: python

   # ...
   class BasicShell(cmd.Cmd):
      prompt = "> "
      # ...

And try it:

.. code-block:: console

   $ python basic_shell.py
   > greet Ivan
   Hello, Ivan!
   > bye
   Bye!

As you can see the prompt has changed from default ``"(cmd)""`` to ``"> "``.

Welcome message
-----------------

We want when our interactive shell is started, to print the welcome message ``"Welcome to BasicShell! For help type `?` or `help`."`` (`gist <https://gist.github.com/ivangeorgiev/8cba5b37bdd83c63c31353fcc0516ac5#file-basic_shell_welcome_message-py>`__):

.. code-block::python

   class BasicShell(cmd.Cmd):
      """Interactive shell example."""
      intro = "Welcome to BasicShell! For help type `?` or `help`.\n"
      prompt = "> "

We can now start the interactive shell:

.. code-block:: console

   Welcome to BasicShell! For help type `?` or `help`.

   > eval 112*2
   224
   > bye
   Bye!

Empty command
--------------

When the user enters an empty line, the default behavior is to execute the last executed command. We want to modify this by adding a message showing the command being executed. To implement we need to override the ``emptyline()`` method (`basic_shell_repeat.py gist <https://gist.github.com/ivangeorgiev/8cba5b37bdd83c63c31353fcc0516ac5#file-basic_shell_welcome_message-py>`__):

.. code-block:: python

    def emptyline(self):
        """Re-execute the last command"""
        print(f"REPEAT: {self.lastcmd}")
        super().emptyline()

The last executed command is stored in the `lastcmd`.

Trying the above approach:

.. code-block:: console

   $ python basic_shell_repeat.py
   Welcome to BasicShell! For help type `?` or `help`.

   > eval 112*2
   224
   >
   REPEAT: eval 112*2
   224
   > bye
   Bye!


Command arguments
-------------------

Let's add a command ``eval`` which evaluates the expression given as parameter to the command (`basic_shell_eval.py gist <https://gist.github.com/ivangeorgiev/8cba5b37bdd83c63c31353fcc0516ac5?file=basic_shell_prompt-py#file-basic_shell_eval-py>`__):

.. code-block:: python

    def do_eval(self, argline):
        try:
            print(eval(argline))
        except Exception as error:
            print(f"ERROR EVALUATING {argline}: {error}")

and try it:

.. code-block:: console

   $ python basic_shell_prompt.py
   > eval 3+2
   5
   > eval 2**3
   8
   > bye
   Bye!

Running shell command
----------------------

The special command ``!`` is a shortcut to the ``shell``. Let's implement a ``shell`` command (`basic_shell_shell.py <https://gist.github.com/ivangeorgiev/8cba5b37bdd83c63c31353fcc0516ac5#file-basic_shell_welcome_message-py>`__):

.. code-block:: python

   def do_shell(self, argline):
      """Execute a shell command and print the output."""
      output = os.popen(argline).read()
      print(output)


Let's try it:

.. code-block:: console

   $ python basic_shell_shell.py
   Welcome to BasicShell! For help type `?` or `help`.

   > !dir
   Volume in drive C is OS
   Volume Serial Number is B89A-B1F9

   Directory of C:\Sandbox\PoC\python-repl-cmd

   12/22/2021  09:15 PM    <DIR>          .
   12/22/2021  09:15 PM    <DIR>          ..
   12/22/2021  09:14 PM               280 .dccache
   12/22/2021  09:15 PM    <DIR>          src
                  1 File(s)            280 bytes
                  3 Dir(s)  23,383,117,824 bytes free

   > bye
   Bye!

Exit the shell on EOF character
--------------------------------

By default the interative shell is not processing the ``EOF`` character. To process it, implement the ``EOF`` command (`basic_shell_eof.py <https://gist.github.com/ivangeorgiev/8cba5b37bdd83c63c31353fcc0516ac5#file-basic_shell_eof-py>`__):

.. code-block:: python

    def do_EOF(self, argline):
        """Exit the shell."""
        return self.do_bye(argline)

There is more
--------------

The ``cmd.Cmd`` class provides other customization options like pre- and post- command hooks, pre- and post- command loop hooks, help customization etc. You can find more information in the module `documentation <https://docs.python.org/3.10/library/cmd.html>`__.

Summary
--------

Let's summarize what we've just learned:

1. To create interactive shell, subclass the ``Cmd`` class from core ``cmd`` module.
2. To add a command to the shell, create a ``do_<command-name>`` method to the shell class.
3. To exit the shell session, the command method should return ``False``.
4. The command method's docstring is used as help text by the shell.
5. To change the shell prompt, assign new value to the ``prompt`` attribute of the shell object.
6. To add welcome message, assign value to the ``intro`` attribute.
7. By default empty command (line) re-executes the last non-empty command. To change this, override the ``emptyline()`` method.
8. Commad method receives the user input as a second parameter.
9. To enable shell commands, implement a ``shell`` command (``do_shell()`` method). ``!`` is a shortcut for the ``shell`` command.
10. To process the EOF character, implement the ``EOF`` command (``do_EOF() method``).
