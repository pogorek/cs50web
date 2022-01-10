from django import forms
from django.shortcuts import render
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse

# for changing markdown to html
import markdown2
import random
from random import seed

# temp
from django.http import HttpResponse

# class for search form
class NewEntry(forms.Form):
    entry = forms.CharField(widget=forms.TextInput(attrs={'class': 'search'}))

# class for new page
class NewPage(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control new_page'}))
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control new_page'}))

# main page for GET, search for POST
def index(request):
    # # if request by POST
    # if request.method == "POST":
    #     # save form to form
    #     form = NewEntry(request.POST)
    #     # make empty list for all matches
    #     found = []
    #     # check if form entry is valid
    #     if form.is_valid():
    #         # save users entry as string
    #         entry_search = form.cleaned_data["entry"]
    #         # get all entries to a list
    #         all_entries = util.list_entries()
    #         # loop for all entries in database
    #         for one in all_entries:
    #             # if users entry matches one of existing entries
    #             if entry_search.lower() == one.lower():
    #                 # convert md to html and return page
    #                 html = markdown2.markdown(util.get_entry(entry_search))
    #                 return render(request, "encyclopedia/entry.html", {
    #                     "name": entry_search,
    #                     "entry": html
    #                 })
    #             # if users entry is part of existing entry add it to found list
    #             elif entry_search.lower() in one.lower():
    #                 found.append(one)
    #         # if there were no matches return NO RESULTS
    #         if len(found) == 0:
    #             return render(request, "encyclopedia/search.html", {
    #                 "entries": found,
    #                 "form": NewEntry(),
    #                 "entry_search": entry_search
    #             })
    #         # else return page with all matches
    #         # return HttpResponse(f"YES is VALID, all: {all_entries}<br>entry: {entry_search}<br>match: {found}")
    #         return render(request, "encyclopedia/search.html", {
    #             "entries": found,
    #             "form": NewEntry(),
    #             "entry_search": entry_search
    #         })
    #
    #     # if form entry is not valid
    #     else:
    #         return render(request, "encyclopedia/search.html", {
    #             "entries": found,
    #             "form": NewEntry(),
    #             "entry_search": ""
    #         })
    #
    # else:
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewEntry()
    })

# displaying every entry from wiki
def entry(request, name):
    if util.get_entry(name):
        html = markdown2.markdown(util.get_entry(name))
        return render(request, "encyclopedia/entry.html", {
            "name": name,
            "entry": html
            })
    else:
        html = "<h1>Page does not exist</h1>"
        return render(request, "encyclopedia/entry.html", {
            "name": name,
            "entry": html
        })

def search(request):
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
                    return render(request, "encyclopedia/entry.html", {
                        "name": entry_search,
                        "entry": html
                    })
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
            return render(request, "encyclopedia/search.html", {
                "entries": found,
                "form": NewEntry(),
                "entry_search": entry_search
            })

        # if form entry is not valid
        else:
            return render(request, "encyclopedia/search.html", {
                "entries": found,
                "form": NewEntry(),
                "entry_search": ""
            })
    else:
        return HttpResponseRedirect(reverse("index"))

def new_page(request):
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
                    # return HttpResponse("Juz istnieje")
                    return HttpResponseRedirect(reverse("error"))

            # var for all page content
            content = f"# {new_title}\n\n{new_text}"
            # saving new entry to disk
            util.save_entry(new_title, content)

            # returning new entry page
            if util.get_entry(new_title):
                html = markdown2.markdown(util.get_entry(new_title))
                return render(request, "encyclopedia/entry.html", {
                    "name": new_title,
                    "entry": html
                })
            # return HttpResponse(f"OK<br># {new_title}\n\n{new_text}")
        else:
            return HttpResponse("NO")

    else:
        return render(request, "encyclopedia/new_page.html", {
            "form": NewEntry(),
            "form_page": NewPage()
        })

def error(request):
    return render(request, "encyclopedia/error.html")

def random(request):
    entries = util.list_entries()
    seed(1)
    # ran = random.randint(1, len(entries))
    ran_entry = random.choice(entries)
    if util.get_entry(ran_entry):
        html = markdown2.markdown(util.get_entry(ran_entry))
        return render(request, "encyclopedia/entry.html", {
            "name": ran_entry,
            "entry": html
            })
