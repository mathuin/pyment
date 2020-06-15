from django.urls import path
from cart.views import show_cart

app_name = "cart"
urlpatterns = [path("", show_cart, {"template_name": "cart/cart.html"}, name="show_cart")]
