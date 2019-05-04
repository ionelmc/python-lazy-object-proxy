from __future__ import print_function

import gc
import imp
import pickle
import platform
import sys
import weakref
from datetime import date
from datetime import datetime
from decimal import Decimal
from functools import partial

import pytest
from compat import PY2
from compat import PY3
from compat import exec_

PYPY = '__pypy__' in sys.builtin_module_names

OBJECTS_CODE = """
class TargetBaseClass(object):
    "documentation"

class Target(TargetBaseClass):
    "documentation"

def target():
    "documentation"
    pass
"""

objects = imp.new_module('objects')
exec_(OBJECTS_CODE, objects.__dict__, objects.__dict__)


def load_implementation(name):
    class FakeModule:
        subclass = False
        kind = name
        if name == "slots":
            from lazy_object_proxy.slots import Proxy
        elif name == "simple":
            from lazy_object_proxy.simple import Proxy
        elif name == "cext":
            try:
                from lazy_object_proxy.cext import Proxy
            except ImportError:
                if PYPY:
                    pytest.skip(msg="C Extension not available.")
                else:
                    raise
        elif name == "objproxies":
            Proxy = pytest.importorskip("objproxies").LazyProxy
        elif name == "django":
            Proxy = pytest.importorskip("django.utils.functional").SimpleLazyObject
        else:
            raise RuntimeError("Unsupported param: %r." % name)

        Proxy

    return FakeModule


@pytest.fixture(scope="module", params=[
    "slots", "cext",
    "simple",
    # "external-django", "external-objproxies"
])
def lop_implementation(request):
    return load_implementation(request.param)


@pytest.fixture(scope="module", params=[True, False], ids=['subclassed', 'normal'])
def lop_subclass(request, lop_implementation):
    if request.param:
        class submod(lop_implementation):
            subclass = True
            Proxy = type("SubclassOf_" + lop_implementation.Proxy.__name__,
                         (lop_implementation.Proxy,), {})

        return submod
    else:
        return lop_implementation


@pytest.fixture(scope="function")
def lazy_object_proxy(request, lop_subclass):
    if request.node.get_closest_marker('xfail_subclass'):
        request.applymarker(pytest.mark.xfail(
            reason="This test can't work because subclassing disables certain "
                   "features like __doc__ and __module__ proxying."
        ))
    if request.node.get_closest_marker('xfail_simple'):
        request.applymarker(pytest.mark.xfail(
            reason="The lazy_object_proxy.simple.Proxy has some limitations."
        ))

    return lop_subclass


def test_round(lazy_object_proxy):
    proxy = lazy_object_proxy.Proxy(lambda: 1.2)
    assert round(proxy) == 1


def test_attributes(lazy_object_proxy):
    def function1(*args, **kwargs):
        return args, kwargs

    function2 = lazy_object_proxy.Proxy(lambda: function1)

    assert function2.__wrapped__ == function1


def test_get_wrapped(lazy_object_proxy):
    def function1(*args, **kwargs):
        return args, kwargs

    function2 = lazy_object_proxy.Proxy(lambda: function1)

    assert function2.__wrapped__ == function1

    function3 = lazy_object_proxy.Proxy(lambda: function2)

    assert function3.__wrapped__ == function1


def test_set_wrapped(lazy_object_proxy):
    def function1(*args, **kwargs):
        return args, kwargs

    function2 = lazy_object_proxy.Proxy(lambda: function1)

    assert function2 == function1
    assert function2.__wrapped__ is function1
    assert function2.__name__ == function1.__name__

    if PY3:
        assert function2.__qualname__ == function1.__qualname__

    function2.__wrapped__ = None

    assert not hasattr(function1, '__wrapped__')

    assert function2 == None  # noqa
    assert function2.__wrapped__ is None
    assert not hasattr(function2, '__name__')

    if PY3:
        assert not hasattr(function2, '__qualname__')

    def function3(*args, **kwargs):
        return args, kwargs

    function2.__wrapped__ = function3

    assert function2 == function3
    assert function2.__wrapped__ == function3
    assert function2.__name__ == function3.__name__

    if PY3:
        assert function2.__qualname__ == function3.__qualname__


def test_wrapped_attribute(lazy_object_proxy):
    def function1(*args, **kwargs):
        return args, kwargs

    function2 = lazy_object_proxy.Proxy(lambda: function1)

    function2.variable = True

    assert hasattr(function1, 'variable')
    assert hasattr(function2, 'variable')

    assert function2.variable is True

    del function2.variable

    assert not hasattr(function1, 'variable')
    assert not hasattr(function2, 'variable')

    assert getattr(function2, 'variable', None) is None


def test_class_object_name(lazy_object_proxy):
    # Test preservation of class __name__ attribute.

    target = objects.Target
    wrapper = lazy_object_proxy.Proxy(lambda: target)

    assert wrapper.__name__ == target.__name__


def test_class_object_qualname(lazy_object_proxy):
    # Test preservation of class __qualname__ attribute.

    target = objects.Target
    wrapper = lazy_object_proxy.Proxy(lambda: target)

    try:
        __qualname__ = target.__qualname__
    except AttributeError:
        pass
    else:
        assert wrapper.__qualname__ == __qualname__


@pytest.mark.xfail_subclass
def test_class_module_name(lazy_object_proxy):
    # Test preservation of class __module__ attribute.

    target = objects.Target
    wrapper = lazy_object_proxy.Proxy(lambda: target)

    assert wrapper.__module__ == target.__module__


@pytest.mark.xfail_subclass
def test_class_doc_string(lazy_object_proxy):
    # Test preservation of class __doc__ attribute.

    target = objects.Target
    wrapper = lazy_object_proxy.Proxy(lambda: target)

    assert wrapper.__doc__ == target.__doc__


@pytest.mark.xfail_subclass
def test_instance_module_name(lazy_object_proxy):
    # Test preservation of instance __module__ attribute.

    target = objects.Target()
    wrapper = lazy_object_proxy.Proxy(lambda: target)

    assert wrapper.__module__ == target.__module__


@pytest.mark.xfail_subclass
def test_instance_doc_string(lazy_object_proxy):
    # Test preservation of instance __doc__ attribute.

    target = objects.Target()
    wrapper = lazy_object_proxy.Proxy(lambda: target)

    assert wrapper.__doc__ == target.__doc__


def test_function_object_name(lazy_object_proxy):
    # Test preservation of function __name__ attribute.

    target = objects.target
    wrapper = lazy_object_proxy.Proxy(lambda: target)

    assert wrapper.__name__ == target.__name__


