import os
from manage import _set_source_root_parent

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chief.settings")
_set_source_root_parent('submodules')

application = get_wsgi_application()
