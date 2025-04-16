#!/usr/bin/env python
import os
import platform
import re
import sys
from pathlib import Path

from setuptools import Extension
from setuptools import find_packages
from setuptools import setup
from setuptools.command.build_ext import build_ext
from setuptools.dist import Distribution

# Enable code coverage for C code: we cannot use CFLAGS=-coverage in tox.ini, since that may mess with compiling
# dependencies (e.g. numpy). Therefore, we set SETUPPY_CFLAGS=-coverage in tox.ini and copy it to CFLAGS here (after
# deps have been safely installed).
if 'TOX_ENV_NAME' in os.environ and os.environ.get('SETUPPY_EXT_COVERAGE') == 'yes' and platform.system() == 'Linux':
    CFLAGS = os.environ['CFLAGS'] = '-fprofile-arcs -ftest-coverage'
    LFLAGS = os.environ['LFLAGS'] = '-lgcov'
else:
    CFLAGS = ''
    LFLAGS = ''

allow_extensions = True
if '__pypy__' in sys.builtin_module_names:
    print('NOTICE: C extensions disabled on PyPy (would be broken)!')
    allow_extensions = False
if os.environ.get('SETUPPY_FORCE_PURE'):
    print('NOTICE: C extensions disabled (SETUPPY_FORCE_PURE)!')
    allow_extensions = False


class OptionalBuildExt(build_ext):
    """
    Allow the building of C extensions to fail.
    """

    def run(self):
        try:
            super().run()
        except Exception as e:
            self._unavailable(e)
            self.extensions = []  # avoid copying missing files (it would fail).

    def _unavailable(self, e):
        print('*' * 80)
        print(
            """WARNING:

    An optional code optimization (C extension) could not be compiled.

    Optimizations for this package will not be available!
            """
        )

        print('CAUSE:')
        print('')
        print('    ' + repr(e))
        print('*' * 80)


class BinaryDistribution(Distribution):
    """
    Distribution which almost always forces a binary package with platform name
    """

    def has_ext_modules(self):
        return super().has_ext_modules() or not os.environ.get('SETUPPY_ALLOW_PURE')


def read(*names, **kwargs):
    with Path(__file__).parent.joinpath(*names).open(encoding=kwargs.get('encoding', 'utf8')) as fh:
        return fh.read()


setup(
    name='lazy-object-proxy',
    use_scm_version={
        'local_scheme': 'dirty-tag',
        'write_to': 'src/lazy_object_proxy/_version.py',
        'fallback_version': '1.11.0',
    },
    license='BSD-2-Clause',
    description='A fast and thorough lazy object proxy.',
    long_description='{}\n{}'.format(
        re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub('', read('README.rst')),
        re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst')),
    ),
    long_description_content_type='text/x-rst',
    author='Ionel Cristian Mărieș',
    author_email='contact@ionelmc.ro',
    url='https://github.com/ionelmc/python-lazy-object-proxy',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[path.stem for path in Path('src').glob('*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        # uncomment if you test on these interpreters:
        # "Programming Language :: Python :: Implementation :: IronPython",
        # "Programming Language :: Python :: Implementation :: Jython",
        # "Programming Language :: Python :: Implementation :: Stackless",
        'Topic :: Utilities',
    ],
    project_urls={
        'Documentation': 'https://python-lazy-object-proxy.readthedocs.io/',
        'Changelog': 'https://python-lazy-object-proxy.readthedocs.io/en/latest/changelog.html',
        'Issue Tracker': 'https://github.com/ionelmc/python-lazy-object-proxy/issues',
    },
    keywords=[
        # eg: "keyword1", "keyword2", "keyword3",
    ],
    python_requires='>=3.9',
    install_requires=[
        # eg: "aspectlib==1.1.1", "six>=1.7",
    ],
    extras_require={
        # eg:
        #   "rst": ["docutils>=0.11"],
        #   ":python_version=='3.8'": ["backports.zoneinfo"],
    },
    setup_requires=[
        'setuptools_scm>=3.3.1',
    ],
    cmdclass={'build_ext': OptionalBuildExt},
    ext_modules=[
        Extension(
            str(path.relative_to('src').with_suffix('')).replace(os.sep, '.'),
            sources=[str(path)],
            extra_compile_args=CFLAGS.split(),
            extra_link_args=LFLAGS.split(),
            include_dirs=[str(path.parent)],
        )
        for path in Path('src').glob('**/*.c')
    ]
    if allow_extensions
    else [],
    distclass=BinaryDistribution if allow_extensions else None,
)
