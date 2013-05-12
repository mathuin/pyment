from django.shortcuts import render
from django.template import RequestContext


def file_not_found_404(request):
    page_title = 'Page Not Found'
    return render(request, '404.djhtml', locals(), status=404)
