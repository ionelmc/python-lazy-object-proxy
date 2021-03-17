import sys

PY3 = sys.version_info[0] >= 3


def pytest_ignore_collect(path, config):
    basename = path.basename

    if not PY3 and "py3" in basename or PY3 and "py2" in basename:
        return True
