from job.models import Application
from django import forms

from .models import InternshipApplication

class InternshipApplicationForm(forms.ModelForm):
    class Meta:
        model = InternshipApplication
        fields = ['cover_letter', 'resume']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'resume': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

from django import forms
from .models import Internship

class InternshipPostForm(forms.ModelForm):
    class Meta:
        model = Internship
        fields = ['title', 'company', 'description', 'duration', 'location', 'image', 'pdf']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'duration': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'pdf': forms.FileInput(attrs={'class': 'form-control-file'}),
        }
