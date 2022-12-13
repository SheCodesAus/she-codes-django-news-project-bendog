from django.contrib.auth import get_user_model
from django.db.models import Q
from django.views import generic
from django.urls import reverse_lazy
from .models import NewsStory
from .forms import StoryForm, SearchForm


User = get_user_model()

class IndexView(generic.ListView):
    template_name = 'news/index.html'
    context_object_name = 'all_stories'

    def get_queryset(self):
        '''Return all news stories.'''
        qs = NewsStory.objects.all()
        form = SearchForm(self.request.GET)
        if form.is_valid():
            if author := form.cleaned_data.get('with_author'):
                qs = qs.filter(author=author)
            if search_text := form.cleaned_data.get('search'):
                qs = qs.filter(
                    Q(title__icontains=search_text) | 
                    Q(content__icontains=search_text)
                    )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_stories'] = NewsStory.objects.all()[:4]
        context['author_list'] = User.objects.all()
        context['form'] = SearchForm(self.request.GET)
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
    