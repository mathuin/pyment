from django.urls import path
from accounts.views import register, my_account, order_details, order_info
from django.contrib.auth.views import login, logout, password_change

app_name = 'accounts'
urlpatterns = [
    path('register/', register, {'template_name': 'registration/register.djhtml'}, name='register'),
    path('my_account/', my_account, {'template_name': 'registration/my_account.djhtml'}, name='my_account'),
    path('order_details/<order_id>/', order_details, {'template_name': 'registration/order_details.djhtml'}, name='order_details'),
    path('order_info/', order_info, {'template_name': 'registration/order_info.djhtml'}, name='order_info'),
]

urlpatterns += [
    path('login/', login, {'template_name': 'registration/login.djhtml'}, name='login'),
    path('logout/', logout, {'template_name': 'registration/logout.djhtml'}, name='logout'),
    path('password_change/', password_change, name='password_change')
]
