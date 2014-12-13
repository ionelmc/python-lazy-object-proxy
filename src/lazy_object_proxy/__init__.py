__version__ = "0.1.0"

__all__ = "Proxy",

try:
    from .cext import Proxy
except ImportError:
    from .slots import Proxy
