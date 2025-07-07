from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from .models import Profile
from .forms import EditProfileForm


def _redirect_username(
    user: User, username: str, url: str
) -> HttpResponseRedirect | None:
    if user.username != username:
        return redirect(url, user.id, user.username)
    return None


def _get_or_create_profile(user: User) -> Profile:
    return Profile.objects.get_or_create(pk=user)[0]


def user_page(request, user_id, username):
    """User page."""

    user = get_object_or_404(User, id=user_id)
    profile = _get_or_create_profile(user)

    _r = _redirect_username(user, username, "users:user_page")
    if _r:
        return _r

    can_edit_profile = (
        True
        if (
            user == request.user
            or request.user.has_perm("users.change_profile")
        )
        else False
    )

    context = {
        "title": str(user),
        "user": user,
        "profile": profile,
        # "following": following,
        "edit_profile": (
            reverse(
                "users:edit_profile",
                kwargs={
                    "user_id": user.id,
                    "username": user.username,
                },
            )
            if can_edit_profile
            else False
        ),
        "change_avatar": (
            reverse("avatar:change")
            if user == request.user
            else False
        ),
    }

    return render(request, "users/user_page.html", context)


def edit_profile(request, user_id, username):
    """This is a placeholder"""

    user = get_object_or_404(User, id=user_id)
    profile = _get_or_create_profile(user)

    _r = _redirect_username(user, username, "users:edit_profile")
    if _r:
        return _r

    if user != request.user and user.has_perm('users.change_profile'):
        raise PermissionDenied

    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()

            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.save()

            messages.add_message(request, messages.SUCCESS,
                f"Updated profile.")

            return redirect(
                "users:user_page",
                user_id=user.id,
                username=user.username,
            )
        else:
            return render(request, "form.html", {"form": form})
    else:
        form = EditProfileForm(instance=profile)

        context = {
            "title": f"Edit profile",
            "form": form,
        }
        return render(request, "form.html", context)
