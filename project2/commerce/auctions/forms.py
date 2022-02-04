from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Category, User, Listing, Comment, Bid
# For registration page
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ("title", "description", "bid_start", "img_url", "category",)

        # input labels | need library
        labels = {
            'title': _('Title'),
            'description': _('Description'),
            'bid_start': _('Starting bid'),
            'img_url': _('URL to image'),
            'category': _('Category'),
        }

        # help_texts = {
        #     'title': _('Some useful help text.'),
        # }
        error_messages = {
            'title': {
                'max_length': _("This text is too long."),
            },
        }

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "bid_start": forms.NumberInput(attrs={"class": "form-control"}),
            "img_url": forms.URLInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
        }


# For registration page fields update
class SignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={"class": "form-control"}))
    first_name = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name",
                  "email", "password1", "password2")

    # Add args to each field
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["class"] = "form-control"

        # Remove helptext
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
