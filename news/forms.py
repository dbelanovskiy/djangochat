from .models import Articles
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea

class AriclesForm(ModelForm):
    class Meta:
        model = Articles
        fields = ['title', 'anons', 'full_text', 'date']
        widgets = {
            "title": TextInput(attrs={
                'class': 'w-full mt-2 px-4 py-2 rounded-xl bg-gray-300',
                'placeholder':'Название статьи'
            }),
            "anons": TextInput(attrs={
                'class': 'w-full mt-2 px-4 py-2 rounded-xl bg-gray-300',
                'placeholder': 'Анонс статьи'
            }),
            "date": DateTimeInput(attrs={
                'class': 'w-full mt-2 px-4 py-2 rounded-xl bg-gray-300',
                'placeholder': 'Дата публикации'
            }),
            "full_text": Textarea(attrs={
                'class': 'w-full mt-2 px-4 py-2 rounded-xl bg-gray-300',
                'placeholder': 'Текст статьи'
            }),
        }