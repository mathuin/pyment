from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       
    url(r'^', include('catalog.urls')),
    url(r'^cart/', include('cart.urls')),
    url(r'^checkout/', include('checkout.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),

    #(r'^inventory/$', 'inventory.views.home'),
    #(r'^brewery/$', 'meadery.views.home'),
    # Examples:
    # url(r'^$', 'pyment.views.home', name='home'),
    # url(r'^pyment/', include('pyment.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

handler404 = 'views.file_not_found_404'
