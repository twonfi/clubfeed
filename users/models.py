from martor.models import MartorField
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Profile(models.Model):
    """User profile.

    This is used to store additional information for users that cannot
     be stored in the base user object.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE,
        primary_key=True)
    description = MartorField(blank=True)

    class Meta:
        default_permissions = ("view", "change")

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse("users:user_page", kwargs={
            "user_id": self.user.id,
            "username": self.user.username,
        })
