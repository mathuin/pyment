from models import SearchTerm
from meadery.models import NewProduct
from django.db.models import Q
from stats import stats

STRIP_WORDS = ['a', 'an', 'and', 'by', 'for', 'from', 'in', 'no', 'not', 'of', 'on', 'or', 'that', 'the', 'to', 'with']


# store the search text in the database
def store(request, q):
    # if search term is at least three chars long, store in db
    if len(q) > 2:
        term = SearchTerm()
        term.q = q
        term.ip_address = request.META.get('REMOTE_ADDR')
        term.tracking_id = stats.tracking_id(request)
        term.user = None
        if request.user.is_authenticated():
            term.user = request.user
        term.save()


# get products matching the search text
def products(search_text):
    words = _prepare_words(search_text)
    products = NewProduct.active.all()
    results = {}
    results['products'] = []
    # iterate through keywords
    for word in words:
        products = products.filter(Q(title__icontains=word) |
                                   Q(description__icontains=word) |
                                   Q(meta_description__icontains=word) |
                                   Q(meta_keywords__icontains=word))
        results['products'] = products
    return results


# strip out common words, limit to 5 words
def _prepare_words(search_text):
    words = search_text.split()
    for common in STRIP_WORDS:
        if common in words:
            words.remove(common)
    return words[0:5]
