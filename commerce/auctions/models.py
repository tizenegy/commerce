from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=1024)
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2)
    image_url = models.URLField(max_length=256)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    pass

class Comment(models.Model):
    pass
