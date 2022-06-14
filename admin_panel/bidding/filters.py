import django_filters
from django.contrib.admin.models import LogEntry
from django_filters import DateFilter
from apis.bidding_and_transection.models import Bidding, NftTransaction
from accounts.models import User
from django import forms
from apis.nft_management.models import Nft


class BiddingFilter(django_filters.FilterSet):
    nft = django_filters.ModelChoiceFilter(queryset=Nft.objects.all(),
                                           widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))
    offer_by = django_filters.ModelChoiceFilter(queryset=User.objects.all(),
                                                widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))
    price = django_filters.NumberFilter(field_name='price',
                                       widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm'}))

    class Meta:
        model = Bidding
        fields = ['price', 'offer_by', 'nft']


class BiddingTransactionFilter(django_filters.FilterSet):
    user = django_filters.ModelChoiceFilter(queryset=User.objects.all(),
                                             widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))


    class Meta:
        model = User
        fields = ['user']
