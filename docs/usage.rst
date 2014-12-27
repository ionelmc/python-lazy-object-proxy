=====
Usage
=====

The lazy object proxy class is available as ``lazy_object_proxy.Proxy``.

.. code:: pycon

    >>> table = {}
    >>> import lazy_object_proxy
    >>> proxy = lazy_object_proxy.Proxy(lambda: table)
    >>> proxy['key-1'] = 'value-1'
    >>> proxy['key-2'] = 'value-2'

    >>> sorted(proxy.keys())
    ['key-1', 'key-2']
    >>> sorted(table.keys())
    ['key-1', 'key-2']

    >>> isinstance(proxy, dict)
    True

    >>> dir(proxy)
    ['__class__', ...'__contains__', '__delattr__', '__delitem__', ...'__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__iter__', '__le__', '__len__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', ...'__setattr__', '__setitem__', ...'__str__', '__subclasshook__', 'clear', 'copy', 'fromkeys', 'get', ...]


This ability for a proxy to stand in for the original goes as far as
arithmetic operations, rich comparison and hashing.

.. code:: pycon

    >>> value = 1
    >>> proxy = lazy_object_proxy.Proxy(lambda: value)

    >>> proxy + 1
    2

    >>> int(proxy)
    1
    >>> hash(proxy)
    1
    >>> hash(value)
    1

    >>> proxy < 2
    True
    >>> proxy == 0
    False

Do note however, that when wrapping an object proxy around a literal value,
the original value is effectively copied into the proxy object and any
operation which updates the value will only update the value held by the
proxy object.

.. code:: pycon

    >>> value = 1
    >>> proxy = lazy_object_proxy.Proxy(lambda: value)
    >>> type(proxy)
    <... 'Proxy'>

    >>> proxy += 1

    >>> type(proxy)
    <... 'Proxy'>

    >>> print(proxy)
    2
    >>> print(value)
    1

Object wrappers may therefore have limited use in conjunction with literal
values.

Type Comparison
---------------

The type of an instance of the object proxy will be ``ObjectProxy``, or that
of any derived class type if creating a custom object proxy.

.. code:: pycon

    >>> value = 1
    >>> proxy = lazy_object_proxy.Proxy(lambda: value)
    >>> type(proxy)
    <... 'Proxy'>

    >>> class CustomProxy(lazy_object_proxy.Proxy):
    ...     pass

    >>> proxy = CustomProxy(lambda: 1)

    >>> type(proxy)
    <class '...CustomProxy'>

Direct type comparisons in Python are generally frowned upon and allowance
for 'duck typing' preferred. Instead of direct type comparison, the
``isinstance()`` function would therefore be used. Using ``isinstance()``,
comparison of the type of the object proxy will properly evaluate against
the wrapped object.

.. code:: pycon

    >>> isinstance(proxy, int)
    True

This works because the ``__class__`` attribute actually returns the class
type for the wrapped object.

.. code:: pycon

    >>> proxy.__class__
    <... 'int'>

Note that ``isinstance()`` will still also succeed if comparing to the
``ObjectProxy`` type. It is therefore still possible to use ``isinstance()``
to determine if an object is an object proxy.

.. code:: pycon

    >>> isinstance(proxy, lazy_object_proxy.Proxy)
    True

    >>> class CustomProxy(lazy_object_proxy.Proxy):
    ...     pass

    >>> proxy = CustomProxy(lambda: 1)

    >>> isinstance(proxy, lazy_object_proxy.Proxy)
    True
    >>> isinstance(proxy, CustomProxy)
    True


Custom Object Proxies
---------------------

A custom proxy is where one creates a derived object proxy and overrides
some specific behaviour of the proxy.

.. code:: pycon

    >>> def function():
    ...     print(('executing', function.__name__))

    >>> class CallableWrapper(lazy_object_proxy.Proxy):
    ...     def __call__(self, *args, **kwargs):
    ...         print(('entering', self.__wrapped__.__name__))
    ...         try:
    ...             return self.__wrapped__(*args, **kwargs)
    ...         finally:
    ...             print(('exiting', self.__wrapped__.__name__))

    >>> proxy = CallableWrapper(lambda: function)

    >>> proxy()
    ('entering', 'function')
    ('executing', 'function')
    ('exiting', 'function')

Any method of the original wrapped object can be overridden, including
special Python methods such as ``__call__()``. If it is necessary to change
what happens when a specific attribute of the wrapped object is accessed,
then properties can be used.

If it is necessary to access the original wrapped object from within an
overridden method or property, then ``self.__wrapped__`` is used.

Proxy Object Attributes
-----------------------

When an attempt is made to access an attribute from the proxy, the same
named attribute would in normal circumstances be accessed from the wrapped
object. When updating an attributes value, or deleting the attribute, that
change will also be reflected in the wrapped object.

.. code:: pycon

    >>> proxy = CallableWrapper(lambda: function)

    >>> hasattr(function, 'attribute')
    False
    >>> hasattr(proxy, 'attribute')
    False

    >>> proxy.attribute = 1

    >>> hasattr(function, 'attribute')
    True
    >>> hasattr(proxy, 'attribute')
    True

    >>> function.attribute
    1
    >>> proxy.attribute
    1

If an attribute was updated on the wrapped object directly, that change is
still reflected in what is available via the proxy.

.. code:: pycon

    >>> function.attribute = 2

    >>> function.attribute
    2
    >>> proxy.attribute
    2

Custom attributes can be specified as a class attribute, with
that then being overridden if necessary, with a specific value in the
``__init__()`` method of the class.

.. code:: pycon

    >>> class CustomProxy(lazy_object_proxy.Proxy):
    ...     attribute = None
    ...     def __init__(self, wrapped):
    ...         super(CustomProxy, self).__init__(wrapped)
    ...         self.attribute = 1

    >>> proxy = CustomProxy(lambda: 1)
    >>> proxy.attribute
    1
    >>> proxy.attribute = 2
    >>> proxy.attribute
    2
    >>> del proxy.attribute
    >>> print(proxy.attribute)
    None

Just be aware that although the attribute can be deleted from the instance
of the custom proxy, lookup will then fallback to using the class attribute.
