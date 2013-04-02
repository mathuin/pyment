from django.conf.urls import patterns

urlpatterns = patterns('cart.views',
                       (r'^$', 'show_cart', {'template_name': 'cart/cart.djhtml'}, 'show_cart'), )
