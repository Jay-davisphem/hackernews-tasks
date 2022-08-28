from django.db.models import Q
from django.shortcuts import get_object_or_404
from newsapp.models import AllStories, Comment, Job, Poll, PollOption, Story
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (AllStoriesSerializers, CommentSerielizers,
                          PollOptionSerializers)


def deletion(cls, pk, request):
    obj = get_object_or_404(cls, pk=pk)
    if obj.fetched:
        return Response(
            "Deletions of fetched item not allowed",
            status=status.HTTP_403_FORBIDDEN,
        )
    obj.delete()
    return Response("Deleted successfully")


def updown(cls, clss, pk, request):
    obj = get_object_or_404(cls, pk=pk)
    if obj.fetched:
        return Response(
            "Update of fetched item not allowed",
            status=status.HTTP_403_FORBIDDEN,
        )
    ser = clss(data=request.data)
    if ser.is_valid(raise_exception=True):
        ser.save()
        return Response(ser.data)


class AllStoriesViewSet(viewsets.ModelViewSet):
    queryset = AllStories.objects.exclude(type__in=("comment", "pollopt"))
    serializer_class = AllStoriesSerializers

    def list(self, request):
        type = request.GET.get("type")
        text = request.GET.get("text")
        fetched = request.GET.get("fetched")
        _fetch = fetched
        fetched = True if fetched == 'True' else False
        print(type, text, fetched)
        qs = None
        if _fetch == None:
            qs = self.queryset
        else:
            qs = self.queryset.filter(fetched=fetched)
        if type and text:
            qs = qs.filter(text__icontains=text.lower(), type=type.lower())
        else:
            if type:
                qs = qs.filter(type=type.lower())
            if text:
                qs = qs.filter(text__icontains=text.lower())

        page = self.paginate_queryset(qs)
        if page:
            data = AllStoriesSerializers(page, many=True).data
            return self.get_paginated_response(data)
        data = AllStoriesSerializers(qs, many=True).data
        return Response(data)

    def create(self, request):
        ser = AllStoriesSerializers(data=request.data)
        stor = {"job": Job, "story": Story, "poll": Poll}
        data = dict(request.data)
        if ser.is_valid(raise_exception=True):
            type = ser.data.get("type")
            score = int(data["score"][0])
            text = data["text"][0]
            by = data["by"][0]
            url = data["url"][0]
            del data["csrfmiddlewaretoken"]
            del data["score"]
            del data["text"]
            del data["by"]
            del data["url"]
            sobj = stor[type].objects.create(
                **data, score=score, url=url, text=text, by=by
            )
            sobj.obj_id = sobj.id
            sobj.save()
            return Response("Successfully created", status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        return deletion(AllStories, pk, request)

    def update(self, request, pk=None):
        return updown(AllStories, AllStoriesSerializers, pk, request)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerielizers

    def destroy(self, request, pk=None):
        return deletion(Comment, pk, request)

    def update(self, request, pk=None):
        return updown(Comment, CommentSerielizers, pk, request)


class PollOptionViewSet(viewsets.ModelViewSet):
    queryset = PollOption.objects.all()
    serializer_class = PollOptionSerializers

    def destroy(self, request, pk=None):
        return deletion(PollOption, pk, request)

    def update(self, request, pk=None):
        return updown(PollOption, PollOptionSerializers, pk, request)
