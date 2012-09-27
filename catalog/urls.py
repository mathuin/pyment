from django.conf.urls import patterns

urlpatterns = patterns('catalog.views',
                       (r'^$', 'index', { 'template_name':'catalog/index.djhtml'}, 'catalog_home'),
                       (r'^category/(?P<category_slug>[-\w]+)/$',
                        'show_category', { 'template_name':'catalog/category.djhtml'}, 'catalog_category'),
                       (r'^product/(?P<product_slug>[-\w]+)/$', 
                        'show_product', { 'template_name':'catalog/product.djhtml'}, 'catalog_product'),
)
