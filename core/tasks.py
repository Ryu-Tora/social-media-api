from django.contrib.auth import get_user_model

from core.models import Post
from celery import shared_task


@shared_task
def create_post_task(user_id, content):
    user = get_user_model().objects.get(id=user_id)
    Post.objects.create(user=user, content=content)
