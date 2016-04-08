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
