from django.contrib import admin

from core.models import Profile, Post, Comment, Reaction, Follower

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reaction)
admin.site.register(Follower)
