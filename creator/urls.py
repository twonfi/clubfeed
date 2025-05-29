from django.urls import path

from creator.views import create_post

urlpatterns = [
    path('post/', create_post, name='create_post'),
]
