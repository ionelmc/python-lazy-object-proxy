from __future__ import print_function

import unittest
import imp
import operator
import sys

is_pypy = '__pypy__' in sys.builtin_module_names

import wrapt

from wrapt import six

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
six.exec_(OBJECTS_CODE, objects.__dict__, objects.__dict__)

class TestAttributeAccess(unittest.TestCase):

    def test_attributes(self):
        def function1(*args, **kwargs):
            return args, kwargs
        function2 = wrapt.ObjectProxy(function1)

        self.assertEqual(function2._self_wrapped, function1)

    def test_get_wrapped(self):
        def function1(*args, **kwargs):
            return args, kwargs
        function2 = wrapt.ObjectProxy(function1)

        self.assertEqual(function2.__wrapped__, function1)

        function3 = wrapt.ObjectProxy(function2)

        self.assertEqual(function3.__wrapped__, function1)

    def test_set_wrapped(self):
        def function1(*args, **kwargs):
            return args, kwargs
        function2 = wrapt.ObjectProxy(function1)

        self.assertEqual(function2.__wrapped__, function1)

        function2.__wrapped__ = None

        self.assertEqual(function2.__wrapped__, None)

class TestNamingObjectProxy(unittest.TestCase):

    def test_class_object_name(self):
        # Test preservation of class __name__ attribute.

        target = objects.Target
        wrapper = wrapt.ObjectProxy(target)

        self.assertEqual(wrapper.__name__, target.__name__)

    def test_class_object_qualname(self):
        # Test preservation of class __qualname__ attribute.

        target = objects.Target
        wrapper = wrapt.ObjectProxy(target)

        try:
            __qualname__ = target.__qualname__
        except AttributeError:
            pass
        else:
            self.assertEqual(wrapper.__qualname__, __qualname__)

    def test_class_module_name(self):
       # Test preservation of class __module__ attribute.

        target = objects.Target
        wrapper = wrapt.ObjectProxy(target)

        self.assertEqual(wrapper.__module__, target.__module__)

    def test_class_doc_string(self):
        # Test preservation of class __doc__ attribute.

        target = objects.Target
        wrapper = wrapt.ObjectProxy(target)

        self.assertEqual(wrapper.__doc__, target.__doc__)

    def test_instance_module_name(self):
       # Test preservation of instance __module__ attribute.

        target = objects.Target()
        wrapper = wrapt.ObjectProxy(target)

        self.assertEqual(wrapper.__module__, target.__module__)

    def test_instance_doc_string(self):
        # Test preservation of instance __doc__ attribute.

        target = objects.Target()
        wrapper = wrapt.ObjectProxy(target)

        self.assertEqual(wrapper.__doc__, target.__doc__)

    def test_function_object_name(self):
        # Test preservation of function __name__ attribute.

        target = objects.target
        wrapper = wrapt.ObjectProxy(target)

        self.assertEqual(wrapper.__name__, target.__name__)

    def test_function_object_qualname(self):
        # Test preservation of function __qualname__ attribute.

        target = objects.target
        wrapper = wrapt.ObjectProxy(target)

        try:
            __qualname__ = target.__qualname__
        except AttributeError:
            pass
        else:
            self.assertEqual(wrapper.__qualname__, __qualname__)

    def test_function_module_name(self):
       # Test preservation of function __module__ attribute.

        target = objects.target
        wrapper = wrapt.ObjectProxy(target)

        self.assertEqual(wrapper.__module__, target.__module__)

    def test_function_doc_string(self):
        # Test preservation of function __doc__ attribute.

        target = objects.target
        wrapper = wrapt.ObjectProxy(target)

        self.assertEqual(wrapper.__doc__, target.__doc__)

class TestTypeObjectProxy(unittest.TestCase):

    def test_class_of_class(self):
        # Test preservation of class __class__ attribute.

        target = objects.Target
        wrapper = wrapt.ObjectProxy(target)

        self.assertEqual(wrapper.__class__, target.__class__)

        self.assertTrue(isinstance(wrapper, type(target)))

    def test_class_of_instance(self):
        # Test preservation of instance __class__ attribute.

        target = objects.Target()
        wrapper = wrapt.ObjectProxy(target)

        self.assertEqual(wrapper.__class__, target.__class__)

        self.assertTrue(isinstance(wrapper, objects.Target))
        self.assertTrue(isinstance(wrapper, objects.TargetBaseClass))

    def test_class_of_function(self):
        # Test preservation of function __class__ attribute.

        target = objects.target
        wrapper = wrapt.ObjectProxy(target)

        self.assertEqual(wrapper.__class__, target.__class__)

        self.assertTrue(isinstance(wrapper, type(target)))

