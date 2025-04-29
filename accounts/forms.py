from django import forms
from .models import UserProfile

class RoleUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['role']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-control'}),
        }
