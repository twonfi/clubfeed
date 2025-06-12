from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.urls import reverse

from core.models import Club, Post
from .forms import EditClubForm


def _redirect_club_page(club, club_slug):
    if club.slug != club_slug:
        return redirect('clubs:club_page', club.id, club.slug)


def view_post(request, club_id, club_slug, post_id, post_slug):
    club = get_object_or_404(Club, id=club_id)
    post = get_object_or_404(Post, id=post_id)

    if post.slug != post_slug or club.slug != club_slug:
        return redirect('clubs:view_post',
            club_id=club.id, club_slug=club_slug,
            post_id=post.id, post_slug=post.slug)

    upvoting = post.upvoters.contains(request.user)

    # Post actions
    if request.method == 'POST':
        if 'action-upvote-toggle' in request.POST:
            if upvoting:
                post.upvoters.remove(request.user)
                upvoting = False
            else:
                post.upvoters.add(request.user)
                upvoting = True
            post.save()

    context = {
        'title': post.title,
        'post': post,
        'upvoting': upvoting,
    }

    return render(request, 'clubs/post.html', context)


def club_list(request):
    context = {
        'title': 'All clubs',
        'clubs': Club.objects.all(),
    }

    return render(request, 'clubs/club_list.html', context)


def club_page(request, club_id, club_slug):
    club = get_object_or_404(Club, id=club_id)

    _redirect_club_page(club, club_slug)

    following = club.followers.contains(request.user)

    # Club actions
    if request.method == 'POST':
        if 'action-follow-toggle' in request.POST:
            if following:
                club.followers.remove(request.user)
                following = False
            else:
                club.followers.add(request.user)
                following = True
            club.save()

    posts = Post.objects.filter(club=club).order_by('-post_date')

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    can_edit_club = True if (
            club.owners.contains(request.user)
            or request.user.has_perm('core.change_club')) else False

    context = {
        'title': club.name,
        'club': club,
        'posts': page_obj,
        'following': following,
        'edit_club': reverse('clubs:edit_club', kwargs={
            'club_id': club.id,
            'club_slug': club.slug,
        }) if can_edit_club else False,
    }

    return render(request, 'clubs/club.html', context)


def edit_club(request, club_id, club_slug):
    club = get_object_or_404(Club, id=club_id)

    _redirect_club_page(club, club_slug)

    # Check if the user is an owner or has permission to modify clubs
    if (not request.user.has_perm('core.edit_club')
            and not club.owners.contains(request.user)):
        raise PermissionDenied

    club = get_object_or_404(Club, id=club_id)

    if request.method == 'POST':
        form = EditClubForm(request.POST, instance=club)
        if form.is_valid():
            form.save()

            messages.add_message(request, messages.SUCCESS,
                f'Updated {club.name}.')

            return redirect('clubs:club_page',
                club_id=club.id,
                club_slug=club.slug,
            )
    else:
        form = EditClubForm(instance=club)

        context = {
            'title': f'Edit club',
            'form': form,
        }
        return render(request, 'form.html', context)