class TestDirObjectProxy(unittest.TestCase):

    def test_dir_of_class(self):
        # Test preservation of class __dir__ attribute.

        target = objects.Target
        wrapper = wrapt.ObjectProxy(target)

        self.assertEqual(dir(wrapper), dir(target))

    def test_vars_of_class(self):
        # Test preservation of class __dir__ attribute.

        target = objects.Target
        wrapper = wrapt.ObjectProxy(target)

        self.assertEqual(vars(wrapper), vars(target))

    def test_dir_of_instance(self):
        # Test preservation of instance __dir__ attribute.

        target = objects.Target()
        wrapper = wrapt.ObjectProxy(target)

        self.assertEqual(dir(wrapper), dir(target))

    def test_vars_of_instance(self):
        # Test preservation of instance __dir__ attribute.

        target = objects.Target()
        wrapper = wrapt.ObjectProxy(target)

        self.assertEqual(vars(wrapper), vars(target))

    def test_dir_of_function(self):
        # Test preservation of function __dir__ attribute.

        target = objects.target
        wrapper = wrapt.ObjectProxy(target)

        self.assertEqual(dir(wrapper), dir(target))

    def test_vars_of_function(self):
        # Test preservation of function __dir__ attribute.

        target = objects.target
        wrapper = wrapt.ObjectProxy(target)

        self.assertEqual(vars(wrapper), vars(target))

