from django.db.models import Q

from clubs.models import Club


def can_post_context(request):
    if not request.user.is_authenticated or (
        not request.user.has_perm("core.add_post")
        and not Club.objects.filter(Q(owners=request.user) | Q(posters=request.user))
    ):
        status = False
    else:
        status = True
    return {"can_post": status}
