from django.conf.urls.defaults import *
from django.contrib import admin
from mysite.polls import views as polls_views

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', polls_views.polls),
    (r'^admin/', include(admin.site.urls)),
)

