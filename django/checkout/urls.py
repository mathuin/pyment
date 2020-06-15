from django.urls import path
from checkout.views import show_checkout, receipt

app_name = "checkout"
urlpatterns = [
    path("", show_checkout, {"template_name": "checkout/checkout.html"}, name="checkout"),
    path("receipt/", receipt, {"template_name": "checkout/receipt.html"}, name="checkout_receipt"),
]
