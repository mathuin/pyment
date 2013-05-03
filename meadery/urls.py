from django.conf.urls import patterns

urlpatterns = patterns('meadery.views',
                       (r'^$', 'index', {'template_name': 'meadery/index.djhtml'}, 'meadery_home'),
                       (r'^category/(?P<category_value>[-\w]+)/$',
                        'show_category', {'template_name': 'meadery/category.djhtml'}, 'meadery_category'),
                       (r'^product/(?P<product_slug>[-\w]+)/$',
                        'show_product', {'template_name': 'meadery/product.djhtml'}, 'meadery_product'),
                       (r'^review/product/add/$', 'add_review', {}, 'product_add_review'), )
