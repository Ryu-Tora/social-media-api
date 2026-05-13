from rest_framework import serializers

from core.models import Profile, Follower, Post, Comment, Reaction


class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)

    class Meta:
        model = Profile
        fields = (
            "id",
            "first_name",
            "last_name",
            "bio",
            "birth_date",
            "profile_pic",
        )


class ProfileRetrieveSerializer(ProfileSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")

    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "first_name",
            "last_name",
            "email",
            "bio",
            "birth_date",
            "profile_pic",
        )

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user")

        user = instance.user
        user.first_name = user_data.get("first_name", user.first_name)
        user.last_name = user_data.get("last_name", user.last_name)
        user.save()

        return instance


class ProfileListSerializer(ProfileSerializer):
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)

    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "first_name",
            "last_name",
            "profile_pic",
        )


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ("id", "user", "user_to_follow")


class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)
    dislikes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "content",
            "created_at",
            "image",
            "scheduled_date",
            "likes_count",
            "dislikes_count",
            "comments_count",
        )
        read_only_fields = ("id", "author", "created_at")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "author", "post", "content", "created_at")


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ("id", "author", "post", "type", "created_at")


class ScheduledPostSerializer(serializers.Serializer):
    content = serializers.CharField()
    scheduled_time = serializers.DateTimeField()
