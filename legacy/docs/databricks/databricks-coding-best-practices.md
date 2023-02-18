# Databricks Best Practices for Testability

# Table of Contents

[[_TOC_]]

# Overview

By following simple practices, you could enable and improve the testability of your Databricks code.

* Name notebooks, using valid Python module names
* Name folders, using valid Python package names
* Refer notebooks, using relative paths
* Add `__init__` notebook at each folder
* `import` referred notebooks conditionally

# Naming Databricks Objects

## Naming Databricks notebooks

Name Databricks notebooks, using valid Python module names (see [PEP-8](https://www.python.org/dev/peps/pep-0008/#package-and-module-names))

> Modules should have short, all-lowercase names. Underscores can be used in the module name if it improves readability. Python packages should also have short, all-lowercase names, although the use of underscores is discouraged.

This would allow to import notebooks as regular Python modules when running the code outside Databricks, e.g. executing unit tests from build pipeline.

## Naming Databricks folders

Name Databricks folders, using valid Python package names (see [PEP-8](https://www.python.org/dev/peps/pep-0008/#package-and-module-names))

> Modules should have short, all-lowercase names. Underscores can be used in the module name if it improves readability. Python packages should also have short, all-lowercase names, although the use of underscores is discouraged.

This would allow to import folders as regular Python packages when running the code outside Databricks, e.g. executing unit tests from build pipeline.

# Structure

## Refer notebooks, using relative paths



## `import` referred notebooks conditionally

For all notebooks that are run by the current notebook, add conditional import statements:

```python
if "DATABRICKS_RUNTIME_VERSION" not in os.environ:
    from .other_notebook import *
```

This technique is useful in situations where you need to run code, defined by Databricks notebooks outside of Databricks environment, e.g. in unit tests.

If you are passing Databricks code through static code analysis tools, like SonarQube, you will get errors for symbols which are not defined in the notebook. Using this technique the symbols will be imported from dependent notebooks and the static analysis will pass.

**Example:**

If you created a notebook `process-data`  which runs two other notebooks `process-lib` and `quality-lib`:

```
%run ./process_lib
```

```
%run ./quality_lib
```

You have to add one cell with import statements:

```python
if "DATABRICKS_RUNTIME_VERSION" not in os.environ:
    from .process_lib import *
    from .quality_lib import *
```



## Add `__init__` notebook in each Databricks folder

Following this practice enables importing Databricks folders as packages. Useful when you need to run notebook code outside Databricks.

# Other

## How to detect if running inside Databricks?

Databricks has number of environment variables defined. You can use one of them, e.g. `DATABRICKS_RUNTIME_VERSION` to detect if the code is running inside Databricks.

```python
import os

def is_databricks() -> bool:
  return "DATABRICKS_RUNTIME_VERSION" in os.environ
```

