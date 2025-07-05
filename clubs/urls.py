from django.urls import path, include

from clubs.views import (
    view_post,
    club_list,
    club_page,
    edit_club,
    edit_post,
    media_manager,
    edit_media,
)

app_name = "clubs"

urlpatterns = [
    path("<int:club_id>-<slug:club_slug>/", include([
        path("posts/<int:post_id>-<slug:post_slug>/", include([
            path("edit/", edit_post, name="edit_post"),
            path("", view_post, name="view_post"),
        ])),
        path("edit/", edit_club, name="edit_club"),
        path("media/", include([
            path("<int:media_id>/", edit_media, name="edit_media"),
            path("", media_manager, name="media_manager"),
        ])),
        path("", club_page, name="club_page"),
    ])),
    path("", club_list, name="club_list"),
]
