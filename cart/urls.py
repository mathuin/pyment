from django.conf.urls import url
from views import show_cart

urlpatterns = [
    url(r'^$', show_cart, {'template_name': 'cart/cart.djhtml'}, name='show_cart'),
]
