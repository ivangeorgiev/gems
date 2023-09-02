from collections import defaultdict


class Event:
    pass


class JobCreated(Event):
    def __init__(self, job):
        self.job = job


class JobUpdated(Event):
    def __init__(self, job):
        self.job = job


def handle(event: Event):
    for handler in HANDLERS[type(event)]:
        handler(event)


HANDLERS = defaultdict(list)
