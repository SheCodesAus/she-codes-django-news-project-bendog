from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.StoryView.as_view(), name="story"),
    path('<int:pk>/like', views.like_post, name="like"),
    path("add-story/", views.AddStoryView.as_view(), name='newStory'),
]
