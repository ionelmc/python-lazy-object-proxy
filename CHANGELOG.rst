
Changelog
=========

1.4.1 (2019-05-10)
------------------

* Fixed wheels being built with ``-coverage`` cflags. No more issues about bogus ``cext.gcda`` files.
* Removed useless C file from wheels.
* Changed ``setup.py`` to use setuptools-scm.

1.4.0 (2019-05-05)
------------------

* Fixed ``__mod__`` for the slots backend. Contributed by Ran Benita in
  `#28 <https://github.com/ionelmc/python-lazy-object-proxy/pull/28>`_.
* Dropped support for Python 2.6 and 3.3. Contributed by "hugovk" in
  `#24 <https://github.com/ionelmc/python-lazy-object-proxy/pull/24>`_.

1.3.1 (2017-05-05)
------------------

* Fix broken release (``sdist`` had a broken ``MANIFEST.in``).

1.3.0 (2017-05-02)
------------------

* Speed up arithmetic operations involving ``cext.Proxy`` subclasses.

1.2.2 (2016-04-14)
------------------

* Added `manylinux <https://www.python.org/dev/peps/pep-0513/>`_ wheels.
* Minor cleanup in readme.

1.2.1 (2015-08-18)
------------------

* Fix a memory leak (the wrapped object would get bogus references). Contributed by Astrum Kuo in
  `#10 <https://github.com/ionelmc/python-lazy-object-proxy/pull/10>`_.

1.2.0 (2015-07-06)
------------------

* Don't instantiate the object when __repr__ is called. This aids with debugging (allows one to see exactly in
  what state the proxy is).

1.1.0 (2015-07-05)
------------------

* Added support for pickling. The pickled value is going to be the wrapped object *without* any Proxy container.
* Fixed a memory management issue in the C extension (reference cycles weren't garbage collected due to improper
  handling in the C extension). Contributed by Alvin Chow in
  `#8 <https://github.com/ionelmc/python-lazy-object-proxy/pull/8>`_.

1.0.2 (2015-04-11)
-----------------------------------------

* First release on PyPI.
