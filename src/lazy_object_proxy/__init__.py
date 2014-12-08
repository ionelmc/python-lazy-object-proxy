__version__ = "0.1.0"

__all__ = "Proxy",

try:
    from ._proxy import Proxy
except ImportError:
    from .proxy import Proxy