def test_function_object_qualname(lazy_object_proxy):
    # Test preservation of function __qualname__ attribute.

    target = objects.target
    wrapper = lazy_object_proxy.Proxy(lambda: target)

    try:
        __qualname__ = target.__qualname__
    except AttributeError:
        pass
    else:
        assert wrapper.__qualname__ == __qualname__


@pytest.mark.xfail_subclass
def test_function_module_name(lazy_object_proxy):
    # Test preservation of function __module__ attribute.

    target = objects.target
    wrapper = lazy_object_proxy.Proxy(lambda: target)

    assert wrapper.__module__ == target.__module__


@pytest.mark.xfail_subclass
def test_function_doc_string(lazy_object_proxy):
    # Test preservation of function __doc__ attribute.

    target = objects.target
    wrapper = lazy_object_proxy.Proxy(lambda: target)

    assert wrapper.__doc__ == target.__doc__


def test_class_of_class(lazy_object_proxy):
    # Test preservation of class __class__ attribute.

    target = objects.Target
    wrapper = lazy_object_proxy.Proxy(lambda: target)

    assert wrapper.__class__ is target.__class__

    assert isinstance(wrapper, type(target))


def test_revert_class_proxying(lazy_object_proxy):
    class ProxyWithOldStyleIsInstance(lazy_object_proxy.Proxy):
        __class__ = object.__dict__['__class__']

    target = objects.Target()
    wrapper = ProxyWithOldStyleIsInstance(lambda: target)

    assert wrapper.__class__ is ProxyWithOldStyleIsInstance

    assert isinstance(wrapper, ProxyWithOldStyleIsInstance)
    assert not isinstance(wrapper, objects.Target)
    assert not isinstance(wrapper, objects.TargetBaseClass)

    class ProxyWithOldStyleIsInstance2(ProxyWithOldStyleIsInstance):
        pass

    wrapper = ProxyWithOldStyleIsInstance2(lambda: target)

    assert wrapper.__class__ is ProxyWithOldStyleIsInstance2

    assert isinstance(wrapper, ProxyWithOldStyleIsInstance2)
    assert not isinstance(wrapper, objects.Target)
    assert not isinstance(wrapper, objects.TargetBaseClass)


def test_class_of_instance(lazy_object_proxy):
    # Test preservation of instance __class__ attribute.

    target = objects.Target()
    wrapper = lazy_object_proxy.Proxy(lambda: target)

    assert wrapper.__class__ is target.__class__

    assert isinstance(wrapper, objects.Target)
    assert isinstance(wrapper, objects.TargetBaseClass)


def test_class_of_function(lazy_object_proxy):
    # Test preservation of function __class__ attribute.

    target = objects.target
    wrapper = lazy_object_proxy.Proxy(lambda: target)

    assert wrapper.__class__ is target.__class__

    assert isinstance(wrapper, type(target))


def test_dir_of_class(lazy_object_proxy):
    # Test preservation of class __dir__ attribute.

    target = objects.Target
    wrapper = lazy_object_proxy.Proxy(lambda: target)

    assert dir(wrapper) == dir(target)


@pytest.mark.xfail_simple
def test_vars_of_class(lazy_object_proxy):
    # Test preservation of class __dir__ attribute.

    target = objects.Target
    wrapper = lazy_object_proxy.Proxy(lambda: target)

    assert vars(wrapper) == vars(target)


def test_dir_of_instance(lazy_object_proxy):
    # Test preservation of instance __dir__ attribute.

    target = objects.Target()
    wrapper = lazy_object_proxy.Proxy(lambda: target)

    assert dir(wrapper) == dir(target)


@pytest.mark.xfail_simple
def test_vars_of_instance(lazy_object_proxy):
    # Test preservation of instance __dir__ attribute.

    target = objects.Target()
    wrapper = lazy_object_proxy.Proxy(lambda: target)

    assert vars(wrapper) == vars(target)


def test_dir_of_function(lazy_object_proxy):
    # Test preservation of function __dir__ attribute.

    target = objects.target
    wrapper = lazy_object_proxy.Proxy(lambda: target)

    assert dir(wrapper) == dir(target)


@pytest.mark.xfail_simple
def test_vars_of_function(lazy_object_proxy):
    # Test preservation of function __dir__ attribute.

    target = objects.target
    wrapper = lazy_object_proxy.Proxy(lambda: target)

    assert vars(wrapper) == vars(target)


def test_function_no_args(lazy_object_proxy):
    _args = ()
    _kwargs = {}

    def function(*args, **kwargs):
        return args, kwargs

    wrapper = lazy_object_proxy.Proxy(lambda: function)

    result = wrapper()

    assert result == (_args, _kwargs)


def test_function_args(lazy_object_proxy):
    _args = (1, 2)
    _kwargs = {}

    def function(*args, **kwargs):
        return args, kwargs

    wrapper = lazy_object_proxy.Proxy(lambda: function)

    result = wrapper(*_args)

    assert result == (_args, _kwargs)


def test_function_kwargs(lazy_object_proxy):
    _args = ()
    _kwargs = {"one": 1, "two": 2}

    def function(*args, **kwargs):
        return args, kwargs

    wrapper = lazy_object_proxy.Proxy(lambda: function)

    result = wrapper(**_kwargs)

    assert result == (_args, _kwargs)


def test_function_args_plus_kwargs(lazy_object_proxy):
    _args = (1, 2)
    _kwargs = {"one": 1, "two": 2}

    def function(*args, **kwargs):
        return args, kwargs

    wrapper = lazy_object_proxy.Proxy(lambda: function)

    result = wrapper(*_args, **_kwargs)

    assert result == (_args, _kwargs)


def test_instancemethod_no_args(lazy_object_proxy):
    _args = ()
    _kwargs = {}

    class Class(object):
        def function(self, *args, **kwargs):
            return args, kwargs

    wrapper = lazy_object_proxy.Proxy(lambda: Class().function)

    result = wrapper()

    assert result == (_args, _kwargs)


def test_instancemethod_args(lazy_object_proxy):
    _args = (1, 2)
    _kwargs = {}

    class Class(object):
        def function(self, *args, **kwargs):
            return args, kwargs

    wrapper = lazy_object_proxy.Proxy(lambda: Class().function)

    result = wrapper(*_args)

    assert result == (_args, _kwargs)


