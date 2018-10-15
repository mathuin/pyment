from django.conf.urls import url
from meadery.views import index, show_category, show_product, add_review

app_name = 'meadery'
urlpatterns = [
    url(r'^$', index, {'template_name': 'meadery/index.djhtml'}, name='meadery_home'),
    url(r'^category/(?P<category_value>[-\w]+)/$', show_category, {'template_name': 'meadery/category.djhtml'}, name='meadery_category'),
    url(r'^product/(?P<product_slug>[-\w]+)/$', show_product, {'template_name': 'meadery/product.djhtml'}, name='meadery_product'),
    url(r'^review/product/add/$', add_review, {}, name='product_add_review'),
]
