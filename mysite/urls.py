from django.conf.urls.defaults import *
from django.contrib import admin
from mysite.polls import views

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', views.home),
    (r'^poll/(\d+)/$', views.poll),
    (r'^admin/', include(admin.site.urls)),
)

