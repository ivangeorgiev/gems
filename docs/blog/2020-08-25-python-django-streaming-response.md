---
created: 2020-08-25 16:55:00
tags: python,django,straming
---

# Streaming response from Python Django application

![stream](img/stream-waterfalls.jpg)

There are many situations where you might need to stream your content. For example you might need to return big files which are impractical to be loaded fully into the memory.

For such situations, you should use Django's *StreamingHttpResponse*. I created a simple simulation for such situation. It has two parts:

A view:

```python
def streamed(request):
    sleep_interval = int(request.GET.get('sleep', 10))
    response = StreamingHttpResponse(my_processor(sleep_interval), content_type='text')
    return response
```

The view will create a *StreamingHttpResponse* object, using a generator, from the second part of the solution - a generator function:

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

The function iterates over a list of strings (*lines*) and yields each string. After string is processed by the generator client, the function sleeps for a given interval of time. Once all the strings from the list are processed, the loop starts over.

The view is registered in the application `views.py`.

You can find the [complete source](https://github.com/ivangeorgiev/gems/tree/master/src/python-django-streaming) for the streaming view solution in Python Django, along with more explanations, in [GitHub](https://github.com/ivangeorgiev/gems/tree/master/src/python-django-streaming).

