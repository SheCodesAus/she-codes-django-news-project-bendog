from django.contrib.auth import get_user_model
from django.db import models

USER = get_user_model()

class NewsStory(models.Model):
    title = models.CharField(max_length=200)
    # author = models.CharField(max_length=200)
    author = models.ForeignKey(
        USER, on_delete=models.CASCADE
    )
    pub_date = models.DateTimeField()
    content = models.TextField()


class Comment(models.Model):
    story = models.ForeignKey(NewsStory, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(
        USER, related_name="comments" ,on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    