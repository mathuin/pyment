from django.shortcuts import render


def file_not_found_404(request, exception):
    page_title = "Page Not Found"
    return render(request, "404.html", locals(), status=404)
