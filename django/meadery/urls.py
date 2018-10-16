from django.urls import path
from meadery.views import index, show_category, show_product, add_review

app_name = 'meadery'
urlpatterns = [
    path('', index, {'template_name': 'meadery/index.html'}, name='home'),
    path('category/<category_value>/', show_category, {'template_name': 'meadery/category.html'}, name='category'),
    path('product/<slug:product_slug>/', show_product, {'template_name': 'meadery/product.html'}, name='product'),
    path('review/product/add/', add_review, {}, name='product_add_review'),
]
