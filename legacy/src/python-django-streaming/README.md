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

## The Streaming View

### Create the view

In the `polls/views.py` add following view:

```python
def streamed(request):
    sleep_interval = int(request.GET.get('sleep', 10))
    response = StreamingHttpResponse(my_processor(sleep_interval), content_type='text')
    return response
```

The view will return a StreamingHttpResponse to django. The streaming iterable streaming content to it. Django will iterable over the content and push the response to the client until the iteration finishes. 

The view accepts one argument `interval`. It is passed to the generator function. We will see it's purpose later.

In this case we passed a generator function `my_processor` which is our iterable content.

### Create the generator function

```python
def my_processor(sleep_interval):
    lines = [
        'Little brown lady',
        'Jumped into the blue water',
        'And smiled'
    ]
    start_time = time.time()
    while True:
        for line in lines:
            elapsed_time = int(time.time() - start_time)
            yield f"[{elapsed_time:>10} s] {line}\n"
            time.sleep(sleep_interval)
        yield "=========== Here we go again ===========\n"
```

What this function will do is, it will loop forever yielding the lines from the `lines` list to the client. Between each iteration it will sleep for a given interval of time.

### Register the view

Modify the `polls/urls.py`  to register the new view:

```python
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('streamed', views.streamed, name='streamed'),
]
```

### Test it

Start the development server and open a browser. Navigate to http://localhost:8000/polls/streamed. You will see a never ending output, like this:

```
[         0 s] Little brown lady
[        10 s] Jumped into the blue water
[        20 s] And smiled
=========== Here we go again ===========
[        30 s] Little brown lady
[        40 s] Jumped into the blue water
[        50 s] And smiled
=========== Here we go again ===========
[        60 s] Little brown lady
[        70 s] Jumped into the blue water
[        80 s] And smiled
=========== Here we go again ===========
[        90 s] Little brown lady
[       100 s] Jumped into the blue water
[       110 s] And smiled
=========== Here we go again ===========
[       120 s] Little brown lady
[       130 s] Jumped into the blue water
[       140 s] And smiled
=========== Here we go again ===========
[       150 s] Little brown lady
[       160 s] Jumped into the blue water
```

## Word of caution

You might be tempted to use HTTP views for processing data. Long processing could be interrupted for many reasons. For example middleware components, like load balancers might timeout. You can use the described approach to avoid this timeout by sending some dummy string, e.g. space on each iteration and prevent the load balancer from timing out. However, do not forget that the connection can be easily interrupted for variety of reasons. When the connection is interrupted, the web server usually kills the corresponding process immediately. Special measures need to be taken to keep your processing consistent.

## Further Reference

Django StreamingHttpResponse class is documented [here](https://docs.djangoproject.com/en/3.1/ref/request-response/#streaminghttpresponse-objects).

Other examples on using StreamingHttpResponse:

* [Django streaming view accepting byte range requests](https://gist.github.com/dcwatson/cb5d8157a8fa5a4a046e) (GitHub Gist)
* [Python django.http.StreamingHttpResponse() Examples](https://www.programcreek.com/python/example/52439/django.http.StreamingHttpResponse)