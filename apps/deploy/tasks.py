import os

import sh
from django.conf import settings
from celery.task import task


@task
def captain_deploy(env):
    # Update local HQ
    sh.git('-C', settings.HQ_SOURCE_ROOT, 'pull')

    with cd(settings.HQ_SOURCE_ROOT):
        sh.fab(env, 'setup_release')


class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)