class TestCallingObject(unittest.TestCase):

    def test_function_no_args(self):
        _args = ()
        _kwargs = {}

        def function(*args, **kwargs):
            return args, kwargs

        wrapper = wrapt.ObjectProxy(function)

        result = wrapper()

        self.assertEqual(result, (_args, _kwargs))

    def test_function_args(self):
        _args = (1, 2)
        _kwargs = {}

        def function(*args, **kwargs):
            return args, kwargs

        wrapper = wrapt.ObjectProxy(function)

        result = wrapper(*_args)

        self.assertEqual(result, (_args, _kwargs))

    def test_function_kwargs(self):
        _args = ()
        _kwargs = { "one": 1, "two": 2 }

        def function(*args, **kwargs):
            return args, kwargs

        wrapper = wrapt.ObjectProxy(function)

        result = wrapper(**_kwargs)

        self.assertEqual(result, (_args, _kwargs))

    def test_function_args_plus_kwargs(self):
        _args = (1, 2)
        _kwargs = { "one": 1, "two": 2 }

        def function(*args, **kwargs):
            return args, kwargs

        wrapper = wrapt.ObjectProxy(function)

        result = wrapper(*_args, **_kwargs)

        self.assertEqual(result, (_args, _kwargs))

    def test_instancemethod_no_args(self):
        _args = ()
        _kwargs = {}

        class Class(object):
            def function(self, *args, **kwargs):
                return args, kwargs

        wrapper = wrapt.ObjectProxy(Class().function)

        result = wrapper()

        self.assertEqual(result, (_args, _kwargs))

    def test_instancemethod_args(self):
        _args = (1, 2)
        _kwargs = {}

        class Class(object):
            def function(self, *args, **kwargs):
                return args, kwargs

        wrapper = wrapt.ObjectProxy(Class().function)

        result = wrapper(*_args)

        self.assertEqual(result, (_args, _kwargs))

    def test_instancemethod_kwargs(self):
        _args = ()
        _kwargs = { "one": 1, "two": 2 }

        class Class(object):
            def function(self, *args, **kwargs):
                return args, kwargs

        wrapper = wrapt.ObjectProxy(Class().function)

        result = wrapper(**_kwargs)

        self.assertEqual(result, (_args, _kwargs))

    def test_instancemethod_args_plus_kwargs(self):
        _args = (1, 2)
        _kwargs = { "one": 1, "two": 2 }

        class Class(object):
            def function(self, *args, **kwargs):
                return args, kwargs

        wrapper = wrapt.ObjectProxy(Class().function)

        result = wrapper(*_args, **_kwargs)

        self.assertEqual(result, (_args, _kwargs))

    def test_instancemethod_via_class_no_args(self):
        _args = ()
        _kwargs = {}

        class Class(object):
            def function(self, *args, **kwargs):
                return args, kwargs

        wrapper = wrapt.ObjectProxy(Class.function)

        result = wrapper(Class())

        self.assertEqual(result, (_args, _kwargs))

    def test_instancemethod_via_class_args(self):
        _args = (1, 2)
        _kwargs = {}

        class Class(object):
            def function(self, *args, **kwargs):
                return args, kwargs

        wrapper = wrapt.ObjectProxy(Class.function)

        result = wrapper(Class(), *_args)

        self.assertEqual(result, (_args, _kwargs))

    def test_instancemethod_via_class_kwargs(self):
        _args = ()
        _kwargs = { "one": 1, "two": 2 }

        class Class(object):
            def function(self, *args, **kwargs):
                return args, kwargs

        wrapper = wrapt.ObjectProxy(Class.function)

        result = wrapper(Class(), **_kwargs)

        self.assertEqual(result, (_args, _kwargs))

    def test_instancemethod_via_class_args_plus_kwargs(self):
        _args = (1, 2)
        _kwargs = { "one": 1, "two": 2 }

        class Class(object):
            def function(self, *args, **kwargs):
                return args, kwargs

        wrapper = wrapt.ObjectProxy(Class.function)

        result = wrapper(Class(), *_args, **_kwargs)

        self.assertEqual(result, (_args, _kwargs))

    def test_classmethod_no_args(self):
        _args = ()
        _kwargs = {}

        class Class(object):
            @classmethod
            def function(cls, *args, **kwargs):
                return args, kwargs

        wrapper = wrapt.ObjectProxy(Class().function)

        result = wrapper()

        self.assertEqual(result, (_args, _kwargs))

    def test_classmethod_args(self):
        _args = (1, 2)
        _kwargs = {}

        class Class(object):
            @classmethod
            def function(cls, *args, **kwargs):
                return args, kwargs

        wrapper = wrapt.ObjectProxy(Class().function)

        result = wrapper(*_args)

        self.assertEqual(result, (_args, _kwargs))

    def test_classmethod_kwargs(self):
        _args = ()
        _kwargs = { "one": 1, "two": 2 }

        class Class(object):
            @classmethod
            def function(cls, *args, **kwargs):
                return args, kwargs

        wrapper = wrapt.ObjectProxy(Class().function)

        result = wrapper(**_kwargs)

        self.assertEqual(result, (_args, _kwargs))

    def test_classmethod_args_plus_kwargs(self):
        _args = (1, 2)
        _kwargs = { "one": 1, "two": 2 }

        class Class(object):
            @classmethod
            def function(cls, *args, **kwargs):
                return args, kwargs

        wrapper = wrapt.ObjectProxy(Class().function)

        result = wrapper(*_args, **_kwargs)

        self.assertEqual(result, (_args, _kwargs))

    def test_classmethod_via_class_no_args(self):
        _args = ()
        _kwargs = {}

        class Class(object):
            @classmethod
            def function(cls, *args, **kwargs):
                return args, kwargs

        wrapper = wrapt.ObjectProxy(Class.function)

        result = wrapper()

        self.assertEqual(result, (_args, _kwargs))

    def test_classmethod_via_class_args(self):
        _args = (1, 2)
        _kwargs = {}

        class Class(object):
            @classmethod
            def function(cls, *args, **kwargs):
                return args, kwargs

        wrapper = wrapt.ObjectProxy(Class.function)

        result = wrapper(*_args)

        self.assertEqual(result, (_args, _kwargs))

    def test_classmethod_via_class_kwargs(self):
        _args = ()
        _kwargs = { "one": 1, "two": 2 }

        class Class(object):
            @classmethod
            def function(cls, *args, **kwargs):
                return args, kwargs

        wrapper = wrapt.ObjectProxy(Class.function)

        result = wrapper(**_kwargs)

        self.assertEqual(result, (_args, _kwargs))

    def test_classmethod_via_class_args_plus_kwargs(self):
        _args = (1, 2)
        _kwargs = { "one": 1, "two": 2 }

        class Class(object):
            @classmethod
            def function(cls, *args, **kwargs):
                return args, kwargs

        wrapper = wrapt.ObjectProxy(Class.function)

        result = wrapper(*_args, **_kwargs)

        self.assertEqual(result, (_args, _kwargs))

    def test_staticmethod_no_args(self):
        _args = ()
        _kwargs = {}

        class Class(object):
            @staticmethod
            def function(*args, **kwargs):
                return args, kwargs

        wrapper = wrapt.ObjectProxy(Class().function)

        result = wrapper()

        self.assertEqual(result, (_args, _kwargs))

    def test_staticmethod_args(self):
        _args = (1, 2)
        _kwargs = {}

        class Class(object):
            @staticmethod
            def function(*args, **kwargs):
                return args, kwargs

        wrapper = wrapt.ObjectProxy(Class().function)

        result = wrapper(*_args)

        self.assertEqual(result, (_args, _kwargs))

    def test_staticmethod_kwargs(self):
        _args = ()
        _kwargs = { "one": 1, "two": 2 }

        class Class(object):
            @staticmethod
            def function(*args, **kwargs):
                return args, kwargs

        wrapper = wrapt.ObjectProxy(Class().function)

        result = wrapper(**_kwargs)

        self.assertEqual(result, (_args, _kwargs))

    def test_staticmethod_args_plus_kwargs(self):
        _args = (1, 2)
        _kwargs = { "one": 1, "two": 2 }

        class Class(object):
            @staticmethod
            def function(*args, **kwargs):
                return args, kwargs

        wrapper = wrapt.ObjectProxy(Class().function)

        result = wrapper(*_args, **_kwargs)

        self.assertEqual(result, (_args, _kwargs))

    def test_staticmethod_via_class_no_args(self):
        _args = ()
        _kwargs = {}

        class Class(object):
            @staticmethod
            def function(*args, **kwargs):
                return args, kwargs

        wrapper = wrapt.ObjectProxy(Class.function)

        result = wrapper()

        self.assertEqual(result, (_args, _kwargs))

    def test_staticmethod_via_class_args(self):
        _args = (1, 2)
        _kwargs = {}

        class Class(object):
            @staticmethod
            def function(*args, **kwargs):
                return args, kwargs

        wrapper = wrapt.ObjectProxy(Class.function)

        result = wrapper(*_args)

        self.assertEqual(result, (_args, _kwargs))

    def test_staticmethod_via_class_kwargs(self):
        _args = ()
        _kwargs = { "one": 1, "two": 2 }

        class Class(object):
            @staticmethod
            def function(*args, **kwargs):
                return args, kwargs

        wrapper = wrapt.ObjectProxy(Class.function)

        result = wrapper(**_kwargs)

        self.assertEqual(result, (_args, _kwargs))

    def test_staticmethod_via_class_args_plus_kwargs(self):
        _args = (1, 2)
        _kwargs = { "one": 1, "two": 2 }

        class Class(object):
            @staticmethod
            def function(*args, **kwargs):
                return args, kwargs

        wrapper = wrapt.ObjectProxy(Class.function)

        result = wrapper(*_args, **_kwargs)

        self.assertEqual(result, (_args, _kwargs))

