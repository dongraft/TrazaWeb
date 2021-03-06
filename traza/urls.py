from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
from carlitos import views as carlitos_views
from mapitas import views as mapitas_views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', carlitos_views.receive, name='receive'),
    url(r'^stats/$', mapitas_views.stats, name='stats'),
    url(r'^data/$', mapitas_views.get_data, name='get_data'),
    url(r'^graphs/$', mapitas_views.graphs, name='graphs'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += patterns('django.views.static', )
