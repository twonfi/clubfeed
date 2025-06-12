from django.urls import path, include

from creator.views import create_post

app_name = 'creator'

urlpatterns = [
    path('post/', create_post, name='create_post'),
]
