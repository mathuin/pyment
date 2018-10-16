from django.urls import path
from checkout.views import show_checkout, receipt

app_name = 'checkout'
urlpatterns = [
    path('', show_checkout, {'template_name': 'checkout/checkout.djhtml'}, name='checkout'),
    path('receipt/', receipt, {'template_name': 'checkout/receipt.djhtml'}, name='checkout_receipt'),
]
