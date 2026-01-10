from django.urls import path, include
from rest_framework import routers

from core.views import (
    ProfileViewSet,
    FollowerViewSet,
    PostViewSet,
    CommentViewSet,
    ReactionViewSet,
    SchedulePostView,
)


router = routers.DefaultRouter()
router.register("profile", ProfileViewSet)
router.register("follower", FollowerViewSet)
router.register("post", PostViewSet)
router.register("comment", CommentViewSet)
router.register("reaction", ReactionViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("posts/schedule/", SchedulePostView.as_view()),
]
