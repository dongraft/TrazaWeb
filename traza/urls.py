from django.conf.urls import patterns, include, url

from django.contrib import admin
from carlitos import views as carlitos_views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', carlitos_views.receive, name='receive'),
)
