from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"allstories", views.AllStoriesViewSet, basename="allstories")
router.register(r"comments", views.CommentViewSet, basename="comments")
router.register(r"polloptions", views.PollOptionViewSet, basename="polloptions")
urlpatterns = [
    path("", include(router.urls)),
]
