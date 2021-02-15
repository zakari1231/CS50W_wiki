import secrets

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from . import util

from markdown2 import Markdown


app_name = 'wiki_app'
markdowner = Markdown()

class Search(forms.Form):
    search = forms.CharField(label='Search Encyclopedia',widget=forms.TextInput(attrs={'placeholder': 'Search ...'}))

class New_entry(forms.Form):
    title = forms.CharField(label='title ',widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    textarea = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'text area here ...', 'rows': 5,'cols': 40, 'style': 'height: 10em;'}))

def index(request):
    markdowner = Markdown()
    searched = []
    entries = util.list_entries()
    if request.method =="POST":
        form = Search(request.POST)
        if form.is_valid():
            search = form.cleaned_data["search"]
            entries_context = util.get_entry(search)
            for i in entries:
                if search in entries:
                    page = util.get_entry(search)
                    converted_page = markdowner.convert(page)
                    dicts = {
                        'page': page,
                        'title': search,
                        'entries':entries,
                        'context':converted_page,
                        "form":Search()
                    }
                    return render(request, "encyclopedia/entry.html", dicts)
                elif search.upper() in i.upper():
                    searched.append(i)
                    context= {
                        'searched': searched,
                        'entries':entries,
                        'form': Search()
                    }
            return render(request, "encyclopedia/search.html", context)
        else:
            return render(request, "encyclopedia/index.html", {
            "entries": entries,
            "form":Search()
        })

    else:
        return render(request, "encyclopedia/index.html", {
            "entries": entries,
            "form":Search()
        })

def new_entry(request):
    formm = New_entry()
    search = Search()
    
    entries = util.list_entries()
    if request.method == 'POST':
        formm = New_entry(request.POST)
        if formm.is_valid():
            title = formm.cleaned_data["title"]
            textarea = formm.cleaned_data["textarea"]
            if title in entries:
                return render(request, "encyclopedia/error.html", {"message":"page already exists, please add another topic !!!"})
            else:
                util.save_entry(title, textarea)
                page = util.get_entry(title)
                markdown_page = markdowner.convert(page)
                dicts = {
                    'form':Search(),
                    'context':markdown_page,
                    'title': title,
                    'entries':entries,
                }
                return render(request, "encyclopedia/entry.html", dicts)
    else:
        return render(request, "encyclopedia/new_entry.html", {"formm":formm, "form":search})


def wiki_title(request, title):
    entries = util.list_entries()
    entries_context = util.get_entry(title)
    markdowner = Markdown()
    if title in entries:
        page = util.get_entry
        dicts = {
            'page': page,
            'title': title,
            'entries':entries,
            'context':markdowner.convert(entries_context),
            "form":Search()
        }
        return render(request, "encyclopedia/entry.html", dicts)
    else:
        return render(request, "encyclopedia/error.html", {"message":"page not found please try another title !"})


def wiki_title_edit(request, title):
    if request.method == 'GET':
        entries = util.list_entries()
        entries_context = util.get_entry(title)
        context = markdowner.convert(entries_context)
        dicts = {
            'title': title,
            'entries':entries,
            'context':markdowner.convert(entries_context),
            "edit": New_entry(initial={'textarea':entries_context, 'title':title}),
            "form":Search(),
        }
        return render(request, "encyclopedia/edit.html", dicts)
    else:
        form = New_entry(request.POST)
        if form.is_valid():
            textarea = form.cleaned_data["textarea"]
            title = form.cleaned_data["title"]
            util.save_entry(title, textarea)
            page = util.get_entry(title)
            markdower_page = markdowner.convert(page)
            entries = util.list_entries()
            dicts={
                'form':Search(),
                'context':markdower_page,
                'title':title,
                'entries':entries,
            }
            return render(request, "encyclopedia/entry.html", dicts)

def randomPage(request):
    entries = util.list_entries()
    randomEntry = secrets.choice(entries)
    print = (randomEntry)
    return HttpResponseRedirect(reverse("wiki_title", kwargs={'title': randomEntry}))

# def randomPage(request):
#     if request.method == 'GET':
#         entries = util.list_entries()
#         num = random.randint(0, len(entries) - 1)
#         page_random = entries[num]
#         page = util.get_entry(page_random)
#         page_converted = markdowner.convert(page)

#         context = {
#             'form': Search(),
#             'page': page_converted,
#             'title': page_random
#         }

#         return render(request, "encyclopedia/entry.html", context)




