from django import forms
from settings.models import SiteSetting, SocialSetting, PercentageSetting


class SiteForm(forms.ModelForm):
    class Meta:
        model = SiteSetting
        fields = '__all__'
        exclude = ('code',)
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'nft@example.com','pattern':"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$",'title':'Enter Valid Email Address','style': 'width:300px; margin-left:300px'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+923004455666','pattern':"[0-9]{3}-[0-9]{3}-[0-9]{4}",'title':'Enter Valid Phone Number','style': 'width:300px; margin-left:300px'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+923004455666','style': 'width:300px; margin-left:300px'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'street','style': 'width:300px; margin-left:300px'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'description','style': 'width:300px; margin-left:300px'}),
            'mailgun_domain': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'mailgun_domain','style': 'width:300px; margin-left:300px'}),
            'mailgun_Api_Key': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'mailgun_Api_Key','style': 'width:300px; margin-left:300px'}),
        }


class SocialForm(forms.ModelForm):
    class Meta:
        model = SocialSetting
        fields = '__all__'
        exclude = ('code',)
        widgets = {
            'discord': forms.TextInput(attrs={'class': 'form-control', 'type': 'url', 'placeholder': 'example.com','pattern':"https?://.+",'size':'3000','title':'Please Enter Valid Url','style': 'width:300px; margin-left:300px' }),
            'twitter': forms.TextInput(attrs={'class': 'form-control', 'type': 'url', 'placeholder': 'example.com','pattern':"https?://.+",'size':'3000','title':'Please Enter Valid Url' ,'style': 'width:300px; margin-left:300px'}),
            'youTube': forms.TextInput(attrs={'class': 'form-control', 'type': 'url', 'placeholder': 'example.com','pattern':"https?://.+",'size':'3000','title':'Please Enter Valid Url','style': 'width:300px; margin-left:300px' }),
            'instagram': forms.TextInput(attrs={'class': 'form-control', 'type': 'url', 'placeholder': 'example.com','pattern':"https?://.+",'size':'3000','title':'Please Enter Valid Url','style': 'width:300px; margin-left:300px' }),
            'medium': forms.TextInput(attrs={'class': 'form-control', 'type': 'url', 'placeholder': 'example.com','pattern':"https?://.+",'size':'3000','title':'Please Enter Valid Url' ,'style': 'width:300px; margin-left:300px'}),
            'telegram': forms.TextInput(attrs={'class': 'form-control', 'type': 'url', 'placeholder': 'example.com','pattern':"https?://.+",'size':'3000','title':'Please Enter Valid Url','style': 'width:300px; margin-left:300px' }),
            'reddit': forms.TextInput(attrs={'class': 'form-control', 'type': 'url', 'placeholder': 'example.com','pattern':"https?://.+",'size':'3000','title':'Please Enter Valid Url','style': 'width:300px; margin-left:300px' }),
            'github': forms.TextInput(attrs={'class': 'form-control', 'type': 'url', 'placeholder': 'example.com','pattern':"https?://.+",'size':'3000','title':'Please Enter Valid Url' ,'style': 'width:300px; margin-left:300px'}),

        }


class PercentageForm(forms.ModelForm):
    class Meta:
        model = PercentageSetting
        fields = '__all__'
        exclude = ('code',)

        widgets = {
            'royalty': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number','pattern':"[0-9]+" ,'title':"please enter number only",'style': 'width:300px; margin-left:300px'}),
            'platform_share': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number','pattern':"[0-9]+" ,'title':"please enter number only",'style': 'width:300px; margin-left:300px'})
        }
