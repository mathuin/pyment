from cart import cart
from checkout.models import Order, OrderItem, PickList, PickListItem
from checkout.forms import CheckoutForm
from meadery.models import Product
from django.core.exceptions import ValidationError
from django.core.mail import mail_managers, send_mail
from django.core.urlresolvers import reverse
from pyment import settings


def get_checkout_url(request):
    return reverse('checkout')


def process(request):
    order = create_order(request)
    results = {'order_number': order.id, 'message': ''}
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
        profile.fill(request)
    # mail the managers
    mail_manager_subject = '{0} has been placed!'.format(order)
    mail_manager_message = '{0} has been placed by {1}.\n\nClick here: {2}'.format(order, order.user if order.user else 'anonymous', request.build_absolute_uri(reverse('admin:checkout_order_change', args=(order.pk,))))
    mail_managers(mail_manager_subject, mail_manager_message)
    # mail the customer
    if order.email:
        # FIXME: someday make templates for these emails
        mail_customer_subject = 'Thank you for placing {0}!'.format(order.name)
        mail_customer_message = '{0} was placed by you.  Click here for more details: {1}\n\nThank you for your order!\n\n{2}'.format(order.name, request.build_absolute_uri(order.get_absolute_url()), settings.SITE_NAME)
        send_mail(mail_customer_subject, mail_customer_message, settings.DEFAULT_FROM_EMAIL, [order.email])
    # return the new order object
    return order


def cancel_order(self):
    if self.status == Order.SUBMITTED:
        # FIXME: test for presence of order
        OrderItem.objects.filter(order=self.pk).delete()
        self.status = Order.CANCELLED
        self.save()
        # mail the customer
        if self.email:
            # FIXME: someday make templates for these emails
            mail_customer_subject = '{0} has been cancelled'.format(self.name)
            mail_customer_message = 'Our warehouse minions have cancelled {0}.  If you have any questions, please email us at {1}.\n\nWe apologize for any inconvenience!\n\n{2}'.format(self.name, settings.DEFAULT_FROM_EMAIL, settings.SITE_NAME)
            send_mail(mail_customer_subject, mail_customer_message, settings.DEFAULT_FROM_EMAIL, [self.email])
        return True
    else:
        return False


def create_picklist(order):
    if order.status == Order.SUBMITTED and all_in_stock(order):
        picklist = PickList()
        picklist.order = order
        picklist.status = PickList.SUBMITTED
        picklist.save()
        if picklist.pk:
            order_items = OrderItem.objects.filter(order=order)
            for oi in order_items:
                for _ in range(oi.quantity):
                    # create picklist item for each individual order item
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
        # mail the customer
        if order.email:
            # FIXME: someday make templates for these emails
            mail_customer_subject = '{0} is being processed!'.format(order.name)
            mail_customer_message = 'Good news!  {0} has been generated from {1} which was placed by you.\n\nThank you again for your order!\n\n{2}'.format(picklist.name, order.name, settings.SITE_NAME)
            send_mail(mail_customer_subject, mail_customer_message, settings.DEFAULT_FROM_EMAIL, [order.email])
        return picklist
    else:
        return None


def all_in_stock(order):
    order_items = OrderItem.objects.filter(order=order)
    try:
        if order_items.exists():
            for oi in order_items:
                if Product.objects.get(id=oi.product_id).jars_in_stock() < oi.quantity:
                    raise ValidationError('Insufficient product in stock - please select another product')
        else:
            raise ValidationError('No items in order!')
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
        # mail the customer
        if self.order.email:
            # FIXME: someday make templates for these emails
            mail_customer_subject = '{0} is available for pickup!'.format(self.order.name)
            mail_customer_message = 'Good news!  Our friendly warehouse minions have processed {0} which was generated from {1} which was placed by you.\n\nPlease stop by and pick up your order soon!\n\n{2}'.format(self.name, self.order.name, settings.SITE_NAME)
            send_mail(mail_customer_subject, mail_customer_message, settings.DEFAULT_FROM_EMAIL, [self.order.email])
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
        # mail the customer
        if self.order.email:
            # FIXME: someday make templates for these emails
            mail_customer_subject = '{0} is being reexamined'.format(self.order.name)
            mail_customer_message = 'How unexpected!  {0} has been cancelled by our warehouse minions, but {1} is still active.\n\nWe apologize for any inconvenience, and we encourage you to watch your email for more details!\n\n{2}'.format(self.name, self.order.name, settings.SITE_NAME)
            send_mail(mail_customer_subject, mail_customer_message, settings.DEFAULT_FROM_EMAIL, [self.order.email])
        return True
    else:
        return False
