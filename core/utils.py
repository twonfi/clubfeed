from avatar.templatetags.avatar_tags import avatar_url


def avatar_url_from_comment(comment):
    return avatar_url(comment.user)
