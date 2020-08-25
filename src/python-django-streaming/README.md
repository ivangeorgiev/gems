# Django Streaming

Sample Django application with streaming response.

## Setup

### Install Django

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

### Create Django Project

To create an empty Django project:

```bash
$ django-admin startproject mysite .
```

### Start a development server

To run the development server:

```bash
$ python manage.py runserver
```

Alternatively for running on a different port:

```bash
$ python manage.py runserver 8080
```

or for binding at another IP address (0 is shortcut for 0.0.0.0):

```bash
$ python manage.py runserver 0:8000
```

### Create a new application

```bash
$ python manage.py startapp polls
```

Your application will be created in the polls directory.

Modify the `polls/views.py` file:

```python
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
```

Create a `polls/urls.py` file:

```python
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```

Modify the project's `mysite/urls.py` file:

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]
```

Run the development server and open your browser http://localhost:8000/polls/

## Streaming View