def test_instancemethod_kwargs(lazy_object_proxy):
    _args = ()
    _kwargs = {"one": 1, "two": 2}

    class Class(object):
        def function(self, *args, **kwargs):
            return args, kwargs

    wrapper = lazy_object_proxy.Proxy(lambda: Class().function)

    result = wrapper(**_kwargs)

    assert result == (_args, _kwargs)


def test_instancemethod_args_plus_kwargs(lazy_object_proxy):
    _args = (1, 2)
    _kwargs = {"one": 1, "two": 2}

    class Class(object):
        def function(self, *args, **kwargs):
            return args, kwargs

    wrapper = lazy_object_proxy.Proxy(lambda: Class().function)

    result = wrapper(*_args, **_kwargs)

    assert result == (_args, _kwargs)


def test_instancemethod_via_class_no_args(lazy_object_proxy):
    _args = ()
    _kwargs = {}

    class Class(object):
        def function(self, *args, **kwargs):
            return args, kwargs

    wrapper = lazy_object_proxy.Proxy(lambda: Class.function)

    result = wrapper(Class())

    assert result == (_args, _kwargs)


def test_instancemethod_via_class_args(lazy_object_proxy):
    _args = (1, 2)
    _kwargs = {}

    class Class(object):
        def function(self, *args, **kwargs):
            return args, kwargs

    wrapper = lazy_object_proxy.Proxy(lambda: Class.function)

    result = wrapper(Class(), *_args)

    assert result == (_args, _kwargs)


def test_instancemethod_via_class_kwargs(lazy_object_proxy):
    _args = ()
    _kwargs = {"one": 1, "two": 2}

    class Class(object):
        def function(self, *args, **kwargs):
            return args, kwargs

    wrapper = lazy_object_proxy.Proxy(lambda: Class.function)

    result = wrapper(Class(), **_kwargs)

    assert result == (_args, _kwargs)


def test_instancemethod_via_class_args_plus_kwargs(lazy_object_proxy):
    _args = (1, 2)
    _kwargs = {"one": 1, "two": 2}

    class Class(object):
        def function(self, *args, **kwargs):
            return args, kwargs

    wrapper = lazy_object_proxy.Proxy(lambda: Class.function)

    result = wrapper(Class(), *_args, **_kwargs)

    assert result == (_args, _kwargs)


def test_classmethod_no_args(lazy_object_proxy):
    _args = ()
    _kwargs = {}

    class Class(object):
        @classmethod
        def function(cls, *args, **kwargs):
            return args, kwargs

    wrapper = lazy_object_proxy.Proxy(lambda: Class().function)

    result = wrapper()

    assert result == (_args, _kwargs)


def test_classmethod_args(lazy_object_proxy):
    _args = (1, 2)
    _kwargs = {}

    class Class(object):
        @classmethod
        def function(cls, *args, **kwargs):
            return args, kwargs

    wrapper = lazy_object_proxy.Proxy(lambda: Class().function)

    result = wrapper(*_args)

    assert result == (_args, _kwargs)


def test_classmethod_kwargs(lazy_object_proxy):
    _args = ()
    _kwargs = {"one": 1, "two": 2}

    class Class(object):
        @classmethod
        def function(cls, *args, **kwargs):
            return args, kwargs

    wrapper = lazy_object_proxy.Proxy(lambda: Class().function)

    result = wrapper(**_kwargs)

    assert result == (_args, _kwargs)


def test_classmethod_args_plus_kwargs(lazy_object_proxy):
    _args = (1, 2)
    _kwargs = {"one": 1, "two": 2}

    class Class(object):
        @classmethod
        def function(cls, *args, **kwargs):
            return args, kwargs

    wrapper = lazy_object_proxy.Proxy(lambda: Class().function)

    result = wrapper(*_args, **_kwargs)

    assert result == (_args, _kwargs)


def test_classmethod_via_class_no_args(lazy_object_proxy):
    _args = ()
    _kwargs = {}

    class Class(object):
        @classmethod
        def function(cls, *args, **kwargs):
            return args, kwargs

    wrapper = lazy_object_proxy.Proxy(lambda: Class.function)

    result = wrapper()

    assert result == (_args, _kwargs)


def test_classmethod_via_class_args(lazy_object_proxy):
    _args = (1, 2)
    _kwargs = {}

    class Class(object):
        @classmethod
        def function(cls, *args, **kwargs):
            return args, kwargs

    wrapper = lazy_object_proxy.Proxy(lambda: Class.function)

    result = wrapper(*_args)

    assert result == (_args, _kwargs)


def test_classmethod_via_class_kwargs(lazy_object_proxy):
    _args = ()
    _kwargs = {"one": 1, "two": 2}

    class Class(object):
        @classmethod
        def function(cls, *args, **kwargs):
            return args, kwargs

    wrapper = lazy_object_proxy.Proxy(lambda: Class.function)

    result = wrapper(**_kwargs)

    assert result == (_args, _kwargs)


def test_classmethod_via_class_args_plus_kwargs(lazy_object_proxy):
    _args = (1, 2)
    _kwargs = {"one": 1, "two": 2}

    class Class(object):
        @classmethod
        def function(cls, *args, **kwargs):
            return args, kwargs

    wrapper = lazy_object_proxy.Proxy(lambda: Class.function)

    result = wrapper(*_args, **_kwargs)

    assert result == (_args, _kwargs)


def test_staticmethod_no_args(lazy_object_proxy):
    _args = ()
    _kwargs = {}

    class Class(object):
        @staticmethod
        def function(*args, **kwargs):
            return args, kwargs

    wrapper = lazy_object_proxy.Proxy(lambda: Class().function)

    result = wrapper()

    assert result == (_args, _kwargs)


def test_staticmethod_args(lazy_object_proxy):
    _args = (1, 2)
    _kwargs = {}

    class Class(object):
        @staticmethod
        def function(*args, **kwargs):
            return args, kwargs

    wrapper = lazy_object_proxy.Proxy(lambda: Class().function)

    result = wrapper(*_args)

    assert result == (_args, _kwargs)


def test_staticmethod_kwargs(lazy_object_proxy):
    _args = ()
    _kwargs = {"one": 1, "two": 2}

    class Class(object):
        @staticmethod
        def function(*args, **kwargs):
            return args, kwargs

    wrapper = lazy_object_proxy.Proxy(lambda: Class().function)

    result = wrapper(**_kwargs)

    assert result == (_args, _kwargs)


