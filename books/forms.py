from django import forms
from .models import Book, Thread

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'reading_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = '__all__'
        widgets = {
            'reading_date': forms.DateInput(attrs={'type': 'date'}),
        }
