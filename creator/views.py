from datetime import datetime, timezone

from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import CreatePostForm
from clubs.models import Club


@login_required
def create_post(request):
    # Only show clubs that include the user as an owner
    if request.user.has_perm("core.add_post"):
        queryset = Club.objects.all()
    else:
        queryset = Club.objects.filter(Q(owners=request.user) | Q(posters=request.user))
        if not queryset:  # Deny if user doesn't have access to a club
            raise PermissionDenied

    if request.method == "POST":
        form = CreatePostForm(request.POST, queryset=queryset)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.post_date = datetime.now(tz=timezone.utc)
            post.save()

            messages.add_message(
                request, messages.SUCCESS, f"Posted {post.title} to {post.club}."
            )

            return redirect(
                "clubs:view_post",
                club_id=form.cleaned_data["club"].id,
                club_slug=form.cleaned_data["club"].slug,
                post_id=form.instance.id,
                post_slug=form.instance.slug,
            )
        else:
            return render(request, "form.html", {"form": form})
    else:
        form = CreatePostForm(queryset=queryset)

        context = {
            "title": "Create post",
            "pre_form": "To upload a file,"
                        " use the media manager from the club page.",
            "form": form,
        }
        return render(request, "form.html", context)
