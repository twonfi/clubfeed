from martor.models import MartorField
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """User profile.

    This is used to store additional information for users that cannot
     be stored in the base user object.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE,
        primary_key=True)
    picture = models.ImageField()
    description = MartorField()
