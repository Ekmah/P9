from django import forms
from litreview.models import Ticket, Review, UserFollows
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class AskCriticForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ("title", "description", "image")
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control', 'maxlength': '128'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'maxlength': '2048'}),
            'image': forms.FileInput(
                attrs={'class': 'form-control'})
        }
        labels = {'title': 'Titre du livre', 'description': 'Description',
                  'image': 'Image'}


class AnswerCriticForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("headline", "rating", "body")
        widgets = {
            'headline': forms.TextInput(
                attrs={'class': 'form-control', 'maxlength': '128'}),
            'rating': forms.RadioSelect(
                attrs={'class': 'inline'}
            ),
            'body': forms.Textarea(
                attrs={'class': 'form-control', 'maxlength': '8192'}),
        }
        labels = {'headline': 'Titre', 'rating': 'Note', 'body': 'Commentaire'}
