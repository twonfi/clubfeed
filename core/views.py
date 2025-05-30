from django.shortcuts import render


# noinspection PyUnusedLocal
def handler_404(request, exception):
    return render(request, 'core/404.html',
        {'title': 'Four, oh, four!'})
