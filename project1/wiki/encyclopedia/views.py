from django import forms
from django.shortcuts import render
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse

# for changing markdown to html
import markdown2
# for random page
import random

# class for search form
class NewEntry(forms.Form):
    entry = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'search'}))

# class for new page
class NewPage(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control new_page'}))
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control new_page'}))

# class for edit page
class EditPage(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control new_page'}))


# main page for GET, search for POST
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewEntry()
    })

def entry(request, name):
    """ Displaying every entry from wiki """
    # check if entry exist
    if util.get_entry(name):
        html = markdown2.markdown(util.get_entry(name))
        return render(request, "encyclopedia/entry.html", {
            "name": name,
            "entry": html,
            "form": NewEntry()
            })
    # if entry does not exist
    else:
        html = "Page does not exist"
        return render(request, "encyclopedia/error.html", {
            "message": html,
            "form": NewEntry()
        })

def search(request):
    """ Searching entries via textfield """
    # if request by POST
    if request.method == "POST":
        # save form to form
        form = NewEntry(request.POST)
        # make empty list for all matches
        found = []
        # check if form entry is valid
        if form.is_valid():
            # save users entry as string
            entry_search = form.cleaned_data["entry"]
            # get all entries to a list
            all_entries = util.list_entries()
            # loop for all entries in database
            for one in all_entries:
                # if users entry matches one of existing entries
                if entry_search.lower() == one.lower():
                    # convert md to html and return page
                    html = markdown2.markdown(util.get_entry(entry_search))
                    return HttpResponseRedirect(reverse("entry", args=[entry_search]))
                # if users entry is part of existing entry add it to found list
                elif entry_search.lower() in one.lower():
                    found.append(one)
            # if there were no matches return NO RESULTS
            if len(found) == 0:
                return render(request, "encyclopedia/search.html", {
                    "entries": found,
                    "form": NewEntry(),
                    "entry_search": entry_search
                })
            # else return page with all matches
            else:
                return render(request, "encyclopedia/search.html", {
                    "entries": found,
                    "form": NewEntry(),
                    "entry_search": entry_search
                })
        # if form entry is not valid
        else:
            html = "Invalid input"
            return render(request, "encyclopedia/error.html", {
                "message": html,
                "form": NewEntry()
            })
    else:
        return HttpResponseRedirect(reverse("index"))

def new_page(request):
    """ Creating new entry """
    if request.method == "POST":
        # save form to form
        form_page = NewPage(request.POST)
        # check if form entry is valid
        if form_page.is_valid():
            # get title and text to vars
            new_title = form_page.cleaned_data["title"]
            new_text = form_page.cleaned_data["text"]
            # check if entry already exist
            for one in util.list_entries():
                if new_title.lower() == one.lower():
                    html = "Page already exist"
                    return render(request, "encyclopedia/error.html", {
                        "message": html,
                        "form": NewEntry()
                    })
            # var for all page content
            content = f"# {new_title}\n\n{new_text}"
            # saving new entry to disk
            util.save_entry(new_title, content)

            # double check entry and return new entry page
            if util.get_entry(new_title):
                html = markdown2.markdown(util.get_entry(new_title))
                return render(request, "encyclopedia/entry.html", {
                    "name": new_title,
                    "entry": html
                })
            # if entry does not exist
            else:
                html = "Page does not exist"
                return render(request, "encyclopedia/error.html", {
                    "message": html,
                    "form": NewEntry()
                })
        # if input is not valid
        else:
            html = "Invalid input"
            return render(request, "encyclopedia/error.html", {
                "message": html,
                "form": NewEntry()
            })
    # if method GET render new page
    else:
        return render(request, "encyclopedia/new_page.html", {
            "form": NewEntry(),
            "form_page": NewPage()
        })

def error(request, message):
    """ Display error messages """
    return render(request, "encyclopedia/error.html", {
        "message": message
    })

def random_page(request):
    """ Return random page """
    # get all entries
    entries = util.list_entries()
    # save random entry to var
    ran_entry = random.choice(entries)
    # double checking if entry exist
    if util.get_entry(ran_entry):
        # convert md to html and return page
        html = markdown2.markdown(util.get_entry(ran_entry))
        return render(request, "encyclopedia/entry.html", {
            "name": ran_entry,
            "entry": html,
            "form": NewEntry()
            })
    # if entry does not exist
    else:
        html = "Page does not exist"
        return render(request, "encyclopedia/error.html", {
            "message": html,
            "form": NewEntry()
        })

def edit(request, name):
    """ Edit entry """
    if request.method == "POST":
        # save form to form
        edit_page = EditPage(request.POST)
        # check if form input is valid
        if edit_page.is_valid():
            # get text to var
            new_text = edit_page.cleaned_data["text"]
            # save new entry to disk
            util.save_entry(name, new_text)
            # double check and return new entry page
            if util.get_entry(name):
                html = markdown2.markdown(util.get_entry(name))
                return render(request, "encyclopedia/entry.html", {
                    "name": name,
                    "entry": html
                })
            # if entry does not exist
            else:
                html = "Page does not exist"
                return render(request, "encyclopedia/error.html", {
                    "message": html,
                    "form": NewEntry()
                })
        # if input is not valid
        else:
            html = "Invalid input"
            return render(request, "encyclopedia/error.html", {
                "message": html,
                "form": NewEntry()
            })
    # if method GET
    else:
        # check if entry exist
        if util.get_entry(name):
            # save md text to var and return page
            entry_text = util.get_entry(name)
            return render(request, "encyclopedia/edit.html", {
                "name": name,
                "form": NewEntry(),
                "form_edit": EditPage(initial={"text": entry_text})
            })
        # if entry does not exist
        else:
            html = "Page does not exist"
            return render(request, "encyclopedia/error.html", {
                "message": html,
                "form": NewEntry()
            })
