from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

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
    template_name = 'news/story.html' # default: news/newsstory_detail.html
    context_object_name = 'story' # default: newsstory
    

class AddStoryView(generic.CreateView):
    form_class = StoryForm
    template_name = 'news/newsstory_form.html'
    success_url = reverse_lazy('news:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class StoryEditView(LoginRequiredMixin, generic.UpdateView):
    model = NewsStory
    fields = ['title', 'pub_date', 'content']
    
    def get_success_url(self) -> str:
        return reverse_lazy('news:story', kwargs={"pk":self.kwargs['pk']})

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(author=self.request.user)


class StoryDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = NewsStory
    success_url = reverse_lazy('news:index')
    
    def get_queryset(self):
        """ filter to only allow delete of own stories """
        qs = super().get_queryset()
        return qs.filter(author=self.request.user)
        
    