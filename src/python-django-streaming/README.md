



## Setup

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install Django
```

You can validate the installation by running following within Python REPL:

```python
>>> import django
>>> print(django.get_version())
3.1
```

Alternatively you could run following at the command line:

```bash
$ python -m django --version
3.1
```

To create an empty Django project:

```bash
$ django-admin startproject mysite .
```

