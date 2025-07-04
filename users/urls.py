from django.urls import path, include

from .views import user_page, edit_profile

app_name = "users"

urlpatterns = [
    path(
        "<int:user_id>-<str:username>/",
        include(
            [
                path("edit/", edit_profile, name="edit_profile"),
                path("", user_page, name="user_page"),
            ]
        )
    ),
]
