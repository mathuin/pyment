from cart import cart
from models import Order, OrderItem
from forms import CheckoutForm
from django.core import urlresolvers

# returns the URL from the checkout module for cart
def get_checkout_url(request):
    return urlresolvers.reverse('checkout')

# process request
def process(request):
    order = create_order(request)
    results = {'order_number':order.id, 'message':''}
    return results

def create_order(request):
    order = Order()
    checkout_form = CheckoutForm(request.POST, instance=order)
    order = checkout_form.save(commit=False)
    order.ip_address = request.META.get('REMOTE_ADDR')
    order.user = None
    if request.user.is_authenticated():
        order.user = request.user
    order.status = Order.SUBMITTED
    order.save()
    # if the order save succeeded
    if order.pk:
        cart_items = cart.get_cart_items(request)
        for ci in cart_items:
            # create order item for each cart item
            oi = OrderItem()
            oi.order = order
            oi.quantity = ci.quantity
            oi.product = ci.product
            oi.save()
        # all set, empty cart
        cart.empty_cart(request)
    # save profile info for future orders
    if request.user.is_authenticated():
        from accounts import profile
        profile.set(request)
    # return the new order object
    return order

