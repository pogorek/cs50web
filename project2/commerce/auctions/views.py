from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic

from .forms import ListingForm, SignUpForm
from .models import Category, User, Listing, Comment, Bid

# Constant with query for all categories
CATEGORIES = Category.objects.all()


class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")
    # LOGIN_REDIRECT_URL = 'home' w settings.py


def index(request):
    """ Main page. """
    return render(request, "auctions/index.html", {
        "categories": CATEGORIES,
        "listings": Listing.objects.filter(active=True),
    })


def login_view(request):
    """ Login page """
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
            messages.error(request, "Invalid username and/or password.")
            return render(request, "auctions/login.html", {
                "categories": CATEGORIES,
            })
    else:
        return render(request, "auctions/login.html", {
            "categories": CATEGORIES,
        })


def logout_view(request):
    """ Logout function """
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    """ Register page """
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            messages.error(request, "Passwords must match.")
            return render(request, "auctions/register.html", {
                "categories": CATEGORIES,
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.error(request, "Username already taken.")
            return render(request, "auctions/register.html", {
                "categories": CATEGORIES,
            })
        login(request, user)
        messages.success(
            request, "Registered successfully!")
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html", {
            "categories": CATEGORIES,
        })


@login_required(login_url='login')
def new_listing(request):
    """ New listing page """
    if request.method == "POST":
        # Take in the data the user submitted and save it as form
        form = ListingForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():

            # Isolate the input from the 'cleaned' version of form data
            author = request.user
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            bid_start = form.cleaned_data["bid_start"]
            img_url = form.cleaned_data["img_url"]
            if img_url == None:
                img_url = "https://kaverisias.com/wp-content/uploads/2018/01/catalog-default-img.gif"
            category = form.cleaned_data["category"]
            # Create new Listing
            Listing.objects.create(title=title, author=author, description=description,
                                   bid_start=bid_start, category=category, img_url=img_url)

            # Redirect user to Index Page
            messages.success(
                request, "SUCCESS! New listing created.")
            return HttpResponseRedirect(reverse("index"))
        # If the form is invalid
        else:
            # Re-render the page with existing information.
            messages.error(request, "Something went wrong.")
            return render(request, "auctions/new_listing.html", {
                "categories": CATEGORIES,
                "form": ListingForm(),
            })
    # if method GET
    else:
        return render(request, "auctions/new_listing.html", {
            "categories": CATEGORIES,
            "form": ListingForm(),
        })


def listing_details(request, listing_id):
    """ Show listing page """
    # get vars
    if request.user.is_authenticated:
        watch = request.user.watchlist.filter(pk=listing_id)
    else:
        watch = None
    user = request.user
    listing = Listing.objects.get(pk=listing_id)
    # Filter to current listing, get highest bid
    bids = Bid.objects.filter(
        auction=listing_id).order_by('-bid_value').first()
    comments = Comment.objects.filter(
        listing=listing_id).order_by('-time_created')

    # If listing not active and user is winner
    if not listing.active and request.user == bids.author:
        messages.info(
            request, "You won this auction. Congratulations!")

    if request.method == "POST":
        # Get values from form
        new_bid = float(request.POST["bid"])
        # check if there are no bids yet and if new bid is higher then starting price
        if listing.bid_current == None and listing.bid_start <= new_bid:
            # Create bid and update listing
            bid = Bid.objects.create(
                author=user, auction=listing, bid_value=new_bid)
            Listing.objects.filter(pk=listing_id).update(bid_current=bid)
            messages.success(
                request, "New bid placed successfully.")
        # Check if there are bids and if new one is higher then current one
        elif listing.bid_current:
            if listing.bid_current.bid_value < new_bid:
                # Create bid and update listing
                bid = Bid.objects.create(
                    author=user, auction=listing, bid_value=new_bid)
                Listing.objects.filter(
                    pk=listing_id).update(bid_current=bid)
                messages.success(
                    request, "New bid placed successfully.")
            else:
                messages.error(
                    request, "New bid must be higher then current price.")
        else:
            messages.error(
                request, "New bid must be higher then current price.")
        # update vars
        listing = Listing.objects.get(pk=listing_id)
        bids = Bid.objects.filter(
            auction=listing_id).order_by('-bid_value').first()

        return render(request, "auctions/listing_details.html", {
            "categories": CATEGORIES,
            "new_bid": new_bid,
            "user": user,
            "listing": listing,
            "bids": bids,
        })

    # If method GET
    else:
        return render(request, "auctions/listing_details.html", {
            "categories": CATEGORIES,
            "listing": Listing.objects.get(pk=listing_id),
            "watch": watch,
            "bids": bids,
            "comments": comments,
        })


