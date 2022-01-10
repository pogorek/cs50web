from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("entry/", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("new_page", views.new_page, name="new_page"),
    path("error", views.error, name="error"),
    path("random_page", views.random_page, name="random_page"),
    path("edit/<str:name>", views.edit, name="edit"),
    path("wiki/<str:name>", views.entry, name="entry")
]
