from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date

class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse('home')


class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    body = models.TextField()
    slug = models.SlugField(unique=True, blank=True, default="Awsome blog")
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="blog_post")
    
    def total_likes(self):
        return self.likes.count()

    def __str__(self) -> str:
        return self.title + "|" + str(self.author)
    
    def get_absolute_url(self):
        return reverse('blogPage', args=(self.slug,))

