from django.shortcuts import render
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from search import search
from pyment import settings


def results(request, template_name="search/results.djhtml"):
    # get current search phrase
    q = request.GET.get('q', '')
    # get current page number. Set to 1 is missing or invalid
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1
    # retrieve the matching products
    matching = search.products(q).get('products')
    # generate the pagintor object
    paginator = Paginator(matching, settings.PRODUCTS_PER_PAGE)
    try:
        results = paginator.page(page).object_list
    except (InvalidPage, EmptyPage):
        results = paginator.page(1).object_list
    # store the search
    search.store(request, q)
    # the usual...
    page_title = 'Search Results for: ' + q
    return render(request, template_name, locals())