class TestIterObjectProxy(unittest.TestCase):

    def test_iteration(self):
        items = [1, 2]

        wrapper = wrapt.ObjectProxy(items)

        result = [x for x in wrapper]

        self.assertEqual(result, items)

class TestContextManagerObjectProxy(unittest.TestCase):

    def test_context_manager(self):
        class Class(object):
            def __enter__(self):
                return self
            def __exit__(*args, **kwargs):
                return

        instance = Class()

        wrapper = wrapt.ObjectProxy(instance)

        with wrapper:
            pass

class TestEqualityObjectProxy(unittest.TestCase):

    def test_object_hash(self):
        def function1(*args, **kwargs):
            return args, kwargs
        function2 = wrapt.ObjectProxy(function1)

        self.assertEqual(hash(function2), hash(function1))

    def test_mapping_key(self):
        def function1(*args, **kwargs):
            return args, kwargs
        function2 = wrapt.ObjectProxy(function1)

        table = dict()
        table[function1] = True

        self.assertTrue(table.get(function2))

        table = dict()
        table[function2] = True

        self.assertTrue(table.get(function1))

    def test_comparison(self):
        one = wrapt.ObjectProxy(1)
        two = wrapt.ObjectProxy(2)
        three = wrapt.ObjectProxy(3)

        self.assertTrue(two > 1)
        self.assertTrue(two >= 1)
        self.assertTrue(two < 3)
        self.assertTrue(two <= 3)
        self.assertTrue(two != 1)
        self.assertTrue(two == 2)
        self.assertTrue(two != 3)

        self.assertTrue(2 > one)
        self.assertTrue(2 >= one)
        self.assertTrue(2 < three)
        self.assertTrue(2 <= three)
        self.assertTrue(2 != one)
        self.assertTrue(2 == two)
        self.assertTrue(2 != three)

        self.assertTrue(two > one)
        self.assertTrue(two >= one)
        self.assertTrue(two < three)
        self.assertTrue(two <= three)
        self.assertTrue(two != one)
        self.assertTrue(two == two)
        self.assertTrue(two != three)

