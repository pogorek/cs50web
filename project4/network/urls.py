from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("data/", views.index_data, name="index_data"),
    path("data/<int:current_page>/", views.index_data, name="index_data"),

    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post/", views.new_post, name="new_post"),
    path("user_page/<int:pk>", views.user_page, name="user_page"),
    path("user_page_data/<int:pk>", views.user_page_data, name="user_page_data"),
    path("user_page_data/<int:pk>/<int:current_page>/",
         views.user_page_data, name="user_page_data"),
    path('follow_user/', views.follow_user, name="follow_user"),
    path('like_unlike/', views.like_unlike_post, name="like_unlike"),
    path('save_post/', views.save_post, name="save_post"),

    path("follow_page/", views.follow_page, name="follow_page"),
    path("follow_page_data/",
         views.follow_page_data, name="follow_page_data"),
    path("follow_page_data/<int:current_page>/",
         views.follow_page_data, name="follow_page_data"),
]
