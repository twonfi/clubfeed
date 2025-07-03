from django.contrib import admin
from .models import Club, Post

admin.site.register(
    [
        Club,
        Post,
    ]
)
