from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views import generic
from django.urls import reverse_lazy
from .models import NewsStory
from .forms import StoryForm, FilterForm

User = get_user_model()
class IndexView(generic.ListView):
    template_name = 'news/index.html'
    context_object_name = 'all_stories'

    def get_queryset(self):
        '''Return all news stories.'''
        qs = NewsStory.objects.all()
        form = FilterForm(self.request.GET)
        order_by = "-pub_date"
        if form.is_valid():
            order = form.cleaned_data.get('order')
            if order == "oldfirst":
                order_by = "pub_date"
                

            if author := form.cleaned_data.get('author'):
                qs = qs.filter(author=author)

            if search := form.cleaned_data.get('search'):
                qs = qs.filter(Q(title__icontains=search) | Q(content__icontains=search))


        return qs.order_by(order_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['latest_stories'] = NewsStory.objects.all()[:4]
        context['form'] = FilterForm(self.request.GET)
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
    