def test_staticmethod_args_plus_kwargs(lazy_object_proxy):
    _args = (1, 2)
    _kwargs = {"one": 1, "two": 2}

    class Class(object):
        @staticmethod
        def function(*args, **kwargs):
            return args, kwargs

    wrapper = lazy_object_proxy.Proxy(lambda: Class().function)

    result = wrapper(*_args, **_kwargs)

    assert result == (_args, _kwargs)


def test_staticmethod_via_class_no_args(lazy_object_proxy):
    _args = ()
    _kwargs = {}

    class Class(object):
        @staticmethod
        def function(*args, **kwargs):
            return args, kwargs

    wrapper = lazy_object_proxy.Proxy(lambda: Class.function)

    result = wrapper()

    assert result == (_args, _kwargs)


def test_staticmethod_via_class_args(lazy_object_proxy):
    _args = (1, 2)
    _kwargs = {}

    class Class(object):
        @staticmethod
        def function(*args, **kwargs):
            return args, kwargs

    wrapper = lazy_object_proxy.Proxy(lambda: Class.function)

    result = wrapper(*_args)

    assert result == (_args, _kwargs)


def test_staticmethod_via_class_kwargs(lazy_object_proxy):
    _args = ()
    _kwargs = {"one": 1, "two": 2}

    class Class(object):
        @staticmethod
        def function(*args, **kwargs):
            return args, kwargs

    wrapper = lazy_object_proxy.Proxy(lambda: Class.function)

    result = wrapper(**_kwargs)

    assert result == (_args, _kwargs)


def test_staticmethod_via_class_args_plus_kwargs(lazy_object_proxy):
    _args = (1, 2)
    _kwargs = {"one": 1, "two": 2}

    class Class(object):
        @staticmethod
        def function(*args, **kwargs):
            return args, kwargs

    wrapper = lazy_object_proxy.Proxy(lambda: Class.function)

    result = wrapper(*_args, **_kwargs)

    assert result == (_args, _kwargs)


def test_iteration(lazy_object_proxy):
    items = [1, 2]

    wrapper = lazy_object_proxy.Proxy(lambda: items)

    result = [x for x in wrapper]

    assert result == items

    with pytest.raises(TypeError):
        for _ in lazy_object_proxy.Proxy(lambda: 1):
            pass


def test_iter_builtin(lazy_object_proxy):
    iter(lazy_object_proxy.Proxy(lambda: [1, 2]))
    pytest.raises(TypeError, iter, lazy_object_proxy.Proxy(lambda: 1))


def test_context_manager(lazy_object_proxy):
    class Class(object):
        def __enter__(self):
            return self

        def __exit__(*args, **kwargs):
            return

    instance = Class()

    wrapper = lazy_object_proxy.Proxy(lambda: instance)

    with wrapper:
        pass


def test_object_hash(lazy_object_proxy):
    def function1(*args, **kwargs):
        return args, kwargs

    function2 = lazy_object_proxy.Proxy(lambda: function1)

    assert hash(function2) == hash(function1)


def test_mapping_key(lazy_object_proxy):
    def function1(*args, **kwargs):
        return args, kwargs

    function2 = lazy_object_proxy.Proxy(lambda: function1)

    table = dict()
    table[function1] = True

    assert table.get(function2)

    table = dict()
    table[function2] = True

    assert table.get(function1)


def test_comparison(lazy_object_proxy):
    one = lazy_object_proxy.Proxy(lambda: 1)
    two = lazy_object_proxy.Proxy(lambda: 2)
    three = lazy_object_proxy.Proxy(lambda: 3)

    assert two > 1
    assert two >= 1
    assert two < 3
    assert two <= 3
    assert two != 1
    assert two == 2
    assert two != 3

    assert 2 > one
    assert 2 >= one
    assert 2 < three
    assert 2 <= three
    assert 2 != one
    assert 2 == two
    assert 2 != three

    assert two > one
    assert two >= one
    assert two < three
    assert two <= three
    assert two != one
    assert two == two
    assert two != three


def test_nonzero(lazy_object_proxy):
    true = lazy_object_proxy.Proxy(lambda: True)
    false = lazy_object_proxy.Proxy(lambda: False)

    assert true
    assert not false

    assert bool(true)
    assert not bool(false)

    assert not false
    assert not not true


def test_int(lazy_object_proxy):
    one = lazy_object_proxy.Proxy(lambda: 1)

    assert int(one) == 1

    if not PY3:
        assert long(one) == 1  # noqa


def test_float(lazy_object_proxy):
    one = lazy_object_proxy.Proxy(lambda: 1)

    assert float(one) == 1.0


def test_add(lazy_object_proxy):
    one = lazy_object_proxy.Proxy(lambda: 1)
    two = lazy_object_proxy.Proxy(lambda: 2)

    assert one + two == 1 + 2
    assert 1 + two == 1 + 2
    assert one + 2 == 1 + 2


def test_sub(lazy_object_proxy):
    one = lazy_object_proxy.Proxy(lambda: 1)
    two = lazy_object_proxy.Proxy(lambda: 2)

    assert one - two == 1 - 2
    assert 1 - two == 1 - 2
    assert one - 2 == 1 - 2


def test_mul(lazy_object_proxy):
    two = lazy_object_proxy.Proxy(lambda: 2)
    three = lazy_object_proxy.Proxy(lambda: 3)

    assert two * three == 2 * 3
    assert 2 * three == 2 * 3
    assert two * 3 == 2 * 3


def test_div(lazy_object_proxy):
    # On Python 2 this will pick up div and on Python
    # 3 it will pick up truediv.

    two = lazy_object_proxy.Proxy(lambda: 2)
    three = lazy_object_proxy.Proxy(lambda: 3)

    assert two / three == 2 / 3
    assert 2 / three == 2 / 3
    assert two / 3 == 2 / 3


def test_divdiv(lazy_object_proxy):
    two = lazy_object_proxy.Proxy(lambda: 2)
    three = lazy_object_proxy.Proxy(lambda: 3)

    assert three // two == 3 // 2
    assert 3 // two == 3 // 2
    assert three // 2 == 3 // 2


def test_mod(lazy_object_proxy):
    two = lazy_object_proxy.Proxy(lambda: 2)
    three = lazy_object_proxy.Proxy(lambda: 3)

    assert three % two == 3 % 2
    assert 3 % two == 3 % 2
    assert three % 2 == 3 % 2


def test_divmod(lazy_object_proxy):
    two = lazy_object_proxy.Proxy(lambda: 2)
    three = lazy_object_proxy.Proxy(lambda: 3)

    assert divmod(three, two), divmod(3 == 2)
    assert divmod(3, two), divmod(3 == 2)
    assert divmod(three, 2), divmod(3 == 2)


