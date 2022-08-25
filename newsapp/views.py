from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

from .models import AllStories


def paginate(all_stories, page):
    paginator = Paginator(all_stories, 5)
    page_obj = paginator.get_page(page)
    page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page)
    return page_obj


def _listing(request, page=1):
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
    page_obj = paginate(all_stories, page)
    return render(request, "home.html", {"page_obj": page_obj})


def home(request):
    return _listing(request)


def listing(request, page):
    return _listing(request, page)
