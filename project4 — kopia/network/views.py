import json
import time

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post  # , Like, Follow


def index(request):
    return render(request, "network/index.html", {
        "posts": Post.objects.all(),
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@csrf_exempt
@login_required
def new_post(request):

    # Composing a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Check recipient emails
    data = json.loads(request.body)

    # Get contents of email
    content = data.get("new_post_textarea", "")
    author = request.user
    # time_created = '2006-10-25 14:30:59'

    post = Post(author=author, content=content)  # , time_created=time_created)

    post.save()

    return JsonResponse({"message": "Post created successfully."}, status=201)


def user_page(request, pk):

    if request.method == "GET":
        hr = JsonResponse({"error": "Email not found."})

        user = User.objects.get(pk=pk)
        # if user != request.user:

        return render(request, "network/user_page.html", {
            "users_page": user,
            "posts": Post.objects.filter(author=user),
            # "hr": json.loads(hr),
        })
    if request.method == "PUT":
        pass
