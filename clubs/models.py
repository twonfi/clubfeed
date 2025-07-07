from martor.models import MartorField
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import Group, User
from django.urls import reverse


class Club(models.Model):
    """Club model.

    A club in ClubFeed sense is some sort of group for grouping posts
    and other messages.
    They do not necessarily need to be school clubs.
    """

    name = models.CharField(unique=True, max_length=255)
    description = MartorField()
    logo = models.ImageField(upload_to="club_logos", blank=True)

    owners = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="owners", blank=True
    )
    posters = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="posters", blank=True
    )
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="followers", blank=True
    )

    always_shown = models.BooleanField(default=False)
    always_shown_for_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="always_shown_for_users",
        blank=True,
    )
    always_shown_for_groups = models.ManyToManyField(
        Group, related_name="always_shown_for_groups", blank=True
    )

    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:50]
        super(Club, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("clubs:club_page", kwargs={
            "club_id": self.id, "club_slug": self.slug})


class ClubImage(models.Model):
    """Image upload for clubs."""

    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    uploader = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
    )
    image = models.ImageField(upload_to='club_images')
    name = models.CharField('File name', max_length=255)
    alt = models.CharField('Alternative description',
        max_length=255, blank=True,
        help_text="Describe the image for screen reader users and if the"
                  " image cannot load.")
    show_on_club_page = models.BooleanField(default=False)

    def __str__(self):
        return (f'{str(self.club)}'
                f' > {str(self.image).replace('club_images/', '')}'
                f'{f' [{self.alt}]' if self.alt else ''}')


class Post(models.Model):
    """Long (blog) post model.

    This defines a blog-style post
    """

    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = MartorField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    post_date = models.DateTimeField()
    slug = models.SlugField(unique=True, blank=True)
    upvoters = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="upvoters", blank=True
    )
    allow_comments = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = (
                f"{self.post_date.date().isoformat()}-"
                f"{slugify(self.title)}"
            )[:50]
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return f"{str(self.club)} > {self.title}"

    def get_absolute_url(self):
        return reverse("clubs:view_post", kwargs={
            "club_id": self.club.id, "club_slug": self.club.slug,
            "post_id": self.id, "post_slug": self.slug})


class ShortMessage(models.Model):
    """Short message model.

    A short message is something that is more routine and more suitable
     for SMS text messages and directly in push notifications.
     These messages do not have separate pages, instead appearing on
     the main club page, and do not support Markdown.
    """

    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    post_date = models.DateTimeField()

    def __str__(self):
        return f"{str(self.club)} > {self.text}"
