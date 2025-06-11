from django.shortcuts import render, HttpResponse

from core.models import Post


def home(request):
    """Home sweet home."""
    if request.user.is_authenticated:
        return render(request, 'home/feed.html', context={
            'posts': Post.objects.all().order_by('-post_date')
        })
    else:
        # TODO: Redirect to login instead
        # return render(request, 'home/logged_out.html')
        return HttpResponse('Unauthorized.', status=401)
