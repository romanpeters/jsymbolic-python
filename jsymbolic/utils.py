import os
from contextlib import contextmanager


@contextmanager
def cd(newdir):
    """Safely change working directory"""
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)