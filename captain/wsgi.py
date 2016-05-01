import os
from manage import _set_source_root_parent

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "captain.settings")
_set_source_root_parent('submodules')

application = get_wsgi_application()
application = DjangoWhiteNoise(application)
