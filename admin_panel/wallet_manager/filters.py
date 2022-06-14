import django_filters
from apis.wallet_management.models import Wallet, WalletTransaction
from django_filters import CharFilter
from django import forms
from accounts.models import User
from django.forms import TextInput


class WalletFilter(django_filters.FilterSet):
    user = django_filters.ModelChoiceFilter(queryset=User.objects.all(), widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))
    wallet_address = CharFilter(field_name='wallet_address', lookup_expr='icontains', widget=TextInput(attrs={'class': 'form-control form-control-sm'}))
    is_verified = CharFilter(field_name='is_verified', lookup_expr='icontains',widget=TextInput(attrs={'class': 'form-control form-control-sm'}))
    is_active = CharFilter(field_name='is_active',lookup_expr='icontains',
                             widget=TextInput(attrs={'class': 'form-control form-control-sm'}))
    class Meta:
        model = Wallet
        fields = ['user', 'wallet_address', 'is_verified', 'is_active', 'is_removed']



class WalletTransactionFilter(django_filters.FilterSet):

    wallet = django_filters.ModelChoiceFilter(queryset=Wallet.objects.all(),
                                            widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))
    transaction_type = CharFilter(field_name='transaction_type', lookup_expr='icontains', widget=TextInput(attrs={'class': 'form-control form-control-sm'}))
    amount = django_filters.NumberFilter(field_name='amount', widget=forms.NumberInput(attrs={'class': 'form-control form-control-'}))


    class Meta:
        model = WalletTransaction
        fields = ['transaction_type', 'amount', 'wallet']