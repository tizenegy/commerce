from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User, Category, Listing

no_image_placeholder = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/480px-No_image_available.svg.png"

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
        label="", 
        empty_label='Select category',
        queryset=Category.objects.all(),
        required=False
        )


def index(request):
    all_listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": all_listings
    })

def new_listing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            listing = Listing()
            listing.title = form.cleaned_data["title"]
            listing.description = form.cleaned_data["description"]
            listing.starting_bid = form.cleaned_data["starting_bid"]
            listing.image_url = form.cleaned_data["image_url"]
            if listing.image_url == '':
                listing.image_url = no_image_placeholder
            listing.category = form.cleaned_data["category"]
            Listing.save(listing)
            all_listings = Listing.objects.all()
            return render(request, "auctions/index.html", {
                "new_listing_form": NewListingForm(),
                "listings": all_listings,
                "message": "Succesfully created new listing."
    })
        else:
            return render(request, "auctions/new_listing.html", {
                "new_listing_form": NewListingForm(),
                "message": "Invalid input, please try again."
        })
    return render(request, "auctions/new_listing.html", {
        "new_listing_form": NewListingForm()
    })

def bids(request):
    # if request.method == "POST":
    #     form = NewListingForm(request.POST)
    #     if form.is_valid():
    #         listing = Listing()
    #         listing.title = form.cleaned_data["title"]
    #         listing.description = form.cleaned_data["description"]
    #         listing.starting_bid = form.cleaned_data["starting_bid"]
    #         listing.image_url = form.cleaned_data["image_url"]
    #         if listing.image_url == '':
    #             listing.image_url = no_image_placeholder
    #         listing.category = form.cleaned_data["category"]
    #         Listing.save(listing)
    #         all_listings = Listing.objects.all()
    #         return render(request, "auctions/index.html", {
    #             "new_listing_form": NewListingForm(),
    #             "listings": all_listings,
    #             "message": "Succesfully created new listing."
    # })
    #     else:
    #         return render(request, "auctions/new_listing.html", {
    #             "new_listing_form": NewListingForm(),
    #             "message": "Invalid input, please try again."
    #     })
    # return render(request, "auctions/new_listing.html", {
    #     "new_listing_form": NewListingForm()
    # })
    pass

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auction:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auction:index"))


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
        return HttpResponseRedirect(reverse("auction:index"))
    else:
        return render(request, "auctions/register.html")

def listing(request, item_id):
    item = Listing.objects.get(pk=int(item_id))
    user = request.user
    if user.id is not None:
        on_watchlist = item.watchlists.filter(pk=int(user.id)).exists()
        return render(request, "auctions/listing.html", {
            "listing": item,
            "on_watchlist": on_watchlist
        })
    return render(request, "auctions/listing.html", {
        "listing": item,
        "on_watchlist": False
    })

def watchlist(request, item_id):
    item = Listing.objects.get(pk=int(item_id))
    user = request.user
    if user.id is not None:
        on_watchlist = item.watchlists.filter(pk=int(user.id)).exists()
        if on_watchlist:
            item.watchlists.remove(user)
            on_watchlist = False
            return render(request, "auctions/listing.html", {
                "listing": item,
                "on_watchlist": on_watchlist,
                "message": "Successfully removed from watchlist."
            })
        else:
            item.watchlists.add(user)
            on_watchlist = True
            return render(request, "auctions/listing.html", {
                "listing": item,
                "on_watchlist": on_watchlist,
                "message": "Successfully added to watchlist."
            })
    return render(request, "auctions/listing.html", {
        "listing": item,
        "on_watchlist": False,
        "message": "Successfully added to watchlist."
    })