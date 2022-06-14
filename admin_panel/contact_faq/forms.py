from django import forms
from django_summernote.widgets import SummernoteWidget

from apis.admin_site_management.models import FAQ
from django.core.exceptions import ValidationError


class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['title', 'description']
        widgets = {
            'description': SummernoteWidget(),
            'title': forms.TextInput(attrs={'class': 'form-control','pattern':'[-_\.a-zA-Z,!? ]*$' ,'title':" please enter characters only"})
        }

