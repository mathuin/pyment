from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from checkout.forms import CheckoutForm
from checkout.models import Order, OrderItem
from checkout import checkout
from cart import cart
from accounts import profile


def show_checkout(request, template_name='checkout/checkout.html'):
    if cart.is_empty(request):
        cart_url = reverse('cart:show_cart')
        return HttpResponseRedirect(cart_url)
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = CheckoutForm(postdata)
        if form.is_valid():
            response = checkout.process(request)
            order_number = response.get('order_number', 0)
            error_message = response.get('message', '')
            if order_number:
                request.session['order_number'] = order_number
                receipt_url = reverse('checkout_receipt')
                return HttpResponseRedirect(receipt_url)
        else:
            error_message = 'Correct the errors below'
    else:
        if request.user.is_authenticated:
            user_profile = profile.retrieve(request)
            form = CheckoutForm(instance=user_profile)
        else:
            form = CheckoutForm()
    page_title = 'Checkout'
    return render(request, template_name, locals())


def receipt(request, template_name='checkout/receipt.html'):
    order_number = request.session.get('order_number', '')
    if order_number:
        order = Order.objects.filter(id=order_number)[0]
        order_items = OrderItem.objects.filter(order=order)
        del request.session['order_number']
    else:
        cart_url = reverse('cart:show_cart')
        return HttpResponseRedirect(cart_url)
    return render(request, template_name, locals())
