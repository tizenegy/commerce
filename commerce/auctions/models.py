from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    title = models.CharField(
        max_length=64,
        null=False
        )
    description = models.TextField(
        max_length=1024,
        null=False
        )
    starting_bid = models.DecimalField(
        max_digits=8,
        null=False,
        decimal_places=2
        )
    image_url = models.URLField(
        null=True
        )
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE,
        null=True
        )
    watchlists = models.ManyToManyField(User, blank=True, related_name="listings_on_watchlist")
    bids = models.ManyToManyField(User, blank=True, through='Bid')
    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    listing = models.ForeignKey(
        Listing, 
        default='0',
        on_delete=models.CASCADE
        )
    user = models.ForeignKey(
        User, 
        default='0',
        on_delete=models.CASCADE
        )
    amount = models.DecimalField(
        max_digits=8,
        null=False,
        decimal_places=2,
        default='0'
        )
    # bid_datetime = models.DateTimeField(
    #     auto_now_add=True
    # )

class Comment(models.Model):
    body = models.TextField(max_length=1024, default="")
