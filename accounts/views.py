from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from checkout.models import Order, OrderItem
from django.contrib.auth.decorators import login_required
from accounts.forms import UserProfileForm
from accounts import profile

def register(request, template_name="registration/register.djhtml"):
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = UserCreationForm(postdata)
        if form.is_valid():
            form.save()
            un = postdata.get('username','')
            pw = postdata.get('password1','')
            from django.contrib.auth import login, authenticate
            new_user = authenticate(username=un, password=pw)
            if new_user and new_user.is_active:
                login(request, new_user)
                url = urlresolvers.reverse('my_account')
                return HttpResponseRedirect(url)
    else:
        form = UserCreationForm()
    page_title = 'User Registration'
    return render(request, template_name, locals())

@login_required
def my_account(request, template_name="registration/my_account.djhtml"):
    page_title = 'My Account'
    orders = Order.objects.filter(user=request.user)
    name = request.user.username
    return render(request, template_name, locals())

@login_required
def order_details(request, order_id, template_name="registration/order_details.djhtml"):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    page_title = 'Order Details for Order #' + order_id
    order_items = OrderItem.objects.filter(order=order)
    return render(request, template_name, locals())

@login_required
def order_info(request, template_name="registration/order_info.djhtml"):
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = UserProfileForm(postdata)
        if form.is_valid():
            profile.set(request)
            url = urlresolvers.reverse('my_account')
            return HttpResponseRedirect(url)
    else:
        user_profile = profile.retrieve(request)
        form = UserProfileForm(instance=user_profile)
    page_title = 'Edit Order Information'
    return render(request, template_name, locals())
