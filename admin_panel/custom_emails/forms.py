from django import forms
from django_summernote.widgets import SummernoteWidget
from admin_panel.custom_emails.models import EmailTemplate


class EmailTemplateForm(forms.ModelForm):

    class Meta:
        model = EmailTemplate
        fields = ['subject', 'body']

        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control input-lg','pattern':'[A-Za-z ]+', 'title':'please enter alphabets only '}),
            'body': SummernoteWidget()
        }

