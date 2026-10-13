=====
Usage
=====

To use lazy-object-proxy in a project::

    import lazy_object_proxy

Explicit evaluation
===================

Access ``proxy.__wrapped__`` to evaluate the factory and obtain its result
without invoking another operation on that result. The returned object is the
wrapped object itself, not a copy. ``proxy.__resolved__`` lets you check whether
it is already available without evaluating the factory:

.. doctest::

    >>> from lazy_object_proxy import Proxy
    >>> calls = []
    >>> def make_value():
    ...     calls.append('called')
    ...     return {'answer': 42}
    >>> proxy = Proxy(make_value)
    >>> proxy.__resolved__
    False
    >>> calls
    []
    >>> value = proxy.__wrapped__
    >>> value
    {'answer': 42}
    >>> proxy.__resolved__
    True
    >>> proxy.__wrapped__ is value
    True
    >>> calls
    ['called']

The factory's successful result is cached for subsequent access. Evaluation runs
your factory code, which may have side effects or raise exceptions. It is not a
conversion in place: the proxy remains a separate object.

Identity and ``None``
=====================

Python's ``is`` operator compares object identity and cannot be forwarded by a
proxy. In particular, ``proxy is None`` is always false, even if the factory
would return ``None``, and it does not evaluate the factory. Unwrap first when
you need to check the identity of the result:

.. doctest::

    >>> optional = Proxy(lambda: None)
    >>> optional is None
    False
    >>> optional.__resolved__
    False
    >>> optional.__wrapped__ is None
    True
    >>> optional.__resolved__
    True

Do not substitute ``not proxy`` for an identity check: it evaluates the wrapped
object's truth value, so it also accepts values such as ``0``, ``False`` and an
empty collection:

.. doctest::

    >>> empty = Proxy(lambda: [])
    >>> not empty
    True
    >>> empty.__wrapped__ is None
    False

Likewise, ``type(proxy)`` is the proxy's actual type. Use ``type(proxy.__wrapped__)``
when the concrete type of the result is required; this also evaluates the factory
if necessary. These identity and exact-type limitations apply even though many
ordinary operations are forwarded to the wrapped object.
