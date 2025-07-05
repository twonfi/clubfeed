def media_access(user, club = None) -> str:
    """Return a c/r/u/d/p (create, read, update, delete, club page)
    value based on the user's access to media.

    :type user: django.contrib.auth.models.User
    :type club: clubs.models.Club
    """

    access = ""

    if club:
        if club.owners.contains(user):
            access += "crudp"
        if club.posters.contains(user):
            access += "cr"

    if user.has_perm("clubs:add_media_file"):
        access += "c"
    if user.has_perm("clubs:view_media_file"):
        access += "r"
    if user.has_perm("clubs:edit_media_file"):
        access += "up"
    if user.has_perm("clubs:delete_media_file"):
        access += "d"

    return access
