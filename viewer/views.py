from django.shortcuts import render, redirect, HttpResponse
from django.http import Http404

from core.models import Club, Post


def view_post(request, club_slug, post_id, post_slug):
    club = Club.objects.get(slug=club_slug)
    post = Post.objects.get(id=post_id, club=club)

    if not post:
        raise Http404
    elif post.slug != post_slug:
        return redirect(f'/clubs/{club_slug}/posts/{post.id}/{post.slug}/')
    else:
        context = {
            'title': post.title,
            'post': post,
        }

        return render(request, 'viewer/post.html', context)


def club_list(request):
    context = {
        'title': 'All clubs',
        'clubs': Club.objects.all(),
    }

    return render(request, 'viewer/club_list.html', context)


def club_page(request, club_slug):
    club = Club.objects.get(slug=club_slug)
    if not club:
        raise Http404

    return HttpResponse(f'Club page: {club_slug}')
