import django_filters
from django.forms import TextInput, Select
from apis.admin_site_management.models import Contact,FAQ
from django_filters import CharFilter
from accounts.models import User


class ContactFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains',
                      widget=TextInput(attrs={'class': 'form-control form-control-sm'}))
    resolved_by = django_filters.ModelChoiceFilter(queryset=User.objects.all(),
                                                widget=Select(attrs={'class': 'form-control form-control-sm'}))
    class Meta:
        model = Contact
        fields =['name', 'resolved_by']


class FAQFilter(django_filters.FilterSet):
    title = CharFilter(field_name='title', lookup_expr='icontains',
                      widget=TextInput(attrs={'class': 'form-control form-control-sm'}))

    class Meta:
        model = FAQ
        fields = ['title']