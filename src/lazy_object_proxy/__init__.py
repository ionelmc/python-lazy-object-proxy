__version__ = "1.0.1"

__all__ = "Proxy",

try:
    from .cext import Proxy
except ImportError:
    from .slots import Proxy
