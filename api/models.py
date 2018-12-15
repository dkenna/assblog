from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    title = models.CharField(max_length=64)
    text = models.TextField(blank = True)
    user = models.CharField(max_length=64, blank=True)
    creation_date = models.DateTimeField(auto_now=True)
