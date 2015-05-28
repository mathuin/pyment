from django.shortcuts import get_object_or_404, render
from .models import Product, ProductReview
from django.core import urlresolvers
from cart.cart import add_to_cart
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from .forms import ProductAddToCartForm, ProductReviewForm
from stats import stats
from pyment.settings import PRODUCTS_PER_ROW, SITE_NAME
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
import json


def index(request, template_name='meadery/index.djhtml'):
    page_title = SITE_NAME
    search_recs = stats.recommended_from_search(request)
    featured = Product.featured.all()[0:PRODUCTS_PER_ROW]
    recently_viewed = stats.get_recently_viewed(request)
    view_recs = stats.recommended_from_views(request)
    return render(request, template_name, locals())


def show_category(request, category_value, template_name='meadery/category.djhtml'):
    try:
        intcv = int(category_value)
    except ValueError:
        return HttpResponseNotFound('<h1>Invalid category</h1>')
    names = [name for (value, name) in Product.MEAD_VIEWS if value == intcv]
    if len(names) == 0:
        return HttpResponseNotFound('<h1>Category not found</h1>')
    name = names[0]
    description = Product.MEAD_DESCRIPTIONS[intcv]
    if intcv == Product.ALL:
        products = Product.instock.all()  # .exclude(thumbnail='')
    else:
        products = Product.instock.filter(category=category_value)  # .exclude(thumbnail='')
    page_title = name
    return render(request, template_name, locals())


# new product view, with POST vs GET detection
def show_product(request, product_slug, template_name="meadery/product.djhtml"):
    p = get_object_or_404(Product, slug=product_slug)
    cname = [name for (value, name) in Product.MEAD_VIEWS if value == p.category][0]
    curl = urlresolvers.reverse('meadery_category', kwargs={'category_value': p.category})
    page_title = p.name
    # need to evaluate the HTTP method
    if request.method == 'POST':
        # add to cart...create the bound form
        postdata = request.POST.copy()
        form = ProductAddToCartForm(request, postdata)
        # check if posted data is valid
        if form.is_valid():
            add_to_cart(request)
            # if test cookie worked, get rid of it
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            url = urlresolvers.reverse('show_cart')
            return HttpResponseRedirect(url)
    else:
        # it's a GET, create the unbound form. Note request as a kwarg
        form = ProductAddToCartForm(request=request, label_suffix=':')
    # assign the hidden input the product slug
    form.fields['product_slug'].widget.attrs['value'] = product_slug
    # set the test cookie on our first GET request
    request.session.set_test_cookie()
    # log product view
    stats.log_product_view(request, p)
    # don't forget product reviews
    product_reviews = ProductReview.approved.filter(product=p).order_by('-date')
    review_form = ProductReviewForm()

    return render(request, 'meadery/product.djhtml', locals())


@login_required
def add_review(request):
    if request.method == 'POST':
        form = ProductReviewForm(request.POST)
        slug = request.POST.get('slug')
        product = Product.active.get(slug=slug)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()

            template = "meadery/product_review.djhtml"
            html = render_to_string(template, {'review': review})
            response = json.dumps({'success': 'True', 'html': html})

        else:
            html = form.errors.as_ul()
            response = json.dumps({'success': 'False', 'html': html})

        if request.is_ajax():
            return HttpResponse(response, content_type="application/javascript")
        else:
            return HttpResponseRedirect(product.get_absolute_url())
