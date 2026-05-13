from django.db.models import Q, Count
from django.utils.timezone import now
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Profile, Follower, Post, Comment, Reaction
from core.permissions import IsAuthorOrReadOnly
from core.serializers import (
    ProfileSerializer,
    FollowerSerializer,
    PostSerializer,
    CommentSerializer,
    ReactionSerializer,
    ProfileRetrieveSerializer,
    ProfileListSerializer,
    ScheduledPostSerializer,
)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        queryset = self.queryset
        if self.action in ("list", "retrieve"):
            return queryset.select_related("user")
        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProfileRetrieveSerializer
        elif self.action == "list":
            return ProfileListSerializer

        return ProfileSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FollowerViewSet(viewsets.ModelViewSet):
    queryset = Follower.objects.select_related(
        "user", "user__user", "user_to_follow", "user_to_follow__user"
    )
    serializer_class = FollowerSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related("author", "author__user").annotate(
        likes_count=Count(
            "reactions",
            filter=Q(reactions__type="like"),
        ),
        dislikes_count=Count(
            "reactions",
            filter=Q(reactions__type="dislike"),
        ),
        comments_count=Count("comments"),
    )
    serializer_class = PostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related("author", "author__user", "post")
    serializer_class = CommentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ReactionViewSet(viewsets.ModelViewSet):
    queryset = Reaction.objects.select_related("author", "author__user", "post")
    serializer_class = ReactionSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class SchedulePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, create_post_task=None):
        serializer = ScheduledPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        scheduled_time = serializer.validated_data["scheduled_time"]
        content = serializer.validated_data["content"]

        if scheduled_time <= now():
            return Response(
                {"error": "scheduled_time must be in the future"}, status=400
            )

        create_post_task.apply_async(
            args=[request.user.id, content], eta=scheduled_time
        )

        return Response({"message": "Post scheduled successfully"}, status=201)
