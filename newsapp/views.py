from django.core.paginator import EmptyPage, Paginator
from django.db.models import Q
from django.shortcuts import redirect, render

from .models import AllStories, Comment, Job, Poll, Story


def paginate(all_stories, page, num=20):
    paginator = Paginator(all_stories, num)
    page_obj = paginator.get_page(page)
    page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page)
    return page_obj


def _listing(request, page=1):
    type_q = request.GET.get("type")
    search_q = request.GET.get("search")
    type_q = type_q.lower() if type_q else ""
    search_q = search_q.lower() if search_q else ""
    q1 = Q(type=type_q)
    q2 = Q(text__icontains=search_q) | Q(title__icontains=search_q)

    q3 = q1 | q2
    all_stories = AllStories.objects.exclude(type__in=("pollopt", "comment"))
    past = request.GET.get("past")
    if past == "past":
        all_stories = all_stories.order_by("id")
    if type_q and search_q:
        all_stories = all_stories.filter(q3)
    elif type_q:
        all_stories = all_stories.filter(q1)
    elif search_q:
        all_stories = all_stories.filter(q2)
    else:
        pass
    page_obj = paginate(all_stories, page)
    try:
        return render(request, "home.html", {"page_obj": page_obj})
    except:
        return redirect("home")


def home(request):
    return _listing(request)


def listing(request, page):
    return _listing(request, page)


def story_comments(request, pk):
    obj = AllStories.objects.get(pk=pk)
    dic = {"job": Job, "story": Story, "poll": Poll}
    type = obj.type
    comments = {}
    if type == "story":
        comments = Comment.objects.filter(story__id=pk)
    elif type == "poll":
        comments = Comment.objects.filter(poll_id=pk)
    return render(request, "comments.html", {"comments": comments, "i": obj})
