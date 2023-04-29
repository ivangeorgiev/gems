Change the Remote Git Repository URL
=====================================

Problem
------------

You have local clone of a remote git repository, but the url of the repository has changed.
How to point the local repository to the new remote url?

Solution
---------------

Use the `git remote set-url` command to change the url of the remote repository.

.. code-block:: bash

   $ git remote set-url origin <new-remote-repository-url>

- `origin` is the name of the remote.
- `<new-remote-repository-url>` is the new url of the remote repository, e.g. `https://github.com/ivangeorgiev/gems`
