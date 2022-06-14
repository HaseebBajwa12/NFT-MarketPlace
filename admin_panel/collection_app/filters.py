from apis.nft_management.models import Collection, Category, FavouriteNft, ReportedNft, NftPriceHistory, Nft
from django_filters import FilterSet, CharFilter
import django_filters
from accounts.models import User
from django import forms

import django_filters
from apis.nft_management.models import Nft

from django.forms import TextInput, Select, NumberInput


class CollectionFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains',
                      widget=TextInput(attrs={'class': 'form-control form-control-sm'}))
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all(),
                                                widget=Select(attrs={'class': 'form-control form-control-sm'}))
    user = django_filters.ModelChoiceFilter(queryset=User.objects.all(),
                                            widget=Select(attrs={'class': 'form-control form-control-sm'}))

    class Meta:
        model = Collection
        fields = ['name', 'category', 'user']


class CategoryFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains',
                      widget=TextInput(attrs={'class': 'form-control form-control-sm'}))

    class Meta:
        model = Category
        fields = ['name']


class FavouriteNftFilter(FilterSet):
    user = django_filters.ModelChoiceFilter(queryset=User.objects.all(),
                                            widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))
    nft = django_filters.ModelChoiceFilter(queryset=FavouriteNft.objects.all(),
                                           widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))


    class Meta:
        model = FavouriteNft
        fields = ['user', 'nft']


class ReportedNftFilter(FilterSet):
    reporter = django_filters.ModelChoiceFilter(queryset=User.objects.all(),
                                                widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))
    nft = django_filters.ModelChoiceFilter(queryset=ReportedNft.objects.all(),
                                           widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))
    report_type = CharFilter(field_name='report_type', lookup_expr='icontains',
                             widget=TextInput(attrs={'class': 'form-control form-control-sm'}))


    class Meta:
        model = ReportedNft
        fields = ['nft', 'reporter', 'report_type']


class nphFilter(FilterSet):
    nft = django_filters.ModelChoiceFilter(field_name='nft', queryset=NftPriceHistory.objects.all(),
                                             widget=Select(attrs={'class': 'form-control form-control-sm'}))
    price = django_filters.NumberFilter(field_name='price', lookup_expr='icontains',
                                        widget=NumberInput(attrs={'class': 'form-control form-control-sm'}))

    class Meta:
        model = NftPriceHistory
        fields = ['nft', 'price']


class nftFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains',
                      widget=TextInput(attrs={'class': 'form-control form-control-sm'}))
    collection = django_filters.ModelChoiceFilter(queryset=Collection.objects.all(),
                                                  widget=Select(attrs={'class': 'form-control form-control-sm'}))
    owner = django_filters.ModelChoiceFilter(queryset=User.objects.all(),
                                             widget=Select(attrs={'class': 'form-control form-control-sm'}))
    price = django_filters.NumberFilter(field_name='price', lookup_expr='icontains',
                                        widget=NumberInput(attrs={'class': 'form-control form-control-sm'}))

    class Meta:
        model = Nft
        fields = ['name', 'owner', 'collection', 'price']
