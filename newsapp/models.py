from django.db import models


class AllStories(models.Model):
    base_type = "all"
    obj_id = models.CharField(max_length=255, default=None, null=True)
    fetched = models.BooleanField(default=False)
    type = models.CharField(max_length=100)
    by = models.CharField(max_length=100, null=True)
    time = models.DateTimeField(editable=True, auto_now_add=True)  # creation date
    url = models.URLField(max_length=500, null=True)
    title = models.CharField(max_length=200, null=True)
    text = models.TextField(null=True)
    score = models.BigIntegerField(default=0, null=True)

    class Meta:
        verbose_name = "All Story"
        verbose_name_plural = "All Stories"
        ordering = ['-time', 'title']

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = self.base_type
        super().save(*args, **kwargs)

    @classmethod
    def _check_model(cls):
        return []

    def __str__(self):
        return f"{self.type} | All stories {self.id}"


class JobQuerySet(models.QuerySet):
    def job(self):
        return self.filter(type="job")


class JobManager(models.Manager):
    def get_queryset(self):
        return JobQuerySet(self.model, using=self._db).job()


class Job(AllStories):
    base_type = "job"
    objects = JobManager()

    class Meta:
        proxy = True

    def __str__(self):
        return f"Job {self.by} -{self.id}"


class StoryQuerySet(models.QuerySet):
    def story(self):
        return self.filter(type="story")


class StoryManager(models.Manager):
    def get_queryset(self):
        return StoryQuerySet(self.model, using=self._db).story()


class Story(AllStories):
    # kids(list of comm)
    # descendants count in views
    base_type = "story"
    objects = StoryManager()

    class Meta:
        ordering = ['-time', 'title']
        proxy = True
        verbose_name = "Story"
        verbose_name_plural = "Stories"

    def __str__(self):
        return f"Story {self.by} {self.id}"


class PollQuerySet(models.QuerySet):
    def poll(self):
        return self.filter(type="poll")


class PollManager(models.Manager):
    def get_queryset(self):
        return PollQuerySet(self.model, using=self._db).poll()


class Poll(AllStories):
    base_type = "poll"
    objects = PollManager()

    # kids and parts(list of related poll opts)
    # descendants count in views
    class Meta:
        proxy = True
        ordering = ['-time', 'title']

    def __str__(self):
        return f"Poll {self.by} - {self.id}"


class Comment(AllStories):
    base_type = "comment"
    kids = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="comment_comments", null=True
    )
    story = models.ForeignKey(
        Story, on_delete=models.CASCADE, related_name="story_comments", null=True
    )
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='poll_comments', null=True)
    def __str__(self):
        return f"Comment {self.by} - {self.id}"


class PollOption(AllStories):
    base_type = "pollopt"
    poll = models.ForeignKey(
        Poll, on_delete=models.CASCADE, related_name="poll_polloptions"
    )

    def __str__(self):
        return f"PollOption {self.by} - {self.id}"
