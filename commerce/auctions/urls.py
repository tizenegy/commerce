from django.urls import path
from . import views

app_name = "auction"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("bids/<str:item_id>", views.bids, name="bids"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category_id>", views.bids, name="category"),
    path("comment/<str:item_id>", views.comment, name="comment"),
    path("listing/<str:item_id>", views.listing, name="listing"),
    path("view_watchlist", views.view_watchlist, name="view_watchlist"),
    path("watchlist/<str:item_id>", views.watchlist, name="watchlist"),
    path("new_listing", views.new_listing, name="new_listing")
]
