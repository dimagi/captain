from django.conf.urls import patterns, url

from .views import ChiefStatusPage, ChiefDeploy, LogFileView


urlpatterns = patterns('corehq.apps.chief.views',
    url(r'^$', ChiefStatusPage.as_view(), name=ChiefStatusPage.urlname),
    url(r'^deploy/$', ChiefDeploy.as_view(), name=ChiefDeploy.urlname),
    url(r'^logfile/$', LogFileView.as_view(), name=LogFileView.urlname),
)
