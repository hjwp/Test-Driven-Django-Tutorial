from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'polls.views.home_page', name='home'),
    url(r'^poll/(\d+)/$', 'polls.views.poll', name='poll'),
    url(r'^poll/(\d+)/vote$', 'polls.views.vote', name='vote'),

    url(r'^admin/', include(admin.site.urls)),
)
