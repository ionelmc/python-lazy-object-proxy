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
      - |version| |downloads| |wheel| |supported-versions| |supported-implementations|

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

.. |codacy| image:: https://img.shields.io/codacy/REPLACE_WITH_PROJECT_ID.svg?style=flat
    :target: https://www.codacy.com/app/ionelmc/python-lazy-object-proxy
    :alt: Codacy Code Quality Status

.. |codeclimate| image:: https://codeclimate.com/github/ionelmc/python-lazy-object-proxy/badges/gpa.svg
   :target: https://codeclimate.com/github/ionelmc/python-lazy-object-proxy
   :alt: CodeClimate Quality Status

.. |version| image:: https://img.shields.io/pypi/v/lazy-object-proxy.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/lazy-object-proxy

.. |downloads| image:: https://img.shields.io/pypi/dm/lazy-object-proxy.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/lazy-object-proxy

.. |wheel| image:: https://img.shields.io/pypi/wheel/lazy-object-proxy.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/lazy-object-proxy

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/lazy-object-proxy.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/lazy-object-proxy

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/lazy-object-proxy.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/lazy-object-proxy

.. |scrutinizer| image:: https://img.shields.io/scrutinizer/g/ionelmc/python-lazy-object-proxy/master.svg?style=flat
    :alt: Scrutinizer Status
    :target: https://scrutinizer-ci.com/g/ionelmc/python-lazy-object-proxy/


.. end-badges

A fast and thorough lazy object proxy.

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

Acknowledgements
================

This project is based on some code from `wrapt <https://github.com/GrahamDumpleton/wrapt>`_
as you can see in the git history.