def test_pow(lazy_object_proxy):
    two = lazy_object_proxy.Proxy(lambda: 2)
    three = lazy_object_proxy.Proxy(lambda: 3)

    assert three ** two == pow(3, 2)
    assert 3 ** two == pow(3, 2)
    assert three ** 2 == pow(3, 2)

    assert pow(three, two) == pow(3, 2)
    assert pow(3, two) == pow(3, 2)
    assert pow(three, 2) == pow(3, 2)

    # Only PyPy implements __rpow__ for ternary pow().

    if PYPY:
        assert pow(three, two, 2) == pow(3, 2, 2)
        assert pow(3, two, 2) == pow(3, 2, 2)

    assert pow(three, 2, 2) == pow(3, 2, 2)


def test_lshift(lazy_object_proxy):
    two = lazy_object_proxy.Proxy(lambda: 2)
    three = lazy_object_proxy.Proxy(lambda: 3)

    assert three << two == 3 << 2
    assert 3 << two == 3 << 2
    assert three << 2 == 3 << 2


def test_rshift(lazy_object_proxy):
    two = lazy_object_proxy.Proxy(lambda: 2)
    three = lazy_object_proxy.Proxy(lambda: 3)

    assert three >> two == 3 >> 2
    assert 3 >> two == 3 >> 2
    assert three >> 2 == 3 >> 2


def test_and(lazy_object_proxy):
    two = lazy_object_proxy.Proxy(lambda: 2)
    three = lazy_object_proxy.Proxy(lambda: 3)

    assert three & two == 3 & 2
    assert 3 & two == 3 & 2
    assert three & 2 == 3 & 2


def test_xor(lazy_object_proxy):
    two = lazy_object_proxy.Proxy(lambda: 2)
    three = lazy_object_proxy.Proxy(lambda: 3)

    assert three ^ two == 3 ^ 2
    assert 3 ^ two == 3 ^ 2
    assert three ^ 2 == 3 ^ 2


def test_or(lazy_object_proxy):
    two = lazy_object_proxy.Proxy(lambda: 2)
    three = lazy_object_proxy.Proxy(lambda: 3)

    assert three | two == 3 | 2
    assert 3 | two == 3 | 2
    assert three | 2 == 3 | 2


def test_iadd(lazy_object_proxy):
    value = lazy_object_proxy.Proxy(lambda: 1)
    one = lazy_object_proxy.Proxy(lambda: 1)

    value += 1
    assert value == 2

    if lazy_object_proxy.kind != 'simple':
        assert type(value) == lazy_object_proxy.Proxy

    value += one
    assert value == 3

    if lazy_object_proxy.kind != 'simple':
        assert type(value) == lazy_object_proxy.Proxy


def test_isub(lazy_object_proxy):
    value = lazy_object_proxy.Proxy(lambda: 1)
    one = lazy_object_proxy.Proxy(lambda: 1)

    value -= 1
    assert value == 0
    if lazy_object_proxy.kind != 'simple':
        assert type(value) == lazy_object_proxy.Proxy

    value -= one
    assert value == -1

    if lazy_object_proxy.kind != 'simple':
        assert type(value) == lazy_object_proxy.Proxy


def test_imul(lazy_object_proxy):
    value = lazy_object_proxy.Proxy(lambda: 2)
    two = lazy_object_proxy.Proxy(lambda: 2)

    value *= 2
    assert value == 4

    if lazy_object_proxy.kind != 'simple':
        assert type(value) == lazy_object_proxy.Proxy

    value *= two
    assert value == 8

    if lazy_object_proxy.kind != 'simple':
        assert type(value) == lazy_object_proxy.Proxy


def test_idiv(lazy_object_proxy):
    # On Python 2 this will pick up div and on Python
    # 3 it will pick up truediv.

    value = lazy_object_proxy.Proxy(lambda: 2)
    two = lazy_object_proxy.Proxy(lambda: 2)

    value /= 2
    assert value == 2 / 2

    if lazy_object_proxy.kind != 'simple':
        assert type(value) == lazy_object_proxy.Proxy

    value /= two
    assert value == 2 / 2 / 2

    if lazy_object_proxy.kind != 'simple':
        assert type(value) == lazy_object_proxy.Proxy


def test_ifloordiv(lazy_object_proxy):
    value = lazy_object_proxy.Proxy(lambda: 2)
    two = lazy_object_proxy.Proxy(lambda: 2)

    value //= 2
    assert value == 2 // 2

    if lazy_object_proxy.kind != 'simple':
        assert type(value) == lazy_object_proxy.Proxy

    value //= two
    assert value == 2 // 2 // 2

    if lazy_object_proxy.kind != 'simple':
        assert type(value) == lazy_object_proxy.Proxy


def test_imod(lazy_object_proxy):
    value = lazy_object_proxy.Proxy(lambda: 10)
    two = lazy_object_proxy.Proxy(lambda: 2)

    value %= 2
    assert value == 10 % 2

    if lazy_object_proxy.kind != 'simple':
        assert type(value) == lazy_object_proxy.Proxy

    value %= two
    assert value == 10 % 2 % 2

    if lazy_object_proxy.kind != 'simple':
        assert type(value) == lazy_object_proxy.Proxy


def test_ipow(lazy_object_proxy):
    value = lazy_object_proxy.Proxy(lambda: 10)
    two = lazy_object_proxy.Proxy(lambda: 2)

    value **= 2
    assert value == 10 ** 2

    if lazy_object_proxy.kind != 'simple':
        assert type(value) == lazy_object_proxy.Proxy

    value **= two
    assert value == 10 ** 2 ** 2

    if lazy_object_proxy.kind != 'simple':
        assert type(value) == lazy_object_proxy.Proxy


def test_ilshift(lazy_object_proxy):
    value = lazy_object_proxy.Proxy(lambda: 256)
    two = lazy_object_proxy.Proxy(lambda: 2)

    value <<= 2
    assert value == 256 << 2

    if lazy_object_proxy.kind != 'simple':
        assert type(value) == lazy_object_proxy.Proxy

    value <<= two
    assert value == 256 << 2 << 2

    if lazy_object_proxy.kind != 'simple':
        assert type(value) == lazy_object_proxy.Proxy


