from django.conf.urls.defaults import patterns

urlpatterns = patterns('checkout.views',
                       (r'^$', 'show_checkout', {'template_name': 'checkout/checkout.djhtml',}, 'checkout'),
                       (r'^receipt/$', 'receipt', {'template_name': 'checkout/receipt.djhtml',}, 'checkout_receipt'),
)
