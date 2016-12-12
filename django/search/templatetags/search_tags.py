from django import template
from search.forms import SearchForm
import urllib.request
import urllib.parse
import urllib.error

register = template.Library()


@register.inclusion_tag("tags/search_box.djhtml")
def search_box(request):
    q = request.GET.get('q', '')
    form = SearchForm({'q': q})
    return {'form': form}


@register.inclusion_tag('tags/pagination_links.djhtml')
def pagination_links(request, paginator):
    raw_params = request.GET.copy()
    page = raw_params.get('page', 1)
    p = paginator.page(page)
    try:
        del raw_params['page']
    except KeyError:
        pass
    params = urllib.parse.urlencode(raw_params)
    return {'request': request,
            'paginator': paginator,
            'p': p,
            'params': params}
