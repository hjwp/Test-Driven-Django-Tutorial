from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'polls.views.home'),
    url(r'^poll/(\d+)/$', 'polls.views.poll'),
    url(r'^admin/', include(admin.site.urls)),
)
