from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'polls.views.home'),
    (r'^poll/(\d+)/$', 'polls.views.poll'),
    (r'^admin/', include(admin.site.urls)),
)