def test_irshift(lazy_object_proxy):
    value = lazy_object_proxy.Proxy(lambda: 2)
    two = lazy_object_proxy.Proxy(lambda: 2)

    value >>= 2
    assert value == 2 >> 2

    if lazy_object_proxy.kind != 'simple':
        assert type(value) == lazy_object_proxy.Proxy

    value >>= two
    assert value == 2 >> 2 >> 2

    if lazy_object_proxy.kind != 'simple':
        assert type(value) == lazy_object_proxy.Proxy


def test_iand(lazy_object_proxy):
    value = lazy_object_proxy.Proxy(lambda: 1)
    two = lazy_object_proxy.Proxy(lambda: 2)

    value &= 2
    assert value == 1 & 2

    if lazy_object_proxy.kind != 'simple':
        assert type(value) == lazy_object_proxy.Proxy

    value &= two
    assert value == 1 & 2 & 2

    if lazy_object_proxy.kind != 'simple':
        assert type(value) == lazy_object_proxy.Proxy


def test_ixor(lazy_object_proxy):
    value = lazy_object_proxy.Proxy(lambda: 1)
    two = lazy_object_proxy.Proxy(lambda: 2)

    value ^= 2
    assert value == 1 ^ 2

    if lazy_object_proxy.kind != 'simple':
        assert type(value) == lazy_object_proxy.Proxy

    value ^= two
    assert value == 1 ^ 2 ^ 2

    if lazy_object_proxy.kind != 'simple':
        assert type(value) == lazy_object_proxy.Proxy


def test_ior(lazy_object_proxy):
    value = lazy_object_proxy.Proxy(lambda: 1)
    two = lazy_object_proxy.Proxy(lambda: 2)

    value |= 2
    assert value == 1 | 2

    if lazy_object_proxy.kind != 'simple':
        assert type(value) == lazy_object_proxy.Proxy

    value |= two
    assert value == 1 | 2 | 2

    if lazy_object_proxy.kind != 'simple':
        assert type(value) == lazy_object_proxy.Proxy


def test_neg(lazy_object_proxy):
    value = lazy_object_proxy.Proxy(lambda: 1)

    assert -value == -1


def test_pos(lazy_object_proxy):
    value = lazy_object_proxy.Proxy(lambda: 1)

    assert +value == 1


def test_abs(lazy_object_proxy):
    value = lazy_object_proxy.Proxy(lambda: -1)

    assert abs(value) == 1


def test_invert(lazy_object_proxy):
    value = lazy_object_proxy.Proxy(lambda: 1)

    assert ~value == ~1


def test_oct(lazy_object_proxy):
    value = lazy_object_proxy.Proxy(lambda: 20)

    assert oct(value) == oct(20)


def test_hex(lazy_object_proxy):
    value = lazy_object_proxy.Proxy(lambda: 20)

    assert hex(value) == hex(20)


def test_index(lazy_object_proxy):
    class Class(object):
        def __index__(self):
            return 1

    value = lazy_object_proxy.Proxy(lambda: Class())
    items = [0, 1, 2]

    assert items[value] == items[1]


def test_length(lazy_object_proxy):
    value = lazy_object_proxy.Proxy(lambda: list(range(3)))

    assert len(value) == 3


def test_contains(lazy_object_proxy):
    value = lazy_object_proxy.Proxy(lambda: list(range(3)))

    assert 2 in value
    assert -2 not in value


def test_getitem(lazy_object_proxy):
    value = lazy_object_proxy.Proxy(lambda: list(range(3)))

    assert value[1] == 1


def test_setitem(lazy_object_proxy):
    value = lazy_object_proxy.Proxy(lambda: list(range(3)))
    value[1] = -1

    assert value[1] == -1


def test_delitem(lazy_object_proxy):
    value = lazy_object_proxy.Proxy(lambda: list(range(3)))

    assert len(value) == 3

    del value[1]

    assert len(value) == 2
    assert value[1] == 2


def test_getslice(lazy_object_proxy):
    value = lazy_object_proxy.Proxy(lambda: list(range(5)))

    assert value[1:4] == [1, 2, 3]


def test_setslice(lazy_object_proxy):
    value = lazy_object_proxy.Proxy(lambda: list(range(5)))

    value[1:4] = reversed(value[1:4])

    assert value[1:4] == [3, 2, 1]


def test_delslice(lazy_object_proxy):
    value = lazy_object_proxy.Proxy(lambda: list(range(5)))

    del value[1:4]

    assert len(value) == 2
    assert value == [0, 4]


def test_dict_length(lazy_object_proxy):
    value = lazy_object_proxy.Proxy(lambda: dict.fromkeys(range(3), False))

    assert len(value) == 3


def test_dict_contains(lazy_object_proxy):
    value = lazy_object_proxy.Proxy(lambda: dict.fromkeys(range(3), False))

    assert 2 in value
    assert -2 not in value


def test_dict_getitem(lazy_object_proxy):
    value = lazy_object_proxy.Proxy(lambda: dict.fromkeys(range(3), False))

    assert value[1] is False


def test_dict_setitem(lazy_object_proxy):
    value = lazy_object_proxy.Proxy(lambda: dict.fromkeys(range(3), False))
    value[1] = True

    assert value[1] is True


def test_dict_delitem(lazy_object_proxy):
    value = lazy_object_proxy.Proxy(lambda: dict.fromkeys(range(3), False))

    assert len(value) == 3

    del value[1]

    assert len(value) == 2


def test_str(lazy_object_proxy):
    value = lazy_object_proxy.Proxy(lambda: 10)

    assert str(value) == str(10)

    value = lazy_object_proxy.Proxy(lambda: (10,))

    assert str(value) == str((10,))

    value = lazy_object_proxy.Proxy(lambda: [10])

    assert str(value) == str([10])

    value = lazy_object_proxy.Proxy(lambda: {10: 10})

    assert str(value) == str({10: 10})


def test_repr(lazy_object_proxy):
    class Foobar:
        pass

    value = lazy_object_proxy.Proxy(lambda: Foobar())
    str(value)
    representation = repr(value)
    print(representation)
    assert 'Proxy at' in representation
    assert 'lambda' in representation
    assert 'Foobar' in representation


def test_repr_doesnt_consume(lazy_object_proxy):
    consumed = []
    value = lazy_object_proxy.Proxy(lambda: consumed.append(1))
    print(repr(value))
    assert not consumed


def test_derived_new(lazy_object_proxy):
    class DerivedObjectProxy(lazy_object_proxy.Proxy):
        def __new__(cls, wrapped):
            instance = super(DerivedObjectProxy, cls).__new__(cls)
            instance.__init__(wrapped)
            return instance

        def __init__(self, wrapped):
            super(DerivedObjectProxy, self).__init__(wrapped)

    def function():
        return 123

    obj = DerivedObjectProxy(lambda: function)
    assert obj() == 123


