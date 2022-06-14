from accounts.models import User, Profile
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.forms import ModelForm, ImageField


class UserForm(ModelForm):
    """
    UserForm class

    This From used to make form of User

    Parameters
    ----------
    ModelForm : django.forms

    """

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}),
                   'first_name': forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder': 'Enter description here'}),
                   'last_name': forms.TextInput(attrs={'class': 'form-control'}),
                   }


class ProfileForm(ModelForm):
    """
    ProfileForm class

    This From used to make form of Profile

    Parameters
    ----------
    ModelForm : django.forms

    """

    class Meta:
        model = Profile
        fields = '__all__'


class ChangePass(PasswordChangeForm):
    old_password = forms.CharField(label='Current Password',
                                   widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label=' Confirm Password',
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['__all__']


class UpdateProfileForm(ModelForm):
    profile_image = ImageField(label='Profile_Image', widget=forms.FileInput)
    banner_image = ImageField(label='Banner_Image', widget=forms.FileInput)

    class Meta:
        model = Profile
        fields = ['profile_image', 'banner_image', 'google_plus_link', 'vine_link', 'facebook_link', 'twitter_link']

        widgets = {
            'google_plus_link': forms.TextInput(attrs={'class': 'form-control','pattern':"https?://.+",'size':'3000','title':'Please Enter Valid Url','style': 'width:300px; margin-left:300px'}),
            'vine_link': forms.TextInput(attrs={'class': 'form-control','pattern':"https?://.+",'size':'3000','title':' Please Enter Valid Url','style': 'width:300px; margin-left:300px' }),
            'facebook_link': forms.TextInput(attrs={'class': 'form-control','pattern':"https?://.+",'size':'3000','title':'Please Enter Valid Url' ,'style': 'width:300px; margin-left:300px'}),
            'twitter_link': forms.TextInput(attrs={'class': 'form-control','pattern':"https?://.+",'size':'3000','title':'Please Enter Valid Url' ,'style': 'width:300px; margin-left:300px'}),

        }




