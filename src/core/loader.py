"""Generic file loading functions."""

from os.path import isfile, isdir
from glob import glob

import yaml


############################################################
# Lambda functions
############################################################
ls_all = lambda path: [path for path in glob(f"{path}/*")]
ls_dir = lambda path: [path for path in glob(f"{path}/*") if isdir(path)]
ls_file = lambda path: [path for path in glob(f"{path}/*") if isfile(path)]


############################################################
# File loading functions
############################################################
def load_yaml(path: str) -> dict:
    """Load yaml file."""
    with open(path, "r") as f:
        config = yaml.safe_load(f)
    return config
