from django.urls import path

from . import views

app_name = "auction"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("bids", views.bids, name="bids"),
    path("listing/<str:item_id>", views.listing, name="listing"),
    path("watchlist/<str:item_id>", views.watchlist, name="watchlist"),
    path("new_listing", views.new_listing, name="new_listing")
]
