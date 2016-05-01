from django.conf.urls import patterns, url

from .views import CaptainStatusPage, CaptainDeploy, MonitorPage


urlpatterns = patterns('corehq.apps.captain.views',
    url(r'^$', CaptainStatusPage.as_view(), name=CaptainStatusPage.urlname),
    url(r'^monitor/$', MonitorPage.as_view(), name=MonitorPage.urlname),
    url(r'^deploy/$', CaptainDeploy.as_view(), name=CaptainDeploy.urlname),
)
