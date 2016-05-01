from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('apps.deploy.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^django-rq/', include('django_rq.urls')),
]
