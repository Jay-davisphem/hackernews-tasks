from django.shortcuts import render

from .models import AllStories

def home(request):
    all_stories = AllStories.objects.exclude(type__in=("pollopt", "comment"))
    return render(request, "home.html", {"show_show": all_stories})
