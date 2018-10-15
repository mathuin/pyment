from django.conf.urls import url
from checkout.views import show_checkout, receipt

app_name = 'checkout'
urlpatterns = [
    url(r'^$', show_checkout, {'template_name': 'checkout/checkout.djhtml'}, name='checkout'),
    url(r'^receipt/$', receipt, {'template_name': 'checkout/receipt.djhtml'}, name='checkout_receipt'),
]
