from django.conf.urls import url
from cart.views import show_cart

app_name = 'cart'
urlpatterns = [
    url(r'^$', show_cart, {'template_name': 'cart/cart.djhtml'}, name='show_cart'),
]
