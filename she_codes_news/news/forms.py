from django import forms 
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from .models import NewsStory

User = get_user_model()

class StoryForm(ModelForm):
    class Meta:
        model = NewsStory
        fields = ['title', 'pub_date', 'content']
        widgets = {
            'pub_date': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        }


class SearchForm(forms.Form):
    with_author = forms.ModelChoiceField(
        label='Author', queryset=User.objects.all(), required=False
        )
    search = forms.CharField(label="Search", required=False)