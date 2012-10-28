from django import template
from cart import cart
from catalog.models import Category
from pyment.settings import BREWER_NAME, BREWER_EMAIL, BREWER_LOCATION

register = template.Library()

@register.inclusion_tag("tags/cart_box.djhtml")
def cart_box(request):
    cart_item_count = cart.cart_distinct_item_count(request)
    return {'cart_item_count': cart_item_count }

@register.inclusion_tag("tags/category_list.djhtml")
def category_list(request_path):
    # should only return categories that meet the following requirements:
    # is_active is True,
    # they have products,
    # and those products have jars
    # there has to be a more django-ish way to do this
    active_categories = [ category for category in Category.objects.filter(is_active=True) if any([product for product in category.products if product.jars_in_stock > 0])]
    return {
            'active_categories': active_categories,
            'request_path': request_path
            }

@register.inclusion_tag("tags/footer.djhtml")
def footer():
    return {
        'name': BREWER_NAME,
        'email': BREWER_EMAIL,
        'location': BREWER_LOCATION,
        }

@register.inclusion_tag("tags/product_list.djhtml")
def product_list(products, header_text):
    return { 
        'products': products,
        'header_text': header_text 
        }
