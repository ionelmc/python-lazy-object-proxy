def identity(obj):
    return obj


class cached_property(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, cls):
        if obj is None:
            return self
        value = obj.__dict__[self.func.__name__] = self.func(obj)
        return value


try:
    exec("""
from inspect import isawaitable


async def do_await(obj):
    return await obj


def do_yield_from(gen):
    return (yield from gen)


def await_(obj):
    if isawaitable(obj):
        return do_await(obj).__await__()
    else:
        return do_yield_from(obj)
""")
except (ImportError, SyntaxError):
    await_ = None
