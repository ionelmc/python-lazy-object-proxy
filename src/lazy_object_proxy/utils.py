import sys

PY3 = sys.version_info[0] == 3

if PY3:
    string_types = str, bytes
else:
    string_types = basestring,


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
