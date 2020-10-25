from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User, Category

class NewListingForm(forms.Form):
    title = forms.CharField(
        label="", 
        widget=forms.TextInput(attrs={'placeholder':'Title'}),
        required=True
        )
    description = forms.CharField(
        label="", 
        widget=forms.Textarea(attrs={'placeholder':'Description'}),
        required=True
        )
    starting_bid = forms.DecimalField(
        label="",
        widget=forms.NumberInput(attrs={'placeholder': 'Starting bid'}),
        required=True
        )
    image_url = forms.URLField(
        label="",
        widget=forms.TextInput(attrs={'placeholder': 'Image URL'}),
        required=False
        )
    category = forms.ModelChoiceField(
        label="Category", 
        queryset=Category.objects.all()
        )


def index(request):
    return render(request, "auctions/index.html")

def new_listing(request):
    return render(request, "auctions/new_listing.html", {
        "new_listing_form": NewListingForm()
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
