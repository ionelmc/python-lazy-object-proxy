========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |coveralls| |codecov|
        | |landscape| |scrutinizer| |codacy| |codeclimate|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/python-lazy-object-proxy/badge/?style=flat
    :target: https://readthedocs.org/projects/python-lazy-object-proxy
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/ionelmc/python-lazy-object-proxy.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/ionelmc/python-lazy-object-proxy

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/ionelmc/python-lazy-object-proxy?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/ionelmc/python-lazy-object-proxy

.. |requires| image:: https://requires.io/github/ionelmc/python-lazy-object-proxy/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/ionelmc/python-lazy-object-proxy/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/ionelmc/python-lazy-object-proxy/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/ionelmc/python-lazy-object-proxy

.. |codecov| image:: https://codecov.io/github/ionelmc/python-lazy-object-proxy/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/ionelmc/python-lazy-object-proxy

.. |landscape| image:: https://landscape.io/github/ionelmc/python-lazy-object-proxy/master/landscape.svg?style=flat
    :target: https://landscape.io/github/ionelmc/python-lazy-object-proxy/master
    :alt: Code Quality Status

.. |codacy| image:: https://img.shields.io/codacy/REPLACE_WITH_PROJECT_ID.svg
    :target: https://www.codacy.com/app/ionelmc/python-lazy-object-proxy
    :alt: Codacy Code Quality Status

.. |codeclimate| image:: https://codeclimate.com/github/ionelmc/python-lazy-object-proxy/badges/gpa.svg
   :target: https://codeclimate.com/github/ionelmc/python-lazy-object-proxy
   :alt: CodeClimate Quality Status

.. |version| image:: https://img.shields.io/pypi/v/lazy-object-proxy.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/lazy-object-proxy

.. |commits-since| image:: https://img.shields.io/github/commits-since/ionelmc/python-lazy-object-proxy/v1.3.1.svg
    :alt: Commits since latest release
    :target: https://github.com/ionelmc/python-lazy-object-proxy/compare/v1.3.1...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/lazy-object-proxy.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/lazy-object-proxy

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/lazy-object-proxy.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/lazy-object-proxy

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/lazy-object-proxy.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/lazy-object-proxy

.. |scrutinizer| image:: https://img.shields.io/scrutinizer/g/ionelmc/python-lazy-object-proxy/master.svg
    :alt: Scrutinizer Status
    :target: https://scrutinizer-ci.com/g/ionelmc/python-lazy-object-proxy/


.. end-badges

A fast and thorough lazy object proxy.

* Free software: BSD license

Note that this is based on `wrapt`_'s ObjectProxy with one big change: it calls a function the first time the proxy object is
used, while `wrapt.ObjectProxy` just forwards the method calls to the target object.

In other words, you use `lazy-object-proxy` when you only have the object way later and you use `wrapt.ObjectProxy` when you
want to override few methods (by subclassing) and forward everything else to the target object.

Example::

    def expensive_func():
        # create expensive object
        return stuff

    obj = lazy_object_proxy.Proxy(expensive_func)
    # function is called only when object is actually used
    print(obj.foobar)  # now expensive_func is called

Installation
============

::

    pip install lazy-object-proxy

Documentation
=============

https://python-lazy-object-proxy.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Acknowledgements
================

This project is based on some code from `wrapt`_ as you can see in the git history.

.. _wrapt: https://github.com/GrahamDumpleton/wrapt
