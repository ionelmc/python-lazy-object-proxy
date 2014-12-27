===============================
lazy-object-proxy
===============================

| |docs| |travis| |appveyor| |coveralls| |landscape| |scrutinizer|
| |version| |downloads| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/python-lazy-object-proxy/badge/?style=flat
    :target: https://readthedocs.org/projects/python-lazy-object-proxy
    :alt: Documentation Status

.. |travis| image:: http://img.shields.io/travis/ionelmc/python-lazy-object-proxy/master.png?style=flat
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/ionelmc/python-lazy-object-proxy

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/ionelmc/python-lazy-object-proxy?branch=master
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/ionelmc/python-lazy-object-proxy

.. |coveralls| image:: http://img.shields.io/coveralls/ionelmc/python-lazy-object-proxy/master.png?style=flat
    :alt: Coverage Status
    :target: https://coveralls.io/r/ionelmc/python-lazy-object-proxy

.. |landscape| image:: https://landscape.io/github/ionelmc/python-lazy-object-proxy/master/landscape.svg?style=flat
    :target: https://landscape.io/github/ionelmc/python-lazy-object-proxy/master
    :alt: Code Quality Status

.. |version| image:: http://img.shields.io/pypi/v/lazy-object-proxy.png?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/lazy-object-proxy

.. |downloads| image:: http://img.shields.io/pypi/dm/lazy-object-proxy.png?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/lazy-object-proxy

.. |wheel| image:: https://pypip.in/wheel/lazy-object-proxy/badge.png?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/lazy-object-proxy

.. |supported-versions| image:: https://pypip.in/py_versions/lazy-object-proxy/badge.png?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/lazy-object-proxy

.. |supported-implementations| image:: https://pypip.in/implementation/lazy-object-proxy/badge.png?style=flat
    :alt: Supported imlementations
    :target: https://pypi.python.org/pypi/lazy-object-proxy

.. |scrutinizer| image:: https://img.shields.io/scrutinizer/g/ionelmc/python-lazy-object-proxy/master.png?style=flat
    :alt: Scrtinizer Status
    :target: https://scrutinizer-ci.com/g/ionelmc/python-lazy-object-proxy/

An example package. Replace this with a proper project description. Generated with https://github.com/ionelmc/cookiecutter-pylibrary

* Free software: BSD license

Installation
============

::

    pip install lazy-object-proxy

Documentation
=============

https://python-lazy-object-proxy.readthedocs.org/

Development
===========

To run the all tests run::

    tox

Benchmarks
==========

The tested implementations:

* ``lazy_object_proxy.slots.Proxy``, available as ``lazy_object_proxy.Proxy`` if the C extension is not available.
* ``lazy_object_proxy.cext.Proxy``, available as ``lazy_object_proxy.Proxy``.
* `objproxies <https://pypi.python.org/pypi/objproxies>`_ - fork of PJE's `ProxyTypes <https://pypi.python.org/pypi/ProxyTypes>`_ with Python 3 support. [1]_
* `SimpleLazyObject <https://github.com/django/django/blob/stable/1.7.x/django/utils/functional.py#L337>`_ from Django. [1]_
* ``lazy_object_proxy.simple.Proxy`` - uses the non-data descriptor `trick <http://blog.ionelmc.ro/2014/11/04/an-interesting-python-descriptor-quirk/>`_. [1]_

For Python 2.7::

    ------ benchmark: min 5 rounds (of min 25.00us), 5.00s max time, timer: time.clock -----
    Name (time in ns)                Min        Max       Mean    StdDev  Rounds  Iterations
    ----------------------------------------------------------------------------------------
    test_perf[slots]            705.3837  3091.0072   720.4805   27.2588  180453          38
    test_perf[cext]              93.6346   278.9731    95.1876    2.5474  164373         312
    test_perf[simple]           398.1636  1863.2017   405.4325   13.1411  207521          59
    test_perf[django]           471.6515   983.0809   480.4264   10.2059  193043          53
    test_perf[objproxies]      1204.7003  4818.8010  1475.3419  114.8213   55898           1
    ----------------------------------------------------------------------------------------

For Python 3.4::

    -- benchmark: min 5 rounds (of min 25.00us), 5.00s max time, timer: time.perf_counter --
    Name (time in ns)                 Min        Max       Mean   StdDev  Rounds  Iterations
    ----------------------------------------------------------------------------------------
    test_perf[slots]             803.1335  2728.8286   826.0882  20.5562  182436          33
    test_perf[cext]              103.2911   254.4223   104.6869   2.6294  164373         277
    test_perf[simple]            448.6894  2040.6147   462.0342  17.1546  218443          49
    test_perf[django]            518.3013  1225.7125   532.0523  14.4672  218443          43
    test_perf[objproxies]       1116.8575  3827.4331  1157.8419  43.9602  174755          24
    ----------------------------------------------------------------------------------------

For PyPy 2.4:

    Note that the mean difference between ``simple``, ``django`` and ``objproxies`` is smaller the standard deviance, thus it cannot be considered.

::

    ------ benchmark: min 5 rounds (of min 25.00us), 15.00s max time, timer: time.clock ----
    Name (time in ns)                   Min        Max     Mean   StdDev  Rounds  Iterations
    ----------------------------------------------------------------------------------------
    test_perf[slots]                 1.9577   260.2979   2.2457   0.4882  498050       15384
    test_perf[simple]               31.3536  4374.4246  34.7433  11.7566  478894         999
    test_perf[django]               32.5269  4443.8381  35.8729  16.9071  461157        1000
    test_perf[objproxies]           33.1293  4529.3718  36.7435  13.3377  452773        1000
    ----------------------------------------------------------------------------------------

.. [1] Lacks support for certain more tricky operations like ``vars(obj)`` and other operators.