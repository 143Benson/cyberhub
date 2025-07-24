from django import forms
from .models import ConversionTask

class ConversionTaskForm(forms.ModelForm):
    class Meta:
        model = ConversionTask
        fields = ['uploaded_file', 'conversion_type']
        widgets = {
            'conversion_type': forms.Select(attrs={'class': 'form-control'}),
            'uploaded_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

