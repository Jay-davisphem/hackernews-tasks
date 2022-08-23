from django.contrib import admin
from .models import Job, Story, Poll, Comment, PollOption, AllStories

admin.site.register(Job)
admin.site.register(Story)
admin.site.register(Poll)
admin.site.register(Comment)
admin.site.register(PollOption)
admin.site.register(AllStories)