@ login_required(login_url='login')
def watchlist_add(request, listing_id):
    """ Add or remove from watchlist """
    # Check if listing is in watchlist
    if request.user.watchlist.filter(pk=listing_id).exists():
        # Remove from watchlist
        request.user.watchlist.remove(listing_id)
        messages.success(request, "Auction removed from Watchlist.")
    # If listing is not in watchlist
    else:
        # Add to watchlist
        request.user.watchlist.add(listing_id)
        messages.success(request, "Auction added to Watchlist.")

    return HttpResponseRedirect(reverse("listing_details", args=[str(listing_id)]))


@ login_required(login_url='login')
def deactivate(request, listing_id):
    """ Finish auction """
    # Check if listing is active
    if Listing.objects.get(pk=listing_id).active == True:
        # Check if Listing has no bids > Update Listing
        if not Bid.objects.filter(auction=listing_id).first():
            Listing.objects.filter(pk=listing_id).update(
                active=False, winner=None)
        # If there are bids
        else:
            # Get from Listing User with highest Bid
            winner = Bid.objects.filter(
                auction=listing_id).order_by('-bid_value').first().author
            # Update listing
            Listing.objects.filter(pk=listing_id).update(
                active=False, winner=winner)

        messages.success(request, "Auction ended.")
    # If Listing is not active
    # else:
    #     Listing.objects.filter(pk=listing_id).update(
    #         active=True, winner=None)
    #     messages.success(request, "Auction started.")

    return HttpResponseRedirect(reverse("listing_details", args=[str(listing_id)]))


@ login_required(login_url='login')
def add_comment(request, listing_id):
    """ Add comment """
    # Get comment from form
    text = request.POST["comment"]
    # Check if there was text in form
    if text:
        author = request.user
        listing = Listing.objects.get(pk=listing_id)
        Comment.objects.create(listing=listing, author=author, text=text)
        messages.success(request, "Comment added.")
    # If no text
    else:
        messages.error(request, "You must provide comment text.")
    return HttpResponseRedirect(reverse("listing_details", args=[str(listing_id)]))


@ login_required(login_url='login')
def watchlist(request):
    """ Watchlist page """
    watchlist = request.user.watchlist_check()

    return render(request, "auctions/watchlist.html", {
        "categories": CATEGORIES,
        "watchlist": watchlist,
    })


def category(request):
    """ All categories page """

    return render(request, "auctions/category.html", {
        "categories": CATEGORIES,
    })


def category_details(request, pk):
    """ Single category with listings page """
    category = Category.objects.get(pk=pk)
    posts = Listing.objects.filter(category=pk)

    return render(request, "auctions/category_details.html", {
        "categories": CATEGORIES,
        "category": category,
        "posts": posts,
    })


@ login_required(login_url='login')
def my_listings(request):
    """ My listings page """
    listings = Listing.objects.filter(author=request.user)

    return render(request, "auctions/my_listings.html", {
        "categories": CATEGORIES,
        "listings": listings,
    })


@ login_required(login_url='login')
def my_bids(request):
    """ My bids page """

    # Query for all Listings user won
    listings = Listing.objects.filter(winner=request.user)

    # Raw query to select all auctions where user is bidding | convert to list
    bids = list(Bid.objects.raw(
        "SELECT id, auction_id FROM auctions_bid GROUP BY auction_id HAVING author_id=%s;", [request.user.id]))
    print(bids)

    return render(request, "auctions/my_bids.html", {
        "categories": CATEGORIES,
        "listings": listings,
        "bids": bids,
    })
