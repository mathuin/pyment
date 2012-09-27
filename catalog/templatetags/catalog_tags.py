from django import template
from cart import cart
from catalog.models import Category
from django.template.defaultfilters import stringfilter

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
    active_categories = [ category for category in Category.objects.filter(is_active=True) if any([product for product in category.products if product.jars > 0])]
    return {
            'active_categories': active_categories,
            'request_path': request_path
            }

@register.filter(is_safe=True)
@stringfilter
def obfuscate(value):
    obfuscated_string = ''
    for character in value:
        obfuscated_string = obfuscated_string + '&#' + str(ord(character)) + ';'
    return obfuscated_string
