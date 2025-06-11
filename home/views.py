from django.core.paginator import Paginator
from django.shortcuts import render, HttpResponse

from core.models import Post


def home(request):
    """Home sweet home."""
    if request.user.is_authenticated:
        posts = Post.objects.filter(club__followers=request.user).order_by('-post_date')

        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'home/feed.html', context={
            'title': 'My feed',
            'h1_from_title': False,  # The template provides a hidden h1
            'posts': page_obj,
        })
    else:
        # TODO: Redirect to login instead
        # return render(request, 'home/logged_out.html')
        return HttpResponse('Unauthorized.', status=401)
