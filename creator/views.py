from datetime import datetime, timezone

from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied

from .forms import CreatePostForm
from core.models import Club


def create_post(request):
    # Only show clubs that include the user as an owner
    if request.user.is_staff or request.user.is_superuser:
        # Staff and superusers have admin access anyway
        queryset = Club.objects.all()
    else:
        queryset = Club.objects.filter(owners=request.user.id)
        if not queryset:
            raise PermissionDenied

    if request.method == 'POST':
        form = CreatePostForm(request.POST, queryset=queryset)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.post_date = datetime.now(tz=timezone.utc)
            post.save()

            return redirect('viewer:view_post',
                club_slug=form.cleaned_data['club'].slug,
                post_id=form.instance.id,
                post_slug=form.instance.slug,
            )
    else:
        form = CreatePostForm(queryset=queryset)

    context = {
        'title': 'Create post',
        'form': form,
    }
    return render(request, 'creator/post.html', context)
