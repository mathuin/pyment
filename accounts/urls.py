from django.conf.urls import patterns

urlpatterns = patterns('accounts.views',
                       (r'^register/$', 'register',
                        {'template_name': 'registration/register.djhtml', }, 'register'),
                       (r'^my_account/$', 'my_account',
                        {'template_name': 'registration/my_account.djhtml'}, 'my_account'),
                       (r'^order_details/(?P<order_id>[-\w]+)/$', 'order_details',
                        {'template_name': 'registration/order_details.djhtml'}, 'order_details'),
                       (r'^order_info/$', 'order_info',
                        {'template_name': 'registration/order_info.djhtml'}, 'order_info'), )

urlpatterns += patterns('django.contrib.auth.views',
                        (r'^login/$', 'login',
                         {'template_name': 'registration/login.djhtml', }, 'login'),
                        (r'^logout/$', 'logout',
                         {'template_name': 'registration/logout.djhtml', }, 'logout'), )
