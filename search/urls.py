from django.conf.urls import patterns

urlpatterns = patterns('search.views',
                       (r'^results/$', 'results', {'template_name': 'search/results.djhtml'}, 'search_results'),
                       )
