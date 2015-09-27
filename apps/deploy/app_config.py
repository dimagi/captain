import os
from django.apps import AppConfig
import sys
from django.conf import settings


def _add_source_root(source_root):
    sys.path.append(source_root)


class HqDeploy(AppConfig):
    name = "apps.deploy"

    def ready(self):
        # sneaky trick to add the HQ source onto the python path
        _add_source_root(os.path.join(settings.HQ_SOURCE_ROOT))
