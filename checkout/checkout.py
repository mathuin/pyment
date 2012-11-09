from cart import cart
from models import Order, OrderItem, PickList, PickListItem
from forms import CheckoutForm
from django.core import urlresolvers
from catalog.models import Product
from django.core.exceptions import ValidationError

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

def create_picklist(order):
    if order.status == Order.SUBMITTED:
        picklist = PickList()
        picklist.order = order
        picklist.status = PickList.SUBMITTED
        picklist.save()
        if picklist.pk:
            order_items = OrderItem.objects.filter(order=order)
            for oi in order_items:
                # create picklist item for each order item
                pi = PickListItem()
                pi.picklist = picklist
                pi.jar = oi.product.first_available()
                # take the jar off the shelf!
                pi.jar.is_available = False
                pi.jar.save()
                pi.save()
        # on success, set picklist to Submitted and order to Processed
        order.status = Order.PROCESSED
        order.save()
        return picklist
    else:
        return None

def all_in_stock(order):
    order_items = OrderItem.objects.filter(order=order)
    try:
        for oi in order_items:
            if Product.objects.get(id=oi.product_id).jars_in_stock().count() < oi.quantity:
                raise ValidationError, 'Insufficient product in stock - please select another product'
    except ValidationError:
        return None
    else:
        return order 
                
def process_picklist(self):
    if self.status == PickList.SUBMITTED and self.order.status == Order.PROCESSED:
        # FIXME: test for presence of picklist
        picklist_items = PickListItem.objects.filter(picklist=self.pk)
        for pli in picklist_items:
            pli.jar.is_active = False
            pli.jar.save()
        self.order.status = Order.DELIVERED
        self.order.save()
        self.status = PickList.PROCESSED
        self.save()
        return True
    else:
        return False
        
def cancel_picklist(self):
    if self.status == PickList.SUBMITTED and self.order.status == Order.PROCESSED:
        # FIXME: test for presence of picklist
        picklist_items = PickListItem.objects.filter(picklist=self.pk)
        for pli in picklist_items:
            pli.jar.is_available = True
            pli.jar.save()           
        self.order.status = Order.SUBMITTED
        self.order.save()
        self.status = PickList.CANCELLED
        self.save()
        return True
    else:
        return False
    
       
    
