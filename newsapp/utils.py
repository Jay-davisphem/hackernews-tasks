import datetime as dt
import os

import requests
from django.utils.timezone import make_aware

from .models import AllStories, Comment, Job, Poll, PollOption, Story

news_base_detail_url = "https://hacker-news.firebaseio.com/v0/item/"
top_news_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
show_news_url = "https://hacker-news.firebaseio.com/v0/showstories.json"
ask_news_url = "https://hacker-news.firebaseio.com/v0/askstories.json"
job_news_url = "https://hacker-news.firebaseio.com/v0/jobstories.json"


def fetch_news(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()


def get_results_keys(news_detail):
    type = news_detail.get("type")
    obj_id = str(news_detail.get("id"))
    by = news_detail.get("by")
    secs = news_detail.get("time")
    time = make_aware(dt.datetime.fromtimestamp(secs))
    url = news_detail.get("url")
    title = news_detail.get("title")
    text = news_detail.get("text")
    score = news_detail.get("score", 0)
    kids = list(reversed(sorted(news_detail.get("kids", []))))
    parent = news_detail.get("parent")
    parts = news_detail.get("parts", [])  # pollopt
    vals = {
        "type": type,
        "obj_id": obj_id,
        "by": by,
        "time": time,
        "url": url,
        "title": title,
        "text": text,
        "score": score,
        "fetched": True,
    }
    return vals, (kids, parent, parts)


def fetch_children(type, kids, par, obj, sm_n=5, gch=False):
    if not kids:
        return

    for com_id in kids:
        print(
            f"{obj._meta.model_name} parent_id",
            par.id,
            "child",
            com_id,
            end="...",
        )
        sing_com = fetch_news(f"{news_base_detail_url}{com_id}.json")
        com_lte = get_results_keys(sing_com)
        real_com = com_lte[0]
        s_type = real_com["type"]
        s_kids = com_lte[-1][0]
        s_par = None
        if type == "story":
            s_par = obj.objects.create(**real_com, story_id=par.id)
        else:
            s_par = obj.objects.create(**real_com, poll_id=par.id)
        print(f"{obj._meta.model_name} created successfully")
        fetch_children(s_type, s_kids, s_par, obj, sm_n=2, gch=True)
        if gch:
            print("Grandchildren bossman")
    print()


def save_to_db(news_ids, num=100):
    news_ids = list(reversed(sorted(news_ids)))[:num]
    if news_ids:
        exists = AllStories.objects.filter(obj_id=news_ids[0]).exists()
        if exists:
            return
    else:
        return
    news_dict = {
        "job": Job,
        "poll": Poll,
        "story": Story,
    }
    for i in news_ids:
        news_detail = fetch_news(f"{news_base_detail_url}{i}.json")
        ite = get_results_keys(news_detail)
        news_vals = ite[0]
        kids = ite[-1][0]
        parts = ite[-1][-1]
        type = news_vals["type"]
        try:
            par = news_dict.get(type).objects.create(**news_vals)
            if kids and type in ("story", "poll"):
                fetch_children(type, kids, par, Comment)
            if parts and type == "poll":
                fetch_children(type, parts, par, PollOption)
        except Exception as e:
            print(e, "failed to fetch")
            pass
    return None


def scheduled_tasks1():
    print("Task started")
    news_ids = (fetch_news(top_news_url) + fetch_news(show_news_url) +
                fetch_news(job_news_url) + fetch_news(ask_news_url))
    print(f'len(news_id) = {len(news_ids)}')
    news_ids = set(news_ids)
    print(f'after len(news_id) = {len(news_ids)}')
    save_to_db(news_ids)
    print("Task ran")


def test_tasks():
    print("Tasks running Halleluyahhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
