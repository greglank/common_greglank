import os
from pathlib import Path
from inspect import currentframe, getframeinfo

def get_local_path(filename):
    """
    Returns the absolute path to a file relative to the calling script's directory.
        
    Example:
        If called from /path/to/caller/script.py with filename='config.toml',
        returns '/path/to/caller/config.toml' as a string
    """

    caller_frame = currentframe().f_back
    caller_path = Path(getframeinfo(caller_frame).filename)
    return str(caller_path.parent / filename)
