from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'polls.views.home_page', name='home'),
    url(r'^poll/', include('polls.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
