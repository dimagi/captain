import os

from fabric.network import disconnect_all
from fabric.api import execute

# HQ's fabfile
from fab import fabfile


def captain_deploy(env):
    execute(getattr(fabfile, env))
    try:
        execute(fabfile.setup_release)
    finally:
        disconnect_all()


class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)
