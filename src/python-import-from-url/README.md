# pyimporter

Python import lib extensions with implementation to import from url.

## Installation

The easiest way to install the package is to use `pip` and install directly from `pypi`:

```bash
$ pip install pyimporter
```

## Building

Install dependencies:

```bash
$ pip install --upgrade setuptools wheel
$ pip install --upgrade twine
```

Build the distribution package:

```bash
$ python setup.py sdist bdist_wheel
```

Upload the package to pypi:

```bash
$ python -m twine upload dist/*
```

## Testing

The tests are implemented using pytest. You need to install pytest first:

```bash
$ pip install pytest
```

For functional tests, internally a live server is used. By default the functional tests are deselected. To run the functional tests, add the `--functional` option flag to pytest command line:

```bash
$ pytest --functional
```

If you prefer verbose output, add `-v` or `-vv` option to the pytest command line:

```bash
$ pytest --functional -vv
```


## Reference

The import system: https://docs.python.org/3/reference/import.html

Sample implementations:
- https://blog.quiltdata.com/import-almost-anything-in-python-an-intro-to-module-loaders-and-finders-f5e7b15cda47
- https://github.com/polinom/knockout
