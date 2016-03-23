from django.conf.urls import url
from views import results

urlpatterns = [
    url(r'^results/$', results, {'template_name': 'search/results.djhtml'}, 'search_results'),
    ]
