from django import forms
from .models import Service

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'category', 'icon', 'description', 'price', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_icon(self):
        icon = self.cleaned_data['icon']
        # Remove 'fa-' prefix if included
        return icon.replace('fa-', '') if icon else icon 