from django.urls import path
from .views import UserRegisterView

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("listing-details/<int:listing_id>",
         views.listing_details, name="listing_details"),
    path("watchlist_add/<int:listing_id>",
         views.watchlist_add, name="watchlist_add"),
    path("watchlist/",
         views.watchlist, name="watchlist"),
    path("deactivate/<int:listing_id>",
         views.deactivate, name="deactivate"),
    path("listing-details/<int:listing_id>/comment/",
         views.add_comment, name="add_comment"),
    path("category/",
         views.category, name="category"),
    path("category_details/<int:pk>",
         views.category_details, name="category_details"),
    path("my_listings",
         views.my_listings, name="my_listings"),
    path("my_bids",
         views.my_bids, name="my_bids"),
]
