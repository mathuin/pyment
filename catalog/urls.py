from django.conf.urls import patterns

urlpatterns = patterns('catalog.views',
                       (r'^foo$', 'index', {'template_name': 'catalog/index.djhtml'}, 'catalog_home'),
                       (r'^foocategory/(?P<category_slug>[-\w]+)/$',
                        'show_category', {'template_name': 'catalog/category.djhtml'}, 'catalog_category'),
                       (r'^fooproduct/(?P<product_slug>[-\w]+)/$',
                        'show_product', {'template_name': 'catalog/product.djhtml'}, 'catalog_product'),
                       (r'^fooreview/product/add/$', 'add_review', {}, 'product_add_review'), )
