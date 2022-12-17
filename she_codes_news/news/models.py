from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class NewsStory(models.Model):
    title = models.CharField(max_length=200)
    # author = models.CharField(max_length=200)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    pub_date = models.DateTimeField()
    content = models.TextField()
    favourited_by = models.ManyToManyField(
        User, related_name="favourites", blank=True
    )