def test_setup_class_attributes(lazy_object_proxy):
    def function():
        pass

    class DerivedObjectProxy(lazy_object_proxy.Proxy):
        pass

    obj = DerivedObjectProxy(lambda: function)

    DerivedObjectProxy.ATTRIBUTE = 1

    assert obj.ATTRIBUTE == 1
    assert not hasattr(function, 'ATTRIBUTE')

    del DerivedObjectProxy.ATTRIBUTE

    assert not hasattr(DerivedObjectProxy, 'ATTRIBUTE')
    assert not hasattr(obj, 'ATTRIBUTE')
    assert not hasattr(function, 'ATTRIBUTE')


def test_override_class_attributes(lazy_object_proxy):
    def function():
        pass

    class DerivedObjectProxy(lazy_object_proxy.Proxy):
        ATTRIBUTE = 1

    obj = DerivedObjectProxy(lambda: function)

    assert DerivedObjectProxy.ATTRIBUTE == 1
    assert obj.ATTRIBUTE == 1

    obj.ATTRIBUTE = 2

    assert DerivedObjectProxy.ATTRIBUTE == 1

    assert obj.ATTRIBUTE == 2
    assert not hasattr(function, 'ATTRIBUTE')

    del DerivedObjectProxy.ATTRIBUTE

    assert not hasattr(DerivedObjectProxy, 'ATTRIBUTE')
    assert obj.ATTRIBUTE == 2
    assert not hasattr(function, 'ATTRIBUTE')


def test_attr_functions(lazy_object_proxy):
    def function():
        pass

    proxy = lazy_object_proxy.Proxy(lambda: function)

    assert hasattr(proxy, '__getattr__')
    assert hasattr(proxy, '__setattr__')
    assert hasattr(proxy, '__delattr__')


def test_override_getattr(lazy_object_proxy):
    def function():
        pass

    accessed = []

    class DerivedObjectProxy(lazy_object_proxy.Proxy):
        def __getattr__(self, name):
            accessed.append(name)
            try:
                __getattr__ = super(DerivedObjectProxy, self).__getattr__
            except AttributeError as e:
                raise RuntimeError(str(e))
            return __getattr__(name)

    function.attribute = 1

    proxy = DerivedObjectProxy(lambda: function)

    assert proxy.attribute == 1

    assert 'attribute' in accessed


skipcallable = pytest.mark.xfail(
    reason="Don't know how to make this work. This tests the existence of the __call__ method.")


@skipcallable
def test_proxy_hasattr_call(lazy_object_proxy):
    proxy = lazy_object_proxy.Proxy(lambda: None)

    assert not hasattr(proxy, '__call__')


@skipcallable
def test_proxy_getattr_call(lazy_object_proxy):
    proxy = lazy_object_proxy.Proxy(lambda: None)

    assert getattr(proxy, '__call__', None) is None


@skipcallable
def test_proxy_is_callable(lazy_object_proxy):
    proxy = lazy_object_proxy.Proxy(lambda: None)

    assert not callable(proxy)


def test_callable_proxy_hasattr_call(lazy_object_proxy):
    proxy = lazy_object_proxy.Proxy(lambda: None)

    assert hasattr(proxy, '__call__')


@skipcallable
def test_callable_proxy_getattr_call(lazy_object_proxy):
    proxy = lazy_object_proxy.Proxy(lambda: None)

    assert getattr(proxy, '__call__', None) is None


def test_callable_proxy_is_callable(lazy_object_proxy):
    proxy = lazy_object_proxy.Proxy(lambda: None)

    assert callable(proxy)


def test_class_bytes(lazy_object_proxy):
    if PY3:
        class Class(object):
            def __bytes__(self):
                return b'BYTES'

        instance = Class()

        proxy = lazy_object_proxy.Proxy(lambda: instance)

        assert bytes(instance) == bytes(proxy)


def test_str_format(lazy_object_proxy):
    instance = 'abcd'

    proxy = lazy_object_proxy.Proxy(lambda: instance)

    assert format(instance, ''), format(proxy == '')


def test_list_reversed(lazy_object_proxy):
    instance = [1, 2]

    proxy = lazy_object_proxy.Proxy(lambda: instance)

    assert list(reversed(instance)) == list(reversed(proxy))


def test_decimal_complex(lazy_object_proxy):
    import decimal

    instance = decimal.Decimal(123)

    proxy = lazy_object_proxy.Proxy(lambda: instance)

    assert complex(instance) == complex(proxy)


def test_fractions_round(lazy_object_proxy):
    import fractions

    instance = fractions.Fraction('1/2')

    proxy = lazy_object_proxy.Proxy(lambda: instance)

    assert round(instance) == round(proxy)


def test_readonly(lazy_object_proxy):
    class Foo(object):
        if PY2:
            @property
            def __qualname__(self):
                return 'object'

    proxy = lazy_object_proxy.Proxy(lambda: Foo() if PY2 else object)
    assert proxy.__qualname__ == 'object'


def test_del_wrapped(lazy_object_proxy):
    foo = object()
    called = []

    def make_foo():
        called.append(1)
        return foo

    proxy = lazy_object_proxy.Proxy(make_foo)
    str(proxy)
    assert called == [1]
    assert proxy.__wrapped__ is foo
    # print(type(proxy), hasattr(type(proxy), '__wrapped__'))
    del proxy.__wrapped__
    str(proxy)
    assert called == [1, 1]


def test_raise_attribute_error(lazy_object_proxy):
    def foo():
        raise AttributeError("boom!")

    proxy = lazy_object_proxy.Proxy(foo)
    pytest.raises(AttributeError, str, proxy)
    pytest.raises(AttributeError, lambda: proxy.__wrapped__)
    assert proxy.__factory__ is foo


def test_patching_the_factory(lazy_object_proxy):
    def foo():
        raise AttributeError("boom!")

    proxy = lazy_object_proxy.Proxy(foo)
    pytest.raises(AttributeError, lambda: proxy.__wrapped__)
    assert proxy.__factory__ is foo

    proxy.__factory__ = lambda: foo
    pytest.raises(AttributeError, proxy)
    assert proxy.__wrapped__ is foo


def test_deleting_the_factory(lazy_object_proxy):
    proxy = lazy_object_proxy.Proxy(None)
    assert proxy.__factory__ is None
    proxy.__factory__ = None
    assert proxy.__factory__ is None

    pytest.raises(TypeError, str, proxy)
    del proxy.__factory__
    pytest.raises(ValueError, str, proxy)


