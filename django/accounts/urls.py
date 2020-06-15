from django.urls import path
from accounts.views import register, my_account, order_details, order_info
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView

app_name = "accounts"
urlpatterns = [
    path("register/", register, {"template_name": "registration/register.html"}, name="register"),
    path("my_account/", my_account, {"template_name": "registration/my_account.html"}, name="my_account"),
    path("order_details/<order_id>/", order_details, {"template_name": "registration/order_details.html"}, name="order_details"),
    path("order_info/", order_info, {"template_name": "registration/order_info.html"}, name="order_info"),
]

urlpatterns += [
    path("login/", LoginView.as_view(), {"template_name": "registration/login.html"}, name="login"),
    path("logout/", LogoutView.as_view(), {"template_name": "registration/logout.html"}, name="logout"),
    path("password_change/", PasswordChangeView.as_view(), name="password_change"),
]
