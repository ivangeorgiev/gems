def repeat(function, before=None, after=None):
    while True:
        try:
            value = function()
        except StopIteration:
            break
        if before is not None:
            before(value)
        yield value
        if after is not None:
            after(value)
