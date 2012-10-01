# Create your views here.
from django.shortcuts import render
from django.http import HttpResponseRedirect
from checkout import checkout
import cart

def show_cart(request, template_name="cart/cart.djhtml"):
    if request.method == 'POST':
        postdata = request.POST.copy()
        if postdata['submit'] == 'Remove':
            cart.remove_from_cart(request)
        if postdata['submit'] == 'Update':
            cart.update_cart(request)
        if postdata['submit'] == 'Checkout':
            checkout_url = checkout.get_checkout_url(request)
            return HttpResponseRedirect(checkout_url)

    cart_items = cart.get_cart_items(request)
    page_title = 'Shopping Cart'
    return render(request, template_name, locals())
