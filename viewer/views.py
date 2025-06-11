from django.core.paginator import Paginator
from django.shortcuts import render, redirect
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

    # Post actions
    if request.method == 'POST':
        if 'action-upvote-toggle' in request.POST:
            if Post.objects.filter(upvoters=request.user).exists():
                post.upvoters.remove(request.user)
            else:
                post.upvoters.add(request.user)
            post.save()

    context = {
        'title': post.title,
        'post': post,
        'upvoting': Post.objects.filter(upvoters=request.user).exists(),
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

    # Club actions
    if request.method == 'POST':
        if 'action-follow-toggle' in request.POST:
            if Club.objects.filter(followers=request.user).exists():
                club.followers.remove(request.user)
            else:
                club.followers.add(request.user)
            club.save()

    posts = Post.objects.filter(club=club).order_by('-post_date')

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': club.name,
        'club': club,
        'posts': page_obj,
        'following': Club.objects.filter(followers=request.user).exists(),
    }

    return render(request, 'viewer/club.html', context)
