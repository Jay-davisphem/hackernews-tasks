from django.db.models import Q
from django.shortcuts import render

from .models import AllStories


def home(request):
    type_q = request.GET.get("type")
    search_q = request.GET.get("search")
    print(search_q)
    type_q = type_q.lower() if type_q else ""
    search_q = search_q.lower() if search_q else ""
    q1 = Q(type=type_q)
    q2 = Q(text__icontains=search_q) | Q(title__icontains=search_q)

    q3 = q1 | q2

    all_stories = AllStories.objects.exclude(type__in=("pollopt", "comment"))

    if type_q and search_q:
        all_stories = all_stories.filter(q3)
    elif type_q:
        all_stories = all_stories.filter(q1)
    elif search_q:
        all_stories = all_stories.filter(q2)
    else:
        pass
    return render(request, "home.html", {"show_show": all_stories})
