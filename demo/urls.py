from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from demo import views

urlpatterns = patterns('',
                       url(r'^$', view=views.index, name='index'),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^login/$', 'django.contrib.auth.views.login'),
                       url(r'^logout/$', 'django.contrib.auth.views.logout'),
                       url(r'^qrtoauth/', include('django_auth_qr2auth.urls',
                                                  app_name='QR2Auth')),
                       ) + static(settings.STATIC_URL,
                                  document_root=settings.STATIC_ROOT)
