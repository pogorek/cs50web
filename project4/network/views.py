import json

from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Follow

num_pages = 10


def index(request):
    return render(request, "network/index.html")


def index_data(request, current_page=1):
    if request.method == "GET":

        qs = Post.objects.all()
        p = Paginator(qs, num_pages)
        page = p.page(current_page)
        page_list = p.page(current_page).object_list

        p_data = {
            "pages": [],
            "num_pages": p.num_pages,
            "previous": page.has_previous(),
            "next": page.has_next(),
            "current_page": current_page
        }

        # pagination
        for obj in page_list:
            item = {
                'id': obj.id,
                'author': obj.author.username,
                'author_id': obj.author.id,
                'content': obj.content,
                'liked': True if request.user in obj.likes.all() else False,
                'count': obj.likes_count,
                'time_created': obj.created,
                'user': request.user.id,
            }
            p_data["pages"].append(item)

        return JsonResponse({"p_data": p_data})


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

    post = Post(author=author, content=content)  # , time_created=time_created)
    post.save()

    return JsonResponse({"message": "Post created successfully."}, status=201)


def user_page(request, pk):
    if request.method == "GET":
        return render(request, "network/user_page.html")
    else:
        return JsonResponse({"error": "Something went wrong"})


def user_page_data(request, pk, current_page=1):
    if request.method == "GET":
        user = User.objects.get(pk=pk)
        posts = Post.objects.filter(author=user)
        visitor = user != request.user and request.user.is_authenticated
        # print(request.user.is_authenticated)

        p = Paginator(posts, num_pages)
        page = p.page(current_page)
        page_list = p.page(current_page).object_list
        data = []
        p_data = {
            "pages": [],
            "num_pages": p.num_pages,
            "previous": page.has_previous(),
            "next": page.has_next(),
            "current_page": current_page
        }

        # pagination
        for obj in page_list:
            item = {
                'id': obj.id,
                'author': obj.author.username,
                'author_id': obj.author.id,
                'content': obj.content,
                'liked': True if request.user in obj.likes.all() else False,
                'count': obj.likes_count,
                'time_created': obj.created,
                'user': request.user.id,
            }
            p_data["pages"].append(item)

        follow = []

        for obj in user.followers_in():
            item = obj.follower.id
            # item = {
            #     'id': obj.follower.id,
            #     'username': obj.follower.username,
            # }
            follow.append(item)

        user_data = {
            "id": user.id,
            "username": user.username,
            "followers": user.followers(),
            "following": user.following,
            "follow": follow,
        }

        data = []
        for obj in posts:
            item = {
                'id': obj.id,
                'author': obj.author.username,
                'author_id': obj.author.id,
                'content': obj.content,
                'liked': True if request.user in obj.likes.all() else False,
                'count': obj.likes_count,
                'time_created': obj.created,
            }
            data.append(item)
        return JsonResponse({
            "posts": data,
            "visitor": visitor,
            "user": user_data,
            "user_id": request.user.id,
            "p_data": p_data,
        })

    if request.method == "PUT":
        pass


@csrf_exempt
def follow_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        data = data["pk"]
        owner = User.objects.get(pk=data)
        follower = request.user

        followers = Follow.objects.filter(user=owner)
        # print(followers[0].follower)
        for fol in followers:
            if fol.follower == follower:
                fol.delete()
                return JsonResponse({'result': "deleted", })

        follow = Follow(user=owner, follower=follower,)
        follow.save()
        return JsonResponse({'result': "added", })


@csrf_exempt
def like_unlike_post(request):
    # if request.is_ajax(): # doesn't work work - obsolete
    if request.method == 'POST':
        data = json.loads(request.body)
        pk = data["pk"]
        obj = Post.objects.get(pk=pk)
        if request.user in obj.likes.all():
            liked = False
            obj.likes.remove(request.user)
        else:
            liked = True
            obj.likes.add(request.user)

    return JsonResponse({'liked': liked, 'count': obj.likes_count})


@csrf_exempt
def save_post(request):
    data = json.loads(request.body)
    pk = data["pk"]
    content = data["content"]
    post = Post.objects.get(pk=pk)
    if post.author == request.user:
        post.content = content
        post.save()
        content = {
            'id': post.id,
            'author': post.author.username,
            'author_id': post.author.id,
            'content': post.content,
            'liked': True if request.user in post.likes.all() else False,
            'count': post.likes_count,
            'time_created': post.created,
            'user': request.user.id,
        }

    return JsonResponse({"data": content})


def follow_page(request):
    return render(request, "network/follow_page.html")


def follow_page_data(request, current_page=1):
    if request.method == "GET":
        pk = request.user.pk
        user_following = User.objects.get(pk=pk)
        all_users = list(User.objects.all())
        user_following_list = Follow.objects.filter(follower=user_following)

        for user in user_following_list:
            all_users.remove(user.user)

        qs = list(Post.objects.all())
        qs[:] = [x for x in qs if not x.author in all_users]

        p = Paginator(qs, num_pages)
        page = p.page(current_page)
        page_list = p.page(current_page).object_list
        data = []
        p_data = {
            "pages": [],
            "num_pages": p.num_pages,
            "previous": page.has_previous(),
            "next": page.has_next(),
            "current_page": current_page,
            'user': request.user.username,
        }

        # pagination
        for obj in page_list:
            item = {
                'id': obj.id,
                'author': obj.author.username,
                'author_id': obj.author.id,
                'content': obj.content,
                'liked': True if request.user in obj.likes.all() else False,
                'count': obj.likes_count,
                'time_created': obj.created,
                'user': request.user.id,
            }
            p_data["pages"].append(item)

        # old
        for obj in qs:
            item = {
                'id': obj.id,
                'author': obj.author.username,
                'author_id': obj.author.id,
                'content': obj.content,
                'liked': True if request.user in obj.likes.all() else False,
                'count': obj.likes_count,
                'time_created': obj.created,
                'user': request.user.id,
            }
            data.append(item)
        return JsonResponse({'data': data, "p_data": p_data})