def test_patching_the_factory_with_none(lazy_object_proxy):
    proxy = lazy_object_proxy.Proxy(None)
    assert proxy.__factory__ is None
    proxy.__factory__ = None
    assert proxy.__factory__ is None
    proxy.__factory__ = None
    assert proxy.__factory__ is None

    def foo():
        return 1

    proxy.__factory__ = foo
    assert proxy.__factory__ is foo
    assert proxy.__wrapped__ == 1
    assert str(proxy) == '1'


def test_new(lazy_object_proxy):
    a = lazy_object_proxy.Proxy.__new__(lazy_object_proxy.Proxy)
    b = lazy_object_proxy.Proxy.__new__(lazy_object_proxy.Proxy)
    # NOW KISS
    pytest.raises(ValueError, lambda: a + b)
    # no segfault, yay
    pytest.raises(ValueError, lambda: a.__wrapped__)


def test_set_wrapped_via_new(lazy_object_proxy):
    obj = lazy_object_proxy.Proxy.__new__(lazy_object_proxy.Proxy)
    obj.__wrapped__ = 1
    assert str(obj) == '1'
    assert obj + 1 == 2


def test_set_wrapped_regular(lazy_object_proxy):
    obj = lazy_object_proxy.Proxy(None)
    obj.__wrapped__ = 1
    assert str(obj) == '1'
    assert obj + 1 == 2


@pytest.fixture(params=["pickle", "cPickle"])
def pickler(request):
    return pytest.importorskip(request.param)


@pytest.mark.parametrize("obj", [
    1,
    1.2,
    "a",
    ["b", "c"],
    {"d": "e"},
    date(2015, 5, 1),
    datetime(2015, 5, 1),
    Decimal("1.2")
])
@pytest.mark.parametrize("level", range(pickle.HIGHEST_PROTOCOL + 1))
def test_pickling(lazy_object_proxy, obj, pickler, level):
    proxy = lazy_object_proxy.Proxy(lambda: obj)
    dump = pickler.dumps(proxy, protocol=level)
    result = pickler.loads(dump)
    assert obj == result


@pytest.mark.parametrize("level", range(pickle.HIGHEST_PROTOCOL + 1))
def test_pickling_exception(lazy_object_proxy, pickler, level):
    class BadStuff(Exception):
        pass

    def trouble_maker():
        raise BadStuff("foo")

    proxy = lazy_object_proxy.Proxy(trouble_maker)
    pytest.raises(BadStuff, pickler.dumps, proxy, protocol=level)


@pytest.mark.skipif(platform.python_implementation() != 'CPython',
                    reason="Interpreter doesn't have reference counting")
def test_garbage_collection(lazy_object_proxy):
    leaky = lambda: "foobar"  # noqa
    proxy = lazy_object_proxy.Proxy(leaky)
    leaky.leak = proxy
    ref = weakref.ref(leaky)
    assert proxy == "foobar"
    del leaky
    del proxy
    gc.collect()
    assert ref() is None


@pytest.mark.skipif(platform.python_implementation() != 'CPython',
                    reason="Interpreter doesn't have reference counting")
def test_garbage_collection_count(lazy_object_proxy):
    obj = object()
    count = sys.getrefcount(obj)
    for _ in range(100):
        str(lazy_object_proxy.Proxy(lambda: obj))
    assert count == sys.getrefcount(obj)


@pytest.mark.parametrize("name", ["slots", "cext", "simple", "django", "objproxies"])
def test_perf(benchmark, name):
    implementation = load_implementation(name)
    obj = "foobar"
    proxied = implementation.Proxy(lambda: obj)
    assert benchmark(partial(str, proxied)) == obj


empty = object()


@pytest.fixture(scope="module", params=["SimpleProxy", "LocalsSimpleProxy", "CachedPropertyProxy",
                                        "LocalsCachedPropertyProxy"])
def prototype(request):
    from lazy_object_proxy.simple import cached_property
    name = request.param

    if name == "SimpleProxy":
        class SimpleProxy(object):
            def __init__(self, factory):
                self.factory = factory
                self.object = empty

            def __str__(self):
                if self.object is empty:
                    self.object = self.factory()
                return str(self.object)

        return SimpleProxy
    elif name == "CachedPropertyProxy":
        class CachedPropertyProxy(object):
            def __init__(self, factory):
                self.factory = factory

            @cached_property
            def object(self):
                return self.factory()

            def __str__(self):
                return str(self.object)

        return CachedPropertyProxy
    elif name == "LocalsSimpleProxy":
        class LocalsSimpleProxy(object):
            def __init__(self, factory):
                self.factory = factory
                self.object = empty

            def __str__(self, func=str):
                if self.object is empty:
                    self.object = self.factory()
                return func(self.object)

        return LocalsSimpleProxy
    elif name == "LocalsCachedPropertyProxy":
        class LocalsCachedPropertyProxy(object):
            def __init__(self, factory):
                self.factory = factory

            @cached_property
            def object(self):
                return self.factory()

            def __str__(self, func=str):
                return func(self.object)

        return LocalsCachedPropertyProxy


@pytest.mark.benchmark(group="prototypes")
def test_proto(benchmark, prototype):
    obj = "foobar"
    proxied = prototype(lambda: obj)
    assert benchmark(partial(str, proxied)) == obj


def test_subclassing_with_local_attr(lazy_object_proxy):
    class Foo:
        pass
    called = []

    class LazyProxy(lazy_object_proxy.Proxy):
        name = None

        def __init__(self, func, **lazy_attr):
            super(LazyProxy, self).__init__(func)
            for attr, val in lazy_attr.items():
                setattr(self, attr, val)

    proxy = LazyProxy(lambda: called.append(1) or Foo(), name='bar')
    assert proxy.name == 'bar'
    assert not called


def test_subclassing_dynamic_with_local_attr(lazy_object_proxy):
    if lazy_object_proxy.kind == 'cext':
        pytest.skip("Not possible.")

    class Foo:
        pass

    called = []

    class LazyProxy(lazy_object_proxy.Proxy):
        def __init__(self, func, **lazy_attr):
            super(LazyProxy, self).__init__(func)
            for attr, val in lazy_attr.items():
                object.__setattr__(self, attr, val)

    proxy = LazyProxy(lambda: called.append(1) or Foo(), name='bar')
    assert proxy.name == 'bar'
    assert not called
