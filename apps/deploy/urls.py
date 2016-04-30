from django.conf.urls import patterns, url

from .views import ChiefStatusPage, ChiefDeploy, MonitorPage


urlpatterns = patterns('corehq.apps.chief.views',
    url(r'^$', ChiefStatusPage.as_view(), name=ChiefStatusPage.urlname),
    url(r'^monitor/$', MonitorPage.as_view(), name=MonitorPage.urlname),
    url(r'^deploy/$', ChiefDeploy.as_view(), name=ChiefDeploy.urlname),
)
