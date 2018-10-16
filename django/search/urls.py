from django.urls import path
from search.views import results

app_name = 'search'
urlpatterns = [
    path('results/', results, {'template_name': 'search/results.html'}, name='search_results'),
]
