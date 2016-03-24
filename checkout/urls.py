from django.conf.urls import url
from views import show_checkout, receipt

urlpatterns = [
    url(r'^$', show_checkout, {'template_name': 'checkout/checkout.djhtml'}, name='show_checkout'),
    url(r'^receipt/$', receipt, {'template_name': 'checkout/receipt.djhtml'}, name='receipt'),
]
