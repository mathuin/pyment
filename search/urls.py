from django.conf.urls.defaults import patterns

urlpatterns = patterns('search.views',
                       (r'^results/$','results', {'template_name': 'search/results.djhtml'}, 'search_results'),
                       )
