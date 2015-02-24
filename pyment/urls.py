from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^', include('meadery.urls')),
                       url(r'^cart/', include('cart.urls')),
                       url(r'^checkout/', include('checkout.urls')),
                       url(r'^accounts/', include('accounts.urls')),
                       url(r'^accounts/', include('django.contrib.auth.urls')),
                       url(r'^search/', include('search.urls')),

                       #(r'^inventory/$', 'inventory.views.home'),
                       #(r'^brewery/$', 'meadery.views.home'),
                       # Examples:
                       # url(r'^$', 'pyment.views.home', name='home'),
                       # url(r'^pyment/', include('pyment.foo.urls')),

                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       url(r'^admin/', include(admin.site.urls)), )

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'pyment.views.file_not_found_404'
