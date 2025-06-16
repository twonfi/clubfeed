from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.urls import reverse

from core.models import Club, Post
from .forms import EditClubForm, EditPostForm


def _redirect_club_page(club: Club, club_slug: str,
                        url: str) -> (HttpResponseRedirect | None):
    if club.slug != club_slug:
        return redirect(url, club.id, club.slug)
    return None


def _redirect_post_page(club: Club, club_slug: str, post: Post, post_slug: str,
                        url: str) -> (HttpResponseRedirect | None):
    if post.slug != post_slug or club.slug != club_slug:
        return redirect(url,
            club_id=club.id, club_slug=club_slug,
            post_id=post.id, post_slug=post.slug,)
    return None


def view_post(request, club_id, club_slug, post_id, post_slug):
    club = get_object_or_404(Club, id=club_id)
    post = get_object_or_404(Post, id=post_id)

    _r = _redirect_post_page(club, club_slug, post, post_slug,
        'clubs:view_post')
    if _r:
        return _r

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
        'edit_url': reverse('clubs:edit_post', kwargs={
            'club_id': club.id, 'club_slug': club_slug,
            'post_id': post.id, 'post_slug': post.slug,}),
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

    _r = _redirect_club_page(club, club_slug, 'clubs:club_page')
    if _r:
        return _r

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
        'elided_page_range': paginator.get_elided_page_range(),
    }

    return render(request, 'clubs/club.html', context)


def edit_club(request, club_id, club_slug):
    club = get_object_or_404(Club, id=club_id)

    _r = _redirect_club_page(club, club_slug, 'clubs:edit_club')
    if _r:
        return _r

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
            return render(request, 'form.html', {'form': form})
    else:
        form = EditClubForm(instance=club)

        context = {
            'title': f'Edit club',
            'form': form,
        }
        return render(request, 'form.html', context)


def edit_post(request, club_id, club_slug, post_id, post_slug):
    club = get_object_or_404(Club, id=club_id)
    post = get_object_or_404(Post, id=post_id)

    _r = _redirect_post_page(club, club_slug, post, post_slug,
        'clubs:edit_post')
    if _r:
        return _r

    print(post.author == request.user)

    # Check if the user is the poster, owner or has permission to modify posts
    if (not request.user.has_perm('core.edit_post')
            and not club.owners.contains(request.user)
            and not post.author == request.user):
        raise PermissionDenied

    if request.method == 'POST':
        form = EditPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()

            messages.add_message(request, messages.SUCCESS,
                f'Updated {post.title}.')

            return redirect('clubs:view_post',
                club_id=club.id, club_slug=club.slug,
                post_id=post.id, post_slug=post.slug,
            )
        else:
            return render(request, 'form.html', {'form': form})
    else:
        form = EditPostForm(instance=post)

        context = {
            'title': f'Edit post',
            'form': form,
        }
        return render(request, 'form.html', context)
