import time
from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

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


def streamed(request):
    sleep_interval = int(request.GET.get('sleep', 10))
    response = StreamingHttpResponse(my_processor(sleep_interval), content_type='text')
    return response
