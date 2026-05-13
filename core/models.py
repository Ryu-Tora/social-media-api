from django.conf import settings
from django.db import models
from rest_framework.exceptions import ValidationError


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    bio = models.TextField()
    birth_date = models.DateField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to="profile_images", blank=True, null=True)

    class Meta:
        ordering = ["user__first_name", "user__last_name"]

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Follower(models.Model):
    user = models.ForeignKey(Profile, related_name="follower", on_delete=models.CASCADE)
    user_to_follow = models.ForeignKey(
        Profile, related_name="followed", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("user", "user_to_follow")
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["user_to_follow"]),
        ]

    def __str__(self):
        return (
            f"{self.user.user.first_name} follows {self.user_to_follow.user.first_name}"
        )

    def validate(self, attrs):
        if attrs["user"] == self.user_to_follow:
            raise ValidationError("You cannot follow yourself.")
        return attrs


class Post(models.Model):
    author = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="posts",
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="post_images", blank=True)
    scheduled_date = models.DateTimeField(blank=True, null=True, default=None)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Post created by {self.author} at {self.created_at}"


class Comment(models.Model):
    author = models.ForeignKey(
        Profile, related_name="comments", on_delete=models.CASCADE
    )
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Reaction(models.Model):
    LIKE = "like"
    DISLIKE = "dislike"
    TYPE_CHOICES = [
        (LIKE, "Like"),
        (DISLIKE, "Dislike"),
    ]
    author = models.ForeignKey(
        Profile, related_name="reactions", on_delete=models.CASCADE
    )
    post = models.ForeignKey(Post, related_name="reactions", on_delete=models.CASCADE)
    type = models.CharField(choices=TYPE_CHOICES, max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("author", "post")
        indexes = [
            models.Index(fields=["author"]),
            models.Index(fields=["post"]),
        ]
