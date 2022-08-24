from django.contrib import admin

from .models import AllStories, Comment, Job, Poll, PollOption, Story


class CommentInline(admin.TabularInline):
    model = Comment
    fields = ["text", "by"]


class Comment1Inline(CommentInline):
    fk_name = "kids"


class Comment2Inline(CommentInline):
    fk_name = "story"


class PollOptionInline(admin.TabularInline):
    model = PollOption
    fk_name = "poll"
    fields = ["text", "by", "score"]


class Comment3Inline(CommentInline):
    fk_name = "poll"


class CommentAdmin(admin.ModelAdmin):
    inlines = [Comment1Inline]
    fields = ["text", "by"]


class StoryAdmin(admin.ModelAdmin):
    inlines = [Comment2Inline]
    fields = ["title", "text", "by", "url", "score"]


class PollAdmin(admin.ModelAdmin):
    inlines = [Comment3Inline, PollOptionInline]
    fields = ["title", "text", "by", "url", "score"]


admin.site.register(Job)
admin.site.register(Story, StoryAdmin)
admin.site.register(Poll, PollAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(PollOption)
admin.site.register(AllStories)
