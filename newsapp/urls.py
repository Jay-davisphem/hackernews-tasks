from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("page/<int:page>/", views.listing, name="listing"),
    path("stories/<int:pk>/comments", views.story_comments, name="comments"),
]
