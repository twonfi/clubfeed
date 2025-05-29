from django.shortcuts import render, redirect, HttpResponse
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

from core.models import Club, Post


def view_post(request, club_id, club_slug, post_id, post_slug):
    try:
        club = Club.objects.get(id=club_id)
        post = Post.objects.get(id=post_id)
    except ObjectDoesNotExist:
        raise Http404

    if post.slug != post_slug or club.slug != club_slug:
        return redirect('viewer:view_post',
            club_id=club.id, club_slug=club_slug,
            post_id=post.id, post_slug=post.slug)
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


def club_page(request, club_id, club_slug):
    try:
        club = Club.objects.get(id=club_id)
    except ObjectDoesNotExist:
        raise Http404
    
    if club.slug != club_slug:
        return redirect('viewer:club_page', club.id, club.slug)

    return HttpResponse(f'Club page: {club_slug}')
