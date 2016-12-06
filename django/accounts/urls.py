from django.conf.urls import url
from accounts.views import register, my_account, order_details, order_info
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^register/$', register, {'template_name': 'registration/register.djhtml'}, name='register'),
    url(r'^my_account/$', my_account, {'template_name': 'registration/my_account.djhtml'}, name='my_account'),
    url(r'^order_details/(?P<order_id>[-\w]+)/$', order_details, {'template_name': 'registration/order_details.djhtml'}, name='order_details'),
    url(r'^order_info/$', order_info, {'template_name': 'registration/order_info.djhtml'}, name='order_info'),
]

urlpatterns += [
    url(r'^login/$', login, {'template_name': 'registration/login.djhtml'}, name='login'),
    url(r'^logout/$', logout, {'template_name': 'registration/logout.djhtml'}, name='logout'),
]
