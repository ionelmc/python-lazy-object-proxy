from functools import partial

import pytest


@pytest.mark.parametrize('name', ['slots', 'cext', 'simple', 'django', 'objproxies'])
def test_perf(benchmark, name, lop_loader):
    implementation = lop_loader(name)
    obj = 'foobar'
    proxied = implementation.Proxy(lambda: obj)
    assert benchmark(partial(str, proxied)) == obj


empty = object()


@pytest.fixture(scope='module', params=['SimpleProxy', 'LocalsSimpleProxy', 'CachedPropertyProxy', 'LocalsCachedPropertyProxy'])
def prototype(request):
    from lazy_object_proxy.simple import cached_property

    name = request.param

    if name == 'SimpleProxy':

        class SimpleProxy:
            def __init__(self, factory):
                self.factory = factory
                self.object = empty

            def __str__(self):
                if self.object is empty:
                    self.object = self.factory()
                return str(self.object)

        return SimpleProxy
    elif name == 'CachedPropertyProxy':

        class CachedPropertyProxy:
            def __init__(self, factory):
                self.factory = factory

            @cached_property
            def object(self):
                return self.factory()

            def __str__(self):
                return str(self.object)

        return CachedPropertyProxy
    elif name == 'LocalsSimpleProxy':

        class LocalsSimpleProxy:
            def __init__(self, factory):
                self.factory = factory
                self.object = empty

            def __str__(self, func=str):
                if self.object is empty:
                    self.object = self.factory()
                return func(self.object)

        return LocalsSimpleProxy
    elif name == 'LocalsCachedPropertyProxy':

        class LocalsCachedPropertyProxy:
            def __init__(self, factory):
                self.factory = factory

            @cached_property
            def object(self):
                return self.factory()

            def __str__(self, func=str):
                return func(self.object)

        return LocalsCachedPropertyProxy


@pytest.mark.benchmark(group='prototypes')
def test_proto(benchmark, prototype):
    obj = 'foobar'
    proxied = prototype(lambda: obj)
    assert benchmark(partial(str, proxied)) == obj
