from django.shortcuts import render, HttpResponse

from core.models import Post


def home(request):
    """Home sweet home."""
    if request.user.is_authenticated:
        offset = int(request.GET.get('offset')) if request.GET.get('offset') else 0

        return render(request, 'home/feed.html', context={
            'title': 'My feed',
            'h1_from_title': False,  # The template provides a hidden h1
            'posts': Post.objects.filter(club__followers=request.user).order_by('-post_date')[offset:offset+10],
        })
    else:
        # TODO: Redirect to login instead
        # return render(request, 'home/logged_out.html')
        return HttpResponse('Unauthorized.', status=401)
