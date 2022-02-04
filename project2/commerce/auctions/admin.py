from django.contrib import admin

from .models import Category, User, Listing, Bid, Comment


class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'active')


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name')


# Register your models here.
admin.site.register(Category)
admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid)
admin.site.register(Comment)
