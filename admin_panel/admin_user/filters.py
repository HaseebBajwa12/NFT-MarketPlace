import django_filters
from django import forms
from django.forms import TextInput
from django_filters import DateFilter, CharFilter, filters
from accounts.models import User, Profile


class UserFilter(django_filters.FilterSet):

    username=CharFilter(field_name='username',lookup_expr='icontains',widget=TextInput(attrs={'placeholder': 'Username'}))
    email = CharFilter(field_name='email', lookup_expr='icontains',widget=TextInput(attrs={'placeholder': 'Email'}))
    first_name = CharFilter(field_name='first_name', lookup_expr='icontains',widget=TextInput(attrs={'placeholder': 'First_name'}))
    last_name = CharFilter(field_name='last_name', lookup_expr='icontains',
                            widget=TextInput(attrs={'placeholder': 'Last_name','class':'color'}))

    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']


class ProfileFilter(django_filters.FilterSet):
    class Meta:
        model = Profile
        fields = ['user']
