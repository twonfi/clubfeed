from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Club(models.Model):
    """Club model.

    A club in ClubFeed sense is some sort of group for grouping posts
     and other messages. They do not necessarily need to be school
     clubs.
    """
    name = models.CharField(unique=True)
    description = models.TextField()

    owners = models.ManyToManyField(settings.AUTH_USER_MODEL)

    slug = models.SlugField(unique=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Club, self).save(*args, **kwargs)


    def __str__(self):
        return self.name


class Post(models.Model):
    """Long (blog) post model.

    This defines a blog-style post
    """
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    title = models.CharField()
    body = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    post_date = models.DateTimeField()
    slug = models.SlugField(unique=True, blank=True)
    upvotes = models.PositiveIntegerField(default=0)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = (f'{self.post_date.date().isoformat()}-'
                         f'{slugify(self.title)}')
        super(Post, self).save(*args, **kwargs)


    def __str__(self):
        return f'{str(self.club)} > {self.title}'