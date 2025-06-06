from django.shortcuts import render

from core.models import Post


def home(request):
    """Home sweet home."""
    if request.user.is_authenticated:
        return render(request, 'home/feed.html', context={
            'posts': Post.objects.all()
        })
    else:
        return render(request, 'home/logged_out.html')
