__version__ = "1.0.0"
registry_date = "2019-10-07"

# store the path to the data directory
import os.path as _osp

data_dir = _osp.join(_osp.abspath(_osp.dirname(__file__)), "data")

# load the registry
from .core import load_registry

