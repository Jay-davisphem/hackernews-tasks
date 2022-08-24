import datetime as dt
import os

import requests

from .models import Comment, Job, Poll, PollOption, Story

top_news_url = os.getenv("top_news_url")
news_base_detail_url = os.getenv("news_base_detail_url")


def fetch_news(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()


def get_results_keys(news_detail):
    type = news_detail.get("type")
    obj_id = str(news_detail.get("id"))
    by = news_detail.get("by")
    secs = news_detail.get("time")
    time = dt.datetime.utcfromtimestamp(secs) if secs else ""
    url = news_detail.get("url")
    title = news_detail.get("title")
    text = news_detail.get("text")
    score = news_detail.get("score", 0)
    kids = news_detail.get("kids", [])
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


def save_to_db(news_ids, num=10):
    news_ids = sorted(news_ids)[::num]  # latest top (num) news_ids
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
                for com_id in kids[:5]:
                    print("parent_id", par.id, "child", com_id, end="...")
                    sing_com = fetch_news(f"{news_base_detail_url}{com_id}.json")
                    com_lte = get_results_keys(sing_com)
                    real_com = com_lte[0]
                    if type == "story":
                        com_res = Comment.objects.create(**real_com, story_id=par.id)
                    else:
                        com_res = Comment.objects.create(**real_com, poll_id=par.id)
                    print("Comment created successfully")

                print()

            if parts and type == "poll":
                for opt_id in parts:
                    print("parent_poll_id", par.id, "option", opt_id, end="...")
                    sing_opt = fetch_news(f"{news_base_detail_url}{opt_id}.json")
                    poll_lte = get_results_keys(sing_opt)
                    real_opt = com_lte[0]
                    opt_res = PollOption.objects.create(**real_opt, poll_id=par.id)
                    print("Poll Option created successfully")
                print()

        except Exception as e:
            print(e, "failed to fetch")
            pass
    return None
