from django.urls import path, include

from clubs.views import (
    view_post,
    club_list,
    club_page,
    edit_club
)

app_name = 'clubs'

club_slug_patterns = [
    path('posts/<int:post_id>-<slug:post_slug>/',
        view_post, name='view_post'),
    path('edit/', edit_club, name='edit_club'),
    path('', club_page, name='club_page')
]

urlpatterns = [
    path('<int:club_id>-<slug:club_slug>/',
        include(club_slug_patterns)),
    path('', club_list, name='club_list'),
]
