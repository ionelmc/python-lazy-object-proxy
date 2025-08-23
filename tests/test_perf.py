from functools import partial

import pytest


@pytest.mark.parametrize('name', ['slots', 'cext', 'simple', 'django', 'objproxies'])
def test_perf(benchmark, name, lop_loader):
    implementation = lop_loader(name)
    obj = 'foobar'
    proxied = implementation.Proxy(lambda: obj)
    assert benchmark(partial(str, proxied)) == obj
