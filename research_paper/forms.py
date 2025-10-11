from django import forms
from .models import ResearchPaper

class ResearchPaperPostForm(forms.ModelForm):
    class Meta:
        model = ResearchPaper
        fields = ['title', 'authors', 'abstract', 'pdf', 'thumbnail']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'authors': forms.TextInput(attrs={'class': 'form-control'}),
            'abstract': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'pdf': forms.FileInput(attrs={'class': 'form-control-file'}),
            'thumbnail': forms.FileInput(attrs={'class': 'form-control-file'}),
        }