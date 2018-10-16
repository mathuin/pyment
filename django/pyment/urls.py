from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    path('', include('meadery.urls', namespace='meadery')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('checkout/', include('checkout.urls', namespace='checkout')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('search/', include('search.urls', namespace='search')),

    # ('inventory/$', 'inventory.views.home'),
    # ('brewery/$', 'meadery.views.home'),

    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'pyment.views.file_not_found_404'
