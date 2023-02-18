Git Commit Messages
====================

Git Template
-------------------------------

See `Customizing Git configuration <https://git-scm.com/book/en/v2/Customizing-Git-Git-Configuration>`__.

.. code-block:: none

   Subject line (try to keep under 50 characters)

   Multi-line description of commit,
   feel free to be detailed.

   [Ticket: X]

Conventional Commit Message
---------------------------

Conventional commit message follows the structure:

.. code-block:: none

   [subject line]

   [optional body]

   [optional footer(s)]

Subject Line
~~~~~~~~~~~~~

Subject line gives a short summary (72 characters or less), describing the commit. Follows convention, e.g. Semantic Commit Messages (see below).

As `Angular <https://github.com/angular/angular/blob/master/CONTRIBUTING.md#commit>`__ suggests: “It should be present tense. Not capitalized. No period in the end.”, and **imperative like the type**.

As Chris Beams mentions in his `article about commit messages <https://cbea.ms/git-commit/>`__, the summary should always be able to complete the following sentence:

**If applied, this commit will…** add authorization for document access.

Body
~~~~~

Gives details on the change. Should be an imperative sentence explaining why we're changing the code, compared to what it was before.

Format is multiline with line length 72 characters or less.

Footer
~~~~~~~

The footer can contain information about breaking changes and deprecations and is also the place to reference GitHub issues, Jira tickets, and other PRs that this commit closes or is related to. For example:

.. code-block:: none

   BREAKING CHANGE: <breaking change summary>
   <BLANK LINE>
   <breaking change description + migration instructions>
   <BLANK LINE>
   <BLANK LINE>
   Fixes #<issue number>

or

.. code-block:: none

   DEPRECATED: <what is deprecated>
   <BLANK LINE>
   <deprecation description + recommended update path>
   <BLANK LINE>
   <BLANK LINE>
   Closes #<pr number>

To link commit (PR) to an issue, use a `keyword <https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue#linking-a-pull-request-to-an-issue-using-a-keyword>`__:

- lose
- closes
- closed
- fix
- fixes
- fixed
- resolve
- resolves
- resolved

Semantic Commit Messages
-------------------------------------

Semantic Commit Messages define standard structure for the commit subject line. The Semantic Commit Message format goes hand in hand with `semantic versioning <https://semver.org/>`__.

.. code-block:: none

             ┌─⫸ Subject: 72 characters or less.
             │
   ┌─────────┴─────────────┐
    <type>: <short summary>
      │           │
      │           └─⫸ Summary in imperative mood. Not capitalized.
      │                No period at the end. At least 20 characters.
      │
      └─⫸ Commit Type: build|ci|deprecate|docs|feat|fix|other|perf|
                        refactor|release|style|test

Commit Types
~~~~~~~~~~~~~

- build: (changes related to the build system)
- ci: (changes related to the continuous integration and deployment system)
- docs: (changes to the documentation)
- feat: (new feature for the user, not a new feature for build script)
- fix: (bug fix for the user, not a fix to a build script)
- other: (anything not covered by other types -- use as a last resort!)
- perf: (changes related to backward-compatible performance improvements)
- refactor: (refactoring production code, eg. renaming a variable)
- release: (making a release, e.g. bumping the package version for release)
- style: (formatting, missing semi colons, etc; no production code change)
- test: (adding missing tests, refactoring tests; no production code change)
- deprecate: (mark some code as deprecated)

.. note::

   Imperative is used to give a command, instruction or make a request.

   The imperative is formed with the verb in base form (without "to") without a subject. Imperative sentencies could be affirmative or negative to indicate prohibitions. The negative imperative is formed with "do not" or "don't" and the verb.

Semantic Commit Messages++
-------------------------------------

Adds optional scope, breaking change indicator and PR (pull request) number.

.. code-block:: none

                          ┌─⫸ Subject: 72 characters or less.
                          │
   ┌──────────────────────┴────────────────────────┐
    <type>(<scope>)!: <short summary> (<PR number>)
      │       │    │        │              │
      │       │    │        │              └─⫸ Optional Pull request number.
      │       │    │        │                   E.g. #765
      │       │    │        │
      │       │    │        └─⫸ Summary: Same as Semantic Commit Message
      │       │    │
      │       │    └─⫸ Optional breaking change indicator.
      │       │
      │       └─⫸ Optional Commit Scope: Module, package, component, area or
      │                                   issue number, e.g. #123.
      │
      └─⫸ Commit Type: Same as Semantic Commit Message.

Linting Commit Messages
-----------------------

https://jorisroovers.com/gitlint/


Generate changelog
-------------------

https://github.com/vaab/gitchangelog

`Generating release notes from git commit messages using basic shell commands (git/grep) <https://blogs.sap.com/2018/06/22/generating-release-notes-from-git-commit-messages-using-basic-shell-commands-gitgrep/>`__

`Automatically generated release notes <https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes>`__ at Github


Browsing History
-----------------

Git provides us the power to browse the repository commit history - so we're able to figure out what actually happened, who contributed and so on.

Let's see how the conventions might ease up the browsing:

.. code-block:: console

   $ git log --oneline --grep "^feat\|^fix\|^perf"

We use the commit message type to filter out and so showing only the production changes (all of the messages that start with feat, fix or perf).

Another example:

.. code-block:: console

   $ git log --oneline --grep "^feat" | wc -l

Further reading
----------------

- `Understanding Semantic Commit Messages <https://nitayneeman.com/posts/understanding-semantic-commit-messages-using-git-and-angular/>`__
- Executable Book `Commit Messages <https://executablebooks.org/en/latest/contributing.html#commit-messages>`__
- `Commit Message Guidelines <https://gist.github.com/robertpainsi/b632364184e70900af4ab688decf6f53>`__
- `Conventional Commits <https://www.conventionalcommits.org/en/v1.0.0/>`__
- `Angular Convention <https://github.com/angular/angular/blob/master/CONTRIBUTING.md#-commit-message-format>`__
- `Semantic Commit Messages <https://sparkbox.com/foundry/semantic_commit_messages>`__ by Jeremy Mack
- `Semantic Commit Messages <https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716>`__ by Josh Buchea
- `Git Commit Msg <http://karma-runner.github.io/6.3/dev/git-commit-msg.html>`__ - Karma Runner
- `Writing Meaningful Commit Messages <https://reflectoring.io/meaningful-commit-messages/>`_ - reflectoring.io
- `Git Commit Best Practices <https://gist.github.com/luismts/495d982e8c5b1a0ced4a57cf3d93cf60>`__ - gist
- `How to Write a Git Commit Message <https://cbea.ms/git-commit/>`__ by Chris Beams
