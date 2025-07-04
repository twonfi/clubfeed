from django.contrib import admin
from .models import Club, Post, ClubImage

admin.site.register(
    [
        Club,
        Post,
        ClubImage,
    ]
)
