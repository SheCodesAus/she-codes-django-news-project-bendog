from django.contrib.auth.decorators import login_required
from django.views import generic
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import NewsStory
from .forms import StoryForm

class IndexView(generic.ListView):
    template_name = 'news/index.html'

    def get_queryset(self):
        '''Return all news stories.'''
        return NewsStory.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_stories'] = NewsStory.objects.all()[:4]
        context['all_stories'] = NewsStory.objects.all()
        return context

class StoryView(generic.DetailView):
    model = NewsStory
    template_name = 'news/story.html'
    context_object_name = 'story'
    

class AddStoryView(generic.CreateView):
    form_class = StoryForm
    context_object_name = 'storyForm'
    template_name = 'news/createStory.html'
    success_url = reverse_lazy('news:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

@login_required
def like_post(request, pk):
    story = get_object_or_404(NewsStory, pk=pk)
    user = request.user
    if story.liked_by.filter(id=user.id).exists():
        story.liked_by.remove(user)
    else:
        story.liked_by.all(user)
    return redirect('news:story', pk=story.id)

