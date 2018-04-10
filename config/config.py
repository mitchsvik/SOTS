import os
try:
    from .config_local import *
except ImportError as e:
    from .config_base import *

BASEDIR = os.path.abspath(os.path.dirname(__file__))
