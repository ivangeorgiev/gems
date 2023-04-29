Merge Local Branch
====================

Following example merges a local branch `feature/create-user`

.. code-block:: bash
   :linenos:

   $ git checkout main
   $ git pull
   $ git merge feature/create-user
   $ git push

Here is what the script is doing, line by line:

# Switch the current working branch to `main`.
# Make sure local `main` branch is in sync sith remote branch. Optional.
# Merge the `feature/create-user` branch with the current working branch (`main`)
# Push changes from the local working branch `main` to the remote branch.

See Also
---------

- `Basic Merging <https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging#_basic_merging>`__ from Gitbook
- `Git Branching Rebasing <https://git-scm.com/book/en/v2/Git-Branching-Rebasing>`__ Rebasing from Gitbook
- `Intro to rebase <https://gitready.com/intermediate/2009/01/31/intro-to-rebase.html>`__ from git ready
