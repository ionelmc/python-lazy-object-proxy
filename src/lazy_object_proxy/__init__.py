__version__ = "1.0.2"

__all__ = "Proxy",

try:
    from .cext import Proxy
except ImportError:
    from .slots import Proxy
