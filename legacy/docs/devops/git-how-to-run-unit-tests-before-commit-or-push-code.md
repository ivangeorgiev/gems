# How to execute unit tests before commit or push to git?

The term “shift left” refers to a practice in software development in which teams focus on quality, work on problem prevention instead of detection, and begin testing as early as possible. The goal is to increase quality, shorten long test cycles and reduce the possibility of unpleasant surprises at the end of the development cycle—or, worse, in production.

For teams who exercise Test Driven Development (TDD) the red-green-refactor cycle is natural. It is very unlikely for such teams to commit or push into the repository code which was not tested.

I like saying that if some process is not automated than we do not follow it. How we can guarantee that the code being committed to git passes all the tests?

## Solution

### Pre-commit hooks

Create a pre-commit git hook to execute your tests. In an example, Python projects use pytest to execute tests.   

In your `.git/hooks` directory create a `pre-commit` file:

```bash
#!/bin/sh

pytest || exit 1
```

Now each time you issue commit command to git it will run the script. The commit will fail when pytest fails. Effectively you will not be able to commit to git code which is not tested.

### Pre-push hooks

If you like committing often, you might find the pre-commit hook approach overwhelming. It might be better that you you execute the tests before the code gets pushed to remote repository.

For this solution, you should remove the `.git/hooks/pre-commit` file if you have created one and create a file `.git/hooks/pre-push`:

```bash
#!/bin/sh

pytest || exit 1
```

You will be able to commit code locally, but when you run `git push`, before git executes the command, it will execute the pre-push script. If the script finishes with error, the push command will be aborted.

## Running the hooks manually

If you want to run hooks, you can:

1. Execute manually by running the script:

   ```
   bash .git/hooks/pre-commit
   ```

2. You can run the `git commit` or `git push` command. The hook will be executed before the actual command runs. So the pre-commit hook will be executed even if there are no files staged.

## Further Extensions

You could create hooks which not only run tests, but also ensure that certain code coverage is achieved. 

```bash
#!/bin/sh

pytest || exit 1
coverage report --fail-under=80 || exit 1
```

to perform also style checks, you could run `flake8`:

```bash
#!/bin/sh

flake8 pykata || exit 1
pytest || exit 1
coverage report --fail-under=80 || exit 1
```



## Further Reading

* [Shift left testing](https://en.wikipedia.org/wiki/Shift-left_testing)  on Wikipedia
* [DevOps: Shift Left to Reduce Failure](https://devops.com/devops-shift-left-avoid-failure/)
* [Githooks documentation](https://git-scm.com/docs/githooks)
* [Git Hooks](https://githooks.com/) article by Matthew Hudson
* [Pre-commit](https://pre-commit.com/) framework for managing and maintaining multi-language pre-commit hooks

