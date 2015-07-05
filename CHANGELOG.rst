
Changelog
=========

1.1.0 (2015-07-05)
------------------

* Added support for pickling. The pickled value is going to be the wrapped object *without* any Proxy container.
* Fixed a memory management issue in the C extension (reference cycles weren't garbage collected due to improper
  handling in the C extension).

1.0.2 (2015-04-11)
-----------------------------------------

* First release on PyPI.
