from django.db import models
from django.db.models.fields import CharField
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextField(blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    # adding snippet
    snippet = models.CharField(max_length=500)
    # User on delete delete their post also
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # ALWAYS RUN "python manage.py makemigrations" WHENEVER THEIR IS CHANGE IN DATABASE
    # adding like functions here ->
    likes = models.ManyToManyField(User, related_name="blog_posts")
    # adding image/header image to our post
    header_image = models.ImageField(
        null=True, blank=True, upload_to="images/")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})

    def total_like(self):
        return self.likes.count()
