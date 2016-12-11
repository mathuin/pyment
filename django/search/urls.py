from django.conf.urls import url
from search.views import results

urlpatterns = [
    url(r'^results/$', results, {'template_name': 'search/results.djhtml'}, name='search_results'),
]
