from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    categories = (
        ('1', 'Fashion'),
        ('2', 'Toys'),
        ('3', 'Electronics'),
        ('4', 'Home'),
        ('5', 'Sports')
    )
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=1024)
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2)
    image_url = models.URLField(max_length=256)
    category = models.CharField(max_length=64, choices=categories)

class Bid(models.Model):
    pass

class Comment(models.Model):
    pass