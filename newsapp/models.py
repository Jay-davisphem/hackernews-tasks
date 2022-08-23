from django.db import models


class AllStories(models.Model):
    base_type = "all"
    type = models.CharField(max_length=100)
    by = models.CharField(max_length=100)
    time = models.DateTimeField(editable=True)  # creation date
    url = models.CharField(max_length=500)
    title = models.CharField(max_length=200)
    text = models.TextField()
    score = models.BigIntegerField(default=0)

    class Meta:
        verbose_name = "All Story"
        verbose_name_plural = "All Stories"

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

    def __str__(self):
        return f"Poll {self.by} - {self.id}"


class Comment(AllStories):
    base_type = "comment"
    kids = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="comment_comments"
    )
    parent = models.ForeignKey(
        Story, on_delete=models.CASCADE, related_name="comments_story"
    )

    def __str__(self):
        return f"Comment {self.by} - {self.id}"


class PollOption(AllStories):
    base_type = "pollopt"
    parent = models.ForeignKey(
        Poll, on_delete=models.CASCADE, related_name="polloptions_poll"
    )

    def __str__(self):
        return f"PollOption {self.by} - {self.id}"
