from django.urls import path, include


from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("new_entry", views.new_entry, name="new_entry"),
    path("wiki/<str:title>", views.wiki_title, name="wiki_title"),
    path("edit/<str:title>", views.wiki_title_edit, name="wiki_title_edit"),
    path("wiki/", views.randomPage, name="random"),
    # path("wiki", include("wiki.urls"))
]
