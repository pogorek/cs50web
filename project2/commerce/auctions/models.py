from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    # check if user is logged in and return watchlist or None
    def watchlist_check(self):
        return self.watchlist.all()


class Category(models.Model):
    class Meta:
        # improving admin panel to display properly plural Category
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class Listing(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    winner = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE, related_name="winnerX")
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=512)
    bid_start = models.DecimalField(max_digits=12, decimal_places=2)
    bid_current = models.ForeignKey(
        'Bid', blank=True, null=True, on_delete=models.CASCADE)
    img_url = models.URLField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} | {self.author} | {self.title}"


class Bid(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid_value = models.DecimalField(max_digits=12, decimal_places=2)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} | {self.auction} | {self.bid_value}"


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=512)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s - %s" % (self.listing.title, self.author)
