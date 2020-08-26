# pyimporter

Python import lib extensions with import from implementation.

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
