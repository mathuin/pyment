from django.conf.urls import url
from views import show_checkout, receipt

urlpatterns = [
    url(r'^$', show_checkout, {'template_name': 'checkout/checkout.djhtml'}),
    url(r'^receipt/$', receipt, {'template_name': 'checkout/receipt.djhtml'}),
]