class TestAsNumberObjectProxy(unittest.TestCase):

    def test_nonzero(self):
        true = wrapt.ObjectProxy(True)
        false = wrapt.ObjectProxy(False)

        self.assertTrue(true)
        self.assertFalse(false)

        self.assertTrue(bool(true))
        self.assertFalse(bool(false))

        self.assertTrue(not false)
        self.assertFalse(not true)

    def test_int(self):
        one = wrapt.ObjectProxy(1)

        self.assertEqual(int(one), 1)

        if not six.PY3:
            self.assertEqual(long(one), 1)

    def test_float(self):
        one = wrapt.ObjectProxy(1)

        self.assertEqual(float(one), 1.0)

    def test_add(self):
        one = wrapt.ObjectProxy(1)
        two = wrapt.ObjectProxy(2)

        self.assertEqual(one+two, 1+2)
        self.assertEqual(1+two, 1+2)
        self.assertEqual(one+2, 1+2)
        
    def test_sub(self):
        one = wrapt.ObjectProxy(1)
        two = wrapt.ObjectProxy(2)

        self.assertEqual(one-two, 1-2)
        self.assertEqual(1-two, 1-2)
        self.assertEqual(one-2, 1-2)

    def test_mul(self):
        two = wrapt.ObjectProxy(2)
        three = wrapt.ObjectProxy(3)

        self.assertEqual(two*three, 2*3)
        self.assertEqual(2*three, 2*3)
        self.assertEqual(two*3, 2*3)

    def test_div(self):
        # On Python 2 this will pick up div and on Python
        # 3 it will pick up truediv.

        two = wrapt.ObjectProxy(2)
        three = wrapt.ObjectProxy(3)

        self.assertEqual(two/three, 2/3)
        self.assertEqual(2/three, 2/3)
        self.assertEqual(two/3, 2/3)

    def test_mod(self):
        two = wrapt.ObjectProxy(2)
        three = wrapt.ObjectProxy(3)

        self.assertEqual(three//two, 3//2)
        self.assertEqual(3//two, 3//2)
        self.assertEqual(three//2, 3//2)

    def test_mod(self):
        two = wrapt.ObjectProxy(2)
        three = wrapt.ObjectProxy(3)

        self.assertEqual(three%two, 3%2)
        self.assertEqual(3%two, 3%2)
        self.assertEqual(three%2, 3%2)

    def test_divmod(self):
        two = wrapt.ObjectProxy(2)
        three = wrapt.ObjectProxy(3)

        self.assertEqual(divmod(three, two), divmod(3, 2))
        self.assertEqual(divmod(3, two), divmod(3, 2))
        self.assertEqual(divmod(three, 2), divmod(3, 2))

    def test_pow(self):
        two = wrapt.ObjectProxy(2)
        three = wrapt.ObjectProxy(3)

        self.assertEqual(three**two, pow(3, 2))
        self.assertEqual(3**two, pow(3, 2))
        self.assertEqual(three**2, pow(3, 2))

        self.assertEqual(pow(three, two), pow(3, 2))
        self.assertEqual(pow(3, two), pow(3, 2))
        self.assertEqual(pow(three, 2), pow(3, 2))

        # Only PyPy implements __rpow__ for ternary pow().

        if is_pypy:
            self.assertEqual(pow(three, two, 2), pow(3, 2, 2))
            self.assertEqual(pow(3, two, 2), pow(3, 2, 2))

        self.assertEqual(pow(three, 2, 2), pow(3, 2, 2))

    def test_lshift(self):
        two = wrapt.ObjectProxy(2)
        three = wrapt.ObjectProxy(3)

        self.assertEqual(three<<two, 3<<2)
        self.assertEqual(3<<two, 3<<2)
        self.assertEqual(three<<2, 3<<2)

    def test_rshift(self):
        two = wrapt.ObjectProxy(2)
        three = wrapt.ObjectProxy(3)

        self.assertEqual(three>>two, 3>>2)
        self.assertEqual(3>>two, 3>>2)
        self.assertEqual(three>>2, 3>>2)

    def test_and(self):
        two = wrapt.ObjectProxy(2)
        three = wrapt.ObjectProxy(3)

        self.assertEqual(three&two, 3&2)
        self.assertEqual(3&two, 3&2)
        self.assertEqual(three&2, 3&2)

    def test_xor(self):
        two = wrapt.ObjectProxy(2)
        three = wrapt.ObjectProxy(3)

        self.assertEqual(three^two, 3^2)
        self.assertEqual(3^two, 3^2)
        self.assertEqual(three^2, 3^2)

    def test_or(self):
        two = wrapt.ObjectProxy(2)
        three = wrapt.ObjectProxy(3)

        self.assertEqual(three|two, 3|2)
        self.assertEqual(3|two, 3|2)
        self.assertEqual(three|2, 3|2)

    def test_iadd(self):
        value = wrapt.ObjectProxy(1)
        one = wrapt.ObjectProxy(1)

        value += 1
        self.assertEqual(value, 2)

        value += one
        self.assertEqual(value, 3)

    def test_isub(self):
        value = wrapt.ObjectProxy(1)
        one = wrapt.ObjectProxy(1)

        value -= 1
        self.assertEqual(value, 0)

        value -= one
        self.assertEqual(value, -1)

    def test_imul(self):
        value = wrapt.ObjectProxy(2)
        two = wrapt.ObjectProxy(2)

        value *= 2
        self.assertEqual(value, 4)

        value *= two
        self.assertEqual(value, 8)

    def test_idiv(self):
        # On Python 2 this will pick up div and on Python
        # 3 it will pick up truediv.

        value = wrapt.ObjectProxy(2)
        two = wrapt.ObjectProxy(2)

        value /= 2
        self.assertEqual(value, 2/2)

        value /= two
        self.assertEqual(value, 2/2/2)

    def test_ifloordiv(self):
        value = wrapt.ObjectProxy(2)
        two = wrapt.ObjectProxy(2)

        value //= 2
        self.assertEqual(value, 2//2)

        value //= two
        self.assertEqual(value, 2//2//2)

    def test_imod(self):
        value = wrapt.ObjectProxy(10)
        two = wrapt.ObjectProxy(2)

        value %= 2
        self.assertEqual(value, 10%2)

        value %= two
        self.assertEqual(value, 10%2%2)

    def test_ipow(self):
        value = wrapt.ObjectProxy(10)
        two = wrapt.ObjectProxy(2)

        value **= 2
        self.assertEqual(value, 10**2)

        value **= two
        self.assertEqual(value, 10**2**2)

    def test_ilshift(self):
        value = wrapt.ObjectProxy(256)
        two = wrapt.ObjectProxy(2)

        value <<= 2
        self.assertEqual(value, 256<<2)

        value <<= two
        self.assertEqual(value, 256<<2<<2)

    def test_irshift(self):
        value = wrapt.ObjectProxy(2)
        two = wrapt.ObjectProxy(2)

        value >>= 2
        self.assertEqual(value, 2>>2)

        value >>= two
        self.assertEqual(value, 2>>2>>2)

    def test_iand(self):
        value = wrapt.ObjectProxy(1)
        two = wrapt.ObjectProxy(2)

        value &= 2
        self.assertEqual(value, 1&2)

        value &= two
        self.assertEqual(value, 1&2&2)

    def test_ixor(self):
        value = wrapt.ObjectProxy(1)
        two = wrapt.ObjectProxy(2)

        value ^= 2
        self.assertEqual(value, 1^2)

        value ^= two
        self.assertEqual(value, 1^2^2)

    def test_ior(self):
        value = wrapt.ObjectProxy(1)
        two = wrapt.ObjectProxy(2)

        value |= 2
        self.assertEqual(value, 1|2)

        value |= two
        self.assertEqual(value, 1|2|2)

    def test_neg(self):
        value = wrapt.ObjectProxy(1)

        self.assertEqual(-value, -1)

    def test_pos(self):
        value = wrapt.ObjectProxy(1)

        self.assertEqual(+value, 1)

    def test_abs(self):
        value = wrapt.ObjectProxy(-1)

        self.assertEqual(abs(value), 1)

    def test_invert(self):
        value = wrapt.ObjectProxy(1)

        self.assertEqual(~value, ~1)

    def test_oct(self):
        value = wrapt.ObjectProxy(20)

        self.assertEqual(oct(value), oct(20))

    def test_hex(self):
        value = wrapt.ObjectProxy(20)

        self.assertEqual(hex(value), hex(20))

    def test_index(self):
        value = wrapt.ObjectProxy(20)

        # PyPy doesn't implement operator.__index__().

        if not is_pypy:
            self.assertEqual(value.__index__(), operator.__index__(20))

if __name__ == '__main__':
    unittest.main()