from newsapp.models import AllStories, Comment, Poll, PollOption, Story
from rest_framework import serializers


class AllStoriesSerializers(serializers.ModelSerializer):
    time = serializers.CharField(read_only=True)

    class Meta:
        model = AllStories
        fields = [
            "id",
            "title",
            "text",
            "score",
            "fetched",
            "type",
            "by",
            "title",
            "url",
            "time",
        ]


class CommentSerielizers(serializers.ModelSerializer):
    time = serializers.CharField(read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "text",
            "story_id",
            "poll_id",
            "kids",
            "by",
            "time",
            "comment_comments",
        ]


class PollOptionSerializers(serializers.ModelSerializer):
    time = serializers.CharField(read_only=True)

    class Meta:
        model = PollOption
        fields = ["id", "by", "url", "title", "text", "poll_id", "time"]
